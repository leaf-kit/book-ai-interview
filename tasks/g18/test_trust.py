"""등급이 자리에 따라 달라진다는 것을 못 박아 두는 테스트."""

from g18.demo_trust import BUILDER, FINDINGS, OPERATOR
from g18.trust import GRADES, Finding, grade_for, missing_lenses, why


def test_the_same_record_gives_two_different_grades():
    """사람 옆에 등급 하나만 적으면 안 되는 이유가 이것이다."""
    assert grade_for(FINDINGS, BUILDER).name == "바로 맡김"
    assert grade_for(FINDINGS, OPERATOR).name == "붙여서 맡김"


def test_a_missing_lens_adds_six_weeks_of_pairing():
    builder = grade_for(FINDINGS, BUILDER)
    operator = grade_for(FINDINGS, OPERATOR)
    assert operator.pairing_weeks - builder.pairing_weeks == 6


def test_two_missing_lenses_mean_look_again():
    thin = tuple(
        Finding(f.lens, f.lens in ("기초", "사람"), f.note) for f in FINDINGS
    )
    assert grade_for(thin, OPERATOR).name == "다시 보기"
    assert len(missing_lenses(thin, OPERATOR)) == 4


def test_every_grade_carries_an_onboarding_amount():
    for grade in GRADES:
        assert grade.review


def test_the_reason_names_the_missing_lens():
    assert "운영" in why(FINDINGS, OPERATOR)
    assert "다 확인됐다" in why(FINDINGS, BUILDER)
