"""규모를 키웠을 때 무엇이 늘고 무엇이 안 느는지를 못 박아 두는 테스트."""

from g14.scale import LADDER, load_table, measure_load


def test_chunks_grow_with_documents():
    small, big = measure_load(1), measure_load(10)
    assert big.docs == small.docs * 10
    assert big.chunks == small.chunks * 10


def test_every_chunk_is_scored_on_every_query():
    """거르는 단계가 없어서 조각 수가 곧 질의 하나의 비용이다."""
    load = measure_load(10)
    assert load.scored_per_query == load.chunks


def test_vocabulary_does_not_grow_with_copies():
    """같은 문서를 백 벌 넣어도 어휘는 안 는다. 먼저 버거워지는 쪽이 여기서 갈린다."""
    assert measure_load(1).vocabulary == measure_load(100).vocabulary == 120


def test_ladder_is_ten_times_each_step():
    for before, after in zip(LADDER, LADDER[1:]):
        assert after == before * 10


def test_demo_output_file_matches_the_real_run():
    from pathlib import Path

    from g14.demo_scale import run

    recorded = Path(__file__).with_name("demo_scale.py.out").read_text(encoding="utf-8")
    assert recorded.splitlines() == run()
