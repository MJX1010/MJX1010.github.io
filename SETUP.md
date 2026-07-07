# 部署到 MJX1010.github.io

本仓库基于 [Quartz v4](https://quartz.jzhao.xyz) 搭建，content/ 下的 markdown 会被构建成静态站点 + 知识图谱 + 全文搜索，部署到 GitHub Pages。

## 一、首次部署到 GitHub

### 1. 把仓库推到 GitHub

> 注意：若 `MJX1010/MJX1010.github.io` 仓库里已有旧内容，先在 GitHub 新建一个 `legacy-backup` 分支保留它，再用本目录覆盖 `main`。

```bash
# 在本机当前目录（MJX1010.github.io/）
git remote remove origin                                # 解除上游 jackyzha0/quartz 关联
git remote add origin git@github.com:MJX1010/MJX1010.github.io.git
git checkout -b main
git add -A
git commit -m "feat: bootstrap quartz knowledge base from urls/"
git push -u origin main --force                         # 第一次需要覆盖远端
```

### 2. 在 GitHub 上启用 Pages

仓库 → **Settings** → **Pages**：
- **Source** 选 **GitHub Actions**（不是默认的 "Deploy from a branch"）
- 不要选 main 分支 root 那种旧模式

第一次 push 上去后，`.github/workflows/deploy.yml` 会自动触发，约 1~3 分钟构建完成，访问 `https://mjx1010.github.io` 就能看到。

### 3. 如果 Action 报"environment protection rules"

仓库 → **Settings** → **Environments** → 把名为 `github-pages` 的环境删除，下次 Action 自动重建即可。

## 二、本地预览

```bash
npm install            # 一次性，~150 MB 依赖
npx quartz build       # 单次构建到 public/
npx quartz build --serve  # 起本地服务器，热更新预览（推荐）
```

打开 http://localhost:8080 看效果。

## 三、日常更新流程

### A. 直接编辑 markdown

```bash
# 在 content/ 下编辑/新增 .md
vim content/02-引擎与游戏开发/Unity-框架与工具.md
git add content
git commit -m "docs: 新增 ECS 学习链接"
git push                  # GitHub Action 自动构建并发布
```

### B. 用 Obsidian 当编辑器（推荐）

把 `content/` 目录加成 Obsidian 的 vault：
1. Obsidian → Open folder as vault → 选 `MJX1010.github.io/content/`
2. 直接在 Obsidian 里编辑、写 `[[wikilink]]`、加 tag、看本地图谱
3. 写完之后回到 git 命令行 push

Obsidian 的实时图谱预览 ↔ Quartz 发布到网页的图谱效果完全一致。

## 四、添加新链接到现有分类

1. 找到目标 .md（如 `content/04-AI-Coding/AI工具与导航.md`）
2. 在合适小节加一行：
   ```markdown
   - [Cursor 官网](https://cursor.com): AI IDE 主入口
   ```
3. 想让它进图谱并和别的页面有连边，再加一条 wikilink：
   ```markdown
   > 同类参考: [[AI-Coding-与-Agent]]
   ```
4. commit + push 即可

## 五、未来换自有域名

### 用根域名（如 `kb.mjx.dev`）

1. 在 `static/` 目录下新建一个文件叫 `CNAME`，**只写一行**：
   ```
   kb.mjx.dev
   ```
2. 改 `quartz.config.ts` 里的 `baseUrl`：
   ```ts
   baseUrl: "kb.mjx.dev"
   ```
3. 域名 DNS 设置：
   - 子域名：加一条 `CNAME` 记录指向 `mjx1010.github.io`
   - 根域名：加 4 条 `A` 记录指向 GitHub 的官方 IP（185.199.108.153 / 109 / 110 / 111）
4. push，GitHub Pages 后台 Settings → Pages 里勾选 **Enforce HTTPS**
5. 等 ~10 分钟 DNS 生效

### 迁到自己的服务器（Nginx）

整个 `public/` 目录就是静态站点，传上去即可：
```bash
npx quartz build
rsync -avz --delete public/ user@server:/var/www/kb/
```
Nginx 配置极简（参考 Quartz 官方文档 hosting.md 里的 Nginx 段）。

## 六、目录结构

```
MJX1010.github.io/
├── content/                    # 你的 markdown，构建源
├── quartz/                     # Quartz 框架代码（不要改）
├── quartz.config.ts            # 站点配置（标题 / baseUrl / 主题色）
├── quartz.layout.ts            # 页面布局组件配置
├── package.json
├── scripts/
│   ├── add_frontmatter.py      # 给新文件批量加 frontmatter
│   └── convert_to_wikilinks.py # 把 markdown link 转成 wikilink
├── static/                     # 静态资源（CNAME、favicon、自定义图片放这）
├── .github/workflows/deploy.yml  # GitHub Pages 自动部署
└── public/                     # 构建产物（不进 git）
```

## 七、写新内容时

- **wikilink**: `[[页面名]]` 或 `[[页面名|显示别名]]`，跨目录用 `[[文件夹/页面名]]`
- **tag**: 文件顶部 frontmatter `tags: [tag1, tag2]`，搜索/图谱按颜色聚类
- **callout**: 用 `> [!note]` `> [!warning]` 这种 obsidian 风格，会渲染成漂亮的提示框
- **新文件没有 frontmatter**: 跑一次 `python scripts/add_frontmatter.py`，会按目录补默认 tag

## 八、关键链接

- Quartz 官方文档：https://quartz.jzhao.xyz
- 配置项：https://quartz.jzhao.xyz/configuration
- 主题色 / 字体改法：https://quartz.jzhao.xyz/features/customizing-fonts
- 图谱视图说明：https://quartz.jzhao.xyz/features/graph-view
- 全文搜索说明：https://quartz.jzhao.xyz/features/full-text-search
