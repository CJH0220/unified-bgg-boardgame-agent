"""Shared retrieval helpers for the unified_bgg local indexes."""
from __future__ import annotations

import re
import sys
from collections import Counter
from typing import Any

STOPWORDS = {
    "a", "about", "after", "all", "also", "an", "and", "any", "are", "as",
    "at", "be", "been", "board", "bgg", "but", "by", "can", "comment",
    "comments", "digest", "do", "does", "during", "each", "for", "from",
    "game", "games", "has", "have", "if", "in", "into", "is", "it", "its",
    "may", "more", "not", "of", "on", "one", "or", "other", "overview",
    "play", "played", "player", "players", "review", "reviews", "rules",
    "selected", "some", "supports", "than", "that", "the", "their", "them",
    "there", "these", "this", "to", "turn", "user", "users", "was", "were",
    "when", "which", "who", "will", "with", "you", "your",
}

QUERY_EXPANSIONS = {
    # High-confidence Chinese game aliases. Values use English tokens already present in local indexes.
    "卡坦岛": "CATAN Catan Settlers trading negotiation dice resource production",
    "卡坦": "CATAN Catan Settlers trading negotiation dice resource production",
    "殖民者": "Settlers Catan trading negotiation resource production",
    "卡卡颂": "Carcassonne tile placement tile laying area majority followers",
    "幽港迷城 狮子之颚": "Gloomhaven Jaws of the Lion cooperative campaign fantasy tactical combat",
    "狮子之颚": "Gloomhaven Jaws of the Lion cooperative campaign tactical combat",
    "幽港迷城": "Gloomhaven cooperative campaign fantasy tactical combat",
    "晦暗港湾": "Gloomhaven cooperative campaign fantasy tactical combat",
    "伯明翰重工业": "Brass Birmingham economic network route building industry canals rails",
    "伯明翰 重工业": "Brass Birmingham economic network route building industry canals rails",
    "瘟疫危机传承第一季": "Pandemic Legacy Season 1 cooperative legacy campaign disease",
    "瘟疫危机 传承": "Pandemic Legacy Season 1 cooperative legacy campaign disease",
    "方舟动物园": "Ark Nova zoo animal conservation card drafting tile placement",
    "暮光帝国第四版": "Twilight Imperium Fourth Edition space negotiation area control",
    "暮光帝国": "Twilight Imperium Fourth Edition space negotiation area control",
    "沙丘帝国": "Dune Imperium deck building worker placement political intrigue",
    "殖民火星": "Terraforming Mars engine building card drafting tile placement science fiction",
    "魔戒圣战": "War of the Ring Second Edition fantasy war dice cards hidden movement",
    "魔戒之战": "War of the Ring Second Edition fantasy war dice cards hidden movement",
    "星球大战反叛": "Star Wars Rebellion asymmetric conflict hidden movement area control",
    "星球大战 反叛": "Star Wars Rebellion asymmetric conflict hidden movement area control",
    "灵迹岛": "Spirit Island cooperative variable player powers area control invaders",
    "盖亚计划": "Gaia Project space economy network route building variable powers",
    "冷战热斗": "Twilight Struggle card driven area influence political wargame",
    "历史巨轮": "Through the Ages A New Story of Civilization civilization card drafting development",
    "文明新篇章": "Through the Ages A New Story of Civilization civilization card drafting development",
    "勃艮第城堡": "The Castles of Burgundy dice rolling tile placement set collection",
    "车票之旅": "Ticket to Ride train route building set collection network",
    "铁路环游": "Ticket to Ride train route building set collection network",
    "皇舆争霸": "Dominion deck building card market hand management",
    "领土": "Dominion deck building card market hand management",
    "行动代号": "Codenames word association deduction teams party game",
    "花砖物语": "Azul tile drafting pattern building abstract strategy",
    "璀璨宝石": "Splendor engine building set collection card development",
    "情书": "Love Letter deduction hand management bluffing quick card game",
    "瘟疫危机": "Pandemic cooperative disease outbreak hand management action points",
    "七大奇迹": "7 Wonders card drafting civilization set collection simultaneous action",
    "妙语说书人": "Dixit storytelling voting party imagination cards",
    "拼布艺术": "Patchwork two player tile placement time track puzzle",
    "小世界": "Small World area majority variable player powers fantasy conquest",
    "花火": "Hanabi cooperative hand management deduction limited communication",
    "东京之王": "King of Tokyo dice rolling push your luck monster combat",
    "星际探险队": "The Crew Quest for Planet Nine cooperative trick taking missions",
    "第九行星": "The Crew Quest for Planet Nine cooperative trick taking missions",
    "深海任务": "The Crew Mission Deep Sea cooperative trick taking missions",
    # Common Chinese mechanism phrases.
    "拼放版图": "tile placement tile laying modular board",
    "版图拼放": "tile placement tile laying modular board",
    "版图放置": "tile placement tile laying modular board",
    "牌库构筑": "deck bag pool building deck building card market",
    "卡牌构筑": "deck bag pool building deck building card market",
    "牌组构筑": "deck bag pool building deck building card market",
    "工人放置": "worker placement action drafting worker placement",
    "掷骰": "dice rolling random production",
    "骰子": "dice rolling random production",
    "交易": "trading negotiation resource exchange",
    "谈判": "negotiation trading bargaining",
    "协商": "negotiation trading bargaining",
    "合作": "cooperative game campaign teamwork",
    "合作游戏": "cooperative game cooperative teamwork",
    "战役": "scenario mission campaign game legacy campaign",
    "区域控制": "area majority influence area control",
    "区域优势": "area majority influence area control",
    "区域移动": "area movement map movement",
    "行动点": "action points action allowance",
    "手牌管理": "hand management cards hand limit",
    "成套收集": "set collection collecting sets",
    "套装收集": "set collection collecting sets",
    "可变玩家能力": "variable player powers asymmetric factions",
    "玩家能力可变": "variable player powers asymmetric factions",
    "可变设置": "variable set up modular setup",
    "路线建设": "network and route building route building connections",
    "网络建设": "network and route building route building connections",
    "同时行动选择": "simultaneous action selection simultaneous play",
    "卡牌轮抽": "card drafting drafting cards",
    "选牌": "card drafting drafting cards",
    "隐蔽身份": "hidden roles social deduction roles",
    "隐藏身份": "hidden roles social deduction roles",
    "讲故事": "storytelling voting imagination",
    "吃墩": "trick taking card game",
    "逼牌": "trick taking card game",
    "赌运气": "push your luck press your luck risk reward",
    "冒险押注": "push your luck press your luck risk reward",
    "虚张声势": "betting and bluffing bluffing hidden information",
    "模块化版图": "modular board variable setup tiles",
    "六角格": "hexagon grid hex map",
    "收入": "income resource production",
    "随机生产": "random production dice resource",
    "拍卖竞价": "auction bidding auction fixed placement sealed bid",
    # Query intent expansions.
    "评论": "review comments digest user rating snippets",
    "热门评论": "review comments digest user rating snippets",
    "玩家评论": "review comments digest user rating snippets",
    "简介": "overview description summary mechanisms rating",
    "游戏简介": "overview description summary mechanisms rating",
    "机制": "mechanic mechanisms category taxonomy",
    "规则": "rules turn flow objective scoring setup",
}

KNOWN_GAME_ROUTES = [
    {
        "bgg_id": 291457,
        "title": "Gloomhaven: Jaws of the Lion",
        "needles": ["幽港迷城 狮子之颚", "狮子之颚"],
        "english_any": ["gloomhaven jaws", "jaws of the lion"],
        "english_exclude": [],
    },
    {
        "bgg_id": 161936,
        "title": "Pandemic Legacy: Season 1",
        "needles": ["瘟疫危机传承第一季", "瘟疫危机 传承"],
        "english_any": ["pandemic legacy season 1", "pandemic legacy: season 1"],
        "english_exclude": [],
    },
    {
        "bgg_id": 324856,
        "title": "The Crew: Mission Deep Sea",
        "needles": ["深海任务"],
        "english_any": ["the crew mission deep sea", "the crew: mission deep sea"],
        "english_exclude": [],
    },
    {
        "bgg_id": 284083,
        "title": "The Crew: The Quest for Planet Nine",
        "needles": ["星际探险队", "第九行星"],
        "english_any": ["the crew quest for planet nine", "the crew: the quest for planet nine"],
        "english_exclude": ["mission deep sea"],
    },
    {
        "bgg_id": 13,
        "title": "CATAN",
        "needles": ["卡坦岛", "卡坦", "殖民者"],
        "english_any": ["catan"],
        "english_exclude": ["junior", "histories", "rivals", "card game", "starfarers"],
    },
    {
        "bgg_id": 822,
        "title": "Carcassonne",
        "needles": ["卡卡颂"],
        "english_any": ["carcassonne"],
        "english_exclude": ["hunters", "inns", "cathedrals", "traders", "builders"],
    },
    {
        "bgg_id": 174430,
        "title": "Gloomhaven",
        "needles": ["幽港迷城", "晦暗港湾"],
        "english_any": ["gloomhaven"],
        "english_exclude": ["jaws", "lion", "second edition", "founders"],
    },
    {"bgg_id": 224517, "title": "Brass: Birmingham", "needles": ["伯明翰重工业", "伯明翰 重工业"], "english_any": ["brass birmingham", "brass: birmingham"], "english_exclude": []},
    {"bgg_id": 342942, "title": "Ark Nova", "needles": ["方舟动物园"], "english_any": ["ark nova"], "english_exclude": []},
    {"bgg_id": 233078, "title": "Twilight Imperium: Fourth Edition", "needles": ["暮光帝国第四版", "暮光帝国"], "english_any": ["twilight imperium fourth edition", "twilight imperium: fourth edition"], "english_exclude": []},
    {"bgg_id": 316554, "title": "Dune: Imperium", "needles": ["沙丘帝国"], "english_any": ["dune imperium", "dune: imperium"], "english_exclude": ["uprising"]},
    {"bgg_id": 167791, "title": "Terraforming Mars", "needles": ["殖民火星"], "english_any": ["terraforming mars"], "english_exclude": ["ares expedition", "dice game"]},
    {"bgg_id": 115746, "title": "War of the Ring: Second Edition", "needles": ["魔戒圣战", "魔戒之战"], "english_any": ["war of the ring second edition", "war of the ring: second edition"], "english_exclude": []},
    {"bgg_id": 187645, "title": "Star Wars: Rebellion", "needles": ["星球大战反叛", "星球大战 反叛"], "english_any": ["star wars rebellion", "star wars: rebellion"], "english_exclude": []},
    {"bgg_id": 162886, "title": "Spirit Island", "needles": ["灵迹岛"], "english_any": ["spirit island"], "english_exclude": []},
    {"bgg_id": 220308, "title": "Gaia Project", "needles": ["盖亚计划"], "english_any": ["gaia project"], "english_exclude": []},
    {"bgg_id": 12333, "title": "Twilight Struggle", "needles": ["冷战热斗"], "english_any": ["twilight struggle"], "english_exclude": []},
    {"bgg_id": 182028, "title": "Through the Ages: A New Story of Civilization", "needles": ["历史巨轮", "文明新篇章"], "english_any": ["through the ages a new story", "through the ages: a new story", "through the ages civilization"], "english_exclude": []},
    {"bgg_id": 84876, "title": "The Castles of Burgundy", "needles": ["勃艮第城堡"], "english_any": ["castles of burgundy", "the castles of burgundy"], "english_exclude": []},
    {"bgg_id": 9209, "title": "Ticket to Ride", "needles": ["车票之旅", "铁路环游"], "english_any": ["ticket to ride"], "english_exclude": ["europe", "legacy", "rails"]},
    {"bgg_id": 36218, "title": "Dominion", "needles": ["皇舆争霸", "领土"], "english_any": ["dominion"], "english_exclude": ["intrigue", "prosperity", "seaside"]},
    {"bgg_id": 178900, "title": "Codenames", "needles": ["行动代号"], "english_any": ["codenames"], "english_exclude": ["duet", "pictures"]},
    {"bgg_id": 230802, "title": "Azul", "needles": ["花砖物语"], "english_any": ["azul"], "english_exclude": ["summer pavilion", "stained glass", "queen"]},
    {"bgg_id": 148228, "title": "Splendor", "needles": ["璀璨宝石"], "english_any": ["splendor"], "english_exclude": ["duel", "cities"]},
    {"bgg_id": 129622, "title": "Love Letter", "needles": ["情书"], "english_any": ["love letter"], "english_exclude": []},
    {"bgg_id": 30549, "title": "Pandemic", "needles": ["瘟疫危机"], "english_any": ["pandemic"], "english_exclude": ["legacy", "iberia", "reign", "fall of rome"]},
    {"bgg_id": 68448, "title": "7 Wonders", "needles": ["七大奇迹"], "english_any": ["7 wonders"], "english_exclude": ["duel", "architects"]},
    {"bgg_id": 39856, "title": "Dixit", "needles": ["妙语说书人"], "english_any": ["dixit"], "english_exclude": []},
    {"bgg_id": 163412, "title": "Patchwork", "needles": ["拼布艺术"], "english_any": ["patchwork"], "english_exclude": []},
    {"bgg_id": 40692, "title": "Small World", "needles": ["小世界"], "english_any": ["small world"], "english_exclude": []},
    {"bgg_id": 98778, "title": "Hanabi", "needles": ["花火"], "english_any": ["hanabi"], "english_exclude": []},
    {"bgg_id": 70323, "title": "King of Tokyo", "needles": ["东京之王"], "english_any": ["king of tokyo"], "english_exclude": []},
]


def expand_query(query: str) -> str:
    """Append auditable Chinese-to-English expansion terms."""
    additions: list[str] = []
    for needle, expansion in QUERY_EXPANSIONS.items():
        if needle in query:
            additions.append(expansion)
    if not additions:
        return query
    return " ".join([query, *additions])


def detect_game_route(query: str) -> dict[str, Any] | None:
    """Detect a small set of high-confidence game aliases for exact BGG routing."""
    lowered = query.lower()
    for route in KNOWN_GAME_ROUTES:
        if any(needle and needle in query for needle in route["needles"]):
            return {"bgg_id": route["bgg_id"], "title": route["title"]}
        if any(needle in lowered for needle in route["english_any"]):
            if not any(excluded in lowered for excluded in route["english_exclude"]):
                return {"bgg_id": route["bgg_id"], "title": route["title"]}
    return None


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for token in re.findall(r"[a-z0-9]+", text.lower()):
        if len(token) < 2 or len(token) > 40:
            continue
        if token in STOPWORDS:
            continue
        if token.isdigit() and len(token) != 4:
            continue
        tokens.append(token)
    return tokens


def weighted_doc_terms(row: dict[str, Any]) -> Counter[str]:
    counter: Counter[str] = Counter()
    fields = [
        (row.get("title") or "", 12),
        (row.get("mechanic") or "", 12),
        (row.get("mechanics_text") or "", 10),
        (row.get("doc_type") or "", 2),
        (row.get("text") or "", 1),
    ]
    for value, weight in fields:
        for token in tokenize(str(value)):
            counter[token] += weight
    return counter


def query_terms(query: str) -> Counter[str]:
    return Counter(tokenize(expand_query(query)))


def configure_utf8_stdout() -> None:
    """Avoid Windows console encoding failures for Unicode titles/snippets."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
