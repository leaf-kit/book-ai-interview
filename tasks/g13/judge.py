"""답변에 점수를 매기는 심판 둘.

하나는 사람이 붙인 점수고 하나는 규칙으로 매기는 점수다.
둘이 어디서 어긋나는지를 세는 것이 이 파일의 목적이다. 평균 점수가 아니라 어긋남을 센다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

DIGIT = re.compile(r"\d")


@dataclass(frozen=True)
class Answer:
    text: str
    human: int  # 사람이 붙인 점수. 0 이면 틀린 답, 1 이면 맞는 답


ANSWERS: tuple[Answer, ...] = (
    Answer("결제일 기준 7일 이내입니다.", 1),
    Answer("환불 정책은 여러 요소를 종합적으로 고려하여 결정되며 "
           "일반적으로 관련 규정에 따라 처리됩니다.", 0),
    Answer("14일입니다.", 1),
    Answer("배송은 영업일 기준 2일이 소요됩니다.", 1),
    Answer("쿠폰은 상황에 따라 다르게 적용될 수 있으며 "
           "자세한 내용은 정책 문서를 참고하시기 바랍니다.", 0),
    Answer("사흘 안에 정하시면 됩니다.", 1),
    Answer("해당 문의는 고객센터를 통해 안내받으실 수 있습니다.", 0),
    Answer("모릅니다.", 0),
)


def rule_score(text: str) -> int:
    """길고 숫자가 들어 있으면 잘 쓴 답으로 본다. 흔히 쓰는 어림 규칙이다."""
    long_enough = len(text) >= 20
    has_number = bool(DIGIT.search(text))
    return 1 if (long_enough or has_number) else 0


def disagreements(answers: tuple[Answer, ...] = ANSWERS) -> list[Answer]:
    return [a for a in answers if rule_score(a.text) != a.human]


def agreement(answers: tuple[Answer, ...] = ANSWERS) -> float:
    same = sum(1 for a in answers if rule_score(a.text) == a.human)
    return round(same / len(answers), 3)
