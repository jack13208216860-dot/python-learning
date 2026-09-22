import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

response = client.responses.create(
    model="gpt-6-astra",
    input="请用一句话解释什么是 Python 函数。"
)
print(response.output_text)