# Review Digest Report

Generated at: `2026-08-25T17:15:12`

## Outputs

| Output | Rows | Bytes |
| --- | ---: | ---: |
| `samples/rag/review_digest.jsonl` | 27851 | 196789608 |
| `samples/rag/review_digest.preview.jsonl` | 50 | 521946 |

## Streaming Scan

| Metric | Value |
| --- | ---: |
| Raw rows scanned | 26200012 |
| Games with rating rows | 27865 |
| Games with non-empty comments | 27851 |
| Non-empty comments | 4206543 |
| Comment coverage | 16.0555% |

## Notes

- Source file: `bgg-reviews-jvanelteren/raw/bgg-26m-reviews.csv`
- The output is extractive: it stores per-game rating/comment aggregates plus representative positive, mixed, and critical snippets.
- Review snippets are BGG user-generated content; keep this output local until release/legal policy is reviewed.
