"""Evaluate Phase 8 hybrid retrieval with English and Chinese smoke queries."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from query_hybrid_index import hybrid_search
from retrieval_common import configure_utf8_stdout

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
RAW_INDEX = ROOT / "raw_index"
DOCS = ROOT / "docs"
OUTPUT = RAW_INDEX / "hybrid_retrieval_summary.json"
REPORT = DOCS / "hybrid_retrieval_report.md"

QUERIES = [
    {
        "query": "卡坦岛 交易 评论",
        "doc_type": "review_digest",
        "expected_any": ["reviews:bgg:13"],
    },
    {
        "query": "卡坦岛 游戏简介",
        "doc_type": "game_overview",
        "expected_any": ["game:bgg:13"],
    },
    {
        "query": "幽港迷城 合作 战役",
        "doc_type": "game_overview",
        "expected_any": ["game:bgg:174430"],
    },
    {
        "query": "卡卡颂 拼放版图 评论",
        "doc_type": "review_digest",
        "expected_any": ["reviews:bgg:822"],
    },
    {
        "query": "牌库构筑 机制",
        "doc_type": "mechanic_profile",
        "expected_any": ["mechanic:deck,-bag,-and-pool-building"],
    },
    {
        "query": "工人放置 机制",
        "doc_type": "mechanic_profile",
        "expected_any": ["mechanic:worker-placement:profile"],
    },
    {
        "query": "Brass Birmingham economic network route building",
        "doc_type": "game_overview",
        "expected_any": ["game:bgg:224517"],
    },
    {
        "query": "Catan trading negotiation user comments",
        "doc_type": "review_digest",
        "expected_any": ["reviews:bgg:13"],
    },
    {
        "query": "Gloomhaven cooperative campaign fantasy",
        "doc_type": "game_overview",
        "expected_any": ["game:bgg:174430"],
    },
]


def is_hit(results: list[dict[str, Any]], expected_any: list[str], top_k: int) -> bool:
    for row in results[:top_k]:
        doc_id = row.get("doc_id") or ""
        if any(fragment in doc_id for fragment in expected_any):
            return True
    return False


def compact(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "rank": row.get("rank"),
        "fusion_score": round(row.get("fusion_score") or 0.0, 6),
        "fts_rank": row.get("fts_rank"),
        "vector_rank": row.get("vector_rank"),
        "vector_score": round(row.get("vector_score") or 0.0, 6) if row.get("vector_score") is not None else None,
        "doc_id": row.get("doc_id"),
        "doc_type": row.get("doc_type"),
        "title": row.get("title"),
        "game_id": row.get("game_id"),
        "bgg_id": row.get("bgg_id"),
        "source_file": row.get("source_file"),
    }


def run(top_k: int, candidate_limit: int) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    passed = 0
    for spec in QUERIES:
        retrieved = hybrid_search(
            spec["query"],
            top_k,
            doc_type=spec.get("doc_type"),
            candidate_limit=candidate_limit,
        )
        hit = is_hit(retrieved, spec["expected_any"], top_k)
        if hit:
            passed += 1
        results.append(
            {
                "query": spec["query"],
                "doc_type_filter": spec.get("doc_type"),
                "expected_any": spec["expected_any"],
                "passed": hit,
                "top_results": [compact(row) for row in retrieved],
            }
        )
    return {
        "generated_at": datetime.now().replace(microsecond=0).isoformat(),
        "top_k": top_k,
        "candidate_limit": candidate_limit,
        "passed": passed,
        "total": len(QUERIES),
        "pass_rate": round(passed / len(QUERIES), 4),
        "results": results,
    }


def write_report(summary: dict[str, Any]) -> None:
    lines = [
        "# Hybrid Retrieval Report",
        "",
        f"Generated at: `{summary['generated_at']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Passed queries | {summary['passed']} / {summary['total']} |",
        f"| Pass rate | {summary['pass_rate']} |",
        f"| Top K | {summary['top_k']} |",
        f"| Candidate limit | {summary['candidate_limit']} |",
        "",
        "## Method",
        "",
        "- FTS layer: existing SQLite FTS5/BM25 index at `final/rag_index.sqlite`.",
        "- Vector layer: local sparse TF-IDF inverted index at `final/rag_vector_index.sqlite`.",
        "- Chinese queries are expanded with a small auditable dictionary before retrieval.",
        "- Fusion uses reciprocal rank fusion and records `fts_rank`, `vector_rank`, `vector_score`, and `fusion_score`.",
        "",
        "## Query Results",
        "",
    ]
    for item in summary["results"]:
        status = "PASS" if item["passed"] else "FAIL"
        lines.extend(
            [
                f"### {status}: `{item['query']}`",
                "",
                f"- Doc type filter: `{item['doc_type_filter']}`",
                f"- Expected: `{', '.join(item['expected_any'])}`",
                "",
                "| Rank | Fusion | FTS rank | Vector rank | Vector score | Title | Doc ID |",
                "| ---: | ---: | ---: | ---: | ---: | --- | --- |",
            ]
        )
        for row in item["top_results"]:
            title = (row.get("title") or "").replace("|", "\\|")
            lines.append(
                f"| {row['rank']} | {row['fusion_score']} | {row.get('fts_rank')} | "
                f"{row.get('vector_rank')} | {row.get('vector_score')} | {title} | `{row.get('doc_id')}` |"
            )
        lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    configure_utf8_stdout()
    parser = argparse.ArgumentParser(description="Evaluate Phase 8 hybrid retrieval.")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--candidate-limit", type=int, default=50)
    args = parser.parse_args()
    RAW_INDEX.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    summary = run(args.top_k, args.candidate_limit)
    OUTPUT.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_report(summary)
    print(json.dumps(summary, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
