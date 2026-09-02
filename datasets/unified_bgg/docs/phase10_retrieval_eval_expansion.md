# Phase 10 Retrieval Evaluation Expansion

Generated at: `2026-08-26`

## Purpose

Phase 10 expands the validated retrieval surface for Chinese board-game queries before adding heavier retrieval methods such as neural embeddings. The goal is to make common Chinese game names and mechanism phrases auditable through a reusable query suite, not just through one-off manual checks.

## Changes

- Expanded `scripts/retrieval_common.py` with high-confidence Chinese-to-English query expansions for 30 well-known games and 28 common mechanisms.
- Expanded exact entity routing for Chinese aliases and canonical English titles where the BGG ID is unambiguous.
- Added `scripts/retrieval_suite_expanded.py`, a deterministic Phase 10 query suite with 146 validated queries.
- Added `scripts/export_retrieval_suite_expanded.py`, an exporter/evaluator that writes JSONL, summary JSON, and Markdown reports.
- Generated reusable Phase 10 outputs in `raw_index/` and `docs/`.

## Evaluation Scope

| Area | Queries | Passed |
| --- | ---: | ---: |
| `game_overview` | 60 | 60 |
| `review_digest` | 30 | 30 |
| `mechanic_profile` | 56 | 56 |
| Total | 146 | 146 |

Validation used the Phase 9 unified interface with the hybrid engine:

```powershell
python scripts\export_retrieval_suite_expanded.py --engine hybrid --limit 5 --candidate-limit 50
```

Result:

- Suite size: `146`
- Validated queries: `146`
- Passed: `146`
- Failed: `0`
- Pass rate: `1.0`
- Output JSONL: `raw_index/retrieval_suite_expanded.jsonl`
- Summary JSON: `raw_index/retrieval_suite_expanded_summary.json`
- Full report: `docs/retrieval_suite_expanded_report.md`

## Coverage Added

Game aliases now cover gateway games, top-ranked strategy games, cooperative/campaign games, and common Chinese localized names, including CATAN, Carcassonne, Brass: Birmingham, Pandemic Legacy: Season 1, Ark Nova, Gloomhaven, Dune: Imperium, Terraforming Mars, Through the Ages, Ticket to Ride, Dominion, Codenames, Azul, Splendor, Pandemic, 7 Wonders, Dixit, Patchwork, Hanabi, and King of Tokyo.

Mechanism aliases now cover worker placement, deck/bag/pool building, dice rolling, auction, area majority, action points, hand management, set collection, variable player powers, cooperative game, campaign/scenario play, tile placement, network/route building, simultaneous action selection, card drafting, hidden roles, storytelling, trick-taking, push your luck, bluffing, modular board, hex grid, income, negotiation, trading, and random production.

## Notes

- Chinese aliases are expansion/routing helpers only; the underlying RAG documents remain English-heavy because they are built from the local BGG-derived datasets.
- Broad mechanism labels such as auction intentionally accept canonical sub-mechanics in evaluation when the taxonomy has split labels.
- Review digests remain local extractive summaries of BGG user-generated content and should not be published externally before legal/release review.
- Windows PowerShell can corrupt Chinese text when writing through here-strings or shell pipelines. Phase 10 files were validated by UTF-8 readback with zero question-mark mojibake runs and zero replacement characters.

## Recommended Next Work

1. Add a lightweight regression command that runs Phase 9 and Phase 10 suites together.
2. Add optional `--suite base|expanded|all` support to a unified suite exporter.
3. Start Phase 11 neural-embedding design only after deciding whether local/offline embeddings or API embeddings are acceptable.
