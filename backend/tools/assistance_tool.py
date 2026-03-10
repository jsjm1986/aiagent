"""Agent 工具 - 人类协助请求"""
from smolagents import Tool

class RequestHumanHelpTool(Tool):
    name = "request_human_help"
    description = "当遇到超出能力范围的问题时，请求人类提供资源或信息"
    inputs = {
        "request_type": {"type": "string", "description": "类型: missing_resource/need_information/capability_limit"},
        "title": {"type": "string", "description": "简短标题"},
        "description": {"type": "string", "description": "详细描述"}
    }
    output_type = "string"

    def __init__(self, assistance_mgr):
        super().__init__()
        self.assistance_mgr = assistance_mgr

    def forward(self, request_type: str, title: str, description: str):
        request_id = self.assistance_mgr.create_request(request_type, title, description)
        return f"协助请求已创建: {request_id}，你可以继续其他任务"
