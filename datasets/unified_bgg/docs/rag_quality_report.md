# RAG Quality Report

Generated at: `2026-08-26T14:53:33`

## Summary

| Metric | Value |
| --- | ---: |
| Parsed docs | 128420 |
| Unique doc IDs | 128420 |
| Duplicate doc IDs | 0 |
| Finding rows written | 71 |

## Rows by File

| Item | Count |
| --- | ---: |
| `samples/rag/game_overview.jsonl` | 100274 |
| `samples/rag/review_digest.jsonl` | 27851 |
| `samples/rag/mechanic_profile.jsonl` | 195 |
| `samples/rag/rulebook_text.jsonl` | 100 |

## Doc Types

| Item | Count |
| --- | ---: |
| `game_overview` | 100274 |
| `review_digest` | 27851 |
| `mechanic_profile` | 195 |
| `rulebook_text` | 100 |

## Text Lengths

| Doc type | Min | Median | P95 | Max |
| --- | ---: | ---: | ---: | ---: |
| `game_overview` | 128 | 1007 | 1925 | 2690 |
| `mechanic_profile` | 621 | 799 | 901 | 978 |
| `review_digest` | 188 | 2589 | 3553 | 3664 |
| `rulebook_text` | 1234 | 38913 | 93037 | 142468 |

## Structural Flags

| Item | Count |
| --- | ---: |
| none | 0 |

## Text Health Flags

| Item | Count |
| --- | ---: |
| `very_long_text` | 71 |

## Game Overview Flags

| Item | Count |
| --- | ---: |
| `missing_rating_values` | 24339 |
| `missing_mechanics` | 14509 |
| `missing_reliable_mechanics` | 14509 |
| `expansion_doc` | 13633 |
| `game_needs_review` | 4 |
| `missing_title` | 4 |
| `missing_overall_stats` | 3 |

## Mechanic Profile Flags

| Item | Count |
| --- | ---: |
| none | 0 |

## Review Digest Flags

| Item | Count |
| --- | ---: |
| `missing_positive_snippets` | 3591 |
| `missing_critical_snippets` | 2547 |
| `missing_mixed_snippets` | 995 |
| `very_low_comment_coverage` | 7 |

## Notes

- This audit checks generated RAG JSONL structure and text health only.
- `raw_index/rag_quality_findings.jsonl` contains capped example findings for inspection.
- Review snippets are user-generated text and remain local-only until release/legal review.
