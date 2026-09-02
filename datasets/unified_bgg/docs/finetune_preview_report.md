# Finetune Preview Report

Generated at: `2026-08-26T09:37:15`

## Summary

| Metric | Value |
| --- | ---: |
| Parsed rows | 250 |
| Unique sample IDs | 250 |
| Finding rows written | 0 |
| RAG doc IDs loaded for source validation | 128320 |
| Preview size per task | 50 |
| Source game_overview docs | 100274 |
| Source mechanic_profile docs | 195 |
| Source review_digest docs | 27851 |

## Rows by File

| Item | Count |
| --- | ---: |
| `samples/finetune/extraction.preview.jsonl` | 50 |
| `samples/finetune/game_qa.preview.jsonl` | 50 |
| `samples/finetune/mechanic_explanation.preview.jsonl` | 50 |
| `samples/finetune/recommendation_reasoning.preview.jsonl` | 50 |
| `samples/finetune/review_summary.preview.jsonl` | 50 |

## Task Counts

| Item | Count |
| --- | ---: |
| `extraction` | 50 |
| `game_qa` | 50 |
| `mechanic_explanation` | 50 |
| `recommendation_reasoning` | 50 |
| `review_summary` | 50 |

## Structural Flags

| Item | Count |
| --- | ---: |
| none | 0 |

## Source Flags

| Item | Count |
| --- | ---: |
| none | 0 |

## Input Text Flags

| Item | Count |
| --- | ---: |
| none | 0 |

## Output Text Flags

| Item | Count |
| --- | ---: |
| none | 0 |

## Sample Quality Flags

| Item | Count |
| --- | ---: |
| `template_generated` | 250 |

## Output Lengths

| Task type | Min | Median | P95 | Max |
| --- | ---: | ---: | ---: | ---: |
| `extraction` | 423 | 666 | 743 | 752 |
| `game_qa` | 190 | 365 | 424 | 446 |
| `mechanic_explanation` | 403 | 495 | 574 | 620 |
| `recommendation_reasoning` | 278 | 302 | 334 | 341 |
| `review_summary` | 223 | 239 | 254 | 264 |

## Notes

- Preview samples are deterministic template outputs for audit and iteration.
- `template_generated` is expected on every row.
- Source document IDs are checked against current RAG JSONL outputs.
- Review-derived outputs summarize themes and do not reproduce long user comments.
