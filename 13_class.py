class Student:
    def __init__(self, name, age, score, course):
        self.name = name
        self.age = age
        self.score = score
        self.course = course

    def introduce(self):
        print(f"我是{self.name}，今年{self.age}岁，分数是{self.score}, 课程是{self.course}。")

    def update_score(self, new_score):
        self.score = new_score

    def is_passed(self):
        return self.score >= 60


student1 = Student("Eason", 18, 90, "java")
student2 = Student("Jack", 20, 99, "python")

student1.introduce()
student2.introduce()
print("是否及格：", student1.is_passed())
print("是否及格：", student2.is_passed())

student1.update_score(95)
student1.introduce()