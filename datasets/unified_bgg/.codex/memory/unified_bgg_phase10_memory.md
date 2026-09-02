# unified_bgg Phase 10 Memory

Date: 2026-08-26

Project root: `D:\OpenViking\research\datasets\unified_bgg`

## Milestone

Phase 10 is complete. The project advanced from `0.9.0-unified-retrieval-interface` to `0.10.0-expanded-retrieval-eval`, with status `phase_10_expanded_retrieval_eval_built_and_validated`.

## What Changed

- Expanded Chinese query expansion and exact entity routing in `scripts/retrieval_common.py`.
- Added 30 high-confidence game alias routes, covering CATAN, Carcassonne, Brass: Birmingham, Pandemic Legacy: Season 1, Ark Nova, Gloomhaven, Twilight Imperium: Fourth Edition, Dune: Imperium, Terraforming Mars, War of the Ring: Second Edition, Star Wars: Rebellion, Spirit Island, Gaia Project, Twilight Struggle, Through the Ages, The Castles of Burgundy, Ticket to Ride, Dominion, Codenames, Azul, Splendor, Love Letter, Pandemic, 7 Wonders, Dixit, Patchwork, Small World, Hanabi, King of Tokyo, and selected The Crew titles.
- Added Chinese mechanism expansion coverage for 28 mechanism families, including worker placement, deck/bag/pool building, dice rolling, auction, area majority, action points, hand management, set collection, cooperative game, campaign/scenario play, tile placement, route building, card drafting, hidden roles, storytelling, trick-taking, push-your-luck, bluffing, modular board, hex grid, income, negotiation, trading, and random production.
- Added `scripts/retrieval_suite_expanded.py` and `scripts/export_retrieval_suite_expanded.py`.
- Generated `raw_index/retrieval_suite_expanded.jsonl`, `raw_index/retrieval_suite_expanded_summary.json`, `docs/retrieval_suite_expanded_report.md`, and `docs/phase10_retrieval_eval_expansion.md`.
- Updated `README.md` and `manifest.json`.

## Validation

Command:

```powershell
python scripts\export_retrieval_suite_expanded.py --engine hybrid --limit 5 --candidate-limit 50
```

Result:

- Suite size: 146
- Validated queries: 146
- Passed: 146
- Failed: 0
- Pass rate: 1.0
- Per doc type: `game_overview` 60/60, `review_digest` 30/30, `mechanic_profile` 56/56

Additional checks:

- `python -m py_compile` passed for modified retrieval scripts.
- UTF-8 readback confirmed zero replacement characters and zero question-mark mojibake runs in modified scripts, generated JSON/JSONL, and generated Markdown.

## Important Lesson

Do not write Chinese source files through PowerShell here-strings or fragile shell pipelines. Use `apply_patch` or a Python writer with safe UTF-8 handling, then validate by reading files back with `encoding="utf-8"`.

## Recommended Next Work

1. Add a combined regression runner for Phase 9 base suite plus Phase 10 expanded suite.
2. Add `--suite base|expanded|all` support to the retrieval-suite exporter.
3. Decide whether Phase 11 should use local/offline embeddings or API embeddings before building a neural vector index.
