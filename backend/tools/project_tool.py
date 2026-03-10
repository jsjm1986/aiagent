"""Agent 工具 - 项目管理"""
from smolagents import Tool

class ProjectManagementTool(Tool):
    name = "manage_project"
    description = "创建或更新项目"
    inputs = {
        "action": {"type": "string", "description": "操作: create/update"},
        "name": {"type": "string", "description": "项目名称"},
        "description": {"type": "string", "description": "项目描述", "nullable": True}
    }
    output_type = "string"

    def __init__(self, project_mgr):
        super().__init__()
        self.project_mgr = project_mgr

    def forward(self, action: str, name: str, description: str = ""):
        if action == "create":
            project = self.project_mgr.create_project(name, description)
            return f"项目已创建: {project.id}"
        return "操作完成"
