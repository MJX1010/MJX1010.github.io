@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ==============================
echo   Quartz 一键发布
echo ==============================
echo.

:: 检查是否有变更
git status --short >nul 2>&1
if "%errorlevel%"=="0" (
    git diff --quiet --exit-code 2>nul && git diff --cached --quiet --exit-code 2>nul
    if errorlevel 1 (
        echo [INFO] 检测到内容变更，准备发布...
    ) else (
        echo [INFO] 没有检测到本地变更，仍将尝试推送...
    )
)

:: 使用 quartz sync 自动 add / commit / push（--no-pull 跳过拉取 Quartz 框架更新）
echo [STEP] 同步并推送到 GitHub...
npx quartz sync --no-pull

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] 发布失败，请检查网络或 git 配置。
    pause
    exit /b 1
)

echo.
echo [OK] 发布成功！GitHub Actions 将自动构建并部署。
echo      站点地址: https://mjx1010.github.io
echo.
pause
