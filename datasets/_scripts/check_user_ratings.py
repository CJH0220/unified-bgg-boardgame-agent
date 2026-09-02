#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
user_ratings.csv 的精确事实核查（19M 行全量单遍扫描），产出写文档需要的硬数字：
唯一用户数、评分越界情况、整数/小数评分占比、人均与每游戏评分数分布。
结果写到 _profiles/user_ratings_facts.json。
"""
import csv, io, json, os, statistics

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(BASE, "bgg-threnjen", "raw", "user_ratings.csv")

users = {}
games = {}
n = 0
below1 = 0
above10 = 0
noninteger = 0
exact_int = 0
hist_int = {}

with io.open(SRC, encoding="utf-8-sig", newline="") as f:
    r = csv.DictReader(f)
    print("header:", r.fieldnames, flush=True)
    for row in r:
        n += 1
        u = row["Username"]
        users[u] = users.get(u, 0) + 1
        g = row["BGGId"]
        games[g] = games.get(g, 0) + 1
        v = float(row["Rating"])
        if v < 1:
            below1 += 1
        if v > 10:
            above10 += 1
        if v == int(v):
            exact_int += 1
            hist_int[int(v)] = hist_int.get(int(v), 0) + 1
        else:
            noninteger += 1
        if n % 5_000_000 == 0:
            print("  ...%d rows" % n, flush=True)

uc = sorted(users.values())
gc = sorted(games.values())
facts = {
    "rows": n,
    "unique_users": len(users),
    "unique_games": len(games),
    "ratings_below_1": below1,
    "ratings_above_10": above10,
    "integer_ratings": exact_int,
    "non_integer_ratings": noninteger,
    "non_integer_pct": round(100.0 * noninteger / n, 2),
    "integer_histogram": dict(sorted(hist_int.items())),
    "ratings_per_user": {"min": uc[0], "p50": uc[len(uc) // 2], "p90": uc[int(len(uc) * 0.9)],
                         "max": uc[-1], "mean": round(statistics.mean(uc), 2)},
    "ratings_per_game": {"min": gc[0], "p50": gc[len(gc) // 2], "p90": gc[int(len(gc) * 0.9)],
                         "max": gc[-1], "mean": round(statistics.mean(gc), 2)},
    "single_rating_users": sum(1 for c in uc if c == 1),
}
out = os.path.join(BASE, "_profiles", "user_ratings_facts.json")
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(facts, f, ensure_ascii=False, indent=1)
print(json.dumps(facts, ensure_ascii=False, indent=1))
print("wrote", out)
