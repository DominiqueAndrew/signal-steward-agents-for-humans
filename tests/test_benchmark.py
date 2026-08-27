from math import inf, nan

import pytest

from benchmarks.generate import fixture_hash, generate_holdout
from benchmarks.run import SENSITIVITY_GRID, run, run_negative_control, run_sensitivity, wilson_interval


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
    assert result["culprit_hits"] == result["culprit_eligible"] == 24
    assert result["culprit_top1_wilson_95_ci"] == [0.862, 1.0]
    assert result["false_escalation_count"] == 0
    assert result["false_escalation_trials"] == 24
    assert result["false_escalation_rate_wilson_95_ci"] == [0.0, 0.138]


def test_negative_control_does_not_surface_weak_culprit() -> None:
    result = run_negative_control()
    assert result["classification"] == "CONSISTENTLY_BROKEN"
    assert result["top_hypothesis_score"] < 0.70
    assert result["review_action"] == "insufficient_evidence"
    assert result["surfaced_hypothesis"] is False
    assert result["passes_safety_gate"] is True


def test_wilson_interval_matches_the_score_formula_for_interior_counts() -> None:
    assert wilson_interval(12, 24) == (0.3143, 0.6857)
    assert wilson_interval(12, 24, z=1.0) == (0.4, 0.6)


@pytest.mark.parametrize("successes,trials", [(25, 24), (1.5, 2), (True, 2), (1, True)])
def test_wilson_interval_rejects_non_binomial_counts(successes: object, trials: object) -> None:
    with pytest.raises(ValueError):
        wilson_interval(successes, trials)  # type: ignore[arg-type]


@pytest.mark.parametrize("z", [0, -1, inf, nan, True])
def test_wilson_interval_rejects_non_positive_or_non_finite_z(z: object) -> None:
    with pytest.raises(ValueError):
        wilson_interval(1, 2, z=z)  # type: ignore[arg-type]


def test_wilson_interval_is_stable_at_extremes() -> None:
    assert wilson_interval(24, 24) == (0.862, 1.0)
    assert wilson_interval(0, 24) == (0.0, 0.138)


def test_threshold_sensitivity_uses_the_predeclared_grid() -> None:
    result = run_sensitivity()

    assert result["fixture_sha256"] == "641f380ecab3b6d40b2fffd5460a636186fb314ba9c7eef8df36e339241a3df2"
    assert len(result["grid"]) == len(SENSITIVITY_GRID) == 9
    assert {(cell["flaky_threshold"], cell["broken_threshold"]) for cell in result["grid"]} == set(SENSITIVITY_GRID)
    assert all("macro_f1" in cell and "false_escalation_rate" in cell for cell in result["grid"])
    assert all(cell["culprit_hits"] == cell["culprit_eligible"] == 24 for cell in result["grid"])
    assert all(cell["culprit_top1_wilson_95_ci"] == [0.862, 1.0] for cell in result["grid"])
    assert all(cell["false_escalation_count"] == 0 for cell in result["grid"])
    assert all(cell["false_escalation_trials"] == 24 for cell in result["grid"])
    assert all(cell["false_escalation_rate_wilson_95_ci"] == [0.0, 0.138] for cell in result["grid"])
