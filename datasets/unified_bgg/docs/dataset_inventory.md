# Dataset Inventory

Generated at: `2026-08-25T15:19:44`
Source root: `D:/OpenViking/research/datasets`
Summary: 7 datasets, 3.02 GB.

## Dataset Summary

| Dataset | Files | Size | Snapshot | License | Role |
|---|---:|---:|---|---|---|
| `bgg-andrewmvd` | 3 | 2.34 MB | 2021-02 | CC BY 4.0 | Lightweight baseline and cross-check source |
| `bgg-gabrio` | 3 | 140.25 MB | 2017-06 | Other | Supplement for SQLite coverage, expansions, historical descriptions, and 2017 mechanisms |
| `bgg-mrpantherson` | 5 | 4.49 MB | 2017-04 / 2018-01 / 2018-06 | CC0 | Specialized source for rating/ranking drift across homogeneous Top-5000 snapshots |
| `bgg-ranked-mattadamhouser` | 7 | 1.43 MB | 2023-08 | CC0 | Supplement for Top-2000 ranked games, 2023 mechanisms, and reimplementations |
| `bgg-reviews-jvanelteren` | 6 | 2.23 GB | 2025-02 plus historical files 2020-08-19/2022-01-08 | Other | Primary source for 2025 metadata, 26.2M ratings, and review text |
| `bgg-sujaykapadnis` | 3 | 15.80 MB | 2017 derived subset | Other | Demo/cross-reference only; strict subset of bgg-gabrio, not independent evidence |
| `bgg-threnjen` | 11 | 642.23 MB | 2021-12 | CC BY-SA 3.0 | Primary source for normalized user ratings and wide taxonomy/entity matrices |

## Files

### `bgg-andrewmvd`

| File | Size | Rows/scanned rows | Columns | Encoding | Delimiter | Notes |
|---|---:|---:|---:|---|---|---|
| `bgg-andrewmvd/DATASET.md` | 4.64 KB |  |  |  |  | source documentation |
| `bgg-andrewmvd/raw/.bundle-ok` | 38 B |  |  |  |  |  |
| `bgg-andrewmvd/raw/bgg_dataset.csv` | 2.33 MB | 20343 | 14 | utf-8-sig | ; |  |

### `bgg-gabrio`

| File | Size | Rows/scanned rows | Columns | Encoding | Delimiter | Notes |
|---|---:|---:|---:|---|---|---|
| `bgg-gabrio/DATASET.md` | 9.01 KB |  |  |  |  | source documentation |
| `bgg-gabrio/raw/.bundle-ok` | 38 B |  |  |  |  |  |
| `bgg-gabrio/raw/database.sqlite` | 140.24 MB | BoardGames=90400; bgg.ldaOut.top.documents=288; bgg.ldaOut.top.terms=250; bgg.ldaOut.topics=29229; bgg.topics=29313 |  |  |  |  |

### `bgg-mrpantherson`

| File | Size | Rows/scanned rows | Columns | Encoding | Delimiter | Notes |
|---|---:|---:|---:|---|---|---|
| `bgg-mrpantherson/DATASET.md` | 4.80 KB |  |  |  |  | source documentation |
| `bgg-mrpantherson/raw/.bundle-ok` | 38 B |  |  |  |  |  |
| `bgg-mrpantherson/raw/bgg_db_1806.csv` | 1.63 MB | 4999 | 20 | utf-8-sig | , |  |
| `bgg-mrpantherson/raw/bgg_db_2017_04.csv` | 1.42 MB | 4999 | 20 | cp1252 | , |  |
| `bgg-mrpantherson/raw/bgg_db_2018_01.csv` | 1.43 MB | 4999 | 20 | cp1252 | , |  |

### `bgg-ranked-mattadamhouser`

| File | Size | Rows/scanned rows | Columns | Encoding | Delimiter | Notes |
|---|---:|---:|---:|---|---|---|
| `bgg-ranked-mattadamhouser/DATASET.md` | 6.79 KB |  |  |  |  | source documentation |
| `bgg-ranked-mattadamhouser/raw/.bundle-ok` | 38 B |  |  |  |  |  |
| `bgg-ranked-mattadamhouser/raw/basic_data_2023.csv` | 296.93 KB | 2000 | 17 | utf-8-sig | , |  |
| `bgg-ranked-mattadamhouser/raw/mechanisms_2023.csv` | 752.15 KB | 2000 | 189 | utf-8-sig | , |  |
| `bgg-ranked-mattadamhouser/raw/reimplementations_2023.csv` | 12.24 KB | 470 | 7 | utf-8-sig | , |  |
| `bgg-ranked-mattadamhouser/raw/subdomains_2023.csv` | 46.00 KB | 2000 | 9 | utf-8-sig | , |  |
| `bgg-ranked-mattadamhouser/raw/themes_2023.csv` | 348.52 KB | 2000 | 85 | utf-8-sig | , |  |

### `bgg-reviews-jvanelteren`

| File | Size | Rows/scanned rows | Columns | Encoding | Delimiter | Notes |
|---|---:|---:|---:|---|---|---|
| `bgg-reviews-jvanelteren/DATASET.md` | 9.28 KB |  |  |  |  | source documentation |
| `bgg-reviews-jvanelteren/raw/2020-08-19.csv` | 3.52 MB | 19330 | 10 | utf-8-sig | , |  |
| `bgg-reviews-jvanelteren/raw/2022-01-08.csv` | 4.82 MB | 21831 | 10 | utf-8-sig | , |  |
| `bgg-reviews-jvanelteren/raw/bgg-26m-reviews.csv` | 2.03 GB | >= 3000000 (truncated profile) | 6 | utf-8-sig | , |  |
| `bgg-reviews-jvanelteren/raw/games_detailed_info.csv` | 94.86 MB | 21631 | 56 | utf-8-sig | , |  |
| `bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv` | 104.96 MB | 27780 | 52 | utf-8-sig | , |  |

### `bgg-sujaykapadnis`

| File | Size | Rows/scanned rows | Columns | Encoding | Delimiter | Notes |
|---|---:|---:|---:|---|---|---|
| `bgg-sujaykapadnis/DATASET.md` | 3.91 KB |  |  |  |  | source documentation |
| `bgg-sujaykapadnis/raw/.bundle-ok` | 38 B |  |  |  |  |  |
| `bgg-sujaykapadnis/raw/board_games.csv` | 15.79 MB | 10532 | 22 | utf-8-sig | , |  |

### `bgg-threnjen`

| File | Size | Rows/scanned rows | Columns | Encoding | Delimiter | Notes |
|---|---:|---:|---:|---|---|---|
| `bgg-threnjen/DATASET.md` | 20.78 KB |  |  |  |  | source documentation |
| `bgg-threnjen/raw/artists_reduced.csv` | 70.43 MB | 21925 | 1681 | utf-8-sig | , |  |
| `bgg-threnjen/raw/bgg_data_documentation.txt` | 3.20 KB |  |  |  |  |  |
| `bgg-threnjen/raw/designers_reduced.csv` | 66.79 MB | 21925 | 1594 | utf-8-sig | , |  |
| `bgg-threnjen/raw/games.csv` | 21.12 MB | 21925 | 48 | utf-8-sig | , |  |
| `bgg-threnjen/raw/mechanics.csv` | 6.72 MB | 21925 | 158 | utf-8-sig | , |  |
| `bgg-threnjen/raw/publishers_reduced.csv` | 78.17 MB | 21925 | 1866 | utf-8-sig | , |  |
| `bgg-threnjen/raw/ratings_distribution.csv` | 8.29 MB | 21925 | 96 | utf-8-sig | , |  |
| `bgg-threnjen/raw/subcategories.csv` | 583.46 KB | 21925 | 11 | utf-8-sig | , |  |
| `bgg-threnjen/raw/themes.csv` | 9.23 MB | 21925 | 218 | utf-8-sig | , |  |
| `bgg-threnjen/raw/user_ratings.csv` | 380.89 MB | 18942215 | 3 | utf-8-sig | , |  |
