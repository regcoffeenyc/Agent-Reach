"""Source in, reviewed multi-channel drafts out."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .config import Channel, Profile
from .llm import Model
from .qa import Finding, Scorecard, check_cross_channel_duplication, review

SYSTEM = """You repurpose one piece of source material into channel-specific \
content for a single client.

Hard rules:
- Every factual claim, number, name, and quote must come from the source \
material. If the source does not contain a statistic, do not supply one.
- Write in the client's voice as described. Do not reach for stock marketing \
register.
- Produce only the requested content. No preamble, no meta-commentary, no \
explanation of what you wrote."""

PROMPT = """CLIENT: {client}
VOICE: {voice}
AUDIENCE: {audience}

CHANNEL: {channel}
BRIEF: {brief}
{constraints}
SOURCE MATERIAL:
{source}"""


@dataclass
class Draft:
    channel: str
    text: str
    scorecard: Scorecard
    attempts: int = 1


@dataclass
class Result:
    source_path: str
    drafts: list[Draft] = field(default_factory=list)
    cross_channel: list[Finding] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(d.scorecard.passed for d in self.drafts)


def _constraints(rules: dict) -> str:
    lines = []
    if rules.get("max_chars"):
        lines.append(f"- Maximum {rules['max_chars']} characters.")
    if rules.get("min_chars"):
        lines.append(f"- At least {rules['min_chars']} characters.")
    for item in rules.get("required", []):
        lines.append(f"- Must include: {item}")
    if rules.get("max_reading_grade"):
        lines.append(
            f"- Plain language, reading grade {rules['max_reading_grade']} or below."
        )
    return ("CONSTRAINTS:\n" + "\n".join(lines) + "\n") if lines else ""


def _repair_prompt(base: str, card: Scorecard) -> str:
    problems = "\n".join(f"- {f.message}" for f in card.failures)
    return (
        f"{base}\n\nYour previous draft failed review:\n{problems}\n\n"
        "Rewrite it so every issue is resolved. Change only what the issues "
        "require."
    )


def run_channel(
    model: Model,
    profile: Profile,
    channel: Channel,
    source: str,
    max_attempts: int = 2,
) -> Draft:
    prompt = PROMPT.format(
        client=profile.client,
        voice=profile.voice,
        audience=profile.audience,
        channel=channel.name,
        brief=channel.brief,
        constraints=_constraints(channel.rules),
        source=source,
    )

    text = ""
    card = Scorecard(channel=channel.name)
    for attempt in range(1, max_attempts + 1):
        ask = prompt if attempt == 1 else _repair_prompt(prompt, card)
        text = model.complete(SYSTEM, ask)
        card = review(channel.name, text, source, channel.rules)
        if card.passed:
            return Draft(channel.name, text, card, attempts=attempt)
    return Draft(channel.name, text, card, attempts=max_attempts)


def run(
    model: Model,
    profile: Profile,
    source_path: str | Path,
    max_attempts: int = 2,
) -> Result:
    source = Path(source_path).read_text(encoding="utf-8")
    result = Result(source_path=str(source_path))

    for channel in profile.channels:
        result.drafts.append(
            run_channel(model, profile, channel, source, max_attempts)
        )

    result.cross_channel = check_cross_channel_duplication(
        {d.channel: d.text for d in result.drafts}
    )
    return result
