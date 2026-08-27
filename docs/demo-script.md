# Signal Steward: four-minute demo

This is a credential-free, local replay. It uses the same service and evidence
store as the CLI; the browser can record only an append-only local human audit
event. It cannot rerun CI, open an issue, quarantine a test, or merge code.

## Start

From the repository root:

```sh
.venv/bin/python -m signal_steward.server --port 8810
open http://127.0.0.1:8810
```

If the optional Strands adapter is shown, explain that it exposes the same
three read-only tools; the local walkthrough does not require AWS credentials.

## Run of show (under five minutes)

| Time | Beat | What to show |
| --- | --- | --- |
| 0:00–0:25 | The cost of noise | “A failed CI run is not a decision.” Signal Steward replays the window in the background and leaves only three review items. |
| 0:25–1:20 | Intermittent signal | Open `CI / integration`. Point to the same-SHA recovery and the `QUARANTINE CANDIDATE` label. The system recommends; it does not disable the test. |
| 1:20–2:10 | Persistent signal | Open `CI / unit`. Point to the exact head SHA, cache vocabulary overlap, and the `INVESTIGATE REGRESSION` label. Say “hypothesis, not proof.” |
| 2:10–2:50 | The stop condition | Open `CI / ambiguous`. There is a failure, but no captured test output or matching commit, so the system refuses to invent a culprit and surfaces `INSUFFICIENT EVIDENCE`. |
| 2:50–3:35 | Human boundary | On `CI / integration`, choose `Hold for more evidence`, add a rationale, and record it. The card changes state and the ledger shows the decision. |
| 3:35–4:20 | Evidence, not theatre | Show `RESULTS.md`: holdout macro-F1 1.00, culprit top-1 1.00, false escalation 0.00, and 54.55% review reduction on the synthetic labelled fixture. Point out the uncertainty: 24/24 culprit hits have a Wilson 95% interval of `[0.862, 1.000]`, while 0/24 false escalations have `[0.000, 0.138]`; these are descriptive bounds on a fixed synthetic sample, not production accuracy or a proven safety target. Then flash [`PUBLIC_CASES.md`](PUBLIC_CASES.md): one public same-SHA retry maps to a flaky signal, while one public lone failure stays `INSUFFICIENT_EVIDENCE`. |
| 4:20–4:50 | Architecture and limits | Point to the visible Strands contract (version + optional provider-configured model → tools → reasoning → response loop + three read-only tools), then show `docs/architecture.md` and `RESEARCH.md`. Close with: “It prepares a review packet; a person still owns the consequential action.” |

## Reset between takes

Stop the server with `Ctrl-C` and restart it. The store is in-memory, so the
audit ledger resets without modifying a repository, CI system, or tracker.

## Evidence commands

```sh
.venv/bin/python -m pytest -q
.venv/bin/python -m pip check
.venv/bin/python -m signal_steward
```

The demo is intentionally local. A live GitHub/AWS connection, AWS Builder ID,
public demo recording, and any Devpost submission action remain human-owned
gates; see `README.md` for the exact handoff packet.

The evidence line to say aloud is: “A retry is evidence, not permission; a lone
failure is not enough to invent a culprit.”
