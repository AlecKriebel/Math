#!/usr/bin/env python3
"""Check every declared archive body against its size and SHA256.

Run from an extracted package. Standard library only; no writes or network.
HASHES.json deliberately excludes itself to avoid self-reference.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / "HASHES.json").read_text())
assert manifest["self_exclusion"] == "HASHES.json only"
seen = set()
for entry in manifest["files"]:
    relative = PurePosixPath(entry["path"])
    assert not relative.is_absolute() and ".." not in relative.parts
    assert str(relative) == entry["path"] and entry["path"] not in seen
    seen.add(entry["path"])
    source = root.joinpath(*relative.parts)
    assert source.is_file() and not source.is_symlink()
    body = source.read_bytes()
    assert len(body) == entry["bytes"], entry["path"]
    assert hashlib.sha256(body).hexdigest() == entry["sha256"], entry["path"]
print(json.dumps({"status": "PASS", "verified_files": len(seen),
                  "self_exclusion": "HASHES.json only"}, sort_keys=True))
