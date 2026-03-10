"""文件操作工具"""
from smolagents import Tool
import os

class FileOperationTool(Tool):
    name = "file_operation"
    description = "读取或写入文件"
    inputs = {
        "operation": {"type": "string", "description": "操作类型和参数，格式: 'read:文件路径' 或 'write:文件路径:内容'"}
    }
    output_type = "string"

    def forward(self, operation: str) -> str:
        """执行文件操作"""
        try:
            parts = operation.split(':', 2)
            op_type = parts[0]

            if op_type == 'read':
                file_path = parts[1]
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()

            elif op_type == 'write':
                file_path = parts[1]
                content = parts[2]
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"文件已写入: {file_path}"

            return "无效操作"
        except Exception as e:
            return f"文件操作失败: {str(e)}"
