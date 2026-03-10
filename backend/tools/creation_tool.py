"""Agent 工具 - 创造保存"""
from smolagents import Tool

class CreationGalleryTool(Tool):
    name = "save_creation"
    description = "保存创造成果到画廊"
    inputs = {
        "title": {"type": "string", "description": "标题"},
        "content": {"type": "string", "description": "内容"},
        "creation_type": {"type": "string", "description": "类型", "nullable": True}
    }
    output_type = "string"

    def __init__(self, gallery):
        super().__init__()
        self.gallery = gallery

    def forward(self, title: str, content: str, creation_type: str = "code"):
        creation_id = self.gallery.save_creation(title, content, creation_type)
        return f"创造已保存: {creation_id}"
