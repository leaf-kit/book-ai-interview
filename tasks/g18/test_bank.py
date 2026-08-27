"""질문이 닳고 물러나는 규칙을 못 박아 두는 테스트."""

from g18.bank import MAIN, RETIRED, TRIAL, TRIAL_RUNS, WORN_OUT, Bank


def test_a_new_question_goes_to_trial_on_first_use():
    bank = Bank()
    q = bank.add("여기서 단계가 몇 개예요")
    q.use()
    assert q.state == TRIAL


def test_a_question_joins_the_main_bank_after_three_runs():
    bank = Bank()
    q = bank.add("여기서 단계가 몇 개예요")
    for _ in range(TRIAL_RUNS):
        q.use()
    assert q.state == MAIN


def test_a_worn_out_question_retires_by_itself():
    bank = Bank()
    q = bank.add("여기서 단계가 몇 개예요")
    for _ in range(WORN_OUT):
        q.use()
    assert q.state == RETIRED


def test_a_leaked_textbook_question_retires_at_once():
    bank = Bank()
    q = bank.add("임베딩이 무엇인가요", anchored=False)
    q.use()
    q.mark_leaked()
    assert q.state == RETIRED


def test_a_leaked_anchored_question_survives():
    """실물에 붙은 질문은 밖에 돌아다녀도 우리 저장소를 안 열면 못 답한다."""
    bank = Bank()
    q = bank.add("retrieve.py 를 열어 두고, 여기서 단계가 몇 개예요")
    q.use()
    q.mark_leaked()
    assert q.state != RETIRED


def test_health_counts_every_state():
    bank = Bank()
    bank.add("가")
    bank.add("나").use()
    assert bank.health()["새 질문"] == 1
    assert bank.health()["시험 중"] == 1


def test_demo_output_file_matches_the_real_run():
    from pathlib import Path

    from g18.demo_trust import run

    out = Path(__file__).with_name("demo_trust.py.out")
    assert out.read_text(encoding="utf-8").splitlines() == run()
