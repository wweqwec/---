@echo off
chcp 65001 > nul
echo ================================
echo 手机评价分析系统 - 启动脚本
echo ================================
echo.

REM 检查端口是否被占用
netstat -ano | findstr ":8080" > nul
if %errorlevel% == 0 (
    echo [警告] 端口8080已被占用，尝试停止旧进程...
    for /f "tokens=5" %%i in ('netstat -ano ^| findstr ":8080"') do taskkill /f /pid %%i > nul 2>&1
    timeout /t 2 > nul
)

netstat -ano | findstr ":5000" > nul
if %errorlevel% == 0 (
    echo [警告] 端口5000已被占用，尝试停止旧进程...
    for /f "tokens=5" %%i in ('netstat -ano ^| findstr ":5000"') do taskkill /f /pid %%i > nul 2>&1
    timeout /t 2 > nul
)

echo [1/3] 启动后端AI服务...
start "后端AI服务" cmd /k "cd /d %~dp0frontend-simple && python ai_assistant.py"

echo [2/3] 等待后端启动...
timeout /t 5 > nul

echo [3/3] 启动前端HTTP服务器...
start "前端HTTP服务器" cmd /k "cd /d %~dp0frontend-simple && python -m http.server 8080"

echo.
echo ================================
echo 服务启动中，请稍候...
echo ================================
timeout /t 3 > nul

echo 正在打开浏览器...
start http://localhost:8080

echo.
echo ✅ 如果浏览器未自动打开，请手动访问：
echo    http://localhost:8080
echo.
echo ⚠️  请勿关闭这两个命令行窗口！
echo    关闭窗口将停止网站服务。
echo.
echo 按任意键退出此窗口...
pause > nul
