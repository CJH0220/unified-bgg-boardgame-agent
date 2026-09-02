#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
宽表（0/1 标签矩阵）摘要器 —— 面向 mechanics / themes / subcategories / *_reduced。

profile_csv.py 会给每列都产出统计，宽表几千列时人读不过来；本脚本直接从原始 csv 算：
  - 行数 / 列数
  - 每行标签数的分布（min/median/mean/max）—— 即「一款游戏平均几个机制」
  - 标签流行度 TopN 与「零标签游戏数」
  - 非 0/1 值告警

用法:
    python digest_wide.py bgg-threnjen/raw/mechanics.csv [--top 40]
    python digest_wide.py --all          # 扫所有已知宽表
输出到 stdout，同时写 _profiles/<dataset>__<file>.digest.json
"""
import csv, io, json, os, statistics, sys

HERE     = os.path.dirname(os.path.abspath(__file__))
BASE     = os.path.dirname(HERE)
PROFILES = os.path.join(BASE, "_profiles")

WIDE_DEFAULT = [
    "bgg-threnjen/raw/mechanics.csv",
    "bgg-threnjen/raw/themes.csv",
    "bgg-threnjen/raw/subcategories.csv",
    "bgg-threnjen/raw/designers_reduced.csv",
    "bgg-threnjen/raw/artists_reduced.csv",
    "bgg-threnjen/raw/publishers_reduced.csv",
]

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


def digest(rel, top=40):
    path = os.path.join(BASE, rel.replace("/", os.sep))
    with io.open(path, encoding="utf-8-sig", newline="") as f:
        rdr = csv.reader(f)
        header = next(rdr)
        # ⚠️ 不能假设主键在第 0 列：mechanics/themes/subcategories 的 BGGId 在首列，
        # 但 designers/artists/publishers_reduced 的 BGGId 在**倒数第二列**（首列是实体名）。
        # mattadamhouser 的 themes_2023.csv 还带一个无名索引列，主键 game_id 在第 1 列
        key_idx = 0
        for cand in ("BGGId", "game_id", "ID"):
            if cand in header:
                key_idx = header.index(cand)
                break
        label_idx = [i for i in range(len(header)) if i != key_idx]
        labels = [header[i] for i in label_idx]
        pos = [0] * len(labels)
        per_row = []
        weird = {}
        rows = 0
        for rec in rdr:
            rows += 1
            k = 0
            for j, i in enumerate(label_idx):
                v = rec[i] if i < len(rec) else ""
                if v == "1":
                    pos[j] += 1
                    k += 1
                elif v != "0":
                    weird[v] = weird.get(v, 0) + 1
            per_row.append(k)
    order = sorted(range(len(labels)), key=lambda i: -pos[i])
    out = {
        "file": rel,
        "rows": rows,
        "key_column": header[key_idx],
        "key_column_index": key_idx,
        "total_columns": len(header),
        "label_columns": len(labels),
        "labels_per_row": {
            "min": min(per_row), "max": max(per_row),
            "mean": round(statistics.mean(per_row), 3),
            "median": statistics.median(per_row),
            "zero_label_rows": sum(1 for k in per_row if k == 0),
        },
        "non_binary_values_distinct": len(weird),
        "non_binary_values_sample": dict(list(sorted(weird.items()))[:10]),
        "top_labels": [{"label": labels[i], "n": pos[i], "pct": round(100.0 * pos[i] / rows, 2)}
                       for i in order[:top]],
        "singleton_labels": sum(1 for p in pos if p == 1),
        "empty_labels": sum(1 for p in pos if p == 0),
    }
    return out


def main():
    argv = sys.argv[1:]
    top = 40
    if "--top" in argv:
        i = argv.index("--top")
        top = int(argv[i + 1])
        del argv[i:i + 2]          # 把 --top 及其取值一起摘掉，否则取值会被当成文件名
    args = [a for a in argv if not a.startswith("--")]
    targets = WIDE_DEFAULT if ("--all" in sys.argv or not args) else args
    os.makedirs(PROFILES, exist_ok=True)
    for rel in targets:
        p = os.path.join(BASE, rel.replace("/", os.sep))
        if not os.path.exists(p):
            print("skip (missing): %s" % rel)
            continue
        d = digest(rel, top=top)
        ds, fn = rel.split("/")[0], os.path.basename(rel)
        with io.open(os.path.join(PROFILES, "%s__%s.digest.json" % (ds, fn)), "w", encoding="utf-8") as fh:
            json.dump(d, fh, ensure_ascii=False, indent=1)
        print("\n=== %s  rows=%d  cols=%d  key=%s@%d  label_cols=%d" %
              (rel, d["rows"], d["total_columns"], d["key_column"], d["key_column_index"],
               d["label_columns"]))
        lp = d["labels_per_row"]
        print("    labels/row: mean=%s median=%s min=%s max=%s  zero-label rows=%d" %
              (lp["mean"], lp["median"], lp["min"], lp["max"], lp["zero_label_rows"]))
        print("    singleton labels=%d  empty labels=%d  non-binary distinct=%d %s" %
              (d["singleton_labels"], d["empty_labels"], d["non_binary_values_distinct"],
               d["non_binary_values_sample"] or ""))
        for r in d["top_labels"]:
            print("      %-46s %7d  %5.2f%%" % (r["label"][:46], r["n"], r["pct"]))


if __name__ == "__main__":
    main()
