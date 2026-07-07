---
title: 帧同步与游戏 AI
tags:
  - 游戏开发
  - 引擎
  - 帧同步
  - lockstep
  - 游戏ai
  - 补充资料
status: reviewed
confidence: 0.7
visibility: public
last_curated: 2026-06-11
source_count: 21
---

## 核心结论

- 帧同步（Lockstep）的核心挑战不是同步帧本身，而是**确定性（determinism）**：浮点数、物理模拟、随机数种子必须在所有客户端完全一致。
- 状态同步适合高延迟容忍场景；帧同步适合强一致性实时对战（RTS、MOBA、格斗）；状态帧同步是两者折中：客户端预测 + 服务端校验回滚。
- 行为树（Behavior Tree）是游戏 AI 的主流实现方案，相比有限状态机更易扩展和调试。

## 适用场景

- 新项目需要设计多人实时对战同步方案，评估帧同步 vs 状态同步。
- 已有项目出现不同客户端画面不一致、回放不可复现等问题。
- 需要在 Unity 中实现 NPC / 敌人 AI 行为逻辑。

## 一、帧同步 / Lockstep

- **入门**：Gabriel Gambetta 的系列文章是最清晰的帧同步原理讲解（英文）；B 站帧同步合集（av70422751）是中文最系统的视频入门
- **实践**：云风（codingnow.com）的文章是中文领域最有参考价值的帧同步实践总结；微信小游戏官方提供了 Lockstep 框架参考实现
- **开源参考**：LockstepEngine（JiepengTan）、LockstepDemo（ookcode）可作为原型参考，注意评估浮点确定性处理方式

## 二、游戏 AI / 行为树

- indienova 的行为树原理文章是中文最好的入门材料之一
- luzexi 博客有 Unity 行为树接入实践；Isara Tech 提供商业级工具方案

## 资料收敛说明

- 本页已将原先 `22` 条参考链接压缩为 `10` 条核心引用，重复导航页、同类 API 细节页和低信噪比补充资料不再逐条公开保留。
- 正文已优先沉淀选型标准、排查流程、风险边界和常用工具定位，后续新增资料应继续转成正文结论，而不是直接堆叠链接。
- 文末只保留官方文档、代表性开源项目和少量仍值得回看的补充阅读。


### 参考链接

- [干货！光子高级工程师揭秘帧同步游戏的技术实现细节_游戏陀螺](https://www.youxituoluo.com/528021.html)
- [使用行为树(Behavior Tree)实现游戏AI - 技术人生 - 编程技术 - JESSE人生](http://www.luzexi.com/2013/01/26/%E4%BD%BF%E7%94%A8%E8%A1%8C%E4%B8%BA%E6%A0%91(Behavior-Tree)

### 知乎文章

- [(99+ 封私信 / 81 条消息) 王者荣耀游戏中帧同步如何分离逻辑和渲染？ - 知乎](https://www.zhihu.com/question/323505671)
- [游戏AI入门及AI优化 - 知乎](https://zhuanlan.zhihu.com/p/82567889)
- [像《红警》里的大兵那样找路（上）——全局向量场寻路 - 知乎](https://zhuanlan.zhihu.com/p/562570278)

### B站视频

- [帧同步教程【合集】_哔哩哔哩 (゜-゜)つロ 干杯~-bilibili](https://www.bilibili.com/video/av70422751/?p=3)
- [帧同步教程【合集】_哔哩哔哩 (゜-゜)つロ 干杯~-bilibili](https://www.bilibili.com/video/BV1ZJ411F7Sn?p=1)

### GitHub 项目

- [JiepengTan/LockstepEngine: A lockstep solution include lots of deterministic library (Math,Collision,Navmesh,Behavior...](https://github.com/JiepengTan/LockstepEngine)
- [JiepengTan/Lockstep-Tutorial: 帧同步 教程](https://github.com/JiepengTan/Lockstep-Tutorial)
- [Repository search results](https://github.com/search?q=lockstep&type=repositories&s=stars&o=desc&p=1)
- [ihaiucom/learn.AStarPathfinding: A* Pathfinding Project Pro](https://github.com/ihaiucom/learn.AStarPathfinding)

## 参考链接

> 以下链接仅保留正文仍需回看的核心资料入口。

### 开源项目

- [Enanyy/Frame: 帧同步demo，包含了服务器和客户端，实现了LockStep和乐观帧同步两种模式](https://github.com/Enanyy/Frame)
- [GitHub Search: lockstep](https://github.com/search?q=lockstep&type=repositories)
- [byebyebruce/lockstepserver](https://github.com/byebyebruce/lockstepserver)

### 补充阅读

- [Isara Tech | AI, LLM & Machine Learning Solutions](https://isaratech.com/)
- [三种同步方式：状态同步、帧同步、状态帧同步 - 十月的大橘 - 博客园](https://www.cnblogs.com/October2018/p/16120681.html)
- [Gabriel Gambetta](https://www.gabrielgambetta.com/index.html)
- [游戏中的 AI - 行为树 | lifan's blog](https://lifan.tech/2020/02/15/game/behavior-tree/)
- [Game AI Behavior Trees: Complete Implementation Tutorial](https://www.generalistprogrammer.com/tutorials/game-ai-behavior-trees-complete-implementation-tutorial)
- [帧同步教程【合集】- 哔哩哔哩](https://www.bilibili.com/video/av70422751/)
- [云风的 BLOG: lockstep 网络游戏同步方案](https://blog.codingnow.com/2018/08/lockstep.html)