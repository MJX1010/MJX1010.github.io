#!/usr/bin/env python3
"""Audit GitHub repositories for native alerts and possible secret or PII leaks."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

TEXT_SUFFIX_BLOCKLIST = {
    ".7z",
    ".a",
    ".bin",
    ".class",
    ".dll",
    ".dylib",
    ".exe",
    ".gif",
    ".ico",
    ".jar",
    ".jpeg",
    ".jpg",
    ".lib",
    ".lockb",
    ".mp3",
    ".mp4",
    ".otf",
    ".pdf",
    ".png",
    ".so",
    ".ttf",
    ".wav",
    ".webm",
    ".woff",
    ".woff2",
    ".zip",
}

DEFAULT_PATTERNS = [
    ("github_pat", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("github_classic_pat", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("anthropic_key", re.compile(r"sk-ant-[A-Za-z0-9\-_]{20,}")),
    ("openai_project_key", re.compile(r"sk-proj-[A-Za-z0-9\-_]{20,}")),
    ("generic_sk_key", re.compile(r"\bsk-[A-Za-z0-9\-_]{24,}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    (
        "private_key_block",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    ),
]


@dataclass
class PatternRule:
    label: str
    regex: re.Pattern[str]


def run_command(args: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd or ROOT,
        check=check,
        text=True,
        capture_output=True,
    )


def gh_json(args: list[str]) -> object:
    completed = run_command(["gh", *args])
    return json.loads(completed.stdout)


def sanitize_repo_dir(name_with_owner: str) -> str:
    return name_with_owner.replace("/", "__")


def mask_value(value: str) -> str:
    cleaned = value.strip()
    if len(cleaned) <= 12:
        return cleaned[:3] + "***"
    return f"{cleaned[:6]}***{cleaned[-4:]}"


def should_scan_file(path: Path) -> bool:
    if ".git" in path.parts:
        return False
    return path.suffix.lower() not in TEXT_SUFFIX_BLOCKLIST


def build_rules(emails: list[str]) -> list[PatternRule]:
    rules = [PatternRule(label, regex) for label, regex in DEFAULT_PATTERNS]
    for email in sorted({item.strip() for item in emails if item.strip()}):
        rules.append(
            PatternRule(
                f"email:{email}",
                re.compile(re.escape(email), re.IGNORECASE),
            )
        )
    return rules


def list_repos(owner: str, limit: int) -> list[dict[str, object]]:
    repos = gh_json(
        [
            "repo",
            "list",
            owner,
            "--limit",
            str(limit),
            "--json",
            "nameWithOwner,isPrivate,isArchived,diskUsage,defaultBranchRef,url",
        ]
    )
    assert isinstance(repos, list)
    return repos


def api_or_unavailable(path: str) -> tuple[str, list[dict[str, object]]]:
    try:
        payload = gh_json(["api", path])
    except subprocess.CalledProcessError:
        return "unavailable", []
    if isinstance(payload, list):
        return "ok", payload
    return "ok", []


def collect_native_alerts(repo_name: str) -> dict[str, object]:
    secret_status, secret_alerts = api_or_unavailable(f"repos/{repo_name}/secret-scanning/alerts?per_page=100")
    dependabot_status, dependabot_alerts = api_or_unavailable(f"repos/{repo_name}/dependabot/alerts?per_page=100")
    code_status, code_alerts = api_or_unavailable(f"repos/{repo_name}/code-scanning/alerts?per_page=100")
    return {
        "secret_scanning": {
            "status": secret_status,
            "open_count": sum(1 for item in secret_alerts if item.get("state") == "open"),
        },
        "dependabot": {
            "status": dependabot_status,
            "open_count": sum(1 for item in dependabot_alerts if item.get("state") == "open"),
        },
        "code_scanning": {
            "status": code_status,
            "open_count": sum(1 for item in code_alerts if item.get("state") == "open"),
        },
    }


def clone_or_update_repo(repo_name: str, branch: str, clone_root: Path) -> Path:
    target = clone_root / sanitize_repo_dir(repo_name)
    if target.exists():
        run_command(["git", "-C", str(target), "fetch", "--depth", "1", "origin", branch], check=False)
        run_command(["git", "-C", str(target), "checkout", branch], check=False)
        run_command(["git", "-C", str(target), "reset", "--hard", f"origin/{branch}"], check=False)
        run_command(["git", "-C", str(target), "clean", "-fd"], check=False)
        return target
    clone_root.mkdir(parents=True, exist_ok=True)
    run_command(
        ["gh", "repo", "clone", repo_name, str(target), "--", "--depth", "1"],
        cwd=clone_root,
    )
    return target


def scan_file(path: Path, repo_root: Path, rules: list[PatternRule]) -> list[dict[str, object]]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return []
    except OSError:
        return []

    findings: list[dict[str, object]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for rule in rules:
            for match in rule.regex.finditer(line):
                findings.append(
                    {
                        "pattern": rule.label,
                        "path": path.relative_to(repo_root).as_posix(),
                        "line": line_number,
                        "match": mask_value(match.group(0)),
                        "snippet": line.strip()[:240],
                    }
                )
    return findings


def scan_repo_worktree(repo_root: Path, rules: list[PatternRule]) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for path in repo_root.rglob("*"):
        if not path.is_file() or not should_scan_file(path):
            continue
        findings.extend(scan_file(path, repo_root, rules))
    return findings


def summarize(repos: list[dict[str, object]]) -> dict[str, object]:
    native_secret_open = sum(
        int(repo["native_alerts"]["secret_scanning"]["open_count"])  # type: ignore[index]
        for repo in repos
    )
    local_findings = sum(len(repo.get("local_findings", [])) for repo in repos)
    skipped = [repo["nameWithOwner"] for repo in repos if repo.get("local_scan_status") == "skipped_large"]
    errors = [repo["nameWithOwner"] for repo in repos if repo.get("local_scan_status") == "clone_error"]
    pattern_counts = Counter()
    for repo in repos:
        for finding in repo.get("local_findings", []):
            pattern_counts[finding["pattern"]] += 1
    return {
        "repo_count": len(repos),
        "native_secret_open_alerts": native_secret_open,
        "local_finding_count": local_findings,
        "local_pattern_counts": dict(sorted(pattern_counts.items())),
        "skipped_large_repos": skipped,
        "clone_error_repos": errors,
    }


def render_markdown(summary: dict[str, object], repos: list[dict[str, object]], output_json: Path) -> str:
    lines = [
        "# GitHub Account Audit",
        "",
        f"- 报告来源：`{output_json.name}`",
        f"- 仓库总数：`{summary['repo_count']}`",
        f"- Native secret scanning open alerts：`{summary['native_secret_open_alerts']}`",
        f"- 本地内容扫描命中数：`{summary['local_finding_count']}`",
        "",
        "## 重点结论",
        "",
    ]
    pattern_counts: dict[str, int] = summary["local_pattern_counts"]  # type: ignore[assignment]
    if not pattern_counts:
        lines.append("- 本地浅扫描未发现命中的 key / token / private key / 指定邮箱字面量。")
    else:
        for label, count in pattern_counts.items():
            lines.append(f"- `{label}`：`{count}`")
    skipped: list[str] = summary["skipped_large_repos"]  # type: ignore[assignment]
    if skipped:
        lines.append(f"- 因仓库体积过大而跳过本地浅扫描：`{len(skipped)}` 个")
    errors: list[str] = summary["clone_error_repos"]  # type: ignore[assignment]
    if errors:
        lines.append(f"- 克隆失败仓库：`{len(errors)}` 个")
    lines.extend(["", "## 仓库明细", ""])
    for repo in repos:
        native = repo["native_alerts"]
        lines.append(
            "- "
            f"`{repo['nameWithOwner']}` | "
            f"secret:{native['secret_scanning']['status']}/{native['secret_scanning']['open_count']} | "
            f"dependabot:{native['dependabot']['status']}/{native['dependabot']['open_count']} | "
            f"code:{native['code_scanning']['status']}/{native['code_scanning']['open_count']} | "
            f"local:{repo.get('local_scan_status', 'n/a')} | "
            f"findings:{len(repo.get('local_findings', []))}"
        )
        for finding in repo.get("local_findings", [])[:10]:
            lines.append(
                f"  - `{finding['pattern']}` at `{finding['path']}:{finding['line']}` -> `{finding['match']}`"
            )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit GitHub repositories for potential leaks.")
    parser.add_argument("--owner", default="MJX1010")
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--report-dir", type=Path, default=Path("private/github_audit"))
    parser.add_argument("--clone-root", type=Path, default=Path("_temp/github_audit_repos"))
    parser.add_argument(
        "--max-clone-kb",
        type=int,
        default=200000,
        help="Skip local shallow clone for repos larger than this size in KB.",
    )
    parser.add_argument(
        "--email",
        action="append",
        default=[],
        help="Email values to look for in repository contents.",
    )
    args = parser.parse_args()

    report_dir = (ROOT / args.report_dir).resolve() if not args.report_dir.is_absolute() else args.report_dir
    clone_root = (ROOT / args.clone_root).resolve() if not args.clone_root.is_absolute() else args.clone_root
    report_dir.mkdir(parents=True, exist_ok=True)
    clone_root.mkdir(parents=True, exist_ok=True)

    repos = list_repos(args.owner, args.limit)
    rules = build_rules(args.email)
    enriched: list[dict[str, object]] = []

    for repo in repos:
        name_with_owner = str(repo["nameWithOwner"])
        branch_info = repo.get("defaultBranchRef") or {}
        branch = branch_info.get("name") if isinstance(branch_info, dict) else None
        branch = branch or "main"
        native_alerts = collect_native_alerts(name_with_owner)
        record = dict(repo)
        record["native_alerts"] = native_alerts
        record["local_scan_status"] = "not_requested"
        record["local_findings"] = []
        disk_usage = int(repo.get("diskUsage") or 0)

        if disk_usage > args.max_clone_kb:
            record["local_scan_status"] = "skipped_large"
            enriched.append(record)
            continue

        try:
            repo_root = clone_or_update_repo(name_with_owner, branch, clone_root)
        except subprocess.CalledProcessError as exc:
            record["local_scan_status"] = "clone_error"
            record["clone_error"] = exc.stderr.strip() or exc.stdout.strip()
            enriched.append(record)
            continue

        record["local_scan_status"] = "scanned"
        record["local_findings"] = scan_repo_worktree(repo_root, rules)
        enriched.append(record)

    summary = summarize(enriched)
    ts = run_command(
        [sys.executable, "-c", "from datetime import datetime; print(datetime.now().strftime('%Y%m%d-%H%M%S'))"]
    ).stdout.strip()
    output_json = report_dir / f"github-account-audit-{ts}.json"
    output_md = report_dir / f"github-account-audit-{ts}.md"
    payload = {"summary": summary, "repos": enriched}
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md.write_text(render_markdown(summary, enriched, output_json), encoding="utf-8")
    print(json.dumps({"json": str(output_json), "markdown": str(output_md), "summary": summary}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
