"""하루치 질의 기록. 배포한 뒤에 들여다보는 것이 이 기록이다.

실제 로그가 아니라 저자가 손으로 지은 것이다. 사람을 특정할 수 있는 것은 애초에 안 넣었다.
날짜가 이틀치인 이유는 어제와 오늘을 견주는 자리가 관문 15에 있기 때문이다.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Record:
    day: str
    query: str
    hits: int          # 뽑아 온 조각 수
    top_doc: str       # 맨 위 조각이 나온 문서. 없으면 빈 문자열
    cached: bool


YESTERDAY: tuple[Record, ...] = (
    Record("어제", "환불 며칠", 3, "refund", False),
    Record("어제", "환불 며칠", 3, "refund", True),
    Record("어제", "배송 얼마나", 3, "ship", False),
    Record("어제", "쿠폰 환불", 3, "coupon", False),
    Record("어제", "비밀번호 언제", 0, "", False),
    Record("어제", "환불 개정", 3, "refund-2025", False),
    Record("어제", "환불 며칠", 3, "refund", True),
    Record("어제", "탈퇴 어떻게", 0, "", False),
)

TODAY: tuple[Record, ...] = (
    Record("오늘", "환불 며칠", 3, "refund-2025", False),
    Record("오늘", "환불 며칠", 3, "refund-2025", True),
    Record("오늘", "배송 얼마나", 3, "ship", False),
    Record("오늘", "쿠폰 환불", 3, "coupon", False),
    Record("오늘", "비밀번호 언제", 0, "", False),
    Record("오늘", "환불 개정", 3, "refund-2025", False),
    Record("오늘", "환불 며칠", 3, "refund-2025", True),
    Record("오늘", "탈퇴 어떻게", 0, "", False),
)
