"""Build ID profiles and an initial BGG entity alignment map.

Phase 2 stays lightweight: it scans metadata and taxonomy files that expose BGG
IDs directly, but skips large row-level rating/review files by default.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sqlite3
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

HERE = Path(__file__).resolve()
UNIFIED_ROOT = HERE.parents[1]
DATASETS_ROOT = UNIFIED_ROOT.parent
RAW_INDEX = UNIFIED_ROOT / "raw_index"
INTERMEDIATE = UNIFIED_ROOT / "intermediate"
DOCS = UNIFIED_ROOT / "docs"

REFERENCE_LABEL = "bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:id"


@dataclass(frozen=True)
class SourceSpec:
    dataset: str
    file: str
    id_column: str
    name_column: str | None = None
    year_column: str | None = None
    type_column: str | None = None
    encoding: str = "utf-8-sig"
    delimiter: str = ","
    kind: str = "csv"
    table: str | None = None
    snapshot_date: str = "unknown"
    id_role: str = "primary"
    include_in_id_map: bool = True
    skip_reason: str | None = None

    @property
    def path(self) -> Path:
        return DATASETS_ROOT / self.dataset / self.file

    @property
    def rel_path(self) -> str:
        return f"{self.dataset}/{self.file.replace(chr(92), '/')}"

    @property
    def label(self) -> str:
        return f"{self.rel_path}:{self.id_column}"


SOURCE_SPECS: list[SourceSpec] = [
    SourceSpec("bgg-reviews-jvanelteren", "raw/games_detailed_info2025.csv", "id", "name", "yearpublished", "type", snapshot_date="2025-02"),
    SourceSpec("bgg-reviews-jvanelteren", "raw/games_detailed_info.csv", "id", "primary", "yearpublished", "type", snapshot_date="2020-08-19"),
    SourceSpec("bgg-reviews-jvanelteren", "raw/2022-01-08.csv", "ID", "Name", "Year", snapshot_date="2022-01-08"),
    SourceSpec("bgg-reviews-jvanelteren", "raw/2020-08-19.csv", "ID", "Name", "Year", snapshot_date="2020-08-19"),
    SourceSpec(
        "bgg-reviews-jvanelteren",
        "raw/bgg-26m-reviews.csv",
        "ID",
        "name",
        snapshot_date="2025-02",
        include_in_id_map=False,
        skip_reason="large row-level review file; use --include-large to scan",
    ),
    SourceSpec("bgg-threnjen", "raw/games.csv", "BGGId", "Name", "YearPublished", snapshot_date="2021-12"),
    SourceSpec("bgg-threnjen", "raw/mechanics.csv", "BGGId", snapshot_date="2021-12", id_role="taxonomy_matrix"),
    SourceSpec("bgg-threnjen", "raw/themes.csv", "BGGId", snapshot_date="2021-12", id_role="taxonomy_matrix"),
    SourceSpec("bgg-threnjen", "raw/subcategories.csv", "BGGId", snapshot_date="2021-12", id_role="taxonomy_matrix"),
    SourceSpec("bgg-threnjen", "raw/ratings_distribution.csv", "BGGId", snapshot_date="2021-12", id_role="rating_distribution"),
    SourceSpec(
        "bgg-threnjen",
        "raw/user_ratings.csv",
        "BGGId",
        snapshot_date="2021-12",
        id_role="row_level_ratings",
        include_in_id_map=False,
        skip_reason="large row-level rating file; use --include-large to scan",
    ),
    SourceSpec("bgg-ranked-mattadamhouser", "raw/basic_data_2023.csv", "game_id", "name", "year", snapshot_date="2023-08"),
    SourceSpec("bgg-ranked-mattadamhouser", "raw/mechanisms_2023.csv", "game_id", snapshot_date="2023-08", id_role="taxonomy_matrix"),
    SourceSpec("bgg-ranked-mattadamhouser", "raw/themes_2023.csv", "game_id", snapshot_date="2023-08", id_role="taxonomy_matrix"),
    SourceSpec("bgg-ranked-mattadamhouser", "raw/subdomains_2023.csv", "game_id", snapshot_date="2023-08", id_role="taxonomy_matrix"),
    SourceSpec("bgg-ranked-mattadamhouser", "raw/reimplementations_2023.csv", "game_id", year_column="year", snapshot_date="2023-08", id_role="relation_child"),
    SourceSpec("bgg-ranked-mattadamhouser", "raw/reimplementations_2023.csv", "parent_id", snapshot_date="2023-08", id_role="relation_parent"),
    SourceSpec("bgg-mrpantherson", "raw/bgg_db_2017_04.csv", "game_id", "names", "year", encoding="cp1252", snapshot_date="2017-04"),
    SourceSpec("bgg-mrpantherson", "raw/bgg_db_2018_01.csv", "game_id", "names", "year", encoding="cp1252", snapshot_date="2018-01"),
    SourceSpec("bgg-mrpantherson", "raw/bgg_db_1806.csv", "game_id", "names", "year", snapshot_date="2018-06"),
    SourceSpec("bgg-andrewmvd", "raw/bgg_dataset.csv", "ID", "Name", "Year Published", delimiter=";", snapshot_date="2021-02"),
    SourceSpec("bgg-sujaykapadnis", "raw/board_games.csv", "game_id", "name", "year_published", snapshot_date="2017-derived"),
    SourceSpec("bgg-gabrio", "raw/database.sqlite", "game.id", "details.name", "details.yearpublished", "game.type", kind="sqlite", table="BoardGames", snapshot_date="2017-06"),
]


def clean_id(value: Any) -> int | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if re.fullmatch(r"[+-]?\d+", text):
        result = int(text)
    elif re.fullmatch(r"[+-]?\d+\.0+", text):
        result = int(float(text))
    else:
        return None
    return result if result > 0 else None


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def clean_year(value: Any) -> str:
    text = clean_text(value)
    if not text:
        return ""
    if re.fullmatch(r"-?\d+", text):
        return text
    if re.fullmatch(r"-?\d+\.0+", text):
        return str(int(float(text)))
    return text


def normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.casefold())


def quote_ident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def iter_csv_rows(spec: SourceSpec) -> Iterable[dict[str, str]]:
    with spec.path.open("r", encoding=spec.encoding, newline="") as handle:
        reader = csv.DictReader(handle, delimiter=spec.delimiter)
        missing = [col for col in [spec.id_column, spec.name_column, spec.year_column, spec.type_column] if col and col not in (reader.fieldnames or [])]
        if missing:
            raise KeyError(f"Missing columns {missing} in {spec.rel_path}; found {reader.fieldnames}")
        yield from reader


def iter_sqlite_rows(spec: SourceSpec) -> Iterable[dict[str, Any]]:
    if not spec.table:
        raise ValueError(f"SQLite source needs table: {spec.label}")
    columns = [spec.id_column]
    for col in [spec.name_column, spec.year_column, spec.type_column]:
        if col and col not in columns:
            columns.append(col)
    select_cols = ", ".join(f"{quote_ident(col)} AS {quote_ident(col)}" for col in columns)
    query = f"SELECT {select_cols} FROM {quote_ident(spec.table)}"
    con = sqlite3.connect(spec.path)
    con.row_factory = sqlite3.Row
    try:
        for row in con.execute(query):
            yield dict(row)
    finally:
        con.close()


def iter_rows(spec: SourceSpec) -> Iterable[dict[str, Any]]:
    if spec.kind == "sqlite":
        yield from iter_sqlite_rows(spec)
    else:
        yield from iter_csv_rows(spec)


def profile_source(spec: SourceSpec, include_large: bool) -> tuple[dict[str, Any], dict[int, dict[str, Any]]]:
    if spec.skip_reason and not include_large:
        return {
            "label": spec.label,
            "dataset": spec.dataset,
            "source_file": spec.rel_path,
            "id_column": spec.id_column,
            "id_role": spec.id_role,
            "snapshot_date": spec.snapshot_date,
            "scanned": False,
            "skip_reason": spec.skip_reason,
        }, {}

    ids: dict[int, dict[str, Any]] = {}
    total_rows = 0
    missing_id_rows = 0
    invalid_id_rows = 0
    nonempty_name_rows = 0
    year_values: list[int] = []
    type_counts: Counter[str] = Counter()

    for row in iter_rows(spec):
        total_rows += 1
        raw_id = clean_text(row.get(spec.id_column))
        bgg_id = clean_id(raw_id)
        if raw_id == "":
            missing_id_rows += 1
            continue
        if bgg_id is None:
            invalid_id_rows += 1
            continue

        name = clean_text(row.get(spec.name_column)) if spec.name_column else ""
        year = clean_year(row.get(spec.year_column)) if spec.year_column else ""
        game_type = clean_text(row.get(spec.type_column)) if spec.type_column else ""
        if name:
            nonempty_name_rows += 1
        if year and re.fullmatch(r"-?\d+", year):
            year_values.append(int(year))
        if game_type:
            type_counts[game_type] += 1

        item = ids.setdefault(
            bgg_id,
            {
                "bgg_id": bgg_id,
                "source_game_id": raw_id,
                "names": Counter(),
                "years": Counter(),
                "types": Counter(),
                "row_count": 0,
            },
        )
        item["row_count"] += 1
        if name:
            item["names"][name] += 1
        if year:
            item["years"][year] += 1
        if game_type:
            item["types"][game_type] += 1

    valid_id_rows = total_rows - missing_id_rows - invalid_id_rows
    profile = {
        "label": spec.label,
        "dataset": spec.dataset,
        "source_file": spec.rel_path,
        "id_column": spec.id_column,
        "id_role": spec.id_role,
        "snapshot_date": spec.snapshot_date,
        "scanned": True,
        "rows": total_rows,
        "valid_id_rows": valid_id_rows,
        "unique_valid_ids": len(ids),
        "duplicate_id_rows": max(0, valid_id_rows - len(ids)),
        "missing_id_rows": missing_id_rows,
        "invalid_id_rows": invalid_id_rows,
        "nonempty_name_rows": nonempty_name_rows,
        "min_bgg_id": min(ids) if ids else None,
        "max_bgg_id": max(ids) if ids else None,
        "min_year": min(year_values) if year_values else None,
        "max_year": max(year_values) if year_values else None,
        "type_counts": dict(type_counts),
    }
    return profile, ids


def choose_counter_value(counter: Counter[str]) -> str:
    if not counter:
        return ""
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def serializable_ids(ids_by_label: dict[str, dict[int, dict[str, Any]]]) -> dict[str, Any]:
    return {label: sorted(ids) for label, ids in ids_by_label.items()}


def build_id_map(specs: list[SourceSpec], ids_by_label: dict[str, dict[int, dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in specs:
        ids = ids_by_label.get(spec.label, {})
        if not ids:
            continue
        for bgg_id, data in sorted(ids.items()):
            rows.append({
                "game_id": f"bgg:{bgg_id}",
                "bgg_id": bgg_id,
                "source_dataset": spec.dataset,
                "source_file": spec.rel_path,
                "source_id_column": spec.id_column,
                "id_role": spec.id_role,
                "source_game_id": data["source_game_id"],
                "source_name": choose_counter_value(data["names"]),
                "source_year": choose_counter_value(data["years"]),
                "source_type": choose_counter_value(data["types"]),
                "snapshot_date": spec.snapshot_date,
                "match_method": "bgg_id_exact",
                "match_confidence": "1.0",
                "needs_review": "false",
                "row_count_in_source": data["row_count"],
            })
    return rows


def dataset_unions(specs: list[SourceSpec], ids_by_label: dict[str, dict[int, dict[str, Any]]]) -> dict[str, set[int]]:
    unions: dict[str, set[int]] = defaultdict(set)
    for spec in specs:
        ids = ids_by_label.get(spec.label)
        if ids:
            unions[spec.dataset].update(ids)
    return dict(unions)


def build_coverage(profiles: list[dict[str, Any]], ids_by_label: dict[str, dict[int, dict[str, Any]]]) -> list[dict[str, Any]]:
    reference_ids = set(ids_by_label.get(REFERENCE_LABEL, {}))
    rows: list[dict[str, Any]] = []
    for profile in profiles:
        ids = set(ids_by_label.get(profile["label"], {}))
        row = dict(profile)
        if ids and reference_ids:
            overlap = len(ids & reference_ids)
            row["overlap_with_reference"] = overlap
            row["pct_of_source_in_reference"] = round(overlap * 100 / len(ids), 2)
            row["ids_not_in_reference"] = len(ids - reference_ids)
            row["reference_ids_missing_from_source"] = len(reference_ids - ids)
        rows.append(row)
    return rows


def build_name_conflicts(specs: list[SourceSpec], ids_by_label: dict[str, dict[int, dict[str, Any]]]) -> list[dict[str, Any]]:
    names_by_id: dict[int, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for spec in specs:
        for bgg_id, data in ids_by_label.get(spec.label, {}).items():
            for name in data["names"]:
                if name:
                    names_by_id[bgg_id][normalize_name(name)].append(f"{spec.rel_path}:{name}")

    conflicts: list[dict[str, Any]] = []
    for bgg_id, variants in names_by_id.items():
        if len(variants) <= 1:
            continue
        raw_variants = []
        for items in variants.values():
            raw_variants.extend(items[:3])
        conflicts.append({
            "bgg_id": bgg_id,
            "game_id": f"bgg:{bgg_id}",
            "normalized_variant_count": len(variants),
            "examples": sorted(raw_variants)[:12],
        })
    conflicts.sort(key=lambda item: (-item["normalized_variant_count"], item["bgg_id"]))
    return conflicts


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def pct(num: int, denom: int) -> str:
    if denom == 0:
        return ""
    return f"{num * 100 / denom:.2f}%"


def md_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def render_report(
    generated_at: str,
    profiles: list[dict[str, Any]],
    ids_by_label: dict[str, dict[int, dict[str, Any]]],
    dataset_sets: dict[str, set[int]],
    id_map_rows: list[dict[str, Any]],
    conflicts: list[dict[str, Any]],
) -> str:
    reference_ids = set(ids_by_label.get(REFERENCE_LABEL, {}))
    union_all: set[int] = set()
    for ids in dataset_sets.values():
        union_all.update(ids)

    lines = [
        "# ID Profile Report",
        "",
        f"Generated at: `{generated_at}`",
        "",
        "## Summary",
        "",
        f"- Scanned source ID columns: {sum(1 for p in profiles if p.get('scanned'))}.",
        f"- Skipped large row-level files: {sum(1 for p in profiles if not p.get('scanned'))}.",
        f"- Union of scanned BGG IDs: {len(union_all)}.",
        f"- Initial `id_map.csv` rows: {len(id_map_rows)}.",
        f"- Reference set `{REFERENCE_LABEL}` IDs: {len(reference_ids)}.",
        f"- Possible name-conflict IDs: {len(conflicts)}.",
        "",
        "## Source ID Profiles",
        "",
        "| Source | Role | Rows | Valid ID rows | Unique IDs | Missing IDs | Invalid IDs | Duplicate ID rows | Reference overlap | Not in reference |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for p in profiles:
        if not p.get("scanned"):
            lines.append(
                f"| `{md_escape(p['label'])}` | {md_escape(p.get('id_role'))} | skipped |  |  |  |  |  |  | {md_escape(p.get('skip_reason'))} |"
            )
            continue
        overlap = p.get("overlap_with_reference", "")
        overlap_text = f"{overlap} ({p.get('pct_of_source_in_reference')}%)" if overlap != "" else ""
        lines.append(
            f"| `{md_escape(p['label'])}` | {md_escape(p.get('id_role'))} | {p.get('rows')} | {p.get('valid_id_rows')} | {p.get('unique_valid_ids')} | "
            f"{p.get('missing_id_rows')} | {p.get('invalid_id_rows')} | {p.get('duplicate_id_rows')} | {overlap_text} | {p.get('ids_not_in_reference', '')} |"
        )

    lines += [
        "",
        "## Dataset-Level Coverage",
        "",
        "| Dataset | Unique scanned IDs | In 2025 reference | Percent in reference | IDs not in reference | 2025 IDs missing from dataset |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for dataset, ids in sorted(dataset_sets.items()):
        overlap = len(ids & reference_ids) if reference_ids else 0
        lines.append(
            f"| `{dataset}` | {len(ids)} | {overlap} | {pct(overlap, len(ids))} | {len(ids - reference_ids)} | {len(reference_ids - ids) if reference_ids else ''} |"
        )

    lines += [
        "",
        "## Dataset Pairwise Intersections",
        "",
        "| Dataset A | Dataset B | Intersection | A coverage | B coverage |",
        "|---|---|---:|---:|---:|",
    ]
    items = sorted(dataset_sets.items())
    for i, (a_name, a_ids) in enumerate(items):
        for b_name, b_ids in items[i + 1 :]:
            inter = len(a_ids & b_ids)
            lines.append(f"| `{a_name}` | `{b_name}` | {inter} | {pct(inter, len(a_ids))} | {pct(inter, len(b_ids))} |")

    lines += [
        "",
        "## Possible Name Conflicts",
        "",
        "These are not necessarily errors. BGG titles can change over time, and some sources use alternate or older names.",
        "",
        "| BGG ID | Variant count | Examples |",
        "|---:|---:|---|",
    ]
    for item in conflicts[:25]:
        examples = "; ".join(item["examples"][:6])
        lines.append(f"| {item['bgg_id']} | {item['normalized_variant_count']} | {md_escape(examples)} |")

    lines += [
        "",
        "## Outputs",
        "",
        "- `raw_index/id_profiles.json`: source-level ID stats and reference coverage.",
        "- `raw_index/id_sets.json`: scanned BGG ID sets by source label.",
        "- `raw_index/name_conflicts.json`: possible same-ID name variants.",
        "- `intermediate/id_map.csv`: initial source-to-`bgg:{id}` alignment rows.",
        "- `intermediate/dataset_id_coverage.csv`: dataset-level coverage against the 2025 reference.",
        "",
        "## Next Steps",
        "",
        "1. Review possible name conflicts and decide whether any require manual alias rows.",
        "2. Decide whether to run `build_id_map.py --include-large` to scan row-level rating/review files.",
        "3. Start `games`, `game_stats`, and `game_taxonomy` transforms using this `id_map.csv`.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build ID profiles and initial id_map for unified_bgg.")
    parser.add_argument("--include-large", action="store_true", help="Also scan row-level rating/review files.")
    args = parser.parse_args()

    generated_at = datetime.now().isoformat(timespec="seconds")
    profiles: list[dict[str, Any]] = []
    ids_by_label: dict[str, dict[int, dict[str, Any]]] = {}

    for spec in SOURCE_SPECS:
        profile, ids = profile_source(spec, include_large=args.include_large)
        profiles.append(profile)
        if ids:
            ids_by_label[spec.label] = ids

    coverage_profiles = build_coverage(profiles, ids_by_label)
    dataset_sets = dataset_unions(SOURCE_SPECS, ids_by_label)
    id_map_rows = build_id_map(SOURCE_SPECS, ids_by_label)
    conflicts = build_name_conflicts(SOURCE_SPECS, ids_by_label)

    RAW_INDEX.mkdir(parents=True, exist_ok=True)
    INTERMEDIATE.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    (RAW_INDEX / "id_profiles.json").write_text(
        json.dumps({"generated_at": generated_at, "profiles": coverage_profiles}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (RAW_INDEX / "id_sets.json").write_text(
        json.dumps({"generated_at": generated_at, "ids_by_source": serializable_ids(ids_by_label)}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (RAW_INDEX / "name_conflicts.json").write_text(
        json.dumps({"generated_at": generated_at, "conflicts": conflicts}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    id_map_fields = [
        "game_id",
        "bgg_id",
        "source_dataset",
        "source_file",
        "source_id_column",
        "id_role",
        "source_game_id",
        "source_name",
        "source_year",
        "source_type",
        "snapshot_date",
        "match_method",
        "match_confidence",
        "needs_review",
        "row_count_in_source",
    ]
    write_csv(INTERMEDIATE / "id_map.csv", id_map_rows, id_map_fields)

    reference_ids = set(ids_by_label.get(REFERENCE_LABEL, {}))
    coverage_rows = []
    for dataset, ids in sorted(dataset_sets.items()):
        overlap = len(ids & reference_ids) if reference_ids else 0
        coverage_rows.append({
            "dataset": dataset,
            "unique_scanned_ids": len(ids),
            "in_reference_2025": overlap,
            "pct_in_reference_2025": f"{overlap * 100 / len(ids):.2f}" if ids else "",
            "ids_not_in_reference_2025": len(ids - reference_ids) if reference_ids else "",
            "reference_2025_ids_missing_from_dataset": len(reference_ids - ids) if reference_ids else "",
        })
    write_csv(
        INTERMEDIATE / "dataset_id_coverage.csv",
        coverage_rows,
        [
            "dataset",
            "unique_scanned_ids",
            "in_reference_2025",
            "pct_in_reference_2025",
            "ids_not_in_reference_2025",
            "reference_2025_ids_missing_from_dataset",
        ],
    )

    report = render_report(generated_at, coverage_profiles, ids_by_label, dataset_sets, id_map_rows, conflicts)
    (DOCS / "id_profile_report.md").write_text(report, encoding="utf-8")

    print(f"Wrote {len(id_map_rows)} id_map rows from {len(ids_by_label)} scanned source columns.")
    print(f"Union IDs: {len(set().union(*dataset_sets.values())) if dataset_sets else 0}; conflicts: {len(conflicts)}")


if __name__ == "__main__":
    main()
