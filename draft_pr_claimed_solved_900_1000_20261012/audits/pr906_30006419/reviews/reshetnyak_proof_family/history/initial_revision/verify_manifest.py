#!/usr/bin/env python3
"""Check this review's public allowlist and the immutable input snapshot."""
from pathlib import Path
import fnmatch
import hashlib
import json


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "MANIFEST.json").read_text())
    intentional = manifest["intentional_public_files"]
    allowed = set(intentional) | {manifest["manifest_self_path"]}
    observed = set()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        name = path.relative_to(root).as_posix()
        if any(fnmatch.fnmatch(name, rule) for rule in manifest["excluded_globs"]):
            continue
        assert not path.is_symlink(), f"Public symlink rejected: {name}"
        observed.add(name)
    assert observed == allowed, f"Public allowlist mismatch: {observed ^ allowed}"
    for name, expected in intentional.items():
        path = root / name
        assert path.stat().st_size == expected["bytes"], f"Size mismatch: {name}"
        assert sha256(path) == expected["sha256"], f"Hash mismatch: {name}"
    audit_root = root.parents[1]
    snapshot = json.loads((audit_root / "ORIGINAL_SNAPSHOT.json").read_text())
    assert snapshot["head"] == manifest["original_head"]
    for name, expected_hash in snapshot["files"].items():
        assert sha256(audit_root / "original" / name) == expected_hash, \
            f"Original packet changed: {name}"
    return {"public_allowlist_passed": True,
            "public_hashed_file_count": len(intentional),
            "original_snapshot_unchanged": True,
            "original_file_count": len(snapshot["files"]),
            "raw_sources_excluded": True}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
