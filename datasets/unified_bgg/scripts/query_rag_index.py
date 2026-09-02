"""Query the local unified_bgg SQLite FTS5 RAG index."""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
INDEX = ROOT / "final" / "rag_index.sqlite"


def fts_query(text: str) -> str:
    tokens = re.findall(r"[\w]+", text.lower(), flags=re.UNICODE)
    tokens = [token for token in tokens if len(token) > 1]
    if not tokens:
        raise SystemExit("Query must contain at least one searchable token.")
    # OR keeps recall high; callers should use doc_type/game filters for routing.
    return " OR ".join(f'"{token}"' for token in tokens[:24])


def search(
    index: Path,
    query: str,
    limit: int,
    doc_type: str | None,
    game_id: str | None,
    bgg_id: int | None,
) -> list[dict[str, Any]]:
    con = sqlite3.connect(index)
    con.row_factory = sqlite3.Row
    try:
        where = ["rag_fts MATCH ?"]
        params: list[Any] = [fts_query(query)]
        if doc_type:
            where.append("docs.doc_type = ?")
            params.append(doc_type)
        if game_id:
            where.append("docs.game_id = ?")
            params.append(game_id)
        if bgg_id is not None:
            where.append("docs.bgg_id = ?")
            params.append(bgg_id)
        params.append(limit)
        sql = f"""
            SELECT
                docs.doc_id,
                docs.doc_type,
                docs.title,
                docs.game_id,
                docs.bgg_id,
                docs.year_published,
                docs.source_file,
                docs.text,
                docs.json,
                bm25(rag_fts, 5.0, 1.0) AS score
            FROM rag_fts
            JOIN docs ON docs.rowid = rag_fts.rowid
            WHERE {' AND '.join(where)}
            ORDER BY score ASC
            LIMIT ?
        """
        rows = con.execute(sql, params).fetchall()
    finally:
        con.close()
    results: list[dict[str, Any]] = []
    for row in rows:
        payload = json.loads(row["json"])
        results.append(
            {
                "score": row["score"],
                "doc_id": row["doc_id"],
                "doc_type": row["doc_type"],
                "title": row["title"],
                "game_id": row["game_id"],
                "bgg_id": row["bgg_id"],
                "year_published": row["year_published"],
                "source_file": row["source_file"],
                "text_preview": (row["text"] or "")[:500],
                "document": payload,
            }
        )
    return results


def print_text(results: list[dict[str, Any]]) -> None:
    for idx, row in enumerate(results, start=1):
        print(f"{idx}. {row['title']} [{row['doc_type']}] {row['doc_id']}")
        print(f"   score={row['score']:.6f} game_id={row['game_id']} bgg_id={row['bgg_id']} source={row['source_file']}")
        preview = (row["text_preview"] or "").replace("\n", " ")
        print(f"   {preview}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Query local SQLite FTS5 RAG index.")
    parser.add_argument("query")
    parser.add_argument("--index", default=str(INDEX))
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--doc-type", choices=["game_overview", "mechanic_profile", "review_digest", "rulebook_text"])
    parser.add_argument("--game-id")
    parser.add_argument("--bgg-id", type=int)
    parser.add_argument("--json", action="store_true", help="Print full JSON result list.")
    args = parser.parse_args()
    results = search(Path(args.index), args.query, args.limit, args.doc_type, args.game_id, args.bgg_id)
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=True))
    else:
        print_text(results)


if __name__ == "__main__":
    main()
