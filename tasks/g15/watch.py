"""배포한 뒤에 들여다보는 숫자들.

평균은 조용하다. 그래서 평균 말고 무엇을 봐야 하는지가 관문 15의 자리다.
아래 넷 중 셋은 어제와 오늘이 똑같고, 하나만 다르다.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from g15.traffic import TODAY, YESTERDAY, Record


@dataclass(frozen=True)
class DayView:
    day: str
    queries: int
    empty_rate: float      # 결과가 0건이던 비율
    cache_rate: float      # 캐시로 답한 비율
    top_doc_share: float   # 맨 위를 가장 많이 차지한 문서의 몫


def look(records: tuple[Record, ...]) -> DayView:
    total = len(records)
    empty = sum(1 for r in records if r.hits == 0)
    cached = sum(1 for r in records if r.cached)
    tops = Counter(r.top_doc for r in records if r.top_doc)
    share = tops.most_common(1)[0][1] / sum(tops.values()) if tops else 0.0
    return DayView(
        day=records[0].day,
        queries=total,
        empty_rate=round(empty / total, 3),
        cache_rate=round(cached / total, 3),
        top_doc_share=round(share, 3),
    )


def answers_changed(
    before: tuple[Record, ...] = YESTERDAY,
    after: tuple[Record, ...] = TODAY,
) -> list[tuple[str, str, str]]:
    """같은 질의에 맨 위 문서가 바뀐 것만 고른다. 지표가 아니라 답을 견주는 것이다."""
    changed = []
    for old, new in zip(before, after):
        if old.query == new.query and old.top_doc != new.top_doc:
            changed.append((old.query, old.top_doc, new.top_doc))
    return changed


def same_numbers(left: DayView, right: DayView) -> bool:
    """날짜만 빼고 숫자가 다 같은가."""
    return (left.queries, left.empty_rate, left.cache_rate) == (
        right.queries, right.empty_rate, right.cache_rate)
