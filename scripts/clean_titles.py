"""Two-pass cleanup on every content/*.md:

1. Strip the `onetab_urls.14[ -]` prefix from the YAML `title:` field
   (also strips a trailing parenthetical `(onetab_urls.14)`).
2. Remove the first H1 line in the body so Quartz's auto-rendered page title
   is not duplicated by an in-body heading.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"

PREFIX_PATTERNS = [
    re.compile(r"^onetab_urls\.\d+\s*[-—]\s*"),
    re.compile(r"^onetab_urls\.\d+\s+"),
]
SUFFIX_PAREN_PATTERN = re.compile(r"\s*[（(]\s*onetab_urls\.\d+\s*[)）]\s*$")
TITLE_LINE = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)
FRONTMATTER = re.compile(r"^(---\n)(.*?)(\n---\n)", re.DOTALL)
# strip any leading BOM, then optional blank lines, then a single H1 line + trailing blanks
H1_AT_START = re.compile(r"^﻿?\s*#\s+[^\n]+\n+", re.MULTILINE)


def strip_title(raw: str) -> str:
    s = raw
    for pat in PREFIX_PATTERNS:
        s = pat.sub("", s)
    s = SUFFIX_PAREN_PATTERN.sub("", s)
    return s.strip()


def process(path: Path) -> tuple[bool, bool]:
    text = path.read_text(encoding="utf-8")
    title_changed = False
    h1_removed = False

    fm_match = FRONTMATTER.match(text)
    if fm_match:
        fm_open, fm_body, fm_close = fm_match.groups()

        def replace_title(m: re.Match[str]) -> str:
            nonlocal title_changed
            original = m.group(1)
            cleaned = strip_title(original)
            if cleaned != original:
                title_changed = True
            return f"title: {cleaned}"

        new_fm_body = TITLE_LINE.sub(replace_title, fm_body)
        body = text[fm_match.end():]
    else:
        new_fm_body = ""
        fm_open = fm_close = ""
        body = text

    new_body, n = H1_AT_START.subn("", body, count=1)
    if n > 0:
        h1_removed = True

    if not (title_changed or h1_removed):
        return False, False

    if fm_match:
        new_text = fm_open + new_fm_body + fm_close + new_body
    else:
        new_text = new_body
    path.write_text(new_text, encoding="utf-8")
    return title_changed, h1_removed


def main() -> int:
    if not ROOT.exists():
        print(f"content/ not found at {ROOT}", file=sys.stderr)
        return 1
    title_count = 0
    h1_count = 0
    for md in sorted(ROOT.rglob("*.md")):
        title_changed, h1_removed = process(md)
        if title_changed or h1_removed:
            rel = md.relative_to(ROOT)
            tags = []
            if title_changed:
                tags.append("title")
            if h1_removed:
                tags.append("H1")
            print(f"  [{', '.join(tags):<8}] {rel}")
            if title_changed:
                title_count += 1
            if h1_removed:
                h1_count += 1
    print(f"\nDone. Title cleaned in {title_count} file(s); H1 removed in {h1_count} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
