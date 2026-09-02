"""Download ready-made unified_bgg indexes from Hugging Face for beginners."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from huggingface_hub import hf_hub_download

HERE = Path(__file__).resolve()
PROJECT = HERE.parents[1]
DEFAULT_REPO = "ChenJinHua/BGG_datasets_Agent"
FILES = {
    "fts": ("indexes/final/rag_index.sqlite", PROJECT / "final" / "rag_index.sqlite"),
    "vector": ("indexes/final/rag_vector_index.sqlite", PROJECT / "final" / "rag_vector_index.sqlite"),
    "rulebook": ("indexes/final/rulebook_index.sqlite", PROJECT / "final" / "rulebook_index.sqlite"),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-id", default=DEFAULT_REPO)
    parser.add_argument("--kind", choices=["query", "all", "fts", "vector", "rulebook"], default="query")
    parser.add_argument("--project", type=Path, default=PROJECT)
    args = parser.parse_args()

    project = args.project.resolve()
    selected = ["fts", "vector"] if args.kind in {"query", "all"} else [args.kind]
    if args.kind == "all":
        selected = list(FILES)
    for kind in selected:
        remote, default_target = FILES[kind]
        target = project / "final" / default_target.name
        target.parent.mkdir(parents=True, exist_ok=True)
        cached = Path(hf_hub_download(repo_id=args.repo_id, repo_type="dataset", filename=remote))
        if cached.resolve() != target.resolve():
            shutil.copyfile(cached, target)
        print(f"ready: {target}")


if __name__ == "__main__":
    main()
