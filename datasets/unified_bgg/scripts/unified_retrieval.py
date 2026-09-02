"""Unified retrieval entry points for the unified_bgg project."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import query_hybrid_index
import query_rag_index
import query_vector_index
from retrieval_common import configure_utf8_stdout, detect_game_route, expand_query, query_terms

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
FTS_INDEX = ROOT / "final" / "rag_index.sqlite"
VECTOR_INDEX = ROOT / "final" / "rag_vector_index.sqlite"


@dataclass(frozen=True)
class UnifiedSearchConfig:
    engine: str = "hybrid"
    limit: int = 5
    candidate_limit: int = 50
    doc_type: str | None = None
    game_id: str | None = None
    bgg_id: int | None = None
    fts_index: Path = FTS_INDEX
    vector_index: Path = VECTOR_INDEX


def _search_fts(query: str, config: UnifiedSearchConfig) -> list[dict[str, Any]]:
    return query_rag_index.search(
        config.fts_index,
        expand_query(query),
        config.limit,
        config.doc_type,
        config.game_id,
        config.bgg_id,
    )


def _search_vector(query: str, config: UnifiedSearchConfig) -> list[dict[str, Any]]:
    return query_vector_index.search(
        config.vector_index,
        query,
        config.limit,
        config.doc_type,
        config.game_id,
        config.bgg_id,
        config.candidate_limit,
    )


def _search_hybrid(query: str, config: UnifiedSearchConfig) -> list[dict[str, Any]]:
    return query_hybrid_index.hybrid_search(
        query,
        config.limit,
        config.doc_type,
        config.game_id,
        config.bgg_id,
        config.fts_index,
        config.vector_index,
        config.candidate_limit,
    )


def _first_score(row: dict[str, Any]) -> float | None:
    for key in ("fusion_score", "score", "raw_vector_score", "vector_score"):
        value = row.get(key)
        if value is not None:
            return float(value)
    return None


def normalize_results(rows: list[dict[str, Any]], engine: str) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        rank = row.get("rank") or index
        score = _first_score(row)
        normalized.append(
            {
                "rank": rank,
                "score": score,
                "doc_id": row.get("doc_id"),
                "doc_type": row.get("doc_type"),
                "title": row.get("title"),
                "game_id": row.get("game_id"),
                "bgg_id": row.get("bgg_id"),
                "year_published": row.get("year_published"),
                "source_file": row.get("source_file"),
                "text_preview": row.get("text_preview"),
                "fts_rank": row.get("fts_rank") if engine != "fts" else rank,
                "fts_score": row.get("fts_score") if row.get("fts_score") is not None else (score if engine == "fts" else None),
                "vector_rank": row.get("vector_rank") if engine != "vector" else rank,
                "vector_score": row.get("vector_score") if row.get("vector_score") is not None else (score if engine == "vector" else None),
                "raw_vector_score": row.get("raw_vector_score"),
                "fusion_score": row.get("fusion_score"),
                "entity_route_boost": row.get("entity_route_boost") or row.get("vector_entity_route_boost"),
            }
        )
    return normalized


def search_unified(query: str, config: UnifiedSearchConfig) -> dict[str, Any]:
    configure_utf8_stdout()
    engine = (config.engine or "hybrid").lower()
    if engine == "auto":
        engine = "hybrid"

    if engine == "fts":
        results = _search_fts(query, config)
    elif engine == "vector":
        results = _search_vector(query, config)
    elif engine == "hybrid":
        results = _search_hybrid(query, config)
    else:
        raise ValueError(f"Unsupported engine: {config.engine}")

    expanded_query = expand_query(query)
    route = detect_game_route(query)
    return {
        "generated_at": datetime.now().replace(microsecond=0).isoformat(),
        "query": query,
        "expanded_query": expanded_query,
        "engine": engine,
        "limit": config.limit,
        "candidate_limit": config.candidate_limit,
        "doc_type_filter": config.doc_type,
        "game_id_filter": config.game_id,
        "bgg_id_filter": config.bgg_id,
        "entity_route": route,
        "query_tokens": dict(query_terms(query)),
        "results": normalize_results(results, engine),
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Unified Retrieval Report",
        "",
        f"- Query: `{result['query']}`",
        f"- Engine: `{result['engine']}`",
        f"- Doc type filter: `{result.get('doc_type_filter')}`",
        f"- Game ID filter: `{result.get('game_id_filter')}`",
        f"- BGG ID filter: `{result.get('bgg_id_filter')}`",
        f"- Expanded query: `{result['expanded_query']}`",
        "",
        "## Top Results",
        "",
        "| Rank | Score | Doc type | Title | Doc ID | Game ID | BGG ID |",
        "| ---: | ---: | --- | --- | --- | --- | ---: |",
    ]
    for row in result["results"]:
        score = row.get("fusion_score")
        if score is None:
            score = row.get("score")
        if score is None:
            score = row.get("raw_vector_score")
        title = (row.get("title") or "").replace("|", "\\|")
        lines.append(
            f"| {row.get('rank')} | {score} | `{row.get('doc_type')}` | {title} | "
            f"`{row.get('doc_id')}` | `{row.get('game_id')}` | {row.get('bgg_id')} |"
        )
    return "\n".join(lines) + "\n"
