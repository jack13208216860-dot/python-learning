# for number in range(1, 6):
#     print(number)

# courses = ["Python", "Java", "Go"]

# for course in courses:
#     print(course)

# student = {
#     "name": "Eason",
#     "age": 18,
#     "course": "Python"
# }

# for key, value in student.items():
#     print(key, ":", value)

# number = 1

# while number <= 5:
#     print(number)
#     number += 1

for number in range(1, 11):
    print(number)

courses = ["Python", "Java", "Go"]
for course in courses:
    print(course)

grade = {
    "Math": 90,
    "English": 80,
    "Chinese": 70
}

for subject, score in grade.items():
    print(subject, ":", score)

number = 10
while number >= 1:
    print(number)
    number -= 1

# 输出 1 到 10 中的偶数
for number in range(2, 11, 2):
    print(number)

# 计算 1 到 100 的总和
total = 0

for number in range(1, 101):
    total += number

print("总和为：", total)

# 遇到 7 时停止循环
for number in range(1, 11):
    if number == 7:
        break

    print(number)

# 跳过数字 5
for number in range(1, 11):
    if number == 5:
        continue

    print(number)