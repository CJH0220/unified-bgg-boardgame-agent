# unified_bgg Phase 9 Retrieval Interface

Generated: 2026-08-26

## Goal

Phase 9 turns the Phase 8 retrieval stack into a unified interface for downstream use.
It is meant to reduce script fragmentation and provide a single entry point for:

- ad hoc retrieval;
- board-game recall for later fine-tune or RAG tasks;
- repeatable query-suite exports;
- consistent result schemas across FTS, vector, and hybrid engines.

## What Phase 9 Adds

- `scripts/unified_retrieval.py`
  - shared search dispatcher and Markdown renderer.
- `scripts/query_unified_index.py`
  - single CLI for `auto`, `fts`, `vector`, and `hybrid` retrieval.
- `scripts/retrieval_suite.py`
  - curated query set for board-game validation and sample export.
- `scripts/export_retrieval_suite.py`
  - writes JSONL and Markdown output for the curated suite.

## Standard Result Shape

Each retrieval response keeps:

- `query`
- `engine`
- `expanded_query`
- `doc_type_filter`
- `game_id_filter`
- `bgg_id_filter`
- `results`

Each result row keeps engine-specific evidence fields such as:

- `score`
- `raw_vector_score`
- `fts_rank`
- `vector_rank`
- `fusion_score`
- `source_file`
- `doc_id`

## Recommended Usage

```powershell
python scripts\query_unified_index.py "卡坦岛 交易 评论" --doc-type review_digest --bgg-id 13 --markdown
python scripts\query_unified_index.py "Brass Birmingham economic network route building" --doc-type game_overview --json
python scripts\export_retrieval_suite.py --engine hybrid
```

## Outputs

- `raw_index/retrieval_suite.jsonl`
- `raw_index/retrieval_suite_summary.json`
- `docs/retrieval_suite_report.md`

## Validation Target

Phase 9 is considered complete when:

- the unified query CLI runs for FTS, vector, and hybrid engines;
- the query-suite export succeeds;
- the exported suite preserves expected board-game anchors for the validated queries;
- the docs and manifest reflect the new interface.

## Validation Result

The current Phase 9 run passed these checks:

- `python -m py_compile scripts\retrieval_suite.py scripts\unified_retrieval.py scripts\query_unified_index.py scripts\export_retrieval_suite.py`
- `python scripts\query_unified_index.py "卡坦岛 交易 评论" --doc-type review_digest --engine fts --limit 2 --json`
- `python scripts\query_unified_index.py "卡坦岛 交易 评论" --doc-type review_digest --engine vector --limit 2 --json`
- `python scripts\query_unified_index.py "卡坦岛 交易 评论" --doc-type review_digest --engine hybrid --limit 3 --json`
- `python scripts\export_retrieval_suite.py --engine hybrid --limit 5 --candidate-limit 50`

Retrieval suite result:

| Metric | Value |
| --- | ---: |
| Suite size | 12 |
| Validated queries | 12 |
| Passed | 12 |
| Pass rate | 1.0 |

