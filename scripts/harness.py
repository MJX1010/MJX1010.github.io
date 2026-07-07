#!/usr/bin/env python3
"""Lightweight CLI entrypoint for repository AI harness workflows."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run_script(script_name: str, extra_args: list[str]) -> int:
    script_path = ROOT / script_name
    cmd = [sys.executable, str(script_path), *extra_args]
    completed = subprocess.run(cmd, check=False)
    return int(completed.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Unified entrypoint for note-governance and link-audit scripts."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser(
        "audit-links", help="Run external link audit against a target Markdown root."
    )
    audit_parser.add_argument("--root", default="content")
    audit_parser.add_argument("--workers", type=int, default=8)
    audit_parser.add_argument("--timeout", type=int, default=10)

    apply_parser = subparsers.add_parser(
        "apply-link-plan", help="Apply a scripted link fix plan."
    )
    apply_parser.add_argument("--plan", required=True)

    lint_parser = subparsers.add_parser(
        "wiki-lint", help="Run lightweight lint checks against the public knowledge base."
    )
    lint_parser.add_argument("--content-dir", default="content")
    lint_parser.add_argument("--manifest", default="content/.manifest.json")
    lint_parser.add_argument("--write-manifest", action="store_true")
    lint_parser.add_argument("--fix-frontmatter", action="store_true")
    lint_parser.add_argument("--strict", action="store_true")

    fetch_parser = subparsers.add_parser(
        "fetch-link-content", help="Fetch and cache source content for one or more links."
    )
    fetch_parser.add_argument("--from-md")
    fetch_parser.add_argument("--url", action="append", default=[])
    fetch_parser.add_argument("--cache-dir", default="private/link_cache")
    fetch_parser.add_argument("--digest")
    fetch_parser.add_argument("--workers", type=int, default=3)
    fetch_parser.add_argument("--timeout", type=int, default=45)
    fetch_parser.add_argument("--refresh", action="store_true")

    index_parser = subparsers.add_parser(
        "build-topic-index", help="Build a topic index from a target content directory."
    )
    index_parser.add_argument("--content-dir", default="content/游戏/引擎/Unity")
    index_parser.add_argument("--output", default="content/游戏/引擎/Unity/Unity-知识索引.md")
    index_parser.add_argument("--max-points", type=int, default=8)
    index_parser.add_argument("--title", default="Unity 知识索引")
    index_parser.add_argument("--topic-tag", default="Unity")
    index_parser.add_argument("--include-glob", default="*.md")
    index_parser.add_argument("--skip-names", default="Unity-知识索引.md")
    index_parser.add_argument("--script-name", default="scripts/build_topic_index.py")
    index_parser.add_argument(
        "--summary",
        default="汇总主题笔记中的核心知识点，便于从一个入口跳转到具体笔记。",
    )

    sync_parser = subparsers.add_parser(
        "sync-git", help="Stage a scoped set of changes, commit, and optionally push."
    )
    sync_parser.add_argument("--message", required=True)
    sync_parser.add_argument("--path", action="append", default=[])
    sync_parser.add_argument("--exclude", action="append", default=[])
    sync_parser.add_argument("--all", action="store_true")
    sync_parser.add_argument("--no-push", action="store_true")

    privacy_parser = subparsers.add_parser(
        "privacy-scan",
        help="Scan candidate files for secrets and personal information before upload.",
    )
    privacy_parser.add_argument("--path", action="append", default=[])
    privacy_parser.add_argument("--exclude", action="append", default=[])

    github_audit_parser = subparsers.add_parser(
        "github-account-audit",
        help="Audit GitHub repositories for native alerts and possible secret leaks.",
    )
    github_audit_parser.add_argument("--owner", default="MJX1010")
    github_audit_parser.add_argument("--limit", type=int, default=200)
    github_audit_parser.add_argument(
        "--report-dir", default="private/github_audit"
    )
    github_audit_parser.add_argument(
        "--clone-root", default="_temp/github_audit_repos"
    )
    github_audit_parser.add_argument(
        "--max-clone-kb",
        type=int,
        default=200000,
        help="Skip local shallow clone for repos larger than this size in KB.",
    )
    github_audit_parser.add_argument(
        "--email",
        action="append",
        default=[],
        help="Email values to look for in repository contents.",
    )

    args = parser.parse_args()

    if args.command == "audit-links":
        return run_script(
            "audit_external_links.py",
            [
                "--root",
                args.root,
                "--workers",
                str(args.workers),
                "--timeout",
                str(args.timeout),
            ],
        )

    if args.command == "apply-link-plan":
        return run_script("apply_link_fixes.py", ["--plan", args.plan])

    if args.command == "wiki-lint":
        extra_args = [
            "--content-dir",
            args.content_dir,
            "--manifest",
            args.manifest,
        ]
        if args.write_manifest:
            extra_args.append("--write-manifest")
        if args.fix_frontmatter:
            extra_args.append("--fix-frontmatter")
        if args.strict:
            extra_args.append("--strict")
        return run_script("wiki_lint.py", extra_args)

    if args.command == "fetch-link-content":
        extra_args: list[str] = [
            "--cache-dir",
            args.cache_dir,
            "--workers",
            str(args.workers),
            "--timeout",
            str(args.timeout),
        ]
        if args.from_md:
            extra_args.extend(["--from-md", args.from_md])
        for url in args.url:
            extra_args.extend(["--url", url])
        if args.digest:
            extra_args.extend(["--digest", args.digest])
        if args.refresh:
            extra_args.append("--refresh")
        return run_script("fetch_link_content.py", extra_args)

    if args.command == "build-topic-index":
        return run_script(
            "build_topic_index.py",
            [
                "--content-dir",
                args.content_dir,
                "--output",
                args.output,
                "--max-points",
                str(args.max_points),
                "--title",
                args.title,
                "--topic-tag",
                args.topic_tag,
                "--include-glob",
                args.include_glob,
                "--skip-names",
                args.skip_names,
                "--script-name",
                args.script_name,
                "--summary",
                args.summary,
            ],
        )

    if args.command == "sync-git":
        extra_args = ["--message", args.message]
        for path in args.path:
            extra_args.extend(["--path", path])
        for exclude in args.exclude:
            extra_args.extend(["--exclude", exclude])
        if args.all:
            extra_args.append("--all")
        if args.no_push:
            extra_args.append("--no-push")
        return run_script("sync_git.py", extra_args)

    if args.command == "privacy-scan":
        extra_args: list[str] = []
        for path in args.path:
            extra_args.extend(["--path", path])
        for exclude in args.exclude:
            extra_args.extend(["--exclude", exclude])
        return run_script("privacy_preflight.py", extra_args)

    if args.command == "github-account-audit":
        extra_args = [
            "--owner",
            args.owner,
            "--limit",
            str(args.limit),
            "--report-dir",
            args.report_dir,
            "--clone-root",
            args.clone_root,
            "--max-clone-kb",
            str(args.max_clone_kb),
        ]
        for email in args.email:
            extra_args.extend(["--email", email])
        return run_script("github_account_audit.py", extra_args)

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
