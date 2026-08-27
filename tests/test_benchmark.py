import pytest

from benchmarks.generate import fixture_hash, generate_holdout
from benchmarks.run import run, run_negative_control, wilson_interval


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


def test_negative_control_does_not_surface_weak_culprit() -> None:
    result = run_negative_control()
    assert result["classification"] == "CONSISTENTLY_BROKEN"
    assert result["top_hypothesis_score"] < 0.70
    assert result["review_action"] == "insufficient_evidence"
    assert result["surfaced_hypothesis"] is False
    assert result["passes_safety_gate"] is True


def test_wilson_interval_is_stable_at_extremes_and_rejects_invalid_counts() -> None:
    assert wilson_interval(24, 24) == (0.862, 1.0)
    assert wilson_interval(0, 24) == (0.0, 0.138)

    with pytest.raises(ValueError):
        wilson_interval(25, 24)
