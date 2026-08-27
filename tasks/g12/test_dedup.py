from g12.dedup import dedup_by_title, dedup_keep_newest
from g12.retrieve import Chunk

TITLES = {"v1": "환불 정책", "v2": "환불 정책", "ship": "배송 안내"}
UPDATED = {"v1": "2024-03-02", "v2": "2025-11-19", "ship": "2025-01-08"}

ORDER = [
    Chunk("v1", 0, "결제일 기준 7일 이내"),
    Chunk("v2", 0, "결제일 기준 14일 이내"),
    Chunk("ship", 0, "영업일 기준 이틀"),
]


def ids(chunks):
    return [c.doc_id for c in chunks]


def test_draft_keeps_whichever_came_first():
    assert ids(dedup_by_title(ORDER, TITLES)) == ["v1", "ship"]


def test_newest_version_survives():
    assert ids(dedup_keep_newest(ORDER, TITLES, UPDATED)) == ["v2", "ship"]


def test_reordering_the_input_changes_the_draft():
    flipped = [ORDER[1], ORDER[0], ORDER[2]]
    assert ids(dedup_by_title(flipped, TITLES)) == ["v2", "ship"]
    assert ids(dedup_keep_newest(flipped, TITLES, UPDATED)) == ["v2", "ship"]


def test_missing_dates_fall_back_to_input_order():
    assert ids(dedup_keep_newest(ORDER, TITLES, {})) == ["v1", "ship"]
