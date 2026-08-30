#!/usr/bin/env python3
"""Produce a deterministic, byte-level inventory of a review target tree."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    files: dict[str, dict[str, int | str]] = {}
    symlinks: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            symlinks[relative] = path.readlink().as_posix()
        elif path.is_file():
            files[relative] = {"bytes": path.stat().st_size, "sha256": sha256(path)}
    payload = {
        "schema": "k2p-independent-referee-tree-inventory-v1",
        "root_label": root.name,
        "file_count": len(files),
        "total_bytes": sum(int(row["bytes"]) for row in files.values()),
        "symlink_count": len(symlinks),
        "files": files,
        "symlinks": symlinks,
    }
    report = dict(payload)
    report["payload_sha256"] = canonical_hash(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: report[key] for key in ("file_count", "total_bytes", "symlink_count", "payload_sha256")}, sort_keys=True))


if __name__ == "__main__":
    main()
