#!/usr/bin/env python3
"""Verify the frozen directory, without creating any output files."""
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "MANIFEST.json").read_text())
    listed = {entry["path"] for entry in manifest["files"]}
    actual = {p.name for p in root.iterdir() if p.is_file()}
    assert actual == listed | {"MANIFEST.json"}, "Unexpected or missing file"
    assert all(p.is_file() and not p.is_symlink() for p in root.iterdir()), "Nonregular entry"
    for entry in manifest["files"]:
        assert "/" not in entry["path"] and "\\" not in entry["path"]
        data = (root / entry["path"]).read_bytes()
        assert len(data) == entry["bytes"], entry["path"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"], entry["path"]
    print("PASS: all", len(listed), "manifested files match; no extra files")


if __name__ == "__main__":
    main()
