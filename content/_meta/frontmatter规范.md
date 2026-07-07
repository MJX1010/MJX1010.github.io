---
title: Frontmatter 规范
tags:
  - 元数据
  - 维护规范
  - wiki-lint
  - quartz
status: reviewed
confidence: 0.9
visibility: public
last_curated: 2026-06-11
source_count: 2
---

## 目标

统一公开知识库笔记的元数据，兼容 Quartz 4 发布引擎，方便自动归档、链接检查、知识质量评估和发布前安全扫描。

## 推荐模板

新建公开笔记时，使用以下 frontmatter：

```yaml
---
title: 笔记标题
tags:
  - 一级主题
  - 二级专题
description: 一句话描述（用于链接预览和 SEO）
status: draft
confidence: 0.6
visibility: public
last_curated: 2026-06-11
source_count: 0
---
```

## 字段说明

| 字段 | 说明 | 必填 |
|------|------|------|
| `title` | 页面显示标题，建议与文件名语义一致 | ✅ |
| `tags` | 主题标签，建议 2-5 个 | ✅ |
| `description` | 一句话描述，用于链接预览和 SEO | 推荐 |
| `status` | 笔记生命周期状态 | ✅ |
| `confidence` | 内容可信度 (0.0-1.0) | ✅ |
| `visibility` | 发布可见性 | ✅ |
| `last_curated` | 最近人工整理日期 (YYYY-MM-DD) | ✅ |
| `source_count` | 当前笔记吸收的主要来源数量 | 推荐 |
| `aliases` | 别名列表，用于 wikilink 匹配 | 可选 |
| `lang` | 页面语言 (zh/en) | 可选 |
| `enableToc` | 是否显示目录 (默认 true) | 可选 |
| `draft` | 是否为草稿 (Quartz 不发布草稿) | 可选 |
| `publish` | 是否发布 (与 draft 互补) | 可选 |
| `permalink` | 自定义 URL 路径 | 可选 |
| `cssclasses` | 自定义 CSS 类名 | 可选 |

## Quartz 兼容别名

Quartz 支持多种字段名，统一使用以下规范名：

| 规范名 | Quartz 别名 |
|--------|------------|
| `tags` | `tag` |
| `aliases` | `alias` |
| `last_curated` | `modified` / `lastmod` / `updated` |
| `description` | — |

## status 取值

| 状态 | 含义 |
|------|------|
| `seed` | 只有素材或链接，尚未整理成正文 |
| `draft` | 已有正文结构，但结论、引用或分类还需要复核 |
| `reviewed` | 已经人工整理过，适合作为公开知识库正文 |
| `verified` | 经过实践或权威来源验证，可作为高可信参考 |
| `archived` | 历史内容，仅保留兼容或索引意义 |

## confidence 参考

| 分值 | 含义 |
|------|------|
| 0.3 | 来源少、上下文弱、主要来自个人判断 |
| 0.5 | 有可用来源，但还没有系统整理或交叉验证 |
| 0.7 | 经过人工整理，有多个公开来源支撑 |
| 0.9 | 来自官方文档、项目实践或长期稳定资料 |

## visibility 规则

| 值 | 含义 |
|----|------|
| `public` | 可以发布到 GitHub Pages 的公开知识内容 |
| `internal` | 公司、团队、项目内部资料，不进入公开 content/ |
| `private` | 个人账号、控制台、订阅等，不进入公开 content/ |
| `pii` | 个人身份、邮箱、支付等敏感信息 |

公开笔记中如出现 internal/private/pii 内容，应直接移出公开目录。

## 参考链接规则

- 正文优先沉淀结论、流程和判断标准
- 外部链接统一放在文末 `## 参考链接`
- 登录页、控制台、API Key 管理页不进入公开参考链接
- 明确失效、低价值或灰色资源不进入公开正文

## 自动检查

```bash
python scripts/wiki_lint.py                  # 常规检查
python scripts/wiki_lint.py --write-manifest # 刷新 manifest
python scripts/wiki_lint.py --strict         # 严格模式（发布前）
```
