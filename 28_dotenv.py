import os
from dotenv import load_dotenv

load_dotenv()

app_name = os.getenv("APP_NAME")
debug = os.getenv("DEBUG")

print("项目名称：", app_name)
print("调试模式：",debug)