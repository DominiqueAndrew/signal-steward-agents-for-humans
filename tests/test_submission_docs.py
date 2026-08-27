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
