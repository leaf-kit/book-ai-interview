"""틀린 답이 나갔을 때 세는 순서를 못 박아 두는 테스트."""

from g15.incident import STEPS, blast_radius, undo_before_fix


def test_counting_comes_before_fixing():
    assert undo_before_fix()
    assert "캐시를 비운다" in STEPS[1]


def test_blast_radius_counts_both_days():
    blast = blast_radius("refund-2025")
    assert blast.served == 5
    assert blast.of_total == 16
    assert blast.days == ("어제", "오늘")


def test_a_document_that_stopped_appearing_still_counts():
    """오늘은 안 나오는 문서도 어제 나간 건수는 남아 있다."""
    blast = blast_radius("refund")
    assert blast.served == 3
    assert blast.days == ("어제",)
