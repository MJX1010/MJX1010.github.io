"""Drop dataset-lineage cruft from titles and bodies.

What it removes:
- frontmatter `title:` containing `urls` / `urls2` lineage prefix
- body lines that reference urls2 or onetab_urls as 来源/原始文件 (only those —
  internal cross-refs like `[[知识清单]]` are kept)
- collapses 3+ blank lines back to a single blank line after deletion
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"

# Lines that mention the raw datasets — these are pure lineage notes, drop them.
LINEAGE_LINE = re.compile(
    r"^[>\-\s]*(?:来源|原始文件)\s*[：:].*?(?:urls2|onetab_urls)[^\n]*\n",
    re.MULTILINE,
)

# Title overrides for the two homepage-ish files
TITLE_OVERRIDES: dict[str, str] = {
    "index.md": "MJX1010 知识库",
    "99-原始数据/urls2.md": "原始数据备份",
}


def normalise(path_rel: Path) -> str:
    return path_rel.as_posix()


def process(path: Path) -> tuple[bool, int]:
    text = path.read_text(encoding="utf-8")
    rel = normalise(path.relative_to(ROOT))
    title_changed = False
    new_title = TITLE_OVERRIDES.get(rel)

    if new_title:
        new_text, n = re.subn(
            r"^title:\s*.+$",
            f"title: {new_title}",
            text,
            count=1,
            flags=re.MULTILINE,
        )
        if n:
            text = new_text
            title_changed = True

    text, removed = LINEAGE_LINE.subn("", text)

    if title_changed or removed:
        # collapse runs of blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)
        path.write_text(text, encoding="utf-8")
    return title_changed, removed


def main() -> int:
    if not ROOT.exists():
        print(f"content/ not found at {ROOT}", file=sys.stderr)
        return 1
    title_count = 0
    line_count = 0
    for md in sorted(ROOT.rglob("*.md")):
        title_changed, removed = process(md)
        if title_changed or removed:
            rel = md.relative_to(ROOT)
            tags = []
            if title_changed:
                tags.append("title")
            if removed:
                tags.append(f"-{removed}")
            print(f"  [{', '.join(tags):<10}] {rel}")
            if title_changed:
                title_count += 1
            line_count += removed
    print(f"\nDone. Title overrides: {title_count}; lineage lines removed: {line_count}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
