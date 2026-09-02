# Taxonomy Profile Report

Generated at: `2026-08-26T09:25:33`

## Outputs

- `intermediate/taxonomy_aliases.csv`: 15149 rows.
- `intermediate/game_taxonomy_canonical.csv`: 1162257 rows.
- `raw_index/taxonomy_profile.json`: machine-readable summary.

## Canonical Reference

- `mechanic`, `category`, and `family` use the 2025-02 jvanelteren vocabulary as the preferred reference.
- `domain`, `theme`, and `subcategory` currently use self-canonical vocabularies because there is no 2025 reference table for those types in the current intermediate data.
- Phase 7 applies automatic decisions for high-impact legacy mechanics and keeps unmapped legacy family labels as useful non-blocking facets.
- Legacy compound mechanics can fan out to multiple canonical rows when a safe split is known.
- Invalid placeholder labels such as `NA` are recorded in `taxonomy_aliases.csv` but excluded from `game_taxonomy_canonical.csv`.

## Alias Strategy Counts

| Strategy | Rows |
|---|---:|
| `auto_keep_legacy_broad_mechanic` | 5 |
| `auto_keep_legacy_family` | 5233 |
| `auto_merge_2025_equivalent` | 8 |
| `auto_merge_legacy_synonym` | 4 |
| `auto_normalize_legacy_label` | 1 |
| `auto_split_legacy_combo` | 2 |
| `canonical_reference_exact` | 4484 |
| `exact_label_match` | 5335 |
| `invalid_label` | 3 |
| `manual_alias` | 20 |
| `normalized_label_match` | 54 |

## Canonical Row Counts By Review Flag

| Needs review | Rows |
|---|---:|
| `false` | 1162257 |

## Vocabularies By Type/Snapshot/Source

| Type | Snapshot | Source | Rows | Vocab size |
|---|---|---|---:|---:|
| `category` | `2017-06` | `bgg-gabrio` | 227530 | 84 |
| `category` | `2017-derived` | `bgg-sujaykapadnis` | 27514 | 84 |
| `category` | `2020-08-19` | `bgg-reviews-jvanelteren` | 56632 | 84 |
| `category` | `2025-02` | `bgg-reviews-jvanelteren` | 73043 | 84 |
| `domain` | `2021-02` | `bgg-andrewmvd` | 11689 | 8 |
| `domain` | `2021-12` | `bgg-threnjen` | 12328 | 8 |
| `domain` | `2023-08` | `bgg-ranked-mattadamhouser` | 2529 | 8 |
| `family` | `2017-06` | `bgg-gabrio` | 79506 | 2546 |
| `family` | `2017-derived` | `bgg-sujaykapadnis` | 17151 | 1733 |
| `family` | `2020-08-19` | `bgg-reviews-jvanelteren` | 48026 | 3532 |
| `family` | `2021-12` | `bgg-threnjen` | 6663 | 1456 |
| `family` | `2025-02` | `bgg-reviews-jvanelteren` | 77056 | 4208 |
| `mechanic` | `2017-06` | `bgg-gabrio` | 161759 | 51 |
| `mechanic` | `2017-derived` | `bgg-sujaykapadnis` | 24900 | 52 |
| `mechanic` | `2020-08-19` | `bgg-reviews-jvanelteren` | 62901 | 182 |
| `mechanic` | `2021-02` | `bgg-andrewmvd` | 56762 | 182 |
| `mechanic` | `2021-12` | `bgg-threnjen` | 68080 | 157 |
| `mechanic` | `2023-08` | `bgg-ranked-mattadamhouser` | 11405 | 188 |
| `mechanic` | `2025-02` | `bgg-reviews-jvanelteren` | 88793 | 192 |
| `subcategory` | `2021-12` | `bgg-threnjen` | 11810 | 10 |
| `theme` | `2021-12` | `bgg-threnjen` | 32379 | 217 |
| `theme` | `2023-08` | `bgg-ranked-mattadamhouser` | 6283 | 83 |

## Top Unmapped Mechanics

| Snapshot | Raw name | Rows | Sources | Reason |
|---|---|---:|---|---|

## Next Steps

1. Rebuild RAG samples and the local FTS index after taxonomy changes.
2. Use `taxonomy_alias_overrides.csv` as the durable record of automatic merge/keep/split decisions.
3. Revisit only remaining `canonical_needs_review=true` rows if future sources introduce new unresolved labels.
