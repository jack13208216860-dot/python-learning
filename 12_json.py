# import json

# student = {
#     "name": "Eason",
#     "age": 18,
#     "courses": ["Python", "AI"],
#     "is_adult": True
# }

# with open("student.json", "w", encoding="utf-8") as file:
#     json.dump(student, file, ensure_ascii=False, indent=4)

# print("JSON 文件保存成功。")

# with open("student.json", "r", encoding="utf-8") as file:
#     student_data = json.load(file)

# print(student_data)
# print(student_data["name"])
# print(student_data["courses"])

import json

student = [
{
    "name": "Eason",
    "age": 18,
    "score": 90 
},
{
    "name": "Alice",
    "age": 20,
    "score": 85
},
{
    "name": "Bob",
    "age": 19,
    "score": 92
}
]
with open("students.json", "w", encoding = "utf-8") as file:
    json.dump(student, file, ensure_ascii=False, indent=4)

with open("students.json", "r", encoding = "utf-8") as file:
    student_data = json.load(file)
    for student in student_data:
        print(f"姓名: {student['name']}, 年龄: {student['age']}, 分数: {student['score']}")

total_score = 0

for student in student_data:
    total_score += student["score"]
average_score = total_score / len(student_data)
print("平均分：", average_score)

student_data[0]["course"] = "python"
with open("students.json", "w", encoding="utf-8") as file:
    json.dump(student_data, file, ensure_ascii=False, indent=4)

with open("students.json", "r", encoding = "utf-8") as file:
    student_data = json.load(file)
    print(student_data)
    for student in student_data:
         print(f"姓名: {student['name']}, 年龄: {student['age']}, 分数: {student['score']}, 课程：{student.get('course', '未设置')}")
