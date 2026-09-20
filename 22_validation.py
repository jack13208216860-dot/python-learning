from dataclasses import dataclass


@dataclass
class Student:
    name: str
    age: int
    score: float

    def __post_init__(self):
        if self.age <= 0:
            raise ValueError("年龄必须大于 0。")

        if not 0 <= self.score <= 100:
            raise ValueError("分数必须在 0 到 100 之间。")


try:
    student1 = Student("Eason", 18, 90)
    print(student1)

    student2 = Student("Alice", 20, 120)
    print(student2)

except ValueError as error:
    print("数据错误：", error)