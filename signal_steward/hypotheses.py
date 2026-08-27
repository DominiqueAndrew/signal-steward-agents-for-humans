from __future__ import annotations

import re
from dataclasses import dataclass

from .models import CommitRecord, JobAttempt

_TOKEN = re.compile(r"[a-z0-9_]{3,}")


@dataclass(frozen=True)
class CulpritHypothesis:
    commit_sha: str
    score: float
    supporting: tuple[str, ...]
    contradicting: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "commit_sha": self.commit_sha,
            "score": round(self.score, 4),
            "supporting": list(self.supporting),
            "contradicting": list(self.contradicting),
        }


def _tokens(value: str) -> set[str]:
    return set(_TOKEN.findall(value.lower()))


def rank_culprits(
    failed_attempts: tuple[JobAttempt, ...] | list[JobAttempt],
    commits: tuple[CommitRecord, ...] | list[CommitRecord],
    *,
    limit: int = 3,
) -> tuple[CulpritHypothesis, ...]:
    """Rank evidence-backed hypotheses; this intentionally does not claim causality."""

    if not failed_attempts or not commits:
        return ()
    latest_failure = max(failed_attempts, key=lambda item: (item.started_at, item.run_id))
    log_tokens = _tokens(latest_failure.log_excerpt) | _tokens(" ".join(latest_failure.touched_files))
    ordered = sorted(commits, key=lambda item: item.committed_at, reverse=True)
    hypotheses: list[CulpritHypothesis] = []
    total = max(len(ordered), 1)
    for index, commit in enumerate(ordered):
        commit_tokens = _tokens(commit.message) | _tokens(" ".join(commit.changed_files))
        overlap = len(log_tokens & commit_tokens) / max(len(log_tokens), 1)
        head_match = commit.sha == latest_failure.head_sha
        recency = 1 - (index / total)
        score = min(1.0, 0.55 * float(head_match) + 0.30 * overlap + 0.15 * recency)
        supporting: list[str] = []
        contradicting: list[str] = []
        if head_match:
            supporting.append("commit is the exact head SHA of the latest failing attempt")
        if overlap:
            matching = sorted(log_tokens & commit_tokens)
            supporting.append(f"failure evidence overlaps commit vocabulary: {', '.join(matching[:5])}")
        if not head_match:
            contradicting.append("commit is not the failing attempt's head SHA")
        if not overlap:
            contradicting.append("no token overlap with the captured failure excerpt or touched files")
        hypotheses.append(
            CulpritHypothesis(
                commit_sha=commit.sha,
                score=score,
                supporting=tuple(supporting),
                contradicting=tuple(contradicting),
            )
        )
    return tuple(sorted(hypotheses, key=lambda item: (-item.score, item.commit_sha))[:limit])

