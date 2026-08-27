"""다시 쓴 질문이 실제로 실물에 붙었는지를 못 박아 두는 테스트."""

from g17.hardening import BANK, Question, before_after, leaks, unanchored


def test_none_of_the_original_questions_touch_our_code():
    before, _ = before_after()
    assert before == 0


def test_every_rewritten_question_touches_our_code():
    _, after = before_after()
    assert after == len(BANK)
    assert unanchored() == []


def test_no_rewritten_question_is_still_searchable():
    assert leaks() == []


def test_a_question_naming_a_file_is_anchored():
    assert Question("retrieve.py 의 split 을 보세요").anchored


def test_a_question_naming_our_number_is_anchored():
    assert Question("0.83이 1.0이 된 건 왜일까요").anchored


def test_a_textbook_question_is_searchable():
    assert Question("임베딩이 무엇인가요").searchable
