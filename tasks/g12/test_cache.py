"""캐시의 지금 동작을 그대로 적어 둔 테스트.

마지막 테스트가 관문 12의 디버깅 과제다. 통과하는 테스트지만 옳은 동작은 아니다.
지금 무엇이 일어나는지를 못 박아 두는 것이 여기서 하는 일이다.
"""

from g12.cache import QueryCache, first_hit
from g12.retrieve import Index

POLICY = "환불 정책 결제일 기준 7일 이내 환불 가능 "
NOTICE = "환불 정책 개정 안내 결제일 기준 14일로 늘어납니다 "


def make_cache() -> QueryCache:
    index = Index()
    index.add_document("policy", POLICY * 6)
    return QueryCache(index=index)


def test_first_call_is_a_miss_and_second_is_a_hit():
    cache = make_cache()
    cache.search("환불")
    cache.search("환불")
    assert cache.log[0].startswith("cache miss")
    assert cache.log[1].startswith("cache hit")


def test_key_ignores_case_and_padding():
    cache = make_cache()
    cache.search("환불")
    cache.search("  환불  ")
    assert cache.log[1].startswith("cache hit")


def test_first_hit_returns_none_for_empty_result():
    assert first_hit([]) is None


def test_new_document_does_not_change_the_cached_answer():
    """과제. 문서를 넣어도 캐시가 그대로라 새 문서가 영영 안 나온다."""
    cache = make_cache()
    before = cache.search("환불")

    cache.add_document("notice", NOTICE * 6)
    after = cache.search("환불")

    assert before == after
    assert cache.log[-1].startswith("cache hit")
    assert "chunks=" in cache.log[-1]


def test_demo_output_file_matches_the_real_run():
    """본문에 실린 로그가 실제 출력과 같은지 대조한다."""
    from pathlib import Path

    from g12.demo_cache import run

    recorded = Path(__file__).with_name("demo_cache.py.out").read_text(encoding="utf-8")
    assert recorded.splitlines() == run()
