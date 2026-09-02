"""Evaluate generated RAG JSONL document quality for unified_bgg.

This script performs deterministic structural and text-health checks over the
current RAG outputs. It does not call any model and does not scan raw datasets.

Outputs:
- raw_index/rag_quality_summary.json
- raw_index/rag_quality_findings.jsonl
- docs/rag_quality_report.md
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import median
from typing import Any

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
SAMPLES_RAG = ROOT / "samples" / "rag"
RAW_INDEX = ROOT / "raw_index"
DOCS = ROOT / "docs"

SUMMARY = RAW_INDEX / "rag_quality_summary.json"
FINDINGS = RAW_INDEX / "rag_quality_findings.jsonl"
REPORT = DOCS / "rag_quality_report.md"

DEFAULT_FILES = [
    SAMPLES_RAG / "game_overview.jsonl",
    SAMPLES_RAG / "mechanic_profile.jsonl",
    SAMPLES_RAG / "review_digest.jsonl",
    SAMPLES_RAG / "rulebook_text.jsonl",
]


def percentile(values: list[int], pct: float) -> int | None:
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    idx = round((len(ordered) - 1) * pct)
    return ordered[idx]


def text_health_flags(text: str) -> list[str]:
    flags: list[str] = []
    if not text.strip():
        flags.append("empty_text")
    if "\ufffd" in text:
        flags.append("replacement_character")
    if "????" in text:
        flags.append("many_question_marks")
    if re.search(r"</?\s*[A-Za-z][A-Za-z0-9:-]*(?:\s+[^<>]*)?>", text):
        flags.append("html_tag_remnant")
    if len(text) < 80:
        flags.append("very_short_text")
    if len(text) > 12000:
        flags.append("very_long_text")
    return flags


def add_finding(findings: list[dict[str, Any]], row: dict[str, Any], source_file: Path, severity: str, code: str, detail: str) -> None:
    if len(findings) >= 500:
        return
    findings.append(
        {
            "severity": severity,
            "code": code,
            "detail": detail,
            "doc_id": row.get("doc_id"),
            "doc_type": row.get("doc_type"),
            "title": row.get("title") or row.get("mechanic"),
            "game_id": row.get("game_id"),
            "source_file": source_file.relative_to(ROOT).as_posix(),
        }
    )


def evaluate_row(row: dict[str, Any], source_file: Path, counters: dict[str, Counter[str]], findings: list[dict[str, Any]]) -> None:
    doc_type = row.get("doc_type") or "unknown"
    text = row.get("text") or ""
    for flag in text_health_flags(text):
        counters["text_flags"][flag] += 1
        severity = "error" if flag in {"empty_text", "replacement_character"} else "warning"
        add_finding(findings, row, source_file, severity, flag, "Text health flag detected.")

    if not row.get("doc_id"):
        counters["structural_flags"]["missing_doc_id"] += 1
        add_finding(findings, row, source_file, "error", "missing_doc_id", "Document has no doc_id.")
    if not row.get("schema_version"):
        counters["structural_flags"]["missing_schema_version"] += 1
    if not row.get("source_datasets"):
        counters["structural_flags"]["missing_source_datasets"] += 1

    if doc_type == "game_overview":
        quality_flags = row.get("quality_flags") or []
        for flag in quality_flags:
            counters["game_quality_flags"][flag] += 1
        if not row.get("title"):
            counters["game_quality_flags"]["missing_title"] += 1
        stats = row.get("stats") or {}
        if not stats.get("average_rating") and not stats.get("bayes_average"):
            counters["game_quality_flags"]["missing_rating_values"] += 1
        taxonomy = row.get("taxonomy") or {}
        if not taxonomy.get("mechanic"):
            counters["game_quality_flags"]["missing_mechanics"] += 1
        if row.get("game_type") == "boardgameexpansion":
            counters["game_quality_flags"]["expansion_doc"] += 1
    elif doc_type == "mechanic_profile":
        if not row.get("mechanic"):
            counters["mechanic_quality_flags"]["missing_mechanic"] += 1
        if not row.get("game_count"):
            counters["mechanic_quality_flags"]["zero_game_count"] += 1
        if not row.get("representative_games"):
            counters["mechanic_quality_flags"]["missing_representatives"] += 1
    elif doc_type == "review_digest":
        summary = row.get("rating_summary") or {}
        snippets = row.get("representative_snippets") or {}
        if not summary.get("comment_rows"):
            counters["review_quality_flags"]["zero_comment_rows"] += 1
        if not snippets.get("positive"):
            counters["review_quality_flags"]["missing_positive_snippets"] += 1
        if not snippets.get("mixed"):
            counters["review_quality_flags"]["missing_mixed_snippets"] += 1
        if not snippets.get("critical"):
            counters["review_quality_flags"]["missing_critical_snippets"] += 1
        if summary.get("comment_coverage_pct", 0) < 2:
            counters["review_quality_flags"]["very_low_comment_coverage"] += 1
    elif doc_type == "rulebook_text":
        source = row.get("source") or {}
        if not source.get("url"):
            counters["rulebook_quality_flags"]["missing_source_url"] += 1
        if not source.get("page_url"):
            counters["rulebook_quality_flags"]["missing_page_url"] += 1
        if not source.get("title"):
            counters["rulebook_quality_flags"]["missing_source_title"] += 1
        if not row.get("mechanics_text"):
            counters["rulebook_quality_flags"]["missing_mechanics_text"] += 1
        if not row.get("text"):
            counters["rulebook_quality_flags"]["missing_extracted_text"] += 1
        for flag in row.get("quality_flags") or []:
            counters["rulebook_quality_flags"][flag] += 1
    else:
        counters["structural_flags"]["unknown_doc_type"] += 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate RAG JSONL output quality.")
    parser.add_argument("--files", nargs="*", default=[str(path) for path in DEFAULT_FILES])
    args = parser.parse_args()

    RAW_INDEX.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    counters: dict[str, Counter[str]] = defaultdict(Counter)
    findings: list[dict[str, Any]] = []
    doc_ids: set[str] = set()
    duplicate_doc_ids: list[str] = []
    lengths_by_type: dict[str, list[int]] = defaultdict(list)
    rows_by_file: Counter[str] = Counter()
    parsed_docs = 0

    files = [Path(path) if Path(path).is_absolute() else ROOT / path for path in args.files]
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    counters["structural_flags"]["json_decode_error"] += 1
                    if len(findings) < 500:
                        findings.append(
                            {
                                "severity": "error",
                                "code": "json_decode_error",
                                "detail": f"{rel}:{line_no}: {exc}",
                                "source_file": rel,
                            }
                        )
                    continue
                parsed_docs += 1
                rows_by_file[rel] += 1
                doc_type = row.get("doc_type") or "unknown"
                counters["doc_types"][doc_type] += 1
                text = row.get("text") or ""
                lengths_by_type[doc_type].append(len(text))
                doc_id = row.get("doc_id")
                if doc_id in doc_ids:
                    duplicate_doc_ids.append(doc_id)
                    counters["structural_flags"]["duplicate_doc_id"] += 1
                    add_finding(findings, row, path, "error", "duplicate_doc_id", "Duplicate doc_id found.")
                elif doc_id:
                    doc_ids.add(doc_id)
                evaluate_row(row, path, counters, findings)

    length_summary = {}
    for doc_type, values in lengths_by_type.items():
        length_summary[doc_type] = {
            "min": min(values) if values else None,
            "median": int(median(values)) if values else None,
            "p95": percentile(values, 0.95),
            "max": max(values) if values else None,
        }

    summary = {
        "generated_at": datetime.now().replace(microsecond=0).isoformat(),
        "files": [path.relative_to(ROOT).as_posix() for path in files],
        "parsed_docs": parsed_docs,
        "unique_doc_ids": len(doc_ids),
        "duplicate_doc_ids": len(duplicate_doc_ids),
        "rows_by_file": dict(rows_by_file),
        "doc_types": dict(counters["doc_types"]),
        "text_length_summary": length_summary,
        "structural_flags": dict(counters["structural_flags"]),
        "text_flags": dict(counters["text_flags"]),
        "game_quality_flags": dict(counters["game_quality_flags"]),
        "mechanic_quality_flags": dict(counters["mechanic_quality_flags"]),
        "review_quality_flags": dict(counters["review_quality_flags"]),
        "finding_rows_written": len(findings),
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with FINDINGS.open("w", encoding="utf-8", newline="\n") as f:
        for finding in findings:
            f.write(json.dumps(finding, ensure_ascii=False, sort_keys=True) + "\n")
    write_report(summary)
    print(json.dumps(summary, indent=2, ensure_ascii=True))


def table(counter: dict[str, Any]) -> str:
    if not counter:
        return "| Item | Count |\n| --- | ---: |\n| none | 0 |"
    lines = ["| Item | Count |", "| --- | ---: |"]
    for key, value in sorted(counter.items(), key=lambda item: (-int(item[1]), item[0])):
        lines.append(f"| `{key}` | {value} |")
    return "\n".join(lines)


def write_report(summary: dict[str, Any]) -> None:
    length_lines = ["| Doc type | Min | Median | P95 | Max |", "| --- | ---: | ---: | ---: | ---: |"]
    for doc_type, stats in sorted(summary["text_length_summary"].items()):
        length_lines.append(
            f"| `{doc_type}` | {stats['min']} | {stats['median']} | {stats['p95']} | {stats['max']} |"
        )
    text = f"""# RAG Quality Report

Generated at: `{summary['generated_at']}`

## Summary

| Metric | Value |
| --- | ---: |
| Parsed docs | {summary['parsed_docs']} |
| Unique doc IDs | {summary['unique_doc_ids']} |
| Duplicate doc IDs | {summary['duplicate_doc_ids']} |
| Finding rows written | {summary['finding_rows_written']} |

## Rows by File

{table(summary['rows_by_file'])}

## Doc Types

{table(summary['doc_types'])}

## Text Lengths

{chr(10).join(length_lines)}

## Structural Flags

{table(summary['structural_flags'])}

## Text Health Flags

{table(summary['text_flags'])}

## Game Overview Flags

{table(summary['game_quality_flags'])}

## Mechanic Profile Flags

{table(summary['mechanic_quality_flags'])}

## Review Digest Flags

{table(summary['review_quality_flags'])}

## Notes

- This audit checks generated RAG JSONL structure and text health only.
- `raw_index/rag_quality_findings.jsonl` contains capped example findings for inspection.
- Review snippets are user-generated text and remain local-only until release/legal review.
"""
    REPORT.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
