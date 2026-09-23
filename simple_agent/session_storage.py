import json
from pathlib import Path


SESSION_DIRECTORY = (
    Path(__file__).parent
    / "data"
    / "sessions"
)


def get_session_file(session_id: str) -> Path:
    return SESSION_DIRECTORY / f"{session_id}.json"


def load_session(session_id: str) -> list[dict]:
    session_file = get_session_file(session_id)

    if not session_file.exists():
        return []

    with open(
        session_file,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("会话文件格式错误")

    return data


def save_session(
    session_id: str,
    conversation_items: list[dict]
) -> None:
    SESSION_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    session_file = get_session_file(session_id)
    temporary_file = session_file.with_suffix(".tmp")

    with open(
        temporary_file,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            conversation_items,
            file,
            ensure_ascii=False,
            indent=2
        )

    temporary_file.replace(session_file)


def delete_session_file(session_id: str) -> bool:
    session_file = get_session_file(session_id)

    if not session_file.exists():
        return False

    session_file.unlink()

    return True