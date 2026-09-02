# 桌游数据集本地仓库（带评分属性的全部公开数据集）

对应调研报告：[`../boardgame-datasets-survey.md`](../boardgame-datasets-survey.md)
建立日期：2026-08-17 · 全部数据于当日从 Kaggle 匿名下载 · 总计 **3.02 GB / 7 个数据集 / 26 个数据文件**

> **一句话**：调研报告里所有「具有评分属性」的公开数据集都已落到本地，每个数据集配一份
> `DATASET.md` 逐字段注释，所有数字均来自**本地全量扫描实测**（非抽样、非引用 Kaggle 页面宣称值）。

---

## 1. 评分属性对照表（回答「哪些数据集有评分」）

| 数据集 | 游戏数 | 算术均分 | **Geek 贝叶斯分** | 综合排名 | 子域排名 | 评分离散度 | 复杂度 | **用户级逐条评分** | 文本评论 |
|---|---|---|---|---|---|---|---|---|---|
| **bgg-threnjen** (2021) | 21,925 | ✅ `AvgRating` | ✅ `BayesAvgRating` | ✅ | ✅ 9 个 | ✅ `StdDev` | ✅ | ✅ **18,942,215 条** | ❌ |
| **bgg-reviews-jvanelteren** (2025) | 27,780 | ✅ `average` | ✅ `bayesaverage` | ✅ | ✅ 9 个 | ✅ `stddev` | ✅ | ✅ **26,200,012 条** | ✅ **4,215,806 条** |
| **bgg-gabrio** (2017) | 90,400 | ✅ `stats.average` | ✅ `stats.bayesaverage` | ✅ | ✅ 8 个 | ✅ | ✅ | ❌ | ❌ |
| **bgg-ranked-mattadamhouser** (2023) | 2,000 | ✅ `avg_rating` | ✅ `geek_rating` | ✅ | ❌（只有 8 个子域**二值标签**，无名次） | ❌ | ✅ | ❌ | ❌ |
| **bgg-mrpantherson** (2017–18 ×3) | 4,999 ×3 | ✅ `avg_rating` | ✅ `geek_rating` | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **bgg-andrewmvd** (2021) | 20,343 | ✅ `Rating Average` | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **bgg-sujaykapadnis** (2017) | 10,532 | ✅ `average_rating` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**评分总量**：用户级逐条评分共 **45.1M 条**（threnjen 18.9M + jvanelteren 26.2M，两者时点不同、有重叠）。

---

## 2. 目录结构

```
research/datasets/
├── README.md                         ← 本文件
├── _scripts/                         ← 全部可复现执行
│   ├── download.ps1                    Kaggle 匿名下载（无需 token），支持 -Only / -Force
│   ├── fetch_kaggle_meta.ps1           抓许可证/更新时间/官方描述
│   ├── profile_csv.py                  纯标准库 CSV 剖析器（列类型/空值/区间/样例）
│   ├── digest_wide.py                  宽表（0/1 标签矩阵）摘要 + 标签流行度
│   ├── show_profile.py                 把剖析 JSON 压成紧凑表
│   ├── check_user_ratings.py           19M 行全量事实核查
│   └── check_reviews.py                26M 行全量事实核查
├── _profiles/                        ← 上述脚本产出的机器可读事实（写文档的证据来源）
├── bgg-threnjen/          DATASET.md + raw/  (10 文件, 642 MB)
├── bgg-reviews-jvanelteren/ DATASET.md + raw/  (5 文件, 2,286 MB)
├── bgg-gabrio/            DATASET.md + raw/  (SQLite, 140 MB)
├── bgg-ranked-mattadamhouser/ DATASET.md + raw/  (5 文件, 1.4 MB)
├── bgg-mrpantherson/      DATASET.md + raw/  (3 文件, 4.5 MB)
├── bgg-andrewmvd/         DATASET.md + raw/  (1 文件, 2.3 MB)
└── bgg-sujaykapadnis/     DATASET.md + raw/  (1 文件, 15.8 MB)
```

复现下载（**不需要 Kaggle 账号或 kaggle.json**，实测匿名可下）：

```powershell
powershell -ExecutionPolicy Bypass -File _scripts\download.ps1
powershell -ExecutionPolicy Bypass -File _scripts\download.ps1 -Only bgg-threnjen      # 单个
powershell -ExecutionPolicy Bypass -File _scripts\download.ps1 -IncludeHistoricalReviews  # 加 2.9GB 历史评论快照
```

重新生成全部剖析事实：

```powershell
python _scripts\profile_csv.py            # 所有 csv
python _scripts\digest_wide.py --all      # 宽表标签统计
python _scripts\check_user_ratings.py     # 19M 行，约 1 分钟
python _scripts\check_reviews.py          # 26M 行，约 3 分钟
```

---

## 3. 该用哪一个？

| 你要做的事 | 用 | 理由 |
|---|---|---|
| **协同过滤 / 推荐系统** | `bgg-threnjen/raw/user_ratings.csv` | 411,375 用户 × 21,925 游戏 × 18.9M 评分，唯一带完整用户 id 的规范化表 |
| **更大的评分矩阵 + 文本** | `bgg-reviews-jvanelteren/raw/bgg-26m-reviews.csv` | 555,482 用户 / 26.2M 评分，其中 4.2M 带文本 |
| **最新、最干净的游戏元数据** | `bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv` | 2025 快照、**原始描述全文**、192 机制词表、子域排名用真 NaN |
| **机制 ↔ 评分 关联分析** | `bgg-threnjen`（games + mechanics 按 `BGGId` join） | 157 机制 0/1 矩阵 + 聚合评分，开箱即用 |
| **要原始英文描述做 RAG/微调** | `games_detailed_info2025.csv` 或 `bgg-gabrio` | ⚠️ threnjen 的 `Description` 已被词干化，**不可用作自然语言** |
| **覆盖面最广（含 13,712 个扩展）** | `bgg-gabrio`（SQLite 90,400 行） | 唯一含扩展、唯一保留 BGG 原始投票字段 |
| **续作/机制传承谱系** | `bgg-ranked-mattadamhouser/reimplementations_2023.csv` | 470 条 parent→child 关系 + 迭代代数，别处没有 |
| **评分随时间漂移** | `bgg-mrpantherson`（3 个快照） | 同 schema 多时点，见其 DATASET.md §3 |
| **快速原型 / 教学 demo** | `bgg-andrewmvd`（单文件 2.3 MB） | ⚠️ 必须 `sep=";", decimal=","` |
| ~~交叉验证 gabrio~~ | ❌ 不要用 `bgg-sujaykapadnis` | 实测是 gabrio 的严格子集，评分逐条相同，非独立来源 |

---

## 4. 跨数据集整合

### 4.1 主键是通的

所有数据集都用 **BGG 官方游戏 id**（列名各异：`BGGId` / `id` / `ID` / `game_id` / `game.id`），可直接 join。实测交集：

| | threnjen<br>2021 | detailed<br>2025 | matt<br>2023 | andrewmvd<br>2021 | mrpanth<br>2018 | gabrio<br>2017 |
|---|---|---|---|---|---|---|
| **threnjen 2021** (21,925) | — | **21,497** | 1,902 | 20,246 | 4,998 | 17,384 |
| **detailed 2025** (27,780) | 21,497 | — | 1,996 | 20,224 | 4,989 | 18,078 |
| **matt 2023** (2,000) | 1,902 | 1,996 | — | 1,842 | 1,373 | 1,349 |
| **andrewmvd 2021** (20,327) | 20,246 | 20,224 | 1,842 | — | 4,994 | 16,855 |
| **mrpanth 2018** (4,999) | 4,998 | 4,989 | 1,373 | 4,994 | — | 4,868 |
| **gabrio 2017** (90,400) | 17,384 | 18,078 | 1,349 | 16,855 | 4,868 | — |

threnjen(2021) 的游戏 **98.0%** 能在 2025 表里找到，2025 表另有 6,283 款是 2021 后新增/新进榜的。

⚠️ 类型注意：`bgg-gabrio` 的 `game.id` 存成 **TEXT**，`bgg-andrewmvd` 有 **16 行 `ID` 为空**。

### 4.2 ⚠️ 机制名**不通** —— 跨快照 join 的最大陷阱

BGG 机制词表在这几年被大幅重构，**按名称字符串直接匹配会静默丢数据**：

| 快照 | 数据集 | 机制数 |
|---|---|---|
| 2017-06 | gabrio | **51** |
| 2018-06 | mrpantherson / sujaykapadnis | 52 |
| 2021-12 | threnjen | **157** |
| 2023-08 | mattadamhouser | 188 |
| 2025-02 | games_detailed_info2025 | **192** |

- 2017 的 51 个与 2021 的 157 个**只有 36 个同名** —— 15 个被改名（`Area Control / Area Influence` → `Area Majority / Influence`、`Press Your Luck` → `Push Your Luck` …，完整映射见 [`bgg-gabrio/DATASET.md`](bgg-gabrio/DATASET.md) §4）
- 2023 新增 37 个，主要是把拍卖与回合顺序**拆成子类型族**：`Auction: Dutch / English / Sealed Bid / Once Around …`、`Turn Order: Progressive / Random / Pass Order …`
  → 这正好对应 Engelstein & Shalev 百科的 **AUC / TRN 分类码**结构，是 BGG 采纳该书体系的直接证据
- 2025 又出现**空格差异**：`Auction/Bidding`(2023) → `Auction / Bidding`(2025)，字符串比较会当成两个机制

**做法**：统一到 2025 的 192 个词表，维护一张改名映射表；或只在同一快照内部做机制分析。

---

## 5. 对调研报告的实测修正

本地数据推翻/修正了 `../boardgame-datasets-survey.md` 中的几处数字：

| 报告原文 | 实测 | 影响 |
|---|---|---|
| jvanelteren「**~13M 条评论**，2019 采集」 | **26,200,012 条，2025-02** | 规模翻倍 |
| 该数据集是「**带文本**的评论」 | **仅 16.09% 带文本**（4.22M 条），83.91% 是纯评分 | ⚠️ 文本语料规模差 3 倍以上，影响 L2 语料规划 |
| 「每款游戏平均 **6.35** 个机制」 | 全量 **3.11**（threnjen）/ **3.20**（2025）；Top-2000 才是 **5.70** | 文献统计的是头部子集 |
| 「Hand Management **38.4%**」 | 全量 **20.5%**；Top-2000 为 **35.6%** | 同上，引用时必须注明样本范围 |
| 「Dice Rolling 29.0%」 | **29.58%** ✅ | 吻合 |
| 「机制约 **192** 个」 | ✅ 2025 词表实测 **192** | 完全吻合 |
| 「历史上曾只有 **51** 个机制」 | ✅ gabrio 2017 实测 **51** | 完全吻合 |
| gabrio「~94,000 个游戏」 | **90,400**（含 13,712 扩展） | 小幅偏差 |
| threnjen「22k 游戏 / 411k 用户 / 19M 评分」 | **21,925 / 411,375 / 18,942,215** ✅ | 基本吻合 |

> 报告第 1 节关于 **BGG XML API 自 2025-10 起强制 token** 的结论不受影响 —— 本地这批全是 Kaggle 历史快照，
> **不依赖 BGG API**，可以直接用于原型开发。需要实时数据时仍需申请 application token。

---

## 6. 全数据集通用坑位清单

写代码前扫一眼，这些都是实测踩到的：

1. **哨兵值伪装成数值** —— threnjen 的 `Rank:*` 用 `21926`（=行数+1）表示未排名；gabrio 的 `bayesaverage` 用 `0`；多处 `MaxPlayers` 用 `99`/`999`；`weight` / `MfgAgeRec` / `MinPlayers` 用 `0` 表示未知。**不清洗会让均值/回归全错**。
2. **重复列** —— threnjen `MfgPlaytime` ≡ `ComMaxPlaytime`（21,925/21,925 行相同）；mattadamhouser `avg_time` ≡ `max_time`（2,000/2,000）；sujaykapadnis `playing_time` ≡ `max_playtime`（10,532/10,532）。
3. **废列** —— threnjen `NumComments` 全 0；2025 表 `median` 全 0；mattadamhouser `expansion` 全 0。
4. **主键位置不固定** —— threnjen 的 `*_reduced.csv` 里 `BGGId` 在**倒数第二列**；mattadamhouser 的 `themes_2023.csv` 首列是**无名索引列**。`index_col=0` 会静默出错。
5. **编码混杂** —— mrpantherson 三个文件里两个是 **cp1252**；其余基本是 UTF-8-BOM（标准库读需 `encoding="utf-8-sig"`）。
6. **欧洲数字格式** —— andrewmvd 是 `;` 分隔 + `,` 小数点，忘了会让评分列静默变成字符串。
7. **纯数字用户名** —— threnjen `Username`、jvanelteren `user` 里有形如 `123456` 的用户名，pandas 会推成数值甚至溢出，必须 `dtype="string"`。
8. **多值字段两种格式** —— gabrio/andrewmvd/sujaykapadnis 是**逗号分隔字符串**；threnjen `GoodPlayers` 与 2025 表的属性列是**字符串化的 Python 列表**（单引号，`json.loads` 会失败，要用 `ast.literal_eval`）。
9. **文件按游戏排序** —— `bgg-26m-reviews.csv` 前 300 万行只有 60 款游戏，`nrows=` 抽样严重有偏。
10. **截断样本** —— mattadamhouser（Top-2000，评分下界 6.38）与 mrpantherson（Top-5000，下界 5.78）存在 range restriction，不能用于估计总体分布。
11. **同一指标两个口径** —— threnjen 的 `games.NumUserRatings` 与 `user_ratings` 聚合结果对 64% 的游戏不一致（不同抓取时点），**不要混用**。

---

## 7. 许可一览（发布前必看）

| 数据集 | 许可 | 可商用 | 义务 |
|---|---|---|---|
| bgg-ranked-mattadamhouser | **CC0** | ✅ | 无 |
| bgg-mrpantherson | **CC0** | ✅ | 无 |
| bgg-andrewmvd | **CC BY 4.0** | ✅ | 署名 |
| bgg-threnjen | **CC BY-SA 3.0** | ✅ | 署名 + **相同方式共享**（衍生数据集也必须同许可） |
| bgg-gabrio | Other（作者自定） | ⚠️ 需确认 | 回原页面/上游 R 包确认 |
| bgg-sujaykapadnis | Other（作者自定） | ⚠️ 需确认 | 同上 |
| bgg-reviews-jvanelteren | Other（作者自定） | ⚠️ 需确认 | **本地许可最不明确的一个**；且评论文本著作权属各 BGG 用户 |

底层数据版权均归 BoardGameGeek。大规模再分发或商用前，建议同时查看 BGG 的
[Using the XML API](https://boardgamegeek.com/using_the_xml_api) 条款。
