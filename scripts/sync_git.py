#!/usr/bin/env python3
"""Stage a scoped set of git changes, commit, and optionally push."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EXCLUDES = ["_temp", "g", "weread-analysis"]


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        text=True,
        capture_output=True,
    )


def get_branch() -> str:
    result = run_git("rev-parse", "--abbrev-ref", "HEAD")
    return result.stdout.strip()


def get_status_lines() -> list[str]:
    result = run_git("status", "--short", "--branch")
    return [line.rstrip() for line in result.stdout.splitlines() if line.strip()]


def get_changed_paths() -> list[str]:
    result = run_git("status", "--porcelain=v1")
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        raw_path = line[3:]
        if " -> " in raw_path:
            raw_path = raw_path.split(" -> ", 1)[1]
        paths.append(raw_path)
    return paths


def normalize_paths(items: list[str]) -> list[str]:
    normalized: list[str] = []
    for item in items:
        cleaned = item.strip().replace("\\", "/").rstrip("/")
        if cleaned:
            normalized.append(cleaned)
    return normalized


def is_under(path: str, scopes: list[str]) -> bool:
    return any(path == scope or path.startswith(f"{scope}/") for scope in scopes)


def has_staged_changes() -> bool:
    result = run_git("diff", "--cached", "--quiet", check=False)
    return result.returncode != 0


def run_privacy_scan(scopes: list[str], excludes: list[str], scan_all: bool) -> dict[str, object]:
    cmd = [sys.executable, str(ROOT / "scripts" / "privacy_preflight.py")]
    if scan_all:
        cmd.extend(["--path", "."])
    else:
        for scope in scopes:
            cmd.extend(["--path", scope])
    for exclude in excludes:
        cmd.extend(["--exclude", exclude])
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout or "{}")
    payload["exit_code"] = result.returncode
    return payload


def commit(message: str) -> str:
    run_git("commit", "-m", message)
    result = run_git("rev-parse", "--short", "HEAD")
    return result.stdout.strip()


def push(branch: str) -> str:
    result = run_git("push", check=False)
    if result.returncode == 0:
        return result.stdout.strip() or result.stderr.strip() or "git push succeeded"
    upstream = run_git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", check=False)
    if upstream.returncode == 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "git push failed")
    result = run_git("push", "-u", "origin", branch, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "git push failed")
    return result.stdout.strip() or result.stderr.strip() or "git push -u origin succeeded"


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage scoped changes, commit, and push.")
    parser.add_argument("--message", required=True, help="Commit message.")
    parser.add_argument("--path", action="append", default=[], help="Explicit path to stage.")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Path prefix to exclude from the dirty-worktree warning.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Stage the whole worktree. Use carefully when unrelated changes exist.",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Create the commit but skip git push.",
    )
    args = parser.parse_args()

    scopes = normalize_paths(args.path)
    excludes = normalize_paths([*DEFAULT_EXCLUDES, *args.exclude])
    branch = get_branch()
    status_before = get_status_lines()
    changed_paths = get_changed_paths()
    unexpected = [
        path
        for path in changed_paths
        if not is_under(path, excludes) and not args.all and (not scopes or not is_under(path, scopes))
    ]

    if unexpected:
        print(
            json.dumps(
                {
                    "ok": False,
                    "reason": "unexpected_changes_outside_scope",
                    "branch": branch,
                    "unexpected_paths": unexpected,
                    "status": status_before,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2

    privacy_report = run_privacy_scan(scopes, excludes, args.all)
    if not privacy_report.get("ok", False):
        print(
            json.dumps(
                {
                    "ok": False,
                    "reason": "privacy_scan_failed",
                    "branch": branch,
                    "privacy_report": privacy_report,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 3

    if args.all:
        run_git("add", "-A")
    elif scopes:
        run_git("add", "--", *scopes)
    else:
        print(
            json.dumps(
                {
                    "ok": False,
                    "reason": "missing_scope",
                    "branch": branch,
                    "message": "Use --path for scoped staging or --all for the whole worktree.",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2

    if not has_staged_changes():
        print(
            json.dumps(
                {
                    "ok": False,
                    "reason": "nothing_staged",
                    "branch": branch,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2

    commit_hash = commit(args.message)
    push_result = "push skipped"
    if not args.no_push:
        push_result = push(branch)

    status_after = get_status_lines()
    recent_log = run_git("log", "--oneline", "--decorate", "-n", "3").stdout.splitlines()
    print(
        json.dumps(
            {
                "ok": True,
                "branch": branch,
                "commit": commit_hash,
                "message": args.message,
                "pushed": not args.no_push,
                "push_result": push_result,
                "privacy_scan": {
                    "scanned_file_count": privacy_report.get("scanned_file_count", 0),
                    "finding_count": privacy_report.get("finding_count", 0),
                },
                "status_before": status_before,
                "status_after": status_after,
                "recent_log": recent_log,
                "scoped_paths": scopes,
                "excluded_paths": excludes,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
