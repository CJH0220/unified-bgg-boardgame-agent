"""Build taxonomy aliases and canonical taxonomy for unified_bgg.

Phase 4 uses the 2025 BGG vocabulary as the canonical anchor where available.
It writes:
- intermediate/taxonomy_aliases.csv
- intermediate/taxonomy_alias_overrides.csv
- intermediate/game_taxonomy_canonical.csv
- raw_index/taxonomy_profile.json
- docs/taxonomy_profile_report.md
- docs/taxonomy_auto_decision_report.md
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
INTERMEDIATE = ROOT / "intermediate"
RAW_INDEX = ROOT / "raw_index"
DOCS = ROOT / "docs"

SRC = INTERMEDIATE / "game_taxonomy.csv"
ALIASES = INTERMEDIATE / "taxonomy_aliases.csv"
OVERRIDES = INTERMEDIATE / "taxonomy_alias_overrides.csv"
CANONICAL = INTERMEDIATE / "game_taxonomy_canonical.csv"
PROFILE = RAW_INDEX / "taxonomy_profile.json"
REPORT = DOCS / "taxonomy_profile_report.md"
AUTO_DECISION_REPORT = DOCS / "taxonomy_auto_decision_report.md"

ALIAS_FIELDS = [
    "taxonomy_type",
    "raw_snapshot",
    "raw_name",
    "canonical_name",
    "canonical_targets",
    "mapping_strategy",
    "mapping_confidence",
    "needs_review",
    "auto_decision",
    "decision_reason",
    "row_count",
    "source_count",
    "sources",
]

OVERRIDE_FIELDS = [
    "taxonomy_type",
    "raw_name",
    "action",
    "canonical_targets",
    "mapping_strategy",
    "mapping_confidence",
    "needs_review",
    "decision_reason",
]

CANONICAL_EXTRA = [
    "canonical_name",
    "canonical_mapping_strategy",
    "canonical_mapping_confidence",
    "canonical_needs_review",
]

# Conservative manually curated mechanic aliases from the project notes. Ambiguous
# splits (for example Action / Movement Programming) are deliberately left for
# review unless a safe one-to-one canonical target is clear enough.
MANUAL_MECHANIC_ALIASES = {
    "Action Point Allowance System": "Action Points",
    "Area Control / Area Influence": "Area Majority / Influence",
    "Area Enclosure": "Enclosure",
    "Auction/Bidding": "Auction / Bidding",
    "Betting/Wagering": "Betting and Bluffing",
    "Co-operative Play": "Cooperative Game",
    "Deck / Pool Building": "Deck, Bag, and Pool Building",
    "Deck Bag and Pool Building": "Deck, Bag, and Pool Building",
    "Hex-and-Counter": "Hexagon Grid",
    "Partnerships": "Team-Based Game",
    "Press Your Luck": "Push Your Luck",
    "Route/Network Building": "Network and Route Building",
}

AUTO_MECHANIC_DECISIONS = {
    # The 2025 vocabulary splits drafting into open/closed variants. The legacy
    # sources do not reliably distinguish those variants, so preserve a broad
    # legacy canonical label instead of over-tagging every old row with both.
    "Card Drafting": {
        "action": "keep",
        "targets": ["Card Drafting"],
        "strategy": "auto_keep_legacy_broad_mechanic",
        "confidence": "legacy_keep",
        "reason": "Legacy broad label; cannot infer Open Drafting vs Closed Drafting from source rows.",
    },
    "Drafting": {
        "action": "merge",
        "targets": ["Card Drafting"],
        "strategy": "auto_merge_legacy_synonym",
        "confidence": "auto",
        "reason": "Older generic drafting label is consolidated into the legacy broad Card Drafting label.",
    },
    "Action / Movement Programming": {
        "action": "split",
        "targets": ["Action Queue", "Programmed Movement"],
        "strategy": "auto_split_legacy_combo",
        "confidence": "auto_split",
        "reason": "Legacy compound label corresponds to two newer explicit BGG mechanisms.",
    },
    "Acting / Singing / Rock-Paper-Scissors": {
        "action": "split",
        "targets": ["Acting", "Singing", "Rock-Paper-Scissors"],
        "strategy": "auto_split_legacy_combo",
        "confidence": "auto_split",
        "reason": "Legacy mixed party-game label can be represented by three newer explicit mechanisms.",
    },
    "Dexterity": {
        "action": "keep",
        "targets": ["Dexterity"],
        "strategy": "auto_keep_legacy_broad_mechanic",
        "confidence": "legacy_keep",
        "reason": "Legacy broad dexterity label is broader than any single 2025 physical submechanism.",
    },
    "Physical": {
        "action": "merge",
        "targets": ["Dexterity"],
        "strategy": "auto_merge_legacy_synonym",
        "confidence": "auto",
        "reason": "Legacy physical-skill label is semantically closest to the broad Dexterity mechanism.",
    },
    "Time Track": {
        "action": "merge",
        "targets": ["Turn Order: Time Track"],
        "strategy": "auto_merge_2025_equivalent",
        "confidence": "auto",
        "reason": "Old BGG Time Track mechanism maps to the newer turn-order time-track mechanism.",
    },
    "TableauBuilding": {
        "action": "merge",
        "targets": ["Tableau Building"],
        "strategy": "auto_normalize_legacy_label",
        "confidence": "normalized",
        "reason": "CamelCase spelling normalized to a readable legacy canonical label.",
    },
    "Different Worker Types": {
        "action": "merge",
        "targets": ["Worker Placement, Different Worker Types"],
        "strategy": "auto_merge_2025_equivalent",
        "confidence": "auto",
        "reason": "Legacy shorthand maps to the explicit 2025 worker-placement mechanism.",
    },
    "Multiple-Lot Auction": {
        "action": "merge",
        "targets": ["Auction: Multiple Lot"],
        "strategy": "auto_merge_2025_equivalent",
        "confidence": "auto",
        "reason": "Legacy hyphenated auction label maps to the explicit 2025 auction subtype.",
    },
}

PREFERRED_REFERENCE = {
    "category": "2025-02",
    "family": "2025-02",
    "mechanic": "2025-02",
}

SELF_CANONICAL_TYPES = {"domain", "theme", "subcategory"}
INVALID_LABELS = {"", "NA", "N/A", "na", "n/a", "nan", "None"}


def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def read_rows() -> list[dict[str, str]]:
    with SRC.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def vocab_stats(rows: list[dict[str, str]]) -> tuple[dict[tuple[str, str, str], Counter[str]], Counter[tuple[str, str, str]]]:
    vocab: dict[tuple[str, str, str], Counter[str]] = defaultdict(Counter)
    row_counts: Counter[tuple[str, str, str]] = Counter()
    for row in rows:
        key = (row["taxonomy_type"], row["taxonomy_snapshot"], row["source_dataset"])
        name = row["taxonomy_name_raw"]
        vocab[key][name] += 1
        row_counts[key] += 1
    return vocab, row_counts


def build_reference(rows: list[dict[str, str]]) -> dict[str, set[str]]:
    ref: dict[str, set[str]] = defaultdict(set)
    all_names: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        typ = row["taxonomy_type"]
        name = row["taxonomy_name_raw"]
        all_names[typ].add(name)
        if PREFERRED_REFERENCE.get(typ) == row["taxonomy_snapshot"]:
            ref[typ].add(name)
    for typ in SELF_CANONICAL_TYPES:
        ref[typ] = set(all_names.get(typ, set()))
    return ref


def alias_result(
    canonical: str,
    strategy: str,
    confidence: str,
    needs_review: str,
    targets: list[str] | None = None,
    decision: str = "",
    reason: str = "",
) -> dict[str, str]:
    target_list = targets or ([canonical] if canonical else [])
    return {
        "canonical_name": canonical,
        "canonical_targets": "|".join(target_list),
        "mapping_strategy": strategy,
        "mapping_confidence": confidence,
        "needs_review": needs_review,
        "auto_decision": decision,
        "decision_reason": reason,
    }


def resolve_alias(typ: str, snapshot: str, raw_name: str, ref: dict[str, set[str]]) -> dict[str, str]:
    if raw_name in INVALID_LABELS:
        return alias_result("", "invalid_label", "invalid", "true", [], "drop", "Invalid placeholder label.")
    names = ref.get(typ, set())
    if not names:
        return alias_result(raw_name, "self_no_reference", "self", "false", decision="keep", reason="No reference vocabulary for this taxonomy type.")
    if raw_name in names:
        if snapshot == PREFERRED_REFERENCE.get(typ):
            return alias_result(raw_name, "canonical_reference_exact", "exact", "false", decision="keep", reason="Exact label in preferred reference vocabulary.")
        return alias_result(raw_name, "exact_label_match", "exact", "false", decision="keep", reason="Exact label match in reference vocabulary.")

    norm_index = {norm(name): name for name in names}
    nkey = norm(raw_name)
    if nkey in norm_index:
        return alias_result(norm_index[nkey], "normalized_label_match", "normalized", "false", decision="merge", reason="Normalized spelling matches a reference label.")

    if typ == "mechanic":
        decision = AUTO_MECHANIC_DECISIONS.get(raw_name)
        if decision:
            targets = decision["targets"]
            return alias_result(
                targets[0],
                decision["strategy"],
                decision["confidence"],
                "false",
                targets=targets,
                decision=decision["action"],
                reason=decision["reason"],
            )
        target = MANUAL_MECHANIC_ALIASES.get(raw_name)
        if target and target in names:
            return alias_result(target, "manual_alias", "manual", "false", decision="merge", reason="Curated one-to-one legacy mechanic alias.")

    if typ == "family":
        # BGG family labels are broad, fast-changing facets. A legacy family not
        # present in the 2025 reference is still useful evidence and should not
        # block downstream finetune/RAG generation as an unresolved error.
        return alias_result(
            raw_name,
            "auto_keep_legacy_family",
            "legacy_keep",
            "false",
            decision="keep",
            reason="Legacy family label is retained because family vocabulary evolves and many labels have no safe one-to-one 2025 equivalent.",
        )

    # Keep the raw name as a usable fallback, but mark it as unresolved.
    return alias_result(raw_name, "unmapped_raw_fallback", "unmapped", "true", decision="review", reason="No safe automatic mapping rule matched.")


def build_aliases(rows: list[dict[str, str]], ref: dict[str, set[str]]) -> tuple[list[dict[str, str]], dict[tuple[str, str, str], dict[str, str]]]:
    grouped: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in rows:
        key = (row["taxonomy_type"], row["taxonomy_snapshot"], row["taxonomy_name_raw"])
        item = grouped.setdefault(key, {"row_count": 0, "sources": set()})
        item["row_count"] += 1
        item["sources"].add(row["source_dataset"])

    alias_rows: list[dict[str, str]] = []
    alias_lookup: dict[tuple[str, str, str], dict[str, str]] = {}
    for (typ, snapshot, raw_name), item in sorted(grouped.items()):
        resolved = resolve_alias(typ, snapshot, raw_name, ref)
        alias = {
            "taxonomy_type": typ,
            "raw_snapshot": snapshot,
            "raw_name": raw_name,
            **resolved,
            "row_count": str(item["row_count"]),
            "source_count": str(len(item["sources"])),
            "sources": ";".join(sorted(item["sources"])),
        }
        alias_rows.append(alias)
        alias_lookup[(typ, snapshot, raw_name)] = alias
    return alias_rows, alias_lookup


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> int:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def write_canonical(rows: list[dict[str, str]], alias_lookup: dict[tuple[str, str, str], dict[str, str]]) -> int:
    if not rows:
        return 0
    fields = list(rows[0].keys()) + CANONICAL_EXTRA
    count = 0
    with CANONICAL.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            alias = alias_lookup[(row["taxonomy_type"], row["taxonomy_snapshot"], row["taxonomy_name_raw"])]
            if alias["mapping_strategy"] == "invalid_label":
                continue
            targets = [t for t in alias.get("canonical_targets", "").split("|") if t]
            if not targets:
                targets = [alias["canonical_name"]]
            for target in targets:
                out = dict(row)
                out.update({
                    "canonical_name": target,
                    "canonical_mapping_strategy": alias["mapping_strategy"],
                    "canonical_mapping_confidence": alias["mapping_confidence"],
                    "canonical_needs_review": alias["needs_review"],
                })
                writer.writerow(out)
                count += 1
    return count


def top_unmapped(alias_rows: list[dict[str, str]], typ: str, limit: int = 30) -> list[dict[str, str]]:
    rows = [r for r in alias_rows if r["taxonomy_type"] == typ and r["needs_review"] == "true" and r["mapping_strategy"] != "invalid_label"]
    return sorted(rows, key=lambda r: (-int(r["row_count"]), r["raw_snapshot"], r["raw_name"]))[:limit]


def build_override_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for raw_name, item in sorted(AUTO_MECHANIC_DECISIONS.items()):
        rows.append({
            "taxonomy_type": "mechanic",
            "raw_name": raw_name,
            "action": item["action"],
            "canonical_targets": "|".join(item["targets"]),
            "mapping_strategy": item["strategy"],
            "mapping_confidence": item["confidence"],
            "needs_review": "false",
            "decision_reason": item["reason"],
        })
    rows.append({
        "taxonomy_type": "family",
        "raw_name": "*",
        "action": "keep",
        "canonical_targets": "<raw_name>",
        "mapping_strategy": "auto_keep_legacy_family",
        "mapping_confidence": "legacy_keep",
        "needs_review": "false",
        "decision_reason": "Retain unmapped legacy family labels because family vocabulary evolves and many labels have no safe one-to-one 2025 equivalent.",
    })
    return rows


def render_report(summary: dict[str, Any]) -> str:
    lines = [
        "# Taxonomy Profile Report",
        "",
        f"Generated at: `{summary['generated_at']}`",
        "",
        "## Outputs",
        "",
        f"- `intermediate/taxonomy_aliases.csv`: {summary['alias_rows']} rows.",
        f"- `intermediate/game_taxonomy_canonical.csv`: {summary['canonical_rows']} rows.",
        "- `raw_index/taxonomy_profile.json`: machine-readable summary.",
        "",
        "## Canonical Reference",
        "",
        "- `mechanic`, `category`, and `family` use the 2025-02 jvanelteren vocabulary as the preferred reference.",
        "- `domain`, `theme`, and `subcategory` currently use self-canonical vocabularies because there is no 2025 reference table for those types in the current intermediate data.",
        "- Phase 7 applies automatic decisions for high-impact legacy mechanics and keeps unmapped legacy family labels as useful non-blocking facets.",
        "- Legacy compound mechanics can fan out to multiple canonical rows when a safe split is known.",
        "- Invalid placeholder labels such as `NA` are recorded in `taxonomy_aliases.csv` but excluded from `game_taxonomy_canonical.csv`.",
        "",
        "## Alias Strategy Counts",
        "",
        "| Strategy | Rows |",
        "|---|---:|",
    ]
    for key, value in summary["alias_strategy_counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines += ["", "## Canonical Row Counts By Review Flag", "", "| Needs review | Rows |", "|---|---:|"]
    for key, value in summary["canonical_review_counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines += ["", "## Vocabularies By Type/Snapshot/Source", "", "| Type | Snapshot | Source | Rows | Vocab size |", "|---|---|---|---:|---:|"]
    for item in summary["vocabulary_profiles"]:
        lines.append(f"| `{item['taxonomy_type']}` | `{item['snapshot']}` | `{item['source_dataset']}` | {item['rows']} | {item['vocab_size']} |")
    lines += ["", "## Top Unmapped Mechanics", "", "| Snapshot | Raw name | Rows | Sources | Reason |", "|---|---|---:|---|---|"]
    for item in summary["top_unmapped_mechanics"]:
        reason = item.get("decision_reason") or item["mapping_strategy"]
        lines.append(f"| `{item['raw_snapshot']}` | `{item['raw_name']}` | {item['row_count']} | `{item['sources']}` | {reason} |")
    lines += [
        "",
        "## Next Steps",
        "",
        "1. Rebuild RAG samples and the local FTS index after taxonomy changes.",
        "2. Use `taxonomy_alias_overrides.csv` as the durable record of automatic merge/keep/split decisions.",
        "3. Revisit only remaining `canonical_needs_review=true` rows if future sources introduce new unresolved labels.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def render_auto_decision_report(summary: dict[str, Any]) -> str:
    lines = [
        "# Taxonomy Auto Decision Report",
        "",
        f"Generated at: `{summary['generated_at']}`",
        "",
        "## Purpose",
        "",
        "The user chose not to do manual taxonomy review. Phase 7 therefore applies conservative automatic merge/keep/split decisions based on label semantics and the 2025 BGG vocabulary.",
        "",
        "## Decision Policy",
        "",
        "- Merge only when the legacy label has a clear one-to-one modern equivalent.",
        "- Split only when the legacy label is explicitly a compound of modern labels.",
        "- Keep broad legacy labels when source rows do not contain enough information to infer a more specific modern label.",
        "- Keep unmapped legacy `family` labels as non-blocking facets because family vocabulary changes frequently and many old family labels remain useful.",
        "",
        "## Explicit Mechanic Decisions",
        "",
        "| Raw label | Action | Canonical target(s) | Strategy | Reason |",
        "|---|---|---|---|---|",
    ]
    for raw_name, item in sorted(AUTO_MECHANIC_DECISIONS.items()):
        targets = ", ".join(f"`{t}`" for t in item["targets"])
        lines.append(f"| `{raw_name}` | `{item['action']}` | {targets} | `{item['strategy']}` | {item['reason']} |")
    lines += [
        "",
        "## Aggregate Impact",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Alias rows | {summary['alias_rows']} |",
        f"| Canonical rows | {summary['canonical_rows']} |",
        f"| Invalid label rows excluded | {summary['invalid_label_rows']} |",
    ]
    for key, value in summary["canonical_review_counts"].items():
        lines.append(f"| Canonical rows with needs_review={key} | {value} |")
    lines += [
        "",
        "## Override Resource",
        "",
        "- `intermediate/taxonomy_alias_overrides.csv` records the explicit automatic mechanic decisions and the blanket legacy-family keep policy.",
        "- `intermediate/taxonomy_aliases.csv` records the resolved mapping for each `(taxonomy_type, raw_snapshot, raw_name)` alias row.",
        "- `intermediate/game_taxonomy_canonical.csv` materializes split decisions as multiple canonical rows.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    generated_at = datetime.now().isoformat(timespec="seconds")
    rows = read_rows()
    vocab, row_counts = vocab_stats(rows)
    ref = build_reference(rows)
    alias_rows, alias_lookup = build_aliases(rows, ref)
    override_rows = build_override_rows()
    override_count = write_csv(OVERRIDES, override_rows, OVERRIDE_FIELDS)
    alias_count = write_csv(ALIASES, alias_rows, ALIAS_FIELDS)
    canonical_count = write_canonical(rows, alias_lookup)

    strategy_counts = Counter(r["mapping_strategy"] for r in alias_rows)
    canonical_review_counts = Counter()
    for row in rows:
        alias = alias_lookup[(row["taxonomy_type"], row["taxonomy_snapshot"], row["taxonomy_name_raw"])]
        if alias["mapping_strategy"] == "invalid_label":
            continue
        targets = [t for t in alias.get("canonical_targets", "").split("|") if t] or [alias["canonical_name"]]
        canonical_review_counts[alias["needs_review"]] += len(targets)

    vocabulary_profiles = []
    for (typ, snapshot, source), names in sorted(vocab.items()):
        vocabulary_profiles.append({
            "taxonomy_type": typ,
            "snapshot": snapshot,
            "source_dataset": source,
            "rows": row_counts[(typ, snapshot, source)],
            "vocab_size": len(names),
        })

    summary = {
        "generated_at": generated_at,
        "input_rows": len(rows),
        "alias_rows": alias_count,
        "override_rows": override_count,
        "canonical_rows": canonical_count,
        "reference_vocab_sizes": {typ: len(names) for typ, names in sorted(ref.items())},
        "alias_strategy_counts": dict(sorted(strategy_counts.items())),
        "invalid_label_rows": sum(int(r["row_count"]) for r in alias_rows if r["mapping_strategy"] == "invalid_label"),
        "canonical_review_counts": dict(sorted(canonical_review_counts.items())),
        "vocabulary_profiles": vocabulary_profiles,
        "top_unmapped_mechanics": top_unmapped(alias_rows, "mechanic", 40),
        "manual_mechanic_aliases": MANUAL_MECHANIC_ALIASES,
        "auto_mechanic_decisions": AUTO_MECHANIC_DECISIONS,
    }
    PROFILE.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(render_report(summary), encoding="utf-8")
    AUTO_DECISION_REPORT.write_text(render_auto_decision_report(summary), encoding="utf-8")
    print(f"Wrote overrides={override_count}, aliases={alias_count}, canonical_rows={canonical_count}, needs_review_rows={canonical_review_counts.get('true', 0)}")


if __name__ == "__main__":
    main()





