# CLAUDE.md — MJX1010 知识库 Agent 工作规范

本文件供 Claude Code / AI Agent 在此仓库内工作时遵守。

## 项目概览

基于 Quartz v4 搭建的个人知识库站点，部署到 `https://mjx1010.github.io`。

- `content/`：公开发布内容，按「顶层主题 → 二级专题目录 → 主题笔记」组织
- `content/private/`：私有资料（登录态、公司账号、控制台等），不进入公开站点
- `content/_meta/`：frontmatter 规范与笔记模板
- `scripts/`：链接整理、隐私扫描、索引生成辅助脚本
- `quartz/`：Quartz 框架源码（一般不修改）
- `static/`：静态资源（CNAME、favicon、自定义图片）

公开目录顶层大类：`AI`、`游戏`、`计算机`、`工具`、`资源`、`资讯`、`读书`。

## 常用命令

```bash
npm install                           # 安装依赖
npx quartz build                      # 单次构建
npx quartz build --serve              # 本地预览（热更新）
python scripts/wiki_lint.py           # 检查公开区治理状态
python scripts/wiki_lint.py --strict  # 严格模式（发布前）
python scripts/harness.py privacy-scan --path <scope>  # 隐私扫描
python scripts/harness.py build-topic-index             # 生成 Unity 知识索引
```

## Frontmatter 规范

所有公开笔记必须包含以下 frontmatter：

```yaml
---
title: 笔记标题
tags:
  - 一级主题
  - 二级专题
description: 一句话描述（用于链接预览和 SEO）
status: draft          # seed | draft | reviewed | verified | archived
confidence: 0.6        # 0.0–1.0
visibility: public     # public | internal | private | pii
last_curated: 2026-06-26
source_count: 0
---
```

**_index.md 文件** 同样需要包含 `status`、`confidence`、`visibility`、`last_curated`、`source_count`。

### status 取值

| 状态 | 含义 |
|------|------|
| `seed` | 只有素材或链接，尚未整理成正文 |
| `draft` | 已有正文结构，但还需复核 |
| `reviewed` | 已人工整理，适合作为公开正文 |
| `verified` | 经过实践或权威来源验证 |
| `archived` | 历史内容，仅保留兼容或索引意义 |

### visibility 规则

| 值 | 含义 |
|----|------|
| `public` | 可发布到 GitHub Pages |
| `internal` | 公司/团队内部资料 → `private/` |
| `private` | 个人账号/控制台 → `private/` |
| `pii` | 个人身份/邮箱/支付等敏感信息 → 不入 Git |

## 强制规则

1. **全量清空待整理** — 发现 `_temp`、OneTab、收集箱等来源时必须完整处理，不允许保留"待整理"长期状态。
2. **禁止只贴链接** — 必须先访问原链接内容，提取核心信息后合并进正文；只有仍有回看价值的链接才保留到 `## 参考链接`。
3. **优先合并现有笔记** — 先查找已有专题笔记，优先合并而非新建平行笔记。
4. **公开与私有分流** — 需要登录态、公司账号、内网地址、Jenkins、控制台、个人项目页等进入 `private/`。
5. **禁止上传隐私与密钥** — 不得将个人邮箱、手机号、token、API key 等推入公开 Git 历史；推送前必须运行隐私扫描。
6. **清理重复与低价值入口** — 同一工具只保留一个主入口；releases、issues、搜索结果页、营销落地页一般不作主入口。

## 笔记结构要求

- 正文优先写结论、分类、流程、适用场景、限制条件
- `## 参考链接` 只放正文之外仍值得回看的原始资料
- 参考链接下最多保留一级子标题（如 `### 官方文档`、`### 开源项目`、`### 补充阅读`）
- 不允许出现多个 `## 参考链接` 二级标题，所有参考链接应归入同一个二级 section
- 对入口型笔记，逐步把"链接清单"升级为"主题综述 + 少量主入口"
- 文件中不允许保留 `> 阶段：xx-xxx` 形式的旧分类标记

## 写作约定

- **wikilink**：`[[页面名]]` 或 `[[页面名|显示别名]]`
- **tags**：frontmatter 中 `tags: [tag1, tag2]`，2–5 个为宜
- **callout**：`> [!note]`、`> [!warning]` 等 Obsidian 风格
- **新文件无 frontmatter**：运行 `python scripts/add_frontmatter.py` 按目录补默认 tag
- Quartz 忽略 `private`、`_meta`、`templates`、`.obsidian` 目录（见 `quartz.config.ts`）

## 变更完成标准

- 当前批次不存在"待整理公开链接"
- 不存在明显重复笔记或重复主入口
- 新增内容已归入正式分类
- 私有内容已移出公开区
- 待提交改动已通过隐私扫描
- Markdown 通过基础诊断检查
- 所有公开笔记 frontmatter 完整（`status`、`confidence`、`visibility`、`last_curated`）

## 参考资料

- Agent 详细规范：`Agent.md`
- 部署指南：`SETUP.md`
- Frontmatter 规范：`content/_meta/frontmatter规范.md`
- 读书笔记模板：`content/_meta/reading-note-template.md`
- Quartz 文档：https://quartz.jzhao.xyz
