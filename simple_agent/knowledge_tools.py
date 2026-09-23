import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np


KNOWLEDGE_DIRECTORY = (
    Path(__file__).parent
    / "knowledge"
)

DOCUMENTS_DIRECTORY = (
    KNOWLEDGE_DIRECTORY
    / "documents"
)

SUPPORTED_FILE_TYPES = {
    ".md",
    ".txt"
}

KNOWLEDGE_FILE = (
    KNOWLEDGE_DIRECTORY
    / "python_notes.json"
)

CHUNKS_FILE = (
    KNOWLEDGE_DIRECTORY
    / "knowledge_chunks.json"
)

VECTOR_FILE = (
    KNOWLEDGE_DIRECTORY
    / "knowledge_vectors.npy"
)

METADATA_FILE = (
    KNOWLEDGE_DIRECTORY
    / "knowledge_index_meta.json"
)

MODEL_NAME = "BAAI/bge-small-zh-v1.5"
MIN_SIMILARITY = 0.446

CHUNK_SIZE = 120
CHUNK_OVERLAP = 30

embedding_model: Any = None
cached_chunks: list[dict] | None = None
cached_vectors = None


def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        from sentence_transformers import (
            SentenceTransformer
        )

        print("正在加载Embedding模型……")

        embedding_model = SentenceTransformer(
            MODEL_NAME
        )

    return embedding_model


def get_document_files() -> list[Path]:
    if not DOCUMENTS_DIRECTORY.exists():
        return []

    return sorted(
        path
        for path in DOCUMENTS_DIRECTORY.rglob("*")
        if (
            path.is_file()
            and path.suffix.lower()
            in SUPPORTED_FILE_TYPES
        )
    )

def calculate_knowledge_hash() -> str:
    sha256 = hashlib.sha256()

    source_files = []

    if KNOWLEDGE_FILE.exists():
        source_files.append(
            KNOWLEDGE_FILE
        )

    source_files.extend(
        get_document_files()
    )

    for path in source_files:
        relative_path = path.relative_to(
            KNOWLEDGE_DIRECTORY
        )

        sha256.update(
            str(relative_path).encode("utf-8")
        )

        with open(path, "rb") as file:
            while True:
                data = file.read(8192)

                if not data:
                    break

                sha256.update(data)

    return sha256.hexdigest()


def load_documents() -> list[dict]:
    documents = []

    if KNOWLEDGE_FILE.exists():
        with open(
            KNOWLEDGE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            json_documents = json.load(file)

        if not isinstance(
            json_documents,
            list
        ):
            raise ValueError(
                "python_notes.json最外层必须是列表"
            )

        for document in json_documents:
            documents.append(
                {
                    "title": document["title"],
                    "content": document["content"],
                    "source": "python_notes.json"
                }
            )

    for path in get_document_files():
        content = path.read_text(
            encoding="utf-8"
        ).strip()

        if not content:
            continue

        documents.append(
            {
                "title": path.stem,
                "content": content,
                "source": str(
                    path.relative_to(
                        KNOWLEDGE_DIRECTORY
                    )
                )
            }
        )

    if not documents:
        raise ValueError(
            "没有找到可建立索引的知识文档"
        )

    return documents


def split_document(
    title: str,
    content: str,
    source: str
) -> list[dict]:
    content = content.strip()

    if not content:
        return []

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(content):
        end = min(
            start + CHUNK_SIZE,
            len(content)
        )

        chunk_content = content[start:end]

        chunks.append(
            {
                "title": title,
                "source": source,
                "chunk_index": chunk_index,
                "content": chunk_content
            }
        )

        if end == len(content):
            break

        start = end - CHUNK_OVERLAP
        chunk_index += 1

    return chunks


def create_chunks(
    documents: list[dict]
) -> list[dict]:
    chunks = []

    for document in documents:
        document_chunks = split_document(
            title=document["title"],
            content=document["content"],
            source=document["source"]
        )

        chunks.extend(document_chunks)

    return chunks


def build_knowledge_index() -> int:
    global cached_chunks
    global cached_vectors

    documents = load_documents()
    chunks = create_chunks(documents)

    if not chunks:
        raise ValueError(
            "知识库没有可以建立索引的内容"
        )

    chunk_texts = [
        chunk["title"]
        + " "
        + chunk["content"]
        for chunk in chunks
    ]

    model = get_embedding_model()

    vectors = model.encode(
        chunk_texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    with open(
        CHUNKS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            chunks,
            file,
            ensure_ascii=False,
            indent=2
        )

    np.save(
        VECTOR_FILE,
        vectors
    )

    metadata = {
        "model_name": MODEL_NAME,
        "document_count": len(documents),
        "chunk_count": len(chunks),
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "knowledge_hash": calculate_knowledge_hash()
    }

    with open(
        METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            metadata,
            file,
            ensure_ascii=False,
            indent=2
        )

    cached_chunks = chunks
    cached_vectors = vectors

    return len(chunks)


def load_knowledge_index():
    global cached_chunks
    global cached_vectors

    if (
        cached_chunks is not None
        and cached_vectors is not None
    ):
        return cached_chunks, cached_vectors

    required_files = [
        CHUNKS_FILE,
        VECTOR_FILE,
        METADATA_FILE
    ]

    if not all(
        path.exists()
        for path in required_files
    ):
        raise FileNotFoundError(
            "知识库索引不完整，请运行："
            "python -m simple_agent.build_knowledge_index"
        )

    with open(
        METADATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        metadata = json.load(file)

    if (
        metadata.get("knowledge_hash")
        != calculate_knowledge_hash()
    ):
        raise ValueError(
            "知识库内容已经变化，请重新构建索引"
        )

    if metadata.get("model_name") != MODEL_NAME:
        raise ValueError(
            "Embedding模型已经变化，请重新构建索引"
        )

    if metadata.get("chunk_size") != CHUNK_SIZE:
        raise ValueError(
            "切块大小已经变化，请重新构建索引"
        )

    if (
        metadata.get("chunk_overlap")
        != CHUNK_OVERLAP
    ):
        raise ValueError(
            "重叠大小已经变化，请重新构建索引"
        )

    with open(
        CHUNKS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        chunks = json.load(file)

    vectors = np.load(
        VECTOR_FILE,
        allow_pickle=False
    )

    if len(chunks) != len(vectors):
        raise ValueError(
            "文本块与向量数量不一致，请重新构建索引"
        )

    if metadata.get("chunk_count") != len(chunks):
        raise ValueError(
            "索引元数据不一致，请重新构建索引"
        )

    cached_chunks = chunks
    cached_vectors = vectors

    return chunks, vectors


def retrieve_knowledge(
    query: str,
    top_k: int = 3
) -> list[dict]:
    query = query.strip()

    if not query:
        raise ValueError(
            "搜索关键词不能为空"
        )

    if top_k <= 0:
        raise ValueError(
            "top_k必须大于0"
        )

    chunks, chunk_vectors = (
        load_knowledge_index()
    )

    model = get_embedding_model()

    query_text = (
        "为这个句子生成表示以用于检索相关文章："
        + query
    )

    query_vector = model.encode(
        query_text,
        normalize_embeddings=True
    )

    similarities = (
        chunk_vectors
        @ query_vector
    )

    ranked_indexes = similarities.argsort()[::-1]
    results = []

    for index in ranked_indexes[:top_k]:
        chunk = chunks[index]

        results.append(
            {
                "title": chunk["title"],
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"],
                "similarity": float(
                    similarities[index]
                ),
                "content": chunk["content"]
            }
        )

    return results


def search_knowledge(keyword: str) -> str:
    try:
        results = retrieve_knowledge(
            query=keyword,
            top_k=3
        )

    except (
        FileNotFoundError,
        ValueError
    ) as error:
        return f"搜索失败：{error}"

    if not results:
        return "没有找到相关知识。"

    highest_similarity = results[0][
        "similarity"
    ]

    if highest_similarity < MIN_SIMILARITY:
        return (
            "知识库中没有足够信息回答这个问题。"
            f"最高相似度只有"
            f"{highest_similarity:.3f}，"
            f"低于阈值{MIN_SIMILARITY:.3f}。"
        )

    relevant_results = [
        result
        for result in results
        if (
            result["similarity"]
            >= MIN_SIMILARITY
        )
    ]

    formatted_results = []

    for result in relevant_results:
        formatted_results.append(
            f'标题：{result["title"]}\n'
            f'文件：{result["source"]}\n'
            f'文本块：{result["chunk_index"]}\n'
            f'相似度：{result["similarity"]:.3f}\n'
            f'内容：{result["content"]}'
        )

    return "\n\n".join(formatted_results)