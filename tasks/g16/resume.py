"""이력서 한 줄에서 물을 것을 뽑는 자리.

점수를 매기지 않는다. 이력서는 판정하는 물건이 아니라 질문을 뽑는 재료다.
그래서 이 코드가 내놓는 것은 등급이 아니라 물어볼 문장이다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

NUMBER = re.compile(r"\d")
# 누가 했는지가 흐려지는 동사들. 잘못이 아니라 물어볼 자리 표시다.
VAGUE_VERB = re.compile(r"(담당|참여|기여|관여|진행|수행)")
# 이름만 늘어놓은 줄. 쉼표나 가운뎃점으로 셋 이상 이어지면 나열로 본다.
LISTY = re.compile(r"([A-Za-z가-힣]+(\s[A-Za-z가-힣]+)*\s*[,/]\s*){2,}")


@dataclass(frozen=True)
class Line:
    text: str


def questions_for(line: str) -> list[str]:
    """한 줄에서 나오는 질문들. 없으면 빈 목록이고, 그건 물을 게 없다는 뜻이다."""
    asks = []
    if not NUMBER.search(line):
        asks.append("그게 얼마나였는지 숫자로 하나만 말씀해 주시겠어요")
    if VAGUE_VERB.search(line):
        asks.append("그중에 직접 하신 건 어디까지예요")
    if LISTY.search(line):
        asks.append("이 중에 직접 고치신 게 있는 건 어느 거예요")
    return asks


def sheet(lines: tuple[str, ...]) -> list[tuple[str, list[str]]]:
    """이력서 전체에서 질문지를 만든다. 줄 순서를 그대로 둔다."""
    return [(line, questions_for(line)) for line in lines]


def total_questions(lines: tuple[str, ...]) -> int:
    return sum(len(asks) for _, asks in sheet(lines))
