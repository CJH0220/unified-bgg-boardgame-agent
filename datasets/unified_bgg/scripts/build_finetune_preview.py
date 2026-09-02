"""Build deterministic Phase 7 finetune preview samples for unified_bgg.

Outputs:
- samples/finetune/game_qa.preview.jsonl
- samples/finetune/mechanic_explanation.preview.jsonl
- samples/finetune/review_summary.preview.jsonl
- samples/finetune/recommendation_reasoning.preview.jsonl
- samples/finetune/extraction.preview.jsonl
- samples/finetune/*.candidate.jsonl when --kind candidate is used
- raw_index/finetune_sample_summary.json
- raw_index/finetune_candidate_summary.json when --kind candidate is used
- docs/finetune_preview_report.md
- docs/finetune_candidate_report.md when --kind candidate is used
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1]
SAMPLES_RAG = ROOT / "samples" / "rag"
SAMPLES_FINETUNE = ROOT / "samples" / "finetune"
RAW_INDEX = ROOT / "raw_index"
DOCS = ROOT / "docs"

GAME_OVERVIEW = SAMPLES_RAG / "game_overview.jsonl"
MECHANIC_PROFILE = SAMPLES_RAG / "mechanic_profile.jsonl"
REVIEW_DIGEST = SAMPLES_RAG / "review_digest.jsonl"

SCHEMA_VERSION = "finetune-preview-v0.1"
TRANSFORM_VERSION = "phase7-finetune-preview-v0.1"
TASK_TYPES = [
    "game_qa",
    "mechanic_explanation",
    "review_summary",
    "recommendation_reasoning",
    "extraction",
]

THEME_KEYWORDS = [
    ("易教和入门友好", ("easy to teach", "gateway", "new players", "non-gamers", "simple", "accessible")),
    ("重开性和变化", ("replay", "replayable", "variety", "variable", "different every")),
    ("玩家互动", ("interaction", "interactive", "trading", "negotiation", "talk", "group")),
    ("策略深度", ("strategy", "strategic", "depth", "decision", "tactical")),
    ("主题代入感", ("theme", "thematic", "story", "setting", "immersive")),
    ("美术和组件", ("art", "component", "components", "production", "beautiful", "quality")),
    ("随机性和运气", ("luck", "random", "dice", "draw", "swingy")),
    ("时长和节奏", ("long", "length", "slow", "downtime", "drag")),
    ("平衡性", ("balance", "balanced", "unbalanced", "runaway", "catch up")),
    ("体验落差", ("boring", "overrated", "disappointed", "tedious", "repetitive")),
    ("乐趣和桌面氛围", ("fun", "love", "enjoy", "favorite", "great game")),
]

BUCKET_THEME_LABELS = {
    "positive": {
        "乐趣和桌面氛围": "乐趣和桌面氛围好",
        "策略深度": "策略决策有吸引力",
        "随机性和运气": "随机性带来变化",
        "时长和节奏": "节奏或流程受到认可",
        "平衡性": "平衡性受到认可",
        "美术和组件": "美术或组件受到认可",
    },
    "mixed": {
        "乐趣和桌面氛围": "乐趣体验存在分歧",
        "策略深度": "策略深度评价不一",
        "随机性和运气": "随机性带来争议",
        "时长和节奏": "时长或节奏存在分歧",
        "平衡性": "平衡性存在争议",
        "美术和组件": "美术或组件评价不一",
    },
    "critical": {
        "乐趣和桌面氛围": "乐趣不足或体验落差",
        "策略深度": "策略感不足或决策空间受质疑",
        "随机性和运气": "随机性或运气占比过高",
        "时长和节奏": "时长过长或节奏拖沓",
        "平衡性": "平衡性或追赶机制受质疑",
        "美术和组件": "美术或组件存在批评",
        "玩家互动": "互动方式存在负面体验",
        "重开性和变化": "重开性不足或重复感",
        "易教和入门友好": "入门体验仍有门槛",
        "主题代入感": "主题代入感不足",
        "体验落差": "体验落差或被认为高估",
    },
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def task_files(kind: str) -> dict[str, Path]:
    return {task: SAMPLES_FINETUNE / f"{task}.{kind}.jsonl" for task in TASK_TYPES}


def summary_path(kind: str) -> Path:
    return RAW_INDEX / ("finetune_sample_summary.json" if kind == "preview" else "finetune_candidate_summary.json")


def report_path(kind: str) -> Path:
    return DOCS / ("finetune_preview_report.md" if kind == "preview" else "finetune_candidate_report.md")


def fmt_num(value: Any) -> str:
    if value is None:
        return "未知"
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def fmt_players(doc: dict[str, Any]) -> str:
    players = doc.get("players") or {}
    lo, hi = players.get("min_players"), players.get("max_players")
    if lo and hi:
        return f"{lo}-{hi} 人" if lo != hi else f"{lo} 人"
    return "未知"


def fmt_playtime(doc: dict[str, Any]) -> str:
    playtime = doc.get("playtime") or {}
    lo, hi = playtime.get("min_playtime"), playtime.get("max_playtime")
    if lo and hi:
        return f"{lo}-{hi} 分钟" if lo != hi else f"{lo} 分钟"
    return "未知"


def labels(doc: dict[str, Any], typ: str, limit: int = 8) -> list[str]:
    values = ((doc.get("taxonomy") or {}).get(typ) or [])[:limit]
    return [str(v) for v in values if v]


def join(values: list[str], empty: str = "暂无") -> str:
    return "、".join(values) if values else empty


def slug(value: str) -> str:
    out = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return out or "item"


def sample_base(
    task_type: str,
    suffix: str,
    input_text: str,
    output_text: str,
    source_doc_ids: list[str],
    source_game_ids: list[str],
    snapshot_date: str | None,
    source_files: list[str],
    generated_at: str,
    quality_flags: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "sample_id": f"{task_type}:{suffix}:{SCHEMA_VERSION}",
        "schema_version": SCHEMA_VERSION,
        "task_type": task_type,
        "language": "zh",
        "input": input_text,
        "output": output_text,
        "source_doc_ids": source_doc_ids,
        "source_game_ids": source_game_ids,
        "snapshot_date": snapshot_date,
        "quality_flags": sorted(set((quality_flags or []) + ["template_generated"])),
        "metadata": {
            "generated_at": generated_at,
            "transform_version": TRANSFORM_VERSION,
            "source_files": source_files,
        },
    }


def game_sort_key(doc: dict[str, Any]) -> tuple[Any, ...]:
    stats = doc.get("stats") or {}
    rank = stats.get("rank_position") or 999_999_999
    users = stats.get("users_rated") or 0
    bayes = stats.get("bayes_average") or 0
    return (rank, -users, -bayes)


def selected_game_docs(games: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def usable(doc: dict[str, Any]) -> bool:
        flags = set(doc.get("quality_flags") or [])
        stats = doc.get("stats") or {}
        return (
            doc.get("game_type") == "boardgame"
            and doc.get("title")
            and "missing_reliable_mechanics" not in flags
            and bool(stats.get("average_rating") or stats.get("bayes_average"))
            and bool(stats.get("snapshot_date"))
        )

    return sorted([doc for doc in games if usable(doc)], key=game_sort_key)


def review_sort_key(review: dict[str, Any]) -> tuple[Any, ...]:
    summary = review.get("rating_summary") or {}
    return (-(summary.get("comment_rows") or 0), -(summary.get("rating_rows") or 0), review.get("title") or "")


def detect_themes(snippets: list[dict[str, Any]], limit: int = 4) -> list[str]:
    counts: Counter[str] = Counter()
    for item in snippets:
        text = (item.get("text") or "").casefold()
        for label, keys in THEME_KEYWORDS:
            if any(key in text for key in keys):
                counts[label] += 1
    if not counts and snippets:
        return ["整体体验反馈"]
    return [name for name, _ in counts.most_common(limit)]


def bucket_themes(snippets: list[dict[str, Any]], bucket: str) -> str:
    themes = detect_themes(snippets)
    labels = BUCKET_THEME_LABELS.get(bucket, {})
    return join([labels.get(theme, theme) for theme in themes])


def complexity_label(weight: Any) -> str:
    if not isinstance(weight, (int, float)):
        return "未知复杂度"
    if weight < 2:
        return "轻度到轻中度"
    if weight < 3.25:
        return "中等复杂度"
    if weight < 4:
        return "中重度"
    return "重度"


def build_game_qa(docs: list[dict[str, Any]], size: int, generated_at: str) -> list[dict[str, Any]]:
    rows = []
    for doc in docs[:size]:
        stats = doc.get("stats") or {}
        title = doc.get("title")
        snapshot = stats.get("snapshot_date")
        output = (
            f"《{title}》是 {doc.get('year_published') or '未知年份'} 年的桌游，BGG ID 为 {doc.get('bgg_id')}。"
            f"它支持 {fmt_players(doc)}，常见时长为 {fmt_playtime(doc)}，建议年龄 {fmt_num(doc.get('min_age'))}+。"
            f"在 {snapshot} 快照中，平均分为 {fmt_num(stats.get('average_rating'))}，"
            f"贝叶斯分为 {fmt_num(stats.get('bayes_average'))}，总榜排名为 {fmt_num(stats.get('rank_position'))}，"
            f"复杂度为 {fmt_num(stats.get('weight_average'))}/5。"
            f"核心机制包括：{join(labels(doc, 'mechanic', 10))}。"
            f"主要分类包括：{join(labels(doc, 'category', 6))}。"
        )
        rows.append(
            sample_base(
                "game_qa",
                doc["game_id"],
                f"请介绍桌游《{title}》的基础信息，包括人数、时长、复杂度、评分和核心机制。",
                output,
                [doc["doc_id"]],
                [doc["game_id"]],
                snapshot,
                ["samples/rag/game_overview.jsonl"],
                generated_at,
                doc.get("quality_flags") or [],
            )
        )
    return rows


def build_mechanic_explanation(docs: list[dict[str, Any]], size: int, generated_at: str) -> list[dict[str, Any]]:
    rows = []
    for doc in docs[:size]:
        mechanic = doc.get("mechanic")
        reps = [g.get("title") for g in doc.get("representative_games") or [] if g.get("title")][:8]
        gids = [g.get("game_id") for g in doc.get("representative_games") or [] if g.get("game_id")][:12]
        co = [x["name"] for x in (doc.get("cooccurring_mechanics") or [])[:8]]
        cats = [x["name"] for x in (doc.get("common_categories") or [])[:6]]
        output = (
            f"{mechanic} 是 unified_bgg 中的桌游机制标签，覆盖 {fmt_num(doc.get('game_count'))} 款游戏。"
            f"代表游戏包括：{join(reps)}。"
            f"它常与这些机制一起出现：{join(co)}。"
            f"常见分类包括：{join(cats)}。"
            "这些信息来自机制画像文档，适合用于机制解释、相似游戏召回和推荐理由生成。"
        )
        rows.append(
            sample_base(
                "mechanic_explanation",
                slug(str(mechanic)),
                f"请解释桌游机制 {mechanic}，并说明它常和哪些机制一起出现。",
                output,
                [doc["doc_id"]],
                gids,
                None,
                ["samples/rag/mechanic_profile.jsonl"],
                generated_at,
            )
        )
    return rows


def review_flags(review: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    summary = review.get("rating_summary") or {}
    snippets = review.get("representative_snippets") or {}
    if (summary.get("comment_coverage_pct") or 0) < 5:
        flags.append("low_comment_coverage")
    missing = [name for name in ["positive", "mixed", "critical"] if not snippets.get(name)]
    if missing:
        flags.append("missing_review_bucket")
    return flags


def review_theme_text(review: dict[str, Any]) -> tuple[str, str, str]:
    snippets = review.get("representative_snippets") or {}
    return (
        bucket_themes(snippets.get("positive") or [], "positive"),
        bucket_themes(snippets.get("mixed") or [], "mixed"),
        bucket_themes(snippets.get("critical") or [], "critical"),
    )


def paired_review_docs(
    reviews: list[dict[str, Any]],
    game_by_id: dict[str, dict[str, Any]],
) -> list[tuple[dict[str, Any], dict[str, Any] | None]]:
    pairs = [(r, game_by_id.get(r.get("game_id"))) for r in reviews if r.get("game_id")]
    return sorted(pairs, key=lambda pair: review_sort_key(pair[0]))


def build_review_summary(
    pairs: list[tuple[dict[str, Any], dict[str, Any] | None]],
    size: int,
    generated_at: str,
) -> list[dict[str, Any]]:
    rows = []
    for review, game in pairs[:size]:
        summary = review.get("rating_summary") or {}
        pos, mixed, critical = review_theme_text(review)
        title = review.get("title")
        snapshot = ((game or {}).get("stats") or {}).get("snapshot_date")
        output = (
            f"《{title}》在评论摘要中包含 {fmt_num(summary.get('rating_rows'))} 条评分记录、"
            f"{fmt_num(summary.get('comment_rows'))} 条非空评论，评论覆盖率为 {fmt_num(summary.get('comment_coverage_pct'))}%。"
            f"扫描评分均值为 {fmt_num(summary.get('average_rating'))}。"
            f"正面主题主要是：{pos}。"
            f"混合或争议主题主要是：{mixed}。"
            f"负面主题主要是：{critical}。"
            "该总结是基于 BGG 用户评论摘要的主题归纳，不复制长篇评论原文。"
        )
        source_ids = [review["doc_id"]] + ([game["doc_id"]] if game else [])
        rows.append(
            sample_base(
                "review_summary",
                review["game_id"],
                f"请总结 BGG 玩家对《{title}》的主要好评、争议和批评点。",
                output,
                source_ids,
                [review["game_id"]],
                snapshot,
                ["samples/rag/review_digest.jsonl", "samples/rag/game_overview.jsonl"],
                generated_at,
                review_flags(review),
            )
        )
    return rows


def build_recommendation_reasoning(
    pairs: list[tuple[dict[str, Any], dict[str, Any] | None]],
    size: int,
    generated_at: str,
) -> list[dict[str, Any]]:
    rows = []
    usable = [(r, g) for r, g in pairs if g and (g.get("taxonomy") or {}).get("mechanic")]
    for review, game in usable[:size]:
        assert game is not None
        title = game.get("title")
        stats = game.get("stats") or {}
        mechanics = labels(game, "mechanic", 4)
        pos, mixed, critical = review_theme_text(review)
        weight = stats.get("weight_average")
        recommendation = "可以优先尝试" if (stats.get("average_rating") or 0) >= 7 else "可以谨慎尝试"
        output = (
            f"{recommendation}《{title}》。理由是它的机制包含 {join(mechanics)}，"
            f"与问题中的偏好有较高重合；在 {stats.get('snapshot_date')} 快照中平均分为 "
            f"{fmt_num(stats.get('average_rating'))}，复杂度为 {fmt_num(weight)}/5。"
            f"评论摘要中的正面信号包括：{pos}。"
            f"需要注意的争议包括：{mixed}；潜在风险包括：{critical}。"
            "如果玩家不喜欢这些风险点，应先阅读规则或观看试玩再决定。"
        )
        rows.append(
            sample_base(
                "recommendation_reasoning",
                game["game_id"],
                f"我喜欢{join(mechanics[:2])}和{complexity_label(weight)}桌游，是否适合尝试《{title}》？请给出推荐理由和风险。",
                output,
                [game["doc_id"], review["doc_id"]],
                [game["game_id"]],
                stats.get("snapshot_date"),
                ["samples/rag/game_overview.jsonl", "samples/rag/review_digest.jsonl"],
                generated_at,
                review_flags(review) + (game.get("quality_flags") or []),
            )
        )
    return rows


def build_extraction(docs: list[dict[str, Any]], size: int, generated_at: str) -> list[dict[str, Any]]:
    rows = []
    for doc in docs[:size]:
        stats = doc.get("stats") or {}
        extracted = {
            "title": doc.get("title"),
            "bgg_id": doc.get("bgg_id"),
            "year_published": doc.get("year_published"),
            "players": doc.get("players"),
            "playtime": doc.get("playtime"),
            "min_age": doc.get("min_age"),
            "mechanics": labels(doc, "mechanic", 12),
            "categories": labels(doc, "category", 8),
            "rating_snapshot": {
                "snapshot_date": stats.get("snapshot_date"),
                "average_rating": stats.get("average_rating"),
                "bayes_average": stats.get("bayes_average"),
                "rank_position": stats.get("rank_position"),
                "weight_average": stats.get("weight_average"),
            },
        }
        input_text = "从下面介绍中抽取桌游结构化信息：\n" + (doc.get("text") or "")[:900]
        rows.append(
            sample_base(
                "extraction",
                doc["game_id"],
                input_text,
                json.dumps(extracted, ensure_ascii=False, sort_keys=True),
                [doc["doc_id"]],
                [doc["game_id"]],
                stats.get("snapshot_date"),
                ["samples/rag/game_overview.jsonl"],
                generated_at,
                doc.get("quality_flags") or [],
            )
        )
    return rows


def render_report(summary: dict[str, Any]) -> str:
    title = "Finetune Preview Report" if summary["kind"] == "preview" else "Finetune Candidate Report"
    lines = [
        f"# {title}",
        "",
        f"Generated at: `{summary['generated_at']}`",
        f"Schema version: `{summary['schema_version']}`",
        f"Transform version: `{summary['transform_version']}`",
        "",
        "## Outputs",
        "",
        "| File | Rows | Bytes |",
        "| --- | ---: | ---: |",
    ]
    for item in summary["outputs"]:
        lines.append(f"| `{item['path']}` | {item['rows']} | {item['bytes']} |")
    lines += [
        "",
        "## Task Counts",
        "",
        "| Task type | Rows |",
        "| --- | ---: |",
    ]
    for task, count in sorted(summary["task_counts"].items()):
        lines.append(f"| `{task}` | {count} |")
    lines += [
        "",
        "## Selection Policy",
        "",
        "- Samples use deterministic templates, not model rewriting.",
        "- Game-level samples prioritize base boardgames with ratings, reliable mechanics, and selected snapshot stats.",
        "- Review samples summarize themes from BGG user-generated snippets without copying long comments.",
        "- All samples preserve `source_doc_ids` and `source_game_ids` for traceability.",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build unified_bgg finetune preview samples.")
    parser.add_argument("--kind", choices=["preview", "candidate"], default="preview")
    parser.add_argument("--preview-size", type=int, default=None, help="Backward-compatible alias for --sample-size.")
    parser.add_argument("--sample-size", type=int, default=None, help="Rows per task type. Defaults: preview=50, candidate=1000.")
    args = parser.parse_args()

    global SCHEMA_VERSION, TRANSFORM_VERSION
    if args.kind == "candidate":
        SCHEMA_VERSION = "finetune-candidate-v0.1"
        TRANSFORM_VERSION = "phase7-finetune-candidate-v0.1"
    sample_size = args.sample_size or args.preview_size or (50 if args.kind == "preview" else 1000)

    SAMPLES_FINETUNE.mkdir(parents=True, exist_ok=True)
    RAW_INDEX.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now().replace(microsecond=0).isoformat()
    games = read_jsonl(GAME_OVERVIEW)
    mechanics = read_jsonl(MECHANIC_PROFILE)
    reviews = read_jsonl(REVIEW_DIGEST)
    selected_games = selected_game_docs(games)
    game_by_id = {doc["game_id"]: doc for doc in games}
    review_pairs = paired_review_docs(reviews, game_by_id)

    samples_by_task = {
        "game_qa": build_game_qa(selected_games, sample_size, generated_at),
        "mechanic_explanation": build_mechanic_explanation(mechanics, sample_size, generated_at),
        "review_summary": build_review_summary(review_pairs, sample_size, generated_at),
        "recommendation_reasoning": build_recommendation_reasoning(review_pairs, sample_size, generated_at),
        "extraction": build_extraction(selected_games, sample_size, generated_at),
    }

    outputs = []
    files = task_files(args.kind)
    for task, rows in samples_by_task.items():
        path = files[task]
        count = write_jsonl(path, rows)
        outputs.append({"path": path.relative_to(ROOT).as_posix(), "rows": count, "bytes": path.stat().st_size})

    summary = {
        "generated_at": generated_at,
        "schema_version": SCHEMA_VERSION,
        "transform_version": TRANSFORM_VERSION,
        "kind": args.kind,
        "sample_size": sample_size,
        "preview_size": sample_size,
        "inputs": {
            "game_overview_docs": len(games),
            "mechanic_profile_docs": len(mechanics),
            "review_digest_docs": len(reviews),
            "selected_game_docs": len(selected_games),
            "review_game_pairs": len(review_pairs),
        },
        "task_counts": {task: len(rows) for task, rows in samples_by_task.items()},
        "outputs": outputs,
    }
    summary_path(args.kind).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path(args.kind).write_text(render_report(summary), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
