@echo off
chcp 65001 >nul
echo ==========
echo  启动手机评价分析系统
echo ==========
echo.

cd /d "%~dp0"

echo [1/2] 正在启动后端AI服务...
start "后端AI服务" cmd /c "python ai_assistant.py"

echo [2/2] 正在启动前端服务...
timeout /t 3 >nul
start "前端服务" cmd /c "python -m http.server 8080"

echo.
echo ==========
echo  服务启动完成！
echo ==========
echo.
echo 访问地址：
echo   前端页面: http://localhost:8080
echo   AI助手API: http://localhost:5000/api/health
echo.
echo 功能说明：
echo   1. 在首页选择手机品牌和型号
echo   2. 在AI助手面板输入问题，获取智能推荐
echo   3. 示例问题："3000元预算推荐哪款手机？"
echo.
echo 按任意键打开浏览器...
pause >nul
start http://localhost:8080
