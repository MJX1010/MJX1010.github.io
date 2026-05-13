---
title: Unity FMOD 音频接入笔记
tags:
  - Unity
  - FMOD
  - 音频
  - 移动端
status: reviewed
confidence: 0.7
visibility: public
last_curated: 2026-05-13
source_count: 5
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

## 工程规范

- FMOD Studio 工程、Unity 工程和资源发布系统要共享同一套版本号，不要各自独立发布。
- 事件命名建议按业务域分组，例如 `ui/`、`battle/`、`music/`、`ambient/`，减少后续迁移成本。
- 事件路径、GUID 和 Bank 依赖应生成校验报告，至少在 CI 中检查“代码引用的事件都存在”。
- 公共音效、场景音乐、角色音效和活动音效适合拆成不同 Bank，便于按场景加载和卸载。
- 面向策划或音频设计师的导出流程应尽量按钮化或命令化，减少手动复制 Bank 文件。

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

## 排查流程

1. 先确认问题类型：事件不存在、声音不播放、声音残留、格式错误、内存升高还是切后台异常。
2. 检查 Bank 是否加载：Master、Strings、业务 Bank 和依赖 Bank 是否都在当前平台目录。
3. 检查事件路径和 GUID：确认代码引用、FMOD Studio、导出的 Strings Bank 是同一版本。
4. 检查资源发布：首包 Bank、热更新 Bank、Manifest、CDN 文件和本地缓存是否一致。
5. 检查生命周期：事件实例是否重复创建、是否停止、是否释放、场景切换是否卸载 Bank。
6. 在真机上验证内存和音频格式，尤其是 Android 热更新 Bank 和 iOS 前后台切换。

## 发布检查清单

- FMOD Studio 工程版本和 Unity 插件版本是否匹配。
- 各平台 Bank 是否重新导出。
- 事件路径是否生成或校验，避免手写路径漂移。
- 远端 Bank 是否和资源 Manifest 同步发布。
- 首包 Bank 与热更新 Bank 是否存在重复或版本冲突。
- Android / iOS 音频格式是否分别验证。
- Bank 加载、事件播放、停止、卸载是否有自动化冒烟测试。

## 参考链接

> 以下链接作为本笔记的资料来源保留。

### 链接分组

- [FMOD User Guide](https://www.fmod.com/docs/2.00/unity/user-guide.html)
- [FMOD 热更新在安卓下的堆内存占用](https://blog.uwa4d.com/archives/TechSharing_202.html)
- [ERR_EVENT_NOTFOUND 讨论](https://qa.fmod.com/t/err-event-notfound-the-requested-event-bus-or-vca-could-not-be-found/15391/6)
- [StudioEventEmitter isPlaying](https://www.fmod.com/docs/2.00/unity/api-studioeventemitter.html)

### AI 相关链接

- [检查 FMOD event 是否播放](https://qa.fmod.com/t/can-unity-check-if-certain-fmod-event-is-playing/15342/7)
