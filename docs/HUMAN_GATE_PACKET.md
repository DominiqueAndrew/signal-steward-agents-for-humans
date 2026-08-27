# Signal Steward — human gate packet

This packet is the smallest remaining action set for a truthful Agents for
Humans submission. It intentionally does not ask for secrets, accept rules,
submit a project, or claim a live AWS deployment.

## Live official facts (refreshed 2026-08-27)

Fetched through the Devpost Hackathons capability on 2026-08-27 at
17:07:19–17:07:24 UTC; the event page remains in `submissions_open`.

- Event: [Agents for Humans Hackathon](https://agentsforhumans.devpost.com/)
- Deadline: **2026-09-15 00:00:00 UTC** (the event is displayed in Pacific Time;
  target September 14 before 5:00 pm PT).
- Prize pool: **$40,000** across the Grand Prize and three tracks.
- Required technology: Strands Agents SDK.
- Current rules payload: legal age of majority in the country of residence;
  specific countries/territories are excluded; team is not required; all
  occupations; no company required. The participant must confirm their own
  eligibility.
- Submission deliverables: **video required**; website and zip are not
  required. The live demo URL is optional.
- Required submission fields: submitter type, country of residence, track,
  public code-repository URL, architecture diagram upload, and AWS Builder ID.
- Judging criteria: Technological Implementation, Design, Potential Impact,
  Creativity & Originality, and Presentation.

The authoritative pages are [rules](https://agentsforhumans.devpost.com/rules),
[resources](https://agentsforhumans.devpost.com/resources), and the
[official event page](https://agentsforhumans.devpost.com/). Recheck them at
the moment of the human action; Devpost can change the form.

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

Human-only gate: the participant decides whether the personal eligibility
statements are true and whether to use an AWS account. The agent must not make
that decision.

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
| Testing instructions | `python3 -m venv .venv && .venv/bin/python -m pip install -e '.[dev]' && .venv/bin/python -m pytest -q`; then run the local server command above |
| Bonus blog | Optional; leave blank unless a truthful public AWS Builder post exists |

Before the final click, verify:

```sh
git status --short --branch
.venv/bin/python -m pytest -q
.venv/bin/python -m pip check
git grep -nE 'AKIA[0-9A-Z]{16}|AWS_SECRET_ACCESS_KEY|aws_secret_access_key' -- ':!docs/HUMAN_GATE_PACKET.md' || true
```

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
- [ ] Human records a public/unlisted video URL.
- [ ] Human reviews and submits the Devpost form.
