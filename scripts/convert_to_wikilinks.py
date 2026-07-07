"""Convert internal `[label](relative_path.md)` to Quartz wikilinks `[[basename|label]]`.

Rules:
- only relative paths starting with ./ or ../ are converted
- external links (http/https/file://) are left untouched
- labels that contain backticks (inline code) are kept as markdown links
- if label == basename, output is `[[basename]]` (no alias)
- frontmatter and fenced code blocks are skipped
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"

LINK_RE = re.compile(
    r"\[(?P<label>[^\]\n]+?)\]\((?P<path>\.{1,2}/(?:[^)\n]+/)*(?P<base>[^/)\n]+)\.md)\)"
)
FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)


def split_code_fences(text: str) -> list[tuple[str, bool]]:
    """Return [(chunk, is_code), ...] alternating non-code and code-fence blocks."""
    chunks: list[tuple[str, bool]] = []
    in_code = False
    buf: list[str] = []
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            chunks.append(("\n".join(buf), in_code))
            buf = [line]
            in_code = not in_code
            continue
        buf.append(line)
    chunks.append(("\n".join(buf), in_code))
    return chunks


def convert_in_text(text: str) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        label = match.group("label").strip()
        base = match.group("base")
        # strip wrapping backticks from label so the alias renders as plain text
        if label.startswith("`") and label.endswith("`") and len(label) > 2:
            label = label[1:-1]
        # treat ".md" suffix on the label as redundant when label looks like the file stem
        if label.endswith(".md"):
            label = label[:-3]
        count += 1
        if label == base or not label:
            return f"[[{base}]]"
        return f"[[{base}|{label}]]"

    return LINK_RE.sub(repl, text), count


def process(text: str) -> tuple[str, int]:
    # Preserve frontmatter as-is
    fm_match = FRONTMATTER_RE.match(text)
    if fm_match:
        fm = fm_match.group(0)
        body = text[fm_match.end() :]
    else:
        fm = ""
        body = text

    # Split into code/non-code chunks; only convert non-code
    chunks = split_code_fences(body)
    out_parts: list[str] = []
    total = 0
    for i, (chunk, is_code) in enumerate(chunks):
        if is_code:
            out_parts.append(chunk)
        else:
            new_chunk, count = convert_in_text(chunk)
            out_parts.append(new_chunk)
            total += count
        # Re-insert the fence line that delimited this chunk except the last
        # (split_code_fences puts fence lines at chunk start except the very first)
    return fm + "\n".join(out_parts), total


def main() -> int:
    if not ROOT.exists():
        print(f"content/ not found at {ROOT}", file=sys.stderr)
        return 1

    total_links = 0
    total_files = 0
    for md in sorted(ROOT.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        new_text, count = process(text)
        if count > 0 and new_text != text:
            md.write_text(new_text, encoding="utf-8")
            rel = md.relative_to(ROOT)
            print(f"  {count:>3} -> {rel}")
            total_links += count
            total_files += 1
    print(f"\nDone. Converted {total_links} link(s) across {total_files} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
