"""Query the local unified_bgg sparse TF-IDF vector index."""
from __future__ import annotations

import argparse
import json
import math
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any

from retrieval_common import configure_utf8_stdout, detect_game_route, expand_query, query_terms

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
INDEX = ROOT / "final" / "rag_vector_index.sqlite"


def build_query_vector(con: sqlite3.Connection, query: str) -> tuple[str, dict[int, float], dict[str, Any]]:
    expanded = expand_query(query)
    counts = query_terms(query)
    if not counts:
        raise SystemExit("Query must contain at least one searchable token after expansion.")

    placeholders = ",".join("?" for _ in counts)
    rows = con.execute(
        f"SELECT term_id, term, df, idf FROM terms WHERE term IN ({placeholders})",
        list(counts.keys()),
    ).fetchall()
    weighted: dict[int, float] = {}
    matched_terms: list[dict[str, Any]] = []
    for row in rows:
        weight = (1.0 + math.log(counts[row["term"]])) * row["idf"]
        weighted[row["term_id"]] = weight
        matched_terms.append({"term": row["term"], "df": row["df"], "idf": row["idf"]})
    norm = math.sqrt(sum(weight * weight for weight in weighted.values()))
    if norm > 0:
        weighted = {term_id: weight / norm for term_id, weight in weighted.items()}
    meta = {
        "expanded_query": expanded,
        "tokens": dict(counts),
        "matched_terms": matched_terms,
    }
    return expanded, weighted, meta


def search(
    index: Path,
    query: str,
    limit: int,
    doc_type: str | None = None,
    game_id: str | None = None,
    bgg_id: int | None = None,
    candidate_limit: int = 200,
) -> list[dict[str, Any]]:
    con = sqlite3.connect(index)
    con.row_factory = sqlite3.Row
    try:
        _, qvec, meta = build_query_vector(con, query)
        if not qvec:
            return []
        route = detect_game_route(query)
        meta["entity_route"] = route

        scores: defaultdict[int, float] = defaultdict(float)
        route_boosts: defaultdict[int, float] = defaultdict(float)
        filters = []
        filter_params: list[Any] = []
        if doc_type:
            filters.append("docs.doc_type = ?")
            filter_params.append(doc_type)
        if game_id:
            filters.append("docs.game_id = ?")
            filter_params.append(game_id)
        if bgg_id is not None:
            filters.append("docs.bgg_id = ?")
            filter_params.append(bgg_id)
        filter_sql = ""
        if filters:
            filter_sql = " AND " + " AND ".join(filters)

        for term_id, q_weight in qvec.items():
            rows = con.execute(
                f"""
                SELECT postings.doc_rowid, postings.weight
                FROM postings
                JOIN docs ON docs.doc_rowid = postings.doc_rowid
                WHERE postings.term_id = ?{filter_sql}
                """,
                [term_id, *filter_params],
            )
            for row in rows:
                scores[row["doc_rowid"]] += q_weight * row["weight"]

        if route and bgg_id is None and (doc_type in {None, "game_overview", "review_digest"}):
            route_filters = list(filters)
            route_params = list(filter_params)
            route_filters.append("docs.bgg_id = ?")
            route_params.append(route["bgg_id"])
            route_sql = " AND ".join(route_filters)
            for row in con.execute(f"SELECT doc_rowid FROM docs WHERE {route_sql}", route_params):
                route_boosts[row["doc_rowid"]] += 0.6

        sort_scores = {
            doc_rowid: score + route_boosts.get(doc_rowid, 0.0)
            for doc_rowid, score in scores.items()
        }
        for doc_rowid, boost in route_boosts.items():
            sort_scores.setdefault(doc_rowid, boost)
        ranked = sorted(sort_scores.items(), key=lambda item: item[1], reverse=True)[:candidate_limit]
        ranked = ranked[:limit]
        if not ranked:
            return []

        placeholders = ",".join("?" for _ in ranked)
        docs = {
            row["doc_rowid"]: row
            for row in con.execute(
                f"""
                SELECT doc_rowid, doc_id, doc_type, title, game_id, bgg_id,
                       year_published, source_file, text_preview
                FROM docs
                WHERE doc_rowid IN ({placeholders})
                """,
                [doc_rowid for doc_rowid, _ in ranked],
            )
        }
    finally:
        con.close()

    results: list[dict[str, Any]] = []
    for rank, (doc_rowid, score) in enumerate(ranked, start=1):
        row = docs[doc_rowid]
        results.append(
            {
                "rank": rank,
                "score": score,
                "raw_vector_score": scores.get(doc_rowid, 0.0),
                "entity_route_boost": route_boosts.get(doc_rowid, 0.0),
                "doc_id": row["doc_id"],
                "doc_type": row["doc_type"],
                "title": row["title"],
                "game_id": row["game_id"],
                "bgg_id": row["bgg_id"],
                "year_published": row["year_published"],
                "source_file": row["source_file"],
                "text_preview": row["text_preview"],
                "query_meta": meta,
            }
        )
    return results


def print_text(results: list[dict[str, Any]]) -> None:
    for row in results:
        print(f"{row['rank']}. {row['title']} [{row['doc_type']}] {row['doc_id']}")
        print(
            f"   score={row['score']:.6f} raw_vector={row['raw_vector_score']:.6f} game_id={row['game_id']} "
            f"bgg_id={row['bgg_id']} source={row['source_file']}"
        )
        preview = (row["text_preview"] or "").replace("\n", " ")
        print(f"   {preview[:500]}")


def main() -> None:
    configure_utf8_stdout()
    parser = argparse.ArgumentParser(description="Query local sparse TF-IDF vector index.")
    parser.add_argument("query")
    parser.add_argument("--index", default=str(INDEX))
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--candidate-limit", type=int, default=200)
    parser.add_argument("--doc-type", choices=["game_overview", "mechanic_profile", "review_digest", "rulebook_text"])
    parser.add_argument("--game-id")
    parser.add_argument("--bgg-id", type=int)
    parser.add_argument("--json", action="store_true", help="Print full JSON result list.")
    args = parser.parse_args()
    results = search(
        Path(args.index),
        args.query,
        args.limit,
        args.doc_type,
        args.game_id,
        args.bgg_id,
        args.candidate_limit,
    )
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=True))
    else:
        print_text(results)


if __name__ == "__main__":
    main()
