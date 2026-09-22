import os
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI


# 读取 .env，并覆盖终端里可能存在的旧环境变量
load_dotenv(override=True)


api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise RuntimeError("没有读取到 DEEPSEEK_API_KEY，请检查 .env 文件")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

MODEL = "deepseek-flash"


# 这是 Agent 真正能够执行的 Python 工具
def get_current_time() -> str:
    current_time = datetime.now().astimezone()

    return current_time.strftime(
        "%Y年%m月%d日 %H:%M:%S"
    )


# 把 Python 工具的名称、作用和参数结构告诉模型
tools = [
    {
        "type": "function",
        "name": "get_current_time",
        "description": "获取运行程序的计算机当前本地日期和时间",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    }
]


# 第一次请求：让模型判断是否需要调用工具
first_response = client.responses.create(
    model=MODEL,
    instructions=(
        "你是一个中文助手。"
        "当用户询问当前日期或时间时，"
        "必须调用 get_current_time 工具，不能猜测。"
    ),
    input="现在几点了？",
    tools=tools
)


# 在模型输出中寻找工具调用
tool_call = None

for item in first_response.output:
    if (
        item.type == "function_call"
        and item.name == "get_current_time"
    ):
        tool_call = item
        break


# 如果模型没有选择工具，就结束程序并显示原因
if tool_call is None:
    print("模型没有调用 get_current_time 工具。")

    if first_response.output_text:
        print("模型直接回答：", first_response.output_text)

    raise SystemExit


# Python 真正执行工具
tool_result = get_current_time()

print("Python 工具返回：", tool_result)


# 创建第二次请求需要的完整上下文
conversation_items = [
    {
        "role": "user",
        "content": "现在几点了？"
    }
]


# 加入模型第一次返回的内容，其中包含 function_call
for item in first_response.output:
    conversation_items.append(
        item.model_dump(exclude_none=True)
    )


# 加入 Python 工具的执行结果
conversation_items.append(
    {
        "type": "function_call_output",
        "call_id": tool_call.call_id,
        "output": tool_result
    }
)


# 第二次请求：把完整上下文和工具结果交给模型
final_response = client.responses.create(
    model=MODEL,
    instructions="请根据工具返回的真实结果，用中文回答用户。",
    tools=tools,
    input=conversation_items
)


# 显示模型最终回答
print("Agent 最终回答：", final_response.output_text)