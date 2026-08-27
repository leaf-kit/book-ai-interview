"""경계를 어디에 긋든 지금은 결과가 같다는 것, 그리고 언제 갈리는지를 못 박는다."""

from g13.goldset import DOCS
from g14.boundary import (
    chunk_ids,
    index_by_kind,
    index_inside,
    index_outside,
    same_result,
)

KINDS = {
    doc_id: ("notice" if "개정" in text else "policy")
    for doc_id, text in DOCS.items()
}


def test_both_boundaries_give_the_same_index_today():
    assert same_result(index_inside(DOCS), index_outside(DOCS))


def test_per_kind_chunking_needs_the_outside_boundary():
    """종류마다 다르게 자르면 조각 수가 달라진다. 안쪽 경계로는 못 하는 일이다."""
    mixed = index_by_kind(DOCS, KINDS)
    assert len(chunk_ids(mixed)) != len(chunk_ids(index_inside(DOCS)))


def test_notice_documents_are_cut_into_fewer_pieces():
    mixed = index_by_kind(DOCS, KINDS)
    notice = [c for c in mixed.chunks if KINDS[c.doc_id] == "notice"]
    policy = [c for c in mixed.chunks if KINDS[c.doc_id] == "policy"]
    assert len(notice) < len(policy)
