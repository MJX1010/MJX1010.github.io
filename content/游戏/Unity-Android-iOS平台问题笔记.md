---
title: Unity Android iOS 平台问题笔记
tags:
  - Unity
  - Android
  - iOS
  - 移动端
  - 发布
---

## 结论

- 移动端问题通常发生在 Unity、原生 SDK、系统版本、商店政策和构建工具链的交界处。
- Android 16 KB Page Size、SDK 版本升级、OpenURL 文件权限、ANR、Crashlytics 符号化都是发布前必须单独验证的风险点。
- iOS 侧要重点关注符号表、Framework 链接、动态字体、UnityFramework 和原生插件兼容。
- 平台问题不能只在 Editor 验证，必须用真机、Release 包、目标 ABI 和线上等价构建配置验证。

## Android 关注点

- Android 16 KB Page Size 要求会影响 native library，对 Unity 版本、NDK、第三方 so 和打包方式都有要求。
- SDK 34 等 Target API 升级可能引发权限、文件访问、通知、广告 SDK 和 Gradle 插件兼容问题。
- Android 7 之后 `OpenURL()` 打开本地文件受 FileProvider / URI 权限限制影响，不能继续依赖旧的 `file://` 行为。
- ANR 常见于主线程阻塞、SDK 初始化、广告回调、文件 IO、网络等待和 Unity 与原生线程交互。
- Crashlytics 上报要确认符号文件上传完整，否则 native crash 难以定位。

### Android 构建链风险

- AGP、Gradle、JDK、NDK 和 Unity Editor 之间存在隐性兼容关系，升级前应先在最小工程验证。
- 多渠道包要检查 Manifest 合并结果，尤其是 `provider`、`activity`、`queries`、`uses-permission` 和 `exported`。
- Native crash 必须保留 tombstone、Build ID、ABI、符号文件和构建产物，否则只能看到不可读地址。
- 三方 SDK 初始化应延后、异步化并记录耗时，避免启动阶段同时初始化广告、统计、支付、推送和分享。

## iOS 关注点

- iOS 崩溃排查依赖 dSYM / cSYM / 符号化流程，上传失败会导致堆栈不可读。
- UnityFramework.framework 链接问题可能与 Unity 版本、Xcode 设置、插件集成方式有关。
- 动态字体纹理、CJK 字体、TextMeshPro fallback 在 iOS/Mac 上要做专项测试。
- 原生 SDK 要检查 bitcode、最低系统版本、隐私清单、权限描述和 App Store 审核要求。

### iOS 构建链风险

- Pod 版本升级应和 Unity 导出的 Xcode 工程脚本一起验证，避免本机可编译、CI 或打包机失败。
- Framework Search Paths、Other Linker Flags、静态库/动态库混用容易导致只在 Release 包暴露的问题。
- 权限描述、隐私清单、URL Scheme、Associated Domains、ATS 配置都应在提审前导出复核。
- dSYM/cSYM 上传要验证构建 UUID 是否匹配，不能只看上传命令是否成功。

## 第三方 SDK

- Firebase、Crashlytics、广告 SDK、ShareSDK、TopOn、AppLovin 等都可能引入 Gradle、Manifest、权限和 native library 冲突。
- SDK 初始化应避免阻塞主线程，必要时拆分到启动后异步流程。
- SDK 版本升级要记录兼容矩阵：Unity 版本、Gradle、AGP、Android SDK、iOS SDK、Xcode。
- 接入 SDK 后要新增最小复现工程或自动化冒烟测试，避免主工程里问题难以定位。

## 版本矩阵

- 每次平台升级至少记录：Unity 版本、Android SDK、AGP、Gradle、JDK、NDK、Xcode、Pods、三方 SDK 版本。
- 版本矩阵要区分开发环境、CI 环境、打包机环境和线上正式包，避免只在个人电脑验证成功。
- 对广告、支付、统计、分享、推送类 SDK 建立冒烟测试：初始化、登录态、权限、回调、前后台切换、弱网和隐私弹窗。
- 所有三方 SDK 的 Manifest、Info.plist、权限和隐私声明都要在提审前导出并人工复核。

## 排查流程

1. 明确问题发生平台、系统版本、机型、Unity 版本和构建配置。
2. 使用 Release/IL2CPP/目标 ABI 复现，不要只看 Editor 或 Development Build。
3. 收集平台日志：Android `logcat`、ANR trace、tombstone；iOS device log、crash log、symbolicated stack。
4. 排除第三方 SDK：按二分法禁用插件、资源、初始化逻辑。
5. 检查构建链：Gradle、AGP、NDK、Xcode、Pods、Manifest、Info.plist、Framework 链接。
6. 修复后建立发布前 checklist，避免下次 SDK 或 Target API 升级再次踩坑。

## 发布检查清单

- Android 是否验证 16 KB Page Size 兼容。
- Target API / Compile SDK / AGP / Gradle 是否与 Unity 版本匹配。
- 所有 native so 是否覆盖目标 ABI。
- Crashlytics 符号文件是否上传并能正确符号化。
- ANR 是否有主线程堆栈和 SDK 初始化耗时记录。
- iOS dSYM 是否上传并能还原堆栈。
- Framework、Pods、权限描述和隐私清单是否符合当前商店要求。
- OpenURL、文件分享、相册、相机、通知等系统能力是否真机验证。

## 参考链接

> 以下链接作为本笔记的资料来源保留。

### GitHub 相关链接

- [Firebase Unity cSYM 符号化问题](https://github.com/firebase/quickstart-unity/issues/745)

### 链接分组

- [Unity 项目支持 Android 16 KB 的方案](https://developer.unity.cn/projects/6854c4fcedbc2ada96ddb533)
- [Android 适配 16 KB Page Size](https://developer.unity.cn/projects/687efd5fedbc2aa66b703c86)
- [Android OpenURL 本地文件问题](https://issuetracker.unity3d.com/issues/android-openurl-doesnt-open-local-files-on-android-6-if-target-api-level-is-23)
- [Android SDK 34 构建讨论](https://discussions.unity.com/t/cant-build-for-android-sdk-34/927940/35)
