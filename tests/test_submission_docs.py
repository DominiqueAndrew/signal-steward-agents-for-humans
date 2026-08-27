import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_submission_materials_require_a_public_demo_video() -> None:
    draft = (REPO_ROOT / "docs" / "DEVPOST_DRAFT.md").read_text()
    packet = (REPO_ROOT / "docs" / "HUMAN_GATE_PACKET.md").read_text()
    receipt = (REPO_ROOT / "docs" / "RELEASE_RECEIPT.md").read_text()

    assert "public YouTube/Vimeo URL" in draft
    assert "public YouTube/Vimeo video URL" in packet
    assert "An unlisted video" in packet
    assert "does not satisfy the current official rules." in packet
    assert "public ≤5-minute YouTube/Vimeo demo" in receipt
    assert "public or unlisted" not in packet
    assert "public/unlisted" not in packet
    assert "public or unlisted" not in draft
    assert "public/unlisted" not in draft
    assert "Join hackathon" in packet
    assert "submissions_open" not in packet
    assert "Technical Implementation" in packet
    assert "Technological Implementation" not in packet
    assert "Technical Implementation" in draft
    assert "Technological Implementation" not in draft


def test_judge_materials_keep_referenced_artifacts_and_demo_budget() -> None:
    readme = (REPO_ROOT / "README.md").read_text()
    draft = (REPO_ROOT / "docs" / "DEVPOST_DRAFT.md").read_text()
    demo = (REPO_ROOT / "docs" / "demo-script.md").read_text()
    architecture = (REPO_ROOT / "docs" / "architecture.md").read_text()
    architecture_diagram = (REPO_ROOT / "docs" / "architecture-diagram.svg").read_text()
    results = (REPO_ROOT / "RESULTS.md").read_text()

    referenced_artifacts = (
        "docs/architecture-diagram.png",
        "docs/architecture.md",
        "docs/demo-script.md",
        "docs/PUBLIC_CASES.md",
        "docs/RELEASE_RECEIPT.md",
        "RESEARCH.md",
        "RESULTS.md",
        "signal-steward-threat-model.md",
    )
    for relative_path in referenced_artifacts:
        assert (REPO_ROOT / relative_path).is_file(), relative_path

    assert "Run of show (under five minutes)" in demo
    assert "4:20–4:50" in demo
    assert "CI failures are not decisions." in draft
    assert "A maintainer still has to decide" in draft
    assert "reduction in review items" in draft
    assert "architecture-diagram.png" in readme
    assert "optional Strands agent adapter" in architecture
    assert "Optional Strands Agent" in architecture
    assert "asks a Strands agent" not in architecture
    assert "optional provider-configured Strands adapter" in architecture_diagram
    assert "Optional Strands adapter" in architecture_diagram
    assert "The evaluated Signal Steward classifier" in results
    assert "the evaluated Signal Steward ranker" in results
    assert "production classifier" not in results
    assert "production ranker" not in results


def test_release_receipt_preserves_a_recheckable_two_sha_boundary() -> None:
    receipt = (REPO_ROOT / "docs" / "RELEASE_RECEIPT.md").read_text()

    assert re.search(
        r"\*\*Validated release-content tree:\*\* `[0-9a-f]{40}`", receipt
    )
    assert "commit cannot contain its own hash" in receipt
    assert "git ls-remote origin refs/heads/main" in receipt
    assert "public receipt-refresh commit" in receipt
    assert "not the release-content SHA recorded above" in receipt


def test_human_packet_limits_project_age_evidence_to_its_provenance_scope() -> None:
    packet = (REPO_ROOT / "docs" / "HUMAN_GATE_PACKET.md").read_text()

    assert "Observed repository evidence (not a substitute for that confirmation)" in packet
    assert "e354df4c5120d56bc14b1c375feed3f35c0e971e" in packet
    assert "2026-08-27T18:27:04+02:00" in packet
    assert "Git metadata alone" in packet
    assert "cannot prove when underlying work was created" in packet


def test_human_packet_bounds_third_party_review_without_claiming_clearance() -> None:
    packet = (REPO_ROOT / "docs" / "HUMAN_GATE_PACKET.md").read_text()

    assert "Observed inventory to make this review bounded (not legal clearance)" in packet
    assert "strands-agents==1.53.0" in packet
    assert "pytest>=8.3,<9" in packet
    assert "two small, manually normalized JSON fixtures" in packet
    assert "does not settle third-party permissions" in packet
    assert "submission adds original functionality" in packet
    assert "must still review" in packet
    assert "no full transitive lockfile" in packet
    assert "GitHub API HTTP 403" in packet
    assert "anonymous rate" in packet
    assert "limit is exhausted" in packet
    assert 'GITHUB_TOKEN="$(gh auth token)" ./scripts/verify-public-release.sh' in packet
    assert "Never paste" in packet


def test_public_release_verifier_is_read_only_and_covers_judge_artifacts() -> None:
    verifier = (REPO_ROOT / "scripts" / "verify-public-release.sh").read_text()

    assert "git ls-remote" in verifier
    assert "raw_base=\"https://raw.githubusercontent.com/${public_repo}/${public_sha}\"" in verifier
    assert "len(files) >= 300" in verifier
    assert "file list may be truncated" in verifier
    assert "docs/RELEASE_RECEIPT.md" in verifier
    assert "scripts/verify-public-release.sh" in verifier
    assert "image/png" in verifier
    assert "image/svg+xml" in verifier
    assert "visibility" in verifier
    assert "git push" not in verifier
    assert "aws " not in verifier
