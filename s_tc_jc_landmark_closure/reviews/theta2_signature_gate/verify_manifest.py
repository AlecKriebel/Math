#!/usr/bin/env python3
"""Verify the deterministic theta-2 gate manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
MANIFEST = HERE / "manifest.json"


def digest(path: Path) -> str:
    answer = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def main():
    payload = json.loads(MANIFEST.read_text())
    failures = []
    for relative, expected in payload["scoped_files"].items():
        path = HERE / relative
        if not path.is_file() or digest(path) != expected:
            failures.append(relative)
    for relative, expected in payload["external_inputs"].items():
        path = PROJECT / relative
        if not path.is_file() or digest(path) != expected:
            failures.append(relative)
    signature = json.loads((HERE / "signature_certificate.json").read_text())
    quotient = json.loads((HERE / "canonical_quotient_certificate.json").read_text())
    if signature.get("status") != "VERIFIED":
        failures.append("signature_certificate.status")
    if quotient.get("status") != "VERIFIED":
        failures.append("canonical_quotient_certificate.status")
    if failures:
        raise SystemExit("manifest verification failed: " + ", ".join(failures))
    print(json.dumps({"status": "VERIFIED", "files": len(payload["scoped_files"]),
                      "external_inputs": len(payload["external_inputs"])}, sort_keys=True))


if __name__ == "__main__":
    main()
