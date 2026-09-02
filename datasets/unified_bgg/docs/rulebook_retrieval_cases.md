# 规则书召回案例

本次使用的是当前 top100 高分桌游的规则书语料，检索入口优先用 `scripts/query_rag_index.py`。
为了避免把长篇规则正文直接堆进报告，下面只保留结构化结果和简短说明。

## 检索命令

```powershell
python scripts\query_rag_index.py "civilization production military culture" --doc-type rulebook_text --bgg-id 182028 --limit 1 --json
python scripts\query_rag_index.py "network route building loans market" --doc-type rulebook_text --bgg-id 224517 --limit 1 --json
```

## 案例 1：Through the Ages: A New Story of Civilization

- 查询：`civilization production military culture`
- 命中规则书：`rulebook:bgg:182028:1jour1jeu:through-the-ages-a-new-story-of-civilization-rulebook`
- 命中游戏简介：`game:bgg:182028:overview:rag-v0.1`
- 命中评论摘要：`reviews:bgg:182028:digest:rag-v0.1`

| 项目 | 值 |
| --- | --- |
| BGG ID | `182028` |
| 规则书页数 | `24` |
| 规则书字符数 | `140324` |
| 规则书抽取方式 | `pdf_text_fitz` |
| 规则书来源 | `https://cdn.1j1ju.com/medias/67/54/3d-through-the-ages-a-new-story-of-civilization-rulebook.pdf` |
| 游戏简介 | 2-4人，120分钟，14+，综合评分 8.27，Bayesian 8.04，复杂度 4.44/5，总排名 14。 |
| 评论摘要 | 32,752 条评分行、3,684 条非空评论，覆盖率 11.25%，评论主要聚焦在“很重、很长、要反复查规则”，同时认可其文明构筑深度与新版流畅度。 |

- 规则书内容要点：规则书正文从新手手册、玩家区、科学/文化板块、回合结构、军事系统一路展开，适合回答“怎么玩、每阶段做什么、战争与发展如何工作”这类问题。
- 观察 1：这个案例很适合做规则召回，因为 query 里的 civilization / military / culture / production 都能在规则书、游戏简介和评论摘要中形成一致语义。
- 观察 2：规则书长度很大，但主题高度集中，适合训练“长文规则分段召回 + 结构化总结”。
- 观察 3：评论摘要与简介能补足规则书没有显式讲的体验维度，例如“很长”“要经常查规则”“数字版更顺手”。

## 案例 2：Brass: Birmingham

- 查询：`network route building loans market`
- 命中规则书：`rulebook:bgg:224517:1jour1jeu:brass-birmingham-rulebook`
- 命中游戏简介：`game:bgg:224517:overview:rag-v0.1`
- 命中评论摘要：`reviews:bgg:224517:digest:rag-v0.1`

| 项目 | 值 |
| --- | --- |
| BGG ID | `224517` |
| 规则书页数 | `7` |
| 规则书字符数 | `38819` |
| 规则书抽取方式 | `pdf_text_fitz` |
| 规则书来源 | `https://cdn.1j1ju.com/medias/60/39/64-brass-birmingham-rulebook.pdf` |
| 游戏简介 | 2-4人，60-120分钟，14+，综合评分 8.59，Bayesian 8.41，复杂度 3.87/5，总排名 1。 |
| 评论摘要 | 50,029 条评分行、5,154 条非空评论，覆盖率 10.30%，评论主要赞美核心机制精炼、工业革命主题强、生产精美；批评主要集中在规则细节多、算盘感强、互动偏“各玩各的”。 |

- 规则书内容要点：规则书开头直接给出工业革命背景、两时代结构、六大动作、结算与提示，特别适合回答“回合里能做什么、建路/贷款/卖货/发展怎么运作”。
- 观察 1：这个案例适合验证“动作型规则召回”，因为 query 里的 network / loans / market 都是 Brass 的核心操作词。
- 观察 2：规则书较短，信息密度很高，适合评估检索是否能精准抓住动作和结算规则，而不是只抓到游戏简介。
- 观察 3：评论摘要与简介显示，这个游戏的难点不在“有没有规则”，而在“规则细节多、资源链复杂”，这对微调和召回都很有价值。

## 结论

- 这两个案例都能从规则书、简介和评论三类文档里形成一致语义，适合做“规则理解 + 机制解释 + 口碑摘要”的联合召回。
- 现在更稳的检索入口是 `scripts/query_rag_index.py`，因为它能直接命中 `rulebook_text`。
- 如果你后面要补 Catan，它目前还不在这批 top100 规则书里，需要单独扩充或显式指定游戏列表。
