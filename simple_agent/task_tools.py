import json
from pathlib import Path


TASK_FILE = (
    Path(__file__).parent.parent
    / "task_manager"
    / "tasks.json"
)

PENDING_DELETE_ID = None

def list_tasks(**kwargs) -> str:
    if not TASK_FILE.exists():
        return "任务数据文件不存在。"

    with open(TASK_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not data:
        return "当前没有任务。"

    task_lines = []

    for task in data:
        status = "已完成" if task["completed"] else "未完成"

        task_lines.append(
            f'{task["id"]}. {task["title"]} - {status}'
        )

    return "\n".join(task_lines)

def add_task(title: str) -> str:
    title = title.strip()

    if not title:
        return "添加失败：任务标题不能为空。"

    if TASK_FILE.exists():
        with open(TASK_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        data = []

    next_id = max(
        (task["id"] for task in data),
        default=0
    ) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "completed": False
    }

    data.append(new_task)

    with open(TASK_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

    return f"已添加任务：{next_id}. {title}"

def complete_task(task_id: int) -> str:
    if not TASK_FILE.exists():
        return "完成失败：任务数据文件不存在。"

    with open(TASK_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    for task in data:
        if task["id"] == task_id:
            if task["completed"]:
                return f'任务“{task["title"]}”已经完成了。'

            task["completed"] = True

            with open(TASK_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

            return f'任务“{task["title"]}”已完成。'

    return f"完成失败：没有找到编号为{task_id}的任务。"

def request_delete_task(task_id: int) -> str:
    global PENDING_DELETE_ID

    if not TASK_FILE.exists():
        return "删除失败：任务数据文件不存在。"

    with open(TASK_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    for task in data:
        if task["id"] == task_id:
            PENDING_DELETE_ID = task_id

            return (
                f'即将删除任务{task_id}：'
                f'“{task["title"]}”。'
                f'请输入“确认删除”继续。'
            )

    return f"删除失败：没有找到编号为{task_id}的任务。"


def confirm_delete_task(**kwargs) -> str:
    global PENDING_DELETE_ID

    if PENDING_DELETE_ID is None:
        return "当前没有等待确认删除的任务。"

    with open(TASK_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    for task in data:
        if task["id"] == PENDING_DELETE_ID:
            data.remove(task)

            with open(TASK_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

            deleted_id = PENDING_DELETE_ID
            deleted_title = task["title"]
            PENDING_DELETE_ID = None

            return (
                f'任务{deleted_id}：'
                f'“{deleted_title}”已删除。'
            )

    PENDING_DELETE_ID = None

    return "删除失败：待删除的任务已经不存在。"
