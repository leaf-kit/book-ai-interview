"""배포 뒤에 보는 숫자가 조용할 수 있다는 것을 못 박아 두는 테스트."""

from g15.traffic import TODAY, YESTERDAY
from g15.watch import answers_changed, look, same_numbers


def test_three_numbers_are_identical_across_the_two_days():
    assert same_numbers(look(YESTERDAY), look(TODAY))


def test_but_three_answers_changed():
    changed = answers_changed()
    assert len(changed) == 3
    assert all(query == "환불 며칠" for query, _, _ in changed)


def test_only_the_skew_moved():
    before, after = look(YESTERDAY), look(TODAY)
    assert before.top_doc_share == 0.5
    assert after.top_doc_share == 0.667


def test_empty_results_are_counted_not_hidden():
    """결과가 0건이던 질의도 세어 둔다. 안 세면 없던 일이 된다."""
    assert look(YESTERDAY).empty_rate == 0.25


def test_demo_output_file_matches_the_real_run():
    from pathlib import Path

    from g15.demo_watch import run

    recorded = Path(__file__).with_name("demo_watch.py.out").read_text(encoding="utf-8")
    assert recorded.splitlines() == run()
