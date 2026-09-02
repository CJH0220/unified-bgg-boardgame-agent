"""Curated retrieval queries for Phase 9 validation and sample export."""
from __future__ import annotations

from typing import TypedDict


class RetrievalQuery(TypedDict, total=False):
    query_id: str
    query: str
    doc_type: str
    expected_any: list[str]
    engine: str


RETRIEVAL_SUITE: list[RetrievalQuery] = [
    {
        "query_id": "q01",
        "query": "卡坦岛 游戏简介",
        "doc_type": "game_overview",
        "expected_any": ["game:bgg:13"],
        "engine": "hybrid",
    },
    {
        "query_id": "q02",
        "query": "卡坦岛 交易 评论",
        "doc_type": "review_digest",
        "expected_any": ["reviews:bgg:13"],
        "engine": "hybrid",
    },
    {
        "query_id": "q03",
        "query": "卡卡颂 规则",
        "doc_type": "game_overview",
        "expected_any": ["game:bgg:822"],
        "engine": "hybrid",
    },
    {
        "query_id": "q04",
        "query": "卡卡颂 评论",
        "doc_type": "review_digest",
        "expected_any": ["reviews:bgg:822"],
        "engine": "hybrid",
    },
    {
        "query_id": "q05",
        "query": "幽港迷城 合作 战役",
        "doc_type": "game_overview",
        "expected_any": ["game:bgg:174430"],
        "engine": "hybrid",
    },
    {
        "query_id": "q06",
        "query": "Brass Birmingham economic network route building",
        "doc_type": "game_overview",
        "expected_any": ["game:bgg:224517"],
        "engine": "hybrid",
    },
    {
        "query_id": "q07",
        "query": "Through the Ages civilization",
        "doc_type": "game_overview",
        "expected_any": ["game:bgg:182028"],
        "engine": "hybrid",
    },
    {
        "query_id": "q08",
        "query": "worker placement",
        "doc_type": "mechanic_profile",
        "expected_any": ["mechanic:worker-placement:profile"],
        "engine": "hybrid",
    },
    {
        "query_id": "q09",
        "query": "deck bag pool building",
        "doc_type": "mechanic_profile",
        "expected_any": ["mechanic:deck,-bag,-and-pool-building:profile"],
        "engine": "hybrid",
    },
    {
        "query_id": "q10",
        "query": "dice rolling mechanic",
        "doc_type": "mechanic_profile",
        "expected_any": ["mechanic:dice-rolling:profile"],
        "engine": "hybrid",
    },
    {
        "query_id": "q11",
        "query": "auction bidding",
        "doc_type": "mechanic_profile",
        "expected_any": ["mechanic:auction---bidding:profile"],
        "engine": "hybrid",
    },
    {
        "query_id": "q12",
        "query": "popular comments for Catan",
        "doc_type": "review_digest",
        "expected_any": ["reviews:bgg:13"],
        "engine": "hybrid",
    },
]
