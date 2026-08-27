from __future__ import annotations

from typing import Any, Callable

from .service import SignalSteward

STRANDS_SDK_VERSION = "1.53.0"


def read_only_tool_names() -> tuple[str, ...]:
    return ("inspect_window", "explain_signal", "prepare_review_packet")


def read_only_contract() -> dict[str, object]:
    """Describe the registered agent boundary without invoking a provider."""
    return {
        "sdk": "Strands Agents SDK",
        "sdk_version": STRANDS_SDK_VERSION,
        "tools": list(read_only_tool_names()),
        "side_effects": [],
        "invocation": "optional; provider-configured",
    }


def make_read_only_tools(service: SignalSteward) -> tuple[Callable[..., Any], ...]:
    """Create the Strands tool boundary; every tool reads the local evidence store."""

    try:
        from strands import tool
    except ModuleNotFoundError as exc:  # pragma: no cover - dependency is pinned in the project
        raise RuntimeError("install the pinned strands-agents dependency to enable the agent adapter") from exc

    @tool
    def inspect_window() -> dict[str, object]:
        """Read the current evidence window and return no-mutation metadata."""

        rows = service.store.connection.execute(
            "SELECT COUNT(*) AS attempts, COUNT(DISTINCT head_sha) AS shas FROM job_attempts"
        ).fetchone()
        return {"attempts": rows["attempts"], "distinct_shas": rows["shas"], "read_only": True}

    @tool
    def explain_signal(job_key: str) -> dict[str, object]:
        """Read stored attempt evidence for one workflow and job key."""

        workflow, separator, job_name = job_key.partition(" / ")
        if not separator:
            return {"error": "job_key must be formatted as 'workflow / job'", "read_only": True}
        rows = service.store.connection.execute(
            """
            SELECT run_id, head_sha, attempt, conclusion, started_at, log_excerpt
            FROM job_attempts WHERE workflow = ? AND job_name = ? ORDER BY started_at
            """,
            (workflow, job_name),
        ).fetchall()
        return {"job_key": job_key, "attempts": [dict(row) for row in rows], "read_only": True}

    @tool
    def prepare_review_packet(job_key: str) -> dict[str, object]:
        """Prepare a human-review handoff without opening an issue or changing CI."""

        return {
            "job_key": job_key,
            "next_step": "load the local replay and review the deterministic analysis",
            "human_required": True,
            "side_effects": [],
            "read_only": True,
        }

    return inspect_window, explain_signal, prepare_review_packet


def build_strands_agent(service: SignalSteward, *, model: Any | None = None) -> Any:
    """Build a real Strands Agent; invocation remains opt-in and provider-configured."""

    try:
        from strands import Agent
    except ModuleNotFoundError as exc:  # pragma: no cover - dependency is pinned in the project
        raise RuntimeError("install the pinned strands-agents dependency to enable the agent adapter") from exc

    kwargs: dict[str, Any] = {
        "name": "signal_steward",
        "system_prompt": (
            "You are Signal Steward. Use only the read-only evidence tools. "
            "Do not claim causal certainty. Surface a concise human decision only "
            "when the evidence packet is sufficient; otherwise say insufficient evidence."
        ),
        "tools": list(make_read_only_tools(service)),
    }
    if model is not None:
        kwargs["model"] = model
    return Agent(**kwargs)
