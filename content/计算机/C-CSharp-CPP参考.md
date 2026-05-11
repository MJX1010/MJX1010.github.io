---
title: C / C# / C++ 参考
tags:
  - 参考
  - 文档
  - c++
  - c#
  - dotnet
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

## 参考链接

> 以下链接作为本笔记的资料来源保留。

### 链接分组

- [cplusplus.com](https://cplusplus.com/)
- [cppreference 中文](https://zh.cppreference.com/首页)
- [cppreference EN](https://en.cppreference.com/cpp)
- [cpp.hotexamples 中文](https://cpp.hotexamples.com/zh/)
- [System Namespace | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/system?view=net-8.0)
- [Maven Repository: com.google.gms » google-services](https://mvnrepository.com/artifact/com.google.gms/google-services)
- [NuGet Gallery | Packages matching Tags:"devtoys-app" json](https://www.nuget.org/packages?q=Tags%3A%22devtoys-app%22+json&includeComputedFrameworks=true&prerel=true&sortby=relevance)
- [NuGet Gallery | DevToys.JsonToCsharp 1.1.0](https://www.nuget.org/packages/DevToys.JsonToCsharp#readme-body-tab)
- [NuGet Gallery | Scriban 5.11.0](https://www.nuget.org/packages/Scriban/5.11.0#releasenotes-body-tab)
- [适用于 Visual Studio 的 .NET SDK](https://dotnet.microsoft.com/zh-cn/download/visual-studio-sdks?cid=getdotnetsdk)
- [C# 语言参考 | Microsoft Learn](https://learn.microsoft.com/zh-cn/dotnet/csharp/language-reference/)
- [C++ 文档（Microsoft Learn）](https://learn.microsoft.com/zh-cn/cpp/cpp/?view=msvc-160)
- [.NET 工具和诊断文档 | Microsoft Learn](https://learn.microsoft.com/zh-cn/dotnet/navigate/tools-diagnostics/)
- [Maven Repository: io.github.yidun » crashreport](https://mvnrepository.com/artifact/io.github.yidun/crashreport)
- [PIX on Windows](https://devblogs.microsoft.com/pix/)
- [Download .NET 8.0 (Linux, macOS, and Windows)](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)
- [Download .NET 8.0 Desktop Runtime (v8.0.6) - Windows x64 Installer](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-desktop-8.0.6-windows-x64-installer)

### AI 相关链接

- [FP16、FP32 等浮点格式全解析 - CSDN](https://blog.csdn.net/yuanmomoya/article/details/147327546)

### GitHub 相关链接

- [dotnet/runtime - Int128.cs (GitHub)](https://github.com/dotnet/runtime/blob/5535e31a712343a63f5d7d796cd874e563e5ac14/src/libraries/System.Private.CoreLib/src/System/Int128.cs)
