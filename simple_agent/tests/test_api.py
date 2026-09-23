import pytest
from fastapi.testclient import TestClient

from simple_agent import api
from simple_agent import session_storage


class FakeAgent:
    def __init__(
        self,
        client=None,
        conversation_items=None
    ):
        if conversation_items is None:
            conversation_items = []

        self.conversation_items = conversation_items

    def ask(self, message: str) -> str:
        self.conversation_items.append(
            {
                "role": "user",
                "content": message
            }
        )

        answer = f"测试回答：{message}"

        self.conversation_items.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        return answer


@pytest.fixture
def api_client(tmp_path, monkeypatch):
    monkeypatch.setattr(
        session_storage,
        "SESSION_DIRECTORY",
        tmp_path
    )

    monkeypatch.setattr(
        api,
        "SimpleAgent",
        FakeAgent
    )

    api.agents.clear()

    monkeypatch.setenv(
        "AGENT_API_KEY",
        "test-agent-key"
    )

    with TestClient(api.app) as client:
        client.headers.update(
            {
                 "X-API-Key": "test-agent-key"
            }
        )

        yield client

    api.agents.clear()


def test_root_endpoint(api_client):
    response = api_client.get("/")

    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "Simple Agent API正在运行"
    )


def test_chat_endpoint(api_client):
    response = api_client.post(
        "/chat",
        json={
            "session_id": "test-session",
            "message": "你好"
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "session_id": "test-session",
        "answer": "测试回答：你好"
    }


def test_chat_saves_session(api_client):
    api_client.post(
        "/chat",
        json={
            "session_id": "save-test",
            "message": "保存这句话"
        }
    )

    history = session_storage.load_session(
        "save-test"
    )

    assert len(history) == 2
    assert history[0]["content"] == "保存这句话"


def test_invalid_session_id(api_client):
    response = api_client.post(
        "/chat",
        json={
            "session_id": "../unsafe",
            "message": "测试"
        }
    )

    assert response.status_code == 422


def test_delete_session(api_client):
    api_client.post(
        "/chat",
        json={
            "session_id": "delete-test",
            "message": "测试"
        }
    )

    response = api_client.delete(
        "/sessions/delete-test"
    )

    assert response.status_code == 200
    assert "已删除" in response.json()["message"]

    assert (
        session_storage
        .get_session_file("delete-test")
        .exists()
        is False
    )


def test_delete_unknown_session(api_client):
    response = api_client.delete(
        "/sessions/not-found"
    )

    assert response.status_code == 404


def test_missing_api_key(
    tmp_path,
    monkeypatch
):
    monkeypatch.setattr(
        session_storage,
        "SESSION_DIRECTORY",
        tmp_path
    )

    monkeypatch.setenv(
        "AGENT_API_KEY",
        "test-agent-key"
    )

    with TestClient(api.app) as client:
        response = client.post(
            "/chat",
            json={
                "session_id": "auth-test",
                "message": "你好"
            }
        )

    assert response.status_code == 401
    assert response.json()["detail"] == "缺少X-API-Key"