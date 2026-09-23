from simple_agent import session_storage


def test_save_and_load_session(
    tmp_path,
    monkeypatch
):
    monkeypatch.setattr(
        session_storage,
        "SESSION_DIRECTORY",
        tmp_path
    )

    history = [
        {
            "role": "user",
            "content": "你好"
        },
        {
            "role": "assistant",
            "content": "你好！"
        }
    ]

    session_storage.save_session(
        "test-session",
        history
    )

    loaded_history = session_storage.load_session(
        "test-session"
    )

    assert loaded_history == history


def test_load_unknown_session(
    tmp_path,
    monkeypatch
):
    monkeypatch.setattr(
        session_storage,
        "SESSION_DIRECTORY",
        tmp_path
    )

    result = session_storage.load_session(
        "unknown-session"
    )

    assert result == []


def test_delete_session_file(
    tmp_path,
    monkeypatch
):
    monkeypatch.setattr(
        session_storage,
        "SESSION_DIRECTORY",
        tmp_path
    )

    session_storage.save_session(
        "delete-test",
        [
            {
                "role": "user",
                "content": "测试"
            }
        ]
    )

    deleted = session_storage.delete_session_file(
        "delete-test"
    )

    assert deleted is True
    assert (
        session_storage
        .get_session_file("delete-test")
        .exists()
        is False
    )