"""Command line entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import Profile
from .llm import get_model
from .pipeline import Result, run
from .qa import reading_grade

TICK, CROSS, WARN = "PASS", "FAIL", "WARN"


def _slug(name: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")


def write_outputs(result: Result, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    for draft in result.drafts:
        (out_dir / f"{_slug(draft.channel)}.md").write_text(
            draft.text + "\n", encoding="utf-8"
        )

    lines = [
        "# QA scorecard",
        "",
        f"Source: `{result.source_path}`",
        f"Result: **{'PASS' if result.passed else 'FAIL'}**",
        "",
        "| Channel | Status | Attempts | Chars | Grade | Failures | Warnings |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for d in result.drafts:
        lines.append(
            f"| {d.channel} | {'PASS' if d.scorecard.passed else 'FAIL'} "
            f"| {d.attempts} | {len(d.text)} | {reading_grade(d.text)} "
            f"| {len(d.scorecard.failures)} | {len(d.scorecard.warnings)} |"
        )

    for d in result.drafts:
        if not d.scorecard.findings:
            continue
        lines += ["", f"## {d.channel}", ""]
        for f in d.scorecard.findings:
            lines.append(f"- **{f.severity.upper()}** ({f.check}) {f.message}")
            if f.evidence:
                lines.append(f"  - `{f.evidence}`")

    if result.cross_channel:
        lines += ["", "## Cross-channel", ""]
        for f in result.cross_channel:
            lines.append(f"- **WARN** ({f.check}) {f.message}")
            if f.evidence:
                lines.append(f"  - `{f.evidence}`")

    report = out_dir / "scorecard.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="repurpose",
        description="Turn one source document into reviewed multi-channel content.",
    )
    p.add_argument("source", help="path to the source article, transcript, or notes")
    p.add_argument("--profile", required=True, help="client profile YAML")
    p.add_argument("--out", default="dist", help="output directory (default: dist)")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="use the offline stub model — no API key needed",
    )
    p.add_argument(
        "--max-attempts",
        type=int,
        default=2,
        help="rewrite attempts per channel before giving up (default: 2)",
    )
    p.add_argument(
        "--effort",
        default="medium",
        choices=["low", "medium", "high", "xhigh", "max"],
        help="model effort (default: medium)",
    )
    args = p.parse_args(argv)

    profile = Profile.load(args.profile)
    model = get_model(args.dry_run, effort=args.effort)
    result = run(model, profile, args.source, max_attempts=args.max_attempts)
    report = write_outputs(result, Path(args.out))

    for d in result.drafts:
        status = TICK if d.scorecard.passed else CROSS
        print(f"[{status}] {d.channel:<24} {len(d.text):>5} chars, {d.attempts} attempt(s)")
        for f in d.scorecard.findings:
            mark = CROSS if f.severity == "fail" else WARN
            print(f"        [{mark}] {f.check}: {f.message}")
    for f in result.cross_channel:
        print(f"[{WARN}] cross-channel: {f.message}")

    print(f"\nDrafts and scorecard written to {report.parent}/")
    if not result.passed:
        print("Review failed — nothing here is ready to publish.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
