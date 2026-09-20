# student = {
#     "name": "Eason",
#     "age": 18,
#     "course": "Python"
# }

# print(student)
# print(student["name"])
# print(student["age"])


book = {
    "name": "Python",
    "price": 100,
    "author": "Eason",
    "num": 1000
}
print(book["name"])
print(book["price"])
book["source"] = "China"
book["price"] = 200
book.pop("num")
print(book.get("grade"))
for key, value in book.items():
    print(key, ":", value)
print(book)