import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.services.rule_engine import RuleEngine


def _finance(**overrides):
    base = {
        "pemasukan": 10_000_000,
        "makanan": 3_000_000,
        "transportasi": 1_000_000,
        "pendidikan": 500_000,
        "hiburan": 500_000,
        "lainnya": 500_000,
        "total_pengeluaran": 5_500_000,
        "saldo": 4_500_000,
        "target": 12_000_000,
        "deadline": 6,
    }
    base.update(overrides)
    return base


def test_healthy_finance_triggers_healthy_rule():
    engine = RuleEngine()
    result = engine.evaluate(_finance())
    names = {r["rule"] for r in result}
    assert "KEUANGAN_SEHAT" in names
    assert "DEFISIT" not in names


def test_deficit_is_detected():
    engine = RuleEngine()
    finance = _finance(total_pengeluaran=12_000_000, saldo=-2_000_000)
    names = {r["rule"] for r in engine.evaluate(finance)}
    assert "DEFISIT" in names
    assert "SALDO_RENDAH" in names


def test_excessive_entertainment_is_detected():
    engine = RuleEngine()
    finance = _finance(hiburan=3_000_000)  # 30% of income
    names = {r["rule"] for r in engine.evaluate(finance)}
    assert "HIBURAN_BERLEBIHAN" in names
