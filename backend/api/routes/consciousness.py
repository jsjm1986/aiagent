"""API 路由 - 意识流"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/stream")
async def get_stream(engine, limit: int = 50):
    """获取意识流"""
    return engine.consciousness.get_recent(limit)
