import requests

url = "https://jsonplaceholder.typicode.com/todos/1"

try:
    response = requests.get(url, timeout=10)

    # 如果状态码是 4xx 或 5xx，主动抛出异常
    response.raise_for_status()

    data = response.json()

    print("状态码：", response.status_code)
    print("任务标题：", data["title"])
    print("是否完成：", data["completed"])

except requests.exceptions.Timeout:
    print("请求超时，请稍后再试。")

except requests.exceptions.RequestException as error:
    print("请求失败：", error)