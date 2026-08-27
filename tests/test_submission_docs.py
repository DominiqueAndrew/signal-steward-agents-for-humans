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


def test_judge_materials_keep_referenced_artifacts_and_demo_budget() -> None:
    readme = (REPO_ROOT / "README.md").read_text()
    draft = (REPO_ROOT / "docs" / "DEVPOST_DRAFT.md").read_text()
    demo = (REPO_ROOT / "docs" / "demo-script.md").read_text()

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


def test_release_receipt_preserves_a_recheckable_two_sha_boundary() -> None:
    receipt = (REPO_ROOT / "docs" / "RELEASE_RECEIPT.md").read_text()

    assert re.search(
        r"\*\*Validated release-content tree:\*\* `[0-9a-f]{40}`", receipt
    )
    assert "commit cannot contain its own hash" in receipt
    assert "git ls-remote origin refs/heads/main" in receipt
    assert "public receipt-refresh commit" in receipt
    assert "not the release-content SHA recorded above" in receipt
