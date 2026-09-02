# 规则书召回原始数据

下面保存的是支撑上面两个案例的结构化原始字段。这里不直接贴长段规则正文，只保留定位、统计和抽样信息。

## 当前规则书语料概况

| 指标 | 数值 |
| --- | ---: |
| `rulebook_text` 文档数 | `100` |
| 总字符数 | `3,988,723` |
| 总页数 | `1,419` |
| 抽取方式 | `pdf_text_fitz: 74`, `fallback_local_summary: 26` |
| 质量审计 | 无结构性错误；`very_long_text: 71` |

## 原始记录 1：Through the Ages: A New Story of Civilization

| 字段 | 原始值 |
| --- | --- |
| 规则书 doc_id | `rulebook:bgg:182028:1jour1jeu:through-the-ages-a-new-story-of-civilization-rulebook` |
| 规则书 title | `Through the Ages: A New Story of Civilization` |
| 规则书 bgg_id | `182028` |
| 规则书 source URL | `https://cdn.1j1ju.com/medias/67/54/3d-through-the-ages-a-new-story-of-civilization-rulebook.pdf` |
| 规则书 page_url | `https://en.1jour-1jeu.com/rules/search?q=Through+the+Ages%3A+A+New+Story+of+Civilization` |
| 规则书 page_count | `24` |
| 规则书 bytes | `29700445` |
| 规则书 extraction | `pdf_text_fitz` |
| 规则书 quality_flags | `[]` |
| 规则书 source_datasets | `['intermediate/games.csv', 'intermediate/game_stats.csv', 'intermediate/game_taxonomy_canonical.csv']` |
| 游戏简介 doc_id | `game:bgg:182028:overview:rag-v0.1` |
| 游戏简介 stats | rating 8.27 / bayes 8.04 / rank 14 |
| 游戏简介 players/playtime | `2-4` 人 / `120-120` 分钟 / `14+` |
| 评论摘要 doc_id | `reviews:bgg:182028:digest:rag-v0.1` |
| 评论摘要 stats | `rating_rows=32752`, `comment_rows=3684`, `coverage=11.25%` |
| 评论摘要主题 | `positive / mixed / critical` 三类；见分析文件中的归纳 |

| 规则书原始内容说明 | 摘要 |
| --- | --- |
| 规则书内容定位 | 规则书正文从新手手册、玩家区、科学/文化板块、回合结构、军事系统一路展开，适合回答“怎么玩、每阶段做什么、战争与发展如何工作”这类问题。 |

## 原始记录 2：Brass: Birmingham

| 字段 | 原始值 |
| --- | --- |
| 规则书 doc_id | `rulebook:bgg:224517:1jour1jeu:brass-birmingham-rulebook` |
| 规则书 title | `Brass: Birmingham` |
| 规则书 bgg_id | `224517` |
| 规则书 source URL | `https://cdn.1j1ju.com/medias/60/39/64-brass-birmingham-rulebook.pdf` |
| 规则书 page_url | `https://en.1jour-1jeu.com/rules/search?q=Brass%3A+Birmingham` |
| 规则书 page_count | `7` |
| 规则书 bytes | `6674219` |
| 规则书 extraction | `pdf_text_fitz` |
| 规则书 quality_flags | `[]` |
| 规则书 source_datasets | `['intermediate/games.csv', 'intermediate/game_stats.csv', 'intermediate/game_taxonomy_canonical.csv']` |
| 游戏简介 doc_id | `game:bgg:224517:overview:rag-v0.1` |
| 游戏简介 stats | rating 8.59 / bayes 8.41 / rank 1 |
| 游戏简介 players/playtime | `2-4` 人 / `60-120` 分钟 / `14+` |
| 评论摘要 doc_id | `reviews:bgg:224517:digest:rag-v0.1` |
| 评论摘要 stats | `rating_rows=50029`, `comment_rows=5154`, `coverage=10.30%` |
| 评论摘要主题 | `positive / mixed / critical` 三类；见分析文件中的归纳 |

| 规则书原始内容说明 | 摘要 |
| --- | --- |
| 规则书内容定位 | 规则书开头直接给出工业革命背景、两时代结构、六大动作、结算与提示，特别适合回答“回合里能做什么、建路/贷款/卖货/发展怎么运作”。 |
