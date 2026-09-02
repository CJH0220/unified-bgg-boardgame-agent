# Retrieval Suite Report

Generated at: `2026-08-26T11:37:29`

## Summary

| Metric | Value |
| --- | ---: |
| Suite size | 12 |
| Validated queries | 12 |
| Passed | 12 |
| Pass rate | 1.0 |
| Engine | `hybrid` |
| Limit | 5 |
| Candidate limit | 50 |

## Per Doc Type

| Doc type | Count |
| --- | ---: |
| `game_overview` | 5 |
| `mechanic_profile` | 4 |
| `review_digest` | 3 |

## Samples

### PASS: `q01` - `卡坦岛 游戏简介`

- Expected: `game:bgg:13`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | CATAN | `game:bgg:13:overview:rag-v0.1` |
| 2 | 0.031746031746031744 | `game_overview` | Settlers of Catan: Gallery Edition | `game:bgg:38821:overview:rag-v0.1` |
| 3 | 0.031054405392392875 | `game_overview` | Settlers of Catan: Rockman Edition | `game:bgg:20899:overview:rag-v0.1` |
| 4 | 0.031054405392392875 | `game_overview` | The Settlers of Catan: The Great River | `game:bgg:20247:overview:rag-v0.1` |
| 5 | 0.027984344422700584 | `game_overview` | Catan: Family Edition | `game:bgg:147240:overview:rag-v0.1` |

### PASS: `q02` - `卡坦岛 交易 评论`

- Expected: `reviews:bgg:13`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.07889344262295082 | `review_digest` | CATAN | `reviews:bgg:13:digest:rag-v0.1` |
| 2 | 0.03200204813108039 | `review_digest` | Catan Histories: Merchants of Europe | `reviews:bgg:103091:digest:rag-v0.1` |
| 3 | 0.030886196246139225 | `review_digest` | Dante's Inferno | `reviews:bgg:6201:digest:rag-v0.1` |
| 4 | 0.030834914611005692 | `review_digest` | Settlers of Catan: Rockman Edition | `reviews:bgg:20899:digest:rag-v0.1` |
| 5 | 0.03057889822595705 | `review_digest` | Die Siedler von Catan: Junior | `reviews:bgg:27766:digest:rag-v0.1` |

### PASS: `q03` - `卡卡颂 规则`

- Expected: `game:bgg:822`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.06639344262295083 | `game_overview` | Carcassonne | `game:bgg:822:overview:rag-v0.1` |
| 2 | 0.031754032258064516 | `game_overview` | Carcassonne: The River | `game:bgg:2591:overview:rag-v0.1` |
| 3 | 0.0315136476426799 | `game_overview` | Carcassonne: The City | `game:bgg:12902:overview:rag-v0.1` |
| 4 | 0.03131881575727918 | `game_overview` | Carcassonne: The Gold Mines | `game:bgg:118617:overview:rag-v0.1` |
| 5 | 0.030776515151515152 | `game_overview` | Carcassonne: The Count of Carcassonne | `game:bgg:12903:overview:rag-v0.1` |

### PASS: `q04` - `卡卡颂 评论`

- Expected: `reviews:bgg:822`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.06639344262295083 | `review_digest` | Carcassonne | `reviews:bgg:822:digest:rag-v0.1` |
| 2 | 0.030798389007344232 | `review_digest` | Horus | `reviews:bgg:9616:digest:rag-v0.1` |
| 3 | 0.030776515151515152 | `review_digest` | Queensland | `reviews:bgg:364488:digest:rag-v0.1` |
| 4 | 0.029726775956284153 | `review_digest` | Cornwall | `reviews:bgg:181328:digest:rag-v0.1` |
| 5 | 0.029709507042253523 | `review_digest` | Manhattan TraffIQ | `reviews:bgg:179813:digest:rag-v0.1` |

### PASS: `q05` - `幽港迷城 合作 战役`

- Expected: `game:bgg:174430`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `game_overview` | Gloomhaven | `game:bgg:174430:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | Gloomhaven: Jaws of the Lion | `game:bgg:291457:overview:rag-v0.1` |
| 3 | 0.03149801587301587 | `game_overview` | Trench Club: Legacy | `game:bgg:368939:overview:rag-v0.1` |
| 4 | 0.031024531024531024 | `game_overview` | Gloomhaven: Second Edition | `game:bgg:390478:overview:rag-v0.1` |
| 5 | 0.03007688828584351 | `game_overview` | Gascony's Legacy | `game:bgg:224793:overview:rag-v0.1` |

### PASS: `q06` - `Brass Birmingham economic network route building`

- Expected: `game:bgg:224517`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Brass: Birmingham | `game:bgg:224517:overview:rag-v0.1` |
| 2 | 0.03225806451612903 | `game_overview` | Brass 2-player board | `game:bgg:201381:overview:rag-v0.1` |
| 3 | 0.030330882352941176 | `game_overview` | Birmingham in a Box | `game:bgg:17673:overview:rag-v0.1` |
| 4 | 0.029957522915269395 | `game_overview` | Brass: Lancashire | `game:bgg:28720:overview:rag-v0.1` |
| 5 | 0.029910714285714284 | `game_overview` | Catalonia (fan expansion for Brass) | `game:bgg:138329:overview:rag-v0.1` |

### PASS: `q07` - `Through the Ages civilization`

- Expected: `game:bgg:182028`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.031746031746031744 | `game_overview` | Die Civilization | `game:bgg:91003:overview:rag-v0.1` |
| 2 | 0.030679156908665108 | `game_overview` | Through the Ages: A New Story of Civilization | `game:bgg:182028:overview:rag-v0.1` |
| 3 | 0.030621785881252923 | `game_overview` | Through the Ages: A Story of Civilization | `game:bgg:25613:overview:rag-v0.1` |
| 4 | 0.028665028665028666 | `game_overview` | Mega Civilization | `game:bgg:184424:overview:rag-v0.1` |
| 5 | 0.028125 | `game_overview` | Through the Ages: A Story of Civilization – Czech expansion | `game:bgg:98880:overview:rag-v0.1` |

### PASS: `q08` - `worker placement`

- Expected: `mechanic:worker-placement:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Worker Placement, Different Worker Types | `mechanic:worker-placement,-different-worker-types:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Worker Placement with Dice Workers | `mechanic:worker-placement-with-dice-workers:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Worker Placement | `mechanic:worker-placement:profile:rag-v0.1` |
| 4 | 0.03125 | `mechanic_profile` | Auction: Fixed Placement | `mechanic:auction:-fixed-placement:profile:rag-v0.1` |
| 5 | 0.029877369007803793 | `mechanic_profile` | Contracts | `mechanic:contracts:profile:rag-v0.1` |

### PASS: `q09` - `deck bag pool building`

- Expected: `mechanic:deck,-bag,-and-pool-building:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Deck, Bag, and Pool Building | `mechanic:deck,-bag,-and-pool-building:profile:rag-v0.1` |
| 2 | 0.03200204813108039 | `mechanic_profile` | Move Through Deck | `mechanic:move-through-deck:profile:rag-v0.1` |
| 3 | 0.03149801587301587 | `mechanic_profile` | Deck Construction | `mechanic:deck-construction:profile:rag-v0.1` |
| 4 | 0.03076923076923077 | `mechanic_profile` | Auction: Dutch | `mechanic:auction:-dutch:profile:rag-v0.1` |
| 5 | 0.029857397504456328 | `mechanic_profile` | Open Drafting | `mechanic:open-drafting:profile:rag-v0.1` |

### PASS: `q10` - `dice rolling mechanic`

- Expected: `mechanic:dice-rolling:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Dice Rolling | `mechanic:dice-rolling:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Re-rolling and Locking | `mechanic:re-rolling-and-locking:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Different Dice Movement | `mechanic:different-dice-movement:profile:rag-v0.1` |
| 4 | 0.030303030303030304 | `mechanic_profile` | Worker Placement with Dice Workers | `mechanic:worker-placement-with-dice-workers:profile:rag-v0.1` |
| 5 | 0.029850746268656716 | `mechanic_profile` | Random Production | `mechanic:random-production:profile:rag-v0.1` |

### PASS: `q11` - `auction bidding`

- Expected: `mechanic:auction---bidding:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Auction / Bidding | `mechanic:auction---bidding:profile:rag-v0.1` |
| 2 | 0.031754032258064516 | `mechanic_profile` | Constrained Bidding | `mechanic:constrained-bidding:profile:rag-v0.1` |
| 3 | 0.031054405392392875 | `mechanic_profile` | Auction: Once Around | `mechanic:auction:-once-around:profile:rag-v0.1` |
| 4 | 0.031009615384615385 | `mechanic_profile` | Auction: Multiple Lot | `mechanic:auction:-multiple-lot:profile:rag-v0.1` |
| 5 | 0.03057889822595705 | `mechanic_profile` | Auction Compensation | `mechanic:auction-compensation:profile:rag-v0.1` |

### PASS: `q12` - `popular comments for Catan`

- Expected: `reviews:bgg:13`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.07691975841242452 | `review_digest` | CATAN | `reviews:bgg:13:digest:rag-v0.1` |
| 2 | 0.03200204813108039 | `review_digest` | Baden-Württemberg Catan | `reviews:bgg:123386:digest:rag-v0.1` |
| 3 | 0.031754032258064516 | `review_digest` | Catan: Big Game Event Kit | `reviews:bgg:194097:digest:rag-v0.1` |
| 4 | 0.030776515151515152 | `review_digest` | Catan Junior Mitbringspiel | `reviews:bgg:269978:digest:rag-v0.1` |
| 5 | 0.03057889822595705 | `review_digest` | Catan Dice Game | `reviews:bgg:27710:digest:rag-v0.1` |
