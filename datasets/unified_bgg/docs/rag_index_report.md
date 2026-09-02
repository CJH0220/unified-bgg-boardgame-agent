# RAG Index Report

Generated at: `2026-08-26T14:53:31`

## Summary

| Metric | Value |
| --- | ---: |
| Parsed docs | 128420 |
| Duplicate errors | 0 |
| Index bytes | 1131544576 |
| Elapsed seconds | 17.963 |

## Index

- SQLite file: `final/rag_index.sqlite`
- FTS engine: SQLite FTS5
- Query script: `scripts/query_rag_index.py`

## Doc Types

| Item | Count |
| --- | ---: |
| `game_overview` | 100274 |
| `mechanic_profile` | 195 |
| `review_digest` | 27851 |
| `rulebook_text` | 100 |

## Rows by Source File

| Item | Count |
| --- | ---: |
| `samples/rag/game_overview.jsonl` | 100274 |
| `samples/rag/mechanic_profile.jsonl` | 195 |
| `samples/rag/review_digest.jsonl` | 27851 |
| `samples/rag/rulebook_text.jsonl` | 100 |

## Example

```powershell
python scripts/query_rag_index.py "Through the Ages civilization" --doc-type game_overview
python scripts/query_rag_index.py "deck bag pool building" --doc-type mechanic_profile
python scripts/query_rag_index.py "Catan trading negotiation comments" --doc-type review_digest
```
