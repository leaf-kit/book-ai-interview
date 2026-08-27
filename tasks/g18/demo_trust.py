"""등급 판정과 질문 은행의 상태를 그대로 찍는다.

관문 18에서 지원자에게 보여 주는 표가 이 출력이다.
같은 사람인데 자리가 바뀌면 등급도 바뀐다는 것이 앞부분의 요지다.
"""

from __future__ import annotations

from g18.bank import Bank
from g18.trust import Finding, grade_for, missing_lenses, why

FINDINGS: tuple[Finding, ...] = (
    Finding("기초", True, "조각 수를 값으로 댔다"),
    Finding("만들기", True, "첫 3분에 손댈 자리를 짚었다"),
    Finding("평가", True, "기준선 0.83을 댔다"),
    Finding("판단", True, "되돌린 값을 조각 수로 댔다"),
    Finding("운영", False, "배포 뒤에 본 숫자를 못 댔다"),
    Finding("사람", True, "모르는 자리를 하나 댔다"),
)

BUILDER = ("기초", "만들기", "평가", "판단")
OPERATOR = ("기초", "만들기", "평가", "판단", "운영")


def run() -> list[str]:
    out = ["같은 면접 기록, 두 자리"]
    for label, needed in (("만드는 자리", BUILDER), ("운영까지 맡는 자리", OPERATOR)):
        grade = grade_for(FINDINGS, needed)
        gaps = missing_lenses(FINDINGS, needed)
        out.append(
            f"  {label:<12s} {grade.name}  붙는 기간 {grade.pairing_weeks}주"
            f"  빠진 렌즈 {len(gaps)}"
        )
        out.append(f"      {why(FINDINGS, needed)}")
        out.append(f"      {grade.review}")

    bank = Bank()
    anchored = bank.add("retrieve.py 를 열어 두고, 여기서 단계가 몇 개예요")
    generic = bank.add("임베딩이 무엇인가요", anchored=False)
    for _ in range(4):
        anchored.use()
        generic.use()
    anchored.mark_leaked()
    generic.mark_leaked()

    out.append("")
    out.append("질문 은행, 둘 다 네 번 쓰고 둘 다 유출됐을 때")
    out.append(f"  실물에 붙은 질문   {anchored.state}  쓴 횟수 {anchored.runs}")
    out.append(f"  교과서 질문        {generic.state}  쓴 횟수 {generic.runs}")
    out.append(f"  은행 상태 {bank.health()}")
    return out


if __name__ == "__main__":
    for line in run():
        print(line)
