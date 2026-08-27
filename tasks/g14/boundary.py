"""자르는 규칙을 색인 안에 두는 것과 밖에 두는 것.

두 방법은 지금 같은 결과를 낸다. 그래서 지금은 어느 쪽이든 상관이 없다.
달라지는 것은 문서 종류가 늘었을 때다. 경계는 그때 값을 치른다.
"""

from __future__ import annotations

from g12.retrieve import Chunk, Index, split

# 문서 종류마다 다르게 자르고 싶어졌을 때 쓰는 표. 색인은 이 표를 모른다.
RULES: dict[str, dict[str, int]] = {
    "policy": {"size": 30, "overlap": 5},
    "notice": {"size": 60, "overlap": 15},
}


def index_inside(docs: dict[str, str]) -> Index:
    """자르는 규칙이 색인 안에 있다. 지금 코드가 이쪽이다."""
    index = Index()
    for doc_id, text in docs.items():
        index.add_document(doc_id, text, size=30, overlap=5)
    return index


def index_outside(docs: dict[str, str]) -> Index:
    """밖에서 자르고 조각만 넣는다. 색인은 자르는 법을 모른다."""
    index = Index()
    for doc_id, text in docs.items():
        for chunk in split(doc_id, text, size=30, overlap=5):
            index.add(chunk)
    return index


def index_by_kind(docs: dict[str, str], kinds: dict[str, str]) -> Index:
    """종류마다 다르게 자른다. 밖에서 자를 때만 되는 일이다."""
    index = Index()
    for doc_id, text in docs.items():
        rule = RULES[kinds[doc_id]]
        for chunk in split(doc_id, text, **rule):
            index.add(chunk)
    return index


def chunk_ids(index: Index) -> list[str]:
    return [c.chunk_id for c in index.chunks]


def same_result(left: Index, right: Index) -> bool:
    return chunk_ids(left) == chunk_ids(right)
