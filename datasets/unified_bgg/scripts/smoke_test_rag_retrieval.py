"""Run a lightweight lexical RAG retrieval smoke test over generated JSONL docs.

This is not a replacement for vector retrieval evaluation. It verifies that the
generated docs are parseable, searchable, and contain enough obvious terms for
basic board-game queries to retrieve expected entities.
"""
from __future__ import annotations

import argparse
import heapq
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
SAMPLES_RAG = ROOT / "samples" / "rag"
RAW_INDEX = ROOT / "raw_index"
DOCS = ROOT / "docs"

OUTPUT = RAW_INDEX / "rag_retrieval_smoke_test.json"
REPORT = DOCS / "rag_retrieval_smoke_test_report.md"

DEFAULT_FILES = [
    SAMPLES_RAG / "game_overview.jsonl",
    SAMPLES_RAG / "mechanic_profile.jsonl",
    SAMPLES_RAG / "review_digest.jsonl",
]

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "game", "games", "in", "is", "it", "of", "on", "or", "the", "to",
    "user", "users", "with",
}

QUERIES = [
    {
        "query": "Brass Birmingham economic network route building",
        "doc_type_filter": "game_overview",
        "expected_doc_substrings": ["bgg:224517"],
    },
    {
        "query": "dice rolling mechanic variable player powers",
        "doc_type_filter": "mechanic_profile",
        "expected_doc_substrings": ["mechanic:dice-rolling"],
    },
    {
        "query": "Carcassonne player review tile laying comments",
        "doc_type_filter": "review_digest",
        "expected_doc_substrings": ["reviews:bgg:822"],
    },
    {
        "query": "Catan trading negotiation user comments",
        "doc_type_filter": "review_digest",
        "expected_doc_substrings": ["bgg:13"],
    },
    {
        "query": "Gloomhaven cooperative campaign fantasy",
        "doc_type_filter": "game_overview",
        "expected_doc_substrings": ["bgg:174430"],
    },
    {
        "query": "deck bag pool building card market mechanic",
        "doc_type_filter": "mechanic_profile",
        "expected_doc_substrings": ["mechanic:deck,-bag,-and-pool-building"],
    },
]


def tokenize(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) > 1 and token not in STOPWORDS
    ]


def doc_terms(row: dict[str, Any]) -> Counter[str]:
    counter: Counter[str] = Counter()
    weighted_fields = [
        (row.get("title") or "", 25),
        (row.get("mechanic") or "", 25),
        (row.get("doc_type") or "", 3),
        (row.get("text") or "", 1),
    ]
    for text, weight in weighted_fields:
        for token in tokenize(str(text)):
            counter[token] += weight
    return counter


def compact_doc(row: dict[str, Any], source_file: Path, score: float) -> dict[str, Any]:
    return {
        "score": round(score, 4),
        "doc_id": row.get("doc_id"),
        "doc_type": row.get("doc_type"),
        "title": row.get("title") or row.get("mechanic"),
        "game_id": row.get("game_id"),
        "source_file": source_file.relative_to(ROOT).as_posix(),
        "text_preview": (row.get("text") or "")[:240],
    }


def maybe_push(top: list[tuple[float, int, dict[str, Any]]], score: float, serial: int, row: dict[str, Any], source_file: Path, limit: int) -> None:
    if score <= 0:
        return
    item = (score, serial, compact_doc(row, source_file, score))
    if len(top) < limit:
        heapq.heappush(top, item)
    elif item[0] > top[0][0]:
        heapq.heapreplace(top, item)


def normalized_tokens(text: str) -> str:
    return " ".join(tokenize(text))


def score_doc(query_terms: Counter[str], terms: Counter[str], row: dict[str, Any], query: str) -> float:
    score = 0.0
    for token, q_count in query_terms.items():
        if token in terms:
            score += (1.0 + min(terms[token], 12) ** 0.5) * q_count
    normalized_query = normalized_tokens(query)
    for field in ["title", "mechanic"]:
        normalized_field = normalized_tokens(str(row.get(field) or ""))
        if normalized_field and normalized_field in normalized_query:
            score += 50.0
    return score


def run(files: list[Path], top_k: int) -> dict[str, Any]:
    query_terms = [Counter(tokenize(item["query"])) for item in QUERIES]
    tops: list[list[tuple[float, int, dict[str, Any]]]] = [[] for _ in QUERIES]
    parsed_docs = 0
    serial = 0

    for path in files:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                parsed_docs += 1
                serial += 1
                terms = doc_terms(row)
                for idx, q_terms in enumerate(query_terms):
                    doc_type_filter = QUERIES[idx].get("doc_type_filter")
                    if doc_type_filter and row.get("doc_type") != doc_type_filter:
                        continue
                    score = score_doc(q_terms, terms, row, QUERIES[idx]["query"])
                    maybe_push(tops[idx], score, serial, row, path, top_k)

    results = []
    passed = 0
    for spec, top in zip(QUERIES, tops):
        ranked = [item[2] for item in sorted(top, key=lambda item: item[0], reverse=True)]
        expected = spec["expected_doc_substrings"]
        hit = any(
            any(fragment in (doc.get("doc_id") or "") for fragment in expected)
            for doc in ranked
        )
        if hit:
            passed += 1
        results.append(
            {
                "query": spec["query"],
                "doc_type_filter": spec.get("doc_type_filter"),
                "expected_doc_substrings": expected,
                "passed": hit,
                "top_results": ranked,
            }
        )

    return {
        "generated_at": datetime.now().replace(microsecond=0).isoformat(),
        "files": [path.relative_to(ROOT).as_posix() for path in files],
        "parsed_docs": parsed_docs,
        "top_k": top_k,
        "passed": passed,
        "total": len(QUERIES),
        "pass_rate": round(passed / len(QUERIES), 4),
        "results": results,
    }


def write_report(result: dict[str, Any]) -> None:
    lines = [
        "# RAG Retrieval Smoke Test Report",
        "",
        f"Generated at: `{result['generated_at']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Parsed docs | {result['parsed_docs']} |",
        f"| Passed queries | {result['passed']} / {result['total']} |",
        f"| Pass rate | {result['pass_rate']} |",
        "",
        "## Query Results",
        "",
    ]
    for item in result["results"]:
        status = "PASS" if item["passed"] else "FAIL"
        lines.extend(
            [
                f"### {status}: `{item['query']}`",
                "",
                "| Rank | Score | Doc type | Title | Doc ID |",
                "| ---: | ---: | --- | --- | --- |",
            ]
        )
        for idx, doc in enumerate(item["top_results"], start=1):
            title = (doc.get("title") or "").replace("|", "\\|")
            lines.append(
                f"| {idx} | {doc['score']} | `{doc.get('doc_type')}` | {title} | `{doc.get('doc_id')}` |"
            )
        lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Smoke-test lexical retrieval over RAG JSONL outputs.")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--files", nargs="*", default=[str(path) for path in DEFAULT_FILES])
    args = parser.parse_args()

    RAW_INDEX.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    files = [Path(path).resolve() if Path(path).is_absolute() else (ROOT / path).resolve() for path in args.files]
    result = run(files, args.top_k)
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_report(result)
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
