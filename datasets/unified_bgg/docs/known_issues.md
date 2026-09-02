# Known Issues and Cleaning Rules

## Global rules

- BGG IDs are the cross-dataset anchor, but column names vary: `BGGId`, `id`, `ID`, `game_id`, and `game.id`.
- User names must be read as strings; numeric-looking usernames exist.
- Multi-value fields appear as comma-separated strings or stringified Python lists; use `ast.literal_eval` for the latter.
- Ratings, ranks, user counts, and complexity values often come from different snapshots; do not mix them as one timestamp.
- Fine-tuning samples and RAG chunks must include source metadata.

## Source-specific traps

| Source | Issue | Rule |
|---|---|---|
| `bgg-andrewmvd` | Uses `;` delimiter and `,` decimal mark; 16 empty IDs | Read with `sep=";"`, `decimal=","`; drop or QA empty IDs |
| `bgg-gabrio` | SQLite columns contain dots; `game.id` is TEXT; `bayesaverage=0` means unknown | Quote SQL column names; cast ID; turn zero bayes into null |
| `bgg-gabrio` | Includes 13,712 expansions | Filter `game.type='boardgame'` for base-game analysis |
| `bgg-mrpantherson` | 2017-04 and 2018-01 are cp1252; 2018-06 is UTF-8 | Set encoding per file |
| `bgg-threnjen` | `Rank:*` uses `21926` as not-ranked sentinel | Replace sentinel with null |
| `bgg-threnjen` | `NumComments` is always 0; `MfgPlaytime` duplicates `ComMaxPlaytime` | Do not use `NumComments`; drop one duplicate playtime column |
| `bgg-threnjen` | `LanguageEase` is not the official 1-5 language-dependence level | Do not use it directly as language dependence |
| `bgg-threnjen` | `BGGId` is not the first column in `*_reduced.csv` | Do not use `index_col=0`; explicitly `set_index("BGGId")` |
| `bgg-reviews-jvanelteren` | `bgg-26m-reviews.csv` is ordered by game; `nrows` profiling is biased | Use full chunked stats or stratified sampling |
| `bgg-reviews-jvanelteren` | Only about 16.09% of ratings have comments | Filter non-empty text for review tasks |
| `bgg-sujaykapadnis` | Strict subset of gabrio with identical ratings | Keep lineage only; do not count as independent evidence |

## Mechanic vocabulary rules

- 2017 gabrio has about 51 mechanism names, 2021 threnjen has 157, 2023 matt has 188, and 2025 jvanelteren has 192.
- Do not join cross-year mechanisms by raw string alone.
- Prefer the 2025 vocabulary as canonical, but maintain `taxonomy_aliases`.
- If a mapping is not manually reviewed, mark it as `manual_review` or `unmapped`, not `exact`.

## License and release notes

- `bgg-ranked-mattadamhouser` and `bgg-mrpantherson` are CC0.
- `bgg-andrewmvd` is CC BY 4.0 and needs attribution.
- `bgg-threnjen` is CC BY-SA 3.0 and derived releases may need share-alike.
- `bgg-gabrio`, `bgg-sujaykapadnis`, and `bgg-reviews-jvanelteren` are Other/unclear and need source-page review before release or commercial use.
- Review text may include BGG user-generated content; keep it local for research until legal/release policy is clear.
