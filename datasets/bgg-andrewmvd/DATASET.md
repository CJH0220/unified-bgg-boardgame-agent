# bgg-andrewmvd — Board Games（2021-02 全量已排名游戏）

> **本地路径** `research/datasets/bgg-andrewmvd/raw/bgg_dataset.csv`（2.3 MB）
> **来源** [kaggle.com/datasets/andrewmvd/board-games](https://www.kaggle.com/datasets/andrewmvd/board-games)
> **许可** **CC BY 4.0**（署名即可，商用友好）
> **快照** 2021-02（页面自述采集时间）
> **本仓库定位** 轻量级 L1 —— 20,343 款已排名游戏，单文件，字段干净，适合快速原型

## 0. ⚠️ 读这个文件之前必看

这份 csv 用的是**欧洲格式**，用默认参数读会得到一堆错误：

| 陷阱 | 后果 | 解法 |
|---|---|---|
| 分隔符是 **`;`** 不是 `,` | 整个文件被读成 1 列 | `sep=";"` |
| 小数点是 **`,`** 不是 `.` | `Rating Average` = `"8,79"` 被读成**字符串**，静默变成类别特征 | `decimal=","` |

只影响 `Rating Average` 与 `Complexity Average` 两列（其余数值列是整数，没有小数点）。
**这是本仓库里最容易踩、也最容易不被发现的坑** —— 不会报错，只会让评分列变成 object dtype。

```python
df = pd.read_csv("raw/bgg_dataset.csv", sep=";", decimal=",")
```

## 1. Schema（14 列，20,343 行）

| 列 | 类型 | 实测 | 说明 |
|---|---|---|---|
| `ID` | int | 1 – 331,787，**16 行为空** | BGG 游戏 id。⚠️ 有 16 款游戏缺 id（如 `Ace of Aces: Jet Eagles`、`Die Erben von Hoax`），**这 16 行无法与任何其它数据集 join**，建议直接剔除 |
| `Name` | str | 19,975 唯一 | 2 行为空 |
| `Year Published` | int | **-3500** – 2022 | 负数为公元前游戏 |
| `Min Players` / `Max Players` | int | 0–10 / 0–**999** | 0 = 未知，999 = 人数不限（哨兵） |
| `Play Time` | int | 0 – **60,000** | 分钟，极值需 winsorize |
| `Min Age` | int | 0 – 25 | 0 = 未知 |
| ⭐ `Users Rated` | int | **30** – 102,214 | 最小 30 → 与 BGG 排名门槛一致 |
| ⭐ `Rating Average` | float | **1.05 – 9.58**，均值 6.403 | 算术均分。**只保留 2 位小数**（其它数据集是 5 位），做精确复现或差分时精度不够 |
| ⭐ `Complexity Average` | float | 0 – 5，均值 1.991 | 复杂度，**0 = 无投票**（不是「极简」）。同样 2 位小数 |

> 上面两列的范围是**按 `decimal=","` 正确解析后**的实测值。
> 若忘了加 `decimal=","`，它们会变成字符串列 —— 而且 `describe()` 仍会给出一个「看起来正常」的数值摘要（只统计了恰好没有小数点的整数值，范围会缩成 3.0–8.0），**错得很隐蔽**。
| `BGG Rank` | int | 1 – **20,344** | 无重复；**序列中缺 2230 这一名次**（源站当时的排名空洞），所以 max 比行数大 1 |
| `Owned Users` | int | 0 – 155,312，0.11% 空 | 拥有人数 |
| `Mechanics` | str | **7.86% 空** | 逗号+空格分隔（`"Action Points, Cooperative Game"`） |
| `Domains` | str | **49.94% 空** | 子域，逗号分隔 |

> **注意本数据集没有 `bayesaverage` / Geek Rating**，只有算术均分。
> 要做排序目标必须去 `bgg-threnjen`、`games_detailed_info2025` 或 `bgg-mrpantherson` 取。

### 1.1 子域分布（`Domains` 非空的一半样本）

Wargames 3,316 · Strategy Games 2,205 · Family Games 2,173 · Thematic Games 1,174 · Abstract Games 1,070 · Children's Games 849 · Party Games 605 · Customizable Games 297

与 threnjen（2021 同期）的 `Cat:*` 分布高度一致（War 3,530 / Strategy 2,319 / Family 2,316 …），
可以互为**交叉校验** —— 两份独立抓取给出接近的子域计数，说明两边的子域标注都可信。

## 2. 加载配方

```python
import pandas as pd
df = pd.read_csv("raw/bgg_dataset.csv", sep=";", decimal=",")

df = df.dropna(subset=["ID"])                       # 剔除 16 行无 id 的记录
df["ID"] = df["ID"].astype(int)
df.loc[df["Max Players"] >= 99, "Max Players"] = pd.NA
df.loc[df["Min Players"] == 0, "Min Players"] = pd.NA
df.loc[df["Complexity Average"] == 0, "Complexity Average"] = pd.NA

df["Mechanics"] = df["Mechanics"].fillna("").str.split(", ")
df = df.explode("Mechanics")                        # 多值字段展开
```

## 3. 什么时候用它 / 什么时候别用

**适合**：快速原型、教学 demo、只需要「游戏 + 均分 + 机制」的轻量任务（单文件 2 MB，秒级加载）。

**不适合**：
- 需要 Geek Rating / 子域排名 → 没有
- 需要用户级评分 → 没有
- 需要高精度评分 → `Rating Average` 只有 2 位小数（threnjen / 2025 元数据表是 5 位）
- 需要原始描述文本 → 没有 description 列

## 4. 合规

**CC BY 4.0**：可自由使用与商用，需**署名**原作者（Kaggle 用户 `andrewmvd`）。
