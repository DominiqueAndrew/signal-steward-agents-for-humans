from __future__ import annotations

import uuid
from dataclasses import dataclass

from .classifier import JobSignal, classify_jobs
from .hypotheses import CulpritHypothesis, rank_culprits
from .models import Conclusion, ReplayBundle
from .policy import ReviewItem, build_review_queue
from .store import EvidenceStore


@dataclass(frozen=True)
class AnalysisReport:
    source_hash: str
    signals: tuple[JobSignal, ...]
    hypotheses: dict[str, tuple[CulpritHypothesis, ...]]
    review_queue: tuple[ReviewItem, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "source_hash": self.source_hash,
            "signals": [signal.to_dict() for signal in self.signals],
            "hypotheses": {
                job_key: [hypothesis.to_dict() for hypothesis in values]
                for job_key, values in sorted(self.hypotheses.items())
            },
            "review_queue": [item.to_dict() for item in self.review_queue],
        }


class SignalSteward:
    def __init__(self, store: EvidenceStore) -> None:
        self.store = store

    def analyze(self, bundle: ReplayBundle) -> AnalysisReport:
        self.store.write_bundle(bundle)
        signals = classify_jobs(bundle.attempts)
        hypotheses: dict[str, tuple[CulpritHypothesis, ...]] = {}
        for signal in signals:
            failed = tuple(
                attempt
                for attempt in bundle.attempts
                if attempt.job_key == signal.job_key and attempt.conclusion == Conclusion.FAILURE
            )
            hypotheses[signal.job_key] = rank_culprits(failed, bundle.commits)
        return AnalysisReport(
            source_hash=bundle.source_hash,
            signals=signals,
            hypotheses=hypotheses,
            review_queue=build_review_queue(signals, hypotheses),
        )

    def record_human_decision(self, item: ReviewItem, decision: str, rationale: str) -> str:
        """Persist the decision only; this method has no external side effects."""

        if decision not in {"approve", "hold"}:
            raise ValueError("decision must be 'approve' or 'hold'")
        event_id = str(uuid.uuid4())
        self.store.append_decision(event_id, item.item_id, item.action.value, decision, rationale)
        return event_id

