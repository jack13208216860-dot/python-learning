from datetime import datetime

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
    "calculate": calculate
}

TOOL_DEFINITIONS = [
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

    if tool_function is None:
        return f"未知工具：{tool_name}"

    result = tool_function(**arguments)

    return str(result)