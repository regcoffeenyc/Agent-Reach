from pathlib import Path

import pytest

from repurpose.cli import main, write_outputs
from repurpose.config import Profile
from repurpose.pipeline import run

PROFILE = Path(__file__).parent.parent / "profiles" / "example.yaml"
SOURCE = Path(__file__).parent.parent / "samples" / "source.md"


class ScriptedModel:
    """Returns queued responses in order, recording what it was asked."""

    def __init__(self, *responses: str) -> None:
        self.responses = list(responses)
        self.prompts: list[str] = []

    def complete(self, system, prompt, max_tokens=4000):
        self.prompts.append(prompt)
        return self.responses.pop(0) if self.responses else "fallback draft"


def test_profile_loads_and_merges_banned_phrases():
    profile = Profile.load(PROFILE)
    assert profile.client == "Northwind Logistics"
    linkedin = next(c for c in profile.channels if c.name == "linkedin_post")
    # global list plus the built-in defaults
    assert "revolutionize" in linkedin.rules["banned_phrases"]
    assert "delve" in linkedin.rules["banned_phrases"]


def test_profile_rejects_missing_keys(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text("client: X\nvoice: Y\n")
    with pytest.raises(ValueError, match="missing required keys"):
        Profile.load(bad)


def test_failed_draft_triggers_a_repair_attempt():
    profile = Profile.load(PROFILE)
    channel = next(c for c in profile.channels if c.name == "seo_meta")
    from repurpose.pipeline import run_channel

    # First response fabricates a number; second is clean.
    model = ScriptedModel(
        "Title: Wait times cut 99%\nDescription: A look at the pilot.",
        "Title: Dock waits cut 46%\nDescription: What 18 months of data showed.",
    )
    draft = run_channel(model, profile, channel, SOURCE.read_text(), max_attempts=2)

    assert draft.attempts == 2
    assert draft.scorecard.passed
    assert "failed review" in model.prompts[1]


def test_gives_up_after_max_attempts():
    profile = Profile.load(PROFILE)
    channel = next(c for c in profile.channels if c.name == "seo_meta")
    from repurpose.pipeline import run_channel

    model = ScriptedModel("Growth of 99%", "Still 99% growth")
    draft = run_channel(model, profile, channel, SOURCE.read_text(), max_attempts=2)

    assert draft.attempts == 2
    assert not draft.scorecard.passed


def test_run_produces_one_draft_per_channel():
    profile = Profile.load(PROFILE)
    result = run(ScriptedModel(), profile, SOURCE, max_attempts=1)
    assert [d.channel for d in result.drafts] == [c.name for c in profile.channels]
    # identical fallback text across channels must be caught
    assert result.cross_channel == [] or result.cross_channel[0].check == "duplication"


def test_write_outputs_creates_files_and_scorecard(tmp_path):
    profile = Profile.load(PROFILE)
    result = run(ScriptedModel(), profile, SOURCE, max_attempts=1)
    report = write_outputs(result, tmp_path)

    assert report.exists()
    assert "QA scorecard" in report.read_text()
    for channel in profile.channels:
        slug = "".join(c if c.isalnum() else "-" for c in channel.name.lower())
        assert (tmp_path / f"{slug}.md").exists()


def test_cli_dry_run_exits_nonzero_when_review_fails(tmp_path, capsys):
    code = main(
        [str(SOURCE), "--profile", str(PROFILE), "--out", str(tmp_path), "--dry-run"]
    )
    out = capsys.readouterr().out
    # The stub deliberately fabricates "47%" and uses a banned phrase.
    assert code == 1
    assert "claims_grounded" in out
    assert "banned_phrases" in out
