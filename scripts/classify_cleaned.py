"""Classify cleaned.txt long-tail URLs into per-topic markdown files.

Reads:
- content/元数据/cleaned.txt (URL | TITLE per line, 1703 lines)
- content/元数据/selected.txt (already-curated URLs, skip these)

Bucket each remaining URL by host pattern + title keywords, then append a
"## 长尾（未审核）" section to the target markdown (or create a new long-tail file).
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
CLEANED = CONTENT / "元数据" / "cleaned.txt"
SELECTED = CONTENT / "元数据" / "selected.txt"


def parse_line(line: str) -> tuple[str, str] | None:
    line = line.strip().lstrip("﻿")
    if not line or not line.startswith(("http://", "https://")):
        return None
    if " | " in line:
        url, title = line.split(" | ", 1)
    else:
        url, title = line, ""
    return url.strip(), title.strip()


def load_selected_urls() -> set[str]:
    urls: set[str] = set()
    for raw in SELECTED.read_text(encoding="utf-8").splitlines():
        parsed = parse_line(raw)
        if parsed:
            urls.add(parsed[0])
    return urls


def is_blacklist(url: str, title: str) -> bool:
    t = title.lower()
    u = url.lower()
    if any(p in u for p in [
        "google.com/search", "google.com.hk/search", "baidu.com/s?",
        "bing.com/search", "search.bilibili.com", "bytetech.info/search",
    ]):
        return True
    if "chatgpt.com/c/" in u or "gemini.google.com/app/" in u:
        return True
    if "mail.google.com" in u or "mail.163.com" in u:
        return True
    if "wechat_redirect" in u and "weixin" in u:
        return True
    if any(t.startswith(s) for s in ["403 forbidden", "404", "page not found", "页面找不到"]):
        return True
    if "账号已迁移" in title or "Error From Ingress" in title or "域名不可访问" in title:
        return True
    return False


def is_workspace(url: str, title: str) -> bool:
    u = url.lower()
    if re.search(r"https?://(?:10|192)\.[\d\.]+:\d+", u):
        return True
    if any(p in u for p in [
        "console.firebase.google.com", "console.cloud.google.com",
        "play.google.com/console", "appstoreconnect.apple.com",
        "developer.apple.com/account",
    ]):
        return True
    if "jenkins" in u and ":808" in u:
        return True
    return False


def is_internal(url: str, title: str) -> bool:
    u = url.lower()
    if any(d in u for d in [
        "larkoffice.com", "feishu.cn", "feishuapp.cn", "feishu.com",
        "moonton.feishu", "bytedance.larkoffice",
        "project.feishu.cn", "open.feishu.cn",
    ]):
        return True
    return False


AI_HOSTS = (
    "openai.com", "platform.openai.com", "anthropic.com", "claude.com", "claude.ai",
    "deepseek.com", "kimi.com", "doubao.com", "yiyan.baidu.com", "qianwen.com",
    "yuanbao.tencent.com", "hunyuan.tencent.com", "xinghuo.xfyun.cn",
    "gemini.google.com", "aistudio.google.com", "ai.google.dev",
    "copilot.microsoft.com", "github.com/features/copilot", "qwen.ai",
    "civitai.com", "ollama.com", "dify.ai", "agent.minimaxi", "agent.minimax",
    "aibase", "ai-bot.cn", "trae.ai", "trae.cn", "minimaxi.com",
    "aicodewith", "chatgptzhinan", "zhida.zhihu.com", "huggingface.co",
    "fornax.bytedance", "aime.bytedance", "mira.byteintl",
)

UNITY_HOSTS = (
    "unity.com", "unity3d.com", "developer.unity", "assetstore.unity",
    "docs.unity3d", "discussions.unity", "blog.unity",
    "uwa4d.com", "u3dchina.com", "fmod.com",
)

UNITY_REPO_KEYWORDS = (
    "unity", "spine", "fairygui", "cinemachine", "cysharp", "hybridclr",
    "yooasset", "luban", "ugui", "et-framework", "etetet", "tuyoogame",
    "framepack", "shader", "uxml", "uguid", "addressables", "rosalina",
    "obsr-",
)

LOCKSTEP_KEYWORDS = ("lockstep", "frame sync", "帧同步", "behavior tree", "ai 行为树", "behaviortree")

UNREAL_HOSTS = (
    "unrealengine.com", "epicgames.com", "dev.epicgames.com",
    "unrealcommunity.wiki",
)

GAME_MOBILE_HOSTS = (
    "firebase.google.com", "firebase.google.cn", "developer.android.com",
    "developer.apple.com", "fmod.com", "toponad.net", "toponteam",
    "googleads-mobile-unity", "googleads/googleads-mobile",
)

CS_REF_HOSTS = (
    "cppreference.com", "isocpp.org", "google.github.io/styleguide",
    "zh-google-styleguide", "cplusplus.com", "cpp.hotexamples",
)

CS_REF_PATHS = ("learn.microsoft.com/zh-cn/dotnet", "learn.microsoft.com/en-us/dotnet",
                "learn.microsoft.com/zh-cn/cpp", "learn.microsoft.com/en-us/cpp",
                "learn.microsoft.com/zh-cn/csharp", "learn.microsoft.com/en-us/csharp")

BLOG_HOSTS = (
    "csdn.net", "cnblogs.com", "jianshu.com", "juejin.cn", "zhuanlan.zhihu.com",
    "zhihu.com/question", "infoq.com", "hackernoon.com", "stackoverflow.com",
    "stackexchange.com", "yuque.com", "ruanyifeng.com", "bytetech.info/articles",
    "blog.codingnow.com", "imzlp.com", "luzexi.com", "vishalchovatiya.com",
    "aaronbos.dev", "code-corner.dev", "dev.to", "medium.com",
    "qiankanglai.me", "lvmingbei.hatenablog", "tsubakit1.hateblo",
    "fredxxx123.wordpress", "lifan.tech",
)

VIDEO_HOSTS = (
    "bilibili.com/video", "bilibili.com/v/", "space.bilibili",
    "youtube.com/watch", "youtube.com/@", "udemy.com", "sikiedu.com",
    "linecg.com", "taikr.com", "boxueio.com", "yxtown.com",
    "bycwedu.com", "ke.qq.com", "freegeektime.com", "imooc.com",
    "patreon.com", "aboutcg.org", "edu.csdn.net", "kaiwu.lagou.com",
    "edu.manew.com", "w3cschool.cn",
)

TOOLS_HOSTS = (
    "regex101.com", "easings.net", "diagrams.net", "naotu.baidu",
    "apifox.com", "cpp.sh", "coliru.stacked", "godbolt.org",
    "cppinsights.io", "jsrun.net", "xlcompare.com", "iloveimg.com",
    "tool.chinaz", "iamwawa", "jyshare.com", "halove.net", "mubu.com",
    "mindline.cn", "gitmind.com", "gist.github.com",
    "banlikanban.com", "tampermonkey.net", "it-tools.tech",
    "sm.ms", "cybermagicsec", "colorhexa.com", "cv.ftqq.com",
)

PROXY_HOSTS = (
    "clashfor.win", "clashverge.dev", "clashforandroid", "tampermonkey",
    "wallmama.com", "sms-activate.org", "dingtone.me",
    "dg5.biz", "csjc.win", "ikuuu",
)

GREY_HOSTS = (
    "shikey.com", "z-lib", "magazinelib.com", "yabook.org", "sobooks",
    "shuge.org", "zuo.cc", "52pojie.cn", "clcat.net", "xjyxi.com",
    "2cyshare.com", "galgamezz.cc", "usersdrive.com",
    "t.me/s/quanwangzy", "47.52.5.90", "ad.rapidhits", "twblogs.net",
    "geekch.art", "fantsida", "leaaiv", "910laoshi", "yxkfw",
    "narkii.com", "doggygo", "hotscripts", "msi.cn", "coolermaster.com",
    "td.sx.gov", "kq.gov", "thispointer.com", "secrss.com",
)

# Output buckets and their target markdown files
TARGETS: dict[str, dict] = {
    "ai-tail": {"file": "AI/AI-长尾.md", "title": "AI 长尾", "tags": ["ai-coding", "长尾", "未审核"]},
    "unity-tail": {"file": "游戏/Unity-长尾.md", "title": "Unity 长尾仓库", "tags": ["unity", "游戏开发", "长尾", "未审核"]},
    "unreal-tail": {"file": "游戏/Unreal-长尾.md", "title": "Unreal 长尾", "tags": ["unreal-engine", "长尾", "未审核"]},
    "framesync-tail": {"file": "游戏/帧同步与游戏AI.md", "section": "## 长尾（未审核）", "append": True, "tags_add": ["长尾"]},
    "game-mobile-tail": {"file": "游戏/移动端接入与平台问题.md", "section": "## 长尾（未审核）", "append": True, "tags_add": ["长尾"]},
    "cs-ref-tail": {"file": "计算机/C-CSharp-CPP参考.md", "section": "## 长尾（未审核）", "append": True, "tags_add": ["长尾"]},
    "github-tail": {"file": "计算机/GitHub-长尾.md", "title": "GitHub 长尾仓库", "tags": ["github", "长尾", "未审核"]},
    "blog-tail": {"file": "资讯/技术博客-长尾.md", "title": "技术博客 长尾", "tags": ["博客", "长尾", "未审核"]},
    "video-tail": {"file": "资讯/视频与课程.md", "section": "## 长尾（未审核）", "append": True, "tags_add": ["长尾"]},
    "tools-tail": {"file": "工具/在线工具与协作.md", "section": "## 长尾（未审核）", "append": True, "tags_add": ["长尾"]},
    "proxy-tail": {"file": "工具/网络与代理.md", "section": "## 长尾（未审核）", "append": True, "tags_add": ["长尾"]},
    "workspace-tail": {"file": "工作台/工作台与控制台入口.md", "section": "## 六、长尾（未审核）", "append": True, "tags_add": ["长尾"]},
    "internal-tail": {"file": "工作台/内部长期项目页.md", "section": "## 长尾（未审核）", "append": True, "tags_add": ["长尾"]},
    "blacklist": {"file": "元数据/失效黑名单.md", "section": "## 十二、长尾扫出的失效（未审核）", "append": True, "tags_add": []},
    "unsorted": {"file": "元数据/未分类长尾.md", "title": "未分类长尾", "tags": ["元数据", "长尾", "未分类"]},
}


def host_match(url: str, hosts: tuple[str, ...]) -> bool:
    return any(h in url.lower() for h in hosts)


def classify(url: str, title: str) -> str:
    u = url.lower()
    t = title.lower()

    if is_blacklist(url, title):
        return "blacklist"
    if is_internal(url, title):
        return "internal-tail"
    if is_workspace(url, title):
        return "workspace-tail"

    if host_match(u, AI_HOSTS):
        return "ai-tail"

    if host_match(u, UNREAL_HOSTS):
        return "unreal-tail"

    if host_match(u, UNITY_HOSTS):
        return "unity-tail"

    # GitHub: classify by repo title keywords
    if "github.com/" in u:
        if any(k in t for k in LOCKSTEP_KEYWORDS):
            return "framesync-tail"
        if any(k in t for k in UNITY_REPO_KEYWORDS):
            return "unity-tail"
        if any(k in t for k in ("ai", "llm", "agent", "gpt", "chatbot", "claude", "openai")):
            return "ai-tail"
        if "unreal" in t or "ue4" in t or "ue5" in t:
            return "unreal-tail"
        return "github-tail"

    if any(k in t for k in LOCKSTEP_KEYWORDS):
        return "framesync-tail"

    if host_match(u, GAME_MOBILE_HOSTS):
        return "game-mobile-tail"

    if host_match(u, CS_REF_HOSTS):
        return "cs-ref-tail"
    if any(p in u for p in CS_REF_PATHS):
        return "cs-ref-tail"

    if host_match(u, VIDEO_HOSTS):
        return "video-tail"

    if host_match(u, BLOG_HOSTS):
        return "blog-tail"

    if host_match(u, PROXY_HOSTS):
        return "proxy-tail"

    if host_match(u, TOOLS_HOSTS):
        return "tools-tail"

    if host_match(u, GREY_HOSTS):
        return "blacklist"

    return "unsorted"


def format_entry(url: str, title: str) -> str:
    if title:
        # truncate very long titles
        if len(title) > 200:
            title = title[:197] + "..."
        return f"- [{title}]({url})"
    return f"- <{url}>"


def write_new_file(path: Path, title: str, tags: list[str], entries: list[str]) -> None:
    fm = ["---", f"title: {title}", "tags:"]
    for tg in tags:
        fm.append(f"  - {tg}")
    fm.append("---")
    body = ["", f"自动从 `元数据/cleaned.txt` 长尾分类入桶；未审核，按需提升到主分类。", "", *entries, ""]
    path.write_text("\n".join(fm + body), encoding="utf-8")


def append_section(path: Path, section_header: str, tags_add: list[str], entries: list[str]) -> None:
    text = path.read_text(encoding="utf-8")

    # Add new tags to frontmatter if missing
    if tags_add:
        fm_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if fm_match:
            fm_body = fm_match.group(1)
            for tg in tags_add:
                if f"  - {tg}" not in fm_body and f"- {tg}" not in fm_body:
                    fm_body += f"\n  - {tg}"
            text = "---\n" + fm_body + "\n---\n" + text[fm_match.end():]

    # Append section
    appendix = "\n" + section_header + "\n\n" + "\n".join(entries) + "\n"
    text = text.rstrip() + "\n" + appendix
    path.write_text(text, encoding="utf-8")


def main() -> int:
    selected = load_selected_urls()
    print(f"Loaded {len(selected)} selected URLs to skip.\n")

    buckets: dict[str, list[tuple[str, str]]] = defaultdict(list)
    skipped = 0
    total = 0

    for raw in CLEANED.read_text(encoding="utf-8").splitlines():
        parsed = parse_line(raw)
        if not parsed:
            continue
        total += 1
        url, title = parsed
        if url in selected:
            skipped += 1
            continue
        bucket = classify(url, title)
        buckets[bucket].append((url, title))

    print(f"Parsed {total} URLs in cleaned.txt.")
    print(f"Skipped {skipped} already in selected.txt.")
    print(f"Remaining {sum(len(v) for v in buckets.values())} routed:\n")

    # Write each bucket
    for bucket_id, entries in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        target = TARGETS[bucket_id]
        path = CONTENT / target["file"]
        formatted = [format_entry(u, t) for u, t in entries]

        if target.get("append"):
            append_section(
                path,
                target["section"],
                target.get("tags_add", []),
                formatted,
            )
            action = "appended"
        else:
            write_new_file(
                path,
                target["title"],
                target["tags"],
                formatted,
            )
            action = "created"

        print(f"  [{bucket_id:<18}] {len(entries):>4} -> {target['file']} ({action})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
