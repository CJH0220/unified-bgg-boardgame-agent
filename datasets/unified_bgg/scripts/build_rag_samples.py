"""Build Phase 5 RAG JSONL samples for unified_bgg.

Outputs:
- samples/rag/game_overview.jsonl
- samples/rag/game_overview.preview.jsonl
- samples/rag/mechanic_profile.jsonl
- samples/rag/mechanic_profile.preview.jsonl
- raw_index/rag_sample_summary.json
- docs/rag_samples_report.md

The script uses only intermediate tables and does not scan row-level
ratings/reviews. It is safe to rerun after rebuilding Phase 3/4 tables.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
INTERMEDIATE = ROOT / "intermediate"
SAMPLES_RAG = ROOT / "samples" / "rag"
RAW_INDEX = ROOT / "raw_index"
DOCS = ROOT / "docs"
MANIFEST = ROOT / "manifest.json"

GAMES = INTERMEDIATE / "games.csv"
STATS = INTERMEDIATE / "game_stats.csv"
TAXONOMY = INTERMEDIATE / "game_taxonomy_canonical.csv"

GAME_OVERVIEW = SAMPLES_RAG / "game_overview.jsonl"
GAME_OVERVIEW_PREVIEW = SAMPLES_RAG / "game_overview.preview.jsonl"
MECHANIC_PROFILE = SAMPLES_RAG / "mechanic_profile.jsonl"
MECHANIC_PROFILE_PREVIEW = SAMPLES_RAG / "mechanic_profile.preview.jsonl"
SUMMARY = RAW_INDEX / "rag_sample_summary.json"
REPORT = DOCS / "rag_samples_report.md"

SCHEMA_VERSION = "rag-v0.1"
TRANSFORM_VERSION = "phase5-rag-samples-v0.2"
PREVIEW_SIZE_DEFAULT = 50

SOURCE_PRIORITY = {
    "bgg-reviews-jvanelteren": 70,
    "bgg-ranked-mattadamhouser": 60,
    "bgg-threnjen": 50,
    "bgg-andrewmvd": 40,
    "bgg-mrpantherson": 30,
    "bgg-gabrio": 20,
    "bgg-sujaykapadnis": 10,
}

TAXONOMY_TYPES = ["mechanic", "category", "family", "domain", "theme", "subcategory"]


def boolish(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y"}


def clean_text(value: str | None, limit: int = 1400) -> str:
    text = html.unescape(value or "")
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\?{4,}", "?", text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "..."
    return text


def split_sources(value: str | None) -> list[str]:
    return [part for part in (value or "").split(";") if part]


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


def date_score(value: str | None) -> tuple[int, int, int]:
    value = (value or "").strip()
    nums = [int(part) for part in re.findall(r"\d+", value)]
    if len(nums) == 1:
        return (nums[0], 0, 0)
    if len(nums) == 2:
        return (nums[0], nums[1], 0)
    if len(nums) >= 3:
        return (nums[0], nums[1], nums[2])
    return (0, 0, 0)


def stat_score(row: dict[str, str]) -> tuple[Any, ...]:
    source = row.get("source_dataset", "")
    has_rating = 1 if row.get("average_rating") or row.get("bayes_average") else 0
    has_users = 1 if row.get("users_rated") else 0
    return (
        date_score(row.get("snapshot_date")),
        SOURCE_PRIORITY.get(source, 0),
        has_rating,
        has_users,
    )


def rating_sort_key(game_id: str, stats: dict[str, dict[str, str]]) -> tuple[Any, ...]:
    row = stats.get(game_id, {})
    bayes = float_or_none(row.get("bayes_average")) or 0.0
    avg = float_or_none(row.get("average_rating")) or 0.0
    users = int_or_none(row.get("users_rated")) or 0
    rank = int_or_none(row.get("rank_position")) or 999999999
    return (bayes, avg, users, -rank)


def load_games() -> dict[str, dict[str, str]]:
    games: dict[str, dict[str, str]] = {}
    with GAMES.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            games[row["game_id"]] = row
    return games


def load_best_overall_stats() -> dict[str, dict[str, str]]:
    best: dict[str, dict[str, str]] = {}
    with STATS.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if (row.get("rank_domain") or "overall") != "overall":
                continue
            gid = row["game_id"]
            if gid not in best or stat_score(row) > stat_score(best[gid]):
                best[gid] = row
    return best


def load_taxonomy() -> tuple[
    dict[str, dict[str, set[str]]],
    dict[str, Counter[str]],
    dict[str, set[str]],
    Counter[str],
]:
    per_game: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    per_game_sources: dict[str, set[str]] = defaultdict(set)
    review_counts: Counter[str] = Counter()
    source_counts: dict[str, Counter[str]] = defaultdict(Counter)

    with TAXONOMY.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            gid = row["game_id"]
            tax_type = row.get("taxonomy_type", "")
            if tax_type not in TAXONOMY_TYPES:
                continue
            name = (row.get("canonical_name") or row.get("taxonomy_name_canonical") or "").strip()
            if not name:
                continue
            source = row.get("source_dataset", "")
            if source:
                per_game_sources[gid].add(source)
                source_counts[name][source] += 1
            if boolish(row.get("canonical_needs_review")):
                review_counts[tax_type] += 1
                continue
            per_game[gid][tax_type].add(name)

    return per_game, source_counts, per_game_sources, review_counts


def values_for(row: dict[str, str], fields: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for field in fields:
        value = row.get(field, "")
        if value == "":
            out[field] = None
        elif field in {"bgg_id", "year_published", "min_players", "max_players", "min_playtime", "max_playtime", "min_age", "users_rated", "rank_position", "weight_votes"}:
            out[field] = int_or_none(value)
        elif field in {"average_rating", "bayes_average", "weight_average"}:
            out[field] = float_or_none(value)
        else:
            out[field] = value
    return out


def join_labels(labels: list[str], limit: int = 12) -> str:
    if not labels:
        return ""
    shown = labels[:limit]
    suffix = "" if len(labels) <= limit else f", and {len(labels) - limit} more"
    return ", ".join(shown) + suffix


def build_game_text(game: dict[str, str], stat: dict[str, str] | None, tax: dict[str, set[str]]) -> str:
    title = game.get("primary_name") or f"BGG {game.get('bgg_id')}"
    parts: list[str] = [title]
    year = game.get("year_published")
    if year:
        parts[0] += f" ({year})"
    game_type = game.get("game_type")
    if game_type:
        parts.append(f"is a {game_type}.")
    else:
        parts.append("is a BoardGameGeek game entity.")

    min_players = int_or_none(game.get("min_players"))
    max_players = int_or_none(game.get("max_players"))
    min_time = int_or_none(game.get("min_playtime"))
    max_time = int_or_none(game.get("max_playtime"))
    min_age = int_or_none(game.get("min_age"))
    play_bits: list[str] = []
    if min_players and max_players:
        play_bits.append(f"{min_players}-{max_players} players")
    if min_time and max_time:
        if min_time == max_time:
            play_bits.append(f"{min_time} minutes")
        else:
            play_bits.append(f"{min_time}-{max_time} minutes")
    if min_age:
        play_bits.append(f"ages {min_age}+")
    if play_bits:
        parts.append("It supports " + ", ".join(play_bits) + ".")

    if stat:
        stats_bits: list[str] = []
        avg = float_or_none(stat.get("average_rating"))
        bayes = float_or_none(stat.get("bayes_average"))
        users = int_or_none(stat.get("users_rated"))
        rank = int_or_none(stat.get("rank_position"))
        weight = float_or_none(stat.get("weight_average"))
        if avg is not None:
            stats_bits.append(f"average rating {avg:.2f}")
        if bayes is not None:
            stats_bits.append(f"Bayesian rating {bayes:.2f}")
        if users is not None:
            stats_bits.append(f"{users:,} users rated")
        if rank is not None:
            stats_bits.append(f"overall rank {rank}")
        if weight is not None:
            stats_bits.append(f"complexity {weight:.2f}/5")
        if stats_bits:
            parts.append(
                "Selected overall stats"
                f" ({stat.get('snapshot_date')}, {stat.get('source_dataset')}): "
                + "; ".join(stats_bits)
                + "."
            )

    for tax_type, label in [
        ("mechanic", "Canonical mechanics"),
        ("category", "Categories"),
        ("domain", "Domains"),
        ("theme", "Themes"),
        ("family", "Families"),
        ("subcategory", "Subcategories"),
    ]:
        labels = sorted(tax.get(tax_type, set()))
        text = join_labels(labels, limit=16 if tax_type == "family" else 12)
        if text:
            parts.append(f"{label}: {text}.")

    description = clean_text(game.get("description"))
    if description:
        parts.append("Description: " + description)
    text = " ".join(parts)
    if len(text) < 80:
        text += " This record is retained for entity completeness but has limited descriptive metadata."
    return text


def make_game_doc(
    game: dict[str, str],
    stat: dict[str, str] | None,
    tax: dict[str, set[str]],
    tax_sources: set[str],
    generated_at: str,
) -> dict[str, Any]:
    selected_sources = set(split_sources(game.get("selected_source_datasets")))
    if stat and stat.get("source_dataset"):
        selected_sources.add(stat["source_dataset"])
    selected_sources.update(tax_sources)
    quality_flags: list[str] = []
    if boolish(game.get("needs_review")):
        quality_flags.append("game_needs_review")
    if not game.get("primary_name"):
        quality_flags.append("missing_title")
    if not stat:
        quality_flags.append("missing_overall_stats")
    if not tax.get("mechanic"):
        quality_flags.append("missing_reliable_mechanics")

    return {
        "doc_id": f"game:{game['game_id']}:overview:{SCHEMA_VERSION}",
        "doc_type": "game_overview",
        "schema_version": SCHEMA_VERSION,
        "game_id": game["game_id"],
        "bgg_id": int_or_none(game.get("bgg_id")),
        "title": game.get("primary_name") or f"BGG {game.get('bgg_id')}",
        "game_type": game.get("game_type") or None,
        "year_published": int_or_none(game.get("year_published")),
        "players": values_for(game, ["min_players", "max_players"]),
        "playtime": values_for(game, ["min_playtime", "max_playtime"]),
        "min_age": int_or_none(game.get("min_age")),
        "stats": values_for(
            stat or {},
            ["snapshot_date", "average_rating", "bayes_average", "users_rated", "rank_position", "weight_average", "weight_votes", "source_dataset", "source_file"],
        ),
        "taxonomy": {tax_type: sorted(tax.get(tax_type, set())) for tax_type in TAXONOMY_TYPES},
        "source_datasets": sorted(selected_sources),
        "quality_flags": quality_flags,
        "metadata": {
            "generated_at": generated_at,
            "transform_version": TRANSFORM_VERSION,
            "source_tables": [
                "intermediate/games.csv",
                "intermediate/game_stats.csv",
                "intermediate/game_taxonomy_canonical.csv",
            ],
        },
        "text": build_game_text(game, stat, tax),
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def stream_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    write_jsonl(path, rows)


def build_game_docs(
    games: dict[str, dict[str, str]],
    stats: dict[str, dict[str, str]],
    taxonomy: dict[str, dict[str, set[str]]],
    tax_sources: dict[str, set[str]],
    generated_at: str,
) -> list[dict[str, Any]]:
    docs = []
    for gid in sorted(games, key=lambda x: int(x.split(":", 1)[1]) if ":" in x and x.split(":", 1)[1].isdigit() else x):
        docs.append(make_game_doc(games[gid], stats.get(gid), taxonomy.get(gid, {}), tax_sources.get(gid, set()), generated_at))
    return docs


def top_counter(counter: Counter[str], limit: int) -> list[dict[str, Any]]:
    return [{"name": name, "count": count} for name, count in counter.most_common(limit)]


def build_mechanic_docs(
    games: dict[str, dict[str, str]],
    stats: dict[str, dict[str, str]],
    taxonomy: dict[str, dict[str, set[str]]],
    source_counts: dict[str, Counter[str]],
    generated_at: str,
) -> list[dict[str, Any]]:
    mechanic_games: dict[str, set[str]] = defaultdict(set)
    for gid, types in taxonomy.items():
        for mechanic in types.get("mechanic", set()):
            mechanic_games[mechanic].add(gid)

    docs: list[dict[str, Any]] = []
    for mechanic, gids in mechanic_games.items():
        co_mechanics: Counter[str] = Counter()
        categories: Counter[str] = Counter()
        domains: Counter[str] = Counter()
        families: Counter[str] = Counter()
        avg_values: list[float] = []
        bayes_values: list[float] = []
        users_total = 0
        ranked_count = 0
        rated_count = 0

        for gid in gids:
            types = taxonomy.get(gid, {})
            for other in types.get("mechanic", set()):
                if other != mechanic:
                    co_mechanics[other] += 1
            categories.update(types.get("category", set()))
            domains.update(types.get("domain", set()))
            families.update(types.get("family", set()))
            row = stats.get(gid)
            if row:
                avg = float_or_none(row.get("average_rating"))
                bayes = float_or_none(row.get("bayes_average"))
                users = int_or_none(row.get("users_rated"))
                rank = int_or_none(row.get("rank_position"))
                if avg is not None:
                    avg_values.append(avg)
                    rated_count += 1
                if bayes is not None:
                    bayes_values.append(bayes)
                if users is not None:
                    users_total += users
                if rank is not None:
                    ranked_count += 1

        representative_ids = sorted(gids, key=lambda gid: rating_sort_key(gid, stats), reverse=True)[:12]
        representatives = []
        for gid in representative_ids:
            game = games.get(gid, {})
            row = stats.get(gid, {})
            representatives.append(
                {
                    "game_id": gid,
                    "bgg_id": int_or_none(game.get("bgg_id")),
                    "title": game.get("primary_name") or None,
                    "year_published": int_or_none(game.get("year_published")),
                    "average_rating": float_or_none(row.get("average_rating")),
                    "bayes_average": float_or_none(row.get("bayes_average")),
                    "users_rated": int_or_none(row.get("users_rated")),
                    "rank_position": int_or_none(row.get("rank_position")),
                }
            )

        rep_titles = [item["title"] for item in representatives if item.get("title")]
        text_parts = [
            f"{mechanic} is a canonical BGG mechanic in unified_bgg.",
            f"It appears on {len(gids):,} games after excluding taxonomy rows marked for review.",
        ]
        if rep_titles:
            text_parts.append("Representative games include " + join_labels(rep_titles, limit=8) + ".")
        if co_mechanics:
            text_parts.append(
                "Common co-occurring mechanics: "
                + join_labels([item["name"] for item in top_counter(co_mechanics, 12)], limit=12)
                + "."
            )
        if categories:
            text_parts.append(
                "Common categories: "
                + join_labels([item["name"] for item in top_counter(categories, 12)], limit=12)
                + "."
            )
        if avg_values:
            text_parts.append(f"Mean selected average rating across rated games is {mean(avg_values):.2f}.")

        docs.append(
            {
                "doc_id": f"mechanic:{mechanic.lower().replace(' ', '-').replace('/', '-')}:profile:{SCHEMA_VERSION}",
                "doc_type": "mechanic_profile",
                "schema_version": SCHEMA_VERSION,
                "mechanic": mechanic,
                "game_count": len(gids),
                "rated_game_count": rated_count,
                "ranked_game_count": ranked_count,
                "rating_summary": {
                    "mean_average_rating": round(mean(avg_values), 4) if avg_values else None,
                    "mean_bayes_average": round(mean(bayes_values), 4) if bayes_values else None,
                    "users_rated_total": users_total,
                },
                "representative_games": representatives,
                "cooccurring_mechanics": top_counter(co_mechanics, 20),
                "common_categories": top_counter(categories, 20),
                "common_domains": top_counter(domains, 20),
                "common_families": top_counter(families, 20),
                "source_datasets": sorted(source_counts.get(mechanic, Counter()).keys()),
                "metadata": {
                    "generated_at": generated_at,
                    "transform_version": TRANSFORM_VERSION,
                    "source_tables": [
                        "intermediate/games.csv",
                        "intermediate/game_stats.csv",
                        "intermediate/game_taxonomy_canonical.csv",
                    ],
                },
                "text": " ".join(text_parts),
            }
        )

    docs.sort(key=lambda row: (-row["game_count"], row["mechanic"].lower()))
    return docs


def update_manifest(status: str) -> None:
    if not MANIFEST.exists():
        return
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    current_status = manifest.get("status", "")
    # Do not let a later rerun of this Phase 5 script downgrade a Phase 6/7
    # manifest. Later phases rebuild these files as dependencies.
    if not re.match(r"phase_[6-9]", current_status):
        manifest["version"] = "0.5.0-rag-samples"
        manifest["status"] = status
    notes = manifest.setdefault("notes", [])
    note = "Phase 5 generated RAG JSONL outputs: game_overview and mechanic_profile, with preview files and quality summary."
    if note not in notes:
        notes.append(note)
    generated = manifest.setdefault("generated_outputs", {})
    rag_outputs = [
        "game_overview.jsonl",
        "game_overview.preview.jsonl",
        "mechanic_profile.jsonl",
        "mechanic_profile.preview.jsonl",
    ]
    generated["rag_samples"] = rag_outputs
    docs = generated.setdefault("docs", [])
    if "rag_samples_report.md" not in docs:
        docs.append("rag_samples_report.md")
    raw_index = generated.setdefault("raw_index", [])
    if "rag_sample_summary.json" not in raw_index:
        raw_index.append("rag_sample_summary.json")
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_report(summary: dict[str, Any]) -> None:
    text = f"""# RAG Samples Report

Generated at: `{summary['generated_at']}`

## Outputs

| Output | Rows | Bytes |
| --- | ---: | ---: |
| `samples/rag/game_overview.jsonl` | {summary['outputs']['game_overview']['rows']} | {summary['outputs']['game_overview']['bytes']} |
| `samples/rag/game_overview.preview.jsonl` | {summary['outputs']['game_overview_preview']['rows']} | {summary['outputs']['game_overview_preview']['bytes']} |
| `samples/rag/mechanic_profile.jsonl` | {summary['outputs']['mechanic_profile']['rows']} | {summary['outputs']['mechanic_profile']['bytes']} |
| `samples/rag/mechanic_profile.preview.jsonl` | {summary['outputs']['mechanic_profile_preview']['rows']} | {summary['outputs']['mechanic_profile_preview']['bytes']} |

## Source Tables

- `intermediate/games.csv`
- `intermediate/game_stats.csv`
- `intermediate/game_taxonomy_canonical.csv`

## Quality Summary

| Metric | Value |
| --- | ---: |
| Game docs missing selected overall stats | {summary['quality']['game_docs_missing_overall_stats']} |
| Game docs missing reliable mechanics | {summary['quality']['game_docs_missing_reliable_mechanics']} |
| Game docs marked needs review | {summary['quality']['game_docs_needs_review']} |
| Taxonomy rows excluded from RAG text because canonical review is required | {summary['quality']['taxonomy_review_rows_excluded']} |

## Notes

- Phase 5 uses only intermediate tables and does not scan the 26M row rating/review file.
- `game_overview` docs are one per game entity.
- `mechanic_profile` docs are one per canonical mechanic after excluding labels marked `canonical_needs_review=true`.
- Preview files contain the highest-quality/top-ranked examples for manual text inspection.
"""
    REPORT.write_text(text, encoding="utf-8")


def file_info(path: Path, rows: int) -> dict[str, Any]:
    return {"path": path.relative_to(ROOT).as_posix(), "rows": rows, "bytes": path.stat().st_size}


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Phase 5 RAG JSONL samples.")
    parser.add_argument("--preview-size", type=int, default=PREVIEW_SIZE_DEFAULT)
    parser.add_argument("--preview-only", action="store_true", help="Write only preview files and reports.")
    parser.add_argument("--no-manifest-update", action="store_true")
    args = parser.parse_args()

    SAMPLES_RAG.mkdir(parents=True, exist_ok=True)
    RAW_INDEX.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now().replace(microsecond=0).isoformat()
    games = load_games()
    stats = load_best_overall_stats()
    taxonomy, source_counts, tax_sources, review_counts = load_taxonomy()

    game_docs = build_game_docs(games, stats, taxonomy, tax_sources, generated_at)
    mechanic_docs = build_mechanic_docs(games, stats, taxonomy, source_counts, generated_at)

    preview_games = sorted(
        game_docs,
        key=lambda row: rating_sort_key(row["game_id"], stats),
        reverse=True,
    )[: args.preview_size]
    preview_mechanics = mechanic_docs[: args.preview_size]

    write_jsonl(GAME_OVERVIEW_PREVIEW, preview_games)
    write_jsonl(MECHANIC_PROFILE_PREVIEW, preview_mechanics)
    if not args.preview_only:
        stream_jsonl(GAME_OVERVIEW, game_docs)
        stream_jsonl(MECHANIC_PROFILE, mechanic_docs)
    else:
        write_jsonl(GAME_OVERVIEW, [])
        write_jsonl(MECHANIC_PROFILE, [])

    quality = {
        "game_docs_missing_overall_stats": sum("missing_overall_stats" in row["quality_flags"] for row in game_docs),
        "game_docs_missing_reliable_mechanics": sum("missing_reliable_mechanics" in row["quality_flags"] for row in game_docs),
        "game_docs_needs_review": sum("game_needs_review" in row["quality_flags"] for row in game_docs),
        "taxonomy_review_rows_excluded": sum(review_counts.values()),
        "taxonomy_review_rows_by_type": dict(sorted(review_counts.items())),
    }
    summary = {
        "generated_at": generated_at,
        "schema_version": SCHEMA_VERSION,
        "transform_version": TRANSFORM_VERSION,
        "preview_size": args.preview_size,
        "preview_only": args.preview_only,
        "inputs": {
            "games": len(games),
            "games_with_selected_overall_stats": len(stats),
            "games_with_reliable_taxonomy": len(taxonomy),
            "mechanics": len(mechanic_docs),
        },
        "outputs": {
            "game_overview": file_info(GAME_OVERVIEW, 0 if args.preview_only else len(game_docs)),
            "game_overview_preview": file_info(GAME_OVERVIEW_PREVIEW, len(preview_games)),
            "mechanic_profile": file_info(MECHANIC_PROFILE, 0 if args.preview_only else len(mechanic_docs)),
            "mechanic_profile_preview": file_info(MECHANIC_PROFILE_PREVIEW, len(preview_mechanics)),
        },
        "quality": quality,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_report(summary)
    if not args.no_manifest_update:
        update_manifest("phase_5_rag_samples_generated" if not args.preview_only else "phase_5_rag_preview_generated")

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
