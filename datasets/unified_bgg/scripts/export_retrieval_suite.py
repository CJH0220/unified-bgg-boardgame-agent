"""Export curated retrieval suite runs for downstream validation and reuse."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from retrieval_suite import RETRIEVAL_SUITE
from unified_retrieval import UnifiedSearchConfig, search_unified

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
RAW_INDEX = ROOT / "raw_index"
DOCS = ROOT / "docs"
OUTPUT = RAW_INDEX / "retrieval_suite.jsonl"
SUMMARY = RAW_INDEX / "retrieval_suite_summary.json"
REPORT = DOCS / "retrieval_suite_report.md"


def run(engine: str, limit: int, candidate_limit: int) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    passed = 0
    validated = 0
    per_doc_type: dict[str, int] = {}
    for spec in RETRIEVAL_SUITE:
        config = UnifiedSearchConfig(
            engine=spec.get("engine", engine),
            limit=limit,
            candidate_limit=candidate_limit,
            doc_type=spec.get("doc_type"),
        )
        result = search_unified(spec["query"], config)
        top_ids = [row.get("doc_id") or "" for row in result["results"][:limit]]
        expected_any = spec.get("expected_any") or []
        hit = bool(expected_any) and any(any(fragment in doc_id for fragment in expected_any) for doc_id in top_ids)
        if expected_any:
            validated += 1
            if hit:
                passed += 1
        doc_type = spec.get("doc_type") or "unknown"
        per_doc_type[doc_type] = per_doc_type.get(doc_type, 0) + 1
        records.append(
            {
                "query_id": spec["query_id"],
                "query": spec["query"],
                "doc_type_filter": spec.get("doc_type"),
                "expected_any": expected_any,
                "passed": hit if expected_any else None,
                "engine": result["engine"],
                "limit": limit,
                "candidate_limit": candidate_limit,
                "generated_at": result["generated_at"],
                "results": result["results"],
            }
        )

    summary = {
        "generated_at": datetime.now().replace(microsecond=0).isoformat(),
        "engine": engine,
        "limit": limit,
        "candidate_limit": candidate_limit,
        "suite_size": len(RETRIEVAL_SUITE),
        "validated_queries": validated,
        "passed": passed,
        "pass_rate": round(passed / validated, 4) if validated else None,
        "per_doc_type": per_doc_type,
        "records": records,
    }
    return summary


def write_outputs(summary: dict[str, Any]) -> None:
    RAW_INDEX.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        for record in summary["records"]:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Retrieval Suite Report",
        "",
        f"Generated at: `{summary['generated_at']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Suite size | {summary['suite_size']} |",
        f"| Validated queries | {summary['validated_queries']} |",
        f"| Passed | {summary['passed']} |",
        f"| Pass rate | {summary['pass_rate']} |",
        f"| Engine | `{summary['engine']}` |",
        f"| Limit | {summary['limit']} |",
        f"| Candidate limit | {summary['candidate_limit']} |",
        "",
        "## Per Doc Type",
        "",
        "| Doc type | Count |",
        "| --- | ---: |",
    ]
    for key, value in sorted(summary["per_doc_type"].items()):
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Samples", ""])
    for record in summary["records"]:
        status = "PASS" if record.get("passed") else "INFO"
        lines.append(f"### {status}: `{record['query_id']}` - `{record['query']}`")
        lines.append("")
        if record.get("expected_any"):
            lines.append(f"- Expected: `{', '.join(record['expected_any'])}`")
        lines.append("")
        lines.append("| Rank | Score | Doc type | Title | Doc ID |")
        lines.append("| ---: | ---: | --- | --- | --- |")
        for row in record["results"][: summary["limit"]]:
            score = row.get("fusion_score")
            if score is None:
                score = row.get("score")
            if score is None:
                score = row.get("raw_vector_score")
            title = (row.get("title") or "").replace("|", "\\|")
            lines.append(
                f"| {row.get('rank')} | {score} | `{row.get('doc_type')}` | {title} | `{row.get('doc_id')}` |"
            )
        lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export curated retrieval suite runs.")
    parser.add_argument("--engine", choices=["auto", "fts", "vector", "hybrid"], default="hybrid")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--candidate-limit", type=int, default=50)
    args = parser.parse_args()
    summary = run(args.engine, args.limit, args.candidate_limit)
    write_outputs(summary)
    print(json.dumps(summary, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
