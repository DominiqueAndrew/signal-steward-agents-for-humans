from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import CommitRecord, JobAttempt, ReplayBundle


class EvidenceStore:
    """Small append-only evidence store; a changed replay row fails closed."""

    def __init__(self, path: str | Path = ":memory:") -> None:
        self.connection = sqlite3.connect(str(path))
        self.connection.row_factory = sqlite3.Row
        self.connection.executescript(
            """
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS job_attempts (
                run_id INTEGER NOT NULL,
                job_name TEXT NOT NULL,
                workflow TEXT NOT NULL,
                head_sha TEXT NOT NULL,
                attempt INTEGER NOT NULL,
                conclusion TEXT NOT NULL,
                started_at TEXT NOT NULL,
                log_excerpt TEXT NOT NULL,
                touched_files_json TEXT NOT NULL,
                evidence_hash TEXT NOT NULL,
                PRIMARY KEY (run_id, job_name)
            );
            CREATE TABLE IF NOT EXISTS commits (
                sha TEXT PRIMARY KEY,
                committed_at TEXT NOT NULL,
                message TEXT NOT NULL,
                changed_files_json TEXT NOT NULL,
                evidence_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_events (
                event_id TEXT PRIMARY KEY,
                subject_id TEXT NOT NULL,
                action TEXT NOT NULL,
                decision TEXT NOT NULL,
                created_at TEXT NOT NULL,
                rationale TEXT NOT NULL
            );
            """
        )
        self.connection.commit()

    @staticmethod
    def _hash(value: dict[str, Any]) -> str:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()

    def _write_attempt(self, attempt: JobAttempt) -> None:
        value = {
            "run_id": attempt.run_id,
            "workflow": attempt.workflow,
            "job_name": attempt.job_name,
            "head_sha": attempt.head_sha,
            "attempt": attempt.attempt,
            "conclusion": attempt.conclusion.value,
            "started_at": attempt.started_at,
            "log_excerpt": attempt.log_excerpt,
            "touched_files": list(attempt.touched_files),
        }
        evidence_hash = self._hash(value)
        existing = self.connection.execute(
            "SELECT evidence_hash FROM job_attempts WHERE run_id = ? AND job_name = ?",
            (attempt.run_id, attempt.job_name),
        ).fetchone()
        if existing and existing["evidence_hash"] != evidence_hash:
            raise ValueError(f"immutable evidence conflict for run {attempt.run_id} job {attempt.job_name}")
        self.connection.execute(
            """
            INSERT OR IGNORE INTO job_attempts
            (run_id, job_name, workflow, head_sha, attempt, conclusion, started_at,
             log_excerpt, touched_files_json, evidence_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                attempt.run_id,
                attempt.job_name,
                attempt.workflow,
                attempt.head_sha,
                attempt.attempt,
                attempt.conclusion.value,
                attempt.started_at,
                attempt.log_excerpt,
                json.dumps(attempt.touched_files),
                evidence_hash,
            ),
        )

    def _write_commit(self, commit: CommitRecord) -> None:
        value = {
            "sha": commit.sha,
            "committed_at": commit.committed_at,
            "message": commit.message,
            "changed_files": list(commit.changed_files),
        }
        evidence_hash = self._hash(value)
        existing = self.connection.execute(
            "SELECT evidence_hash FROM commits WHERE sha = ?", (commit.sha,)
        ).fetchone()
        if existing and existing["evidence_hash"] != evidence_hash:
            raise ValueError(f"immutable evidence conflict for commit {commit.sha}")
        self.connection.execute(
            """
            INSERT OR IGNORE INTO commits
            (sha, committed_at, message, changed_files_json, evidence_hash)
            VALUES (?, ?, ?, ?, ?)
            """,
            (commit.sha, commit.committed_at, commit.message, json.dumps(commit.changed_files), evidence_hash),
        )

    def write_bundle(self, bundle: ReplayBundle) -> None:
        for attempt in bundle.attempts:
            self._write_attempt(attempt)
        for commit in bundle.commits:
            self._write_commit(commit)
        self.connection.commit()

    def append_decision(self, event_id: str, subject_id: str, action: str, decision: str, rationale: str) -> None:
        created_at = datetime.now(timezone.utc).isoformat()
        self.connection.execute(
            "INSERT INTO audit_events (event_id, subject_id, action, decision, created_at, rationale) VALUES (?, ?, ?, ?, ?, ?)",
            (event_id, subject_id, action, decision, created_at, rationale),
        )
        self.connection.commit()

    def audit_events(self) -> list[dict[str, Any]]:
        rows = self.connection.execute("SELECT * FROM audit_events ORDER BY created_at").fetchall()
        return [dict(row) for row in rows]

    def close(self) -> None:
        self.connection.close()

