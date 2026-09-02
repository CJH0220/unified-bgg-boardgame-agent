"""Query unified_bgg with FTS5 BM25 plus sparse TF-IDF reciprocal-rank fusion."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import query_rag_index
import query_vector_index
from retrieval_common import configure_utf8_stdout, detect_game_route, expand_query

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
FTS_INDEX = ROOT / "final" / "rag_index.sqlite"
VECTOR_INDEX = ROOT / "final" / "rag_vector_index.sqlite"


def hybrid_search(
    query: str,
    limit: int,
    doc_type: str | None = None,
    game_id: str | None = None,
    bgg_id: int | None = None,
    fts_index: Path = FTS_INDEX,
    vector_index: Path = VECTOR_INDEX,
    candidate_limit: int = 50,
    rrf_k: int = 60,
) -> list[dict[str, Any]]:
    expanded = expand_query(query)
    route = detect_game_route(query)
    try:
        fts_results = query_rag_index.search(
            fts_index,
            expanded,
            candidate_limit,
            doc_type,
            game_id,
            bgg_id,
        )
    except SystemExit:
        fts_results = []
    vector_results = query_vector_index.search(
        vector_index,
        query,
        candidate_limit,
        doc_type,
        game_id,
        bgg_id,
        candidate_limit,
    )

    fused: dict[str, dict[str, Any]] = {}
    for rank, row in enumerate(fts_results, start=1):
        item = fused.setdefault(row["doc_id"], dict(row))
        item["fts_rank"] = rank
        item["fts_score"] = row["score"]
        item["fusion_score"] = item.get("fusion_score", 0.0) + 1.0 / (rrf_k + rank)
    for rank, row in enumerate(vector_results, start=1):
        item = fused.setdefault(row["doc_id"], dict(row))
        item["vector_rank"] = rank
        item["vector_score"] = row.get("raw_vector_score", row["score"])
        if row.get("entity_route_boost"):
            item["vector_entity_route_boost"] = row["entity_route_boost"]
        item["fusion_score"] = item.get("fusion_score", 0.0) + 1.0 / (rrf_k + rank)
        item.setdefault("score", row["score"])

    if route and bgg_id is None and (doc_type in {None, "game_overview", "review_digest"}):
        route_results = query_vector_index.search(
            vector_index,
            query,
            10,
            doc_type,
            game_id,
            route["bgg_id"],
            10,
        )
        for row in route_results:
            item = fused.setdefault(row["doc_id"], dict(row))
            item["entity_route"] = route
            item["entity_route_boost"] = 0.05
            item["fusion_score"] = item.get("fusion_score", 0.0) + 0.05

    ranked = sorted(
        fused.values(),
        key=lambda item: (
            item.get("fusion_score", 0.0),
            -(item.get("fts_rank") or 999999),
            -(item.get("vector_score") or 0.0),
        ),
        reverse=True,
    )[:limit]

    for rank, row in enumerate(ranked, start=1):
        row["rank"] = rank
        row["expanded_query"] = expanded
        if route:
            row.setdefault("entity_route", route)
        row.setdefault("fts_rank", None)
        row.setdefault("fts_score", None)
        row.setdefault("vector_rank", None)
        row.setdefault("vector_score", None)
    return ranked


def print_text(results: list[dict[str, Any]]) -> None:
    for row in results:
        print(f"{row['rank']}. {row['title']} [{row['doc_type']}] {row['doc_id']}")
        print(
            "   "
            f"fusion={row['fusion_score']:.6f} "
            f"fts_rank={row['fts_rank']} vector_rank={row['vector_rank']} "
            f"vector_score={row['vector_score']} bgg_id={row['bgg_id']}"
        )
        preview = (row.get("text_preview") or "").replace("\n", " ")
        print(f"   {preview[:500]}")


def main() -> None:
    configure_utf8_stdout()
    parser = argparse.ArgumentParser(description="Query local hybrid FTS + sparse TF-IDF indexes.")
    parser.add_argument("query")
    parser.add_argument("--fts-index", default=str(FTS_INDEX))
    parser.add_argument("--vector-index", default=str(VECTOR_INDEX))
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--candidate-limit", type=int, default=50)
    parser.add_argument("--rrf-k", type=int, default=60)
    parser.add_argument("--doc-type", choices=["game_overview", "mechanic_profile", "review_digest", "rulebook_text"])
    parser.add_argument("--game-id")
    parser.add_argument("--bgg-id", type=int)
    parser.add_argument("--json", action="store_true", help="Print full JSON result list.")
    args = parser.parse_args()
    results = hybrid_search(
        args.query,
        args.limit,
        args.doc_type,
        args.game_id,
        args.bgg_id,
        Path(args.fts_index),
        Path(args.vector_index),
        args.candidate_limit,
        args.rrf_k,
    )
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=True))
    else:
        print_text(results)


if __name__ == "__main__":
    main()
