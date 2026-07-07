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
last_curated: 2026-06-11
source_count: 99
---

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


### UGUI 基础与组件

- [基于ugui的代码生成工具-腾讯游戏学堂](https://gwb.tencent.com/community/detail/128563)
- [1 | UGUI DrawCall 概念_详解UGUI DrawCall计算和Rebuild操作优化_UWA学堂](https://edu.uwa4d.com/lesson-detail/126/482/0?isPreview=false)
- [【Unity编辑器扩展基础】、EditorGUILayout （三）_editorguilayout.popup-CSDN博客](https://blog.csdn.net/qq_33461689/article/details/103193029)
- [A Detailed Guide to EditorGUILayout by Unity - Yarsa DevBlog](https://blog.yarsalabs.com/exploring-editorguilayout-by-unity-part1/)
- [UGUI研究院之LayoutGroup布局（八） | 雨松MOMO程序研究院](https://www.xuanyusong.com/archives/3336)
- [Unity编辑器扩展基础二、EditorGUILayout（二） - 简书](https://www.jianshu.com/p/887b539252fd)
- [EditorGUILayout-BeginFoldoutHeaderGroup - Unity 脚本 API](https://docs.unity3d.com/cn/2022.1/ScriptReference/EditorGUILayout.BeginFoldoutHeaderGroup.html)
- [GUILayout-BeginScrollView - Unity 脚本 API](https://docs.unity3d.com/cn/2019.4/ScriptReference/GUILayout.BeginScrollView.html)
- [Unity - Scripting API: UI.ScrollRect.verticalNormalizedPosition](https://docs.unity3d.com/2018.3/Documentation/ScriptReference/UI.ScrollRect-verticalNormalizedPosition.html)
- [【100个 Unity实用技能】☀️ | UGUI Text中加入超链接文本，可直接点击跳转-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/2335488)
- [UGUI最佳实践(4)-UI 控件优化 | 码了个球](https://huosk.github.io/2018/12/14/UguiOptimiseControl/)
- [Unity - Manual: Sprite (2D and UI) Import Settings reference](https://docs.unity3d.com/2022.3/Documentation/Manual/texture-type-sprite.html)
- [Unity UGUI系列二 材质 SpriteRenderer和Image - 简书](https://www.jianshu.com/p/3ccef33f51fc)
- [Unity UGUI系列一 Canvas 和 Canvas Group - 简书](https://www.jianshu.com/p/3a32e01a0bb1)
- [Unity中Mask和Layout性能分析和优化 - 知乎](https://zhuanlan.zhihu.com/p/627504485)
- [UGUI性能优化 - Bob的博客 | Bob Blog](https://chenanbao.github.io/2018/11/13/UGUI%E6%80%A7%E8%83%BD%E4%BC%98%E5%8C%96/)
- [Unity官方的UGUI优化指南读后总结 - 简书](https://www.jianshu.com/p/0be8b113824a)
- [UGUI性能优化总结 | 无境](https://www.drflower.top/posts/aad79bf1/#Canvas-Renderer)
- [如何快速优化手游性能问题？从UGUI优化说起 - 腾讯WeTest](https://wetest.qq.com/labs/272)
- [Unity中UGUI自适应三大组件以及锚点的使用_父物体身上挂载了horizontal layoutgroup,怎么改变子物体身上的锚点-CSDN博客](https://blog.csdn.net/weixin_44302602/article/details/117386347)
- [UGUI和NGUI的优化分享 - 赵青青 - 博客园](https://www.cnblogs.com/zhaoqingqing/p/6151758.html)
- [unity3D 编辑器扩展，MenuItem 和 ContextMenu 的用法和分析_contextmenuitem menuitem-CSDN博客](https://blog.csdn.net/swj524152416/article/details/54016488)
- [Unity-UGUI动态修改 RectTransform 的Left，Top，Right和Bottom值_recttransform left-CSDN博客](https://blog.csdn.net/z502768095/article/details/80606485)
- [Unity之EditorGUILayout-Enum、Popup、EnumMaskField_editorguilayout.enumpopup-CSDN博客](https://blog.csdn.net/LIQIANGEASTSUN/article/details/50095641)
- [Unity - Scripting API: GUILayout.Width](https://docs.unity3d.com/ScriptReference/GUILayout.Width.html)
- [【Unity3D-UGUI应用篇】（八）Image实现画线、画三角形、画正方形、画圆_51CTO博客_unity3d ugui](https://blog.51cto.com/itMonon/3796793)
- [Unity使用UGUI的Image在UI两个对象之间画线 - CodeAntenna](https://codeantenna.com/a/FArdvLK33q)
- [【Unity3d】如何解决错误:A script behaviour has a different serialization layout when loading_did you #ifdef unity_editor a se...](https://blog.csdn.net/u011355822/article/details/46551211)
- [3.3 UGUI 事件体系分析 · 博军一笑的个人主页](https://shenjun4unity.github.io/unityhtml/%E7%AC%AC3%E7%AB%A0%20UGUI/33-ugui-%E4%BA%8B%E4%BB%B6%E4%BD%93%E7%B3%BB%E5%88%86%E6%9E%90.html)
- [ecslite-unity-ugui/Editor.meta at master · Leopotam/ecslite-unity-ugui](https://github.com/Leopotam/ecslite-unity-ugui/blob/master/Editor.meta)
- [使用TextMeshPro实现打字机效果_textmeshpro 打字效果-CSDN博客](https://blog.csdn.net/h824612113/article/details/127674761?spm=1001.2014.3001.5502)
- [Unity UGUI Rect_unity recttransform.rect 有时是负数-CSDN博客](https://blog.csdn.net/weixin_43129170/article/details/121122275)
- [UGUI中的anchor和canvas(屏幕适配) - 雁过留声](https://blogml.top/2023/01/17/ugui-anchor-and-canvas/)
- [qiankanglai/LoopScrollRect: These scripts will make your UGUI ScrollRect reusing cells, to improve performance, loadi...](https://github.com/qiankanglai/LoopScrollRect)
- [Unity游戏开发——TextMeshPro的使用 - 知乎](https://zhuanlan.zhihu.com/p/84700094)
- [【Unity3D-UGUI系列】（二）Text文本组件详解_51CTO博客_unity ugui](https://blog.51cto.com/itMonon/3749533)
- [Making UI elements fit the size of their content | Unity UI | 2.0.0](https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/HOWTO-UIFitContentSize.html)
- [UI Image sorting layer? - Unity Forum](https://forum.unity.com/threads/ui-image-sorting-layer.470896/)
- [基于Unity TextMeshPro的图文混排和超链接功能 | 登峰造极者，殊途亦同归。](https://www.lfzxb.top/unity-textmeshpro-something/)
- [(UGUI图文混排一)TextMehPro(TMP)使用手册 - 知乎](https://zhuanlan.zhihu.com/p/457041220)
- [yasirkula/UnitySimpleFileBrowser: A uGUI based runtime file browser for Unity 3D (draggable and resizable)](https://github.com/yasirkula/UnitySimpleFileBrowser)
- [【Unity3D】UGUI的anchoredPosition锚点坐标_unity anchoredposition-CSDN博客](https://blog.csdn.net/qq_39574690/article/details/145554860?spm=1001.2014.3001.5502)
- [2丨WillRenderCanvases源码解读_UGUI深度研究之源码鉴赏_UWA学堂](https://edu.uwa4d.com/lesson-detail/79/99/0?isPreview=0)
- [LiShengYang-yiyi/YIUI: Unity3D UGUI Framework, 基于UI数据事件绑定为核心 数据驱动的UGUI框架, ETUI框架, ET框架官方推荐UI框架](https://github.com/LiShengYang-yiyi/YIUI)
- [MJX1010/UGUI-Editor: Unity UGUI editor tools,improve the efficiency of ui development.](https://github.com/MJX1010/UGUI-Editor)
- [gkjolin/UIEditor: Unity UGUI编辑器扩展工具集，提高界面开发效率，欢迎pull request或提需求哈](https://github.com/gkjolin/UIEditor)
- [sunsvip/PSD2UGUI_X: Convert psd file to ugui prefab, text, image, raw image, button, slider, scroll view, dropdown, t...](https://github.com/sunsvip/PSD2UGUI_X)

### UI 性能优化

- [Unity 构建过程的时间优化 | VyronLee's Notebook](https://vyronlee.com/2018/03/10/20180310-optimization-of-building-unity-project/)
- [Unity之UI性能优化相关 - 知乎](https://zhuanlan.zhihu.com/p/606929778)
- [优化移动游戏性能：来自Unity顶级工程师的Physics、UI和音频设置小贴士 | Unity Blog](https://blog.unity.com/cn/games/optimize-your-mobile-game-performance-get-expert-tips-on-physics-ui-and-audio-settings)
- [Unity优化备忘录 | Zuig Blog](https://blog.zuig.net/article/81d50f45-2c5d-4040-bd8f-28c6c6ec81e2)
- [Unity引擎渲染、UI、逻辑代码模块的量化分析和优化方法_UWA学堂](https://edu.uwa4d.com/course-intro/1/93?purchased=true&entrance=4)

### UI Toolkit / UIElements

- [Unity-Technologies/UIElementsExamples: Unity project containing examples to use UIElements in the Editor](https://github.com/Unity-Technologies/UIElementsExamples)
- [Unity-Technologies/ui-toolkit-manual-code-examples: Unity UI Toolkit documentation code examples](https://github.com/Unity-Technologies/ui-toolkit-manual-code-examples)
- [Unity - Manual: UI Toolkit](https://docs.unity3d.com/Manual/UIElements.html)
- [thekiwicoder0/UnityBehaviourTreeEditor: Behaviour Tree Editor for Unity built with UIToolkit](https://github.com/thekiwicoder0/UnityBehaviourTreeEditor)

### 屏幕适配与分辨率

- [游戏引擎 / Unity WebGL微信小游戏适配](https://developers.weixin.qq.com/minigame/dev/guide/game-engine/unity-webgl-transform.html)

### 动画与过渡

- [图解游戏引擎 - Unity动画原理（1）](https://mp.weixin.qq.com/s/Tq2LNqqJSeuInLeQgBHXGA)
- [CCLBStudio/DOTweenBuilder: A tool for the Unity DOTween plugin, allowing you to easily create complex effects without...](https://github.com/CCLBStudio/DOTweenBuilder)

### UI 框架与架构

- [Me-Maped/Gameframework-at-FairyGUI: UnityGameFramework+FairyGUI+YooAsset+HybridCLR+Luban+UniTask](https://github.com/Me-Maped/Gameframework-at-FairyGUI)
- [fairygui/FairyGUI-unity: A flexible UI framework for Unity](https://github.com/fairygui/FairyGUI-unity)

### 图集与资源管理

- [IcePower/X-ET7: X-ET 是一个融合了 ET, FairyGUI, luban, YooAsset 的缝合怪。](https://github.com/IcePower/X-ET7)
- [FlameskyDexive/ETPlus: ET8.1加强版，EUI+Luban+YooAsset](https://github.com/FlameskyDexive/ETPlus)
- [GameFrameX/GameFrameX: Unity前后端+管理端一体化解决方案-HybridCLR+YooAssets+LuBan+ProtoBuff+FairyGUI+DoTween+GameAnalytics+LitJson...](https://github.com/GameFrameX/GameFrameX)
- [资源构建 | YooAsset](https://www.yooasset.com/docs/guide-editor/AssetBundleBuilder)

### 其他参考

- [Unity3D研究院之3D界面与2D界面的结合（一百二十四） | 雨松MOMO程序研究院](https://www.xuanyusong.com/archives/4783)
- [GUITable | API Documentation | Odin Inspector for Unity](https://odininspector.com/documentation/sirenix.utilities.editor.guitable)
- [Syy9/EditorGUITable: A beautiful, easy-to-use and customizable table to display in the Unity Editor](https://github.com/Syy9/EditorGUITable)
- [（译）快速入门Unity编辑器拓展（IMGUI） | 登峰造极者，殊途亦同归。](https://www.lfzxb.top/unity-editor-crash-course/)
- [Unity编辑器拓展之自定义UnityToolbar_imguicontainer-CSDN博客](https://blog.csdn.net/u011428080/article/details/106689329)
- [Unity中的GUIStyle详解-CSDN博客](https://blog.csdn.net/u011428080/article/details/106676213)
- [【Unity3D编辑器扩展】Unity3D中实现UI界面控制，UI界面的显示和隐藏实现_unity实现数据变动实时在界面显示-CSDN博客](https://blog.csdn.net/q764424567/article/details/128496892)
- [2.0.1 【Unity】3D UI的实现方式_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1r54y1A7ia/?vd_source=5aeec11224a2dcfe0ebe94495dda445e)
- [2.0.1 【Unity】3D UI的实现方式 - 哔哩哔哩](https://www.bilibili.com/read/cv21808472/)
- [UI系统 | 3D Game Programming & Design](https://pmlpml.github.io/unity3d-learning/09-ui.html)
- [Unity使粒子特效支持UI的Mask遮罩_unity 粒子代码设置masking-CSDN博客](https://blog.csdn.net/capricorn1245/article/details/134684973)
- [unity 获取当前正在点击的UI_unity is click ui-CSDN博客](https://blog.csdn.net/weixin_44568736/article/details/121074391)
- [Unity - Scripting API: SearchField](https://docs.unity3d.com/ScriptReference/IMGUI.Controls.SearchField.html)
- [Unity在UI上绘制直线_unity ui 动态生成直线-CSDN博客](https://blog.csdn.net/zouxin_88/article/details/118185083)
- [Eastrall/Rosalina: Rosalina is a code generation tool for Unity's UI documents. It generates C# code-behind script ba...](https://github.com/Eastrall/Rosalina)
- [ILRuntime中的反射 — ILRuntime](https://ourpalm.github.io/ILRuntime/public/v1/guide/reflection.html)
- [Unity - Manual: iOS build settings](https://docs.unity3d.com/2019.4/Documentation/Manual/BuildSettingsiOS.html)
- [Error - Unity Forum](https://forum.unity.com/register/genesis?state=lhcrp4A3khbEPJumlMUBqU51MELlMTecVt3yg0fl%3B%2Fthreads%2Fwhat-reasons-could-cause-script-must-derive-from-monobehaviour-when-it-already-does-code-shown.588853%2F&error=login_required)
- [UnityWebRequest的初步使用及常用方法解析-CSDN博客](https://blog.csdn.net/vrmogui/article/details/124106217)
- [Unity之UI_unity ui-CSDN博客](https://blog.csdn.net/qq_45548042/article/details/121011915)
- [LiuOcean/Luban_Unity_GUI: Luban Unity GUI 工具](https://github.com/LiuOcean/Luban_Unity_GUI)
- [TeamSirenix/odin-serializer: Fast, robust, powerful and extendible .NET serializer built for Unity](https://github.com/TeamSirenix/odin-serializer)
- [yukuyoulei/Unity-GUI-Game-In-Single-File: Write Games In A Single Script File With Unity.](https://github.com/yukuyoulei/Unity-GUI-Game-In-Single-File)

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