#!/usr/bin/env python3
"""Build a deterministic hash manifest for this review directory."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "MANIFEST.json")
    args = parser.parse_args()
    output = args.output.resolve()
    files = {}
    for path in sorted(HERE.rglob("*")):
        if not path.is_file() or path.resolve() == output:
            continue
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        relative = path.relative_to(HERE).as_posix()
        files[relative] = {"bytes": path.stat().st_size, "sha256": sha256_file(path)}
    manifest = {
        "schema": "arbitrary-subdivision-promotion-review-manifest-v1",
        "status": "VERIFIED_AFTER_CORRECTION",
        "files": files,
    }
    args.output.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"files": len(files), "status": manifest["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
