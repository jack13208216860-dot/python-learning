import json

import pytest

from simple_agent import task_tools


@pytest.fixture
def temporary_task_file(tmp_path, monkeypatch):
    test_file = tmp_path / "tasks.json"

    test_file.write_text(
        "[]",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        task_tools,
        "TASK_FILE",
        test_file
    )

    monkeypatch.setattr(
        task_tools,
        "PENDING_DELETE_ID",
        None
    )

    return test_file


def read_test_data(test_file):
    with open(
        test_file,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def test_empty_task_list(temporary_task_file):
    result = task_tools.list_tasks()

    assert result == "当前没有任务。"


def test_add_task(temporary_task_file):
    result = task_tools.add_task(
        "学习Agent测试"
    )

    data = read_test_data(
        temporary_task_file
    )

    assert "已添加任务" in result
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["title"] == "学习Agent测试"
    assert data[0]["completed"] is False


def test_add_multiple_tasks(temporary_task_file):
    task_tools.add_task("任务一")
    task_tools.add_task("任务二")

    data = read_test_data(
        temporary_task_file
    )

    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2


def test_complete_task(temporary_task_file):
    task_tools.add_task("完成测试")

    result = task_tools.complete_task(1)

    data = read_test_data(
        temporary_task_file
    )

    assert "已完成" in result
    assert data[0]["completed"] is True


def test_complete_unknown_task(
    temporary_task_file
):
    result = task_tools.complete_task(999)

    assert "没有找到编号为999的任务" in result


def test_delete_requires_confirmation(
    temporary_task_file
):
    task_tools.add_task("等待删除")

    result = task_tools.request_delete_task(1)

    data = read_test_data(
        temporary_task_file
    )

    assert "请输入“确认删除”" in result
    assert len(data) == 1


def test_confirm_delete_task(
    temporary_task_file
):
    task_tools.add_task("需要删除")

    task_tools.request_delete_task(1)
    result = task_tools.confirm_delete_task()

    data = read_test_data(
        temporary_task_file
    )

    assert "已删除" in result
    assert data == []


def test_confirm_without_request(
    temporary_task_file
):
    result = task_tools.confirm_delete_task()

    assert result == "当前没有等待确认删除的任务。"