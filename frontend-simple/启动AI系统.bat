@echo off
chcp 65001 >nul
echo ======================================
echo  智能手机评价分析系统 - AI助手版
echo ======================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖包
echo [1/4] 检查依赖包...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装依赖包...
    pip install flask flask-cors requests
)

REM 检查数据文件
echo [2/4] 检查数据文件...
if not exist "data\reviews.json" (
    echo [错误] 数据文件不存在: data\reviews.json
    pause
    exit /b 1
)

REM 启动后端服务（新窗口）
echo [3/4] 启动后端AI服务 (端口 5000)...
start "后端AI服务" cmd /k "python ai_assistant.py"

REM 等待后端启动
timeout /t 3 >nul

REM 启动前端服务（新窗口）
echo [4/4] 启动前端HTTP服务器 (端口 8000)...
start "前端HTTP服务器" cmd /k "python -m http.server 8000"

REM 等待前端启动
timeout /t 2 >nul

REM 打开浏览器
echo.
echo ======================================
echo  系统启动成功！
echo ======================================
echo.
echo  访问地址：
echo  http://localhost:8000
echo.
echo  功能说明：
echo  1. 在首页选择手机品牌和型号
echo  2. 在AI助手面板输入问题
echo  3. 示例: 3000元预算推荐哪款手机？
echo.
echo  按任意键打开浏览器...
pause >nul
start http://localhost:8000
