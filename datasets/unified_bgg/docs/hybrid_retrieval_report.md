# Hybrid Retrieval Report

Generated at: `2026-08-26T09:53:46`

## Summary

| Metric | Value |
| --- | ---: |
| Passed queries | 9 / 9 |
| Pass rate | 1.0 |
| Top K | 5 |
| Candidate limit | 50 |

## Method

- FTS layer: existing SQLite FTS5/BM25 index at `final/rag_index.sqlite`.
- Vector layer: local sparse TF-IDF inverted index at `final/rag_vector_index.sqlite`.
- Chinese queries are expanded with a small auditable dictionary before retrieval.
- Fusion uses reciprocal rank fusion and records `fts_rank`, `vector_rank`, `vector_score`, and `fusion_score`.

## Query Results

### PASS: `卡坦岛 交易 评论`

- Doc type filter: `review_digest`
- Expected: `reviews:bgg:13`

| Rank | Fusion | FTS rank | Vector rank | Vector score | Title | Doc ID |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | 0.078893 | 20 | 1 | 0.29466 | CATAN | `reviews:bgg:13:digest:rag-v0.1` |
| 2 | 0.032002 | 2 | 3 | 0.335663 | Catan Histories: Merchants of Europe | `reviews:bgg:103091:digest:rag-v0.1` |
| 3 | 0.030886 | 1 | 9 | 0.280932 | Dante's Inferno | `reviews:bgg:6201:digest:rag-v0.1` |
| 4 | 0.030835 | 8 | 2 | 0.367858 | Settlers of Catan: Rockman Edition | `reviews:bgg:20899:digest:rag-v0.1` |
| 5 | 0.030579 | 3 | 8 | 0.282102 | Die Siedler von Catan: Junior | `reviews:bgg:27766:digest:rag-v0.1` |

### PASS: `卡坦岛 游戏简介`

- Doc type filter: `game_overview`
- Expected: `game:bgg:13`

| Rank | Fusion | FTS rank | Vector rank | Vector score | Title | Doc ID |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | 0.082787 | 1 | 1 | 0.307343 | CATAN | `game:bgg:13:overview:rag-v0.1` |
| 2 | 0.031746 | 3 | 3 | 0.479576 | Settlers of Catan: Gallery Edition | `game:bgg:38821:overview:rag-v0.1` |
| 3 | 0.031054 | 2 | 7 | 0.41857 | Settlers of Catan: Rockman Edition | `game:bgg:20899:overview:rag-v0.1` |
| 4 | 0.031054 | 7 | 2 | 0.522249 | The Settlers of Catan: The Great River | `game:bgg:20247:overview:rag-v0.1` |
| 5 | 0.027984 | 13 | 10 | 0.403408 | Catan: Family Edition | `game:bgg:147240:overview:rag-v0.1` |

### PASS: `幽港迷城 合作 战役`

- Doc type filter: `game_overview`
- Expected: `game:bgg:174430`

| Rank | Fusion | FTS rank | Vector rank | Vector score | Title | Doc ID |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | 0.082522 | 2 | 1 | 0.309891 | Gloomhaven | `game:bgg:174430:overview:rag-v0.1` |
| 2 | 0.032522 | 1 | 2 | 0.304902 | Gloomhaven: Jaws of the Lion | `game:bgg:291457:overview:rag-v0.1` |
| 3 | 0.031498 | 3 | 4 | 0.287199 | Trench Club: Legacy | `game:bgg:368939:overview:rag-v0.1` |
| 4 | 0.031025 | 6 | 3 | 0.293062 | Gloomhaven: Second Edition | `game:bgg:390478:overview:rag-v0.1` |
| 5 | 0.030077 | 7 | 6 | 0.224823 | Gascony's Legacy | `game:bgg:224793:overview:rag-v0.1` |

### PASS: `卡卡颂 拼放版图 评论`

- Doc type filter: `review_digest`
- Expected: `reviews:bgg:822`

| Rank | Fusion | FTS rank | Vector rank | Vector score | Title | Doc ID |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | 0.066393 | None | 1 | 0.166101 | Carcassonne | `reviews:bgg:822:digest:rag-v0.1` |
| 2 | 0.031754 | 2 | 4 | 0.236884 | Horus | `reviews:bgg:9616:digest:rag-v0.1` |
| 3 | 0.031319 | 1 | 7 | 0.222568 | Manhattan TraffIQ | `reviews:bgg:179813:digest:rag-v0.1` |
| 4 | 0.031258 | 3 | 5 | 0.233514 | Queensland | `reviews:bgg:364488:digest:rag-v0.1` |
| 5 | 0.030622 | 9 | 2 | 0.249774 | Maori | `reviews:bgg:40425:digest:rag-v0.1` |

### PASS: `牌库构筑 机制`

- Doc type filter: `mechanic_profile`
- Expected: `mechanic:deck,-bag,-and-pool-building`

| Rank | Fusion | FTS rank | Vector rank | Vector score | Title | Doc ID |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | 0.032787 | 1 | 1 | 0.417614 | Deck, Bag, and Pool Building | `mechanic:deck,-bag,-and-pool-building:profile:rag-v0.1` |
| 2 | 0.031754 | 4 | 2 | 0.279879 | Move Through Deck | `mechanic:move-through-deck:profile:rag-v0.1` |
| 3 | 0.031746 | 3 | 3 | 0.269152 | Deck Construction | `mechanic:deck-construction:profile:rag-v0.1` |
| 4 | 0.029418 | 7 | 9 | 0.221806 | Open Drafting | `mechanic:open-drafting:profile:rag-v0.1` |
| 5 | 0.029116 | 2 | 17 | 0.205245 | Melding and Splaying | `mechanic:melding-and-splaying:profile:rag-v0.1` |

### PASS: `工人放置 机制`

- Doc type filter: `mechanic_profile`
- Expected: `mechanic:worker-placement:profile`

| Rank | Fusion | FTS rank | Vector rank | Vector score | Title | Doc ID |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | 0.032522 | 1 | 2 | 0.380935 | Worker Placement with Dice Workers | `mechanic:worker-placement-with-dice-workers:profile:rag-v0.1` |
| 2 | 0.032522 | 2 | 1 | 0.398993 | Worker Placement, Different Worker Types | `mechanic:worker-placement,-different-worker-types:profile:rag-v0.1` |
| 3 | 0.031746 | 3 | 3 | 0.377127 | Worker Placement | `mechanic:worker-placement:profile:rag-v0.1` |
| 4 | 0.03125 | 4 | 4 | 0.317392 | Action Drafting | `mechanic:action-drafting:profile:rag-v0.1` |
| 5 | 0.03031 | 5 | 7 | 0.261811 | Turn Order: Claim Action | `mechanic:turn-order:-claim-action:profile:rag-v0.1` |

### PASS: `Brass Birmingham economic network route building`

- Doc type filter: `game_overview`
- Expected: `game:bgg:224517`

| Rank | Fusion | FTS rank | Vector rank | Vector score | Title | Doc ID |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | 0.082787 | 1 | 1 | 0.484826 | Brass: Birmingham | `game:bgg:224517:overview:rag-v0.1` |
| 2 | 0.032258 | 2 | 2 | 0.521126 | Brass 2-player board | `game:bgg:201381:overview:rag-v0.1` |
| 3 | 0.030331 | 8 | 4 | 0.375478 | Birmingham in a Box | `game:bgg:17673:overview:rag-v0.1` |
| 4 | 0.029958 | 3 | 11 | 0.255923 | Brass: Lancashire | `game:bgg:28720:overview:rag-v0.1` |
| 5 | 0.029911 | 4 | 10 | 0.266003 | Catalonia (fan expansion for Brass) | `game:bgg:138329:overview:rag-v0.1` |

### PASS: `Catan trading negotiation user comments`

- Doc type filter: `review_digest`
- Expected: `reviews:bgg:13`

| Rank | Fusion | FTS rank | Vector rank | Vector score | Title | Doc ID |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | 0.080092 | 13 | 1 | 0.2831 | CATAN | `reviews:bgg:13:digest:rag-v0.1` |
| 2 | 0.031025 | 6 | 3 | 0.318671 | Baden-Württemberg Catan | `reviews:bgg:123386:digest:rag-v0.1` |
| 3 | 0.030622 | 9 | 2 | 0.340602 | Catan: Big Game Event Kit | `reviews:bgg:194097:digest:rag-v0.1` |
| 4 | 0.03009 | 8 | 5 | 0.302959 | Catan: Junior | `reviews:bgg:125921:digest:rag-v0.1` |
| 5 | 0.029828 | 2 | 13 | 0.246745 | A Game of Thrones: Catan – Brotherhood of the Watch | `reviews:bgg:229218:digest:rag-v0.1` |

### PASS: `Gloomhaven cooperative campaign fantasy`

- Doc type filter: `game_overview`
- Expected: `game:bgg:174430`

| Rank | Fusion | FTS rank | Vector rank | Vector score | Title | Doc ID |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | 0.082018 | 4 | 1 | 0.399266 | Gloomhaven | `game:bgg:174430:overview:rag-v0.1` |
| 2 | 0.032258 | 2 | 2 | 0.37891 | Gloomhaven: Second Edition | `game:bgg:390478:overview:rag-v0.1` |
| 3 | 0.032018 | 1 | 4 | 0.363835 | Gloomhaven: Jaws of the Lion | `game:bgg:291457:overview:rag-v0.1` |
| 4 | 0.031025 | 3 | 6 | 0.28131 | Gloomholdin' | `game:bgg:340909:overview:rag-v0.1` |
| 5 | 0.030798 | 7 | 3 | 0.374863 | Founders of Gloomhaven | `game:bgg:214032:overview:rag-v0.1` |
