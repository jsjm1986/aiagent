#!/bin/bash

echo "🚀 启动自主智能体系统"

# 检查环境变量
if [ ! -f backend/.env ]; then
    echo "⚠️  未找到 .env 文件，从模板复制..."
    cp backend/.env.example backend/.env
    echo "请编辑 backend/.env 添加 ANTHROPIC_API_KEY"
    exit 1
fi

# 创建数据目录
mkdir -p data/consciousness data/creations

# 启动后端
echo "📦 启动后端..."
cd backend
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端
echo "🎨 启动前端..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ 系统已启动"
echo "前端: http://localhost:5173"
echo "后端: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止"

# 等待
wait
