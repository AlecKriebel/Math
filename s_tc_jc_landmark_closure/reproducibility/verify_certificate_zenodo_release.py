#!/usr/bin/env python3
"""Authenticate a certificate archive downloaded from the public DOI."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
ENVELOPE = PROJECT / "release_artifacts/CERTIFICATE_BUNDLE_ENVELOPE.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    record = json.loads(ENVELOPE.read_text(encoding="utf-8"))
    if record["zenodo_doi"] == "ZENODO_DOI_PENDING":
        raise SystemExit("release envelope still contains ZENODO_DOI_PENDING")
    if args.archive.name != record["archive"]:
        raise SystemExit(f"wrong filename: expected {record['archive']}")
    actual = sha256(args.archive)
    if actual != record["archive_sha256"]:
        raise SystemExit(f"SHA-256 mismatch: {actual}")
    print(json.dumps({
        "status": "VERIFIED",
        "archive": args.archive.name,
        "sha256": actual,
        "zenodo_doi": record["zenodo_doi"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
