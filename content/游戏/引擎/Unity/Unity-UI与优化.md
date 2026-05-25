---
title: Unity UI 与优化
tags:
  - 游戏开发
  - 引擎
  - unity
  - ugui
  - 性能优化
status: reviewed
confidence: 0.7
visibility: public
last_curated: 2026-05-13
source_count: 10
---

> 阶段：02-引擎与游戏开发  

## 核心结论

- 本笔记是 Unity UI、渲染优化、框架入口和常用资料的综合索引，适合做“问题定位入口”，更细的 UI 工程实践可继续看 [[Unity-UGUI与UI工具笔记]]。
- UI 与渲染优化要先建立观测链路，再决定改代码、改资源、改层级还是改工具流程。
- DrawCall、Batch、Overdraw、GC、资源加载和脚本开销经常互相影响，不能只盯一个指标。
- 框架资料、PureMVC、ET、DOTween、Asset Store 工具都应按项目实际使用价值筛选，避免资料堆积成新的链接池。

## 适用场景

- 需要快速查找 Unity 官方入口、社区入口、Asset Store、DOTween、PureMVC、ECS、UGUI 优化资料。
- 项目出现 UI 打开慢、滑动掉帧、DrawCall 高、GC Alloc 高、渲染过度或脚本更新过重。
- 需要对旧项目的 UI 和框架资料进行二次筛选，沉淀成可执行的优化规范。

## UI 优化框架

- 先区分问题类型：打开卡顿、持续掉帧、内存增长、点击异常、渲染过重、资源加载慢。
- 打开卡顿通常来自同步加载、实例化过多、Layout 递归、文本生成、图集加载和脚本初始化。
- 持续掉帧通常来自高频重建、大量 Raycast、列表未复用、Update 逻辑、动画和粒子特效。
- DrawCall 高时先检查材质、图集、Mask、Canvas 拆分和动态材质实例。
- Overdraw 高时检查全屏半透明、遮罩、背景叠层、UI 粒子和复杂 Shader。

## 渲染与性能排查

1. 用 Profiler 确认瓶颈在 CPU、Rendering、Scripts、UI、GC 还是资源加载。
2. 用 Frame Debugger 查看 DrawCall、Batch 中断原因、材质、纹理和渲染顺序。
3. 用 Memory Profiler 或平台工具检查纹理、Mesh、Shader、Audio、Native 内存和托管对象。
4. 对比空场景、单面板、完整场景，拆分出真正导致指标变化的模块。
5. 修复后记录基准数据，例如打开耗时、峰值内存、DrawCall、GC Alloc 和平均帧耗时。

## 框架与工具使用原则

- DOTween 适合 UI 动画和简单序列动画，但要管理 Tween 生命周期，避免隐藏对象仍在播放。
- PureMVC 可以作为理解 MVC/MVP/MVVM 分层的资料，但新项目应结合团队习惯和 Unity 生命周期重新评估。
- ET、GameFramework、YooAsset、HybridCLR 等框架类资料应落到具体工程问题：资源、网络、热更、配置、实体和流程管理。
- Asset Store 或第三方工具要先看维护状态、授权、源码可控性、运行时成本和是否能进入 CI。
- 教程类链接应转化成项目规范或检查清单，否则只保留在参考链接里。

## 资料整理方式

- 官方文档、Unity Learn、开发者社区作为优先入口。
- 性能文章按“问题类型”归档，例如 DrawCall、GC、渲染、UGUI、脚本、内存。
- 框架文章按“解决的问题”归档，例如 UI 架构、资源管理、热更新、ECS、PureMVC。
- 对站点不稳定、无标题、内容重复的链接只保留备注或移动到待清理。
- 每次从参考链接吸收一个主题后，应把正文补充为规则、流程、风险和检查清单。

## 检查清单

- 是否能从本页跳转到更细的 Unity 笔记，而不是在本页堆所有内容。
- 是否保留官方入口、稳定社区和高价值教程，删除低质量重复链接。
- UI 优化是否有可量化指标：打开耗时、DrawCall、Overdraw、GC、内存峰值。
- 框架和插件是否有实际项目落地场景，而不是只因为“看起来有用”就收录。
- 参考链接是否在正文末尾，正文是否表达自己的结论和实践规则。

## 资料收敛说明

- 本页已将原先 `42` 条参考链接压缩为 `10` 条核心引用，重复导航页、同类 API 细节页和低信噪比补充资料不再逐条公开保留。
- 正文已优先沉淀选型标准、排查流程、风险边界和常用工具定位，后续新增资料应继续转成正文结论，而不是直接堆叠链接。
- 文末只保留官方文档、代表性开源项目和少量仍值得回看的补充阅读。

## 参考链接

> 以下链接仅保留正文仍需回看的核心资料入口。

### 官方文档

- [Unity Learn](https://learn.unity.com/)
- [Unity Asset Store](https://assetstore.unity.com/zh-CN)

### 补充阅读

- [优化 UGUI 的 ScrollRect | Loading & Learning](https://qiankanglai.me/2015/08/15/LoopScrollRect/)
- [PureMVC Framework](https://puremvc.org/)
- [PureMVC -- 一款多平台 MVC 框架 - 简书](https://www.jianshu.com/p/47deaced9eb3)
- MVC、MVP 和 MVVM 的图示：概念对照仍值得回看，但原文站点对自动探测常返回 `403`
- [UGUI 不消耗 DRAW CALL 的 EventTrigger 接收器 - CSDN](https://blog.csdn.net/rcfalcon/article/details/51431734)
- [Unity 中文手册](https://docs.unity.cn/cn/current/Manual/index.html)
- [关于 Unity 渲染优化，你可能遇到这些问题 - UWA](https://blog.uwa4d.com/archives/QA_Rendering.html)
- [PureMVC 和 Unity3D 的 UGUI 制作员工管理系统实例 - 简书](https://www.jianshu.com/p/904b36ad37e2)
