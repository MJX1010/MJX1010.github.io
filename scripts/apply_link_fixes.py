#!/usr/bin/env python3
"""Apply scripted link replacements and archive dead links as plain text."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path


MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
SKIP_QUERY_KEYS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "utm_id",
    "spm",
    "from",
    "ref",
    "source",
}


def normalize_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url.strip().rstrip(".,;，。；"))
    query = urllib.parse.urlencode(
        [
            (k, v)
            for k, v in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
            if k.lower() not in SKIP_QUERY_KEYS
        ],
        doseq=True,
    )
    path = parsed.path.rstrip("/") or parsed.path or "/"
    return urllib.parse.urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, query, ""))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def replace_urls(file_path: Path, replacements: list[dict]) -> tuple[int, int]:
    text = file_path.read_text(encoding="utf-8")
    original = text
    changed = 0
    for item in replacements:
        old_url = item["old_url"]
        new_url = item["new_url"]
        hits = text.count(old_url)
        if hits:
            text = text.replace(old_url, new_url)
            changed += hits
    if text != original:
        file_path.write_text(text, encoding="utf-8")
        return 1, changed
    return 0, 0


def collect_dead_urls(audit_json: Path, target_path: str, statuses: set[str]) -> set[str]:
    payload = load_json(audit_json)
    dead_urls: set[str] = set()
    for item in payload["results"]:
        if item["status"] not in statuses:
            continue
        refs = item.get("refs", [])
        if any(ref["path"] == target_path for ref in refs):
            dead_urls.add(item["url"])
            dead_urls.add(item["normalized_url"])
    return dead_urls


def unlink_markdown_links(file_path: Path, dead_urls: set[str]) -> tuple[int, int]:
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    changed_lines = 0
    changed_links = 0
    new_lines: list[str] = []

    for line in lines:
        line_changed = False

        def replacer(match: re.Match[str]) -> str:
            nonlocal changed_links, line_changed
            label = match.group(1)
            url = match.group(2)
            if url not in dead_urls and normalize_url(url) not in dead_urls:
                return match.group(0)
            changed_links += 1
            line_changed = True
            return f"{label}（失效归档）：`{url}`"

        new_line = MARKDOWN_LINK_RE.sub(replacer, line)
        if line_changed:
            changed_lines += 1
        new_lines.append(new_line)

    if changed_lines:
        file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        return changed_lines, changed_links
    return 0, 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply scripted link fixes.")
    parser.add_argument("--plan", type=Path, required=True, help="JSON plan describing replacements and unlink steps")
    args = parser.parse_args()

    plan = load_json(args.plan)
    touched_files = 0
    changed_links = 0

    for item in plan.get("replacements", []):
        file_path = Path(item["path"])
        files_changed, links_changed = replace_urls(file_path, [item])
        touched_files += files_changed
        changed_links += links_changed
        if links_changed:
            print(f"replace\t{file_path.as_posix()}\t{links_changed}")

    for item in plan.get("audit_unlink", []):
        file_path = Path(item["path"])
        audit_json = Path(item["audit_json"])
        statuses = set(item.get("statuses", ["broken", "error"]))
        dead_urls = collect_dead_urls(audit_json, item["path"], statuses)
        if not dead_urls:
            continue
        files_changed, links_changed = unlink_markdown_links(file_path, dead_urls)
        touched_files += files_changed
        changed_links += links_changed
        if links_changed:
            print(f"unlink\t{file_path.as_posix()}\t{links_changed}")

    print(f"files_changed={touched_files}")
    print(f"links_changed={changed_links}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
