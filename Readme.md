# Unified BGG Boardgame Agent Dataset

面向桌游设计平台的 BoardGameGeek 统一数据集与本地召回 Skill。项目已经预先完成数据对齐、taxonomy 规范化、RAG 文档生成和本地索引构建；使用者无需从原始文件开始处理，下载现成索引即可查询。

## 你可以用它做什么

- 查询桌游基础信息：人数、时长、年龄、评分、排名、复杂度和发行年份。
- 按机制、类别、主题或玩家人数查找相似桌游。
- 召回游戏概览、机制画像、玩家评论摘要和规则书文本。
- 为桌游设计提供机制组合、竞品比较、体验分析和设计启发。
- 输出带 BGG ID、数据快照和来源文件的 Markdown 或 JSON 结果。
- 在 Codex 等 Agent 中安装 `unified-bgg-rag-retrieval` Skill，让 Agent 直接调用本地数据。

## 数据集入口

完整大文件和预构建索引存放在 Hugging Face：

**https://huggingface.co/datasets/ChenJinHua/BGG_datasets_Agent**

| 产品 | 内容 | 适合谁 |
| --- | --- | --- |
| `indexes/final/rag_index.sqlite` | FTS5/BM25 统一检索索引 | 所有使用者，默认入口 |
| `indexes/final/rag_vector_index.sqlite` | 稀疏 TF-IDF 向量索引 | 需要混合检索的使用者 |
| `indexes/final/rulebook_index.sqlite` | 规则书专用索引 | 规则和行动流程分析 |
| `derived/samples/rag/` | 完整游戏、机制、评论 RAG JSONL | RAG/嵌入/研究开发 |
| `raw/` | 7 个原始 BGG 数据集 | 数据工程和统计分析 |
| `derived/intermediate/` | 统一游戏、统计和 taxonomy 表 | 需要结构化数据的研究者 |

大文件的远程路径、直链、下载方式、SHA256 校验和许可限制见 [`HUGGINGFACE_DATA_GUIDE.md`](HUGGINGFACE_DATA_GUIDE.md)。

## 小白使用流程

### 1. 准备环境

需要 Python 3.10 或更高版本。查询索引只依赖 Python 标准库；下载 Hugging Face 文件需要 `huggingface_hub`。

```powershell
git clone https://github.com/CJH0220/unified-bgg-boardgame-agent.git
Set-Location unified-bgg-boardgame-agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. 下载现成索引

默认下载 FTS 和 vector 两个索引（约 1.6 GB，需要足够磁盘空间）：

```powershell
python datasets\unified_bgg\scripts\download_public_data.py --kind query
```

只需要规则书查询时：

```powershell
python datasets\unified_bgg\scripts\download_public_data.py --kind rulebook
```

下载完成后，索引位于 `datasets/unified_bgg/final/`，无需额外转换。

### 3. 直接查询

```powershell
Set-Location datasets\unified_bgg
python scripts\query_unified_index.py "Brass Birmingham loans network" --engine hybrid --limit 5
python scripts\query_unified_index.py "卡坦岛 交易 资源" --doc-type game_overview --limit 5 --markdown
python scripts\query_unified_index.py "Gloomhaven rules" --doc-type rulebook_text --bgg-id 174430 --json
```

结果会显示标题、文档类型、BGG ID、来源文件、排名和召回分数。`--engine` 可选 `auto`、`fts`、`vector`、`hybrid`。

### 4. 让 Agent 使用 Skill

将仓库中的 `skills/unified-bgg-rag-retrieval` 复制到 Codex Skill 目录：

```powershell
Copy-Item -Recurse -Force `
  skills\unified-bgg-rag-retrieval `
  "$env:USERPROFILE\.codex\skills\unified-bgg-rag-retrieval"
```

重新打开 Agent 后，可以直接提出以下请求：

```text
使用 unified-bgg-rag-retrieval，介绍 Brass: Birmingham 的核心行动链、贷款门槛和玩家评价。
使用 unified-bgg-rag-retrieval，找出适合 2 人、带工人放置和网络构筑的桌游，并说明相似点。
使用 unified-bgg-rag-retrieval，比较 Gloomhaven、Spirit Island 和 Pandemic Legacy 的合作机制。
使用 unified-bgg-rag-retrieval，为一个“资源交易 + 路网扩张”的新桌游寻找竞品和设计启发。
```

Skill 会优先查询本地索引；如果索引缺失，参照 Hugging Face 下载指南补齐，不要求使用者理解底层数据构建过程。

## 统一数据内容

`unified_bgg` 将 7 个 BGG 公共快照按官方游戏 ID 对齐，内部实体键为 `bgg:{bgg_id}`。当前统一产品包括：

- 约 100,274 个游戏实体和 345,282 条来源映射；
- 多来源、多时间点的评分、排名、投票数、复杂度、人数和时长快照；
- 规范化机制、类别、主题、子域、家族和领域 taxonomy；
- 约 128,320 条游戏/机制/评论 RAG 文档，以及 100 个高分游戏的规则书语料；
- 4,195 条可追溯的中文微调候选样本，覆盖问答、机制解释、评论总结、推荐理由和结构化抽取。

所有时间敏感事实都保留 `snapshot_date` 和 `source_dataset`。评论和规则书内容属于来源方或用户生成内容，仅用于研究、检索和设计分析。

## Skill 目录

```text
skills/unified-bgg-rag-retrieval/
├─ SKILL.md                         Agent 工作规范和报告契约
├─ agents/openai.yaml               Skill 列表显示信息
└─ scripts/query_unified_bgg_game.py  游戏概览 + 评论摘要便捷查询器
```

Skill 支持游戏查找、机制召回、规则摘要、评论主题、玩家人数定位、竞品比较和 Markdown 报告生成。详细设计见 `skills/unified-bgg-rag-retrieval/SKILL.md`。

## 示例和研究报告

只保留当前版本的示例输出：

- `datasets/unified_bgg/docs/top100_reports/`：100 个高分游戏报告；
- `datasets/unified_bgg/docs/top10_reports_v4/`：按实际游玩流程组织的最新 Top 10 报告；
- `datasets/unified_bgg/docs/party_top10/`：派对游戏分类示例；
- `datasets/unified_bgg/docs/two_player_top10/`：双人游戏分类示例；
- `datasets/unified_bgg/docs/brass_birmingham_flow_report_v2.md`：流程化单篇示例；
- `datasets/unified_bgg/docs/brass_birmingham_full_report.md`：完整资料型示例。

示例目录的文件清单和使用边界见 [`datasets/unified_bgg/docs/README.md`](datasets/unified_bgg/docs/README.md)；阶段性审计和旧版本批量报告已移除。

## 常见问题

**查询时报索引不存在**：先在仓库根目录执行 `python datasets\unified_bgg\scripts\download_public_data.py --kind query`。

**只想下载一个大文件**：使用 Hugging Face 页面中的 `resolve/main/<remote-path>` 直链，或参考 `HUGGINGFACE_DATA_GUIDE.md` 的 `hf_hub_download` 示例。

**磁盘空间不足**：只下载 FTS 索引，使用 `python ...\download_public_data.py --kind fts`；vector、规则书索引和完整语料可以按需下载。

**中文输出乱码**：使用 Windows PowerShell 5.1 时保持终端 UTF-8，并将 Markdown 文件以 UTF-8 保存；查询脚本已经统一配置 UTF-8 输出。

**需要重新处理原始数据**：这是维护者工作，不属于普通使用流程。底层脚本和工程说明保留在 `datasets/unified_bgg/scripts/` 与 `datasets/unified_bgg/README.md`。

## 许可和引用

本项目整合的数据许可并不统一。`bgg-threnjen` 为 CC BY-SA 3.0，`bgg-andrewmvd` 为 CC BY 4.0；部分来源为 Other/自定义许可，发布、再分发或商用前必须核对原始来源页面。BGG 用户评论和规则书可能受额外版权约束。

引用本项目时请同时注明：

- GitHub：`https://github.com/CJH0220/unified-bgg-boardgame-agent`
- Hugging Face：`https://huggingface.co/datasets/ChenJinHua/BGG_datasets_Agent`
- 使用的数据快照、文件路径和 `manifest.json` 版本。
