@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ==============================
echo   Quartz 一键发布
echo ==============================
echo.

for /f %%i in ('git branch --show-current') do set CURRENT_BRANCH=%%i
if /I not "%CURRENT_BRANCH%"=="main" (
    echo [ERROR] 当前分支是 %CURRENT_BRANCH%，请切换到 main 后再发布。
    pause
    exit /b 1
)

echo [STEP] 生成 Unity 知识索引...
python scripts\build_unity_note_index.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Unity 知识索引生成失败。
    pause
    exit /b 1
)

echo [STEP] 执行 Quartz 构建校验...
npx quartz build
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Quartz 构建失败，请先修复后再发布。
    pause
    exit /b 1
)

echo [STEP] 复制微信读书图书馆静态页...
if not exist "public\weread" mkdir "public\weread"
copy /Y "weread-analysis\index.html" "public\weread\index.html" >nul
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] 复制 weread-analysis\index.html 失败。
    pause
    exit /b 1
)

echo [STEP] 隐私预检扫描...
python scripts\harness.py privacy-scan --path content
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] 隐私扫描发现敏感内容，请先修复后再发布。
    pause
    exit /b 1
)

echo [STEP] 暂存所有改动...
git add -A

git diff --cached --quiet --exit-code 2>nul
if %errorlevel% equ 0 (
    echo [INFO] 没有新的已暂存改动，将直接尝试推送 main。
) else (
    set "COMMIT_MSG=Publish knowledge base"
    if not "%~1"=="" set "COMMIT_MSG=%~1"
    echo [STEP] 提交改动...
    git commit -m "%COMMIT_MSG%"
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] git commit 失败，请检查冲突或 Git 配置。
        pause
        exit /b 1
    )
)

echo [STEP] 推送到 origin/main...
git push origin main

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] 推送失败，请检查网络、凭据或远程分支状态。
    pause
    exit /b 1
)

echo.
echo [OK] 发布完成！GitHub Actions 将自动构建并部署。
echo      仓库: https://github.com/MJX1010/MJX1010.github.io
echo      站点: https://mjx1010.github.io
echo.
pause
