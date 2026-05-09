---
title: Unity FMOD 音频接入笔记
tags:
  - Unity
  - FMOD
  - 音频
  - 移动端
---

## 结论

- FMOD 接入重点不只是播放声音，还包括 Bank 打包、事件路径、平台格式、热更新、内存占用和生命周期管理。
- `ERR_EVENT_NOTFOUND` 通常不是播放 API 本身的问题，而是 Bank 没加载、事件路径变更、GUID 不一致或构建产物没同步。
- 移动端要特别关注 Bank 加载策略、Android 音频格式、热更新下载和内存峰值。
- 音频系统需要和资源系统统一版本，不要让客户端代码、FMOD Studio 工程、Bank 文件和远端资源各自独立发布。

## 接入流程

1. 在 FMOD Studio 中建立事件、Bus、VCA 和 Bank。
2. 导出目标平台 Bank，并确认 Unity 工程中的 FMOD Settings 指向正确目录。
3. Unity 侧使用 `StudioEventEmitter` 或 RuntimeManager 播放事件。
4. 构建时将 Bank 文件作为 RawFile 或 StreamingAssets 资源处理。
5. 热更新场景中，先下载并校验 Bank，再加载对应事件。
6. 发布前检查事件路径、Bank 版本、平台格式和缺失资源。

## 事件与 Bank

- 事件播放前必须保证对应 Bank 已加载。
- 事件路径、GUID、Bank 文件之间要保持一致，改名或移动事件后必须重新导出 Bank。
- 使用字符串路径播放事件时要防止拼写错误，项目中更推荐封装常量或生成代码。
- 多 Bank 项目要明确依赖关系，避免播放事件时只加载了主 Bank，没有加载依赖 Bank。

## 常见错误

- `ERR_EVENT_NOTFOUND`：检查事件路径、Bank 是否加载、Bank 是否为最新导出、远端资源是否更新。
- `ERR_FORMAT`：检查 Android / iOS 平台音频格式、编码设置、FMOD 版本和目标平台导出配置。
- `StudioEventEmitter.isPlaying` 判断异常：确认事件实例生命周期、Stop 模式和组件是否重复创建。
- AssetBundle 导入 Bank 后生成 `TextAsset` 异常偏小：检查导入类型、文件后缀、资源构建规则和原始 Bank 是否被压缩或替换。

## 热更新与内存

- Bank 热更新应当走 RawFile 或独立文件路径，不建议作为普通 Unity 资源频繁反序列化。
- 下载后要做文件大小、Hash 和版本校验，避免加载半文件或旧文件。
- 大 Bank 不应在战斗中同步加载，应在进入场景前预加载或按模块拆分。
- 卸载 Bank 前要确认事件实例已经停止，避免引用仍在播放的资源。
- Android 上要关注 FMOD 热更新 Bank 的堆内存占用和 Native 内存，不要只看 Unity Managed Heap。

## 发布检查清单

- FMOD Studio 工程版本和 Unity 插件版本是否匹配。
- 各平台 Bank 是否重新导出。
- 事件路径是否生成或校验，避免手写路径漂移。
- 远端 Bank 是否和资源 Manifest 同步发布。
- 首包 Bank 与热更新 Bank 是否存在重复或版本冲突。
- Android / iOS 音频格式是否分别验证。
- Bank 加载、事件播放、停止、卸载是否有自动化冒烟测试。

## 参考链接

## 链接归档

- [[Unity-FMOD音频接入笔记链接归档]]: 外部链接已集中归档
