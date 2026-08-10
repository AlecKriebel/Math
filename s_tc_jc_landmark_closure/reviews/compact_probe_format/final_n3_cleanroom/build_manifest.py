#!/usr/bin/env python3
"""Build a deterministic SHA-256 manifest for this isolated review."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
OUTPUT = HERE / "MANIFEST.json"
LOCKED_INPUTS = [
    PROJECT / "primary/certificates/probe_extension_schema3_n3_final_summary.json",
    *[PROJECT / "primary/certificates" /
      f"compact_probe_schema3_n3_compact_s{i}_summary.json"
      for i in range(4)],
    PROJECT / "primary/COMPACT_PROBE_SCHEMA.md",
]


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path):
    return str(path.resolve().relative_to(PROJECT))


def main():
    files = []
    for path in sorted(HERE.rglob("*")):
        if (not path.is_file() or path == OUTPUT or
                "__pycache__" in path.parts or path.name == ".DS_Store"):
            continue
        files.append({
            "path": relative(path), "bytes": path.stat().st_size,
            "sha256": sha(path),
        })
    payload = {
        "schema": "compact-probe-final-n3-cleanroom-manifest-v1",
        "status": "VERIFIED_AFTER_CORRECTION",
        "review_files": files,
        "locked_primary_inputs": [
            {"path": relative(path), "bytes": path.stat().st_size,
             "sha256": sha(path)} for path in LOCKED_INPUTS
        ],
    }
    OUTPUT.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"], "review_files": len(files),
        "output": relative(OUTPUT), "output_sha256": sha(OUTPUT),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
