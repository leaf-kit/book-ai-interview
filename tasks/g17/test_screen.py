"""도구가 매긴 순위를 사람이 되짚었는지를 못 박아 두는 테스트."""

from g17.screen import APPS, Screening


def test_the_tool_ranks_by_how_little_is_left_to_ask():
    ranked = [a.label for a in Screening().rank(APPS)]
    assert ranked[0] == "가"


def test_two_fall_below_the_cut():
    below = [a.label for a in Screening(cut=2).below_cut(APPS)]
    assert sorted(below) == ["나", "다"]


def test_screening_is_unaudited_until_someone_reads_below_the_cut():
    screening = Screening(cut=2)
    assert not screening.audited()
    screening.revive("다")
    assert screening.audited()


def test_the_cut_rewards_resumes_that_already_answer_themselves():
    """숫자가 적힌 이력서가 위로 간다. 그건 글을 잘 쓴 순위에 가깝다."""
    screening = Screening()
    assert screening.score(APPS[0]) == 0
    assert screening.score(APPS[1]) < 0


def test_demo_output_file_matches_the_real_run():
    from pathlib import Path

    from g17.demo_screen import run

    out = Path(__file__).with_name("demo_screen.py.out")
    assert out.read_text(encoding="utf-8").splitlines() == run()
