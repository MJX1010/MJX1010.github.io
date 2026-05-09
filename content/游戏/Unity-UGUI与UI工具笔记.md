---
title: Unity UGUI 与 UI 工具笔记
tags:
  - Unity
  - UGUI
  - UI
  - 工具链
---

## 结论

- UGUI 优化不是单点问题，通常要同时处理事件系统、布局重建、滚动列表复用、图集规范、字体资源和 UI 生产流程。
- UI 工具链的核心目标是减少重复劳动：PSD 转 Prefab、批量检查组件、自动绑定代码、图文混排、图表控件和原型调试。
- 高频 UI 的性能瓶颈常见于 `Canvas` 重建、`Layout` 递归计算、`ScrollRect` 大量实例化、字体纹理膨胀和过度使用 Mask。
- 复杂 UI 项目应建立“资源规范 + Prefab 规范 + 自动检查 + 运行时复用”的闭环。

## 适用场景

- 主界面、背包、排行榜、聊天、活动页等大量 UI 面板。
- 滚动列表元素多、打开卡顿、滑动掉帧或内存持续增长。
- UI 制作依赖人工切图、拖组件、绑定脚本，效率低且容易出错。
- TextMeshPro 图文混排、超链接、动态字体、图集管理问题频繁出现。

## 运行时优化

- 滚动列表应优先使用 Cell 复用，避免一次性实例化全部条目。
- 高频变化元素应拆到独立 `Canvas`，避免小范围变化触发大 Canvas 重建。
- 能固定尺寸的 UI 尽量避免频繁 `ContentSizeFitter`、`LayoutGroup` 和嵌套布局。
- 图片资源应进入图集，避免碎图过多造成加载、DrawCall 和管理成本。
- 遮罩、半透明、粒子和复杂 Shader 会增加 Overdraw，需要配合 Frame Debugger 检查。
- 动态字体纹理要设置合理 fallback 和字符集策略，避免字体贴图无限膨胀。

## 事件系统

- `EventSystem` 负责输入事件分发，项目中通常只应存在一个有效事件系统。
- 多摄像机、多 Canvas、世界空间 UI 要明确 `GraphicRaycaster`、排序层和事件相机。
- UI 点击穿透问题通常来自 Raycast Target、CanvasGroup、遮罩层级或 GraphicRaycaster 设置错误。
- 运行时调试 UI 事件时，优先检查是否有透明 Image 拦截、父节点 CanvasGroup 禁用交互或排序层覆盖。

## 工具链

- `PSD2UGUI` 适合把设计稿批量转换为 UGUI Prefab，但需要统一图层命名、组件映射和字体规范。
- `UGUI-Editor` / `UIEditor` 类工具适合做批量替换、引用检查、组件规范化和面板生成。
- `LoopScrollRect` 适合大列表复用，使用前要明确 Cell 尺寸、复用生命周期和数据刷新边界。
- `XCharts` 适合做图表类 UI，需要关注动态数据刷新频率和图表元素数量。
- `ProtoGUI` 适合原型和调试窗口，不宜直接替代正式 UI 框架。

## TextMeshPro 与图文混排

- 图文混排应统一定义 sprite asset、字体 asset、标签语法和点击区域。
- 超链接要明确点击命中范围、事件回调、颜色样式和多语言换行策略。
- 动态表情、道具图标、富文本标签要避免在运行时频繁创建材质或字体资源实例。
- 多语言项目应提前规划字体 fallback、CJK 字符集和动态加载策略。

## 检查清单

- 是否存在一个页面多个 Canvas 无意义嵌套。
- 是否有大列表未做复用。
- 是否有 UI Sprite 误开 Mipmap 或 Read/Write。
- 是否有动态字体纹理异常增大。
- 是否有大量 Raycast Target 没有必要地开启。
- 是否有 UI 打开时同步加载大图或大量 Prefab。
- 是否有 Mask、透明图和粒子导致严重 Overdraw。
- 是否有设计稿转 Prefab 的命名和组件规范。

## 参考链接

## 链接归档

- [[Unity-UGUI与UI工具笔记链接归档]]: 外部链接已集中归档
