# bgg-ranked-mattadamhouser — Ranked Board Game Data（2023，Top-2000）

> **本地路径** `research/datasets/bgg-ranked-mattadamhouser/raw/`（5 个 csv，共 1.4 MB）
> **来源** [kaggle.com/datasets/mattadamhouser/ranked-board-game-data-from-boardgamegeek](https://www.kaggle.com/datasets/mattadamhouser/ranked-board-game-data-from-boardgamegeek)
> **许可** **CC0（公共领域）** —— 本地许可最宽松的数据集，可随意使用
> **快照** 2023-08
> **爬虫源码** [github.com/mhouser42/bgg_scrape](https://github.com/mhouser42/bgg_scrape)
> **本仓库定位** L3 机制本体的**中间时间锚点** + 唯一的**续作谱系**数据

## 0. 小而精，三个别处没有的东西

体量只有 2,000 款游戏（BGG Top-2000），但含三样别的数据集没有的：

1. **188 个机制的 2023 词表** —— 正好卡在 2021（157 个）与 2025（192 个）之间，是观察 BGG 机制体系拆分的关键中间态
2. **`reimplementations_2023.csv`** —— 470 条**续作/重做谱系**（`parent_id` + `iteration` 迭代代数），做「机制传承」分析的唯一现成数据
3. 作者的原始动机就是「比较 2017 mechanics 与 2023 mechanisms 对子域的分类能力」，与本仓库的机制本体研究目标高度重合

## 1. 文件与 schema

5 张表全部以 **`game_id`** 关联。

| 文件 | 行数 | 列数 | 说明 |
|---|---|---|---|
| `basic_data_2023.csv` | 2,000 | 17 | 基础信息 + 评分 |
| `mechanisms_2023.csv` | 2,000 | 189 | **188 个机制** 0/1 矩阵，`game_id` 在第 0 列 |
| `themes_2023.csv` | 2,000 | 85 | 84 个主题 0/1 矩阵，⚠️ **首列是无名索引列**，`game_id` 在第 1 列 |
| `subdomains_2023.csv` | 2,000 | 9 | 8 个子域 0/1 |
| `reimplementations_2023.csv` | 470 | 7 | 续作谱系 |

> ⚠️ `themes_2023.csv` 用 `pd.read_csv` 会多出一列 `Unnamed: 0`，读时加 `index_col=0`。
> 同一数据集里 `mechanisms_2023.csv` 却没有这一列 —— **两张表布局不一致，逐表确认**。

### 1.1 `basic_data_2023.csv`

| 列 | 实测范围 | 说明 |
|---|---|---|
| `rank` | 1 – 2000 | BGG 综合排名，无缺失（本来就是按排名截取的 Top-2000） |
| `game_id` | 1 – 374,173 | 主键 |
| `bgg_url` / `name` / `designer` | — | `designer` 为逗号分隔多值，0.15% 空 |
| `year` | **-2200** – 2023 | 负数为公元前传统游戏 |
| `min_players` / `max_players` | 1–8 / 0–100 | `max_players=0` 仍存在（未知） |
| `min_time` / `avg_time` / `max_time` | 0 – 12,000 分钟 | ⚠️ `avg_time` 与 `max_time` **逐行完全相同（2000/2000 行，实测）**，是重复列；`min_time` 有 889 行也与之相同。与 threnjen 的 `MfgPlaytime`/`ComMaxPlaytime` 同类问题 |
| `weight` | 1.018 – 4.828 | 复杂度，**这里没有 0**（Top-2000 都有足够投票） |
| ⭐ `avg_rating` | **6.377** – 9.224 | 算术均分。注意下界 6.38 —— **样本被排名截断，不含低分游戏** |
| ⭐ `geek_rating` | **6.179** – 8.423 | 贝叶斯收缩分 |
| `num_votes` | **673** – 119,956 | 最少也有 673 票，与全量数据集的 30 票门槛完全不同 |
| `owned` | 829 – 191,284 | 拥有人数 |
| `age` | 0 – 18 | 建议年龄 |

> ### ⚠️ 这是一份「截断样本」，不能用来估计总体分布
> 评分下界 6.38、票数下界 673，意味着**低分游戏和冷门游戏被系统性排除**。
> 任何「评分 ~ 机制」的回归在这份数据上都会遭遇**选择偏差**（range restriction），相关系数会被压低。
> 它适合做的是：头部游戏的机制画像、机制词表对照、续作谱系分析。
> 要做总体统计请用 `bgg-threnjen`（21,925 款，含长尾）或 `games_detailed_info2025`（27,780 款）。

### 1.2 `mechanisms_2023.csv` —— 188 个机制

- 每款游戏平均 **5.702 个机制**（中位 5，最多 21，6 款零标注）
- Top 8：Hand Management **35.55%** · Dice Rolling 30.40% · Variable Player Powers 28.90% · Set Collection 22.15% · Open Drafting 20.55% · Solo / Solitaire Game 18.05% · Area Majority / Influence 17.65% · Modular Board 15.95%

> ### 📌 这组数字解释了调研报告与实测的分歧
> `../../boardgame-datasets-survey.md` 引用文献称「平均 6.35 个机制、Hand Management 38.4%」。
> - 本数据集（**Top-2000**）：平均 **5.70** 个，Hand Management **35.6%** —— 与文献接近
> - threnjen（**全量 21,925**）：平均 **3.11** 个，Hand Management **20.5%**
> - 2025 全量（27,780）：平均 **3.20** 个，Hand Management **20.6%**
>
> **文献统计的是头部游戏子集**。头部游戏标注更完整、机制更复杂，所以数字系统性偏高。
> 引用任何「机制平均数/流行度」时**必须同时说明样本是 Top-N 还是全量**，否则结论不可比。

### 1.3 `subdomains_2023.csv`

8 个子域 0/1：Strategy Games **50.2%** · Family Games 30.0% · Thematic Games 20.1% · Wargames 8.8% · Party Games 6.3% · Abstract Games 5.7% · Customizable Games 3.5% · Children's Games 2.0%

对比 threnjen 全量的子域分布（War 16.1% · Strategy 10.6% · Family 10.6%），**Top-2000 里 Strategy 占了一半** —— 直观量化了 BGG 排行榜的「重策偏好」。这正是调研报告第 7 节「采样偏差」的实证。

### 1.4 ⭐ `reimplementations_2023.csv` —— 续作谱系

| 列 | 说明 |
|---|---|
| `game_id` | 子游戏 |
| `parent_id` | 被重做/继承的父游戏（359 个不同父节点） |
| `year` | 1903 – 2022 |
| `iteration` | **1 – 5**，第几代 |
| `reimplementation` | 98.94% 为 1 |
| `expansion` | **恒为 0**（废列） |
| `compilation` | 1.7% |

470 条关系构成一片**森林**：可以直接建图做「机制在系列内如何演化」——同一 `parent_id` 下不同代的机制集合差分，就是设计师的迭代取舍记录。这在其它数据集里都拿不到。

```python
import pandas as pd, networkx as nx
re_ = pd.read_csv("raw/reimplementations_2023.csv")
mech = pd.read_csv("raw/mechanisms_2023.csv")
G = nx.from_pandas_edgelist(re_, "parent_id", "game_id", create_using=nx.DiGraph)
# 对每条父子边，比较两侧机制集合的增删
```

## 2. 加载配方

```python
import pandas as pd
RAW = "research/datasets/bgg-ranked-mattadamhouser/raw"
basic = pd.read_csv(f"{RAW}/basic_data_2023.csv")
mech  = pd.read_csv(f"{RAW}/mechanisms_2023.csv")
theme = pd.read_csv(f"{RAW}/themes_2023.csv", index_col=0)   # ← 必须，去掉无名索引列
sub   = pd.read_csv(f"{RAW}/subdomains_2023.csv")
df = basic.merge(mech, on="game_id").merge(theme, on="game_id").merge(sub, on="game_id")
df = df.drop(columns=["max_time"])                            # avg_time 与 max_time 重复
```

## 3. 合规

**CC0 公共领域**，无署名义务，可自由用于任何用途（含商用）。底层数据来自 BGG，二次分发大规模衍生数据时仍建议注明 BGG 来源。
