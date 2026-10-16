#!/usr/bin/env python3
"""Offline explicit closure verification; does not establish mathematical priority."""
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    manifest = json.loads((BASE / "MANIFEST.json").read_text())
    expected = manifest["authored_files"]
    require(not any(p.is_symlink() for p in BASE.rglob("*")), "Symlink in closed audit folder")
    actual = {
        str(p.relative_to(BASE)): p
        for p in BASE.rglob("*")
        if p.is_file()
        and p != BASE / "MANIFEST.json"
    }
    require(set(actual) == set(expected), "Authored file inventory changed")
    for name, pin in expected.items():
        p = actual[name]
        require(not p.is_symlink(), "Symlink is not an allowed authored file")
        data = p.read_bytes()
        require(len(data) == pin["bytes"], name + ": size mismatch")
        require(hashlib.sha256(data).hexdigest() == pin["sha256"], name + ": hash mismatch")
    proof = BASE.parent / manifest["frozen_input"]["path_from_audit"]
    if proof.exists():
        data = proof.read_bytes()
        pin = manifest["frozen_input"]
        require(len(data) == pin["bytes"], "Frozen input size mismatch")
        require(hashlib.sha256(data).hexdigest() == pin["sha256"], "Frozen input hash mismatch")
    print(json.dumps({"result": "PASS", "authored_files": len(expected), "frozen_input_present": proof.exists()}))


if __name__ == "__main__":
    main()
