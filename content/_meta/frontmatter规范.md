---
title: Frontmatter 规范
tags:
  - 元数据
  - 维护规范
  - wiki-lint
status: reviewed
confidence: 0.9
visibility: public
last_curated: 2026-05-11
source_count: 2
---

## 目标

本规范用于统一公开知识库笔记的元数据，方便后续自动归档、链接检查、知识质量评估和发布前安全扫描。

## 推荐模板

新建公开笔记时，优先使用以下 frontmatter：

```yaml
---
title: 笔记标题
tags:
  - 一级主题
  - 二级专题
status: draft
confidence: 0.6
visibility: public
last_curated: 2026-05-11
source_count: 0
---
```

## 字段说明

- `title`：页面显示标题，建议与文件名语义一致。
- `tags`：主题标签，建议 2-5 个，避免把目录层级和所有关键词都塞进标签。
- `status`：笔记生命周期状态，用于区分草稿、已整理和已验证内容。
- `confidence`：内容可信度，范围 `0.0` 到 `1.0`，用于提示这篇笔记是否需要复核。
- `visibility`：发布可见性，公开站点只允许 `public`。
- `last_curated`：最近人工整理日期，格式为 `YYYY-MM-DD`。
- `source_count`：当前笔记吸收的主要来源数量，不需要精确到每个参考链接。

## status 取值

- `seed`：只有素材或链接，尚未整理成正文。
- `draft`：已有正文结构，但结论、引用或分类还需要复核。
- `reviewed`：已经人工整理过，适合作为公开知识库正文。
- `verified`：经过实践或权威来源验证，可作为高可信参考。
- `archived`：历史内容，仅保留兼容或索引意义，不建议继续扩写。

## confidence 参考

- `0.3`：来源少、上下文弱、主要来自个人判断或临时记录。
- `0.5`：有可用来源，但还没有系统整理或交叉验证。
- `0.7`：经过人工整理，有多个公开来源支撑。
- `0.9`：来自官方文档、项目实践或长期稳定资料。

## visibility 规则

- `public`：可以发布到 GitHub Pages 的公开知识内容。
- `internal`：公司、团队、项目内部资料，不进入公开 `content/`。
- `private`：个人账号、控制台、订阅、登录态入口，不进入公开 `content/`。
- `pii`：个人身份、邮箱、支付、会话信息等敏感内容，不进入公开仓库。

当前仓库采用物理隔离策略：`content/private/` 被 `.gitignore` 忽略，不进入公开 Git 仓库。公开笔记中如出现 `internal/private/pii` 内容，应直接移出公开目录。

## 参考链接规则

- 正文优先沉淀结论、流程和判断标准。
- 外部链接统一放在文末 `## 参考链接`。
- 登录页、控制台、API Key 管理页、会话页、带 token 的 URL 不进入公开参考链接。
- 明确失效、低价值或灰色资源不进入公开正文。

## 自动检查

运行以下命令检查公开内容：

```bash
python scripts/wiki_lint.py
```

刷新 manifest：

```bash
python scripts/wiki_lint.py --write-manifest
```

严格模式会把 warning 也视为失败，适合发布前使用：

```bash
python scripts/wiki_lint.py --strict
```
