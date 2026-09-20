import os

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("已读取到 API Key。")
    print("前四位是：", api_key[:4])
else:
    print("没有找到 OPENAI_API_KEY。")