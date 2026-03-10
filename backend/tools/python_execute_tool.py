"""Python代码执行工具"""
from smolagents import Tool
import subprocess
import tempfile
import os

class PythonExecuteTool(Tool):
    name = "python_execute"
    description = "执行Python代码并返回结果"
    inputs = {
        "code": {"type": "string", "description": "要执行的Python代码"}
    }
    output_type = "string"

    def forward(self, code: str) -> str:
        """执行Python代码"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(code)
                temp_file = f.name

            result = subprocess.run(
                ['python', temp_file],
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8'
            )

            os.unlink(temp_file)

            output = result.stdout if result.stdout else result.stderr
            return output if output else "代码执行完成，无输出"
        except Exception as e:
            return f"执行失败: {str(e)}"
