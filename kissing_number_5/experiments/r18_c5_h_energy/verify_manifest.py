#!/usr/bin/env python3
"""Check the pinned hashes of proof-critical files."""

from hashlib import sha256
import json
from pathlib import Path


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def main():
    here = Path(__file__).resolve().parent
    manifest = json.loads((here / "manifest.json").read_text())
    checked = 0
    for relative, expected in manifest["proof_files"].items():
        path = here / relative
        require(path.is_file(), f"missing proof file: {relative}")
        actual = sha256(path.read_bytes()).hexdigest()
        require(actual == expected, f"hash mismatch: {relative}")
        checked += 1
    require(checked == 6, f"unexpected proof-file count: {checked}")
    print(f"verified: manifest hashes for {checked} proof files")


if __name__ == "__main__":
    main()
