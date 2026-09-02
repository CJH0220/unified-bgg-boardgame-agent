#!/usr/bin/env python3
"""Query unified_bgg overview and review digest for one board game."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_PROJECT = Path(r"D:\OpenViking\research\datasets\unified_bgg")


def discover_project(explicit: Path | None = None) -> Path:
    """Resolve a checkout-independent project path for installed or repo skills."""
    candidates = []
    if explicit:
        candidates.append(explicit)
    if value := __import__("os").environ.get("UNIFIED_BGG_ROOT"):
        candidates.append(Path(value))
    candidates.append(Path(__file__).resolve().parents[3] / "datasets" / "unified_bgg")
    candidates.append(DEFAULT_PROJECT)
    candidates.append(Path.cwd() / "datasets" / "unified_bgg")
    candidates.append(Path.cwd())
    for candidate in candidates:
        if (candidate / "scripts" / "query_unified_index.py").exists():
            return candidate.resolve()
    return (explicit or DEFAULT_PROJECT).resolve()


def run_query(project: Path, query: str, doc_type: str, bgg_id: int | None, limit: int) -> list[dict]:
    script = project / "scripts" / "query_rag_index.py"
    if not script.exists():
        raise SystemExit(f"query script not found: {script}")
    cmd = [sys.executable, str(script), query, "--doc-type", doc_type, "--limit", str(limit), "--json"]
    if bgg_id is not None:
        cmd.extend(["--bgg-id", str(bgg_id)])
    proc = subprocess.run(cmd, cwd=str(project), text=True, capture_output=True, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f"query failed: {cmd}")
    return json.loads(proc.stdout)


def first_doc(results: list[dict]) -> dict | None:
    return results[0].get("document") if results else None


def as_markdown(payload: dict) -> str:
    overview = first_doc(payload["game_overview"])
    reviews = first_doc(payload["review_digest"])
    lines = ["# unified_bgg Retrieval", ""]
    lines.append(f"- Query: `{payload['query']}`")
    if payload.get("bgg_id") is not None:
        lines.append(f"- BGG ID filter: `{payload['bgg_id']}`")
    lines.append(f"- Project: `{payload['project']}`")
    lines.append("")
    if overview:
        stats = overview.get("stats") or {}
        players = overview.get("players") or {}
        playtime = overview.get("playtime") or {}
        tax = overview.get("taxonomy") or {}
        lines.extend([
            "## Game Overview",
            "",
            f"- Title: {overview.get('title')}",
            f"- Game ID: {overview.get('game_id')}",
            f"- Year: {overview.get('year_published')}",
            f"- Players: {players.get('min_players')}-{players.get('max_players')}",
            f"- Playtime: {playtime.get('min_playtime')}-{playtime.get('max_playtime')} minutes",
            f"- Age: {overview.get('min_age')}+",
            f"- Average rating: {stats.get('average_rating')}",
            f"- Bayes average: {stats.get('bayes_average')}",
            f"- Rank: {stats.get('rank_position')}",
            f"- Weight: {stats.get('weight_average')}",
            f"- Mechanics: {', '.join(tax.get('mechanic') or [])}",
            f"- Categories: {', '.join(tax.get('category') or [])}",
            "",
            "### Text Preview",
            "",
            (overview.get("text") or "")[:1200],
            "",
        ])
    if reviews:
        summary = reviews.get("rating_summary") or {}
        lines.extend([
            "## Review Digest",
            "",
            f"- Rating rows: {summary.get('rating_rows')}",
            f"- Comment rows: {summary.get('comment_rows')}",
            f"- Average rating: {summary.get('average_rating')}",
            f"- Comment coverage pct: {summary.get('comment_coverage_pct')}",
            "",
            "### Text Preview",
            "",
            (reviews.get("text") or "")[:1200],
            "",
        ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Search query, preferably in English plus key mechanisms")
    parser.add_argument("--bgg-id", type=int, help="Exact BGG ID filter")
    parser.add_argument("--project", type=Path, default=DEFAULT_PROJECT, help="unified_bgg project root")
    parser.add_argument("--limit", type=int, default=1, help="results per document type")
    parser.add_argument("--markdown", action="store_true", help="print compact Markdown instead of JSON")
    parser.add_argument("--out", type=Path, help="optional output file path")
    args = parser.parse_args()

    project = discover_project(args.project)
    payload = {
        "project": str(project),
        "query": args.query,
        "bgg_id": args.bgg_id,
        "game_overview": run_query(project, args.query, "game_overview", args.bgg_id, args.limit),
        "review_digest": run_query(project, args.query + " comments", "review_digest", args.bgg_id, args.limit),
    }
    output = as_markdown(payload) if args.markdown else json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output + "\n", encoding="utf-8")
    else:
        sys.stdout.write(output + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
