---
name: unified-bgg-rag-retrieval
description: Query and explain the unified BoardGameGeek dataset for board-game design work. Use when a user asks to find a game, compare mechanisms, retrieve rules or reviews, recommend games, inspect player-count profiles, or generate a Markdown game report from unified_bgg or its Hugging Face dataset.
---

# Unified BGG Retrieval Skill

Use the ready-made `unified_bgg` data products as the default source for board-game design and research questions. Do not ask beginners to rebuild the dataset. First use the local indexes; if they are absent, follow the Hugging Face download guide and then retry.

## Data products

- `game_overview`: one structured overview per game, including players, time, ratings, rank, complexity, taxonomy and description.
- `mechanic_profile`: canonical mechanism profiles with representative games and co-occurrence evidence.
- `review_digest`: per-game rating/comment coverage and summarized player sentiment. Treat text as BGG user-generated content.
- `rulebook_text`: extracted rulebook or rule-summary text for the selected high-rated games.

The stable entity key is `bgg:{bgg_id}`. Prefer an exact BGG ID when a title may refer to an expansion, edition or localized variant.

## Beginner workflow

1. Confirm the requested game or mechanism and resolve an exact BGG ID when possible.
2. Query the unified index with the bundled helper or `query_unified_index.py`.
3. For a game report, retrieve both `game_overview` and `review_digest`; add `rulebook_text` when the user asks about rules or action flow.
4. For mechanism research, query `mechanic_profile` and then retrieve representative game overviews.
5. Separate sourced facts, rule summaries, and interpretation. Keep snapshot dates and source files visible for ratings/ranks.
6. Summarize review themes instead of reproducing long user comments.
7. Return concise Markdown with sources (`doc_id`, `game_id`, BGG ID and source file). Write durable reports only to a user-requested output path.

## Commands

Run from `datasets/unified_bgg` in this repository:

```powershell
python scripts/query_unified_index.py "Brass Birmingham loans network" --engine hybrid --limit 5
python scripts/query_unified_index.py "卡坦岛 交易 资源" --doc-type game_overview --limit 5 --markdown
python scripts/query_unified_index.py "Gloomhaven rules" --doc-type rulebook_text --bgg-id 174430 --json
```

For a compact overview plus review digest:

```powershell
python skills/unified-bgg-rag-retrieval/scripts/query_unified_bgg_game.py "Catan trading negotiation" --bgg-id 13 --markdown
```

The unified CLI supports `--engine auto|fts|vector|hybrid`, `--limit`, `--candidate-limit`, `--doc-type`, `--game-id`, `--bgg-id`, `--json` and `--markdown`.

## Missing local data

Download ready-made data or indexes from `ChenJinHua/BGG_datasets_Agent` using `HUGGINGFACE_DATA_GUIDE.md`. Restore files under `datasets/` or pass explicit `--fts-index`/`--vector-index` paths. Do not rebuild raw tables unless the task is dataset engineering.

## Reporting contract

For Chinese game reports, use this order when relevant:

1. 游戏身份：名称、常见中文名、BGG ID、年份和类型。
2. 基础事实：人数、时长、年龄、评分、排名、复杂度和快照日期。
3. 实际游玩流程：回合、行动链、资源门槛和局面后果。
4. 核心机制：只解释该游戏中真实出现的机制及其作用。
5. 规则/规则书证据：标明是规则书文本、游戏描述还是推断。
6. 玩家体验：正面、混合和负面评论主题，并给出样本覆盖。
7. 设计启发：可迁移的机制结构，明确标注分析性结论。
8. 来源：文档 ID、数据类型、源文件和本地/Hugging Face 路径。

Never invent edge cases that are not present in the retrieved text. Mention when a rulebook source is missing or a value comes from an older snapshot.

## Local environment

The bundled helper discovers the repository copy automatically and accepts `--project` for another checkout. Set `UNIFIED_BGG_ROOT` when the data lives outside the repository. Keep all generated Chinese Markdown in UTF-8.
