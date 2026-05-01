"""Second pass: re-classify remaining entries in 元数据/未分类长尾.md
with refined host/title rules. Append matched entries to target files,
keep only truly leftover in the unsorted file.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
UNSORTED = CONTENT / "元数据" / "未分类长尾.md"

ENTRY_RE = re.compile(r"^- (?:\[([^\]]+)\]\((https?://[^)]+)\)|<(https?://[^>]+)>)")


def parse_entries(text: str) -> list[tuple[str, str, str]]:
    """Return list of (url, title, raw_line)."""
    out = []
    for line in text.splitlines():
        m = ENTRY_RE.match(line)
        if not m:
            continue
        title = m.group(1) or ""
        url = m.group(2) or m.group(3)
        out.append((url, title, line))
    return out


# Refined / additional rules for the second pass
INTERNAL_CORP = (
    "xgjoy.games", "xgjoy.org", "xgjoy.com",
    "muyinetwork.com", "longqs.muyinetwork", "patch-prod",
    "kubernetes-dashboard.xgjoy", "platform01.xgjoy",
    "tapd.cn",
)

AI_HOSTS_2 = ("cursor.com", "chatgpt.com", "perplexity.ai", "anthropic.com",
              "x.ai", "you.com", "phind.com", "unite.ai", "aihub.cn",
              "agi-eval.cn", "huggingface.co")

UNITY_HOSTS_2 = (
    "zh.esotericsoftware.com", "esotericsoftware.com", "spine-runtimes",
    "et-framework.cn", "xuanyusong.com", "luban.doc.code-philosophy",
    "yooasset.com", "yooaios", "tonytang1990.github.io",
    "lfzxb.top", "odininspector.com", "moremountains.com",
    "withpinbox.com", "hybridclr.cn", "feel-docs",
    "nice-vibrations", "datable.cn",
    "unity.cn", "docs.unity.cn", "opsive.com", "xasset.cc",
    "hybridclr.doc.code-philosophy", "gafferongames.com",
)

GAME_MOBILE_2 = (
    "crashsight.qq.com", "crashsight.wetest.net", "mob.com",
    "dun.163.com", "harmonyos.com", "developer.huawei.com",
    "ldmnq.com", "patch-prod.longqs", "lqs.muyinetwork",
)

CS_REF_2 = (
    "dotnet.microsoft.com", "devblogs.microsoft.com",
    "mvnrepository.com", "nuget.org",
)

VIDEO_2 = ("time.geekbang.org", "bilibili.com")

BLOG_2 = (
    "mp.weixin.qq.com", "reddit.com", "zhihu.com",
    "cloud.tencent.com", "blog.51cto.com", "blog.lujun.co",
    "www.bookstack.cn", "weread.qq.com", "midwayjs.org",
    "technology.riotgames.com",
    "segmentfault.com", "xiaolincoding.com", "yangwc.com",
    "xiexuewu.github.io", "yank-note.com",
    "changkun.de", "gwb.tencent.com",
    "blog.lupin.com", "zoucz.com",
)

TOOLS_2 = (
    "voidtools.com", "kubernetes.io", "docker.com",
    "alibabacloud.com", "jetbrains.com/help",
    "marketplace.visualstudio.com", "nginx.org",
    "adoptium.net", "gradle.org", "plantuml.com",
    "mermaidchart.com", "lizhi.shop", "withpinbox.com",
    "ip138.com", "ossbrowser",
    "developer.aliyun.com", "wanwang.aliyun.com",
    "translate.google.com", "support.microsoft.com",
    "gitee.com", "gitlab.com", "runoob.com",
    "openphone.com", "dropbox.com", "clashios.com",
)

DOC_HUB_HOSTS = ("readthedocs", "developer.mozilla.org")


def classify(url: str, title: str) -> str:
    u = url.lower()
    t = title.lower()

    # Already-known dead patterns we may have missed in pass 1
    if "wechat_redirect" in u and "weixin" in u:
        return "blacklist"
    if title.startswith("403 Forbidden") or "Page not found" in title:
        return "blacklist"

    if any(h in u for h in INTERNAL_CORP):
        return "workspace-tail"

    if any(h in u for h in AI_HOSTS_2):
        return "ai-tail"

    if any(h in u for h in UNITY_HOSTS_2):
        return "unity-tail"

    if any(h in u for h in GAME_MOBILE_2):
        return "game-mobile-tail"

    if any(h in u for h in CS_REF_2):
        return "cs-ref-tail"

    if any(h in u for h in VIDEO_2):
        return "video-tail"

    if any(h in u for h in TOOLS_2):
        return "tools-tail"

    if any(h in u for h in BLOG_2):
        return "blog-tail"

    return "unsorted"


TARGETS = {
    "workspace-tail": "工作台/工作台与控制台入口.md",
    "ai-tail": "AI/AI-长尾.md",
    "unity-tail": "游戏/Unity-长尾.md",
    "game-mobile-tail": "游戏/移动端接入与平台问题.md",
    "cs-ref-tail": "计算机/C-CSharp-CPP参考.md",
    "video-tail": "资讯/视频与课程.md",
    "tools-tail": "工具/在线工具与协作.md",
    "blog-tail": "资讯/技术博客-长尾.md",
    "blacklist": "元数据/失效黑名单.md",
}


def main() -> int:
    text = UNSORTED.read_text(encoding="utf-8")
    entries = parse_entries(text)

    print(f"Loaded {len(entries)} entries from 未分类长尾.md\n")

    buckets: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for url, title, raw in entries:
        bucket = classify(url, title)
        buckets[bucket].append((url, title, raw))

    # For each non-unsorted bucket, append to target file under "二次分桶"
    for bucket, items in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        if bucket == "unsorted":
            continue
        target = CONTENT / TARGETS[bucket]
        if not target.exists():
            print(f"  WARN: target {TARGETS[bucket]} missing, skipping {len(items)} entries")
            continue
        contents = target.read_text(encoding="utf-8").rstrip()
        appendix = ["", "## 长尾二次分桶", ""]
        for _, _, raw in items:
            appendix.append(raw)
        target.write_text(contents + "\n" + "\n".join(appendix) + "\n", encoding="utf-8")
        print(f"  [{bucket:<18}] {len(items):>4} -> {TARGETS[bucket]}")

    # Rewrite 未分类长尾.md with only the truly unsorted
    leftover = buckets.get("unsorted", [])
    fm = (
        "---\n"
        "title: 未分类长尾\n"
        "tags:\n"
        "  - 元数据\n"
        "  - 长尾\n"
        "  - 未分类\n"
        "---\n\n"
        "经过两轮分类后仍未归桶的长尾。每条都需要人工判断主题或确认作废。\n\n"
    )
    body = "\n".join(raw for _, _, raw in leftover)
    UNSORTED.write_text(fm + body + "\n", encoding="utf-8")
    print(f"\n  [{'unsorted':<18}] {len(leftover):>4} -> 元数据/未分类长尾.md (rewritten)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
