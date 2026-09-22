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
print("AI助手已启动。输入exit退出。")

while True:
    user_input = input("\n你：")
    if user_input.lower() == "exit":
        print("再见!")
        break

    response = client.responses.create(
        model=MODEL,
        instructions=instructions,
        input=user_input
    )

    print("\nAI:",response.output_text)