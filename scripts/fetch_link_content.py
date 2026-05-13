#!/usr/bin/env python3
"""
Link content fetcher for the knowledge base.

The script turns links from Markdown notes into cached Markdown/JSON source
material. It prefers local specialist tools when available, then falls back to
public URL-to-Markdown services for accessible pages.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Iterable


DEFAULT_CACHE_DIR = Path("private/link_cache")
DEFAULT_TIMEOUT = 45

SERVICE_ENDPOINTS = [
    ("jina", "https://r.jina.ai/{url}"),
    ("markdown.new", "https://markdown.new/{url}"),
    ("defuddle", "https://defuddle.md/{url}"),
]

URL_RE = re.compile(r"https?://[^\s)<>\"]+")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def normalize_url(url: str) -> str:
    return url.strip().rstrip(".,;，。；")


def cache_key(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def safe_name(text: str, max_len: int = 80) -> str:
    text = re.sub(r"[\\/:*?\"<>|\r\n\t]+", "-", text).strip(" -")
    text = re.sub(r"\s+", " ", text)
    return text[:max_len] or "untitled"


def run_cmd(cmd: list[str], timeout: int) -> tuple[bool, str, str]:
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as exc:
        return False, "", str(exc)


def http_get(url: str, timeout: int = DEFAULT_TIMEOUT) -> tuple[bool, str, str]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,text/plain;q=0.8,*/*;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            data = resp.read()
        return True, data.decode(charset, errors="replace"), ""
    except urllib.error.HTTPError as exc:
        return False, "", f"HTTP {exc.code}: {exc.reason}"
    except Exception as exc:
        return False, "", str(exc)


def resolve_final_url(url: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
        )
    }
    req = urllib.request.Request(url, headers=headers, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.geturl()
    except Exception:
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.geturl()
        except Exception:
            return url


def html_to_text(markup: str) -> str:
    markup = re.sub(r"(?is)<(script|style|noscript|svg).*?</\1>", "\n", markup)
    markup = re.sub(r"(?i)<br\s*/?>", "\n", markup)
    markup = re.sub(r"(?i)</(p|div|section|article|h[1-6]|li|tr)>", "\n", markup)
    markup = re.sub(r"(?is)<[^>]+>", " ", markup)
    text = html.unescape(markup)
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def extract_title(markdown_or_html: str, fallback: str) -> str:
    for pattern in [
        r"(?im)^#\s+(.+)$",
        r"(?is)<title[^>]*>(.*?)</title>",
        r"(?is)<h1[^>]*>(.*?)</h1>",
        r"(?im)^Title:\s*(.+)$",
    ]:
        match = re.search(pattern, markdown_or_html)
        if match:
            title = html_to_text(match.group(1)).strip()
            if title:
                return title[:120]
    return fallback


def looks_like_error_page(title: str, content: str) -> bool:
    title_lower = title.strip().lower()
    if title_lower in {"404", "404 not found", "not found", "page not found", "login", "sign in"}:
        return True
    head = content[:1000].lower()
    return any(
        marker in head
        for marker in [
            "404 not found",
            "page not found",
            "页面不存在",
            "请先登录",
            "访问频繁",
            "环境异常",
            "验证",
            "login required",
            "sign in",
            "not found |",
        ]
    )


def extract_markdown_links(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    items: list[dict[str, str]] = []
    seen: set[str] = set()
    for title, url in MD_LINK_RE.findall(text):
        clean = normalize_url(url)
        if clean not in seen:
            seen.add(clean)
            items.append({"title": title.strip(), "url": clean})
    for url in URL_RE.findall(text):
        clean = normalize_url(url)
        if clean not in seen:
            seen.add(clean)
            items.append({"title": "", "url": clean})
    return items


def classify_url(url: str) -> str:
    host = urllib.parse.urlparse(url).netloc.lower()
    if "youtube.com" in host or "youtu.be" in host:
        return "youtube"
    if "bilibili.com" in host or "b23.tv" in host:
        return "bilibili"
    if "mp.weixin.qq.com" in host:
        return "wechat"
    if "github.com" in host or "raw.githubusercontent.com" in host:
        return "github"
    return "web"


def extract_bilibili_id(url: str) -> tuple[str, str] | None:
    match = re.search(r"BV[a-zA-Z0-9]{10}", url)
    if match:
        return "bvid", match.group(0)
    match = re.search(r"(?:/av|av)(\d+)", url)
    if match:
        return "aid", match.group(1)
    return None


def subtitle_to_text(raw: str) -> str:
    lines: list[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        if (
            not stripped
            or stripped.upper() == "WEBVTT"
            or "-->" in stripped
            or re.match(r"^\d+$", stripped)
            or stripped.startswith(("NOTE", "Kind:", "Language:"))
        ):
            continue
        stripped = re.sub(r"<[^>]+>", "", stripped)
        if stripped and (not lines or lines[-1] != stripped):
            lines.append(stripped)
    return "\n".join(lines)


def json_to_video_markdown(data: dict[str, object], url: str, source: str) -> str:
    title = str(data.get("title") or data.get("fulltitle") or "Untitled video")
    owner = data.get("owner")
    owner_name = owner.get("name", "") if isinstance(owner, dict) else ""
    uploader = str(data.get("uploader") or data.get("channel") or owner_name)
    duration = data.get("duration")
    description = str(data.get("description") or data.get("desc") or "").strip()
    tags = data.get("tags") or []
    if isinstance(tags, list):
        tag_text = ", ".join(str(tag) for tag in tags[:20])
    else:
        tag_text = ""
    lines = [
        f"# {title}",
        "",
        f"- Source: {source}",
        f"- URL: {url}",
    ]
    if uploader:
        lines.append(f"- Uploader: {uploader}")
    if duration:
        lines.append(f"- Duration: {duration}s")
    if tag_text:
        lines.append(f"- Tags: {tag_text}")
    if description:
        lines.extend(["", "## Description", "", description])
    return "\n".join(lines).strip()


def try_bilibili_api(url: str, timeout: int) -> tuple[bool, str, str]:
    bilibili_id = extract_bilibili_id(url)
    if not bilibili_id and "b23.tv" in urllib.parse.urlparse(url).netloc.lower():
        bilibili_id = extract_bilibili_id(resolve_final_url(url, timeout))
    if not bilibili_id:
        return False, "", "no bvid/aid found"
    id_type, value = bilibili_id
    api_url = f"https://api.bilibili.com/x/web-interface/view?{id_type}={value}"
    ok, raw, error = http_get(api_url, timeout=timeout)
    if not ok:
        return False, "", error
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        return False, "", str(exc)
    if payload.get("code") != 0:
        return False, "", str(payload.get("message") or "bilibili api error")
    data = payload.get("data") or {}
    if not isinstance(data, dict):
        return False, "", "empty bilibili data"
    markdown = json_to_video_markdown(data, url, "bilibili-api")
    return True, markdown, ""


def try_ytdlp_metadata(url: str, timeout: int) -> tuple[bool, str, str]:
    if not shutil.which("yt-dlp"):
        return False, "", "yt-dlp not installed"
    with tempfile.TemporaryDirectory(prefix="link-fetch-ytdlp-") as tmp:
        ok, stdout, stderr = run_cmd(
            [
                "yt-dlp",
                "--skip-download",
                "--dump-json",
                "--no-warnings",
                "--write-subs",
                "--write-auto-subs",
                "--sub-langs",
                "zh-Hans,zh-CN,zh,en",
                "--sub-format",
                "vtt",
                "-P",
                tmp,
                "-o",
                "%(id)s.%(ext)s",
                url,
            ],
            timeout=timeout,
        )
        if not ok or not stdout:
            return False, "", stderr or "empty yt-dlp output"
        try:
            data = json.loads(stdout.splitlines()[-1])
        except json.JSONDecodeError as exc:
            return False, "", str(exc)
        markdown = json_to_video_markdown(data, url, "yt-dlp")
        subtitle_blocks: list[str] = []
        for subtitle_path in sorted(Path(tmp).glob("*.vtt")):
            subtitle_text = subtitle_to_text(subtitle_path.read_text(encoding="utf-8", errors="replace"))
            if subtitle_text:
                subtitle_blocks.append(subtitle_text)
        if subtitle_blocks:
            markdown += "\n\n## Transcript\n\n" + "\n\n".join(subtitle_blocks)
        return True, markdown, ""


def try_wechat_public_html(url: str, timeout: int) -> tuple[bool, str, str]:
    ok, raw, error = http_get(url, timeout=timeout)
    if not ok or not raw:
        return False, "", error or "empty wechat html"
    blocked_markers = [
        "访问频繁",
        "环境异常",
        "请在微信客户端打开",
        "验证码",
        "请点击下方按钮继续访问",
        "继续访问",
        "该内容已被发布者删除",
        "此内容因违规无法查看",
        "当前内容可能存在未经审核的第三方商业营销信息",
        "微信公众平台安全验证",
    ]
    if any(marker in raw for marker in blocked_markers):
        return False, "", "wechat page requires verification or client context"
    title = extract_title(raw, "微信公众号文章")
    author_match = re.search(r'id=["\']js_name["\'][^>]*>(.*?)</', raw, re.I | re.S)
    content_match = re.search(r'id=["\']js_content["\'][^>]*>(.*?)</div>', raw, re.I | re.S)
    author = html_to_text(author_match.group(1)).strip() if author_match else ""
    body = html_to_text(content_match.group(1)).strip() if content_match else html_to_text(raw)
    if len(body) < 200:
        return False, "", "wechat content too short"
    lines = [f"# {title}", "", f"- URL: {url}"]
    if author:
        lines.append(f"- 公众号: {author}")
    lines.extend(["", "## 正文", "", body])
    return True, "\n".join(lines).strip(), ""


def try_kind_specific_fetch(url: str, kind: str, timeout: int) -> tuple[bool, str, str, str]:
    if kind == "wechat":
        ok, content, error = try_wechat_public_html(url, timeout)
        return ok, content, "wechat-public-html" if ok else "", error
    if kind == "bilibili":
        ok, content, error = try_bilibili_api(url, timeout)
        api_content = content if ok else ""
        api_error = error
        ytdlp_ok, ytdlp_content, ytdlp_error = try_ytdlp_metadata(url, timeout)
        if ok and ytdlp_ok:
            if "## Transcript" in ytdlp_content:
                transcript = ytdlp_content.split("## Transcript", 1)[1].strip()
                content = api_content.rstrip() + "\n\n## Transcript\n\n" + transcript
            return True, content, "bilibili-api+yt-dlp", ""
        if ok:
            return True, api_content, "bilibili-api", ytdlp_error
        return ytdlp_ok, ytdlp_content, "yt-dlp" if ytdlp_ok else "", api_error or ytdlp_error
    if kind == "youtube":
        ok, content, error = try_ytdlp_metadata(url, timeout)
        return ok, content, "yt-dlp" if ok else "", error
    return False, "", "", "no kind-specific fetcher"


def try_firecrawl(url: str, timeout: int) -> tuple[bool, str, str]:
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        return False, "", "FIRECRAWL_API_KEY not set"
    payload = json.dumps({"url": url, "formats": ["markdown"], "onlyMainContent": True}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v2/scrape",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        markdown = data.get("data", {}).get("markdown") or data.get("markdown") or ""
        return bool(markdown), markdown, "" if markdown else "empty firecrawl response"
    except Exception as exc:
        return False, "", str(exc)


def try_specialist_cli(url: str, kind: str, timeout: int) -> tuple[bool, str, str, str]:
    candidates: list[tuple[str, list[str]]] = []

    if kind in {"youtube", "bilibili"} and shutil.which("cat-crawl"):
        candidates.append(("cat-crawl", ["cat-crawl", "download", url]))

    for name in ["arcfetch", "markgrab", "web-crawl"]:
        if shutil.which(name):
            candidates.append((name, [name, url]))

    for name, cmd in candidates:
        ok, stdout, stderr = run_cmd(cmd, timeout=timeout)
        if ok and stdout and len(stdout) > 200:
            return True, stdout, name, ""
        if stderr:
            last_error = stderr
        else:
            last_error = "empty output"
    return False, "", "", locals().get("last_error", "no specialist CLI available")


def try_public_services(url: str, timeout: int) -> tuple[bool, str, str, str]:
    errors = []
    for name, template in SERVICE_ENDPOINTS:
        service_url = template.format(url=url)
        ok, text, error = http_get(service_url, timeout=timeout)
        if ok and text and len(text.strip()) > 200:
            return True, text.strip(), name, ""
        errors.append(f"{name}: {error or 'empty response'}")
        time.sleep(0.5)
    return False, "", "", "; ".join(errors)


def fetch_one(item: dict[str, str], cache_dir: Path, timeout: int, refresh: bool) -> dict[str, object]:
    url = item["url"]
    kind = classify_url(url)
    key = cache_key(url)
    out_dir = cache_dir / kind
    out_dir.mkdir(parents=True, exist_ok=True)
    meta_path = out_dir / f"{key}.json"
    md_path = out_dir / f"{key}.md"

    if meta_path.exists() and md_path.exists() and not refresh:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        meta["cached"] = True
        return meta

    attempts: list[str] = []
    content = ""
    method = ""

    ok, content, method, error = try_kind_specific_fetch(url, kind, timeout)
    attempts.append(f"kind-specific: {method or error}")

    if not ok:
        ok, content, method, error = try_specialist_cli(url, kind, timeout)
        attempts.append(f"specialist: {method or error}")

    if not ok:
        ok, content, error = try_firecrawl(url, timeout)
        method = "firecrawl" if ok else ""
        attempts.append(f"firecrawl: {'ok' if ok else error}")

    if not ok:
        ok, content, method, error = try_public_services(url, timeout)
        attempts.append(f"public-service: {method or error}")

    if not ok:
        ok, raw, error = http_get(url, timeout=timeout)
        if ok and raw:
            content = html_to_text(raw)
            method = "direct-html"
            ok = len(content) > 200
        attempts.append(f"direct-html: {'ok' if ok else error}")

    title = extract_title(content, item.get("title") or urllib.parse.urlparse(url).netloc)
    if ok and looks_like_error_page(title, content):
        ok = False
        attempts.append("error-page-detected")
    meta: dict[str, object] = {
        "url": url,
        "title": title,
        "kind": kind,
        "method": method,
        "fetched_at": now_iso(),
        "content_chars": len(content),
        "cached": False,
        "ok": bool(ok and content),
        "attempts": attempts,
        "markdown_path": str(md_path),
    }

    if content:
        header = [
            "---",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"source_url: {json.dumps(url, ensure_ascii=False)}",
            f"source_kind: {kind}",
            f"fetch_method: {method}",
            f"fetched_at: {meta['fetched_at']}",
            "---",
            "",
        ]
        md_path.write_text("\n".join(header) + content.strip() + "\n", encoding="utf-8")
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return meta


def build_digest(results: Iterable[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Link Fetch Digest",
        "",
        f"- Generated: {now_iso()}",
        "",
        "## Sources",
        "",
    ]
    for meta in results:
        status = "OK" if meta.get("ok") else "FAIL"
        title = str(meta.get("title") or meta.get("url"))
        url = str(meta.get("url"))
        method = str(meta.get("method") or "-")
        path = str(meta.get("markdown_path") or "")
        lines.append(f"- **{status}** [{title}]({url})")
        lines.append(f"  - kind: `{meta.get('kind')}`; method: `{method}`; chars: `{meta.get('content_chars')}`")
        if path:
            lines.append(f"  - cache: `{path}`")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch URL contents from Markdown or URL list into private/link_cache.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:
              python scripts/fetch_link_content.py --from-md content/游戏/引擎/Unity/Unity-内存与性能优化笔记.md
              python scripts/fetch_link_content.py --url https://example.com --refresh
            """
        ),
    )
    parser.add_argument("--from-md", type=Path, help="Read links from a Markdown file")
    parser.add_argument("--url", action="append", default=[], help="Fetch one URL; can be repeated")
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    parser.add_argument("--digest", type=Path, help="Write a Markdown digest")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--refresh", action="store_true", help="Ignore existing cache")
    args = parser.parse_args()

    items: list[dict[str, str]] = []
    if args.from_md:
        items.extend(extract_markdown_links(args.from_md))
    for url in args.url:
        items.append({"title": "", "url": normalize_url(url)})

    deduped: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in items:
        if item["url"] and item["url"] not in seen:
            seen.add(item["url"])
            deduped.append(item)

    if not deduped:
        print("No URLs found.", file=sys.stderr)
        return 1

    args.cache_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, object]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = [
            executor.submit(fetch_one, item, args.cache_dir, args.timeout, args.refresh)
            for item in deduped
        ]
        for future in concurrent.futures.as_completed(futures):
            meta = future.result()
            results.append(meta)
            status = "OK" if meta.get("ok") else "FAIL"
            print(f"[{status}] {meta.get('title')} <{meta.get('url')}> via {meta.get('method')}")

    results.sort(key=lambda item: str(item.get("url")))
    digest = args.digest or args.cache_dir / "digest.md"
    build_digest(results, digest)
    print(f"Digest written to {digest}")
    return 0 if any(item.get("ok") for item in results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
