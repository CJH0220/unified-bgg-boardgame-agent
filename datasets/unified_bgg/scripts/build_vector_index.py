"""Build a pure-Python TF-IDF sparse-vector index for unified_bgg RAG docs.

Outputs:
- final/rag_vector_index.sqlite
- raw_index/vector_index_summary.json
"""
from __future__ import annotations

import argparse
import json
import math
import sqlite3
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from retrieval_common import configure_utf8_stdout, weighted_doc_terms

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
SAMPLES_RAG = ROOT / "samples" / "rag"
FINAL = ROOT / "final"
RAW_INDEX = ROOT / "raw_index"

INDEX = FINAL / "rag_vector_index.sqlite"
SUMMARY = RAW_INDEX / "vector_index_summary.json"

DEFAULT_FILES = [
    SAMPLES_RAG / "game_overview.jsonl",
    SAMPLES_RAG / "mechanic_profile.jsonl",
    SAMPLES_RAG / "review_digest.jsonl",
    SAMPLES_RAG / "rulebook_text.jsonl",
]


def as_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def iter_rows(files: list[Path]) -> Iterable[tuple[Path, dict[str, Any]]]:
    for path in files:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield path, json.loads(line)


def setup_db(path: Path) -> sqlite3.Connection:
    if path.exists():
        path.unlink()
    con = sqlite3.connect(path)
    con.execute("PRAGMA journal_mode=OFF")
    con.execute("PRAGMA synchronous=OFF")
    con.execute("PRAGMA temp_store=MEMORY")
    con.execute(
        """
        CREATE TABLE docs (
            doc_rowid INTEGER PRIMARY KEY,
            doc_id TEXT NOT NULL UNIQUE,
            doc_type TEXT NOT NULL,
            title TEXT,
            game_id TEXT,
            bgg_id INTEGER,
            year_published INTEGER,
            source_file TEXT NOT NULL,
            text_preview TEXT NOT NULL
        )
        """
    )
    con.execute(
        """
        CREATE TABLE terms (
            term_id INTEGER PRIMARY KEY,
            term TEXT NOT NULL UNIQUE,
            df INTEGER NOT NULL,
            idf REAL NOT NULL
        )
        """
    )
    con.execute(
        """
        CREATE TABLE postings (
            term_id INTEGER NOT NULL,
            doc_rowid INTEGER NOT NULL,
            weight REAL NOT NULL
        )
        """
    )
    con.execute(
        """
        CREATE TABLE index_metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )
    return con


def count_document_frequency(files: list[Path], progress_every: int) -> tuple[Counter[str], Counter[str], int]:
    df: Counter[str] = Counter()
    doc_types: Counter[str] = Counter()
    parsed_docs = 0
    for _, row in iter_rows(files):
        parsed_docs += 1
        doc_types[row.get("doc_type") or "unknown"] += 1
        df.update(weighted_doc_terms(row).keys())
        if parsed_docs % progress_every == 0:
            print(f"df_pass_docs={parsed_docs} vocab_seen={len(df)}", flush=True)
    return df, doc_types, parsed_docs


def select_vocabulary(
    df: Counter[str],
    doc_count: int,
    min_df: int,
    max_df_ratio: float,
    max_vocab: int,
) -> dict[str, tuple[int, int, float]]:
    max_df = max(1, int(doc_count * max_df_ratio))
    eligible = [
        (term, freq)
        for term, freq in df.items()
        if freq >= min_df and freq <= max_df
    ]
    eligible.sort(key=lambda item: (-item[1], item[0]))
    if max_vocab > 0:
        eligible = eligible[:max_vocab]
    vocab: dict[str, tuple[int, int, float]] = {}
    for term_id, (term, freq) in enumerate(eligible, start=1):
        idf = math.log((doc_count + 1) / (freq + 1)) + 1.0
        vocab[term] = (term_id, freq, idf)
    return vocab


def flush_postings(con: sqlite3.Connection, postings: list[tuple[int, int, float]]) -> None:
    if not postings:
        return
    con.executemany(
        "INSERT INTO postings(term_id, doc_rowid, weight) VALUES (?, ?, ?)",
        postings,
    )
    postings.clear()


def build(
    files: list[Path],
    min_df: int,
    max_df_ratio: float,
    max_vocab: int,
    max_terms_per_doc: int,
    batch_size: int,
    progress_every: int,
) -> dict[str, Any]:
    FINAL.mkdir(parents=True, exist_ok=True)
    RAW_INDEX.mkdir(parents=True, exist_ok=True)
    start = time.time()
    generated_at = datetime.now().replace(microsecond=0).isoformat()

    df, doc_types, parsed_docs = count_document_frequency(files, progress_every)
    vocab = select_vocabulary(df, parsed_docs, min_df, max_df_ratio, max_vocab)
    print(f"selected_vocab={len(vocab)} from_vocab_seen={len(df)}", flush=True)

    con = setup_db(INDEX)
    postings_batch: list[tuple[int, int, float]] = []
    indexed_docs = 0
    postings_count = 0
    rows_by_file: Counter[str] = Counter()

    try:
        con.execute("BEGIN")
        con.executemany(
            "INSERT INTO terms(term_id, term, df, idf) VALUES (?, ?, ?, ?)",
            ((term_id, term, freq, idf) for term, (term_id, freq, idf) in vocab.items()),
        )

        for source_file, row in iter_rows(files):
            indexed_docs += 1
            doc_rowid = indexed_docs
            rel_source = source_file.relative_to(ROOT).as_posix()
            title = row.get("title") or row.get("mechanic") or ""
            text = row.get("text") or ""
            con.execute(
                """
                INSERT INTO docs (
                    doc_rowid, doc_id, doc_type, title, game_id, bgg_id,
                    year_published, source_file, text_preview
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    doc_rowid,
                    row["doc_id"],
                    row["doc_type"],
                    title,
                    row.get("game_id"),
                    as_int(row.get("bgg_id")),
                    as_int(row.get("year_published")),
                    rel_source,
                    text[:800],
                ),
            )
            rows_by_file[rel_source] += 1

            weighted: list[tuple[int, float]] = []
            for term, tf in weighted_doc_terms(row).items():
                info = vocab.get(term)
                if info is None:
                    continue
                term_id, _, idf = info
                weighted.append((term_id, (1.0 + math.log(tf)) * idf))
            if weighted:
                weighted.sort(key=lambda item: item[1], reverse=True)
                weighted = weighted[:max_terms_per_doc]
                norm = math.sqrt(sum(weight * weight for _, weight in weighted))
                if norm > 0:
                    for term_id, weight in weighted:
                        postings_batch.append((term_id, doc_rowid, weight / norm))
                    postings_count += len(weighted)

            if len(postings_batch) >= batch_size:
                flush_postings(con, postings_batch)
            if indexed_docs % progress_every == 0:
                flush_postings(con, postings_batch)
                con.commit()
                con.execute("BEGIN")
                print(f"vector_pass_docs={indexed_docs} postings={postings_count}", flush=True)

        flush_postings(con, postings_batch)
        for key, value in {
            "generated_at": generated_at,
            "schema_version": "sqlite-tfidf-sparse-v0.1",
            "source_files": json.dumps([p.relative_to(ROOT).as_posix() for p in files]),
            "min_df": str(min_df),
            "max_df_ratio": str(max_df_ratio),
            "max_vocab": str(max_vocab),
            "max_terms_per_doc": str(max_terms_per_doc),
        }.items():
            con.execute("INSERT INTO index_metadata(key, value) VALUES (?, ?)", (key, value))
        con.commit()

        print("creating_sqlite_indexes=true", flush=True)
        con.execute("CREATE INDEX idx_docs_doc_type ON docs(doc_type)")
        con.execute("CREATE INDEX idx_docs_game_id ON docs(game_id)")
        con.execute("CREATE INDEX idx_docs_bgg_id ON docs(bgg_id)")
        con.execute("CREATE INDEX idx_terms_term ON terms(term)")
        con.execute("CREATE INDEX idx_postings_term_id ON postings(term_id)")
        con.execute("CREATE INDEX idx_postings_doc_rowid ON postings(doc_rowid)")
        con.commit()
        con.execute("VACUUM")
    finally:
        con.close()

    elapsed = round(time.time() - start, 3)
    summary = {
        "generated_at": generated_at,
        "index_path": INDEX.relative_to(ROOT).as_posix(),
        "index_bytes": INDEX.stat().st_size,
        "schema_version": "sqlite-tfidf-sparse-v0.1",
        "source_files": [path.relative_to(ROOT).as_posix() for path in files],
        "parsed_docs": parsed_docs,
        "indexed_docs": indexed_docs,
        "doc_types": dict(doc_types),
        "rows_by_file": dict(rows_by_file),
        "vocab_seen": len(df),
        "selected_vocab": len(vocab),
        "min_df": min_df,
        "max_df_ratio": max_df_ratio,
        "max_vocab": max_vocab,
        "max_terms_per_doc": max_terms_per_doc,
        "postings": postings_count,
        "elapsed_seconds": elapsed,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    configure_utf8_stdout()
    parser = argparse.ArgumentParser(description="Build local SQLite sparse TF-IDF index.")
    parser.add_argument("--files", nargs="*", default=[str(path) for path in DEFAULT_FILES])
    parser.add_argument("--min-df", type=int, default=2)
    parser.add_argument("--max-df-ratio", type=float, default=0.35)
    parser.add_argument("--max-vocab", type=int, default=200000)
    parser.add_argument("--max-terms-per-doc", type=int, default=90)
    parser.add_argument("--batch-size", type=int, default=100000)
    parser.add_argument("--progress-every", type=int, default=10000)
    args = parser.parse_args()
    files = [Path(path) if Path(path).is_absolute() else ROOT / path for path in args.files]
    summary = build(
        files,
        args.min_df,
        args.max_df_ratio,
        args.max_vocab,
        args.max_terms_per_doc,
        args.batch_size,
        args.progress_every,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
