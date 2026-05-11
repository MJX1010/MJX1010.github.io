---
title: Unity 框架与工具
tags:
  - 游戏开发
  - 引擎
  - unity
  - 框架
  - 工具链
---

## 核心结论

- Unity 框架选型不是“找一个大全框架”，而是围绕项目痛点拆分基础设施：资源、热更新、配置、异步、UI、网络、存档、编辑器工具和发布流水线。
- 工具链价值来自可重复、可验证和可维护，优先沉淀项目真实使用过、能进入 CI、能降低人工错误的能力。
- 官方资料和核心开源项目应作为长期入口，但正文必须记录自己的选型原则、接入边界和风险，而不是只保存链接。
- 框架越重，越要关注团队理解成本、升级成本、调试成本、包体/内存成本和与 Unity 版本的耦合。

## 适用场景

- 新项目需要搭建客户端基础设施，确定资源、热更、配置、UI、异步和编辑器工具路线。
- 老项目工具链分散，存在大量手工操作、重复脚本和不可复现构建。
- 团队想引入 HybridCLR、YooAsset、Luban、ET、GameFramework、UniTask、MemoryPack 等工具，但需要评估边界。
- 需要把长尾仓库筛选成真正可落地的项目规范。

## 框架分层模型

### 运行时基础层

- 异步：统一协程、Task、UniTask、取消令牌、超时和异常处理，不要混用多套异步模型。
- 资源：统一加载、卸载、依赖、缓存、引用计数、远端下载和版本管理。
- 配置：统一 schema、导表、校验、代码生成、运行时读取和多端一致性。
- 热更新：明确代码热更、资源热更、配置热更的边界和版本兼容策略。
- 日志与诊断：统一日志级别、远端上报、异常捕获和调试开关。

### 业务框架层

- UI 框架要解决窗口栈、层级、生命周期、打开参数、异步加载、事件解绑和返回逻辑。
- 网络框架要解决协议、重连、超时、心跳、序列化、错误码和弱网恢复。
- 实体/玩法框架要解决生命周期、组件划分、数据驱动、状态机、技能、Buff 或 ECS 边界。
- 存档和账号体系要明确本地数据、云端数据、加密、版本迁移和灰度兼容。

### 工具链层

- 资源扫描、引用查找、批量修改、Prefab 规范检查和自动修复应放入 Editor 工具或 CI。
- 构建流水线要覆盖导表、生成代码、打包资源、构建客户端、上传资源、生成 Manifest 和验证下载。
- 工具入口要统一，危险操作要支持 dry-run、日志、Undo 或回滚。

## 选型原则

- 优先解决明确问题，不因为工具热门就引入。
- 优先选择活跃、文档完整、源码可控、社区反馈明确的项目。
- 接入前用最小工程验证，不直接在主工程试错。
- 核心路径必须能被团队理解和调试，不能完全依赖黑盒工具。
- 引入框架后要写项目内二次规范，例如目录结构、命名、构建命令、升级流程和故障处理。

## 常见工具定位

- `HybridCLR`：解决 IL2CPP 平台 C# 代码热更新和 AOT 补充元数据问题。
- `YooAsset` / `xasset`：解决资源构建、版本、下载、加载、加密和分包问题。
- `Luban`：解决配置 schema、代码生成、数据导出和多端一致性问题。
- `UniTask`：统一 Unity 异步模型，降低协程回调和 Task 混用成本。
- `MemoryPack`：面向高性能序列化，但要评估版本兼容和数据迁移。
- `GameFramework` / `ET`：提供较完整的工程组织范式，适合学习或二次裁剪，不宜无脑全量引入。
- `Cinemachine`、`Spine`、`FairyGUI`、行为树、节点编辑器等应按玩法需求独立评估。

## 接入流程

1. 写清楚要解决的问题和不解决的问题，例如只解决资源加载，不顺带重构 UI 框架。
2. 建最小验证工程，验证 Unity 版本、平台、构建、包体、性能和调试体验。
3. 设计接入边界，封装项目自己的接口，避免业务代码直接散落依赖第三方 API。
4. 接入 CI，保证生成代码、构建资源、运行测试和上传产物可重复。
5. 写项目内文档，记录目录、命令、常见错误、升级方式和回滚方式。
6. 灰度替换旧流程，避免一次性切换导致所有模块同时不可控。

## 风险清单

- 框架过度封装导致新人无法理解 Unity 原生生命周期。
- 工具链只能在个人电脑运行，CI 或打包机无法复现。
- 资源、代码、配置版本没有统一，线上出现兼容事故。
- 三方仓库停止维护，Unity 升级后无法构建。
- 生成代码没有纳入编译校验，运行时才发现接口漂移。
- 编辑器工具直接修改大量资源但没有日志和回滚。

## 后续长尾筛选规则

- 保留官方仓库、项目已实用仓库、能进入 CI 的生产工具。
- 对 Demo、教程、插件仓库，只在能转化成项目规范时吸收进正文。
- 对破解、授权风险或来源不清的工具不进入公开知识库正文。
- 每次新增链接都要标记用途：学习、选型、接入、排查、废弃。

## 参考链接

> 以下链接作为本笔记的资料来源保留。

### 链接分组

- [ByteTech: ECS 架构设计介绍](https://bytetech.info/videos/set/7288660699621359674/7288640177994465292)
- [ByteTech: 小游戏&直播客户端内存优化实践](https://bytetech.info/videos/set/7581092880536125483/7579539088949182516)
- [Luban: 流式格式 + 紧凑格式](https://www.datable.cn/docs/beginner/streamandcolumnformat)
- [Luban: 命令行工具](https://www.datable.cn/docs/manual/commandtools)

### GitHub 相关链接

- [focus-creative-games/hybridclr_unity](https://github.com/focus-creative-games/hybridclr_unity)
- [focus-creative-games/luban](https://github.com/focus-creative-games/luban)
- [focus-creative-games/luban_examples](https://github.com/focus-creative-games/luban_examples)
- [EllanJiang/UnityGameFramework](https://github.com/EllanJiang/UnityGameFramework)
- [tuyoogame/YooAsset](https://github.com/tuyoogame/YooAsset)
- [Unity-Technologies/UnityCsReference](https://github.com/Unity-Technologies/UnityCsReference)
- [Unity-Technologies/com.unity.cinemachine](https://github.com/Unity-Technologies/com.unity.cinemachine)
- [EsotericSoftware/spine-runtimes](https://github.com/EsotericSoftware/spine-runtimes)
- [fairygui/FairyGUI-unity](https://github.com/fairygui/FairyGUI-unity)
- [thekiwicoder0/UnityBehaviourTreeEditor](https://github.com/thekiwicoder0/UnityBehaviourTreeEditor)
- [XINCGer/UnityToolchainsTrick](https://github.com/XINCGer/UnityToolchainsTrick)
- [mob-sakai/CSharpCompilerSettingsForUnity](https://github.com/mob-sakai/CSharpCompilerSettingsForUnity)

### 链接分组

- [ByteTech: iOS 内存工具分享与实践](https://bytetech.info/videos/set/7581092880536125483/7574343259054178331)
- [Unity 官方 Cinemachine 产品页](https://unity.com/cn/features/cinemachine)
- [Unity 手册：事件函数执行顺序](https://docs.unity3d.com/cn/2022.3/Manual/ExecutionOrder.html)
- [Unity 手册总入口](https://docs.unity3d.com/Manual/index.html)
- [Android Developers: 使用 Unity 制作游戏](https://developer.android.com/games/engines/unity/unity-on-android?hl=zh-cn#16-kb-page-support)
- [ByteTech: Unity il2cpp 编译流程分享](https://bytetech.info/videos/7134694941254483976)
- [ByteTech: Unity il2cpp 编译流程分享（下）](https://bytetech.info/videos/7134657562808418340)
- [catlikecoding tutorials](https://catlikecoding.com/unity/tutorials/)
- [PlayableDirector 脚本 API](https://docs.unity3d.com/6000.2/Documentation/ScriptReference/Playables.PlayableDirector.html)
- [IL2CPP clang arguments 讨论](https://discussions.unity.com/t/il2cpp-build-target-clang-arguments/942288/5)
- [UWA 社区搜索：ET](https://community.uwa4d.com/search?keyword=ET&scope=1)

### AI 相关链接

- [Unity Android 要求与兼容性](https://docs.unity3d.com/6000.1/Documentation/Manual/android-requirements-and-compatibility.html?utm_source=chatgpt.com)

### GitHub 相关链接

- [Cysharp/UniTask](https://github.com/Cysharp/UniTask)
- [Cysharp/MemoryPack](https://github.com/Cysharp/MemoryPack)
- [focus-creative-games/hybridclr](https://github.com/focus-creative-games/hybridclr)
- [egametang/ET](https://github.com/egametang/ET)
- [LiShengYang-yiyi/YIUI](https://github.com/LiShengYang-yiyi/YIUI)
- [Siccity/xNode](https://github.com/Siccity/xNode)
- [Siccity/Dialogue](https://github.com/Siccity/Dialogue)
- [ad313/SourceGenerator.Template](https://github.com/ad313/SourceGenerator.Template)
