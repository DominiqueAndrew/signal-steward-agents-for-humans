from signal_steward.agent import make_read_only_tools, read_only_tool_names
from signal_steward.ingest import load_bundle
from signal_steward.service import SignalSteward
from signal_steward.store import EvidenceStore


def test_replay_surfaces_only_two_human_review_items_and_no_audit_side_effect() -> None:
    bundle = load_bundle("fixtures/ci_replay.json")
    store = EvidenceStore()
    try:
        report = SignalSteward(store).analyze(bundle)
        assert {item.job_key for item in report.review_queue} == {"CI / integration", "CI / unit"}
        assert all(item.human_required for item in report.review_queue)
        assert store.audit_events() == []
    finally:
        store.close()


def test_human_decision_is_an_audit_event_only() -> None:
    bundle = load_bundle("fixtures/ci_replay.json")
    store = EvidenceStore()
    try:
        service = SignalSteward(store)
        report = service.analyze(bundle)
        event_id = service.record_human_decision(report.review_queue[0], "hold", "owner wants one more run")
        assert store.audit_events()[0]["event_id"] == event_id
        assert store.audit_events()[0]["decision"] == "hold"
    finally:
        store.close()


def test_strands_boundary_exposes_read_only_tools() -> None:
    bundle = load_bundle("fixtures/ci_replay.json")
    store = EvidenceStore()
    try:
        service = SignalSteward(store)
        service.analyze(bundle)
        tools = make_read_only_tools(service)
        names = tuple(getattr(tool, "tool_name", getattr(tool, "__name__", "")) for tool in tools)
        assert names == read_only_tool_names()
        assert not {"rerun_ci", "create_issue", "quarantine_test", "merge_pr"}.intersection(names)
    finally:
        store.close()

