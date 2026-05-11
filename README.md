# MJX1010 Knowledge Base

基于 Quartz 搭建的个人知识库与数字花园，用于整理 AI、游戏开发、编程基础、工具、资源和技术资讯。

线上地址：

- <https://mjx1010.github.io/>

## 仓库定位

- `content/`：实际发布的知识库内容
- `content/private/`：私有整理材料，不发布到站点
- `scripts/`：链接整理、内容抓取、索引生成等辅助脚本
- `quartz/`：Quartz 站点构建框架

本仓库已经从“链接导航页”逐步转为“主题正文 + 文末参考链接”的结构。

## 常用命令

安装依赖：

```bash
npm install
```

本地构建：

```bash
npx quartz build
```

本地预览：

```bash
npx quartz build --serve
```

生成 Unity 知识索引：

```bash
python scripts/build_unity_note_index.py
```

## 一键发布

Windows 下可直接运行：

```bat
publish.bat
```

脚本会执行以下流程：

1. 重新生成 Unity 知识索引
2. 执行 Quartz 构建校验
3. 自动 `git add -A`
4. 自动提交并推送到 `origin/main`
5. 由 GitHub Actions 自动部署到 GitHub Pages

## 内容维护约定

- 正式知识尽量沉淀到主题正文，不再维护公开的历史链接池目录
- 外部链接统一保留在正文末尾的 `参考链接`
- 需要登录态、公司账号或私有访问权限的内容放入 `content/private/`
- 批量整理链接时，优先更新现有主题正文或补充资料分组，而不是新增孤立链接页

## 备注

- Quartz 上游项目：<https://github.com/jackyzha0/quartz>
- 本仓库是基于 Quartz 定制后的个人知识库站点仓库，不是 Quartz 官方源码仓库本身
