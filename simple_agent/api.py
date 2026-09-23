import os
import secrets

from pathlib import Path
from fastapi import (
    Depends,
    FastAPI,
    Header,
    HTTPException
)
from pydantic import BaseModel, Field
from fastapi.responses import FileResponse
from .agent import SimpleAgent
from .session_storage import (
    delete_session_file,
    get_session_file,
    load_session,
    save_session
)


STATIC_DIRECTORY = (
    Path(__file__).parent
    / "static"
)

app = FastAPI(
    title="Simple Agent API",
    description="支持工具调用和持久化记忆的Agent",
    version="1.2.0"
)


agents: dict[str, SimpleAgent] = {}

def verify_api_key(
    x_api_key: str | None = Header(
        default=None,
        alias="X-API-Key"
    )
):
    expected_api_key = os.getenv(
        "AGENT_API_KEY"
    )

    if not expected_api_key:
        raise HTTPException(
            status_code=500,
            detail="服务器没有配置AGENT_API_KEY"
        )

    if x_api_key is None:
        raise HTTPException(
            status_code=401,
            detail="缺少X-API-Key"
        )

    if not secrets.compare_digest(
        x_api_key,
        expected_api_key
    ):
        raise HTTPException(
            status_code=401,
            detail="X-API-Key不正确"
        )

class ChatRequest(BaseModel):
    session_id: str = Field(
        min_length=1,
        max_length=50,
        pattern=r"^[A-Za-z0-9_-]+$"
    )

    message: str = Field(
        min_length=1,
        max_length=500
    )


class ChatResponse(BaseModel):
    session_id: str
    answer: str


class DeleteSessionResponse(BaseModel):
    message: str


@app.get("/")
def read_root():
    return {
        "message": "Simple Agent API正在运行",
        "active_sessions": len(agents)
    }

@app.get(
    "/chat-ui",
    include_in_schema=False
)
def chat_ui():
    return FileResponse(
        STATIC_DIRECTORY / "index.html"
    )

@app.post(
    "/chat",
    response_model=ChatResponse,
    dependencies=[
        Depends(verify_api_key)
    ]
)
def chat(request: ChatRequest):
    try:
        agent = agents.get(request.session_id)

        if agent is None:
            saved_history = load_session(
                request.session_id
            )

            agent = SimpleAgent(
                conversation_items=saved_history
            )

            agents[request.session_id] = agent

        answer = agent.ask(
            request.message
        )

        save_session(
            request.session_id,
            agent.conversation_items
        )

        return ChatResponse(
            session_id=request.session_id,
            answer=answer
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        ) from error


@app.delete(
    "/sessions/{session_id}",
    response_model=DeleteSessionResponse,
    dependencies=[
        Depends(verify_api_key)
    ]
)
def delete_session(session_id: str):
    exists_in_memory = session_id in agents
    exists_on_disk = get_session_file(
        session_id
    ).exists()

    if not exists_in_memory and not exists_on_disk:
        raise HTTPException(
            status_code=404,
            detail="没有找到这个会话"
        )

    agents.pop(session_id, None)
    delete_session_file(session_id)

    return DeleteSessionResponse(
        message=f"会话{session_id}已删除"
    )