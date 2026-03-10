"""测试 LLM 基本功能"""
from smolagents import CodeAgent, LiteLLMModel
from backend.config import Config

# 创建模型
model = LiteLLMModel(
    model_id=Config.MODEL_NAME,
    api_key=Config.API_KEY,
    api_base=Config.API_BASE
)

# 创建 agent（不带工具）
agent = CodeAgent(tools=[], model=model, max_steps=1)

# 测试简单对话
print("测试1: 简单问候")
try:
    result = agent.run("你好")
    print(f"成功: {result}")
except Exception as e:
    print(f"失败: {e}")

print("\n测试2: 简单计算")
try:
    result = agent.run("1+1等于几？")
    print(f"成功: {result}")
except Exception as e:
    print(f"失败: {e}")
