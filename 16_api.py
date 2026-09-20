import requests

url = "https://jsonplaceholder.typicode.com/todos/1"

response = requests.get(url)
data = response.json()

print(data)
print("任务标题：", data["title"])
print("是否完成：", data["completed"])