"""API 路由 - 项目"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_projects(engine):
    """获取所有项目"""
    return engine.project_mgr.get_active_projects()

@router.post("/")
async def create_project(name: str, description: str, engine):
    """创建项目"""
    project = engine.project_mgr.create_project(name, description)
    return project.to_dict()
