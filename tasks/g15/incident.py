"""틀린 답이 나간 뒤에 세는 것.

먼저 세고 그다음에 고친다. 순서를 바꾸면 몇 명이 봤는지 영영 모른다.
로그를 지우고 고치면 그날 일이 통째로 없어진다.
"""

from __future__ import annotations

from dataclasses import dataclass

from g15.traffic import TODAY, YESTERDAY, Record


@dataclass(frozen=True)
class Blast:
    bad_doc: str
    served: int        # 그 문서를 맨 위로 내준 질의 건수
    of_total: int
    days: tuple[str, ...]


def blast_radius(bad_doc: str) -> Blast:
    """틀린 문서 하나가 몇 건에 닿았는지 센다. 되돌리기 전에 세는 숫자다."""
    records: tuple[Record, ...] = YESTERDAY + TODAY
    touched = [r for r in records if r.top_doc == bad_doc]
    return Blast(
        bad_doc=bad_doc,
        served=len(touched),
        of_total=len(records),
        days=tuple(sorted({r.day for r in touched})),
    )


STEPS: tuple[str, ...] = (
    "몇 건에 나갔는지 센다",
    "캐시를 비운다. 안 비우면 고쳐도 옛 답이 계속 나간다",
    "그 문서를 색인에서 뺀다",
    "센 건수를 그대로 적어 남긴다",
    "왜 안 걸렸는지 볼 자리를 하나 정한다",
)


def undo_before_fix(steps: tuple[str, ...] = STEPS) -> bool:
    """세는 일이 고치는 일보다 앞에 있는가."""
    return steps.index("몇 건에 나갔는지 센다") == 0
