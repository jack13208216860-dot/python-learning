# import random

# number = random.randint(1, 10)

# print("随机数字是：", number)

# import random

# courses = ["Python", "Java", "Go", "AI"]

# course = random.choice(courses)

# print("今天学习：", course)

# import my_tools
# result = my_tools.add(10, 20)
# print("结果为：", result)

import random
number = random.randint(1, 100)
print(number)

import my_tools
print("分数等级:", my_tools.get_grade(number))
if my_tools.is_adult(number):
    print("成年")
else:
    print("未成年")
