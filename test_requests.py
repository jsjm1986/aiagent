"""使用requests直接调用API"""
import requests
import json
from backend.config import Config

url = f"{Config.API_BASE}/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {Config.API_KEY}"
}

print("测试1: 中文问候")
data = {
    "model": Config.MODEL_NAME,
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 50
}

try:
    response = requests.post(url, headers=headers, json=data, timeout=30)
    result = response.json()
    if "choices" in result:
        print(f"成功: {result['choices'][0]['message']['content']}")
    else:
        print(f"失败: {result}")
except Exception as e:
    print(f"失败: {e}")

print("\n测试2: 评估候选")
data = {
    "model": Config.MODEL_NAME,
    "messages": [{"role": "user", "content": """请评估以下候选行动的价值(0-1分):
1. 执行项目任务
2. 优化现有项目
3. 探索新机会

返回格式: 候选编号,value,impact,long_term,feasibility,risk,compound,goal_alignment
每行一个候选,用逗号分隔数字。"""}],
    "max_tokens": 200
}

try:
    response = requests.post(url, headers=headers, json=data, timeout=30)
    result = response.json()
    if "choices" in result:
        print(f"成功: {result['choices'][0]['message']['content']}")
    else:
        print(f"失败: {result}")
except Exception as e:
    print(f"失败: {e}")
