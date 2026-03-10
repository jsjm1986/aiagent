"""测试 litellm 直接调用"""
import litellm
from backend.config import Config

litellm.api_key = Config.API_KEY
litellm.api_base = Config.API_BASE

print("测试1: 直接调用litellm")
try:
    response = litellm.completion(
        model=Config.MODEL_NAME,
        messages=[{"role": "user", "content": "你好"}],
        max_tokens=50
    )
    print(f"成功: {response.choices[0].message.content}")
except Exception as e:
    print(f"失败: {e}")

print("\n测试2: 英文问候")
try:
    response = litellm.completion(
        model=Config.MODEL_NAME,
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=50
    )
    print(f"成功: {response.choices[0].message.content}")
except Exception as e:
    print(f"失败: {e}")
