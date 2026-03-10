"""网络搜索工具"""
from smolagents import Tool
import requests

class WebSearchTool(Tool):
    name = "web_search"
    description = "搜索互联网获取信息"
    inputs = {
        "query": {"type": "string", "description": "搜索关键词"}
    }
    output_type = "string"

    def forward(self, query: str) -> str:
        """执行网络搜索"""
        try:
            url = f"https://api.duckduckgo.com/?q={query}&format=json"
            response = requests.get(url, timeout=10)
            data = response.json()

            result = f"搜索: {query}\n\n"
            if data.get('AbstractText'):
                result += f"摘要: {data['AbstractText']}\n"
            if data.get('AbstractURL'):
                result += f"来源: {data['AbstractURL']}\n"

            return result if len(result) > 20 else "未找到相关信息"
        except Exception as e:
            return f"搜索失败: {str(e)}"
