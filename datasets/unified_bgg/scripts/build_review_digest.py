"""Build review_digest RAG docs by streaming the 26M BGG review/rating CSV.

The source file is large, so this script performs a single streaming pass and
keeps only per-game aggregates plus a few representative snippets in memory.

Outputs:
- samples/rag/review_digest.jsonl
- samples/rag/review_digest.preview.jsonl
- raw_index/review_digest_summary.json
- docs/review_digest_report.md
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
DATA = ROOT.parent
INTERMEDIATE = ROOT / "intermediate"
SAMPLES_RAG = ROOT / "samples" / "rag"
RAW_INDEX = ROOT / "raw_index"
DOCS = ROOT / "docs"
MANIFEST = ROOT / "manifest.json"

SOURCE = DATA / "bgg-reviews-jvanelteren" / "raw" / "bgg-26m-reviews.csv"
GAMES = INTERMEDIATE / "games.csv"

OUTPUT = SAMPLES_RAG / "review_digest.jsonl"
PREVIEW = SAMPLES_RAG / "review_digest.preview.jsonl"
SUMMARY = RAW_INDEX / "review_digest_summary.json"
REPORT = DOCS / "review_digest_report.md"

SCHEMA_VERSION = "rag-v0.1"
TRANSFORM_VERSION = "phase5-review-digest-v0.2"
SOURCE_DATASET = "bgg-reviews-jvanelteren"
SOURCE_FILE = "bgg-reviews-jvanelteren/raw/bgg-26m-reviews.csv"


def int_or_none(value: str | None) -> int | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def float_or_none(value: str | None) -> float | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def clean_comment(value: str | None, limit: int = 360) -> str:
    text = html.unescape(value or "")
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\[[A-Za-z/][^\]]{0,40}\]", " ", text)
    text = re.sub(r"\?{4,}", "?", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "..."
    return text


def bucket_for_rating(rating: float | None) -> str:
    if rating is None:
        return "unrated"
    if rating >= 8:
        return "positive"
    if rating <= 5:
        return "critical"
    return "mixed"


def snippet_score(text: str, rating: float | None) -> tuple[int, float]:
    # Prefer informative mid-length comments; use rating only as a stable tiebreaker.
    length_score = min(len(text), 280)
    return (length_score, rating or 0.0)


def add_snippet(group: dict[str, Any], bucket: str, text: str, rating: float | None, user: str | None, max_snippets: int) -> None:
    if len(text) < 40:
        return
    snippets = group["snippets"][bucket]
    normalized = text.lower()
    if any(item["normalized"] == normalized for item in snippets):
        return
    snippets.append(
        {
            "rating": rating,
            "user": user or None,
            "text": text,
            "normalized": normalized,
            "score": snippet_score(text, rating),
        }
    )
    snippets.sort(key=lambda item: item["score"], reverse=True)
    del snippets[max_snippets:]


def load_game_lookup() -> dict[int, dict[str, Any]]:
    lookup: dict[int, dict[str, Any]] = {}
    with GAMES.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            bgg_id = int_or_none(row.get("bgg_id"))
            if bgg_id is None:
                continue
            lookup[bgg_id] = {
                "game_id": row.get("game_id") or f"bgg:{bgg_id}",
                "title": row.get("primary_name") or None,
                "game_type": row.get("game_type") or None,
                "year_published": int_or_none(row.get("year_published")),
            }
    return lookup


def new_group(bgg_id: int, raw_name: str | None) -> dict[str, Any]:
    return {
        "bgg_id": bgg_id,
        "raw_name": raw_name or None,
        "rating_rows": 0,
        "rating_sum": 0.0,
        "comment_rows": 0,
        "comment_char_sum": 0,
        "rating_histogram": Counter(),
        "snippets": {
            "positive": [],
            "mixed": [],
            "critical": [],
            "unrated": [],
        },
    }


def update_group(group: dict[str, Any], row: dict[str, str], max_snippets: int) -> None:
    rating = float_or_none(row.get("rating"))
    if rating is not None:
        group["rating_rows"] += 1
        group["rating_sum"] += rating
        bucket = str(int(max(1, min(10, round(rating)))))
        group["rating_histogram"][bucket] += 1

    comment = clean_comment(row.get("comment"))
    if comment:
        group["comment_rows"] += 1
        group["comment_char_sum"] += len(comment)
        add_snippet(
            group,
            bucket_for_rating(rating),
            comment,
            rating,
            row.get("user"),
            max_snippets,
        )


def avg(value_sum: float, count: int) -> float | None:
    if not count:
        return None
    return round(value_sum / count, 4)


def pct(part: int, total: int) -> float:
    if not total:
        return 0.0
    return round(part * 100.0 / total, 4)


def public_snippets(snippets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "rating": item["rating"],
            "user": item["user"],
            "text": item["text"],
        }
        for item in snippets
    ]


def build_text(doc: dict[str, Any]) -> str:
    title = doc.get("title") or f"BGG {doc['bgg_id']}"
    rating_summary = doc["rating_summary"]
    parts = [
        f"BGG user review digest for {title}.",
        (
            f"Scanned {rating_summary['rating_rows']:,} rating rows and "
            f"{rating_summary['comment_rows']:,} non-empty comments from {SOURCE_DATASET}."
        ),
    ]
    if rating_summary.get("average_rating") is not None:
        parts.append(
            f"Average rating in the scanned rating rows is {rating_summary['average_rating']:.2f}; "
            f"comment coverage is {rating_summary['comment_coverage_pct']:.2f}%."
        )

    snippets = doc["representative_snippets"]
    for key, label in [
        ("positive", "Positive snippets"),
        ("mixed", "Mixed snippets"),
        ("critical", "Critical snippets"),
    ]:
        items = snippets.get(key, [])[:3]
        if not items:
            continue
        quoted = []
        for item in items:
            rating = item.get("rating")
            prefix = f"{rating:g}/10: " if isinstance(rating, (int, float)) else ""
            quoted.append(prefix + item["text"])
        parts.append(label + ": " + " | ".join(quoted))
    return " ".join(parts)


def make_doc(group: dict[str, Any], lookup: dict[int, dict[str, Any]], generated_at: str) -> dict[str, Any]:
    bgg_id = group["bgg_id"]
    game = lookup.get(bgg_id, {})
    game_id = game.get("game_id") or f"bgg:{bgg_id}"
    rating_rows = group["rating_rows"]
    comment_rows = group["comment_rows"]
    doc = {
        "doc_id": f"reviews:{game_id}:digest:{SCHEMA_VERSION}",
        "doc_type": "review_digest",
        "schema_version": SCHEMA_VERSION,
        "game_id": game_id,
        "bgg_id": bgg_id,
        "title": game.get("title") or group.get("raw_name"),
        "game_type": game.get("game_type"),
        "year_published": game.get("year_published"),
        "rating_summary": {
            "rating_rows": rating_rows,
            "comment_rows": comment_rows,
            "comment_coverage_pct": pct(comment_rows, rating_rows),
            "average_rating": avg(group["rating_sum"], rating_rows),
            "average_comment_length": avg(group["comment_char_sum"], comment_rows),
            "rating_histogram": dict(sorted(group["rating_histogram"].items(), key=lambda item: int(item[0]))),
        },
        "representative_snippets": {
            key: public_snippets(group["snippets"][key])
            for key in ["positive", "mixed", "critical", "unrated"]
            if group["snippets"][key]
        },
        "source_datasets": [SOURCE_DATASET],
        "metadata": {
            "generated_at": generated_at,
            "transform_version": TRANSFORM_VERSION,
            "source_file": SOURCE_FILE,
            "source_note": "Extractive digest; comments are user-generated BGG text and should remain local until release/legal review.",
        },
    }
    doc["text"] = build_text(doc)
    return doc


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def update_manifest() -> None:
    if not MANIFEST.exists():
        return
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["version"] = "0.5.1-review-digest"
    manifest["status"] = "phase_5_review_digest_generated"
    generated = manifest.setdefault("generated_outputs", {})
    rag_samples = generated.setdefault("rag_samples", [])
    for name in ["review_digest.jsonl", "review_digest.preview.jsonl"]:
        if name not in rag_samples:
            rag_samples.append(name)
    raw_index = generated.setdefault("raw_index", [])
    if "review_digest_summary.json" not in raw_index:
        raw_index.append("review_digest_summary.json")
    docs = generated.setdefault("docs", [])
    if "review_digest_report.md" not in docs:
        docs.append("review_digest_report.md")
    notes = manifest.setdefault("notes", [])
    note = "Phase 5.1 streamed the 26M-row review/rating CSV and generated extractive review_digest RAG docs."
    if note not in notes:
        notes.append(note)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_report(summary: dict[str, Any]) -> None:
    text = f"""# Review Digest Report

Generated at: `{summary['generated_at']}`

## Outputs

| Output | Rows | Bytes |
| --- | ---: | ---: |
| `samples/rag/review_digest.jsonl` | {summary['outputs']['review_digest']['rows']} | {summary['outputs']['review_digest']['bytes']} |
| `samples/rag/review_digest.preview.jsonl` | {summary['outputs']['review_digest_preview']['rows']} | {summary['outputs']['review_digest_preview']['bytes']} |

## Streaming Scan

| Metric | Value |
| --- | ---: |
| Raw rows scanned | {summary['scan']['rows_scanned']} |
| Games with rating rows | {summary['scan']['games_with_ratings']} |
| Games with non-empty comments | {summary['scan']['games_with_comments']} |
| Non-empty comments | {summary['scan']['comment_rows']} |
| Comment coverage | {summary['scan']['comment_coverage_pct']}% |

## Notes

- Source file: `bgg-reviews-jvanelteren/raw/bgg-26m-reviews.csv`
- The output is extractive: it stores per-game rating/comment aggregates plus representative positive, mixed, and critical snippets.
- Review snippets are BGG user-generated content; keep this output local until release/legal policy is reviewed.
"""
    REPORT.write_text(text, encoding="utf-8")


def file_info(path: Path, rows: int) -> dict[str, Any]:
    return {"path": path.relative_to(ROOT).as_posix(), "rows": rows, "bytes": path.stat().st_size}


def main() -> None:
    parser = argparse.ArgumentParser(description="Stream BGG 26M reviews and build review_digest RAG docs.")
    parser.add_argument("--preview-size", type=int, default=50)
    parser.add_argument("--max-rows", type=int, default=0, help="Optional debug cap; 0 means full scan.")
    parser.add_argument("--chunk-size", type=int, default=1_000_000, help="Progress interval in rows.")
    parser.add_argument("--max-snippets-per-bucket", type=int, default=5)
    parser.add_argument("--no-manifest-update", action="store_true")
    args = parser.parse_args()

    SAMPLES_RAG.mkdir(parents=True, exist_ok=True)
    RAW_INDEX.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now().replace(microsecond=0).isoformat()
    lookup = load_game_lookup()
    groups: dict[int, dict[str, Any]] = {}
    rows_scanned = 0
    malformed_rows = 0

    with SOURCE.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows_scanned += 1
            bgg_id = int_or_none(row.get("ID"))
            if bgg_id is None:
                malformed_rows += 1
                continue
            group = groups.get(bgg_id)
            if group is None:
                group = new_group(bgg_id, row.get("name"))
                groups[bgg_id] = group
            update_group(group, row, args.max_snippets_per_bucket)
            if args.chunk_size and rows_scanned % args.chunk_size == 0:
                print(f"scanned_rows={rows_scanned} games={len(groups)} comments={sum(g['comment_rows'] for g in groups.values())}", flush=True)
            if args.max_rows and rows_scanned >= args.max_rows:
                break

    docs = [
        make_doc(group, lookup, generated_at)
        for group in groups.values()
        if group["comment_rows"] > 0
    ]
    docs.sort(key=lambda row: (row["rating_summary"]["comment_rows"], row["rating_summary"]["rating_rows"]), reverse=True)
    preview = docs[: args.preview_size]
    write_jsonl(OUTPUT, docs)
    write_jsonl(PREVIEW, preview)

    rating_rows = sum(group["rating_rows"] for group in groups.values())
    comment_rows = sum(group["comment_rows"] for group in groups.values())
    summary = {
        "generated_at": generated_at,
        "schema_version": SCHEMA_VERSION,
        "transform_version": TRANSFORM_VERSION,
        "source_file": SOURCE_FILE,
        "scan": {
            "rows_scanned": rows_scanned,
            "malformed_rows": malformed_rows,
            "games_with_ratings": sum(1 for group in groups.values() if group["rating_rows"] > 0),
            "games_with_comments": len(docs),
            "rating_rows": rating_rows,
            "comment_rows": comment_rows,
            "comment_coverage_pct": pct(comment_rows, rating_rows),
        },
        "outputs": {
            "review_digest": file_info(OUTPUT, len(docs)),
            "review_digest_preview": file_info(PREVIEW, len(preview)),
        },
        "parameters": {
            "preview_size": args.preview_size,
            "max_rows": args.max_rows,
            "chunk_size": args.chunk_size,
            "max_snippets_per_bucket": args.max_snippets_per_bucket,
        },
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_report(summary)
    if not args.no_manifest_update:
        update_manifest()
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
