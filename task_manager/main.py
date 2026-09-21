from pydantic import ValidationError
from models import Task
from storage import load_tasks, save_tasks


tasks: list[Task] = load_tasks()



def add_task(title: str) -> Task:
    next_id = max((task.id for task in tasks), default=0) + 1
    task = Task(id=next_id, title=title)
    tasks.append(task)
    save_tasks(tasks)
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
            save_tasks(tasks)
            print(f"任务“{task.title}”已完成。")
            return

    print("没有找到这个任务。")

def delete_task(task_id: int) -> None:
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"任务“{task.title}已删除。”")
            return
    print("没有找到这个任务。")

def search_tasks(keyword: str) -> None:
    keyword = keyword.strip().lower()

    found_tasks = [
        task for task in tasks
        if keyword in task.title.lower()
    ]

    if not found_tasks:
        print("没有找到匹配的任务。")
        return

    for task in found_tasks:
        status = "已完成" if task.completed else "未完成"
        print(f"{task.id}. {task.title} - {status}")

def show_statistics() -> None:
    total = len(tasks)

    completed_count = sum(
        1 for task in tasks
        if task.completed
    )

    pending_count = total - completed_count

    print(f"任务总数：{total}")
    print(f"已完成：{completed_count}")
    print(f"未完成：{pending_count}")

def main() -> None:
    while True:
        print("\n--- 任务管理器 ---")
        print("1. 添加任务")
        print("2. 查看任务")
        print("3. 完成任务")
        print("4. 删除任务")
        print("5. 搜索任务")
        print("6. 查看统计")
        print("7. 退出")

        choice = input("请选择功能：")

        if choice == "1":
            title = input("请输入任务标题：")

            try:
                task = add_task(title)
                print(f"已添加任务：{task.title}")

            except ValidationError:
                print("任务标题不能为空。")

        elif choice == "2":
            show_tasks()

        elif choice == "3":
            try:
                task_id = int(input("请输入要完成的任务编号："))
                complete_task(task_id)

            except ValueError:
                print("任务编号必须是整数。")

        elif choice == "4":
            try:
                task_id = int(input("请输入要删除的任务编号："))
                delete_task(task_id)

            except ValueError:
                print("任务编号必须是整数。")

        elif choice == "5":
            keyword = input("请输入关键词：")
            search_tasks(keyword)

        elif choice == "6":
            show_statistics()

        elif choice == "7":
            print("再见! ")
            break

        else:
            print("无效选择，请输入 1 到 7。")


if __name__ == "__main__":
    main()