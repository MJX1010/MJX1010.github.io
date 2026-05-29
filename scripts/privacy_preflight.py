#!/usr/bin/env python3
"""Scan files for secrets and personal information before they are uploaded."""

from __future__ import annotations

import argparse
import json
import re
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
DEFAULT_EXCLUDES = ["_temp", "g", "weread-analysis", ".git", "node_modules", ".quartz-cache"]
PLACEHOLDER_HINTS = ("example", "sample", "dummy", "placeholder", "fake", "test", "changeme")


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    severity: str


RULES = [
    Rule("email", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE), "high"),
    Rule("cn_mobile", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"), "high"),
    Rule("cn_id_card", re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)"), "high"),
    Rule("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"), "critical"),
    Rule("github_pat", re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "critical"),
    Rule("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), "critical"),
    Rule("anthropic_key", re.compile(r"sk-ant-[A-Za-z0-9\-_]{20,}"), "critical"),
    Rule("openai_project_key", re.compile(r"sk-proj-[A-Za-z0-9\-_]{20,}"), "critical"),
    Rule("generic_sk_key", re.compile(r"\bsk-[A-Za-z0-9\-_]{24,}\b"), "critical"),
    Rule("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "critical"),
    Rule("google_api_key", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b"), "critical"),
    Rule("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "critical"),
]


def normalize(items: list[str]) -> list[str]:
    return [item.strip().replace("\\", "/").rstrip("/") for item in items if item.strip()]


def should_scan(path: Path, excludes: list[str]) -> bool:
    path_str = path.as_posix()
    if any(part in {".git", "node_modules", ".quartz-cache"} for part in path.parts):
        return False
    if any(path_str == prefix or path_str.startswith(f"{prefix}/") for prefix in excludes):
        return False
    return path.suffix.lower() not in TEXT_SUFFIX_BLOCKLIST


def iter_targets(paths: list[str], excludes: list[str]) -> list[Path]:
    if not paths:
        paths = ["."]
    results: list[Path] = []
    for raw in paths:
        candidate = (ROOT / raw).resolve() if not Path(raw).is_absolute() else Path(raw)
        if not candidate.exists():
            continue
        if candidate.is_file():
            rel = candidate.resolve().relative_to(ROOT).as_posix()
            if should_scan(Path(rel), excludes):
                results.append(candidate)
            continue
        for file_path in candidate.rglob("*"):
            if not file_path.is_file():
                continue
            rel = file_path.resolve().relative_to(ROOT).as_posix()
            if should_scan(Path(rel), excludes):
                results.append(file_path)
    seen: set[Path] = set()
    ordered: list[Path] = []
    for item in results:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def is_placeholder(match_text: str) -> bool:
    lowered = match_text.lower()
    if any(hint in lowered for hint in PLACEHOLDER_HINTS):
        return True
    if lowered.endswith("@example.com") or lowered.endswith("@example.org"):
        return True
    return False


def mask(text: str) -> str:
    if len(text) <= 12:
        return text[:3] + "***"
    return f"{text[:6]}***{text[-4:]}"


def scan_file(path: Path) -> list[dict[str, object]]:
    rel = path.resolve().relative_to(ROOT).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []

    findings: list[dict[str, object]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for rule in RULES:
            for match in rule.pattern.finditer(line):
                raw = match.group(0)
                if is_placeholder(raw):
                    continue
                findings.append(
                    {
                        "path": rel,
                        "line": line_number,
                        "rule": rule.name,
                        "severity": rule.severity,
                        "match": mask(raw),
                        "snippet": line.strip()[:240],
                    }
                )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan candidate files for privacy and secret leaks.")
    parser.add_argument("--path", action="append", default=[], help="Path to scan. Defaults to repository root.")
    parser.add_argument("--exclude", action="append", default=[], help="Path prefix to exclude from scanning.")
    args = parser.parse_args()

    excludes = normalize([*DEFAULT_EXCLUDES, *args.exclude])
    targets = iter_targets(normalize(args.path), excludes)
    findings: list[dict[str, object]] = []
    for target in targets:
        findings.extend(scan_file(target))

    payload = {
        "ok": not findings,
        "scanned_file_count": len(targets),
        "finding_count": len(findings),
        "findings": findings[:200],
        "excluded_paths": excludes,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not findings else 3


if __name__ == "__main__":
    raise SystemExit(main())
