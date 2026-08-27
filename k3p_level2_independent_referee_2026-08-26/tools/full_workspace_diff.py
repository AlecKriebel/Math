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
                relative = path.relative_to(root).as_posix()
                records[relative] = {
                    "type": "symlink",
                    "target": os.readlink(path),
                }
                dirnames.remove(name)
        for name in filenames:
            path = base / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                records[relative] = {
                    "type": "symlink",
                    "target": os.readlink(path),
                }
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

    baseline_root = args.baseline.resolve()
    target_root = args.target.resolve()
    before = manifest(baseline_root)
    after = manifest(target_root)
    before_keys, after_keys = set(before), set(after)
    added = [
        {"path": path, "after": after[path]}
        for path in sorted(after_keys - before_keys)
    ]
    removed = [
        {"path": path, "before": before[path]}
        for path in sorted(before_keys - after_keys)
    ]
    changed = [
        {"path": path, "before": before[path], "after": after[path]}
        for path in sorted(before_keys & after_keys)
        if before[path] != after[path]
    ]
    unchanged = [
        path for path in before_keys & after_keys if before[path] == after[path]
    ]
    report = {
        "schema": "k3p-referee-full-workspace-byte-diff-v1",
        "baseline": str(baseline_root),
        "target": str(target_root),
        "baseline_entries": len(before),
        "target_entries": len(after),
        "unchanged_entries": len(unchanged),
        "unchanged_regular_file_bytes": sum(
            int(before[path]["bytes"])
            for path in unchanged
            if before[path]["type"] == "file"
        ),
        "difference_counts": {
            "added": len(added),
            "removed": len(removed),
            "changed": len(changed),
        },
        "added": added,
        "removed": removed,
        "changed": changed,
        "interpretation": (
            "Every regular-file byte difference is represented by size and SHA-256; "
            "every symlink difference is represented by its link target."
        ),
    }
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(report["difference_counts"], sort_keys=True))


if __name__ == "__main__":
    main()
