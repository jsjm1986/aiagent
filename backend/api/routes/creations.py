"""API 路由 - 创造画廊"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_creations(engine):
    """获取所有创造"""
    return engine.creations.get_all()
