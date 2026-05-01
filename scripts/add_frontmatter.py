"""Batch-add YAML frontmatter (title + tags) to every .md under content/.

Rules:
- title: extracted from the first H1 heading; falls back to the file stem
- tags: derived from the top-level folder (and a few specific files)
- existing frontmatter (--- ... ---) is preserved and only fields missing get added
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"

# Tag rules: top-level folder name -> tags, plus per-file overrides
FOLDER_TAGS: dict[str, list[str]] = {
    "00-高价值精选": ["精选", "入口"],
    "01-学习与基础": ["学习", "基础"],
    "02-引擎与游戏开发": ["游戏开发", "引擎"],
    "03-移动端与平台": ["移动端", "平台"],
    "04-AI-Coding": ["ai-coding", "llm"],
    "05-开发工具": ["开发工具"],
    "06-参考文档": ["参考", "文档"],
    "07-社区与资讯": ["社区", "资讯"],
    "08-资源下载": ["资源"],
    "09-工作台与账号": ["工作台", "账号"],
    "10-待处理": ["待处理"],
    "11-待清理": ["待清理"],
    "90-过程文件": ["过程", "元数据"],
    "99-原始数据": ["原始数据"],
}

# More specific tags by filename (added on top of folder tags)
FILE_EXTRA_TAGS: dict[str, list[str]] = {
    "Unity-框架与工具.md": ["unity", "框架", "工具链"],
    "Unity-UI与优化.md": ["unity", "ugui", "性能优化"],
    "Unreal-Engine.md": ["unreal-engine"],
    "帧同步与游戏AI.md": ["帧同步", "lockstep", "游戏ai"],
    "其他引擎.md": ["godot", "rpg-maker"],
    "移动端接入与平台问题.md": ["android", "ios", "firebase"],
    "平台与规范.md": ["代码规范", "android", "apple"],
    "AI-Coding-与-Agent.md": ["agent"],
    "大模型产品.md": ["llm", "chatbot"],
    "AI工具与导航.md": ["ai-tools"],
    "IDE与桌面工具.md": ["ide", "桌面工具"],
    "在线工具与协作.md": ["在线工具", "协作"],
    "网络与代理.md": ["代理", "网络"],
    "C-CSharp-CPP参考.md": ["c++", "c#", "dotnet"],
    "技术博客与社区.md": ["博客", "社区"],
    "视频与课程.md": ["视频", "课程"],
    "媒体与资讯.md": ["媒体", "资讯"],
    "电子书与素材.md": ["电子书", "素材"],
    "软件与游戏资源.md": ["软件", "游戏资源"],
    "个人账号与控制台.md": ["账号", "控制台"],
    "工作台与控制台入口.md": ["工作台", "jenkins"],
    "失效与低价值.md": ["失效", "灰色资源"],
    "待删除链接.md": ["规则"],
    "未归档待处理.md": ["待二筛"],
    "内部项目页二次分类.md": ["内部"],
    "临时入口删除建议.md": ["规则"],
    "编程语言.md": ["c++", "c#", "lua"],
    "算法与计算机基础.md": ["算法", "数据结构"],
    "学习导航.md": ["导航"],
    "知识清单.md": ["主索引"],
    "个人常用版.md": ["高频"],
    "内部长期知识补充.md": ["内部"],
    "总目录-链接归档.md": ["索引", "入口"],
    "链接整理归档.md": ["索引", "入口", "ai-coding"],
    "index.md": ["首页", "入口"],
}

H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def extract_title(body: str, fallback: str) -> str:
    match = H1_RE.search(body)
    if match:
        return match.group(1).strip()
    return fallback


def derive_tags(rel_path: Path) -> list[str]:
    parts = rel_path.parts
    tags: list[str] = []
    if len(parts) > 1 and parts[0] in FOLDER_TAGS:
        tags.extend(FOLDER_TAGS[parts[0]])
    elif len(parts) == 1:
        # root-level files: README/总目录/链接整理归档/index
        pass
    extra = FILE_EXTRA_TAGS.get(rel_path.name)
    if extra:
        for t in extra:
            if t not in tags:
                tags.append(t)
    # de-dup, preserve order
    seen: set[str] = set()
    out: list[str] = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def make_frontmatter(title: str, tags: list[str]) -> str:
    yaml_lines = ["---", f"title: {title}"]
    if tags:
        yaml_lines.append("tags:")
        for tag in tags:
            yaml_lines.append(f"  - {tag}")
    yaml_lines.append("---")
    return "\n".join(yaml_lines) + "\n"


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    fallback = path.stem
    has_fm = text.startswith("---\n")

    if has_fm:
        # Skip if already has frontmatter (idempotent)
        return False

    title = extract_title(text, fallback)
    tags = derive_tags(rel)
    fm = make_frontmatter(title, tags)
    path.write_text(fm + text, encoding="utf-8")
    return True


def main() -> int:
    if not ROOT.exists():
        print(f"content/ not found at {ROOT}", file=sys.stderr)
        return 1
    touched = 0
    for md in sorted(ROOT.rglob("*.md")):
        if process(md):
            touched += 1
            rel = md.relative_to(ROOT)
            print(f"  + frontmatter -> {rel}")
    print(f"\nDone. Added frontmatter to {touched} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
