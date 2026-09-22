import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

MODEL = "deepseek-flash"

instructions = """
你是一位耐心的python学习助手。
回答使用中文，先给简洁结论，再解释原因。
"""

history = []

print("AI 助手已启动。")
print("输入 exit 退出，输入 clear 清空记忆。")

while True:
    user_input = input("\n你：").strip()

    if user_input.lower() == "exit":
        print("再见！")
        break

    if user_input.lower() == "clear":
        history.clear()
        print("对话记忆已清空。")
        continue

    history.append({
        "role": "user",
        "content": user_input
    })

    response = client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=history
    )

    answer = response.output_text
    print("\nAI：", answer)

    history.append({
        "role": "assistant",
        "content": answer
    })