#!/usr/bin/env python3
"""Bind the historical release to its exact captured 22-file inventory.

This supplies the missing trust boundary of the original release verifier.
It checks a known authored inventory, not semantic authorship of arbitrary files.
Uses only the Python standard library and performs no writes or network access.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

EXPECTED_HEAD = "e4b27ac757babc1aea75149ea986ed2beea438f9"
EXPECTED_SNAPSHOT_SHA256 = "3be36a104aef0cd87652ec12ed0b12fafc2a907cd302edd2abc2667b81e439c2"
EXPECTED_PREFIX = "unsolved_math_prioritization/attempts/30004404/"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_path(name):
    require(isinstance(name, str) and bool(name), "Invalid original path")
    require("\\" not in name and ":" not in name, "Invalid original path")
    path = PurePosixPath(name)
    require(not path.is_absolute() and path.as_posix() == name,
            "Invalid original path")
    require(all(part not in ("", ".", "..") for part in path.parts),
            "Invalid original path")
    require(name.startswith(EXPECTED_PREFIX), "Wrong original target")
    require(not any(part in (".cache", "sources", "scratch", "qa", ".secrets")
                    for part in path.parts), "Excluded original path")
    require(".private" not in path.name, "Private original path")
    return path


def verify(root):
    snapshot_file = root / "ORIGINAL_SNAPSHOT.json"
    require(not snapshot_file.is_symlink(), "Snapshot symlink forbidden")
    raw = snapshot_file.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_SNAPSHOT_SHA256,
            "Original snapshot binding differs")
    snapshot = json.loads(raw)
    require(snapshot["head"] == EXPECTED_HEAD, "Original head differs")
    require(len(snapshot["files"]) == 22, "Original file count differs")
    originals = root / "original"
    require(originals.is_dir() and not originals.is_symlink(),
            "Invalid original directory")
    entries = list(originals.rglob("*"))
    require(not any(path.is_symlink() for path in entries),
            "Original symlink forbidden")
    expected = {}
    for record in snapshot["files"]:
        name = safe_path(record["path"]).as_posix()
        require(name not in expected, "Duplicate original path")
        expected[name] = record
    actual = {path.relative_to(originals).as_posix()
              for path in entries if path.is_file()}
    require(actual == set(expected), "Original inventory differs")
    for name, record in expected.items():
        path = originals / name
        require(path.resolve().is_relative_to(originals.resolve()),
                "Original escapes its root")
        data = path.read_bytes()
        require(len(data) == record["size"], "Original size differs: " + name)
        require(hashlib.sha256(data).hexdigest() == record["sha256"],
                "Original hash differs: " + name)
    return {
        "status": "PASS",
        "original_head": EXPECTED_HEAD,
        "original_snapshot_sha256": EXPECTED_SNAPSHOT_SHA256,
        "original_files_verified": 22,
        "original_outer_manifest_anchored": True,
        "original_nested_manifests_anchored": 2,
        "exclusion_basis": "Exact captured authored paths and hashes, including the historical outer manifest; not automatic classification of arbitrary contents.",
        "limits": "Integrity is not authenticity, topology verification, priority, human peer review or formal proof certification.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path,
                        default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    print(json.dumps(verify(args.root.resolve()), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
