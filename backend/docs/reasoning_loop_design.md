# 推理循环架构设计

## 1. 核心问题
- `agent.run()` 被API阻止,无法使用工具
- 需要自己实现推理循环,直接调用API

## 2. 数据流

```
用户提示 → API调用 → 解析响应 → 工具调用?
                                    ↓ 是
                            执行工具 → 收集结果 → 继续循环(最多10步)
                                    ↓ 否
                                返回最终结果
```

## 3. 核心逻辑伪代码

```python
def reasoning_loop(prompt, max_steps=10):
    messages = [{"role": "user", "content": prompt}]

    for step in range(max_steps):
        # 调用API
        response = call_api(messages)
        content = response['choices'][0]['message']['content']

        # 解析工具调用
        tool_calls = parse_tool_calls(content)

        if not tool_calls:
            return content  # 完成

        # 执行工具
        tool_results = []
        for call in tool_calls:
            result = execute_tool(call['name'], call['args'])
            tool_results.append(result)

        # 添加到消息历史
        messages.append({"role": "assistant", "content": content})
        messages.append({"role": "user", "content": format_tool_results(tool_results)})

    return "达到最大步数"
```

## 4. API调用格式

```python
import requests

response = requests.post(
    f"{API_BASE}/chat/completions",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    },
    json={
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": 2000,
        "temperature": 0.7
    },
    timeout=60
)
```

## 5. 工具调用解析

### 方法1: 结构化输出(推荐)
要求模型返回JSON格式:
```json
{
  "thought": "我需要执行Python代码",
  "tool": "python_execute",
  "args": {"code": "print('hello')"}
}
```

### 方法2: 文本解析
解析特定标记:
```
<tool>python_execute</tool>
<args>{"code": "print('hello')"}</args>
```

正则表达式:
```python
import re
import json

def parse_tool_calls(content):
    pattern = r'<tool>(.*?)</tool>\s*<args>(.*?)</args>'
    matches = re.findall(pattern, content, re.DOTALL)

    calls = []
    for tool_name, args_str in matches:
        calls.append({
            'name': tool_name.strip(),
            'args': json.loads(args_str.strip())
        })
    return calls
```

## 6. 工具执行映射

```python
TOOLS = {
    'python_execute': PythonExecuteTool(),
    'file_operation': FileOperationTool(),
    'web_search': WebSearchTool(),
    'creation_gallery': CreationGalleryTool(),
    'consciousness_record': ConsciousnessRecordTool()
}

def execute_tool(name, args):
    tool = TOOLS.get(name)
    if not tool:
        return f"工具不存在: {name}"

    try:
        return tool.forward(**args)
    except Exception as e:
        return f"执行失败: {str(e)}"
```

## 7. 系统提示词

```python
SYSTEM_PROMPT = """你是一个自主agent,可以使用以下工具:

1. python_execute(code: str) - 执行Python代码
2. file_operation(action: str, path: str, content: str) - 文件操作
3. web_search(query: str) - 网络搜索
4. creation_gallery(title: str, content: str, type: str) - 保存创作
5. consciousness_record(type: str, data: dict) - 记录思考

使用工具格式:
<tool>工具名</tool>
<args>{"参数名": "参数值"}</args>

每次只调用一个工具。如果任务完成,直接返回结果。"""
```

## 8. 完整实现框架

```python
class ReasoningLoop:
    def __init__(self, api_base, api_key, model_name):
        self.api_base = api_base
        self.api_key = api_key
        self.model_name = model_name
        self.tools = self._init_tools()

    def run(self, prompt, max_steps=10):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]

        for step in range(max_steps):
            response = self._call_api(messages)
            content = response['choices'][0]['message']['content']

            tool_calls = self._parse_tools(content)

            if not tool_calls:
                return content

            results = []
            for call in tool_calls:
                result = self._execute_tool(call['name'], call['args'])
                results.append(f"{call['name']}: {result}")

            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user", "content": "\n".join(results)})

        return "达到最大步数限制"
```

## 9. 关键优化点

1. **错误处理**: 每个工具调用都要try-catch
2. **超时控制**: API调用设置timeout
3. **消息压缩**: 超过token限制时压缩历史
4. **并发执行**: 多个独立工具调用可并行
5. **日志记录**: 记录每步的输入输出

## 10. 测试用例

```python
# 测试1: 简单代码执行
prompt = "计算1+1并告诉我结果"
# 预期: 调用python_execute → 返回2

# 测试2: 多步推理
prompt = "搜索Python最新版本,然后写代码打印版本号"
# 预期: web_search → python_execute → 返回结果

# 测试3: 文件操作
prompt = "创建一个hello.txt文件,内容是'Hello World'"
# 预期: file_operation(write) → 确认成功
```
