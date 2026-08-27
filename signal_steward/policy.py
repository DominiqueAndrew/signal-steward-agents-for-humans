from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .classifier import JobSignal
from .hypotheses import CulpritHypothesis
from .models import Classification, ReviewAction


@dataclass(frozen=True)
class ReviewItem:
    item_id: str
    job_key: str
    action: ReviewAction
    confidence: float
    summary: str
    evidence: tuple[str, ...]
    human_required: bool = True

    def to_dict(self) -> dict[str, object]:
        return {
            "item_id": self.item_id,
            "job_key": self.job_key,
            "action": self.action.value,
            "confidence": round(self.confidence, 4),
            "summary": self.summary,
            "evidence": list(self.evidence),
            "human_required": self.human_required,
            "side_effect_boundary": "read-only analysis; no CI, issue, quarantine, or merge mutation",
        }


def build_review_queue(
    signals: tuple[JobSignal, ...],
    hypotheses: dict[str, tuple[CulpritHypothesis, ...]],
) -> tuple[ReviewItem, ...]:
    queue: list[ReviewItem] = []
    for signal in signals:
        top = hypotheses.get(signal.job_key, ())
        evidence = list(signal.evidence)
        # Keep weak global matches in the diagnostic report, but do not surface
        # them as a review explanation. A low score is not useful evidence.
        if top and top[0].score >= 0.70:
            evidence.append(f"top hypothesis {top[0].commit_sha} scores {top[0].score:.2f}; hypothesis only")

        if signal.classification == Classification.FLAKY and signal.recovery_groups:
            action = ReviewAction.QUARANTINE_CANDIDATE
            confidence = min(0.95, 0.65 + 0.10 * signal.recovery_rate)
            summary = "Repeated same-SHA recovery suggests an intermittent signal; decide whether to quarantine it."
        elif signal.classification == Classification.CONSISTENTLY_BROKEN and top and top[0].score >= 0.70:
            action = ReviewAction.INVESTIGATE_REGRESSION
            confidence = top[0].score
            summary = "The failure is persistent and has a strong evidence-backed change hypothesis; investigate before shipping."
        elif signal.failure_count:
            action = ReviewAction.INSUFFICIENT_EVIDENCE
            confidence = 0.30
            summary = "A failure exists, but the evidence is insufficient for a safe next-action recommendation."
        else:
            continue

        item_id = hashlib.sha256(f"{signal.job_key}:{action.value}".encode()).hexdigest()[:12]
        queue.append(
            ReviewItem(
                item_id=item_id,
                job_key=signal.job_key,
                action=action,
                confidence=confidence,
                summary=summary,
                evidence=tuple(evidence),
            )
        )
    return tuple(queue)
