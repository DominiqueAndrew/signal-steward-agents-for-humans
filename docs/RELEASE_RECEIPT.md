# Signal Steward release receipt

**Scope:** credential-free local slice and submission materials  
**Validated tree:** `2ed600cccb5287948bf9e30763664557e070ea33`
**Public repository:** https://github.com/DominiqueAndrew/signal-steward-agents-for-humans  
**Validated:** 2026-08-27 (Europe/Paris)

## Verified

- `15 passed` from `.venv/bin/python -m pytest -q`, including the loopback
  binding, oversized-fixture, Wilson-interval, and provenance-boundary tests.
- `.venv/bin/python -m pip check` reports `No broken requirements found.`
- Main holdout: `holdout-2026-08-27.v1`, fixture SHA
  `641f380ecab3b6d40b2fffd5460a636186fb314ba9c7eef8df36e339241a3df2`, 60
  histories, macro-F1 `1.0`, culprit top-1 `1.0`, false escalation `0.0`,
  review reduction `0.5455`.
- Negative control: fixture SHA
  `8b429bd3e691ba08e14bb9aa58b6c614e639c65d3d260efaf045d4aa57332cd6`, weak
  hypothesis score `0.3375`, action `insufficient_evidence`, surfaced
  hypothesis `false`, safety gate `true`.
- CLI and browser expose Strands Agents SDK `1.53.0` with exactly three
  read-only tools: `inspect_window`, `explain_signal`, and
  `prepare_review_packet`; no side effects are registered.
- Browser checks show the real local service, three review items, the
  insufficient-evidence case, human hold → append-only audit event, zero
  console errors, and no horizontal overflow at 390, 768, 1366, 1440, 1920,
  and 2560 CSS-pixel widths.
- Upload-ready architecture diagram: `docs/architecture-diagram.png`, PNG
  2400×1350; source is `docs/architecture-diagram.svg`.
- `git diff --check` passes and the tracked tree contains no AWS access-key or
  private-key pattern.
- The local server rejects non-loopback binding, fixture ingest rejects inputs
  over 2 MiB, and the bounded threat model is recorded in
  [`signal-steward-threat-model.md`](../signal-steward-threat-model.md).
- Fresh HTTP smoke on the validated tree returned `/health` 200, `/api/report`
  200 with 9 runs, 9 jobs, 3 review items, 0 audit events, the three read-only
  Strands tools, and 404 for an unknown route.
- Human decisions are append-only local events bound to the analyzed replay
  source hash; the browser ledger shows the abbreviated evidence source.
- Fresh browser smoke at the validated tree recorded a human hold, showed
  `evidence source · 911795bffb45` in the ledger, reported zero console errors,
  and had `scrollWidth == innerWidth` at 390×844, 1440×900, and 2560×1440.
- The authorized local environment passed the bounded read-only AWS STS identity
  check (`aws sts get-caller-identity`); account and ARN output were deliberately
  not recorded.

## Human-gated / not claimed

- Participant confirms legal eligibility, country, submitter type, and any
  Devpost agreements.
- Participant creates or supplies their AWS Builder ID and decides whether an
  authorized AWS profile is available for optional live evidence.
- Participant records and publishes the ≤5-minute demo video URL.
- Participant reviews the form, uploads the diagram, enters the private
  Builder ID, and clicks the final Devpost **Submit** action.
- No live GitHub integration, AWS deployment, AgentCore deployment, model
  invocation, production accuracy, or Devpost submission status is claimed. The
  STS identity result proves credentials were available, not that the product
  was deployed or that a model was invoked.

## Reproduce

```sh
.venv/bin/python -m pytest -q
.venv/bin/python -m pip check
.venv/bin/python -m benchmarks.run
.venv/bin/python -m benchmarks.run --negative-control
.venv/bin/python -m signal_steward
.venv/bin/python -m signal_steward.server --port 8810
git diff --check
git grep -nE 'AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----|sk-[A-Za-z0-9]{20,}' -- ':!docs/HUMAN_GATE_PACKET.md'
```

The exact human handoff is [`HUMAN_GATE_PACKET.md`](HUMAN_GATE_PACKET.md).
