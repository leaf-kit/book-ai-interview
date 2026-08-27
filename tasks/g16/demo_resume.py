"""저장소를 훑은 것과 이력서에서 뽑은 질문을 그대로 찍는다.

관문 16에서 지원자에게 보여 주는 표가 이 출력이다.
이력서에 점수가 안 붙고 질문만 붙는다는 것이 이 출력의 요지다.
"""

from __future__ import annotations

from g16.repo_read import asserts_per_test_file, doc_rate, look
from g16.resume import sheet

# 실물 이력서에서 자주 보는 네 줄을 본떠 지은 것이다.
# 도구 이름은 일부러 안 넣었다. 이름을 넣으면 몇 해 뒤에 이 줄이 통째로 낡는다.
RESUME: tuple[str, ...] = (
    "사내 문서 검색 서비스 개발 담당",
    "Python, 웹 프레임워크, 관계형 DB, 캐시 활용",
    "검색 정확도를 0.58에서 0.71로 개선",
    "검색 파이프라인 구축 및 성능 최적화 수행",
)


def run() -> list[str]:
    view = look()
    out = [
        f"코드 파일 {view.code_files}  테스트 파일 {view.test_files}"
        f"  코드 줄 {view.code_lines}",
        f"단언 {view.asserts}개, 테스트 파일당 {asserts_per_test_file(view)}",
        f"설명이 붙은 함수 {view.documented}/{view.documented + view.undocumented}"
        f" ({doc_rate(view)})",
        f"일부러 남겼다고 적어 둔 파일 {view.marked_defects}",
        "",
        "이력서에서 뽑은 질문",
    ]
    for line, asks in sheet(RESUME):
        out.append(f"  {line}")
        for ask in asks:
            out.append(f"    - {ask}")
        if not asks:
            out.append("    - 물을 것 없음")
    return out


if __name__ == "__main__":
    for line in run():
        print(line)
