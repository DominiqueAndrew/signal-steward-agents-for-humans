# Agents for Humans opportunity sprint

**Research date:** 2026-08-27
**Decision boundary:** Clearline is frozen as an archive at public commit `32c73b970c64cbb471e8cab0b3d47a7f0ae91045`. This note is strategy work only; it contains no product implementation. A new project root is created only after the thesis is selected.

## Method and evidence policy

The sprint looks for recurring work where a person must repeatedly inspect evidence, reconcile conflicting signals, and make a consequential but bounded decision. A concept is not accepted because a source says “AI could help.” It needs:

1. a firsthand account from an affected practitioner or maintainer;
2. a primary scientific, engineering, standards, or government source that makes the burden or mechanism more concrete; and
3. a safe, reproducible local slice that can run on synthetic or public data without pretending that the agent can replace the accountable human.

Firsthand posts are treated as qualitative pain signals, not population estimates. Upvotes and self-reported numbers are recorded as directional evidence only. Quantitative claims are attributed to the primary source that measured them. “Current” event facts are recorded with the fetch timestamp because the event page can change.

## Official event constraints (verified 2026-08-27)

The Devpost Hackathons plugin returned the live `agentsforhumans` record as `submissions_open`, fetched at `2026-08-27T16:21:23Z`.

- Official page: <https://agentsforhumans.devpost.com>
- Brief: build an AI agent with the Strands Agents SDK that handles repetitive tasks in the background and surfaces only genuine human decisions.
- Tracks: Everyday Agents, Professional Agents, Good Neighbor Agents. The candidate targets **Professional Agents** because the primary user is a maintainer doing skilled operational work.
- Submission end from the plugin: `2026-09-15T00:00:00Z` (the rules express this as Monday 2026-09-14 at 5:00 pm Pacific Time).
- Judging: technological implementation, design, potential impact, creativity/originality, and presentation.
- Required submission artifacts: public source repository with MIT or Apache license, architecture diagram, AWS Builder ID, and a public demo video. The plugin reports the video as required and a website/zip as not required.
- The official announcement on 2026-08-21 says to solve a specific problem, do real work rather than chat, make Strands visible in the description/Built With/video, protect keys, and use the five minutes as a pitch covering problem, user, and why it matters.
- The official resources name Strands Agents Python/TypeScript quickstarts and examples. AgentCore is optional, not a substitute for a working end-to-end slice.

Sources: [Devpost overview](https://agentsforhumans.devpost.com/), [official rules](https://agentsforhumans.devpost.com/rules), [resources](https://agentsforhumans.devpost.com/resources), [submission requirements](https://agentsforhumans.devpost.com/), [Strands quickstart](https://strandsagents.com/docs/user-guide/quickstart/overview/), [AWS announcement on Strands architecture](https://aws.amazon.com/blogs/machine-learning/strands-agents-sdk-a-technical-deep-dive-into-agent-architectures-and-observability/).

## Pain dossiers

### A. CI failure signal and culprit triage — candidate: Signal Steward

**Affected users and recurring task.** Software maintainers and code owners repeatedly decide whether a failed CI run is a real regression, a flaky test, infrastructure noise, or a change that should be investigated first. The safe action is not “make the pipeline green”; it is to produce an evidence packet and ask the owner whether to open a bug, quarantine a candidate, or keep investigating.

**Firsthand signals.** In a March 19, 2026 r/devops post, a maintainer reported about 1,300 monorepo runs with 26% success, 231 failed and 428 cancelled runs, 43 minutes wall time versus 10 hours 54 minutes of parallel compute, and an estimate of 208 days of wasted compute. The author described manually digging through 20+ parallel logs, deciding whether the issue was code, a flaky test, or infrastructure, then rerunning and context-switching. A March 12, 2026 post described an 8-minute push-to-red loop repeated four or five times. A December 30, 2025 post described roughly 650 Selenium tests, 40–60 minutes per run, and 8–12 different flakes per run; the stated workaround was repeated reruns and selective/parallel tests.

Sources: [r/devops: CI cost account](https://www.reddit.com/r/devops/comments/1rxlfxd/i_calculated_how_much_my_ci_failures_actually_cost/) (2026-03-19, firsthand), [r/devops: feedback loop](https://www.reddit.com/r/devops/comments/1rrvqyt/the_cicd_feedback_loop_from_hell_push_wait_8_min/) (2026-03-12, firsthand), [r/devops: QA tests blocking deploys](https://www.reddit.com/r/devops/comments/1pzgupz/qa_tests_blocking_deploys_6_times_today_averaging/) (2025-12-30, firsthand).

**Engineering evidence.** A 2024 industrial case study from TUM analysed five years of CI logs, VCS history, issue tickets, and tracked work in a project with 30 developers and 1M SLOC. It reports at least 2.5% of productive developer time spent handling flaky tests: 1.1% investigation, 1.3% repair, 0.1% tooling. In that context, an automated rerun cost 0.02 cents while a manual investigation after not rerunning cost $5.67. Google’s ICST 2023 work evaluated 13,000+ test breakages and used Bayesian inference/noisy binary search to locate buggy commits more accurately than traditional bisection in the presence of flaky tests. Apache Magpie’s read-only triage skill is a useful open-source pattern: group by SHA/workflow, count successes and failures, and distinguish intermittent from consistently broken jobs.

Sources: [TUM industrial case study](https://portal.fis.tum.de/en/publications/cost-of-flaky-tests-in-continuous-integration-an-industrial-case-/) (2024), [Google Flake Aware Culprit Finding](https://research.google/pubs/flake-aware-culprit-finding/) (ICST 2023), [FlakeRake DOI](https://doi.org/10.1109/ICST60714.2024.00032) (ICST 2024), [Apache Magpie triage pattern](https://github.com/apache/magpie/blob/main/skills/flaky-test-triage/SKILL.md) (accessed 2026-08-27), [Tenstorrent CI triage repository](https://github.com/tenstorrent/tt-auto-triage) (accessed 2026-08-27).

**Workarounds and failure costs.** Reruns, retries, quarantines, local prechecks, selective tests, and parallelization are common. They either burn compute, hide a deterministic regression under green retries, or leave a maintainer to reconstruct causality from distributed logs. The first-hand dollar estimates are unverified and should not be generalized; the TUM measurement supplies the stronger productivity signal.

**Uncertainty and falsifier.** The pain is strongest for multi-job repositories with long feedback cycles; small projects may not need a product. A local replay must beat a “rerun twice and keyword scan” baseline on labelled histories. If same-SHA retry outcomes and commit/test topology do not improve classification or reduce review load, the thesis is false.

### B. Prior-authorization packet completeness — candidate: Care Packet Steward

**Affected users and recurring task.** Clinic staff repeatedly gather evidence, answer payer-specific questions, and track a prior-authorization request through portals, fax, phone, and email. The clinical decision remains with a licensed professional; the safe wedge is completeness checking, evidence indexing, and deadline escalation—not approval or denial advice.

**Firsthand signals.** Health-IT practitioners describe exact-match failures across portal/fax/phone, payer responses marked “unknown,” and interactive questions changing by case. A family-medicine physician wrote on 2026-08-16 that a week was dominated by PAs, including a 40-minute peer-to-peer and a one-hour response deadline. A medicine thread from 2024 reports spending ten hours on one patient PA and repeatedly answering the same questions in different forms. These are vivid but self-selected reports, not prevalence estimates.

Sources: [r/healthIT prior authorization](https://www.reddit.com/r/healthIT/comments/1n81e8g/prior_authorization_whats_your_1_frustration_and/) (2025-09-04), [r/FamilyMedicine](https://www.reddit.com/r/FamilyMedicine/comments/1vq1r0i/prior_authorization_has_turned_primary_care_into/) (2026-08-16), [r/medicine: prior auths](https://www.reddit.com/r/medicine/comments/1ehgmlf) (2024-08-01), [r/medicine: prior authorization](https://www.reddit.com/r/medicine/comments/1ufj0dp/prior_authorization_or_how_i_became_radicalized/) (2026-06-25).

**Engineering and cost evidence.** The 2024 CAQH Index reports provider/staff time of 24 minutes per authorization by phone, fax, or email and 16 minutes through a portal; it identifies changing plan requirements, inconsistent data, and low adoption as burden multipliers. It reports a $10.86 industry cost per manual authorization and a $515M electronic prior-authorization savings opportunity. The AMA’s February 2025 research page describes patient-care delays, administrative costs, and workflow disruption as the focus of its physician survey and qualitative work. The Federal Register’s CMS prior-authorization rule is the regulatory anchor for interoperability and turnaround requirements.

Sources: [CAQH 2024 Index](https://www.caqh.org/hubfs/Index/2024%20Index%20Report/CAQH_IndexReport_2024_FINAL.pdf) (2024), [AMA research and reports](https://www.ama-assn.org/practice-management/prior-authorization/prior-authorization-research-reports) (updated 2025-02-24), [CMS prior-authorization rule](https://www.govinfo.gov/content/pkg/FR-2024-08-05/pdf/2024-14975.pdf) (2024-08-05).

**Workarounds and failure costs.** Staff duplicate data entry, switch channels, call the payer, use spreadsheets, and escalate peer-to-peer reviews. The ethical cost of an incorrect or late packet can be delayed care, so an autonomous agent must not make coverage or clinical decisions.

**Uncertainty and falsifier.** A synthetic packet completeness checker can prove extraction, missing-field detection, source citation, and deadline routing, but not payer approval or patient outcomes. If the wedge requires real PHI, payer login, or regulatory interpretation to look useful, it fails the event’s credential-free proof constraint.

### C. Field evidence chain for small construction crews — candidate: Site Ledger

**Affected users and recurring task.** Foremen and project managers repeatedly reconstruct daily work, material receipts, time, instructions, blockers, and approvals from paper, photos, Excel, email, and messaging. The valuable decision is which missing evidence threatens a payment, variation, or dispute—not the generation of another generic daily report.

**Firsthand signals.** In an r/Construction thread (posted December 11, 2025), a commercial-project user with a 15-person crew described four suppliers, missing timesheets, lost paper, illegible handwriting, and an office manager spending hours reconstructing events. Replies emphasize that adoption fails when a form has too many steps and describe 15-minute daily logs, Excel, WhatsApp, and tap-to-log tools. A December 18, 2025 r/ConstructionManagers post called out location, blockers, verbal approvals, context photos, and timestamps as the five things crews need before leaving; it claimed an almost-lost $15k draw due to missing documentation. The dollar loss is anecdotal and not independently verified.

Sources: [r/Construction: daily logs and receipts](https://www.reddit.com/r/Construction/comments/1pk6ouk/whats_your_system_for_tracking_daily_logs_and/) (2025-12-11, firsthand), [r/ConstructionManagers: lawyer-proof daily log](https://www.reddit.com/r/ConstructionManagers/comments/1pq25yb/the_lawyerproof_daily_log_5_things_my_crews_have/) (2025-12-18, firsthand), [r/ConstructionManagers: daily-log time](https://www.reddit.com/r/ConstructionManagers/comments/17w2gsb/how_much_time_do_you_spend_writing_daily_logs/) (2023-11-15, firsthand).

**Engineering evidence.** ASCE’s January 22, 2026 summary of Love’s field-rework research reports actual pre-completion rework averaging 0.38% of contract value and 0.76% when post-completion corrections are included, and explicitly connects better documentation and analysis with quality management and cost forecasting. A peer-reviewed 2005 survey covered 161 construction projects and studied contract-documentation variables related to rework; importantly, it found no significant relationship in that sample, so documentation quality should not be presented as a proven causal cure.

Sources: [ASCE field-rework summary](https://www.asce.org/publications-and-news/civil-engineering-source/article/2026/01/22/how-much-does-field-rework-in-construction-actually-cost) (2026-01-22), [Love, Edwards & Smith, peer-reviewed study](https://pure.uj.ac.za/en/publications/contract-documentation-and-the-incidence-of-rework-in-projects/) (2005).

**Workarounds and failure costs.** Paper, spreadsheets, email, WhatsApp, voice notes, and repeated office reconstruction. The architecture could combine timestamped artifact intake, provenance graphs, and a missing-evidence queue, but geolocation, legal defensibility, and field adoption are hard to prove with synthetic data.

**Uncertainty and falsifier.** The causal link from better capture to fewer disputes/rework is not established by the cited 2005 study. If a demo cannot show a concrete downstream decision (for example, “hold variation packet until approval evidence arrives”) without claiming legal proof, the wedge is too abstract.

### D. Critical-flow accessibility regression triage — candidate: Access Gate

**Affected users and recurring task.** Accessibility professionals and product teams repeatedly inspect critical flows, map automated findings to WCAG success criteria, reproduce issues with assistive technologies, and decide which barriers block a release. The human decision is the accessibility specialist’s acceptance or exception; the agent must not claim conformance.

**Firsthand signals.** Accessibility practitioners report approximately a day per page for a small WCAG 2.2 AA audit and anxiety that a single missed issue can affect thousands of users. They describe combined automated, manual, and screen-reader testing because automated tools miss important barriers. These accounts are directional and the time estimates vary by page complexity.

Sources: [r/accessibility: audit time](https://www.reddit.com/r/accessibility/comments/1itv6rl/time_required_for_a11y_audit/) (2025-02-20, firsthand), [r/accessibility: missing a violation](https://www.reddit.com/r/accessibility/comments/1umo8o8) (2026-07-03, firsthand), [r/accessibility: manual remediation](https://www.reddit.com/r/accessibility/comments/1hwowey) (accessed 2026-08-27, firsthand).

**Engineering evidence.** WCAG 2.2 is a W3C Recommendation (2024-12-12) with testable success criteria and an explicit warning that even AAA conformance does not cover every disability. WebAIM’s 2025 Million report evaluated one million home pages and found 50,960,288 detected errors, 51 per page on average, and detected WCAG failures on 94.8% of pages; it explicitly warns that automated absence of errors does not establish accessibility. GitHub’s accessibility scanner illustrates an existing pattern of filing and reopening findings, including issues automated tools can miss.

Sources: [W3C WCAG 2.2](https://www.w3.org/TR/wcag/) (Recommendation 2024-12-12), [WebAIM Million 2025](https://webaim.org/projects/million/2025) (last updated 2025-03-31), [GitHub accessibility scanner](https://github.com/github/accessibility-scanner) (accessed 2026-08-27).

**Workarounds and failure costs.** Axe/WAVE/Lighthouse followed by manual review and screen-reader testing. A naive AI auditor can produce false reassurance, so a defensible system needs reproducible browser traces, rule citations, and an explicit human verification state.

**Uncertainty and falsifier.** WebAIM’s sample is home pages and its detected error set is not full conformance. If the project cannot demonstrate that it surfaces a small number of high-impact, reproducible critical-flow decisions without claiming “accessible,” it is another automated scanner wrapper.

### E. Evidence-review screening with auditable disagreement — candidate: Review Queue

**Affected users and recurring task.** Solo researchers and small review teams repeatedly screen titles/abstracts/full text, record inclusion reasons, reconcile disagreements, and preserve a reproducible audit trail for a systematic review. The human decision is eligibility and interpretation; the agent can prioritize, extract structured evidence, and surface disagreement.

**Firsthand signals.** A recent r/AskAcademia thread describes screening 3,400 papers as overwhelming and says dual screening exists because a solo reviewer can miss studies without noticing. Other graduate-research threads describe full-text screening for hours and workarounds of skimming abstract/intro/conclusion/figures, keyword searching, bookmarks, and AI as a “mentor,” with concern about quality. A 2021 post describes 40–60 hour weeks for literature review work. These are self-selected and the review types differ.

Sources: [r/AskAcademia screening workflow](https://www.reddit.com/r/AskAcademia/comments/1uqcvtq/looking_for_advice_on_screening_workflow/) (accessed 2026-08-27, firsthand), [r/GradSchool systematic review](https://www.reddit.com/r/GradSchool/comments/1hbyfbm/how_to_get_through_systematic_review) (2024-12-11, firsthand), [r/GradSchool literature review](https://www.reddit.com/r/GradSchool/comments/qmrt7m) (2021-11-04, firsthand), [r/AskAcademia reading for a review](https://www.reddit.com/r/AskAcademia/comments/142feka) (2023-06-06, firsthand).

**Engineering evidence.** PRISMA 2020 is a published reporting guideline with a 27-item checklist and flow diagrams. Its explanation paper requires reporting counts and reasons across identification, screening, retrieval, eligibility, and inclusion—exactly the provenance that ad-hoc AI summarization tends to erase. The standard is about reporting, not a claim that automated screening is valid.

Sources: [PRISMA 2020 statement](https://www.prisma-statement.org/prisma-2020-statement) (2021, DOI 10.1136/bmj.n71), [PRISMA explanation and elaboration](https://www.bmj.com/content/372/bmj.n160) (2021).

**Workarounds and failure costs.** Manual spreadsheets, reference managers, full-text skimming, dual review, and informal AI assistance. False exclusion can bias a review and is harder to detect than a missed formatting task.

**Uncertainty and falsifier.** The public evidence here is strongest for workload and process complexity, not a measurable market size. If a demo cannot preserve source spans, exclusion reasons, disagreement history, and a PRISMA-compatible flow without exposing copyrighted full text, it fails the ethical and reproducibility bar.

### F. Exploitability-aware dependency remediation — candidate: KEV Path

**Affected users and recurring task.** Small security and platform teams repeatedly triage dependency alerts, map a CVE to a runtime asset and owner, decide urgency, and coordinate a safe fix. The human decision is whether and when to patch, mitigate, or accept risk; the agent must not auto-merge a change or declare a system safe.

**Firsthand signals.** A Dependabot maintainer issue opened April 9, 2026 describes security-alert emails as long and flat, severity buried, scope vague, and the path from alert to decision to fix unstructured, with no batch-remediation support. It names repository maintainers and code owners as primary users and explicitly asks “what is urgent” and “what should I fix first, given risk and effort?”

Source: [Dependabot issue #14675](https://github.com/dependabot/dependabot-core/issues/14675) (opened 2026-04-09, maintainer-authored).

**Engineering evidence.** NIST SP 800-218 recommends vulnerability disclosure/remediation processes and risk-informed analysis. CISA describes its KEV catalog as the authoritative list of vulnerabilities exploited in the wild and tells organizations to use it as an input to prioritization. GitHub’s documentation exposes alert identifiers, dependency graphs, remediation tracking, and assignment to owners, but also states that alerts cannot catch every security issue.

Sources: [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) (2022-02), [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) (accessed 2026-08-27), [GitHub vulnerability exposure](https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/vulnerability-exposure) (accessed 2026-08-27), [GitHub Dependabot alert docs](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts) (accessed 2026-08-27).

**Workarounds and failure costs.** Email scanning, severity sorting, spreadsheets, manual dependency-graph inspection, and ad-hoc issue assignment. The cost of false urgency is alert fatigue; the cost of false reassurance is exposure. A demo must use synthetic or public package graphs and immutable evidence.

**Uncertainty and falsifier.** Existing SCA products already occupy this space. Without a clearly differentiated evidence-to-owner path and safety policy, this is a dashboard wrapper; without authenticated repo access, the live integration is unproven.

## Scoring model

Scores are 0–5, assigned after reading the sources above. A score is a planning judgment, not measured user validation. The weighted score is:

`S = 0.20P + 0.10N + 0.15T + 0.15M + 0.15J + 0.10F + 0.10E + 0.05V`

where `P` = evidenced pain, `N` = novelty of the narrow wedge, `T` = technical depth, `M` = defensibility/moat, `J` = judge wow, `F` = event fit, `E` = ethical feasibility, and `V` = time-to-proof. A high score does not excuse missing evidence. Ethics is intentionally weighted above proof speed because the event asks for real work and human decisions, not unsafe automation.

| Concept | P | N | T | M | J | F | E | V | Weighted S | Main uncertainty |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Signal Steward: CI evidence and culprit triage | 5 | 4 | 5 | 4 | 5 | 5 | 5 | 5 | **4.75** | Small repos may not feel enough pain; local replay must beat rerun baseline |
| Site Ledger: construction field-evidence chain | 4 | 4 | 5 | 4 | 5 | 5 | 4 | 3 | **4.35** | Legal/causal value and field adoption are not established |
| KEV Path: exploitability-aware remediation | 5 | 3 | 5 | 4 | 4 | 5 | 3 | 4 | **4.25** | Crowded market; authenticated integration and patch safety |
| Care Packet Steward: PA completeness | 5 | 4 | 5 | 4 | 5 | 5 | 2 | 2 | **4.30** | PHI, payer variation, and clinical/regulatory boundary |
| Access Gate: critical-flow accessibility triage | 5 | 3 | 4 | 3 | 4 | 5 | 5 | 4 | **4.15** | Automated testing cannot establish conformance; crowded tools |
| Review Queue: auditable evidence-review screening | 4 | 4 | 5 | 4 | 4 | 5 | 3 | 4 | **4.15** | Bias/copyright risks and weak population-level pain data |

The raw scores are close among several professional workflows. The decisive tie-break is not “AI novelty”; it is the combination of low-risk synthetic proof, a measurable technical baseline, explicit human gates, and a useful failure mode that can be shown in five minutes. Care Packet’s 4.30 is lower in practical readiness than its pain score suggests because the ethical and credential boundary is material. Signal Steward therefore wins the falsifiable-build test.

## Selected thesis

### Thesis: Signal Steward

**Falsifiable claim.** For a maintainer reviewing a backlog of CI failures, a provenance-first background agent that compares same-SHA retry outcomes, normalizes job/test evidence, and ranks likely culprit changes will classify intermittent versus deterministic failures and produce a correct first next action more often than a baseline of “rerun twice, then keyword-scan,” while never mutating CI or tracker state without an explicit human decision.

**Narrow initial wedge.** One GitHub Actions repository (or a deterministic local replay of its exported run history), one default branch, one 30-day window, and job-level triage. The first version handles three decisions: `investigate regression`, `candidate for flaky-test quarantine`, or `insufficient evidence`. It does not patch code, disable tests, merge PRs, or claim root cause from logs alone.

**Minimum demonstrable architecture.**

1. A read-only collector accepts GitHub Actions-shaped events or seeded JSON fixtures; no token is required for the local demo.
2. A normalizer stores immutable runs, jobs, attempts, SHAs, log excerpts, and evidence hashes in SQLite.
3. A deterministic signal layer groups by `(workflow, job, head_sha)`, computes failure rate and same-SHA recovery, and labels `FLAKY`, `CONSISTENTLY_BROKEN`, or `CLEAN`.
4. A causal ranker uses commit proximity, changed-file/test overlap, and prior failure history to produce a ranked hypothesis with explicit supporting and contradicting evidence. It must say “hypothesis,” not “root cause,” unless the evidence is independently confirmed.
5. A real Strands agent orchestrates read-only tools such as `list_runs`, `compare_attempts`, `inspect_commit_window`, and `build_evidence_packet`. The tools, not free-form model text, define the side-effect boundary.
6. A small review surface shows only the few packets that cross a policy threshold, plus the evidence needed to choose a next action. Approve/hold decisions append an audit event; no CI mutation occurs in the demo.

**Explicit model.** For job `j` over the observation window, let `f_j` be failed attempts and `s_j` successful attempts, excluding cancelled/skipped jobs. `r_j = f_j / (f_j + s_j)`. Let `q_j` be the fraction of same-SHA groups where an initial failure is followed by a success on a later attempt. The conservative baseline policy is:

- `FLAKY` if `r_j >= 0.10` and there is same-SHA recovery or both success and failure in the window;
- `CONSISTENTLY_BROKEN` if `r_j >= 0.70` and no same-SHA rerun succeeds;
- `CLEAN` if `r_j < 0.10`.

The thresholds are starting policy parameters, not scientific constants; they are aligned with the Apache Magpie triage pattern and must be sensitivity-tested. For a candidate commit `c`, the agent reports `P(c | e) ∝ P(e | c)P(c)`, where `e` includes temporal proximity, changed-file overlap, test history, and retry evidence. This is a ranked hypothesis, not a causal proof.

**Evaluation design.** Build a labelled synthetic replay with at least 60 histories: deterministic regression, same-SHA flake, infrastructure interruption, cancellation, and mixed multi-job runs. Hold out scenarios by incident seed so the agent cannot memorize fixtures. Compare against the baseline policy above plus blind two-rerun triage. Report:

- macro-F1 for `FLAKY` vs `CONSISTENTLY_BROKEN` vs `CLEAN`;
- same-SHA recovery precision and recall;
- top-1 culprit-hypothesis hit rate on seeded regressions;
- false-escalation rate (surfacing a decision where evidence is insufficient);
- human decisions required per 10 incidents and median evidence-packet size;
- exact replay command, fixture hash, model/provider configuration, and failure cases.

The thesis is supported only if the holdout classification clears a pre-registered target of macro-F1 ≥ 0.85, top-1 culprit hit rate is ≥ 0.70, and false-escalation rate is ≤ 0.10 while requiring fewer than half as many human review items as the blind-rerun baseline. These are engineering acceptance targets, not results; the implementation must publish actual results and limitations.

**Safety and ethical boundary.** Synthetic or public non-sensitive data only. Read-only GitHub scope in the first integration. No secrets in fixtures or logs. No automatic rerun, quarantine, issue creation, merge, or workflow edit. An ambiguous or missing evidence packet is surfaced as `INSUFFICIENT_EVIDENCE`; it is never silently discarded.

**Why this is defensible.** The wedge is not generic “AI explains a failed build.” Its durable unit is a versioned evidence packet joining same-SHA retry behavior, job-level classification, commit/test topology, and a human decision record. Over time, repository-specific flake fingerprints and reviewed outcomes can improve priors and expose threshold drift, while the read-only boundary keeps trust recoverable. The moat is calibrated provenance, not a hidden prompt.

## Decision and next gate

The evidence sprint selects Signal Steward. The next action is to create a new project root and repository containing this annex (before product code), then implement only the smallest vertical slice described above. Clearline remains untouched as a recoverable archive.

The first holdout run is recorded in [`RESULTS.md`](RESULTS.md). It meets the pre-registered engineering targets on synthetic data, but the limitations in that report are part of the result and prevent any production-accuracy claim.

## Reproducibility checklist

- Record this file’s SHA in the first new-repository commit.
- Keep every fixture synthetic, small, and versioned; include expected labels.
- Pin Python/Node dependencies and the Strands SDK version used.
- Run a credential-free local replay in CI.
- Run a separate optional read-only GitHub integration test only when an authorized token exists; report it as unverified otherwise.
- Publish architecture diagram, test command, benchmark command, fixture hash, and demo steps in the README.
