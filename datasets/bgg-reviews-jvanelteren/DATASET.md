# bgg-reviews-jvanelteren — BoardGameGeek Reviews

> **本地路径** `research/datasets/bgg-reviews-jvanelteren/raw/`
> **来源** [kaggle.com/datasets/jvanelteren/boardgamegeek-reviews](https://www.kaggle.com/datasets/jvanelteren/boardgamegeek-reviews)
> **许可** Other（作者在页面描述中自定，非标准开源许可 —— **商用前需自行确认**）
> **最新快照** 2025-02-01
> **本地体量** 5 个文件 / 2,286 MB（已跳过两份被取代的历史快照，见 §6）
> **本仓库定位** L2 文本评论 + **最新的 L1 元数据**（`games_detailed_info2025.csv` 比 threnjen 新 4 年）

## 0. 先修正调研报告里的三个数字

`../../boardgame-datasets-survey.md` 第 2.3 节写的是「**~13M 条评论**（评分 + 可选文本），2019 年采集」。本地实测：

| 项 | 调研报告 | **实测（全量单遍扫描）** |
|---|---|---|
| 评论条数 | ~13M | **26,200,012** |
| 采集时间 | 2019 | **2025-02**（作者持续更新，13M→15M→19M→26M） |
| 带文本比例 | 未提 | ⚠️ **仅 16.09%**（4,215,806 条），其余 83.91% 是**纯评分无文本** |

> **最后一行是本文档最重要的信息**：如果按「13M 条文本评论」做语料规模估算，实际可用文本量会**差 3 倍以上**。
> 真正的文本语料是 **421 万条、平均 213.5 字符**（最长 26,962 字符）。

---

## 1. 文件清单

| 文件 | 行数 | 列数 | 大小 | 内容 |
|---|---|---|---|---|
| `bgg-26m-reviews.csv` | **26,200,012** | 6 | 2,078 MB | 逐条评分 + 可选文本评论（2025 快照） |
| `games_detailed_info2025.csv` | **27,780** | 52 | 105 MB | ⭐ **最新游戏元数据**（2025） |
| `games_detailed_info.csv` | 21,631 | 56 | 95 MB | 旧版元数据（约 2022，含已废弃的电子游戏排名列） |
| `2022-01-08.csv` | 21,831 | 10 | 4.8 MB | 2022-01-08 排行榜快照 |
| `2020-08-19.csv` | 19,330 | 10 | 3.5 MB | 2020-08-19 排行榜快照 |

**未下载**（可用 `-IncludeHistoricalReviews` 补）：`bgg-15m-reviews.csv`（1,326 MB）、`bgg-19m-reviews.csv`（1,550 MB）—— 是 26M 版的历史前缀快照，除非要做「同一批用户评分随时间漂移」的分析，否则没必要占 2.9 GB。

---

## 2. `bgg-26m-reviews.csv` —— 26.2M 条评分/评论

| 列 | 类型 | 说明 |
|---|---|---|
| *(无列名，第 0 列)* | int | ⚠️ **是 pandas 导出残留的自增行号**（实测 0…26200011 严格连续）。读入时必须 `index_col=0` 或 `usecols=[1,2,3,4,5]`，否则多出一列 `Unnamed: 0` |
| `user` | str | 用户名。**同样有纯数字用户名，必须 `dtype={"user":"string"}`** |
| `rating` | float | 1.0 – 10.0 |
| `comment` | str | **83.91% 为空**。非空时平均 213.5 字符 |
| `ID` | int | BGG 游戏 id，可与其它数据集的 `BGGId` / `game_id` 直接 join |
| `name` | str | 游戏名（冗余列，join 时用 `ID` 不要用 `name`） |

### 2.1 实测统计（`_profiles/reviews_facts.json`，全量非抽样）

- **555,482 个用户 × 27,865 款游戏**，稀疏度 0.17%
- 评分分布强烈右偏，整数评分众数是 `7`（5,883,610）> `8`（5,140,393）> `6`（3,722,536）
- 非整数评分占 **17.0%**
- **12 条评分 < 1**（越界脏数据），无 > 10
- 每用户评论数：中位 **11**，均值 47，最多 **16,792**；**114,538 个用户（20.6%）只评过 1 次**
- 每游戏评论数：中位 **125**，最多 131,303，最少 **29**（≈ BGG 的 30 票门槛）

### 2.2 ⚠️ 文件按游戏聚簇排序，禁止用前缀抽样

实测：**前 300 万行只覆盖 60 款游戏**（CATAN、Carcassonne 等头部热门）。

```python
df = pd.read_csv("bgg-26m-reviews.csv", nrows=1_000_000)   # ❌ 得到的是十几款热门游戏的评论
```

这样抽出来的样本平均分 7.70（全表 7.13 左右），完全不可用于任何分布估计。
要抽样必须**随机跳行**或先按 `ID` 分组再抽：

```python
import random
random.seed(0)
keep = lambda i: i == 0 or random.random() < 0.01          # 1% 均匀抽样
df = pd.read_csv("bgg-26m-reviews.csv", index_col=0, skiprows=lambda i: not keep(i),
                 dtype={"user": "string"})
```

### 2.3 只要带文本的那 421 万条

```python
it = pd.read_csv("bgg-26m-reviews.csv", index_col=0, chunksize=1_000_000,
                 dtype={"user": "string", "comment": "string"})
text = pd.concat([c[c["comment"].notna()] for c in it])     # ≈ 4.22M 行，内存约 1.5 GB
```

---

## 3. ⭐ `games_detailed_info2025.csv` —— 本仓库最新、最干净的元数据表

**27,780 行 × 52 列**，2025-02 快照。**在多个维度上优于 threnjen 的 `games.csv`（2021）**：

| 维度 | threnjen `games.csv` (2021) | **本表 (2025)** |
|---|---|---|
| 游戏数 | 21,925 | **27,780** |
| 描述文本 | ❌ 已词干化 + 去停用词，不可读 | ✅ **原始英文全文**（`In CATAN (formerly The Settlers of Catan), players try to be the dominant force…`） |
| 机制词表 | 157 个（2021 版） | ✅ **192 个（2025 版）** |
| 子域排名缺失值 | ❌ 哨兵 `21926` | ✅ **真正的空值** |
| 语言依赖度 | ❌ 语义存疑的 `LanguageEase` | ✅ 原始投票 `suggested_language_dependence`（含 `@level` 1–6） |
| 用户级评分 | ✅ 19M 条 | ❌ 无（要配 `bgg-26m-reviews.csv`） |

### 3.1 评分与排名列

| 列 | 实测 | 说明 |
|---|---|---|
| `usersrated` | 30 – 132,477 | 评分人数，最小 30 = BGG 排名门槛 |
| `average` | 1.259 – 9.839，均值 6.469 | 算术均分 |
| `bayesaverage` | 3.660 – 8.409，均值 5.671 | **Geek Rating，排序用这个** |
| `stddev` | 0.447 – 4.238 | 评分离散度 |
| `averageweight` | 0 – 5，均值 1.941 | 复杂度，**0 = 无人投票** |
| `numweights` | 0 – 8,414 | 复杂度投票数（threnjen 那边作者标为「? Unknown」的字段，这里语义明确） |
| `numcomments` | 0 – 22,600 | ✅ 有效（threnjen 的同名列全是 0） |
| `Board Game Rank` | 1 – 27,869 | 综合排名 |
| 9 个子域排名 | 见下 | **空值率就是「不属于该子域」，无哨兵值** |

子域排名缺失率：War Game 84.4% · Family Game 87.9% · Strategy Game 89.1% · Thematic 93.9% · Abstract 94.8% · Children's 96.1% · Party 96.7% · Customizable 98.7% · RPG Item / Accessory 99.996%（各只剩 1 款，属于误入的非桌游条目，建议直接剔除）

> ⚠️ `median` 列恒为 **0**（BGG API 一直返回 0），是废列，与 threnjen 的 `NumComments` 同类问题。

### 3.2 多值字段都是「字符串化的 Python 列表」

`boardgamecategory` / `boardgamemechanic` / `boardgamedesigner` / `boardgameartist` / `boardgamepublisher` / `boardgamefamily` / `boardgameexpansion` / `alternate` 等，存的是 `"['Chaining', 'Dice Rolling']"` 这样的**字符串**，不是 JSON（单引号），`json.loads` 会失败：

```python
import ast
df["mechanics"] = df["boardgamemechanic"].fillna("[]").map(ast.literal_eval)
df = df.explode("mechanics")
```

`suggested_num_players` / `suggested_playerage` / `suggested_language_dependence` 则是**字符串化的字典列表**（`[{'@numplayers': '1', ...}]`），同样用 `ast.literal_eval` 解。

### 3.3 机制标注

- 词表 **192 个机制**，`boardgamemechanic` 空值率 6.35%
- **平均每款游戏 3.196 个机制**
- Top 10：Dice Rolling 27.54% · Hand Management 20.57% · Set Collection 13.81% · Variable Player Powers 12.39% · Hexagon Grid 10.54% · Simulation 9.27% · Open Drafting 8.95% · Cooperative Game 8.76% · Tile Placement 8.37% · Grid Movement 7.93%

---

## 4. `games_detailed_info.csv`（旧版，21,631 行 × 56 列）

与 2025 版的差异：
- **多出 6 列**：`Amiga Rank`、`Arcade Rank`、`Atari ST Rank`、`Commodore 64 Rank`、`Video Game Rank`、`primary`
  → BGG 早期把电子游戏排名混在同一接口里，后来拆走了
- 2025 版把 `primary` 更名为 `name`，新增 `boardgameaccessory`
- `bayesaverage` 最小值是 **0.0**（未排名游戏填 0，是另一种哨兵），2025 版最小值 3.66（已剔除）

**除非要做 2022 vs 2025 的纵向对比，否则直接用 2025 版。**

---

## 5. `2020-08-19.csv` / `2022-01-08.csv`

各 10 列的排行榜快照（19,330 / 21,831 行）。加上 `games_detailed_info`（~2022）与 `games_detailed_info2025`，这个数据集内部就构成一条 **2020 → 2022 → 2025 的时间线**，可以直接测「同一批游戏的评分/排名漂移」而不必跨数据集对齐。

---

## 6. 复现与合规

```powershell
# 默认（跳过 15m/19m 历史快照）
powershell -ExecutionPolicy Bypass -File ..\_scripts\download.ps1 -Only bgg-reviews-jvanelteren
# 需要历史快照时
powershell -ExecutionPolicy Bypass -File ..\_scripts\download.ps1 -Only bgg-reviews-jvanelteren -IncludeHistoricalReviews
```

- 许可为 **Other（作者自定）**，Kaggle 页面未给标准开源协议。**做公开发布或商用前必须回原页面确认授权**，这是本地所有数据集里许可最不明确的一个。
- 底层内容是 BGG 用户撰写的评论，**著作权属于各用户**；用于训练/再发布时请只保留聚合统计或做去标识化。
- 事实来源：`../_profiles/reviews_facts.json`（全量扫描）与 `../_profiles/bgg-reviews-jvanelteren__*.json`
  ⚠️ 其中 `bgg-26m-reviews.csv.json` 是**前 300 万行的截断剖析**（且该文件按游戏排序，前缀有偏），该文件的权威数字以 `reviews_facts.json` 为准。
