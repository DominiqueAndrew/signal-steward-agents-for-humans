# Signal Steward release receipt

**Scope:** credential-free local slice and submission materials  
**Validated release-content tree:** `eb67ca002e7ec72ec2f9c2ba0a1eeeb38b73408a`
**Public repository:** https://github.com/DominiqueAndrew/signal-steward-agents-for-humans  
**Validated:** 2026-08-27 (Europe/Paris)

This receipt refresh records the exact public release-content SHA above. A
commit cannot contain its own hash, so the receipt-refresh commit must be
checked separately with the `git ls-remote` command below after this file is
published.

## Verified

- `30 passed` from `.venv/bin/python -m pytest -q`, including the loopback
  binding, oversized-fixture, Wilson-interval, provenance-boundary, offline
  Strands-construction, HTTP-contract, and public-incident sanity tests.
- Threshold sensitivity benchmark: `PYTHONPATH=. .venv/bin/python -m
  benchmarks.run --sensitivity`; all 9 predeclared cells returned macro-F1
  `1.000`, false-escalation rate `0.000`, and review-item reduction `0.5455`
  with `24/24` culprit hits and `0/24` false escalations, carrying Wilson
  95% intervals `[0.862, 1.000]` and `[0.000, 0.138]`, respectively, on
  fixture SHA-256
  `641f380ecab3b6d40b2fffd5460a636186fb314ba9c7eef8df36e339241a3df2`.
- `.venv/bin/python -m pip check` reports `No broken requirements found.`
- Main holdout: `holdout-2026-08-27.v1`, fixture SHA
  `641f380ecab3b6d40b2fffd5460a636186fb314ba9c7eef8df36e339241a3df2`, 60
  histories, macro-F1 `1.0`, culprit top-1 `1.0` (`24/24`, Wilson 95% CI
  `[0.862, 1.000]`), false escalation `0.0` (`0/24`, Wilson 95% CI
  `[0.000, 0.138]`), review reduction `0.5455`.
- Wilson uncertainty is computed from validated integer binomial counts using
  the score-test formula and propagated through every sensitivity cell. These
  intervals are descriptive under an iid Bernoulli approximation; the fixed,
  synthetic histories are not a random production sample and do not establish
  production accuracy or safety.
- Public incident sanity case: Apache Maka issue #2221, fixture SHA
  `635d77bdf0f82d8bb904811baaf8629c3236c95eb53c7569a4bdc5b27970b849`,
  classified `FLAKY` from `1/2` failures and `1/1` same-SHA recovery. This
  case is documented separately and is not mixed into headline metrics.
- Public negative control: Kubernetes issue #131150, fixture SHA
  `b974705ea60d3ff628c37b037e71d545eb78d2495c6e423ce920c6d074c6a92d`,
  emitted `INSUFFICIENT_EVIDENCE` with no surfaced hypothesis or audit event.
- Negative control: fixture SHA
  `8b429bd3e691ba08e14bb9aa58b6c614e639c65d3d260efaf045d4aa57332cd6`, weak
  hypothesis score `0.3375`, action `insufficient_evidence`, surfaced
  hypothesis `false`, safety gate `true`.
- CLI and browser expose Strands Agents SDK `1.53.0` with exactly three
  read-only tools: `inspect_window`, `explain_signal`, and
  `prepare_review_packet`; no side effects are registered.
- Offline construction of a real Strands `Agent` succeeds without provider
  invocation and exposes exactly those three tool names; no audit event is
  created by construction.
- Fixture-only invocation of all three decorated tools returned read-only
  window/evidence/packet data and left the audit ledger empty.
- Browser checks show the real local service, three review items, the
  insufficient-evidence case, human hold → append-only audit event, zero
  console errors, and no horizontal overflow at 390, 768, 1366, 1440, 1920,
  and 2560 CSS-pixel widths.
- Upload-ready architecture diagram: `docs/architecture-diagram.png`, PNG
  2400×1350; source is `docs/architecture-diagram.svg`.
- `git diff --check` passes and the tracked tree contains no AWS access-key or
  private-key pattern.
- A wheel built with `python -m pip wheel --no-deps .` installed into an
  isolated target and imported successfully outside the checkout.
- The local server rejects non-loopback binding, fixture ingest rejects inputs
  over 2 MiB, and the bounded threat model is recorded in
  [`signal-steward-threat-model.md`](../signal-steward-threat-model.md).
- Fresh HTTP smoke on the validated tree returned `/health` 200, `/api/report`
  200 with 9 runs, 9 jobs, 3 review items, 0 audit events, the three read-only
  Strands tools, and 404 for an unknown route.
- The loopback HTTP contract test recorded one valid hold bound to the report
  source hash, rejected an invalid `rerun` decision with HTTP 400, and left no
  extra audit event.
- Human decisions are append-only local events bound to the analyzed replay
  source hash; the browser ledger shows the abbreviated evidence source.
- Fresh browser smoke at the validated tree recorded a human hold, showed
  `evidence source · 911795bffb45` in the ledger, reported zero console errors,
  and had `scrollWidth == innerWidth` at 390×844, 768×900, 1366×900,
  1440×900, 1920×1080, and 2560×1440.
- The authorized local environment passed the bounded read-only AWS STS identity
  check (`aws sts get-caller-identity`); account and ARN output were deliberately
  not recorded.
- Public artifact gate at published remote `main` SHA
  `eb67ca002e7ec72ec2f9c2ba0a1eeeb38b73408a`: all 11
  GitHub document URLs and both architecture raw URLs returned HTTP 200. The
  PNG response was `image/png`, 337,684 bytes; the SVG response was
  `image/svg+xml`, 6,325 bytes. This was a certificate-verified, read-only
  HTTPS check; no login or Devpost action was performed.
- The canonical local gate `./scripts/verify-release.sh` passed from the
  repository root: 30 tests, clean dependencies, all three benchmark modes,
  `git diff --check`, and the secret-pattern scan.
- The same release gate was invoked by absolute path from `/tmp`; it entered
  its repository root before running tests and passed 30 tests, dependencies,
  all benchmark modes, the whitespace check, and the secret-pattern scan.
- Public [GitHub Actions run #50](https://github.com/DominiqueAndrew/signal-steward-agents-for-humans/actions/runs/33107233048)
  for commit `eb67ca002e7ec72ec2f9c2ba0a1eeeb38b73408a` completed with
  status `success` using `actions/checkout@v7`, `actions/setup-python@v7`,
  Python 3.11, dependency installation, the test suite, and CLI replay.
- Fresh public-clone gate: commit
  `eb67ca002e7ec72ec2f9c2ba0a1eeeb38b73408a` matched remote `main`; a new
  Python 3.11 venv installed `.[dev]`, then `./scripts/verify-release.sh`
  returned `30 passed`, `No broken requirements found`, all benchmark modes,
  clean diff, clean secret scan, and `release verification passed`.
- Public release SHA check: `git ls-remote origin refs/heads/main` returned
  `eb67ca002e7ec72ec2f9c2ba0a1eeeb38b73408a` at the time of the
  post-publication verification for the release-content tree. Repeat it after
  this receipt refresh and after any subsequent push; the resulting SHA is the
  public receipt-refresh commit, not the release-content SHA recorded above.

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

The single local release gate is:

```sh
./scripts/verify-release.sh
```

It runs the complete suite, dependency check, main/negative-control/threshold
sensitivity benchmarks, whitespace check, and secret-pattern scan. The
component commands below remain available for diagnosis:

```sh
.venv/bin/python -m pytest -q
.venv/bin/python -m pip check
.venv/bin/python -m benchmarks.run
.venv/bin/python -m benchmarks.run --sensitivity
.venv/bin/python -m benchmarks.run --negative-control
.venv/bin/python -m pytest -q tests/test_public_case.py
shasum -a 256 fixtures/public/maka-issue-2221.json
.venv/bin/python -m signal_steward
.venv/bin/python -m signal_steward.server --port 8810
git diff --check
git grep -nE 'AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----|sk-[A-Za-z0-9]{20,}' -- ':!docs/HUMAN_GATE_PACKET.md'
```

The exact human handoff is [`HUMAN_GATE_PACKET.md`](HUMAN_GATE_PACKET.md).
