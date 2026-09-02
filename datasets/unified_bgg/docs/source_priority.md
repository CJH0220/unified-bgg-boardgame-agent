# Source Priority and Field Ownership

## Source roles

| Source | Role | Primary fact source? |
|---|---|---:|
| `bgg-reviews-jvanelteren` | 2025 metadata, 26.2M user ratings, and 4.2M review texts | yes |
| `bgg-threnjen` | 2021 normalized rating matrix plus wide mechanic/theme/entity tables | yes |
| `bgg-gabrio` | 2017 SQLite, broadest coverage, expansions, raw descriptions | supplement |
| `bgg-ranked-mattadamhouser` | 2023 Top-2000, 188 mechanism columns, reimplementation links | supplement |
| `bgg-mrpantherson` | 2017-2018 Top-5000 three homogeneous snapshots | time-series only |
| `bgg-andrewmvd` | 2021 lightweight CC BY 4.0 baseline | prototype/check |
| `bgg-sujaykapadnis` | strict subset of gabrio | lineage only; no duplicate weighting |

## Field priority

| Field family | Preferred source | Backup source | Notes |
|---|---|---|---|
| Name/year/player counts/playtime/age | jvanelteren `games_detailed_info2025.csv` | threnjen `games.csv`, gabrio `BoardGames` | 2025 is newest; gabrio can fill expansions/history |
| Raw English description | jvanelteren `games_detailed_info2025.csv` | gabrio `details.description` | threnjen `Description` is stemmed and not suitable for natural text |
| Current average/Geek rating | jvanelteren 2025 | threnjen 2021 | Store as snapshots, not as one overwritten value |
| User rating matrix | threnjen `user_ratings.csv` | jvanelteren `bgg-26m-reviews.csv` | Keep source spaces separate |
| Review text | jvanelteren `bgg-26m-reviews.csv` | none | Only a minority of ratings include comments |
| Mechanics | jvanelteren 2025 vocabulary | threnjen 2021, matt 2023, gabrio 2017 | Cross-year analysis needs alias mapping |
| Themes/categories/subdomains | threnjen wide tables plus jvanelteren details | andrewmvd Domains | `subcategories` and `Cat:*` are not the same concept |
| Designers/artists/publishers | threnjen reduced wide tables | gabrio multi-value fields | Reduced tables are not safe for full entity productivity stats |
| Reimplementation/expansion links | mattadamhouser `reimplementations_2023.csv` | gabrio relation fields | Useful for lineage and mechanic inheritance |
| Rating drift | mrpantherson three snapshots | jvanelteren historical metadata files | mrpantherson has homogeneous schema |

## Conflict policy

1. Do not overwrite conflicting source facts silently.
2. Store time-sensitive metrics as rows in `game_stats` with snapshot metadata.
3. Keep raw taxonomy labels and add canonical labels only through explicit mapping.
4. Keep unclear-license and review-text content local until release/commercial review is complete.
