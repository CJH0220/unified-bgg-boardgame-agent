"""Evaluate unified_bgg finetune preview JSONL samples.

Outputs:
- raw_index/finetune_quality_summary.json
- raw_index/finetune_quality_findings.jsonl
- raw_index/finetune_candidate_quality_summary.json when --kind candidate is used
- raw_index/finetune_candidate_quality_findings.jsonl when --kind candidate is used
- docs/finetune_preview_report.md
- docs/finetune_candidate_report.md when --kind candidate is used
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import median
from typing import Any

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
SAMPLES_FINETUNE = ROOT / "samples" / "finetune"
SAMPLES_RAG = ROOT / "samples" / "rag"
RAW_INDEX = ROOT / "raw_index"
DOCS = ROOT / "docs"

TASK_TYPES = [
    "game_qa",
    "mechanic_explanation",
    "review_summary",
    "recommendation_reasoning",
    "extraction",
]
RAG_FILES = [
    SAMPLES_RAG / "game_overview.jsonl",
    SAMPLES_RAG / "mechanic_profile.jsonl",
    SAMPLES_RAG / "review_digest.jsonl",
]
REQUIRED_FIELDS = [
    "sample_id",
    "schema_version",
    "task_type",
    "language",
    "input",
    "output",
    "source_doc_ids",
    "source_game_ids",
    "quality_flags",
    "metadata",
]
EXPECTED_TASKS = {
    "game_qa",
    "mechanic_explanation",
    "review_summary",
    "recommendation_reasoning",
    "extraction",
}


def default_files(kind: str) -> list[Path]:
    return [SAMPLES_FINETUNE / f"{task}.{kind}.jsonl" for task in TASK_TYPES]


def summary_path(kind: str) -> Path:
    return RAW_INDEX / ("finetune_quality_summary.json" if kind == "preview" else "finetune_candidate_quality_summary.json")


def findings_path(kind: str) -> Path:
    return RAW_INDEX / ("finetune_quality_findings.jsonl" if kind == "preview" else "finetune_candidate_quality_findings.jsonl")


def build_summary_path(kind: str) -> Path:
    return RAW_INDEX / ("finetune_sample_summary.json" if kind == "preview" else "finetune_candidate_summary.json")


def report_path(kind: str) -> Path:
    return DOCS / ("finetune_preview_report.md" if kind == "preview" else "finetune_candidate_report.md")


def percentile(values: list[int], pct: float) -> int | None:
    if not values:
        return None
    ordered = sorted(values)
    idx = round((len(ordered) - 1) * pct)
    return ordered[idx]


def load_rag_doc_ids() -> set[str]:
    doc_ids: set[str] = set()
    for path in RAG_FILES:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("doc_id"):
                    doc_ids.add(row["doc_id"])
    return doc_ids


def add_finding(
    findings: list[dict[str, Any]],
    source_file: Path,
    line_no: int,
    code: str,
    detail: str,
    row: dict[str, Any] | None = None,
) -> None:
    if len(findings) >= 500:
        return
    findings.append(
        {
            "source_file": source_file.relative_to(ROOT).as_posix(),
            "line_no": line_no,
            "code": code,
            "detail": detail,
            "sample_id": (row or {}).get("sample_id"),
            "task_type": (row or {}).get("task_type"),
        }
    )


def text_flags(text: str) -> list[str]:
    flags = []
    if not text.strip():
        flags.append("empty_text")
    if "\ufffd" in text:
        flags.append("replacement_character")
    if ("?" * 4) in text:
        flags.append("question_mark_mojibake")
    if len(text) < 20:
        flags.append("very_short_text")
    if len(text) > 8000:
        flags.append("very_long_text")
    return flags


def table(counter: dict[str, Any]) -> str:
    if not counter:
        return "| Item | Count |\n| --- | ---: |\n| none | 0 |"
    lines = ["| Item | Count |", "| --- | ---: |"]
    for key, value in sorted(counter.items(), key=lambda item: (-int(item[1]), str(item[0]))):
        lines.append(f"| `{key}` | {value} |")
    return "\n".join(lines)


def length_table(summary: dict[str, dict[str, int | None]]) -> str:
    lines = ["| Task type | Min | Median | P95 | Max |", "| --- | ---: | ---: | ---: | ---: |"]
    for task, values in sorted(summary.items()):
        lines.append(f"| `{task}` | {values['min']} | {values['median']} | {values['p95']} | {values['max']} |")
    return "\n".join(lines)


def evaluate(files: list[Path]) -> dict[str, Any]:
    rag_doc_ids = load_rag_doc_ids()
    counters: dict[str, Counter[str]] = defaultdict(Counter)
    output_lengths: dict[str, list[int]] = defaultdict(list)
    rows_by_file: Counter[str] = Counter()
    sample_ids: set[str] = set()
    findings: list[dict[str, Any]] = []
    parsed_rows = 0

    for path in files:
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    counters["structural_flags"]["json_decode_error"] += 1
                    add_finding(findings, path, line_no, "json_decode_error", str(exc))
                    continue
                parsed_rows += 1
                rows_by_file[path.relative_to(ROOT).as_posix()] += 1
                task = row.get("task_type") or "unknown"
                counters["task_counts"][task] += 1
                output_lengths[task].append(len(row.get("output") or ""))

                sid = row.get("sample_id")
                if sid in sample_ids:
                    counters["structural_flags"]["duplicate_sample_id"] += 1
                    add_finding(findings, path, line_no, "duplicate_sample_id", "Duplicate sample_id.", row)
                elif sid:
                    sample_ids.add(sid)

                for field in REQUIRED_FIELDS:
                    if field not in row:
                        counters["structural_flags"][f"missing_{field}"] += 1
                        add_finding(findings, path, line_no, f"missing_{field}", "Required field missing.", row)

                if task not in EXPECTED_TASKS:
                    counters["structural_flags"]["unknown_task_type"] += 1
                    add_finding(findings, path, line_no, "unknown_task_type", f"Unexpected task_type={task}.", row)
                if row.get("language") != "zh":
                    counters["structural_flags"]["non_zh_language"] += 1
                if not row.get("source_doc_ids"):
                    counters["source_flags"]["missing_source_doc_ids"] += 1
                    add_finding(findings, path, line_no, "missing_source_doc_ids", "source_doc_ids is empty.", row)
                else:
                    for doc_id in row["source_doc_ids"]:
                        if doc_id not in rag_doc_ids:
                            counters["source_flags"]["unknown_source_doc_id"] += 1
                            add_finding(findings, path, line_no, "unknown_source_doc_id", doc_id, row)
                if not row.get("source_game_ids"):
                    counters["source_flags"]["missing_source_game_ids"] += 1
                if task in {"game_qa", "recommendation_reasoning", "extraction"} and not row.get("snapshot_date"):
                    counters["source_flags"]["missing_snapshot_date"] += 1

                for flag in text_flags(row.get("input") or ""):
                    counters["input_text_flags"][flag] += 1
                    add_finding(findings, path, line_no, f"input_{flag}", "Input text issue.", row)
                for flag in text_flags(row.get("output") or ""):
                    counters["output_text_flags"][flag] += 1
                    add_finding(findings, path, line_no, f"output_{flag}", "Output text issue.", row)

                for flag in row.get("quality_flags") or []:
                    counters["sample_quality_flags"][flag] += 1

    return {
        "generated_at": datetime.now().replace(microsecond=0).isoformat(),
        "files": [path.relative_to(ROOT).as_posix() for path in files],
        "parsed_rows": parsed_rows,
        "unique_sample_ids": len(sample_ids),
        "rows_by_file": dict(rows_by_file),
        "task_counts": dict(counters["task_counts"]),
        "structural_flags": dict(counters["structural_flags"]),
        "source_flags": dict(counters["source_flags"]),
        "input_text_flags": dict(counters["input_text_flags"]),
        "output_text_flags": dict(counters["output_text_flags"]),
        "sample_quality_flags": dict(counters["sample_quality_flags"]),
        "output_length_summary": {
            task: {
                "min": min(values),
                "median": int(median(values)),
                "p95": percentile(values, 0.95),
                "max": max(values),
            }
            for task, values in sorted(output_lengths.items())
        },
        "finding_rows_written": len(findings),
        "rag_doc_ids_loaded": len(rag_doc_ids),
        "findings": findings,
    }


def render_report(summary: dict[str, Any], build_summary: dict[str, Any] | None, kind: str) -> str:
    title = "Finetune Preview Report" if kind == "preview" else "Finetune Candidate Report"
    lines = [
        f"# {title}",
        "",
        f"Generated at: `{summary['generated_at']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Parsed rows | {summary['parsed_rows']} |",
        f"| Unique sample IDs | {summary['unique_sample_ids']} |",
        f"| Finding rows written | {summary['finding_rows_written']} |",
        f"| RAG doc IDs loaded for source validation | {summary['rag_doc_ids_loaded']} |",
    ]
    if build_summary:
        lines += [
            f"| Preview size per task | {build_summary.get('preview_size')} |",
            f"| Source game_overview docs | {build_summary.get('inputs', {}).get('game_overview_docs')} |",
            f"| Source mechanic_profile docs | {build_summary.get('inputs', {}).get('mechanic_profile_docs')} |",
            f"| Source review_digest docs | {build_summary.get('inputs', {}).get('review_digest_docs')} |",
        ]
    lines += [
        "",
        "## Rows by File",
        "",
        table(summary["rows_by_file"]),
        "",
        "## Task Counts",
        "",
        table(summary["task_counts"]),
        "",
        "## Structural Flags",
        "",
        table(summary["structural_flags"]),
        "",
        "## Source Flags",
        "",
        table(summary["source_flags"]),
        "",
        "## Input Text Flags",
        "",
        table(summary["input_text_flags"]),
        "",
        "## Output Text Flags",
        "",
        table(summary["output_text_flags"]),
        "",
        "## Sample Quality Flags",
        "",
        table(summary["sample_quality_flags"]),
        "",
        "## Output Lengths",
        "",
        length_table(summary["output_length_summary"]),
        "",
        "## Notes",
        "",
        "- Preview samples are deterministic template outputs for audit and iteration.",
        "- `template_generated` is expected on every row.",
        "- Source document IDs are checked against current RAG JSONL outputs.",
        "- Review-derived outputs summarize themes and do not reproduce long user comments.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate unified_bgg finetune preview samples.")
    parser.add_argument("--kind", choices=["preview", "candidate"], default="preview")
    parser.add_argument("--files", nargs="*", default=None)
    args = parser.parse_args()

    RAW_INDEX.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    file_args = args.files if args.files is not None else [str(path) for path in default_files(args.kind)]
    files = [Path(path) if Path(path).is_absolute() else ROOT / path for path in file_args]
    summary = evaluate(files)
    findings = summary.pop("findings")
    summary_path(args.kind).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with findings_path(args.kind).open("w", encoding="utf-8", newline="\n") as f:
        for finding in findings:
            f.write(json.dumps(finding, ensure_ascii=False, sort_keys=True) + "\n")
    build_path = build_summary_path(args.kind)
    build_summary = json.loads(build_path.read_text(encoding="utf-8")) if build_path.exists() else None
    report_path(args.kind).write_text(render_report(summary, build_summary, args.kind), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
