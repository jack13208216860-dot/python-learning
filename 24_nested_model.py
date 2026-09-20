from pydantic import BaseModel, Field


class Course(BaseModel):
    name: str
    hours: int = Field(gt=0)


class Student(BaseModel):
    name: str
    age: int = Field(gt=0)
    courses: list[Course]


raw_data = {
    "name": "Eason",
    "age": 18,
    "courses": [
        {"name": "Python", "hours": 30},
        {"name": "Agent Development", "hours": 20}
    ]
}

student = Student.model_validate(raw_data)

print(student)
print(student.model_dump())

for course in student.courses:
    print(f"课程：{course.name}，学习时长：{course.hours} 小时")