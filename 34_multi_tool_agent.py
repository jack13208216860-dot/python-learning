import json
import os
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(override=True)

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise RuntimeError("没有读取到 DEEPSEEK_API_KEY，请检查 .env 文件")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

MODEL = "deepseek-flash"


# 工具1：获取当前时间
def get_current_time() -> str:
    current_time = datetime.now().astimezone()

    return current_time.strftime(
        "%Y年%m月%d日 %H:%M:%S"
    )


# 工具2：计算两个数字
def calculate(
    number1: float,
    number2: float,
    operation: str
) -> float:
    if operation == "add":
        return number1 + number2

    if operation == "subtract":
        return number1 - number2

    if operation == "multiply":
        return number1 * number2

    if operation == "divide":
        if number2 == 0:
            raise ValueError("除数不能为0")

        return number1 / number2

    raise ValueError(f"不支持的运算：{operation}")


# 向模型描述它能够使用的工具
tools = [
    {
        "type": "function",
        "name": "get_current_time",
        "description": "获取计算机当前的本地日期和时间",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "calculate",
        "description": "计算两个数字的加法、减法、乘法或除法",
        "parameters": {
            "type": "object",
            "properties": {
                "number1": {
                    "type": "number",
                    "description": "第一个数字"
                },
                "number2": {
                    "type": "number",
                    "description": "第二个数字"
                },
                "operation": {
                    "type": "string",
                    "enum": [
                        "add",
                        "subtract",
                        "multiply",
                        "divide"
                    ],
                    "description": "需要执行的运算"
                }
            },
            "required": [
                "number1",
                "number2",
                "operation"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
]


user_question = input("请输入问题：")


# 第一次请求：让模型选择合适的工具
first_response = client.responses.create(
    model=MODEL,
    instructions=(
        "你是一个中文助手。"
        "查询当前日期或时间时，调用 get_current_time。"
        "进行数学计算时，调用 calculate。"
        "不能自己猜测工具能够提供的结果。"
    ),
    input=user_question,
    tools=tools
)


# 寻找模型返回的工具调用
tool_call = None

for item in first_response.output:
    if item.type == "function_call":
        tool_call = item
        break


# 模型可能认为问题不需要调用工具
if tool_call is None:
    print("模型没有调用工具。")
    print("Agent 回答：", first_response.output_text)
    raise SystemExit


print("模型选择的工具：", tool_call.name)


# 根据工具名称，调用不同的 Python 函数
try:
    if tool_call.name == "get_current_time":
        tool_result = get_current_time()

    elif tool_call.name == "calculate":
        arguments = json.loads(tool_call.arguments)

        print("模型提供的参数：", arguments)

        tool_result = calculate(**arguments)

    else:
        tool_result = f"未知工具：{tool_call.name}"

except (ValueError, TypeError, json.JSONDecodeError) as error:
    tool_result = f"工具执行失败：{error}"


print("Python 工具返回：", tool_result)


# 组合第一次请求、工具调用和工具结果
conversation_items = [
    {
        "role": "user",
        "content": user_question
    }
]

for item in first_response.output:
    conversation_items.append(
        item.model_dump(exclude_none=True)
    )

conversation_items.append(
    {
        "type": "function_call_output",
        "call_id": tool_call.call_id,
        "output": str(tool_result)
    }
)


# 第二次请求：让模型解释工具结果
final_response = client.responses.create(
    model=MODEL,
    instructions=(
        "请根据 Python 工具返回的真实结果，"
        "用简洁的中文回答用户。"
    ),
    input=conversation_items,
    tools=tools
)


print("Agent 最终回答：", final_response.output_text)