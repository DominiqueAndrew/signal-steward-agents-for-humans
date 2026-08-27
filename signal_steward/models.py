from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Conclusion(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"


class Classification(StrEnum):
    FLAKY = "FLAKY"
    CONSISTENTLY_BROKEN = "CONSISTENTLY_BROKEN"
    CLEAN = "CLEAN"


class ReviewAction(StrEnum):
    INVESTIGATE_REGRESSION = "investigate_regression"
    QUARANTINE_CANDIDATE = "quarantine_candidate"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


@dataclass(frozen=True)
class JobAttempt:
    run_id: int
    workflow: str
    job_name: str
    head_sha: str
    attempt: int
    conclusion: Conclusion
    started_at: str
    log_excerpt: str = ""
    touched_files: tuple[str, ...] = ()

    @property
    def job_key(self) -> str:
        return f"{self.workflow} / {self.job_name}"


@dataclass(frozen=True)
class CommitRecord:
    sha: str
    committed_at: str
    message: str
    changed_files: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReplayBundle:
    attempts: tuple[JobAttempt, ...]
    commits: tuple[CommitRecord, ...]
    source_hash: str

