# Skills Index

本文件是当前仓库的轻量 AI harness 路由入口，用来把任务先分发到最合适的 skill，再按需补读详细规则。

## 使用原则

- 先读本索引，不要一开始把所有 skill 正文全部加载。
- 先命中一个主 skill；只有任务跨域时，才叠加第二个 skill。
- 规则文档负责“做什么、何时做、如何验收”，具体执行优先走 `scripts/` 下的脚本入口。

## 主技能路由

### 1. 笔记整理与知识归档

- 场景：OneTab、收集箱、导入批次、专题重组、公开/私有分流
- 主 skill：`.trae/skills/note-curation/SKILL.md`
- 主规则：`Agent.md`
- 补充能力：`.claude/skills/weread-skills/SKILL.md`
- 默认动作：
  - 先按 `Agent.md` 判断公开 / 私有 / 淘汰
  - 访问原始链接内容并提炼，不允许只贴链接
  - 合并进现有专题正文，最后清理重复和无效入口

### 2. 外链体检与批量清理

- 场景：批量检查 `content/` 或 `private/` 下的外链状态、修复失效链接、转存失效归档
- 主 skill：`.trae/skills/link-audit/SKILL.md`
- 默认动作：
  - 先跑体检脚本
  - 再根据计划文件批量替换或归档
  - 最后复跑报告确认 `broken/error/auth` 是否下降

### 3. Git 同步与上传

- 场景：本轮改动已完成，需要安全地提交并推送
- 主 skill：`.trae/skills/git-sync-push/SKILL.md`
- 默认动作：
  - 先检查工作区
  - 先做隐私扫描，确认没有个人信息或真实凭证
  - 明确提交范围
  - 排除 `_temp/`、分析产物和无关改动

### 4. 隐私扫描与敏感信息拦截
- 场景：提交前检查邮箱、手机号、身份证、token、私钥或 API key，防止进入 Git 历史
- 主 skill：`.trae/skills/privacy-scan/SKILL.md`
- 默认动作：
  - 扫描待提交路径
  - 区分真实敏感信息与占位示例
  - 将真实敏感内容移到 `private/` 或做脱敏
  - 复扫通过后再继续提交

## 脚本入口

- 统一入口：`python scripts/harness.py <subcommand>`
- 当前已接入：
  - `wiki-lint`
  - `fetch-link-content`
  - `build-topic-index`
  - `audit-links`
  - `apply-link-plan`
  - `sync-git`
  - `privacy-scan`
  - `github-account-audit`

## 当前建议

- 日常知识库整理：切到 `note-curation`
- 需要查和修外链：切到 `link-audit`
- 需要上传 Git：切到 `git-sync-push`
