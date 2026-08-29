#!/usr/bin/env python3
"""Record a deterministic full tree inventory for reviewer-side drift checks."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def inventory(root: Path, excluded_top_level: set[str]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(directory)
        relative_base = base.relative_to(root)
        if relative_base == Path("."):
            dirnames[:] = [name for name in dirnames if name not in excluded_top_level]
        for name in sorted(list(dirnames)):
            path = base / name
            metadata = path.lstat()
            relative = path.relative_to(root).as_posix()
            if stat.S_ISLNK(metadata.st_mode):
                records.append({
                    "path": relative,
                    "type": "symlink",
                    "mode": stat.S_IMODE(metadata.st_mode),
                    "target": os.readlink(path),
                })
                dirnames.remove(name)
            elif stat.S_ISDIR(metadata.st_mode):
                records.append({
                    "path": relative,
                    "type": "directory",
                    "mode": stat.S_IMODE(metadata.st_mode),
                })
            else:
                raise RuntimeError(f"unsupported directory entry: {path}")
        for name in sorted(filenames):
            path = base / name
            metadata = path.lstat()
            relative = path.relative_to(root).as_posix()
            if stat.S_ISLNK(metadata.st_mode):
                record: dict[str, object] = {
                    "path": relative,
                    "type": "symlink",
                    "mode": stat.S_IMODE(metadata.st_mode),
                    "target": os.readlink(path),
                }
            elif stat.S_ISREG(metadata.st_mode):
                record = {
                    "path": relative,
                    "type": "file",
                    "mode": stat.S_IMODE(metadata.st_mode),
                    "bytes": metadata.st_size,
                    "sha256": sha256(path),
                }
            else:
                raise RuntimeError(f"unsupported file entry: {path}")
            records.append(record)
    return sorted(records, key=lambda row: str(row["path"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--exclude-top-level", action="append", default=[])
    arguments = parser.parse_args()
    root = arguments.root.resolve(strict=True)
    records = inventory(root, set(arguments.exclude_top_level))
    payload = {
        "schema": "k3p-second-revision-referee-tree-inventory-v1",
        "root": str(root),
        "excluded_top_level": sorted(set(arguments.exclude_top_level)),
        "entry_count": len(records),
        "regular_file_bytes": sum(
            int(row["bytes"]) for row in records if row["type"] == "file"
        ),
        "records": records,
    }
    raw = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_bytes(raw)
    print(json.dumps({
        "entries": payload["entry_count"],
        "regular_file_bytes": payload["regular_file_bytes"],
        "inventory_sha256": hashlib.sha256(raw).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
