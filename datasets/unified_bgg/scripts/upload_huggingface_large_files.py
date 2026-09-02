"""Upload GitHub-excluded large project files to a Hugging Face dataset repo."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import HfApi

HERE = Path(__file__).resolve()
UNIFIED = HERE.parents[1]
DATASETS = UNIFIED.parent
RESEARCH = DATASETS.parent
DEFAULT_REPO = "ChenJinHua/BGG_datasets_Agent"
MANIFEST = RESEARCH / "huggingface_upload_manifest.json"
DATASET_CARD = RESEARCH / "HUGGINGFACE_DATA_GUIDE.md"


def collect_files() -> list[tuple[Path, str, str]]:
    """Return (local path, remote path, category) in deterministic order."""
    rows: list[tuple[Path, str, str]] = []
    for dataset_dir in sorted(DATASETS.glob("bgg-*/raw")):
        if not dataset_dir.is_dir():
            continue
        dataset = dataset_dir.parent.name
        for path in sorted(dataset_dir.rglob("*")):
            if path.is_file():
                rows.append((path, f"raw/{dataset}/{path.relative_to(dataset_dir).as_posix()}", "raw"))

    intermediate = UNIFIED / "intermediate"
    for name in ("games.csv", "game_taxonomy.csv", "game_taxonomy_canonical.csv"):
        path = intermediate / name
        if path.is_file():
            rows.append((path, f"derived/intermediate/{name}", "derived"))

    samples = UNIFIED / "samples" / "rag"
    for name in ("game_overview.jsonl", "review_digest.jsonl"):
        path = samples / name
        if path.is_file():
            rows.append((path, f"derived/samples/rag/{name}", "derived"))

    for path in sorted((UNIFIED / "final").glob("*.sqlite")):
        rows.append((path, f"indexes/final/{path.name}", "index"))

    cache = UNIFIED / "raw_index" / "rulebook_cache"
    for path in sorted(cache.rglob("*")) if cache.is_dir() else []:
        if path.is_file():
            rows.append((path, f"rulebook_cache/{path.relative_to(cache).as_posix()}", "cache"))
    return rows


def sha256(path: Path, chunk_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(rows: list[tuple[Path, str, str]]) -> dict:
    files = []
    for local, remote, category in rows:
        files.append(
            {
                "local_path": local.relative_to(RESEARCH).as_posix(),
                "remote_path": remote,
                "category": category,
                "size_bytes": local.stat().st_size,
                "sha256": sha256(local),
            }
        )
    return {
        "repo_id": DEFAULT_REPO,
        "repo_type": "dataset",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_root": str(RESEARCH),
        "file_count": len(files),
        "total_bytes": sum(item["size_bytes"] for item in files),
        "files": files,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-id", default=DEFAULT_REPO)
    parser.add_argument("--manifest-only", action="store_true", help="Only write the local manifest.")
    parser.add_argument("--skip-existing", action="store_true", help="Skip remote files already present.")
    args = parser.parse_args()

    rows = collect_files()
    manifest = build_manifest(rows)
    manifest["repo_id"] = args.repo_id
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Manifest: {MANIFEST} ({len(rows)} files, {manifest['total_bytes']} bytes)")
    if args.manifest_only:
        return

    api = HfApi()
    existing = set(api.list_repo_files(args.repo_id, repo_type="dataset")) if args.skip_existing else set()
    for local, remote in ((DATASET_CARD, "README.md"), (MANIFEST, MANIFEST.name)):
        print(f"uploading metadata: {remote}", flush=True)
        api.upload_file(
            path_or_fileobj=str(local),
            path_in_repo=remote,
            repo_id=args.repo_id,
            repo_type="dataset",
            commit_message=f"Update {remote}",
        )
    for local, remote, _category in rows:
        if remote in existing:
            print(f"skip existing: {remote}")
            continue
        print(f"uploading: {remote} ({local.stat().st_size} bytes)", flush=True)
        api.upload_file(
            path_or_fileobj=str(local),
            path_in_repo=remote,
            repo_id=args.repo_id,
            repo_type="dataset",
            commit_message=f"Upload {remote}",
        )
        print(f"uploaded: {remote}", flush=True)


if __name__ == "__main__":
    main()
