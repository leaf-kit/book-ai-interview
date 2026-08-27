"""질문이 준비로 채워지는지 재는 자리.

막는 코드가 아니다. 화면 너머에서 무엇을 보고 있는지는 잴 방법이 없다.
잴 수 있는 것은 이쪽이다. 이 질문이 우리 실물을 가리키고 있는가.

다시 쓰는 일은 사람이 한다. 코드는 다시 쓴 것이 실제로 실물에 붙었는지만 확인한다.
기계로 문장을 고치면 뜻이 망가지고, 망가진 질문은 면접장에서 못 쓴다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# 우리 실물을 가리키는 표시. 파일 이름, 우리가 잰 숫자, 우리가 찍어 둔 로그 줄.
ANCHOR = re.compile(r"(\.py\b|\.out\b|0\.\d\d|\d+개|\d+건|\d+줄|cache (hit|miss)|top_k)")
# 어느 회사에 갖다 놔도 말이 되는 질문. 검색하면 답이 나온다.
GENERIC = re.compile(r"(무엇인가요|무엇입니까|설명해 (주세요|보세요)|차이는|장단점|왜 쓰나요)")


@dataclass(frozen=True)
class Question:
    text: str

    @property
    def anchored(self) -> bool:
        """우리 실물을 가리키는가. 가리키면 밖에서 미리 못 만든다."""
        return bool(ANCHOR.search(self.text))

    @property
    def searchable(self) -> bool:
        return bool(GENERIC.search(self.text)) and not self.anchored


@dataclass(frozen=True)
class Pair:
    before: Question
    after: Question


# 왼쪽은 그대로 두면 준비로 채워지는 질문이고, 오른쪽은 저자가 손으로 다시 쓴 것이다.
BANK: tuple[Pair, ...] = (
    Pair(
        Question("검색 파이프라인의 구성 요소를 설명해 주세요"),
        Question("retrieve.py 를 열어 두고 여쭤볼게요. 여기서 단계가 몇 개예요"),
    ),
    Pair(
        Question("임베딩과 키워드 검색의 차이는 뭔가요"),
        Question("이 코드는 키워드로만 찾는데, 0.83이 1.0이 된 건 왜일까요"),
    ),
    Pair(
        Question("좋은 청크 크기는 무엇인가요"),
        Question("여기 겹침이 5인데 10으로 바꾸면 조각 210개가 어떻게 되죠"),
    ),
)


def leaks(bank: tuple[Pair, ...] = BANK) -> list[Question]:
    """다시 썼는데도 여전히 검색되는 질문. 하나라도 있으면 다시 쓴 것이 아니다."""
    return [pair.after for pair in bank if pair.after.searchable]


def unanchored(bank: tuple[Pair, ...] = BANK) -> list[Question]:
    """다시 썼는데 실물을 안 가리키는 질문."""
    return [pair.after for pair in bank if not pair.after.anchored]


def before_after(bank: tuple[Pair, ...] = BANK) -> tuple[int, int]:
    """다시 쓰기 전과 후에 실물에 붙은 질문이 각각 몇 개인가."""
    return (
        sum(1 for p in bank if p.before.anchored),
        sum(1 for p in bank if p.after.anchored),
    )
