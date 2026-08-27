"""문서가 열 배가 되면 어디가 먼저 버거워지는지를 세는 자리.

시간을 재지 않고 횟수를 센다. 시간은 돌릴 때마다 다르고 횟수는 안 그렇다.
관문 14에서 지원자에게 보여 주는 표가 여기서 나온다.
"""

from __future__ import annotations

from dataclasses import dataclass

from g13.goldset import DOCS
from g12.retrieve import Index


def grow(times: int, size: int = 30, overlap: int = 5) -> Index:
    """같은 문서 묶음을 여러 벌 넣는다. 문서 수만 늘리고 종류는 그대로 둔다."""
    index = Index()
    for copy in range(times):
        for doc_id, text in DOCS.items():
            index.add_document(f"{doc_id}-{copy}", text, size=size, overlap=overlap)
    return index


@dataclass(frozen=True)
class Load:
    docs: int
    chunks: int
    scored_per_query: int
    vocabulary: int


def measure_load(times: int) -> Load:
    index = grow(times)
    return Load(
        docs=times * len(DOCS),
        # search 는 조각을 하나도 안 거르고 전부 점수 매긴다. 그래서 조각 수가 곧 비용이다.
        chunks=len(index.chunks),
        scored_per_query=len(index.chunks),
        vocabulary=len(index._df),
    )


LADDER: tuple[int, ...] = (1, 10, 100)


def load_table(ladder: tuple[int, ...] = LADDER) -> list[Load]:
    return [measure_load(times) for times in ladder]
