"""Build the core unified_bgg intermediate tables.

Outputs games.csv, game_stats.csv, game_taxonomy.csv, plus a summary report.
The transform uses only stdlib modules and skips row-level ratings/reviews.
"""
from __future__ import annotations

import ast
import csv
import json
import re
import sqlite3
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
DATA = ROOT.parent
RAW_INDEX = ROOT / "raw_index"
INTERMEDIATE = ROOT / "intermediate"
DOCS = ROOT / "docs"

GAME_FIELDS = [
    "game_id", "bgg_id", "primary_name", "game_type", "year_published",
    "min_players", "max_players", "min_playtime", "max_playtime", "min_age",
    "description", "thumbnail_url", "image_url", "selected_source_datasets",
    "field_sources", "needs_review",
]
STAT_FIELDS = [
    "game_id", "bgg_id", "snapshot_date", "rank_domain", "average_rating",
    "bayes_average", "users_rated", "rank_position", "weight_average",
    "weight_votes", "stddev_rating", "median_rating", "owned", "trading",
    "wanting", "wishing", "numcomments", "source_dataset", "source_file",
]
TAX_FIELDS = [
    "game_id", "bgg_id", "taxonomy_type", "taxonomy_name_raw",
    "taxonomy_name_canonical", "taxonomy_snapshot", "mapping_confidence",
    "source_dataset", "source_file", "source_format",
]

JV_RANKS = {
    "Strategy Game Rank": "strategygames",
    "Family Game Rank": "familygames",
    "Abstract Game Rank": "abstracts",
    "Party Game Rank": "partygames",
    "Thematic Rank": "thematic",
    "War Game Rank": "wargames",
    "Customizable Rank": "cgs",
    "Children's Game Rank": "childrensgames",
}
TH_RANKS = {
    "Rank:strategygames": "strategygames",
    "Rank:familygames": "familygames",
    "Rank:abstracts": "abstracts",
    "Rank:partygames": "partygames",
    "Rank:thematic": "thematic",
    "Rank:wargames": "wargames",
    "Rank:cgs": "cgs",
    "Rank:childrensgames": "childrensgames",
}
TH_DOMAINS = {
    "Cat:Thematic": "Thematic Games",
    "Cat:Strategy": "Strategy Games",
    "Cat:War": "Wargames",
    "Cat:Family": "Family Games",
    "Cat:CGS": "Customizable Games",
    "Cat:Abstract": "Abstract Games",
    "Cat:Party": "Party Games",
    "Cat:Childrens": "Children's Games",
}


def rel(path: Path) -> str:
    return path.relative_to(DATA).as_posix()


def txt(value: Any) -> str:
    return "" if value is None else str(value).strip()


def bgg_id(value: Any) -> int | None:
    s = txt(value)
    if not s:
        return None
    if re.fullmatch(r"[+-]?\d+", s):
        n = int(s)
    elif re.fullmatch(r"[+-]?\d+\.0+", s):
        n = int(float(s))
    else:
        return None
    return n if n > 0 else None


def as_int(value: Any, *, zero_null: bool = False, max_sentinel: int | None = None) -> str:
    s = txt(value)
    if not s:
        return ""
    try:
        n = int(float(s.replace(",", ".")))
    except ValueError:
        return ""
    if zero_null and n == 0:
        return ""
    if max_sentinel is not None and n >= max_sentinel:
        return ""
    return str(n)


def as_float(value: Any, *, zero_null: bool = False, comma: bool = False) -> str:
    s = txt(value)
    if not s:
        return ""
    if comma:
        s = s.replace(",", ".")
    try:
        n = float(s)
    except ValueError:
        return ""
    if zero_null and n == 0:
        return ""
    return f"{n:.6g}"


def rank(value: Any, *, sentinel: int | None = None) -> str:
    s = as_int(value, zero_null=True)
    if not s:
        return ""
    if sentinel is not None and int(s) == sentinel:
        return ""
    return s


def listish(value: Any) -> list[str]:
    s = txt(value)
    if not s or s in {"[]", "nan", "None"}:
        return []
    if s.startswith("[") and s.endswith("]"):
        try:
            obj = ast.literal_eval(s)
        except (SyntaxError, ValueError):
            obj = None
        if isinstance(obj, list):
            return [txt(x) for x in obj if txt(x)]
    return [part.strip() for part in s.split(",") if part.strip()]


def read_csv(path: Path, *, enc: str = "utf-8-sig", delim: str = ",") -> Iterable[dict[str, str]]:
    with path.open("r", encoding=enc, newline="") as f:
        yield from csv.DictReader(f, delimiter=delim)


def quote(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def known_id_sources() -> dict[int, set[str]]:
    sources: dict[int, set[str]] = {}
    with (INTERMEDIATE / "id_map.csv").open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            n = bgg_id(row.get("bgg_id"))
            if n is not None:
                sources.setdefault(n, set()).add(txt(row.get("source_dataset")))
    return sources


def ensure(games: dict[int, dict[str, Any]], n: int) -> dict[str, Any]:
    return games.setdefault(n, {
        "game_id": f"bgg:{n}", "bgg_id": str(n), "primary_name": "",
        "game_type": "", "year_published": "", "min_players": "",
        "max_players": "", "min_playtime": "", "max_playtime": "",
        "min_age": "", "description": "", "thumbnail_url": "",
        "image_url": "", "_sources": set(), "_field_sources": {},
        "needs_review": "false",
    })


def put(game: dict[str, Any], field: str, value: str, source: str) -> None:
    if value and not game.get(field):
        game[field] = value
        game["_field_sources"][field] = source


def add_jv_games(games: dict[int, dict[str, Any]], path: Path, name_col: str) -> int:
    src = rel(path)
    c = 0
    for row in read_csv(path):
        n = bgg_id(row.get("id"))
        if n is None:
            continue
        g = ensure(games, n)
        g["_sources"].add("bgg-reviews-jvanelteren")
        put(g, "primary_name", txt(row.get(name_col)), src)
        put(g, "game_type", txt(row.get("type")), src)
        put(g, "year_published", as_int(row.get("yearpublished"), zero_null=True), src)
        put(g, "min_players", as_int(row.get("minplayers"), zero_null=True), src)
        put(g, "max_players", as_int(row.get("maxplayers"), zero_null=True, max_sentinel=99), src)
        put(g, "min_playtime", as_int(row.get("minplaytime"), zero_null=True), src)
        put(g, "max_playtime", as_int(row.get("maxplaytime"), zero_null=True), src)
        put(g, "min_age", as_int(row.get("minage"), zero_null=True), src)
        put(g, "description", txt(row.get("description")), src)
        put(g, "thumbnail_url", txt(row.get("thumbnail")), src)
        put(g, "image_url", txt(row.get("image")), src)
        c += 1
    return c


def add_th_games(games: dict[int, dict[str, Any]], path: Path) -> int:
    src = rel(path)
    c = 0
    for row in read_csv(path):
        n = bgg_id(row.get("BGGId"))
        if n is None:
            continue
        g = ensure(games, n)
        g["_sources"].add("bgg-threnjen")
        put(g, "primary_name", txt(row.get("Name")), src)
        put(g, "year_published", as_int(row.get("YearPublished"), zero_null=True), src)
        put(g, "min_players", as_int(row.get("MinPlayers"), zero_null=True), src)
        put(g, "max_players", as_int(row.get("MaxPlayers"), zero_null=True, max_sentinel=99), src)
        put(g, "min_playtime", as_int(row.get("ComMinPlaytime"), zero_null=True), src)
        put(g, "max_playtime", as_int(row.get("ComMaxPlaytime"), zero_null=True), src)
        put(g, "min_age", as_int(row.get("MfgAgeRec"), zero_null=True), src)
        put(g, "thumbnail_url", txt(row.get("ImagePath")), src)
        c += 1
    return c


def add_simple_games(games: dict[int, dict[str, Any]], path: Path, dataset: str, id_col: str, name_col: str, year_col: str, *, delim: str = ",", enc: str = "utf-8-sig") -> int:
    src = rel(path)
    c = 0
    for row in read_csv(path, enc=enc, delim=delim):
        n = bgg_id(row.get(id_col))
        if n is None:
            continue
        g = ensure(games, n)
        g["_sources"].add(dataset)
        put(g, "primary_name", txt(row.get(name_col)), src)
        put(g, "year_published", as_int(row.get(year_col), zero_null=True), src)
        if dataset == "bgg-andrewmvd":
            put(g, "min_players", as_int(row.get("Min Players"), zero_null=True), src)
            put(g, "max_players", as_int(row.get("Max Players"), zero_null=True, max_sentinel=99), src)
            put(g, "max_playtime", as_int(row.get("Play Time"), zero_null=True), src)
            put(g, "min_age", as_int(row.get("Min Age"), zero_null=True), src)
        elif dataset == "bgg-sujaykapadnis":
            put(g, "min_players", as_int(row.get("min_players"), zero_null=True), src)
            put(g, "max_players", as_int(row.get("max_players"), zero_null=True, max_sentinel=99), src)
            put(g, "min_playtime", as_int(row.get("min_playtime"), zero_null=True), src)
            put(g, "max_playtime", as_int(row.get("max_playtime"), zero_null=True), src)
            put(g, "min_age", as_int(row.get("min_age"), zero_null=True), src)
            put(g, "description", txt(row.get("description")), src)
            put(g, "thumbnail_url", txt(row.get("thumbnail")), src)
            put(g, "image_url", txt(row.get("image")), src)
        else:
            put(g, "min_players", as_int(row.get("min_players"), zero_null=True), src)
            put(g, "max_players", as_int(row.get("max_players"), zero_null=True, max_sentinel=99), src)
            put(g, "min_playtime", as_int(row.get("min_time"), zero_null=True), src)
            put(g, "max_playtime", as_int(row.get("max_time"), zero_null=True), src)
            put(g, "min_age", as_int(row.get("age"), zero_null=True), src)
        c += 1
    return c


def add_gabrio_games(games: dict[int, dict[str, Any]], path: Path) -> int:
    src = rel(path)
    cols = ["game.id", "game.type", "details.name", "details.yearpublished",
            "details.minplayers", "details.maxplayers", "details.minplaytime",
            "details.maxplaytime", "details.minage", "details.description",
            "details.thumbnail", "details.image"]
    sql = "SELECT " + ", ".join(f"{quote(c)} AS {quote(c)}" for c in cols) + " FROM BoardGames"
    c = 0
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    try:
        for row in con.execute(sql):
            n = bgg_id(row["game.id"])
            if n is None:
                continue
            g = ensure(games, n)
            g["_sources"].add("bgg-gabrio")
            put(g, "primary_name", txt(row["details.name"]), src)
            put(g, "game_type", txt(row["game.type"]), src)
            put(g, "year_published", as_int(row["details.yearpublished"], zero_null=True), src)
            put(g, "min_players", as_int(row["details.minplayers"], zero_null=True), src)
            put(g, "max_players", as_int(row["details.maxplayers"], zero_null=True, max_sentinel=99), src)
            put(g, "min_playtime", as_int(row["details.minplaytime"], zero_null=True), src)
            put(g, "max_playtime", as_int(row["details.maxplaytime"], zero_null=True), src)
            put(g, "min_age", as_int(row["details.minage"], zero_null=True), src)
            put(g, "description", txt(row["details.description"]), src)
            put(g, "thumbnail_url", txt(row["details.thumbnail"]), src)
            put(g, "image_url", txt(row["details.image"]), src)
            c += 1
    finally:
        con.close()
    return c


def build_games(id_sources: dict[int, set[str]]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    games: dict[int, dict[str, Any]] = {}
    for n, sources in id_sources.items():
        ensure(games, n)["_sources"].update(source for source in sources if source)
    counts = {
        "jv_2025": add_jv_games(games, DATA / "bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv", "name"),
        "jv_2020_detail": add_jv_games(games, DATA / "bgg-reviews-jvanelteren/raw/games_detailed_info.csv", "primary"),
        "threnjen_games": add_th_games(games, DATA / "bgg-threnjen/raw/games.csv"),
        "matt_basic": add_simple_games(games, DATA / "bgg-ranked-mattadamhouser/raw/basic_data_2023.csv", "bgg-ranked-mattadamhouser", "game_id", "name", "year"),
        "mr_2018_06": add_simple_games(games, DATA / "bgg-mrpantherson/raw/bgg_db_1806.csv", "bgg-mrpantherson", "game_id", "names", "year"),
        "andrewmvd": add_simple_games(games, DATA / "bgg-andrewmvd/raw/bgg_dataset.csv", "bgg-andrewmvd", "ID", "Name", "Year Published", delim=";"),
        "sujay": add_simple_games(games, DATA / "bgg-sujaykapadnis/raw/board_games.csv", "bgg-sujaykapadnis", "game_id", "name", "year_published"),
        "gabrio": add_gabrio_games(games, DATA / "bgg-gabrio/raw/database.sqlite"),
    }
    out = []
    for n in sorted(games):
        g = games[n]
        g["selected_source_datasets"] = ";".join(sorted(g.pop("_sources")))
        g["field_sources"] = json.dumps(g.pop("_field_sources"), ensure_ascii=False, sort_keys=True)
        if not g["primary_name"]:
            g["needs_review"] = "true"
        out.append(g)
    return out, counts


def stat(n: int, snapshot: str, dataset: str, source: str, domain: str = "overall", **vals: str) -> dict[str, str]:
    row = {k: "" for k in STAT_FIELDS}
    row.update({"game_id": f"bgg:{n}", "bgg_id": str(n), "snapshot_date": snapshot,
                "rank_domain": domain, "source_dataset": dataset, "source_file": source})
    row.update({k: v for k, v in vals.items() if k in row})
    return row


def add_jv_stats(out: list[dict[str, str]], path: Path, snapshot: str, *, detail: bool) -> int:
    src = rel(path)
    c = 0
    for row in read_csv(path):
        n = bgg_id(row.get("id") or row.get("ID"))
        if n is None:
            continue
        if detail:
            out.append(stat(n, snapshot, "bgg-reviews-jvanelteren", src,
                average_rating=as_float(row.get("average")),
                bayes_average=as_float(row.get("bayesaverage"), zero_null=True),
                users_rated=as_int(row.get("usersrated"), zero_null=True),
                rank_position=rank(row.get("Board Game Rank")),
                weight_average=as_float(row.get("averageweight"), zero_null=True),
                weight_votes=as_int(row.get("numweights"), zero_null=True),
                stddev_rating=as_float(row.get("stddev")),
                median_rating=as_float(row.get("median")),
                owned=as_int(row.get("owned"), zero_null=True),
                trading=as_int(row.get("trading"), zero_null=True),
                wanting=as_int(row.get("wanting"), zero_null=True),
                wishing=as_int(row.get("wishing"), zero_null=True),
                numcomments=as_int(row.get("numcomments"), zero_null=True)))
            c += 1
            for col, domain in JV_RANKS.items():
                r = rank(row.get(col))
                if r:
                    out.append(stat(n, snapshot, "bgg-reviews-jvanelteren", src, domain, rank_position=r))
                    c += 1
        else:
            out.append(stat(n, snapshot, "bgg-reviews-jvanelteren", src,
                average_rating=as_float(row.get("Average")),
                bayes_average=as_float(row.get("Bayes average"), zero_null=True),
                users_rated=as_int(row.get("Users rated"), zero_null=True),
                rank_position=rank(row.get("Rank"))))
            c += 1
    return c


def add_th_stats(out: list[dict[str, str]], path: Path) -> int:
    src = rel(path)
    c = 0
    for row in read_csv(path):
        n = bgg_id(row.get("BGGId"))
        if n is None:
            continue
        votes = as_int(row.get("NumWeightVotes"), zero_null=True)
        weight = as_float(row.get("GameWeight"), zero_null=True)
        if not votes or int(votes) < 5:
            weight = ""
        out.append(stat(n, "2021-12", "bgg-threnjen", src,
            average_rating=as_float(row.get("AvgRating")),
            bayes_average=as_float(row.get("BayesAvgRating"), zero_null=True),
            users_rated=as_int(row.get("NumUserRatings"), zero_null=True),
            rank_position=rank(row.get("Rank:boardgame"), sentinel=21926),
            weight_average=weight, weight_votes=votes,
            stddev_rating=as_float(row.get("StdDev")),
            owned=as_int(row.get("NumOwned"), zero_null=True),
            wanting=as_int(row.get("NumWant"), zero_null=True),
            wishing=as_int(row.get("NumWish"), zero_null=True)))
        c += 1
        for col, domain in TH_RANKS.items():
            r = rank(row.get(col), sentinel=21926)
            if r:
                out.append(stat(n, "2021-12", "bgg-threnjen", src, domain, rank_position=r))
                c += 1
    return c


def add_basic_stats(out: list[dict[str, str]], path: Path, dataset: str, snapshot: str, *, delim: str = ",", enc: str = "utf-8-sig") -> int:
    src = rel(path)
    c = 0
    for row in read_csv(path, enc=enc, delim=delim):
        id_col = "ID" if dataset == "bgg-andrewmvd" else "game_id"
        n = bgg_id(row.get(id_col))
        if n is None:
            continue
        if dataset == "bgg-andrewmvd":
            out.append(stat(n, snapshot, dataset, src,
                average_rating=as_float(row.get("Rating Average"), comma=True),
                users_rated=as_int(row.get("Users Rated"), zero_null=True),
                rank_position=rank(row.get("BGG Rank")),
                weight_average=as_float(row.get("Complexity Average"), zero_null=True, comma=True),
                owned=as_int(row.get("Owned Users"), zero_null=True)))
        elif dataset == "bgg-sujaykapadnis":
            out.append(stat(n, snapshot, dataset, src,
                average_rating=as_float(row.get("average_rating")),
                users_rated=as_int(row.get("users_rated"), zero_null=True)))
        else:
            out.append(stat(n, snapshot, dataset, src,
                average_rating=as_float(row.get("avg_rating")),
                bayes_average=as_float(row.get("geek_rating"), zero_null=True),
                users_rated=as_int(row.get("num_votes"), zero_null=True),
                rank_position=rank(row.get("rank")),
                weight_average=as_float(row.get("weight"), zero_null=True),
                owned=as_int(row.get("owned"), zero_null=True)))
        c += 1
    return c


def add_gabrio_stats(out: list[dict[str, str]], path: Path) -> int:
    src = rel(path)
    cols = ["game.id", "stats.average", "stats.bayesaverage", "stats.usersrated",
            "stats.subtype.boardgame.pos", "stats.averageweight", "stats.numweights",
            "stats.stddev", "stats.median", "stats.owned", "stats.trading",
            "stats.wanting", "stats.wishing", "stats.numcomments"]
    sql = "SELECT " + ", ".join(f"{quote(c)} AS {quote(c)}" for c in cols) + " FROM BoardGames"
    c = 0
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    try:
        for row in con.execute(sql):
            n = bgg_id(row["game.id"])
            if n is None:
                continue
            out.append(stat(n, "2017-06", "bgg-gabrio", src,
                average_rating=as_float(row["stats.average"]),
                bayes_average=as_float(row["stats.bayesaverage"], zero_null=True),
                users_rated=as_int(row["stats.usersrated"], zero_null=True),
                rank_position=rank(row["stats.subtype.boardgame.pos"]),
                weight_average=as_float(row["stats.averageweight"], zero_null=True),
                weight_votes=as_int(row["stats.numweights"], zero_null=True),
                stddev_rating=as_float(row["stats.stddev"]),
                median_rating=as_float(row["stats.median"]),
                owned=as_int(row["stats.owned"], zero_null=True),
                trading=as_int(row["stats.trading"], zero_null=True),
                wanting=as_int(row["stats.wanting"], zero_null=True),
                wishing=as_int(row["stats.wishing"], zero_null=True),
                numcomments=as_int(row["stats.numcomments"], zero_null=True)))
            c += 1
    finally:
        con.close()
    return c


def build_stats() -> tuple[list[dict[str, str]], dict[str, int]]:
    rows: list[dict[str, str]] = []
    counts = {
        "jv_2025_detail": add_jv_stats(rows, DATA / "bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv", "2025-02", detail=True),
        "jv_2020_detail": add_jv_stats(rows, DATA / "bgg-reviews-jvanelteren/raw/games_detailed_info.csv", "2020-08-19", detail=True),
        "jv_2022_simple": add_jv_stats(rows, DATA / "bgg-reviews-jvanelteren/raw/2022-01-08.csv", "2022-01-08", detail=False),
        "jv_2020_simple": add_jv_stats(rows, DATA / "bgg-reviews-jvanelteren/raw/2020-08-19.csv", "2020-08-19", detail=False),
        "threnjen": add_th_stats(rows, DATA / "bgg-threnjen/raw/games.csv"),
        "matt": add_basic_stats(rows, DATA / "bgg-ranked-mattadamhouser/raw/basic_data_2023.csv", "bgg-ranked-mattadamhouser", "2023-08"),
        "mr_2017_04": add_basic_stats(rows, DATA / "bgg-mrpantherson/raw/bgg_db_2017_04.csv", "bgg-mrpantherson", "2017-04", enc="cp1252"),
        "mr_2018_01": add_basic_stats(rows, DATA / "bgg-mrpantherson/raw/bgg_db_2018_01.csv", "bgg-mrpantherson", "2018-01", enc="cp1252"),
        "mr_2018_06": add_basic_stats(rows, DATA / "bgg-mrpantherson/raw/bgg_db_1806.csv", "bgg-mrpantherson", "2018-06"),
        "andrewmvd": add_basic_stats(rows, DATA / "bgg-andrewmvd/raw/bgg_dataset.csv", "bgg-andrewmvd", "2021-02", delim=";"),
        "sujay": add_basic_stats(rows, DATA / "bgg-sujaykapadnis/raw/board_games.csv", "bgg-sujaykapadnis", "2017-derived"),
        "gabrio": add_gabrio_stats(rows, DATA / "bgg-gabrio/raw/database.sqlite"),
    }
    return rows, counts


def tax_row(n: int, typ: str, name: str, snap: str, dataset: str, src: str, fmt: str) -> dict[str, str]:
    return {
        "game_id": f"bgg:{n}", "bgg_id": str(n), "taxonomy_type": typ,
        "taxonomy_name_raw": name, "taxonomy_name_canonical": name if snap == "2025-02" else "",
        "taxonomy_snapshot": snap, "mapping_confidence": "exact" if snap == "2025-02" else "raw_unmapped",
        "source_dataset": dataset, "source_file": src, "source_format": fmt,
    }


def add_tax_values(out: list[dict[str, str]], n: int, typ: str, vals: list[str], snap: str, dataset: str, src: str, fmt: str) -> int:
    seen: set[str] = set()
    for v in vals:
        if v and v not in seen:
            seen.add(v)
            out.append(tax_row(n, typ, v, snap, dataset, src, fmt))
    return len(seen)


def add_jv_tax(out: list[dict[str, str]], path: Path, snap: str) -> int:
    src = rel(path)
    c = 0
    for row in read_csv(path):
        n = bgg_id(row.get("id"))
        if n is None:
            continue
        c += add_tax_values(out, n, "category", listish(row.get("boardgamecategory")), snap, "bgg-reviews-jvanelteren", src, "list_literal")
        c += add_tax_values(out, n, "mechanic", listish(row.get("boardgamemechanic")), snap, "bgg-reviews-jvanelteren", src, "list_literal")
        c += add_tax_values(out, n, "family", listish(row.get("boardgamefamily")), snap, "bgg-reviews-jvanelteren", src, "list_literal")
    return c


def add_wide_tax(out: list[dict[str, str]], path: Path, dataset: str, snap: str, id_col: str, typ: str) -> int:
    src = rel(path)
    c = 0
    for row in read_csv(path):
        n = bgg_id(row.get(id_col))
        if n is None:
            continue
        for col, val in row.items():
            if col not in {id_col, "", "col_0"} and txt(val) in {"1", "1.0", "True", "true"}:
                out.append(tax_row(n, typ, col, snap, dataset, src, "wide_binary"))
                c += 1
    return c


def add_th_domain_tax(out: list[dict[str, str]], path: Path) -> int:
    src = rel(path)
    c = 0
    for row in read_csv(path):
        n = bgg_id(row.get("BGGId"))
        if n is None:
            continue
        for col, name in TH_DOMAINS.items():
            if txt(row.get(col)) in {"1", "1.0"}:
                out.append(tax_row(n, "domain", name, "2021-12", "bgg-threnjen", src, "wide_binary"))
                c += 1
        fam = txt(row.get("Family"))
        if fam:
            out.append(tax_row(n, "family", fam, "2021-12", "bgg-threnjen", src, "string"))
            c += 1
    return c


def add_simple_tax(out: list[dict[str, str]], path: Path, dataset: str, snap: str, id_col: str, cols: dict[str, str], *, delim: str = ",") -> int:
    src = rel(path)
    c = 0
    for row in read_csv(path, delim=delim):
        n = bgg_id(row.get(id_col))
        if n is None:
            continue
        for col, typ in cols.items():
            c += add_tax_values(out, n, typ, listish(row.get(col)), snap, dataset, src, "delimited_string")
    return c


def add_gabrio_tax(out: list[dict[str, str]], path: Path) -> int:
    src = rel(path)
    cols = ["game.id", "attributes.boardgamecategory", "attributes.boardgamemechanic", "attributes.boardgamefamily"]
    sql = "SELECT " + ", ".join(f"{quote(c)} AS {quote(c)}" for c in cols) + " FROM BoardGames"
    c = 0
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    try:
        for row in con.execute(sql):
            n = bgg_id(row["game.id"])
            if n is None:
                continue
            c += add_tax_values(out, n, "category", listish(row["attributes.boardgamecategory"]), "2017-06", "bgg-gabrio", src, "delimited_string")
            c += add_tax_values(out, n, "mechanic", listish(row["attributes.boardgamemechanic"]), "2017-06", "bgg-gabrio", src, "delimited_string")
            c += add_tax_values(out, n, "family", listish(row["attributes.boardgamefamily"]), "2017-06", "bgg-gabrio", src, "delimited_string")
    finally:
        con.close()
    return c


def build_taxonomy() -> tuple[list[dict[str, str]], dict[str, int]]:
    rows: list[dict[str, str]] = []
    counts = {
        "jv_2025": add_jv_tax(rows, DATA / "bgg-reviews-jvanelteren/raw/games_detailed_info2025.csv", "2025-02"),
        "jv_2020": add_jv_tax(rows, DATA / "bgg-reviews-jvanelteren/raw/games_detailed_info.csv", "2020-08-19"),
        "threnjen_mechanics": add_wide_tax(rows, DATA / "bgg-threnjen/raw/mechanics.csv", "bgg-threnjen", "2021-12", "BGGId", "mechanic"),
        "threnjen_themes": add_wide_tax(rows, DATA / "bgg-threnjen/raw/themes.csv", "bgg-threnjen", "2021-12", "BGGId", "theme"),
        "threnjen_subcategories": add_wide_tax(rows, DATA / "bgg-threnjen/raw/subcategories.csv", "bgg-threnjen", "2021-12", "BGGId", "subcategory"),
        "threnjen_domains": add_th_domain_tax(rows, DATA / "bgg-threnjen/raw/games.csv"),
        "matt_mechanisms": add_wide_tax(rows, DATA / "bgg-ranked-mattadamhouser/raw/mechanisms_2023.csv", "bgg-ranked-mattadamhouser", "2023-08", "game_id", "mechanic"),
        "matt_themes": add_wide_tax(rows, DATA / "bgg-ranked-mattadamhouser/raw/themes_2023.csv", "bgg-ranked-mattadamhouser", "2023-08", "game_id", "theme"),
        "matt_subdomains": add_wide_tax(rows, DATA / "bgg-ranked-mattadamhouser/raw/subdomains_2023.csv", "bgg-ranked-mattadamhouser", "2023-08", "game_id", "domain"),
        "andrewmvd": add_simple_tax(rows, DATA / "bgg-andrewmvd/raw/bgg_dataset.csv", "bgg-andrewmvd", "2021-02", "ID", {"Mechanics": "mechanic", "Domains": "domain"}, delim=";"),
        "sujay": add_simple_tax(rows, DATA / "bgg-sujaykapadnis/raw/board_games.csv", "bgg-sujaykapadnis", "2017-derived", "game_id", {"category": "category", "mechanic": "mechanic", "family": "family"}),
        "gabrio": add_gabrio_tax(rows, DATA / "bgg-gabrio/raw/database.sqlite"),
    }
    return rows, counts


def write_table(path: Path, rows: Iterable[dict[str, Any]], fields: list[str]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
            count += 1
    return count


def by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    c = Counter(txt(r.get(key)) for r in rows)
    c.pop("", None)
    return dict(sorted(c.items()))


def report(summary: dict[str, Any]) -> str:
    lines = [
        "# Core Tables Report",
        "",
        f"Generated at: `{summary['generated_at']}`",
        "",
        "## Outputs",
        "",
        f"- `intermediate/games.csv`: {summary['games']['rows']} rows.",
        f"- `intermediate/game_stats.csv`: {summary['game_stats']['rows']} rows.",
        f"- `intermediate/game_taxonomy.csv`: {summary['game_taxonomy']['rows']} rows.",
        "- `raw_index/core_table_summary.json`: machine-readable summary.",
        "",
        "## Games",
        "",
        f"- Input ID universe from `id_map.csv`: {summary['games']['known_ids']} BGG IDs.",
        f"- Games missing `primary_name`: {summary['games']['missing_primary_name']}.",
        f"- Games with description: {summary['games']['with_description']}.",
        "",
        "### Game source scans",
        "",
        "| Source | Rows used |",
        "|---|---:|",
    ]
    for k, v in summary["games"]["source_counts"].items():
        lines.append(f"| `{k}` | {v} |")
    lines += ["", "## Game Stats", "", "### Rows by source", "", "| Source | Rows |", "|---|---:|"]
    for k, v in summary["game_stats"]["by_source"].items():
        lines.append(f"| `{k}` | {v} |")
    lines += ["", "### Rows by rank domain", "", "| Domain | Rows |", "|---|---:|"]
    for k, v in summary["game_stats"]["by_rank_domain"].items():
        lines.append(f"| `{k}` | {v} |")
    lines += ["", "## Game Taxonomy", "", "### Rows by taxonomy type", "", "| Type | Rows |", "|---|---:|"]
    for k, v in summary["game_taxonomy"]["by_type"].items():
        lines.append(f"| `{k}` | {v} |")
    lines += ["", "### Rows by source", "", "| Source | Rows |", "|---|---:|"]
    for k, v in summary["game_taxonomy"]["by_source"].items():
        lines.append(f"| `{k}` | {v} |")
    lines += [
        "",
        "## Notes",
        "",
        "- `games.csv` uses field-level source priority and stores `field_sources` as JSON.",
        "- `game_stats.csv` is a long snapshot table; domain ranks are separate rows.",
        "- `game_taxonomy.csv` keeps raw labels. Only 2025 labels are marked `exact`; older snapshots are marked `raw_unmapped` until alias mapping is built.",
        "- Row-level ratings and reviews are intentionally not transformed in this phase.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    generated_at = datetime.now().isoformat(timespec="seconds")
    id_sources = known_id_sources()
    games, game_counts = build_games(id_sources)
    stats, stat_counts = build_stats()
    tax, tax_counts = build_taxonomy()
    game_rows = write_table(INTERMEDIATE / "games.csv", games, GAME_FIELDS)
    stat_rows = write_table(INTERMEDIATE / "game_stats.csv", stats, STAT_FIELDS)
    tax_rows = write_table(INTERMEDIATE / "game_taxonomy.csv", tax, TAX_FIELDS)
    summary = {
        "generated_at": generated_at,
        "games": {
            "rows": game_rows,
            "known_ids": len(id_sources),
            "missing_primary_name": sum(1 for r in games if not r["primary_name"]),
            "with_description": sum(1 for r in games if r["description"]),
            "source_counts": game_counts,
            "by_game_type": by(games, "game_type"),
        },
        "game_stats": {
            "rows": stat_rows,
            "source_counts_from_build": stat_counts,
            "by_source": by(stats, "source_dataset"),
            "by_rank_domain": by(stats, "rank_domain"),
        },
        "game_taxonomy": {
            "rows": tax_rows,
            "source_counts_from_build": tax_counts,
            "by_source": by(tax, "source_dataset"),
            "by_type": by(tax, "taxonomy_type"),
            "by_mapping_confidence": by(tax, "mapping_confidence"),
        },
    }
    (RAW_INDEX / "core_table_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DOCS / "core_tables_report.md").write_text(report(summary), encoding="utf-8")
    print(f"Wrote games={game_rows}, game_stats={stat_rows}, game_taxonomy={tax_rows}")


if __name__ == "__main__":
    main()
