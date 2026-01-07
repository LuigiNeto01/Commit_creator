from __future__ import annotations

import argparse
import os
from pathlib import Path

from app.gemini_client import GeminiConfig, GeminiError, generate_commit
from app.git_utils import (
    GitCommandError,
    add_all,
    commit,
    get_git_diff,
    get_git_status,
    push,
)
from app.prompt_builder import CommitRequest, build_prompt


def _parse_args() -> argparse.Namespace:
    # CLI keeps config simple: repo path + optional model.
    parser = argparse.ArgumentParser(description="Generate commit message from git changes.")
    parser.add_argument("repo_path", type=Path, help="Path to the git repository")
    parser.add_argument(
        "--model",
        default="gemini-2.5-flash",
        help="Gemini model name (default: gemini-2.5-flash)",
    )
    return parser.parse_args()


def _load_env_file(repo_path: Path) -> None:
    # Lightweight .env loader to avoid extra dependencies.
    env_path = repo_path / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def main() -> int:
    args = _parse_args()
    repo_path: Path = args.repo_path
    _load_env_file(Path.cwd())

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Missing GEMINI_API_KEY environment variable.")
        return 1

    config = GeminiConfig(api_key=api_key, model=args.model)

    while True:
        # Refresh git context for each attempt.
        try:
            status = get_git_status(repo_path)
            diff = get_git_diff(repo_path)
        except GitCommandError as exc:
            print(f"Git error: {exc}")
            return 1

        prompt = build_prompt(CommitRequest(status=status, diff=diff))

        try:
            result = generate_commit(config, prompt)
        except GeminiError as exc:
            print(f"Gemini error: {exc}")
            return 1

        prefix = result.get("prefix", "").strip()
        message = result.get("message", "").strip()
        if prefix and not message.startswith(prefix):
            message = f"{prefix}: {message}"

        # Ask for confirmation before committing/pushing.
        print("\nCommit sugerido:")
        print(message)
        approve = input("Aprovar e commitar/push? (s/n): ").strip().lower()
        if approve in {"s", "sim", "y", "yes"}:
            try:
                add_all(repo_path)
                commit(repo_path, message)
                push(repo_path)
            except GitCommandError as exc:
                print(f"Git error: {exc}")
                return 1
            print("Commit realizado e enviado para a branch.")
            return 0

        again = input("Gerar outro commit? (s/n): ").strip().lower()
        if again not in {"s", "sim", "y", "yes"}:
            print("Saindo sem commitar.")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
