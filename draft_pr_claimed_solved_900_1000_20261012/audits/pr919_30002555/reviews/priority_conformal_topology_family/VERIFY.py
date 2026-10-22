#!/usr/bin/env python3
"""Verify the sealed explicit allowlist with an independently supplied manifest hash."""
import hashlib
import json
from pathlib import Path
import sys


def fail(message):
    raise SystemExit(message)


def main():
    if len(sys.argv) != 2:
        fail("Usage: python -B VERIFY.py EXPECTED_MANIFEST_SHA256")
    root = Path(__file__).resolve().parent
    manifest_path = root / "MANIFEST.json"
    body = manifest_path.read_bytes()
    actual = hashlib.sha256(body).hexdigest()
    if actual != sys.argv[1]:
        fail("Manifest hash mismatch")
    manifest = json.loads(body)
    allowed = manifest["public_allowlist"]
    if "MANIFEST.json" in allowed or any("/" in x or "\\" in x for x in allowed):
        fail("Unsafe or self-inclusive allowlist")
    public_inventory = {x.name for x in root.iterdir() if x.is_file()} - {"MANIFEST.json"}
    if public_inventory != set(allowed):
        fail("Public file inventory mismatch")
    directories = {x.name for x in root.iterdir() if x.is_dir()}
    if directories - {"private_sources"}:
        fail("Unexpected directory")
    for name, expected in allowed.items():
        path = root / name
        if path.is_symlink() or not path.is_file():
            fail("Non-regular public file: " + name)
        data = path.read_bytes()
        if len(data) != expected["bytes"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
            fail("Public file binding mismatch: " + name)
    start = json.loads((root / "AUTHENTICATION_START.json").read_text())
    end = json.loads((root / "AUTHENTICATION_END.json").read_text())
    if not start["all_match"] or not end["all_match"] or start["files"] != end["files"]:
        fail("Original snapshot authentication record mismatch")
    print(json.dumps({"verified": True, "public_files": len(allowed), "manifest_sha256": actual,
                      "original_files_unchanged": len(start["files"]),
                      "scope": "Byte bindings and recorded snapshot consistency, not a proof or priority certificate"},
                     sort_keys=True))


if __name__ == "__main__":
    main()
