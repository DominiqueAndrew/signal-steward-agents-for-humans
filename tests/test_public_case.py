from signal_steward.classifier import classify_jobs
from signal_steward.ingest import load_bundle
from signal_steward.models import Classification


def test_public_case_preserves_same_sha_recovery_signal() -> None:
    bundle = load_bundle("fixtures/public/maka-issue-2221.json")

    signals = classify_jobs(bundle.attempts)

    assert len(signals) == 1
    signal = signals[0]
    assert signal.job_key == "test_workspaces / [cli]"
    assert signal.runs_analyzed == 2
    assert signal.failure_rate == 0.5
    assert signal.same_sha_groups == 1
    assert signal.recovery_groups == 1
    assert signal.classification == Classification.FLAKY
