import subprocess
from pathlib import Path

class GitCommandError(RuntimeError):
    pass

def _run_git(repo_path: Path, args: list[str]) -> str:
    # Execute git in the target repo and return stdout.
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), *args],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        raise GitCommandError(f"git {' '.join(args)} failed: {stderr}") from exc
    return (result.stdout or "").strip()

def get_git_status(repo_path: Path) -> str:
    # Short status is enough to guide a commit message.
    return _run_git(repo_path, ["status", "--short"])

def get_git_diff(repo_path: Path) -> str:
    # Compare the working tree with the current origin branch.
    branch = _run_git(repo_path, ['branch', '--show-current'])
    return _run_git(repo_path, ["diff", f'origin/{branch}'])

def add_all(repo_path: Path) -> None:
    # Stage all changes for the commit.
    _run_git(repo_path, ["add", "-A"])

def commit(repo_path: Path, subject: str, body: str | None = None) -> None:
    # Create the commit with a subject and optional body.
    args = ["commit", "-m", subject]
    if body:
        args.extend(["-m", body])
    _run_git(repo_path, args)

def push(repo_path: Path) -> None:
    # Push to the current upstream branch.
    _run_git(repo_path, ["push"])
