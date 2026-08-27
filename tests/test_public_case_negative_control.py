from signal_steward.ingest import load_bundle
from signal_steward.models import Classification, ReviewAction
from signal_steward.policy import build_review_queue
from signal_steward.service import SignalSteward
from signal_steward.store import EvidenceStore


def test_public_case_without_retry_or_commit_evidence_fails_closed() -> None:
    bundle = load_bundle("fixtures/public/kubernetes-issue-131150.json")
    store = EvidenceStore()
    try:
        report = SignalSteward(store).analyze(bundle)

        assert report.signals[0].classification == Classification.CONSISTENTLY_BROKEN
        assert report.hypotheses["canonical/k8s-snap / Conformance / scheduler"] == ()
        assert len(report.review_queue) == 1
        item = report.review_queue[0]
        assert item.action == ReviewAction.INSUFFICIENT_EVIDENCE
        assert not any(line.startswith("top hypothesis") for line in item.evidence)
        assert store.audit_events() == []
    finally:
        store.close()
