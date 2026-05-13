---
title: "C / C# / C++ 参考"
tags:
  - 参考
  - 文档
  - c++
  - "c#"
  - dotnet
status: reviewed
confidence: 0.7
visibility: public
last_curated: 2026-05-13
source_count: 10
---

> 阶段：05-参考文档  

## 定位说明

C / C# / C++ 的官方 API 文档和在线参考工具汇总，作为日常开发的快速查阅入口。在线编译器（Coliru / Compiler Explorer / C++ Insights）见 [[在线工具与协作]]。

## 一、C++ 参考

> 在线编译器 (Coliru / C++ Insights / Compiler Explorer) 见 [[在线工具与协作]]

- **cppreference**（中英文）：最完整的 C++ 标准库参考，建议中英文对照查阅
- **cplusplus.com**：对初学者更友好，示例代码更完整
- **Microsoft C++ 文档**（learn.microsoft.com）：MSVC / Windows 开发场景专用
- C++ Core Guidelines 见 [[平台与规范]]

## 二、C# / .NET 参考

- **C# 语言参考**（learn.microsoft.com）：最权威的官方语法入口
- **System Namespace**（.NET 8）：查阅基础类型和集合 API
- **.NET 工具和诊断文档**：性能分析、dump 分析、dotnet-trace 等工具入口
- **NuGet Gallery**：第三方包查找，DevToys.JsonToCsharp、Scriban 等常用工具包

## 三、源代码参考

- **dotnet/runtime**（GitHub）：.NET 运行时源码，查阅底层实现（如 Int128）
- **Visual Studio SDK**（dotnet.microsoft.com）：VS 相关 SDK 下载
- PIX on Windows：DirectX 性能分析和调试工具

## 四、相关学习参考

- FP16/FP32 浮点格式解析：GPU 和 AI 推理场景必读
- CLR Via C#（语雀笔记版）：深入理解 .NET 运行时的系统性资料
- Maven / NuGet 制品仓库：Android 和 .NET 依赖管理查询入口

## 资料收敛说明

- 本页已将原先 `91` 条参考链接压缩为 `10` 条核心引用，重复导航页、同类 API 细节页和低信噪比补充资料不再逐条公开保留。
- 正文已优先沉淀选型标准、排查流程、风险边界和常用工具定位，后续新增资料应继续转成正文结论，而不是直接堆叠链接。
- 文末只保留官方文档、代表性开源项目和少量仍值得回看的补充阅读。

## 参考链接

> 以下链接仅保留正文仍需回看的核心资料入口。

### 官方文档

- [C# 语言参考 | Microsoft Learn](https://learn.microsoft.com/zh-cn/dotnet/csharp/language-reference/)
- [list.cs](https://referencesource.microsoft.com/)
- [适用于 Visual Studio 的 .NET SDK](https://dotnet.microsoft.com/zh-cn/download/visual-studio-sdks?cid=getdotnetsdk)
- [cplusplus.com](https://cplusplus.com/)
- [cppreference EN](https://en.cppreference.com/cpp)

### 开源项目

- [fanslead/Learn-SourceGenerator: 学习SourceGenerator代码仓库](https://github.com/fanslead/Learn-SourceGenerator)
- [dotnet/runtime - Int128.cs (GitHub)](https://github.com/dotnet/runtime/blob/5535e31a712343a63f5d7d796cd874e563e5ac14/src/libraries/System.Private.CoreLib/src/System/Int128.cs)
- [ihaiucom/learn.AStarPathfinding: A* Pathfinding Project Pro](https://github.com/ihaiucom/learn.AStarPathfinding)

### 补充阅读

- [FP16、FP32 等浮点格式全解析 - CSDN](https://blog.csdn.net/yuanmomoya/article/details/147327546)
- [Animating in C++: Curves and Easing Functions - Tom Looman](https://www.tomlooman.com/animating-in-cpp-curves-and-easing-functions/)
