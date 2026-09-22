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


conversation_items = []

print("对话 Agent 已启动，输入 exit 可以退出。")


while True:
    user_question = input("\n你：").strip()

    if user_question.lower() in {"exit", "quit", "退出"}:
        print("Agent：再见！")
        break

    if not user_question:
        print("请输入问题。")
        continue

    # 保存用户的新问题
    conversation_items.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # 每个用户问题最多运行5轮
    for step in range(1, 6):
        print(f"  [Agent第{step}轮]")

        response = client.responses.create(
            model=MODEL,
            instructions=(
                "你是一个会使用工具并具有对话记忆的中文助手。"
                "查询当前日期或时间时，调用 get_current_time。"
                "进行数学计算时，调用 calculate。"
                "你可以参考前面的对话内容理解代词和省略的信息。"
                "获得足够信息后，直接回答用户。"
            ),
            input=conversation_items,
            tools=tools
        )

        # 保存模型本轮的全部输出
        for item in response.output:
            conversation_items.append(
                item.model_dump(exclude_none=True)
            )

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        # 没有工具调用，说明已经产生最终答案
        if not tool_calls:
            print("Agent：", response.output_text)
            break

        # 执行模型要求的全部工具
        for tool_call in tool_calls:
            print("  选择工具：", tool_call.name)

            try:
                arguments = json.loads(tool_call.arguments)

                print("  工具参数：", arguments)

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

            print("  工具结果：", tool_result)

            conversation_items.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": tool_result
                }
            )

    else:
        print("Agent：本次任务超过5轮，已经停止。")