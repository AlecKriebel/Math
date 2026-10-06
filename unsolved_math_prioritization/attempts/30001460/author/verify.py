#!/usr/bin/env python3
"""Strict sealed-package replay. No caches, links, directories, or extra nodes."""
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys

CERTIFICATE_SHA256 = "d5bcdd749406083c2128441b09ce545886db4745325d73d0e98c048835fb2cf0"
FILES = {"README.md", "RESULT.md", "APPROACHES.md", "SOURCES.json",
         "certificate.py", "EXPECTED.json", "verify.py", "MANIFEST.json"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(b):
    return hashlib.sha256(b).hexdigest()


def run():
    root = Path(__file__).absolute().parent
    require(stat.S_ISDIR(root.lstat().st_mode), "root is not a real directory")
    observed = set()
    for path in root.iterdir():
        require(stat.S_ISREG(path.lstat().st_mode),
                "nonregular node: " + path.name)
        observed.add(path.name)
    require(observed == FILES, "inventory mismatch")
    manifest_bytes = (root / "MANIFEST.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    require(set(manifest) == {"schema", "files"} and manifest["schema"] == 1,
            "manifest schema mismatch")
    require(set(manifest["files"]) == FILES - {"MANIFEST.json"},
            "manifest inventory mismatch")
    for name in sorted(FILES - {"MANIFEST.json"}):
        data = (root / name).read_bytes()
        record = manifest["files"][name]
        require(set(record) == {"bytes", "sha256"}, "record schema: " + name)
        require(record["bytes"] == len(data), "size mismatch: " + name)
        require(record["sha256"] == digest(data), "hash mismatch: " + name)
    require(digest((root / "certificate.py").read_bytes()) == CERTIFICATE_SHA256,
            "certificate source pin mismatch; execution refused")
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command += ["-B", str(root / "certificate.py")]
    completed = subprocess.run(command, cwd=root, capture_output=True,
                               text=True, timeout=20, check=False)
    require(completed.returncode == 0, "certificate process failed")
    require(not completed.stderr, "unexpected certificate stderr")
    actual = json.loads(completed.stdout)
    expected = json.loads((root / "EXPECTED.json").read_bytes())
    require(actual == expected, "certificate result mismatch")
    # Execution must not leave even a benign cache or temporary artifact.
    require({x.name for x in root.iterdir()} == FILES,
            "post-execution inventory mismatch")
    for path in root.iterdir():
        require(stat.S_ISREG(path.lstat().st_mode), "post-execution nonregular node")
    return {"schema": 1, "verified": True, "files": len(FILES),
            "certificate_source_pinned_before_execution": True,
            "identities_passed": actual["identities_passed"],
            "manifest_sha256": digest(manifest_bytes),
            "scope": "sealed-file replay and exact rank-one formulas only"}


if __name__ == "__main__":
    try:
        print(json.dumps(run(), indent=2, sort_keys=True))
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print("VERIFICATION FAILED: " + str(error), file=sys.stderr)
        sys.exit(1)
