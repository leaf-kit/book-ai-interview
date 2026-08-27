"""규모를 열 배씩 키우며 센 것과 되돌리기 비용을 그대로 찍는다.

관문 14에서 지원자에게 보여 주는 표가 이 출력이다.
시간이 아니라 횟수라서 어디서 돌려도 같은 값이 나온다.
"""

from __future__ import annotations

from g14.scale import load_table
from g14.undo import cheap_first


def run() -> list[str]:
    out = ["문서    조각    질의 하나에 점수 매기는 조각    어휘"]
    for load in load_table():
        out.append(
            f"{load.docs:<6d}  {load.chunks:<6d}"
            f"  {load.scored_per_query:<24d}  {load.vocabulary}"
        )
    out.append("")
    out.append("되돌리려면 다시 만들 조각 (문서 50개 기준)")
    for decision, cost in cheap_first():
        out.append(f"  {decision.name:<22s} {cost}")
    return out


if __name__ == "__main__":
    for line in run():
        print(line)
