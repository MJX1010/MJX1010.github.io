---
title: Unity 框架与工具
tags:
  - 游戏开发
  - 引擎
  - unity
  - 框架
  - 工具链
---
## 说明
- 用途：沉淀 Unity 客户端开发中可长期复用的框架、工具链、官方文档与学习入口
- 收录原则：优先保留官方仓库、核心开源项目、稳定教程和项目中高概率复用的能力入口

## 一、核心框架与基础设施

- [Cysharp/UniTask](https://github.com/Cysharp/UniTask): Unity 常用高性能 async/await 基础库
- [Cysharp/MemoryPack](https://github.com/Cysharp/MemoryPack): 面向 C# / Unity 的高性能序列化方案
- [focus-creative-games/hybridclr](https://github.com/focus-creative-games/hybridclr): Unity 热更核心方案
- [focus-creative-games/hybridclr_unity](https://github.com/focus-creative-games/hybridclr_unity): HybridCLR Unity 包入口
- [focus-creative-games/luban](https://github.com/focus-creative-games/luban): 配表与代码生成核心项目
- [focus-creative-games/luban_examples](https://github.com/focus-creative-games/luban_examples): Luban 示例项目
- [EllanJiang/UnityGameFramework](https://github.com/EllanJiang/UnityGameFramework): UnityGameFramework 主仓库
- [egametang/ET](https://github.com/egametang/ET): ET 框架主仓库
- [tuyoogame/YooAsset](https://github.com/tuyoogame/YooAsset): Unity 资源管理系统
- [Unity-Technologies/UnityCsReference](https://github.com/Unity-Technologies/UnityCsReference): Unity C# 参考源码

## 二、UI / 编辑器扩展 / 运行时工具

- [Unity-Technologies/com.unity.cinemachine](https://github.com/Unity-Technologies/com.unity.cinemachine): Cinemachine 官方仓库
- [Unity 官方 Cinemachine 产品页](https://unity.com/cn/features/cinemachine): Cinemachine 功能总览
- [EsotericSoftware/spine-runtimes](https://github.com/EsotericSoftware/spine-runtimes): Spine 运行时
- [fairygui/FairyGUI-unity](https://github.com/fairygui/FairyGUI-unity): FairyGUI Unity 版
- [LiShengYang-yiyi/YIUI](https://github.com/LiShengYang-yiyi/YIUI): YIUI 框架入口
- [Siccity/xNode](https://github.com/Siccity/xNode): Unity 节点编辑器
- [Siccity/Dialogue](https://github.com/Siccity/Dialogue): 节点式对话系统
- [thekiwicoder0/UnityBehaviourTreeEditor](https://github.com/thekiwicoder0/UnityBehaviourTreeEditor): 行为树编辑器
- [XINCGer/UnityToolchainsTrick](https://github.com/XINCGer/UnityToolchainsTrick): UnityEditor 工具链技巧集合
- [mob-sakai/CSharpCompilerSettingsForUnity](https://github.com/mob-sakai/CSharpCompilerSettingsForUnity): Unity C# 编译器设置工具
- [ad313/SourceGenerator.Template](https://github.com/ad313/SourceGenerator.Template): Source Generator 模板项目

## 三、性能 / 构建 / 排查资料

- [Unity 手册：事件函数执行顺序](https://docs.unity3d.com/cn/2022.3/Manual/ExecutionOrder.html): 生命周期与执行顺序的稳定参考
- [Unity 手册总入口](https://docs.unity3d.com/Manual/index.html): Unity 6 文档入口
- [Unity Android 要求与兼容性](https://docs.unity3d.com/6000.1/Documentation/Manual/android-requirements-and-compatibility.html?utm_source=chatgpt.com): Android 平台构建要求
- [Android Developers: 使用 Unity 制作游戏](https://developer.android.com/games/engines/unity/unity-on-android?hl=zh-cn#16-kb-page-support): Unity on Android 官方文档
- [ByteTech: ECS 架构设计介绍](https://bytetech.info/videos/set/7288660699621359674/7288640177994465292): ECS 主题学习材料
- [ByteTech: Unity il2cpp 编译流程分享](https://bytetech.info/videos/7134694941254483976): IL2CPP 相关学习视频
- [ByteTech: Unity il2cpp 编译流程分享（下）](https://bytetech.info/videos/7134657562808418340): IL2CPP 补充视频
- [catlikecoding tutorials](https://catlikecoding.com/unity/tutorials/): Unity / Shader 高质量教程
- [PlayableDirector 脚本 API](https://docs.unity3d.com/6000.2/Documentation/ScriptReference/Playables.PlayableDirector.html): Timeline / Playables 参考
- [IL2CPP clang arguments 讨论](https://discussions.unity.com/t/il2cpp-build-target-clang-arguments/942288/5): IL2CPP 构建参数讨论
- [UWA 社区搜索：ET](https://community.uwa4d.com/search?keyword=ET&scope=1): ET / Unity 性能社区入口
- [ByteTech: iOS 内存工具分享与实践](https://bytetech.info/videos/set/7581092880536125483/7574343259054178331): iOS 内存排查专题
- [ByteTech: 小游戏&直播客户端内存优化实践](https://bytetech.info/videos/set/7581092880536125483/7579539088949182516): 客户端优化专题

## 四、内部长期知识入口

- [YIUI 基础组件](https://bytedance.larkoffice.com/wiki/RioNwVFDdiKzZwkFvy9cRAJKnBc?sheet=V62m5h): 明确主题的 UI 组件知识页
- [YIUI](https://ai.feishu.cn/wiki/ES7Gwz4EAiVGKSkotY5cRbTznuh): YIUI 相关知识入口
- [龙2 Luban 策划使用简要指南](https://moonton.feishu.cn/wiki/ZCGwwX5YYiDWO6kUkKMcmyvhnDc): 配表工具使用页

## 五、Luban 官方文档（datable.cn）

- [Luban: 流式格式 + 紧凑格式](https://www.datable.cn/docs/beginner/streamandcolumnformat): 配表行为入门
- [Luban: 命令行工具](https://www.datable.cn/docs/manual/commandtools): 命令行使用

## 五、后续可补充的长尾方向

- 当前原始文件中还有大量 Unity 插件仓库、Demo 仓库、编辑器扩展仓库未逐条吸收
- 下次二筛时建议只继续保留三类：
  - 官方仓库
  - 项目已实用过的仓库
  - 能明显提升生产效率的工具类仓库
