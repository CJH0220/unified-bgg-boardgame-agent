# RAG Samples Report

Generated at: `2026-08-26T09:26:21`

## Outputs

| Output | Rows | Bytes |
| --- | ---: | ---: |
| `samples/rag/game_overview.jsonl` | 100274 | 226440688 |
| `samples/rag/game_overview.preview.jsonl` | 50 | 203629 |
| `samples/rag/mechanic_profile.jsonl` | 195 | 1328585 |
| `samples/rag/mechanic_profile.preview.jsonl` | 50 | 352437 |

## Source Tables

- `intermediate/games.csv`
- `intermediate/game_stats.csv`
- `intermediate/game_taxonomy_canonical.csv`

## Quality Summary

| Metric | Value |
| --- | ---: |
| Game docs missing selected overall stats | 3 |
| Game docs missing reliable mechanics | 14509 |
| Game docs marked needs review | 4 |
| Taxonomy rows excluded from RAG text because canonical review is required | 0 |

## Notes

- Phase 5 uses only intermediate tables and does not scan the 26M row rating/review file.
- `game_overview` docs are one per game entity.
- `mechanic_profile` docs are one per canonical mechanic after excluding labels marked `canonical_needs_review=true`.
- Preview files contain the highest-quality/top-ranked examples for manual text inspection.
