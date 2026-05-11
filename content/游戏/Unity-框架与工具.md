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
- 需要把补充仓库筛选成真正可落地的项目规范。

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

## 后续补充资料筛选规则

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
- [Android Developers: 使用 Unity 制作游戏](https://developer.android.com/games/engines/unity/unity-on-android?hl=zh-cn)
- [ByteTech: Unity il2cpp 编译流程分享](https://bytetech.info/videos/7134694941254483976)
- [ByteTech: Unity il2cpp 编译流程分享（下）](https://bytetech.info/videos/7134657562808418340)
- [catlikecoding tutorials](https://catlikecoding.com/unity/tutorials/)
- [PlayableDirector 脚本 API](https://docs.unity3d.com/6000.2/Documentation/ScriptReference/Playables.PlayableDirector.html)
- [IL2CPP clang arguments 讨论](https://discussions.unity.com/t/il2cpp-build-target-clang-arguments/942288/5)
- [UWA 社区搜索：ET](https://community.uwa4d.com/search?keyword=ET&scope=1)

### AI 相关链接

- [Unity Android 要求与兼容性](https://docs.unity3d.com/6000.1/Documentation/Manual/android-requirements-and-compatibility.html)

### GitHub 相关链接

- [Cysharp/UniTask](https://github.com/Cysharp/UniTask)
- [Cysharp/MemoryPack](https://github.com/Cysharp/MemoryPack)
- [focus-creative-games/hybridclr](https://github.com/focus-creative-games/hybridclr)
- [egametang/ET](https://github.com/egametang/ET)
- [LiShengYang-yiyi/YIUI](https://github.com/LiShengYang-yiyi/YIUI)
- [Siccity/xNode](https://github.com/Siccity/xNode)
- [Siccity/Dialogue](https://github.com/Siccity/Dialogue)
- [ad313/SourceGenerator.Template](https://github.com/ad313/SourceGenerator.Template)

### 补充归档（Unity 补充资料）

- [Feel | Particles/Effects | Unity Asset Store](https://assetstore.unity.com/packages/tools/particles-effects/feel-183370?aid=1011lKhG)
- [Feel Documentation | Feel Documentation](https://feel-docs.moremountains.com/)
- [Feel: Lofelt.NiceVibrations Namespace Reference](https://feel-docs.moremountains.com/API/namespace_lofelt_1_1_nice_vibrations.html)
- [How to install Feel? | Feel Documentation](https://feel-docs.moremountains.com/how-to-install.html)
- [Contents of the asset | Feel Documentation](https://feel-docs.moremountains.com/contents.html)
- [Cysharp/R3: The new future of dotnet/reactive and UniRx.](https://github.com/Cysharp/R3)
- [ET-Packages/cn.etetet.core](https://github.com/ET-Packages/cn.etetet.core)
- [falseeeeeeeeee/ShaderLibrary](https://github.com/falseeeeeeeeee/ShaderLibrary)
- [Cysharp, Inc.](https://github.com/Cysharp)
- [收集的大佬博客/Github - ET社区](https://et-framework.cn/d/23-github)
- [数学与缓动 | 走停人生路](https://tonytang1990.github.io/2020/05/29/%E6%95%B0%E5%AD%A6%E4%B8%8E%E7%BC%93%E5%8A%A8/)
- [ET社区](https://et-framework.cn/)
- [联系站长 | 雨松MOMO程序研究院](https://www.xuanyusong.com/contact)
- [Gaffer On Games](https://gafferongames.com/)
- [Fixing the Internet for Games | Gaffer On Games](https://gafferongames.com/post/fixing_the_internet_for_games/)
- [Downloads - Opsive](https://opsive.com/downloads/?pid=803)
- [Videos - Opsive](https://opsive.com/videos/?pid=803)
- [CCLBStudio/DOTweenBuilder](https://github.com/CCLBStudio/DOTweenBuilder)
- [Cysharp/NativeMemoryArray](https://github.com/Cysharp/NativeMemoryArray)
- [EsotericSoftware/spine-scripts](https://github.com/EsotericSoftware/spine-scripts)
- [LeahLee13/UnityCameraSystem_CC](https://github.com/LeahLee13/UnityCameraSystem_CC)
- [LeahLee13/UnityCameraSystem_RB](https://github.com/LeahLee13/UnityCameraSystem_RB)
- [LiuOcean/UnityAppFlavor](https://github.com/LiuOcean/UnityAppFlavor)
- [NibbleByte/UnityWiseSVN](https://github.com/NibbleByte/UnityWiseSVN)
- [No78Vino/gameplay-ability-system-for-unity](https://github.com/No78Vino/gameplay-ability-system-for-unity)
- [TeamSirenix/odin-serializer](https://github.com/TeamSirenix/odin-serializer)
- [Unity-Technologies/megacity-metro](https://github.com/Unity-Technologies/megacity-metro)
- [YouwantLee/Joker_Unity_SkillEditor](https://github.com/YouwantLee/Joker_Unity_SkillEditor)
- [hwaet/UnityProjectCloner](https://github.com/hwaet/UnityProjectCloner)
- [niepp/Sync: 基于Unity2019的状态同步技术demo](https://github.com/niepp/Sync)
- [sschmid/Entitas](https://github.com/sschmid/Entitas)
- [tinyantstudio/SimpleTimeLineWindow](https://github.com/tinyantstudio/SimpleTimeLineWindow)
- [yukuyoulei/Unity-GUI-Game-In-Single-File](https://github.com/yukuyoulei/Unity-GUI-Game-In-Single-File)
- [IvanMurzak/Unity-ImageLoader](https://github.com/IvanMurzak/Unity-ImageLoader)
- [GlitchEnzo/NuGetForUnity](https://github.com/GlitchEnzo/NuGetForUnity)
- [bdovaz/UnityNuGet](https://github.com/bdovaz/UnityNuGet)
- [mikerochip/unity-websocket](https://github.com/mikerochip/unity-websocket)
- [neuecc/UniRx](https://github.com/neuecc/UniRx)
- [unity3d-jp/UnityChanToonShaderVer2_Project](https://github.com/unity3d-jp/UnityChanToonShaderVer2_Project)
- [JiepengTan/GamesTanTools](https://github.com/JiepengTan/GamesTanTools?tab=readme-ov-file)
- [Unity-Technologies/PostProcessing at v2](https://github.com/Unity-Technologies/PostProcessing/tree/v2/PostProcessing)
- [CoderGamester/mcp-unity](https://github.com/CoderGamester/mcp-unity)
- [Eastrall/Rosalina](https://github.com/Eastrall/Rosalina)
- [Unity-Technologies/ml-agents](https://github.com/Unity-Technologies/ml-agents)
- [Unity-Technologies/EntityComponentSystemSamples](https://github.com/Unity-Technologies/EntityComponentSystemSamples?tab=readme-ov-file)
- [Easing Functions for Unity3D - Gist](https://gist.github.com/ManeFunction/9f2d437fca6ccf31e4a48fec0584e21a)
- [liangddyy/TweenUtil](https://github.com/liangddyy/TweenUtil)
- [foldcc/MintAnimation](https://github.com/foldcc/MintAnimation)
- [kisence-mian/MyUnityFrameWork](https://github.com/kisence-mian/MyUnityFrameWork)
- [tylearymf/UniHacker](https://github.com/tylearymf/UniHacker)
- [Unity Technologies](https://github.com/Unity-Technologies)
- [MetaZhi/unity-learning-path](https://github.com/MetaZhi/unity-learning-path)
- [lengly/UnityGame](https://github.com/lengly/UnityGame)
- [QianMo/Unity-Design-Pattern](https://github.com/QianMo/Unity-Design-Pattern)
- [linxinfa/Unity-RpgGameDemo](https://github.com/linxinfa/Unity-RpgGameDemo)
- [akof1314/UnitySpritePackerOverview](https://github.com/akof1314/UnitySpritePackerOverview)
- [akof1314/UnityParticleSystemPreview](https://github.com/akof1314/UnityParticleSystemPreview)
- [MirrorNetworking/Mirror](https://github.com/MirrorNetworking/Mirror)
- [evskii/UnityFishingMinigame](https://github.com/evskii/UnityFishingMinigame)
- [Bullrich/Unity-5-2D-Tile-Map-Editor](https://github.com/Bullrich/Unity-5-2D-Tile-Map-Editor/tree/master)
- [Unity-Technologies/2d-extras](https://github.com/Unity-Technologies/2d-extras)
- [yasirkula/UnityRuntimePreviewGenerator](https://github.com/yasirkula/UnityRuntimePreviewGenerator)
- [ChuKuang/Unity-Dev-Tools](https://github.com/ChuKuang/Unity-Dev-Tools?tab=readme-ov-file)
- [Json.Net in Unity - Gist](https://gist.github.com/onionmk2/d2e3e4cca27a37a89796e084e05de212)
- [Githaojiejie/unity3D-tutorial](https://github.com/Githaojiejie/unity3D-tutorial)
- [Slate Cinematic Sequencer | Unity Asset Store](https://assetstore.unity.com/packages/tools/animation/slate-cinematic-sequencer-56558)
- [MVVM and Databinding for Unity3d - Unity Discussions](https://discussions.unity.com/t/mvvm-and-databinding-for-unity3d/711555)
- [Open Source WebSocket client - Unity Discussions](https://discussions.unity.com/t/open-source-websocket-client/944630)
- [Ultimate Screenshot Creator | Unity Asset Store](https://assetstore.unity.com/packages/tools/utilities/ultimate-screenshot-creator-82008)
- [Happy Harvest - 2D Sample Project | Unity Asset Store](https://assetstore.unity.com/packages/essentials/tutorial-projects/happy-harvest-2d-sample-project-259218)
- [Lost Crypt - 2D Sample Project | Unity Asset Store](https://assetstore.unity.com/packages/essentials/tutorial-projects/lost-crypt-2d-sample-project-158673)
- [关于ET中Unity部分工作流思考和建议 - ET社区](https://et-framework.cn/d/2098-etunity/5)
- [Spine官网：专注于游戏的2D动画软件](https://zh.esotericsoftware.com/)
- [Spine Forum - SkeletonGraphic and SkeletonAnimation appear differently](https://zh-hans.esotericsoftware.com/forum/d/23919-skeletongraphic-and-skeletonanimation-appear-differently)
- [Optimize Animations - Spine Forum](https://zh.esotericsoftware.com/forum/d/14292-optimize-animations)
- [How to get Bounds of Spine Animation - Spine Forum](https://zh.esotericsoftware.com/forum/d/13648-how-to-get-bounds-of-spine-animation-object/2)
- [Unity资源管理 | 走停人生路](https://tonytang1990.github.io/2016/10/13/Unity%E8%B5%84%E6%BA%90/)
- [雨松MOMO程序研究院](https://www.xuanyusong.com/)
- [Bian-Sh/Dotween-Animation-Provider](https://github.com/Bian-Sh/Dotween-Animation-Provider)
- [allfake/Dotween-Simple-Timeline](https://github.com/allfake/Dotween-Simple-Timeline)
- [medvejut/dotween-timeline: Timeline component for DOTween Pro](https://github.com/medvejut/dotween-timeline)
- [Alex-Rachel/GameFramework-Next](https://github.com/Alex-Rachel/GameFramework-Next)
- [skywind3000/kcp: KCP - A Fast and Reliable ARQ Protocol](https://github.com/skywind3000/kcp)
- [NullStackSuger/ET-OWDemo](https://github.com/NullStackSuger/ET-OWDemo)
- [Viagi/LandlordsCore: ET斗地主Demo](https://github.com/Viagi/LandlordsCore)
- [ikamei/GameMechanic](https://github.com/ikamei/GameMechanic)
- [GameFrameX](https://github.com/GameFrameX)
- [killop/anything_about_game: A wonderful list of Game Development resources.](https://github.com/killop/anything_about_game)

### 再归档补充

- [https://www.luban3d.com/](https://www.luban3d.com/)
- [Luban 适配 MemoryPack | L's Blog](https://www.liuocean.com/archives/luban-gua-pei-memorypack)
- [Bolt可视化编程工具 | Unity 中文课堂](https://learn.u3d.cn/tutorial/bolt-mstudio?chapterId=63562b29edca72001f21d183&sectionId=60389634bed13a002239eabd)
- [数据驱动类技能 - Valve Developer Community](https://developer.valvesoftware.com/wiki/Zh/Dota_2_Workshop_Tools/Scripting/Abilities_Data_Driven)
- [Unity Now Forcing Cloud Projects – GameFromScratch.com](https://gamefromscratch.com/unity-now-forcing-cloud-projects/)
- [Guide to Extending Unity Editor’s Menus | by Edward Rowe | Red Blue Games](https://blog.redbluegames.com/guide-to-extending-unity-editors-menus-b2de47a746db)
- [如何把unity 5提供的YAML merge tool 整合至TortoriseSVN – mattchen730](https://mattchen730.wordpress.com/2016/12/09/%E5%A6%82%E4%BD%95%E6%8A%8Aunity-5%E6%8F%90%E4%BE%9B%E7%9A%84yaml-merge-tool-%E6%95%B4%E5%90%88%E8%87%B3tortorisesvn/)
- [猫都能学会的Unity3D Shader入门指南（一） | OneV's Den](https://onevcat.com/2013/07/shader-tutorial-1/)
- [UGUI中的anchor和canvas(屏幕适配) - 雁过留声](https://blogml.top/2023/01/17/ugui-anchor-and-canvas/)
- [UGUI TextMeshPro 控件详解 | Unity3D 学习汇总](https://jsdocunity.jsopy.com/UGUI/U7.html)
- [Unity Luban - ReubenSun](https://reubensun.com/engine/UnityLuban/)
- [Unity-Technologies / Repositories — Bitbucket](https://bitbucket.org/Unity-Technologies/workspace/repositories/)
- [UGUI源码分析(一): Image的渲染 - 杨世玲的博客](https://www.young40.com/post/2021-12-26-ugui-source-reading-01/)
- [在Unity游戏中使用LINQ技术 | WN Hub](https://wnhub.io/zh/news/engines/item-44558)
- [Unity游戏内存优化——以TileMatch为例](https://www.potatoyz.tech/Posts/Unity%E6%B8%B8%E6%88%8F%E5%86%85%E5%AD%98%E4%BC%98%E5%8C%96%E2%80%94%E2%80%94%E4%BB%A5TileMatch%E4%B8%BA%E4%BE%8B)
- [【Unity3D开发小游戏】《贪吃蛇》Unity开发教程 · 764424567](https://itmonon.github.io/posts/unity3d-game/Unity3D%E5%BC%80%E5%8F%91%E5%B0%8F%E6%B8%B8%E6%88%8F-%E8%B4%AA%E5%90%83%E8%9B%87-Unity%E5%BC%80%E5%8F%91%E6%95%99%E7%A8%8B)
- [Unity编辑器的扩展，MenuItem的使用整理 | 禾文的博客](https://unique849997563.github.io/2019/03/06/Unity%E7%BC%96%E8%BE%91%E5%99%A8%E7%9A%84%E6%89%A9%E5%B1%95%EF%BC%8CMenuItem%E7%9A%84%E4%BD%BF%E7%94%A8%E6%95%B4%E7%90%86/)
- [Unity3D通过反射实现安卓的代码热更新 | 六饼](https://bbbbbbion.github.io/2015/09/16/Unity3D%E9%80%9A%E8%BF%87%E5%8F%8D%E5%B0%84%E5%AE%9E%E7%8E%B0%E5%AE%89%E5%8D%93%E7%9A%84%E4%BB%A3%E7%A0%81%E7%83%AD%E6%9B%B4%E6%96%B0/)
- [UGUI性能优化总结 | 无境](https://www.drflower.top/posts/aad79bf1/)
- [Unity UI Extensions README | Unity-UI-Extensions.GitHub.io](https://unity-ui-extensions.github.io/)
- [Unity3D：关于Texture2D和byte字节互转的坑 | 大腿Plus](https://www.zhaoshijun.com/archives/2043)
- [Unity怎么改界面字体大小 - 3D天堂网(i3dtt.com)](https://www.i3dtt.com/104248.html)
- [Unity-Serialization理解 | StoneのBLOG](https://stonelzp.github.io/unity-serialization/)
- [Unity SerializeField和Serializable - DullSword's Blog](https://dullsword.github.io/2021/03/03/Unity-SerializeField%E5%92%8CSerializable/)
- [Unity编辑器扩展：使用xNode制作自己的可视化工具（2） | ydwj的游戏开发日记](https://auniquepig.com/2021/06/27/Story-Editor2/)
- [Warl-G's Blog - Unity手册—Attribute汇总说明](https://warl.top/posts/Unity-Manual-Attribute/)
- [CodeGize-Unity编辑器开发，使用CustomPropertyDrawer实现枚举中文显示](http://www.codegize.com/post/38.html)
- [事件函数执行顺序 · Unity-Manual](https://nuysoft.gitbooks.io/unity-manual/content/Manual/ExecutionOrder.html)
- [游戏引擎 / Unity WebGL微信小游戏适配](https://developers.weixin.qq.com/minigame/dev/guide/game-engine/unity-webgl-transform.html)
- [《Unity性能优化》-- 5. 性能优化实战 | 不特别周のBlog](https://1024114.xyz/posts/4a5d44c0/)
- [TinaX Framework - Delightful Unity-based Framework](https://tinax.corala.space/)
- [Unity 解决包体过大问题记录和纹理相关知识点-云社区-华为云](https://bbs.huaweicloud.com/blogs/293517)
- [Visual Studio crashes when debugging mixed mode and hitting a breakpoint in native code - Developer Community](https://developercommunity.visualstudio.com/t/visual-studio-crashes-when-debugging-mixed-mode-an/1356008)
- [Assetを全検索する #Unity - Qiita](https://qiita.com/TETTASUN/items/bbd03ad320fbc03595af)
- [Holopix AI: AI Game Art Creation Platform & Community](https://app.holopixai.art/)
- [YouWare | First AI Coding Community Where Creators Build](https://www.youware.com/home)

### 再归档补充

- [DOTween - Documentation](https://dotween.demigiant.com/documentation.php)
- [纹理贴图资源（Texture） | Cocos Creator](https://docs.cocos.com/creator/3.8/manual/zh/asset/texture.html)
- [MoonSharp](https://www.moonsharp.org/)
- [Using ASTC Texture Compression for Game Assets | NVIDIA Developer](https://developer.nvidia.com/astc-texture-compression-for-game-assets)
- [Wwise 教学 | Audiokinetic](https://www.audiokinetic.com/zh/learning/teach-wwise/)
- [在EditorWindow上显示自定义类型列表 - 雪千渔Blog](https://www.imxqy.com/gdev/unity/ueditor-clst.html)
- [ILRuntime中的反射 — ILRuntime](https://ourpalm.github.io/ILRuntime/public/v1/guide/reflection.html)
- [Odin Inspector 系列教程 - Odin工具箱【一键批量更改Raycast Target选项】 - 个人技术笔记](https://aihailan.com/archives/912)

### 人工压缩补充

- [如何使用及维护Github的LayaAir引擎源码__LAYABOX技术文档](https://ldc2.layabox.com/doc/?language=zh&nav=zh-ts-0-3-4)
- [代码哲学官网](https://code-philosophy.com/)
