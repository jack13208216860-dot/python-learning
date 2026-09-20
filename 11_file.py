# with open("notes.txt", "w", encoding="utf-8") as file:
#     file.write("今天学习了 Python 文件读写。\n")
#     file.write("下一步学习 JSON。\n")

# print("文件写入完成。")

# with open("notes.txt", "r", encoding="utf-8") as file:
#     content = file.read()

# print(content)

with open("learning_notes.txt", "w", encoding="utf-8") as file:
    file.write("姓名：Eason\n")
    file.write("当前学习内容：Python 文件读写\n")
    file.write("下一步计划：学习 JSON\n")

with open("learning_notes.txt", "r", encoding="utf-8") as file:
    content = file.read()
print(content)

with open("learning_notes.txt", "a", encoding="utf-8") as file:
    file.write("我正在为学习 Agent 开发打基础。\n")

with open("learning_notes.txt", "r", encoding="utf-8") as file:
    content = file.read()
print(content)