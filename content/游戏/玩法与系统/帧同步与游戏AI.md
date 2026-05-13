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
last_curated: 2026-05-13
source_count: 22
---

> 阶段：02-引擎与游戏开发  

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

## 参考链接

> 以下链接作为本笔记的资料来源保留。

### 链接分组

- [Gabriel Gambetta](https://www.gabrielgambetta.com/index.html)
- [帧同步教程【合集】- 哔哩哔哩](https://www.bilibili.com/video/av70422751/)
- [基于状态帧同步的战斗系统-技能预测/回滚演示_游戏热门视频](https://www.bilibili.com/video/BV11L4y1u7rS/)
- [LT_02_LockstepDeveolpAdvice_哔哩哔哩_bilibili](https://www.bilibili.com/video/av70422751/?p=3)
- [开放能力 / 游戏服务 / 帧同步](https://developers.weixin.qq.com/minigame/dev/guide/open-ability/lock-step.html)
- [三种同步方式：状态同步、帧同步、状态帧同步 - 十月的大橘 - 博客园](https://www.cnblogs.com/October2018/p/16120681.html)
- [Unity 状态帧同步+技能系统 Demo_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1XC8yejETS/)
- [云风的 BLOG: lockstep 网络游戏同步方案](https://blog.codingnow.com/2018/08/lockstep.html)
- [setuppf/GameBookServer](https://github.com/setuppf/GameBookServer)

### AI 相关链接

- [AI 行为树的工作原理 | indienova](https://indienova.com/indie-game-development/ai-behavior-trees-how-they-work/)
- [aisharing.com 行为树文章](http://www.aisharing.com/archives/90)
- [游戏中的 AI - 行为树 | lifan's blog](https://lifan.tech/2020/02/15/game/behavior-tree/)
- [Isara Tech | AI, LLM & Machine Learning Solutions](https://isaratech.com/)
- [使用行为树(Behavior Tree)实现游戏AI - 技术人生 - 编程技术 - JESSE人生](http://www.luzexi.com/2013/01/26/%E4%BD%BF%E7%94%A8%E8%A1%8C%E4%B8%BA%E6%A0%91(Behavior-Tree)

### GitHub 相关链接

- [JiepengTan - GitHub](https://github.com/JiepengTan)
- [JiepengTan/LockstepEngine](https://github.com/JiepengTan/LockstepEngine)
- [GitHub Search: lockstep](https://github.com/search?q=lockstep&type=repositories)
- [ookcode/LockstepDemo](https://github.com/ookcode/LockstepDemo)
- [byebyebruce/lockstepserver](https://github.com/byebyebruce/lockstepserver)
- [YouRenJee/LockstepFundation](https://github.com/YouRenJee/LockstepFundation)
- [Enanyy/Frame: 帧同步demo，包含了服务器和客户端，实现了LockStep和乐观帧同步两种模式](https://github.com/Enanyy/Frame)
- [wechat-miniprogram/minigame-lockstep-demo](https://github.com/wechat-miniprogram/minigame-lockstep-demo)
