def calculate_average(scores: list[int]) -> float:
    return sum(scores) / len(scores)


def get_result(score: int) -> str:
    if score >= 60:
        return "及格"
    return "不及格"


scores = [90, 85, 92]

average = calculate_average(scores)

print("平均分：", average)
print("考试结果：", get_result(int(average)))