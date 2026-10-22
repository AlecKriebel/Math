#!/usr/bin/env python3
"""Read-only bundle verification with a caller-supplied external manifest pin."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def no_duplicate_keys(pairs):
    out = {}
    for k, v in pairs:
        require(k not in out, "duplicate JSON key")
        out[k] = v
    return out


def verify(root, expected):
    require(re.fullmatch(r"[0-9a-f]{64}", expected) is not None, "invalid external pin")
    require(root.is_dir() and not root.is_symlink(), "root must be a real directory")
    manifest_path = root / "MANIFEST.json"
    require(manifest_path.is_file() and not manifest_path.is_symlink(), "missing or linked manifest")
    require(manifest_path.stat().st_size <= 65536, "oversized manifest")
    raw = manifest_path.read_bytes()
    require(len(raw) <= 65536, "oversized manifest")
    require(hashlib.sha256(raw).hexdigest() == expected, "manifest external pin mismatch")
    manifest = json.loads(raw, object_pairs_hook=no_duplicate_keys)
    require(type(manifest) is dict and set(manifest) == {"format", "files"}, "manifest schema mismatch")
    require(manifest["format"] == "su2-surgery-audit-v1", "wrong bundle format")
    files = manifest["files"]
    require(type(files) is list and 1 <= len(files) <= 20, "invalid file list")
    seen = set()
    for f in files:
        require(type(f) is dict and set(f) == {"name", "sha256", "bytes"}, "file schema mismatch")
        name = f["name"]
        require(type(name) is str and re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", name), "unsafe filename")
        require(name not in {"MANIFEST.json", ".", ".."} and name not in seen, "duplicate/reserved filename")
        seen.add(name)
        require(type(f["bytes"]) is int and 0 <= f["bytes"] <= 2_000_000, "invalid byte count")
        require(type(f["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", f["sha256"]), "invalid file pin")
        path = root / name
        require(path.is_file() and not path.is_symlink(), "missing, nonregular, or linked file")
        require(path.stat().st_size == f["bytes"], "byte count mismatch")
        content = path.read_bytes()
        require(len(content) == f["bytes"], "byte count mismatch")
        require(hashlib.sha256(content).hexdigest() == f["sha256"], "file hash mismatch")
    require({p.name for p in root.iterdir()} == seen | {"MANIFEST.json"}, "unexpected or missing bundle entry")
    return {"status": "passed", "file_count": len(seen), "manifest_sha256": expected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--manifest-sha256", required=True)
    args = parser.parse_args()
    try:
        result = verify(args.root, args.manifest_sha256)
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    except (ValueError, TypeError, OSError) as e:
        print("REJECTED: " + str(e), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
