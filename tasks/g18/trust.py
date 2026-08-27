"""합격을 등급으로 적는 자리.

느낌으로 정하면 사람마다 다르고, 사람마다 다르면 팀에서 못 쓴다.
그래서 렌즈마다 확인됐는지를 적고, 등급은 그 기록에서 나온다.
등급마다 붙는 온보딩의 양이 정해져 있다. 그게 등급을 쓰는 이유다.
"""

from __future__ import annotations

from dataclasses import dataclass

LENSES: tuple[str, ...] = ("기초", "만들기", "평가", "판단", "운영", "사람")


@dataclass(frozen=True)
class Finding:
    lens: str
    confirmed: bool
    note: str


@dataclass(frozen=True)
class Grade:
    name: str
    pairing_weeks: int
    review: str


GRADES: tuple[Grade, ...] = (
    Grade("다시 보기", 0, "다음 라운드에서 한 번 더 확인한다"),
    Grade("붙여서 맡김", 8, "첫 두 달은 나가는 것마다 같이 본다"),
    Grade("바로 맡김", 2, "첫 두 주만 같이 보고 그 뒤로는 평소대로 본다"),
)


def confirmed_lenses(findings: tuple[Finding, ...]) -> list[str]:
    return [f.lens for f in findings if f.confirmed]


def missing_lenses(findings: tuple[Finding, ...], needed: tuple[str, ...]) -> list[str]:
    """이 자리에 필요한 렌즈 중 확인이 안 된 것. 평균이 아니라 빠진 것을 센다."""
    seen = set(confirmed_lenses(findings))
    return [lens for lens in needed if lens not in seen]


def grade_for(findings: tuple[Finding, ...], needed: tuple[str, ...]) -> Grade:
    """빠진 렌즈 수로 등급이 정해진다. 평균을 내면 못 하는 자리가 가려진다."""
    gaps = len(missing_lenses(findings, needed))
    if gaps >= 2:
        return GRADES[0]
    if gaps == 1:
        return GRADES[1]
    return GRADES[2]


def why(findings: tuple[Finding, ...], needed: tuple[str, ...]) -> str:
    """등급 옆에 붙는 한 줄. 이게 없으면 반년 뒤에 아무도 이유를 모른다."""
    gaps = missing_lenses(findings, needed)
    if not gaps:
        return f"이 자리에 필요한 렌즈 {len(needed)}개가 다 확인됐다"
    return f"{', '.join(gaps)} 쪽이 확인 안 됐다"
