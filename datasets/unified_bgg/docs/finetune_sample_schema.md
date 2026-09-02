# unified_bgg Finetune 样本 Schema

生成日期：2026-08-26  
适用阶段：Phase 7 finetune preview / candidate  
上游数据：`samples/rag/game_overview.jsonl`、`samples/rag/mechanic_profile.jsonl`、`samples/rag/review_digest.jsonl`

## 1. 设计目标

finetune preview 的目标不是直接产出最终训练集，而是先验证 `unified_bgg` 数据能否稳定支持桌游方向的微调任务。第一版 preview 采用确定性模板生成，方便审计、复现和回溯来源。

用户已认可 50 条/类的 preview 文本质量。Phase 7.2 在此基础上生成 candidate 样本：默认 1000 条/类，总计 5000 条，仍然使用确定性模板，并保留独立的 candidate 文件、摘要和质量报告。

本阶段优先支持中文问答场景，同时保留英文游戏名、机制名和 BGG ID，避免翻译损失实体精度。

## 2. 通用 JSONL 结构

每一行是一个 JSON 对象，必须包含以下字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `sample_id` | string | 稳定唯一 ID |
| `schema_version` | string | 样本 schema 版本 |
| `task_type` | string | 样本任务类型 |
| `language` | string | 当前固定为 `zh` |
| `input` | string | 用户问题或模型输入 |
| `output` | string | 期望模型输出 |
| `source_doc_ids` | array[string] | 样本引用的 RAG 文档 ID |
| `source_game_ids` | array[string] | 样本涉及的游戏 ID，例如 `bgg:13` |
| `snapshot_date` | string/null | 评分、排名、复杂度等快照日期 |
| `quality_flags` | array[string] | 样本级质量标记 |
| `metadata` | object | 生成脚本、时间、源文件等信息 |

通用约束：

- `sample_id` 在全部 preview 文件中必须唯一。
- `source_doc_ids` 必须非空，且应能在 RAG JSONL 中找到。
- 如果 `output` 包含评分、排名、复杂度或评分人数，必须说明快照日期。
- 评论类样本不能长篇复制 BGG 用户评论原文，只能做主题总结。
- 生成样本应保留 `quality_flags`，不要把数据缺口伪装成确定事实。

## 3. 任务类型

### 3.1 `game_qa`

用途：训练模型回答单款桌游的基础事实问题。

输入示例：

```text
请介绍桌游《CATAN》的基础信息，包括人数、时长、复杂度、评分和核心机制。
```

输出应包含：

- 游戏名、年份、BGG ID
- 人数、时长、年龄
- 评分、排名、复杂度与快照日期
- 核心机制和分类
- 简短说明

来源：`game_overview`。

### 3.2 `mechanic_explanation`

用途：训练模型解释桌游机制，并给出代表游戏与共现机制。

输入示例：

```text
请解释桌游机制 Dice Rolling，并说明它常和哪些机制一起出现。
```

输出应包含：

- 机制名
- 在 unified_bgg 中覆盖的游戏数量
- 代表游戏
- 常见共现机制
- 常见分类或领域

来源：`mechanic_profile`。

### 3.3 `review_summary`

用途：训练模型把玩家评论摘要转成正面、混合、负面主题总结。

输入示例：

```text
请总结 BGG 玩家对《CATAN》的主要好评、争议和批评点。
```

输出应包含：

- 评分记录数
- 非空评论数
- 评论覆盖率
- 正面主题
- 混合/争议主题
- 负面主题

来源：`review_digest`，可联合 `game_overview`。

### 3.4 `recommendation_reasoning`

用途：训练模型基于机制、复杂度、评分和评论主题生成推荐理由。

输入示例：

```text
我喜欢交易、谈判和中等复杂度桌游，是否适合尝试《CATAN》？
```

输出应包含：

- 是否推荐或谨慎推荐
- 推荐理由
- 可能风险
- 适合/不适合玩家
- 数据快照说明

来源：`game_overview` + `review_digest`。

### 3.5 `extraction`

用途：训练模型把自然语言桌游介绍抽取为结构化字段。

输入示例：

```text
从下面介绍中抽取桌游结构化信息：...
```

输出应为 JSON 字符串，至少包含：

- `title`
- `bgg_id`
- `year_published`
- `players`
- `playtime`
- `min_age`
- `mechanics`
- `categories`
- `rating_snapshot`

来源：`game_overview`。

## 4. 质量标记

常见 `quality_flags`：

| flag | 含义 |
| --- | --- |
| `source_game_needs_review` | 上游游戏实体仍需复核 |
| `source_missing_rating_values` | 上游缺少评分值 |
| `source_missing_reliable_mechanics` | 上游缺少可靠机制 |
| `source_expansion_doc` | 样本来自扩展而非基础游戏 |
| `low_comment_coverage` | 评论覆盖率较低 |
| `missing_review_bucket` | 评论摘要缺少正面/混合/负面某类片段 |
| `template_generated` | 由确定性模板生成，未经过人工润色 |

## 5. 文件命名

Preview 输出位于 `samples/finetune/`：

- `game_qa.preview.jsonl`
- `mechanic_explanation.preview.jsonl`
- `review_summary.preview.jsonl`
- `recommendation_reasoning.preview.jsonl`
- `extraction.preview.jsonl`

Candidate 输出同样位于 `samples/finetune/`：

- `game_qa.candidate.jsonl`
- `mechanic_explanation.candidate.jsonl`
- `review_summary.candidate.jsonl`
- `recommendation_reasoning.candidate.jsonl`
- `extraction.candidate.jsonl`

构建与审计摘要：

- `raw_index/finetune_sample_summary.json`
- `raw_index/finetune_quality_summary.json`
- `docs/finetune_preview_report.md`
- `raw_index/finetune_candidate_summary.json`
- `raw_index/finetune_candidate_quality_summary.json`
- `raw_index/finetune_candidate_quality_findings.jsonl`
- `docs/finetune_candidate_report.md`

## 6. 当前阶段边界

- Phase 7 生成 preview 与 candidate，不生成最终全量训练集。
- 第一版样本使用模板生成，不调用大模型改写。
- 不发布 `review_digest` 原文片段；评论类输出只保留主题总结和统计信息。
- 后续全量生成前，需要先由用户检查 candidate 文本质量、任务结构和规模策略。
