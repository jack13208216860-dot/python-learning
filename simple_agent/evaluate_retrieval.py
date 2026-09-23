import json
from pathlib import Path

from .knowledge_tools import (
    retrieve_knowledge
)


EVALUATION_FILE = (
    Path(__file__).parent
    / "knowledge"
    / "retrieval_eval.json"
)


def main():
    with open(
        EVALUATION_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        test_cases = json.load(file)

    correct_count = 0
    positive_count = 0
    positive_scores = []
    negative_scores = []

    for number, test_case in enumerate(
        test_cases,
        start=1
    ):
        query = test_case["query"]
        expected_title = test_case["expected_title"]

        results = retrieve_knowledge(
            query=query,
            top_k=3
        )

        top_result = results[0]
        actual_title = top_result["title"]
        similarity = top_result["similarity"]

        print(f"\n测试{number}")
        print(f"问题：{query}")
        print(f"预期：{expected_title}")
        print(f"实际：{actual_title}")
        print(f"最高相似度：{similarity:.3f}")

        if expected_title is None:
            negative_scores.append(
                similarity
            )

            print("类型：知识库外问题")

        else:
            positive_count += 1
            positive_scores.append(
                similarity
            )

            if actual_title == expected_title:
                correct_count += 1
                print("检索结果：通过")
            else:
                print("检索结果：失败")

        print("Top 3：")

        for rank, result in enumerate(
            results,
            start=1
        ):
            print(
                f'  {rank}. '
                f'{result["title"]} '
                f'({result["similarity"]:.3f})'
            )

    accuracy = (
        correct_count / positive_count
        if positive_count
        else 0
    )

    print("\n--- 正向问题评测 ---")
    print(f"正向问题：{positive_count}")
    print(f"正确数量：{correct_count}")
    print(f"Top-1准确率：{accuracy:.1%}")

    if positive_scores:
        lowest_positive = min(
            positive_scores
        )

        print(
            f"正向问题最低相似度："
            f"{lowest_positive:.3f}"
        )

    if negative_scores:
        highest_negative = max(
            negative_scores
        )

        print(
            f"无关问题最高相似度："
            f"{highest_negative:.3f}"
        )

    if positive_scores and negative_scores:
        lowest_positive = min(
            positive_scores
        )

        highest_negative = max(
            negative_scores
        )

        print("\n--- 阈值分析 ---")

        if lowest_positive > highest_negative:
            suggested_threshold = (
                lowest_positive
                + highest_negative
            ) / 2

            print(
                "正向和无关问题可以分开。"
            )

            print(
                f"建议阈值："
                f"{suggested_threshold:.3f}"
            )

        else:
            print(
                "正向和无关问题的分数存在重叠。"
            )

            print(
                "暂时不能只依靠一个固定阈值，"
                "需要增加评测问题或改进知识库。"
            )


if __name__ == "__main__":
    main()