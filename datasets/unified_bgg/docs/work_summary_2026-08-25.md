# unified_bgg 当前工作总结

生成日期：2026-08-25  
项目目录：`D:\OpenViking\research\datasets\unified_bgg`  
当前版本：`0.4.0-taxonomy-canonical`  
当前状态：`phase_4_taxonomy_canonicalization_generated`

## 1. 项目目标

`unified_bgg` 是 OpenViking 项目下的统一 BoardGameGeek 桌游数据集整合工程。目标是把多个公开 BGG 数据集整合为一个可长期维护的数据底座，用于后续两类任务：

1. 面向 RAG / 数据召回：生成统一游戏实体、机制/分类画像、评论摘要和可向量化文本。
2. 面向模型微调：生成游戏问答、机制解释、推荐理由、评论总结、结构化抽取等训练样本。

核心原则是：以 BGG 官方游戏 ID 作为实体对齐锚点，保留来源、快照日期和转换规则，避免把不同年份、不同来源的评分/排名/标签直接混合为单一事实。

## 2. 源数据集范围

当前纳入 7 个公开 BGG 数据集，源数据根目录为 `D:\OpenViking\research\datasets`，总大小约 3.02GB。

| 数据集 | 主要价值 | 当前处理定位 |
| --- | --- | --- |
| `bgg-reviews-jvanelteren` | 2020/2022/2025 游戏元数据、2025 详细信息、约 26M 评论/评分 | 作为 2025 游戏与 taxonomy canonical anchor 的核心来源；大评论表暂未默认扫描 |
| `bgg-threnjen` | 21,925 款游戏，多表结构，18,942,215 条用户评分，411,375 位用户 | 后续协同过滤和用户级评分矩阵的首选来源 |
| `bgg-gabrio` | SQLite 数据库，约 90,400 行，包含扩展与 2017 标签 | 提供大覆盖面历史元数据和旧 taxonomy 词表 |
| `bgg-ranked-mattadamhouser` | 2023 Top-2000、排名与 reimplementation 关系 | 提供较新的排名快照和关系补充 |
| `bgg-mrpantherson` | 2017-04、2018-01、2018-06 三个 Top-5000 快照 | 用于时间快照型排名/统计补充 |
| `bgg-andrewmvd` | 2021 结构化 CSV，含机制/分类等字段 | 补充 2021 快照和 domain/mechanic 信息 |
| `bgg-sujaykapadnis` | `bgg-gabrio` 的派生/子集数据 | 不作为独立强证据重复计权，仅作为兼容来源记录 |

## 3. 已完成阶段

### 阶段 1：目录、盘点、schema 与来源优先级

已完成统一数据集脚手架和源数据盘点，生成基础文档与 profiling 结果。

关键产物：

- `README.md`
- `manifest.json`
- `docs/dataset_inventory.md`
- `docs/profiling_report.md`
- `docs/unified_schema.md`
- `docs/source_priority.md`
- `docs/known_issues.md`
- `scripts/profile_sources.py`
- `raw_index/source_files.json`

主要结论：

- 本地 7 个源数据集均存在。
- 大行级文件默认跳过，避免无必要的超大规模扫描。
- 后续统一表设计拆分为实体、统计快照、taxonomy、评分、评论和数据血缘，而不是直接合并为一张宽表。

### 阶段 2：实体对齐基础

已完成基于 BGG 官方 ID 的初始实体对齐。

关键产物：

- `scripts/build_id_map.py`
- `docs/id_profile_report.md`
- `raw_index/id_profiles.json`
- `raw_index/id_sets.json`
- `raw_index/name_conflicts.json`
- `intermediate/id_map.csv`
- `intermediate/dataset_id_coverage.csv`

关键指标：

| 文件 | 行数 / 指标 |
| --- | ---: |
| `intermediate/id_map.csv` | 345,282 行 |
| 唯一 BGG ID | 100,274 个 |

主要决策：

- 内部统一 ID 格式为 `bgg:{bgg_id}`。
- 以 BGG ID exact match 作为当前实体对齐基础，不用名称模糊匹配替代 ID。
- 名称冲突保留到 `name_conflicts.json`，作为后续人工复核或实体别名处理输入。
- `bgg-reviews-jvanelteren/raw/bgg-26m-reviews.csv` 与 `bgg-threnjen/raw/user_ratings.csv` 暂不默认扫描；如需完整扫描，使用 `scripts/build_id_map.py --include-large`。

### 阶段 3：核心中间表转换

已完成三张核心中间表：游戏主表、统计快照表、原始 taxonomy 关系表。

关键产物：

- `scripts/build_core_tables.py`
- `docs/core_tables_report.md`
- `raw_index/core_table_summary.json`
- `intermediate/games.csv`
- `intermediate/game_stats.csv`
- `intermediate/game_taxonomy.csv`

关键指标：

| 表 | 行数 | 说明 |
| --- | ---: | --- |
| `intermediate/games.csv` | 100,274 | 统一游戏实体表 |
| `intermediate/game_stats.csv` | 291,640 | 多来源、多快照统计表 |
| `intermediate/game_taxonomy.csv` | 1,164,739 | 原始 taxonomy 关系表 |

补充指标：

- `games.csv` 中 100,099 行带 description。
- `games.csv` 中 4 个缺失 `primary_name` 的 ID 已标记 `needs_review=true`。
- `game_stats.csv` 覆盖全部 7 个源数据集。
- `game_taxonomy.csv` taxonomy 类型包括 `mechanic`、`category`、`family`、`domain`、`theme`、`subcategory`。

### 阶段 4：taxonomy alias 与 canonicalization

已完成 taxonomy 词表盘点、别名映射和 canonical 关系表生成。

关键产物：

- `scripts/build_taxonomy_aliases.py`
- `docs/taxonomy_profile_report.md`
- `raw_index/taxonomy_profile.json`
- `intermediate/taxonomy_aliases.csv`
- `intermediate/game_taxonomy_canonical.csv`

关键指标：

| 表 / 指标 | 数值 |
| --- | ---: |
| `intermediate/taxonomy_aliases.csv` | 15,149 行 |
| `intermediate/game_taxonomy_canonical.csv` | 1,160,887 行 |
| 被排除 invalid placeholder 标签行数 | 3,852 行 |
| canonical 表中 invalid placeholder 标签 | 0 行 |
| `canonical_needs_review=false` | 1,075,150 行 |
| `canonical_needs_review=true` | 85,737 行 |

canonical anchor 策略：

- `mechanic`、`category`、`family`：优先使用 2025-02 `bgg-reviews-jvanelteren` 词表作为 canonical anchor。
- `domain`、`theme`、`subcategory`：当前中间表没有对应的 2025 reference 表，因此暂时使用 self-canonical 策略。
- 旧标签不会被无脑字符串拼接；通过 `taxonomy_aliases.csv` 记录 raw label 到 canonical label 的映射策略。

alias 策略统计：

| 策略 | 数量 |
| --- | ---: |
| `canonical_reference_exact` | 4,484 |
| `exact_label_match` | 5,335 |
| `normalized_label_match` | 54 |
| `manual_alias` | 20 |
| `ambiguous_legacy_label` | 2 |
| `invalid_label` | 3 |
| `unmapped_raw_fallback` | 5,251 |

已处理的典型别名包括：

- `Auction/Bidding` -> `Auction / Bidding`
- `Action/Event` -> `Action / Event`
- `Deck Bag and Pool Building` -> `Deck, Bag, and Pool Building`
- `Action Point Allowance System` -> `Action Points`
- `Area Control / Area Influence` -> `Area Majority / Influence`
- `Co-operative Play` -> `Cooperative Game`

仍需人工复核的典型标签：

- `Action / Movement Programming`：可能需要拆分为 `Action Queue` / `Programmed Movement`。
- `Card Drafting` / `Drafting`：2025 词表可能已有拆分或语义调整，当前未强行映射。
- `Dexterity`、`Physical`、`Time Track`、`TableauBuilding`、`Multiple-Lot Auction`：建议后续人工确认。

## 4. 当前文件清单

### 文档

- `README.md`
- `docs/dataset_inventory.md`
- `docs/profiling_report.md`
- `docs/id_profile_report.md`
- `docs/core_tables_report.md`
- `docs/taxonomy_profile_report.md`
- `docs/unified_schema.md`
- `docs/source_priority.md`
- `docs/known_issues.md`
- `docs/work_summary_2026-08-25.md`

### 脚本

- `scripts/profile_sources.py`
- `scripts/build_id_map.py`
- `scripts/build_core_tables.py`
- `scripts/build_taxonomy_aliases.py`

### raw_index

- `raw_index/source_files.json`
- `raw_index/id_profiles.json`
- `raw_index/id_sets.json`
- `raw_index/name_conflicts.json`
- `raw_index/core_table_summary.json`
- `raw_index/taxonomy_profile.json`

### intermediate

- `intermediate/id_map.csv`
- `intermediate/dataset_id_coverage.csv`
- `intermediate/games.csv`
- `intermediate/game_stats.csv`
- `intermediate/game_taxonomy.csv`
- `intermediate/taxonomy_aliases.csv`
- `intermediate/game_taxonomy_canonical.csv`

## 5. 关键工程决策

1. 实体对齐锚点使用 BGG 官方游戏 ID，不用游戏名作为主键。
2. 内部统一游戏 ID 使用 `bgg:{bgg_id}`。
3. 评分、排名、用户数等时间敏感字段必须保留 `snapshot_date` 和 `source_dataset`。
4. taxonomy 采用 raw label、canonical label、alias strategy、needs_review 的可追踪结构。
5. `bgg-sujaykapadnis` 是 `bgg-gabrio` 的严格子集，不应作为独立证据源重复加权。
6. 大型逐行评分/评论文件目前暂不默认处理，避免在 schema 和 source semantics 未稳定前引入高成本数据处理。
7. 所有派生事实都应保留来源数据集、来源文件和转换规则，方便回溯与重建。

## 6. 已知问题与注意事项

- `bgg-reviews-jvanelteren/raw/bgg-26m-reviews.csv` 很大，约 26M 行，只有约 16.09% ratings 带 comment 文本；后续处理评论时需要分块扫描。
- `bgg-threnjen/raw/user_ratings.csv` 有 18,942,215 行，适合协同过滤，但不应在不需要用户级数据时默认扫描。
- `bgg-threnjen` 的 `Rank:*` 列使用 `21926` 作为未排名哨兵值，不是普通数值排名。
- `bgg-threnjen` 的 `NumComments` 是废列，不能作为评论数量依据。
- `bgg-gabrio` 中 `game.id` 以 text 形式存储，`stats.bayesaverage=0` 应视为 unknown。
- `bgg-andrewmvd` 使用分号分隔与欧洲小数逗号，读取时需要指定解析规则。
- `bgg-mrpantherson` 的 2017-04/2018-01 快照为 cp1252，2018-06 为 UTF-8。
- Windows PowerShell 5.1 下中文 here-string 曾出现编码污染；涉及中文 Markdown 写入时应优先使用 `apply_patch` 或 Python `Path.write_text(..., encoding="utf-8")` 配合 Unicode 转义。

## 7. OpenViking 记忆状态

当前项目进展已经在 OpenViking 中有可检索记忆，主要线索：

- `viking://user/default/memories/entities/桌游数据集工程/unified_bgg.md`
- 可检索关键词：`unified_bgg`、`taxonomy canonicalization`、`phase_4_taxonomy_canonicalization_generated`、`桌游数据集工程`

如果后续重启 Codex 或切换会话，可以先检索这些关键词恢复上下文。

## 8. 下一阶段建议

建议进入第 5 阶段：生成 RAG 用数据产品。推荐顺序如下：

1. 先生成 preview 样本，而不是一次性全量生成。
2. 生成 `samples/rag/game_overview.jsonl`：每个游戏一条概览文档，整合 `games.csv`、最新/可信统计快照、canonical taxonomy。
3. 生成 `samples/rag/mechanic_profile.jsonl`：每个 canonical mechanic 一条机制画像，包含代表游戏、共现标签、评分/排名分布。
4. 设计 `review_digest.jsonl` 的输入策略，决定是否开始分块扫描 26M 评论表。
5. 质量检查 preview 样本：事实一致性、来源可追踪性、是否混淆旧/新 taxonomy、中文/英文输出策略。
6. 通过验证后，再批量生成 RAG 样本和后续微调样本。

## 9. 当前可恢复状态

如果需要从当前状态继续工作，最小恢复步骤是：

```powershell
cd D:\OpenViking\research\datasets\unified_bgg
python scripts\build_id_map.py
python scripts\build_core_tables.py
python scripts\build_taxonomy_aliases.py
```

当前已经生成的中间表足够支撑下一步 RAG preview 生成，不必先处理 26M 评论/评分大表。
