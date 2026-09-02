# 桌游数据集调研（面向「桌游机制 Agent」）

调研日期：2026-08-17

---

## 0. 结论速览

按用途分四层取数，**没有单一数据集能同时满足元数据 + 机制 + 规则文本**：

| 层 | 需求 | 首选 | 备选 |
|---|---|---|---|
| L1 元数据 + 评分 + 机制标签 | 冷启动、统计画像 | Kaggle `threnjen/board-games-database-from-boardgamegeek` | Kaggle `gabrio`（覆盖最广 ~94k）、IEEE DataPort 2021 快照 |
| L2 用户级评分/评论 | 协同过滤、口碑建模 | 同上（19M 评分 / 411k 用户）；`jvanelteren` BGG Reviews（~13M 带文本） | Recommend.Games 持续更新的 dump |
| L3 机制本体（taxonomy） | Agent 的机制词表与组合规则 | BGG `boardgamemechanic` 标签体系（源自 Engelstein & Shalev 百科） | 《Building Blocks of Tabletop Game Design》第 3 版（书，需购买） |
| L4 规则文本 / 可执行规则 | 生成、验证、模拟 | **Ludii**（1000+ 游戏，形式化 GDL，可直接跑）| AutoBG 的 2.2K 结构化 rulebook（未确认开放）|

**最省事的起步组合**：`threnjen` Kaggle 数据集（L1+L2）+ Ludii（L4）+ 自建机制词表（L3）。

---

## 1. ⚠️ 先看这个：BGG XML API 已不再匿名开放

**实测确认**（2026-08-17）：

```
GET https://boardgamegeek.com/xmlapi2/thing?id=224517&stats=1
→ HTTP 401 Unauthorized. See https://boardgamegeek.com/using_the_xml_api
```

时间线：
- 2025-04 BGG 宣布将引入注册与 Authorization 头
- 2025-06 token 注册开放
- 2025-07-02 官方政策页《Using the XML API》发布
- **2025-10 强制生效**，未带 token 的第三方工具直接挂掉

现状：
- 商用与非商用**都必须注册**，分不同 license 档位
- 请求需带 `Authorization: Bearer <BGG_APPLICATION_TOKEN>`
- 唯一豁免：登录状态下只下载自己的 collection
- **没有官方 GraphQL API**。网传的 GraphQL 是第三方代理 `tnaskali/bgg-api`，它自己也要求你先拿到 BGG token
- 网页端也在防爬：`boardgamegeek.com/browse/boardgamemechanic` 与 `using_the_xml_api` 对无头请求均返回 403

**行动项**：如果 Agent 需要实时/增量数据，**现在就去申请 application token**，这是关键路径上的外部依赖，别等到开发中期才发现。历史 Kaggle 快照不受影响，可以先用它们做原型。

---

## 2. L1/L2：元数据 + 评分数据集

### 2.1 Kaggle — `threnjen/board-games-database-from-boardgamegeek`（推荐主力）
- 规模：**22k 游戏 / 411k 用户 / 19M 条评分**
- 定位：EDA、建模、推荐系统
- 优势：唯一把「游戏属性」和「用户级评分」放在一起的主流公开集
- 注意：Kaggle 页面对无头抓取返回空内容，具体文件清单/许可证需登录查看

### 2.2 Kaggle — `gabrio/board-games-dataset`（覆盖最广）
- 规模：**~94,000 个游戏及扩展**
- 附带 R 语言爬虫包（GitHub 开源）
- 适合做全量元数据分析，不含用户级评分

### 2.3 Kaggle — `jvanelteren` BGG Reviews（文本评论）
- **~13M 条评论**（评分 + 可选文本），2019 年采集
- 配套 `games_detailed_info.csv`，字段包括：
  `Board Game Rank`、各子域排名（Abstract/Family/Party/Strategy/Thematic/War）、
  `average`、`averageweight`（复杂度）、`bayesaverage`（Geek Score）、
  `boardgamecategory`、`boardgamemechanic`
- **这是做「玩家口碑 → 机制偏好」映射的最佳文本源**

### 2.4 Kaggle — `mattadamhouser/ranked-board-game-data`
- Top 2000 游戏，含 mechanisms / themes / subdomains / **sequel 关系**
- 小而精，sequel 数据在别处少见

### 2.5 Kaggle — `mrpantherson/board-game-data`
- 20 列，字段清晰：Rank, URL, Game ID, Name, Min/Max players, Avg/Min/Max time,
  Year, Average rating, Geek rating, Num votes, Image URL, Age, BGG owners,
  Category, Designer, Mechanic, Weight
- 常见于教学 demo，覆盖偏窄（部分版本只有 Top 5000，有流行度偏差）

### 2.6 IEEE DataPort — BoardGameGeek Dataset on Board Games
- 2021-02 快照，`.xlsx` 格式，需登录
- 只含**已排名**游戏（BGG 要求 ≥30 票才进排名），排除了 unranked
- 引用：Dilini Samarasinghe, doi: `10.21227/9g61-bs59`
- 适合做可引用的学术基线，不适合做生产数据

### 2.7 持续更新的爬虫生态
- **`recommend-games/board-game-scraper`** —— Recommend.Games 官方爬虫，PyPI 上有 `board-game-scraper` 包。作者明确指出「现有 BGG 数据集多是一次性快照、无人维护」，该项目需要持续新鲜数据，dump 发布在其 BGG guild
- **`albert-marrero/bgg-data`** —— Scrapy 实现，含 BGG rankings 与 hotness 的数据字典
- **`lorriman/bggdatadumper`** —— 泛化遍历 XML 标签/属性转 CSV，最大限度保留原始信息，自带 2 req/s 限速
- **Apify BoardGameGeek Scraper** —— 托管方案，输出 categories/mechanics/designers/publishers，支持 CSV/Excel/JSON/XML
- **Dinesh Vatvani 的爬虫** —— 专门补齐了原版爬虫漏掉的 mechanics/categories/designers，产出 **76,597 游戏 + 13,675 扩展**

> ⚠️ 上述爬虫大多写于 token 强制之前，需要改造以支持 Bearer token。

---

## 3. L3：机制本体（对机制 Agent 最关键）

### 3.1 BGG 机制体系的来源
BGG 现行 mechanism 列表**直接源自学术参考书**：
《Building Blocks of Tabletop Game Design: An Encyclopedia of Mechanisms》
—— Geoffrey Engelstein & Isaac Shalev，Routledge/CRC Press。

- 第 1 版：约 200 个机制
- 第 2 版：ISBN 9781032015811（精装 9781032015835），约 2022-03，"hundreds of mechanisms"
- **第 3 版：ISBN 9781032985114**，机制更多、条目更新、含彩图

Engelstein 是 NYU Game Center 桌游设计兼职教授、TTGDA 联合创始人。

### 3.2 分类编码方案
机制按三字母类别码分组，条目编号形如 `<CAT>-<NN>`：

| 码 | 类别 | 码 | 类别 |
|---|---|---|---|
| STR | Game Structure | ECO | Economics |
| TRN | Turn Order and Structure | AUC | Auctions |
| ACT | Actions | WPL | Worker Placement |
| RES | Resolution | MOV | Movement |
| VIC | Game End and Victory | ARC | Area Control |
| UNC | Uncertainty | SET | Set Collection |
| | | CAR | Card Mechanisms |

示例（Actions 类）：
`ACT-01 Action Points`、`ACT-02 Action Drafting`、`ACT-03 Action Retrieval`、
`ACT-04 Action/Event`、`ACT-05 Command Cards`、`ACT-06 Action Queue`、
`ACT-07 Shared Action Queue`、`ACT-08 Follow`、`ACT-09 Order Counters`、`ACT-10 Rondel`

**这套「类别码 + 编号」结构非常适合直接做 Agent 的机制本体 schema**——类别可作一级 slot，编号条目作可枚举值，天然支持「按类别补全设计空缺」的推理。

### 3.3 规模与分布（数据来自研究文献，未逐一核实）
- 机制约 **192** 个，类别约 **85** 个
- 每款游戏平均 **~6.35** 个机制
- 高频机制：Hand Management **38.4%**、Dice Rolling **29.0%**、Variable Player Powers **26.2%**

> 注：BGG 官方 browse 页对无头请求返回 403，上述数量我未能直接核实。该 taxonomy 在持续扩充，**准确当前数字只能以 BGG browse 页为准**。历史上曾只有 51 个机制（无 engine building / dexterity），可见增长幅度。

### 3.4 参考清单
- BGG browse 页：`boardgamegeek.com/browse/boardgamemechanic`（权威实时列表）
- BGG 论坛「List of Mechanisms with Category」thread 2277686（带类别码全量枚举）
- Encyclopedia of Mechanisms Discussion Group（guild 3623，新机制讨论区）
- Board Game Design Lab 的 Mechanisms Master List（每机制含定义与示例游戏）
- BGG geeklist 298665「Board Game Mechanics that are not on BGG yet」（**未收录机制，做前瞻设计有用**）

---

## 4. L4：规则文本与可执行规则

### 4.1 Ludii（形式化规则首选）
- ERC 资助的 Digital Ludeme Project 产物，GitHub: `Ludeme/Ludii`
- **1000+ 可玩桌游与益智游戏**，是 AI 研究领域最大的可执行游戏库之一
- 采用 **ludemic GDL**：语言由 "ludemes"（关键词）组成，与源码 1:1 映射，游戏描述可自动实例化回代码编译
- v1.1.17 含 **547 个 ludeme**；单个游戏描述从几十个（井字棋）到数千个（大局将棋）
- 覆盖类型极广：确定/随机/隐藏信息、棋牌骰砖、无棋盘（多米诺）、叠放（Lasca）、同时行动、图游戏（点格棋）、多人/团队、单人解谜；**1–16 人**
- 关键优势：**ludeme 抽象足够紧凑，规则能塞进现代 LLM 上下文**
- 下载：Ludii Language Reference PDF、User Guide、Game Logic Guide、DLP Database Guide
- 配套：Ludii Example AI (Java)、Ludii Python AI、AI Competition
- 另有 **Ludii Games Database**（B2FIND 上的数据集）：记录公元前 3500 年至今全球游戏的规则 + 考古/历史/人类学证据，含地理位置、时期、史料、玩家年龄性别社会地位等背景

### 4.2 AutoBG（与你的场景最贴近）
arXiv **2606.01976**（cs.HC，2026-06-01 提交，v2 2026-06-13，一作 Zizhen Li）

四模块「critic-driven iterative refinement」架构：
1. **BG-Ideator** —— 多轮对话把模糊概念转成结构化设计草案
2. **BG-Realizer** —— 草案 → 完整规则书，与 critic 循环改写
3. **BG-Critic** —— 找设计缺陷，**门控每次修订，只有验证过的改进才被接受**（Verifier-Gated Iteration，含 principled stopping）
4. **BG-Persona** —— 基于 **150 个真实玩家画像**产出个性化试玩反馈

数据集：
- **2.2K 结构化 rulebook**
- **180K 质量过滤后的真实玩家评论**（评论用 game metadata 增广：type、categories、**core/supporting mechanics**、complexity）
- 每个模块派生了各自的任务训练数据

评估：207 个 held-out 游戏 + 30 人用户研究；称显著超过 SOTA baseline（如 GPT-5.4），规则书质量接近已出版游戏；用户反馈是降低「白纸焦虑」+ 暴露隐藏设计缺陷。

> ⚠️ **abstract 页未见任何数据集/代码发布链接**，也没有 data availability 声明。需查全文附录或直接联系作者。「core/supporting mechanics」这个区分对机制 Agent 很有借鉴价值。

### 4.3 GAVEL：Generating Games via Evolution & LLMs
arXiv 2407.09388
- 进化算法 + 微调 LLM，在 **Ludii GDL** 中生成新游戏
- 微调 **CodeLlama-13b** + **MAP-Elites** 来变异/重组游戏机制
- 训练集来自 **1000+ 桌游**
- 这是「机制组合 → 新游戏」的现成范式，**强烈建议精读**

### 4.4 其他相关工作
- **Boardwalk**（arXiv 2508.16447）—— 测试 LLM 能否从自然语言规则实现数字版桌游，用 Claude / DeepSeek / ChatGPT 编码 12 款流行与冷门游戏，含 free-form 与 General Game Playing API 两种模式
- **Grammar-based Game Description Generation**（arXiv 2407.17404）—— 指出关键数据瓶颈：**Ludii 相关文本在 LLM 预训练语料中极稀缺**，而 BNF 语法很常见，故注入最小 BNF 语法帮模型捕捉 GDL 结构
- **Grammar and Gameplay-aligned RL for Game Description Generation**（arXiv 2503.15783）
- **LLM Game Rule Understanding through OOD Fine-Tuning**（AAAI AIIDE）—— 用自定义 GDL 定义 Solitaire 变体，程序化生成文字描述 + 进程问答 + 答案解释，切分 in-distribution（微调）/ out-of-distribution（评测）
- **Large Language Models and Games: A Survey and Roadmap**（arXiv 2402.18659）—— 领域综述，用于定位
- **MeepleLM: A Virtual Playtester Simulating Diverse Subjective Experiences**（arXiv 2601.07251）—— 虚拟试玩员，未细读
- **Auto-BoardGame**（GitHub `canunj/Auto-BoardGame`）—— AutoBG 的开源前身，LLM 生成桌游概念（标题+描述）。静态数据集**需申请**，来源 BGG，**非商用许可**
- **tasksource/Boardgame-QA**（HuggingFace，arXiv 2306.07934）—— CC-BY-4.0，parquet，10K–100K 行。**注意：这是桌游风格的逻辑推理 benchmark，不是真实规则书或 BGG 元数据**

### 4.5 规则书文本的现实困境
**没有开放的规则书 PDF 语料库**——规则书受出版商版权保护。如需规则文本用于 RAG/微调，只能自建：
- CC 许可的 print-and-play 游戏
- 公有领域传统游戏
- BGG XML API v2 的 description 字段（简介级，非完整规则）
- 也有人做 RAG-over-rulebook 的项目（如 "Board Game Guru"），让用户自行上传规则再检索

HuggingFace 上**没有**权威的 BGG 全量抓取，主流仍在 Kaggle。

---

## 5. 关键字段语义（容易踩坑）

| 字段 | 含义 | 注意 |
|---|---|---|
| `average` | 用户评分算术均值（1–10） | 小样本游戏会虚高 |
| `bayesaverage` | Geek Score，贝叶斯收缩后评分 | **做排序/回归目标用这个** |
| `Board Game Rank` | BGG 官方排名 | **不能由 average 直接推导**，BGG 用内部公式 |
| `averageweight` | 复杂度（1–5） | 机制 Agent 的重要控制变量 |
| `boardgamemechanic` | 机制标签，**多值** | 需 explode / one-hot |
| `boardgamecategory` | 主题分类，**多值** | 与 mechanic 正交，别混用 |
| 子域排名 | Abstract / Family / Party / Strategy / Thematic / War | 做分层评估很有用 |

**多值字段处理**：一款游戏有多个 mechanics 和 categories，分析前必须 split/explode（pandas `explode` 或 OpenRefine）。

---

## 6. 已失效 / 慎用的数据源

| 源 | 状态 | 说明 |
|---|---|---|
| **Board Game Atlas** | ❌ **已关闭**（2023-08-23） | 曾提供 Play Logs / User Data / Game Lists / Prices API。`pybga` 等 wrapper 已成死代码 |
| **BoardGameArena** | ⚠️ **无公开 API，禁止抓取** | 官方明确表示第三方数据访问违反其 data policy，涉及玩家隐私。虽有内部端点（hall-of-fame ranking → player IDs、gamestats → table IDs、archive logs → 逐步 replay），但账号有 replay 配额，绕过需多开账号，**明确违反 ToS** |
| **BGG XML API 匿名访问** | ❌ 2025-10 起失效 | 见第 1 节 |
| 各类一次性 Kaggle 快照 | ⚠️ 时间点数据 | 评分随时间变化，做时序分析要注意采集日期 |

> BGA 的逐步 replay log 是**唯一大规模的真实对局过程数据**，对机制模拟极有价值，但**合规上拿不到**。如果确实需要对局级数据，正规路径是 BGG 的 plays 记录（粒度粗，只有「玩了几次」）或自建模拟器（Ludii 可直接跑）。

---

## 7. 采样偏差提醒

- BGG 用户行为**不代表全体桌游玩家**——偏重欧美、偏重中重度策略游戏，party game 与儿童游戏被系统性低估
- ≥30 票才进排名，长尾/小众/非英语游戏大量缺失
- 部分 Kaggle dump 只含 Top 5000，流行度偏差严重
- **中文/亚洲桌游在所有这些数据集中覆盖都很差**，如果平台面向中文市场需要单独补数据

---

## 8. 针对「机制 Agent」的落地建议

**阶段一 · 本体构建（不依赖外部 API）**
1. 从 BGG 论坛 thread 2277686 抓取「机制 + 类别码」全量列表，建立机制词表
2. 用 Board Game Design Lab 的 Master List 补每个机制的定义与示例游戏
3. 参考《Building Blocks》第 3 版校准定义边界（需购书）
4. 引入 AutoBG 的 **core / supporting mechanics** 区分——不是所有机制权重相等

**阶段二 · 统计先验（用历史快照）**
5. 用 `threnjen` 数据集算机制共现矩阵、机制→评分/复杂度的条件分布
6. 用 `jvanelteren` 评论文本做「机制 → 玩家情绪」映射，为 Critic 模块提供依据
7. 建立机制组合的「可行性先验」：哪些组合从未共现，哪些是高分组合

**阶段三 · 可执行验证**
8. 接入 **Ludii**，把 Agent 产出的机制组合映射到 ludeme 子集，跑自动对局验证可玩性
9. 复现 **GAVEL** 的 MAP-Elites + 微调 LLM 路线做机制变异/重组
10. 用 GAVEL 的思路做质量-多样性搜索，而不是单点生成

**阶段四 · 实时数据（需前置准备）**
11. **尽早申请 BGG application token**（关键路径），改造爬虫支持 Bearer header
12. 或直接跟 Recommend.Games 项目取持续更新的 dump，省去自建维护成本

**风险登记**
- BGG token 审批时长未知 → 现在就申请
- AutoBG 数据集可能不开放 → 准备自建 rulebook 语料的 plan B
- 规则书版权 → 生成而非复制，避免训练数据污染
- Ludii 是 Java 生态 → 需要 JVM 互操作方案（官方有 Python AI 接口）

---

## 9. 链接汇总

**数据集**
- [Kaggle: threnjen/board-games-database-from-boardgamegeek](https://www.kaggle.com/datasets/threnjen/board-games-database-from-boardgamegeek)
- [Kaggle: gabrio/board-games-dataset](https://www.kaggle.com/datasets/gabrio/board-games-dataset)
- [Kaggle: mattadamhouser/ranked-board-game-data-from-boardgamegeek](https://www.kaggle.com/datasets/mattadamhouser/ranked-board-game-data-from-boardgamegeek)
- [Kaggle: andrewmvd/board-games](https://www.kaggle.com/datasets/andrewmvd/board-games)
- [Kaggle: mrpantherson/board-game-data](https://www.kaggle.com/datasets/mrpantherson/board-game-data)
- [Kaggle: sujaykapadnis/board-games](https://www.kaggle.com/datasets/sujaykapadnis/board-games)
- [IEEE DataPort: BoardGameGeek Dataset on Board Games](https://ieee-dataport.org/open-access/boardgamegeek-dataset-board-games)
- [HuggingFace: tasksource/Boardgame-QA](https://huggingface.co/datasets/tasksource/Boardgame-QA)
- [B2FIND: Ludii Games Database](https://b2find.eudat.eu/dataset/2fbdee44-e084-560e-81f1-cc5931c1874a)

**API / 爬虫**
- [BGG XML API2 Wiki](https://boardgamegeek.com/wiki/page/BGG_XML_API2)
- [Using the XML API（政策页，必读）](https://boardgamegeek.com/using_the_xml_api)
- [XML API: Read this for uninterrupted access](https://boardgamegeek.com/thread/3539581/xml-api-read-this-for-uninterrupted-access)
- [recommend-games/board-game-scraper](https://github.com/recommend-games/board-game-scraper)
- [albert-marrero/bgg-data](https://github.com/albert-marrero/bgg-data)
- [lorriman/bggdatadumper](https://github.com/lorriman/bggdatadumper)
- [tnaskali/bgg-api（GraphQL 代理）](https://github.com/tnaskali/bgg-api)
- [Apify BoardGameGeek Scraper](https://apify.com/parseforge/boardgamegeek-scraper)

**机制本体**
- [BGG 机制浏览页](https://boardgamegeek.com/browse/boardgamemechanic)
- [List of Mechanisms with Category](https://boardgamegeek.com/thread/2277686/list-mechanisms-category)
- [Encyclopedia of Mechanisms Discussion Group](https://boardgamegeek.com/guild/3623)
- [Board Game Design Lab: Mechanisms Master List](https://boardgamedesignlab.com/mechanism-master-list/)
- [Board Game Mechanics that are not on BGG yet](https://boardgamegeek.com/geeklist/298665/board-game-mechanics-that-are-not-on-bgg-yet)
- [Routledge: Building Blocks of Tabletop Game Design](https://www.routledge.com/Building-Blocks-of-Tabletop-Game-Design-An-Encyclopedia-of-Mechanisms/Engelstein-Shalev/p/book/9781032015811)

**规则 / 论文**
- [Ludii GitHub](https://github.com/Ludeme/Ludii)
- [Ludii Language Reference PDF](https://ludii.games/downloads/LudiiLanguageReference.pdf)
- [An Overview of the Ludii General Game System (arXiv 1907.00240)](https://arxiv.org/pdf/1907.00240)
- [The Ludii GDL is Universal (arXiv 2205.00451)](https://arxiv.org/pdf/2205.00451)
- [AutoBG (arXiv 2606.01976)](https://arxiv.org/abs/2606.01976)
- [GAVEL: Generating Games via Evolution & LLMs (arXiv 2407.09388)](https://www.emergentmind.com/papers/2407.09388)
- [Boardwalk (arXiv 2508.16447)](https://arxiv.org/abs/2508.16447)
- [Grammar-based Game Description Generation (arXiv 2407.17404)](https://arxiv.org/html/2407.17404v1)
- [LLMs and Games: A Survey and Roadmap (arXiv 2402.18659)](https://arxiv.org/html/2402.18659v5)
- [canunj/Auto-BoardGame](https://github.com/canunj/Auto-BoardGame)
- [Dinesh Vatvani: BGG Analysis](https://dvatvani.github.io/BGG-Analysis-Part-1.html)
