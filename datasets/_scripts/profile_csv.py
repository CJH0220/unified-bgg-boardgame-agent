#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
纯标准库 CSV 剖析器 —— 为 datasets/*/raw/*.csv 生成真实 schema 事实，供人工写 DATASET.md。
不依赖 pandas，Python 3.8+ 可用。

用法:
    python profile_csv.py                      # 剖析 datasets 下全部 csv
    python profile_csv.py bgg-threnjen         # 只剖析某个数据集目录
    python profile_csv.py --full               # 大文件也做全量扫描（慢）

产出:
    _profiles/<dataset-dir>__<filename>.json   每列: 类型/空值率/基数/数值区间/样例
    _profiles/_summary.json                    行列数汇总
"""
import csv, io, json, os, sys, math, time

HERE     = os.path.dirname(os.path.abspath(__file__))
BASE     = os.path.dirname(HERE)
PROFILES = os.path.join(BASE, "_profiles")

SNIFF_ROWS      = 5000        # 用于推断类型 / 采样的前 N 行
MAX_FULL_ROWS   = 3_000_000   # 非 --full 模式下全量扫描的行数上限
DISTINCT_CAP    = 100_000     # 基数统计上限
SAMPLE_VALUES   = 6           # 每列保留的样例值个数
TOPK            = 12          # 低基数列展示的取值分布

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


def open_text(path):
    """BOM 优先，失败退 latin-1（部分 Kaggle 快照混了非 UTF-8 字节）。"""
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            f = io.open(path, "r", encoding=enc, newline="")
            f.read(65536)
            f.seek(0)
            return f, enc
        except UnicodeDecodeError:
            try:
                f.close()
            except Exception:
                pass
    return io.open(path, "r", encoding="latin-1", errors="replace", newline=""), "latin-1/replace"


def sniff_delim(path):
    f, enc = open_text(path)
    head = f.read(65536)
    f.close()
    try:
        return csv.Sniffer().sniff(head, delimiters=",;\t|").delimiter, enc
    except Exception:
        counts = {d: head.count(d) for d in [",", ";", "\t", "|"]}
        return max(counts, key=counts.get), enc


NULLS = {"", "na", "n/a", "nan", "null", "none", "\\n", "-"}


def classify(v):
    """返回 ('int'|'float'|'bool'|'str', 解析值或 None)。"""
    s = v.strip()
    if s.lower() in NULLS:
        return "null", None
    if s in ("0", "1"):
        return "bool01", float(s)
    try:
        i = int(s)
        return "int", float(i)
    except ValueError:
        pass
    try:
        fl = float(s)
        if math.isnan(fl) or math.isinf(fl):
            return "null", None
        return "float", fl
    except ValueError:
        pass
    if s.lower() in ("true", "false"):
        return "bool", 1.0 if s.lower() == "true" else 0.0
    return "str", None


class Col:
    __slots__ = ("name", "n", "nulls", "kinds", "mn", "mx", "sum", "num_n",
                 "distinct", "distinct_overflow", "samples", "maxlen", "counter", "counter_off")

    def __init__(self, name):
        self.name = name
        self.n = self.nulls = self.num_n = 0
        self.kinds = {}
        self.mn = self.mx = None
        self.sum = 0.0
        self.distinct = set()
        self.distinct_overflow = False
        self.samples = []
        self.maxlen = 0
        self.counter = {}
        self.counter_off = False

    def add(self, v):
        self.n += 1
        k, num = classify(v)
        self.kinds[k] = self.kinds.get(k, 0) + 1
        if k == "null":
            self.nulls += 1
            return
        if len(v) > self.maxlen:
            self.maxlen = len(v)
        if num is not None:
            self.num_n += 1
            self.sum += num
            if self.mn is None or num < self.mn:
                self.mn = num
            if self.mx is None or num > self.mx:
                self.mx = num
        if not self.distinct_overflow:
            self.distinct.add(v)
            if len(self.distinct) > DISTINCT_CAP:
                self.distinct_overflow = True
                self.distinct = set()
        if not self.counter_off:
            self.counter[v] = self.counter.get(v, 0) + 1
            if len(self.counter) > 200:
                self.counter_off = True
                self.counter = {}
        if len(self.samples) < SAMPLE_VALUES and v.strip():
            if v not in self.samples:
                self.samples.append(v[:120])

    def dump(self):
        kinds = {k: v for k, v in sorted(self.kinds.items(), key=lambda x: -x[1])}
        non_null = self.n - self.nulls
        # 主类型 = 除 null 外占比最高者；bool01 只有在没有其它数值类型时才成立
        real = {k: v for k, v in kinds.items() if k != "null"}
        dtype = max(real, key=real.get) if real else "empty"
        if dtype == "bool01" and ("int" in real or "float" in real):
            dtype = "int"
        d = {
            "name": self.name,
            "dtype": dtype,
            "kind_counts": kinds,
            "rows": self.n,
            "nulls": self.nulls,
            "null_pct": round(100.0 * self.nulls / self.n, 3) if self.n else None,
            "distinct": (">%d" % DISTINCT_CAP) if self.distinct_overflow else len(self.distinct),
            "max_str_len": self.maxlen,
            "samples": self.samples,
        }
        if self.num_n:
            d["min"] = self.mn
            d["max"] = self.mx
            d["mean"] = round(self.sum / self.num_n, 4)
            d["numeric_pct"] = round(100.0 * self.num_n / non_null, 2) if non_null else None
        if not self.counter_off and self.counter:
            top = sorted(self.counter.items(), key=lambda x: -x[1])[:TOPK]
            d["top_values"] = [{"v": k[:60], "n": c} for k, c in top]
        return d


def profile(path, full=False):
    delim, enc = sniff_delim(path)
    f, _ = open_text(path)
    t0 = time.time()
    limit = None if full else MAX_FULL_ROWS
    with f:
        rdr = csv.reader(f, delimiter=delim)
        try:
            header = next(rdr)
        except StopIteration:
            return {"file": os.path.basename(path), "error": "empty file"}
        header = [h.strip() or ("col_%d" % i) for i, h in enumerate(header)]
        cols = [Col(h) for h in header]
        ncol = len(cols)
        rows = 0
        ragged = 0
        for rec in rdr:
            if len(rec) != ncol:
                ragged += 1
                if len(rec) < ncol:
                    rec = rec + [""] * (ncol - len(rec))
            for i in range(ncol):
                cols[i].add(rec[i])
            rows += 1
            if limit and rows >= limit:
                break
        truncated = bool(limit and rows >= limit)
    return {
        "file": os.path.basename(path),
        "path": os.path.relpath(path, BASE).replace("\\", "/"),
        "bytes": os.path.getsize(path),
        "encoding": enc,
        "delimiter": delim,
        "n_columns": ncol,
        "rows_scanned": rows,
        "scan_truncated": truncated,
        "ragged_rows": ragged,
        "scan_seconds": round(time.time() - t0, 1),
        "columns": [c.dump() for c in cols],
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    full = "--full" in sys.argv
    os.makedirs(PROFILES, exist_ok=True)
    dirs = args or sorted(
        d for d in os.listdir(BASE)
        if os.path.isdir(os.path.join(BASE, d, "raw")) and not d.startswith("_")
    )
    summary = []
    for d in dirs:
        raw = os.path.join(BASE, d, "raw")
        for fn in sorted(os.listdir(raw)):
            if not fn.lower().endswith((".csv", ".tsv")):
                continue
            p = os.path.join(raw, fn)
            print("profiling %s/%s (%.1f MB) ..." % (d, fn, os.path.getsize(p) / 1048576.0), flush=True)
            try:
                prof = profile(p, full=full)
            except Exception as e:
                prof = {"file": fn, "error": "%s: %s" % (type(e).__name__, e)}
            prof["dataset"] = d
            out = os.path.join(PROFILES, "%s__%s.json" % (d, fn))
            with io.open(out, "w", encoding="utf-8") as fh:
                json.dump(prof, fh, ensure_ascii=False, indent=1)
            summary.append({k: prof.get(k) for k in
                            ("dataset", "file", "bytes", "n_columns", "rows_scanned",
                             "scan_truncated", "ragged_rows", "encoding", "error")})
            print("   -> %s cols, %s rows%s" % (prof.get("n_columns"), prof.get("rows_scanned"),
                                                " (TRUNCATED)" if prof.get("scan_truncated") else ""), flush=True)
    with io.open(os.path.join(PROFILES, "_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=1)
    print("\nwrote %d profiles to %s" % (len(summary), PROFILES))


if __name__ == "__main__":
    main()
