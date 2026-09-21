import json
from pathlib import Path

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int
    title: str = Field(min_length=1)
    completed: bool = False


DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks() -> list[Task]:
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [Task.model_validate(item) for item in data]


tasks: list[Task] = load_tasks()


def save_tasks() -> None:
    data = [task.model_dump() for task in tasks]

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def add_task(title: str) -> Task:
    task = Task(id=len(tasks) + 1, title=title)
    tasks.append(task)
    save_tasks()
    return task


def show_tasks() -> None:
    if not tasks:
        print("当前没有任务。")
        return

    for task in tasks:
        status = "已完成" if task.completed else "未完成"
        print(f"{task.id}. {task.title} - {status}")


def complete_task(task_id: int) -> None:
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            save_tasks()
            print(f"任务“{task.title}”已完成。")
            return

    print("没有找到这个任务。")


if not tasks:
    add_task("完成 Python 学习")
    add_task("学习 Agent 开发")

show_tasks()