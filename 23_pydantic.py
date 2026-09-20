from pydantic import BaseModel, Field, ValidationError


class Student(BaseModel):
    name: str
    age: int = Field(gt=0)
    score: float = Field(ge=0, le=100)


try:
    student1 = Student(name="Eason", age=18, score=90)

    print(student1)
    print(student1.model_dump())

    student2 = Student(name="Alice", age=20, score=120)

except ValidationError as error:
    print("数据验证失败：")
    print(error)