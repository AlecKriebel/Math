#!/usr/bin/env python3
"""Emit stable hashes for the candidate package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
FILES = (
    "NOTE.md",
    "RESEARCH_LOG.md",
    "verify_bowtie.py",
    "verify_strict.sh",
    "expected_result.json",
)


def main() -> None:
    result = {
        "schema": "qq1-supported-asymmetry-bowtie-manifest-v1",
        "files": {
            name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            for name in FILES
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
