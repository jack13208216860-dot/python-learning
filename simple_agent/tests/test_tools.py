import pytest

from simple_agent.tools import (
    TOOL_FUNCTIONS,
    calculate,
    execute_tool
)


def test_addition():
    result = calculate(
        number1=10,
        number2=5,
        operation="add"
    )

    assert result == 15


def test_subtraction():
    result = calculate(
        number1=10,
        number2=5,
        operation="subtract"
    )

    assert result == 5


def test_multiplication():
    result = calculate(
        number1=6,
        number2=7,
        operation="multiply"
    )

    assert result == 42


def test_division():
    result = calculate(
        number1=10,
        number2=4,
        operation="divide"
    )

    assert result == pytest.approx(2.5)


def test_division_by_zero():
    with pytest.raises(
        ValueError,
        match="除数不能为0"
    ):
        calculate(
            number1=10,
            number2=0,
            operation="divide"
        )


def test_unknown_operation():
    with pytest.raises(
        ValueError,
        match="不支持的运算"
    ):
        calculate(
            number1=10,
            number2=5,
            operation="power"
        )


def test_invalid_task_id():
    result = execute_tool(
        "complete_task",
        {
            "task_id": 0
        }
    )

    assert "工具参数验证失败" in result


def test_unknown_tool():
    result = execute_tool(
        "unknown_tool",
        {}
    )

    assert result == "未知工具：unknown_tool"


def test_tools_are_registered():
    assert "get_current_time" in TOOL_FUNCTIONS
    assert "calculate" in TOOL_FUNCTIONS
    assert "list_tasks" in TOOL_FUNCTIONS
    assert "add_task" in TOOL_FUNCTIONS
    assert "complete_task" in TOOL_FUNCTIONS
    assert "request_delete_task" in TOOL_FUNCTIONS
    assert "confirm_delete_task" in TOOL_FUNCTIONS