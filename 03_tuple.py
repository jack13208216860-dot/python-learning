student = ("Eason", 18, "python")
print(student[0])
print(student[1])
print(student[2])
print(student[0:2])
print(student.index("python"))
print(student.count(18))
name, age, course = student

print(name)
print(age)
print(course)

student_list=list(student)
student_list[1]=19
student=tuple(student_list)
print(student)