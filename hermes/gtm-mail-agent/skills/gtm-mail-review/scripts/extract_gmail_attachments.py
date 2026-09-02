#!/usr/bin/env python3
"""Extract attachments from a persisted Gmail RAW get_message result.

Usage:
    python3 extract_gmail_attachments.py <persisted-result.json-or-txt> [output-dir]

The input is the file the Gmail MCP tool writes when a RAW get_message result
exceeds the tool-output cap (JSON with a base64url `raw` field). Attachments
are written to output-dir (default: current directory). Prints one line per
attachment: filename and byte size.
"""
import base64
import email
import json
import os
import sys
from email import policy


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    src = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    os.makedirs(out_dir, exist_ok=True)

    with open(src) as f:
        data = json.load(f)
    raw = data["raw"] if isinstance(data, dict) else data
    # base64url with tolerant padding
    msg_bytes = base64.urlsafe_b64decode(raw + "==")
    msg = email.message_from_bytes(msg_bytes, policy=policy.default)

    count = 0
    for part in msg.walk():
        fn = part.get_filename()
        if not fn:
            continue
        payload = part.get_payload(decode=True)
        if payload is None:
            continue
        safe = fn.replace("/", "_").replace("\\", "_")
        path = os.path.join(out_dir, safe)
        with open(path, "wb") as out:
            out.write(payload)
        print(f"{safe}\t{len(payload)} bytes")
        count += 1
    if count == 0:
        print("no attachments found", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
