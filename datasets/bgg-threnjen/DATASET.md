# bgg-threnjen — Board Game Database from BoardGameGeek

> **本地路径** `research/datasets/bgg-threnjen/raw/`
> **来源** [kaggle.com/datasets/threnjen/board-games-database-from-boardgamegeek](https://www.kaggle.com/datasets/threnjen/board-games-database-from-boardgamegeek)
> **许可** CC BY-SA 3.0（**必须署名 + 相同方式共享**，是本地所有数据集里许可最宽松清晰的一个）
> **数据快照时间** 2022-01-17（Kaggle `lastUpdated`），BGG 抓取时点约 2021 年末
> **体量** 9 个 csv + 1 个 txt，压缩包 673 MB
> **本仓库定位** L1（元数据 + 机制标签）+ L2（用户级评分）主力数据源

## 0. 为什么选它

唯一一个把「**游戏属性**」「**机制/主题标签**」「**用户级逐条评分**」放在同一份规范化多表结构里的主流公开集。
其它 Kaggle 桌游数据集要么只有游戏级聚合评分（无法做协同过滤），要么只有评论没有结构化属性。

代价：**时点数据（2021 末）**，评分与排名早已变化，不能当实时数据用；且只含 BGG **已排名**游戏（≥30 票），长尾缺失。

---

## 1. 表结构总览

全部行列数为**全量扫描实测**（非抽样、非 Kaggle 页面宣称值），来源 `_profiles/bgg-threnjen__*.json`。

| 文件 | 粒度 | 行数 | 列数 | 主键（列位置） | 含评分? | 大小 |
|---|---|---|---|---|---|---|
| `games.csv` | 一行一游戏 | 21,925 | 48 | `BGGId` @0 | ✅ 聚合评分 + 排名 | 21 MB |
| `user_ratings.csv` | 一行一（用户,游戏） | **18,942,215** | 3 | (`Username`,`BGGId`) | ✅ **原始逐条评分** | 381 MB |
| `ratings_distribution.csv` | 一行一游戏 | 21,925 | 96 | `BGGId` @0 | ✅ 评分直方图 | 8 MB |
| `mechanics.csv` | 一行一游戏 · 机制 0/1 矩阵 | 21,925 | 158 | `BGGId` @0 | ❌ | 6.7 MB |
| `themes.csv` | 一行一游戏 · 主题 0/1 矩阵 | 21,925 | 218 | `BGGId` @0 | ❌ | 9.2 MB |
| `subcategories.csv` | 一行一游戏 · 子类 0/1 矩阵 | 21,925 | 11 | `BGGId` @0 | ❌ | 0.6 MB |
| `designers_reduced.csv` | 一行一游戏 · 设计师 0/1 矩阵 | 21,925 | 1,594 | `BGGId` **@1592** | ❌ | 67 MB |
| `artists_reduced.csv` | 一行一游戏 · 美术 0/1 矩阵 | 21,925 | 1,681 | `BGGId` **@1679** | ❌ | 70 MB |
| `publishers_reduced.csv` | 一行一游戏 · 出版商 0/1 矩阵 | 21,925 | 1,866 | `BGGId` **@1864** | ❌ | 78 MB |
| `bgg_data_documentation.txt` | 作者原始字段说明 | 95 行 | — | — | — | 2 KB |

**所有表行数一致为 21,925**（除 user_ratings），说明是同一批游戏的横向切分，可直接按 `BGGId` 内连接而不丢行。编码统一 UTF-8 **带 BOM**（`pd.read_csv` 默认能处理，用标准库 `csv` 需 `encoding="utf-8-sig"`）。

所有表都用 **`BGGId`（BoardGameGeek 官方游戏 id）** 关联，可直接与 BGG 网页 `boardgamegeek.com/boardgame/<BGGId>` 对应，也是与 L3/L4 数据做 join 的唯一稳定外键。

> `*_reduced` 的含义：只保留作品数 > 3 的实体作为独立列，长尾实体折叠成一个 `Low-Exp` 类二值标志位。所以**不能**用这些表统计「某设计师共几款游戏」的完整分布。

---

## 2. `games.csv` 逐字段注释（48 列，21,925 行，UTF-8-BOM，无缺列行）

### 2.1 标识与文本

| 列 | 类型 | 实测范围 / 空值 | 语义与坑 |
|---|---|---|---|
| `BGGId` | int | 1 – 349,161，21,925 唯一 | **主键**。非连续，是 BGG 全站 id |
| `Name` | str | 2 空，21,520 唯一 | **355 个重名，涉及 759 行**（不同年份/版本同名）。**不要用名字做 join**。38 个纯数字名（如 `1830`）读入时会被推成 int，需 `dtype=str` 显式指定 |
| `Description` | str | 1 空，最长 8,958 字符 | ⚠️ **已被预处理过**：小写化、去停用词、词形还原、去标点。样例：`die macher game seven sequential political race different region germany player charge national political party manage l…`<br>更糟的是 HTML 实体被打碎：`Tal der Könige` → `tal der koumlnige`（`&ouml;` 残留成 `ouml`）。<br>**结论：这列不能当自然语言语料**（不能喂 LLM、不能做可读摘要），只适合做词袋/TF-IDF。需要原文必须回 BGG API 取 `description` |
| `ImagePath` | str | 17 空 | geekdo CDN 封面图 URL |
| `Family` | str | **69.6% 空**，1,456 唯一 | 游戏系列（如 `3M Bookshelf`），稀疏，慎作特征 |

### 2.2 ⭐ 评分相关（本数据集的核心价值）

| 列 | 类型 | 实测范围 | 均值 | 语义与坑 |
|---|---|---|---|---|
| `AvgRating` | float | 1.041 – 9.914 | 6.425 | = BGG `average`，**算术均值**。小样本虚高，不要直接当排序目标 |
| `BayesAvgRating` | float | 3.575 – 8.515 | 5.686 | = BGG `bayesaverage` / **Geek Rating**，贝叶斯收缩后向 ~5.5 靠。**做排序/回归目标用这列** |
| `StdDev` | float | 0.196 – 4.277 | 1.516 | 评分离散度。**天然的「争议度 / polarizing」指标**——机制 Agent 想找「有人爱有人恨」的机制组合就用它，别只看均值 |
| `NumUserRatings` | int | **30** – 108,101 | 862 | 评分人数。**最小值恰为 30**，反向印证了「BGG 要求 ≥30 票才进排名」这条筛选规则 |
| `NumComments` | int | 恒为 **0** | 0 | ⚠️ **废列**：全表 21,925 行全是 0，抓取时丢失。别用它判断「有没有评论」，要文本评论去 `bgg-reviews-jvanelteren` |
| `GameWeight` | float | 0 – 5 | 1.982 | = BGG `averageweight` 复杂度（1 轻 – 5 重）。**0 不是「极简」而是「无人投票」**，必须配合 `NumWeightVotes` 过滤 |
| `NumWeightVotes` | int | 0 – 7,673 | 49.5 | `GameWeight` 的分母。建议 `NumWeightVotes >= 5` 才采信复杂度 |

### 2.3 ⭐ 排名（含最大的一个陷阱）

| 列 | 覆盖游戏数 | 说明 |
|---|---|---|
| `Rank:boardgame` | 21,578 | BGG 综合总榜 |
| `Rank:strategygames` | 2,319 | 策略子榜 |
| `Rank:wargames` | 3,530 | 战棋子榜 |
| `Rank:familygames` | 2,316 | 家庭子榜 |
| `Rank:thematic` | 1,224 | 主题/叙事子榜 |
| `Rank:abstracts` | 1,115 | 抽象子榜 |
| `Rank:childrensgames` | 881 | 儿童子榜 |
| `Rank:partygames` | 640 | 派对子榜 |
| `Rank:cgs` | 303 | 集换式卡牌子榜 |

> ### ⚠️ 哨兵值陷阱：未排名 = `21926`，不是 `NaN`
> 全部 9 个 `Rank:*` 列的最大值都是 **21926 = 行数 + 1**。作者把「该游戏不在此榜」填成了 `len(df)+1` 而非空值。
>
> 实测哨兵行数（值 == 21926 的行）：`boardgame` 347 · `wargames` 18,395 · `strategygames` 19,606 · `familygames` 19,609 · `thematic` 20,701 · `abstracts` 20,810 · `childrensgames` 21,044 · `partygames` 21,285 · `cgs` 21,622。
>
> 每个子榜「非哨兵行数」与对应 `Cat:*` 标志位为 1 的行数**逐一精确相等**（如 strategygames 2,319 = `Cat:Strategy` 2,319），9 个子榜全部吻合 —— 哨兵语义确认无疑。
>
> 另注：`Rank:boardgame` 也有 **347 行是哨兵**，即这批游戏虽然满足 `NumUserRatings >= 30`，却没有综合排名（抓取时点处于排名边界）。做全站排名建模时这 347 行要单独剔除。
>
> **不处理的后果**：算 `mean(Rank:strategygames)` 得 19,730（≈ 哨兵值），任何「排名 vs 机制」的回归全被污染。
>
> ```python
> RANK_COLS = [c for c in games.columns if c.startswith("Rank:")]
> games[RANK_COLS] = games[RANK_COLS].replace(len(games) + 1, pd.NA)   # 21926 -> NA
> ```

### 2.4 子域二值标签

`Cat:Thematic` / `Cat:Strategy` / `Cat:War` / `Cat:Family` / `Cat:CGS` / `Cat:Abstract` / `Cat:Party` / `Cat:Childrens`，均为 0/1。

计数：War 3,530 · Strategy 2,319 · Family 2,316 · Thematic 1,224 · Abstract 1,115 · Childrens 881 · Party 640 · CGS 303。

**实测覆盖率只有 49.0%**（10,741 / 21,925）：11,184 款游戏 **一个子域标签都没有**，9,167 款恰好 1 个，1,561 款 2 个，13 款 3 个。

两个推论：① 子域标签**不是互斥的单标签**，别用 `argmax` 当分类目标，要按多标签处理；② 过半游戏无子域归属，做分层评估时这批「无标签」样本是主体，不能当缺失值丢掉。

### 2.5 人数与时长

| 列 | 实测范围 | 坑 |
|---|---|---|
| `MinPlayers` | 0 – 10 | **0 = 未知**（50 行）。众数 2（15,039） |
| `MaxPlayers` | 0 – **999** | `99` / `999` 是「人数不限」哨兵（154 行为 99）。0 = 未知（173 行）。算「人数区间宽度」前必须裁剪 |
| `BestPlayers` | 0 – 15 | 社区投票出的最佳人数。**0 = 无共识，占 91%**（19,944 行），实际可用样本仅约 2,000 |
| `GoodPlayers` | str | ⚠️ **是被 str 化的 Python 列表**，如 `"['3', '4', '5']"`，91% 是 `"[]"`。需 `ast.literal_eval` 解析，且元素是字符串不是 int |
| `MfgPlaytime` | 0 – 60,000 | 出版商标称时长（分钟）。⚠️ **与 `ComMaxPlaytime` 逐行完全相同（21,925 / 21,925 行相等，实测）**——是同一列的两个名字，喂模型时必须去掉一个，否则该特征权重被双算 |
| `ComMinPlaytime` | 0 – 60,000 | 社区最短时长，均值 63.7 |
| `ComMaxPlaytime` | 0 – 60,000 | 社区最长时长，均值 90.5 |
| `MfgAgeRec` | 0 – 25 | 出版商建议年龄。**0 = 未知**（1,325 行）。众数 12 |
| `ComAgeRec` | 2 – 21，**25.2% 空** | 社区投票建议年龄，浮点（如 `14.3667`） |

> `60000` 分钟 = 1,000 小时，是战棋/战役游戏的极端值或脏数据，做时长特征前先 winsorize。

### 2.6 收藏热度与关系

| 列 | 实测范围 | 语义 |
|---|---|---|
| `NumOwned` | 0 – 166,497 | 拥有人数，**最强的流行度代理变量** |
| `NumWant` | 0 – 2,031 | 想要（want in trade） |
| `NumWish` | 0 – 19,182 | 心愿单 |
| `NumAlternates` | 0 – 850 | 替代版本数 |
| `NumExpansions` | 0 – 525 | 扩展数（0 占 74.5%） |
| `NumImplementations` | 0 – 38 | 再实现数 |
| `IsReimplementation` | 0/1 | 11.7% 为 1 —— 「这游戏是旧游戏的重做」。**做机制原创性判断时是重要控制变量** |
| `Kickstarted` | 0/1 | 15.3% 为 1 |

### 2.7 待核实字段

| 列 | 实测 | 疑点 |
|---|---|---|
| `LanguageEase` | 1 – **1757**，均值 216，26.9% 空 | BGG 官方的 language dependence 投票是 **1–5 级**，而这列跑到 1757 且均值 216，**不是等级值**（更像投票数或某种混合编码）。作者说明未覆盖。**用之前务必回 BGG API 核对语义**，别当「语言依赖度」直接用 |
| `YearPublished` | **-3500** – 2021 | 负数是公元前的传统游戏（如古埃及塞尼特棋），不是脏数据。**但 193 行为 0 = 未知年份**，做「年份 → 机制演化」分析前先剔 0 |

---

## 3. `user_ratings.csv` —— 逐条原始评分（本仓库唯一的 L2 协同过滤数据）

**18,942,215 行 × 3 列**，全量扫描无缺失。

| 列 | 类型 | 实测 | 说明 |
|---|---|---|---|
| `BGGId` | int | 21,925 唯一 | 与 `games.csv` **完全对齐**，无孤儿 id |
| `Rating` | float | 0.0001 – 10.0 | 原始评分，**10,647 个不同取值** |
| `Username` | str | **411,375 唯一** | ⚠️ 有纯数字用户名（如 `123456`），pandas 会推成 int64 甚至溢出成 float。**必须 `dtype={"Username":"string"}`** |

实测事实（`_profiles/user_ratings_facts.json`，全量非抽样）：

- **稀疏度 0.21%**（18.94M / (411,375 × 21,925)），典型的协同过滤稀疏场景
- **整数评分占 82.8%**，非整数 17.2%（BGG 允许小数评分）
- 整数评分分布：`7` 最多（4,304,908）> `8`（3,689,065）> `6`（2,769,370）> `9`（1,772,299）> `10`（944,321）> `5` > `4` > `3` > `2` > `1`（53,076）
  → **强烈右偏**，均值 7.13，做回归时别假设正态
- **8 条评分 < 1**（最小 0.0001），BGG 官方评分区间是 1–10 —— 这 8 条是脏数据，建议直接剔除；无 > 10 的越界值
- 每用户评分数：中位 **12**，均值 46，p90 115，最大 6,493；**79,296 个用户（19.3%）只评过 1 款游戏**
  → 冷启动用户占比很高，做推荐评测时必须设最小交互数阈值，否则测试集被单次用户主导
- 每游戏评分数：中位 **125**，均值 864，最大 107,760，**最小 7**

> ### ⚠️ 两个「评分人数」不一致
> `user_ratings` 里每游戏最少只有 **7** 条评分，而 `games.NumUserRatings` 最小是 **30**。
>
> 交叉验证发现：`ratings_distribution.total_ratings` 的均值（863.9551）与 `user_ratings` 按游戏聚合的均值（863.96）**完全一致**，而 `games.NumUserRatings` 有 **13,961 / 21,925（64%）** 的游戏与之不同（且系统性偏高几十到几百）。
>
> **结论**：`user_ratings` + `ratings_distribution` 是同一次抓取的快照，`games.NumUserRatings` / `AvgRating` / `Rank:*` 来自另一个（更晚的）BGG 官方计数时点。
> **做法**：算「样本量加权」的指标时，两个来源**只能选一个**；要自洽就从 `user_ratings` 自己聚合，不要混用。

---

## 4. `ratings_distribution.csv` —— 评分直方图

**21,925 行 × 96 列** = `BGGId` + **94 个分桶** + `total_ratings`。

分桶列名就是评分值本身：`0.0`、`0.1`、`0.5`，然后 `1.0` → `10.0` 以 **0.1 步长**共 91 个桶。

实测性质：
- **94 个桶求和 == `total_ratings`，21,925 行全部精确成立**（无舍入误差）
- `total_ratings` 范围 7 – 107,760，均值 863.96
- 用分桶加权还原均分，与 `games.AvgRating` 的偏差：中位 **0.0044**，均值 0.0199，p90 0.052，最大 1.45；**96.2% 的游戏差距 < 0.1**
  → 直方图可信，残余偏差就是上面说的快照时差

**用途**：这是唯一能直接算**评分分布形状**的表 —— 双峰/长尾/极端分歧，比 `StdDev` 单个数字信息量大得多。想找「机制导致口碑撕裂」的证据就用它。

```python
dist = pd.read_csv(f"{RAW}/ratings_distribution.csv")
buckets = [c for c in dist.columns if c not in ("BGGId", "total_ratings")]
vals = np.array([float(c) for c in buckets])
w = dist[buckets].to_numpy()
mean_ = (w * vals).sum(1) / dist["total_ratings"]                       # 还原均分
skew_ = ((w * (vals - mean_[:, None])**3).sum(1) / dist["total_ratings"]) / \
        (((w * (vals - mean_[:, None])**2).sum(1) / dist["total_ratings"])**1.5)
```

---

## 5. 标签宽表：`mechanics` / `themes` / `subcategories`

三张都是 **一行一游戏 + 0/1 标签矩阵**，`BGGId` 在**第 0 列**，全表无非 0/1 脏值。

| 表 | 标签列数 | 每游戏标签数（均值/中位/最大） | 无标签游戏 |
|---|---|---|---|
| `mechanics.csv` | **157** | 3.105 / 3 / 20 | 1,084 |
| `themes.csv` | **217** | 1.477 / 1 / 12 | 4,410 |
| `subcategories.csv` | **10** | 0.539 / 0 / 4 | 11,892 |

### 5.1 机制流行度实测 Top 20（占 21,925 款的百分比）

| # | 机制 | 数量 | 占比 | # | 机制 | 数量 | 占比 |
|---|---|---|---|---|---|---|---|
| 1 | Dice Rolling | 6,486 | **29.58%** | 11 | Area Majority / Influence | 1,639 | 7.48% |
| 2 | Hand Management | 4,496 | **20.51%** | 12 | Cooperative Game | 1,572 | 7.17% |
| 3 | Set Collection | 2,959 | 13.50% | 13 | Betting and Bluffing | 1,548 | 7.06% |
| 4 | Variable Player Powers | 2,736 | 12.48% | 14 | Roll / Spin and Move | 1,371 | 6.25% |
| 5 | Hexagon Grid | 2,438 | 11.12% | 15 | Area Movement | 1,202 | 5.48% |
| 6 | Simulation | 2,134 | 9.73% | 16 | Deduction | 1,199 | 5.47% |
| 7 | Drafting | 2,015 | 9.19% | 17 | Simultaneous Action Selection | 1,184 | 5.40% |
| 8 | Tile Placement | 1,832 | 8.36% | 18 | Action Points | 1,183 | 5.40% |
| 9 | Modular Board | 1,716 | 7.83% | 19 | Auction/Bidding | 1,157 | 5.28% |
| 10 | Grid Movement | 1,643 | 7.49% | 20 | Take That | 1,142 | 5.21% |

> ### 📌 修正调研报告中的三个数字
> `../../boardgame-datasets-survey.md` 第 3.3 节引用文献称「每款游戏平均 6.35 个机制；Hand Management 38.4%、Dice Rolling 29.0%、Variable Player Powers 26.2%」。
>
> 本地全量实测（21,925 款）是：**平均 3.105 个机制**；Hand Management **20.51%**、Dice Rolling **29.58%**、Variable Player Powers **12.48%**。
>
> Dice Rolling 吻合，另两个差近一倍。最可能的原因是文献统计的是**已排名 Top-N 子集**（重策游戏机制标注更全、更偏 Hand Management），而本数据集含大量长尾游戏。**引用机制分布数字时务必带样本范围**，否则结论不可比。

### 5.2 主题 Top 15

Fantasy 12.32% · Science Fiction 7.64% · Fighting 7.61% · Economic 6.93% · Animals 6.23% · World War II 5.66% · Humor 5.60% · Adventure 5.37% · Movies/TV/Radio 4.87% · Medieval 4.80% · Ancient 3.36% · Horror 3.17% · Nautical 2.94% · Racing 2.84% · Trivia 2.68%

### 5.3 子类别（10 列，与 `games.csv` 的 `Cat:*` 不是一回事）

Card Game 29.56% · Miniatures 4.97% · Exploration 4.09% · Puzzle 3.08% · Print & Play 2.75% · Territory Building 2.34% · Educational 2.29% · Word Game 2.21% · Collectible Components 1.64% · Electronic 0.94%

> `subcategories.csv`（10 个细分标签）≠ `games.csv` 的 `Cat:*`（8 个 BGG 官方子域）。前者是 BGG 的 category 标签子集，后者是排行榜子域划分。**名字像但语义不同，别 join 混用。**

---

## 6. 实体宽表：`designers_reduced` / `artists_reduced` / `publishers_reduced`

> ### ⚠️ 布局陷阱：这三张表的 `BGGId` **不在第一列**
> | 表 | 总列数 | `BGGId` 位置 | 标签列数 |
> |---|---|---|---|
> | `designers_reduced.csv` | 1,594 | **第 1592 列（倒数第二）** | 1,593 |
> | `artists_reduced.csv` | 1,681 | **第 1679 列（倒数第二）** | 1,680 |
> | `publishers_reduced.csv` | 1,866 | **第 1864 列（倒数第二）** | 1,865 |
>
> 首列是实体名（如 `Karl-Heinz Schmiel`、`Hans im Glück`），最后一列是 `Low-Exp *` 标志位。
> `pd.read_csv(..., index_col=0)` 会**静默地把第一个设计师的名字当成索引**，不报错但全错。
> 正确写法：`df = pd.read_csv(path).set_index("BGGId")`。
>
> 而 `mechanics` / `themes` / `subcategories` 的 `BGGId` 在第 0 列 —— 同一个数据集里两种布局并存，逐表确认。

每游戏实体数：designers 均值 1.22（最多 16，599 款无设计师）· artists 均值 1.19（最多 **165**，5,997 款无美术）· publishers 均值 2.58（最多 126，仅 1 款无出版商）。

`Low-Exp Designer` / `Low-Exp Artist` / `Low-Exp Publisher`：表示「该游戏有作品数 ≤ 3 的长尾实体未单独建列」。
**因此不能用这些表统计实体的完整作品数分布** —— 长尾被折叠了，任何「设计师产量分布」的结论都会被截断。

---

## 7. 加载配方

```python
import pandas as pd, ast
RAW = "research/datasets/bgg-threnjen/raw"

games = pd.read_csv(f"{RAW}/games.csv", dtype={"Name": "string"})

# 1) 排名哨兵 -> NA
rank_cols = [c for c in games.columns if c.startswith("Rank:")]
games[rank_cols] = games[rank_cols].replace(len(games) + 1, pd.NA)

# 2) 「0 = 未知」的列统一置空
for col in ["MinPlayers", "MaxPlayers", "BestPlayers", "MfgAgeRec", "YearPublished"]:
    games.loc[games[col] == 0, col] = pd.NA

# 3) 人数上限哨兵
games.loc[games["MaxPlayers"] >= 99, "MaxPlayers"] = pd.NA

# 4) 复杂度只在有票时可信
games.loc[games["NumWeightVotes"] < 5, "GameWeight"] = pd.NA

# 5) 丢掉废列与重复列
games = games.drop(columns=["NumComments", "MfgPlaytime"])

# 6) GoodPlayers 还原成 list[int]
games["GoodPlayers"] = games["GoodPlayers"].fillna("[]").map(
    lambda s: [int(x) for x in ast.literal_eval(s)])
```

## 8. 作者原始文档的可疑之处

`raw/bgg_data_documentation.txt` 是作者自带的字段说明，与实测对照后有 4 处需要留意：

| 作者原文 | 实测情况 |
|---|---|
| `StdDev` = "Standard deviation of **Bayes Avg**" | BGG XML API 的 `stddev` 字段是**用户原始评分**的标准差，与 bayes 收缩值无关。作者标注很可能有误，倾向按「原始评分离散度」理解 |
| `NumWeightVotes` = "**? Unknown**" | 作者自己都标了问号。从与 `GameWeight` 的关系看应是复杂度投票数（BGG `numweights`），但**未经官方核实** |
| `LanguageEase` = "Language requirement" | 实测 1–1757、均值 216，不可能是 BGG 的 1–5 级语言依赖度。语义存疑，见 §2.7 |
| 字段名写作 `MfgPlayTime` | 实际列名是 `MfgPlaytime`（小写 t）。按文档拼写取列会 KeyError |

另外文档里 `DESIGNERS_REDUCED` / `PUBLISHERS_REDUCED` 的说明都误写成「various **subcategories** with binary flag」（复制粘贴残留），实际是设计师 / 出版商。

## 9. 引用与合规

- 许可 **CC BY-SA 3.0**：衍生数据集/发布物需署名原作者（Kaggle 用户 `threnjen`）并以相同许可共享。
- 底层数据版权属 BoardGameGeek，商用请先看 BGG 的 XML API 条款（2025-10 起需注册 token，见 `../../boardgame-datasets-survey.md` 第 1 节）。
- 复现下载：`powershell -ExecutionPolicy Bypass -File ../_scripts/download.ps1`
- 字段事实来源：`../_profiles/bgg-threnjen__*.json`（由 `_scripts/profile_csv.py` 全量扫描生成，非抽样）
