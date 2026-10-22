#!/usr/bin/env python3
"""Read-only binding of the exact author freeze. Standard library, no assertions."""
import hashlib
import json
from pathlib import Path
import sys

EXPECTED_MANIFEST_SHA256 = "1f64af140ad77607cfd4a0ea61ed418853f9af99740387632b6f30545050b1f6"
EXPECTED_MANIFEST_BYTES = 1648


def verify(root):
    root = Path(root).resolve()
    manifest_path = root / "MANIFEST.json"
    if manifest_path.is_symlink():
        raise ValueError("The root manifest must not be a symlink")
    data = manifest_path.read_bytes()
    if len(data) != EXPECTED_MANIFEST_BYTES or hashlib.sha256(data).hexdigest() != EXPECTED_MANIFEST_SHA256:
        raise ValueError("Author manifest differs from the independently audited freeze")
    manifest = json.loads(data)
    entries = manifest["files"]
    expected = set()
    for entry in entries:
        name = entry["path"]
        path = Path(name)
        if path.is_absolute() or ".." in path.parts or name in expected or name == "MANIFEST.json":
            raise ValueError("Invalid or repeated manifest entry")
        expected.add(name)
    actual = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError("Symlink in author packet")
        if path.is_file() and path != manifest_path:
            actual.add(path.relative_to(root).as_posix())
    if actual != expected:
        raise ValueError("File-set mismatch: " + json.dumps({"missing": sorted(expected - actual), "extra": sorted(actual - expected)}))
    for entry in entries:
        data = (root / entry["path"]).read_bytes()
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise ValueError("Byte mismatch: " + entry["path"])
    return {"status": "PASS", "files": len(entries), "author_manifest_sha256": EXPECTED_MANIFEST_SHA256,
            "scope": "Exact author-freeze integrity only; not mathematical certification."}


if __name__ == "__main__":
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "packet"
    print(json.dumps(verify(packet), sort_keys=True))
