#!/usr/bin/env python3
"""Artifact integrity only; no mathematical theorem verification."""
from pathlib import Path
import hashlib
import json
import sys


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "MANIFEST.json").read_text())
    records = manifest["files"]
    expected = {r["path"] for r in records}
    if len(expected) != len(records):
        raise ValueError("duplicate manifest path")
    if "MANIFEST.json" in expected:
        raise ValueError("manifest must not include itself")
    for name in expected:
        if Path(name).is_absolute() or ".." in Path(name).parts:
            raise ValueError("unsafe manifest path")
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    if actual != expected | {"MANIFEST.json"}:
        raise ValueError("inventory mismatch")
    for p in root.rglob("*"):
        if p.is_symlink():
            raise ValueError("symlinks forbidden")
    for record in records:
        data = (root / record["path"]).read_bytes()
        if len(data) != record["bytes"] or hashlib.sha256(data).hexdigest() != record["sha256"]:
            raise ValueError("content mismatch: " + record["path"])
    print("PASS: exact inventory and SHA-256/byte counts; integrity only")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
