#!/usr/bin/env python3
"""Authenticate a certificate archive downloaded from the public DOI."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile


PROJECT = Path(__file__).resolve().parents[1]
ENVELOPE = PROJECT / "release_artifacts/CERTIFICATE_BUNDLE_ENVELOPE.json"


def clean_git_environment() -> dict[str, str]:
    allowed = {"PATH", "LANG", "LC_ALL", "LC_CTYPE", "SYSTEMROOT"}
    environment = {
        key: value for key, value in os.environ.items() if key in allowed
    }
    environment["LC_ALL"] = "C"
    return environment


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
    with tarfile.open(args.archive, "r:gz") as archive:
        matches = [
            member for member in archive.getmembers()
            if member.name.endswith("/ACTIVE_MANIFEST.json") and member.isfile()
        ]
        if len(matches) != 1:
            raise SystemExit("archive does not contain one active manifest")
        stream = archive.extractfile(matches[0])
        if stream is None:
            raise SystemExit("cannot read archived active manifest")
        manifest = json.loads(stream.read().decode("utf-8"))
    if not (
        manifest["source_commit"] == record["source_commit"]
        and manifest["source_tree_clean"] is True
        and manifest["prepared_payload_sha256"] == record["prepared_payload_sha256"]
    ):
        raise SystemExit("archive manifest and Zenodo envelope disagree")
    commit_check = subprocess.run(
        ["git", "cat-file", "-e", f"{record['source_commit']}^{{commit}}"],
        cwd=PROJECT.parent,
        env=clean_git_environment(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if commit_check.returncode:
        raise SystemExit("envelope source commit is not present in this Git checkout")
    print(json.dumps({
        "status": "VERIFIED",
        "archive": args.archive.name,
        "sha256": actual,
        "zenodo_doi": record["zenodo_doi"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
