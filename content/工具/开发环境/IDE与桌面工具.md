---
title: IDE 与桌面工具
tags:
  - 开发工具
  - ide
  - 桌面工具
status: reviewed
confidence: 0.7
visibility: public
last_curated: 2026-06-11
source_count: 157
---

## 定位说明

开发环境相关工具汇总：IDE、代码托管平台、容器与运维工具、终端、桌面效率软件和移动端模拟器。

## 一、IDE / 编辑器

- **[VS Code](https://code.visualstudio.com/)**：最常用的轻量编辑器，Remote Development 支持远端开发和容器内开发
- **[Visual Studio](https://visualstudio.microsoft.com/zh-hans/)**：Windows 下 C# / C++ 开发主力，官方文档见 [Microsoft Learn](https://learn.microsoft.com/zh-cn/visualstudio/windows/?view=vs-2022)
- **[JetBrains 全家桶](https://www.jetbrains.com.cn/)**（Rider / CLion / IDEA）：大型项目和重构场景体验更好

## 二、代码托管 / 协作

- **[GitHub](https://github.com/)** / **[Gitee](https://gitee.com/)** / **[GitCode](https://gitcode.com/)**（AtomGit）：主流 Git 托管平台，Gitee 在国内访问最稳定
- **Jenkins**（jenkins-zh.cn）：持续集成 / CD 流水线，构建自动化核心工具

## 三、容器与运维

- **[Docker Hub](https://hub.docker.com/)**：镜像仓库，`docker pull` 的默认来源

## 四、终端 / 远程

- **[FinalShell](https://www.hostbuf.com/t/988.html)**：SSH 客户端，带文件管理和监控面板
- **[Wave Terminal](https://github.com/wavetermdev/waveterm)**：现代终端工作区，近版加入进程查看器、Quake Mode 和 `tab:confirmclose` 等实用配置，适合多标签和上下文工作流
- **[Hermes Desktop](https://github.com/fathah/hermes-desktop)**：桌面化 AI CLI 工作台，支持多模型 provider、SSH tunnel、会话管理和附件输入，适合把 CLI agent 包成稳定桌面环境
- **[Tampermonkey](https://www.tampermonkey.net/)**：浏览器脚本管理器，自动化网页操作

## 五、桌面工具

- **[PixPin](https://pixpin.cn/)**：截图 + 贴图 + OCR，日常效率必备
- **[f.lux](https://justgetflux.com/)**：色温自动调节，护眼必备
- **[Snappy Driver Installer](https://sdi-tool.org/)**：驱动批量安装工具，系统重装后使用

## 六、移动端模拟器

- **[NoxPlayer（夜神模拟器）](https://www.bignox.com/)**：Android 模拟器，适合移动端接入、ADB 联调和 SDK 测试

## 七、开发配套 / SDK

- **[DB Browser for SQLite](https://sqlitebrowser.org/dl/)** / **[DBeaver Community](https://dbeaver.io/download/)**：数据库查看与调试的常用桌面工具
- **[Apache Maven](https://maven.apache.org/download.cgi)**：Java 构建工具，处理 Android / Java 依赖时常会用到
- **[Go](https://go.dev/dl/)** / **[Zig](https://ziglang.org/download/)**：常见编译型语言环境安装入口
- **[Temurin JDK](https://adoptium.net/zh-CN/temurin/releases?version=21)** / **[Oracle JDK](https://www.oracle.com/java/technologies/downloads/#jdk21-windows)**：Windows 下常用 JDK 下载入口
- **[x-cmd install](https://cn.x-cmd.com/install/)**：统一包管理入口，把跨平台安装收敛成 `x install <软件名>`，适合频繁切换系统或维护工具清单的人

## 资料收敛说明

- 本页属于“入口型”清单，正文中的工具名已直接绑定官网、文档或下载入口。
- 文末只保留正文之外仍值得单独回看的项目或补充文章。


## 参考链接

> 以下链接仅保留正文之外仍值得单独回看的补充资料。

### 开源项目

- [DeviceFarmer/stf: Control and manage Android devices from your browser.](https://github.com/DeviceFarmer/stf)
- [Wave Terminal 文档](https://docs.waveterm.dev/config?ref=waveconfig)

### 补充阅读

- [VS Code Remote Development - Even Better](https://code.visualstudio.com/blogs/2022/12/07/remote-even-better)