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


def get_current_time() -> str:
    current_time = datetime.now().astimezone()

    return current_time.strftime(
        "%Y年%m月%d日 %H:%M:%S"
    )


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
                    ]
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


# 统一执行模型选择的工具
def execute_tool(tool_name: str, arguments: dict) -> str:
    if tool_name == "get_current_time":
        result = get_current_time()

    elif tool_name == "calculate":
        result = calculate(**arguments)

    else:
        result = f"未知工具：{tool_name}"

    return str(result)


user_question = input("请输入问题：")


# 保存完整对话记录
conversation_items = [
    {
        "role": "user",
        "content": user_question
    }
]


# 最多允许模型思考和调用工具5轮
for step in range(1, 6):
    print(f"\n--- Agent第{step}轮 ---")

    response = client.responses.create(
        model=MODEL,
        instructions=(
            "你是一个中文助手。"
            "查询当前日期或时间时，调用 get_current_time。"
            "进行数学计算时，调用 calculate。"
            "如果已经获得足够信息，请直接回答用户。"
        ),
        input=conversation_items,
        tools=tools
    )

    # 把模型本轮输出加入对话记录
    for item in response.output:
        conversation_items.append(
            item.model_dump(exclude_none=True)
        )

    # 找出本轮的全部工具调用
    tool_calls = [
        item
        for item in response.output
        if item.type == "function_call"
    ]

    # 没有工具调用，说明模型已经给出最终答案
    if not tool_calls:
        print("Agent 最终回答：", response.output_text)
        break

    # 逐个执行模型要求调用的工具
    for tool_call in tool_calls:
        print("模型选择的工具：", tool_call.name)

        try:
            arguments = json.loads(tool_call.arguments)

            print("模型提供的参数：", arguments)

            tool_result = execute_tool(
                tool_call.name,
                arguments
            )

        except (
            ValueError,
            TypeError,
            json.JSONDecodeError
        ) as error:
            tool_result = f"工具执行失败：{error}"

        print("Python 工具返回：", tool_result)

        # 把每个工具的执行结果加入对话记录
        conversation_items.append(
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": tool_result
            }
        )

else:
    print("Agent运行超过5轮，程序已停止。")