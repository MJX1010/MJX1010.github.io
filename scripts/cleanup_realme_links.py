from __future__ import annotations

import re
import urllib.parse
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
PRIVATE = CONTENT / "private" / "metadata"

BLACKLIST_FILE = PRIVATE / "失效黑名单.md"
PRIVATE_ARCHIVE_FILE = PRIVATE / "private-account-links-archive.md"
UNSORTED_ARCHIVE_FILE = PRIVATE / "未分类素材链接归档.md"
UNSORTED_POOL_FILE = PRIVATE / "未分类素材池.md"
AUTO_BLACKLIST_HEADING = "## 十三、自动清理补充"

LINK_RE = re.compile(r"^- (?:\[([^\]]+)\]\((https?://[^)]+)\)|<(https?://[^>]+)>)")
FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n?", re.S)

TRACKING_PARAMS = {
    "spm_id_from",
    "vd_source",
    "buvid",
    "share_from",
    "share_medium",
    "share_plat",
    "share_session_id",
    "share_source",
    "share_tag",
    "timestamp",
    "unique_k",
    "from_spmid",
    "_tk",
    "di",
    "scene",
    "source_id",
    "from_source",
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
}

PRIVATE_HOST_MARKERS = (
    "feishu.cn",
    "feishuapp.cn",
    "larkoffice.com",
    "project.feishu.cn",
    "open.feishu.cn",
    "console.firebase.google.com",
    "console.cloud.google.com",
    "play.google.com/console",
    "developer.apple.com/account",
    "appstoreconnect.apple.com",
    "my.openphone.com",
    "dropbox.com/home",
    "tapd.cn",
    "bytedance.larkoffice.com",
    "moonton.feishu.cn",
    "flowgame.feishu.cn",
    "lib9kmxvq7k.feishu.cn",
    "elearning.feishu.cn",
    "mygeektime.anyfun.tech",
)

PRIVATE_PATH_MARKERS = (
    "/login",
    "/dashboard",
    "/onboarding/verify",
    "/account/api-keys",
    "/api-keys",
    "/app/projects/",
    "/drive/me/",
    "/drive/shared/",
)

BLACKLIST_HOST_MARKERS = (
    "ikuuu",
    "trello.com/auroregame/home",
    "shikey.com",
    "2cyshare.com",
    "xjyxi.com",
    "galgamezz.cc",
    "usersdrive.com",
    "clcat.net",
    "52pojie.cn",
    "dg5.biz",
    "csjc.win",
    "xn--30rs3bu7r87f.com",
    "jetbra.in",
    "psdly.to",
    "dllme.com",
    "loveota.com",
    "fileaxa.com",
    "dg6.im",
)

BLACKLIST_TITLE_MARKERS = (
    "403 forbidden",
    "404",
    "page not found",
    "域名不可访问",
    "错误",
    "账号已迁移",
    "访客不能直接访问",
)

AI_HOSTS = (
    "openai.com",
    "anthropic.com",
    "claude.ai",
    "claude.com",
    "trae.ai",
    "trae.cn",
    "deepseek.com",
    "dify.ai",
    "civitai.com",
    "ollama.com",
    "ai-bot.cn",
    "aibase.com",
    "aicodewith.com",
    "x.ai",
    "huggingface.co",
    "gemini.google.com",
    "aistudio.google.com",
    "copilot.microsoft.com",
    "github.com/features/copilot",
    "chatgpt.com",
    "openrouter.ai",
    "volcengine.com",
)

UNITY_HOSTS = (
    "unity.com",
    "unity3d.com",
    "docs.unity3d.com",
    "docs.unity.cn",
    "assetstore.unity.com",
    "uwa4d.com",
    "u3dchina.com",
    "fmod.com",
    "datable.cn",
    "hybridclr.cn",
    "yooasset.com",
)

UNREAL_HOSTS = (
    "unrealengine.com",
    "epicgames.com",
    "dev.epicgames.com",
)

VIDEO_HOSTS = (
    "bilibili.com",
    "youtube.com",
    "udemy.com",
    "sikiedu.com",
    "yxtown.com",
    "boxueio.com",
    "linecg.com",
    "taikr.com",
    "ke.qq.com",
    "aboutcg.org",
    "freegeektime.com",
    "time.geekbang.org",
)

BLOG_HOSTS = (
    "csdn.net",
    "cnblogs.com",
    "zhihu.com",
    "juejin.cn",
    "yuque.com",
    "ruanyifeng.com",
    "blog.codingnow.com",
    "imzlp.com",
    "luzexi.com",
    "aaronbos.dev",
    "code-corner.dev",
    "dev.to",
    "reddit.com",
    "news.ycombinator.com",
    "linux.do",
    "technology.riotgames.com",
    "mp.weixin.qq.com",
    "xiaolincoding.com",
    "jacksondunstan.com",
    "ericlippert.com",
    "andrewlock.net",
    "blog.lindexi.com",
    "blog.walterlv.com",
    "albahari.com",
    "zhangxinxu.com",
    "gohugo.io",
    "gameprogrammingpatterns.com",
)

TOOLS_HOSTS = (
    "godbolt.org",
    "gcc.godbolt.org",
    "coliru.stacked-crooked.com",
    "regex101.com",
    "colorhexa.com",
    "iloveimg.com",
    "mindline.cn",
    "banlikanban.com",
    "it-tools.tech",
    "iamwawa.cn",
    "tool.chinaz.com",
    "xlcompare.com",
    "cv.ftqq.com",
    "readest.com",
    "cpp.sh",
    "cppinsights.io",
    "jsrun.net",
    "easings.net",
    "app.diagrams.net",
    "gitmind.com",
    "cybermagicsec.github.io",
    "halove.net",
    "marketplace.visualstudio.com",
    "plantuml.com",
    "kubernetes.io",
    "docker.com",
    "nginx.org",
    "runoob.com",
    "developer.aliyun.com",
    "alibabacloud.com",
    "translate.google.com",
    "voidtools.com",
    "devtoys.app",
)

PROXY_HOSTS = (
    "clashios.com",
    "clashfor.win",
    "clashverge.dev",
    "wallmama.com",
)

CS_REF_HOSTS = (
    "cppreference.com",
    "cplusplus.com",
    "learn.microsoft.com",
    "referencesource.microsoft.com",
    "changkun.de",
    "newtonsoft.com",
    "benchmarkdotnet.org",
    "dotnetfiddle.net",
    "dotnet.microsoft.com",
    "devblogs.microsoft.com",
    "docs.python.org",
    "learn.microsoft.com",
)

TARGET_FILES = {
    "ai": CONTENT / "AI" / "AI工具与导航.md",
    "unity": CONTENT / "游戏" / "Unity-框架与工具.md",
    "unreal": CONTENT / "游戏" / "Unreal-Engine.md",
    "framesync": CONTENT / "游戏" / "帧同步与游戏AI.md",
    "mobile": CONTENT / "游戏" / "移动端接入与平台问题.md",
    "video": CONTENT / "资讯" / "视频与课程.md",
    "blog": CONTENT / "资讯" / "技术博客与社区.md",
    "tools": CONTENT / "工具" / "在线工具与协作.md",
    "proxy": CONTENT / "工具" / "网络与代理.md",
    "csref": CONTENT / "计算机" / "C-CSharp-CPP参考.md",
    "platform": CONTENT / "计算机" / "平台与规范.md",
}


def parse_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^title:\s*(.+)$", text, re.M)
    return match.group(1).strip() if match else path.stem


def parse_link_line(line: str) -> tuple[str, str] | None:
    match = LINK_RE.match(line.strip())
    if not match:
        return None
    title = (match.group(1) or "").strip()
    url = (match.group(2) or match.group(3) or "").strip()
    return title, url


def format_link(title: str, url: str) -> str:
    return f"- [{title}]({url})" if title else f"- <{url}>"


def normalize_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url.strip())
    query_items = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    filtered = []
    for key, value in query_items:
        lower_key = key.lower()
        if lower_key in TRACKING_PARAMS or lower_key.startswith("utm_"):
            continue
        filtered.append((key, value))
    query = urllib.parse.urlencode(filtered, doseq=True)
    fragment = ""
    cleaned = parsed._replace(query=query, fragment=fragment)
    return urllib.parse.urlunsplit(cleaned)


def load_existing_urls(path: Path) -> set[str]:
    urls: set[str] = set()
    if not path.exists():
        return urls
    for line in path.read_text(encoding="utf-8").splitlines():
        parsed = parse_link_line(line)
        if parsed:
            _, url = parsed
            urls.add(normalize_url(url))
    return urls


def is_blacklist(url: str, title: str) -> bool:
    lowered_url = url.lower()
    lowered_title = title.lower()
    if any(marker in lowered_url for marker in BLACKLIST_HOST_MARKERS):
        return True
    if "gift card" in lowered_title or "信用卡生成器" in title:
        return True
    if any(marker in lowered_title for marker in BLACKLIST_TITLE_MARKERS):
        return True
    return False


def is_private(url: str, title: str) -> bool:
    lowered_url = url.lower()
    lowered_title = title.lower()
    if re.search(r"https?://(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?", lowered_url):
        return True
    if any(marker in lowered_url for marker in PRIVATE_HOST_MARKERS):
        return True
    if any(marker in lowered_url for marker in PRIVATE_PATH_MARKERS):
        return True
    if lowered_url.startswith("https://x.com/home") or lowered_url.startswith("http://x.com/home"):
        return True
    if "note.wiz.cn/wapp/recent" in lowered_url:
        return True
    if " api key" in lowered_title or "dashboard" in lowered_title or "登录" in lowered_title:
        return True
    return False


def classify_unsorted(url: str, title: str) -> str:
    lowered_url = url.lower()
    lowered_title = title.lower()
    if is_blacklist(url, title):
        return "blacklist"
    if is_private(url, title):
        return "private"
    if any(marker in lowered_url for marker in UNREAL_HOSTS):
        return "unreal"
    if any(marker in lowered_url for marker in UNITY_HOSTS):
        return "unity"
    if any(marker in lowered_url for marker in AI_HOSTS):
        return "ai"
    if any(marker in lowered_url for marker in VIDEO_HOSTS):
        return "video"
    if any(marker in lowered_url for marker in BLOG_HOSTS):
        return "blog"
    if any(marker in lowered_url for marker in TOOLS_HOSTS):
        return "tools"
    if any(marker in lowered_url for marker in PROXY_HOSTS):
        return "proxy"
    if any(marker in lowered_url for marker in CS_REF_HOSTS):
        return "csref"
    if any(
        keyword in lowered_title
        for keyword in (
            "android",
            "ios",
            "exportoptions.plist",
            "apple id",
            "google play",
            "短信",
            "短信接收",
        )
    ):
        return "mobile"
    if any(
        keyword in lowered_title
        for keyword in (
            "帧同步",
            "lockstep",
            "behavior tree",
            "behaviour tree",
            "multithreaded_rendering",
        )
    ):
        return "framesync"
    if any(
        keyword in lowered_title
        for keyword in (
            "unity",
            "ugui",
            "fmod",
            "shader",
            "hybridclr",
            "luban",
            "yooasset",
            "xasset",
            "et框架",
            "et framework",
            "il2cpp",
            "dotween",
            "ilruntime",
            "moonsharp",
            "wwise",
            "astc",
            "cocos creator",
            "odin inspector",
            "editorwindow",
            "source generator in rider",
        )
    ):
        return "unity"
    if any(
        keyword in lowered_title
        for keyword in (
            "c#",
            ".net",
            "source generator",
            "thread",
            "readonly",
            "params keyword",
            "decimal in c#",
            "benchmarkdotnet",
            "locks and exceptions",
            "rpc",
            "regex",
            "assembly",
            "程序集",
            "多线程",
            "构造函数",
            "python modules",
        )
    ):
        return "csref"
    if any(
        keyword in lowered_title
        for keyword in (
            "joplin",
            "localsend",
            "tortoisegit",
            "chocolatey",
            "paint",
            "plantuml",
            "uml",
            "file compare",
            "excel",
            "简历",
            "面试",
        )
    ):
        return "tools"
    if any(
        keyword in lowered_title
        for keyword in (
            "机场",
            "clash",
            "proxy",
            "远程",
            "串流",
            "gift card",
            "apple id",
        )
    ):
        return "proxy"
    if "github.com/" in lowered_url:
        if any(keyword in lowered_title for keyword in ("unity", "spine", "cinemachine", "hybridclr", "luban", "yooasset", "unirx", "unitask")):
            return "unity"
        if any(keyword in lowered_title for keyword in ("frame sync", "帧同步", "lockstep", "behavior tree", "behaviour tree")):
            return "framesync"
        if any(keyword in lowered_title for keyword in ("agent", "ai", "llm", "gpt", "claude", "gemini")):
            return "ai"
        if "unreal" in lowered_title or "ue4" in lowered_title or "ue5" in lowered_title:
            return "unreal"
        return "platform"
    if any(keyword in lowered_title for keyword in ("android", "ios", "firebase", "crashlytics", "admob", "google pay")):
        return "mobile"
    if any(keyword in lowered_title for keyword in ("帧同步", "lockstep", "行为树", "aoi", "kcp")):
        return "framesync"
    if any(keyword in lowered_title for keyword in ("unity", "ugui", "fmod", "shader", "hybridclr", "luban", "yooasset", "xasset", "et框架", "et framework")):
        return "unity"
    return "unsorted"


def append_entries_to_note(path: Path, heading: str, entries: list[tuple[str, str]]) -> int:
    if not entries:
        return 0
    text = path.read_text(encoding="utf-8")
    existing = {normalize_url(url) for _, url in extract_links(text)}
    unique_entries = []
    for title, url in entries:
        normalized = normalize_url(url)
        if normalized in existing:
            continue
        existing.add(normalized)
        unique_entries.append((title, normalized))
    if not unique_entries:
        return 0

    lines = text.rstrip().splitlines()
    output = []
    in_ref = False
    heading_written = False
    for line in lines:
        output.append(line)
        if line.strip() == "## 参考链接":
            in_ref = True
            continue
        if in_ref and line.startswith("## ") and line.strip() != "## 参考链接":
            if not heading_written:
                output.extend(["", heading, ""])
                output.extend(format_link(title, url) for title, url in unique_entries)
                heading_written = True
            in_ref = False
    if "## 参考链接" not in text:
        output.extend(["", "## 参考链接", "", heading, ""])
        output.extend(format_link(title, url) for title, url in unique_entries)
    elif not heading_written:
        output.extend(["", heading, ""])
        output.extend(format_link(title, url) for title, url in unique_entries)
    path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
    return len(unique_entries)


def extract_links(text: str) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    for line in text.splitlines():
        parsed = parse_link_line(line)
        if parsed:
            links.append(parsed)
    return links


def process_public_notes() -> tuple[dict[str, list[tuple[str, str]]], dict[str, list[tuple[str, str]]], int]:
    removed_private: dict[str, list[tuple[str, str]]] = defaultdict(list)
    removed_dead: dict[str, list[tuple[str, str]]] = defaultdict(list)
    total_removed = 0
    for path in sorted(CONTENT.rglob("*.md")):
        if "private" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if "## 参考链接" not in text:
            continue
        title = parse_title(path)
        lines = text.splitlines()
        output = []
        in_ref = False
        seen: set[str] = set()
        file_changed = False
        for line in lines:
            stripped = line.strip()
            if stripped == "## 参考链接":
                in_ref = True
                output.append(line)
                continue
            if in_ref and stripped.startswith("## ") and stripped != "## 参考链接":
                in_ref = False
            parsed = parse_link_line(line)
            if in_ref and parsed:
                link_title, url = parsed
                normalized = normalize_url(url)
                if is_blacklist(normalized, link_title):
                    removed_dead[title].append((link_title, normalized))
                    total_removed += 1
                    file_changed = True
                    continue
                if is_private(normalized, link_title):
                    removed_private[title].append((link_title, normalized))
                    total_removed += 1
                    file_changed = True
                    continue
                if normalized in seen:
                    total_removed += 1
                    file_changed = True
                    continue
                seen.add(normalized)
                normalized_line = format_link(link_title, normalized)
                output.append(normalized_line)
                if normalized_line != line:
                    file_changed = True
                continue
            output.append(line)
        if file_changed:
            path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
    return removed_private, removed_dead, total_removed


def append_private_archive(entries_by_note: dict[str, list[tuple[str, str]]]) -> int:
    if not entries_by_note:
        return 0
    text = PRIVATE_ARCHIVE_FILE.read_text(encoding="utf-8").rstrip()
    existing = load_existing_urls(PRIVATE_ARCHIVE_FILE)
    added = 0
    parts = [text]
    for note_title, entries in sorted(entries_by_note.items()):
        unique = []
        for title, url in entries:
            normalized = normalize_url(url)
            if normalized in existing:
                continue
            existing.add(normalized)
            unique.append((title, normalized))
        if not unique:
            continue
        parts.extend(["", f"## {note_title}", ""])
        parts.extend(format_link(title, url) for title, url in unique)
        added += len(unique)
    PRIVATE_ARCHIVE_FILE.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    return added


def append_blacklist(entries_by_note: dict[str, list[tuple[str, str]]]) -> int:
    if not entries_by_note:
        return 0
    text = BLACKLIST_FILE.read_text(encoding="utf-8").rstrip()
    existing = load_existing_urls(BLACKLIST_FILE)
    added = 0
    new_lines: list[str] = []
    for note_title, entries in sorted(entries_by_note.items()):
        for title, url in entries:
            normalized = normalize_url(url)
            if normalized in existing:
                continue
            existing.add(normalized)
            label = title or normalized
            new_lines.append(f"- [{label}]({normalized}): 来自 {note_title}")
            added += 1
    if not new_lines:
        return 0
    if AUTO_BLACKLIST_HEADING not in text:
        text = text.rstrip() + "\n\n" + AUTO_BLACKLIST_HEADING + "\n"
    updated = text.rstrip() + "\n" + "\n".join(new_lines) + "\n"
    BLACKLIST_FILE.write_text(updated, encoding="utf-8")
    return added


def process_unsorted_archive() -> tuple[dict[str, list[tuple[str, str]]], list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str]]]:
    text = UNSORTED_ARCHIVE_FILE.read_text(encoding="utf-8")
    routes: dict[str, list[tuple[str, str]]] = defaultdict(list)
    private_entries: list[tuple[str, str]] = []
    dead_entries: list[tuple[str, str]] = []
    leftovers: list[tuple[str, str]] = []
    for title, url in extract_links(text):
        normalized = normalize_url(url)
        bucket = classify_unsorted(normalized, title)
        if bucket == "private":
            private_entries.append((title, normalized))
        elif bucket == "blacklist":
            dead_entries.append((title, normalized))
        elif bucket == "unsorted":
            leftovers.append((title, normalized))
        else:
            routes[bucket].append((title, normalized))
    return routes, private_entries, dead_entries, leftovers


def categorize_leftover(title: str, url: str) -> str:
    lowered_url = url.lower()
    lowered_title = title.lower()
    if is_private(url, title):
        return "疑似私有或个人入口"
    if any(
        keyword in lowered_title
        for keyword in ("gift card", "信用卡", "机场", "破解", "mod站", "反编译工具", "远程控制软件")
    ):
        return "低价值或风险待删"
    if any(keyword in lowered_title for keyword in ("unity", "godot", "laya", "cocos", "wwise", "dotween", "moonsharp", "il2cpp", "游戏")):
        return "游戏开发与引擎相关"
    if any(keyword in lowered_title for keyword in ("c#", ".net", "source generator", "thread", "readonly", "rpc", "python", "go", "regex", "构造函数")):
        return "编程语言与运行时"
    if any(
        keyword in lowered_title
        for keyword in (
            "工具",
            "editor",
            "download",
            "下载",
            "joplin",
            "localsend",
            "tortoisegit",
            "chocolatey",
            "uml",
            "简历",
            "面试",
            "rider",
            "productivity engineering",
            "openssh",
            "sftp",
            "vscode",
        )
    ):
        return "开发工具与效率软件"
    if any(keyword in lowered_title for keyword in ("clash", "proxy", "apple id", "gift card", "远程", "串流", "短信")):
        return "网络代理与跨区服务"
    if any(keyword in lowered_title for keyword in ("grok", "notebooklm", "world model", "deepmind", "holopix", "生成世界")):
        return "AI 与产品观察"
    if any(host in lowered_url for host in ("grok.com", "notebooklm.google", "deepmind.google", "worldlabs.ai", "ls-ai.cn")):
        return "AI 与产品观察"
    if any(host in lowered_url for host in ("jetbrains.com", "gradle.com", "experienceleague.adobe.com", "docs.pingcode.com", "tool.oschina.net")):
        return "开发工具与效率软件"
    if any(host in lowered_url for host in TOOLS_HOSTS + CS_REF_HOSTS):
        return "通用工具与文档待分流"
    if any(host in lowered_url for host in AI_HOSTS + UNITY_HOSTS + UNREAL_HOSTS + VIDEO_HOSTS + BLOG_HOSTS):
        return "主题相关但待人工判断"
    return "待人工判断"


def rewrite_unsorted_archive(leftovers: list[tuple[str, str]]) -> None:
    unique_leftovers: list[tuple[str, str]] = []
    seen: set[str] = set()
    for title, url in leftovers:
        normalized = normalize_url(url)
        if normalized in seen:
            continue
        seen.add(normalized)
        unique_leftovers.append((title, normalized))
    groups: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for title, url in unique_leftovers:
        groups[categorize_leftover(title, url)].append((title, url))
    lines = [
        "---",
        "title: 未分类素材链接归档",
        "tags:",
        "  - 元数据",
        "  - 素材归档",
        "  - 待人工分类",
        "---",
        "",
        "再次归档后仍无法自动归类的链接。需要后续人工判断是吸收到主题正文、转入黑名单，还是直接删除。",
        "",
        f"> 链接数：{len(unique_leftovers)}",
        "",
    ]
    order = [
        "游戏开发与引擎相关",
        "编程语言与运行时",
        "开发工具与效率软件",
        "网络代理与跨区服务",
        "AI 与产品观察",
        "主题相关但待人工判断",
        "通用工具与文档待分流",
        "疑似私有或个人入口",
        "低价值或风险待删",
        "待人工判断",
    ]
    for section in order:
        entries = groups.get(section, [])
        if not entries:
            continue
        lines.extend([f"## {section}", ""])
        lines.extend(format_link(title, url) for title, url in entries)
        lines.append("")
    UNSORTED_ARCHIVE_FILE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def rewrite_unsorted_pool(leftover_count: int) -> None:
    lines = [
        "---",
        "title: 未分类素材池",
        "tags:",
        "  - 元数据",
        "  - 补充资料",
        "  - 未分类",
        "---",
        "",
        "自动归档后仍需人工判断的素材入口。",
        "",
        "## 当前状态",
        "",
        f"- 待人工归类链接：{leftover_count}",
        "- 账号、登录态、控制台类链接：见 [[private-account-links-archive]]",
        "- 明确失效或低价值链接：见 [[失效黑名单]]",
        "",
        "## 归档入口",
        "",
        "- [[未分类素材链接归档]]：自动归档后仍未能分类的剩余链接。",
        "- [[private-account-links-archive]]：账号、登录、控制台、密钥、支付等私有链接归档。",
        "",
    ]
    UNSORTED_POOL_FILE.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    removed_private, removed_dead, removed_count = process_public_notes()
    private_added = append_private_archive(removed_private)
    dead_added = append_blacklist(removed_dead)

    routes, private_entries, dead_entries, leftovers = process_unsorted_archive()
    rearchived = 0
    for bucket, entries in routes.items():
        rearchived += append_entries_to_note(TARGET_FILES[bucket], "### 再归档补充", entries)

    extra_private = append_private_archive({"未分类素材链接归档": private_entries})
    extra_dead = append_blacklist({"未分类素材链接归档": dead_entries})

    rewrite_unsorted_archive(leftovers)
    rewrite_unsorted_pool(len(leftovers))

    print(f"Removed {removed_count} public note links.")
    print(f"Archived {private_added + extra_private} private links.")
    print(f"Archived {dead_added + extra_dead} dead or low-value links.")
    print(f"Re-archived {rearchived} unsorted links into topic notes.")
    print(f"Left {len(leftovers)} links in unsorted archive.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
