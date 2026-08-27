# Signal Steward — human gate packet

This packet is the smallest remaining action set for a truthful Agents for
Humans submission. It intentionally does not ask for secrets, accept rules,
submit a project, or claim a live AWS deployment.

## Live official facts (refreshed 2026-08-27)

Fetched through the Devpost Hackathons capability on 2026-08-27 at
18:01:03–18:01:32 UTC; the event page remains in `submissions_open`.

- Event: [Agents for Humans Hackathon](https://agentsforhumans.devpost.com/)
- Deadline: **2026-09-15 00:00:00 UTC** (the event is displayed in Pacific Time;
  target September 14 before 5:00 pm PT).
- Prize pool: **$40,000** across the Grand Prize and three tracks.
- Required technology: Strands Agents SDK.
- Entry step: the official rules direct entrants to sign up for an AWS Account
  and install the Strands Agents SDK; this packet does not claim AWS account
  access or a live deployment.
- Current rules payload: legal age of majority in the country of residence;
  specific countries/territories are excluded; team is not required; all
  occupations; no company required. The participant must confirm their own
  eligibility.
- New-project rule: the project must be newly created during the submission
  period; any incorporated pre-existing non-standard code or work must be
  disclosed. Standard tools, libraries, SDKs, templates, and AI coding
  assistants are allowed under the current rules.
- Submission deliverables: **video required**; website and zip are not
  required. The live demo URL is optional.
- Required submission fields: submitter type, country of residence, track,
  public code-repository URL, architecture diagram upload, and AWS Builder ID.
- Judging criteria: Technological Implementation, Design, Potential Impact,
  Creativity & Originality, and Presentation.
- Optional build-cost support: registered participants can request **$50 in AWS
  Promotional Credits**, while supplies last, through the Resources form by
  **2026-09-11 at 12:00 PT**; AWS Promotional Credits terms apply. This is not
  evidence of an AWS deployment or a grant of credits.

The authoritative pages are [rules](https://agentsforhumans.devpost.com/rules),
[resources](https://agentsforhumans.devpost.com/resources), and the
[official event page](https://agentsforhumans.devpost.com/). Recheck them at
the moment of the human action; Devpost can change the form.

## Gate 0 — registration form (human-only)

A read-only registration-form check through the official Devpost capability at
`2026-08-27T18:03:56Z` returned `can_register: true` and
`already_registered: false` for the connected account. No registration or
agreement was submitted. If the participant still needs to register, they
must personally:

1. Choose exactly one team preference: `Working solo`, `Looking for
   teammates`, or `Already have a team`.
2. Answer every required registration question using the form’s current
   options:
   - AWS experience: `New to AWS`; `Some experience (used a few services)`;
     `Comfortable (build on AWS regularly)`; or `Expert (AWS in production daily)`.
   - Bedrock AgentCore/Strands experience: `Never use either`; `Used Bedrock
     AgentCore only`; `Used Strands SDK only`; `Used both`; or `Heard of them
     but haven't built with either`.
   - AI-agent experience: `None yet`; `Tinkered with LLM apps / prompt`;
     `Built a basic agent (tool calling, RAG)`; or `Built production agent systems`.
   - Participation: `Solo`; `I have a team already`; `Looking to join a team`;
     or `Not sure yet`.
   - Event help: `Live mentorship / office hours`; `Starter templates and
     sample code`; `Workshops and tutorials`; `A sandbox environment to
     experiment in`; or `Clear dos and reference architectures`.
3. Read the [official rules](https://agentsforhumans.devpost.com/rules) and
   [Devpost terms](https://info.devpost.com/terms), then personally agree to
   both. The eligibility agreement is also required; the participant must
   confirm the age/geography statements are true for them.

Expected evidence: the participant’s own registration confirmation. Fallback:
do not register or accept agreements; the repository’s local demo remains
usable without registration.

## Gate 1 — identity, eligibility, and optional live AWS proof

Required human inputs: the participant’s eligibility confirmation, AWS Builder
ID, and (only if a live AWS run is wanted) an already-authorized local AWS
profile. Do not paste credentials, access keys, or tokens into chat or the
repository.

1. Open the official [AWS Builder ID profile](https://profile.aws.amazon.com/)
   and sign in or create the ID.
2. If live AWS evidence is desired, configure credentials in the local AWS CLI
   using the participant’s normal private method, then run from the repository:

   ```sh
   aws sts get-caller-identity --query '{Account:Account,Arn:Arn}' --output json
   ```

   Expected proof is only the account/ARN JSON returned by AWS; redact the ARN
   before sharing it. This command does not print secret material.
3. If the command cannot run, stop at the local demo. The project’s default
   replay and tests remain credential-free; no AWS deployment claim is made.

On 2026-08-27 the authorized local environment passed this STS identity check;
the account and ARN were intentionally not recorded. This is only a credential
availability proof. It is not a deployment, AgentCore, or model-invocation
claim, and it does not replace the participant’s Builder ID field.

Human-only gate: the participant decides whether the personal eligibility
statements are true and whether to use an AWS account. The agent must not make
that decision.

## Gate 1b — provenance, ownership, and access (human-only)

Before saving or submitting the Devpost form, the participant must personally
confirm:

1. Signal Steward was newly created during the submission period, and any
   incorporated pre-existing non-standard code or work is disclosed.
2. The submission is the participant’s original work, is solely owned by the
   participant (or the represented team/organization), and does not violate
   another person’s intellectual-property, privacy, contract, or publicity
   rights.
3. Every third-party SDK, library, template, API, dataset, or public incident
   fixture is authorized for this use and its applicable license/terms are
   satisfied. The participant confirms any required attribution or disclosure.
4. If entering for a team or organization, the submitter is the authorized
   representative. The project has not received prohibited financial or
   preferential support from the sponsor or administrator.
5. The text, testing instructions, diagram, and video are in English or have
   the required English translation, and the public project will remain free
   and accessible for judging and testing through the judging period.

Expected evidence: the participant’s own confirmation and any required
disclosures or permissions. The agent must not infer ownership, consent,
eligibility, representation, or license compliance from the repository.

Optional AWS credit action (separate from the identity check):

- Required input: the participant must be registered for the hackathon and must
  personally authorize any AWS credit request.
- Click path: [Agents for Humans Resources](https://agentsforhumans.devpost.com/resources)
  → **Request your AWS Credits** → complete the linked request form before
  2026-09-11 at 12:00 PT.
- Expected evidence: the participant’s own confirmation that the request was
  submitted. Do not claim credits were granted without the provider’s result.
- Fallback: use the credential-free local demo; no AWS credit request is needed
  to run the repository.

## Gate 2 — public demo video

The repository already contains the exact [four-minute run of show](demo-script.md)
and a browser surface backed by the real local service.

1. Start the demo:

   ```sh
   .venv/bin/python -m signal_steward.server --port 8810
   open http://127.0.0.1:8810
   ```

2. Record the screen and voiceover (macOS: `Cmd+Shift+5`) while following
   `docs/demo-script.md`. Keep the final recording under five minutes. It must
   show the background replay, flaky signal, deterministic regression
   hypothesis, insufficient-evidence hold, and the human audit event.
3. Upload the recording to YouTube or Vimeo as public or unlisted, then keep
   the resulting URL. Expected proof: a URL that opens in a private/incognito
   window and visibly demonstrates the project end-to-end.

Fallback: a credential-free local recording is the intended proof. A live
AWS/GitHub connection is optional and must not be implied if it was not used.
Slides, screen recording, and voiceover are acceptable; appearing on camera is
not required according to the latest organizer announcement.

## Gate 3 — final Devpost form

Click path: [Agents for Humans](https://agentsforhumans.devpost.com/) → sign in
→ **Submit a Project** → create or edit the Signal Steward project → complete
the required fields → save draft → personally review → **Submit**.

Use these prepared values:

| Field | Value / action |
| --- | --- |
| Project name | `Signal Steward` |
| Track | `Professional Agents` |
| Submitter type | `Individual` if that is factually correct; otherwise choose the participant’s true type |
| Country | The participant’s actual country of residence |
| Public code repo | `https://github.com/DominiqueAndrew/signal-steward-agents-for-humans` |
| Architecture diagram | Upload the generated `docs/architecture-diagram.png` from this repo |
| AWS Builder ID | The participant’s own Builder ID, entered privately in Devpost |
| Demo video | The public/unlisted YouTube or Vimeo URL from Gate 2 |
| Live demo | Optional: leave blank if no public deployment exists |
| Testing instructions | `python3 -m venv .venv && .venv/bin/python -m pip install -e '.[dev]' && ./scripts/verify-release.sh`; then run the local server command above |
| Bonus blog | Optional; if used, publish on `builder.aws.com` before the deadline and put `Agents for Humans` in the title; leave blank unless a truthful public post exists |

Before the final click, verify:

```sh
git status --short --branch
git ls-remote origin refs/heads/main
./scripts/verify-release.sh
.venv/bin/python -m pytest -q
.venv/bin/python -m pip check
git grep -nE 'AKIA[0-9A-Z]{16}|AWS_SECRET_ACCESS_KEY|aws_secret_access_key' -- ':!docs/HUMAN_GATE_PACKET.md' || true
```

Expected evidence before the final Devpost click: the `git ls-remote` SHA is
the public `main` release being submitted and matches the latest release
receipt check. Re-run it after any later push; do not rely on a copied stale
SHA.

Expected evidence after the human action: the Devpost project page shows the
video, repo, architecture attachment, Builder ID, and **Submitted** status. A
saved draft is not a submission. The agent must never claim this status without
the participant’s direct confirmation.

If the participant is not ready to agree to the rules or cannot satisfy an
eligibility field, save no consequential state and use the local demo/research
annex as the fallback. Do not bypass the form or its agreements.

## Current readiness ledger

- [x] Fresh public repository, Apache-2.0 license, README, tests, and research
  annex.
- [x] Architecture source and upload-ready diagram.
- [x] Credential-free local browser demo and under-five-minute runbook.
- [ ] Participant confirms personal eligibility and Builder ID.
- [ ] Participant confirms the new-project rule and discloses any incorporated
  pre-existing non-standard code or work.
- [ ] Participant confirms original ownership, third-party permissions and
  licenses, and absence of prohibited sponsor support.
- [ ] If applicable, the authorized team representative confirms authority;
  participant confirms English/translation and free public judging access.
- [ ] Human records a public/unlisted video URL.
- [ ] Human reviews and submits the Devpost form.
