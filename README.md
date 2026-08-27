# Signal Steward

Signal Steward is a quiet, read-only CI failure desk for maintainers. It watches the repetitive part—comparing attempts, normalizing evidence, and ranking a change hypothesis—then surfaces only the human decisions that remain:

- “This looks intermittent; should we quarantine the candidate?”
- “This looks persistently broken; should we investigate the likely change?”
- “There is a failure, but is there enough evidence to act?”

It never reruns CI, edits workflows, opens issues, quarantines tests, merges code, or claims causal certainty. If the evidence is weak, it says `insufficient_evidence`.

## Run the credential-free demo

Requires Python 3.11+.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest
.venv/bin/python -m signal_steward
.venv/bin/python -m signal_steward.server --port 8810
# Open http://127.0.0.1:8810 in a browser
```

The replay uses only [`fixtures/ci_replay.json`](fixtures/ci_replay.json) and an ephemeral SQLite database. It produces a deterministic classification for `CI / integration` (flaky), `CI / unit` (consistently broken), `CI / lint` (clean), `CI / e2e` (no signal because the only run was cancelled), and `CI / ambiguous` (insufficient evidence). It surfaces three review packets and creates no audit event until a human explicitly records one. The browser run of show is [`docs/demo-script.md`](docs/demo-script.md).

## What is genuinely agentic

The core safety-critical classifications are deterministic and inspectable. The project also includes a real adapter built with the pinned [Strands Agents SDK](https://strandsagents.com/docs/user-guide/quickstart/overview/) 1.53.0. `signal_steward.agent.build_strands_agent()` registers three custom `@tool` functions documented by the [Strands custom-tools guide](https://strandsagents.com/docs/user-guide/concepts/tools/custom-tools/): `inspect_window`, `explain_signal`, and `prepare_review_packet`. Every registered tool is read-only; the browser and CLI expose this contract without invoking a model. Calling the Strands agent is optional and requires the model provider configured by the operator; the local replay does not call AWS or require credentials.

## Evidence model

For job `j`, `r_j = f_j / (f_j + s_j)` over completed failures and successes; cancelled/skipped outcomes are excluded. A job is a flaky candidate when `r_j >= 0.10` plus an intermittency signal (same-SHA recovery or both success and failure). It is consistently broken when `r_j >= 0.70` and no same-SHA retry succeeds. These are starting policy parameters, not universal constants. A culprit is a ranked hypothesis from current-head match, evidence vocabulary overlap, and recency; it is never presented as proof.

See [`RESEARCH.md`](RESEARCH.md) for the evidence-backed opportunity sprint, sources, assumptions, target metrics, limitations, and the falsifiable thesis. See [`docs/architecture.md`](docs/architecture.md) for the component and side-effect boundaries.
The first reproducible synthetic holdout and its honest interpretation are in [`RESULTS.md`](RESULTS.md).
The upload-ready architecture diagram is [`docs/architecture-diagram.png`](docs/architecture-diagram.png), and the remaining AWS, video, and Devpost human actions are in [`docs/HUMAN_GATE_PACKET.md`](docs/HUMAN_GATE_PACKET.md).
The exact credential-free release evidence is in [`docs/RELEASE_RECEIPT.md`](docs/RELEASE_RECEIPT.md).

## Agents for Humans fit

This is a Professional Agent: a maintainer’s repetitive, high-cost operational workflow runs in the background, while the accountable engineer retains the decisions that change repository state. The event’s official page is [agentsforhumans.devpost.com](https://agentsforhumans.devpost.com/). The repo is Apache-2.0 licensed and contains the source, synthetic fixtures, tests, and setup needed to reproduce the local slice.

## Current scope and honest limits

- The first slice is job-level, not per-test artifact analysis.
- GitHub integration is not enabled by default and has not been claimed as live.
- Synthetic fixtures demonstrate the control loop; they are not evidence of production accuracy.
- The benchmark targets in `RESEARCH.md` are acceptance thresholds, not measured results.
- No Devpost submission or AWS deployment is claimed by this repository.
