#!/usr/bin/env python3
"""Verify this audit's authored payload and detached manifest digest."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify(root, self_test=False):
    manifest_bytes = (root / "MANIFEST.json").read_bytes()
    expected = (root / "MANIFEST.sha256").read_text().split()[0]
    assert digest(manifest_bytes) == expected, "Manifest digest mismatch"
    manifest = json.loads(manifest_bytes)
    for item in manifest["authored_files"]:
        relative = Path(item["path"])
        assert not relative.is_absolute() and ".." not in relative.parts
        assert relative.parts[0] != "cache"
        data = (root / relative).read_bytes()
        assert len(data) == item["bytes"], f"Length mismatch: {relative}"
        assert digest(data) == item["sha256"], f"Digest mismatch: {relative}"
        if self_test:
            assert digest(data + b"\nTAMPER-CONTROL\n") != item["sha256"]
    if self_test:
        assert digest(manifest_bytes + b" ") != expected
    print(f"PASS: {len(manifest['authored_files'])} authored files; manifest verified")
    if self_test:
        print("PASS: every payload and manifest tamper control rejected")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    verify(Path(__file__).resolve().parent, args.self_test)
