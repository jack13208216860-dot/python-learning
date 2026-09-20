class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"我是{self.name}, 今年{self.age}岁。")

class Student(Person):
    def __init__(self, name, age, course):
        super().__init__(name, age)
        self.course = course

    def study(self):
        print(f"{self.name}正在学习{self.course}。")

student1 = Student("Eason", 18, "python")
student1.introduce()
student1.study()

class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def teach(self):
        print(f"{self.name}正在教授{self.subject}。")
teacher1 = Teacher("Eason", 23, "Python")
teacher1.introduce()
teacher1.teach()
