# Public incident evidence cases

This annex contains one small, manually normalized case from a public primary
issue tracker. It is a sanity check for the same-SHA recovery rule, not a
representative evaluation set and not a claim about Apache Maka’s overall CI
health.

## SS-PUB-001 — Apache Maka CI timeout report

- **Primary source:** [Apache Maka issue #2221](https://github.com/apache/maka/issues/2221)
- **Source date:** 2026-08-05; accessed 2026-08-27
- **Affected user:** a project maintainer diagnosing a red CI job on a
  documentation-only pull request.
- **Observed pain (paraphrase):** `test_workspaces` failed in the CLI workspace
  on a documentation-only change; the same job on the same commit passed when
  rerun. The report says the failure appeared at the edge of a fixed 250 ms
  wait budget under runner load and could look like a real regression.
- **Recurring/severity signal:** the issue reports 373 call sites of the shared
  helper, so the described failure mode can affect many tests. This is a
  directional signal from one maintainer report, not a population estimate.
- **Current workaround and cost:** inspect the job log and rerun the same job.
  The immediate cost is a red, ambiguous pull request and another CI cycle;
  the source provides no dollar estimate, so none is invented here.
- **Normalized replay:** `fixtures/public/maka-issue-2221.json` records the
  reported run ID `30986889078`, two attempts, a pseudonymized same-commit SHA,
  and date-only timestamps. The first attempt is `failure`; the second is
  `success`. Identifiers not exposed in the evidence used here are not guessed.
- **Fixture SHA-256:** `635d77bdf0f82d8bb904811baaf8629c3236c95eb53c7569a4bdc5b27970b849`
- **Observed classifier output:** failure rate `1/2 = 0.5`, same-SHA recovery
  `1/1`, classification `FLAKY`. The label confidence is **medium**: the
  same-SHA retry fact is explicit in the source, but no raw job artifact is
  bundled. The classifier does not encode the issue author’s root-cause
  hypothesis as a causal conclusion.
- **Uncertainty:** one incident, no raw workflow artifact, no independent
  replication, and a pseudonymized SHA. This case must not be merged into the
  60-history synthetic headline metrics or used to claim real-world accuracy.

Reproduce the normalization check with:

```sh
.venv/bin/python -m pytest -q tests/test_public_case.py
shasum -a 256 fixtures/public/maka-issue-2221.json
```

## SS-PUB-002 — Kubernetes conformance failure without retry evidence

- **Primary source:** [Kubernetes issue #131150](https://github.com/kubernetes/kubernetes/issues/131150)
- **Source date:** 2025-04-02; accessed 2026-08-27
- **Affected user:** a Kubernetes contributor triaging a conformance failure
  observed in an external CI system.
- **Observed pain (paraphrase):** the issue names a scheduler conformance test
  failure and links an external CI job, while reporting no corresponding
  Kubernetes TestGrid flake and an unknown start date.
- **Evidence boundary:** the source contains one observed failure, no same-SHA
  recovery, and no culprit commit. The normalized replay therefore uses one
  failure, an unknown/pseudonymized SHA, and an empty commit list; no retry or
  root cause is invented.
- **Observed policy output:** the deterministic classifier reports
  `CONSISTENTLY_BROKEN` for the single failed completed outcome, but the policy
  emits `INSUFFICIENT_EVIDENCE`, surfaces no hypothesis, and creates no audit
  event. This is a negative control for safe action selection, not a claim that
  one failure proves a permanently broken test.
- **Fixture SHA-256:** `b974705ea60d3ff628c37b037e71d545eb78d2495c6e423ce920c6d074c6a92d`
- **Uncertainty:** one external job, no raw artifact in this repository, no
  same-SHA comparison, unknown onset, and no independent replication. It is
  outside the synthetic headline metrics and real-world accuracy claims.

Reproduce both public-case checks with:

```sh
.venv/bin/python -m pytest -q tests/test_public_case.py tests/test_public_case_negative_control.py
shasum -a 256 fixtures/public/kubernetes-issue-131150.json
```
