"""되돌리기 비용을 못 박아 두는 테스트."""

from g14.undo import DECISIONS, cheap_first, undo_cost


def test_changing_top_k_rebuilds_nothing():
    top_k = DECISIONS[0]
    assert undo_cost(top_k) == 0


def test_touching_the_chunk_rule_rebuilds_everything():
    for decision in DECISIONS[1:]:
        assert undo_cost(decision) == 210


def test_cheap_decisions_come_first():
    costs = [cost for _, cost in cheap_first()]
    assert costs == sorted(costs)
    assert costs[0] == 0
