from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .models import CommitRecord, Conclusion, JobAttempt, ReplayBundle


def _required(value: Any, field: str) -> Any:
    if value is None or value == "":
        raise ValueError(f"fixture field '{field}' is required")
    return value


def load_bundle(path: str | Path) -> ReplayBundle:
    """Load a small GitHub Actions-shaped replay without contacting GitHub."""

    source = Path(path).read_bytes()
    try:
        payload = json.loads(source)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON fixture: {path}") from exc

    if not isinstance(payload, dict) or not isinstance(payload.get("runs"), list):
        raise ValueError("fixture must contain a 'runs' list")
    attempts: list[JobAttempt] = []
    for run in payload["runs"]:
        if not isinstance(run, dict) or not isinstance(run.get("jobs"), list):
            raise ValueError("each run must contain a 'jobs' list")
        for job in run["jobs"]:
            try:
                conclusion = Conclusion(str(_required(job.get("conclusion"), "conclusion")).lower())
            except ValueError as exc:
                raise ValueError(f"unsupported conclusion in run {run.get('run_id')}") from exc
            attempts.append(
                JobAttempt(
                    run_id=int(_required(run.get("run_id"), "run_id")),
                    workflow=str(_required(run.get("workflow"), "workflow")),
                    job_name=str(_required(job.get("name"), "job.name")),
                    head_sha=str(_required(run.get("head_sha"), "head_sha")),
                    attempt=int(run.get("attempt", 1)),
                    conclusion=conclusion,
                    started_at=str(_required(run.get("started_at"), "started_at")),
                    log_excerpt=str(job.get("log_excerpt", ""))[:4000],
                    touched_files=tuple(str(item) for item in job.get("touched_files", [])),
                )
            )

    commits: list[CommitRecord] = []
    for commit in payload.get("commits", []):
        commits.append(
            CommitRecord(
                sha=str(_required(commit.get("sha"), "commit.sha")),
                committed_at=str(_required(commit.get("committed_at"), "commit.committed_at")),
                message=str(commit.get("message", "")),
                changed_files=tuple(str(item) for item in commit.get("changed_files", [])),
            )
        )

    return ReplayBundle(
        attempts=tuple(attempts),
        commits=tuple(commits),
        source_hash=hashlib.sha256(source).hexdigest(),
    )

