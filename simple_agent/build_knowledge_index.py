from .knowledge_tools import (
    VECTOR_FILE,
    build_knowledge_index
)


def main():
    print("开始切分文档并构建向量索引……")

    chunk_count = build_knowledge_index()

    print(
        f"索引构建完成，共生成"
        f"{chunk_count}个文本块。"
    )

    print(
        f"向量文件：{VECTOR_FILE}"
    )


if __name__ == "__main__":
    main()