from pydantic import BaseModel, Field, ValidationError


class Task(BaseModel):
    title: str
    completed: bool = False
    priority: int = Field(ge=1, le=5)


json_text = """
{
    "title": "学习 Pydantic",
    "completed": false,
    "priority": 3
}
"""

try:
    # JSON 字符串 → Pydantic 对象
    task = Task.model_validate_json(json_text)

    print(task)
    print("任务标题：", task.title)

    # Pydantic 对象 → JSON 字符串
    output_json = task.model_dump_json(indent=2)

    print("输出 JSON：")
    print(output_json)

except ValidationError as error:
    print("数据验证失败：", error)