# unified_bgg Phase 7 工作规划

生成日期：2026-08-26  
项目目录：`D:\OpenViking\research\datasets\unified_bgg`  
当前基线版本：`0.6.1-rag-text-health-cleanup`  
当前基线状态：`phase_6_1_rag_text_health_cleaned_and_index_rebuilt`

## 1. 阶段目标

Phase 7 的目标是把已经完成的结构化数据与 RAG 文档，推进到“可用于模型微调与更高质量召回”的下一层数据产品。

本阶段不再重复做源数据盘点、实体对齐、RAG JSONL 生成或 SQLite FTS 索引重建；这些工作已经在 Phase 1-6.1 完成。Phase 7 的重点是：

1. 建立 taxonomy 人工复核闭环，减少高影响机制/分类标签的语义噪声。
2. 设计并生成小规模 finetune preview 样本，验证数据能否稳定支持桌游问答、机制解释、评论总结和推荐理由生成。
3. 定义后续全量 finetune 样本的 schema、质量门槛和生成脚本接口。
4. 为向量检索与最终结构化发布格式预留接口，但不在本阶段强行全量实现。

## 2. 当前可依赖基线

### 2.1 已完成数据层

| 数据层 | 关键文件 | 当前规模 |
| --- | --- | ---: |
| 实体对齐 | `intermediate/id_map.csv` | 345,282 行 |
| 游戏主表 | `intermediate/games.csv` | 100,274 行 |
| 统计快照 | `intermediate/game_stats.csv` | 291,640 行 |
| 原始 taxonomy | `intermediate/game_taxonomy.csv` | 1,164,739 行 |
| taxonomy alias | `intermediate/taxonomy_aliases.csv` | 15,149 行 |
| canonical taxonomy | `intermediate/game_taxonomy_canonical.csv` | 1,160,887 行 |

### 2.2 已完成 RAG 层

| RAG 文件 | doc_type | 文档数 |
| --- | --- | ---: |
| `samples/rag/game_overview.jsonl` | `game_overview` | 100,274 |
| `samples/rag/mechanic_profile.jsonl` | `mechanic_profile` | 192 |
| `samples/rag/review_digest.jsonl` | `review_digest` | 27,851 |

当前 RAG 文档总数：128,317。  
当前质量审计结果：0 个重复 `doc_id`，0 个 text health flags。  
当前本地检索索引：`final/rag_index.sqlite`，SQLite FTS5，约 1.11GB。

## 3. Phase 7 工作拆分

### 7.1 taxonomy 人工复核候选集

目标：先不直接修改 canonical 表，而是生成一个可审阅、可追踪、可回放的候选复核表。

建议新增文件：

- `scripts/build_taxonomy_review_candidates.py`
- `intermediate/taxonomy_review_candidates.csv`
- `docs/taxonomy_manual_review_plan.md`

输入：

- `intermediate/taxonomy_aliases.csv`
- `intermediate/game_taxonomy_canonical.csv`
- `raw_index/taxonomy_profile.json`

候选优先级：

1. `taxonomy_type=mechanic`
2. `needs_review=true`
3. `mapping_strategy` 属于：
   - `unmapped_raw_fallback`
   - `ambiguous_legacy_label`
4. `row_count` 高、来源数量多、影响游戏多的标签优先。

已知高优先级样例：

| raw label | 当前状态 | 处理建议 |
| --- | --- | --- |
| `Card Drafting` | unmapped fallback | 复核是否映射到 `Drafting` 或保留历史含义 |
| `Drafting` | unmapped fallback | 与 `Card Drafting` 联合复核 |
| `Action / Movement Programming` | ambiguous legacy label | 可能需要拆分到 `Action Queue` / `Programmed Movement` |
| `Dexterity` | unmapped fallback | 复核 2025 词表对应关系 |
| `Physical` | unmapped fallback | 复核是否为旧版混合标签 |
| `Time Track` | unmapped fallback | 复核是否已有 2025 canonical 对应 |
| `TableauBuilding` | unmapped fallback | 可能是 `Tableau Building` 格式问题 |
| `Multiple-Lot Auction` | unmapped fallback | 复核是否映射到拍卖子机制 |

验收标准：

- 生成候选表，包含 raw label、canonical label、taxonomy type、strategy、row_count、source_count、sources、review priority、suggested action。
- 不直接覆盖 `taxonomy_aliases.csv`。
- 文档说明人工复核流程与 override 文件格式。

### 7.2 taxonomy override 机制设计

目标：让人工复核结果可以稳定回放，而不是手改生成产物。

建议新增文件：

- `intermediate/taxonomy_alias_overrides.csv`
- 更新 `scripts/build_taxonomy_aliases.py`
- 更新 `docs/taxonomy_profile_report.md` 或新增 `docs/taxonomy_override_report.md`

建议 override schema：

| 字段 | 说明 |
| --- | --- |
| `taxonomy_type` | mechanic/category/family/domain/theme/subcategory |
| `raw_name` | 原始标签 |
| `raw_snapshot` | 可选，指定年份/快照 |
| `source_dataset` | 可选，指定来源 |
| `override_canonical_name` | 人工决定的 canonical 标签 |
| `override_strategy` | 例如 `manual_review_alias` / `manual_review_keep` / `manual_review_split_needed` |
| `override_confidence` | high/medium/low |
| `notes` | 人工说明 |

验收标准：

- 没有 override 文件时，现有构建结果不变。
- 有 override 文件时，构建脚本优先应用 override。
- 输出报告能统计 override 应用数量、未命中数量和仍需复核数量。

### 7.3 finetune preview 样本 schema 设计

目标：先设计样本格式，再生成小规模 preview，避免全量生成后返工。

建议新增目录：

- `samples/finetune/`

建议新增文件：

- `docs/finetune_sample_schema.md`
- `samples/finetune/game_qa.preview.jsonl`
- `samples/finetune/mechanic_explanation.preview.jsonl`
- `samples/finetune/review_summary.preview.jsonl`
- `samples/finetune/recommendation_reasoning.preview.jsonl`
- `samples/finetune/extraction.preview.jsonl`

通用样本字段：

| 字段 | 说明 |
| --- | --- |
| `sample_id` | 稳定唯一 ID |
| `task_type` | 样本任务类型 |
| `input` | 用户问题或模型输入 |
| `output` | 期望回答 |
| `source_doc_ids` | 来自哪些 RAG 文档 |
| `source_game_ids` | 涉及哪些游戏 |
| `snapshot_date` | 评分/排名等快照日期 |
| `quality_flags` | 样本质量标记 |
| `metadata` | 生成版本、脚本、来源等 |

第一批 preview 任务：

1. `game_qa`：回答单款游戏的基础信息、人数、时长、复杂度、评分、分类。
2. `mechanic_explanation`：解释某个机制，并列出代表游戏和常见共现机制。
3. `review_summary`：把 `review_digest` 转成正面/中性/负面主题总结。
4. `recommendation_reasoning`：基于机制、复杂度、评分和评论主题生成推荐/不推荐理由。
5. `extraction`：把自然语言游戏介绍抽取为结构化字段。

验收标准：

- 每类任务先生成 20-100 条 preview。
- 所有样本必须保留 `source_doc_ids`。
- 对包含评分/排名的回答必须带快照日期。
- 对评论类样本不得长篇复制用户评论原文。
- 至少提供一个脚本级 smoke test，验证 JSONL 可解析、字段完整、ID 不重复。

### 7.4 finetune preview 生成脚本

建议新增脚本：

- `scripts/build_finetune_preview.py`
- `scripts/evaluate_finetune_samples.py`

输入：

- `samples/rag/game_overview.jsonl`
- `samples/rag/mechanic_profile.jsonl`
- `samples/rag/review_digest.jsonl`

输出：

- `samples/finetune/*.preview.jsonl`
- `raw_index/finetune_sample_summary.json`
- `docs/finetune_preview_report.md`

生成策略：

- 优先选高质量样本：
  - 有标题
  - 有可靠机制
  - 有评分/复杂度
  - 评论覆盖率不极低
  - 不是扩展，或明确标记为 expansion
- 样本语言先以中文为主，因为当前使用场景主要是中文交互。
- 保留英文机制名，中文解释可由模板生成。
- 不在 preview 阶段做大模型改写，先用确定性模板保证可审计。

验收标准：

- JSONL 全部可解析。
- `sample_id` 唯一。
- 每条样本至少引用 1 个 `source_doc_id`。
- 生成报告包含任务类型分布、样本数量、质量 flags、示例样本。

### 7.5 检索增强预研

目标：只做设计，不在本阶段强制构建向量库。

建议新增文档：

- `docs/vector_retrieval_design.md`

设计要点：

- 当前 `rag_index.sqlite` 是 SQLite FTS5/BM25，适合词法检索。
- 下一步可加入 embedding 向量索引，形成 hybrid retrieval：
  1. BGG ID 精确过滤
  2. FTS BM25 候选召回
  3. 向量召回候选
  4. rerank
  5. 按 doc_type 合并上下文
- 向量化对象优先级：
  1. `game_overview.text`
  2. `mechanic_profile.text`
  3. `review_digest.text`

验收标准：

- 明确 embedding 输入字段、chunk 策略、索引格式和评估 query set。
- 不强行依赖外部 API；可支持后续本地或远程 embedding。

## 4. 推荐执行顺序

建议按以下顺序推进：

1. 生成 `taxonomy_review_candidates.csv`，先看复核面有多大。
2. 编写 `finetune_sample_schema.md`，冻结 preview 样本字段。
3. 实现 `build_finetune_preview.py`，每类任务生成 20-100 条。
4. 实现 `evaluate_finetune_samples.py`，验证 JSONL 与样本字段。
5. 生成 `finetune_preview_report.md`，让用户审查文本质量。
6. 再决定是否进入全量 finetune 样本生成或向量检索实验。

## 5. 最小执行闭环

如果只做最小 Phase 7 闭环，建议限定为：

```powershell
cd D:\OpenViking\research\datasets\unified_bgg
python scripts\build_taxonomy_review_candidates.py
python scripts\build_finetune_preview.py --preview-size 50
python scripts\evaluate_finetune_samples.py
```

最小闭环产物：

- `intermediate/taxonomy_review_candidates.csv`
- `docs/taxonomy_manual_review_plan.md`
- `docs/finetune_sample_schema.md`
- `samples/finetune/game_qa.preview.jsonl`
- `samples/finetune/mechanic_explanation.preview.jsonl`
- `samples/finetune/review_summary.preview.jsonl`
- `samples/finetune/recommendation_reasoning.preview.jsonl`
- `samples/finetune/extraction.preview.jsonl`
- `raw_index/finetune_sample_summary.json`
- `docs/finetune_preview_report.md`

## 6. 风险与约束

- `review_digest` 包含 BGG 用户生成文本，preview 可本地使用，但发布/商用前仍需 legal/release review。
- taxonomy 的 `unmapped_raw_fallback` 不一定都是错误，有些可能是旧词表中真实存在而 2025 词表未覆盖的标签。
- finetune 样本如果过早引入大模型改写，会降低可审计性；建议第一版用确定性模板。
- 当前 RAG 索引是词法检索，不应把它描述为语义检索或向量库。
- Windows PowerShell 5.1 写中文 Markdown 可能产生编码问题，所有中文文档需 UTF-8 回读验证。

## 7. Phase 7 完成标准

Phase 7 可以在满足以下条件后标记完成：

1. taxonomy 复核候选集已生成，并有清晰人工 override 流程。
2. finetune 样本 schema 已文档化。
3. 至少 5 类 finetune preview JSONL 已生成。
4. finetune preview 通过结构审计：可解析、ID 唯一、字段完整、来源可追踪。
5. 已生成 `docs/finetune_preview_report.md`，并经过人工检查文本质量。
6. `manifest.json` 更新到 Phase 7 状态，并记录新增脚本、文档和样本。

## 8. 建议的下一步实际动作

下一步建议直接执行 Phase 7.1：

1. 新建 `scripts/build_taxonomy_review_candidates.py`。
2. 从 `raw_index/taxonomy_profile.json` 中读取 `top_unmapped_mechanics`。
3. 结合 `intermediate/taxonomy_aliases.csv` 和 `game_taxonomy_canonical.csv` 生成复核候选表。
4. 输出 `docs/taxonomy_manual_review_plan.md`。
5. 暂不修改 canonical 结果，等待复核策略确认后再加入 override。
