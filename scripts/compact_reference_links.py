#!/usr/bin/env python3
"""Compact long reference sections in public notes.

Rules:
- only process public notes under content/ (skip private and _meta)
- if a note has more than MAX_KEEP reference links, keep a curated subset
- kept links are regrouped into 官方文档 / 开源项目 / 补充阅读
- add a short "资料收敛说明" section before references
- refresh `source_count` to match current visible external link count
"""

from __future__ import annotations

import re
import subprocess
import urllib.parse
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
MAX_KEEP = 10

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n\n", re.S)
REF_SECTION_RE = re.compile(r"\n## 参考链接\n[\s\S]*$", re.M)
HEADING_RE = re.compile(r"^###\s+(.+?)\s*$")
LINK_RE = re.compile(r"^- \[([^\]]+)\]\((https?://[^)]+)\)\s*$")
EXT_LINK_RE = re.compile(r"\[[^\]]+\]\((https?://[^)]+)\)")

OFFICIAL_DOMAINS = {
    "docs.unity3d.com",
    "unity.com",
    "developer.android.com",
    "firebase.google.com",
    "learn.microsoft.com",
    "dotnet.microsoft.com",
    "docs.python.org",
    "plantuml.com",
    "kubernetes.io",
    "docker.com",
    "docs.unrealengine.com",
    "dev.epicgames.com",
    "cppreference.com",
    "zh.cppreference.com",
    "en.cppreference.com",
    "cplusplus.com",
    "referencesource.microsoft.com",
}

LOW_SIGNAL_DOMAINS = {
    "csdn.net",
    "zhihu.com",
    "juejin.cn",
    "cnblogs.com",
    "runoob.com",
    "aliyun.com",
    "developer.aliyun.com",
    "bookstack.cn",
    "weixin.qq.com",
    "blog.csdn.net",
}

LOW_SIGNAL_LABELS = (
    "download",
    "排行榜",
    "动态首页",
    "home",
    "feed",
    "marketplace",
    "issue #",
    "issues",
    "releases",
    "目录",
    "月度热门",
    "模板",
)

TOKEN_RE = re.compile(r"[\u4e00-\u9fff]{2,}|[A-Za-z0-9][A-Za-z0-9.+#_-]{2,}")


@dataclass(frozen=True)
class LinkItem:
    section: str
    label: str
    url: str
    domain: str
    normalized: str


def iter_public_notes() -> list[Path]:
    notes: list[Path] = []
    for path in sorted(CONTENT.rglob("*.md")):
        rel = path.relative_to(CONTENT)
        if rel.parts and rel.parts[0] in {"private", "_meta"}:
            continue
        notes.append(path)
    return notes


def normalize_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    query = urllib.parse.urlencode(
        [
            (key, value)
            for key, value in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
            if not key.lower().startswith("utm_")
        ]
    )
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc.lower(), parsed.path.rstrip("/"), query, ""))


def domain_of(url: str) -> str:
    return urllib.parse.urlsplit(url).netloc.lower().removeprefix("www.")


def parse_reference_links(text: str) -> list[LinkItem]:
    if "## 参考链接" not in text:
        return []
    ref_body = text.split("## 参考链接", 1)[1]
    section = "链接分组"
    items: list[LinkItem] = []
    for raw_line in ref_body.splitlines():
        line = raw_line.strip()
        heading = HEADING_RE.match(line)
        if heading:
            section = heading.group(1).strip()
            continue
        match = LINK_RE.match(line)
        if not match:
            continue
        label, url = match.groups()
        items.append(
            LinkItem(
                section=section,
                label=label.strip(),
                url=url.strip(),
                domain=domain_of(url),
                normalized=normalize_url(url),
            )
        )
    return items


def git_source_text(path: Path) -> str | None:
    rel = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "show", f"HEAD:{rel}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        return None
    return result.stdout


def keywords_for(item: LinkItem) -> list[str]:
    source = " ".join(
        [
            item.label,
            item.section,
            item.domain.replace(".", " "),
            urllib.parse.urlsplit(item.url).path.replace("/", " "),
        ]
    )
    seen: set[str] = set()
    out: list[str] = []
    for token in TOKEN_RE.findall(source):
        token = token.lower()
        if token in {"https", "http", "www", "com", "github", "docs", "blob", "tree", "main", "index"}:
            continue
        if token not in seen:
            seen.add(token)
            out.append(token)
    return out


def score_link(item: LinkItem, body_text: str) -> tuple[int, int, int, int]:
    score = 0
    domain = item.domain
    label = item.label.lower()
    url = item.url.lower()
    body_lower = body_text.lower()

    if domain in OFFICIAL_DOMAINS or any(domain.endswith(f".{root}") for root in OFFICIAL_DOMAINS):
        score += 6
    if "github.com" in domain:
        score += 5
    if any(key in label for key in ("manual", "documentation", "scriptreference", "learn", "官方", "手册", "docs")):
        score += 4
    if any(key in item.section for key in ("GitHub", "AI 相关", "链接分组")):
        score += 1
    if "readme" in url or "overview" in url:
        score += 1
    if "?" not in item.url:
        score += 1
    if urllib.parse.urlsplit(item.url).path.count("/") <= 2:
        score += 1

    if any(flag in label for flag in LOW_SIGNAL_LABELS):
        score -= 3
    if domain in LOW_SIGNAL_DOMAINS or any(domain.endswith(f".{root}") for root in LOW_SIGNAL_DOMAINS):
        score -= 2
    if any(flag in url for flag in ("?tab=", "/issues/", "/releases", "rank", "popular")):
        score -= 2
    if any(flag in url for flag in ("/download", "/downloads", "/marketplace", "/search", "/home")):
        score -= 2

    body_hits = 0
    for token in keywords_for(item):
        if token in body_lower:
            body_hits += 1
    score += min(body_hits, 4) * 3

    section_bonus = 2 if "GitHub" in item.section or "AI 相关" in item.section else 1
    official_bonus = 1 if domain in OFFICIAL_DOMAINS or "github.com" in domain else 0
    return score, body_hits, section_bonus, official_bonus


def dedupe_links(items: list[LinkItem]) -> list[LinkItem]:
    seen: set[str] = set()
    out: list[LinkItem] = []
    for item in items:
        if item.normalized in seen:
            continue
        seen.add(item.normalized)
        out.append(item)
    return out


def choose_links(items: list[LinkItem], max_keep: int, body_text: str) -> list[LinkItem]:
    items = dedupe_links(items)
    if len(items) <= max_keep:
        return items

    sorted_items = sorted(items, key=lambda item: score_link(item, body_text), reverse=True)
    selected: list[LinkItem] = []
    used_domains: set[str] = set()
    used_sections: set[str] = set()

    for item in sorted_items:
        if item.section in used_sections:
            continue
        selected.append(item)
        used_sections.add(item.section)
        used_domains.add(item.domain)
        if len(selected) >= max_keep:
            return selected[:max_keep]

    for item in sorted_items:
        if item in selected:
            continue
        if item.domain in used_domains and len(selected) < max_keep - 2:
            continue
        selected.append(item)
        used_domains.add(item.domain)
        if len(selected) >= max_keep:
            break

    return selected[:max_keep]


def category_name(item: LinkItem) -> str:
    if item.domain in OFFICIAL_DOMAINS or any(item.domain.endswith(f".{root}") for root in OFFICIAL_DOMAINS):
        return "官方文档"
    if "github.com" in item.domain:
        return "开源项目"
    return "补充阅读"


def render_compact_reference(items: list[LinkItem]) -> str:
    groups = {"官方文档": [], "开源项目": [], "补充阅读": []}
    for item in items:
        groups[category_name(item)].append(item)

    lines = ["## 参考链接", "", "> 以下链接仅保留正文仍需回看的核心资料入口。", ""]
    for name in ("官方文档", "开源项目", "补充阅读"):
        links = groups[name]
        if not links:
            continue
        lines.append(f"### {name}")
        lines.append("")
        for item in links:
            lines.append(f"- [{item.label}]({item.url})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def ensure_absorb_section(body: str, original_count: int, kept_count: int) -> str:
    section = (
        "## 资料收敛说明\n\n"
        f"- 本页已将原先 `{original_count}` 条参考链接压缩为 `{kept_count}` 条核心引用，重复导航页、同类 API 细节页和低信噪比补充资料不再逐条公开保留。\n"
        "- 正文已优先沉淀选型标准、排查流程、风险边界和常用工具定位，后续新增资料应继续转成正文结论，而不是直接堆叠链接。\n"
        "- 文末只保留官方文档、代表性开源项目和少量仍值得回看的补充阅读。\n"
    )
    marker = "## 资料收敛说明"
    if marker in body:
        body = re.sub(r"\n## 资料收敛说明\n[\s\S]*?(?=\n## )", "\n" + section + "\n", body, count=1)
        return body.rstrip() + "\n"

    insert_after = None
    for heading in ("## 风险清单", "## 维护建议", "## 后续补充资料筛选规则", "## 总结", "## 结论"):
        idx = body.find(heading)
        if idx != -1:
            insert_after = idx
    if insert_after is None:
        return body.rstrip() + "\n\n" + section + "\n"

    next_heading = body.find("\n## ", insert_after + 1)
    if next_heading == -1:
        return body.rstrip() + "\n\n" + section + "\n"
    return body[:next_heading].rstrip() + "\n\n" + section + "\n" + body[next_heading + 1 :].lstrip()


def update_source_count(text: str) -> str:
    count = len(EXT_LINK_RE.findall(text))
    if re.search(r"^source_count:\s*\d+\s*$", text, re.M):
        return re.sub(r"^source_count:\s*\d+\s*$", f"source_count: {count}", text, count=1, flags=re.M)
    return text


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    source_text = git_source_text(path) or text
    items = parse_reference_links(source_text)
    if len(items) <= MAX_KEEP:
        updated = update_source_count(text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            return True
        return False

    body = REF_SECTION_RE.sub("", source_text).rstrip() + "\n"
    kept = choose_links(items, MAX_KEEP, body)
    body = ensure_absorb_section(body, len(items), len(kept))
    new_text = body.rstrip() + "\n\n" + render_compact_reference(kept)
    new_text = update_source_count(new_text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = 0
    for path in iter_public_notes():
        if process(path):
            changed += 1
            print(path.relative_to(ROOT).as_posix())
    print(f"\nUpdated {changed} notes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
