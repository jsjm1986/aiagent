"""API 路由 - 人类协助"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/pending")
async def get_pending(engine):
    """获取待处理请求"""
    return engine.assistance_mgr.get_pending()

@router.post("/{request_id}/respond")
async def respond(request_id: str, response: dict, engine):
    """提交响应"""
    engine.assistance_mgr.submit_response(request_id, response)
    return {"status": "ok"}
