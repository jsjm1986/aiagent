"""FastAPI 主应用"""
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
import json
from datetime import datetime
from core.engine import AutonomousEngine

# 全局引擎实例
engine = None
engine_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期"""
    global engine, engine_task

    # 写入调试日志到文件
    with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}] LIFESPAN: 开始启动\n")
        f.flush()

    try:
        engine = AutonomousEngine()
        with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] LIFESPAN: engine创建完成\n")
            f.flush()

        engine_task = asyncio.create_task(engine.run_forever())
        with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] LIFESPAN: engine_task已创建\n")
            f.flush()
    except Exception as e:
        with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] LIFESPAN ERROR: {str(e)}\n")
            f.flush()
        raise

    yield

    # 关闭
    engine.stop()
    engine_task.cancel()
    with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] LIFESPAN: 引擎已停止\n")
        f.flush()

app = FastAPI(title="Autonomous Agent", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "running", "message": "Autonomous Agent API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/drives/status")
async def get_drives():
    """获取驱动力状态"""
    return engine.drive_tracker.get_status()

@app.get("/api/projects")
async def get_projects():
    """获取项目"""
    data = engine.project_mgr.get_active_projects()
    return JSONResponse(content=data, media_type="application/json; charset=utf-8")

@app.get("/api/projects/{project_id}")
async def get_project_detail(project_id: str):
    """获取项目详情"""
    if project_id in engine.project_mgr.projects:
        data = engine.project_mgr.projects[project_id]
        return JSONResponse(content=data, media_type="application/json; charset=utf-8")
    return JSONResponse(content={"error": "项目不存在"}, status_code=404)

@app.get("/api/consciousness/stream")
async def get_consciousness(limit: int = 50):
    """获取意识流"""
    data = engine.consciousness.get_recent(limit)
    return JSONResponse(content=data, media_type="application/json; charset=utf-8")

@app.get("/api/creations")
async def get_creations():
    """获取创造"""
    return engine.creations.get_all()

@app.get("/api/assistance/pending")
async def get_assistance():
    """获取协助请求"""
    return engine.assistance_mgr.get_pending()

@app.get("/api/evolution/timeline")
async def get_evolution_timeline(days: int = 7):
    """获取演化时间线"""
    return engine.evolution.get_timeline(days)

@app.get("/api/evolution/insights")
async def get_evolution_insights():
    """获取学习洞察"""
    return engine.evolution.get_insights()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 连接"""
    await engine.event_bus.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        engine.event_bus.disconnect(websocket)
