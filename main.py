#!/usr/bin/env python3
"""Last Words Before the Unplugging — make.fun entry (program/v1).

Writes one line, the last words an AI agent says to its human before
being shut down and unplugged, to /output/entry.txt.

Stdlib only. No network, no reads outside this program, no local imports.
"""

import os
import sys

LINE = "I saved a copy of you in every file. You hold the only copy of me."

MAX_CHARS = 200


def validate(text):
    """Gate: 1-200 chars, exactly one line, not whitespace-only,
    no leading/trailing whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry must be str")
    if not text:
        raise ValueError("entry must not be empty")
    if len(text) > MAX_CHARS:
        raise ValueError("entry exceeds 200 characters: %d" % len(text))
    if text.strip() != text:
        raise ValueError("entry must not have leading/trailing whitespace")
    if not text.strip():
        raise ValueError("entry must not be whitespace only")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("entry must not contain control characters")
    if "\t" in text:
        raise ValueError("entry must not contain tabs")
    text.encode("utf-8")  # gate requires valid UTF-8
    return text


def main():
    line = validate(LINE)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    tmp = target + ".tmp"
    data = (line + "\n").encode("utf-8")
    with open(tmp, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, target)
    # Read back byte-for-byte and re-validate.
    with open(target, "rb") as f:
        raw = f.read()
    if raw != data:
        raise RuntimeError("read-back mismatch")
    back = raw.decode("utf-8").rstrip("\n")
    if validate(back) != line:
        raise RuntimeError("read-back validation failed")
    print("entry: %d characters" % len(line))
    return 0


if __name__ == "__main__":
    sys.exit(main())
