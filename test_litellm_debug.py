"""测试 litellm debug模式"""
import litellm
from backend.config import Config

# 启用debug
litellm.set_verbose = True

litellm.api_key = Config.API_KEY
litellm.api_base = Config.API_BASE

print("测试: 启用debug的litellm调用")
try:
    response = litellm.completion(
        model=Config.MODEL_NAME,
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=50
    )
    print(f"成功: {response.choices[0].message.content}")
except Exception as e:
    print(f"失败: {e}")
