#!/usr/bin/env python3
"""Audit external links referenced by Markdown notes under content/.

Features:
- scan all Markdown links from a target directory
- de-duplicate URLs while keeping backlink locations
- probe link health with HEAD, then GET fallback
- classify localhost / private / sensitive-style links separately
- write JSON and Markdown reports under private/link_audit/
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import re
import socket
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


MARKDOWN_LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^)\s]+)\)")
DEFAULT_TIMEOUT = 12
DEFAULT_WORKERS = 10
DEFAULT_OUTPUT_DIR = Path("private/link_audit")
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/136.0.0.0 Safari/537.36"
)
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
PRIVATE_HOST_PATTERNS = (
    "localhost",
    "127.0.0.1",
    ".local",
    ".internal",
    ".corp",
    ".lan",
)
SENSITIVE_PATH_HINTS = (
    "/login",
    "/signin",
    "/dashboard",
    "/admin",
    "/configure",
    "/settings",
    "/transactions",
    "/console",
    "/wiki/",
    "/docx/",
    "/base/",
)


@dataclass(slots=True)
class LinkRef:
    path: str
    line: int
    label: str


@dataclass(slots=True)
class AuditResult:
    url: str
    normalized_url: str
    host: str
    status: str
    category: str
    http_status: int | None = None
    method: str = ""
    final_url: str = ""
    error: str = ""
    refs: list[LinkRef] = field(default_factory=list)


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


def iter_markdown_files(root: Path) -> Iterable[Path]:
    yield from sorted(root.rglob("*.md"))


def parse_links(path: Path) -> list[tuple[str, LinkRef]]:
    text = path.read_text(encoding="utf-8")
    items: list[tuple[str, LinkRef]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for label, url in MARKDOWN_LINK_RE.findall(line):
            items.append(
                (
                    url,
                    LinkRef(path=str(path.as_posix()), line=lineno, label=label.strip()),
                )
            )
    return items


def classify_special(url: str) -> tuple[str, str]:
    parsed = urllib.parse.urlsplit(url)
    host = parsed.netloc.lower()
    if any(token in host for token in PRIVATE_HOST_PATTERNS):
        return "skip", "private_host"
    if host.startswith(("10.", "172.", "192.168.")):
        return "skip", "private_host"
    if any(hint in host for hint in ("larkoffice.com", "byteintl.net")):
        return "skip", "login_or_internal"
    if any(hint in parsed.path.lower() for hint in SENSITIVE_PATH_HINTS):
        return "review", "sensitive_path"
    return "", ""


def build_request(url: str, method: str) -> urllib.request.Request:
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
        method=method,
    )


def perform_request(url: str, timeout: int, method: str) -> tuple[int, str]:
    req = build_request(url, method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        status = getattr(resp, "status", None) or resp.getcode()
        final_url = resp.geturl()
        if method == "GET":
            _ = resp.read(1024)
        return int(status), final_url


def probe_url(url: str, timeout: int) -> tuple[str, int | None, str, str]:
    try:
        status_code, final_url = perform_request(url, timeout, "HEAD")
        return "ok" if status_code < 400 else "broken", status_code, "HEAD", final_url
    except urllib.error.HTTPError as exc:
        # Some sites reject HEAD with 4xx/5xx but succeed on GET, so always retry once.
        try:
            status_code, final_url = perform_request(url, timeout, "GET")
            return "ok" if status_code < 400 else "broken", status_code, "GET", final_url
        except urllib.error.HTTPError as get_exc:
            if get_exc.code in {401, 403}:
                return "auth", get_exc.code, "GET", get_exc.geturl() or url
            return "broken", get_exc.code, "GET", get_exc.geturl() or url
        except (urllib.error.URLError, TimeoutError, socket.timeout) as get_exc:
            if exc.code in {401, 403}:
                return "auth", exc.code, "HEAD", exc.geturl() or url
            return "error", None, "GET", str(get_exc)
        except Exception as get_exc:  # pragma: no cover - defensive fallback
            if exc.code in {401, 403}:
                return "auth", exc.code, "HEAD", exc.geturl() or url
            return "error", None, "GET", str(get_exc)
    except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
        return "error", None, "HEAD", str(exc)
    except Exception as exc:  # pragma: no cover - defensive fallback
        return "error", None, "HEAD", str(exc)


def audit_one(url: str, refs: list[LinkRef], timeout: int) -> AuditResult:
    normalized = normalize_url(url)
    parsed = urllib.parse.urlsplit(normalized)
    special_status, category = classify_special(normalized)
    if special_status:
        return AuditResult(
            url=url,
            normalized_url=normalized,
            host=parsed.netloc.lower(),
            status=special_status,
            category=category,
            refs=refs,
        )

    state, code, method, detail = probe_url(normalized, timeout)
    return AuditResult(
        url=url,
        normalized_url=normalized,
        host=parsed.netloc.lower(),
        status=state,
        category="public",
        http_status=code,
        method=method,
        final_url=detail if state != "error" else "",
        error=detail if state == "error" else "",
        refs=refs,
    )


def render_markdown(results: list[AuditResult], scanned_file_count: int) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_urls = len(results)
    counter = Counter(item.status for item in results)
    lines = [
        "---",
        "title: content 外链体检报告",
        "status: reviewed",
        "visibility: private",
        f"last_curated: {dt.date.today().isoformat()}",
        f"source_count: {total_urls}",
        "---",
        "",
        f"- 扫描时间：{now}",
        f"- 扫描目录：`content/`",
        f"- 扫描文件数：{scanned_file_count}",
        f"- 去重后外链数：{total_urls}",
        f"- `ok`：{counter.get('ok', 0)}",
        f"- `auth`：{counter.get('auth', 0)}",
        f"- `review`：{counter.get('review', 0)}",
        f"- `skip`：{counter.get('skip', 0)}",
        f"- `broken`：{counter.get('broken', 0)}",
        f"- `error`：{counter.get('error', 0)}",
        "",
    ]

    groups = {
        "broken": "## 失效链接",
        "error": "## 访问异常",
        "auth": "## 需要鉴权或被拒绝",
        "review": "## 需人工复核的敏感入口",
        "skip": "## 已跳过的私有/内网链接",
    }
    for status in ("broken", "error", "auth", "review", "skip"):
        bucket = [item for item in results if item.status == status]
        if not bucket:
            continue
        lines.extend([groups[status], ""])
        for item in bucket:
            refs = ", ".join(f"`{ref.path}:{ref.line}`" for ref in item.refs[:5])
            detail = item.error or item.final_url or item.category
            code = f" `{item.http_status}`" if item.http_status is not None else ""
            lines.append(f"- [{item.normalized_url}]({item.normalized_url}){code}：{detail}；位置：{refs}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit external links in Markdown notes.")
    parser.add_argument("--root", type=Path, default=Path("content"), help="Root directory to scan")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Report output directory")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Per-request timeout in seconds")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help="Concurrent workers")
    args = parser.parse_args()

    if not args.root.exists():
        print(f"Scan root not found: {args.root}", file=sys.stderr)
        return 2

    url_map: dict[str, list[LinkRef]] = defaultdict(list)
    scanned_files = list(iter_markdown_files(args.root))
    for path in scanned_files:
        for url, ref in parse_links(path):
            url_map[normalize_url(url)].append(ref)

    results: list[AuditResult] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        future_map = {
            pool.submit(audit_one, refs[0].label and normalize_url(raw) or normalize_url(raw), refs, args.timeout): key
            for key, refs in url_map.items()
            for raw in [key]
        }
        for future in concurrent.futures.as_completed(future_map):
            results.append(future.result())

    results.sort(key=lambda item: (item.status, item.host, item.normalized_url))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    json_path = args.output_dir / f"content-link-audit-{timestamp}.json"
    md_path = args.output_dir / f"content-link-audit-{timestamp}.md"

    payload = {
        "generated_at": dt.datetime.now().isoformat(),
        "scan_root": str(args.root.as_posix()),
        "file_count": len(scanned_files),
        "unique_url_count": len(results),
        "summary": Counter(item.status for item in results),
        "results": [
            {
                **asdict(item),
                "refs": [asdict(ref) for ref in item.refs],
            }
            for item in results
        ],
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(results, len(scanned_files)), encoding="utf-8")

    summary = Counter(item.status for item in results)
    print(f"files={len(scanned_files)} unique_urls={len(results)}")
    for key in ("ok", "auth", "review", "skip", "broken", "error"):
        print(f"{key}={summary.get(key, 0)}")
    print(f"markdown_report={md_path.as_posix()}")
    print(f"json_report={json_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
