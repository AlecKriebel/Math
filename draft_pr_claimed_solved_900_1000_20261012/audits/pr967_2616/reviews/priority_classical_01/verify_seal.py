#!/usr/bin/env python3
"""Authenticate the deliberately public classical-priority seal, never primary bodies."""
from pathlib import Path
import hashlib
import json


def verify(root):
    root = root.resolve()
    manifest_path = root / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    names = manifest["explicit_public_allowlist"]
    assert len(names) == len(set(names)), "duplicate allowlist entry"
    assert set(names) == set(manifest["files"]), "allowlist/member mismatch"
    assert "MANIFEST.json" not in names, "manifest must exclude itself"
    for name in names:
        assert Path(name).name == name and name not in {".", ".."}, "unsafe member path"
        path = root / name
        assert not path.is_symlink() and path.is_file(), "nonregular member"
        body = path.read_bytes()
        expected = manifest["files"][name]
        assert len(body) == expected["bytes"], "byte mismatch: " + name
        assert hashlib.sha256(body).hexdigest() == expected["sha256"], "hash mismatch: " + name
    found = {f.name for f in root.iterdir() if f.is_file() and f.name != "MANIFEST.json"}
    assert found == set(names), "unmanifested public-root file"
    return {"public_members_verified": len(names), "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest()}


if __name__ == "__main__":
    print(json.dumps(verify(Path(__file__).parent), sort_keys=True))
