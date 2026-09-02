#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
把 profile_csv.py 产出的 JSON 压成一行一列的紧凑表，方便快速读 schema。

用法:
    python show_profile.py bgg-threnjen__user_ratings.csv.json
    python show_profile.py bgg-threnjen__ratings_distribution.csv.json --max 120
"""
import io, json, os, sys

HERE     = os.path.dirname(os.path.abspath(__file__))
PROFILES = os.path.join(os.path.dirname(HERE), "_profiles")


def main():
    argv = sys.argv[1:]
    maxcols = 400
    if "--max" in argv:
        i = argv.index("--max")
        maxcols = int(argv[i + 1])
        del argv[i:i + 2]
    for name in argv:
        p = name if os.path.exists(name) else os.path.join(PROFILES, name)
        with io.open(p, encoding="utf-8") as f:
            d = json.load(f)
        print("### %s | %s cols | %s rows%s | %s | %.1f MB" % (
            d.get("file"), d.get("n_columns"), d.get("rows_scanned"),
            " (TRUNCATED)" if d.get("scan_truncated") else "",
            d.get("encoding"), (d.get("bytes") or 0) / 1048576.0))
        print("%-34s %-7s %7s %9s %12s %12s %12s  %s" %
              ("column", "dtype", "null%", "distinct", "min", "max", "mean", "samples"))
        for c in d["columns"][:maxcols]:
            print("%-34s %-7s %7s %9s %12s %12s %12s  %s" % (
                c["name"][:34], c["dtype"], c["null_pct"], c["distinct"],
                c.get("min", ""), c.get("max", ""), c.get("mean", ""),
                " | ".join(str(s)[:22] for s in c["samples"][:2])))
        if d["n_columns"] > maxcols:
            print("... %d more columns omitted" % (d["n_columns"] - maxcols))
        print()


if __name__ == "__main__":
    main()
