from pathlib import Path

import pytest

from signal_steward.server import AppState
from signal_steward.server import create_server


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "ci_replay.json"


def test_local_demo_payload_and_audit_boundary() -> None:
    state = AppState(FIXTURE)
    try:
        payload = state.payload()
        assert payload["mode"] == "local replay / read-only analysis"
        assert payload["observed_runs"] == 9
        assert len(payload["review_queue"]) == 3
        assert payload["audit_events"] == []
        assert payload["agent_contract"]["sdk_version"] == "1.53.0"
        assert payload["agent_contract"]["tools"] == [
            "inspect_window",
            "explain_signal",
            "prepare_review_packet",
        ]
        assert payload["agent_contract"]["side_effects"] == []

        item_id = payload["review_queue"][0]["item_id"]
        updated = state.record_decision(item_id, "hold", "need one more same-SHA run")
        assert len(updated["audit_events"]) == 1
        assert updated["audit_events"][0]["subject_id"] == item_id
        assert updated["audit_events"][0]["decision"] == "hold"
    finally:
        state.close()


def test_server_rejects_non_loopback_binding() -> None:
    with pytest.raises(ValueError, match="bind to loopback"):
        create_server("0.0.0.0", 8810, FIXTURE)
