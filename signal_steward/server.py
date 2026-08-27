from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .agent import read_only_contract
from .ingest import load_bundle
from .service import AnalysisReport, SignalSteward
from .store import EvidenceStore


DEFAULT_FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "ci_replay.json"
STATIC_INDEX = Path(__file__).resolve().parents[1] / "static" / "index.html"
LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}


class AppState:
    """One local replay and its append-only human decision ledger."""

    def __init__(self, fixture: Path) -> None:
        self.store = EvidenceStore()
        self.service = SignalSteward(self.store)
        self.bundle = load_bundle(fixture)
        self.report: AnalysisReport = self.service.analyze(self.bundle)

    def payload(self) -> dict[str, Any]:
        payload = self.report.to_dict()
        payload.update(
            {
                "observed_runs": len({attempt.run_id for attempt in self.bundle.attempts}),
                "observed_jobs": len(self.bundle.attempts),
                "audit_events": self.store.audit_events(),
                "mode": "local replay / read-only analysis",
                "agent_contract": read_only_contract(),
            }
        )
        return payload

    def record_decision(self, item_id: str, decision: str, rationale: str) -> dict[str, Any]:
        item = next((candidate for candidate in self.report.review_queue if candidate.item_id == item_id), None)
        if item is None:
            raise LookupError("review item not found")
        self.service.record_human_decision(item, decision, rationale)
        return self.payload()

    def close(self) -> None:
        self.store.close()


class SignalStewardHTTPServer(HTTPServer):
    def __init__(self, address: tuple[str, int], state: AppState) -> None:
        super().__init__(address, SignalStewardRequestHandler)
        self.state = state

    def server_close(self) -> None:
        self.state.close()
        super().server_close()


class SignalStewardRequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    @property
    def state(self) -> AppState:
        return self.server.state  # type: ignore[attr-defined]

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler hook
        path = urlsplit(self.path).path
        if path == "/health":
            self._send_json({"ok": True, "mode": self.state.payload()["mode"]})
            return
        if path == "/api/report":
            self._send_json(self.state.payload())
            return
        if path == "/favicon.ico":
            self._send_bytes(b"", "image/x-icon", status=204)
            return
        if path == "/":
            try:
                self._send_bytes(STATIC_INDEX.read_bytes(), "text/html; charset=utf-8")
            except OSError:
                self._send_json({"error": "static index unavailable"}, status=500)
            return
        self._send_json({"error": "not found"}, status=404)

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler hook
        if urlsplit(self.path).path != "/api/decisions":
            self._send_json({"error": "not found"}, status=404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 16_384:
                raise ValueError("request body must be between 1 and 16384 bytes")
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError("request body must be an object")
            item_id = data.get("item_id")
            decision = data.get("decision")
            rationale = data.get("rationale", "")
            if not isinstance(item_id, str) or not isinstance(decision, str) or not isinstance(rationale, str):
                raise ValueError("item_id, decision, and rationale must be strings")
            payload = self.state.record_decision(item_id, decision, rationale[:2_000])
        except (ValueError, json.JSONDecodeError, LookupError) as error:
            self._send_json({"error": str(error)}, status=400)
            return
        self._send_json(payload)

    def _send_json(self, value: object, *, status: int = 200) -> None:
        body = json.dumps(value, sort_keys=True).encode("utf-8")
        self._send_bytes(body, "application/json; charset=utf-8", status=status)

    def _send_bytes(self, body: bytes, content_type: str, *, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


def create_server(host: str = "127.0.0.1", port: int = 8810, fixture: Path = DEFAULT_FIXTURE) -> SignalStewardHTTPServer:
    if host not in LOOPBACK_HOSTS:
        raise ValueError("Signal Steward local server must bind to loopback")
    return SignalStewardHTTPServer((host, port), AppState(fixture))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Serve the credential-free Signal Steward local replay.")
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8810)
    args = parser.parse_args(argv)
    server = create_server(args.host, args.port, args.fixture)
    print(f"Signal Steward listening at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
