from pydantic import BaseModel, Field

class Task(BaseModel):
    id: int
    title: str = Field(min_length=1)
    completed: bool = False