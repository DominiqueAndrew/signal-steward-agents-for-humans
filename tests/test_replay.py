import pytest

from signal_steward.agent import build_strands_agent, make_read_only_tools, read_only_tool_names
from signal_steward.ingest import load_bundle
from signal_steward.service import SignalSteward
from signal_steward.store import EvidenceStore


def test_replay_surfaces_only_actionable_human_review_items_and_no_audit_side_effect() -> None:
    bundle = load_bundle("fixtures/ci_replay.json")
    store = EvidenceStore()
    try:
        report = SignalSteward(store).analyze(bundle)
        assert {item.job_key for item in report.review_queue} == {
            "CI / ambiguous",
            "CI / integration",
            "CI / unit",
        }
        assert all(item.human_required for item in report.review_queue)
        ambiguous = next(item for item in report.review_queue if item.job_key == "CI / ambiguous")
        assert ambiguous.action.value == "insufficient_evidence"
        assert not any(line.startswith("top hypothesis") for line in ambiguous.evidence)
        assert store.audit_events() == []
    finally:
        store.close()


def test_human_decision_is_an_audit_event_only() -> None:
    bundle = load_bundle("fixtures/ci_replay.json")
    store = EvidenceStore()
    try:
        service = SignalSteward(store)
        report = service.analyze(bundle)
        event_id = service.record_human_decision(report.review_queue[0], "hold", "owner wants one more run", report.source_hash)
        assert store.audit_events()[0]["event_id"] == event_id
        assert store.audit_events()[0]["decision"] == "hold"
        assert store.audit_events()[0]["source_hash"] == report.source_hash

        with pytest.raises(ValueError, match="source_hash is required"):
            service.record_human_decision(report.review_queue[1], "hold", "missing provenance", "")
        assert len(store.audit_events()) == 1
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

        inspect_window, explain_signal, prepare_review_packet = tools
        assert inspect_window() == {"attempts": 9, "distinct_shas": 8, "read_only": True}
        explanation = explain_signal("CI / integration")
        assert len(explanation["attempts"]) == 3
        assert explanation["read_only"] is True
        packet = prepare_review_packet("CI / integration")
        assert packet["human_required"] is True
        assert packet["side_effects"] == []
        assert packet["read_only"] is True
        assert store.audit_events() == []
    finally:
        store.close()


def test_real_strands_agent_constructs_without_provider_invocation() -> None:
    bundle = load_bundle("fixtures/ci_replay.json")
    store = EvidenceStore()
    try:
        service = SignalSteward(store)
        service.analyze(bundle)
        agent = build_strands_agent(service)

        assert agent.tool_names == list(read_only_tool_names())
        assert store.audit_events() == []
    finally:
        store.close()
