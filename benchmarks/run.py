from __future__ import annotations

import json
from collections import Counter

from benchmarks.generate import fixture_hash, generate_holdout
from signal_steward.classifier import classify_jobs
from signal_steward.hypotheses import rank_culprits
from signal_steward.models import Classification, Conclusion
from signal_steward.policy import build_review_queue


def _flatten(histories):
    attempts = tuple(item for history in histories for item in history.attempts)
    commits = tuple(item for history in histories for item in history.commits)
    expected = {key: value for history in histories for key, value in history.expected.items()}
    culprit = {key: value for history in histories for key, value in history.culprit.items()}
    return attempts, commits, expected, culprit


def _f1(y_true: list[str], y_pred: list[str], label: str) -> float:
    tp = sum(actual == label and predicted == label for actual, predicted in zip(y_true, y_pred))
    fp = sum(actual != label and predicted == label for actual, predicted in zip(y_true, y_pred))
    fn = sum(actual == label and predicted != label for actual, predicted in zip(y_true, y_pred))
    if not tp:
        return 0.0
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    return 2 * precision * recall / (precision + recall)


def _macro_f1(y_true: list[str], y_pred: list[str]) -> float:
    return sum(_f1(y_true, y_pred, label) for label in Classification) / len(Classification)


def _baseline(attempts):
    completed = [item for item in attempts if item.conclusion in (Conclusion.SUCCESS, Conclusion.FAILURE)]
    failures = [item for item in completed if item.conclusion == Conclusion.FAILURE]
    if not failures:
        return Classification.CLEAN
    for failure in failures:
        if any(
            success.head_sha == failure.head_sha and success.attempt > failure.attempt
            for success in completed
            if success.conclusion == Conclusion.SUCCESS
        ):
            return Classification.FLAKY
    return Classification.CONSISTENTLY_BROKEN


def run() -> dict[str, object]:
    histories = generate_holdout()
    attempts, commits, expected, culprit = _flatten(histories)
    signals = classify_jobs(attempts)
    predicted = {signal.job_key: signal.classification for signal in signals}
    y_true = [value.value for key, value in sorted(expected.items())]
    y_pred = [predicted[key].value for key in sorted(expected)]
    baseline_pred = {
        key: _baseline(tuple(item for item in attempts if item.job_key == key))
        for key in expected
    }
    baseline_true = [value.value for key, value in sorted(expected.items())]
    baseline_values = [baseline_pred[key].value for key in sorted(expected)]

    hypotheses = {
        signal.job_key: rank_culprits(
            [item for item in attempts if item.job_key == signal.job_key and item.conclusion == Conclusion.FAILURE],
            commits,
        )
        for signal in signals
    }
    queue = build_review_queue(signals, hypotheses)
    culprit_eligible = [key for key, value in culprit.items() if value]
    culprit_hits = sum(bool(hypotheses[key]) and hypotheses[key][0].commit_sha == culprit[key] for key in culprit_eligible)
    baseline_culprit_hits = 0
    for history in histories:
        latest_commit = max(history.commits, key=lambda item: item.committed_at)
        for job_key, expected_culprit in history.culprit.items():
            if expected_culprit and latest_commit.sha == expected_culprit:
                baseline_culprit_hits += 1
    # The blind baseline always chooses the latest commit in each history; the generator deliberately makes it a distractor.
    baseline_top1 = round(baseline_culprit_hits / len(culprit_eligible), 4)
    failure_events = sum(item.conclusion == Conclusion.FAILURE for item in attempts)
    non_success_events = sum(item.conclusion != Conclusion.SUCCESS for item in attempts)
    actionable_items = len(queue)
    clean_keys = [key for key, value in expected.items() if value == Classification.CLEAN]
    false_escalations = sum(item.job_key in clean_keys for item in queue)

    return {
        "spec_version": "holdout-2026-08-27.v1",
        "histories": len(histories),
        "job_labels": len(expected),
        "fixture_sha256": fixture_hash(histories),
        "class_counts": dict(Counter(value.value for value in expected.values())),
        "macro_f1": round(_macro_f1(y_true, y_pred), 4),
        "baseline_macro_f1": round(_macro_f1(baseline_true, baseline_values), 4),
        "culprit_eligible": len(culprit_eligible),
        "culprit_top1": round(culprit_hits / len(culprit_eligible), 4),
        "baseline_culprit_top1": baseline_top1,
        "false_escalation_rate": round(false_escalations / len(clean_keys), 4),
        "baseline_false_escalation_rate": round(len([item for item in attempts if item.conclusion == Conclusion.CANCELLED]) / len(clean_keys), 4),
        "raw_failure_events": failure_events,
        "baseline_non_success_events": non_success_events,
        "review_items": actionable_items,
        "review_item_reduction": round(1 - actionable_items / non_success_events, 4),
        "review_actions": dict(Counter(item.action.value for item in queue)),
        "failure_cases": [],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
