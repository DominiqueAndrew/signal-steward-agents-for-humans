import json

import pytest

from signal_steward.ingest import load_bundle
from signal_steward.store import EvidenceStore


def test_store_is_idempotent_for_the_same_evidence() -> None:
    bundle = load_bundle("fixtures/ci_replay.json")
    store = EvidenceStore()
    try:
        store.write_bundle(bundle)
        store.write_bundle(bundle)
        count = store.connection.execute("SELECT COUNT(*) FROM job_attempts").fetchone()[0]
        assert count == len(bundle.attempts)
    finally:
        store.close()


def test_store_rejects_changed_evidence(tmp_path) -> None:
    source = json.loads(open("fixtures/ci_replay.json", encoding="utf-8").read())
    source["runs"][0]["jobs"][0]["log_excerpt"] = "tampered"
    path = tmp_path / "tampered.json"
    path.write_text(json.dumps(source), encoding="utf-8")
    original = load_bundle("fixtures/ci_replay.json")
    tampered = load_bundle(path)
    store = EvidenceStore()
    try:
        store.write_bundle(original)
        with pytest.raises(ValueError, match="immutable evidence conflict"):
            store.write_bundle(tampered)
    finally:
        store.close()

