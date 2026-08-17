"""Deterministic quality gate for AI-generated content.

Every check here runs without an API key. That is the point: the model
drafts, but nothing ships until code that cannot hallucinate has signed off.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class Finding:
    check: str
    severity: str  # "fail" | "warn"
    message: str
    evidence: str = ""


@dataclass
class Scorecard:
    channel: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def failures(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "fail"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warn"]

    @property
    def passed(self) -> bool:
        return not self.failures


# Any number a reader would treat as a factual claim: bare integers
# ("94 minutes"), thousands separators, decimals, percentages, currency, and
# k/M/B suffixes. Bare integers matter — "94 minutes" silently becoming
# "84 minutes" is exactly the error this gate exists to catch.
_CLAIM = re.compile(
    r"""
    (?<![\w.,])            # never restart in the middle of a number or word
    (?:[$£€])?             # optional currency symbol
    \d+(?:,\d{3})*(?:\.\d+)?
    (?:\s?%|[kKmMbB]\b)?   # optional percent or magnitude suffix
    """,
    re.VERBOSE,
)

# "1." or "2)" opening a line is a list marker, not a claim.
_LIST_MARKER = re.compile(r"^\s*\d{1,2}[.)]\s")

_SENTENCE = re.compile(r"[^.!?\n]+[.!?]?")
_WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")
_VOWEL_RUN = re.compile(r"[aeiouy]+")


def _normalise_number(raw: str) -> str:
    """Strip formatting so '1,200' and '1200' compare equal."""
    return re.sub(r"[,\s$£€]", "", raw).lower()


def extract_claims(text: str) -> list[str]:
    """Numeric claims a reader would take as fact, minus list markers."""
    claims = []
    for match in _CLAIM.finditer(text):
        line_start = text.rfind("\n", 0, match.start()) + 1
        if _LIST_MARKER.match(text[line_start : match.end() + 2]):
            continue
        claims.append(match.group(0).strip())
    return claims


def check_claims_grounded(draft: str, source: str) -> list[Finding]:
    """Every number in the draft must appear in the source material.

    This is the check that catches the failure mode clients actually fear:
    a confident, well-written paragraph containing a statistic the model
    invented.
    """
    source_numbers = {_normalise_number(c) for c in extract_claims(source)}
    findings: list[Finding] = []
    seen: set[str] = set()
    for claim in extract_claims(draft):
        key = _normalise_number(claim)
        if key in source_numbers or key in seen:
            continue
        seen.add(key)
        findings.append(
            Finding(
                check="claims_grounded",
                severity="fail",
                message=f"'{claim}' does not appear in the source material",
                evidence=_context(draft, claim),
            )
        )
    return findings


def check_banned_phrases(draft: str, banned: Iterable[str]) -> list[Finding]:
    lowered = draft.lower()
    findings = []
    for phrase in banned:
        needle = phrase.lower()
        if needle in lowered:
            findings.append(
                Finding(
                    check="banned_phrases",
                    severity="fail",
                    message=f"contains banned phrase '{phrase}'",
                    evidence=_context(draft, phrase),
                )
            )
    return findings


def check_length(draft: str, min_chars: int | None, max_chars: int | None) -> list[Finding]:
    n = len(draft.strip())
    findings = []
    if min_chars is not None and n < min_chars:
        findings.append(
            Finding("length", "fail", f"{n} chars, minimum is {min_chars}")
        )
    if max_chars is not None and n > max_chars:
        findings.append(
            Finding("length", "fail", f"{n} chars, maximum is {max_chars}")
        )
    return findings


def check_required(draft: str, required: Iterable[str]) -> list[Finding]:
    lowered = draft.lower()
    return [
        Finding("required", "fail", f"missing required element '{item}'")
        for item in required
        if item.lower() not in lowered
    ]


def _syllables(word: str) -> int:
    word = word.lower().rstrip("e")
    return max(1, len(_VOWEL_RUN.findall(word)))


def reading_grade(text: str) -> float:
    """Flesch-Kincaid grade level. Approximate by design — it is a tripwire,
    not a metric anyone should optimise."""
    sentences = [s for s in _SENTENCE.findall(text) if s.strip()]
    words = _WORD.findall(text)
    if not sentences or not words:
        return 0.0
    syllables = sum(_syllables(w) for w in words)
    return round(
        0.39 * (len(words) / len(sentences))
        + 11.8 * (syllables / len(words))
        - 15.59,
        1,
    )


def check_readability(draft: str, max_grade: float | None) -> list[Finding]:
    if max_grade is None:
        return []
    grade = reading_grade(draft)
    if grade > max_grade:
        return [
            Finding(
                "readability",
                "warn",
                f"reading grade {grade}, target is {max_grade} or below",
            )
        ]
    return []


def check_cross_channel_duplication(
    drafts: dict[str, str], window: int = 8
) -> list[Finding]:
    """Catch the same sentence copy-pasted across channels.

    Repurposing that reuses verbatim runs reads as automated the moment a
    reader follows two of the client's accounts.
    """
    seen: dict[tuple[str, ...], str] = {}
    findings: list[Finding] = []
    for channel, text in drafts.items():
        words = _WORD.findall(text.lower())
        for i in range(len(words) - window + 1):
            gram = tuple(words[i : i + window])
            origin = seen.get(gram)
            if origin is None:
                seen[gram] = channel
            elif origin != channel:
                findings.append(
                    Finding(
                        "duplication",
                        "warn",
                        f"shares {window}+ words verbatim with '{origin}'",
                        evidence=" ".join(gram),
                    )
                )
                break
    return findings


def _context(text: str, needle: str, width: int = 40) -> str:
    idx = text.lower().find(needle.lower())
    if idx < 0:
        return ""
    start = max(0, idx - width)
    end = min(len(text), idx + len(needle) + width)
    return ("…" if start else "") + text[start:end].replace("\n", " ") + ("…" if end < len(text) else "")


def review(channel: str, draft: str, source: str, rules: dict) -> Scorecard:
    """Run every gate for one channel."""
    card = Scorecard(channel=channel)
    card.findings += check_claims_grounded(draft, source)
    card.findings += check_banned_phrases(draft, rules.get("banned_phrases", []))
    card.findings += check_length(draft, rules.get("min_chars"), rules.get("max_chars"))
    card.findings += check_required(draft, rules.get("required", []))
    card.findings += check_readability(draft, rules.get("max_reading_grade"))
    return card
