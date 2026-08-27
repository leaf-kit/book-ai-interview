"""정답 목록으로 검색을 재는 자리.

여기서 재는 것은 둘이다. 정답을 얼마나 데려왔는가와 데려온 것 중에 정답이 몇인가.
둘은 같이 안 움직인다. 그 어긋남을 그대로 보이는 것이 이 파일이 하는 일이다.
"""

from __future__ import annotations

from dataclasses import dataclass

from g12.retrieve import Index
from g13.goldset import CASES, DOCS, Case


def build_index(size: int = 40, overlap: int = 10) -> Index:
    index = Index()
    for doc_id, text in DOCS.items():
        index.add_document(doc_id, text, size=size, overlap=overlap)
    return index


def hit_docs(index: Index, query: str, top_k: int) -> list[str]:
    """뽑아 온 조각의 문서 아이디를 순서대로 준다. 같은 문서가 여러 번 나올 수 있다."""
    return [chunk.doc_id for chunk, _ in index.search(query, top_k=top_k)]


@dataclass(frozen=True)
class Score:
    recall: float
    precision: float
    found: int
    gold: int
    pulled: int


def measure(index: Index, cases: tuple[Case, ...], top_k: int) -> Score:
    found = gold = pulled = right = 0
    for case in cases:
        docs = hit_docs(index, case.query, top_k)
        gold += len(case.gold)
        pulled += len(docs)
        found += len(set(docs) & set(case.gold))
        right += sum(1 for doc in docs if doc in case.gold)
    return Score(
        recall=round(found / gold, 3) if gold else 0.0,
        precision=round(right / pulled, 3) if pulled else 0.0,
        found=found,
        gold=gold,
        pulled=pulled,
    )


@dataclass(frozen=True)
class Setting:
    """무엇을 바꿨는지 이름을 달아 둔다. 이름이 없으면 다음 주에 못 알아본다."""

    label: str
    size: int
    overlap: int
    top_k: int


LADDER: tuple[Setting, ...] = (
    Setting("기준선", 40, 10, 3),
    Setting("청크만 30으로", 30, 5, 3),
    Setting("거기서 top_k 만 5로", 30, 5, 5),
)


def run_ladder(ladder: tuple[Setting, ...] = LADDER) -> list[tuple[Setting, Score]]:
    """한 번에 하나씩만 바꿔 가며 잰다. 둘을 같이 바꾸면 어느 쪽이 움직였는지 못 본다."""
    out = []
    for step in ladder:
        index = build_index(step.size, step.overlap)
        out.append((step, measure(index, CASES, step.top_k)))
    return out
