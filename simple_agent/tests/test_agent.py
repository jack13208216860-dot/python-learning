from unittest.mock import Mock

from simple_agent.agent import SimpleAgent


def create_message_item(text: str):
    item = Mock()

    item.type = "message"
    item.model_dump.return_value = {
        "type": "message",
        "role": "assistant",
        "content": [
            {
                "type": "output_text",
                "text": text
            }
        ]
    }

    return item


def create_tool_call(
    name: str,
    arguments: str,
    call_id: str
):
    item = Mock()

    item.type = "function_call"
    item.name = name
    item.arguments = arguments
    item.call_id = call_id

    item.model_dump.return_value = {
        "type": "function_call",
        "name": name,
        "arguments": arguments,
        "call_id": call_id
    }

    return item


def test_agent_answers_without_tool():
    fake_client = Mock()

    message_item = create_message_item(
        "Python是一门编程语言。"
    )

    fake_response = Mock()
    fake_response.output = [message_item]
    fake_response.output_text = "Python是一门编程语言。"

    fake_client.responses.create.return_value = (
        fake_response
    )

    agent = SimpleAgent(client=fake_client)

    answer = agent.ask("Python是什么？")

    assert answer == "Python是一门编程语言。"
    assert fake_client.responses.create.call_count == 1


def test_agent_calls_calculator():
    fake_client = Mock()

    tool_call = create_tool_call(
        name="calculate",
        arguments=(
            '{"number1": 20, '
            '"number2": 6, '
            '"operation": "multiply"}'
        ),
        call_id="test-call-1"
    )

    first_response = Mock()
    first_response.output = [tool_call]
    first_response.output_text = ""

    message_item = create_message_item(
        "20乘以6等于120。"
    )

    second_response = Mock()
    second_response.output = [message_item]
    second_response.output_text = "20乘以6等于120。"

    fake_client.responses.create.side_effect = [
        first_response,
        second_response
    ]

    agent = SimpleAgent(client=fake_client)

    answer = agent.ask("计算20乘以6")

    assert answer == "20乘以6等于120。"
    assert fake_client.responses.create.call_count == 2

    tool_outputs = [
        item
        for item in agent.conversation_items
        if item.get("type") == "function_call_output"
    ]

    assert len(tool_outputs) == 1
    assert tool_outputs[0]["call_id"] == "test-call-1"
    assert float(tool_outputs[0]["output"]) == 120