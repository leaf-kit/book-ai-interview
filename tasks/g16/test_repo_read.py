"""저장소를 5분에 훑을 때 나오는 값을 못 박아 두는 테스트.

훑는 대상은 12장에서 완성한 꾸러미 하나다. 뒤에 다른 꾸러미가 붙어도 이 값은 안 변한다.
"""

from g16.repo_read import asserts_per_test_file, doc_rate, look, python_files


def test_the_target_is_one_finished_package():
    names = [p.name for p in python_files()]
    assert "retrieve.py" in names
    assert "__init__.py" not in names


def test_tests_exist_for_almost_every_code_file():
    view = look()
    assert (view.code_files, view.test_files) == (4, 3)


def test_asserts_are_counted_not_test_functions():
    """테스트 개수가 아니라 못 박은 개수를 센다. 함수 하나에 단언이 여럿일 수 있다."""
    view = look()
    assert view.asserts == 21
    assert asserts_per_test_file(view) == 7.0


def test_most_functions_carry_no_explanation():
    """설명이 붙은 함수가 절반이 안 된다. 이게 5분에 보이는 값이다."""
    assert doc_rate(look()) == 0.357


def test_a_defect_is_marked_as_deliberate():
    assert look().marked_defects == 1
