#!/usr/bin/env python3
"""Extract attachments from a persisted Gmail RAW get_message result.

Usage:
    python3 extract_gmail_attachments.py <persisted-result.json-or-txt> [output-dir]

The input is the file the Gmail MCP tool writes when a RAW get_message result
exceeds the tool-output cap (JSON with a base64url `raw` field). Attachments
are written to output-dir (default: current directory). Prints one line per
attachment: filename and byte size.

Attachment names come from the sender and are hostile input. Every name is
reduced to a safe basename (no directories, no leading dot, printable ASCII
only) and an existing file is never overwritten.
"""
import base64
import email
import json
import os
import re
import sys
from email import policy

_UNSAFE = re.compile(r"[^A-Za-z0-9._ -]")
_MAX_NAME = 120


def safe_name(raw_name: str, fallback: str) -> str:
    """Reduce a sender-supplied filename to a safe basename."""
    name = raw_name.replace("\\", "/")
    name = os.path.basename(name)           # drops any directory component
    name = _UNSAFE.sub("_", name)           # printable ASCII subset only
    name = name.lstrip(". ").strip()        # no dotfiles, no leading spaces
    if not name or name in {".", ".."}:
        name = fallback
    return name[:_MAX_NAME]


def unique_path(out_dir: str, name: str) -> str:
    """Return a path in out_dir that does not exist yet."""
    base, ext = os.path.splitext(name)
    candidate = os.path.join(out_dir, name)
    n = 1
    while os.path.lexists(candidate):
        candidate = os.path.join(out_dir, f"{base}({n}){ext}")
        n += 1
    return candidate


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    src = sys.argv[1]
    out_dir = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else ".")
    os.makedirs(out_dir, exist_ok=True)

    with open(src) as f:
        data = json.load(f)
    raw = data["raw"] if isinstance(data, dict) else data
    # base64url with tolerant padding
    msg_bytes = base64.urlsafe_b64decode(raw + "==")
    msg = email.message_from_bytes(msg_bytes, policy=policy.default)

    count = 0
    for idx, part in enumerate(msg.walk()):
        fn = part.get_filename()
        if not fn:
            continue
        payload = part.get_payload(decode=True)
        if payload is None:
            continue
        name = safe_name(fn, f"attachment-{idx}.bin")
        path = unique_path(out_dir, name)
        # O_EXCL: fail rather than overwrite if something raced us.
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as out:
            out.write(payload)
        print(f"{os.path.basename(path)}\t{len(payload)} bytes")
        count += 1
    if count == 0:
        print("no attachments found", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
