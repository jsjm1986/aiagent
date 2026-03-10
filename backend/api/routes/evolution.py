"""API 路由 - 演化系统"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/timeline")
async def get_timeline(engine, days: int = 7):
    """获取演化时间线"""
    return engine.evolution.get_timeline(days)

@router.get("/insights")
async def get_insights(engine):
    """获取学习洞察"""
    return engine.evolution.get_insights()
