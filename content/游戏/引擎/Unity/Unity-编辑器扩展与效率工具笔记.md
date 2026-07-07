---
title: Unity 编辑器扩展与效率工具笔记
tags:
  - Unity
  - 编辑器扩展
  - IMGUI
  - Odin
  - 工具链
status: reviewed
confidence: 0.7
visibility: public
last_curated: 2026-06-11
source_count: 97
---

## 结论

- 编辑器扩展的价值在于把重复、易错、难检查的人工流程变成可复用工具。
- Unity 编辑器工具主要分三类：Inspector/PropertyDrawer、EditorWindow/IMGUI、资源与编译流程工具。
- Odin Inspector 适合快速提升 Inspector 表达力，IMGUI / UI Toolkit 更适合定制化窗口和复杂编辑器。
- 工具链建设应关注迭代速度：编译耗时、Domain Reload、资源扫描、批量操作和错误可视化。

## 适用场景

- 配置、Prefab、ScriptableObject、技能、关卡、红点、UI 绑定等需要可视化编辑。
- 项目中存在大量重复设置、手工拖引用、手工导出、手工检查。
- 编译和 Domain Reload 时间过长，影响程序和策划迭代。
- 需要做资源规范检查、依赖分析、内存/硬盘大小统计或批量修复。

## IMGUI / EditorWindow

- IMGUI 适合快速搭建编辑器窗口，核心是 `OnGUI()` 的即时模式绘制。
- 工具窗口要避免每帧重做重 IO、全项目扫描或复杂反射。
- 需要长耗时处理时，应拆成异步、分帧或显式按钮触发。
- 事件处理要关注 `Event.current`，鼠标、键盘、拖拽、右键菜单都需要明确消费事件。
- 复杂工具要把 UI 绘制、数据模型、业务操作分层，避免全部堆在 `OnGUI()`。

## Inspector 与 Odin

- 自定义 Inspector 适合为特定组件提供更安全的编辑界面。
- PropertyDrawer 适合复用字段级展示逻辑。
- Odin 的 Attribute 能快速实现搜索、分组、按钮、条件显示和校验。
- Odin 适合提升开发效率，但核心数据结构不应强依赖展示层能力。
- 工具对多人协作友好时，要优先做校验、提示和自动修复，而不是只做漂亮界面。

### UI Toolkit 取舍

- UI Toolkit 更适合长期维护的复杂编辑器窗口，尤其是需要样式、布局和可扩展 UI 的工具。
- IMGUI 更适合快速原型和一次性内部工具，复杂状态管理会逐渐变难维护。
- Odin、IMGUI、UI Toolkit 的选择应按维护周期、复杂度、团队熟悉度和授权成本决定。
- 无论使用哪种 UI 技术，工具的数据模型和业务操作都不应绑定在绘制代码里。

## 资源与项目工具

- 资源大小统计工具可以帮助定位大图、大 Mesh、重复资源和异常导入设置。
- 批量工具应支持 dry-run 或预览模式，避免一次性误改大量资源。
- 资源扫描要记录路径、GUID、依赖关系和修改结果，方便追溯。
- Prefab、ScriptableObject、场景对象的批量修改要注意 Undo、Dirty 标记和保存策略。

## 编译与迭代效率

- Editor Iteration Profiler 可用于观察 Domain Reload、脚本编译和编辑器迭代耗时。
- Compilation Visualizer / DirtyCompiler 类工具适合分析程序集依赖和局部编译策略。
- 拆 asmdef 可以减少无关程序集重编译，但拆太细会增加依赖管理成本。
- 自动编译可在批量改代码或生成代码时临时关闭，但要确保恢复流程明确。
- `YIUI-UnityMCP` 这类 Unity MCP 配套脚本提供了 `compile-unity-flow`、控制台日志抓取和通用工具调用入口，适合把“停止 PlayMode -> 触发编译 -> 读取结果”这类流程串成可重复脚本。
- 如果项目里已经接入 Unity MCP，优先把编译、日志、菜单命令、断言类操作封装成统一脚本入口，而不是每次让 Agent 直接拼接临时命令。

## 工具落地流程

1. 明确工具要替代的人工流程，并记录当前耗时、错误率和涉及角色。
2. 先做最小可用版本，只覆盖最痛的 20% 操作。
3. 加入日志、预览、Undo、dry-run 和失败恢复，再扩大批量能力。
4. 接入项目规范检查或 CI，让工具结果可重复验证。
5. 收集团队反馈，优化入口、提示、默认值和错误恢复。

## 设计原则

- 工具默认行为要保守，危险操作必须二次确认。
- 所有批量修改都要支持日志、Undo 或可回滚方案。
- 编辑器工具不应污染运行时代码和包体。
- 工具入口要集中，不要散落在大量菜单项中。
- 对策划/美术使用的工具，要优先做错误提示和输入约束。

## 检查清单

- 是否有明确的工具入口和使用说明。
- 是否支持 Undo、Dirty、保存和失败回滚。
- 是否避免在 `OnGUI()` 中做重计算。
- 是否处理多选、空引用、Prefab Mode、嵌套 Prefab。
- 是否把 Editor-only 代码放在 Editor 目录或 Editor 程序集。
- 是否有资源扫描结果和自动修复日志。
- 是否衡量过工具本身对编译和 Domain Reload 的影响。


### Odin Inspector

- [云风的 BLOG: 跟踪数据结构的变更](https://blog.codingnow.com/2017/02/tracedoc.html)
- [云风的 BLOG: 游戏数据的展示](https://blog.codingnow.com/2022/05/gameplay_viewport.html)
- [Protocol Buffers与FlatBuffers效率对比 - coding my life - 博客园](https://www.cnblogs.com/coding-my-life/p/7296323.html)
- [Star, a Unity C# Editor Tutorial](https://catlikecoding.com/unity/tutorials/editor/star/)
- [Unity Odin从入门到精通（一）：定制特性详解-CSDN博客](https://blog.csdn.net/zjz520yy/article/details/119940363)
- [Odin常用记录_odin onvaluechanged-CSDN博客](https://blog.csdn.net/weixin_45029839/article/details/130361957?spm=1001.2014.3001.5502)
- [Unity 编辑器扩展二 Editor 自定义Inspector面板 - 简书](https://www.jianshu.com/p/27280468288c)
- [(原创) UnityEditor-Windwos编辑器与Inspector编辑器 - 技术专栏 - Unity官方开发者社区](https://developer.unity.cn/projects/5c8a27c6edbc2a007331fc2b)
- [Unity ContextMenu 扩展组件的环境菜单（在 Inspector 视图组件名称上的右击下拉菜单） - kingBook - 博客园](https://www.cnblogs.com/kingBook/p/14943141.html)
- [Unity编辑器环境在Inspector面板中显示变量 - jiahuafu - 博客园](https://www.cnblogs.com/jiahuafu/p/11162574.html)
- [How to make an enum-like Unity inspector drop-down menu from a string array with C#? - Stack Overflow](https://stackoverflow.com/questions/60864308/how-to-make-an-enum-like-unity-inspector-drop-down-menu-from-a-string-array-with)
- [How can I custom inspector a enum like as component Light - Questions & Answers - Unity Discussions](https://discussions.unity.com/t/how-can-i-custom-inspector-a-enum-like-as-component-light/151203/2)
- [Unity3d property drawer for automatically making enums flags into mask fields in the inspector.](https://gist.github.com/FFouetil/dd081256da0e3475d524d88b414076e3)
- [Epic的虚幻引擎 C++ 代码规范 | 虚幻引擎5.3文档](https://docs.unrealengine.com/5.3/zh-CN/epic-cplusplus-coding-standard-for-unreal-engine/)
- [Unity C# Editor Tutorials](https://catlikecoding.com/unity/tutorials/editor/)
- [云风的 BLOG: lockstep 网络游戏同步方案](https://blog.codingnow.com/2018/08/lockstep.html)
- [Road 2 Coding](https://www.r2coding.com/#/README?id=%e8%ae%be%e8%ae%a1%e6%a8%a1%e5%bc%8f)
- [(99+ 封私信 / 80 条消息) Unity OdinInspector全特性介绍（总结篇） - 知乎](https://zhuanlan.zhihu.com/p/409479682)
- [(99+ 封私信 / 80 条消息) Unity OdinInspector全特性介绍（五） - 知乎](https://zhuanlan.zhihu.com/p/409403629)
- [(99+ 封私信 / 80 条消息) Unity OdinInspector全特性介绍（四） - 知乎](https://zhuanlan.zhihu.com/p/409166888)
- [Unity OdinInspector全特性介绍（三） - 知乎](https://zhuanlan.zhihu.com/p/408785062)
- [Unity OdinInspector全特性介绍（二） - 知乎](https://zhuanlan.zhihu.com/p/408380221)
- [(99+ 封私信 / 80 条消息) Unity OdinInspector全特性介绍（一） - 知乎](https://zhuanlan.zhihu.com/p/408002569)
- [云风的 BLOG](https://blog.codingnow.com/)
- [musistudio/claude-code-router: Use Claude Code as the foundation for coding infrastructure, allowing you to decide ho...](https://github.com/musistudio/claude-code-router)

### 自定义编辑器窗口

- [How do I make a function delegate parameter optional? - Pipeline & Plugins / Editor Scripting - Epic Developer Commun...](https://forums.unrealengine.com/t/how-do-i-make-a-function-delegate-parameter-optional/366830)
- [api.unity.com](https://api.unity.com/v1/oauth2/authorize?client_id=unity_forum&response_type=code&redirect_uri=https%3A%2F%2Fforum.unity.com%2Fregister%2Fgenesis&state=FCO5y0CaZER3ZJC284HcBAsIStEYogMhOERp5SUR%3B%2Fthreads%2Fhow-to-make-a-multi-line-textfield-for-editor.153995%2F&prompt=NONE)
- [How do I add a scrolling input text box in an EditorWindow? (more info added) - Questions & Answers - Unity Discussions](https://discussions.unity.com/t/how-do-i-add-a-scrolling-input-text-box-in-an-editorwindow-more-info-added/131456)
- [EditorWindowの分割（Editor拡張） │ 空の缶詰](https://karanokan.info/2021/01/08/editorsplitarea/)
- [Unity之EditorUtility-DisplayDialog-五_unityeditor.editorutility.displaydialog-CSDN博客](https://blog.csdn.net/LIQIANGEASTSUN/article/details/42174671)
- [Download Archive](https://unity.com/releases/editor/archive#download-archive-2018)
- [UnityEditor知识 | 走停人生路](https://tonytang1990.github.io/2022/02/20/UnityEditor%E7%9F%A5%E8%AF%86/)
- [CoderGamester/mcp-unity: MCP Server to integrate Unity Editor game engine with different AI Model clients (e.g. Claud...](https://github.com/CoderGamester/mcp-unity)
- [arimger/Unity-Editor-Toolbox: Tools, custom attributes, drawers, hierarchy overlay, and other extensions for the Unit...](https://github.com/arimger/Unity-Editor-Toolbox)
- [Unity 6000.0.33](https://unity.com/releases/editor/whats-new/6000.0.33#installs)
- [XINCGer/UnityToolchainsTrick: 提供一些UnityEditor工具链开发的常用小技巧与示例(Provides some common tips and examples for developing the...](https://github.com/XINCGer/UnityToolchainsTrick?tab=readme-ov-file)
- [CodeGize-Unity编辑器开发，使用CustomPropertyDrawer实现枚举中文显示](http://www.codegize.com/post/38.html)
- [Unity - Manual: Editor Windows](https://docs.unity3d.com/Manual/editor-EditorWindows.html)
- [How to highlight or select an asset in project window from editor script? - Questions & Answers - Unity Discussions](https://discussions.unity.com/t/how-to-highlight-or-select-an-asset-in-project-window-from-editor-script/11257)
- [How can I find all instances of a Scriptable Object in the Project (Editor) - Questions & Answers - Unity Discussions](https://discussions.unity.com/t/how-can-i-find-all-instances-of-a-scriptable-object-in-the-project-editor/198002/2)
- [Unity3D 编辑器扩展 Editor中使用协程_unity 编辑器模式下开携程-CSDN博客](https://blog.csdn.net/piai9568/article/details/96895782)
- [TopOn-Unity-Demo-test/AnyThinkUnitySDK/Assets/Editor/IOS at master · toponteam/TopOn-Unity-Demo-test](https://github.com/toponteam/TopOn-Unity-Demo-test/tree/master/AnyThinkUnitySDK/Assets/Editor/IOS)
- [AsehesL/USubWindow: EditorWindow的多子窗口实现](https://github.com/AsehesL/USubWindow)
- [Misaka-Mikoto-Tech/MonoHook: hook C# method at runtime without modify dll file (such as UnityEditor.dll), works on Wi...](https://github.com/Misaka-Mikoto-Tech/MonoHook)
- [XINCGer/UnityToolchainsTrick: 提供一些UnityEditor工具链开发的常用小技巧与示例(Provides some common tips and examples for developing the...](https://github.com/XINCGer/UnityToolchainsTrick)
- [YouwantLee/Joker_Unity_SkillEditor: Joker 老师的 《ARPG系列课程》-->Unity技能编辑器源码，同步课程内容更新（已经Joker老师同意开源代码）](https://github.com/YouwantLee/Joker_Unity_SkillEditor)
- [akof1314/Unity-EditorInternalsVisibleDemo: Unity Editor Internals Visible](https://github.com/akof1314/Unity-EditorInternalsVisibleDemo)

### Editor 工具集合

- [Unity Loom 插件使用 - 知乎](https://zhuanlan.zhihu.com/p/23986194)
- [Unity中的 原生插件/平台交互 原理 - mydddfly - 博客园](https://www.cnblogs.com/jukan/p/8472959.html)
- [Unity3D插件开发Tips](http://blog.icodeten.com/game/2016/07/20/unity-plugins/)
- [【Unity编辑器开发】工具开发之Windows单选或多选文件踩坑记录 - 陌冉 - 博客园](https://www.cnblogs.com/moran-amos/p/11342095.html)
- [使用Unity Localization插件进行项目本地化实战详解 - 草莓♭布丁 - 博客园](https://www.cnblogs.com/strawberryPudding/p/17869493.html)
- [JiepengTan/GamesTanTools: 个人的 Unity 小工具箱，含一些个人比较常用的代码](https://github.com/JiepengTan/GamesTanTools?tab=readme-ov-file)
- [ChuKuang/Unity-Dev-Tools: 收集各种Unity开发的库](https://github.com/ChuKuang/Unity-Dev-Tools?tab=readme-ov-file)
- [needle-tools/compilation-visualizer: Unity Tool showing a timeline of assembly compilation. This is especially helpfu...](https://github.com/needle-tools/compilation-visualizer)
- [命令行工具 | Luban](https://www.datable.cn/docs/manual/commandtools)
- [Unity - Scripting API: AndroidExternalToolsSettings](https://docs.unity3d.com/2019.4/Documentation/ScriptReference/Android.AndroidExternalToolsSettings.html)
- [TopOn Unity3D 插件(2.0.0+)导入说明-TopOn | 帮助中心](https://help.toponad.net/cn/docs/hd01b0)
- [Unity-Technologies/com.unity.cinemachine: Smart camera tools for passionate creators](https://github.com/Unity-Technologies/com.unity.cinemachine)
- [hwaet/UnityProjectCloner: A tool to let the user to create a duplicate project that links back to the original, for m...](https://github.com/hwaet/UnityProjectCloner)
- [tinyantstudio/SimpleTimeLineWindow: Ready to Make Simple Unity's TimeLine Style Extension tools](https://github.com/tinyantstudio/SimpleTimeLineWindow)

### xNode 可视化节点

- [Unity编辑器扩展：使用xNode制作自己的可视化工具（2） - 知乎](https://zhuanlan.zhihu.com/p/364501563)
- [Unity xNode节点插件入门使用介绍1_xnode unity插件-CSDN博客](https://blog.csdn.net/oKaiGuo/article/details/120305976)
- [记一次Unity使用XNode插件时自动连线问题 - 不够自律的人 - 博客园](https://www.cnblogs.com/jbw752746541/p/14922214.html)
- [使用xNode制作可视化剧本编辑插件(1) | ydwj的游戏开发日记](https://auniquepig.com/2021/06/27/Story-Editor/)
- [Unity人工智能开发—基于xNode的图形化FSM教程 - 掘金](https://juejin.cn/post/7168347920184377352)
- [CodeGize-迷宫地图编辑器：Xnode插件实践](http://www.codegize.com/post/83.html)
- [Unity编辑器扩展：使用xNode制作自己的可视化工具（2） | ydwj的游戏开发日记](https://auniquepig.com/2021/06/27/Story-Editor2/)
- [Home · Siccity/xNode Wiki](https://github.com/Siccity/xNode/wiki)
- [Siccity/xNode: Unity Node Editor: Lets you view and edit node graphs inside Unity](https://github.com/Siccity/xNode)

### PropertyDrawer / Attribute

- [Unity - Scripting API: TextAreaAttribute.TextAreaAttribute](https://docs.unity3d.com/ScriptReference/TextAreaAttribute-ctor.html)
- [Unity编辑器拓展学习，（1）特性更新完毕 - 知乎](https://zhuanlan.zhihu.com/p/617999684)
- [Warl-G's Blog - Unity手册—Attribute汇总说明](https://warl.top/posts/Unity-Manual-Attribute/)

### ScriptableObject 工具

- [Unity - 编辑器扩展 - SouthBegonia - 博客园](https://www.cnblogs.com/SouthBegonia/p/12637261.html)
- [ScriptableObject（可编程对象）为团队和代码带来的六个好处 | Unity Blog](https://blog.unity.com/cn/engine-platform/6-ways-scriptableobjects-can-benefit-your-team-and-your-code)
- [Unity-Technologies/ml-agents: The Unity Machine Learning Agents Toolkit (ML-Agents) is an open-source project that en...](https://github.com/Unity-Technologies/ml-agents)

### 其他参考

- [Unity编辑器扩展_Unique_849997563的博客-CSDN博客](https://blog.csdn.net/qq_33461689/category_9529506.html)
- [unity编辑器扩展之美（一）_51CTO博客_unity编辑器](https://blog.51cto.com/u_15273495/2914714)
- [Unity编辑器扩展Texture显示选择框 - 盘子脸 - 博客园](https://www.cnblogs.com/plateFace/p/4282729.html)
- [Unity中实现字段/枚举编辑器中显示中文（中文枚举、中文标签） - Flamesky - 博客园](https://www.cnblogs.com/flamesky/p/15935234.html)
- [【Unity编辑器扩展实践】、通过代码查找所有预制_unity 代码查找所有预制体-CSDN博客](https://blog.csdn.net/qq_33461689/article/details/103773692)
- [Unity 编辑器扩展九 SerializedObject、SerializedProperty、SerializeField - 简书](https://www.jianshu.com/p/ef8bd9d9c6ea)
- [Unity编辑器扩展 - 慕飞 - 博客园](https://www.cnblogs.com/mufei/p/10077178.html)
- [Unity编辑器拓展之九：SearchField_unity searchfield-CSDN博客](https://blog.csdn.net/qq_26999509/article/details/80301320)
- [github 给力的unity编辑器扩展案例项目 - 知乎](https://zhuanlan.zhihu.com/p/563472021)
- [Unity项目多开（同时打开多个编辑器） - 哔哩哔哩](https://www.bilibili.com/read/cv24628888/)

## 参考链接

> 以下链接作为本笔记的资料来源保留。

### 链接分组

- [Editor GUI 事件拦截](https://www.xuanyusong.com/archives/3889)
- [脚本获取资源内存和硬盘大小](https://www.xuanyusong.com/archives/4263)

### GitHub 相关链接

- [Editor Iteration Profiler](https://github.com/Unity-Technologies/com.unity.editoriterationprofiler)
- [UnityDirtyCompiler](https://github.com/GameArki/UnityDirtyCompiler)
- [YIUI-UnityMCP Config README](https://github.com/LiShengYang-yiyi/YIUI-UnityMCP/blob/main/cn.etetet.yiuimcp/Config/README.md)

### 链接分组

- [Going deep with IMGUI and Editor customization](https://blog.unity.com/engine-platform/imgui-and-editor-customization)
- [How to Create a Custom Inspector with Odin](https://odininspector.com/tutorials/getting-started/how-to-create-a-custom-inspector-with-odin-)
- [Odin Searchable Attribute](https://odininspector.com/attributes/searchable-attribute)
- [雨松MOMO Unity3D 拓展编辑器](https://www.xuanyusong.com/archives/category/unity/unity3deditor)