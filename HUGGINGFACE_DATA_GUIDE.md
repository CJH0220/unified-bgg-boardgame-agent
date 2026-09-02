# Hugging Face 大文件数据说明与下载指南

本项目的 GitHub 仓库只提交代码、文档、清单、报告和小型样本。原始数据、完整 RAG 语料、SQLite 索引以及大型中间表存放在 Hugging Face Dataset 仓库：

**https://huggingface.co/datasets/ChenJinHua/BGG_datasets_Agent**

## 1. 为什么使用 Hugging Face

GitHub 普通仓库不适合承载本项目的大文件：单文件上限为 100 MB，而本地最大文件约 2.03 GB，所有待转存文件合计约 5.46 GB。Hugging Face Dataset 使用 LFS/分片存储，适合按文件或按目录下载，也能与 Python 数据处理工具直接集成。

## 2. 远程目录约定

上传后文件映射到以下稳定路径，路径不包含本机 `D:\OpenViking` 前缀：

```text
BGG_datasets_Agent/
├─ raw/                                  原始 BGG 数据集
│  ├─ bgg-threnjen/
│  ├─ bgg-reviews-jvanelteren/
│  ├─ bgg-gabrio/
│  ├─ bgg-ranked-mattadamhouser/
│  ├─ bgg-mrpantherson/
│  ├─ bgg-andrewmvd/
│  └─ bgg-sujaykapadnis/
├─ derived/intermediate/                  大型统一中间表
├─ derived/samples/rag/                   完整 RAG JSONL 语料
├─ indexes/final/                         FTS/vector/rulebook SQLite 索引
└─ rulebook_cache/                        规则书 PDF/文本缓存
```

## 3. 主要文件和用途

| 远程目录 | 内容 | 典型用途 |
| --- | --- | --- |
| `raw/bgg-threnjen/` | 游戏属性、机制/主题矩阵、约 1,894 万用户评分 | 协同过滤、评分矩阵和 2021 快照分析 |
| `raw/bgg-reviews-jvanelteren/` | 2025 游戏详情、约 2,620 万评分/评论行、历史快照 | 最新元数据、评论文本和时间快照分析 |
| `raw/bgg-gabrio/` | 约 90,400 行 SQLite，含扩展和原始描述 | 历史 taxonomy、扩展覆盖和描述补充 |
| `derived/intermediate/` | `games.csv`、`game_taxonomy*.csv` 等统一表 | 不重新扫描原始文件，直接开展分析或重建 RAG |
| `derived/samples/rag/` | 完整 `game_overview.jsonl`、`review_digest.jsonl` | 下游 RAG、嵌入和离线评测 |
| `indexes/final/` | FTS5、稀疏 TF-IDF、规则书索引 | 本地快速查询；也可下载后直接运行查询脚本 |
| `rulebook_cache/` | 规则书 PDF/文本抓取缓存 | 重建规则书语料时复用，避免重复下载 |

## 4. 浏览器下载

数据集主页：

https://huggingface.co/datasets/ChenJinHua/BGG_datasets_Agent/tree/main

单文件直链格式：

```text
https://huggingface.co/datasets/ChenJinHua/BGG_datasets_Agent/resolve/main/<remote-path>
```

例如：

```text
https://huggingface.co/datasets/ChenJinHua/BGG_datasets_Agent/resolve/main/raw/bgg-threnjen/user_ratings.csv
```

## 5. CLI 下载

```powershell
python -m pip install -U huggingface_hub
hf download ChenJinHua/BGG_datasets_Agent `
  --repo-type dataset `
  --include "derived/samples/rag/game_overview.jsonl" `
  --local-dir .\hf_data
```

下载整个数据集需要数 GB 磁盘空间：

```powershell
hf download ChenJinHua/BGG_datasets_Agent `
  --repo-type dataset `
  --local-dir .\hf_data
```

## 6. Python 下载

```python
from huggingface_hub import snapshot_download, hf_hub_download

path = hf_hub_download(
    repo_id="ChenJinHua/BGG_datasets_Agent",
    repo_type="dataset",
    filename="derived/samples/rag/game_overview.jsonl",
    local_dir="hf_data",
)
print(path)

snapshot_download(
    repo_id="ChenJinHua/BGG_datasets_Agent",
    repo_type="dataset",
    allow_patterns=["indexes/final/*"],
    local_dir="hf_data",
)
```

## 7. 下载后接入本项目

把下载目录中的文件放回 `datasets/` 对应位置后，可直接运行：

```powershell
Set-Location D:\OpenViking\research\datasets\unified_bgg
python scripts\evaluate_rag_quality.py
python scripts\build_rag_index.py
python scripts\build_vector_index.py
python scripts\query_unified_index.py "Brass Birmingham" --engine hybrid --limit 5
```

如果下载的是现成 SQLite 索引，可跳过构建步骤，并使用 `--fts-index` 或 `--vector-index` 指向下载后的文件。

## 8. 版本与校验

上传时同步 `huggingface_upload_manifest.json`，记录本地/远程路径、文件大小、SHA256、生成时间、处理版本和内容类型。下载后可校验：

```powershell
Get-FileHash .\hf_data\derived\samples\rag\game_overview.jsonl -Algorithm SHA256
```

## 9. 许可证和内容限制

- BGG 数据及其字段版权归原始来源和 BoardGameGeek 相关权利人所有。
- `bgg-threnjen` 为 CC BY-SA 3.0，`bgg-andrewmvd` 为 CC BY 4.0，发布时必须履行署名/相同方式共享义务。
- `bgg-gabrio`、`bgg-sujaykapadnis`、`bgg-reviews-jvanelteren` 的许可需要以来源页面为准，商用前必须重新确认。
- `bgg-26m-reviews.csv` 及 `review_digest.jsonl` 包含 BGG 用户生成评论文本，公开下载前应完成版权、隐私和平台条款审核。
- 规则书通常受出版商版权保护；相关文件仅用于研究和检索实验，不应默认用于再发布或商业训练。

## 10. 上传维护者

上传需要对 `ChenJinHua/BGG_datasets_Agent` 具有写权限的 Hugging Face User Access Token。Token 只应通过本地 `hf auth login` 或安全环境变量提供，不要写入 Git、Markdown、日志或脚本。
