# ID Profile Report

Generated at: `2026-08-25T15:32:28`

## Summary

- Scanned source ID columns: 21.
- Skipped large row-level files: 2.
- Union of scanned BGG IDs: 100274.
- Initial `id_map.csv` rows: 345282.
- Reference set `bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:id` IDs: 27780.
- Possible name-conflict IDs: 1770.

## Source ID Profiles

| Source | Role | Rows | Valid ID rows | Unique IDs | Missing IDs | Invalid IDs | Duplicate ID rows | Reference overlap | Not in reference |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:id` | primary | 27780 | 27780 | 27780 | 0 | 0 | 0 | 27780 (100.0%) | 0 |
| `bgg-reviews-jvanelteren/raw/games_detailed_info.csv:id` | primary | 21631 | 21631 | 21631 | 0 | 0 | 0 | 21538 (99.57%) | 93 |
| `bgg-reviews-jvanelteren/raw/2022-01-08.csv:ID` | primary | 21831 | 21831 | 21831 | 0 | 0 | 0 | 21736 (99.56%) | 95 |
| `bgg-reviews-jvanelteren/raw/2020-08-19.csv:ID` | primary | 19330 | 19330 | 19330 | 0 | 0 | 0 | 19224 (99.45%) | 106 |
| `bgg-reviews-jvanelteren/raw/bgg-26m-reviews.csv:ID` | primary | skipped |  |  |  |  |  |  | large row-level review file; use --include-large to scan |
| `bgg-threnjen/raw/games.csv:BGGId` | primary | 21925 | 21925 | 21925 | 0 | 0 | 0 | 21497 (98.05%) | 428 |
| `bgg-threnjen/raw/mechanics.csv:BGGId` | taxonomy_matrix | 21925 | 21925 | 21925 | 0 | 0 | 0 | 21497 (98.05%) | 428 |
| `bgg-threnjen/raw/themes.csv:BGGId` | taxonomy_matrix | 21925 | 21925 | 21925 | 0 | 0 | 0 | 21497 (98.05%) | 428 |
| `bgg-threnjen/raw/subcategories.csv:BGGId` | taxonomy_matrix | 21925 | 21925 | 21925 | 0 | 0 | 0 | 21497 (98.05%) | 428 |
| `bgg-threnjen/raw/ratings_distribution.csv:BGGId` | rating_distribution | 21925 | 21925 | 21925 | 0 | 0 | 0 | 21497 (98.05%) | 428 |
| `bgg-threnjen/raw/user_ratings.csv:BGGId` | row_level_ratings | skipped |  |  |  |  |  |  | large row-level rating file; use --include-large to scan |
| `bgg-ranked-mattadamhouser/raw/basic_data_2023.csv:game_id` | primary | 2000 | 2000 | 2000 | 0 | 0 | 0 | 1996 (99.8%) | 4 |
| `bgg-ranked-mattadamhouser/raw/mechanisms_2023.csv:game_id` | taxonomy_matrix | 2000 | 2000 | 2000 | 0 | 0 | 0 | 1996 (99.8%) | 4 |
| `bgg-ranked-mattadamhouser/raw/themes_2023.csv:game_id` | taxonomy_matrix | 2000 | 2000 | 2000 | 0 | 0 | 0 | 1996 (99.8%) | 4 |
| `bgg-ranked-mattadamhouser/raw/subdomains_2023.csv:game_id` | taxonomy_matrix | 2000 | 2000 | 2000 | 0 | 0 | 0 | 1996 (99.8%) | 4 |
| `bgg-ranked-mattadamhouser/raw/reimplementations_2023.csv:game_id` | relation_child | 470 | 470 | 470 | 0 | 0 | 0 | 468 (99.57%) | 2 |
| `bgg-ranked-mattadamhouser/raw/reimplementations_2023.csv:parent_id` | relation_parent | 470 | 470 | 359 | 0 | 0 | 111 | 340 (94.71%) | 19 |
| `bgg-mrpantherson/raw/bgg_db_2017_04.csv:game_id` | primary | 4999 | 4999 | 4999 | 0 | 0 | 0 | 4988 (99.78%) | 11 |
| `bgg-mrpantherson/raw/bgg_db_2018_01.csv:game_id` | primary | 4999 | 4999 | 4999 | 0 | 0 | 0 | 4989 (99.8%) | 10 |
| `bgg-mrpantherson/raw/bgg_db_1806.csv:game_id` | primary | 4999 | 4999 | 4999 | 0 | 0 | 0 | 4989 (99.8%) | 10 |
| `bgg-andrewmvd/raw/bgg_dataset.csv:ID` | primary | 20343 | 20327 | 20327 | 16 | 0 | 0 | 20224 (99.49%) | 103 |
| `bgg-sujaykapadnis/raw/board_games.csv:game_id` | primary | 10532 | 10532 | 10532 | 0 | 0 | 0 | 10376 (98.52%) | 156 |
| `bgg-gabrio/raw/database.sqlite:game.id` | primary | 90400 | 90400 | 90400 | 0 | 0 | 0 | 18078 (20.0%) | 72322 |

## Dataset-Level Coverage

| Dataset | Unique scanned IDs | In 2025 reference | Percent in reference | IDs not in reference | 2025 IDs missing from dataset |
|---|---:|---:|---:|---:|---:|
| `bgg-andrewmvd` | 20327 | 20224 | 99.49% | 103 | 7556 |
| `bgg-gabrio` | 90400 | 18078 | 20.00% | 72322 | 9702 |
| `bgg-mrpantherson` | 5455 | 5442 | 99.76% | 13 | 22338 |
| `bgg-ranked-mattadamhouser` | 2135 | 2112 | 98.92% | 23 | 25668 |
| `bgg-reviews-jvanelteren` | 27907 | 27780 | 99.54% | 127 | 0 |
| `bgg-sujaykapadnis` | 10532 | 10376 | 98.52% | 156 | 17404 |
| `bgg-threnjen` | 21925 | 21497 | 98.05% | 428 | 6283 |

## Dataset Pairwise Intersections

| Dataset A | Dataset B | Intersection | A coverage | B coverage |
|---|---|---:|---:|---:|
| `bgg-andrewmvd` | `bgg-gabrio` | 16855 | 82.92% | 18.64% |
| `bgg-andrewmvd` | `bgg-mrpantherson` | 5448 | 26.80% | 99.87% |
| `bgg-andrewmvd` | `bgg-ranked-mattadamhouser` | 1953 | 9.61% | 91.48% |
| `bgg-andrewmvd` | `bgg-reviews-jvanelteren` | 20324 | 99.99% | 72.83% |
| `bgg-andrewmvd` | `bgg-sujaykapadnis` | 10386 | 51.09% | 98.61% |
| `bgg-andrewmvd` | `bgg-threnjen` | 20246 | 99.60% | 92.34% |
| `bgg-gabrio` | `bgg-mrpantherson` | 5324 | 5.89% | 97.60% |
| `bgg-gabrio` | `bgg-ranked-mattadamhouser` | 1468 | 1.62% | 68.76% |
| `bgg-gabrio` | `bgg-reviews-jvanelteren` | 18178 | 20.11% | 65.14% |
| `bgg-gabrio` | `bgg-sujaykapadnis` | 10532 | 11.65% | 100.00% |
| `bgg-gabrio` | `bgg-threnjen` | 17384 | 19.23% | 79.29% |
| `bgg-mrpantherson` | `bgg-ranked-mattadamhouser` | 1454 | 26.65% | 68.10% |
| `bgg-mrpantherson` | `bgg-reviews-jvanelteren` | 5452 | 99.95% | 19.54% |
| `bgg-mrpantherson` | `bgg-sujaykapadnis` | 4906 | 89.94% | 46.58% |
| `bgg-mrpantherson` | `bgg-threnjen` | 5452 | 99.95% | 24.87% |
| `bgg-ranked-mattadamhouser` | `bgg-reviews-jvanelteren` | 2116 | 99.11% | 7.58% |
| `bgg-ranked-mattadamhouser` | `bgg-sujaykapadnis` | 1262 | 59.11% | 11.98% |
| `bgg-ranked-mattadamhouser` | `bgg-threnjen` | 2015 | 94.38% | 9.19% |
| `bgg-reviews-jvanelteren` | `bgg-sujaykapadnis` | 10405 | 37.28% | 98.79% |
| `bgg-reviews-jvanelteren` | `bgg-threnjen` | 21603 | 77.41% | 98.53% |
| `bgg-sujaykapadnis` | `bgg-threnjen` | 10512 | 99.81% | 47.95% |

## Possible Name Conflicts

These are not necessarily errors. BGG titles can change over time, and some sources use alternate or older names.

| BGG ID | Variant count | Examples |
|---:|---:|---|
| 3615 | 4 | bgg-gabrio/raw/database.sqlite:Agincourt; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Agincourt: The Triumph of Archery over Armor, 25 October 1415; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Agincourt: The Triumph of Archery over Armor; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Agincourt: The Triumph of Archery over Armor; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:Agincourt: The Triumph of Archery over Armor, 1415; bgg-sujaykapadnis/raw/board_games.csv:Agincourt |
| 4207 | 4 | bgg-mrpantherson/raw/bgg_db_2017_04.csv:Kharkov; bgg-mrpantherson/raw/bgg_db_2018_01.csv:Kharkov; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Kharkov: The Soviet Spring Offensive 12 May to 21 May 1942; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Kharkov: The Soviet Spring Offensive; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Kharkov: The Soviet Spring Offensive; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:Kharkov: The Soviet Spring Offensive, 1942 |
| 5769 | 4 | bgg-gabrio/raw/database.sqlite:Edelweiss; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Edelweiss: The Struggle in the Caucasus July - November 1942; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Edelweiss: The Struggle in the Caucasus; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Edelweiss: The Struggle in the Caucasus; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:Edelweiss: The Struggle in the Caucasus, 1942; bgg-sujaykapadnis/raw/board_games.csv:Edelweiss |
| 5965 | 4 | bgg-mrpantherson/raw/bgg_db_1806.csv:October War; bgg-mrpantherson/raw/bgg_db_2017_04.csv:October War; bgg-mrpantherson/raw/bgg_db_2018_01.csv:October War; bgg-reviews-jvanelteren/raw/2020-08-19.csv:October War: Doctrine and Tactics in the Yom Kippur Conflict 6 to 24 October 1973; bgg-reviews-jvanelteren/raw/2022-01-08.csv:October War: Doctrine and Tactics in the Yom Kippur Conflict; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:October War: Doctrine and Tactics in the Yom Kippur Conflict |
| 7503 | 4 | bgg-andrewmvd/raw/bgg_dataset.csv:A Frozen Hell: The Battle of Tolvajärv; bgg-gabrio/raw/database.sqlite:A Frozen Hell; bgg-reviews-jvanelteren/raw/2020-08-19.csv:A Frozen Hell: The Battle of Tolvajärvi, Russo-Finnish War, 1939; bgg-reviews-jvanelteren/raw/2022-01-08.csv:A Frozen Hell: The Battle of Tolvajärvi; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:A Frozen Hell: The Battle of Tolvajärvi; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:A Frozen Hell: The Battle of Tolvajärvi, Russo-Finnish War, 1939 |
| 8208 | 4 | bgg-mrpantherson/raw/bgg_db_2017_04.csv:Trial of Strength; bgg-mrpantherson/raw/bgg_db_2018_01.csv:Trial of Strength; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Trial of Strength: War on the Eastern Front 1941 - 1945 – Second Edition; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Trial of Strength: War on the Eastern Front; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Trial of Strength: War on the Eastern Front; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:Trial of Strength: War on the Eastern Front 1941-45 |
| 8429 | 4 | bgg-gabrio/raw/database.sqlite:Combat Command; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Combat Command: Tactical Combat in Europe, 1944; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Combat Command: Tactical Armored Warfare; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Combat Command: Tactical Armored Warfare; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:Combat Command: Tactical Armored Warfare, France 1944; bgg-threnjen/raw/games.csv:Combat Command: Tactical Armored Warfare |
| 8693 | 4 | bgg-gabrio/raw/database.sqlite:1918; bgg-reviews-jvanelteren/raw/2020-08-19.csv:1918: Operation Michel – March 21-30, Germany's Last Chance in the West; bgg-reviews-jvanelteren/raw/2022-01-08.csv:1918: Operation Michel; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:1918: Operation Michel; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:1918: Operation Michel, Germany's Last Chance in the West; bgg-threnjen/raw/games.csv:1918: Operation Michel |
| 10361 | 4 | bgg-gabrio/raw/database.sqlite:Dead of Winter (first edition); bgg-reviews-jvanelteren/raw/2020-08-19.csv:Dead of Winter: The Battle of Stones River – Murfreesboro, Tennessee December 31, 1862-January 2, 1863; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Dead of Winter: The Battle of Stones River; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Dead of Winter: The Battle of Stones River; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:Dead of Winter: The Battle of Stones River – Murfreesboro, Tennessee; bgg-threnjen/raw/games.csv:Dead of Winter: The Battle of Stones River |
| 31443 | 4 | bgg-mrpantherson/raw/bgg_db_2017_04.csv:The Habit of Victory; bgg-mrpantherson/raw/bgg_db_2018_01.csv:The Habit of Victory; bgg-reviews-jvanelteren/raw/2020-08-19.csv:The Habit of Victory: From Warsaw to Eylau to Friedland – 6 December 1806 - 29 June 1807; bgg-reviews-jvanelteren/raw/2022-01-08.csv:The Habit of Victory: From Warsaw to Eylau to Friedland; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:The Habit of Victory: From Warsaw to Eylau to Friedland; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:The Habit of Victory: From Warsaw to Eylau to Friedland, 1806-7 |
| 68188 | 4 | bgg-mrpantherson/raw/bgg_db_1806.csv:Levée en Masse; bgg-mrpantherson/raw/bgg_db_2017_04.csv:Levée en Masse; bgg-mrpantherson/raw/bgg_db_2018_01.csv:Levée en Masse; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Levée en Masse: The Wars of the French Revolution, 1789-1802; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Levée en Masse: The Wars of the French Revolution; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Levée en Masse: The Wars of the French Revolution |
| 28 | 3 | bgg-mrpantherson/raw/bgg_db_1806.csv:Illuminati:  Deluxe Edition; bgg-mrpantherson/raw/bgg_db_2017_04.csv:Illuminati:  Deluxe Edition; bgg-mrpantherson/raw/bgg_db_2018_01.csv:Illuminati:  Deluxe Edition; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Illuminati (Second Edition); bgg-reviews-jvanelteren/raw/2022-01-08.csv:Illuminati; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Illuminati |
| 63 | 3 | bgg-mrpantherson/raw/bgg_db_1806.csv:Samurai; bgg-mrpantherson/raw/bgg_db_2017_04.csv:Samurai; bgg-mrpantherson/raw/bgg_db_2018_01.csv:Samurai; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Samurai: Game of Politics and Warfare in Feudal Japan – 12th thru 17th Centuries; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Samurai: Game of Politics and Warfare in Feudal Japan; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Samurai: Game of Politics and Warfare in Feudal Japan |
| 68 | 3 | bgg-mrpantherson/raw/bgg_db_2017_04.csv:Successors (second edition); bgg-mrpantherson/raw/bgg_db_2018_01.csv:Successors (second edition); bgg-reviews-jvanelteren/raw/2020-08-19.csv:Successors (Second Edition); bgg-reviews-jvanelteren/raw/2022-01-08.csv:Successors (First/Second Edition); bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Successors (First/Second Edition); bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:Successors: The Battles for Alexander's Empire (First/Second Edition) |
| 255 | 3 | bgg-gabrio/raw/database.sqlite:Jena-Auerstadt; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Jena-Auerstadt: The Battle for Prussia, 14 October 1806; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Jena-Auerstadt: The Battle for Prussia; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Jena-Auerstadt: The Battle for Prussia; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:Jena-Auerstadt: The Battle for Prussia, 14 October 1806; bgg-sujaykapadnis/raw/board_games.csv:Jena-Auerstadt |
| 706 | 3 | bgg-mrpantherson/raw/bgg_db_1806.csv:Frederick the Great; bgg-mrpantherson/raw/bgg_db_2017_04.csv:Frederick the Great; bgg-mrpantherson/raw/bgg_db_2018_01.csv:Frederick the Great; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Frederick the Great: The Campaigns of The Soldier King 1756-1759; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Frederick the Great: The Campaigns of The Soldier King; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Frederick the Great: The Campaigns of The Soldier King |
| 753 | 3 | bgg-mrpantherson/raw/bgg_db_2017_04.csv:Panzerkrieg; bgg-mrpantherson/raw/bgg_db_2018_01.csv:Panzerkrieg; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Panzerkrieg: von Manstein & HeeresGruppe Süd – August 1941-March 1944; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Panzerkrieg: von Manstein & HeeresGruppe Süd; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Panzerkrieg: von Manstein & HeeresGruppe Süd; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:Panzerkrieg: von Manstein & HeeresGruppe Süd |
| 942 | 3 | bgg-andrewmvd/raw/bgg_dataset.csv:Gastero Speed: Les Gros Bourgognes; bgg-gabrio/raw/database.sqlite:Gastérospeed; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Gastero Speed: Les Gros Bourgognes; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Snail's Pace; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Snail's Pace; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:Snail's Pace |
| 1337 | 3 | bgg-gabrio/raw/database.sqlite:Traboulet; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Traboulet; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Kuba; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Kuba; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:Akiba; bgg-sujaykapadnis/raw/board_games.csv:Traboulet |
| 1506 | 3 | bgg-mrpantherson/raw/bgg_db_1806.csv:Conquistador; bgg-mrpantherson/raw/bgg_db_2017_04.csv:Conquistador; bgg-mrpantherson/raw/bgg_db_2018_01.csv:Conquistador; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Conquistador: The Age of Exploration – 1495-1600; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Conquistador: The Age of Exploration; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Conquistador: The Age of Exploration |
| 1585 | 3 | bgg-mrpantherson/raw/bgg_db_1806.csv:Burma; bgg-mrpantherson/raw/bgg_db_2017_04.csv:Burma; bgg-mrpantherson/raw/bgg_db_2018_01.csv:Burma; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Burma: The Campaign in Northern Burma, 1944; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Burma: The Campaign in Northern Burma; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Burma: The Campaign in Northern Burma |
| 2072 | 3 | bgg-mrpantherson/raw/bgg_db_1806.csv:Panzer Command; bgg-mrpantherson/raw/bgg_db_2017_04.csv:Panzer Command; bgg-mrpantherson/raw/bgg_db_2018_01.csv:Panzer Command; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Panzer Command: The Gateway to Stalingrad Fall '42-Spring '43; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Panzer Command: The Gateway to Stalingrad; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Panzer Command: The Gateway to Stalingrad |
| 2077 | 3 | bgg-mrpantherson/raw/bgg_db_1806.csv:Hell's Highway; bgg-mrpantherson/raw/bgg_db_2017_04.csv:Hell's Highway; bgg-mrpantherson/raw/bgg_db_2018_01.csv:Hell's Highway; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Hell's Highway: Operation Market Garden – Holland, 1944; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Hell's Highway: Operation Market Garden; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Hell's Highway: Operation Market Garden |
| 2090 | 3 | bgg-mrpantherson/raw/bgg_db_2017_04.csv:Stalingrad Pocket (first edition); bgg-mrpantherson/raw/bgg_db_2018_01.csv:Stalingrad Pocket (first edition); bgg-reviews-jvanelteren/raw/2020-08-19.csv:Stalingrad Pocket (first edition); bgg-reviews-jvanelteren/raw/2022-01-08.csv:Stalingrad Pocket; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Stalingrad Pocket; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:Stalingrad Pocket: The Wehrmacht's Greatest Disaster |
| 2287 | 3 | bgg-andrewmvd/raw/bgg_dataset.csv:Dungeonbowl: Elves & Dwarfs; bgg-gabrio/raw/database.sqlite:Blood Bowl (Second Edition): Elves, Dwarfs and Dungeonbowl; bgg-reviews-jvanelteren/raw/2020-08-19.csv:Dungeonbowl: Elves & Dwarfs; bgg-reviews-jvanelteren/raw/2022-01-08.csv:Elves, Dwarfs & Dungeonbowl; bgg-reviews-jvanelteren/raw/games_detailed_info.csv:Elves, Dwarfs & Dungeonbowl; bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv:Elves, Dwarfs & Dungeonbowl |

## Outputs

- `raw_index/id_profiles.json`: source-level ID stats and reference coverage.
- `raw_index/id_sets.json`: scanned BGG ID sets by source label.
- `raw_index/name_conflicts.json`: possible same-ID name variants.
- `intermediate/id_map.csv`: initial source-to-`bgg:{id}` alignment rows.
- `intermediate/dataset_id_coverage.csv`: dataset-level coverage against the 2025 reference.

## Next Steps

1. Review possible name conflicts and decide whether any require manual alias rows.
2. Decide whether to run `build_id_map.py --include-large` to scan row-level rating/review files.
3. Start `games`, `game_stats`, and `game_taxonomy` transforms using this `id_map.csv`.
