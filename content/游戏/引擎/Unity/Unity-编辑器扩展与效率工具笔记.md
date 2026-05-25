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
last_curated: 2026-05-22
source_count: 10
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
