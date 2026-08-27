#!/usr/bin/env python3
"""Record every regular-file byte or symlink-target difference between trees."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def manifest(root: Path) -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in list(dirnames):
            path = base / name
            if path.is_symlink():
                records[path.relative_to(root).as_posix()] = {
                    "type": "symlink", "target": os.readlink(path)
                }
                dirnames.remove(name)
        for name in filenames:
            path = base / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                records[relative] = {"type": "symlink", "target": os.readlink(path)}
            elif path.is_file():
                records[relative] = {
                    "type": "file",
                    "bytes": path.stat().st_size,
                    "sha256": file_hash(path),
                }
            else:
                raise RuntimeError(f"unsupported workspace object: {path}")
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    before = manifest(args.baseline.resolve())
    after = manifest(args.target.resolve())
    before_keys, after_keys = set(before), set(after)
    added = [{"path": p, "after": after[p]} for p in sorted(after_keys - before_keys)]
    removed = [{"path": p, "before": before[p]} for p in sorted(before_keys - after_keys)]
    changed = [
        {"path": p, "before": before[p], "after": after[p]}
        for p in sorted(before_keys & after_keys)
        if before[p] != after[p]
    ]
    unchanged = [p for p in before_keys & after_keys if before[p] == after[p]]
    report = {
        "schema": "k3p-revision-referee-full-workspace-byte-diff-v1",
        "baseline": str(args.baseline.resolve()),
        "target": str(args.target.resolve()),
        "baseline_entries": len(before),
        "target_entries": len(after),
        "unchanged_entries": len(unchanged),
        "unchanged_regular_file_bytes": sum(
            int(before[p]["bytes"])
            for p in unchanged
            if before[p]["type"] == "file"
        ),
        "difference_counts": {
            "added": len(added), "removed": len(removed), "changed": len(changed)
        },
        "added": added,
        "removed": removed,
        "changed": changed,
        "interpretation": (
            "Every regular-file difference is represented by size and SHA-256; "
            "every symlink difference is represented by its link target."
        ),
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["difference_counts"], sort_keys=True))


if __name__ == "__main__":
    main()
