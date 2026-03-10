# 快速开始指南

## 前置要求

- Python 3.11+
- Node.js 18+
- Anthropic API Key

## 安装步骤

### 1. 后端设置

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

编辑 `.env` 文件，添加你的 API Key：
```
ANTHROPIC_API_KEY=your_key_here
```

### 2. 前端设置

```bash
cd frontend
npm install
```

### 3. 启动系统

**方式一：使用启动脚本**

Windows:
```bash
start.bat
```

Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

**方式二：手动启动**

终端1 - 后端:
```bash
cd backend
uvicorn api.main:app --reload
```

终端2 - 前端:
```bash
cd frontend
npm run dev
```

**方式三：Docker**

```bash
docker-compose up
```

## 访问系统

- 前端界面: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 验证运行

1. 打开前端界面
2. 查看 WebSocket 连接状态（应显示🟢已连接）
3. 观察驱动力仪表盘是否有数据
4. 查看意识流是否有记录

## 故障排除

**后端无法启动**
- 检查 Python 版本
- 确认已安装所有依赖
- 验证 API Key 是否正确

**前端无法连接**
- 确认后端已启动
- 检查端口 8000 是否被占用
- 查看浏览器控制台错误

**WebSocket 连接失败**
- 确认后端运行正常
- 检查防火墙设置
- 尝试刷新页面
