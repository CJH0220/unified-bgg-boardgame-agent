# bgg-sujaykapadnis — Board Games Dataset（TidyTuesday 版）

> **本地路径** `research/datasets/bgg-sujaykapadnis/raw/board_games.csv`（15.8 MB）
> **来源** [kaggle.com/datasets/sujaykapadnis/board-games](https://www.kaggle.com/datasets/sujaykapadnis/board-games)
> **许可** Other（作者自定）
> **上游** 与 `bgg-gabrio` 同源 —— R 包 [`9thcirclegames/bgg-analysis`](https://github.com/9thcirclegames/bgg-analysis)
> **本仓库定位** ⚠️ **冗余数据** —— 保留仅为可追溯性，实际工作请用 `bgg-gabrio`

## 0. ⚠️ 先说结论：它是 gabrio 的严格子集

实测验证（`_scripts` 下的一次性核查，结果如下）：

| 检查项 | 结果 |
|---|---|
| 本数据集 `game_id` 是否全部落在 gabrio 的 90,400 条内 | ✅ **是**，10,532 / 10,532 全部命中，0 个独有 |
| 同一游戏的 `average_rating` 是否一致 | ✅ **10,532 / 10,532 逐条精确相同**（差值 < 1e-6） |

**因此**：
- ❌ 不能把它和 `bgg-gabrio` 当作两个独立数据源做交叉验证 —— 它们是同一次抓取
- ❌ 不能把两者拼接来「扩大样本」—— 会产生 10,532 条重复
- ✅ 唯一的用处：它是清洗过的**扁平 csv**，字段更少更好读；而 gabrio 是 81 列的 SQLite

这份数据就是 R 社区 **TidyTuesday**（2019-03-12 期）用的那份桌游数据，很多教程/博客的数字出自它。放在这里主要是为了在看到别人引用 TidyTuesday 数字时能对上账。

## 1. Schema（22 列，10,532 行）

| 列 | 实测 | 说明 |
|---|---|---|
| `game_id` | 1 – 216,725，10,532 唯一 | 主键 |
| `name` | 10,356 唯一 | 有重名 |
| `description` | 0% 空 | ✅ **原始英文全文**（与 gabrio 一致，未做词干化） |
| `image` / `thumbnail` | — | 注意是 **`//cf.geekdo-images.com/…` 协议相对 URL**，前面要补 `https:` |
| `year_published` | **1950 – 2016** | ⚠️ 与 gabrio（-3500 – 2019）不同：本子集**砍掉了 1950 年前的古游戏**，做「年份 → 机制演化」会缺古典部分 |
| `min_players` / `max_players` | 0–9 / 0–999 | 999 = 哨兵 |
| `min_playtime` / `playing_time` / `max_playtime` | 0 – 60,000 | ⚠️ `playing_time` 与 `max_playtime` **逐行完全相同（10,532/10,532，实测）**，重复列 |
| `min_age` | 0 – 42 | 42 为脏数据 |
| ⭐ `average_rating` | **1.384 – 9.004**，均值 6.371 | 算术均分，5 位小数 |
| ⭐ `users_rated` | **50** – 67,655 | ⚠️ 门槛是 **50 票**，不是 BGG 常见的 30 —— 作者额外筛过，所以样本比 gabrio 的「≥30 票 18,063 款」更窄 |
| `category` / `mechanic` / `designer` / `artist` / `publisher` / `family` | 逗号分隔多值 | `mechanic` 9.02% 空，实测词表 **52 个机制**（2017 旧版，`Area Control / Area Influence` 等旧名） |
| `expansion` | 73.87% 空 | 该游戏的扩展列表 |
| `compilation` | **96.11% 空** | 合集关系，几乎全空 |

**本数据集没有 `bayesaverage`、没有排名、没有复杂度（weight）** —— 这是它相对 gabrio 丢失最多的部分。

## 2. 加载

```python
import pandas as pd
df = pd.read_csv("raw/board_games.csv")
df["mechanic"] = df["mechanic"].fillna("").str.split(",")
df = df.drop(columns=["playing_time"])            # 与 max_playtime 重复
df["image"] = "https:" + df["image"].fillna("")   # 协议相对 URL 补全
```

## 3. 建议

**新工作不要从这份开始。** 按需求选：

| 需求 | 用 |
|---|---|
| 要同源但更全的数据（含扩展、含 weight、含排名） | `../bgg-gabrio/`（SQLite，90,400 行） |
| 要最新元数据 + 原始描述 | `../bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv`（27,780 行，2025） |
| 要用户级评分 | `../bgg-threnjen/raw/user_ratings.csv`（18.9M 条） |

## 4. 合规

许可为 Other（作者自定），上游 R 包开源。TidyTuesday 数据按其社区惯例可自由用于教学与分析，商用请回溯上游确认。
