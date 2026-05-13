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
source_count: 42
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

## 参考链接

> 以下链接作为本笔记的资料来源保留。

### 链接分组

- [ET 社区](https://et-framework.cn/)
- [DOTween (HOTween v2)](https://dotween.demigiant.com/)
- [深入浅出聊优化：从 Draw Calls 到 GC - 慕容小匹夫 - 博客园](https://www.cnblogs.com/murongxiaopifu/p/4284988.html)
- [U3D DrawCall 优化手记 - 深圳-宝爷 - 博客园](https://www.cnblogs.com/ybgame/p/3588795.html)
- [分类：ECS 入门 - 笨木头的博客](https://www.benmutou.com/archives/category/ECS入门)
- [不懂 PureMVC 框架问题？深入解读看完必会(上) - 知乎](https://zhuanlan.zhihu.com/p/135426258)
- [PureMVC -- 一款多平台 MVC 框架 - 简书](https://www.jianshu.com/p/47deaced9eb3)
- [PureMVC（AS3）剖析：实例 - 吴秦 - 博客园](https://www.cnblogs.com/skynet/archive/2013/01/29/2881244.html)
- [Unity Asset Store](https://assetstore.unity.com/zh-CN)
- [团结引擎手册：商标和使用条款](https://docs.unity.cn/cn/tuanjiemanual/Manual/TermsOfUse.html)
- [Unity 开发者社区](https://developer.unity.cn/)
- [Unity 开发者联盟](https://www.u3dchina.com/)
- [Unity Learn](https://learn.unity.com/)
- [Star, a Unity C# Editor Tutorial - Catlike Coding](https://catlikecoding.com/unity/tutorials/editor/star/)
- [Odin Inspector and Serializer](https://odininspector.com/)
- [Find Reference 2 - Free Download | Dev Asset Collection](https://unityassetcollection.com/find-reference-2-free-download/)
- [Unity UGUI —— 无限循环 List - 博客园](https://www.cnblogs.com/fly-100/p/4549354.html)
- [Unity UI(uGUI) 源码学习笔记(一) Button - lvmingbei](https://lvmingbei.hatenablog.com/entry/2015/05/12/194948)
- [Unity 进阶技巧：RectTransform 详解 - 简书](https://www.jianshu.com/p/dbefa746e50d)
- [UGUI batch 规则和性能优化 - 博客园](https://www.cnblogs.com/fly-100/p/5488757.html)
- [UGUI 性能优化 - 桫椤 - 博客园](https://www.cnblogs.com/suoluo/p/5417152.html)
- [UGUI 表情系统解决方案（微信）](https://mp.weixin.qq.com/s?__biz=MzI3MzA2MzE5Nw%3D%3D&mid=2668904827&idx=1&sn=b3ef1e990c46d90bcb18480b4714a3dc&chksm=f1c9ed09c6be641f2c2e664478608c293eea5c0e612c2b7a7313ff75b87382ac453eb377eef8&mpshare=1&srcid=1124rYS5c8Dcbzv6rQGAHExA)
- [Unity GUI(uGUI) 使用心得与性能总结 - 简书](https://www.jianshu.com/p/061e67308e5f)
- [关于 Unity 渲染优化，你可能遇到这些问题 - UWA](https://blog.uwa4d.com/archives/QA_Rendering.html)
- [Unity – ValueType & boxing with Dictionary - NaCl's Blog](https://fredxxx123.wordpress.com/2017/05/08/unity-valuetype-boxing-with-dictionary/)
- [PureMVC 和 Unity3D 的 UGUI 制作员工管理系统实例 - 简书](https://www.jianshu.com/p/904b36ad37e2)
- [理论 + 实践！如何在 Unity 中应用 PureMVC 框架？ - GameRes](https://www.gameres.com/822910.html)
- [Unity Shader 编程开发系列教程 - 直线网](https://www.linecg.com/video/play31170.html)
- [【游戏开发】Excel 表格批量转换成 lua 的转表工具 - 博客园](https://www.cnblogs.com/msxh/p/8539108.html)
- [MVC、MVP 和 MVVM 的图示 - 阮一峰](https://www.ruanyifeng.com/blog/2015/02/mvcmvp_mvvm.html)

### AI 相关链接

- [UGUI ScrollRect 优化 - CSDN](https://blog.csdn.net/subsystemp/article/details/46912479)
- [UGUI 不消耗 DRAW CALL 的 EventTrigger 接收器 - CSDN](https://blog.csdn.net/rcfalcon/article/details/51431734)
- [优化 UGUI 的 ScrollRect | Loading & Learning](https://qiankanglai.me/2015/08/15/LoopScrollRect/)
- [unity3d 优化总结篇 - CSDN](https://blog.csdn.net/sgnyyy/article/details/41621039)
- [Unity + NGUI 性能优化方法总结 - CSDN](https://blog.csdn.net/zzxiang1985/article/details/43339273)
- [Unity 中性能优化的一些经验与总结（脚本优化篇）- CSDN](https://blog.csdn.net/u013709166/article/details/54934931)
- [Unity3d 开发：编辑器 DrawCall 参数解析 - CSDN](https://blog.csdn.net/fansongy/article/details/51025325)
- [Unity PureMVC 框架解读(上) - CSDN](https://blog.csdn.net/qq_29579137/article/details/73692842)
- [Unity PureMVC 框架解读(下) - CSDN](https://blog.csdn.net/qq_29579137/article/details/73717882)
- [PureMVC 框架解读（下）- CSDN](https://blog.csdn.net/zzwdkxx/article/details/82015101)
- [Unity 框架：PureMVC 在 Unity 中的简单使用 - CSDN](https://blog.csdn.net/lyh916/article/details/50076463)
- [Unity 框架：PureMVC 基础 - CSDN](https://blog.csdn.net/lyh916/article/details/50058207)
