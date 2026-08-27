from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .models import Classification, Conclusion, JobAttempt


@dataclass(frozen=True)
class JobSignal:
    job_key: str
    runs_analyzed: int
    success_count: int
    failure_count: int
    cancelled_count: int
    failure_rate: float
    same_sha_groups: int
    recovery_groups: int
    recovery_rate: float
    classification: Classification
    evidence: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "job_key": self.job_key,
            "runs_analyzed": self.runs_analyzed,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "cancelled_count": self.cancelled_count,
            "failure_rate": round(self.failure_rate, 4),
            "same_sha_groups": self.same_sha_groups,
            "recovery_groups": self.recovery_groups,
            "recovery_rate": round(self.recovery_rate, 4),
            "classification": self.classification.value,
            "evidence": list(self.evidence),
        }


def classify_jobs(
    attempts: tuple[JobAttempt, ...] | list[JobAttempt],
    *,
    flaky_threshold: float = 0.10,
    broken_threshold: float = 0.70,
) -> tuple[JobSignal, ...]:
    """Classify completed job outcomes; cancellations do not dilute the rate."""

    by_job: dict[str, list[JobAttempt]] = defaultdict(list)
    for attempt in attempts:
        by_job[attempt.job_key].append(attempt)

    signals: list[JobSignal] = []
    for job_key in sorted(by_job):
        values = by_job[job_key]
        completed = [item for item in values if item.conclusion in (Conclusion.SUCCESS, Conclusion.FAILURE)]
        success_count = sum(item.conclusion == Conclusion.SUCCESS for item in values)
        failure_count = sum(item.conclusion == Conclusion.FAILURE for item in values)
        cancelled_count = sum(item.conclusion in (Conclusion.CANCELLED, Conclusion.SKIPPED) for item in values)
        denominator = success_count + failure_count
        failure_rate = failure_count / denominator if denominator else 0.0

        by_sha: dict[str, list[JobAttempt]] = defaultdict(list)
        for item in completed:
            by_sha[item.head_sha].append(item)
        recovery_groups = 0
        failed_sha_groups = 0
        for sha_attempts in by_sha.values():
            failures = [item for item in sha_attempts if item.conclusion == Conclusion.FAILURE]
            successes = [item for item in sha_attempts if item.conclusion == Conclusion.SUCCESS]
            if failures:
                failed_sha_groups += 1
            if any(failure.attempt < success.attempt for failure in failures for success in successes):
                recovery_groups += 1

        same_sha_groups = failed_sha_groups
        recovery_rate = recovery_groups / same_sha_groups if same_sha_groups else 0.0
        if denominator == 0:
            classification = Classification.CLEAN
            evidence = ("no completed success/failure outcomes; cancellations and skips excluded",)
        elif failure_rate >= broken_threshold and recovery_groups == 0:
            classification = Classification.CONSISTENTLY_BROKEN
            evidence = (
                f"{failure_count}/{denominator} completed outcomes failed ({failure_rate:.0%})",
                "no same-SHA retry recovered",
            )
        elif failure_rate >= flaky_threshold and (
            recovery_groups > 0 or (success_count > 0 and failure_count > 0)
        ):
            classification = Classification.FLAKY
            evidence = (
                f"{failure_count}/{denominator} completed outcomes failed ({failure_rate:.0%})",
                f"{recovery_groups}/{same_sha_groups} failed SHA groups recovered on a later attempt",
            )
        else:
            classification = Classification.CLEAN
            evidence = (f"{failure_count}/{denominator} completed outcomes failed ({failure_rate:.0%})",)

        signals.append(
            JobSignal(
                job_key=job_key,
                runs_analyzed=len(values),
                success_count=success_count,
                failure_count=failure_count,
                cancelled_count=cancelled_count,
                failure_rate=failure_rate,
                same_sha_groups=same_sha_groups,
                recovery_groups=recovery_groups,
                recovery_rate=recovery_rate,
                classification=classification,
                evidence=evidence,
            )
        )
    return tuple(signals)

