# Core Tables Report

Generated at: `2026-08-25T15:43:43`

## Outputs

- `intermediate/games.csv`: 100274 rows.
- `intermediate/game_stats.csv`: 291640 rows.
- `intermediate/game_taxonomy.csv`: 1164739 rows.
- `raw_index/core_table_summary.json`: machine-readable summary.

## Games

- Input ID universe from `id_map.csv`: 100274 BGG IDs.
- Games missing `primary_name`: 4.
- Games with description: 100099.

### Game source scans

| Source | Rows used |
|---|---:|
| `jv_2025` | 27780 |
| `jv_2020_detail` | 21631 |
| `threnjen_games` | 21925 |
| `matt_basic` | 2000 |
| `mr_2018_06` | 4999 |
| `andrewmvd` | 20327 |
| `sujay` | 10532 |
| `gabrio` | 90400 |

## Game Stats

### Rows by source

| Source | Rows |
|---|---:|
| `bgg-andrewmvd` | 20327 |
| `bgg-gabrio` | 90400 |
| `bgg-mrpantherson` | 14997 |
| `bgg-ranked-mattadamhouser` | 2000 |
| `bgg-reviews-jvanelteren` | 119131 |
| `bgg-sujaykapadnis` | 10532 |
| `bgg-threnjen` | 34253 |

### Rows by rank domain

| Domain | Rows |
|---|---:|
| `abstracts` | 3656 |
| `cgs` | 971 |
| `childrensgames` | 2831 |
| `familygames` | 8008 |
| `overall` | 250753 |
| `partygames` | 2209 |
| `strategygames` | 7690 |
| `thematic` | 4163 |
| `wargames` | 11359 |

## Game Taxonomy

### Rows by taxonomy type

| Type | Rows |
|---|---:|
| `category` | 384719 |
| `domain` | 26546 |
| `family` | 228402 |
| `mechanic` | 474600 |
| `subcategory` | 11810 |
| `theme` | 38662 |

### Rows by source

| Source | Rows |
|---|---:|
| `bgg-andrewmvd` | 68451 |
| `bgg-gabrio` | 468795 |
| `bgg-ranked-mattadamhouser` | 20217 |
| `bgg-reviews-jvanelteren` | 406451 |
| `bgg-sujaykapadnis` | 69565 |
| `bgg-threnjen` | 131260 |

## Notes

- `games.csv` uses field-level source priority and stores `field_sources` as JSON.
- `game_stats.csv` is a long snapshot table; domain ranks are separate rows.
- `game_taxonomy.csv` keeps raw labels. Only 2025 labels are marked `exact`; older snapshots are marked `raw_unmapped` until alias mapping is built.
- Row-level ratings and reviews are intentionally not transformed in this phase.
