---
title: IDE 与桌面工具
tags:
  - 开发工具
  - ide
  - 桌面工具
status: reviewed
confidence: 0.7
visibility: public
last_curated: 2026-05-13
source_count: 10
---

> 阶段：04-开发工具  

## 定位说明

开发环境相关工具汇总：IDE、代码托管平台、容器与运维工具、终端、桌面效率软件和移动端模拟器。

## 一、IDE / 编辑器

- **VS Code**：最常用的轻量编辑器，Remote Development 支持远端开发和容器内开发
- **Visual Studio**：Windows 下 C# / C++ 开发主力，官方文档见 learn.microsoft.com
- **JetBrains 全家桶**（Rider / CLion / IDEA）：大型项目和重构场景体验更好，中文官网 jetbrains.com.cn

## 二、代码托管 / 协作

- **GitHub / Gitee / GitCode（AtomGit）**：主流 Git 托管平台，Gitee 在国内访问最稳定
- **Jenkins**（jenkins-zh.cn）：持续集成 / CD 流水线，构建自动化核心工具

## 三、容器与运维

- **Docker Hub**：镜像仓库，docker pull 的默认来源
- **FinalShell**：SSH + SFTP 图形化一体化工具，适合运维场景

## 四、终端 / 远程

- **FinalShell**：SSH 客户端，带文件管理和监控面板
- **Tampermonkey**：浏览器脚本管理器，自动化网页操作

## 五、桌面工具

- **PixPin**：截图 + 贴图 + OCR，日常效率必备
- **f.lux**：色温自动调节，护眼必备
- **Snappy Driver Installer**：驱动批量安装工具，系统重装后使用

## 六、移动端模拟器

- **夜神模拟器**：Android 模拟器，兼容性较好，适合移动端接入和 SDK 测试

## 资料收敛说明

- 本页已将原先 `31` 条参考链接压缩为 `10` 条核心引用，重复导航页、同类 API 细节页和低信噪比补充资料不再逐条公开保留。
- 正文已优先沉淀选型标准、排查流程、风险边界和常用工具定位，后续新增资料应继续转成正文结论，而不是直接堆叠链接。
- 文末只保留官方文档、代表性开源项目和少量仍值得回看的补充阅读。

## 参考链接

> 以下链接仅保留正文仍需回看的核心资料入口。

### 官方文档

- [Visual Studio 文档 | Microsoft Learn](https://learn.microsoft.com/zh-cn/visualstudio/windows/?view=vs-2022)
- [Docker Hub](https://hub.docker.com/)

### 开源项目

- [DeviceFarmer/stf: Control and manage Android devices from your browser.](https://github.com/DeviceFarmer/stf)

### 补充阅读

- [JetBrains: 软件开发者和团队的必备工具（中文）](https://www.jetbrains.com.cn/)
- [PixPin - 截图/贴图/OCR](https://pixpin.cn/)
- [Snappy Driver Installer](https://sdi-tool.org/)
- [VS Code Remote Development - Even Better](https://code.visualstudio.com/blogs/2022/12/07/remote-even-better)
- [Gitee - 基于 Git 的代码托管平台](https://gitee.com/)
- [AtomGit | GitCode - 全球开发者的开源社区](https://gitcode.com/)
- [VS Code 搭建 C/C++ 编译运行环境的四种方案 - 知乎](https://zhuanlan.zhihu.com/p/35178331)
