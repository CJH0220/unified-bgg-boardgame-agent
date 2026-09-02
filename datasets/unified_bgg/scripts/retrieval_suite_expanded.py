"""Expanded Chinese/English retrieval queries for Phase 10 validation."""
from __future__ import annotations

from typing import TypedDict


class RetrievalQuery(TypedDict, total=False):
    query_id: str
    query: str
    doc_type: str
    expected_any: list[str]
    engine: str


GAME_CASES: list[dict[str, str | int]] = [
    {"bgg_id": 13, "title": "CATAN", "alias": "卡坦岛", "theme": "交易 掷骰 资源"},
    {"bgg_id": 822, "title": "Carcassonne", "alias": "卡卡颂", "theme": "版图拼放 区域控制"},
    {"bgg_id": 224517, "title": "Brass: Birmingham", "alias": "伯明翰重工业", "theme": "经济 路线建设"},
    {"bgg_id": 161936, "title": "Pandemic Legacy: Season 1", "alias": "瘟疫危机传承第一季", "theme": "合作 战役"},
    {"bgg_id": 342942, "title": "Ark Nova", "alias": "方舟动物园", "theme": "动物园 卡牌轮抽"},
    {"bgg_id": 174430, "title": "Gloomhaven", "alias": "幽港迷城", "theme": "合作 战役 战术"},
    {"bgg_id": 233078, "title": "Twilight Imperium: Fourth Edition", "alias": "暮光帝国第四版", "theme": "太空 谈判 区域控制"},
    {"bgg_id": 316554, "title": "Dune: Imperium", "alias": "沙丘帝国", "theme": "牌库构筑 工人放置"},
    {"bgg_id": 167791, "title": "Terraforming Mars", "alias": "殖民火星", "theme": "引擎构筑 版图放置"},
    {"bgg_id": 115746, "title": "War of the Ring: Second Edition", "alias": "魔戒圣战", "theme": "战争 掷骰 卡牌"},
    {"bgg_id": 187645, "title": "Star Wars: Rebellion", "alias": "星球大战反叛", "theme": "不对称 隐蔽移动"},
    {"bgg_id": 162886, "title": "Spirit Island", "alias": "灵迹岛", "theme": "合作 可变玩家能力"},
    {"bgg_id": 291457, "title": "Gloomhaven: Jaws of the Lion", "alias": "狮子之颚", "theme": "合作 战役"},
    {"bgg_id": 220308, "title": "Gaia Project", "alias": "盖亚计划", "theme": "经济 网络建设"},
    {"bgg_id": 12333, "title": "Twilight Struggle", "alias": "冷战热斗", "theme": "卡牌驱动 区域优势"},
    {"bgg_id": 182028, "title": "Through the Ages: A New Story of Civilization", "alias": "历史巨轮", "theme": "文明 卡牌轮抽"},
    {"bgg_id": 84876, "title": "The Castles of Burgundy", "alias": "勃艮第城堡", "theme": "掷骰 版图放置"},
    {"bgg_id": 9209, "title": "Ticket to Ride", "alias": "车票之旅", "theme": "路线建设 成套收集"},
    {"bgg_id": 36218, "title": "Dominion", "alias": "皇舆争霸", "theme": "牌库构筑 手牌管理"},
    {"bgg_id": 178900, "title": "Codenames", "alias": "行动代号", "theme": "词语 联想 推理"},
    {"bgg_id": 230802, "title": "Azul", "alias": "花砖物语", "theme": "选牌 图案构筑"},
    {"bgg_id": 148228, "title": "Splendor", "alias": "璀璨宝石", "theme": "引擎构筑 成套收集"},
    {"bgg_id": 129622, "title": "Love Letter", "alias": "情书", "theme": "推理 手牌管理"},
    {"bgg_id": 30549, "title": "Pandemic", "alias": "瘟疫危机", "theme": "合作 行动点"},
    {"bgg_id": 68448, "title": "7 Wonders", "alias": "七大奇迹", "theme": "卡牌轮抽 文明"},
    {"bgg_id": 39856, "title": "Dixit", "alias": "妙语说书人", "theme": "讲故事 投票"},
    {"bgg_id": 163412, "title": "Patchwork", "alias": "拼布艺术", "theme": "双人 拼放版图"},
    {"bgg_id": 40692, "title": "Small World", "alias": "小世界", "theme": "区域控制 可变玩家能力"},
    {"bgg_id": 98778, "title": "Hanabi", "alias": "花火", "theme": "合作 手牌管理"},
    {"bgg_id": 70323, "title": "King of Tokyo", "alias": "东京之王", "theme": "掷骰 赌运气"},
]

MECHANISM_CASES: list[dict[str, str | list[str]]] = [
    {"cn": "工人放置", "en": "worker placement", "expected_any": ["mechanic:worker-placement:profile"]},
    {"cn": "牌库构筑", "en": "deck bag pool building", "expected_any": ["mechanic:deck,-bag,-and-pool-building:profile"]},
    {"cn": "掷骰", "en": "dice rolling", "expected_any": ["mechanic:dice-rolling:profile"]},
    {"cn": "拍卖竞价", "en": "auction bidding", "expected_any": ["mechanic:auction"]},
    {"cn": "区域控制", "en": "area majority influence", "expected_any": ["mechanic:area-majority---influence:profile"]},
    {"cn": "区域移动", "en": "area movement", "expected_any": ["mechanic:area-movement:profile"]},
    {"cn": "行动点", "en": "action points", "expected_any": ["mechanic:action-points:profile"]},
    {"cn": "手牌管理", "en": "hand management", "expected_any": ["mechanic:hand-management:profile"]},
    {"cn": "成套收集", "en": "set collection", "expected_any": ["mechanic:set-collection:profile"]},
    {"cn": "可变玩家能力", "en": "variable player powers", "expected_any": ["mechanic:variable-player-powers:profile"]},
    {"cn": "可变设置", "en": "variable setup", "expected_any": ["mechanic:variable-set-up:profile"]},
    {"cn": "合作游戏", "en": "cooperative game", "expected_any": ["mechanic:cooperative-game:profile"]},
    {"cn": "战役模式", "en": "scenario mission campaign game", "expected_any": ["mechanic:scenario---mission---campaign-game:profile", "mechanic:campaign---battle-card-driven:profile"]},
    {"cn": "版图放置", "en": "tile placement", "expected_any": ["mechanic:tile-placement:profile"]},
    {"cn": "路线建设", "en": "network and route building", "expected_any": ["mechanic:network-and-route-building:profile"]},
    {"cn": "同时行动选择", "en": "simultaneous action selection", "expected_any": ["mechanic:simultaneous-action-selection:profile"]},
    {"cn": "卡牌轮抽", "en": "card drafting", "expected_any": ["mechanic:card-drafting:profile"]},
    {"cn": "隐蔽身份", "en": "hidden roles", "expected_any": ["mechanic:hidden-roles:profile"]},
    {"cn": "讲故事", "en": "storytelling", "expected_any": ["mechanic:storytelling:profile"]},
    {"cn": "吃墩", "en": "trick taking", "expected_any": ["mechanic:trick-taking:profile"]},
    {"cn": "赌运气", "en": "push your luck", "expected_any": ["mechanic:push-your-luck:profile"]},
    {"cn": "虚张声势", "en": "betting and bluffing", "expected_any": ["mechanic:betting-and-bluffing:profile"]},
    {"cn": "模块化版图", "en": "modular board", "expected_any": ["mechanic:modular-board:profile"]},
    {"cn": "六角格", "en": "hexagon grid", "expected_any": ["mechanic:hexagon-grid:profile"]},
    {"cn": "收入", "en": "income", "expected_any": ["mechanic:income:profile"]},
    {"cn": "谈判", "en": "negotiation", "expected_any": ["mechanic:negotiation:profile"]},
    {"cn": "交易", "en": "trading", "expected_any": ["mechanic:trading:profile"]},
    {"cn": "随机生产", "en": "random production", "expected_any": ["mechanic:random-production:profile"]},
]


def build_suite() -> list[RetrievalQuery]:
    suite: list[RetrievalQuery] = []
    for idx, case in enumerate(GAME_CASES, start=1):
        bgg_id = int(case["bgg_id"])
        alias = str(case["alias"])
        theme = str(case["theme"])
        suite.extend(
            [
                {
                    "query_id": f"g{idx:03d}_cn_overview",
                    "query": f"{alias} 游戏简介",
                    "doc_type": "game_overview",
                    "expected_any": [f"game:bgg:{bgg_id}"],
                    "engine": "hybrid",
                },
                {
                    "query_id": f"g{idx:03d}_cn_review",
                    "query": f"{alias} 玩家评论",
                    "doc_type": "review_digest",
                    "expected_any": [f"reviews:bgg:{bgg_id}"],
                    "engine": "hybrid",
                },
                {
                    "query_id": f"g{idx:03d}_cn_theme",
                    "query": f"{alias} {theme} 机制",
                    "doc_type": "game_overview",
                    "expected_any": [f"game:bgg:{bgg_id}"],
                    "engine": "hybrid",
                },
            ]
        )

    for idx, case in enumerate(MECHANISM_CASES, start=1):
        expected_any = list(case["expected_any"])  # type: ignore[arg-type]
        suite.extend(
            [
                {
                    "query_id": f"m{idx:03d}_cn",
                    "query": f"{case['cn']} 机制讲解",
                    "doc_type": "mechanic_profile",
                    "expected_any": expected_any,
                    "engine": "hybrid",
                },
                {
                    "query_id": f"m{idx:03d}_en",
                    "query": f"{case['en']} mechanism",
                    "doc_type": "mechanic_profile",
                    "expected_any": expected_any,
                    "engine": "hybrid",
                },
            ]
        )
    return suite


EXPANDED_RETRIEVAL_SUITE: list[RetrievalQuery] = build_suite()
