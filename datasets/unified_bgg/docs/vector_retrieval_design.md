# unified_bgg Phase 8 检索增强设计

生成日期：2026-08-26  
项目目录：`D:\OpenViking\research\datasets\unified_bgg`  
当前基线：`0.7.2-finetune-candidates`

## 1. 目标

Phase 8 的目标是在现有 SQLite FTS5 词法检索之外，增加一个本地、可复现、无外部 API 依赖的检索增强实验层。

本阶段不调用远程 embedding API，也不安装额外依赖。当前实现采用纯 Python + SQLite 的稀疏 TF-IDF 向量倒排索引，并与现有 FTS5 结果做 hybrid fusion。

## 2. 为什么需要 Phase 8

现有 `final/rag_index.sqlite` 是 SQLite FTS5/BM25 索引，优势是：

- 构建快；
- 查询快；
- 结构简单；
- 精确英文关键词效果好。

限制是：

- 中文自然语言问题对英文 BGG 文档召回较弱；
- 同义词、译名、机制别称需要额外处理；
- 不能表达真正语义相似度。

Phase 8 先解决“更稳的候选召回”和“中文查询扩展”问题，为未来神经 embedding / rerank 做准备。

## 3. 当前实现范围

新增本地 TF-IDF 向量索引：

- 输入：`samples/rag/game_overview.jsonl`、`samples/rag/mechanic_profile.jsonl`、`samples/rag/review_digest.jsonl`
- 输出：`final/rag_vector_index.sqlite`
- 查询：`scripts/query_vector_index.py`
- 混合查询：`scripts/query_hybrid_index.py`
- 评估：`scripts/evaluate_hybrid_retrieval.py`

### 3.1 向量索引口径

当前向量不是神经 embedding，而是 TF-IDF sparse vector：

1. 对每个 RAG 文档的 `title`、`doc_type`、`text` 分词。
2. 统计文档频率，计算 IDF。
3. 为每个文档保留权重最高的若干 term。
4. 将归一化后的稀疏权重写入 SQLite 倒排表。
5. 查询时把 query 转成同口径 TF-IDF 向量，做 cosine-like dot product。

### 3.2 中文查询扩展

为了让中文问题能召回英文 BGG 文档，Phase 8 在查询层加入轻量中文扩展词典，例如：

- `卡坦岛` -> `CATAN Catan trading negotiation`
- `幽港迷城` -> `Gloomhaven cooperative campaign fantasy`
- `卡卡颂` -> `Carcassonne tile placement`
- `交易` -> `trading negotiation`
- `掷骰` -> `dice rolling`
- `牌库构筑` -> `deck bag pool building deck building`
- `工人放置` -> `worker placement`
- `评论` -> `review comments digest`

这不是翻译模型，而是项目内可审计的 query expansion 规则。

## 4. Hybrid Retrieval

混合检索流程：

1. 对原始 query 做中文扩展。
2. 用现有 FTS5/BM25 召回候选。
3. 用本地 TF-IDF 向量倒排索引召回候选。
4. 用 reciprocal rank fusion 合并结果。
5. 输出每条结果的 FTS rank、vector rank、vector score 和 fusion score。

优先使用过滤条件：

- `--doc-type`
- `--bgg-id`
- `--game-id`

如果用户明确查某个游戏，仍然优先用 BGG ID 过滤，避免扩展/变体污染。

## 5. 评估集

Phase 8 评估包含英文查询和中文自然语言查询，覆盖：

- 单游戏简介；
- 单游戏评论；
- 机制画像；
- 中文译名；
- 中文机制词；
- 混合机制问题。

核心目标不是证明 TF-IDF 等同于 embedding，而是验证：

1. 中文扩展后能召回正确实体；
2. hybrid 至少不弱于原始 FTS；
3. 结果能保留可解释的检索证据。

## 6. 后续可升级方向

如果后续需要真正语义检索，可在当前 Phase 8 基础上替换或并联：

- 本地 embedding 模型；
- 远程 embedding API；
- 向量数据库；
- cross-encoder reranker；
- 中文标题/别名表；
- 基于 BGG ID 的实体路由器。

建议升级顺序：

1. 先扩大中文别名和机制词典。
2. 再加入真正 embedding。
3. 最后做 rerank 与上下文组装策略。

## 7. 成功标准

Phase 8 视为完成需要满足：

- `final/rag_vector_index.sqlite` 构建完成；
- vector 查询脚本能返回结果；
- hybrid 查询脚本能融合 FTS 与 vector；
- 中英文评估 query 全部通过或明确记录失败原因；
- 报告写入 `docs/hybrid_retrieval_report.md`；
- `manifest.json` 更新到 Phase 8 状态。
