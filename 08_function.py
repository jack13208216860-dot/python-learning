# def say_hello():
#     print("你好，Python！")


# say_hello()

# def greet(name):
#     print(f"你好，{name}！")


# greet("Eason")
# greet("Python")

def introduce(name, course):
    print(f"我叫{name}, 我正在学习{course}")

introduce("Eason", "Python")

def calculate_sum(number1, number2):
    return number1 + number2

result = calculate_sum(10, 20)
print("结果为：", result)

def is_adult(age):
    if age >= 18:
        return True
    else:
        return False
print("是否成年：", is_adult(18))


def get_grade(score):
    if score >= 90:
        return "优秀"
    elif score >= 80:
        return "良好"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"
print("成绩等级：", get_grade(85))