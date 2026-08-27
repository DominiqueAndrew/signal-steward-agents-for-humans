# Signal Steward — Devpost draft

**STATUS: DRAFT ONLY — NOT SUBMITTED**  
Prepared against the live Agents for Humans form refreshed 2026-08-27. The
participant must personally confirm eligibility, replace the bracketed fields,
and click the final Devpost action.

## Project fields

- **Name:** Signal Steward
- **Tagline:** A provenance-first CI evidence desk that turns noisy reruns into only the human decisions that remain.
- **Track:** Professional Agents
- **Built with:** Python, Strands Agents SDK 1.53.0, SQLite, GitHub Actions-shaped replay fixtures
- **Repository:** https://github.com/DominiqueAndrew/signal-steward-agents-for-humans
- **Architecture diagram:** `docs/architecture-diagram.png`
- **AWS Builder ID:** `[participant enters privately in Devpost]`
- **Demo video:** `[participant adds public or unlisted YouTube/Vimeo URL]`
- **Live demo:** optional; leave blank unless a public deployment is actually available

## Description to paste

CI failures are not decisions. A maintainer still has to decide whether a red
job is a flaky test, a real regression, or simply too poorly evidenced to act
on—but the raw work of comparing reruns, SHAs, logs, and changed files is
repeated for every incident.

Signal Steward handles that repetitive evidence work in the background. It
replays a GitHub Actions-shaped window, validates and hashes the input, stores
immutable attempt and commit evidence, classifies job behavior from completed
outcomes and same-SHA recovery, and ranks a change hypothesis with supporting
and contradicting evidence. It then surfaces only three possible human review
packets: investigate a persistent regression, consider a flaky candidate, or
hold because the evidence is insufficient.

The important part is the stop condition. In the demo, an ambiguous runner
failure has no captured test output and no matching commit. Signal Steward does
not invent a culprit; it says `insufficient_evidence`. When a maintainer chooses
Approve or Hold, the application appends a local audit event. It cannot rerun
CI, open an issue, quarantine a test, edit a workflow, merge code, or access a
secret.

The deterministic safety layer is paired with a real Strands Agents SDK adapter
that exposes exactly three custom read-only tools:
`inspect_window`, `explain_signal`, and `prepare_review_packet`. The browser
makes that contract visible; the local replay does not require AWS credentials
or a model provider.

On a labelled synthetic holdout of 60 histories, the implementation recorded
macro-F1 1.00, seeded-culprit top-1 1.00, false escalation 0.00, and a 54.55%
reduction in review items versus the blind non-success baseline. A separate
negative control deliberately supplies a plausible vocabulary match without
head-SHA or retry support; the ranker keeps it internal at score 0.3375 and
the policy emits `insufficient_evidence`. These are reproducibility results on
synthetic data, not production-accuracy claims.

Run it locally:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest -q
.venv/bin/python -m signal_steward.server --port 8810
```

Then open http://127.0.0.1:8810 and follow [`docs/demo-script.md`](demo-script.md).
The research, assumptions, sources, benchmark design, and limitations are in
[`RESEARCH.md`](../RESEARCH.md) and [`RESULTS.md`](../RESULTS.md).

The current release evidence is collected in [`RELEASE_RECEIPT.md`](RELEASE_RECEIPT.md):
it records the reproducible checks, the local HTTP smoke, the loopback-only
binding, the 2 MiB fixture safety cap, and the fact that no submission or live
deployment is being claimed. The bounded trust and side-effect analysis is in
[`signal-steward-threat-model.md`](../signal-steward-threat-model.md).

## Rubric mapping

| Official criterion | Evidence to show | Honest framing |
| --- | --- | --- |
| Technological Implementation | `signal_steward/agent.py`, visible SDK contract, immutable store, deterministic classifier, benchmark commands, [`RELEASE_RECEIPT.md`](RELEASE_RECEIPT.md), and [`signal-steward-threat-model.md`](../signal-steward-threat-model.md) | Strands is a real adapter and its tools are read-only; the release receipt records the loopback and input-size boundaries; no live provider or AgentCore deployment is claimed. |
| Design | Minimal review queue, three distinct evidence states, responsive browser UI, hold/approve audit event | The interface is a decision desk, not a chat transcript or autonomous mutation console. |
| Potential Impact | Maintainer workflow, TUM industrial flaky-test evidence, `RESULTS.md` review-load measurement | The likely value is attention recovered in long/noisy CI workflows; production impact remains to be measured. |
| Creativity & Originality | Provenance packet + same-SHA recovery + hypothesis threshold + negative-control stop condition | The wedge is evidence quality and calibrated human gating, not “AI explains a build.” |
| Presentation | [`docs/demo-script.md`](demo-script.md), ≤5-minute sequence: noise → flaky → regression → insufficient evidence → human hold | The video should lead with the problem, show the working loop, and name the synthetic-data limitation. |

## Required form checklist

The current Devpost form also asks for submitter type, country of residence,
track, public repository URL, architecture upload, AWS Builder ID, and a video.
Website and zip are currently optional; the live demo URL is optional. Confirm
the form again before saving or submitting because its fields are organizer
controlled. The exact human steps are in [`HUMAN_GATE_PACKET.md`](HUMAN_GATE_PACKET.md).

## Source-backed claims

- Event constraints: [Agents for Humans official page](https://agentsforhumans.devpost.com/), [official rules](https://agentsforhumans.devpost.com/rules), and [Strands quickstart](https://strandsagents.com/docs/user-guide/quickstart/overview/).
- Industrial pain: [Cost of flaky tests in continuous integration: an industrial case study](https://portal.fis.tum.de/en/publications/cost-of-flaky-tests-in-continuous-integration-an-industrial-case-/).
- Culprit-finding precedent: [Google Flake Aware Culprit Finding](https://research.google/pubs/flake-aware-culprit-finding/).
- Full source map, uncertainty, equations, and reproducibility: [`RESEARCH.md`](../RESEARCH.md).
