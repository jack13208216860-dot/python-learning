import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise RuntimeError("没有读取到 DEEPSEEK_API_KEY, 请检查 .env 文件")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

MODEL = "deepseek-flash"

def calculate(number1: float, number2:float, operation: str) -> float:
    if operation == "add":
        return number1 + number2
    if operation == "subtract":
        return number1 - number2
    if operation == "multiply":
        return number1 * number2
    if operation == "divide":
        if number2 == 0:
            raise ValueError("除数不能为 0")
        return number1 / number2
    raise ValueError(f"不支持的运算：{operation}")

tools = [
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
                    "description": "要执行的运算"
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

user_question = input("请输入计算问题：")

first_response = client.responses.create(
    model=MODEL,
    instructions=(
        "你是一个中文计算助手。"
        "遇到数学计算时，必须调用calculate工具，不能自己猜答案。"
    ),
    input=user_question,
    tools=tools
)

tool_call = None

for item in first_response.output:
    if item.type == "function_call" and item.name == "calculate":
        tool_call = item
        break

if tool_call is None:
    print("模型没有调用calculate工具。")

    if first_response.output_text:
        print("模型回答：", first_response.output_text)

    raise SystemExit

arguments = json.loads(tool_call.arguments)

print("模型提供的参数：", arguments)


try:
    tool_result = calculate(**arguments)
except ValueError as error:
    tool_result = f"计算失败：{error}"

print("Python 工具返回：", tool_result)


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


# 第二次请求：让模型根据工具结果回答
final_response = client.responses.create(
    model=MODEL,
    instructions="请根据工具返回的结果，用中文回答用户。",
    tools=tools,
    input=conversation_items
)

print("Agent 最终回答：", final_response.output_text)