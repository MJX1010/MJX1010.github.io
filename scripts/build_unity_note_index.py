#!/usr/bin/env python3
"""
Build a unified index for Unity notes.

The script scans Unity-themed Markdown notes, extracts their core bullet points
from key sections, and writes a navigable index note.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


DEFAULT_CONTENT_DIR = Path("content") / "游戏"
DEFAULT_OUTPUT = DEFAULT_CONTENT_DIR / "Unity-知识索引.md"
DEFAULT_MAX_POINTS = 8

KEY_SECTIONS = [
    "结论",
    "核心结论",
    "适用场景",
    "典型链路",
    "排查流程",
    "优化决策",
    "发布前检查清单",
    "CI 检查清单",
    "常见风险",
]

SKIP_NAMES = {
    "Unity-知识索引.md",
}


def now_date() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[end + 4 :].lstrip()
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"')
    return meta, body


def slug_to_wikilink(path: Path) -> str:
    return path.stem


def extract_sections(body: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current = ""
    for line in body.splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            current = heading.group(1).strip()
            sections.setdefault(current, [])
            continue
        if current:
            sections[current].append(line)
    return sections


def extract_bullets(lines: list[str]) -> list[str]:
    bullets: list[str] = []
    for line in lines:
        stripped = line.strip()
        match = re.match(r"^[-*]\s+(.+)$", stripped)
        if match:
            text = match.group(1).strip()
            if text and not text.startswith("["):
                bullets.append(text)
    return bullets


def summarize_note(path: Path, max_points: int) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    sections = extract_sections(body)
    points: list[str] = []
    section_hits: list[str] = []
    for section in KEY_SECTIONS:
        bullets = extract_bullets(sections.get(section, []))
        if bullets:
            section_hits.append(section)
            for bullet in bullets:
                if bullet not in points:
                    points.append(bullet)
                if len(points) >= max_points:
                    break
        if len(points) >= max_points:
            break
    if not points:
        for lines in sections.values():
            for bullet in extract_bullets(lines):
                if bullet not in points:
                    points.append(bullet)
                if len(points) >= max_points:
                    break
            if len(points) >= max_points:
                break
    return {
        "path": path,
        "title": meta.get("title") or path.stem,
        "wikilink": slug_to_wikilink(path),
        "sections": section_hits,
        "points": points,
    }


def find_notes(content_dir: Path) -> list[Path]:
    notes = []
    for path in sorted(content_dir.glob("Unity-*.md")):
        if path.name in SKIP_NAMES:
            continue
        if path.name.endswith("链接归档.md") or path.name.endswith("素材链接归档.md"):
            continue
        notes.append(path)
    return notes


def build_index(notes: list[dict[str, object]]) -> str:
    lines = [
        "---",
        "title: Unity 知识索引",
        "tags:",
        "  - Unity",
        "  - 索引",
        "  - 自动生成",
        "---",
        "",
        f"> 本文件由 `scripts/build_unity_note_index.py` 自动生成，生成时间：{now_date()}。",
        ">",
        "> 用途：汇总 Unity 主题笔记中的核心知识点，便于从一个入口跳转到具体笔记。",
        "",
        "## 笔记总览",
        "",
    ]
    for note in notes:
        sections = "、".join(note["sections"]) if note["sections"] else "核心要点"
        lines.append(f"- [[{note['wikilink']}]]：{sections}")
    lines.extend(["", "## 核心知识点", ""])
    for note in notes:
        lines.append(f"### [[{note['wikilink']}]]")
        lines.append("")
        points = note["points"]
        if points:
            for point in points:
                lines.append(f"- {point}")
        else:
            lines.append("- 暂无可自动提取的核心知识点。")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Unity note knowledge index.")
    parser.add_argument("--content-dir", type=Path, default=DEFAULT_CONTENT_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-points", type=int, default=DEFAULT_MAX_POINTS)
    args = parser.parse_args()

    note_paths = find_notes(args.content_dir)
    notes = [summarize_note(path, args.max_points) for path in note_paths]
    args.output.write_text(build_index(notes), encoding="utf-8")
    print(f"Wrote {args.output} from {len(notes)} notes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
