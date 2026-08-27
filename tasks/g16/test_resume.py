"""이력서 한 줄에서 질문이 나오는지를 못 박아 두는 테스트."""

from g16.demo_resume import RESUME
from g16.resume import questions_for, sheet, total_questions


def test_a_line_with_a_number_needs_no_number_question():
    asks = questions_for("검색 정확도를 0.58에서 0.71로 개선")
    assert asks == []


def test_a_vague_verb_pulls_the_mine_or_ours_question():
    asks = questions_for("사내 문서 검색 서비스 개발 담당")
    assert "그중에 직접 하신 건 어디까지예요" in asks


def test_a_list_of_names_pulls_the_which_one_question():
    asks = questions_for("Python, 웹 프레임워크, 관계형 DB, 캐시 활용")
    assert "이 중에 직접 고치신 게 있는 건 어느 거예요" in asks


def test_the_resume_never_gets_a_score():
    """이력서는 판정하는 물건이 아니다. 나오는 것은 질문뿐이다."""
    for _, asks in sheet(RESUME):
        assert all(isinstance(a, str) for a in asks)
    assert total_questions(RESUME) == 6


def test_demo_output_file_matches_the_real_run():
    from pathlib import Path

    from g16.demo_resume import run

    out = Path(__file__).with_name("demo_resume.py.out")
    recorded = out.read_text(encoding="utf-8")
    assert recorded.splitlines() == run()
