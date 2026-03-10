@echo off
echo 启动自主智能体系统

REM 检查环境变量
if not exist backend\.env (
    echo 未找到 .env 文件，从模板复制...
    copy backend\.env.example backend\.env
    echo 请编辑 backend\.env 添加 ANTHROPIC_API_KEY
    pause
    exit
)

REM 创建数据目录
if not exist data mkdir data
if not exist data\consciousness mkdir data\consciousness
if not exist data\creations mkdir data\creations

REM 启动后端
echo 启动后端...
cd backend
start cmd /k "uvicorn api.main:app --reload --host 0.0.0.0 --port 8000"
cd ..

REM 等待后端启动
timeout /t 3 /nobreak

REM 启动前端
echo 启动前端...
cd frontend
start cmd /k "npm run dev"
cd ..

echo.
echo 系统已启动
echo 前端: http://localhost:5173
echo 后端: http://localhost:8000
echo API文档: http://localhost:8000/docs
pause
