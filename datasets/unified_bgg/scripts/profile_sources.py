"""Lightweight inventory generator for unified_bgg.

This script avoids loading large CSV bodies. It reuses the existing
research/datasets/_profiles JSON files and only inspects SQLite metadata.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
UNIFIED_ROOT = HERE.parents[1]
DATASETS_ROOT = UNIFIED_ROOT.parent
PROFILES_ROOT = DATASETS_ROOT / "_profiles"

SOURCE_META: dict[str, dict[str, str]] = {
    "bgg-reviews-jvanelteren": {
        "snapshot": "2025-02 plus historical files 2020-08-19/2022-01-08",
        "license": "Other",
        "role": "Primary source for 2025 metadata, 26.2M ratings, and review text",
    },
    "bgg-threnjen": {
        "snapshot": "2021-12",
        "license": "CC BY-SA 3.0",
        "role": "Primary source for normalized user ratings and wide taxonomy/entity matrices",
    },
    "bgg-gabrio": {
        "snapshot": "2017-06",
        "license": "Other",
        "role": "Supplement for SQLite coverage, expansions, historical descriptions, and 2017 mechanisms",
    },
    "bgg-ranked-mattadamhouser": {
        "snapshot": "2023-08",
        "license": "CC0",
        "role": "Supplement for Top-2000 ranked games, 2023 mechanisms, and reimplementations",
    },
    "bgg-mrpantherson": {
        "snapshot": "2017-04 / 2018-01 / 2018-06",
        "license": "CC0",
        "role": "Specialized source for rating/ranking drift across homogeneous Top-5000 snapshots",
    },
    "bgg-andrewmvd": {
        "snapshot": "2021-02",
        "license": "CC BY 4.0",
        "role": "Lightweight baseline and cross-check source",
    },
    "bgg-sujaykapadnis": {
        "snapshot": "2017 derived subset",
        "license": "Other",
        "role": "Demo/cross-reference only; strict subset of bgg-gabrio, not independent evidence",
    },
}


def human_size(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024
    return f"{num_bytes} B"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def profile_lookup() -> dict[tuple[str, str], dict[str, Any]]:
    lookup: dict[tuple[str, str], dict[str, Any]] = {}
    if not PROFILES_ROOT.exists():
        return lookup
    for path in PROFILES_ROOT.glob("*.json"):
        if path.name.startswith("_") or path.name.endswith(".digest.json"):
            continue
        if path.name in {"kaggle_meta.json", "reviews_facts.json", "user_ratings_facts.json"}:
            continue
        try:
            data = read_json(path)
        except Exception as exc:
            data = {"profile_error": str(exc)}
        dataset = data.get("dataset")
        file_name = data.get("file")
        if dataset and file_name:
            lookup[(dataset, file_name)] = data
    return lookup


def quote_ident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def sqlite_summary(path: Path) -> list[dict[str, Any]]:
    tables: list[dict[str, Any]] = []
    con = sqlite3.connect(path)
    try:
        cur = con.cursor()
        rows = list(cur.execute("select name, type from sqlite_master where type in ('table','view') order by name"))
        for name, kind in rows:
            row_count = cur.execute(f"SELECT COUNT(*) FROM {quote_ident(name)}").fetchone()[0]
            columns = cur.execute(f"PRAGMA table_info({quote_ident(name)})").fetchall()
            tables.append({
                "name": name,
                "type": kind,
                "rows": row_count,
                "n_columns": len(columns),
                "columns_preview": [col[1] for col in columns[:12]],
            })
    finally:
        con.close()
    return tables


def collect_inventory() -> dict[str, Any]:
    profiles = profile_lookup()
    datasets: list[dict[str, Any]] = []
    for dataset_dir in sorted(DATASETS_ROOT.iterdir()):
        if not dataset_dir.is_dir():
            continue
        if dataset_dir.name.startswith("_") or dataset_dir.name == "unified_bgg":
            continue
        files: list[dict[str, Any]] = []
        for file_path in sorted(dataset_dir.rglob("*")):
            if not file_path.is_file():
                continue
            rel = file_path.relative_to(DATASETS_ROOT).as_posix()
            profile = profiles.get((dataset_dir.name, file_path.name), {})
            entry: dict[str, Any] = {
                "path": rel,
                "file": file_path.name,
                "bytes": file_path.stat().st_size,
                "size": human_size(file_path.stat().st_size),
                "suffix": file_path.suffix.lower(),
            }
            for key in ["encoding", "delimiter", "n_columns", "rows_scanned", "scan_truncated", "ragged_rows", "error"]:
                if key in profile:
                    entry[key] = profile[key]
            if file_path.suffix.lower() in {".sqlite", ".db"}:
                entry["sqlite_tables"] = sqlite_summary(file_path)
            files.append(entry)
        datasets.append({
            "dataset": dataset_dir.name,
            "meta": SOURCE_META.get(dataset_dir.name, {}),
            "file_count": len(files),
            "bytes": sum(item["bytes"] for item in files),
            "size": human_size(sum(item["bytes"] for item in files)),
            "files": files,
        })
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "datasets_root": DATASETS_ROOT.as_posix(),
        "dataset_count": len(datasets),
        "total_bytes": sum(item["bytes"] for item in datasets),
        "total_size": human_size(sum(item["bytes"] for item in datasets)),
        "datasets": datasets,
    }


def md_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def render_inventory_md(inv: dict[str, Any]) -> str:
    lines = [
        "# Dataset Inventory",
        "",
        f"Generated at: `{inv['generated_at']}`",
        f"Source root: `{inv['datasets_root']}`",
        f"Summary: {inv['dataset_count']} datasets, {inv['total_size']}.",
        "",
        "## Dataset Summary",
        "",
        "| Dataset | Files | Size | Snapshot | License | Role |",
        "|---|---:|---:|---|---|---|",
    ]
    for ds in inv["datasets"]:
        meta = ds.get("meta", {})
        lines.append(
            f"| `{md_escape(ds['dataset'])}` | {ds['file_count']} | {ds['size']} | "
            f"{md_escape(meta.get('snapshot'))} | {md_escape(meta.get('license'))} | {md_escape(meta.get('role'))} |"
        )
    lines += ["", "## Files", ""]
    for ds in inv["datasets"]:
        lines += [f"### `{ds['dataset']}`", "", "| File | Size | Rows/scanned rows | Columns | Encoding | Delimiter | Notes |", "|---|---:|---:|---:|---|---|---|"]
        for item in ds["files"]:
            rows = item.get("rows_scanned", "")
            if item.get("scan_truncated"):
                rows = f">= {rows} (truncated profile)"
            if "sqlite_tables" in item:
                rows = "; ".join(f"{t['name']}={t['rows']}" for t in item["sqlite_tables"])
            note = ""
            if item.get("error"):
                note = f"profile error: {item['error']}"
            elif item["file"].upper() == "DATASET.MD":
                note = "source documentation"
            lines.append(
                f"| `{md_escape(item['path'])}` | {item['size']} | {md_escape(rows)} | "
                f"{md_escape(item.get('n_columns', ''))} | {md_escape(item.get('encoding', ''))} | "
                f"{md_escape(item.get('delimiter', ''))} | {md_escape(note)} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_profile_md(inv: dict[str, Any]) -> str:
    lines = [
        "# Profiling Report",
        "",
        "This report is generated by `scripts/profile_sources.py` from existing `_profiles/*.json` files and SQLite metadata. It is lightweight and does not reread large CSV files in full.",
        "",
        "## Key observations",
        "",
        "- The largest file is `bgg-reviews-jvanelteren/raw/bgg-26m-reviews.csv`; its existing profile scans only the first 3,000,000 rows.",
        "- `bgg-26m-reviews.csv` is ordered by game, so `nrows` is not an unbiased sample.",
        "- `bgg-threnjen/raw/user_ratings.csv` has a full profile with 18,942,215 rows and is the best collaborative-filtering rating matrix.",
        "- `bgg-gabrio/raw/database.sqlite` should be processed with SQLite queries, not CSV profiling.",
        "- Mechanic vocabularies differ by snapshot: 2021 threnjen has 157 mechanism columns, 2023 matt has 188, and 2025 jvanelteren is the canonical candidate.",
        "",
        "## Structured files",
        "",
        "| Dataset | File | Rows/scanned rows | Columns | Encoding | Delimiter |",
        "|---|---|---:|---:|---|---|",
    ]
    for ds in inv["datasets"]:
        for item in ds["files"]:
            if item["suffix"] not in {".csv", ".sqlite", ".db"}:
                continue
            rows = item.get("rows_scanned", "")
            cols = item.get("n_columns", "")
            if item.get("scan_truncated"):
                rows = f">= {rows}"
            if "sqlite_tables" in item:
                rows = "; ".join(f"{t['name']}={t['rows']}" for t in item["sqlite_tables"])
                cols = "; ".join(f"{t['name']}={t['n_columns']}" for t in item["sqlite_tables"])
            lines.append(
                f"| `{ds['dataset']}` | `{item['file']}` | {md_escape(rows)} | {md_escape(cols)} | "
                f"{md_escape(item.get('encoding', ''))} | {md_escape(item.get('delimiter', ''))} |"
            )
    lines += [
        "",
        "## Next profiling tasks",
        "",
        "1. Add chunked full-file stats for `bgg-26m-reviews.csv`: non-empty comment rate, user count, game count, rating range, and anomalous ratings.",
        "2. Profile every ID column for uniqueness, nulls, and cross-source intersections; then generate the first `id_map`.",
        "3. Generate taxonomy vocabulary diffs and prepare `taxonomy_aliases`.",
        "4. Generate sentinel-value reports for ratings, player counts, playtime, ranks, and weights.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    inv = collect_inventory()
    (UNIFIED_ROOT / "docs").mkdir(exist_ok=True)
    (UNIFIED_ROOT / "raw_index").mkdir(exist_ok=True)
    (UNIFIED_ROOT / "raw_index" / "source_files.json").write_text(
        json.dumps(inv, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (UNIFIED_ROOT / "docs" / "dataset_inventory.md").write_text(render_inventory_md(inv), encoding="utf-8")
    (UNIFIED_ROOT / "docs" / "profiling_report.md").write_text(render_profile_md(inv), encoding="utf-8")
    print(f"Wrote inventory for {inv['dataset_count']} datasets ({inv['total_size']}).")


if __name__ == "__main__":
    main()
