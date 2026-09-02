"""Build a local SQLite FTS5 index for unified_bgg RAG JSONL docs.

Outputs:
- final/rag_index.sqlite
- raw_index/rag_index_summary.json
- docs/rag_index_report.md
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
SAMPLES_RAG = ROOT / "samples" / "rag"
FINAL = ROOT / "final"
RAW_INDEX = ROOT / "raw_index"
DOCS = ROOT / "docs"

INDEX = FINAL / "rag_index.sqlite"
SUMMARY = RAW_INDEX / "rag_index_summary.json"
REPORT = DOCS / "rag_index_report.md"

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
            doc_id TEXT PRIMARY KEY,
            doc_type TEXT NOT NULL,
            title TEXT,
            game_id TEXT,
            bgg_id INTEGER,
            year_published INTEGER,
            source_file TEXT NOT NULL,
            source_datasets TEXT,
            json TEXT NOT NULL,
            text TEXT NOT NULL
        )
        """
    )
    con.execute("CREATE INDEX idx_docs_doc_type ON docs(doc_type)")
    con.execute("CREATE INDEX idx_docs_game_id ON docs(game_id)")
    con.execute("CREATE INDEX idx_docs_bgg_id ON docs(bgg_id)")
    con.execute(
        """
        CREATE VIRTUAL TABLE rag_fts USING fts5(
            title,
            text,
            doc_type UNINDEXED,
            doc_id UNINDEXED,
            game_id UNINDEXED,
            source_file UNINDEXED,
            tokenize='unicode61 remove_diacritics 2'
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


def insert_doc(con: sqlite3.Connection, row: dict[str, Any], source_file: Path) -> None:
    title = row.get("title") or row.get("mechanic") or ""
    text = row.get("text") or ""
    source_datasets = row.get("source_datasets") or []
    doc_id = row["doc_id"]
    doc_type = row["doc_type"]
    game_id = row.get("game_id")
    bgg_id = as_int(row.get("bgg_id"))
    year = as_int(row.get("year_published"))
    rel_source = source_file.relative_to(ROOT).as_posix()
    payload = json.dumps(row, ensure_ascii=False, sort_keys=True)
    cur = con.execute(
        """
        INSERT INTO docs (
            doc_id, doc_type, title, game_id, bgg_id, year_published,
            source_file, source_datasets, json, text
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            doc_id,
            doc_type,
            title,
            game_id,
            bgg_id,
            year,
            rel_source,
            ";".join(source_datasets),
            payload,
            text,
        ),
    )
    rowid = cur.lastrowid
    con.execute(
        """
        INSERT INTO rag_fts(rowid, title, text, doc_type, doc_id, game_id, source_file)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (rowid, title, text, doc_type, doc_id, game_id, rel_source),
    )


def build(files: list[Path], batch_size: int) -> dict[str, Any]:
    FINAL.mkdir(parents=True, exist_ok=True)
    RAW_INDEX.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    start = time.time()
    con = setup_db(INDEX)
    counts: Counter[str] = Counter()
    rows_by_file: Counter[str] = Counter()
    parsed_docs = 0
    duplicate_errors = 0
    generated_at = datetime.now().replace(microsecond=0).isoformat()

    try:
        for path in files:
            rel = path.relative_to(ROOT).as_posix()
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    row = json.loads(line)
                    try:
                        insert_doc(con, row, path)
                    except sqlite3.IntegrityError:
                        duplicate_errors += 1
                        continue
                    parsed_docs += 1
                    rows_by_file[rel] += 1
                    counts[row.get("doc_type") or "unknown"] += 1
                    if parsed_docs % batch_size == 0:
                        con.commit()
                        print(f"indexed_docs={parsed_docs}", flush=True)
        con.commit()
        con.execute("INSERT INTO index_metadata(key, value) VALUES (?, ?)", ("generated_at", generated_at))
        con.execute("INSERT INTO index_metadata(key, value) VALUES (?, ?)", ("schema_version", "sqlite-fts5-v0.1"))
        con.execute("INSERT INTO index_metadata(key, value) VALUES (?, ?)", ("source_files", json.dumps([p.relative_to(ROOT).as_posix() for p in files])))
        con.commit()
        con.execute("INSERT INTO rag_fts(rag_fts) VALUES ('optimize')")
        con.commit()
    finally:
        con.close()

    elapsed = round(time.time() - start, 3)
    summary = {
        "generated_at": generated_at,
        "index_path": INDEX.relative_to(ROOT).as_posix(),
        "index_bytes": INDEX.stat().st_size,
        "schema_version": "sqlite-fts5-v0.1",
        "source_files": [path.relative_to(ROOT).as_posix() for path in files],
        "parsed_docs": parsed_docs,
        "duplicate_errors": duplicate_errors,
        "doc_types": dict(counts),
        "rows_by_file": dict(rows_by_file),
        "elapsed_seconds": elapsed,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_report(summary)
    return summary


def table(counter: dict[str, Any]) -> str:
    lines = ["| Item | Count |", "| --- | ---: |"]
    for key, value in sorted(counter.items(), key=lambda item: str(item[0])):
        lines.append(f"| `{key}` | {value} |")
    return "\n".join(lines)


def write_report(summary: dict[str, Any]) -> None:
    text = f"""# RAG Index Report

Generated at: `{summary['generated_at']}`

## Summary

| Metric | Value |
| --- | ---: |
| Parsed docs | {summary['parsed_docs']} |
| Duplicate errors | {summary['duplicate_errors']} |
| Index bytes | {summary['index_bytes']} |
| Elapsed seconds | {summary['elapsed_seconds']} |

## Index

- SQLite file: `final/rag_index.sqlite`
- FTS engine: SQLite FTS5
- Query script: `scripts/query_rag_index.py`

## Doc Types

{table(summary['doc_types'])}

## Rows by Source File

{table(summary['rows_by_file'])}

## Example

```powershell
python scripts/query_rag_index.py "Through the Ages civilization" --doc-type game_overview
python scripts/query_rag_index.py "deck bag pool building" --doc-type mechanic_profile
python scripts/query_rag_index.py "Catan trading negotiation comments" --doc-type review_digest
```
"""
    REPORT.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build local SQLite FTS5 RAG index.")
    parser.add_argument("--files", nargs="*", default=[str(path) for path in DEFAULT_FILES])
    parser.add_argument("--batch-size", type=int, default=5000)
    args = parser.parse_args()
    files = [Path(path) if Path(path).is_absolute() else ROOT / path for path in args.files]
    summary = build(files, args.batch_size)
    print(json.dumps(summary, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
