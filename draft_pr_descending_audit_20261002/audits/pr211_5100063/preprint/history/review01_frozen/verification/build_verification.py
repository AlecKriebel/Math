#!/usr/bin/env python3
"""Seal this already assembled verification folder, without external inputs.

Root integrates and seals the manuscript and final external ZIP separately.
This utility does not copy research files, run tests, publish, or build a ZIP.
"""
import argparse
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
FORBIDDEN = {"private", "private_reading", "private_transport", "__pycache__"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seal", action="store_true", required=True)
    parser.parse_args()
    rows = []
    for path in sorted(BASE.rglob("*")):
        rel = path.relative_to(BASE)
        if path.is_symlink() or set(rel.parts) & FORBIDDEN:
            raise ValueError(f"Forbidden payload or symlink: {rel}")
        if not path.is_file() or rel.as_posix() == "MANIFEST.json":
            continue
        data = path.read_bytes()
        rows.append({"path": rel.as_posix(), "bytes": len(data),
                     "sha256": hashlib.sha256(data).hexdigest()})
    manifest = {"schema": "portable-pr211-sha256-v1", "source_head": "9d7b623203b525386da3d9d91548c79e7445a11c",
                "scope": "Portable verification payload only; manuscript and final publication seal are separate.",
                "self_excluded": True, "files": rows}
    data = (json.dumps(manifest, indent=2) + "\n").encode()
    (BASE / "MANIFEST.json").write_bytes(data)
    print(json.dumps({"files": len(rows), "bytes": sum(row["bytes"] for row in rows),
                      "manifest_sha256": hashlib.sha256(data).hexdigest()}, indent=2))


if __name__ == "__main__":
    main()
