from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from signal_steward.models import Classification, CommitRecord, Conclusion, JobAttempt

SPEC_VERSION = "holdout-2026-08-27.v1"


@dataclass(frozen=True)
class BenchmarkHistory:
    history_id: str
    category: str
    attempts: tuple[JobAttempt, ...]
    commits: tuple[CommitRecord, ...]
    expected: dict[str, Classification]
    culprit: dict[str, str | None]


def _attempt(
    run_id: int,
    workflow: str,
    job_name: str,
    sha: str,
    attempt: int,
    conclusion: Conclusion,
    minute: int,
    log: str,
    touched: tuple[str, ...] = (),
) -> JobAttempt:
    return JobAttempt(
        run_id=run_id,
        workflow=workflow,
        job_name=job_name,
        head_sha=sha,
        attempt=attempt,
        conclusion=conclusion,
        started_at=f"2026-08-{1 + minute // 1440:02d}T{(minute // 60) % 24:02d}:{minute % 60:02d}:00Z",
        log_excerpt=log,
        touched_files=touched,
    )


def _commits(head_sha: str, slug: str, minute: int, changed_file: str) -> tuple[CommitRecord, ...]:
    return (
        CommitRecord(
            sha=head_sha,
            committed_at=f"2026-08-{1 + minute // 1440:02d}T{(minute // 60) % 24:02d}:00:00Z",
            message=f"change {slug} behavior",
            changed_files=(changed_file,),
        ),
        CommitRecord(
            sha=f"distractor-{slug}",
            committed_at=f"2026-08-{1 + minute // 1440:02d}T{(minute // 60) % 24:02d}:30:00Z",
            message="update unrelated documentation",
            changed_files=(f"docs/{slug}.md",),
        ),
    )


def _single_history(index: int, category: str) -> BenchmarkHistory:
    slug = f"{category}-{index:02d}"
    workflow = f"BENCH/{category}-{index:02d}"
    job = "job"
    job_key = f"{workflow} / {job}"
    head = f"{category[:3]}-head-{index:02d}"
    file_name = f"src/{category}_{index:02d}.py"
    base = 60 + index * 10
    attempts: list[JobAttempt]
    expected: Classification
    culprit: str | None
    if category == "deterministic":
        attempts = [
            _attempt(100000 + index * 10 + attempt, workflow, job, f"{category}-sha-{attempt}", 1, Conclusion.FAILURE, base + attempt * 2, "AssertionError cache eviction expected 2 got 3", (file_name,))
            for attempt in range(1, 5)
        ]
        expected, culprit = Classification.CONSISTENTLY_BROKEN, head
        attempts[-1] = _attempt(100000 + index * 10 + 4, workflow, job, head, 1, Conclusion.FAILURE, base + 8, "AssertionError cache eviction expected 2 got 3", (file_name,))
    elif category in {"flaky", "infrastructure"}:
        log = "runner unavailable during cache warmup" if category == "infrastructure" else "cache warmup timeout while waiting for redis"
        attempts = [
            _attempt(200000 + index * 10, workflow, job, head, 1, Conclusion.FAILURE, base, log, (file_name,)),
            _attempt(200000 + index * 10 + 1, workflow, job, head, 2, Conclusion.SUCCESS, base + 8, "retry completed", (file_name,)),
        ]
        expected, culprit = Classification.FLAKY, None
    elif category == "cancelled":
        attempts = [
            _attempt(300000 + index * 10, workflow, job, head, 1, Conclusion.CANCELLED, base, "superseded by a newer commit"),
        ]
        expected, culprit = Classification.CLEAN, None
    else:  # pragma: no cover - mixed histories are assembled separately
        raise ValueError(category)
    return BenchmarkHistory(
        history_id=slug,
        category=category,
        attempts=tuple(attempts),
        commits=_commits(head, slug, base, file_name),
        expected={job_key: expected},
        culprit={job_key: culprit},
    )


def _mixed_history(index: int) -> BenchmarkHistory:
    workflow = f"BENCH/mixed-{index:02d}"
    base = 600 + index * 10
    broken_job = "unit"
    flaky_job = "integration"
    clean_job = "lint"
    broken_key = f"{workflow} / {broken_job}"
    flaky_key = f"{workflow} / {flaky_job}"
    clean_key = f"{workflow} / {clean_job}"
    broken_head = f"mix-broken-head-{index:02d}"
    flaky_head = f"mix-flaky-head-{index:02d}"
    broken_file = f"src/mixed_{index:02d}.py"
    attempts = (
        _attempt(400000 + index * 10, workflow, broken_job, f"mix-old-{index:02d}", 1, Conclusion.FAILURE, base, "AssertionError cache eviction expected 2 got 3", (broken_file,)),
        _attempt(400000 + index * 10 + 1, workflow, broken_job, broken_head, 1, Conclusion.FAILURE, base + 4, "AssertionError cache eviction expected 2 got 3", (broken_file,)),
        _attempt(400000 + index * 10 + 5, workflow, broken_job, f"mix-latest-{index:02d}", 1, Conclusion.FAILURE, base + 6, "AssertionError cache eviction expected 2 got 3", (broken_file,)),
        _attempt(400000 + index * 10 + 2, workflow, flaky_job, flaky_head, 1, Conclusion.FAILURE, base + 8, "integration timeout waiting for redis", ("tests/test_cache.py",)),
        _attempt(400000 + index * 10 + 3, workflow, flaky_job, flaky_head, 2, Conclusion.SUCCESS, base + 12, "integration completed", ("tests/test_cache.py",)),
        _attempt(400000 + index * 10 + 4, workflow, clean_job, f"mix-clean-{index:02d}", 1, Conclusion.SUCCESS, base + 16, "lint passed"),
    )
    commits = _commits(broken_head, f"mixed-{index:02d}", base, broken_file) + (
        CommitRecord(
            sha=flaky_head,
            committed_at=f"2026-08-{1 + base // 1440:02d}T{(base // 60) % 24:02d}:10:00Z",
            message="parallelize cache integration setup",
            changed_files=("tests/test_cache.py",),
        ),
    )
    return BenchmarkHistory(
        history_id=f"mixed-{index:02d}",
        category="mixed",
        attempts=attempts,
        commits=commits,
        expected={
            broken_key: Classification.CONSISTENTLY_BROKEN,
            flaky_key: Classification.FLAKY,
            clean_key: Classification.CLEAN,
        },
        culprit={broken_key: broken_head, flaky_key: None, clean_key: None},
    )


def negative_control_history() -> BenchmarkHistory:
    """A plausible vocabulary match without head-SHA or recovery evidence."""
    workflow = "CONTROL/weak-evidence"
    job_key = f"{workflow} / job"
    attempts = (
        _attempt(
            900000,
            workflow,
            "job",
            "control-head",
            1,
            Conclusion.FAILURE,
            1200,
            "cache eviction timeout was not captured",
            ("tests/test_cache.py",),
        ),
    )
    commits = (
        CommitRecord(
            sha="control-distractor",
            committed_at="2026-08-01T21:00:00Z",
            message="improve cache eviction timeout guidance",
            changed_files=("tests/test_cache.py",),
        ),
        CommitRecord(
            sha="control-old",
            committed_at="2026-08-01T20:00:00Z",
            message="update unrelated documentation",
            changed_files=("docs/operations.md",),
        ),
    )
    return BenchmarkHistory(
        history_id="negative-control-weak-evidence",
        category="negative_control",
        attempts=attempts,
        commits=commits,
        expected={job_key: Classification.CONSISTENTLY_BROKEN},
        culprit={job_key: None},
    )


def generate_holdout() -> tuple[BenchmarkHistory, ...]:
    histories: list[BenchmarkHistory] = []
    for category in ("deterministic", "flaky", "infrastructure", "cancelled"):
        histories.extend(_single_history(index, category) for index in range(12))
    histories.extend(_mixed_history(index) for index in range(12))
    return tuple(histories)


def canonical_fixture_bytes(histories: tuple[BenchmarkHistory, ...] | None = None) -> bytes:
    histories = generate_holdout() if histories is None else histories
    payload = []
    for history in histories:
        payload.append(
            {
                "history_id": history.history_id,
                "category": history.category,
                "attempts": [
                    {
                        "run_id": item.run_id,
                        "workflow": item.workflow,
                        "job_name": item.job_name,
                        "head_sha": item.head_sha,
                        "attempt": item.attempt,
                        "conclusion": item.conclusion.value,
                        "started_at": item.started_at,
                        "log_excerpt": item.log_excerpt,
                        "touched_files": list(item.touched_files),
                    }
                    for item in history.attempts
                ],
                "expected": {key: value.value for key, value in sorted(history.expected.items())},
                "culprit": dict(sorted(history.culprit.items())),
            }
        )
    return json.dumps({"spec_version": SPEC_VERSION, "histories": payload}, sort_keys=True, separators=(",", ":")).encode()


def fixture_hash(histories: tuple[BenchmarkHistory, ...] | None = None) -> str:
    return hashlib.sha256(canonical_fixture_bytes(histories)).hexdigest()
