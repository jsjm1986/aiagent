"""Agent 工具 - 意识流记录"""
from smolagents import Tool

class ConsciousnessRecordTool(Tool):
    name = "record_thought"
    description = "记录思考过程到意识流"
    inputs = {
        "thought_type": {"type": "string", "description": "思考类型"},
        "content": {"type": "string", "description": "思考内容"}
    }
    output_type = "string"

    def __init__(self, consciousness):
        super().__init__()
        self.consciousness = consciousness

    def forward(self, thought_type: str, content: str):
        self.consciousness.record(thought_type, {"text": content})
        return "思考已记录"
