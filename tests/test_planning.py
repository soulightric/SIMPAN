import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.services.planning_service import PlanningService


def test_plan_when_balance_is_enough():
    plan = PlanningService().create_plan({
        "target": 12_000_000,
        "deadline": 6,
        "saldo": 3_000_000,
    })
    assert plan["target_per_bulan"] == 2_000_000
    assert plan["cukup"] is True
    assert plan["kekurangan"] == 0


def test_plan_when_balance_is_short():
    plan = PlanningService().create_plan({
        "target": 12_000_000,
        "deadline": 6,
        "saldo": 500_000,
    })
    assert plan["cukup"] is False
    assert plan["kekurangan"] == 1_500_000


def test_zero_deadline_does_not_divide_by_zero():
    plan = PlanningService().create_plan({
        "target": 6_000_000,
        "deadline": 0,
        "saldo": 1_000_000,
    })
    assert plan["deadline"] == 1
    assert plan["target_per_bulan"] == 6_000_000
