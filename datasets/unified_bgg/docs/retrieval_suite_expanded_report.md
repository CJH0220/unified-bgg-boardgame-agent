# Phase 10 Expanded Retrieval Suite Report

Generated at: `2026-08-26T11:59:46`

## Summary

| Metric | Value |
| --- | ---: |
| Suite size | 146 |
| Validated queries | 146 |
| Passed | 146 |
| Failed | 0 |
| Pass rate | 1.0 |
| Engine | `hybrid` |
| Limit | 5 |
| Candidate limit | 50 |

## Per Doc Type

| Doc type | Count | Validated | Passed | Pass rate |
| --- | ---: | ---: | ---: | ---: |
| `game_overview` | 60 | 60 | 60 | 1.0 |
| `mechanic_profile` | 56 | 56 | 56 | 1.0 |
| `review_digest` | 30 | 30 | 30 | 1.0 |

## Query Results

### PASS: `g001_cn_overview` - `卡坦岛 游戏简介`

- Expected: `game:bgg:13`
- Entity route: `{'bgg_id': 13, 'title': 'CATAN'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | CATAN | `game:bgg:13:overview:rag-v0.1` |
| 2 | 0.031746031746031744 | `game_overview` | Settlers of Catan: Gallery Edition | `game:bgg:38821:overview:rag-v0.1` |
| 3 | 0.031054405392392875 | `game_overview` | Settlers of Catan: Rockman Edition | `game:bgg:20899:overview:rag-v0.1` |
| 4 | 0.031054405392392875 | `game_overview` | The Settlers of Catan: The Great River | `game:bgg:20247:overview:rag-v0.1` |
| 5 | 0.027984344422700584 | `game_overview` | Catan: Family Edition | `game:bgg:147240:overview:rag-v0.1` |

### PASS: `g001_cn_review` - `卡坦岛 玩家评论`

- Expected: `reviews:bgg:13`
- Entity route: `{'bgg_id': 13, 'title': 'CATAN'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.07921395544346364 | `review_digest` | CATAN | `reviews:bgg:13:digest:rag-v0.1` |
| 2 | 0.03252247488101534 | `review_digest` | Settlers of Catan: Rockman Edition | `reviews:bgg:20899:digest:rag-v0.1` |
| 3 | 0.031746031746031744 | `review_digest` | Catan Histories: Merchants of Europe | `reviews:bgg:103091:digest:rag-v0.1` |
| 4 | 0.030330882352941176 | `review_digest` | Die Siedler von Catan: Junior | `reviews:bgg:27766:digest:rag-v0.1` |
| 5 | 0.02967032967032967 | `review_digest` | Catan: Junior | `reviews:bgg:125921:digest:rag-v0.1` |

### PASS: `g001_cn_theme` - `卡坦岛 交易 掷骰 资源 机制`

- Expected: `game:bgg:13`
- Entity route: `{'bgg_id': 13, 'title': 'CATAN'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | CATAN | `game:bgg:13:overview:rag-v0.1` |
| 2 | 0.03149801587301587 | `game_overview` | Settlers of Catan: Gallery Edition | `game:bgg:38821:overview:rag-v0.1` |
| 3 | 0.030834914611005692 | `game_overview` | The Settlers of Catan: The Great River | `game:bgg:20247:overview:rag-v0.1` |
| 4 | 0.03057889822595705 | `game_overview` | Settlers of Catan: Rockman Edition | `game:bgg:20899:overview:rag-v0.1` |
| 5 | 0.02878726010616578 | `game_overview` | CATAN: Dawn of Humankind | `game:bgg:358858:overview:rag-v0.1` |

### PASS: `g002_cn_overview` - `卡卡颂 游戏简介`

- Expected: `game:bgg:822`
- Entity route: `{'bgg_id': 822, 'title': 'Carcassonne'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.06639344262295083 | `game_overview` | Carcassonne | `game:bgg:822:overview:rag-v0.1` |
| 2 | 0.032018442622950824 | `game_overview` | Carcassonne: The City | `game:bgg:12902:overview:rag-v0.1` |
| 3 | 0.03128054740957967 | `game_overview` | Carcassonne: The River | `game:bgg:2591:overview:rag-v0.1` |
| 4 | 0.031054405392392875 | `game_overview` | Carcassonne: Solovei Razboynik and Vodyanoy | `game:bgg:215144:overview:rag-v0.1` |
| 5 | 0.03076923076923077 | `game_overview` | Carcassonne: The Plague | `game:bgg:85003:overview:rag-v0.1` |

### PASS: `g002_cn_review` - `卡卡颂 玩家评论`

- Expected: `reviews:bgg:822`
- Entity route: `{'bgg_id': 822, 'title': 'Carcassonne'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.06639344262295083 | `review_digest` | Carcassonne | `reviews:bgg:822:digest:rag-v0.1` |
| 2 | 0.03055037313432836 | `review_digest` | Queensland | `reviews:bgg:364488:digest:rag-v0.1` |
| 3 | 0.03036576949620428 | `review_digest` | Manhattan TraffIQ | `reviews:bgg:179813:digest:rag-v0.1` |
| 4 | 0.029551337359792925 | `review_digest` | Cornwall | `reviews:bgg:181328:digest:rag-v0.1` |
| 5 | 0.028991596638655463 | `review_digest` | Horus | `reviews:bgg:9616:digest:rag-v0.1` |

### PASS: `g002_cn_theme` - `卡卡颂 版图拼放 区域控制 机制`

- Expected: `game:bgg:822`
- Entity route: `{'bgg_id': 822, 'title': 'Carcassonne'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.06639344262295083 | `game_overview` | Carcassonne | `game:bgg:822:overview:rag-v0.1` |
| 2 | 0.032266458495966696 | `game_overview` | Carcassonne: The City | `game:bgg:12902:overview:rag-v0.1` |
| 3 | 0.030158730158730156 | `game_overview` | Carcassonne: South Seas | `game:bgg:147303:overview:rag-v0.1` |
| 4 | 0.03007688828584351 | `game_overview` | Carcassonne: The Plague | `game:bgg:85003:overview:rag-v0.1` |
| 5 | 0.029857397504456328 | `game_overview` | Carcassonne: Solovei Razboynik and Vodyanoy | `game:bgg:215144:overview:rag-v0.1` |

### PASS: `g003_cn_overview` - `伯明翰重工业 游戏简介`

- Expected: `game:bgg:224517`
- Entity route: `{'bgg_id': 224517, 'title': 'Brass: Birmingham'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Brass: Birmingham | `game:bgg:224517:overview:rag-v0.1` |
| 2 | 0.03200204813108039 | `game_overview` | Brass: Lancashire | `game:bgg:28720:overview:rag-v0.1` |
| 3 | 0.031754032258064516 | `game_overview` | Brass 2-player board | `game:bgg:201381:overview:rag-v0.1` |
| 4 | 0.03149801587301587 | `game_overview` | Land of Industry | `game:bgg:73612:overview:rag-v0.1` |
| 5 | 0.028006267136701922 | `game_overview` | Catalonia (fan expansion for Brass) | `game:bgg:138329:overview:rag-v0.1` |

### PASS: `g003_cn_review` - `伯明翰重工业 玩家评论`

- Expected: `reviews:bgg:224517`
- Entity route: `{'bgg_id': 224517, 'title': 'Brass: Birmingham'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `review_digest` | Brass: Birmingham | `reviews:bgg:224517:digest:rag-v0.1` |
| 2 | 0.03200204813108039 | `review_digest` | Age of Industry | `reviews:bgg:65901:digest:rag-v0.1` |
| 3 | 0.03149801587301587 | `review_digest` | Roll and Rails | `reviews:bgg:372883:digest:rag-v0.1` |
| 4 | 0.03128054740957967 | `review_digest` | Shinjuku | `reviews:bgg:286690:digest:rag-v0.1` |
| 5 | 0.02967032967032967 | `review_digest` | British Rails | `reviews:bgg:2689:digest:rag-v0.1` |

### PASS: `g003_cn_theme` - `伯明翰重工业 经济 路线建设 机制`

- Expected: `game:bgg:224517`
- Entity route: `{'bgg_id': 224517, 'title': 'Brass: Birmingham'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Brass: Birmingham | `game:bgg:224517:overview:rag-v0.1` |
| 2 | 0.03200204813108039 | `game_overview` | Brass: Lancashire | `game:bgg:28720:overview:rag-v0.1` |
| 3 | 0.031754032258064516 | `game_overview` | Brass 2-player board | `game:bgg:201381:overview:rag-v0.1` |
| 4 | 0.03149801587301587 | `game_overview` | Coast-to-Coast Rails | `game:bgg:41878:overview:rag-v0.1` |
| 5 | 0.029877369007803793 | `game_overview` | Land of Industry | `game:bgg:73612:overview:rag-v0.1` |

### PASS: `g004_cn_overview` - `瘟疫危机传承第一季 游戏简介`

- Expected: `game:bgg:161936`
- Entity route: `{'bgg_id': 161936, 'title': 'Pandemic Legacy: Season 1'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Pandemic Legacy: Season 1 | `game:bgg:161936:overview:rag-v0.1` |
| 2 | 0.03225806451612903 | `game_overview` | Pandemic Legacy: Season 2 | `game:bgg:221107:overview:rag-v0.1` |
| 3 | 0.03149801587301587 | `game_overview` | Pandemic Legacy: Season 0 | `game:bgg:314040:overview:rag-v0.1` |
| 4 | 0.03125763125763126 | `game_overview` | Pandemic: On the Brink | `game:bgg:40849:overview:rag-v0.1` |
| 5 | 0.031009615384615385 | `game_overview` | Pandemic: State of Emergency | `game:bgg:168703:overview:rag-v0.1` |

### PASS: `g004_cn_review` - `瘟疫危机传承第一季 玩家评论`

- Expected: `reviews:bgg:161936`
- Entity route: `{'bgg_id': 161936, 'title': 'Pandemic Legacy: Season 1'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `review_digest` | Pandemic Legacy: Season 1 | `reviews:bgg:161936:digest:rag-v0.1` |
| 2 | 0.03252247488101534 | `review_digest` | Pandemic Legacy: Season 0 | `reviews:bgg:314040:digest:rag-v0.1` |
| 3 | 0.031746031746031744 | `review_digest` | Pandemic Legacy: Season 2 | `reviews:bgg:221107:digest:rag-v0.1` |
| 4 | 0.030330882352941176 | `review_digest` | Pandemic: Contagion | `reviews:bgg:157789:digest:rag-v0.1` |
| 5 | 0.03007688828584351 | `review_digest` | Iberia | `reviews:bgg:198928:digest:rag-v0.1` |

### PASS: `g004_cn_theme` - `瘟疫危机传承第一季 合作 战役 机制`

- Expected: `game:bgg:161936`
- Entity route: `{'bgg_id': 161936, 'title': 'Pandemic Legacy: Season 1'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Pandemic Legacy: Season 1 | `game:bgg:161936:overview:rag-v0.1` |
| 2 | 0.03225806451612903 | `game_overview` | Pandemic Legacy: Season 2 | `game:bgg:221107:overview:rag-v0.1` |
| 3 | 0.031746031746031744 | `game_overview` | Pandemic Legacy: Season 0 | `game:bgg:314040:overview:rag-v0.1` |
| 4 | 0.031009615384615385 | `game_overview` | Pandemic: State of Emergency | `game:bgg:168703:overview:rag-v0.1` |
| 5 | 0.031009615384615385 | `game_overview` | Pandemic: On the Brink | `game:bgg:40849:overview:rag-v0.1` |

### PASS: `g005_cn_overview` - `方舟动物园 游戏简介`

- Expected: `game:bgg:342942`
- Entity route: `{'bgg_id': 342942, 'title': 'Ark Nova'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Ark Nova | `game:bgg:342942:overview:rag-v0.1` |
| 2 | 0.031024531024531024 | `game_overview` | Nova's Ark | `game:bgg:97312:overview:rag-v0.1` |
| 3 | 0.02919863597612958 | `game_overview` | Streichel-Zoo | `game:bgg:110842:overview:rag-v0.1` |
| 4 | 0.029138513513513514 | `game_overview` | Safe in the Ark | `game:bgg:135809:overview:rag-v0.1` |
| 5 | 0.028814262023217248 | `game_overview` | The Zoo Break Game | `game:bgg:88128:overview:rag-v0.1` |

### PASS: `g005_cn_review` - `方舟动物园 玩家评论`

- Expected: `reviews:bgg:342942`
- Entity route: `{'bgg_id': 342942, 'title': 'Ark Nova'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.0822664584959667 | `review_digest` | Ark Nova | `reviews:bgg:342942:digest:rag-v0.1` |
| 2 | 0.03252247488101534 | `review_digest` | 5x5 Zoo | `reviews:bgg:307722:digest:rag-v0.1` |
| 3 | 0.031754032258064516 | `review_digest` | Zoo Tycoon: The Board Game | `reviews:bgg:370757:digest:rag-v0.1` |
| 4 | 0.03125763125763126 | `review_digest` | Zoo Food | `reviews:bgg:15147:digest:rag-v0.1` |
| 5 | 0.030303030303030304 | `review_digest` | Ark of Animals | `reviews:bgg:155113:digest:rag-v0.1` |

### PASS: `g005_cn_theme` - `方舟动物园 动物园 卡牌轮抽 机制`

- Expected: `game:bgg:342942`
- Entity route: `{'bgg_id': 342942, 'title': 'Ark Nova'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Ark Nova | `game:bgg:342942:overview:rag-v0.1` |
| 2 | 0.03125763125763126 | `game_overview` | Nova's Ark | `game:bgg:97312:overview:rag-v0.1` |
| 3 | 0.02964254577157803 | `game_overview` | Ark | `game:bgg:19947:overview:rag-v0.1` |
| 4 | 0.028258706467661692 | `game_overview` | Streichel-Zoo | `game:bgg:110842:overview:rag-v0.1` |
| 5 | 0.02797067901234568 | `game_overview` | 5x5 Zoo | `game:bgg:307722:overview:rag-v0.1` |

### PASS: `g006_cn_overview` - `幽港迷城 游戏简介`

- Expected: `game:bgg:174430`
- Entity route: `{'bgg_id': 174430, 'title': 'Gloomhaven'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.0822664584959667 | `game_overview` | Gloomhaven | `game:bgg:174430:overview:rag-v0.1` |
| 2 | 0.030621785881252923 | `game_overview` | Gloomhaven: Second Edition | `game:bgg:390478:overview:rag-v0.1` |
| 3 | 0.030330882352941176 | `game_overview` | Gloomhaven: Jaws of the Lion | `game:bgg:291457:overview:rag-v0.1` |
| 4 | 0.03028233151183971 | `game_overview` | Frosthaven | `game:bgg:295770:overview:rag-v0.1` |
| 5 | 0.029437229437229435 | `game_overview` | Dragoneart Fantasy-Card Game Book | `game:bgg:223610:overview:rag-v0.1` |

### PASS: `g006_cn_review` - `幽港迷城 玩家评论`

- Expected: `reviews:bgg:174430`
- Entity route: `{'bgg_id': 174430, 'title': 'Gloomhaven'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `review_digest` | Gloomhaven | `reviews:bgg:174430:digest:rag-v0.1` |
| 2 | 0.031009615384615385 | `review_digest` | Gloomholdin' | `reviews:bgg:340909:digest:rag-v0.1` |
| 3 | 0.030017921146953404 | `review_digest` | Gloomhaven: Jaws of the Lion | `reviews:bgg:291457:digest:rag-v0.1` |
| 4 | 0.029906956136464335 | `review_digest` | Melee & Wizard | `reviews:bgg:263996:digest:rag-v0.1` |
| 5 | 0.02964426877470356 | `review_digest` | Oathsworn: Into the Deepwood | `reviews:bgg:251661:digest:rag-v0.1` |

### PASS: `g006_cn_theme` - `幽港迷城 合作 战役 战术 机制`

- Expected: `game:bgg:174430`
- Entity route: `{'bgg_id': 174430, 'title': 'Gloomhaven'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08201844262295083 | `game_overview` | Gloomhaven | `game:bgg:174430:overview:rag-v0.1` |
| 2 | 0.03225806451612903 | `game_overview` | Gloomhaven: Jaws of the Lion | `game:bgg:291457:overview:rag-v0.1` |
| 3 | 0.03125763125763126 | `game_overview` | Trench Club: Legacy | `game:bgg:368939:overview:rag-v0.1` |
| 4 | 0.03036576949620428 | `game_overview` | Frosthaven | `game:bgg:295770:overview:rag-v0.1` |
| 5 | 0.030117753623188408 | `game_overview` | Gloomhaven: Second Edition | `game:bgg:390478:overview:rag-v0.1` |

### PASS: `g007_cn_overview` - `暮光帝国第四版 游戏简介`

- Expected: `game:bgg:233078`
- Entity route: `{'bgg_id': 233078, 'title': 'Twilight Imperium: Fourth Edition'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Twilight Imperium: Fourth Edition | `game:bgg:233078:overview:rag-v0.1` |
| 2 | 0.03225806451612903 | `game_overview` | Twilight Imperium | `game:bgg:24:overview:rag-v0.1` |
| 3 | 0.03149801587301587 | `game_overview` | Twilight Imperium: Second Edition | `game:bgg:26055:overview:rag-v0.1` |
| 4 | 0.03125763125763126 | `game_overview` | Twilight Imperium (Third Edition): Shattered Empire | `game:bgg:22821:overview:rag-v0.1` |
| 5 | 0.031009615384615385 | `game_overview` | Twilight Imperium: The Outer Rim | `game:bgg:6188:overview:rag-v0.1` |

### PASS: `g007_cn_review` - `暮光帝国第四版 玩家评论`

- Expected: `reviews:bgg:233078`
- Entity route: `{'bgg_id': 233078, 'title': 'Twilight Imperium: Fourth Edition'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `review_digest` | Twilight Imperium: Fourth Edition | `reviews:bgg:233078:digest:rag-v0.1` |
| 2 | 0.03200204813108039 | `review_digest` | Twilight Imperium: Second Edition | `reviews:bgg:26055:digest:rag-v0.1` |
| 3 | 0.03200204813108039 | `review_digest` | Twilight Imperium: Armada | `reviews:bgg:2902:digest:rag-v0.1` |
| 4 | 0.030776515151515152 | `review_digest` | Throneworld | `reviews:bgg:2844:digest:rag-v0.1` |
| 5 | 0.030776515151515152 | `review_digest` | Twilight Imperium | `reviews:bgg:24:digest:rag-v0.1` |

### PASS: `g007_cn_theme` - `暮光帝国第四版 太空 谈判 区域控制 机制`

- Expected: `game:bgg:233078`
- Entity route: `{'bgg_id': 233078, 'title': 'Twilight Imperium: Fourth Edition'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Twilight Imperium: Fourth Edition | `game:bgg:233078:overview:rag-v0.1` |
| 2 | 0.03200204813108039 | `game_overview` | Twilight Imperium | `game:bgg:24:overview:rag-v0.1` |
| 3 | 0.0315136476426799 | `game_overview` | Twilight Imperium (Third Edition): Shattered Empire | `game:bgg:22821:overview:rag-v0.1` |
| 4 | 0.03149801587301587 | `game_overview` | Twilight Imperium: Second Edition | `game:bgg:26055:overview:rag-v0.1` |
| 5 | 0.031009615384615385 | `game_overview` | Twilight Imperium: The Outer Rim | `game:bgg:6188:overview:rag-v0.1` |

### PASS: `g008_cn_overview` - `沙丘帝国 游戏简介`

- Expected: `game:bgg:316554`
- Entity route: `{'bgg_id': 316554, 'title': 'Dune: Imperium'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `game_overview` | Dune: Imperium | `game:bgg:316554:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | Dune: Imperium – Uprising | `game:bgg:397598:overview:rag-v0.1` |
| 3 | 0.030536130536130537 | `game_overview` | Twilight Imperium: Second Edition | `game:bgg:26055:overview:rag-v0.1` |
| 4 | 0.029411764705882353 | `game_overview` | Dune | `game:bgg:121:overview:rag-v0.1` |
| 5 | 0.027651515151515153 | `game_overview` | Imperium: The Contention | `game:bgg:266448:overview:rag-v0.1` |

### PASS: `g008_cn_review` - `沙丘帝国 玩家评论`

- Expected: `reviews:bgg:316554`
- Entity route: `{'bgg_id': 316554, 'title': 'Dune: Imperium'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `review_digest` | Dune: Imperium | `reviews:bgg:316554:digest:rag-v0.1` |
| 2 | 0.03252247488101534 | `review_digest` | Dune: Imperium – Uprising | `reviews:bgg:397598:digest:rag-v0.1` |
| 3 | 0.03149801587301587 | `review_digest` | Adventure Realms | `reviews:bgg:344974:digest:rag-v0.1` |
| 4 | 0.03055037313432836 | `review_digest` | Project Universe | `reviews:bgg:291221:digest:rag-v0.1` |
| 5 | 0.03036576949620428 | `review_digest` | Dune Express | `reviews:bgg:42617:digest:rag-v0.1` |

### PASS: `g008_cn_theme` - `沙丘帝国 牌库构筑 工人放置 机制`

- Expected: `game:bgg:316554`
- Entity route: `{'bgg_id': 316554, 'title': 'Dune: Imperium'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `game_overview` | Dune: Imperium | `game:bgg:316554:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | Dune: Imperium – Uprising | `game:bgg:397598:overview:rag-v0.1` |
| 3 | 0.03125 | `game_overview` | King's Town | `game:bgg:135757:overview:rag-v0.1` |
| 4 | 0.028205128205128206 | `game_overview` | Temp Worker Assassins | `game:bgg:198791:overview:rag-v0.1` |
| 5 | 0.026875901875901876 | `game_overview` | The Great Race | `game:bgg:296483:overview:rag-v0.1` |

### PASS: `g009_cn_overview` - `殖民火星 游戏简介`

- Expected: `game:bgg:167791`
- Entity route: `{'bgg_id': 167791, 'title': 'Terraforming Mars'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08201844262295083 | `game_overview` | Terraforming Mars | `game:bgg:167791:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | Terraforming Mars: Small Asteroid promo | `game:bgg:202825:overview:rag-v0.1` |
| 3 | 0.031754032258064516 | `game_overview` | Terraforming Mars: Ares Expedition | `game:bgg:328871:overview:rag-v0.1` |
| 4 | 0.031746031746031744 | `game_overview` | Terraforming Mars: The Dice Game | `game:bgg:296108:overview:rag-v0.1` |
| 5 | 0.030536130536130537 | `game_overview` | Terraforming Mars: Hellas & Elysium | `game:bgg:218127:overview:rag-v0.1` |

### PASS: `g009_cn_review` - `殖民火星 玩家评论`

- Expected: `reviews:bgg:167791`
- Entity route: `{'bgg_id': 167791, 'title': 'Terraforming Mars'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.0822664584959667 | `review_digest` | Terraforming Mars | `reviews:bgg:167791:digest:rag-v0.1` |
| 2 | 0.03252247488101534 | `review_digest` | Terraforming Mars: Ares Expedition | `reviews:bgg:328871:digest:rag-v0.1` |
| 3 | 0.03125763125763126 | `review_digest` | Legends of Void | `reviews:bgg:316795:digest:rag-v0.1` |
| 4 | 0.031009615384615385 | `review_digest` | TINYforming Mars | `reviews:bgg:282493:digest:rag-v0.1` |
| 5 | 0.03055037313432836 | `review_digest` | Terraforming Mars: The Dice Game | `reviews:bgg:296108:digest:rag-v0.1` |

### PASS: `g009_cn_theme` - `殖民火星 引擎构筑 版图放置 机制`

- Expected: `game:bgg:167791`
- Entity route: `{'bgg_id': 167791, 'title': 'Terraforming Mars'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08177805800756621 | `game_overview` | Terraforming Mars | `game:bgg:167791:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | Terraforming Mars: Small Asteroid promo | `game:bgg:202825:overview:rag-v0.1` |
| 3 | 0.03200204813108039 | `game_overview` | Terraforming Mars: The Dice Game | `game:bgg:296108:overview:rag-v0.1` |
| 4 | 0.03149801587301587 | `game_overview` | Terraforming Mars: Ares Expedition | `game:bgg:328871:overview:rag-v0.1` |
| 5 | 0.031009615384615385 | `game_overview` | Terraforming Mars: Hellas & Elysium | `game:bgg:218127:overview:rag-v0.1` |

### PASS: `g010_cn_overview` - `魔戒圣战 游戏简介`

- Expected: `game:bgg:115746`
- Entity route: `{'bgg_id': 115746, 'title': 'War of the Ring: Second Edition'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `game_overview` | War of the Ring: Second Edition | `game:bgg:115746:overview:rag-v0.1` |
| 2 | 0.032266458495966696 | `game_overview` | War of the Ring: Warriors of Middle-earth | `game:bgg:179404:overview:rag-v0.1` |
| 3 | 0.03055037313432836 | `game_overview` | War of the Ring Collector's Edition | `game:bgg:60153:overview:rag-v0.1` |
| 4 | 0.030536130536130537 | `game_overview` | War of the Ring - Scenario: The Breaking of the Fellowship | `game:bgg:188886:overview:rag-v0.1` |
| 5 | 0.030158730158730156 | `game_overview` | Chancellorsville (Second Edition) | `game:bgg:5778:overview:rag-v0.1` |

### PASS: `g010_cn_review` - `魔戒圣战 玩家评论`

- Expected: `reviews:bgg:115746`
- Entity route: `{'bgg_id': 115746, 'title': 'War of the Ring: Second Edition'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `review_digest` | War of the Ring: Second Edition | `reviews:bgg:115746:digest:rag-v0.1` |
| 2 | 0.03252247488101534 | `review_digest` | Kings of War (Second Edition) | `reviews:bgg:198670:digest:rag-v0.1` |
| 3 | 0.03149801587301587 | `review_digest` | Fantasy Pub (Second Edition) | `reviews:bgg:366974:digest:rag-v0.1` |
| 4 | 0.029957522915269395 | `review_digest` | War of the Ring | `reviews:bgg:42131:digest:rag-v0.1` |
| 5 | 0.029211087420042643 | `review_digest` | Rapid Fire! (Second Edition): Fast Play World War Two Wargames Rules | `reviews:bgg:20610:digest:rag-v0.1` |

### PASS: `g010_cn_theme` - `魔戒圣战 战争 掷骰 卡牌 机制`

- Expected: `game:bgg:115746`
- Entity route: `{'bgg_id': 115746, 'title': 'War of the Ring: Second Edition'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | War of the Ring: Second Edition | `game:bgg:115746:overview:rag-v0.1` |
| 2 | 0.03128054740957967 | `game_overview` | War of the Ring Collector's Edition | `game:bgg:60153:overview:rag-v0.1` |
| 3 | 0.03125763125763126 | `game_overview` | War of the Ring: Warriors of Middle-earth | `game:bgg:179404:overview:rag-v0.1` |
| 4 | 0.03125 | `game_overview` | War of the Ring - Scenario: The Breaking of the Fellowship | `game:bgg:188886:overview:rag-v0.1` |
| 5 | 0.02976190476190476 | `game_overview` | Hunt for the Ring | `game:bgg:216070:overview:rag-v0.1` |

### PASS: `g011_cn_overview` - `星球大战反叛 游戏简介`

- Expected: `game:bgg:187645`
- Entity route: `{'bgg_id': 187645, 'title': 'Star Wars: Rebellion'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Star Wars: Rebellion | `game:bgg:187645:overview:rag-v0.1` |
| 2 | 0.030776515151515152 | `game_overview` | Star Wars Campaign | `game:bgg:37511:overview:rag-v0.1` |
| 3 | 0.02964254577157803 | `game_overview` | Star Wars: Galaxy Rebellion | `game:bgg:183532:overview:rag-v0.1` |
| 4 | 0.02946912242686891 | `game_overview` | Star Wars: Star Battle | `game:bgg:190737:overview:rag-v0.1` |
| 5 | 0.029418126757516764 | `game_overview` | Star Wars: Empire vs. Rebellion | `game:bgg:160964:overview:rag-v0.1` |

### PASS: `g011_cn_review` - `星球大战反叛 玩家评论`

- Expected: `reviews:bgg:187645`
- Entity route: `{'bgg_id': 187645, 'title': 'Star Wars: Rebellion'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `review_digest` | Star Wars: Rebellion | `reviews:bgg:187645:digest:rag-v0.1` |
| 2 | 0.031754032258064516 | `review_digest` | Star Wars: Galaxy Rebellion | `reviews:bgg:183532:digest:rag-v0.1` |
| 3 | 0.030886196246139225 | `review_digest` | Mint Imperium | `reviews:bgg:382368:digest:rag-v0.1` |
| 4 | 0.030309988518943745 | `review_digest` | Liberation | `reviews:bgg:251442:digest:rag-v0.1` |
| 5 | 0.030303030303030304 | `review_digest` | Star Wars Fluxx | `reviews:bgg:246986:digest:rag-v0.1` |

### PASS: `g011_cn_theme` - `星球大战反叛 不对称 隐蔽移动 机制`

- Expected: `game:bgg:187645`
- Entity route: `{'bgg_id': 187645, 'title': 'Star Wars: Rebellion'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Star Wars: Rebellion | `game:bgg:187645:overview:rag-v0.1` |
| 2 | 0.03128054740957967 | `game_overview` | Star Wars Campaign | `game:bgg:37511:overview:rag-v0.1` |
| 3 | 0.031009615384615385 | `game_overview` | Star Wars: Star Battle | `game:bgg:190737:overview:rag-v0.1` |
| 4 | 0.030834914611005692 | `game_overview` | Star Wars: Galaxy Rebellion | `game:bgg:183532:overview:rag-v0.1` |
| 5 | 0.03057889822595705 | `game_overview` | Star Wars: Empire vs. Rebellion | `game:bgg:160964:overview:rag-v0.1` |

### PASS: `g012_cn_overview` - `灵迹岛 游戏简介`

- Expected: `game:bgg:162886`
- Entity route: `{'bgg_id': 162886, 'title': 'Spirit Island'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `game_overview` | Spirit Island | `game:bgg:162886:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | Horizons of Spirit Island | `game:bgg:367498:overview:rag-v0.1` |
| 3 | 0.031746031746031744 | `game_overview` | Spirit Island: Branch & Claw | `game:bgg:193065:overview:rag-v0.1` |
| 4 | 0.030117753623188408 | `game_overview` | 12 Realms: Promo Invaders Pack | `game:bgg:142728:overview:rag-v0.1` |
| 5 | 0.026333789329685362 | `game_overview` | Aloha: The Spirit of Hawaii | `game:bgg:130352:overview:rag-v0.1` |

### PASS: `g012_cn_review` - `灵迹岛 玩家评论`

- Expected: `reviews:bgg:162886`
- Entity route: `{'bgg_id': 162886, 'title': 'Spirit Island'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `review_digest` | Spirit Island | `reviews:bgg:162886:digest:rag-v0.1` |
| 2 | 0.03200204813108039 | `review_digest` | SPACE INVADERS: THE BOARD GAME | `reviews:bgg:279967:digest:rag-v0.1` |
| 3 | 0.030776515151515152 | `review_digest` | The Island | `reviews:bgg:70499:digest:rag-v0.1` |
| 4 | 0.030679156908665108 | `review_digest` | The Spirit of Eden | `reviews:bgg:344295:digest:rag-v0.1` |
| 5 | 0.03057889822595705 | `review_digest` | War Titans: Invaders Must Die! | `reviews:bgg:207203:digest:rag-v0.1` |

### PASS: `g012_cn_theme` - `灵迹岛 合作 可变玩家能力 机制`

- Expected: `game:bgg:162886`
- Entity route: `{'bgg_id': 162886, 'title': 'Spirit Island'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.0822664584959667 | `game_overview` | Spirit Island | `game:bgg:162886:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | Horizons of Spirit Island | `game:bgg:367498:overview:rag-v0.1` |
| 3 | 0.03200204813108039 | `game_overview` | Spirit Island: Branch & Claw | `game:bgg:193065:overview:rag-v0.1` |
| 4 | 0.031009615384615385 | `game_overview` | 12 Realms: Promo Invaders Pack | `game:bgg:142728:overview:rag-v0.1` |
| 5 | 0.027119252873563218 | `game_overview` | Kauri | `game:bgg:381188:overview:rag-v0.1` |

### PASS: `g013_cn_overview` - `狮子之颚 游戏简介`

- Expected: `game:bgg:291457`
- Entity route: `{'bgg_id': 291457, 'title': 'Gloomhaven: Jaws of the Lion'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Gloomhaven: Jaws of the Lion | `game:bgg:291457:overview:rag-v0.1` |
| 2 | 0.030090497737556562 | `game_overview` | Gloomhaven | `game:bgg:174430:overview:rag-v0.1` |
| 3 | 0.028438886647841874 | `game_overview` | Gloomhaven: Second Edition | `game:bgg:390478:overview:rag-v0.1` |
| 4 | 0.02719970792259949 | `game_overview` | Lion of Sinai | `game:bgg:225239:overview:rag-v0.1` |
| 5 | 0.02558175373709354 | `game_overview` | Frosthaven | `game:bgg:295770:overview:rag-v0.1` |

### PASS: `g013_cn_review` - `狮子之颚 玩家评论`

- Expected: `reviews:bgg:291457`
- Entity route: `{'bgg_id': 291457, 'title': 'Gloomhaven: Jaws of the Lion'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `review_digest` | Gloomhaven: Jaws of the Lion | `reviews:bgg:291457:digest:rag-v0.1` |
| 2 | 0.03200204813108039 | `review_digest` | Tidal Blades 2: Rise of the Unfolders | `reviews:bgg:233261:digest:rag-v0.1` |
| 3 | 0.03200204813108039 | `review_digest` | Gloomhaven: Buttons & Bugs | `reviews:bgg:393672:digest:rag-v0.1` |
| 4 | 0.03055037313432836 | `review_digest` | Funkoverse Strategy Game: Jaws 100 | `reviews:bgg:303036:digest:rag-v0.1` |
| 5 | 0.02964426877470356 | `review_digest` | Lion Rampant: Medieval Wargaming Rules Second Edition | `reviews:bgg:369011:digest:rag-v0.1` |

### PASS: `g013_cn_theme` - `狮子之颚 合作 战役 机制`

- Expected: `game:bgg:291457`
- Entity route: `{'bgg_id': 291457, 'title': 'Gloomhaven: Jaws of the Lion'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Gloomhaven: Jaws of the Lion | `game:bgg:291457:overview:rag-v0.1` |
| 2 | 0.03225806451612903 | `game_overview` | Trench Club: Legacy | `game:bgg:368939:overview:rag-v0.1` |
| 3 | 0.031009615384615385 | `game_overview` | Gloomhaven | `game:bgg:174430:overview:rag-v0.1` |
| 4 | 0.03036576949620428 | `game_overview` | Gloomhaven: Second Edition | `game:bgg:390478:overview:rag-v0.1` |
| 5 | 0.029910714285714284 | `game_overview` | Gascony's Legacy | `game:bgg:224793:overview:rag-v0.1` |

### PASS: `g014_cn_overview` - `盖亚计划 游戏简介`

- Expected: `game:bgg:220308`
- Entity route: `{'bgg_id': 220308, 'title': 'Gaia Project'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Gaia Project | `game:bgg:220308:overview:rag-v0.1` |
| 2 | 0.028125 | `game_overview` | A Handful of Stars | `game:bgg:197320:overview:rag-v0.1` |
| 3 | 0.027579737335834898 | `game_overview` | Quest for Gaia | `game:bgg:215029:overview:rag-v0.1` |
| 4 | 0.027500922849760058 | `game_overview` | Conquest of Gaia | `game:bgg:110341:overview:rag-v0.1` |
| 5 | 0.025451688923802042 | `game_overview` | Cargo Empire | `game:bgg:394512:overview:rag-v0.1` |

### PASS: `g014_cn_review` - `盖亚计划 玩家评论`

- Expected: `reviews:bgg:220308`
- Entity route: `{'bgg_id': 220308, 'title': 'Gaia Project'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `review_digest` | Gaia Project | `reviews:bgg:220308:digest:rag-v0.1` |
| 2 | 0.03225806451612903 | `review_digest` | Shapers of Gaia | `reviews:bgg:359587:digest:rag-v0.1` |
| 3 | 0.031009615384615385 | `review_digest` | National Economy Mecenat | `reviews:bgg:229527:digest:rag-v0.1` |
| 4 | 0.03057889822595705 | `review_digest` | Age of Innovation | `reviews:bgg:383179:digest:rag-v0.1` |
| 5 | 0.03057889822595705 | `review_digest` | Project Universe | `reviews:bgg:291221:digest:rag-v0.1` |

### PASS: `g014_cn_theme` - `盖亚计划 经济 网络建设 机制`

- Expected: `game:bgg:220308`
- Entity route: `{'bgg_id': 220308, 'title': 'Gaia Project'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Gaia Project | `game:bgg:220308:overview:rag-v0.1` |
| 2 | 0.0315136476426799 | `game_overview` | Next Station: London | `game:bgg:353545:overview:rag-v0.1` |
| 3 | 0.029910714285714284 | `game_overview` | Chaotic Connections | `game:bgg:104272:overview:rag-v0.1` |
| 4 | 0.028438886647841874 | `game_overview` | Airlines Europe: New Bonus Connections | `game:bgg:123504:overview:rag-v0.1` |
| 5 | 0.028404512489927477 | `game_overview` | En Route | `game:bgg:406454:overview:rag-v0.1` |

### PASS: `g015_cn_overview` - `冷战热斗 游戏简介`

- Expected: `game:bgg:12333`
- Entity route: `{'bgg_id': 12333, 'title': 'Twilight Struggle'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08154495777446598 | `game_overview` | Twilight Struggle | `game:bgg:12333:overview:rag-v0.1` |
| 2 | 0.031754032258064516 | `game_overview` | Twilight Struggle: "Referendum NATO" Promo Card | `game:bgg:123262:overview:rag-v0.1` |
| 3 | 0.031746031746031744 | `game_overview` | Twilight of Shogun | `game:bgg:184367:overview:rag-v0.1` |
| 4 | 0.0315136476426799 | `game_overview` | Twilight Struggle: Promo Deck | `game:bgg:190581:overview:rag-v0.1` |
| 5 | 0.030886196246139225 | `game_overview` | Twilight Struggle: "Anni di Piombo" Promo Card | `game:bgg:117145:overview:rag-v0.1` |

### PASS: `g015_cn_review` - `冷战热斗 玩家评论`

- Expected: `reviews:bgg:12333`
- Entity route: `{'bgg_id': 12333, 'title': 'Twilight Struggle'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.0822664584959667 | `review_digest` | Twilight Struggle | `reviews:bgg:12333:digest:rag-v0.1` |
| 2 | 0.03055037313432836 | `review_digest` | United Nations: A Game of World Domination in Our Time | `reviews:bgg:5798:digest:rag-v0.1` |
| 3 | 0.0304147465437788 | `review_digest` | Imperial Struggle | `reviews:bgg:206480:digest:rag-v0.1` |
| 4 | 0.030330882352941176 | `review_digest` | Twilight Struggle: Red Sea – Conflict in the Horn of Africa | `reviews:bgg:300192:digest:rag-v0.1` |
| 5 | 0.029437229437229435 | `review_digest` | SPARTA!: Struggle for Greece | `reviews:bgg:349779:digest:rag-v0.1` |

### PASS: `g015_cn_theme` - `冷战热斗 卡牌驱动 区域优势 机制`

- Expected: `game:bgg:12333`
- Entity route: `{'bgg_id': 12333, 'title': 'Twilight Struggle'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.081099324975892 | `game_overview` | Twilight Struggle | `game:bgg:12333:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | Twilight of Shogun | `game:bgg:184367:overview:rag-v0.1` |
| 3 | 0.03149801587301587 | `game_overview` | Twilight Struggle: "Referendum NATO" Promo Card | `game:bgg:123262:overview:rag-v0.1` |
| 4 | 0.03125763125763126 | `game_overview` | Twilight Struggle: Promo Deck | `game:bgg:190581:overview:rag-v0.1` |
| 5 | 0.031054405392392875 | `game_overview` | Twilight Struggle: "Anni di Piombo" Promo Card | `game:bgg:117145:overview:rag-v0.1` |

### PASS: `g016_cn_overview` - `历史巨轮 游戏简介`

- Expected: `game:bgg:182028`
- Entity route: `{'bgg_id': 182028, 'title': 'Through the Ages: A New Story of Civilization'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `game_overview` | Through the Ages: A New Story of Civilization | `game:bgg:182028:overview:rag-v0.1` |
| 2 | 0.03200204813108039 | `game_overview` | Through the Ages: A Story of Civilization | `game:bgg:25613:overview:rag-v0.1` |
| 3 | 0.028438886647841874 | `game_overview` | Cradle of Civilization | `game:bgg:4546:overview:rag-v0.1` |
| 4 | 0.028298204527712725 | `game_overview` | Guns & Steel: Renaissance | `game:bgg:197269:overview:rag-v0.1` |
| 5 | 0.027579737335834898 | `game_overview` | Age of Civilization | `game:bgg:264647:overview:rag-v0.1` |

### PASS: `g016_cn_review` - `历史巨轮 玩家评论`

- Expected: `reviews:bgg:182028`
- Entity route: `{'bgg_id': 182028, 'title': 'Through the Ages: A New Story of Civilization'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08201844262295083 | `review_digest` | Through the Ages: A New Story of Civilization | `reviews:bgg:182028:digest:rag-v0.1` |
| 2 | 0.032266458495966696 | `review_digest` | Cro-Magnon: First Steps of Civilization | `reviews:bgg:284323:digest:rag-v0.1` |
| 3 | 0.03200204813108039 | `review_digest` | Through the Ages: A Story of Civilization | `reviews:bgg:25613:digest:rag-v0.1` |
| 4 | 0.031754032258064516 | `review_digest` | Gibberers: The Word Game of Language Invention and Civilization Development | `reviews:bgg:380109:digest:rag-v0.1` |
| 5 | 0.029877369007803793 | `review_digest` | Cradle of Civilization | `reviews:bgg:266937:digest:rag-v0.1` |

### PASS: `g016_cn_theme` - `历史巨轮 文明 卡牌轮抽 机制`

- Expected: `game:bgg:182028`
- Entity route: `{'bgg_id': 182028, 'title': 'Through the Ages: A New Story of Civilization'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Through the Ages: A New Story of Civilization | `game:bgg:182028:overview:rag-v0.1` |
| 2 | 0.03225806451612903 | `game_overview` | Through the Ages: A Story of Civilization | `game:bgg:25613:overview:rag-v0.1` |
| 3 | 0.03055037313432836 | `game_overview` | Mosaic: A Story of Civilization | `game:bgg:329551:overview:rag-v0.1` |
| 4 | 0.030090497737556562 | `game_overview` | Civcards | `game:bgg:46390:overview:rag-v0.1` |
| 5 | 0.028484848484848488 | `game_overview` | Through the Ages: A Story of Civilization – Czech expansion | `game:bgg:98880:overview:rag-v0.1` |

### PASS: `g017_cn_overview` - `勃艮第城堡 游戏简介`

- Expected: `game:bgg:84876`
- Entity route: `{'bgg_id': 84876, 'title': 'The Castles of Burgundy'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.0822664584959667 | `game_overview` | The Castles of Burgundy | `game:bgg:84876:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | The Castles of Burgundy | `game:bgg:271320:overview:rag-v0.1` |
| 3 | 0.03125 | `game_overview` | The Castles of Burgundy: 3rd Expansion – German Board Game Championship Board 2013 | `game:bgg:139160:overview:rag-v0.1` |
| 4 | 0.030834914611005692 | `game_overview` | The Castles of Burgundy: 5th Expansion – Pleasure Garden | `game:bgg:166589:overview:rag-v0.1` |
| 5 | 0.03076923076923077 | `game_overview` | The Castles of Burgundy: 7th Expansion – German Board Game Championship Board 2016 | `game:bgg:193585:overview:rag-v0.1` |

### PASS: `g017_cn_review` - `勃艮第城堡 玩家评论`

- Expected: `reviews:bgg:84876`
- Entity route: `{'bgg_id': 84876, 'title': 'The Castles of Burgundy'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `review_digest` | The Castles of Burgundy | `reviews:bgg:84876:digest:rag-v0.1` |
| 2 | 0.03225806451612903 | `review_digest` | The Castles of Burgundy: The Dice Game | `reviews:bgg:232988:digest:rag-v0.1` |
| 3 | 0.03149801587301587 | `review_digest` | The Castles of Tuscany | `reviews:bgg:300327:digest:rag-v0.1` |
| 4 | 0.03149801587301587 | `review_digest` | The Castles of Burgundy: The Card Game | `reviews:bgg:191977:digest:rag-v0.1` |
| 5 | 0.03007688828584351 | `review_digest` | Sweet Lands | `reviews:bgg:425445:digest:rag-v0.1` |

### PASS: `g017_cn_theme` - `勃艮第城堡 掷骰 版图放置 机制`

- Expected: `game:bgg:84876`
- Entity route: `{'bgg_id': 84876, 'title': 'The Castles of Burgundy'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `game_overview` | The Castles of Burgundy | `game:bgg:84876:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | The Castles of Burgundy | `game:bgg:271320:overview:rag-v0.1` |
| 3 | 0.031746031746031744 | `game_overview` | The Castles of Burgundy: 3rd Expansion – German Board Game Championship Board 2013 | `game:bgg:139160:overview:rag-v0.1` |
| 4 | 0.031009615384615385 | `game_overview` | The Castles of Burgundy: 7th Expansion – German Board Game Championship Board 2016 | `game:bgg:193585:overview:rag-v0.1` |
| 5 | 0.031009615384615385 | `game_overview` | The Castles of Burgundy: 1st Expansion – New Player Boards | `game:bgg:110926:overview:rag-v0.1` |

### PASS: `g018_cn_overview` - `车票之旅 游戏简介`

- Expected: `game:bgg:9209`
- Entity route: `{'bgg_id': 9209, 'title': 'Ticket to Ride'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.07990695613646434 | `game_overview` | Ticket to Ride | `game:bgg:9209:overview:rag-v0.1` |
| 2 | 0.02938045560996381 | `game_overview` | Ticket to Ride: 10th Anniversary | `game:bgg:160069:overview:rag-v0.1` |
| 3 | 0.029116045245077504 | `game_overview` | Ticket to Ride: The Dice Expansion | `game:bgg:38454:overview:rag-v0.1` |
| 4 | 0.029083245521601686 | `game_overview` | Ticket to Ride: Ghost Train | `game:bgg:366488:overview:rag-v0.1` |
| 5 | 0.02832415420928403 | `game_overview` | Castilla y León (fan expansion for Ticket to Ride) | `game:bgg:70712:overview:rag-v0.1` |

### PASS: `g018_cn_review` - `车票之旅 玩家评论`

- Expected: `reviews:bgg:9209`
- Entity route: `{'bgg_id': 9209, 'title': 'Ticket to Ride'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.06639344262295083 | `review_digest` | Ticket to Ride | `reviews:bgg:9209:digest:rag-v0.1` |
| 2 | 0.03225806451612903 | `review_digest` | Ticket to Ride Demo | `reviews:bgg:244525:digest:rag-v0.1` |
| 3 | 0.03149801587301587 | `review_digest` | Ticket to Ride: Nordic Countries | `reviews:bgg:31627:digest:rag-v0.1` |
| 4 | 0.03131881575727918 | `review_digest` | Spike | `reviews:bgg:165876:digest:rag-v0.1` |
| 5 | 0.03125763125763126 | `review_digest` | Ticket to Ride: Ghost Train | `reviews:bgg:366488:digest:rag-v0.1` |

### PASS: `g018_cn_theme` - `车票之旅 路线建设 成套收集 机制`

- Expected: `game:bgg:9209`
- Entity route: `{'bgg_id': 9209, 'title': 'Ticket to Ride'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08009207275993713 | `game_overview` | Ticket to Ride | `game:bgg:9209:overview:rag-v0.1` |
| 2 | 0.03149801587301587 | `game_overview` | Holland (fan expansion for Ticket to Ride) | `game:bgg:130183:overview:rag-v0.1` |
| 3 | 0.030886196246139225 | `game_overview` | Ticket to Ride: 10th Anniversary | `game:bgg:160069:overview:rag-v0.1` |
| 4 | 0.030536130536130537 | `game_overview` | Extension France (fan expansion for Ticket to Ride) | `game:bgg:123217:overview:rag-v0.1` |
| 5 | 0.030536130536130537 | `game_overview` | Sweden (fan expansion for Ticket to Ride) | `game:bgg:130182:overview:rag-v0.1` |

### PASS: `g019_cn_overview` - `皇舆争霸 游戏简介`

- Expected: `game:bgg:36218`
- Entity route: `{'bgg_id': 36218, 'title': 'Dominion'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.06639344262295083 | `game_overview` | Dominion | `game:bgg:36218:overview:rag-v0.1` |
| 2 | 0.03225806451612903 | `game_overview` | Dominion: Black Market Promo Card | `game:bgg:41105:overview:rag-v0.1` |
| 3 | 0.03149801587301587 | `game_overview` | Dominion Big Box (German) | `game:bgg:142132:overview:rag-v0.1` |
| 4 | 0.028991596638655463 | `game_overview` | Dominion: Envoy Promo Card | `game:bgg:39707:overview:rag-v0.1` |
| 5 | 0.027149321266968326 | `game_overview` | Dominion (Second Edition) Big Box | `game:bgg:216849:overview:rag-v0.1` |

### PASS: `g019_cn_review` - `皇舆争霸 玩家评论`

- Expected: `reviews:bgg:36218`
- Entity route: `{'bgg_id': 36218, 'title': 'Dominion'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08028233151183971 | `review_digest` | Dominion | `reviews:bgg:36218:digest:rag-v0.1` |
| 2 | 0.03200204813108039 | `review_digest` | Heart of Crown | `reviews:bgg:131904:digest:rag-v0.1` |
| 3 | 0.03177805800756621 | `review_digest` | Heart of Crown: Fairy Garden | `reviews:bgg:156372:digest:rag-v0.1` |
| 4 | 0.03125 | `review_digest` | Het Koninkrijk Dominion | `reviews:bgg:184207:digest:rag-v0.1` |
| 5 | 0.030621785881252923 | `review_digest` | Dominion | `reviews:bgg:64777:digest:rag-v0.1` |

### PASS: `g019_cn_theme` - `皇舆争霸 牌库构筑 手牌管理 机制`

- Expected: `game:bgg:36218`
- Entity route: `{'bgg_id': 36218, 'title': 'Dominion'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.06639344262295083 | `game_overview` | Dominion | `game:bgg:36218:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | Dominion: Black Market Promo Card | `game:bgg:41105:overview:rag-v0.1` |
| 3 | 0.03200204813108039 | `game_overview` | Dominion Big Box (German) | `game:bgg:142132:overview:rag-v0.1` |
| 4 | 0.03036576949620428 | `game_overview` | Dominion: Envoy Promo Card | `game:bgg:39707:overview:rag-v0.1` |
| 5 | 0.030117753623188408 | `game_overview` | Dominion (Second Edition) Big Box | `game:bgg:216849:overview:rag-v0.1` |

### PASS: `g020_cn_overview` - `行动代号 游戏简介`

- Expected: `game:bgg:178900`
- Entity route: `{'bgg_id': 178900, 'title': 'Codenames'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Codenames | `game:bgg:178900:overview:rag-v0.1` |
| 2 | 0.0315136476426799 | `game_overview` | Codenames: Deep Undercover | `game:bgg:205158:overview:rag-v0.1` |
| 3 | 0.031024531024531024 | `game_overview` | Codenames: Pictures | `game:bgg:198773:overview:rag-v0.1` |
| 4 | 0.030834914611005692 | `game_overview` | Codenames: Bonuskaarten 2016 | `game:bgg:225039:overview:rag-v0.1` |
| 5 | 0.03055037313432836 | `game_overview` | Codenames: Harry Potter | `game:bgg:249821:overview:rag-v0.1` |

### PASS: `g020_cn_review` - `行动代号 玩家评论`

- Expected: `reviews:bgg:178900`
- Entity route: `{'bgg_id': 178900, 'title': 'Codenames'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.07905167047105209 | `review_digest` | Codenames | `reviews:bgg:178900:digest:rag-v0.1` |
| 2 | 0.031099324975891997 | `review_digest` | The Only Word: the Party Word Game | `reviews:bgg:283849:digest:rag-v0.1` |
| 3 | 0.030798389007344232 | `review_digest` | So Clover! | `reviews:bgg:329839:digest:rag-v0.1` |
| 4 | 0.02946912242686891 | `review_digest` | Phantom Ink | `reviews:bgg:330592:digest:rag-v0.1` |
| 5 | 0.0293236301369863 | `review_digest` | 13 Words | `reviews:bgg:363039:digest:rag-v0.1` |

### PASS: `g020_cn_theme` - `行动代号 词语 联想 推理 机制`

- Expected: `game:bgg:178900`
- Entity route: `{'bgg_id': 178900, 'title': 'Codenames'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Codenames | `game:bgg:178900:overview:rag-v0.1` |
| 2 | 0.03128054740957967 | `game_overview` | Codenames: Deep Undercover | `game:bgg:205158:overview:rag-v0.1` |
| 3 | 0.030834914611005692 | `game_overview` | Codenames: Bonuskaarten 2016 | `game:bgg:225039:overview:rag-v0.1` |
| 4 | 0.030798389007344232 | `game_overview` | Codenames: Pictures | `game:bgg:198773:overview:rag-v0.1` |
| 5 | 0.030309988518943745 | `game_overview` | Codenames: Harry Potter | `game:bgg:249821:overview:rag-v0.1` |

### PASS: `g021_cn_overview` - `花砖物语 游戏简介`

- Expected: `game:bgg:230802`
- Entity route: `{'bgg_id': 230802, 'title': 'Azul'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.0822664584959667 | `game_overview` | Azul | `game:bgg:230802:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | Azul: Master Chocolatier | `game:bgg:363247:overview:rag-v0.1` |
| 3 | 0.0315136476426799 | `game_overview` | Azul: Stained Glass of Sintra | `game:bgg:256226:overview:rag-v0.1` |
| 4 | 0.03149801587301587 | `game_overview` | Azul: Queen's Garden | `game:bgg:346965:overview:rag-v0.1` |
| 5 | 0.030536130536130537 | `game_overview` | Azul: Summer Pavilion | `game:bgg:287954:overview:rag-v0.1` |

### PASS: `g021_cn_review` - `花砖物语 玩家评论`

- Expected: `reviews:bgg:230802`
- Entity route: `{'bgg_id': 230802, 'title': 'Azul'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.0822664584959667 | `review_digest` | Azul | `reviews:bgg:230802:digest:rag-v0.1` |
| 2 | 0.03225806451612903 | `review_digest` | Portals | `reviews:bgg:386168:digest:rag-v0.1` |
| 3 | 0.030886196246139225 | `review_digest` | Cloomba | `reviews:bgg:261683:digest:rag-v0.1` |
| 4 | 0.030776515151515152 | `review_digest` | Azul: Summer Pavilion | `reviews:bgg:287954:digest:rag-v0.1` |
| 5 | 0.03057889822595705 | `review_digest` | Azul: Stained Glass of Sintra | `reviews:bgg:256226:digest:rag-v0.1` |

### PASS: `g021_cn_theme` - `花砖物语 选牌 图案构筑 机制`

- Expected: `game:bgg:230802`
- Entity route: `{'bgg_id': 230802, 'title': 'Azul'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Azul | `game:bgg:230802:overview:rag-v0.1` |
| 2 | 0.03200204813108039 | `game_overview` | Azul: Master Chocolatier | `game:bgg:363247:overview:rag-v0.1` |
| 3 | 0.031754032258064516 | `game_overview` | Azul: Stained Glass of Sintra | `game:bgg:256226:overview:rag-v0.1` |
| 4 | 0.03149801587301587 | `game_overview` | Azul: Queen's Garden | `game:bgg:346965:overview:rag-v0.1` |
| 5 | 0.03076923076923077 | `game_overview` | Azul: Summer Pavilion | `game:bgg:287954:overview:rag-v0.1` |

### PASS: `g022_cn_overview` - `璀璨宝石 游戏简介`

- Expected: `game:bgg:148228`
- Entity route: `{'bgg_id': 148228, 'title': 'Splendor'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08154495777446598 | `game_overview` | Splendor | `game:bgg:148228:overview:rag-v0.1` |
| 2 | 0.03149801587301587 | `game_overview` | Splendor Duel | `game:bgg:364073:overview:rag-v0.1` |
| 3 | 0.027071520029266508 | `game_overview` | Splendor: Marvel | `game:bgg:293296:overview:rag-v0.1` |
| 4 | 0.02701252236135957 | `game_overview` | Splendor: Special Noble Patron | `game:bgg:190036:overview:rag-v0.1` |
| 5 | 0.026289682539682536 | `game_overview` | Splendor: Nobles Promo Tiles | `game:bgg:178742:overview:rag-v0.1` |

### PASS: `g022_cn_review` - `璀璨宝石 玩家评论`

- Expected: `reviews:bgg:148228`
- Entity route: `{'bgg_id': 148228, 'title': 'Splendor'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `review_digest` | Splendor | `reviews:bgg:148228:digest:rag-v0.1` |
| 2 | 0.03200204813108039 | `review_digest` | Space Explorers | `reviews:bgg:235817:digest:rag-v0.1` |
| 3 | 0.03125763125763126 | `review_digest` | Century: Spice Road | `reviews:bgg:209685:digest:rag-v0.1` |
| 4 | 0.031009615384615385 | `review_digest` | Shadows of Macao | `reviews:bgg:276023:digest:rag-v0.1` |
| 5 | 0.030886196246139225 | `review_digest` | Kardashev Scale | `reviews:bgg:341548:digest:rag-v0.1` |

### PASS: `g022_cn_theme` - `璀璨宝石 引擎构筑 成套收集 机制`

- Expected: `game:bgg:148228`
- Entity route: `{'bgg_id': 148228, 'title': 'Splendor'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08278688524590164 | `game_overview` | Splendor | `game:bgg:148228:overview:rag-v0.1` |
| 2 | 0.0315136476426799 | `game_overview` | Splendor Duel | `game:bgg:364073:overview:rag-v0.1` |
| 3 | 0.03149801587301587 | `game_overview` | Splendor: AsmOPlay Kit | `game:bgg:191361:overview:rag-v0.1` |
| 4 | 0.030798389007344232 | `game_overview` | Starstead | `game:bgg:147256:overview:rag-v0.1` |
| 5 | 0.030330882352941176 | `game_overview` | Splendor: Nobles Promo Tiles | `game:bgg:178742:overview:rag-v0.1` |

### PASS: `g023_cn_overview` - `情书 游戏简介`

- Expected: `game:bgg:129622`
- Entity route: `{'bgg_id': 129622, 'title': 'Love Letter'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.07788769549651405 | `game_overview` | Love Letter | `game:bgg:129622:overview:rag-v0.1` |
| 2 | 0.03055037313432836 | `game_overview` | Love Letter: Princess Princess Ever After | `game:bgg:339905:overview:rag-v0.1` |
| 3 | 0.029857397504456328 | `game_overview` | Love Letter: Premium Edition | `game:bgg:196326:overview:rag-v0.1` |
| 4 | 0.02878726010616578 | `game_overview` | Big Love Letter | `game:bgg:224259:overview:rag-v0.1` |
| 5 | 0.028693528693528692 | `game_overview` | Love Letter: Erweiterung | `game:bgg:219182:overview:rag-v0.1` |

### PASS: `g023_cn_review` - `情书 玩家评论`

- Expected: `reviews:bgg:129622`
- Entity route: `{'bgg_id': 129622, 'title': 'Love Letter'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.06639344262295083 | `review_digest` | Love Letter | `reviews:bgg:129622:digest:rag-v0.1` |
| 2 | 0.032018442622950824 | `review_digest` | Mad Love | `reviews:bgg:194998:digest:rag-v0.1` |
| 3 | 0.0315136476426799 | `review_digest` | Love Letter: 2nd Edition | `reviews:bgg:361207:digest:rag-v0.1` |
| 4 | 0.03125763125763126 | `review_digest` | Cypher | `reviews:bgg:163354:digest:rag-v0.1` |
| 5 | 0.03057889822595705 | `review_digest` | Quick Stop | `reviews:bgg:425533:digest:rag-v0.1` |

### PASS: `g023_cn_theme` - `情书 推理 手牌管理 机制`

- Expected: `game:bgg:129622`
- Entity route: `{'bgg_id': 129622, 'title': 'Love Letter'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08009207275993713 | `game_overview` | Love Letter | `game:bgg:129622:overview:rag-v0.1` |
| 2 | 0.03177805800756621 | `game_overview` | Love Letter: Princess Princess Ever After | `game:bgg:339905:overview:rag-v0.1` |
| 3 | 0.0315136476426799 | `game_overview` | Big Love Letter | `game:bgg:224259:overview:rag-v0.1` |
| 4 | 0.03128054740957967 | `game_overview` | Love Letter: Premium Edition | `game:bgg:196326:overview:rag-v0.1` |
| 5 | 0.030798389007344232 | `game_overview` | Love Letter: Erweiterung | `game:bgg:219182:overview:rag-v0.1` |

### PASS: `g024_cn_overview` - `瘟疫危机 游戏简介`

- Expected: `game:bgg:30549`
- Entity route: `{'bgg_id': 30549, 'title': 'Pandemic'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08154495777446598 | `game_overview` | Pandemic | `game:bgg:30549:overview:rag-v0.1` |
| 2 | 0.032018442622950824 | `game_overview` | Pandemic Legacy: Season 1 | `game:bgg:161936:overview:rag-v0.1` |
| 3 | 0.03200204813108039 | `game_overview` | Pandemic: State of Emergency | `game:bgg:168703:overview:rag-v0.1` |
| 4 | 0.03200204813108039 | `game_overview` | Pandemic: On the Brink | `game:bgg:40849:overview:rag-v0.1` |
| 5 | 0.030776515151515152 | `game_overview` | Pandemic: The Cure | `game:bgg:150658:overview:rag-v0.1` |

### PASS: `g024_cn_review` - `瘟疫危机 玩家评论`

- Expected: `reviews:bgg:30549`
- Entity route: `{'bgg_id': 30549, 'title': 'Pandemic'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08131881575727917 | `review_digest` | Pandemic | `reviews:bgg:30549:digest:rag-v0.1` |
| 2 | 0.03252247488101534 | `review_digest` | Moving Pictures: Dinosaur Outbreak! | `reviews:bgg:352605:digest:rag-v0.1` |
| 3 | 0.031746031746031744 | `review_digest` | Pandemic: Contagion | `reviews:bgg:157789:digest:rag-v0.1` |
| 4 | 0.0315136476426799 | `review_digest` | Kings of Israel | `reviews:bgg:142084:digest:rag-v0.1` |
| 5 | 0.029709507042253523 | `review_digest` | Pandemic: Rising Tide | `reviews:bgg:234671:digest:rag-v0.1` |

### PASS: `g024_cn_theme` - `瘟疫危机 合作 行动点 机制`

- Expected: `game:bgg:30549`
- Entity route: `{'bgg_id': 30549, 'title': 'Pandemic'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08154495777446598 | `game_overview` | Pandemic | `game:bgg:30549:overview:rag-v0.1` |
| 2 | 0.032018442622950824 | `game_overview` | Pandemic Legacy: Season 1 | `game:bgg:161936:overview:rag-v0.1` |
| 3 | 0.03200204813108039 | `game_overview` | Pandemic: On the Brink | `game:bgg:40849:overview:rag-v0.1` |
| 4 | 0.0315136476426799 | `game_overview` | Pandemic: State of Emergency | `game:bgg:168703:overview:rag-v0.1` |
| 5 | 0.029910714285714284 | `game_overview` | Pandemic: Hot Zone – North America | `game:bgg:301919:overview:rag-v0.1` |

### PASS: `g025_cn_overview` - `七大奇迹 游戏简介`

- Expected: `game:bgg:68448`
- Entity route: `{'bgg_id': 68448, 'title': '7 Wonders'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.07844163539403516 | `game_overview` | 7 Wonders | `game:bgg:68448:overview:rag-v0.1` |
| 2 | 0.032266458495966696 | `game_overview` | More Wonders... (fan expansion for 7 Wonders) | `game:bgg:131947:overview:rag-v0.1` |
| 3 | 0.03225806451612903 | `game_overview` | 7 Wonders: Leaders – Nimrod | `game:bgg:166329:overview:rag-v0.1` |
| 4 | 0.030798389007344232 | `game_overview` | 7 Wonders: Leaders – Louis | `game:bgg:127838:overview:rag-v0.1` |
| 5 | 0.030330882352941176 | `game_overview` | Game Wonders (fan expansion for 7 Wonders) | `game:bgg:138187:overview:rag-v0.1` |

### PASS: `g025_cn_review` - `七大奇迹 玩家评论`

- Expected: `reviews:bgg:68448`
- Entity route: `{'bgg_id': 68448, 'title': '7 Wonders'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.07889344262295082 | `review_digest` | 7 Wonders | `reviews:bgg:68448:digest:rag-v0.1` |
| 2 | 0.031754032258064516 | `review_digest` | 7 Dice Wonders | `reviews:bgg:143085:digest:rag-v0.1` |
| 3 | 0.031099324975891997 | `review_digest` | Reflections in the Looking Glass | `reviews:bgg:377943:digest:rag-v0.1` |
| 4 | 0.030621785881252923 | `review_digest` | Chamber of Wonders | `reviews:bgg:329400:digest:rag-v0.1` |
| 5 | 0.03007688828584351 | `review_digest` | Age of Wonders: Planetfall | `reviews:bgg:353848:digest:rag-v0.1` |

### PASS: `g025_cn_theme` - `七大奇迹 卡牌轮抽 文明 机制`

- Expected: `game:bgg:68448`
- Entity route: `{'bgg_id': 68448, 'title': '7 Wonders'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08131881575727917 | `game_overview` | 7 Wonders | `game:bgg:68448:overview:rag-v0.1` |
| 2 | 0.03200204813108039 | `game_overview` | More Wonders... (fan expansion for 7 Wonders) | `game:bgg:131947:overview:rag-v0.1` |
| 3 | 0.03200204813108039 | `game_overview` | 7 Wonders: Leaders – Nimrod | `game:bgg:166329:overview:rag-v0.1` |
| 4 | 0.031099324975891997 | `game_overview` | 7 Wonders (Second Edition) | `game:bgg:316377:overview:rag-v0.1` |
| 5 | 0.03055037313432836 | `game_overview` | 7 Wonders: Leaders – Louis | `game:bgg:127838:overview:rag-v0.1` |

### PASS: `g026_cn_overview` - `妙语说书人 游戏简介`

- Expected: `game:bgg:39856`
- Entity route: `{'bgg_id': 39856, 'title': 'Dixit'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.0787391216352965 | `game_overview` | Dixit | `game:bgg:39856:overview:rag-v0.1` |
| 2 | 0.031754032258064516 | `game_overview` | Dixit Demo Deck | `game:bgg:284007:overview:rag-v0.1` |
| 3 | 0.030886196246139225 | `game_overview` | Dixit: Journey | `game:bgg:121288:overview:rag-v0.1` |
| 4 | 0.030834914611005692 | `game_overview` | Dixit: "Magic bunny" promo card | `game:bgg:212802:overview:rag-v0.1` |
| 5 | 0.03055037313432836 | `game_overview` | Dixit: Spielbox 03/15 Promo Card | `game:bgg:179060:overview:rag-v0.1` |

### PASS: `g026_cn_review` - `妙语说书人 玩家评论`

- Expected: `reviews:bgg:39856`
- Entity route: `{'bgg_id': 39856, 'title': 'Dixit'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.081099324975892 | `review_digest` | Dixit | `reviews:bgg:39856:digest:rag-v0.1` |
| 2 | 0.03125763125763126 | `review_digest` | Keepers | `reviews:bgg:362106:digest:rag-v0.1` |
| 3 | 0.030621785881252923 | `review_digest` | Dixit Demo Deck | `reviews:bgg:284007:digest:rag-v0.1` |
| 4 | 0.03055037313432836 | `review_digest` | Mood X | `reviews:bgg:162223:digest:rag-v0.1` |
| 5 | 0.030536130536130537 | `review_digest` | The Hollow Woods: Storytelling Card Game | `reviews:bgg:236537:digest:rag-v0.1` |

### PASS: `g026_cn_theme` - `妙语说书人 讲故事 投票 机制`

- Expected: `game:bgg:39856`
- Entity route: `{'bgg_id': 39856, 'title': 'Dixit'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.0776293976791306 | `game_overview` | Dixit | `game:bgg:39856:overview:rag-v0.1` |
| 2 | 0.031754032258064516 | `game_overview` | Dixit Demo Deck | `game:bgg:284007:overview:rag-v0.1` |
| 3 | 0.031009615384615385 | `game_overview` | Dixit: Spielbox 03/15 Promo Card | `game:bgg:179060:overview:rag-v0.1` |
| 4 | 0.030621785881252923 | `game_overview` | Dixit: "Magic bunny" promo card | `game:bgg:212802:overview:rag-v0.1` |
| 5 | 0.030309988518943745 | `game_overview` | Dixit: "Pumpkinhead" and "Santa" promo cards | `game:bgg:169639:overview:rag-v0.1` |

### PASS: `g027_cn_overview` - `拼布艺术 游戏简介`

- Expected: `game:bgg:163412`
- Entity route: `{'bgg_id': 163412, 'title': 'Patchwork'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `game_overview` | Patchwork | `game:bgg:163412:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | Stack'n Stuff: A Patchwork Game | `game:bgg:362693:overview:rag-v0.1` |
| 3 | 0.031746031746031744 | `game_overview` | Patchwork Express | `game:bgg:246639:overview:rag-v0.1` |
| 4 | 0.028612012987012988 | `game_overview` | Patchwork Doodle | `game:bgg:264239:overview:rag-v0.1` |
| 5 | 0.02719970792259949 | `game_overview` | Puzzle-Memo | `game:bgg:288969:overview:rag-v0.1` |

### PASS: `g027_cn_review` - `拼布艺术 玩家评论`

- Expected: `reviews:bgg:163412`
- Entity route: `{'bgg_id': 163412, 'title': 'Patchwork'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08131881575727917 | `review_digest` | Patchwork | `reviews:bgg:163412:digest:rag-v0.1` |
| 2 | 0.0315136476426799 | `review_digest` | Stack'n Stuff: A Patchwork Game | `reviews:bgg:362693:digest:rag-v0.1` |
| 3 | 0.03149801587301587 | `review_digest` | Flower Fields | `reviews:bgg:424577:digest:rag-v0.1` |
| 4 | 0.03149801587301587 | `review_digest` | Happy Home | `reviews:bgg:419997:digest:rag-v0.1` |
| 5 | 0.031054405392392875 | `review_digest` | Nova Luna | `reviews:bgg:284435:digest:rag-v0.1` |

### PASS: `g027_cn_theme` - `拼布艺术 双人 拼放版图 机制`

- Expected: `game:bgg:163412`
- Entity route: `{'bgg_id': 163412, 'title': 'Patchwork'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08252247488101534 | `game_overview` | Patchwork | `game:bgg:163412:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | Stack'n Stuff: A Patchwork Game | `game:bgg:362693:overview:rag-v0.1` |
| 3 | 0.029910714285714284 | `game_overview` | Patchwork Express | `game:bgg:246639:overview:rag-v0.1` |
| 4 | 0.027745885954841176 | `game_overview` | Trick Track | `game:bgg:140798:overview:rag-v0.1` |
| 5 | 0.026631393298059962 | `game_overview` | Jarl: The Vikings Tile-Laying Game | `game:bgg:170901:overview:rag-v0.1` |

### PASS: `g028_cn_overview` - `小世界 游戏简介`

- Expected: `game:bgg:40692`
- Entity route: `{'bgg_id': 40692, 'title': 'Small World'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.081099324975892 | `game_overview` | Small World | `game:bgg:40692:overview:rag-v0.1` |
| 2 | 0.03125763125763126 | `game_overview` | Small World: Be Not Afraid... | `game:bgg:81618:overview:rag-v0.1` |
| 3 | 0.03007688828584351 | `game_overview` | Conquest of Gaia | `game:bgg:110341:overview:rag-v0.1` |
| 4 | 0.027402402402402402 | `game_overview` | Small World: Royal Bonus | `game:bgg:144171:overview:rag-v0.1` |
| 5 | 0.02501516070345664 | `game_overview` | Warhammer: Conquest of the New World | `game:bgg:163092:overview:rag-v0.1` |

### PASS: `g028_cn_review` - `小世界 玩家评论`

- Expected: `reviews:bgg:40692`
- Entity route: `{'bgg_id': 40692, 'title': 'Small World'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.081099324975892 | `review_digest` | Small World | `reviews:bgg:40692:digest:rag-v0.1` |
| 2 | 0.03149801587301587 | `review_digest` | Crimea: Conquest & Liberation | `reviews:bgg:387483:digest:rag-v0.1` |
| 3 | 0.030679156908665108 | `review_digest` | Le Saghe di Conquest | `reviews:bgg:8476:digest:rag-v0.1` |
| 4 | 0.029418126757516764 | `review_digest` | Historical Conquest: The Card Game | `reviews:bgg:139456:digest:rag-v0.1` |
| 5 | 0.029386529386529386 | `review_digest` | Conquest Tactics | `reviews:bgg:94633:digest:rag-v0.1` |

### PASS: `g028_cn_theme` - `小世界 区域控制 可变玩家能力 机制`

- Expected: `game:bgg:40692`
- Entity route: `{'bgg_id': 40692, 'title': 'Small World'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08047794966520434 | `game_overview` | Small World | `game:bgg:40692:overview:rag-v0.1` |
| 2 | 0.032266458495966696 | `game_overview` | Small World: Be Not Afraid... | `game:bgg:81618:overview:rag-v0.1` |
| 3 | 0.03128054740957967 | `game_overview` | Conquest of Gaia | `game:bgg:110341:overview:rag-v0.1` |
| 4 | 0.030090497737556562 | `game_overview` | Small World: Royal Bonus | `game:bgg:144171:overview:rag-v0.1` |
| 5 | 0.02854251012145749 | `game_overview` | Zeppelin Conquest | `game:bgg:154521:overview:rag-v0.1` |

### PASS: `g029_cn_overview` - `花火 游戏简介`

- Expected: `game:bgg:98778`
- Entity route: `{'bgg_id': 98778, 'title': 'Hanabi'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.0822664584959667 | `game_overview` | Hanabi | `game:bgg:98778:overview:rag-v0.1` |
| 2 | 0.032018442622950824 | `game_overview` | Hanabi & Ikebana | `game:bgg:70918:overview:rag-v0.1` |
| 3 | 0.03200204813108039 | `game_overview` | Hanabi: Grands Feux | `game:bgg:290357:overview:rag-v0.1` |
| 4 | 0.031754032258064516 | `game_overview` | Hanabi Deluxe II | `game:bgg:272743:overview:rag-v0.1` |
| 5 | 0.030309988518943745 | `game_overview` | Hanabi: Avalanche de couleurs | `game:bgg:121996:overview:rag-v0.1` |

### PASS: `g029_cn_review` - `花火 玩家评论`

- Expected: `reviews:bgg:98778`
- Entity route: `{'bgg_id': 98778, 'title': 'Hanabi'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.07565270188221009 | `review_digest` | Hanabi | `reviews:bgg:98778:digest:rag-v0.1` |
| 2 | 0.03200204813108039 | `review_digest` | Narabi | `reviews:bgg:257836:digest:rag-v0.1` |
| 3 | 0.030834914611005692 | `review_digest` | How Many? | `reviews:bgg:138206:digest:rag-v0.1` |
| 4 | 0.030798389007344232 | `review_digest` | Bomb Squad | `reviews:bgg:323609:digest:rag-v0.1` |
| 5 | 0.030679156908665108 | `review_digest` | Ice and the Sky | `reviews:bgg:180938:digest:rag-v0.1` |

### PASS: `g029_cn_theme` - `花火 合作 手牌管理 机制`

- Expected: `game:bgg:98778`
- Entity route: `{'bgg_id': 98778, 'title': 'Hanabi'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.0822664584959667 | `game_overview` | Hanabi | `game:bgg:98778:overview:rag-v0.1` |
| 2 | 0.032018442622950824 | `game_overview` | Hanabi & Ikebana | `game:bgg:70918:overview:rag-v0.1` |
| 3 | 0.03200204813108039 | `game_overview` | Hanabi: Grands Feux | `game:bgg:290357:overview:rag-v0.1` |
| 4 | 0.031754032258064516 | `game_overview` | Hanabi Deluxe II | `game:bgg:272743:overview:rag-v0.1` |
| 5 | 0.03076923076923077 | `game_overview` | Hanabi: Avalanche de couleurs | `game:bgg:121996:overview:rag-v0.1` |

### PASS: `g030_cn_overview` - `东京之王 游戏简介`

- Expected: `game:bgg:70323`
- Entity route: `{'bgg_id': 70323, 'title': 'King of Tokyo'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.0822664584959667 | `game_overview` | King of Tokyo | `game:bgg:70323:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | King of New Tokyo | `game:bgg:190115:overview:rag-v0.1` |
| 3 | 0.031754032258064516 | `game_overview` | King of Tokyo: Halloween | `game:bgg:147183:overview:rag-v0.1` |
| 4 | 0.030309988518943745 | `game_overview` | King of Tokyo: Dark Edition | `game:bgg:293141:overview:rag-v0.1` |
| 5 | 0.030158730158730156 | `game_overview` | King of Tokyo/New York: Monster Pack – Cthulhu | `game:bgg:207292:overview:rag-v0.1` |

### PASS: `g030_cn_review` - `东京之王 玩家评论`

- Expected: `reviews:bgg:70323`
- Entity route: `{'bgg_id': 70323, 'title': 'King of Tokyo'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.08088619624613923 | `review_digest` | King of Tokyo | `reviews:bgg:70323:digest:rag-v0.1` |
| 2 | 0.031754032258064516 | `review_digest` | King of Tokyo: Origins | `reviews:bgg:403240:digest:rag-v0.1` |
| 3 | 0.03128054740957967 | `review_digest` | King of New Tokyo | `reviews:bgg:190115:digest:rag-v0.1` |
| 4 | 0.030117753623188408 | `review_digest` | My Hero Academia: Plus Ultra! Board Game | `reviews:bgg:361208:digest:rag-v0.1` |
| 5 | 0.03007688828584351 | `review_digest` | King of Monster Island | `reviews:bgg:350755:digest:rag-v0.1` |

### PASS: `g030_cn_theme` - `东京之王 掷骰 赌运气 机制`

- Expected: `game:bgg:70323`
- Entity route: `{'bgg_id': 70323, 'title': 'King of Tokyo'}`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.0822664584959667 | `game_overview` | King of Tokyo | `game:bgg:70323:overview:rag-v0.1` |
| 2 | 0.03252247488101534 | `game_overview` | King of New Tokyo | `game:bgg:190115:overview:rag-v0.1` |
| 3 | 0.03200204813108039 | `game_overview` | King of Tokyo: Halloween | `game:bgg:147183:overview:rag-v0.1` |
| 4 | 0.030776515151515152 | `game_overview` | King of Tokyo: Dark Edition | `game:bgg:293141:overview:rag-v0.1` |
| 5 | 0.028484848484848488 | `game_overview` | King of New York: Power Up! | `game:bgg:193320:overview:rag-v0.1` |

### PASS: `m001_cn` - `工人放置 机制讲解`

- Expected: `mechanic:worker-placement:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03252247488101534 | `mechanic_profile` | Worker Placement with Dice Workers | `mechanic:worker-placement-with-dice-workers:profile:rag-v0.1` |
| 2 | 0.03252247488101534 | `mechanic_profile` | Worker Placement, Different Worker Types | `mechanic:worker-placement,-different-worker-types:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Worker Placement | `mechanic:worker-placement:profile:rag-v0.1` |
| 4 | 0.03125 | `mechanic_profile` | Action Drafting | `mechanic:action-drafting:profile:rag-v0.1` |
| 5 | 0.030309988518943745 | `mechanic_profile` | Turn Order: Claim Action | `mechanic:turn-order:-claim-action:profile:rag-v0.1` |

### PASS: `m001_en` - `worker placement mechanism`

- Expected: `mechanic:worker-placement:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Worker Placement, Different Worker Types | `mechanic:worker-placement,-different-worker-types:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Worker Placement with Dice Workers | `mechanic:worker-placement-with-dice-workers:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Worker Placement | `mechanic:worker-placement:profile:rag-v0.1` |
| 4 | 0.03125 | `mechanic_profile` | Auction: Fixed Placement | `mechanic:auction:-fixed-placement:profile:rag-v0.1` |
| 5 | 0.029877369007803793 | `mechanic_profile` | Contracts | `mechanic:contracts:profile:rag-v0.1` |

### PASS: `m002_cn` - `牌库构筑 机制讲解`

- Expected: `mechanic:deck,-bag,-and-pool-building:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Deck, Bag, and Pool Building | `mechanic:deck,-bag,-and-pool-building:profile:rag-v0.1` |
| 2 | 0.031754032258064516 | `mechanic_profile` | Move Through Deck | `mechanic:move-through-deck:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Deck Construction | `mechanic:deck-construction:profile:rag-v0.1` |
| 4 | 0.029418126757516764 | `mechanic_profile` | Open Drafting | `mechanic:open-drafting:profile:rag-v0.1` |
| 5 | 0.029116045245077504 | `mechanic_profile` | Melding and Splaying | `mechanic:melding-and-splaying:profile:rag-v0.1` |

### PASS: `m002_en` - `deck bag pool building mechanism`

- Expected: `mechanic:deck,-bag,-and-pool-building:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Deck, Bag, and Pool Building | `mechanic:deck,-bag,-and-pool-building:profile:rag-v0.1` |
| 2 | 0.03200204813108039 | `mechanic_profile` | Move Through Deck | `mechanic:move-through-deck:profile:rag-v0.1` |
| 3 | 0.03149801587301587 | `mechanic_profile` | Deck Construction | `mechanic:deck-construction:profile:rag-v0.1` |
| 4 | 0.03076923076923077 | `mechanic_profile` | Auction: Dutch | `mechanic:auction:-dutch:profile:rag-v0.1` |
| 5 | 0.029857397504456328 | `mechanic_profile` | Open Drafting | `mechanic:open-drafting:profile:rag-v0.1` |

### PASS: `m003_cn` - `掷骰 机制讲解`

- Expected: `mechanic:dice-rolling:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Random Production | `mechanic:random-production:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Turn Order: Random | `mechanic:turn-order:-random:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Dice Rolling | `mechanic:dice-rolling:profile:rag-v0.1` |
| 4 | 0.031009615384615385 | `mechanic_profile` | Different Dice Movement | `mechanic:different-dice-movement:profile:rag-v0.1` |
| 5 | 0.030776515151515152 | `mechanic_profile` | Re-rolling and Locking | `mechanic:re-rolling-and-locking:profile:rag-v0.1` |

### PASS: `m003_en` - `dice rolling mechanism`

- Expected: `mechanic:dice-rolling:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Dice Rolling | `mechanic:dice-rolling:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Re-rolling and Locking | `mechanic:re-rolling-and-locking:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Different Dice Movement | `mechanic:different-dice-movement:profile:rag-v0.1` |
| 4 | 0.031009615384615385 | `mechanic_profile` | Worker Placement with Dice Workers | `mechanic:worker-placement-with-dice-workers:profile:rag-v0.1` |
| 5 | 0.030330882352941176 | `mechanic_profile` | Die Icon Resolution | `mechanic:die-icon-resolution:profile:rag-v0.1` |

### PASS: `m004_cn` - `拍卖竞价 机制讲解`

- Expected: `mechanic:auction`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Auction: Sealed Bid | `mechanic:auction:-sealed-bid:profile:rag-v0.1` |
| 2 | 0.03200204813108039 | `mechanic_profile` | Auction: Fixed Placement | `mechanic:auction:-fixed-placement:profile:rag-v0.1` |
| 3 | 0.031754032258064516 | `mechanic_profile` | Auction: Dexterity | `mechanic:auction:-dexterity:profile:rag-v0.1` |
| 4 | 0.03149801587301587 | `mechanic_profile` | Auction: English | `mechanic:auction:-english:profile:rag-v0.1` |
| 5 | 0.030536130536130537 | `mechanic_profile` | Closed Economy Auction | `mechanic:closed-economy-auction:profile:rag-v0.1` |

### PASS: `m004_en` - `auction bidding mechanism`

- Expected: `mechanic:auction`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Auction / Bidding | `mechanic:auction---bidding:profile:rag-v0.1` |
| 2 | 0.031754032258064516 | `mechanic_profile` | Constrained Bidding | `mechanic:constrained-bidding:profile:rag-v0.1` |
| 3 | 0.031054405392392875 | `mechanic_profile` | Auction: Once Around | `mechanic:auction:-once-around:profile:rag-v0.1` |
| 4 | 0.031009615384615385 | `mechanic_profile` | Auction: Multiple Lot | `mechanic:auction:-multiple-lot:profile:rag-v0.1` |
| 5 | 0.03057889822595705 | `mechanic_profile` | Auction Compensation | `mechanic:auction-compensation:profile:rag-v0.1` |

### PASS: `m005_cn` - `区域控制 机制讲解`

- Expected: `mechanic:area-majority---influence:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Area Majority / Influence | `mechanic:area-majority---influence:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Area Movement | `mechanic:area-movement:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Area-Impulse | `mechanic:area-impulse:profile:rag-v0.1` |
| 4 | 0.029138513513513514 | `mechanic_profile` | Variable Player Powers | `mechanic:variable-player-powers:profile:rag-v0.1` |
| 5 | 0.02871794871794872 | `mechanic_profile` | Modular Board | `mechanic:modular-board:profile:rag-v0.1` |

### PASS: `m005_en` - `area majority influence mechanism`

- Expected: `mechanic:area-majority---influence:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Area Majority / Influence | `mechanic:area-majority---influence:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Area Movement | `mechanic:area-movement:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Area-Impulse | `mechanic:area-impulse:profile:rag-v0.1` |
| 4 | 0.029138513513513514 | `mechanic_profile` | Variable Player Powers | `mechanic:variable-player-powers:profile:rag-v0.1` |
| 5 | 0.02871794871794872 | `mechanic_profile` | Modular Board | `mechanic:modular-board:profile:rag-v0.1` |

### PASS: `m006_cn` - `区域移动 机制讲解`

- Expected: `mechanic:area-movement:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03252247488101534 | `mechanic_profile` | Map Reduction | `mechanic:map-reduction:profile:rag-v0.1` |
| 2 | 0.03200204813108039 | `mechanic_profile` | Pieces as Map | `mechanic:pieces-as-map:profile:rag-v0.1` |
| 3 | 0.03177805800756621 | `mechanic_profile` | Area Movement | `mechanic:area-movement:profile:rag-v0.1` |
| 4 | 0.030776515151515152 | `mechanic_profile` | Map Addition | `mechanic:map-addition:profile:rag-v0.1` |
| 5 | 0.030776515151515152 | `mechanic_profile` | Pattern Movement | `mechanic:pattern-movement:profile:rag-v0.1` |

### PASS: `m006_en` - `area movement mechanism`

- Expected: `mechanic:area-movement:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Area Movement | `mechanic:area-movement:profile:rag-v0.1` |
| 2 | 0.03200204813108039 | `mechanic_profile` | Area-Impulse | `mechanic:area-impulse:profile:rag-v0.1` |
| 3 | 0.03128054740957967 | `mechanic_profile` | Area Majority / Influence | `mechanic:area-majority---influence:profile:rag-v0.1` |
| 4 | 0.030117753623188408 | `mechanic_profile` | Enclosure | `mechanic:enclosure:profile:rag-v0.1` |
| 5 | 0.029631255487269532 | `mechanic_profile` | Action Points | `mechanic:action-points:profile:rag-v0.1` |

### PASS: `m007_cn` - `行动点 机制讲解`

- Expected: `mechanic:action-points:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Action Points | `mechanic:action-points:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Action / Event | `mechanic:action---event:profile:rag-v0.1` |
| 3 | 0.02919863597612958 | `mechanic_profile` | Hand Management | `mechanic:hand-management:profile:rag-v0.1` |
| 4 | 0.028850145288501453 | `mechanic_profile` | Point to Point Movement | `mechanic:point-to-point-movement:profile:rag-v0.1` |
| 5 | 0.028693528693528692 | `mechanic_profile` | Action Drafting | `mechanic:action-drafting:profile:rag-v0.1` |

### PASS: `m007_en` - `action points mechanism`

- Expected: `mechanic:action-points:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Action Points | `mechanic:action-points:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Action / Event | `mechanic:action---event:profile:rag-v0.1` |
| 3 | 0.028958333333333336 | `mechanic_profile` | Cube Tower | `mechanic:cube-tower:profile:rag-v0.1` |
| 4 | 0.0288981288981289 | `mechanic_profile` | Impulse Movement | `mechanic:impulse-movement:profile:rag-v0.1` |
| 5 | 0.028850145288501453 | `mechanic_profile` | Point to Point Movement | `mechanic:point-to-point-movement:profile:rag-v0.1` |

### PASS: `m008_cn` - `手牌管理 机制讲解`

- Expected: `mechanic:hand-management:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Hand Management | `mechanic:hand-management:profile:rag-v0.1` |
| 2 | 0.031024531024531024 | `mechanic_profile` | Auction: English | `mechanic:auction:-english:profile:rag-v0.1` |
| 3 | 0.03055037313432836 | `mechanic_profile` | Lose a Turn | `mechanic:lose-a-turn:profile:rag-v0.1` |
| 4 | 0.0304147465437788 | `mechanic_profile` | Matching | `mechanic:matching:profile:rag-v0.1` |
| 5 | 0.026736111111111113 | `mechanic_profile` | Command Cards | `mechanic:command-cards:profile:rag-v0.1` |

### PASS: `m008_en` - `hand management mechanism`

- Expected: `mechanic:hand-management:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Hand Management | `mechanic:hand-management:profile:rag-v0.1` |
| 2 | 0.03149801587301587 | `mechanic_profile` | Lose a Turn | `mechanic:lose-a-turn:profile:rag-v0.1` |
| 3 | 0.03128054740957967 | `mechanic_profile` | Auction: English | `mechanic:auction:-english:profile:rag-v0.1` |
| 4 | 0.031054405392392875 | `mechanic_profile` | Matching | `mechanic:matching:profile:rag-v0.1` |
| 5 | 0.02674825174825175 | `mechanic_profile` | Memory | `mechanic:memory:profile:rag-v0.1` |

### PASS: `m009_cn` - `成套收集 机制讲解`

- Expected: `mechanic:set-collection:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Set Collection | `mechanic:set-collection:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Variable Set-up | `mechanic:variable-set-up:profile:rag-v0.1` |
| 3 | 0.031024531024531024 | `mechanic_profile` | Matching | `mechanic:matching:profile:rag-v0.1` |
| 4 | 0.028782894736842105 | `mechanic_profile` | Speed Matching | `mechanic:speed-matching:profile:rag-v0.1` |
| 5 | 0.028309409888357256 | `mechanic_profile` | Lose a Turn | `mechanic:lose-a-turn:profile:rag-v0.1` |

### PASS: `m009_en` - `set collection mechanism`

- Expected: `mechanic:set-collection:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Set Collection | `mechanic:set-collection:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Variable Set-up | `mechanic:variable-set-up:profile:rag-v0.1` |
| 3 | 0.03125763125763126 | `mechanic_profile` | Stock Holding | `mechanic:stock-holding:profile:rag-v0.1` |
| 4 | 0.030798389007344232 | `mechanic_profile` | Matching | `mechanic:matching:profile:rag-v0.1` |
| 5 | 0.02967032967032967 | `mechanic_profile` | Speed Matching | `mechanic:speed-matching:profile:rag-v0.1` |

### PASS: `m010_cn` - `可变玩家能力 机制讲解`

- Expected: `mechanic:variable-player-powers:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Roles with Asymmetric Information | `mechanic:roles-with-asymmetric-information:profile:rag-v0.1` |
| 2 | 0.03200204813108039 | `mechanic_profile` | Variable Player Powers | `mechanic:variable-player-powers:profile:rag-v0.1` |
| 3 | 0.031754032258064516 | `mechanic_profile` | Hidden Roles | `mechanic:hidden-roles:profile:rag-v0.1` |
| 4 | 0.03149801587301587 | `mechanic_profile` | Variable Set-up | `mechanic:variable-set-up:profile:rag-v0.1` |
| 5 | 0.030309988518943745 | `mechanic_profile` | Variable Phase Order | `mechanic:variable-phase-order:profile:rag-v0.1` |

### PASS: `m010_en` - `variable player powers mechanism`

- Expected: `mechanic:variable-player-powers:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Variable Player Powers | `mechanic:variable-player-powers:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Variable Set-up | `mechanic:variable-set-up:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Variable Phase Order | `mechanic:variable-phase-order:profile:rag-v0.1` |
| 4 | 0.029513888888888888 | `mechanic_profile` | Contracts | `mechanic:contracts:profile:rag-v0.1` |
| 5 | 0.029273504273504274 | `mechanic_profile` | Race | `mechanic:race:profile:rag-v0.1` |

### PASS: `m011_cn` - `可变设置 机制讲解`

- Expected: `mechanic:variable-set-up:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Variable Set-up | `mechanic:variable-set-up:profile:rag-v0.1` |
| 2 | 0.03125 | `mechanic_profile` | Race | `mechanic:race:profile:rag-v0.1` |
| 3 | 0.03021353930031804 | `mechanic_profile` | Modular Board | `mechanic:modular-board:profile:rag-v0.1` |
| 4 | 0.02976190476190476 | `mechanic_profile` | Map Reduction | `mechanic:map-reduction:profile:rag-v0.1` |
| 5 | 0.02964254577157803 | `mechanic_profile` | Tags | `mechanic:tags:profile:rag-v0.1` |

### PASS: `m011_en` - `variable setup mechanism`

- Expected: `mechanic:variable-set-up:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Variable Set-up | `mechanic:variable-set-up:profile:rag-v0.1` |
| 2 | 0.03200204813108039 | `mechanic_profile` | Variable Phase Order | `mechanic:variable-phase-order:profile:rag-v0.1` |
| 3 | 0.03200204813108039 | `mechanic_profile` | Variable Player Powers | `mechanic:variable-player-powers:profile:rag-v0.1` |
| 4 | 0.029513888888888888 | `mechanic_profile` | Contracts | `mechanic:contracts:profile:rag-v0.1` |
| 5 | 0.029273504273504274 | `mechanic_profile` | Race | `mechanic:race:profile:rag-v0.1` |

### PASS: `m012_cn` - `合作游戏 机制讲解`

- Expected: `mechanic:cooperative-game:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03252247488101534 | `mechanic_profile` | Semi-Cooperative Game | `mechanic:semi-cooperative-game:profile:rag-v0.1` |
| 2 | 0.03252247488101534 | `mechanic_profile` | Cooperative Game | `mechanic:cooperative-game:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Campaign / Battle Card Driven | `mechanic:campaign---battle-card-driven:profile:rag-v0.1` |
| 4 | 0.03125 | `mechanic_profile` | Scenario / Mission / Campaign Game | `mechanic:scenario---mission---campaign-game:profile:rag-v0.1` |
| 5 | 0.030536130536130537 | `mechanic_profile` | Turn Order: Random | `mechanic:turn-order:-random:profile:rag-v0.1` |

### PASS: `m012_en` - `cooperative game mechanism`

- Expected: `mechanic:cooperative-game:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03252247488101534 | `mechanic_profile` | Semi-Cooperative Game | `mechanic:semi-cooperative-game:profile:rag-v0.1` |
| 2 | 0.03252247488101534 | `mechanic_profile` | Cooperative Game | `mechanic:cooperative-game:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Traitor Game | `mechanic:traitor-game:profile:rag-v0.1` |
| 4 | 0.030776515151515152 | `mechanic_profile` | Matching | `mechanic:matching:profile:rag-v0.1` |
| 5 | 0.0288981288981289 | `mechanic_profile` | Memory | `mechanic:memory:profile:rag-v0.1` |

### PASS: `m013_cn` - `战役模式 机制讲解`

- Expected: `mechanic:scenario---mission---campaign-game:profile, mechanic:campaign---battle-card-driven:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Scenario / Mission / Campaign Game | `mechanic:scenario---mission---campaign-game:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Legacy Game | `mechanic:legacy-game:profile:rag-v0.1` |
| 3 | 0.03125763125763126 | `mechanic_profile` | Events | `mechanic:events:profile:rag-v0.1` |
| 4 | 0.03125 | `mechanic_profile` | Movement Points | `mechanic:movement-points:profile:rag-v0.1` |
| 5 | 0.030303030303030304 | `mechanic_profile` | Command Cards | `mechanic:command-cards:profile:rag-v0.1` |

### PASS: `m013_en` - `scenario mission campaign game mechanism`

- Expected: `mechanic:scenario---mission---campaign-game:profile, mechanic:campaign---battle-card-driven:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Scenario / Mission / Campaign Game | `mechanic:scenario---mission---campaign-game:profile:rag-v0.1` |
| 2 | 0.03200204813108039 | `mechanic_profile` | Action Timer | `mechanic:action-timer:profile:rag-v0.1` |
| 3 | 0.03149801587301587 | `mechanic_profile` | Command Cards | `mechanic:command-cards:profile:rag-v0.1` |
| 4 | 0.03128054740957967 | `mechanic_profile` | Communication Limits | `mechanic:communication-limits:profile:rag-v0.1` |
| 5 | 0.030776515151515152 | `mechanic_profile` | Action / Event | `mechanic:action---event:profile:rag-v0.1` |

### PASS: `m014_cn` - `版图放置 机制讲解`

- Expected: `mechanic:tile-placement:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Tile Placement | `mechanic:tile-placement:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Modular Board | `mechanic:modular-board:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Worker Placement | `mechanic:worker-placement:profile:rag-v0.1` |
| 4 | 0.030536130536130537 | `mechanic_profile` | Area Majority / Influence | `mechanic:area-majority---influence:profile:rag-v0.1` |
| 5 | 0.030117753623188408 | `mechanic_profile` | Pattern Building | `mechanic:pattern-building:profile:rag-v0.1` |

### PASS: `m014_en` - `tile placement mechanism`

- Expected: `mechanic:tile-placement:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Tile Placement | `mechanic:tile-placement:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Auction: Fixed Placement | `mechanic:auction:-fixed-placement:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Worker Placement, Different Worker Types | `mechanic:worker-placement,-different-worker-types:profile:rag-v0.1` |
| 4 | 0.03125 | `mechanic_profile` | Worker Placement with Dice Workers | `mechanic:worker-placement-with-dice-workers:profile:rag-v0.1` |
| 5 | 0.03076923076923077 | `mechanic_profile` | Worker Placement | `mechanic:worker-placement:profile:rag-v0.1` |

### PASS: `m015_cn` - `路线建设 机制讲解`

- Expected: `mechanic:network-and-route-building:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03252247488101534 | `mechanic_profile` | Connections | `mechanic:connections:profile:rag-v0.1` |
| 2 | 0.03252247488101534 | `mechanic_profile` | Network and Route Building | `mechanic:network-and-route-building:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Bingo | `mechanic:bingo:profile:rag-v0.1` |
| 4 | 0.03125 | `mechanic_profile` | Drawing | `mechanic:drawing:profile:rag-v0.1` |
| 5 | 0.029236022193768675 | `mechanic_profile` | Enclosure | `mechanic:enclosure:profile:rag-v0.1` |

### PASS: `m015_en` - `network and route building mechanism`

- Expected: `mechanic:network-and-route-building:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Network and Route Building | `mechanic:network-and-route-building:profile:rag-v0.1` |
| 2 | 0.03125763125763126 | `mechanic_profile` | Enclosure | `mechanic:enclosure:profile:rag-v0.1` |
| 3 | 0.030621785881252923 | `mechanic_profile` | Investment | `mechanic:investment:profile:rag-v0.1` |
| 4 | 0.030330882352941176 | `mechanic_profile` | Bingo | `mechanic:bingo:profile:rag-v0.1` |
| 5 | 0.030158730158730156 | `mechanic_profile` | Auction: Fixed Placement | `mechanic:auction:-fixed-placement:profile:rag-v0.1` |

### PASS: `m016_cn` - `同时行动选择 机制讲解`

- Expected: `mechanic:simultaneous-action-selection:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Simultaneous Action Selection | `mechanic:simultaneous-action-selection:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Selection Order Bid | `mechanic:selection-order-bid:profile:rag-v0.1` |
| 3 | 0.03057889822595705 | `mechanic_profile` | Action Timer | `mechanic:action-timer:profile:rag-v0.1` |
| 4 | 0.029957522915269395 | `mechanic_profile` | Auction: Dexterity | `mechanic:auction:-dexterity:profile:rag-v0.1` |
| 5 | 0.029709507042253523 | `mechanic_profile` | Hand Management | `mechanic:hand-management:profile:rag-v0.1` |

### PASS: `m016_en` - `simultaneous action selection mechanism`

- Expected: `mechanic:simultaneous-action-selection:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Simultaneous Action Selection | `mechanic:simultaneous-action-selection:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Selection Order Bid | `mechanic:selection-order-bid:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Action Timer | `mechanic:action-timer:profile:rag-v0.1` |
| 4 | 0.03125 | `mechanic_profile` | Action Queue | `mechanic:action-queue:profile:rag-v0.1` |
| 5 | 0.02900988017658188 | `mechanic_profile` | Auction: Dexterity | `mechanic:auction:-dexterity:profile:rag-v0.1` |

### PASS: `m017_cn` - `卡牌轮抽 机制讲解`

- Expected: `mechanic:card-drafting:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.032266458495966696 | `mechanic_profile` | Closed Drafting | `mechanic:closed-drafting:profile:rag-v0.1` |
| 2 | 0.032266458495966696 | `mechanic_profile` | Card Drafting | `mechanic:card-drafting:profile:rag-v0.1` |
| 3 | 0.03225806451612903 | `mechanic_profile` | Action Drafting | `mechanic:action-drafting:profile:rag-v0.1` |
| 4 | 0.03125 | `mechanic_profile` | Open Drafting | `mechanic:open-drafting:profile:rag-v0.1` |
| 5 | 0.029437229437229435 | `mechanic_profile` | Follow | `mechanic:follow:profile:rag-v0.1` |

### PASS: `m017_en` - `card drafting mechanism`

- Expected: `mechanic:card-drafting:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Card Drafting | `mechanic:card-drafting:profile:rag-v0.1` |
| 2 | 0.03200204813108039 | `mechanic_profile` | Closed Drafting | `mechanic:closed-drafting:profile:rag-v0.1` |
| 3 | 0.03200204813108039 | `mechanic_profile` | Action Drafting | `mechanic:action-drafting:profile:rag-v0.1` |
| 4 | 0.03125 | `mechanic_profile` | Open Drafting | `mechanic:open-drafting:profile:rag-v0.1` |
| 5 | 0.03076923076923077 | `mechanic_profile` | Follow | `mechanic:follow:profile:rag-v0.1` |

### PASS: `m018_cn` - `隐蔽身份 机制讲解`

- Expected: `mechanic:hidden-roles:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Hidden Roles | `mechanic:hidden-roles:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Roles with Asymmetric Information | `mechanic:roles-with-asymmetric-information:profile:rag-v0.1` |
| 3 | 0.03149801587301587 | `mechanic_profile` | Targeted Clues | `mechanic:targeted-clues:profile:rag-v0.1` |
| 4 | 0.03149801587301587 | `mechanic_profile` | Deduction | `mechanic:deduction:profile:rag-v0.1` |
| 5 | 0.030536130536130537 | `mechanic_profile` | Traitor Game | `mechanic:traitor-game:profile:rag-v0.1` |

### PASS: `m018_en` - `hidden roles mechanism`

- Expected: `mechanic:hidden-roles:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Hidden Roles | `mechanic:hidden-roles:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Roles with Asymmetric Information | `mechanic:roles-with-asymmetric-information:profile:rag-v0.1` |
| 3 | 0.03125763125763126 | `mechanic_profile` | Targeted Clues | `mechanic:targeted-clues:profile:rag-v0.1` |
| 4 | 0.030798389007344232 | `mechanic_profile` | Hidden Movement | `mechanic:hidden-movement:profile:rag-v0.1` |
| 5 | 0.030776515151515152 | `mechanic_profile` | Deduction | `mechanic:deduction:profile:rag-v0.1` |

### PASS: `m019_cn` - `讲故事 机制讲解`

- Expected: `mechanic:storytelling:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Storytelling | `mechanic:storytelling:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Voting | `mechanic:voting:profile:rag-v0.1` |
| 3 | 0.03149801587301587 | `mechanic_profile` | Acting | `mechanic:acting:profile:rag-v0.1` |
| 4 | 0.031009615384615385 | `mechanic_profile` | Player Judge | `mechanic:player-judge:profile:rag-v0.1` |
| 5 | 0.030798389007344232 | `mechanic_profile` | Targeted Clues | `mechanic:targeted-clues:profile:rag-v0.1` |

### PASS: `m019_en` - `storytelling mechanism`

- Expected: `mechanic:storytelling:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Storytelling | `mechanic:storytelling:profile:rag-v0.1` |
| 2 | 0.03149801587301587 | `mechanic_profile` | Acting | `mechanic:acting:profile:rag-v0.1` |
| 3 | 0.030834914611005692 | `mechanic_profile` | Cooperative Game | `mechanic:cooperative-game:profile:rag-v0.1` |
| 4 | 0.030798389007344232 | `mechanic_profile` | Questions and Answers | `mechanic:questions-and-answers:profile:rag-v0.1` |
| 5 | 0.030536130536130537 | `mechanic_profile` | Player Judge | `mechanic:player-judge:profile:rag-v0.1` |

### PASS: `m020_cn` - `吃墩 机制讲解`

- Expected: `mechanic:trick-taking:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Trick-taking | `mechanic:trick-taking:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Predictive Bid | `mechanic:predictive-bid:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Ladder Climbing | `mechanic:ladder-climbing:profile:rag-v0.1` |
| 4 | 0.03125 | `mechanic_profile` | Single Loser Game | `mechanic:single-loser-game:profile:rag-v0.1` |
| 5 | 0.03076923076923077 | `mechanic_profile` | Bids As Wagers | `mechanic:bids-as-wagers:profile:rag-v0.1` |

### PASS: `m020_en` - `trick taking mechanism`

- Expected: `mechanic:trick-taking:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Trick-taking | `mechanic:trick-taking:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Predictive Bid | `mechanic:predictive-bid:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Ladder Climbing | `mechanic:ladder-climbing:profile:rag-v0.1` |
| 4 | 0.03125 | `mechanic_profile` | Single Loser Game | `mechanic:single-loser-game:profile:rag-v0.1` |
| 5 | 0.03076923076923077 | `mechanic_profile` | Bids As Wagers | `mechanic:bids-as-wagers:profile:rag-v0.1` |

### PASS: `m021_cn` - `赌运气 机制讲解`

- Expected: `mechanic:push-your-luck:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Push Your Luck | `mechanic:push-your-luck:profile:rag-v0.1` |
| 2 | 0.030798389007344232 | `mechanic_profile` | Flicking | `mechanic:flicking:profile:rag-v0.1` |
| 3 | 0.03076923076923077 | `mechanic_profile` | Different Dice Movement | `mechanic:different-dice-movement:profile:rag-v0.1` |
| 4 | 0.03055037313432836 | `mechanic_profile` | Race | `mechanic:race:profile:rag-v0.1` |
| 5 | 0.029513888888888888 | `mechanic_profile` | Score-and-Reset Game | `mechanic:score-and-reset-game:profile:rag-v0.1` |

### PASS: `m021_en` - `push your luck mechanism`

- Expected: `mechanic:push-your-luck:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Push Your Luck | `mechanic:push-your-luck:profile:rag-v0.1` |
| 2 | 0.03200204813108039 | `mechanic_profile` | Physical Removal | `mechanic:physical-removal:profile:rag-v0.1` |
| 3 | 0.03057889822595705 | `mechanic_profile` | Flicking | `mechanic:flicking:profile:rag-v0.1` |
| 4 | 0.030536130536130537 | `mechanic_profile` | Different Dice Movement | `mechanic:different-dice-movement:profile:rag-v0.1` |
| 5 | 0.030309988518943745 | `mechanic_profile` | Race | `mechanic:race:profile:rag-v0.1` |

### PASS: `m022_cn` - `虚张声势 机制讲解`

- Expected: `mechanic:betting-and-bluffing:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03252247488101534 | `mechanic_profile` | Hidden Roles | `mechanic:hidden-roles:profile:rag-v0.1` |
| 2 | 0.032018442622950824 | `mechanic_profile` | Betting and Bluffing | `mechanic:betting-and-bluffing:profile:rag-v0.1` |
| 3 | 0.03200204813108039 | `mechanic_profile` | Roles with Asymmetric Information | `mechanic:roles-with-asymmetric-information:profile:rag-v0.1` |
| 4 | 0.03057889822595705 | `mechanic_profile` | Targeted Clues | `mechanic:targeted-clues:profile:rag-v0.1` |
| 5 | 0.030536130536130537 | `mechanic_profile` | Deduction | `mechanic:deduction:profile:rag-v0.1` |

### PASS: `m022_en` - `betting and bluffing mechanism`

- Expected: `mechanic:betting-and-bluffing:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Betting and Bluffing | `mechanic:betting-and-bluffing:profile:rag-v0.1` |
| 2 | 0.031024531024531024 | `mechanic_profile` | Memory | `mechanic:memory:profile:rag-v0.1` |
| 3 | 0.029513888888888888 | `mechanic_profile` | Dexterity | `mechanic:dexterity:profile:rag-v0.1` |
| 4 | 0.029418126757516764 | `mechanic_profile` | Negotiation | `mechanic:negotiation:profile:rag-v0.1` |
| 5 | 0.029116045245077504 | `mechanic_profile` | Score-and-Reset Game | `mechanic:score-and-reset-game:profile:rag-v0.1` |

### PASS: `m023_cn` - `模块化版图 机制讲解`

- Expected: `mechanic:modular-board:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Modular Board | `mechanic:modular-board:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Variable Set-up | `mechanic:variable-set-up:profile:rag-v0.1` |
| 3 | 0.03149801587301587 | `mechanic_profile` | Variable Phase Order | `mechanic:variable-phase-order:profile:rag-v0.1` |
| 4 | 0.03149801587301587 | `mechanic_profile` | Variable Player Powers | `mechanic:variable-player-powers:profile:rag-v0.1` |
| 5 | 0.029877369007803793 | `mechanic_profile` | Race | `mechanic:race:profile:rag-v0.1` |

### PASS: `m023_en` - `modular board mechanism`

- Expected: `mechanic:modular-board:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Modular Board | `mechanic:modular-board:profile:rag-v0.1` |
| 2 | 0.029571646010002173 | `mechanic_profile` | Different Dice Movement | `mechanic:different-dice-movement:profile:rag-v0.1` |
| 3 | 0.029437229437229435 | `mechanic_profile` | Grid Movement | `mechanic:grid-movement:profile:rag-v0.1` |
| 4 | 0.028612012987012988 | `mechanic_profile` | Role Playing | `mechanic:role-playing:profile:rag-v0.1` |
| 5 | 0.028373015873015873 | `mechanic_profile` | Pattern Building | `mechanic:pattern-building:profile:rag-v0.1` |

### PASS: `m024_cn` - `六角格 机制讲解`

- Expected: `mechanic:hexagon-grid:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.032266458495966696 | `mechanic_profile` | Map Reduction | `mechanic:map-reduction:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Pieces as Map | `mechanic:pieces-as-map:profile:rag-v0.1` |
| 3 | 0.032018442622950824 | `mechanic_profile` | Hexagon Grid | `mechanic:hexagon-grid:profile:rag-v0.1` |
| 4 | 0.03149801587301587 | `mechanic_profile` | Map Addition | `mechanic:map-addition:profile:rag-v0.1` |
| 5 | 0.03076923076923077 | `mechanic_profile` | Grid Movement | `mechanic:grid-movement:profile:rag-v0.1` |

### PASS: `m024_en` - `hexagon grid mechanism`

- Expected: `mechanic:hexagon-grid:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Hexagon Grid | `mechanic:hexagon-grid:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Grid Movement | `mechanic:grid-movement:profile:rag-v0.1` |
| 3 | 0.031024531024531024 | `mechanic_profile` | Map Reduction | `mechanic:map-reduction:profile:rag-v0.1` |
| 4 | 0.031009615384615385 | `mechanic_profile` | Moving Multiple Units | `mechanic:moving-multiple-units:profile:rag-v0.1` |
| 5 | 0.029211087420042643 | `mechanic_profile` | Different Dice Movement | `mechanic:different-dice-movement:profile:rag-v0.1` |

### PASS: `m025_cn` - `收入 机制讲解`

- Expected: `mechanic:income:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.032266458495966696 | `mechanic_profile` | Automatic Resource Growth | `mechanic:automatic-resource-growth:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Random Production | `mechanic:random-production:profile:rag-v0.1` |
| 3 | 0.031544957774465976 | `mechanic_profile` | Income | `mechanic:income:profile:rag-v0.1` |
| 4 | 0.03057889822595705 | `mechanic_profile` | Investment | `mechanic:investment:profile:rag-v0.1` |
| 5 | 0.03055037313432836 | `mechanic_profile` | Ownership | `mechanic:ownership:profile:rag-v0.1` |

### PASS: `m025_en` - `income mechanism`

- Expected: `mechanic:income:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Income | `mechanic:income:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Lose a Turn | `mechanic:lose-a-turn:profile:rag-v0.1` |
| 3 | 0.03149801587301587 | `mechanic_profile` | Contracts | `mechanic:contracts:profile:rag-v0.1` |
| 4 | 0.030158730158730156 | `mechanic_profile` | Random Production | `mechanic:random-production:profile:rag-v0.1` |
| 5 | 0.02946912242686891 | `mechanic_profile` | Alliances | `mechanic:alliances:profile:rag-v0.1` |

### PASS: `m026_cn` - `谈判 机制讲解`

- Expected: `mechanic:negotiation:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03252247488101534 | `mechanic_profile` | Trading | `mechanic:trading:profile:rag-v0.1` |
| 2 | 0.03252247488101534 | `mechanic_profile` | Negotiation | `mechanic:negotiation:profile:rag-v0.1` |
| 3 | 0.03149801587301587 | `mechanic_profile` | Random Production | `mechanic:random-production:profile:rag-v0.1` |
| 4 | 0.031024531024531024 | `mechanic_profile` | Bribery | `mechanic:bribery:profile:rag-v0.1` |
| 5 | 0.030330882352941176 | `mechanic_profile` | Card Drafting | `mechanic:card-drafting:profile:rag-v0.1` |

### PASS: `m026_en` - `negotiation mechanism`

- Expected: `mechanic:negotiation:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Negotiation | `mechanic:negotiation:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Auction: English | `mechanic:auction:-english:profile:rag-v0.1` |
| 3 | 0.03149801587301587 | `mechanic_profile` | Random Production | `mechanic:random-production:profile:rag-v0.1` |
| 4 | 0.031024531024531024 | `mechanic_profile` | Bribery | `mechanic:bribery:profile:rag-v0.1` |
| 5 | 0.031009615384615385 | `mechanic_profile` | Alliances | `mechanic:alliances:profile:rag-v0.1` |

### PASS: `m027_cn` - `交易 机制讲解`

- Expected: `mechanic:trading:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.032266458495966696 | `mechanic_profile` | Negotiation | `mechanic:negotiation:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Trading | `mechanic:trading:profile:rag-v0.1` |
| 3 | 0.032018442622950824 | `mechanic_profile` | Auction: English | `mechanic:auction:-english:profile:rag-v0.1` |
| 4 | 0.030309988518943745 | `mechanic_profile` | Random Production | `mechanic:random-production:profile:rag-v0.1` |
| 5 | 0.029910714285714284 | `mechanic_profile` | Bribery | `mechanic:bribery:profile:rag-v0.1` |

### PASS: `m027_en` - `trading mechanism`

- Expected: `mechanic:trading:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Trading | `mechanic:trading:profile:rag-v0.1` |
| 2 | 0.03149801587301587 | `mechanic_profile` | Random Production | `mechanic:random-production:profile:rag-v0.1` |
| 3 | 0.030621785881252923 | `mechanic_profile` | Card Drafting | `mechanic:card-drafting:profile:rag-v0.1` |
| 4 | 0.030536130536130537 | `mechanic_profile` | Negotiation | `mechanic:negotiation:profile:rag-v0.1` |
| 5 | 0.03036576949620428 | `mechanic_profile` | Bribery | `mechanic:bribery:profile:rag-v0.1` |

### PASS: `m028_cn` - `随机生产 机制讲解`

- Expected: `mechanic:random-production:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Random Production | `mechanic:random-production:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Victory Points as a Resource | `mechanic:victory-points-as-a-resource:profile:rag-v0.1` |
| 3 | 0.031746031746031744 | `mechanic_profile` | Resource to Move | `mechanic:resource-to-move:profile:rag-v0.1` |
| 4 | 0.03125 | `mechanic_profile` | Resource Queue | `mechanic:resource-queue:profile:rag-v0.1` |
| 5 | 0.030536130536130537 | `mechanic_profile` | Automatic Resource Growth | `mechanic:automatic-resource-growth:profile:rag-v0.1` |

### PASS: `m028_en` - `random production mechanism`

- Expected: `mechanic:random-production:profile`

| Rank | Score | Doc type | Title | Doc ID |
| ---: | ---: | --- | --- | --- |
| 1 | 0.03278688524590164 | `mechanic_profile` | Random Production | `mechanic:random-production:profile:rag-v0.1` |
| 2 | 0.03225806451612903 | `mechanic_profile` | Turn Order: Random | `mechanic:turn-order:-random:profile:rag-v0.1` |
