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
last_curated: 2026-06-11
source_count: 175
---

## 定位说明

C / C# / C++ 的官方 API 文档和在线参考工具汇总，作为日常开发的快速查阅入口。在线编译器（Coliru / Compiler Explorer / C++ Insights）见 [[在线工具与协作]]。

## 一、C++ 参考

> 在线编译器 (Coliru / C++ Insights / Compiler Explorer) 见 [[在线工具与协作]]

- **[cppreference](https://en.cppreference.com/cpp)**（中英文）：最完整的 C++ 标准库参考，建议中英文对照查阅
- **[cplusplus.com](https://cplusplus.com/)**：对初学者更友好，示例代码更完整
- **[Microsoft C++ 文档](https://learn.microsoft.com/zh-cn/cpp/?view=msvc-170)**（learn.microsoft.com）：MSVC / Windows 开发场景专用
- C++ Core Guidelines 见 [[平台与规范]]

## 二、C# / .NET 参考

- **[C# 语言参考](https://learn.microsoft.com/zh-cn/dotnet/csharp/language-reference/)**（learn.microsoft.com）：最权威的官方语法入口
- **[System Namespace](https://learn.microsoft.com/zh-cn/dotnet/api/system?view=net-8.0)**（.NET 8）：查阅基础类型和集合 API
- **[.NET 工具和诊断文档](https://learn.microsoft.com/zh-cn/dotnet/core/diagnostics/)**：性能分析、dump 分析、dotnet-trace 等工具入口
- **[NuGet Gallery](https://www.nuget.org/)**：第三方包查找，DevToys.JsonToCsharp、Scriban 等常用工具包

## 三、源代码参考

- **[dotnet/runtime](https://github.com/dotnet/runtime)**（GitHub）：.NET 运行时源码，查阅底层实现（如 Int128）
- **[Visual Studio 扩展性文档](https://learn.microsoft.com/zh-cn/visualstudio/extensibility/?view=vs-2022)**（Microsoft Learn）：VS SDK、扩展模型和开发入口
- **[PIX on Windows](https://devblogs.microsoft.com/pix/download/)**：DirectX 性能分析和调试工具

## 四、相关学习参考

- [FP16/FP32 浮点格式解析](https://blog.csdn.net/yuanmomoya/article/details/147327546)：GPU 和 AI 推理场景必读
- [CLR Via C#（语雀笔记版）](https://www.yuque.com/fhlsteven/clr_via_csharp)：深入理解 .NET 运行时的系统性资料
- Maven / NuGet 制品仓库：Android 和 .NET 依赖管理查询入口

## 资料收敛说明

- 本页属于“入口型”清单，正文中的核心文档、源码仓库和工具入口已直接绑定链接。
- 文末只保留正文之外仍值得单独回看的源码片段或专题文章。


### .NET 运行时与 CLR

- [MVVM框架总结_lua mvvm_程序员菜鸟的博客-CSDN博客](https://blog.csdn.net/qq_40947718/article/details/108295965)
- [支持Lua语言的MVVM游戏框架_lua mvvm_clark_ya的博客-CSDN博客](https://blog.csdn.net/clark_ya/article/details/100575590)
- [VO,DTO,DO,PO的概念、区别和用处_dto vo po bo_Marvin-Fox的博客-CSDN博客](https://blog.csdn.net/fox_bert/article/details/102557904)
- [Lua语言模型 与 Redis应用_菜鸟-翡青的博客-CSDN博客](https://blog.csdn.net/zjf280441589/article/details/52716720)
- [位运算及其应用详解-zhenhuaqin-ChinaUnix博客](http://blog.chinaunix.net/uid-21411227-id-1826986.html)
- [(20条消息) 位运算简介及实用技巧_eff666的博客-CSDN博客](https://blog.csdn.net/eff666/article/details/52071252)
- [(20条消息) 你不知道的Runnable接口，深度解析Runnable接口_zhangxiaowei-CSDN博客_runnable接口](https://blog.csdn.net/zxw136511485/article/details/53032658)
- [(20条消息) Android(线程一) 线程_zhangxiaowei-CSDN博客_android线程](https://blog.csdn.net/zxw136511485/article/details/51541114)
- [(20条消息) Android(线程二) 线程池详解_zhangxiaowei-CSDN博客](https://blog.csdn.net/zxw136511485/article/details/51559759)
- [(20条消息) java中使用length获取二维数组的长度_cnheasy-CSDN博客_二维数组length取得是谁](https://blog.csdn.net/yz972641975/article/details/45666343)
- [(20条消息) Java中如何遍历Map对象的4种方法_Java高知-CSDN博客_遍历map](https://blog.csdn.net/tjcyjd/article/details/11111401)
- [(21条消息) Java 枚举(enum) 详解7种常见的用法_请叫我大师兄-CSDN博客_枚举类型enum用法](https://blog.csdn.net/qq_27093465/article/details/52180865)
- [(21条消息) 扩展类的三种方式（继承，装饰模式，动态代理）_四月的萤火之光的博客-CSDN博客](https://blog.csdn.net/a15920804969/article/details/78512386)
- [(19条消息) 几种Python执行时间的计算方法_wangshuang1631的博客-CSDN博客_python计算运行时间](https://blog.csdn.net/wangshuang1631/article/details/54286551)
- [序列化方案选型对比 - JSON/ProtocolBuffer/FlatBuffer/DIMBIN - 阿里云技术博客的个人空间 - OSCHINA - 中文开源技术交流社区](https://my.oschina.net/u/1464083/blog/3070131)
- [(21条消息) 详解Java异常Throwable、Error、Exception、RuntimeException的区别_Ganymede的Hadoop世界-CSDN博客](https://blog.csdn.net/kwu_ganymede/article/details/51382461)
- [(21条消息) HashMap、ConcurrentHashMap和SynchronizedMap – 哈希表在Java中的同步处理_逆水行舟-CSDN博客](https://blog.csdn.net/hwz2311245/article/details/51454686)
- [(21条消息) java反射之Method类中invoke（）方法的使用_qq30211478的博客-CSDN博客](https://blog.csdn.net/qq30211478/article/details/77834688)
- [(21条消息) java 反射机制 之 getMethod获取公有方法 getDeclaredMethod获取所有方法 然后invoke执行其所有方法_不废话快上车-CSDN博客](https://blog.csdn.net/qq_35146878/article/details/78504268)
- [(21条消息) java如何获取方法参数名_曾舜尧的专栏-CSDN博客_java 获取方法名和参数](https://blog.csdn.net/zengshunyao/article/details/82998328)
- [(21条消息) Java自定义注解+动态代理实现字段注入，方法拦截_jiangzhoudhkvg的博客-CSDN博客](https://blog.csdn.net/jiangzhoudhkvg/article/details/104314971)
- [(21条消息) 化解一个误区,其实switch和enum是可以很方便配合使用的_bright789的博客-CSDN博客](https://blog.csdn.net/bright789/article/details/50987552)
- [(21条消息) Android中UI线程（主线程）和子线程间的通讯方式比较_liugec的博客-CSDN博客_android 线程间通信方式](https://blog.csdn.net/liugec/article/details/78731626)
- [如何提高使用Java反射的效率？ - 深夜里的程序猿 - OSCHINA - 中文开源技术交流社区](https://my.oschina.net/19921228/blog/3042643)
- [(21条消息) 如何利用缓存机制实现JAVA类反射性能提升30倍_gao2175的博客-CSDN博客](https://blog.csdn.net/gao2175/article/details/103045600)
- [Lua __index的作用___index lua_Mr卜颛的博客-CSDN博客](https://blog.csdn.net/qq_15559109/article/details/109666375?ydreferer=aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1NTU5MTA5L2FydGljbGUvZGV0YWlscy8xMDk2NjYzNzU%3D?ydreferer=aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzE1NTU5MTA5L2FydGljbGUvZGV0YWlscy8xMDk2NjYzNzU%3D)
- [Lua __index的作用___index lua_Mr卜颛的博客-CSDN博客](https://blog.csdn.net/qq_15559109/article/details/109666375)
- [导弹跟踪的简单实现逻辑_Kenight_的博客-CSDN博客](https://blog.csdn.net/kenight/article/details/103559245)
- [图的邻接矩阵和邻接表的比较_邻接表和邻接矩阵的区别_书法教育1的博客-CSDN博客](https://blog.csdn.net/qq_29134495/article/details/51376580)
- [TCP的三次握手、四次挥手--非常详细讲解_tcp三次握手_潇潇凤儿的博客-CSDN博客](https://blog.csdn.net/smileiam/article/details/78226816)
- [Regex.Match Method (System.Text.RegularExpressions) | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/system.text.regularexpressions.regex.match?view=net-8.0)
- [阿里云企航_万网域名_商标注册_资质备案_软件著作权_网站建设-阿里云](https://wanwang.aliyun.com/?utm_content=se_882117&gclid=EAIaIQobChMInuv73qCThAMVYiZ7Bx3s9wQgEAAYASABEgKWPfD_BwE)
- [Ha啤酒来大杯的-CSDN博客](https://blog.csdn.net/weixin_45029839?type=blog)
- [uMVVM开源项目学习_uyvm-CSDN博客](https://blog.csdn.net/weixin_45029839/article/details/118437963?spm=1001.2014.3001.5501)
- [【IMGUI】 各种辅助类 EditorGUIUtility、EditorUtility、GUIUtility、GUILayoutUtility_editorguiutility.iconcontent-CSDN博客](https://blog.csdn.net/dmk17771552304/article/details/122500085)
- [知乎 - 安全中心](https://link.zhihu.com/?target=https%3A//blog.csdn.net/qq_41841073/article/details/128336434)
- [设计模式-Provider模式 - .Neterr - 博客园](https://www.cnblogs.com/fanfan-90/p/13473173.html)
- [Github无法访问的解决方法-CSDN博客](https://blog.csdn.net/qq_41839588/article/details/130051873)
- [Cysharp/R3: The new future of dotnet/reactive and UniRx.](https://github.com/Cysharp/R3)
- [ET_烟雨迷离半世殇的博客-CSDN博客](https://blog.csdn.net/qq_15020543/category_8624340.html)
- [ET篇：ETBook笔记(5.6 数值组件设计)_numericcomponent-CSDN博客](https://blog.csdn.net/qq_15020543/article/details/89397347)
- [ET实现游戏中邮件系统逻辑思路（服务端）_游戏邮件系统设计-CSDN博客](https://blog.csdn.net/qq_48512649/article/details/139926567)
- [如何确认电脑USB口哪个快（USB 3.0 3.2 Gen1 Gen2）_电脑如何查看usb接口速度-CSDN博客](https://blog.csdn.net/u013559309/article/details/129098681)
- [在 JetBrains Rider 中调试源生成器 | The .NET Tools Blog](https://blog.jetbrains.com/zh-hans/dotnet/2023/08/07/debug-source-generators-in-jetbrains-rider/)
- [科学计算机怎么用10次方,计算器里10次方怎么按-CSDN博客](https://blog.csdn.net/weixin_39816448/article/details/117944646)
- [网易游戏下载](https://adl.netease.com/d/g/uuremote/c/gw?type=pc)
- [详解C++ friend关键字_c++ string friend关键字无法识别-CSDN博客](https://blog.csdn.net/lwbeyond/article/details/7591415)
- [floating point - Difference between decimal, float and double in .NET? - Stack Overflow](https://stackoverflow.com/questions/618535/difference-between-decimal-float-and-double-in-net)
- [12-long-covid-brain-fog-jan-22-chinese-simplified.pdf](https://appnhs24wp41a8c38064.blob.core.windows.net/blobappnhs24wp41a8c38064/wp-content/uploads/2023/03/12-long-covid-brain-fog-jan-22-chinese-simplified.pdf)
- [阿赵3D-CSDN博客](https://blog.csdn.net/liweizhao?type=blog)
- [Vmware虚拟机Linux配置固定IP地址（详细版）_虚拟机固定ip-CSDN博客](https://blog.csdn.net/jsryin/article/details/123304582)
- [astc纹理压缩格式_长和宽都是2的整数次幂的长方形图片可以正常使用astc压缩吗-CSDN博客](https://blog.csdn.net/wangxiong_zh/article/details/114085488)
- [How to: Copy directories - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/standard/io/how-to-copy-directories)
- [String.Substring Method (System) | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/system.string.substring?view=net-8.0)
- [How to: Write text to a file - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/standard/io/how-to-write-text-to-a-file)
- [集成基础说明-TopOn | 帮助中心](https://help.toponad.net/cn/docs/wHwXTU)
- [TopOn | Boost Your Monetization Revenue of Mobile Ads](https://www.toponad.net/)
- [CPU流水线优化：控制冒险、分支预测与性能提升-CSDN博客](https://blog.csdn.net/zhizhengguan/article/details/121269908)
- [暴击的伪随机算法--PRD算法【转载】-CSDN博客](https://blog.csdn.net/a5292301/article/details/121465249)
- [Beyond Compare比较表格小窍门-CSDN博客](https://blog.csdn.net/chengling3991/article/details/100833813)
- [两水先木示-CSDN博客](https://blog.csdn.net/qq_39574690?type=blog)
- [blog.csdn.net](https://blog.csdn.net/qq_39574690/article/details/149902246?spm=1001.2014.3001.5502)
- [blog.csdn.net](https://blog.csdn.net/qq_39574690/article/details/150393509?spm=1001.2014.3001.5502)
- [图形引擎实战：Spine动画性能优化-CSDN博客](https://blog.csdn.net/qq_41166022/article/details/136097129)
- [Sentinel系列(12) - Sentinel之实时监控_sentinelone会监控电脑内容吗-CSDN博客](https://blog.csdn.net/qq_43437874/article/details/120007499)
- [荣耀手机，Android Studio调试时Logcat没有日志的解决办法_android studio logcat不打印日志-CSDN博客](https://blog.csdn.net/qq_39451645/article/details/145560159)
- [【烂笔头】各厂商手机手动抓log_三星平板sys dump菜单-CSDN博客](https://blog.csdn.net/abbiz/article/details/126183874)
- [2024最新Clash Meta for Android使用教程配置从入门到精通-Clash中文教程](https://www.cnclash.net/108.html)
- [TopOn](https://portal.toponad.net/m/app)
- [adb install 指定设备安装-CSDN博客](https://blog.csdn.net/magicbaby810/article/details/78812689)
- [Windows安装chocolatey过程_chocolatey包管理器cmd安装-CSDN博客](https://blog.csdn.net/m0_54267904/article/details/137041967)
- [scriban/scriban: A fast, powerful, safe and lightweight scripting language and engine for .NET](https://github.com/scriban/scriban)
- [stucampbell/AssemblyComparer: Simple utility to help compare .NET assemblies](https://github.com/stucampbell/AssemblyComparer)
- [What's new in the SDK and tooling for .NET 10 | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-10/sdk)

### C++ 语言基础

- [trumanzhao/luna: 基于C++17的lua/C++绑定库,以及lua的二进制序列化等辅助代码](https://github.com/trumanzhao/luna)
- [Eluna——简单,轻量级的c++和Lua绑定库 | radiotail's blog](https://radiotail.github.io/2014/10/28/Eluna%E5%8F%91%E5%B8%83/)
- [平衡蓝图和C++](https://mp.weixin.qq.com/s/9SY9uf-s3L1vG1Jp7LKkeg)
- [C++ 虚函数的内部实现 - __zxy - 博客园](https://www.cnblogs.com/zxyLeaf/p/virtual_func_cpp.html)
- [Memory Layout of C++ Object in Different Scenarios - huorexiaji - 博客园](https://www.cnblogs.com/tju1895/p/17104288.html)
- [c++ 正则表达式 - Bigben - 博客园](https://www.cnblogs.com/bigben0123/p/13948352.html)
- [C++视频教程_C++基础教程-慕课网课程](https://www.imooc.com/course/list?c=cplusplus)
- [C++ API  |  Protocol Buffers  |  Google Developers](https://developers.google.com/protocol-buffers/docs/reference/cpp#google.protobuf)
- [c++ - Optimize emulated flatbuffer dictionary - Stack Overflow](https://stackoverflow.com/questions/47388994/optimize-emulated-flatbuffer-dictionary)
- [fffaraz/awesome-cpp: A curated list of awesome C++ (or C) frameworks, libraries, resources, and shiny things. Inspire...](https://github.com/fffaraz/awesome-cpp)
- [fffaraz/awesome-cpp: A curated list of awesome C++ (or C) frameworks, libraries, resources, and shiny things. Inspire...](https://github.com/fffaraz/awesome-cpp#standard-libraries)
- [stleary/JSON-java: A reference implementation of a JSON package in Java.](https://github.com/stleary/JSON-java)
- [IL2CPP的内存问题 - UWA问答 | 博客 | 游戏及VR应用性能优化记录分享 | 侑虎科技](https://blog.uwa4d.com/archives/TechSharing_191.html)
- [现代 C++ 教程：高速上手 C++11/14/17/20](https://changkun.de/modern-cpp/pdf/modern-cpp-tutorial-zh-cn.pdf)
- [CPU分支预测原理：if-else性能优化指南 | 性能优化 | C++ 编程指南](https://chengxumiaodaren.com/docs/performance/branch-predict/)

### C# 语言特性

- [.net - Why is Dictionary preferred over Hashtable in C#? - Stack Overflow](https://stackoverflow.com/questions/301371/why-is-dictionary-preferred-over-hashtable-in-c)
- [c#中(StructLayout(LayoutKind.Sequential))的意思 - 竹木人 - 博客园](https://www.cnblogs.com/lonelydog/archive/2012/02/02/2335432.html)
- [FlatBuffers: Use in Java/C#](https://google.github.io/flatbuffers/flatbuffers_guide_use_java_c-sharp.html)
- [(19条消息) 无锁，线程安全，延迟加载的单例实现（C#）_Ian Zhang的专栏-CSDN博客](https://blog.csdn.net/zhanglei4214/article/details/12402373)
- [(19条消息) c#反射获取单例对象的实例_lonelyrains的专栏-CSDN博客](https://blog.csdn.net/lonelyrains/article/details/103294325)
- [Creating and Throwing Exceptions - C# Programming Guide | Microsoft Docs](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/exceptions/creating-and-throwing-exceptions)
- [C#泛型详解 - .NET开发菜鸟 - 博客园](https://www.cnblogs.com/dotnet261010/p/9034594.html)
- [C# 文档 - 入门、教程、参考。 | Microsoft Docs](https://docs.microsoft.com/zh-cn/dotnet/csharp/)
- [C#当中的泛型和java中的对比 - 奋斗的大橙子 - 博客园](https://www.cnblogs.com/dcz2015/p/5356146.html)
- [如何提高C# StringBuilder的性能 - 知乎](https://zhuanlan.zhihu.com/p/434724020)
- [C# - Difference between Int64 and UInt64](https://www.includehelp.com/dot-net/Int64-and-UInt64-in-c-sharp.aspx)
- [C#中的StringBuilder - 苏打兴 - 博客园](https://www.cnblogs.com/lcxBlog/p/4508031.html)
- [C# 垃圾回收机制GC详解 - 掘金](https://juejin.cn/post/7000873616178937887)
- [c# - string.ToLower() and string.ToLowerInvariant() - Stack Overflow](https://stackoverflow.com/questions/6225808/string-tolower-and-string-tolowerinvariant)
- [C#读写Excel（NPOI）_vs if(filename.indexof)-CSDN博客](https://blog.csdn.net/qq_33459369/article/details/79316851)
- [c# - Why is access to the path denied? - Stack Overflow](https://stackoverflow.com/questions/8821410/why-is-access-to-the-path-denied)
- [c# - System.IO.IOException: Sharing violation on path - Stack Overflow](https://stackoverflow.com/questions/59562067/system-io-ioexception-sharing-violation-on-path)
- [c# - How to read StreamReader text line by line - Stack Overflow](https://stackoverflow.com/questions/37103839/how-to-read-streamreader-text-line-by-line)
- [C#?和??的作用_c# ?.作用-CSDN博客](https://blog.csdn.net/simpleshao/article/details/86646836)
- [C#语法 - 标签 - JerryMouseLi - 博客园](https://www.cnblogs.com/JerryMouseLi/tag/C%23%E8%AF%AD%E6%B3%95/)
- [C# 中大端序与小端序 - JerryMouseLi - 博客园](https://www.cnblogs.com/JerryMouseLi/p/13997445.html)
- [linq介绍及工作中应用两例——左联与内联，linq循环方法 - JerryMouseLi - 博客园](https://www.cnblogs.com/JerryMouseLi/p/13356790.html)
- [深入浅出C#结构体——封装以太网心跳包的结构为例 - JerryMouseLi - 博客园](https://www.cnblogs.com/JerryMouseLi/p/12606920.html)
- [在C#中用静态类来扩展类的方法 - JerryMouseLi - 博客园](https://www.cnblogs.com/JerryMouseLi/p/11121884.html)
- [C# - 随笔分类(第4页) - 三页菌 - 博客园](https://www.cnblogs.com/sanyejun/category/1116418.html?page=4)
- [C# 开启新线程的几种方式 多线程_c# 新线程-CSDN博客](https://blog.csdn.net/g313105910/article/details/115749664)
- [Delegates and lambdas - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/standard/delegates-lambdas)
- [Events in C#](https://www.tutorialsteacher.com/csharp/csharp-event)
- [C# 字符串替换第一次或者最后一次出现的匹配项_c# 匹配字符第一个出线-CSDN博客](https://blog.csdn.net/cxu123321/article/details/94847516)
- [Enumerable.cs](https://referencesource.microsoft.com/#System.Core/System/Linq/Enumerable.cs,e276d6892241255b)
- [c# - Example of why IReadOnlyList<T> is better than public List<T> { get; private set; } - Code Review Stack Exchange](https://codereview.stackexchange.com/questions/244067/example-of-why-ireadonlylistt-is-better-than-public-listt-get-private-set)
- [C# 7.0 新特性：本地方法 - 冠军 - 博客园](https://www.cnblogs.com/haogj/p/7636915.html)
- [Convert int to enum in C#](https://www.tutorialsteacher.com/articles/convert-int-to-enum-in-csharp)
- [C#标记废弃方法_c# 标记某个方法不再使用-CSDN博客](https://blog.csdn.net/arrowzz/article/details/56305957)
- [C# String 前面不足位数补零的方法_string长度不够前面补a-CSDN博客](https://blog.csdn.net/jiankunking/article/details/17992857)
- [C# 中结构体与类的区别，值类型一定存放在栈上么？_c# 结构体数组存储在堆还是栈-CSDN博客](https://blog.csdn.net/qq_30585525/article/details/118937481)
- [CLR Via C# 读书笔记-第23章（程序集加载和反射）_assembly.loadfrom加载的程序集是否存在引用的程序集-CSDN博客](https://blog.csdn.net/weixin_45029839/article/details/122732568)
- [C# 10核心技术指南 - (澳)约瑟夫·阿坝哈瑞 - 微信读书](https://weread.qq.com/web/reader/78c32900813ab9613g016259)
- [ET篇：ETBook笔记(3.4 事件机制EventSystem)-CSDN博客](https://blog.csdn.net/qq_15020543/article/details/88203599)
- [c# - How create a new deep copy (clone) of a List<T>? - Stack Overflow](https://stackoverflow.com/questions/14007405/how-create-a-new-deep-copy-clone-of-a-listt)
- [c# struct 灵魂拷问 - 知乎](https://zhuanlan.zhihu.com/p/380603333)
- [推荐.Net、C# 逆向反编译四大工具利器 - 知乎](https://zhuanlan.zhihu.com/p/360022233)
- [原则2：偏爱 readonly 而不是 const | Effective C# 改善C#程序的50种方法](https://wizardforcel.gitbooks.io/effective-csharp/content/2.html)
- [amis92/csharp-source-generators: A list of C# Source Generators (not necessarily awesome) and associated resources: a...](https://github.com/amis92/csharp-source-generators?tab=readme-ov-file)
- [C#压缩和解压文件 - zhaotianff - 博客园](https://www.cnblogs.com/zhaotianff/p/9408695.html)
- [susices/NativeCollection: Native Collection library in c#](https://github.com/susices/NativeCollection)
- [C#结合.NET框架快速构建和部署AI应用_c#如何部署ai-CSDN博客](https://petergao.blog.csdn.net/article/details/144153689)
- [c#_sort排序函数的返回值 - 赵青青 - 博客园](https://www.cnblogs.com/zhaoqingqing/p/11760117.html)
- [C#计算一段程序运行时间的三种方法_c# 统计方法执行时间-CSDN博客](https://blog.csdn.net/xzjxylophone/article/details/6832160)
- [Releases · icsharpcode/ILSpy](https://github.com/icsharpcode/ILSpy/releases)
- [Decimal in C# : How and Where to Use It? (2024)](https://www.bytehide.com/blog/decimal-csharp)
- [C# |构造函数中的继承 开发文档](https://moonapi.com/news/28257.html)
- [如何使用集合初始值设定项初始化字典 - C# 编程指南 - C# | Microsoft Learn](https://learn.microsoft.com/zh-cn/dotnet/csharp/programming-guide/classes-and-structs/how-to-initialize-a-dictionary-with-a-collection-initializer)
- [静态类和静态类成员 - C# 编程指南 - C# | Microsoft Learn](https://learn.microsoft.com/zh-cn/dotnet/csharp/programming-guide/classes-and-structs/static-classes-and-static-class-members)
- [对象和集合初始值设定项 - C# 编程指南 - C# | Microsoft Learn](https://learn.microsoft.com/zh-cn/dotnet/csharp/programming-guide/classes-and-structs/object-and-collection-initializers)
- [Func<T,TResult> Delegate (System) | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/system.func-2?view=net-8.0)
- [2 | 任务系统（Job System）和高性能C# 介绍_DOTS深度研究之原理分析篇_UWA学堂](https://edu.uwa4d.com/lesson-detail/158/784/0?isPreview=0)
- [c# - Difference between Object and object - Stack Overflow](https://stackoverflow.com/questions/3070628/difference-between-object-and-object)
- [C#教程 - 泛型（Generic Types） - 重庆熊猫 - 博客园](https://www.cnblogs.com/cqpanda/p/16690994.html)
- [C++ 模板与 C# 泛型的区别 - C# 编程指南 - C# | Microsoft Learn](https://learn.microsoft.com/zh-cn/dotnet/csharp/programming-guide/generics/differences-between-cpp-templates-and-csharp-generics)
- [c# - Can I convert long to int? - Stack Overflow](https://stackoverflow.com/questions/858904/can-i-convert-long-to-int)
- [Pinbox - 跨平台收藏工具](https://withpinbox.com/search?q=c#%20this%E8%AE%BF%E9%97%AE%E5%99%A8)
- [在C#中，ToUpper()和ToUpperInvariant()有什么不同？-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/ask/sof/72679/answer/102102462)
- [c# - Copying Files Recursively - Stack Overflow](https://stackoverflow.com/questions/7064864/copying-files-recursively)
- [文件处理_c# filestream 覆盖-CSDN博客](https://blog.csdn.net/zsx157326/article/details/50985321)
- [C#之MVVM篇快速入门 - 清安宁 - 博客园](https://www.cnblogs.com/qinganning/p/18974824)
- [WPF/C#：理解与实现WPF中的MVVM模式 - mingupupup - 博客园](https://www.cnblogs.com/mingupupu/p/18218027)
- [c# - Understanding MVVM - How to bind data view ↔ ViewModel + catch Key pressed on view and start function in viewMod...](https://stackoverflow.com/questions/43127642/understanding-mvvm-how-to-bind-data-view-%E2%86%94-viewmodel-catch-key-pressed-on-vi)
- [NuGet Gallery | DevToys.JsonToCsharp 1.1.0](https://www.nuget.org/packages/DevToys.JsonToCsharp#readme-body-tab)
- [【Python】Python与C#的消息传递_c# python json-CSDN博客](https://blog.csdn.net/zigzagbomb/article/details/101212111)
- [ad313/SourceGenerator.Template: C# Source Generator，easy to generate code using templates](https://github.com/ad313/SourceGenerator.Template)
- [vovgou/loxodon-framework: An MVVM & Databinding framework that can use C# and Lua to develop games](https://github.com/vovgou/loxodon-framework)
- [yukuyoulei/ConfigExcel: 【ConfigExcel】 excel导出成C#类并填充数据，省去序列化和反序列化的消耗。以前是不能热更，不往这方面想，能热更了为啥lua能当配置表C#就不行](https://github.com/yukuyoulei/ConfigExcel)
- [pty819/csharpbooks](https://github.com/pty819/csharpbooks)

### 其他参考

- [Downloads - NoSQLBooster for MongoDB](https://www.mongobooster.com/downloads)
- [NuGet Gallery | Packages matching Tags:"devtoys-app" json](https://www.nuget.org/packages?q=Tags%3A%22devtoys-app%22+json&includeComputedFrameworks=true&prerel=true&sortby=relevance)

## 参考链接

> 以下链接仅保留正文之外仍值得单独回看的补充资料。

### 官方文档

- [list.cs](https://referencesource.microsoft.com/)

### 开源项目

- [fanslead/Learn-SourceGenerator: 学习SourceGenerator代码仓库](https://github.com/fanslead/Learn-SourceGenerator)
- [dotnet/runtime - Int128.cs (GitHub)](https://github.com/dotnet/runtime/blob/5535e31a712343a63f5d7d796cd874e563e5ac14/src/libraries/System.Private.CoreLib/src/System/Int128.cs)
- [ihaiucom/learn.AStarPathfinding: A* Pathfinding Project Pro](https://github.com/ihaiucom/learn.AStarPathfinding)

### 补充阅读

- [Animating in C++: Curves and Easing Functions - Tom Looman](https://www.tomlooman.com/animating-in-cpp-curves-and-easing-functions/)