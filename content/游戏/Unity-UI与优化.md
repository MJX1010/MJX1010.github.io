---
title: Unity UI 与优化
tags:
  - 游戏开发
  - 引擎
  - unity
  - ugui
  - 性能优化
---
> 阶段：02-引擎与游戏开发  

## 一、官方与平台入口

- [Unity Asset Store](https://assetstore.unity.com/zh-CN): 官方资源商店
- [团结引擎手册：商标和使用条款](https://docs.unity.cn/cn/tuanjiemanual/Manual/TermsOfUse.html): 团结引擎中文文档
- [Unity 开发者社区](https://developer.unity.cn/): Unity 中国开发者社区
- [Unity 开发者联盟](https://www.u3dchina.com/): 第三方 Unity 中文社区
- [Unity Learn](https://learn.unity.com/): Unity 官方教学平台

## 二、框架与工具

### 1. 框架与社区

- [ET 社区](https://et-framework.cn/): ET 框架社区入口
- [Star, a Unity C# Editor Tutorial - Catlike Coding](https://catlikecoding.com/unity/tutorials/editor/star/): Editor 扩展教程
- [Odin Inspector and Serializer](https://odininspector.com/): Unity 常用 Inspector 增强

### 2. 动画与插件

- [DOTween (HOTween v2)](https://dotween.demigiant.com/): 主流补间动画库
- [Find Reference 2 - Free Download | Dev Asset Collection](https://unityassetcollection.com/find-reference-2-free-download/): 资源引用查找插件

> Dev Asset Collection 站点首页 (https://unityassetcollection.com/) 见 [[软件与游戏资源|08-资源下载/软件与游戏资源]]

### 3. 配表与工具脚本

- [【游戏开发】Excel 表格批量转换成 lua 的转表工具 - 博客园](https://www.cnblogs.com/msxh/p/8539108.html): Excel→Lua 工具

## 三、UGUI 与 UI 优化

- [Unity UGUI —— 无限循环 List - 博客园](https://www.cnblogs.com/fly-100/p/4549354.html)
- [UGUI ScrollRect 优化 - CSDN](https://blog.csdn.net/subsystemp/article/details/46912479)
- [Unity UI(uGUI) 源码学习笔记(一) Button - lvmingbei](https://lvmingbei.hatenablog.com/entry/2015/05/12/194948)
- [UGUI 不消耗 DRAW CALL 的 EventTrigger 接收器 - CSDN](https://blog.csdn.net/rcfalcon/article/details/51431734)
- [优化 UGUI 的 ScrollRect | Loading & Learning](https://qiankanglai.me/2015/08/15/LoopScrollRect/)
- [Unity 进阶技巧：RectTransform 详解 - 简书](https://www.jianshu.com/p/dbefa746e50d)
- [UGUI batch 规则和性能优化 - 博客园](https://www.cnblogs.com/fly-100/p/5488757.html)
- [UGUI 性能优化 - 桫椤 - 博客园](https://www.cnblogs.com/suoluo/p/5417152.html)
- [UGUI 表情系统解决方案（微信）](https://mp.weixin.qq.com/s?__biz=MzI3MzA2MzE5Nw==&mid=2668904827&idx=1&sn=b3ef1e990c46d90bcb18480b4714a3dc&chksm=f1c9ed09c6be641f2c2e664478608c293eea5c0e612c2b7a7313ff75b87382ac453eb377eef8&mpshare=1&scene=23&srcid=1124rYS5c8Dcbzv6rQGAHExA#rd)

> 注：itdadao.com /c15a128032p0 (无标题, 站点不稳定) 已移入 [[失效与低价值|11-待清理/失效与低价值]]

## 四、性能与渲染优化

- [unity3d 优化总结篇 - CSDN](https://blog.csdn.net/sgnyyy/article/details/41621039)
- [Unity GUI(uGUI) 使用心得与性能总结 - 简书](https://www.jianshu.com/p/061e67308e5f)
- [深入浅出聊优化：从 Draw Calls 到 GC - 慕容小匹夫 - 博客园](https://www.cnblogs.com/murongxiaopifu/p/4284988.html)
- [Unity + NGUI 性能优化方法总结 - CSDN](https://blog.csdn.net/zzxiang1985/article/details/43339273)
- [关于 Unity 渲染优化，你可能遇到这些问题 - UWA](https://blog.uwa4d.com/archives/QA_Rendering.html)
- [U3D DrawCall 优化手记 - 深圳-宝爷 - 博客园](https://www.cnblogs.com/ybgame/p/3588795.html)
- [Unity 中性能优化的一些经验与总结（脚本优化篇）- CSDN](https://blog.csdn.net/u013709166/article/details/54934931)
- [Unity3d 开发：编辑器 DrawCall 参数解析 - CSDN](https://blog.csdn.net/fansongy/article/details/51025325)
- [Unity – ValueType & boxing with Dictionary - NaCl's Blog](https://fredxxx123.wordpress.com/2017/05/08/unity-valuetype-boxing-with-dictionary/)

## 五、ECS

- [分类：ECS 入门 - 笨木头的博客](https://www.benmutou.com/archives/category/ECS入门)

## 六、PureMVC（在 Unity 中应用）

- [PureMVC 和 Unity3D 的 UGUI 制作员工管理系统实例 - 简书](https://www.jianshu.com/p/904b36ad37e2)
- [不懂 PureMVC 框架问题？深入解读看完必会(上) - 知乎](https://zhuanlan.zhihu.com/p/135426258)
- [MVC、MVP 和 MVVM 的图示 - 阮一峰](https://www.ruanyifeng.com/blog/2015/02/mvcmvp_mvvm.html)
- [理论 + 实践！如何在 Unity 中应用 PureMVC 框架？ - GameRes](https://www.gameres.com/822910.html)
- [Unity PureMVC 框架解读(上) - CSDN](https://blog.csdn.net/qq_29579137/article/details/73692842)
- [Unity PureMVC 框架解读(下) - CSDN](https://blog.csdn.net/qq_29579137/article/details/73717882)
- [PureMVC 框架解读（下）- CSDN](https://blog.csdn.net/zzwdkxx/article/details/82015101)
- [PureMVC -- 一款多平台 MVC 框架 - 简书](https://www.jianshu.com/p/47deaced9eb3)
- [Unity 框架：PureMVC 在 Unity 中的简单使用 - CSDN](https://blog.csdn.net/lyh916/article/details/50076463)
- [Unity 框架：PureMVC 基础 - CSDN](https://blog.csdn.net/lyh916/article/details/50058207)
- [PureMVC（AS3）剖析：实例 - 吴秦 - 博客园](https://www.cnblogs.com/skynet/archive/2013/01/29/2881244.html)

## 七、其他 Unity 资料

- [Unity Shader 编程开发系列教程 - 直线网](https://www.linecg.com/video/play31170.html)
