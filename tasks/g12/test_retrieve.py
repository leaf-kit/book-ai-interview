import pytest

from g12.retrieve import Index, split, tokenize


def test_tokenize_splits_korean_and_english():
    assert tokenize("환불 정책 v2") == ["환불", "정책", "v2"]


def test_split_covers_the_whole_text():
    text = "가" * 300
    chunks = split("doc", text, size=120, overlap=20)
    joined = "".join(c.text for c in chunks)
    assert len(chunks) == 3
    assert set(joined) == {"가"}


def test_split_returns_nothing_for_blank_text():
    assert split("doc", "   \n  ") == []


@pytest.mark.parametrize("size,overlap", [(0, 0), (10, 10), (10, -1)])
def test_split_rejects_bad_windows(size, overlap):
    with pytest.raises(ValueError):
        split("doc", "본문", size=size, overlap=overlap)


def test_search_ranks_the_matching_chunk_first():
    index = Index()
    index.add_document("policy", "환불 정책 결제일 기준 7일 이내 환불 가능 " * 6)
    index.add_document("shipping", "배송 안내 영업일 기준 이틀 소요 " * 6)

    hits = index.search("환불", top_k=1)

    assert hits
    assert hits[0][0].doc_id == "policy"


def test_search_returns_empty_when_nothing_matches():
    index = Index()
    index.add_document("policy", "환불 정책")
    assert index.search("배송") == []


def test_top_k_zero_returns_empty():
    index = Index()
    index.add_document("policy", "환불 정책")
    assert index.search("환불", top_k=0) == []
