"""결정을 되돌리는 데 조각을 몇 개나 다시 만들어야 하는지를 센다.

되돌리기 비용을 시간이나 돈으로 적으면 환경마다 다르다.
다시 만들어야 하는 조각 수로 적으면 어디서 돌려도 같은 값이 나온다.
"""

from __future__ import annotations

from dataclasses import dataclass

from g14.scale import grow


@dataclass(frozen=True)
class Decision:
    name: str
    rebuilds_chunks: bool
    invalidates_cache: bool


DECISIONS: tuple[Decision, ...] = (
    Decision("top_k 를 3에서 5로", rebuilds_chunks=False, invalidates_cache=True),
    Decision("겹침을 5에서 10으로", rebuilds_chunks=True, invalidates_cache=True),
    Decision("청크를 30에서 40으로", rebuilds_chunks=True, invalidates_cache=True),
    Decision("낱말 자르는 규칙 교체", rebuilds_chunks=True, invalidates_cache=True),
)


def undo_cost(decision: Decision, times: int = 10) -> int:
    """되돌리려면 다시 만들어야 하는 조각 수. 안 만들어도 되면 0 이다."""
    if not decision.rebuilds_chunks:
        return 0
    return len(grow(times).chunks)


def cheap_first(times: int = 10) -> list[tuple[Decision, int]]:
    """싼 것부터 줄 세운다. 면접에서 물을 순서이기도 하다."""
    pairs = [(d, undo_cost(d, times)) for d in DECISIONS]
    return sorted(pairs, key=lambda pair: pair[1])
