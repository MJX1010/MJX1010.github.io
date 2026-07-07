---
title: Unreal Engine
tags:
  - 游戏开发
  - 引擎
  - unreal-engine
status: reviewed
confidence: 0.7
visibility: public
last_curated: 2026-06-11
source_count: 40
---

## 定位说明

Unreal Engine 学习与开发资料入口，以 UE4.27 为主要版本参考（文档链接以 4.27 为准）。UE5 新特性可在 Epic Developer Community 查阅。当前重点专题：UE5 攀爬系统。

## 一、官方文档与入口

- [Epic 官方文档](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-4-27-documentation?application_version=4.27) 是最权威的参考，中英文均有，版本可在 URL 中切换
- UE4.27 C++ API Reference 适合查阅引擎内部类接口
- [Unreal Engine 官方文档与教程区](https://dev.epicgames.com/documentation/zh-cn/unreal-engine) 汇总官方文档、教程和版本资料

## 二、Wiki 与社区

- [unrealcommunity.wiki](https://unrealcommunity.wiki/)：社区 Wiki，涵盖常见模式和 Blueprint 技巧
- [Old UE4 Wiki](https://nerivec.github.io/old-ue4-wiki/index.html)（nerivec 镜像）：原官方 Wiki 内容迁移后的存档
- 52VR 论坛：中文 UE 社区问答；GameDev Stack Exchange：英文通用游戏开发问答，但站点对自动探测常返回 `403`

## 三、学习资料汇总

- B 站虚幻引擎官方空间有系统化中文教程，ueskill.com 有整合性学习路线
- Udemy「Unreal Engine 5 C++: Climbing System」为项目驱动式学习路径，但课程站点对自动探测常返回 `403`
- [ABOUTCG](https://www.aboutcg.org/) 提供 UE 分布式 MMORPG 服务器等进阶课程

## 四、UE5 攀爬系统专题

- [Deema35/Climbing-Movement-Component](https://github.com/Deema35/Climbing-Movement-Component)（GitHub）：开源攀爬组件参考实现
- Gorka Games Drive 资料包：完整教程配套素材
- Udemy 课程提供系统化的 C++ 攀爬系统实现路径

## 资料收敛说明

- 本页以官方文档、社区 Wiki 和专题入口为主，正文中的核心入口已直接绑定链接。
- 文末只保留正文之外仍值得单独回看的扩展资料。


### 蓝图系统

- [Unreal Engine - Accept Delegates as Arguments in Blueprint Functions](https://blog.jamie.holdings/2022/04/14/unreal-engine-4-23-accept-delegates-as-arguments-in-blueprint-functions/)
- [UE4用蓝图在游戏内截图功能的多种方法_虚幻四摄像机截图_一只路过的仓鼠鱼的博客-CSDN博客](https://blog.csdn.net/m0_58475198/article/details/117166419)
- [UE4 截图总结（蓝图、透明通道、超出视野解决） - 知乎](https://zhuanlan.zhihu.com/p/411660911)
- [Take Automation Screenshot Of UI | Unreal Engine Documentation](http://ddns.myredstone.top:4100/BlueprintAPI-HTML/en-US/BlueprintAPI/Automation/TakeAutomationScreenshotOfUI/index.html)
- [Screenshot with UI posted by anonymous | blueprintUE | PasteBin For Unreal Engine](https://blueprintue.com/blueprint/7ishkcpl/)

### C++ 开发

- [【UE4】unlua往c++传动态委托参数的方式_unlua 调用c++函数 传递self有必要吗_看见小车在下雨的博客-CSDN博客](https://blog.csdn.net/qq_28470525/article/details/126032736)
- [Intro to Delegates in C++ · ben🌱ui](https://benui.ca/unreal/delegates-intro/)

### 开源项目与插件

- [fairygui/FairyGUI-unreal: A flexible UI framework for Unreal Engine](https://github.com/fairygui/FairyGUI-unreal)
- [【UE5】《辉电迷境》——火光电解谜毕设作品 | SuzhiのBlog](https://1keven1.github.io/2023/05/19/%E3%80%90UE5%E3%80%91%E3%80%8A%E8%BE%89%E7%94%B5%E8%BF%B7%E5%A2%83%E3%80%8B%E2%80%94%E2%80%94%E7%81%AB%E5%85%89%E7%94%B5%E8%A7%A3%E8%B0%9C%E6%AF%95%E8%AE%BE%E4%BD%9C%E5%93%81/)
- [Allar/ue5-style-guide: An attempt to make Unreal Engine 4 projects more consistent](https://github.com/Allar/ue5-style-guide#important-terminology)
- [terrehbyte/awesome-ue4: A curated list of resources for working with Unreal Engine 4. (Awesome Unreal Engine 4)](https://github.com/terrehbyte/awesome-ue4)

### 官方文档与教程

- [获取截图 | 虚幻引擎文档](https://docs.unrealengine.com/4.27/zh-CN/WorkingWithMedia/CapturingMedia/TakingScreenshots/)
- [屏幕截图比较工具 | 虚幻引擎文档](https://docs.unrealengine.com/4.26/zh-CN/TestingAndOptimization/Automation/ScreenShotComparison/?)
- [(4) UE4 Tutorial - Take Screenshots and GIFs without UI - YouTube](https://www.youtube.com/watch?v=YSvWQB_ZH9M)
- [在Gameplay中触发序列 | 虚幻引擎文档](https://docs.unrealengine.com/4.27/zh-CN/AnimatingObjects/Sequencer/HowTo/TriggeringSequences/)
- [关卡编辑器 | 虚幻引擎文档](https://docs.unrealengine.com/4.26/zh-CN/BuildingWorlds/LevelEditor/)

### 动画系统

- [为“古代山谷”中的机器人制作动画和绑定 - Unreal Engine](https://www.unrealengine.com/zh-CN/tech-blog/animating-and-rigging-the-robot-in-valley-of-the-ancient)
- [虚幻引擎中的过场动画和动画制作 | 虚幻引擎5.2文档](https://docs.unrealengine.com/5.2/zh-CN/cinematics-and-movie-making-in-unreal-engine/)

### 其他参考

- [陆续收集 UE4 常用的宏的用法_ue 可在场景中指的变量宏_鸿蒙老道的博客-CSDN博客](https://blog.csdn.net/maxiaosheng521/article/details/81746462)
- [【虚幻引擎】UE4虚幻架构之属性修饰符 - 简书](https://www.jianshu.com/p/a86d567be8c3)
- [UP­ROP­ER­TY - Gamedev Guide](https://ikrima.dev/ue4guide/engine-programming/uobjects/deprecating-uproperties-ufunctions/)
- [UE4中实现截图功能并保存到指定路径_gengine->gameviewport->exec_蓬 蒿 人的博客-CSDN博客](https://blog.csdn.net/yb0022/article/details/76034181)
- [Taking Runtime Screenshots in Unreal Engine | Mikelis' Game Blog](https://mikelis.net/taking-screenshots-in-unreal-engine/)
- [《巫师3》、UE4与游戏_IceRiver.L的博客-CSDN博客](https://blog.csdn.net/u012945093/article/details/112092854)
- [Using the Level Sequencer](https://www.audiokinetic.com/zh/library/edge/?source=UE4&id=using_features_sequencer.html)
- [UE4 -- Montage 编辑器_kuangben2000的博客-CSDN博客](https://blog.csdn.net/kuangben2000/article/details/107430935)
- [UE4：UPL 与 JNI 调用的最佳实践 - 知乎](https://zhuanlan.zhihu.com/p/294966901?utm_source=zhsharetargetidmore)
- [(UE5)性能优化-PGO和LTO（不改动代码时我们能做什么优化） - 知乎](https://zhuanlan.zhihu.com/p/673637699)

## 参考链接

> 以下链接仅保留正文之外仍值得单独回看的补充资料。

### 官方文档

- [Unreal Engine 4.27 Documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-4-27-documentation?application_version=4.27)

### 补充阅读

- [虚幻引擎学习资源大全：从入门到精通 - CSDN 博客](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/get-started)
- [Simple Climbing System UE5 Tutorial - Gorka Games (Drive)](https://drive.google.com/drive/folders/196L5cmsTWLUcr9k4JPsOk7D5dDZEz1mS)
- [UE4 Guide - Gamedev Guide](https://ikrima.dev/ue4guide/)
- [史上最全的 Unreal Engine 4 学习资料整理 - 51CTO 博客](https://blog.51cto.com/u_15273495/2916556)
- [Unreal Engine 文档总入口（中文）](https://dev.epicgames.com/documentation/zh-cn/unreal-engine)