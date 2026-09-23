import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from .tools import TOOL_DEFINITIONS, execute_tool


load_dotenv(override=True)


class SimpleAgent:
    def __init__(
    self,
    client=None,
    conversation_items=None
    ):
        if client is None:
            api_key = os.getenv("DEEPSEEK_API_KEY")

            if not api_key:
                raise RuntimeError(
                    "没有读取到DEEPSEEK_API_KEY，请检查.env文件"
                )

            client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )

        self.client = client
        self.model = "deepseek-flash"
        if conversation_items is None:
              conversation_items = []

        self.conversation_items = conversation_items

    def ask(self, user_question: str) -> str:
        self.conversation_items.append(
            {
                "role": "user",
                "content": user_question
            }
        )

        for step in range(1, 6):
            print(f"  [Agent第{step}轮]")

            response = self.client.responses.create(
                model=self.model,
                instructions=(
                    "你是一个会使用工具并具有对话记忆的中文助手。"
                    "查询日期或时间时，调用 get_current_time。"
                    "进行数学计算时，调用 calculate。"
                    "查看任务时, 调用list_tasks。"
                    "只有当用户明确要求添加任务时，才调用 add_task。"
                    "只要用户明确要求完成某个编号的任务，"
                    "无论该编号是否存在，都必须调用 complete_task,"
                    "必须以工具返回结果为准，不能根据对话记录自行判断。"
                    "如果用户没有提供任务编号，先查看任务，不要猜测编号。"
                    "用户要求删除任务时，只能调用 request_delete_task。"
                    "不能在同一轮调用 confirm_delete_task。"
                    "只有用户在后续消息中明确输入确认删除时，"
                    "才能调用 confirm_delete_task。"
                    "获得足够信息后，直接回答用户。"
                ),
                input=self.conversation_items,
                tools=TOOL_DEFINITIONS
            )

            for item in response.output:
                self.conversation_items.append(
                    item.model_dump(exclude_none=True)
                )

            tool_calls = [
                item
                for item in response.output
                if item.type == "function_call"
            ]

            if not tool_calls:
                return response.output_text

            for tool_call in tool_calls:
                print("  选择工具：", tool_call.name)

                try:
                    arguments = json.loads(
                        tool_call.arguments
                    )

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

                self.conversation_items.append(
                    {
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": tool_result
                    }
                )

                if tool_call.name == "request_delete_task":
                    return tool_result

        return "本次任务超过5轮，已经停止。"