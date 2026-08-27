"""규칙 심판과 사람이 어디서 어긋나는지를 못 박아 두는 테스트."""

from g13.judge import ANSWERS, agreement, disagreements, rule_score


def test_rule_and_human_agree_only_half_the_time():
    assert agreement() == 0.5


def test_long_and_wrong_answers_fool_the_rule():
    """길고 숫자가 있으면 규칙은 맞다고 본다. 사람은 틀렸다고 본 답들이다."""
    fooled = [a for a in disagreements() if a.human == 0]
    assert len(fooled) == 3
    assert all(rule_score(a.text) == 1 for a in fooled)


def test_short_and_right_answer_is_marked_wrong():
    short = [a for a in disagreements() if a.human == 1]
    assert len(short) == 1
    assert short[0].text == "사흘 안에 정하시면 됩니다."


def test_every_answer_has_a_human_label():
    assert all(a.human in (0, 1) for a in ANSWERS)
    assert sum(a.human for a in ANSWERS) == 4
