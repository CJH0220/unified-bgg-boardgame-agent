#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
bgg-26m-reviews.csv 全量单遍核查（2GB / 2600 万行）。

为什么不用 profile_csv.py 的结果：该文件按游戏聚簇排序，前 300 万行只覆盖 60 款游戏，
任何前缀抽样都严重有偏，必须整表扫一遍。

产出 _profiles/reviews_facts.json
"""
import csv, io, json, os, statistics, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(BASE, "bgg-reviews-jvanelteren", "raw", "bgg-26m-reviews.csv")
csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

users, games = {}, {}
n = with_comment = 0
below1 = above10 = noninteger = 0
hist = {}
clen_sum = 0
clen_max = 0
index_is_sequential = True
expect = 0

with io.open(SRC, encoding="utf-8-sig", newline="") as f:
    rdr = csv.reader(f)
    header = next(rdr)
    print("header:", header, flush=True)
    idx = {name: i for i, name in enumerate(header)}
    i_user, i_rating, i_comment = idx.get("user"), idx.get("rating"), idx.get("comment")
    i_id, i_name = idx.get("ID"), idx.get("name")
    for rec in rdr:
        n += 1
        u = rec[i_user]
        users[u] = users.get(u, 0) + 1
        g = rec[i_id]
        games[g] = games.get(g, 0) + 1
        v = float(rec[i_rating])
        if v < 1:
            below1 += 1
        elif v > 10:
            above10 += 1
        if v == int(v):
            hist[int(v)] = hist.get(int(v), 0) + 1
        else:
            noninteger += 1
        c = rec[i_comment]
        if c:
            with_comment += 1
            L = len(c)
            clen_sum += L
            if L > clen_max:
                clen_max = L
        if index_is_sequential:
            try:
                if int(rec[0]) != expect:
                    index_is_sequential = False
            except ValueError:
                index_is_sequential = False
            expect += 1
        if n % 5_000_000 == 0:
            print("  ...%d rows" % n, flush=True)

uc = sorted(users.values())
gc = sorted(games.values())
facts = {
    "rows": n,
    "unique_users": len(users),
    "unique_games": len(games),
    "reviews_with_text": with_comment,
    "text_pct": round(100.0 * with_comment / n, 2),
    "avg_comment_len": round(clen_sum / with_comment, 1) if with_comment else 0,
    "max_comment_len": clen_max,
    "first_col_is_sequential_index": index_is_sequential,
    "ratings_below_1": below1,
    "ratings_above_10": above10,
    "non_integer_ratings": noninteger,
    "non_integer_pct": round(100.0 * noninteger / n, 2),
    "integer_histogram": dict(sorted(hist.items())),
    "reviews_per_user": {"min": uc[0], "p50": uc[len(uc) // 2], "p90": uc[int(len(uc) * 0.9)],
                         "max": uc[-1], "mean": round(statistics.mean(uc), 2)},
    "reviews_per_game": {"min": gc[0], "p50": gc[len(gc) // 2], "p90": gc[int(len(gc) * 0.9)],
                         "max": gc[-1], "mean": round(statistics.mean(gc), 2)},
    "single_review_users": sum(1 for c in uc if c == 1),
}
out = os.path.join(BASE, "_profiles", "reviews_facts.json")
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(facts, f, ensure_ascii=False, indent=1)
print(json.dumps(facts, ensure_ascii=False, indent=1))
print("wrote", out)
