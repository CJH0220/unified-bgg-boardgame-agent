# bgg-gabrio — Board Games Dataset（SQLite，覆盖面最广的历史快照）

> **本地路径** `research/datasets/bgg-gabrio/raw/database.sqlite`（140 MB）
> **来源** [kaggle.com/datasets/gabrio/board-games-dataset](https://www.kaggle.com/datasets/gabrio/board-games-dataset)
> **上游** R 包 [`9thcirclegames/bgg-analysis`](https://github.com/9thcirclegames/bgg-analysis)（爬虫 + 分析脚本开源）
> **许可** Other（作者自定，见 Kaggle 页面）
> **快照时间** 2017-06
> **本仓库定位** L1 补充 —— 覆盖面最广（**含扩展**）、**带原始描述文本**、保留 BGG 原始投票字段

## 0. 一句话定位

这是**唯一一份 SQLite 格式**的桌游数据集，**90,400 条**记录里包含 **13,712 个扩展**，
而且是 2017 年的旧快照 —— 它的价值不在「新」，而在三点：

1. **原始未处理的 `details.description`**（threnjen 的描述已被词干化毁掉）
2. **保留 BGG 原始投票字段**，包括分级明确的 `polls.language_dependence`
3. **51 个机制的历史词表** —— 做机制本体演化研究的时间锚点（见 §4）

## 1. 库结构

```
database.sqlite
├── BoardGames                  90,400 行 × 81 列   ← 主表
├── bgg.topics                  29,313 行 × 74 列   ← 主表子集 + LDA 主题标注
├── bgg.ldaOut.topics           29,229 行 × 2 列    ← 每款游戏的主题归属
├── bgg.ldaOut.top.terms           250 行 × 4 列    ← 25 个主题 × 各 10 个高权重词
└── bgg.ldaOut.top.documents       288 行 × 4 列    ← 每主题的代表性游戏
```

后四张表是 R 包作者跑的 **LDA 主题模型（25 个主题）** 产物，特征词是「标签名」而非自然语言词，例如主题 1 的高权重项是 `Bluffing.category`(0.183)、`Deduction.category`(0.164)、`Partnerships.mechanic`(0.080)、`PartyGame.category`(0.066)。

> **对机制 Agent 的意义**：这等于一份现成的「**机制/主题共现聚类**」结果 —— 25 个主题就是 25 组经验上会一起出现的机制+主题组合。做机制组合可行性先验时可以直接拿来当基线，不必从零跑一遍 LDA。

## 2. `BoardGames` 主表（81 列）

`game.id` 是主键，注意**存成 TEXT**（`'1'`, `'2'`…），与其它数据集的整数 `BGGId` join 前需转型。

### 2.1 组成

| `game.type` | 行数 |
|---|---|
| `boardgame` | 76,688 |
| `boardgameexpansion` | **13,712** |

> Kaggle 页面写「around 94,000」，实测 **90,400**。做规模对比时用实测值。
> **含扩展**是这份数据独有的：threnjen / andrewmvd 都只有本体。分析前先按 `game.type` 过滤，否则扩展会污染统计。

### 2.2 ⭐ 评分字段（前缀 `stats.`）

| 列 | 说明 |
|---|---|
| `stats.average` | 算术均分，1.0 – 10.0 |
| `stats.bayesaverage` | Geek Rating。⚠️ **未排名游戏填 0**，`> 0` 的只有 **18,063** 款（占 20%）—— 又一个「0 当哨兵」的坑 |
| `stats.usersrated` | 评分人数，0 – 67,655，全库合计 **11,131,331** 条评分（比 threnjen 2021 的 18.9M 少 41%，反映 4 年增长） |
| `stats.stddev` / `stats.median` | 离散度 / 中位数 |
| `stats.averageweight` | 复杂度 0 – 5，**0 = 无投票** |
| `stats.numweights` / `stats.numcomments` | 各自的投票/评论数 |
| `stats.owned` / `trading` / `wanting` / `wishing` | 收藏热度四件套 |
| `stats.subtype.boardgame.pos` | 综合排名，1 – 13,682，**仅 15.1% 非空**（其余是未排名游戏，**这里用的是真 NULL，不是哨兵**）|
| `stats.family.<子域>.bayesaverage` / `.pos` | 8 个子域各自的 Geek 分与排名：abstracts / cgs / childrensgames / familygames / partygames / strategygames / thematic / wargames |

> ⚠️ 库里还有 `stats.family.amiga.*`、`stats.family.arcade.*`、`stats.family.atarist.*`、`stats.family.commodore64.*`、`stats.subtype.videogame.*`、`stats.subtype.rpgitem.*` —— **这些是电子游戏/RPG 条目的残留列**，桌游分析中应直接忽略。

### 2.3 ⭐ 文本与属性

| 列 | 非空率 | 说明 |
|---|---|---|
| `details.description` | **100.0%** | ✅ **原始英文全文**，未做任何清洗。示例：`Die Macher is a game about seven sequential political races in different regions of Germany. Players are in charge of national political parties, and must manage limited resources…` |
| `attributes.boardgamecategory` | 98.3% | **逗号分隔字符串**（不是列表字面量），需 `.split(",")` |
| `attributes.boardgamemechanic` | 83.1% | 同上，示例 `Area Control / Area Influence,Auction/Bidding,Dice Rolling,Hand Management,Simultaneous Action Selection` |
| `attributes.boardgamedesigner` / `artist` / `publisher` / `family` | — | 同为逗号分隔 |
| `attributes.boardgameexpansion` / `implementation` / `integration` / `compilation` | — | **游戏间关系**，做「机制传承 / 系列演化」分析的原料 |
| `details.yearpublished` | 100% | -3500 – 2019 |

> ⚠️ 逗号分隔 + 机制名本身含逗号是有风险的，但实测 BGG 机制名里不含逗号（含的是 `/` 和 `:`），可以安全 split。

### 2.4 ⭐ `polls.language_dependence` —— 解决 threnjen 的字段悬案

本列是**明确的有序分类值**，实测取值只有 5 种（非空 22.9%）：

| 取值 | 行数 |
|---|---|
| `No`（无文字依赖） | 9,756 |
| `Some` | 3,898 |
| `Moderate` | 3,110 |
| `Extensive` | 2,865 |
| `Unplayable`（不懂语言无法玩） | 1,099 |

> **交叉印证**：`bgg-reviews-jvanelteren/games_detailed_info2025.csv` 里的原始投票 `suggested_language_dependence` 带 `@level` 1–6 的分级结构，与此一致。
> 由此可以确认：**threnjen `games.csv` 的 `LanguageEase`（实测 1–1757、均值 216）不是语言依赖度等级**，作者的字段说明有误。要用语言依赖度，请从本表或 2025 元数据表取。

另有 `polls.suggested_numplayers.1` … `.10` / `.Over` 和 `polls.suggested_playerage` —— **逐人数的社区投票原始结果**，比 threnjen 那种压缩成 `BestPlayers` 单值的形式信息量大得多。

## 3. 读取方式（stdlib 即可，无需额外依赖）

```python
import sqlite3, pandas as pd
con = sqlite3.connect("raw/database.sqlite")

games = pd.read_sql_query("""
    SELECT [game.id] AS game_id, [details.name] AS name, [details.description] AS description,
           [details.yearpublished] AS year, [attributes.boardgamemechanic] AS mechanics,
           [stats.average] AS average, [stats.bayesaverage] AS bayes,
           [stats.usersrated] AS n_ratings, [stats.averageweight] AS weight,
           [polls.language_dependence] AS lang_dep
    FROM BoardGames
    WHERE [game.type] = 'boardgame' AND [stats.usersrated] >= 30
""", con)                                            # → 18,063 款有效游戏

games["game_id"] = games["game_id"].astype(int)      # TEXT -> int，才能跟别的数据集 join
games["mechanics"] = games["mechanics"].fillna("").str.split(",")
```

⚠️ 列名带点号，SQL 里**必须用 `[]` 或双引号转义**，否则 SQLite 会当成表名.列名解析。

## 4. ⭐ 机制词表的历史价值：51 → 192

用本地各数据集的机制词表做纵向对比（实测，非引用）：

| 快照 | 数据集 | 机制数 |
|---|---|---|
| 2017-06 | **本数据集** | **51** |
| 2018-06 | mrpantherson | 52 |
| 2021-12 | threnjen | 157 |
| 2023-08 | mattadamhouser | 188 |
| 2025-02 | jvanelteren `games_detailed_info2025` | **192** |

2017 的 51 个与 2021 的 157 个只有 **36 个同名**，其余 15 个是被改名的：

| 2017 旧名 | → 2021+ 新名 |
|---|---|
| Area Control / Area Influence | Area Majority / Influence |
| Action Point Allowance System | Action Points |
| Action / Movement Programming | （拆分为 Action Queue / Programmed Movement 等） |
| Card Drafting | Drafting → 再拆为 Open / Closed Drafting |
| Co-operative Play | Cooperative Game |
| Deck / Pool Building | Deck, Bag, and Pool Building |
| Press Your Luck | Push Your Luck |
| Betting/Wagering | Betting and Bluffing |
| Area Enclosure | Enclosure |
| Route/Network Building | Network and Route Building |
| Partnerships | Team-Based Game |
| Hex-and-Counter | Hexagon Grid |
| Acting / Singing / Rock-Paper-Scissors | 2021 短暂移除，**2023 又加回来** |

> 上表的对应关系是**基于名称与语义的推断，非 BGG 官方映射**，用于跨快照对齐时请抽样人工复核。

**结论**：跨年份数据集做机制 join **绝对不能按名称字符串直接匹配** —— 2017↔2021 会静默丢掉 15 个机制的全部标注。要么统一到最新词表并维护一张改名映射表，要么只用同一快照内部的数据。

## 5. 合规

- 许可 Other（作者自定），上游 R 包为开源；**商用前回 Kaggle 页面与 GitHub 仓库确认**。
- ⚠️ **`bgg-sujaykapadnis` 是本数据集的严格子集**：10,532 款游戏全部落在本库的 90,400 条内，且 `average_rating` **逐条完全相同**（实测 10,532/10,532 精确匹配）。两者共享同一上游 R 包快照，**不能当作两个独立数据源做交叉验证**。
