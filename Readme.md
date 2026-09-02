# OpenViking Research 项目总览

> 项目根目录：`D:\OpenViking\research`  
> 文档用途：说明研究资料、原始数据集、`unified_bgg` 统一桌游数据库及其 RAG/微调数据产品的组成、功能和完整使用流程。  
> 文档更新：2026-09-02

## 1. 项目定位

本目录是 OpenViking 项目中的桌游数据集调研与工程工作区，目标是为“桌游机制 Agent”提供可追溯的数据基础。项目把多个年份、多个格式、不同字段口径的 BoardGameGeek（BGG）公开快照集中管理，并逐步加工为：

- 可用于统计分析、协同过滤和推荐的结构化数据；
- 以 BGG 官方游戏 ID 对齐的统一实体、评分快照和 taxonomy 关系表；
- 面向 RAG 的游戏概览、机制画像、玩家评论摘要和规则书文本；
- 面向后续模型微调的问答、机制解释、推荐理由、评论总结和结构化抽取样本；
- 可在本地运行的 SQLite FTS5/BM25、稀疏 TF-IDF 和混合检索接口。

该目录不是一个 Web 服务，而是一套“原始数据 -> 规范化中间表 -> RAG/微调样本 -> 本地索引 -> 查询与评测”的离线研究流水线。

## 2. 当前状态

| 项目 | 当前结果 |
| --- | ---: |
| 原始 BGG 数据集 | 7 个，约 3.02 GB |
| 统一游戏实体 | 约 100,274 个 BGG ID |
| `id_map.csv` | 345,282 条来源映射 |
| `game_stats.csv` | 291,640 条快照统计 |
| 原始 taxonomy 关系 | 1,164,739 条 |
| canonical taxonomy 关系 | 1,162,257 条 |
| RAG 文档 | 约 128,320 条（游戏、机制、评论；另有规则书语料） |
| 微调预览样本 | 5 类各 50 条，共 250 条 |
| 微调候选样本 | 4,195 条 |
| 规则书语料 | 选取 100 个高分游戏，全部成功写入语料 |
| Phase 10 扩展检索评测 | 146/146 通过，混合引擎，`top_k=5` |
| 主工程 manifest | `datasets/unified_bgg/manifest.json`，版本 `0.10.0-expanded-retrieval-eval` |

`manifest.json` 的状态字段仍记录为 Phase 10；规则书语料已经实际生成，对应产物见 `docs/rulebook_corpus_report.md`、`samples/rag/rulebook_text.jsonl` 和 `final/rulebook_index.sqlite`。

## 3. 能力组成

### 3.1 原始数据管理

保存 7 个来源数据集的原始文件、各自的 `DATASET.md` 字段说明、许可证备注和本地剖析结果。下载脚本支持幂等执行、单数据集下载和历史评论快照下载。

### 3.2 数据剖析与质量审计

`datasets/_scripts` 和 `unified_bgg/scripts` 可生成文件清单、CSV 字段/类型/空值/范围统计，检查 1,894 万条用户评分和 2,620 万条评论评分中的异常，并输出机器可读 JSON 和 Markdown 报告。

### 3.3 实体对齐与统一表

使用 BGG 官方游戏 ID 作为跨数据集实体锚点，内部 ID 统一为 `bgg:{bgg_id}`。生成游戏主表、带来源和时间快照的统计表、原始 taxonomy 关系表，以及完整的来源 lineage。

### 3.4 Taxonomy 规范化

维护不同年份机制、类别、主题、子域、家族和领域标签的 raw-to-canonical 映射。2025 词表优先作为机制/类别/家族的 canonical 参考；自动合并、保留和拆分决策记录在 `taxonomy_alias_overrides.csv`，所有变换可回溯。

### 3.5 RAG 数据产品

生成以下 JSONL 文档类型：

- `game_overview`：游戏名称、人数、时长、评分、复杂度、排名、分类、机制和描述；
- `mechanic_profile`：canonical 机制定义、代表游戏、共现标签与统计画像；
- `review_digest`：从超大评分/评论文件流式提取的每游戏评论主题和代表性片段；
- `rulebook_text`：规则书或规则摘要的可检索文本，带来源、页数和提取方式。

### 3.6 本地检索

支持单独的 FTS5/BM25 词法检索、纯 Python 稀疏 TF-IDF 向量检索，以及 Reciprocal Rank Fusion 混合检索。中文查询会经过可审计的查询扩展和高置信度游戏/机制实体路由，结果统一包含排名、分数、文档类型、游戏 ID、来源文件和引擎证据。

### 3.7 微调样本

`game_qa`、`mechanic_explanation`、`review_summary`、`recommendation_reasoning`、`extraction` 五类样本同时保留 `source_doc_ids`/`source_game_ids`，可先审计 preview，再使用 candidate 文件进行后续训练实验。

## 4. 顶层目录

```text
research/
├─ Readme.md                         本项目总览和使用入口（本文档）
├─ boardgame-datasets-survey.md      桌游数据集调研报告、选型结论和外部依赖说明
└─ datasets/
   ├─ README.md                      原始数据集仓库说明
   ├─ _scripts/                      下载、剖析、摘要和大文件检查工具
   ├─ _profiles/                     脚本产生的字段统计、事实检查和 Kaggle 元数据
   ├─ bgg-*/raw/                     7 个数据源的不可变原始文件
   └─ unified_bgg/                   统一数据库构建、RAG、微调和检索工程
```

## 5. 原始数据集目录说明

每个源目录都包含 `DATASET.md`（字段、规模、许可和陷阱）以及 `raw/` 原始文件。除特别说明外，原始文件不应直接覆盖修改。

| 目录 | 主要内容和用途 | 关键注意事项 |
| --- | --- | --- |
| `bgg-threnjen` | 2021/2022 快照；游戏属性、机制/主题矩阵、聚合评分、约 1,894 万条用户评分 | CC BY-SA 3.0；`Rank:*` 的 `21926` 是未排名哨兵值；用户名必须按字符串读取 |
| `bgg-reviews-jvanelteren` | 2025 最新游戏详情、约 2,620 万条评分/评论行、历史排名快照 | 只有约 16.09% 评分带评论；文件按游戏排序，不能用 `nrows` 代表全局分布；评论文本暂限本地研究 |
| `bgg-gabrio` | 2017 SQLite 快照，约 90,400 行，含 13,712 个扩展和原始描述/投票字段 | `game.id` 为 TEXT；`bayesaverage=0` 表示未知；基础游戏分析需过滤 `game.type='boardgame'` |
| `bgg-ranked-mattadamhouser` | 2023 Top-2000 游戏、机制/主题/子域和 reimplementation 关系 | 只覆盖头部游戏，不能估计全体分布；CC0 |
| `bgg-mrpantherson` | 2017-04、2018-01、2018-06 三个 Top-5000 评分/排名快照 | 前两个文件使用 cp1252，2018-06 使用 UTF-8；适合时间漂移对比；CC0 |
| `bgg-andrewmvd` | 2021 轻量结构化 CSV，包含评分、机制、类别和 domain | 使用 `;` 分隔符、`,` 小数点；CC BY 4.0，发布需署名 |
| `bgg-sujaykapadnis` | TidyTuesday 派生的游戏评分表 | 已确认是 `bgg-gabrio` 的严格子集，只保留 lineage，不作为独立证据重复加权 |

配套研究依据为 `boardgame-datasets-survey.md`；许可不明确的来源（尤其 `gabrio`、`sujaykapadnis`、`jvanelteren`）在发布或商用前必须重新核对来源页面。

## 6. `datasets/_scripts` 工具

| 文件 | 功能 |
| --- | --- |
| `download.ps1` | 从 Kaggle 匿名下载数据；支持 `-Only`、`-Force`、`-IncludeHistoricalReviews` |
| `fetch_kaggle_meta.ps1` | 拉取数据集作者、更新时间、许可和描述到 `_profiles/kaggle_meta.json` |
| `profile_csv.py` | 对 CSV 做列名、类型、空值、范围、样例和行数剖析 |
| `digest_wide.py` | 汇总宽表的标签数量和标签流行度 |
| `show_profile.py` | 将剖析 JSON 压缩为适合人工阅读的摘要 |
| `check_user_ratings.py` | 流式检查大用户评分表的评分范围、重复、缺失和用户字段 |
| `check_reviews.py` | 流式检查大评论/评分表的文本覆盖、长度和异常 |
| `*.log` | 下载和大文件检查的历史运行日志 |

## 7. `datasets/unified_bgg` 目录说明

### 7.1 核心控制文件

- `README.md`：主工程的阶段说明、目录布局和推荐流程。
- `manifest.json`：版本、阶段、来源数据集、生成产物和处理决策的机器可读登记表。
- `.codex/memory/`：面向后续 Agent 的项目恢复提示，不是业务数据。

### 7.2 `scripts/` 构建与查询脚本

| 脚本组 | 文件 | 作用 |
| --- | --- | --- |
| 盘点 | `profile_sources.py` | 扫描源文件并生成数据集清单/剖析报告 |
| 对齐 | `build_id_map.py` | 建立来源 ID、唯一 BGG ID、覆盖率和名称冲突报告；默认跳过超大评分文件 |
| 核心表 | `build_core_tables.py` | 生成 `games.csv`、`game_stats.csv`、`game_taxonomy.csv` |
| taxonomy | `build_taxonomy_aliases.py` | 生成别名表、自动决策覆盖表和 canonical taxonomy |
| RAG 样本 | `build_rag_samples.py` | 生成游戏概览与机制画像 JSONL 及 preview |
| 评论摘要 | `build_review_digest.py` | 分块流式扫描 26M 评论/评分文件，生成每游戏摘要 |
| 规则书 | `build_rulebook_samples.py` | 从 `1jour-1jeu.com` 选取高分游戏、下载/提取规则书并生成规则书语料与专用索引 |
| 质量 | `smoke_test_rag_retrieval.py`、`evaluate_rag_quality.py` | 检查召回可用性、重复文档、文本健康和来源一致性 |
| 微调 | `build_finetune_preview.py`、`evaluate_finetune_samples.py` | 生成并审计 preview/candidate 五类微调样本 |
| 索引 | `build_rag_index.py`、`build_vector_index.py` | 构建 FTS5 和稀疏 TF-IDF SQLite 索引 |
| 单引擎查询 | `query_rag_index.py`、`query_vector_index.py`、`query_hybrid_index.py` | 分别执行 FTS、vector、hybrid 检索 |
| 统一查询 | `unified_retrieval.py`、`query_unified_index.py` | 统一 `auto/fts/vector/hybrid` 入口和结果结构 |
| 评测导出 | `retrieval_suite.py`、`export_retrieval_suite.py`、`retrieval_suite_expanded.py`、`export_retrieval_suite_expanded.py` | 执行并导出基础/扩展查询套件 |
| 公共逻辑 | `retrieval_common.py` | UTF-8 输出、查询分词、实体路由和检索公共函数 |

### 7.3 `intermediate/` 统一中间表

| 文件 | 含义 |
| --- | --- |
| `id_map.csv` | 每个来源记录到 `bgg:{id}` 的映射和置信度 |
| `dataset_id_coverage.csv` | 各来源的 ID 覆盖率 |
| `games.csv` | 一行一个统一游戏实体，保留主名称、元数据和来源 lineage |
| `game_stats.csv` | 多来源、多时间点的评分、排名、投票数、复杂度和人数/时长统计 |
| `game_taxonomy.csv` | 原始机制、类别、主题、子域、家族、领域关系 |
| `taxonomy_aliases.csv` | raw 标签到 canonical 标签的映射、策略和置信度 |
| `taxonomy_alias_overrides.csv` | Phase 7 自动合并/拆分/保留决策的持久化覆盖表 |
| `game_taxonomy_canonical.csv` | 下游 RAG、分析和微调使用的规范化 taxonomy |

### 7.4 `samples/` 样本产品

- `samples/rag/`：`game_overview.jsonl`、`mechanic_profile.jsonl`、`review_digest.jsonl`、`rulebook_text.jsonl` 及对应 `.preview.jsonl`；另有 `through_the_ages_retrieval.md` 示例。
- `samples/finetune/`：五类任务的 `.preview.jsonl` 和 `.candidate.jsonl`。
- JSONL 每行是独立文档/样本，含文档 ID、游戏 ID、来源文件、处理版本和文本或 messages。

### 7.5 `final/` 本地索引

- `rag_index.sqlite`：SQLite FTS5/BM25 主 RAG 索引，默认由四类 RAG JSONL 构建。
- `rag_vector_index.sqlite`：纯 Python 稀疏 TF-IDF 倒排索引。
- `rulebook_index.sqlite`：规则书构建脚本产生的专用 FTS 索引；重建总索引时也可将规则书 JSONL 纳入 `rag_index.sqlite`。

### 7.6 `raw_index/` 机器可读审计结果

保存 `source_files.json`、ID/profile/coverage、核心表摘要、taxonomy 摘要、RAG 质量、向量索引、混合检索、查询套件、微调质量和规则书语料的 JSON/JSONL 结果。它们是判断构建是否成功的首选证据，不应手工编辑。

### 7.7 `docs/` 人工阅读报告

包括数据集清单、schema、来源优先级、已知问题、各阶段计划/总结、taxonomy 决策、RAG 与检索设计/评测、微调 schema/报告、规则书语料和案例分析，以及 Brass: Birmingham 等游戏报告。优先阅读：`database_overview.md`、`unified_schema.md`、`source_priority.md`、`known_issues.md`、`phase10_retrieval_eval_expansion.md`。

## 8. 数据模型和追溯原则

统一 schema 的目标表为 `games`、`game_stats`、`game_taxonomy`、`ratings`、`reviews`、`id_map` 和 `dataset_lineage`。当前默认生成的是前三张核心 CSV、ID/映射表和 RAG 摘要；完整行级 `ratings`/`reviews` 不默认物化，以避免反复处理超大文件。

必须遵守以下原则：

1. 只用官方 BGG ID 做实体对齐，不以游戏名称替代主键。
2. 评分、排名、复杂度、投票数等时间敏感字段必须同时保留 `snapshot_date` 和 `source_dataset`。
3. 跨年份机制不能按原始字符串直接 join，必须经过 `taxonomy_aliases`/canonical 表。
4. 每个派生事实都要能回到来源数据集、来源文件和处理版本。
5. 评论文本属于用户生成内容，当前保持本地研究用途。

## 9. 完整使用流程

以下命令均建议在 `D:\OpenViking\research\datasets\unified_bgg` 执行。Python 脚本主要使用标准库和本地 SQLite；规则书脚本还需要其源码中声明的 PDF/HTML 解析依赖。

### 步骤 0：检查环境

```powershell
Set-Location D:\OpenViking\research\datasets\unified_bgg
python --version
python scripts\query_unified_index.py --help
```

### 步骤 1：准备原始数据（已有数据可跳过）

```powershell
Set-Location D:\OpenViking\research\datasets
powershell -ExecutionPolicy Bypass -File _scripts\download.ps1

# 只下载指定数据集；-Only 支持逗号或空格分隔
powershell -ExecutionPolicy Bypass -File _scripts\download.ps1 -Only bgg-threnjen

# 需要时序评论对比时才下载额外历史快照
powershell -ExecutionPolicy Bypass -File _scripts\download.ps1 -IncludeHistoricalReviews

# 更新 Kaggle 许可/作者/更新时间元数据
powershell -ExecutionPolicy Bypass -File _scripts\fetch_kaggle_meta.ps1
```

脚本默认跳过已经存在的目标文件；只有确认需要覆盖时才使用 `-Force`。

### 步骤 2：盘点和剖析来源

```powershell
Set-Location D:\OpenViking\research\datasets\unified_bgg
python scripts\profile_sources.py

Set-Location D:\OpenViking\research\datasets
python _scripts\profile_csv.py
python _scripts\digest_wide.py --all
python _scripts\check_user_ratings.py
python _scripts\check_reviews.py
```

检查 `unified_bgg/raw_index/source_files.json`、`docs/dataset_inventory.md` 和 `_profiles/` 中的摘要。大文件检查可能需要数分钟。

### 步骤 3：建立实体对齐和核心表

```powershell
Set-Location D:\OpenViking\research\datasets\unified_bgg
python scripts\build_id_map.py
python scripts\build_core_tables.py
python scripts\build_taxonomy_aliases.py
```

如确实需要扫描 26M 评论/评分和 1,894 万用户评分的原始行，再显式执行：

```powershell
python scripts\build_id_map.py --include-large
```

确认 `intermediate/` 文件和 `raw_index/*_summary.json` 的行数、唯一 ID 和 `needs_review` 指标。

### 步骤 4：生成 RAG 样本

```powershell
python scripts\build_rag_samples.py
python scripts\build_review_digest.py
```

开发调试时可限制规模：

```powershell
python scripts\build_rag_samples.py --preview-only --preview-size 50
python scripts\build_review_digest.py --max-rows 100000 --preview-size 50
```

### 步骤 5：质量检查并构建索引

```powershell
python scripts\smoke_test_rag_retrieval.py
python scripts\evaluate_rag_quality.py
python scripts\build_rag_index.py
python scripts\build_vector_index.py
```

质量审计应关注重复文档 ID、空文本、异常问号串、编码替换字符和来源字段缺失。只有审计通过后才将索引用于评测或下游 Agent。

### 步骤 6：可选地加入规则书语料

该步骤需要网络访问，并从 `1jour-1jeu.com` 获取规则书或规则摘要：

```powershell
python scripts\build_rulebook_samples.py --limit 100 --preview-size 20
python scripts\build_rag_index.py
python scripts\build_vector_index.py
```

输出包括 `samples/rag/rulebook_text*.jsonl`、`raw_index/rulebook_corpus_*.json*`、`docs/rulebook_corpus_report.md` 和 `final/rulebook_index.sqlite`。报告会区分 PDF 文本提取、fallback 摘要和缺失来源。

### 步骤 7：生成和审计微调样本

```powershell
# 每类 50 条预览样本
python scripts\build_finetune_preview.py --kind preview
python scripts\evaluate_finetune_samples.py --kind preview

# 每类最多 1000 条候选样本（机制解释按现有机制数生成）
python scripts\build_finetune_preview.py --kind candidate
python scripts\evaluate_finetune_samples.py --kind candidate
```

审计结果分别写入 `raw_index/finetune_*_summary.json` 和 `docs/finetune_*_report.md`。没有通过来源 ID、结构和文本健康检查的样本不得进入训练集。

### 步骤 8：查询本地数据库

统一入口默认使用混合检索并返回 Markdown：

```powershell
python scripts\query_unified_index.py "Through the Ages civilization" --doc-type game_overview
python scripts\query_unified_index.py "Brass Birmingham loans network" --engine hybrid --limit 5
python scripts\query_unified_index.py "卡坦岛 交易 资源" --doc-type game_overview --markdown
python scripts\query_unified_index.py "Gloomhaven rules" --doc-type rulebook_text --json
```

可选引擎为 `fts`、`vector`、`hybrid` 和 `auto`；还可用 `--game-id bgg:224517` 或 `--bgg-id 224517` 做实体过滤。底层单引擎命令分别是 `query_rag_index.py`、`query_vector_index.py` 和 `query_hybrid_index.py`。

结果字段包括 `rank`、`score`、`doc_id`、`doc_type`、`title`、`game_id`、`bgg_id`、`source_file`、`text_preview` 以及 FTS/vector/fusion 证据字段。

### 步骤 9：运行检索评测和导出召回集

```powershell
python scripts\evaluate_hybrid_retrieval.py --top-k 5 --candidate-limit 50
python scripts\export_retrieval_suite.py --engine hybrid --limit 5 --candidate-limit 50
python scripts\export_retrieval_suite_expanded.py --engine hybrid --limit 5 --candidate-limit 50
```

评测结果位于 `raw_index/retrieval_suite*.jsonl`、`raw_index/*_summary.json` 和 `docs/retrieval_suite*_report.md`。当前扩展套件为 146 条查询，已全部通过。

## 10. 复现、排错和维护

- 先运行 `profile_sources.py`，再按“ID 对齐 -> 核心表 -> taxonomy -> RAG -> 质量 -> 索引”的顺序重建；不要跳过来源盘点。
- 修改清洗规则或 taxonomy 映射后，应重新生成受影响的 JSONL、质量审计和两个索引，并同步更新 `manifest.json`。
- 26M 评论文件按游戏排序，不能通过读取前若干行估算整体评论分布；使用 `build_review_digest.py` 的分块扫描。
- Windows PowerShell 5.1 写中文 Markdown 时优先使用 UTF-8 编辑方式；完成后用 UTF-8 读取检查连续问号乱码和 Unicode 替换字符。
- `bgg-andrewmvd` 使用 `sep=';'`、小数逗号；`bgg-mrpantherson` 按文件设置编码；`bgg-gabrio` 的 ID 和列名需要显式转换/引用。
- 如果只更新了 RAG JSONL，必须重新运行 `build_rag_index.py` 和 `build_vector_index.py`，否则查询仍使用旧索引。
- 网络不可用时可以继续使用已有原始文件和本地索引；只有下载数据、抓取规则书或刷新 Kaggle 元数据需要网络。

## 11. 关键文档导航

| 需求 | 首选文档 |
| --- | --- |
| 了解数据集选型和外部 API 限制 | `boardgame-datasets-survey.md` |
| 了解原始数据集字段/许可 | `datasets/README.md`、各数据集 `DATASET.md` |
| 了解数据库产品和限制 | `datasets/unified_bgg/docs/database_overview.md` |
| 了解统一 schema | `datasets/unified_bgg/docs/unified_schema.md` |
| 了解来源优先级和已知陷阱 | `datasets/unified_bgg/docs/source_priority.md`、`known_issues.md` |
| 了解阶段进展和构建产物 | `datasets/unified_bgg/manifest.json`、`docs/work_summary_2026-08-25.md` |
| 了解检索接口和评测 | `docs/phase9_retrieval_interface.md`、`docs/phase10_retrieval_eval_expansion.md`、`docs/retrieval_suite_expanded_report.md` |
| 了解规则书扩展 | `docs/rulebook_corpus_report.md`、`docs/rulebook_retrieval_analysis.md` |
| 了解微调样本 | `docs/finetune_sample_schema.md`、`docs/finetune_candidate_report.md` |
| 查看具体游戏报告 | `docs/top100_reports/`、`docs/top10_reports_v4/`、`docs/party_top10/`、`docs/two_player_top10/` |

## 12. 最小恢复命令

已有中间表和样本时，直接从索引/查询继续：

```powershell
Set-Location D:\OpenViking\research\datasets\unified_bgg
python scripts\build_rag_index.py
python scripts\build_vector_index.py
python scripts\query_unified_index.py "Brass Birmingham" --engine hybrid --limit 5
```

需要从原始数据完整重建时：

```powershell
python scripts\profile_sources.py
python scripts\build_id_map.py
python scripts\build_core_tables.py
python scripts\build_taxonomy_aliases.py
python scripts\build_rag_samples.py
python scripts\build_review_digest.py
python scripts\evaluate_rag_quality.py
python scripts\build_rag_index.py
python scripts\build_vector_index.py
```

所有生成文件都应以 `manifest.json`、`raw_index/` 摘要和 `docs/` 审计报告为准；原始数据、评论文本和规则书的再分发必须另行进行许可与版权审查。
