---
title: AI Coding 与 Agent
tags:
  - ai-coding
  - llm
  - agent
status: reviewed
confidence: 0.7
visibility: public
last_curated: 2026-05-22
source_count: 12
---

## 说明
- 用途：沉淀 AI 编程、Agent、模型产品与相关生态工具入口
- 原则：优先保留“工具本体、官方入口、稳定项目、代表性观察文章”

## 一、Agent / AI Coding 工具入口

- **[MiniMax Agent](https://agent.minimaxi.com/)**：通用 Agent 产品入口，可作为国产通用 Agent 体验参考
- **[TRAE Solo](https://www.trae.ai/solo)**：AI 编程产品入口，偏向实际开发工作流体验
- **[AutoCLI](https://github.com/nashsu/AutoCLI)**：面向网页与桌面应用的信息抓取和自动化 CLI，适合扩展 Agent 工具链边界
- **[YesCode](https://co.yes.vg/subscription)**：面向 Claude Code、Codex、Gemini CLI 的统一路由层，把多家模型供应商收敛到同一个 base URL，并补上自动故障切换、预算封顶和实时费用面板

## 二、相关开源项目

- **[musistudio/claude-code-router](https://github.com/musistudio/claude-code-router)**：Claude Code 路由与工作流增强项目
- **[Hmbown/DeepSeek-TUI](https://github.com/Hmbown/DeepSeek-TUI)**：终端里的 DeepSeek Coding Agent，适合参考 CLI Agent 交互形态
- **[CodeGraphContext/CodeGraphContext](https://github.com/CodeGraphContext/CodeGraphContext)**：本地代码索引图谱与 MCP 服务，适合大仓上下文检索
- **[zilliztech/memsearch](https://github.com/zilliztech/memsearch)** / **[thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)**：面向 Agent 记忆管理的 Markdown-first 方案
- **[ComposioHQ/awesome-codex-skills](https://github.com/ComposioHQ/awesome-codex-skills)** / **[obra/superpowers](https://github.com/obra/superpowers)**：Skill 和 workflow 体系参考，适合设计 AI Coding 工作流
- **[op7418/Claude-to-IM](https://github.com/op7418/Claude-to-IM/blob/main/README.zh-CN.md)**：把 Claude Code 风格的流式会话和工具审批桥接到 Telegram、Discord、飞书等 IM 平台，适合接入团队值班、远程协作或聊天窗口里的 Agent 工作流

## 三、外部观察与行业信息

- **阮一峰对 TRAE SOLO 的观察**：偏行业观察和产品体验总结；原文站点对自动探测常返回 `403`
- **[learn-coding-agent](https://github.com/sanbuphy/learn-coding-agent/blob/main/README_CN.md)**：Coding Agent 学习路径与实践资料整理
- **[AprilNEA/claude-code-source](https://github.com/AprilNEA/claude-code-source)**：通过 source map 恢复 Claude Code 源码的学习向仓库，适合研究 CLI Agent 结构

## 四、不建议纳入长期知识库的同类页面

- `chatgpt.com/c/...` 会话页
- `gemini.google.com/app/...` 会话页
- 带一次性上下文的 prompt / 对话结果页
- 聚合站里的二手介绍页，如果已经保留官方入口，则通常可以不保留

## 五、后续整理建议

- 如果你的目标是“工具调研”，可再拆成：
  - `官方产品入口`
  - `开源增强项目`
  - `行业观察`
- 如果目标是“实际使用”，只保留：
  - 正在用的产品入口
  - 与当前工作流强相关的开源项目

## 资料收敛说明

- 本页属于“入口型”清单，正文中的产品入口、项目仓库和观察文章已直接绑定链接。
## 参考链接

> 本页主入口已直接内联到正文；后续若新增专题文章、CLI 文档或对比评测，再单独保留到此处。

### 补充阅读

- [Claude Code 概述](https://code.claude.com/docs/zh-CN/overview)
- [Claude Code Hooks reference](https://code.claude.com/docs/en/hooks)
