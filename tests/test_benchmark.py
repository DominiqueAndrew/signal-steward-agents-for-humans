from benchmarks.generate import fixture_hash, generate_holdout
from benchmarks.run import run


def test_holdout_is_versioned_and_has_five_families() -> None:
    histories = generate_holdout()
    assert len(histories) == 60
    assert {history.category for history in histories} == {
        "deterministic",
        "flaky",
        "infrastructure",
        "cancelled",
        "mixed",
    }
    assert len(fixture_hash(histories)) == 64


def test_holdout_replay_hits_pre_registered_targets() -> None:
    result = run()
    assert result["histories"] == 60
    assert result["failure_cases"] == []
    assert result["macro_f1"] >= 0.85
    assert result["culprit_top1"] >= 0.70
    assert result["false_escalation_rate"] <= 0.10
    assert result["review_item_reduction"] >= 0.50

