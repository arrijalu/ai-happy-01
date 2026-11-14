#!/usr/bin/env python3
"""Ship the ai-happy-01 competition entry image to the grader.

The entry file is entry.png, which sits next to this script. It is copied
byte-for-byte to /output/entry.png (and to the two relative fallbacks) so
the grader can pick it up regardless of the working directory it runs in.
"""

import os
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SIGNATURE = b"\xff\xd8\xff"

DESTINATIONS = (
    "/output/entry.png",
    "./entry.png",
    "./output/entry.png",
)


def entry_path():
    """Return the entry.png path, resolved from this script's own location."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def signature_ok(data):
    """True when the payload carries a PNG or JPEG signature."""
    return data.startswith(PNG_SIGNATURE) or data.startswith(JPEG_SIGNATURE)


def main():
    with open(entry_path(), "rb") as fh:
        data = fh.read()

    if not signature_ok(data):
        sys.stderr.write("entry.png has no PNG or JPEG signature\n")
        return 1

    written = []

    for dest in DESTINATIONS:
        try:
            parent = os.path.dirname(dest)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(dest, "wb") as fh:
                fh.write(data)
            written.append(dest)
        except OSError:
            pass

    if written:
        print("wrote " + ", ".join(written))
        return 0

    sys.stderr.write("could not write entry.png to any destination\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())