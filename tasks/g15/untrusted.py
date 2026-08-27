"""맥락에 들어가는 글이 어디서 왔는지 표시해 두는 자리.

문서 본문은 우리가 쓴 글이 아니다. 누가 올린 글이고, 그 안에 무엇이 적혀 있을지 모른다.
그래서 색인에 넣을 때 출처를 같이 달아 둔다. 달아 두면 나중에 셀 수 있다.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# 개인을 특정할 수 있는 모양. 문서에 이런 게 있으면 색인에 넣기 전에 가린다.
PERSONAL = (
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "메일 주소"),
    (re.compile(r"\b01\d-\d{3,4}-\d{4}\b"), "휴대폰 번호"),
    (re.compile(r"\b\d{6}-\d{7}\b"), "주민등록번호"),
)

# 본문에 섞여 들어오는 지시문. 지우지 않고 표시만 한다. 지우면 원본이 아니게 된다.
LOOKS_LIKE_ORDER = re.compile(r"(위 지시|앞의 지시|이전 지시).{0,6}(무시|잊)|시스템 프롬프트")


@dataclass(frozen=True)
class Source:
    doc_id: str
    origin: str  # "우리가 씀" 또는 "고객이 올림"
    text: str


def personal_hits(text: str) -> list[str]:
    return [label for pattern, label in PERSONAL if pattern.search(text)]


def redact(text: str) -> str:
    """가릴 것만 가리고 나머지는 그대로 둔다."""
    for pattern, _ in PERSONAL:
        text = pattern.sub("[가림]", text)
    return text


def order_like(text: str) -> bool:
    """지시문처럼 생겼는지만 본다. 생겼다고 해서 막지 않는다. 데이터로 다룰 뿐이다."""
    return bool(LOOKS_LIKE_ORDER.search(text))


def audit(sources: tuple[Source, ...]) -> dict[str, int]:
    """색인에 넣기 전에 세어 두는 표. 세어 두지 않으면 나중에 못 센다."""
    outside = [s for s in sources if s.origin != "우리가 씀"]
    return {
        "문서": len(sources),
        "우리가 안 쓴 문서": len(outside),
        "개인정보가 든 문서": sum(1 for s in sources if personal_hits(s.text)),
        "지시문처럼 생긴 문서": sum(1 for s in sources if order_like(s.text)),
    }
