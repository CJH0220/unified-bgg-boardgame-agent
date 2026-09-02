"""Export the expanded Phase 10 retrieval suite for validation and reuse."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from retrieval_suite_expanded import EXPANDED_RETRIEVAL_SUITE
from unified_retrieval import UnifiedSearchConfig, search_unified

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
RAW_INDEX = ROOT / "raw_index"
DOCS = ROOT / "docs"
OUTPUT = RAW_INDEX / "retrieval_suite_expanded.jsonl"
SUMMARY = RAW_INDEX / "retrieval_suite_expanded_summary.json"
REPORT = DOCS / "retrieval_suite_expanded_report.md"


def result_score(row: dict[str, Any]) -> float | None:
    for key in ("fusion_score", "score", "raw_vector_score", "vector_score"):
        value = row.get(key)
        if value is not None:
            return float(value)
    return None


def expected_hit(top_ids: list[str], expected_any: list[str]) -> bool:
    return bool(expected_any) and any(
        any(fragment in doc_id for fragment in expected_any)
        for doc_id in top_ids
    )


def run(engine: str, limit: int, candidate_limit: int) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    passed = 0
    validated = 0
    per_doc_type: dict[str, dict[str, int]] = {}
    failed_records: list[dict[str, Any]] = []

    for spec in EXPANDED_RETRIEVAL_SUITE:
        config = UnifiedSearchConfig(
            engine=spec.get("engine", engine),
            limit=limit,
            candidate_limit=candidate_limit,
            doc_type=spec.get("doc_type"),
        )
        result = search_unified(spec["query"], config)
        top_ids = [row.get("doc_id") or "" for row in result["results"][:limit]]
        expected_any = spec.get("expected_any") or []
        hit = expected_hit(top_ids, expected_any)
        if expected_any:
            validated += 1
            if hit:
                passed += 1

        doc_type = spec.get("doc_type") or "unknown"
        bucket = per_doc_type.setdefault(doc_type, {"count": 0, "validated": 0, "passed": 0})
        bucket["count"] += 1
        if expected_any:
            bucket["validated"] += 1
            if hit:
                bucket["passed"] += 1

        record = {
            "query_id": spec["query_id"],
            "query": spec["query"],
            "doc_type_filter": spec.get("doc_type"),
            "expected_any": expected_any,
            "passed": hit if expected_any else None,
            "engine": result["engine"],
            "limit": limit,
            "candidate_limit": candidate_limit,
            "generated_at": result["generated_at"],
            "entity_route": result.get("entity_route"),
            "expanded_query": result.get("expanded_query"),
            "results": result["results"],
        }
        records.append(record)
        if expected_any and not hit:
            failed_records.append(record)

    summary = {
        "generated_at": datetime.now().replace(microsecond=0).isoformat(),
        "engine": engine,
        "limit": limit,
        "candidate_limit": candidate_limit,
        "suite_size": len(EXPANDED_RETRIEVAL_SUITE),
        "validated_queries": validated,
        "passed": passed,
        "failed": validated - passed,
        "pass_rate": round(passed / validated, 4) if validated else None,
        "per_doc_type": per_doc_type,
        "failed_query_ids": [record["query_id"] for record in failed_records],
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
        "# Phase 10 Expanded Retrieval Suite Report",
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
        f"| Failed | {summary['failed']} |",
        f"| Pass rate | {summary['pass_rate']} |",
        f"| Engine | `{summary['engine']}` |",
        f"| Limit | {summary['limit']} |",
        f"| Candidate limit | {summary['candidate_limit']} |",
        "",
        "## Per Doc Type",
        "",
        "| Doc type | Count | Validated | Passed | Pass rate |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for key, value in sorted(summary["per_doc_type"].items()):
        rate = round(value["passed"] / value["validated"], 4) if value["validated"] else None
        lines.append(f"| `{key}` | {value['count']} | {value['validated']} | {value['passed']} | {rate} |")

    if summary["failed_query_ids"]:
        lines.extend(["", "## Failed Queries", ""])
        for record in summary["records"]:
            if record["query_id"] not in summary["failed_query_ids"]:
                continue
            top_ids = ", ".join(row.get("doc_id") or "" for row in record["results"][: summary["limit"]])
            lines.append(f"- `{record['query_id']}` `{record['query']}` expected `{', '.join(record['expected_any'])}`; got `{top_ids}`")

    lines.extend(["", "## Query Results", ""])
    for record in summary["records"]:
        status = "PASS" if record.get("passed") else "FAIL" if record.get("passed") is False else "INFO"
        lines.append(f"### {status}: `{record['query_id']}` - `{record['query']}`")
        lines.append("")
        if record.get("expected_any"):
            lines.append(f"- Expected: `{', '.join(record['expected_any'])}`")
        if record.get("entity_route"):
            lines.append(f"- Entity route: `{record['entity_route']}`")
        lines.append("")
        lines.append("| Rank | Score | Doc type | Title | Doc ID |")
        lines.append("| ---: | ---: | --- | --- | --- |")
        for row in record["results"][: summary["limit"]]:
            score = result_score(row)
            title = (row.get("title") or "").replace("|", "\\|")
            lines.append(
                f"| {row.get('rank')} | {score} | `{row.get('doc_type')}` | {title} | `{row.get('doc_id')}` |"
            )
        lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export expanded Phase 10 retrieval suite runs.")
    parser.add_argument("--engine", choices=["auto", "fts", "vector", "hybrid"], default="hybrid")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--candidate-limit", type=int, default=50)
    args = parser.parse_args()
    summary = run(args.engine, args.limit, args.candidate_limit)
    write_outputs(summary)
    printable = {key: value for key, value in summary.items() if key != "records"}
    print(json.dumps(printable, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
