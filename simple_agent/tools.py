from datetime import datetime
from pydantic import ValidationError
from .knowledge_tools import search_knowledge

from .tool_models import (
    AddTaskArguments,
    CalculateArguments,
    EmptyArguments,
    KnowledgeSearchArguments,
    TaskIdArguments
)
from .task_tools import (add_task, 
                        list_tasks, 
                        complete_task,
                        confirm_delete_task,
                        request_delete_task
)

def get_current_time(**kwargs) -> str:
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


TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "list_tasks": list_tasks,
    "add_task": add_task,
    "complete_task": complete_task,
    "request_delete_task": request_delete_task,
    "confirm_delete_task": confirm_delete_task,
    "search_knowledge": search_knowledge

}

TOOL_ARGUMENT_MODELS = {
    "get_current_time": EmptyArguments,
    "calculate": CalculateArguments,
    "list_tasks": EmptyArguments,
    "add_task": AddTaskArguments,
    "complete_task": TaskIdArguments,
    "request_delete_task": TaskIdArguments,
    "confirm_delete_task": EmptyArguments,
    "search_knowledge": KnowledgeSearchArguments
}

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "list_tasks",
        "description": "查看任务管理器的任务及完成情况",
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
        "name": "add_task",
        "description": "向任务管理器添加一个新任务",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "需要添加的任务标题"
                }
            },
            "required": [
                "title"
            ],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "complete_task",
        "description": "根据任务编号把一个任务标记为已完成",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "需要完成的任务编号"
                }
            },
            "required": [
                "task_id"
            ],
            "additionalProperties": False
        },
        "strict": True
    },
        {
        "type": "function",
        "name": "request_delete_task",
        "description": "请求删除指定编号的任务，但不会立即删除，需要用户再次确认",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "准备删除的任务编号"
                }
            },
            "required": [
                "task_id"
            ],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "confirm_delete_task",
        "description": "用户明确说确认删除后，删除当前等待确认的任务",
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
        "name": "search_knowledge",
        "description": (
            "在本地Python和Agent知识库中搜索资料，"
            "返回相关文本、来源文件、文本块编号和相似度。"
            "回答知识库问题前应调用此工具。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "用于搜索知识库的简短关键词，例如函数、异常、Agent循环"
                }
            },
            "required": [
                "keyword"
            ],
            "additionalProperties": False
        },
        "strict": True
    },
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


def execute_tool(tool_name: str, arguments: dict) -> str:
    tool_function = TOOL_FUNCTIONS.get(tool_name)
    argument_model = TOOL_ARGUMENT_MODELS.get(tool_name)

    if tool_function is None:
        return f"未知工具：{tool_name}"

    if argument_model is None:
        return f"工具缺少参数模型：{tool_name}"

    try:
        validated_arguments = argument_model.model_validate(
            arguments
        )

    except ValidationError as error:
        first_error = error.errors()[0]
        field_name = ".".join(
            str(part)
            for part in first_error["loc"]
        )
        error_message = first_error["msg"]

        return (
            f"工具参数验证失败："
            f"{field_name} {error_message}"
        )

    result = tool_function(
        **validated_arguments.model_dump()
    )

    return str(result)