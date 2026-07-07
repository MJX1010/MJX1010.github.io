---
title: Obsidian 与知识库
tags:
  - 开发工具
  - 知识管理
  - obsidian
  - markdown
status: reviewed
confidence: 0.7
visibility: public
last_curated: 2026-06-11
source_count: 5
---

## 定位说明

面向 Obsidian 知识库维护、笔记迁移和附件治理的工具整理。重点不是“收集插件名字”，而是把迁移链路、格式边界和落地顺序讲清楚，方便后续把历史笔记体系平滑迁入 Markdown 知识库。

## 一、Agent / Vault 能力扩展

- `obsidian-skills` 提供了一组面向 Agent 的 Obsidian 技能，覆盖 Obsidian Markdown、Bases、JSON Canvas、Obsidian CLI 和网页正文抽取，适合把 Agent 直接接入本地 vault 的编辑工作流。
- 这类 skill 的价值不在“多一个入口”，而在于让 Agent 知道 Obsidian 特有的语法和文件形态，例如 wikilink、callout、`.canvas`、`.base` 以及 CLI 操作。
- 如果你的知识库工作流已经依赖 Claude Code / Codex CLI，这类 skill 比单纯保存提示词更稳定，因为它把文件格式约束和工具调用方式一起封装了。

## 二、为知笔记迁移链路

- `wiz_export` 是最直接的导出器：通过账号、密码和文件夹参数，把为知笔记导出为 Markdown，适合快速做批量冷迁移。
- `wiz-markdown` 更像底层能力库，核心用途是从为知 HTML 中提取嵌入的 Markdown，适合做二次开发或补齐自定义转换流程。
- `wiz-to-obsidian` 是更完整的迁移方案：它读取本地 `index.db`，解压 `ziw` 包里的 `index.html`，再按笔记类型转换为 Markdown，并处理附件和部分图片下载。
- 从迁移原理看，真正关键的不是“转成 md”本身，而是先摸清为知的本地存储结构：数据库索引、`ziw` 压缩包、HTML 正文、任务清单 XML 都是不同来源，不能只靠表面导出。

## 三、迁移边界与风险

- `wiz-to-obsidian` 明确支持 markdown 笔记、普通笔记和 `todolist2` 任务清单，但普通笔记转 Markdown 时会丢失加粗、字体、颜色、缩进等富文本样式。
- 加密笔记必须先在为知里解密，附件也要先确保已经下载到本地，否则转换过程只能继续执行并把缺失项留给人工补。
- 任务清单类笔记不支持附件和文档链接，说明“任务系统迁移”和“正文迁移”应拆成两条处理链路，不能假设一把梭就能完整保真。
- 批量迁移前最好先做小样本验证，尤其是目录层级、附件命名、图片链接和中英文标题，避免一次性导出后再大面积返工。

## 四、附件治理

- `obsidian-attachment-manager` 适合解决迁移后的附件混乱问题：它可以把附件目录名和笔记名绑定，自动重命名粘贴图片、附件目录和附件文件，还能按需隐藏附件目录。
- 这个插件也支持把当前打开笔记中的远程图片下载到本地附件目录，适合把历史 HTTP 图片逐步收成本地资源。
- 使用时要注意它会改写 Obsidian 的两个设置：新链接格式和默认附件存放位置。对于已有 vault，先确认你的链接策略和附件策略，再启用自动化改名。

## 五、推荐落地顺序

1. 先做样本迁移，验证目录、命名、附件和样式损失边界。
2. 再做批量导出，把“原始导出结果”和“整理后的正式笔记”分开保存。
3. 导入 Obsidian 后，优先统一附件目录、远程图片、本地引用和 frontmatter。
4. 最后再让 Agent 参与整理，把原文内容提取、归并到现有主题笔记，而不是原样把外链或导出文件堆进库里。

## 资料收敛说明

- 本页保留的是“可形成稳定迁移流程”的工具，不保留零散教程页和搜索结果页。
- 对导出器、库和插件，正文优先沉淀其处理边界、依赖前提和适用位置，避免只留下仓库链接却不知道如何组合使用。

## 参考链接

> 以下链接保留为仍有必要回看的原始资料入口。

### 官方 / 项目入口

- [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
- [galaio/wiz_export](https://github.com/galaio/wiz_export)
- [altairwei/wiz-markdown](https://github.com/altairwei/wiz-markdown)
- [chenfeicqq/wiz-to-obsidian](https://github.com/chenfeicqq/wiz-to-obsidian)
- [chenfeicqq/obsidian-attachment-manager](https://github.com/chenfeicqq/obsidian-attachment-manager)