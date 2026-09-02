"""Unified query entry point for unified_bgg retrieval."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from unified_retrieval import FTS_INDEX, VECTOR_INDEX, UnifiedSearchConfig, render_markdown, search_unified


def main() -> None:
    parser = argparse.ArgumentParser(description="Unified query entry for unified_bgg retrieval.")
    parser.add_argument("query")
    parser.add_argument("--engine", choices=["auto", "fts", "vector", "hybrid"], default="hybrid")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--candidate-limit", type=int, default=50)
    parser.add_argument("--doc-type", choices=["game_overview", "mechanic_profile", "review_digest", "rulebook_text"])
    parser.add_argument("--game-id")
    parser.add_argument("--bgg-id", type=int)
    parser.add_argument("--fts-index", default=None)
    parser.add_argument("--vector-index", default=None)
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--markdown", action="store_true", help="Print Markdown output.")
    args = parser.parse_args()

    config = UnifiedSearchConfig(
        engine=args.engine,
        limit=args.limit,
        candidate_limit=args.candidate_limit,
        doc_type=args.doc_type,
        game_id=args.game_id,
        bgg_id=args.bgg_id,
        fts_index=Path(args.fts_index) if args.fts_index else FTS_INDEX,
        vector_index=Path(args.vector_index) if args.vector_index else VECTOR_INDEX,
    )
    result = search_unified(args.query, config)
    if args.markdown:
        print(render_markdown(result), end="")
    elif args.json:
        print(json.dumps(result, indent=2, ensure_ascii=True))
    else:
        print(render_markdown(result), end="")


if __name__ == "__main__":
    main()
