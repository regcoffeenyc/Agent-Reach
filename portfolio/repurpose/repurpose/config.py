"""Client profiles: voice, channels, and the rules the QA gate enforces."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

DEFAULT_BANNED = [
    "delve",
    "in today's fast-paced",
    "unlock the power",
    "it's important to note",
    "game-changer",
    "tapestry",
    "navigate the landscape",
    "dive deep",
    "in conclusion",
]


@dataclass
class Channel:
    name: str
    brief: str
    rules: dict[str, Any]


@dataclass
class Profile:
    client: str
    voice: str
    audience: str
    channels: list[Channel]

    @classmethod
    def load(cls, path: str | Path) -> "Profile":
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        missing = {"client", "voice", "audience", "channels"} - data.keys()
        if missing:
            raise ValueError(f"profile missing required keys: {sorted(missing)}")

        # A profile's list extends the built-in defaults; it never replaces
        # them, so adding one client-specific phrase can't silently switch
        # off every other check.
        global_banned = list(DEFAULT_BANNED) + list(data.get("banned_phrases", []))
        channels = []
        for name, spec in data["channels"].items():
            rules = dict(spec.get("rules", {}))
            # Channel-level banned phrases extend the global list, never replace it.
            rules["banned_phrases"] = list(global_banned) + list(
                rules.get("banned_phrases", [])
            )
            channels.append(Channel(name=name, brief=spec["brief"], rules=rules))

        return cls(
            client=data["client"],
            voice=data["voice"],
            audience=data["audience"],
            channels=channels,
        )
