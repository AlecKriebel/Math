#!/usr/bin/env python3
"""Check the frozen author packet against its manifest, without source files."""
import hashlib
import json
from pathlib import Path


def main():
    base = Path(__file__).resolve().parent
    manifest = json.loads((base / "AUTHOR_MANIFEST.json").read_text())
    allowed = set()
    for entry in manifest["files"]:
        name = entry["path"]
        path = base / name
        if Path(name).is_absolute() or ".." in Path(name).parts:
            raise ValueError("Unsafe manifest path")
        raw = path.read_bytes()
        assert len(raw) == entry["bytes"], name
        assert hashlib.sha256(raw).hexdigest() == entry["sha256"], name
        allowed.add(name)
    actual = {p.name for p in base.iterdir() if p.is_file()}
    assert actual == allowed | {"AUTHOR_MANIFEST.json"}, actual ^ allowed
    print(json.dumps({"all_passed": True, "verified_files": len(allowed),
                      "claim": "Byte integrity only; not mathematical or historical proof verification"},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
