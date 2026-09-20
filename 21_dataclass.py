from dataclasses import dataclass


@dataclass
class Student:
    name: str
    age: int
    score: float
    course: str = "Python"

    def is_passed(self) -> bool:
        return self.score >= 60


student1 = Student("Eason", 18, 90)

print(student1)
print("姓名：", student1.name)
print("课程：", student1.course)
print("是否及格：", student1.is_passed())