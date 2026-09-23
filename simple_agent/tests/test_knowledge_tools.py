from simple_agent import knowledge_tools


def test_rejects_low_similarity(
    monkeypatch
):
    fake_results = [
        {
            "title": "Python函数",
            "source": "python_notes.json",
            "chunk_index": 0,
            "similarity": 0.200,
            "content": "函数相关内容"
        }
    ]

    monkeypatch.setattr(
        knowledge_tools,
        "retrieve_knowledge",
        lambda query, top_k: fake_results
    )

    result = knowledge_tools.search_knowledge(
        "红烧肉怎么做"
    )

    assert "没有足够信息" in result
    assert "0.200" in result


def test_accepts_high_similarity(
    monkeypatch
):
    fake_results = [
        {
            "title": "Python异常处理",
            "source": "python_notes.json",
            "chunk_index": 0,
            "similarity": 0.800,
            "content": "使用try和except处理异常"
        }
    ]

    monkeypatch.setattr(
        knowledge_tools,
        "retrieve_knowledge",
        lambda query, top_k: fake_results
    )

    result = knowledge_tools.search_knowledge(
        "程序出错怎么办"
    )

    assert "Python异常处理" in result
    assert "使用try和except" in result