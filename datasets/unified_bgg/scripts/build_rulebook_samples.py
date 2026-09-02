"""Build a rulebook/mechanics corpus for the top-rated unified_bgg games.

This script:
- selects the top N games from the latest overall stats snapshot
- finds a matching rulebook page on 1jour-1jeu.com
- downloads the rulebook file
- extracts text from PDF/text/HTML sources
- writes a JSONL corpus under samples/rag/
- writes a compact SQLite FTS index for later retrieval

The selected source site is intentionally kept deterministic and public.
For image-only sources, the script records the item as unsupported unless a
future OCR dependency is added.
"""
from __future__ import annotations

import argparse
import csv
import io
import hashlib
import html
import json
import re
import sqlite3
import sys
import unicodedata
import uuid
import urllib.parse
from urllib.error import HTTPError
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from statistics import mean
from typing import Any

from lxml import html as lxml_html
import pymupdf
from PIL import Image
from pypdf import PdfReader

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
INTERMEDIATE = ROOT / "intermediate"
SAMPLES_RAG = ROOT / "samples" / "rag"
RAW_INDEX = ROOT / "raw_index"
DOCS = ROOT / "docs"
FINAL = ROOT / "final"
MANIFEST = ROOT / "manifest.json"
CACHE_DIR = RAW_INDEX / "rulebook_cache"

GAMES = INTERMEDIATE / "games.csv"
STATS = INTERMEDIATE / "game_stats.csv"
TAXONOMY = INTERMEDIATE / "game_taxonomy_canonical.csv"

RULEBOOK_JSONL = SAMPLES_RAG / "rulebook_text.jsonl"
RULEBOOK_PREVIEW = SAMPLES_RAG / "rulebook_text.preview.jsonl"
SUMMARY = RAW_INDEX / "rulebook_corpus_summary.json"
FINDINGS = RAW_INDEX / "rulebook_corpus_findings.jsonl"
REPORT = DOCS / "rulebook_corpus_report.md"
INDEX = FINAL / "rulebook_index.sqlite"

SCHEMA_VERSION = "rulebook-v0.1"
TRANSFORM_VERSION = "phase11-rulebook-corpus-v0.1"
SOURCE_SITE = "1jour-1jeu.com"
DEFAULT_LIMIT = 100
DEFAULT_PREVIEW_SIZE = 20
SEARCH_PAGE_LIMIT = 1

RULEBOOK_SUFFIXES = [
    "rulebook",
    "rule book",
    "living rules reference",
    "rules reference",
    "rules",
    "learn to play",
    "manual",
    "quick start",
    "quickstart",
]

GENERIC_STOPWORDS = {
    "the", "a", "an", "of", "and", "to", "for", "with", "in", "on", "by",
    "board", "game", "games", "rule", "rules", "book", "books", "rulebook",
    "edition", "revised", "complete", "advanced", "living", "reference",
    "deluxe", "anniversary", "big", "box", "ultimate",
}


def normalize_title(value: str) -> str:
    text = unicodedata.normalize("NFKD", value.casefold())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def slugify(value: str) -> str:
    text = normalize_title(value)
    return re.sub(r"\s+", "-", text)[:120] or "rulebook"


def boolish(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y"}


def int_or_none(value: str | None) -> int | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def float_or_none(value: str | None) -> float | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def date_score(value: str | None) -> tuple[int, int, int]:
    value = (value or "").strip()
    nums = [int(part) for part in re.findall(r"\d+", value)]
    if len(nums) == 1:
        return (nums[0], 0, 0)
    if len(nums) == 2:
        return (nums[0], nums[1], 0)
    if len(nums) >= 3:
        return (nums[0], nums[1], nums[2])
    return (0, 0, 0)


def stat_score(row: dict[str, str]) -> tuple[Any, ...]:
    source = row.get("source_dataset", "")
    source_priority = {
        "bgg-reviews-jvanelteren": 70,
        "bgg-ranked-mattadamhouser": 60,
        "bgg-threnjen": 50,
        "bgg-andrewmvd": 40,
        "bgg-mrpantherson": 30,
        "bgg-gabrio": 20,
        "bgg-sujaykapadnis": 10,
    }
    has_rating = 1 if row.get("average_rating") or row.get("bayes_average") else 0
    has_users = 1 if row.get("users_rated") else 0
    return (
        date_score(row.get("snapshot_date")),
        source_priority.get(source, 0),
        has_rating,
        has_users,
    )


def rating_sort_key(game_id: str, stats: dict[str, dict[str, str]]) -> tuple[Any, ...]:
    row = stats.get(game_id, {})
    bayes = float_or_none(row.get("bayes_average")) or 0.0
    avg = float_or_none(row.get("average_rating")) or 0.0
    users = int_or_none(row.get("users_rated")) or 0
    rank = int_or_none(row.get("rank_position")) or 999999999
    return (bayes, avg, users, -rank)


def load_games() -> dict[str, dict[str, str]]:
    games: dict[str, dict[str, str]] = {}
    with GAMES.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            games[row["game_id"]] = row
    return games


def load_best_overall_stats() -> dict[str, dict[str, str]]:
    best: dict[str, dict[str, str]] = {}
    with STATS.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if (row.get("rank_domain") or "overall") != "overall":
                continue
            gid = row["game_id"]
            if gid not in best or stat_score(row) > stat_score(best[gid]):
                best[gid] = row
    return best


def select_top_games(games: dict[str, dict[str, str]], stats: dict[str, dict[str, str]], limit: int) -> list[str]:
    ranked = sorted(stats.keys(), key=lambda gid: rating_sort_key(gid, stats), reverse=True)
    return [gid for gid in ranked if gid in games][:limit]


def load_taxonomy_for_games(target_game_ids: set[str]) -> dict[str, list[str]]:
    mechanics: dict[str, set[str]] = defaultdict(set)
    with TAXONOMY.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            gid = row.get("game_id") or ""
            if gid not in target_game_ids:
                continue
            if (row.get("taxonomy_type") or "") != "mechanic":
                continue
            name = (row.get("canonical_name") or row.get("taxonomy_name_canonical") or "").strip()
            if name:
                mechanics[gid].add(name)
    return {gid: sorted(values) for gid, values in mechanics.items()}


def title_variants(title: str) -> list[str]:
    variants: list[str] = []
    raw = title.strip()
    if raw:
        variants.append(raw)
        if not raw.casefold().endswith("rulebook"):
            variants.append(f"{raw} rulebook")
    if ":" in raw:
        head = raw.split(":", 1)[0].strip()
        variants.append(head)
        if head and not head.casefold().endswith("rulebook"):
            variants.append(f"{head} rulebook")
        tail_removed = raw.rsplit(":", 1)[0].strip()
        if tail_removed and tail_removed not in variants:
            variants.append(tail_removed)
    no_punct = re.sub(r"[()\"'?!,.;:/\-]+", " ", raw)
    no_punct = re.sub(r"\s+", " ", no_punct).strip()
    if no_punct and no_punct not in variants:
        variants.append(no_punct)
        if not no_punct.casefold().endswith("rulebook"):
            variants.append(f"{no_punct} rulebook")
    amp = raw.replace("&", "and")
    if amp not in variants:
        variants.append(amp)
        if not amp.casefold().endswith("rulebook"):
            variants.append(f"{amp} rulebook")
    return [variant for variant in variants if variant]


def content_tokens(title: str) -> list[str]:
    tokens = [
        token
        for token in normalize_title(title).split()
        if token and token not in GENERIC_STOPWORDS
    ]
    return tokens


def fetch_search_html(query: str, page: int = 1) -> tuple[str, str]:
    params = {"q": query}
    if page > 1:
        params["page"] = str(page)
    url = "https://en.1jour-1jeu.com/rules/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        html_text = resp.read().decode("utf-8", "ignore")
    return url, html_text


def extract_candidates(query: str, page: int = 1) -> list[dict[str, Any]]:
    search_url, html_text = fetch_search_html(query, page)
    tree = lxml_html.fromstring(html_text)
    candidates: list[dict[str, Any]] = []
    for heading in tree.xpath('//h3/a[contains(@class, "dark-link")]'):
        title = heading.text_content().strip()
        href = (heading.get("href") or "").strip()
        block = heading.xpath('ancestor::div[contains(@class, "col-center")][1]')
        snippet = ""
        file_type = ""
        if block:
            block_node = block[0]
            snippet = " ".join(block_node.xpath('.//p[contains(@class, "dark-mixed")][1]//text()')).strip()
            badge = block_node.xpath('.//span[contains(@class, "badge")][1]//text()')
            file_type = " ".join(badge).strip().lower()
        candidates.append(
            {
                "search_query": query,
                "search_url": search_url,
                "title": title,
                "url": href,
                "snippet": snippet,
                "file_type": file_type or None,
            }
        )
    return candidates


def strip_rulebook_suffix(title: str) -> str:
    lowered = title.casefold()
    for suffix in RULEBOOK_SUFFIXES:
        marker = suffix.casefold()
        if marker in lowered:
            idx = lowered.rfind(marker)
            if idx >= 0:
                return title[:idx].strip(" -:()[]")
    return title


def candidate_score(game_title: str, candidate_title: str) -> float:
    game_norm = normalize_title(strip_rulebook_suffix(game_title))
    core_title = strip_rulebook_suffix(candidate_title)
    cand_norm = normalize_title(core_title)
    game_tokens = content_tokens(game_title)
    cand_tokens = content_tokens(candidate_title)
    shared_tokens = set(game_tokens) & set(cand_tokens)
    ratio = SequenceMatcher(None, game_norm, cand_norm).ratio()
    score = ratio
    if cand_norm == game_norm:
        score += 2.5
    if cand_norm.startswith(game_norm):
        score += 1.0
    if "rulebook" in candidate_title.casefold() or "rules" in candidate_title.casefold():
        score += 0.2
    if shared_tokens:
        score += len(shared_tokens) * 0.9
        score += (len(shared_tokens) / max(len(set(game_tokens)), 1)) * 1.3
    else:
        score -= 1.5
    if game_tokens and game_tokens[0] not in cand_tokens:
        score -= 0.35
    if game_tokens and game_tokens[-1] not in cand_tokens:
        score -= 0.8
    if len(game_tokens) >= 3 and len(shared_tokens) < 2:
        score -= 0.6
    if len(game_tokens) >= 4 and len(shared_tokens) < 3:
        score -= 0.9
    return score


def find_best_rulebook(game_title: str) -> dict[str, Any] | None:
    seen_urls: set[str] = set()
    all_candidates: list[dict[str, Any]] = []
    for query in title_variants(game_title):
        for page in range(1, SEARCH_PAGE_LIMIT + 1):
            candidates = extract_candidates(query, page)
            if not candidates:
                break
            exact = [
                cand
                for cand in candidates
                if normalize_title(strip_rulebook_suffix(cand.get("title", "")))
                == normalize_title(strip_rulebook_suffix(game_title))
            ]
            if exact:
                chosen = dict(exact[0])
                chosen["score"] = candidate_score(game_title, chosen["title"])
                chosen["candidates"] = candidates[:8]
                chosen["search_page"] = page
                return chosen
            for cand in candidates:
                url = cand.get("url") or ""
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    cand["search_page"] = page
                    all_candidates.append(cand)

    if not all_candidates:
        return None
    all_candidates.sort(
        key=lambda cand: (
            candidate_score(game_title, cand["title"]),
            len(normalize_title(strip_rulebook_suffix(cand["title"]))),
            cand["title"],
        ),
        reverse=True,
    )
    chosen = dict(all_candidates[0])
    chosen["score"] = candidate_score(game_title, chosen["title"])
    chosen["candidates"] = all_candidates[:8]
    if chosen["score"] < 3.0:
        return None
    return chosen


def build_fallback_text(game: dict[str, str], mechanics: list[str], stat: dict[str, str]) -> tuple[str, list[str]]:
    description = html.unescape(game.get("description") or "")
    description = normalize_extracted_text(description)
    if len(description) > 6000:
        description = description[:6000].rsplit(" ", 1)[0].strip() + "..."
    players = []
    min_players = game.get("min_players") or ""
    max_players = game.get("max_players") or ""
    if min_players or max_players:
        players = [f"Players: {min_players or '?'}-{max_players or '?'}"]
    playtime = []
    min_playtime = game.get("min_playtime") or ""
    max_playtime = game.get("max_playtime") or ""
    if min_playtime or max_playtime:
        playtime = [f"Play time: {min_playtime or '?'}-{max_playtime or '?'} minutes"]
    age = game.get("min_age") or ""
    if age:
        playtime.append(f"Age: {age}+")
    stats_bits = []
    if stat.get("average_rating"):
        stats_bits.append(f"average rating {stat.get('average_rating')}")
    if stat.get("bayes_average"):
        stats_bits.append(f"bayes average {stat.get('bayes_average')}")
    if stat.get("users_rated"):
        stats_bits.append(f"{stat.get('users_rated')} users rated")
    sections = [
        f"Game title: {game.get('primary_name') or f'BGG {game.get('bgg_id')}'}",
        "Rulebook source: unavailable from a reliable external match.",
        "Fallback note: this document is synthesized from local unified_bgg metadata because the crawler could not confirm an exact rulebook match.",
    ]
    sections.extend(players)
    sections.extend(playtime)
    if stats_bits:
        sections.append("Stats: " + "; ".join(stats_bits))
    sections.append(build_mechanics_text(mechanics))
    if description:
        sections.extend(["", "Local game overview:", description])
    sections.extend(
        [
            "",
            "Practical summary:",
            "This fallback text is intended to preserve retrieval utility for this game when a trustworthy downloadable rulebook could not be matched.",
        ]
    )
    quality_flags = ["fallback_local_summary"]
    if not description:
        quality_flags.append("missing_local_description")
    return "\n".join(sections).strip(), quality_flags


def download_to_cache(url: str, cache_path: Path) -> tuple[Path, str | None, int, str]:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    if cache_path.exists() and cache_path.stat().st_size > 0:
        data = cache_path.read_bytes()
        return cache_path, None, len(data), hashlib.sha256(data).hexdigest()
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        content_type = resp.headers.get("Content-Type")
        data = resp.read()
    cache_path.write_bytes(data)
    return cache_path, content_type, len(data), hashlib.sha256(data).hexdigest()


def normalize_extracted_text(text: str) -> str:
    text = html.unescape(text)
    text = text.replace("\r", "\n")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"[\u00a0\u200b]+", " ", text)
    text = text.strip()
    return text


def extract_pdf_text(path: Path) -> tuple[str, int, str]:
    try:
        doc = pymupdf.open(str(path))
    except Exception:
        reader = PdfReader(str(path))
        parts: list[str] = []
        for page in reader.pages:
            parts.append(page.extract_text() or "")
        text = normalize_extracted_text("\n\n".join(parts))
        return text, len(reader.pages), "pdf_text_pypdf"

    try:
        fitz_parts: list[str] = []
        for page in doc:
            fitz_parts.append(page.get_text("text") or "")
        fitz_text = normalize_extracted_text("\n\n".join(fitz_parts))
        if len(fitz_text) >= 2000:
            return fitz_text, doc.page_count, "pdf_text_fitz"
        return fitz_text, doc.page_count, "pdf_text_fitz_short"
    finally:
        doc.close()


def _multipart_body(fields: dict[str, str], files: dict[str, tuple[str, bytes, str]]) -> tuple[bytes, str]:
    boundary = "----OpenViking" + uuid.uuid4().hex
    body = bytearray()
    for name, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(value.encode("utf-8"))
        body.extend(b"\r\n")
    for name, (filename, content, content_type) in files.items():
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode("utf-8")
        )
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        body.extend(content)
        body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    return bytes(body), boundary


def render_page_for_ocr(page: pymupdf.Page, scale: float = 1.0, max_side: int = 1600) -> tuple[bytes, str, str]:
    pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)
    image = Image.open(io.BytesIO(pix.tobytes("png")))
    image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=75, optimize=True)
    return buffer.getvalue(), "page.jpg", "image/jpeg"


def ocr_space_image(image_bytes: bytes, filename: str, content_type: str, language: str = "eng") -> str:
    body, boundary = _multipart_body(
        {
            "apikey": "helloworld",
            "language": language,
            "isOverlayRequired": "false",
            "scale": "true",
        },
        {
            "file": (filename, image_bytes, content_type),
        },
    )
    req = urllib.request.Request(
        "https://api.ocr.space/parse/image",
        data=body,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        payload = json.loads(resp.read().decode("utf-8", "ignore"))
    parsed = payload.get("ParsedResults") or []
    if parsed:
        return normalize_extracted_text("\n".join(item.get("ParsedText") or "" for item in parsed))
    return ""


def ocr_pdf_pages(doc: pymupdf.Document) -> str:
    parts: list[str] = []
    for page_index, page in enumerate(doc, start=1):
        page_text = ""
        for scale, max_side in ((1.0, 1600), (0.75, 1300), (0.5, 1000)):
            image_bytes, filename, content_type = render_page_for_ocr(page, scale=scale, max_side=max_side)
            try:
                page_text = ocr_space_image(image_bytes, filename, content_type)
                if page_text:
                    break
            except HTTPError as exc:
                if exc.code == 413:
                    continue
                break
            except Exception:
                break
        if page_text:
            parts.append(page_text)
    return normalize_extracted_text("\n\n".join(parts))


def extract_html_text(path: Path) -> tuple[str, int, str]:
    data = path.read_text(encoding="utf-8", errors="ignore")
    tree = lxml_html.fromstring(data)
    text = normalize_extracted_text(tree.text_content())
    return text, 1, "html_text"


def extract_text_from_source(path: Path, content_type: str | None) -> tuple[str, int, str]:
    lowered = (content_type or "").casefold()
    suffix = path.suffix.casefold()
    if "pdf" in lowered or suffix == ".pdf":
        return extract_pdf_text(path)
    if "html" in lowered or suffix in {".html", ".htm"}:
        return extract_html_text(path)
    if "text" in lowered or suffix in {".txt", ".md"}:
        return normalize_extracted_text(path.read_text(encoding="utf-8", errors="ignore")), 1, "text_plain"
    if "image" in lowered or suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        return "", 0, "image_unsupported"
    try:
        return extract_pdf_text(path)
    except Exception:
        return normalize_extracted_text(path.read_text(encoding="utf-8", errors="ignore")), 1, "fallback_text"


def build_mechanics_text(mechanics: list[str]) -> str:
    if not mechanics:
        return "Canonical mechanics: none captured from the local taxonomy."
    shown = mechanics[:20]
    suffix = "" if len(mechanics) <= 20 else f" and {len(mechanics) - 20} more"
    return "Canonical mechanics: " + ", ".join(shown) + suffix + "."


def build_doc(
    game: dict[str, str],
    stat: dict[str, str],
    mechanics: list[str],
    candidate: dict[str, Any],
    doc_suffix: str,
    source_site: str,
    source_path: Path,
    source_bytes: int,
    source_content_type: str | None,
    source_language: str,
    source_sha256: str,
    extracted_text: str,
    page_count: int,
    extraction_method: str,
    generated_at: str,
) -> dict[str, Any]:
    title = game.get("primary_name") or f"BGG {game.get('bgg_id')}"
    mechanics_text = build_mechanics_text(mechanics)
    leading = [
        f"Game title: {title}",
        f"Rulebook title: {candidate.get('title')}",
        f"Source site: {source_site}",
        f"Source page: {candidate.get('search_url')}",
        f"Source URL: {candidate.get('url')}",
        mechanics_text,
        "",
    ]
    text = "\n".join(leading + [extracted_text]).strip()
    text = text if text else mechanics_text
    quality_flags: list[str] = []
    if not extracted_text.strip():
        quality_flags.append("empty_extracted_text")
    if len(extracted_text) < 400:
        quality_flags.append("very_short_extracted_text")
    if source_content_type and "image" in source_content_type.casefold():
        quality_flags.append("image_source_unsupported")
    if extraction_method.startswith("fallback_"):
        quality_flags.append("fallback_generated_text")

    return {
        "doc_id": f"rulebook:bgg:{game['bgg_id']}:{doc_suffix}",
        "doc_type": "rulebook_text",
        "schema_version": SCHEMA_VERSION,
        "game_id": game["game_id"],
        "bgg_id": int_or_none(game.get("bgg_id")),
        "title": title,
        "game_type": game.get("game_type") or None,
        "year_published": int_or_none(game.get("year_published")),
        "stats": {
            "snapshot_date": stat.get("snapshot_date"),
            "average_rating": float_or_none(stat.get("average_rating")),
            "bayes_average": float_or_none(stat.get("bayes_average")),
            "users_rated": int_or_none(stat.get("users_rated")),
            "rank_position": int_or_none(stat.get("rank_position")),
            "weight_average": float_or_none(stat.get("weight_average")),
            "source_dataset": stat.get("source_dataset"),
            "source_file": stat.get("source_file"),
        },
        "mechanics": mechanics,
        "mechanics_text": mechanics_text,
        "source": {
            "site": source_site,
            "page_url": candidate.get("search_url"),
            "query": candidate.get("search_query"),
            "title": candidate.get("title"),
            "url": candidate.get("url"),
            "language": source_language,
            "content_type": source_content_type,
            "bytes": source_bytes,
            "sha256": source_sha256,
            "page_count": page_count,
            "extraction_method": extraction_method,
            "cache_path": source_path.relative_to(ROOT).as_posix(),
        },
        "quality_flags": quality_flags,
        "source_datasets": [
            "intermediate/games.csv",
            "intermediate/game_stats.csv",
            "intermediate/game_taxonomy_canonical.csv",
        ],
        "metadata": {
            "generated_at": generated_at,
            "transform_version": TRANSFORM_VERSION,
            "source_tables": [
                "intermediate/games.csv",
                "intermediate/game_stats.csv",
                "intermediate/game_taxonomy_canonical.csv",
            ],
        },
        "text": text,
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def setup_db(path: Path) -> sqlite3.Connection:
    if path.exists():
        path.unlink()
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.execute("PRAGMA journal_mode=OFF")
    con.execute("PRAGMA synchronous=OFF")
    con.execute("PRAGMA temp_store=MEMORY")
    con.execute(
        """
        CREATE TABLE docs (
            doc_id TEXT PRIMARY KEY,
            doc_type TEXT NOT NULL,
            title TEXT,
            game_id TEXT,
            bgg_id INTEGER,
            year_published INTEGER,
            game_type TEXT,
            source_site TEXT,
            source_page_url TEXT,
            source_url TEXT,
            source_title TEXT,
            source_language TEXT,
            source_content_type TEXT,
            source_bytes INTEGER,
            source_sha256 TEXT,
            page_count INTEGER,
            extraction_method TEXT,
            mechanics_json TEXT,
            mechanics_text TEXT,
            text_preview TEXT,
            json TEXT NOT NULL,
            text TEXT NOT NULL
        )
        """
    )
    con.execute(
        """
        CREATE VIRTUAL TABLE rulebook_fts USING fts5(
            title,
            mechanics_text,
            text,
            doc_type UNINDEXED,
            doc_id UNINDEXED,
            game_id UNINDEXED,
            source_title UNINDEXED,
            source_site UNINDEXED,
            tokenize='unicode61 remove_diacritics 2'
        )
        """
    )
    con.execute("CREATE INDEX idx_docs_doc_type ON docs(doc_type)")
    con.execute("CREATE INDEX idx_docs_game_id ON docs(game_id)")
    con.execute("CREATE INDEX idx_docs_bgg_id ON docs(bgg_id)")
    con.execute(
        """
        CREATE TABLE index_metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )
    return con


def build_index(rows: list[dict[str, Any]], generated_at: str) -> dict[str, Any]:
    con = setup_db(INDEX)
    try:
        for row in rows:
            payload = json.dumps(row, ensure_ascii=False, sort_keys=True)
            source = row["source"]
            cur = con.execute(
                """
                INSERT INTO docs (
                    doc_id, doc_type, title, game_id, bgg_id, year_published, game_type,
                    source_site, source_page_url, source_url, source_title, source_language,
                    source_content_type, source_bytes, page_count, extraction_method,
                    source_sha256, mechanics_json, mechanics_text, text_preview, json, text
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["doc_id"],
                    row["doc_type"],
                    row["title"],
                    row["game_id"],
                    row["bgg_id"],
                    row["year_published"],
                    row["game_type"],
                    source["site"],
                    source.get("page_url"),
                    source.get("url"),
                    source.get("title"),
                    source.get("language"),
                    source.get("content_type"),
                    source.get("bytes"),
                    source.get("page_count"),
                    source.get("extraction_method"),
                    source.get("sha256"),
                    json.dumps(row["mechanics"], ensure_ascii=False),
                    row["mechanics_text"],
                    row["text"][:800],
                    payload,
                    row["text"],
                ),
            )
            rowid = cur.lastrowid
            con.execute(
                """
                INSERT INTO rulebook_fts(rowid, title, mechanics_text, text, doc_type, doc_id, game_id, source_title, source_site)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    rowid,
                    row["title"],
                    row["mechanics_text"],
                    row["text"],
                    row["doc_type"],
                    row["doc_id"],
                    row["game_id"],
                    source.get("title"),
                    source.get("site"),
                ),
            )

        con.execute("INSERT INTO index_metadata(key, value) VALUES (?, ?)", ("generated_at", generated_at))
        con.execute("INSERT INTO index_metadata(key, value) VALUES (?, ?)", ("schema_version", "sqlite-fts5-rules-v0.1"))
        con.execute(
            "INSERT INTO index_metadata(key, value) VALUES (?, ?)",
            ("source_count", str(len(rows))),
        )
        con.commit()
        con.execute("INSERT INTO rulebook_fts(rulebook_fts) VALUES ('optimize')")
        con.commit()
    finally:
        con.close()

    return {
        "generated_at": generated_at,
        "index_path": INDEX.relative_to(ROOT).as_posix(),
        "index_bytes": INDEX.stat().st_size,
        "schema_version": "sqlite-fts5-rules-v0.1",
        "doc_count": len(rows),
    }


def update_manifest(summary: dict[str, Any]) -> None:
    if not MANIFEST.exists():
        return
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    notes = manifest.setdefault("notes", [])
    note = (
        "Phase 11 ingests top-rated board-game rulebooks from 1jour-1jeu.com, "
        "extracts text from PDFs/text files, and stores rulebook_text docs in the local RAG index."
    )
    if note not in notes:
        notes.append(note)
    generated = manifest.setdefault("generated_outputs", {})
    rag_samples = generated.setdefault("rag_samples", [])
    for item in ["rulebook_text.jsonl", "rulebook_text.preview.jsonl"]:
        if item not in rag_samples:
            rag_samples.append(item)
    raw_index = generated.setdefault("raw_index", [])
    for item in ["rulebook_corpus_summary.json", "rulebook_corpus_findings.jsonl"]:
        if item not in raw_index:
            raw_index.append(item)
    docs = generated.setdefault("docs", [])
    for item in ["rulebook_corpus_report.md"]:
        if item not in docs:
            docs.append(item)
    scripts = generated.setdefault("scripts", [])
    for item in ["build_rulebook_samples.py"]:
        if item not in scripts:
            scripts.append(item)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_report(summary: dict[str, Any]) -> None:
    lines = [
        "# Rulebook Corpus Report",
        "",
        f"Generated at: `{summary['generated_at']}`",
        "",
        "## Selection",
        "",
        f"- Selected games: `{summary['selected_games']}`",
        f"- Successfully ingested: `{summary['ingested_games']}`",
        f"- Missing sources: `{summary['missing_games']}`",
        f"- Source site: `{SOURCE_SITE}`",
        "",
        "## Quality",
        "",
        f"- Total extracted characters: `{summary['total_text_chars']}`",
        f"- Average extracted characters per ingested game: `{summary['avg_text_chars']}`",
        f"- Total downloaded bytes: `{summary['total_source_bytes']}`",
        f"- Total rulebook pages: `{summary['total_pages']}`",
        "",
        "## Extraction Methods",
        "",
        "| Method | Count |",
        "| --- | ---: |",
    ]
    for key, value in sorted(summary["extraction_methods"].items()):
        lines.append(f"| `{key}` | {value} |")

    lines.extend(
        [
            "",
            "## Sample Games",
            "",
            "| Rank | Title | Game Type | Pages | Text chars | Mechanics |",
            "| ---: | --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in summary["samples"]:
        mechanics = ", ".join(row["mechanics"][:8])
        title = (row["title"] or "").replace("|", "\\|")
        lines.append(
            f"| {row['rank']} | {title} | `{row.get('game_type') or ''}` | {row.get('page_count') or 0} | {row.get('text_chars') or 0} | {mechanics} |"
        )

    if summary["missing_titles"]:
        lines.extend(["", "## Missing Sources", ""])
        for title in summary["missing_titles"]:
            lines.append(f"- {title}")

    REPORT.write_text("\n".join(lines), encoding="utf-8")


def append_finding(findings: list[dict[str, Any]], row: dict[str, Any], code: str, detail: str) -> None:
    if len(findings) >= 200:
        return
    findings.append(
        {
            "severity": "warning",
            "code": code,
            "detail": detail,
            "doc_id": row.get("doc_id"),
            "game_id": row.get("game_id"),
            "title": row.get("title"),
            "source_url": row.get("source", {}).get("url"),
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build rulebook corpus from 1jour-1jeu.com.")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--preview-size", type=int, default=DEFAULT_PREVIEW_SIZE)
    args = parser.parse_args()

    SAMPLES_RAG.mkdir(parents=True, exist_ok=True)
    RAW_INDEX.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    FINAL.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now().replace(microsecond=0).isoformat()
    games = load_games()
    stats = load_best_overall_stats()
    selected_game_ids = select_top_games(games, stats, args.limit)
    selected_target_set = set(selected_game_ids)
    mechanics_map = load_taxonomy_for_games(selected_target_set)

    built_rows: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    missing_titles: list[str] = []
    extraction_methods: Counter[str] = Counter()
    total_source_bytes = 0
    total_text_chars = 0
    total_pages = 0

    for rank, game_id in enumerate(selected_game_ids, start=1):
        game = games[game_id]
        stat = stats.get(game_id, {})
        title = game.get("primary_name") or f"BGG {game.get('bgg_id')}"
        candidate = find_best_rulebook(title)
        mechanics = mechanics_map.get(game_id, [])
        if not candidate or not candidate.get("url"):
            fallback_text, fallback_flags = build_fallback_text(game, mechanics, stat)
            missing_titles.append(title)
            append_finding(
                findings,
                {"doc_id": f"rulebook:{game_id}:missing", "game_id": game_id, "title": title},
                "missing_source",
                "No trustworthy external rulebook source could be matched; used a local fallback summary.",
            )
            extraction_methods["fallback_local_summary"] += 1
            total_text_chars += len(fallback_text)
            row = build_doc(
                game=game,
                stat=stat,
                mechanics=mechanics,
                candidate={
                    "title": title,
                    "search_url": None,
                    "url": None,
                    "search_query": title,
                },
                doc_suffix=f"local:{slugify(title)}",
                source_site="unified_bgg-local",
                source_path=ROOT / "raw_index" / "rulebook_fallback" / f"{slugify(title)}.txt",
                source_bytes=0,
                source_content_type="text/plain",
                source_language="en",
                source_sha256="fallback-local-summary",
                extracted_text=fallback_text,
                page_count=0,
                extraction_method="fallback_local_summary",
                generated_at=generated_at,
            )
            row["quality_flags"].extend(fallback_flags)
        else:
            source_url = candidate["url"]
            cache_name = f"{game.get('bgg_id') or game_id}_{slugify(candidate['title'])}{Path(urllib.parse.urlparse(source_url).path).suffix or '.bin'}"
            cache_path = CACHE_DIR / cache_name
            source_path, content_type, source_bytes, source_sha256 = download_to_cache(source_url, cache_path)
            extracted_text, page_count, extraction_method = extract_text_from_source(source_path, content_type)
            if len(extracted_text.strip()) < 400:
                fallback_text, fallback_flags = build_fallback_text(game, mechanics, stat)
                extracted_text = fallback_text
                extraction_method = "fallback_local_summary"
                extraction_methods[extraction_method] += 1
                total_source_bytes += source_bytes
                total_text_chars += len(extracted_text)
                total_pages += page_count
                row = build_doc(
                    game=game,
                    stat=stat,
                    mechanics=mechanics,
                    candidate=candidate,
                    doc_suffix=f"1jour1jeu:{slugify(candidate['title'])}",
                    source_site=SOURCE_SITE,
                    source_path=source_path,
                    source_bytes=source_bytes,
                    source_content_type=content_type,
                    source_language="en",
                    source_sha256=source_sha256,
                    extracted_text=extracted_text,
                    page_count=page_count,
                    extraction_method=extraction_method,
                    generated_at=generated_at,
                )
                row["quality_flags"].extend(fallback_flags)
            else:
                extraction_methods[extraction_method] += 1
                total_source_bytes += source_bytes
                total_text_chars += len(extracted_text)
                total_pages += page_count

                row = build_doc(
                    game=game,
                    stat=stat,
                    mechanics=mechanics,
                    candidate=candidate,
                    doc_suffix=f"1jour1jeu:{slugify(candidate['title'])}",
                    source_site=SOURCE_SITE,
                    source_path=source_path,
                    source_bytes=source_bytes,
                    source_content_type=content_type,
                    source_language="en",
                    source_sha256=source_sha256,
                    extracted_text=extracted_text,
                    page_count=page_count,
                    extraction_method=extraction_method,
                    generated_at=generated_at,
                )
        built_rows.append(row)
        if row["quality_flags"]:
            for flag in row["quality_flags"]:
                append_finding(findings, row, flag, "Rulebook corpus quality flag.")

    preview_rows = built_rows[: args.preview_size]
    write_jsonl(RULEBOOK_JSONL, built_rows)
    write_jsonl(RULEBOOK_PREVIEW, preview_rows)
    with FINDINGS.open("w", encoding="utf-8", newline="\n") as f:
        for finding in findings:
            f.write(json.dumps(finding, ensure_ascii=False, sort_keys=True) + "\n")

    index_summary = build_index(built_rows, generated_at)
    avg_text_chars = round(total_text_chars / len(built_rows), 2) if built_rows else 0
    summary = {
        "generated_at": generated_at,
        "schema_version": SCHEMA_VERSION,
        "transform_version": TRANSFORM_VERSION,
        "selected_games": len(selected_game_ids),
        "ingested_games": len(built_rows),
        "missing_games": len(missing_titles),
        "missing_titles": missing_titles,
        "total_source_bytes": total_source_bytes,
        "total_text_chars": total_text_chars,
        "avg_text_chars": avg_text_chars,
        "total_pages": total_pages,
        "extraction_methods": dict(extraction_methods),
        "source_site": SOURCE_SITE,
        "jsonl": RULEBOOK_JSONL.relative_to(ROOT).as_posix(),
        "preview": RULEBOOK_PREVIEW.relative_to(ROOT).as_posix(),
        "index": index_summary,
        "samples": [
            {
                "rank": idx,
                "title": row["title"],
                "game_type": row.get("game_type"),
                "page_count": row["source"].get("page_count"),
                "text_chars": len(row["text"]),
                "mechanics": row["mechanics"],
            }
            for idx, row in enumerate(built_rows[: min(10, len(built_rows))], start=1)
        ],
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_report(summary)
    update_manifest(summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
