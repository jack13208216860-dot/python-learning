import json
from pathlib import Path
from models import Task

DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks() -> list[Task]:
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [Task.model_validate(item) for item in data]




def save_tasks(tasks: list[Task]) -> None:
    data = [task.model_dump() for task in tasks]

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)