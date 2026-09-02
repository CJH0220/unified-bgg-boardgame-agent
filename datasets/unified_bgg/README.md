# unified_bgg 数据产品

`unified_bgg` 是本仓库的统一桌游数据接口目录。普通使用者从 Hugging Face 下载预构建索引后即可查询，不需要处理原始 BGG 文件或运行数据构建流水线。

## 快速开始

从仓库根目录执行：

```powershell
python -m pip install -r requirements.txt
python datasets\unified_bgg\scripts\download_public_data.py --kind query
python datasets\unified_bgg\scripts\query_unified_index.py "Brass Birmingham loans" --engine hybrid --limit 5
```

只查询规则书时可下载专用索引：

```powershell
python datasets\unified_bgg\scripts\download_public_data.py --kind rulebook
```

完整下载说明见仓库根目录的 [`HUGGINGFACE_DATA_GUIDE.md`](../../HUGGINGFACE_DATA_GUIDE.md)，面向 Agent 的查询规范见 [`skills/unified-bgg-rag-retrieval/SKILL.md`](../../skills/unified-bgg-rag-retrieval/SKILL.md)。

## 统一数据产品

- `final/rag_index.sqlite`：FTS5/BM25 主索引，覆盖游戏概览、机制、评论和规则书文档。
- `final/rag_vector_index.sqlite`：稀疏 TF-IDF 索引，用于混合召回。
- `final/rulebook_index.sqlite`：规则书专用索引。
- `samples/`：仓库内保留的小型预览样本；完整 JSONL 语料在 Hugging Face 的 `derived/samples/rag/`。
- `intermediate/`：统一游戏、统计和 taxonomy 表；完整大文件在 Hugging Face 的 `derived/intermediate/`。
- `scripts/query_unified_index.py`：统一查询入口，支持 `auto`、`fts`、`vector` 和 `hybrid`。

统一实体键为 `bgg:{bgg_id}`。结果应保留 BGG ID、来源文件、`snapshot_date` 和 `source_dataset`，以便追溯评分、排名和其他时间敏感字段。

## 维护者区域

原始数据同步、表构建、RAG 生成、质量审计和索引重建脚本仍位于 `scripts/`，但不属于普通用户流程。发布前请参考脚本内帮助和 Git 历史，并重新核对各来源许可；不要将原始数据、完整语料或访问令牌提交到 GitHub。
