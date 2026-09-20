# try:
#     number = int(input("请输入一个整数："))
#     print("你输入的数字是：", number)

# except ValueError:
#     print("输入错误，请输入整数。")

# try:
#     number1 = float(input("请输入第一个数字："))
#     number2 = float(input("请输入第二个数字："))

#     result = number1 / number2

# except ValueError:
#     print("输入错误，请输入数字。")

# except ZeroDivisionError:
#     print("除数不能为 0。")

# else:
#     print("计算结果：", result)

# finally:
#     print("程序执行结束。")

try:
    number1 = float(input("请输入第一个数字："))
    number2 = float(input("请输入第二个数字: "))
    aa = input("输入运算符(+,-,*,/): ")
    if aa == "+":
        result = number1 + number2
    elif aa == "-":
        result = number1 - number2
    elif aa == "*":
        result = number1 * number2
    elif aa == "/":
        result = number1 / number2
    else:
        print("无效的运算符。")
        result = None
except ValueError:
    print("输入错误，请输入数字。")
except ZeroDivisionError:
    print("除数不能为 0。")
else:
    if result is not None:
        print("计算结果：", result)
finally:
    print("感谢使用计算器!")

