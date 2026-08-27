from signal_steward.classifier import classify_jobs
from signal_steward.ingest import load_bundle
from signal_steward.models import Classification


def test_replay_classifies_flaky_broken_and_clean_jobs() -> None:
    bundle = load_bundle("fixtures/ci_replay.json")
    signals = {signal.job_key: signal for signal in classify_jobs(bundle.attempts)}

    assert signals["CI / integration"].classification == Classification.FLAKY
    assert signals["CI / integration"].recovery_groups == 1
    assert signals["CI / unit"].classification == Classification.CONSISTENTLY_BROKEN
    assert signals["CI / lint"].classification == Classification.CLEAN
    assert signals["CI / e2e"].classification == Classification.CLEAN
    assert signals["CI / e2e"].cancelled_count == 1


def test_cancellations_do_not_change_failure_rate() -> None:
    bundle = load_bundle("fixtures/ci_replay.json")
    signal = next(item for item in classify_jobs(bundle.attempts) if item.job_key == "CI / integration")
    assert signal.failure_rate == 1 / 3
    assert signal.runs_analyzed == 3

