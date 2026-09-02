# Finetune Candidate Report

Generated at: `2026-08-26T09:40:57`

## Summary

| Metric | Value |
| --- | ---: |
| Parsed rows | 4195 |
| Unique sample IDs | 4195 |
| Finding rows written | 0 |
| RAG doc IDs loaded for source validation | 128320 |
| Preview size per task | 1000 |
| Source game_overview docs | 100274 |
| Source mechanic_profile docs | 195 |
| Source review_digest docs | 27851 |

## Rows by File

| Item | Count |
| --- | ---: |
| `samples/finetune/extraction.candidate.jsonl` | 1000 |
| `samples/finetune/game_qa.candidate.jsonl` | 1000 |
| `samples/finetune/recommendation_reasoning.candidate.jsonl` | 1000 |
| `samples/finetune/review_summary.candidate.jsonl` | 1000 |
| `samples/finetune/mechanic_explanation.candidate.jsonl` | 195 |

## Task Counts

| Item | Count |
| --- | ---: |
| `extraction` | 1000 |
| `game_qa` | 1000 |
| `recommendation_reasoning` | 1000 |
| `review_summary` | 1000 |
| `mechanic_explanation` | 195 |

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
| `template_generated` | 4195 |

## Output Lengths

| Task type | Min | Median | P95 | Max |
| --- | ---: | ---: | ---: | ---: |
| `extraction` | 392 | 567 | 704 | 767 |
| `game_qa` | 164 | 313 | 405 | 463 |
| `mechanic_explanation` | 359 | 464 | 553 | 635 |
| `recommendation_reasoning` | 209 | 307 | 341 | 391 |
| `review_summary` | 169 | 241 | 266 | 293 |

## Notes

- Preview samples are deterministic template outputs for audit and iteration.
- `template_generated` is expected on every row.
- Source document IDs are checked against current RAG JSONL outputs.
- Review-derived outputs summarize themes and do not reproduce long user comments.
