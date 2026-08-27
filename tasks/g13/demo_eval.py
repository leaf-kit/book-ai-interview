"""한 번에 하나씩만 바꿔 가며 잰 것을 그대로 찍는다.

관문 13에서 지원자에게 보여 주는 숫자가 이 출력이다.
바꾼 것이 하나씩이라서 어느 숫자가 어느 쪽으로 움직였는지가 보인다.
"""

from __future__ import annotations

from g13.evaluate import run_ladder
from g13.judge import agreement, disagreements


def run() -> list[str]:
    out = []
    for step, score in run_ladder():
        out.append(
            f"{step.label:20s} 재현율 {score.recall:.3f}  정밀도 {score.precision:.3f}"
            f"  건진 정답 {score.found}/{score.gold}  뽑아 온 조각 {score.pulled}"
        )
    out.append(f"규칙 심판과 사람이 맞은 비율 {agreement()}")
    for answer in disagreements():
        label = "사람은 맞다 규칙은 틀리다" if answer.human else "사람은 틀리다 규칙은 맞다"
        out.append(f"어긋남 {label} {answer.text[:22]}")
    return out


if __name__ == "__main__":
    for line in run():
        print(line)
