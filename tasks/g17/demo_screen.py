"""질문을 다시 쓴 결과와 서류 순위를 그대로 찍는다.

관문 17에서 지원자에게 보여 주는 표가 이 출력이다.
순위 아래에 되살린 건수가 붙어 있는 것이 이 표의 요지다.
"""

from __future__ import annotations

from g17.hardening import BANK, before_after, leaks
from g17.screen import APPS, Screening


def run() -> list[str]:
    before, after = before_after()
    out = [
        f"질문 {len(BANK)}개를 다시 썼습니다",
        f"  실물에 붙은 질문  다시 쓰기 전 {before}  다시 쓴 뒤 {after}",
        f"  다시 썼는데도 검색되는 질문 {len(leaks())}",
        "",
    ]
    for pair in BANK:
        out.append(f"  전  {pair.before.text}")
        out.append(f"  후  {pair.after.text}")
    out.append("")

    screening = Screening(cut=2)
    out.append(f"도구가 매긴 순위 (컷 {screening.cut})")
    for place, app in enumerate(screening.rank(APPS), 1):
        mark = "위" if place <= screening.cut else "아래"
        out.append(f"  {place}. {app.label}  물을 것 {-screening.score(app)}개  [{mark}]")

    below = [a.label for a in screening.below_cut(APPS)]
    out.append(f"컷 아래 {len(below)}명 ({', '.join(below)}) 을 사람이 읽습니다")
    out.append(f"되살린 사람 {len(screening.revived)}명, 검증했는가: {screening.audited()}")
    screening.revive("다")
    out.append(f"다를 읽고 되살렸습니다. 검증했는가: {screening.audited()}")
    return out


if __name__ == "__main__":
    for line in run():
        print(line)
