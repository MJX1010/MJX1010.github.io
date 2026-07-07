#!/usr/bin/env python3
"""Lint the public Quartz knowledge base.

The checks are intentionally lightweight and dependency-free:
- frontmatter presence and recommended governance fields
- broken wikilinks
- public sensitive links or token-like strings
- orphan notes and manifest consistency

Use --write-manifest to refresh content/.manifest.json from the current notes.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


DEFAULT_CONTENT_DIR = Path("content")
DEFAULT_MANIFEST = DEFAULT_CONTENT_DIR / ".manifest.json"

ALLOWED_STATUS = {"seed", "draft", "reviewed", "verified", "archived"}
ALLOWED_VISIBILITY = {"public", "internal", "private", "pii"}
RECOMMENDED_FIELDS = ("title", "tags", "status", "confidence", "visibility", "last_curated")
IGNORED_PUBLIC_DIRS = {"_meta"}
SKIP_ORPHAN_DIRS = set()
MAX_REFERENCE_LINKS = 10
INLINE_REFERENCE_HINTS = ("本页属于“入口型”清单", "主入口已直接内联到正文")
ENTRY_NOTE_HINTS = (
    "直达入口汇总",
    "入口汇总",
    "链接汇总",
    "导航首页",
    "快速查阅入口",
    "快速切换模型对话窗口",
    "产品入口",
    "工具入口",
    "文档和社区入口",
)

WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]]+)\]\]")
MARKDOWN_LINK_RE = re.compile(r"!?\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)

HARD_SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z\-_]{20,}\b")),
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("GitHub token", re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9._-]{10,}\.[A-Za-z0-9._-]{10,}\b")),
)

SENSITIVE_LINK_RE = re.compile(
    r"(?i)(/login\b|/dashboard\b|/api-keys?\b|apikey|authSessionId=|sid=|token=|"
    r"redirect_after_login=|dual_domain_token=|cs_live_|checkout/|console\.)"
)


@dataclass
class Finding:
    level: str
    path: Path
    message: str
    line: int | None = None


@dataclass
class Note:
    path: Path
    rel_path: str
    text: str
    frontmatter: dict[str, object]
    body: str
    title: str
    tags: list[str] = field(default_factory=list)


def today() -> str:
    return dt.date.today().isoformat()


def posix(path: Path) -> str:
    return path.as_posix()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def find_line(text: str, needle: str) -> int | None:
    index = text.find(needle)
    if index < 0:
        return None
    return text.count("\n", 0, index) + 1


def iter_markdown_files(content_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(content_dir.rglob("*.md")):
        rel = path.relative_to(content_dir)
        if rel.parts and rel.parts[0] in {"private", *IGNORED_PUBLIC_DIRS}:
            continue
        files.append(path)
    return files


def parse_scalar(value: str) -> object:
    value = value.strip().strip('"').strip("'")
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def parse_frontmatter(text: str) -> tuple[dict[str, object], str, str | None]:
    text = text.lstrip("\ufeff").replace("\r\n", "\n")
    delimiter = None
    if text.startswith("---\n"):
        delimiter = "---"
    elif text.startswith("***\n"):
        delimiter = "***"
    if delimiter is None:
        return {}, text, None

    end_marker = f"\n{delimiter}"
    end = text.find(end_marker, len(delimiter) + 1)
    if end == -1:
        return {}, text, None

    raw = text[len(delimiter) : end].strip("\n")
    body = text[end + len(end_marker) :].lstrip()
    meta: dict[str, object] = {}
    current_key: str | None = None

    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            current = meta.setdefault(current_key, [])
            if isinstance(current, list):
                current.append(line[4:].strip())
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            key = key.strip()
            current_key = key
            if value.strip():
                meta[key] = parse_scalar(value)
            else:
                meta[key] = []
    return meta, body, delimiter


def note_title(path: Path, meta: dict[str, object], body: str) -> str:
    title = meta.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()
    heading = HEADING_RE.search(body)
    if heading:
        return heading.group(1).strip()
    return path.stem


def note_tags(meta: dict[str, object]) -> list[str]:
    tags = meta.get("tags", [])
    if isinstance(tags, list):
        return [str(tag).strip() for tag in tags if str(tag).strip()]
    if isinstance(tags, str):
        return [part.strip() for part in tags.split(",") if part.strip()]
    return []


def load_notes(content_dir: Path) -> list[Note]:
    notes: list[Note] = []
    for path in iter_markdown_files(content_dir):
        text = path.read_text(encoding="utf-8")
        meta, body, _ = parse_frontmatter(text)
        notes.append(
            Note(
                path=path,
                rel_path=posix(path.relative_to(content_dir)),
                text=text,
                frontmatter=meta,
                body=body,
                title=note_title(path, meta, body),
                tags=note_tags(meta),
            )
        )
    return notes


def lint_frontmatter(notes: Iterable[Note]) -> list[Finding]:
    findings: list[Finding] = []
    for note in notes:
        if not note.frontmatter:
            findings.append(Finding("warning", note.path, "缺少 frontmatter"))
            continue

        for field_name in RECOMMENDED_FIELDS:
            if field_name not in note.frontmatter:
                findings.append(Finding("warning", note.path, f"建议补充 frontmatter 字段 `{field_name}`"))

        status = note.frontmatter.get("status")
        if status is not None and str(status) not in ALLOWED_STATUS:
            findings.append(Finding("error", note.path, f"`status` 非法：{status}"))

        visibility = note.frontmatter.get("visibility")
        if visibility is not None and str(visibility) not in ALLOWED_VISIBILITY:
            findings.append(Finding("error", note.path, f"`visibility` 非法：{visibility}"))

        confidence = note.frontmatter.get("confidence")
        if confidence is not None:
            try:
                score = float(confidence)
                if not 0 <= score <= 1:
                    findings.append(Finding("error", note.path, "`confidence` 应在 0.0 到 1.0 之间"))
            except (TypeError, ValueError):
                findings.append(Finding("error", note.path, "`confidence` 应为数字"))
    return findings


def build_registry(notes: Iterable[Note]) -> dict[str, list[Note]]:
    registry: dict[str, list[Note]] = {}
    for note in notes:
        keys = {note.path.stem, note.title}
        keys.add(note.rel_path)
        keys.add(note.rel_path.removesuffix(".md"))
        for key in keys:
            registry.setdefault(key, []).append(note)
    return registry


def normalize_wikilink(raw: str) -> str:
    target = raw.split("|", 1)[0].split("#", 1)[0].strip()
    if target.endswith(".md"):
        target = target[:-3]
    return target


def lint_wikilinks(notes: Iterable[Note], registry: dict[str, list[Note]]) -> list[Finding]:
    findings: list[Finding] = []
    for key, matches in registry.items():
        if "/" not in key and len(matches) > 1:
            paths = ", ".join(note.rel_path for note in matches)
            findings.append(Finding("warning", matches[0].path, f"可能存在重复页面标识 `{key}`：{paths}"))

    for note in notes:
        for match in WIKILINK_RE.finditer(note.text):
            target = normalize_wikilink(match.group(1))
            if target and target not in registry:
                line = note.text.count("\n", 0, match.start()) + 1
                findings.append(Finding("error", note.path, f"失效 wikilink：[[{match.group(1)}]]", line))
    return findings


def lint_sensitive_content(notes: Iterable[Note]) -> list[Finding]:
    findings: list[Finding] = []
    for note in notes:
        for label, pattern in HARD_SECRET_PATTERNS:
            for match in pattern.finditer(note.text):
                line = note.text.count("\n", 0, match.start()) + 1
                findings.append(Finding("error", note.path, f"疑似真实密钥：{label}", line))

        for label, url in MARKDOWN_LINK_RE.findall(note.text):
            if url.startswith(("#", "mailto:")):
                continue
            if SENSITIVE_LINK_RE.search(url):
                line = find_line(note.text, url)
                findings.append(Finding("warning", note.path, f"公开内容疑似账号/控制台入口：{label or url}", line))
    return findings


def lint_reference_sections(notes: Iterable[Note]) -> list[Finding]:
    findings: list[Finding] = []
    for note in notes:
        has_external = any(url.startswith(("http://", "https://")) for _, url in MARKDOWN_LINK_RE.findall(note.text))
        if has_external and "## 参考链接" not in note.text and note.rel_path != "index.md":
            if any(hint in note.text for hint in INLINE_REFERENCE_HINTS):
                continue
            findings.append(Finding("warning", note.path, "包含外链但缺少 `## 参考链接` 小节"))
            continue

        if "## 参考链接" in note.text:
            ref_body = note.text.split("## 参考链接", 1)[1]
            ref_links = [
                url
                for _, url in MARKDOWN_LINK_RE.findall(ref_body)
                if url.startswith(("http://", "https://"))
            ]
            if len(ref_links) > MAX_REFERENCE_LINKS:
                findings.append(
                    Finding(
                        "warning",
                        note.path,
                        f"`参考链接` 过多：{len(ref_links)} 条，建议压缩到 {MAX_REFERENCE_LINKS} 条以内",
                    )
                )
    return findings


def split_reference_section(text: str) -> tuple[str, str]:
    if "## 参考链接" not in text:
        return text, ""
    body, ref = text.split("## 参考链接", 1)
    return body, ref


def note_is_entry_type(note: Note) -> bool:
    if note.rel_path == "index.md":
        return False
    lead = note.body[:800]
    hint_hits = sum(1 for hint in ENTRY_NOTE_HINTS if hint in lead)
    short_bullets = sum(
        1
        for line in lead.splitlines()
        if line.strip().startswith("- ") and len(line.strip()) <= 100
    )
    inline_hint = any(hint in note.text for hint in INLINE_REFERENCE_HINTS)
    return inline_hint or (hint_hits >= 1 and short_bullets >= 3)


def lint_entry_notes(notes: Iterable[Note]) -> list[Finding]:
    findings: list[Finding] = []
    for note in notes:
        if not note_is_entry_type(note):
            continue
        body_text, ref_text = split_reference_section(note.text)
        body_links = [url for _, url in MARKDOWN_LINK_RE.findall(body_text) if url.startswith(("http://", "https://"))]
        ref_links = [url for _, url in MARKDOWN_LINK_RE.findall(ref_text) if url.startswith(("http://", "https://"))]
        if not body_links:
            findings.append(Finding("warning", note.path, "入口型页面应将主入口直接内联到正文，而不是只放在文末参考链接"))
            continue
    return findings


def lint_orphans(notes: list[Note]) -> list[Finding]:
    findings: list[Finding] = []
    linked: set[str] = set()
    registry = build_registry(notes)
    for note in notes:
        for match in WIKILINK_RE.finditer(note.text):
            target = normalize_wikilink(match.group(1))
            for matched in registry.get(target, []):
                linked.add(matched.rel_path)

    for note in notes:
        first_part = Path(note.rel_path).parts[0]
        if note.rel_path == "index.md" or first_part in SKIP_ORPHAN_DIRS:
            continue
        if note.rel_path not in linked:
            findings.append(Finding("warning", note.path, "可能是孤立页面：没有被其他公开笔记 wikilink 到"))
    return findings


def load_manifest(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"_error": f"manifest JSON 解析失败：{exc}"}


def lint_manifest(manifest_path: Path, content_dir: Path, notes: list[Note]) -> list[Finding]:
    findings: list[Finding] = []
    manifest = load_manifest(manifest_path)
    if not manifest:
        findings.append(Finding("warning", manifest_path, "缺少 manifest，可运行 `python scripts/wiki_lint.py --write-manifest` 生成"))
        return findings
    if "_error" in manifest:
        findings.append(Finding("error", manifest_path, str(manifest["_error"])))
        return findings

    existing = {note.rel_path for note in notes}
    manifest_notes = manifest.get("notes", {})
    if isinstance(manifest_notes, dict):
        for rel_path in manifest_notes:
            if rel_path not in existing:
                findings.append(Finding("warning", manifest_path, f"manifest 中记录了不存在的笔记：{rel_path}"))

    sources = manifest.get("sources", [])
    if isinstance(sources, list):
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                continue
            for target in source.get("target_notes", []):
                if target not in existing:
                    findings.append(Finding("warning", manifest_path, f"source[{index}] 指向不存在的笔记：{target}"))
    return findings


def note_manifest_entry(note: Note) -> dict[str, object]:
    external_links = [url for _, url in MARKDOWN_LINK_RE.findall(note.text) if url.startswith(("http://", "https://"))]
    return {
        "title": note.title,
        "tags": note.tags,
        "status": note.frontmatter.get("status", "unclassified"),
        "visibility": note.frontmatter.get("visibility", "public"),
        "confidence": note.frontmatter.get("confidence"),
        "sha256": sha256_text(note.text),
        "external_link_count": len(external_links),
    }


def yaml_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if not text:
        return '""'
    if any(char in text for char in [":", "#", "[", "]", "{", "}", ","]):
        return json.dumps(text, ensure_ascii=False)
    return text


def render_frontmatter(meta: dict[str, object]) -> str:
    lines = ["---"]
    ordered_keys = ["title", "tags", "status", "confidence", "visibility", "last_curated", "source_count"]
    remaining_keys = [key for key in meta if key not in ordered_keys]
    for key in ordered_keys + remaining_keys:
        if key not in meta:
            continue
        value = meta[key]
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {yaml_value(item)}")
        else:
            lines.append(f"{key}: {yaml_value(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def default_tags_for(path: Path, content_dir: Path) -> list[str]:
    rel = path.relative_to(content_dir)
    parts = list(rel.parts[:-1])
    return parts[:3] if parts else ["首页"]


def frontmatter_defaults(note: Note, content_dir: Path) -> dict[str, object]:
    external_links = [url for _, url in MARKDOWN_LINK_RE.findall(note.text) if url.startswith(("http://", "https://"))]
    meta = dict(note.frontmatter)
    meta.setdefault("title", note.title)
    meta.setdefault("tags", note.tags or default_tags_for(note.path, content_dir))
    meta.setdefault("status", "reviewed")
    meta.setdefault("confidence", 0.7)
    meta.setdefault("visibility", "public")
    meta.setdefault("last_curated", today())
    meta.setdefault("source_count", len(external_links))
    return meta


def fix_frontmatter(content_dir: Path, notes: list[Note]) -> int:
    changed = 0
    for note in notes:
        meta = frontmatter_defaults(note, content_dir)
        new_text = render_frontmatter(meta) + note.body.rstrip() + "\n"
        if new_text != note.text:
            note.path.write_text(new_text, encoding="utf-8")
            changed += 1
    return changed


def write_manifest(path: Path, content_dir: Path, notes: list[Note]) -> None:
    existing = load_manifest(path)
    if "_error" in existing:
        existing = {}
    manifest = {
        "schema_version": 1,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "content_root": posix(content_dir),
        "policy": {
            "private_content": "content/private/ is ignored by git and Quartz publication",
            "link_format": "wikilink",
            "frontmatter_spec": "stored in content/_meta/ and excluded from publication",
        },
        "sources": existing.get("sources", []) if isinstance(existing, dict) else [],
        "review_queue": existing.get("review_queue", []) if isinstance(existing, dict) else [],
        "notes": {note.rel_path: note_manifest_entry(note) for note in notes},
    }
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def format_finding(content_dir: Path, finding: Finding) -> str:
    try:
        rel = finding.path.relative_to(content_dir.parent)
    except ValueError:
        rel = finding.path
    suffix = f":{finding.line}" if finding.line else ""
    return f"[{finding.level.upper()}] {posix(rel)}{suffix} - {finding.message}"


def run_lint(content_dir: Path, manifest_path: Path) -> tuple[list[Finding], list[Note]]:
    notes = load_notes(content_dir)
    registry = build_registry(notes)
    findings: list[Finding] = []
    findings.extend(lint_frontmatter(notes))
    findings.extend(lint_wikilinks(notes, registry))
    findings.extend(lint_sensitive_content(notes))
    findings.extend(lint_reference_sections(notes))
    findings.extend(lint_entry_notes(notes))
    findings.extend(lint_orphans(notes))
    findings.extend(lint_manifest(manifest_path, content_dir, notes))
    return findings, notes


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint public Quartz knowledge-base content.")
    parser.add_argument("--content-dir", type=Path, default=DEFAULT_CONTENT_DIR)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--write-manifest", action="store_true", help="Refresh content/.manifest.json from current notes")
    parser.add_argument("--fix-frontmatter", action="store_true", help="Add baseline governance frontmatter to public notes")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()

    findings, notes = run_lint(args.content_dir, args.manifest)

    if args.fix_frontmatter:
        changed = fix_frontmatter(args.content_dir, notes)
        print(f"Updated frontmatter in {changed} notes.")
        findings, notes = run_lint(args.content_dir, args.manifest)

    if args.write_manifest:
        write_manifest(args.manifest, args.content_dir, notes)
        findings, notes = run_lint(args.content_dir, args.manifest)

    errors = [finding for finding in findings if finding.level == "error"]
    warnings = [finding for finding in findings if finding.level == "warning"]

    print(f"Scanned {len(notes)} public markdown notes.")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    for finding in findings:
        print(format_finding(args.content_dir, finding))

    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
