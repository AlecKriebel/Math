#!/usr/bin/env python3
"""Build a deterministic SHA-256 manifest for this certificate directory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    # The mutation report binds this manifest from the outer release lock.  It
    # must not be a member of the manifest it qualifies, or rerunning the
    # mutation suite would create a circular/self-invalidating commitment.
    excluded = {"MANIFEST.sha256", "manifest.json", "mutation_report.json"}
    paths = sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.name not in excluded
        and "__pycache__" not in path.parts
    )
    rows = [(str(path.relative_to(ROOT)), sha256(path)) for path in paths]
    lines = [f"{digest}  {relative}" for relative, digest in rows]
    payload = ("\n".join(lines) + "\n").encode()
    aggregate = hashlib.sha256(payload).hexdigest()
    (ROOT / "MANIFEST.sha256").write_bytes(payload)
    manifest = {
        "schema": "k2p-rank-upper-manifest-v1",
        "file_count": len(rows),
        "aggregate_sha256": aggregate,
        "files": [
            {"path": relative, "sha256": digest} for relative, digest in rows
        ],
    }
    (ROOT / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({key: manifest[key] for key in manifest if key != "files"}, indent=2))


if __name__ == "__main__":
    main()
