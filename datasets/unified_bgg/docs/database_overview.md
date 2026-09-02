# unified_bgg 桌游数据库说明

生成日期：2026-08-25  
数据库目录：`D:\OpenViking\research\datasets\unified_bgg`  
当前版本：`0.6.1-rag-text-health-cleanup`  
当前状态：`phase_6_1_rag_text_health_cleaned_and_index_rebuilt`

## 1. 这是什么数据库

`unified_bgg` 是一个围绕 BoardGameGeek（BGG）公开桌游数据构建的统一桌游数据库。它不是简单地把多个 CSV 拼在一起，而是把多个年份、多个来源、多个格式的 BGG 数据清洗、对齐、标准化，并进一步加工成适合大模型使用的检索数据产品。

从使用角度看，它已经具备三种能力：

1. **桌游实体库**：回答“某款桌游是什么、年份、人数、时长、评分、复杂度、机制、分类”等问题。
2. **机制与分类知识库**：回答“某个机制有哪些代表游戏、常见搭配机制、常见类别和评分分布”等问题。
3. **评论摘要库**：回答“玩家对某款游戏的正面、中性、负面评价集中在哪里”等问题。

最终目标是服务两个方向：

- **RAG 召回**：让大模型能够检索可靠的桌游事实、机制画像和评论摘要。
- **模型微调**：后续生成桌游问答、机制解释、推荐理由、评论总结、结构化抽取等训练样本。

## 2. 数据来源

当前数据库整合了 7 个本地公开 BGG 数据集，源数据总大小约 3.02GB。

| 数据集 | 时间 / 特点 | 在本数据库中的作用 |
| --- | --- | --- |
| `bgg-reviews-jvanelteren` | 2025-02；包含 26,200,012 条评分/评论行，27,865 款游戏，555,482 位用户；另有 2025 详细游戏元数据 | 最新、最重要的元数据来源；也是评论摘要与 2025 机制/分类 canonical anchor 的核心来源 |
| `bgg-threnjen` | 2021-12；21,925 款游戏，18,942,215 条用户评分，411,375 位用户 | 用户级评分矩阵与协同过滤潜在来源；补充 2021 快照的机制、主题、分类 |
| `bgg-gabrio` | 2017-06；SQLite；90,400 行，含 13,712 个扩展 | 覆盖面广，补充旧年份、扩展、历史描述与 2017 taxonomy |
| `bgg-ranked-mattadamhouser` | 2023-08；Top-2000，188 个机制字段，含 reimplementation 关系 | 补充头部游戏、排名、较新机制拆分与重实现关系 |
| `bgg-mrpantherson` | 2017-04 / 2018-01 / 2018-06 三个 Top-5000 快照 | 用于历史排名和评分漂移观察 |
| `bgg-andrewmvd` | 2021-02；20,343 行，CC BY 4.0 | 轻量级结构化补充，含机制、分类、domain 信息 |
| `bgg-sujaykapadnis` | TidyTuesday 派生数据，10,532 行 | 已确认是 `bgg-gabrio` 严格子集，仅保留 lineage，不作为独立证据重复加权 |

## 3. 数据库解决了什么问题

公开 BGG 数据集的问题不是“没有数据”，而是“数据很难直接统一使用”：

- 同一个游戏出现在多个数据集中，字段名、时间快照、评分口径不同。
- 机制名称会随年份变化，例如旧数据中的机制标签和 2025 词表并不完全一致。
- 评论与评分文件巨大，不能每次查询都扫描 26M 行。
- 有些数据集有编码、分隔符、哨兵值、缺失值和废列问题。
- 直接用原始表做 RAG，容易混淆来源、年份、评分口径和标签语义。

`unified_bgg` 的价值在于：

1. 用 BGG 官方 ID 对齐实体。
2. 把时间敏感事实保留为快照行，而不是覆盖成单一值。
3. 把机制、分类、家族等 taxonomy 映射到可追踪的 canonical 形式。
4. 把大型评论文件压缩成每个游戏一条可检索的 `review_digest`。
5. 把最终 RAG 文档建成本地 SQLite FTS5 检索索引，便于快速查询。

## 4. 当前核心内容

### 4.1 中间层表

这些表位于 `intermediate/`，是数据库的结构化基础。

| 文件 | 行数 | 用途 |
| --- | ---: | --- |
| `intermediate/id_map.csv` | 345,282 | 源数据 ID 到统一 `bgg:{id}` 的映射表 |
| `intermediate/games.csv` | 100,274 | 统一游戏主表，一行一个游戏实体 |
| `intermediate/game_stats.csv` | 291,640 | 多来源、多时间快照的评分、排名、复杂度统计 |
| `intermediate/game_taxonomy.csv` | 1,164,739 | 原始 taxonomy 长表，保留 raw label 与来源 |
| `intermediate/taxonomy_aliases.csv` | 15,149 | raw label 到 canonical label 的别名映射表 |
| `intermediate/game_taxonomy_canonical.csv` | 1,160,887 | 标准化后的 taxonomy 关系表 |

`games.csv` 当前包含：

- 100,274 个统一 BGG 游戏实体
- 86,489 个基础桌游
- 13,633 个扩展
- 100,099 条带描述文本的游戏记录

### 4.2 taxonomy 标准化内容

taxonomy 包括：

- `mechanic`
- `category`
- `family`
- `domain`
- `theme`
- `subcategory`

当前 canonical 词表规模：

| 类型 | canonical 词表规模 |
| --- | ---: |
| `mechanic` | 192 |
| `category` | 84 |
| `family` | 4,208 |
| `domain` | 8 |
| `theme` | 241 |
| `subcategory` | 10 |

映射策略统计：

| 策略 | 数量 |
| --- | ---: |
| `canonical_reference_exact` | 4,484 |
| `exact_label_match` | 5,335 |
| `normalized_label_match` | 54 |
| `manual_alias` | 20 |
| `ambiguous_legacy_label` | 2 |
| `invalid_label` | 3 |
| `unmapped_raw_fallback` | 5,251 |

质量状态：

- canonical taxonomy 输出：1,160,887 行
- 被排除的 invalid placeholder 行：3,852
- `canonical_needs_review=false`：1,075,150 行
- `canonical_needs_review=true`：85,737 行

## 5. RAG 数据产品

RAG 数据位于 `samples/rag/`，是面向检索增强生成的文本化数据产品。

| 文件 | 行数 | 说明 |
| --- | ---: | --- |
| `samples/rag/game_overview.jsonl` | 100,274 | 每个游戏一条概览文档，整合基础信息、评分、机制、分类、描述 |
| `samples/rag/mechanic_profile.jsonl` | 192 | 每个 canonical 机制一条画像，包含代表游戏、共现机制、常见分类和评分统计 |
| `samples/rag/review_digest.jsonl` | 27,851 | 每个有非空评论的游戏一条评论摘要，包含评分分布和代表性正/中/负评论片段 |

这些 RAG 文档总计：

- 128,317 条文档
- 128,317 个唯一 `doc_id`
- 当前质量审计中没有 duplicate `doc_id`
- 当前质量审计中没有文本健康问题（`text_flags={}`）

### 5.1 game_overview 的用途

适合回答：

- “这款游戏是什么？”
- “适合几个人玩？”
- “评分、排名、复杂度是多少？”
- “它有哪些机制和分类？”
- “它是基础游戏还是扩展？”

示例：

```powershell
python scripts/query_rag_index.py "Through the Ages civilization" --doc-type game_overview --limit 3
```

### 5.2 mechanic_profile 的用途

适合回答：

- “某个机制是什么意思？”
- “这个机制有哪些代表游戏？”
- “它经常和哪些机制一起出现？”
- “某个机制常见于哪些游戏类型？”

示例：

```powershell
python scripts/query_rag_index.py "deck bag pool building" --doc-type mechanic_profile --limit 3
```

### 5.3 review_digest 的用途

适合回答：

- “玩家对这款游戏的主要好评是什么？”
- “玩家批评这款游戏的点在哪里？”
- “这款游戏评论覆盖率和评分分布如何？”
- “它适合从评论角度做推荐理由总结吗？”

评论摘要来自 `bgg-reviews-jvanelteren/raw/bgg-26m-reviews.csv` 的流式扫描：

| 指标 | 数值 |
| --- | ---: |
| 扫描原始评分/评论行 | 26,200,012 |
| malformed rows | 0 |
| 有评分游戏数 | 27,865 |
| 有非空评论游戏数 | 27,851 |
| 清洗后非空评论数 | 4,206,543 |
| 评论覆盖率 | 16.0555% |

示例：

```powershell
python scripts/query_rag_index.py "Catan trading negotiation comments" --doc-type review_digest --bgg-id 13 --limit 1
```

## 6. 本地检索索引

当前已构建本地 SQLite FTS5 索引：

- 文件：`final/rag_index.sqlite`
- 索引类型：SQLite FTS5
- 索引文档数：128,317
- FTS 行数：128,317
- 索引大小：约 1.11GB

索引包含三类文档：

| doc_type | 文档数 |
| --- | ---: |
| `game_overview` | 100,274 |
| `mechanic_profile` | 192 |
| `review_digest` | 27,851 |

查询入口：

```powershell
python scripts/query_rag_index.py "<query>" --doc-type <game_overview|mechanic_profile|review_digest>
```

如果知道 BGG ID，建议加 `--bgg-id` 精确过滤，尤其是 `Catan`、`Gloomhaven`、`Through the Ages` 这类存在扩展、重制版或同名相关作品的查询。

## 7. 数据库的主要功效

### 7.1 面向大模型 RAG

它可以作为桌游领域的本地知识底座，让模型在回答前先检索：

- 桌游实体事实
- 机制画像
- 玩家评论摘要
- 评分、排名、复杂度
- 分类与主题信息

这能减少模型对桌游事实、机制、评价的幻觉。

### 7.2 面向桌游推荐

数据库可以支持多维推荐：

- 按机制推荐：例如 deck building、worker placement、area control
- 按主题推荐：文明、经济、战争、奇幻、科幻
- 按复杂度推荐：轻度、中度、重度
- 按玩家评论倾向推荐：好评集中点、差评风险点
- 按相似游戏推荐：通过 taxonomy、评分、评论摘要联合判断

### 7.3 面向桌游机制 Agent

对于“桌游机制 Agent”来说，它提供：

- 机制名称的标准化词表
- 机制之间的共现关系
- 每个机制的代表游戏
- 机制与分类、主题、评分的关系
- 可用于解释机制、比较机制、生成设计建议的数据基础

### 7.4 面向模型微调

后续可从当前数据库派生：

- `game_qa`
- `mechanic_explanation`
- `recommendation_reasoning`
- `review_summary`
- `extraction`

当前 RAG 文档已经具备生成这些样本的基础结构。

## 8. 数据库的目录结构

核心目录如下：

```text
unified_bgg/
  README.md
  manifest.json
  docs/
    database_overview.md
    unified_schema.md
    source_priority.md
    known_issues.md
    rag_quality_report.md
    rag_index_report.md
  intermediate/
    games.csv
    game_stats.csv
    game_taxonomy.csv
    taxonomy_aliases.csv
    game_taxonomy_canonical.csv
  samples/
    rag/
      game_overview.jsonl
      mechanic_profile.jsonl
      review_digest.jsonl
  final/
    rag_index.sqlite
  scripts/
    build_id_map.py
    build_core_tables.py
    build_taxonomy_aliases.py
    build_rag_samples.py
    build_review_digest.py
    evaluate_rag_quality.py
    build_rag_index.py
    query_rag_index.py
```

## 9. 质量状态

当前 RAG 质量审计结果：

| 指标 | 数值 |
| --- | ---: |
| parsed docs | 128,317 |
| unique doc IDs | 128,317 |
| duplicate doc IDs | 0 |
| text health flags | 0 |
| finding rows | 0 |

仍需注意的结构性现象：

| 现象 | 数量 | 解释 |
| --- | ---: | --- |
| 缺 reliable mechanics 的游戏文档 | 15,670 | 多为旧数据、冷门游戏或 taxonomy 不完整游戏 |
| 扩展文档 | 13,633 | 数据库保留扩展，但做基础游戏分析时可过滤 |
| 缺评分值的游戏文档 | 24,339 | 多为冷门、旧来源或无当前评分快照游戏 |
| `game_needs_review` | 4 | 需要人工复核的少量游戏实体 |
| 缺 selected overall stats | 3 | 极少数缺少可用统计快照的实体 |
| review digest 缺 positive snippets | 3,591 | 评论数量少或无高分长评论 |
| review digest 缺 mixed snippets | 995 | 评论数量少或评分分布单一 |
| review digest 缺 critical snippets | 2,547 | 评论数量少或缺低分长评论 |
| very low comment coverage | 7 | 评论覆盖率低于 2% 的游戏 |

这些不是当前数据库不可用的错误，而是用于后续筛选、召回路由和质量控制的元信息。

## 10. 当前限制

1. **许可限制**：部分源数据 license 为 Other/unclear，尤其是评论文本属于 BGG 用户生成内容，`review_digest` 应保持本地研究使用，发布或商用前需要 legal/release review。
2. **评论不是完整语料发布品**：当前只生成每个游戏的 extractive digest，没有物化完整逐行 `reviews` 表。
3. **FTS 是词法检索，不是向量检索**：当前 `rag_index.sqlite` 适合本地快速 BM25/FTS 查询；如果要语义召回，还需要 embedding + vector index。
4. **taxonomy 仍有人工复核项**：尤其是历史机制标签和 2025 词表之间存在语义拆分的标签。
5. **评分是快照事实**：评分、排名、复杂度来自不同时间和来源，不能视为实时 BGG 状态。

## 11. 如何使用这个数据库

### 查询某款游戏简介

```powershell
python scripts/query_rag_index.py "Through the Ages civilization" --doc-type game_overview --limit 3
```

### 查询某款游戏评论摘要

```powershell
python scripts/query_rag_index.py "Through the Ages comments" --doc-type review_digest --bgg-id 182028 --limit 1
```

### 查询某个机制画像

```powershell
python scripts/query_rag_index.py "deck bag pool building" --doc-type mechanic_profile --limit 3
```

### 查询 Catan 评论摘要

```powershell
python scripts/query_rag_index.py "Catan trading negotiation comments" --doc-type review_digest --bgg-id 13 --limit 1
```

## 12. 适合下一步做什么

建议的下一阶段：

1. **taxonomy 人工复核**：把 `canonical_needs_review=true` 的重点机制标签做人工决策。
2. **微调样本 preview**：从 `game_overview`、`mechanic_profile`、`review_digest` 生成小规模 QA / explanation / summary 样本。
3. **向量检索实验**：在 SQLite FTS 的基础上增加 embedding 检索与 rerank。
4. **最终发布格式**：生成 Parquet / DuckDB / SQLite 结构化版本。
5. **许可证与归因文档**：整理 `license_release_review.md` 与 `attribution.md`。

## 13. 一句话总结

`unified_bgg` 当前已经是一个可检索、可审计、可扩展的桌游领域数据库：它把 7 个公开 BGG 数据源整合为 100,274 个游戏实体、192 个标准机制画像、27,851 个评论摘要，并构建了 128,317 条 RAG 文档和本地 SQLite FTS 检索索引，可直接支持桌游问答、机制解释、推荐理由和后续微调样本生成。
