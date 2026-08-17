"""Model access, with a deterministic stub so the pipeline is demoable
without an API key."""

from __future__ import annotations

import os
import textwrap
from typing import Protocol

MODEL = "claude-opus-5"


class Model(Protocol):
    def complete(self, system: str, prompt: str, max_tokens: int = 4000) -> str: ...


class ClaudeModel:
    """Thin wrapper over the Anthropic SDK.

    Streams so long generations don't trip the SDK's HTTP timeout, and leaves
    adaptive thinking on — the drafting step benefits from it and the cost is
    small next to a rewrite.
    """

    def __init__(self, model: str = MODEL, effort: str = "medium") -> None:
        import anthropic  # imported lazily so --dry-run needs no SDK

        self._client = anthropic.Anthropic()
        self._model = model
        self._effort = effort

    def complete(self, system: str, prompt: str, max_tokens: int = 4000) -> str:
        with self._client.messages.stream(
            model=self._model,
            max_tokens=max_tokens,
            system=system,
            thinking={"type": "adaptive"},
            output_config={"effort": self._effort},
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            message = stream.get_final_message()

        if message.stop_reason == "refusal":
            raise RuntimeError(
                "model declined this request "
                f"({getattr(message.stop_details, 'category', 'unknown')})"
            )
        return "".join(b.text for b in message.content if b.type == "text").strip()


class StubModel:
    """Offline stand-in.

    Deliberately imperfect: it echoes source sentences verbatim across
    channels and injects a fabricated statistic, so `--dry-run` demonstrates
    the QA gate catching real failure modes rather than rubber-stamping.
    """

    def complete(self, system: str, prompt: str, max_tokens: int = 4000) -> str:
        body = prompt.split("SOURCE MATERIAL:", 1)[-1].strip()
        first = textwrap.shorten(body, width=280, placeholder="…")
        return (
            f"{first}\n\n"
            "Teams adopting this approach report a 47% improvement in "
            "turnaround, which is why it's important to note the shift.\n\n"
            "Read the full write-up at example.com/post"
        )


def get_model(dry_run: bool, effort: str = "medium") -> Model:
    if dry_run:
        return StubModel()
    if not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")):
        raise SystemExit(
            "No credentials found. Export ANTHROPIC_API_KEY, run `ant auth login`,\n"
            "or pass --dry-run to exercise the pipeline offline."
        )
    return ClaudeModel(effort=effort)
