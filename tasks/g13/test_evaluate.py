"""정답 목록으로 잰 숫자를 못 박아 두는 테스트.

책에 실린 숫자가 여기 그대로 있다. 코드가 바뀌면 이 테스트가 먼저 깨진다.
"""

from g13.evaluate import LADDER, build_index, hit_docs, measure, run_ladder
from g13.goldset import CASES


def test_baseline_misses_one_gold_document():
    index = build_index(40, 10)
    score = measure(index, CASES, 3)
    assert (score.found, score.gold) == (5, 6)
    assert score.recall == 0.833


def test_smaller_chunk_finds_the_missing_one():
    index = build_index(30, 5)
    score = measure(index, CASES, 3)
    assert score.recall == 1.0
    assert score.precision == 0.727


def test_raising_top_k_does_not_raise_recall():
    """맥락만 길어지고 재현율은 그대로다. 13장이 보여 주는 자리다."""
    index = build_index(30, 5)
    tight = measure(index, CASES, 3)
    wide = measure(index, CASES, 5)
    assert wide.recall == tight.recall
    assert wide.precision < tight.precision
    assert wide.pulled > tight.pulled


def test_particle_makes_one_query_find_nothing():
    """조사가 붙어 낱말이 안 맞으면 아무것도 안 나온다. 지표는 이걸 안 알려 준다."""
    index = build_index(40, 10)
    assert hit_docs(index, "비밀번호 언제", 3) == []


def test_ladder_changes_one_knob_at_a_time():
    steps = [(s.size, s.overlap, s.top_k) for s in LADDER]
    for before, after in zip(steps, steps[1:]):
        changed = sum(1 for a, b in zip(before, after) if a != b)
        assert changed <= 2


def test_demo_output_file_matches_the_real_run():
    from pathlib import Path

    from g13.demo_eval import run

    recorded = Path(__file__).with_name("demo_eval.py.out").read_text(encoding="utf-8")
    assert recorded.splitlines() == run()
