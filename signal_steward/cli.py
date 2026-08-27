from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agent import read_only_contract
from .ingest import load_bundle
from .service import SignalSteward
from .store import EvidenceStore


DEFAULT_FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "ci_replay.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a credential-free Signal Steward replay.")
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--db", default=":memory:", help="SQLite evidence path; defaults to an ephemeral store")
    args = parser.parse_args(argv)

    bundle = load_bundle(args.fixture)
    store = EvidenceStore(args.db)
    try:
        report = SignalSteward(store).analyze(bundle)
        payload = report.to_dict()
        payload["agent_contract"] = read_only_contract()
        print(json.dumps(payload, indent=2, sort_keys=True))
    finally:
        store.close()
    return 0
