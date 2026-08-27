"""어제와 오늘을 나란히 찍는다.

관문 15에서 지원자에게 보여 주는 표가 이 출력이다.
숫자 셋이 똑같은데 답이 바뀌어 있는 자리를 보여 주는 것이 목적이다.
"""

from __future__ import annotations

from g15.incident import blast_radius
from g15.traffic import TODAY, YESTERDAY
from g15.watch import answers_changed, look, same_numbers


def run() -> list[str]:
    before, after = look(YESTERDAY), look(TODAY)
    out = ["날짜  질의  빈 결과  캐시   맨 위 쏠림"]
    for view in (before, after):
        out.append(
            f"{view.day}  {view.queries:<4d}  {view.empty_rate:<7}"
            f"  {view.cache_rate:<5}  {view.top_doc_share}"
        )
    out.append(f"질의, 빈 결과, 캐시가 어제와 같은가: {same_numbers(before, after)}")
    out.append("")
    out.append("같은 질의인데 맨 위 문서가 바뀐 것")
    for query, old, new in answers_changed():
        out.append(f"  {query}  {old} -> {new}")
    out.append("")
    blast = blast_radius("refund-2025")
    out.append(
        f"그 문서가 틀렸다면 닿은 건수 {blast.served}/{blast.of_total}"
        f" ({', '.join(blast.days)})"
    )
    return out


if __name__ == "__main__":
    for line in run():
        print(line)
