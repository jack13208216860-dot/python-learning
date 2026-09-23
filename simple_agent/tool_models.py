from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EmptyArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CalculateArguments(BaseModel):
    number1: float
    number2: float
    operation: Literal[
        "add",
        "subtract",
        "multiply",
        "divide"
    ]


class AddTaskArguments(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100
    )


class TaskIdArguments(BaseModel):
    task_id: int = Field(gt=0)

class KnowledgeSearchArguments(BaseModel):
    keyword: str = Field(
        min_length=1,
        max_length=50
    )