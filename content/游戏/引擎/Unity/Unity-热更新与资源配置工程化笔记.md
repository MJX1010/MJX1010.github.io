---
title: Unity 热更新与资源配置工程化笔记
tags:
  - Unity
  - 热更新
  - 资源管理
  - 配表
  - 工程化
status: reviewed
confidence: 0.7
visibility: public
last_curated: 2026-06-11
source_count: 29
---

## 结论

- Unity 热更新工程不要只看 `HybridCLR`，完整链路至少包含代码热更新、资源构建、资源分发、配置生成、版本管理和回滚策略。
- `HybridCLR` 解决 C# 代码热更新和 AOT 补充元数据问题；`YooAsset` / `xasset` 更偏资源打包、分包、加密、下载和加载；`Luban` 负责把策划配置转成客户端和服务器可读的数据与代码。
- 这几类工具应通过统一构建流水线串起来，而不是在 Unity Editor 里手工点按钮。
- 正式项目需要把“生成代码/导表/构建资源/构建包体/上传 CDN/生成版本清单/灰度发布”拆成可重复执行的命令。

## 典型链路

1. 策划修改 Excel / JSON / 配置源文件。
2. Luban 校验配置合法性，生成客户端代码、服务器代码和运行时数据。
3. Unity 编译业务程序集，HybridCLR 生成热更新 DLL、AOT 泛型补充元数据和必要的裁剪配置。
4. YooAsset / xasset 收集资源，按标签、分组、包裹或平台构建 AssetBundle / RawFile。
5. 构建系统生成资源版本、Manifest、补丁包和首包资源。
6. CDN / 对象存储上传远端资源，客户端按版本清单下载差异资源。
7. 客户端启动时检查版本，加载资源包、配置表、热更新程序集，再进入业务逻辑。

## 适用场景

- 项目需要在 IL2CPP 平台做代码热更新，同时要求配置和资源也可灰度发布。
- 策划配置更新频繁，且客户端、服务器、工具链需要共享同一份 schema。
- 包体要持续瘦身，需要首包/远端资源分离、增量更新和回滚能力。
- 团队希望把“点按钮”的人工流程替换为 CI 可重复命令。

## HybridCLR

### 解决的问题

- 在 IL2CPP 平台支持近似原生 C# 热更新。
- 避免 Lua / JS 方案带来的双语言维护成本。
- 支持热更新程序集与 Unity 原生工程协作。
- 处理 AOT 泛型、桥接函数、代码裁剪、包体和内存影响等 IL2CPP 相关问题。

### 安装关注点

- Unity 版本需要落在 HybridCLR 支持范围内，常见支持版本包括 `2019.4.x`、`2020.3.x`、`2021.3.x`、`2022.3.x`、`6000.x.y`。
- 低版本 Unity 可能需要先切换到特定补丁版本完成安装，再切回项目版本。
- Android / iOS 打包需要安装对应平台模块；Standalone 需要额外安装 IL2CPP Build Support。
- Windows 需要 Visual Studio 2019 或更高，并包含 Unity 游戏开发和 C++ 游戏开发组件；Mac 需要满足 Xcode 与 macOS 版本要求。
- 项目应固定 HybridCLR package 版本，避免不同机器、CI、分支使用不同实现。

### 工程建议

- 热更新程序集、AOT 程序集、第三方库程序集要明确分层，避免运行时代码引用关系混乱。
- AOT 补充元数据应纳入构建产物，不要依赖开发机临时生成。
- 代码裁剪配置要与实际使用的反射、序列化、泛型场景一起验证。
- 打包流程中要记录 Unity 版本、HybridCLR 版本、平台、Scripting Backend、API Compatibility Level。

## Luban

### 解决的问题

- 将配置源转换成多端一致的数据和代码。
- 支持客户端、服务器、工具链使用同一份 schema。
- 提供配置合法性校验，减少运行时才发现的策划数据错误。
- 支持多种 code target 和 data target，方便生成 C#、Java、Lua、JSON、bin 等产物。

### 命令行要点

- Luban 可以通过 `dotnet <path_of_luban.dll> [args]` 在 Windows、Linux、macOS 上运行。
- `--conf` 指定 Luban 配置文件，通常是必选项。
- `-t / --target` 指定生成目标。
- `-c / --codeTarget` 指定代码生成目标，可以指定多个。
- `-d / --dataTarget` 指定数据生成目标，可以指定多个。
- `--validationFailAsError` 适合在正式构建和 CI 中开启，让校验失败直接中断流水线。
- `--includeTag` / `--excludeTag` 可用于区分渠道、平台、环境或灰度数据。

### 表格设计建议

- 简单结构可以用限定列格式，字段清晰，适合多人维护。
- 复合结构可以使用流式格式、lite 格式或 json 格式，但要避免“漏填字段导致后续字段错位”的风险。
- 复杂嵌套结构应优先考虑可读性和校验能力，不要为了表格紧凑牺牲可维护性。
- 运行时读取格式要和项目性能要求匹配：客户端高频加载优先考虑二进制或预生成代码，编辑器工具可保留 JSON 便利性。

## YooAsset / xasset

### YooAsset 资源构建要点

- `Build Package` 用于选择资源包裹，适合多包或多业务模块管理。
- `Build Pipeline` 决定构建方式；Unity 2021.3 起推荐使用 `ScriptableBuildPipeline`。
- `EditorSimulateBuildPipeline` 可生成资源清单但不生成 Bundle，适合编辑器模拟真实加载环境。
- `RawFileBuildPipeline` 适合构建 Unity 无法识别的原生文件，例如 FMOD bank。
- `Build Version` 是补丁包目录和版本管理的关键字段，需要和发布系统对齐。
- `Clear Build Cache` 会重新构建所有资源；关闭后可使用增量打包提升构建速度。
- `Use Asset Depend DB` 可以利用资源依赖数据库提高资源收集速度。
- 加密可分资源包加密和 Manifest 加密，加载端必须配置对应解密逻辑。

### xasset 关注点

- xasset 偏向完整资产系统，覆盖打包、加载、分包、加密、边玩边下和云端分发。
- 分组配置可以控制资产交付时机，适合首包瘦身和远端资源下载。
- 统一的资产接口有利于多平台适配，减少不同平台写多套加载逻辑。
- 自动切片和加密打包可能改善 IO 和帧率平滑度，但需要项目实测验证。

## 版本与发布

- 每次发布至少要记录：客户端版本、资源版本、配置版本、热更 DLL 版本、HybridCLR 版本、Luban schema 版本。
- 资源版本和代码版本需要有兼容矩阵，避免旧客户端加载新配置或新资源崩溃。
- 配置表要支持回滚，远端资源要支持保留多个历史版本。
- CDN 上传完成后要做文件存在性、Hash、Manifest、下载速度和断点续传验证。
- 灰度发布时优先让小流量走新资源版本，确认崩溃率、下载失败率、热更加载错误后再全量。

## 排查流程

1. 先确认问题在代码热更、资源更新、配置导表、版本清单还是 CDN 发布。
2. 核对版本链路：客户端版本、资源版本、配置版本、热更 DLL 版本、schema 版本是否匹配。
3. 检查构建产物：热更 DLL、AOT 元数据、Manifest、补丁包、配置数据是否完整。
4. 检查发布原子性：资源是否已上传完成、Manifest 是否同步刷新、旧资源是否错误覆盖。
5. 用最小复现包验证下载、解密、加载、反序列化和热更入口加载顺序。
6. 修复后补齐 CI 断言，避免同类问题再次进入发布流程。

## CI 检查清单

- Luban 配置校验失败时是否会阻断构建。
- 生成代码是否被纳入编译并通过测试。
- HybridCLR 热更新 DLL、AOT 元数据、link.xml 是否都生成并进入产物。
- YooAsset / xasset 构建是否生成 Manifest、补丁包、首包资源和远端资源。
- Bundle 依赖、重复资源、包体大小和资源数量是否有报告。
- Android / iOS / WebGL 等目标平台是否各自生成独立资源版本。
- 资源上传后是否验证 Hash、大小、可下载性和 CDN 缓存刷新。

## 常见风险

- 只在本机 Editor 中验证成功，没有在真机 IL2CPP 环境验证。
- 热更新 DLL 引用了不该引用的主工程或 Editor-only 程序集。
- AOT 泛型补充不全，测试路径没覆盖到真实线上泛型组合。
- 配置表结构变更后没有处理旧客户端兼容。
- Bundle 分组过细导致请求数量过多，分组过粗又导致更新包过大。
- 加密策略只考虑安全，没有评估加载耗时和内存峰值。
- 版本清单和 CDN 资源不是原子发布，客户端可能读到半发布状态。


### Lua 热更方案

- [基于xlua和mvvm的unity框架_51CTO博客_mvvm框架](https://blog.51cto.com/u_15127577/2727374)
- [unity lua mvvm-掘金](https://juejin.cn/s/unity%20lua%20mvvm)
- [tolua/README.md at master · topameng/tolua](https://github.com/topameng/tolua/blob/master/README.md)
- [unity lua使用 mvvm 简述 - 知乎](https://zhuanlan.zhihu.com/p/523481872)
- [tenvick/hugula: unity3d lua databinding mvvm](https://github.com/tenvick/hugula/tree/master)
- [【Happy 指南】在 Unity3D 中使用 Lua 版的 PureMVC 实现一个完整的功能 - 匡 振 荣](http://zerokuang.com/%E6%B8%B8%E6%88%8F%E5%BC%80%E5%8F%91/%E3%80%90happy-%E6%8C%87%E5%8D%97%E3%80%91%E5%9C%A8-unity3d-%E4%B8%AD%E4%BD%BF%E7%94%A8-lua-%E7%89%88%E7%9A%84-puremvc-%E5%AE%9E%E7%8E%B0%E4%B8%80%E4%B8%AA%E5%AE%8C%E6%95%B4%E7%9A%84%E5%8A%9F%E8%83%BD/)
- [云风的 BLOG: Lua int64 的支持](https://blog.codingnow.com/2012/04/lua_int64.html)
- [yukuyoulei/ConfigAuto: 【ConfigAuto】Unity编辑器下通过配置匿名类，自动生成C#类并填充数据，省去序列化和反序列化的消耗。以前是不能热更，不往这方面想，能热更了为啥lua能当配置表C#就不行](https://github.com/yukuyoulei/ConfigAuto)

### HybridCLR / huatuo

- [(99+ 封私信 / 80 条消息) 如何评价C#热更框架HybridCLR? - 知乎](https://www.zhihu.com/question/519548488/answer/2551892061)
- [sunsvip/GF_X: Unity GameFramework + HybridCLR，简洁、高效、规范的开发工作流。从业十年的工作流积累，直击开发痛点，大量自动化编辑器扩展工具, 高效的自动化开发工作流](https://github.com/sunsvip/GF_X)
- [1｜HybridCLR——划时代的Unity原生C#热更新技术_HybridCLR(wolong) C# 热更新_UWA学堂](https://edu.uwa4d.com/lesson-detail/432/2122/0?isPreview=false)
- [XuToWei/GameDevelopmentKit: Unity双端开发工具，UnityGameFramework+ET+Luban+HybridCLR+UniTask，努力提供方便开发的工具](https://github.com/XuToWei/GameDevelopmentKit)
- [focus-creative-games/hybridclr_trial: HybridCLR 示例项目](https://github.com/focus-creative-games/hybridclr_trial)
- [focus-creative-games/hybridclr_unity: Unity package for HybridCLR](https://github.com/focus-creative-games/hybridclr_unity)

### 热更原理与对比

- [Unity C#热更新系列(2)-通用MonoBehaviourAdapter实现 - 知乎](https://zhuanlan.zhihu.com/p/455622312)

### ILRuntime

- [(99+ 封私信 / 80 条消息) 如何评价Unity的C#热更方案huatuo与ILRuntime的区别和优缺点？ - 知乎](https://www.zhihu.com/question/534297314/answer/2817560398)

### Addressable / AssetBundle

- [Unity资源管理 | 走停人生路](https://tonytang1990.github.io/2016/10/13/Unity%E8%B5%84%E6%BA%90/)
- [CDN 资源管理 YooAsset](https://uos.unity.cn/doc/cdn/yoo-asset)
- [(Unity 3D) 盘点 Github 上的那些 AssetBundle 框架_yooasset xasset-CSDN博客](https://blog.csdn.net/weixin_41292299/article/details/137928358)

## 参考链接

> 以下链接作为本笔记的资料来源保留。

### 链接分组

- [Luban 命令行工具](https://www.datable.cn/docs/manual/commandtools)
- [Luban 使用列限定与紧凑格式](https://www.datable.cn/docs/beginner/streamandcolumnformat)
- [xasset 官网](https://xasset.cc/)

### GitHub 相关链接

- [DangoRyn/UnityGameFramework_HybridCLR](https://github.com/DangoRyn/UnityGameFramework_HybridCLR)
- [It-Life/Deer_GameFramework_Wolong](https://github.com/It-Life/Deer_GameFramework_Wolong)
- [xasset/xasset](https://github.com/xasset/xasset?tab=readme-ov-file)

### 链接分组

- [YooAsset 资源构建](https://www.yooasset.com/docs/guide-editor/AssetBundleBuilder)
- [YooAsset 官网](https://www.yooasset.com/)
- [HybridCLR 安装](https://www.hybridclr.cn/docs/basic/install)

### GitHub 相关链接

- [GameFrameX/GameFrameX](https://github.com/GameFrameX/GameFrameX)