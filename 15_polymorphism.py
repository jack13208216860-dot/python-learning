class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def work(self):
        print(f"{self.name}正在学习 Python。")


class Teacher(Person):
    def work(self):
        print(f"{self.name}正在教授 Python。")

class Developer(Person):
    def work(self):
        print(f"{self.name}正在开发Agent")


people = [
    Student("Eason"),
    Teacher("Alice"),
    Developer("Jack")
]

for person in people:
    person.work()