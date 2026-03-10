# 原生自主智能体 - 全栈架构设计方案

## 一、系统概览

### 1.1 核心理念

基于提示词中的"原生自主智能体"理念，构建一个：
- **持续运行**的认知-行动系统
- **可视化**的意识流和决策过程
- **可交互**的 Web 界面
- **自主演化**的智能系统

### 1.2 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     Web UI (前端)                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │意识流面板│ │项目看板  │ │目标树    │ │创造画廊  │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │对话界面  │ │价值仪表盘│ │系统监控  │ │设置面板  │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
                            ↕ WebSocket + REST API
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI 后端服务                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ WebSocket    │  │ REST API     │  │ SSE Stream   │      │
│  │ 实时推送     │  │ 接口         │  │ 事件流       │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│              自主运行引擎 (Autonomous Engine)                │
│  持续循环：感知 → 认知 → 决策 → 行动 → 记录 → 演化         │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                smolagents + 自定义工具                       │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│              持久化层 (SQLite + JSON)                        │
└─────────────────────────────────────────────────────────────┘
```

## 二、前端设计

### 2.1 技术栈

```yaml
框架: React 18 + TypeScript
状态管理: Zustand
UI 组件: shadcn/ui + Tailwind CSS
实时通信: WebSocket (原生)
图表: Recharts
动画: Framer Motion
构建: Vite
```

### 2.2 页面结构

```
/
├── 主控台 (Dashboard)
│   ├── 意识流实时显示
│   ├── 当前行动状态
│   ├── 系统健康度
│   └── 快速统计
│
├── 意识流 (Consciousness)
│   ├── 时间线视图
│   ├── 思考类型过滤
│   ├── 搜索和回溯
│   └── 思考详情
│
├── 项目管理 (Projects)
│   ├── 看板视图 (Kanban)
│   ├── 项目详情
│   ├── 里程碑追踪
│   └── 下一步行动
│
├── 目标系统 (Goals)
│   ├── 目标树视图
│   ├── 战略/战术/操作层级
│   ├── 目标进度
│   └── 目标关系图
│
├── 创造画廊 (Creations)
│   ├── 网格视图
│   ├── 创造类型分类
│   ├── 价值排序
│   └── 创造详情
│
├── 对话界面 (Chat)
│   ├── 与智能体对话
│   ├── 历史记录
│   ├── 价值评估显示
│   └── 决策过程可视化
│
├── 价值分析 (Value Analytics)
│   ├── 价值评估历史
│   ├── 多维度雷达图
│   ├── 决策统计
│   └── 趋势分析
│
└── 系统设置 (Settings)
    ├── 配置管理
    ├── 工具管理
    └── 日志查看
```

### 2.3 核心界面设计

#### 2.3.1 意识流面板

```
┌─────────────────────────────────────────────────────────┐
│ 意识流 (Consciousness Stream)              [实时] [暂停] │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ⚡ 18:42:35  [DECISION]                                │
│  正在评估三个候选行动...                                 │
│  候选1: 推进项目 "自主智能体" (价值: 0.85)              │
│  候选2: 优化代码结构 (价值: 0.62)                       │
│  候选3: 学习新技术 (价值: 0.58)                         │
│  → 决策: 选择候选1                                      │
│                                                          │
│  💭 18:42:20  [REFLECTION]                              │
│  分析当前项目进度，发现需要完善前端界面...              │
│                                                          │
│  🔍 18:42:05  [EVALUATION]                              │
│  收到人类请求: "设计 Web UI"                            │
│  价值评估: 0.92 (高价值，符合长期目标)                  │
│                                                          │
│  [加载更多...]                                          │
└─────────────────────────────────────────────────────────┘
```

#### 2.3.2 项目看板

```
┌─────────────────────────────────────────────────────────┐
│ 项目看板                                    [+ 新建项目] │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  IDEA          PLANNING        ACTIVE        COMPLETED   │
│  ┌──────┐     ┌──────┐       ┌──────┐      ┌──────┐   │
│  │项目A │     │项目B │       │项目C │      │项目D │   │
│  │💡    │     │📋    │       │🚀    │      │✅    │   │
│  │价值:0.7│   │价值:0.8│     │价值:0.9│    │价值:0.8│ │
│  └──────┘     └──────┘       └──────┘      └──────┘   │
│                                                          │
│  当前聚焦: 项目C - 自主智能体开发                        │
│  下一步: 实现前端界面                                    │
│  进度: ████████░░ 75%                                   │
└─────────────────────────────────────────────────────────┘
```

#### 2.3.3 对话界面

```
┌─────────────────────────────────────────────────────────┐
│ 与智能体对话                                             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  你: 帮我分析一下当前项目的优先级                        │
│                                                          │
│  🤖 智能体:                                             │
│  [思考中...] 正在评估请求价值...                         │
│  价值评分: 0.78 ⭐⭐⭐⭐                                 │
│                                                          │
│  我分析了当前的 3 个活跃项目:                            │
│  1. 自主智能体开发 (优先级: 最高)                        │
│     - 价值: 0.92                                        │
│     - 理由: 符合长期目标，复利潜力高                     │
│                                                          │
│  2. 代码优化 (优先级: 中)                               │
│     - 价值: 0.65                                        │
│                                                          │
│  建议: 继续聚焦项目1，完成前端界面后再处理其他项目       │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  [输入消息...]                                  [发送]   │
└─────────────────────────────────────────────────────────┘
```


#### 2.3.4 价值仪表盘

```
┌─────────────────────────────────────────────────────────┐
│ 价值分析仪表盘                                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  最近决策价值分布                                        │
│  ┌────────────────────────────────────────────┐        │
│  │        ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫                    │        │
│  │    ⚫⚫                    ⚫⚫              │        │
│  │  ⚫                          ⚫            │        │
│  │ ⚫                            ⚫           │        │
│  │⚫      价值雷达图              ⚫          │        │
│  │ ⚫                            ⚫           │        │
│  │  ⚫                          ⚫            │        │
│  │    ⚫⚫                    ⚫⚫              │        │
│  │        ⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫                    │        │
│  └────────────────────────────────────────────┘        │
│                                                          │
│  价值维度得分:                                           │
│  价值:      ████████░░ 0.85                             │
│  影响:      ███████░░░ 0.72                             │
│  长期收益:  █████████░ 0.90                             │
│  可执行性:  ████████░░ 0.78                             │
│  复利潜力:  ████████░░ 0.82                             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 三、后端设计

### 3.1 技术栈

```yaml
Web框架: FastAPI
异步: asyncio + aiohttp
Agent: smolagents 1.24.0
LLM: Claude via LiteLLM
数据库: SQLite + SQLAlchemy
实时通信: WebSocket
任务队列: asyncio.Queue
监控: 自定义健康检查
```

### 3.2 目录结构

```
autonomous_agent/
├── frontend/                    # 前端代码
│   ├── src/
│   │   ├── components/         # React 组件
│   │   │   ├── Consciousness/  # 意识流组件
│   │   │   ├── Projects/       # 项目管理组件
│   │   │   ├── Goals/          # 目标管理组件
│   │   │   ├── Creations/      # 创造画廊组件
│   │   │   ├── Chat/           # 对话组件
│   │   │   └── Dashboard/      # 仪表盘组件
│   │   ├── stores/             # Zustand 状态管理
│   │   ├── hooks/              # 自定义 Hooks
│   │   ├── services/           # API 服务
│   │   └── App.tsx
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                     # 后端代码
│   ├── core/
│   │   ├── engine.py           # 自主运行引擎
│   │   ├── agent.py            # 扩展的 CodeAgent
│   │   ├── config.py           # 配置管理
│   │   └── events.py           # 事件系统
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── consciousness.py
│   │   │   ├── projects.py
│   │   │   ├── goals.py
│   │   │   ├── chat.py
│   │   │   └── system.py
│   │   ├── websocket.py        # WebSocket 处理
│   │   └── deps.py             # 依赖注入
│   │
│   ├── cognition/
│   │   ├── value_engine.py
│   │   ├── decision.py
│   │   └── candidate_gen.py
│   │
│   ├── memory/
│   │   ├── consciousness.py
│   │   ├── long_term.py
│   │   └── storage.py
│   │
│   ├── projects/
│   │   └── manager.py
│   │
│   ├── goals/
│   │   └── manager.py
│   │
│   ├── tools/                  # smolagents 工具
│   │   ├── consciousness_tool.py
│   │   ├── project_tool.py
│   │   ├── goal_tool.py
│   │   └── creation_tool.py
│   │
│   ├── models/                 # 数据模型
│   │   ├── consciousness.py
│   │   ├── project.py
│   │   ├── goal.py
│   │   └── creation.py
│   │
│   └── main.py                 # FastAPI 应用入口
│
├── data/                       # 数据目录
├── config/
│   └── default.yaml
├── requirements.txt
└── README.md
```

### 3.3 API 设计

#### 3.3.1 REST API

```python
# 意识流 API
GET    /api/consciousness/stream          # 获取意识流（分页）
GET    /api/consciousness/{id}            # 获取单条记录
POST   /api/consciousness/search          # 搜索意识流

# 项目 API
GET    /api/projects                      # 获取所有项目
GET    /api/projects/{id}                 # 获取项目详情
POST   /api/projects                      # 创建项目
PUT    /api/projects/{id}                 # 更新项目
DELETE /api/projects/{id}                 # 删除项目
GET    /api/projects/{id}/next-action     # 获取下一步行动

# 目标 API
GET    /api/goals                         # 获取所有目标
GET    /api/goals/tree                    # 获取目标树
POST   /api/goals                         # 创建目标
PUT    /api/goals/{id}                    # 更新目标
DELETE /api/goals/{id}                    # 删除目标

# 创造成果 API
GET    /api/creations                     # 获取所有创造
GET    /api/creations/{id}                # 获取创造详情
POST   /api/creations                     # 保存创造

# 对话 API
POST   /api/chat/message                  # 发送消息
GET    /api/chat/history                  # 获取历史

# 系统 API
GET    /api/system/status                 # 系统状态
GET    /api/system/stats                  # 统计信息
POST   /api/system/control                # 控制命令（暂停/恢复）
```

#### 3.3.2 WebSocket 事件

```python
# 客户端 → 服务器
{
  "type": "subscribe",
  "channels": ["consciousness", "projects", "system"]
}

# 服务器 → 客户端
{
  "type": "consciousness_update",
  "data": {
    "id": "uuid",
    "timestamp": "2026-03-09T18:42:35Z",
    "thought_type": "decision",
    "content": "...",
    "value_score": 0.85
  }
}

{
  "type": "project_update",
  "data": {
    "id": "uuid",
    "status": "active",
    "progress": 0.75
  }
}

{
  "type": "system_status",
  "data": {
    "running": true,
    "current_action": "...",
    "idle_time": 120
  }
}
```

### 3.4 核心后端实现

#### 3.4.1 FastAPI 应用 (main.py)

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from core.engine import AutonomousEngine
from api.routes import consciousness, projects, goals, chat, system
from api.websocket import websocket_endpoint

app = FastAPI(title="Autonomous Agent")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由
app.include_router(consciousness.router, prefix="/api/consciousness")
app.include_router(projects.router, prefix="/api/projects")
app.include_router(goals.router, prefix="/api/goals")
app.include_router(chat.router, prefix="/api/chat")
app.include_router(system.router, prefix="/api/system")

# WebSocket
app.add_websocket_route("/ws", websocket_endpoint)

# 静态文件（前端）
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")

# 全局引擎实例
engine = None

@app.on_event("startup")
async def startup():
    global engine
    engine = AutonomousEngine()
    # 在后台启动自主循环
    asyncio.create_task(engine.run_forever())

@app.on_event("shutdown")
async def shutdown():
    if engine:
        await engine.stop()
```


#### 3.4.2 WebSocket 管理 (websocket.py)

```python
from fastapi import WebSocket
from typing import Set
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        """广播消息到所有连接"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                self.disconnect(connection)

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # 处理客户端消息
            if data.get("type") == "subscribe":
                # 订阅特定频道
                pass
    except:
        manager.disconnect(websocket)
```

#### 3.4.3 自主引擎与前端集成 (engine.py)

```python
class AutonomousEngine:
    def __init__(self):
        # ... 初始化代码
        self.event_bus = EventBus()  # 事件总线
        
    async def run_forever(self):
        while self.running:
            # ... 主循环逻辑
            
            # 关键：每次行动后推送事件到前端
            if action:
                result = await self.execute_with_agent(action)
                
                # 推送意识流更新
                await self.event_bus.emit("consciousness_update", {
                    "id": result.id,
                    "timestamp": result.timestamp,
                    "thought_type": result.thought_type,
                    "content": result.content,
                    "value_score": result.value_score
                })
                
                # 推送项目更新
                if result.affects_project:
                    await self.event_bus.emit("project_update", {
                        "id": result.project_id,
                        "status": result.project_status,
                        "progress": result.project_progress
                    })
```

## 四、数据流设计

### 4.1 实时数据流

```
智能体行动
    ↓
记录到数据库
    ↓
触发事件
    ↓
WebSocket 推送
    ↓
前端实时更新
```

### 4.2 用户交互流

```
用户在前端发送消息
    ↓
POST /api/chat/message
    ↓
加入输入队列
    ↓
主循环感知到输入
    ↓
价值评估
    ↓
决策执行
    ↓
结果通过 WebSocket 返回
    ↓
前端显示响应
```

## 五、核心功能实现

### 5.1 意识流实时显示

**前端 (ConsciousnessStream.tsx)**
```typescript
import { useEffect, useState } from 'react'
import { useWebSocket } from '@/hooks/useWebSocket'

export function ConsciousnessStream() {
  const [thoughts, setThoughts] = useState([])
  const ws = useWebSocket()

  useEffect(() => {
    // 订阅意识流更新
    ws.subscribe('consciousness_update', (data) => {
      setThoughts(prev => [data, ...prev])
    })
  }, [])

  return (
    <div className="consciousness-stream">
      {thoughts.map(thought => (
        <ThoughtCard key={thought.id} thought={thought} />
      ))}
    </div>
  )
}
```

**后端 (consciousness.py)**
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/stream")
async def get_consciousness_stream(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    thoughts = db.query(ConsciousnessRecord)\
        .order_by(ConsciousnessRecord.timestamp.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()
    return {"thoughts": [t.to_dict() for t in thoughts]}
```

### 5.2 项目看板

**前端 (ProjectBoard.tsx)**
```typescript
export function ProjectBoard() {
  const [projects, setProjects] = useState({
    idea: [],
    planning: [],
    active: [],
    completed: []
  })

  const ws = useWebSocket()

  useEffect(() => {
    // 加载初始数据
    fetch('/api/projects').then(res => res.json()).then(setProjects)
    
    // 订阅更新
    ws.subscribe('project_update', (data) => {
      // 更新对应项目
      updateProject(data)
    })
  }, [])

  return (
    <div className="kanban-board">
      <Column title="IDEA" projects={projects.idea} />
      <Column title="PLANNING" projects={projects.planning} />
      <Column title="ACTIVE" projects={projects.active} />
      <Column title="COMPLETED" projects={projects.completed} />
    </div>
  )
}
```

### 5.3 对话界面

**前端 (Chat.tsx)**
```typescript
export function Chat() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')

  const sendMessage = async () => {
    const response = await fetch('/api/chat/message', {
      method: 'POST',
      body: JSON.stringify({ content: input })
    })
    
    const result = await response.json()
    
    // 显示价值评估
    setMessages(prev => [...prev, {
      role: 'user',
      content: input
    }, {
      role: 'assistant',
      content: result.response,
      value_score: result.value_score,
      thinking_process: result.thinking_process
    }])
  }

  return (
    <div className="chat-interface">
      <MessageList messages={messages} />
      <Input value={input} onChange={setInput} onSend={sendMessage} />
    </div>
  )
}
```


## 六、UI/UX 设计原则

### 6.1 设计理念

1. **透明化思考过程** - 让用户看到智能体的"思考"
2. **实时反馈** - 所有行动立即可见
3. **价值可视化** - 用图表展示决策依据
4. **简洁高效** - 避免信息过载
5. **沉浸式体验** - 让用户感受到智能体的"生命力"

### 6.2 视觉风格

```yaml
配色方案:
  主色: 深蓝 (#1e293b)
  强调色: 青色 (#06b6d4)
  成功: 绿色 (#10b981)
  警告: 黄色 (#f59e0b)
  错误: 红色 (#ef4444)
  背景: 深灰 (#0f172a)

字体:
  主字体: Inter
  代码字体: JetBrains Mono

动画:
  意识流: 淡入淡出
  项目卡片: 拖拽动画
  价值雷达图: 动态绘制
```

## 七、部署方案

### 7.1 开发环境

```bash
# 后端
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 前端
cd frontend
npm install
npm run dev
```

### 7.2 生产部署

```yaml
方案1: Docker 容器化
  - 前端: Nginx 静态服务
  - 后端: Gunicorn + Uvicorn workers
  - 数据库: SQLite 持久化卷

方案2: 单机部署
  - 前端构建: npm run build
  - 后端: systemd 服务
  - 反向代理: Nginx

方案3: 云部署
  - 前端: Vercel/Netlify
  - 后端: Railway/Render
  - 数据库: 云存储
```

### 7.3 Docker 配置

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY backend/ ./backend/
COPY frontend/dist/ ./frontend/dist/

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  autonomous-agent:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    restart: unless-stopped
```

## 八、实现路线图

### Phase 1: 基础框架 (Week 1-2)

**后端**
- [ ] FastAPI 应用骨架
- [ ] SQLite 数据库设计
- [ ] smolagents CodeAgent 集成
- [ ] 基础 API 端点
- [ ] WebSocket 基础设施

**前端**
- [ ] React + Vite 项目搭建
- [ ] 基础路由和布局
- [ ] API 服务封装
- [ ] WebSocket Hook

**验收**
- 前后端可以通信
- 可以发送消息并收到响应

### Phase 2: 核心功能 (Week 3-4)

**后端**
- [ ] 自主运行引擎
- [ ] 价值评估系统
- [ ] 意识流记录
- [ ] 项目管理器
- [ ] 所有自定义工具

**前端**
- [ ] 意识流实时显示
- [ ] 项目看板
- [ ] 对话界面
- [ ] 基础仪表盘

**验收**
- 智能体可以持续运行
- 前端实时显示智能体状态
- 可以通过对话交互

### Phase 3: 高级功能 (Week 5-6)

**后端**
- [ ] 目标管理系统
- [ ] 创造成果画廊
- [ ] 长期记忆系统
- [ ] 主动探索机制

**前端**
- [ ] 目标树可视化
- [ ] 创造画廊
- [ ] 价值分析仪表盘
- [ ] 高级搜索和过滤

**验收**
- 完整的自主能力
- 丰富的可视化界面

### Phase 4: 优化与完善 (Week 7-8)

**后端**
- [ ] 性能优化
- [ ] 错误处理
- [ ] 日志系统
- [ ] 健康检查

**前端**
- [ ] UI/UX 优化
- [ ] 响应式设计
- [ ] 动画效果
- [ ] 暗色模式

**验收**
- 生产级稳定性
- 优秀的用户体验

## 九、技术栈总结

```yaml
前端:
  框架: React 18 + TypeScript
  构建: Vite
  状态: Zustand
  UI: shadcn/ui + Tailwind CSS
  图表: Recharts
  动画: Framer Motion
  WebSocket: 原生 WebSocket API

后端:
  框架: FastAPI
  Agent: smolagents 1.24.0
  LLM: Claude 3.5 Sonnet (via LiteLLM)
  数据库: SQLite + SQLAlchemy
  异步: asyncio
  WebSocket: FastAPI WebSocket

部署:
  容器: Docker + Docker Compose
  反向代理: Nginx
  进程管理: systemd
```

## 十、关键优势

### 10.1 vs 纯后端方案

| 特性 | 纯后端 | 全栈方案 |
|------|--------|----------|
| 可视化 | 无 | 实时可视化 |
| 交互性 | CLI | Web UI |
| 监控 | 日志 | 实时仪表盘 |
| 用户体验 | 差 | 优秀 |
| 调试 | 困难 | 直观 |

### 10.2 核心创新

1. **意识流可视化** - 首次将智能体的"思考"实时展示
2. **价值驱动界面** - 所有决策都有价值评分
3. **项目化管理** - 长期目标的可视化追踪
4. **实时交互** - WebSocket 实现零延迟体验
5. **自主性展示** - 用户可以看到智能体的主动行为

## 十一、下一步行动

1. **确认方案** ✓
2. **搭建项目结构** - 创建目录和基础文件
3. **实现 MVP** - Phase 1 基础框架
4. **迭代开发** - 逐步完善功能
5. **测试部署** - 验证生产环境

---

**方案版本**: v2.0 (全栈版)
**完成时间**: 2026-03-09
**状态**: 待确认并开始实施
