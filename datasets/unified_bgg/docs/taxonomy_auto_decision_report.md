# Taxonomy Auto Decision Report

Generated at: `2026-08-26T09:25:33`

## Purpose

The user chose not to do manual taxonomy review. Phase 7 therefore applies conservative automatic merge/keep/split decisions based on label semantics and the 2025 BGG vocabulary.

## Decision Policy

- Merge only when the legacy label has a clear one-to-one modern equivalent.
- Split only when the legacy label is explicitly a compound of modern labels.
- Keep broad legacy labels when source rows do not contain enough information to infer a more specific modern label.
- Keep unmapped legacy `family` labels as non-blocking facets because family vocabulary changes frequently and many old family labels remain useful.

## Explicit Mechanic Decisions

| Raw label | Action | Canonical target(s) | Strategy | Reason |
|---|---|---|---|---|
| `Acting / Singing / Rock-Paper-Scissors` | `split` | `Acting`, `Singing`, `Rock-Paper-Scissors` | `auto_split_legacy_combo` | Legacy mixed party-game label can be represented by three newer explicit mechanisms. |
| `Action / Movement Programming` | `split` | `Action Queue`, `Programmed Movement` | `auto_split_legacy_combo` | Legacy compound label corresponds to two newer explicit BGG mechanisms. |
| `Card Drafting` | `keep` | `Card Drafting` | `auto_keep_legacy_broad_mechanic` | Legacy broad label; cannot infer Open Drafting vs Closed Drafting from source rows. |
| `Dexterity` | `keep` | `Dexterity` | `auto_keep_legacy_broad_mechanic` | Legacy broad dexterity label is broader than any single 2025 physical submechanism. |
| `Different Worker Types` | `merge` | `Worker Placement, Different Worker Types` | `auto_merge_2025_equivalent` | Legacy shorthand maps to the explicit 2025 worker-placement mechanism. |
| `Drafting` | `merge` | `Card Drafting` | `auto_merge_legacy_synonym` | Older generic drafting label is consolidated into the legacy broad Card Drafting label. |
| `Multiple-Lot Auction` | `merge` | `Auction: Multiple Lot` | `auto_merge_2025_equivalent` | Legacy hyphenated auction label maps to the explicit 2025 auction subtype. |
| `Physical` | `merge` | `Dexterity` | `auto_merge_legacy_synonym` | Legacy physical-skill label is semantically closest to the broad Dexterity mechanism. |
| `TableauBuilding` | `merge` | `Tableau Building` | `auto_normalize_legacy_label` | CamelCase spelling normalized to a readable legacy canonical label. |
| `Time Track` | `merge` | `Turn Order: Time Track` | `auto_merge_2025_equivalent` | Old BGG Time Track mechanism maps to the newer turn-order time-track mechanism. |

## Aggregate Impact

| Metric | Value |
|---|---:|
| Alias rows | 15149 |
| Canonical rows | 1162257 |
| Invalid label rows excluded | 3852 |
| Canonical rows with needs_review=false | 1162257 |

## Override Resource

- `intermediate/taxonomy_alias_overrides.csv` records the explicit automatic mechanic decisions and the blanket legacy-family keep policy.
- `intermediate/taxonomy_aliases.csv` records the resolved mapping for each `(taxonomy_type, raw_snapshot, raw_name)` alias row.
- `intermediate/game_taxonomy_canonical.csv` materializes split decisions as multiple canonical rows.
