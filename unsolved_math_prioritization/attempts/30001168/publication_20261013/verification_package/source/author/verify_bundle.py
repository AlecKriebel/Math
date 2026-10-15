#!/usr/bin/env python3
"""Fail-closed regular-file inventory, hashes, and exact-output replay."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys

PAYLOAD = {
    "APPROACH_LOG.md", "PROOF.md", "README.md", "RESULTS.json",
    "SOURCE_METADATA.json", "certificate.py", "verify_bundle.py",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(root):
    require(root.is_dir() and not root.is_symlink(), "Root must be an ordinary directory")
    entries = list(root.iterdir())
    require({p.name for p in entries} == PAYLOAD | {"MANIFEST.json"},
            "Strict inventory mismatch; extra files and directories are forbidden")
    for path in entries:
        require(stat.S_ISREG(path.lstat().st_mode), f"Nonregular entry: {path.name}")
    manifest = json.loads((root / "MANIFEST.json").read_text())
    require(set(manifest) == {"schema", "problem_id", "files"}, "Manifest keys")
    require(manifest["schema"] == "authored-proof-bundle-v1", "Manifest schema")
    require(manifest["problem_id"] == 30001168, "Manifest problem")
    records = manifest["files"]
    require(isinstance(records, list) and len(records) == len(PAYLOAD), "Manifest count")
    require({r.get("path") for r in records} == PAYLOAD, "Manifest inventory")
    for record in records:
        require(set(record) == {"path", "bytes", "sha256"}, "Manifest record keys")
        data = (root / record["path"]).read_bytes()
        require(len(data) == record["bytes"], f"Byte count mismatch: {record['path']}")
        require(hashlib.sha256(data).hexdigest() == record["sha256"],
                f"Hash mismatch: {record['path']}")
    # No package from the bundle is imported. The isolated interpreter executes
    # the verified source script directly, with bytecode writing disabled.
    command = [sys.executable, "-I", "-B"]
    if sys.flags.optimize:
        command.append("-O")
    command.append(str(root / "certificate.py"))
    result = subprocess.run(command, capture_output=True, text=True, check=False,
                            cwd=str(root.parent))
    require(result.returncode == 0, "Certificate failed: " + result.stderr)
    require(result.stderr == "", "Unexpected certificate stderr")
    expected = (root / "RESULTS.json").read_text()
    require(result.stdout == expected, "Reproduced result differs from RESULTS.json")
    report = json.loads(result.stdout)
    require(report["checks"] == 613, "Unexpected arithmetic-check count")
    return {"verified": True, "payload_files": len(PAYLOAD),
            "arithmetic_checks": report["checks"],
            "optimized": bool(sys.flags.optimize),
            "manifest_sha256": hashlib.sha256((root / "MANIFEST.json").read_bytes()).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).absolute().parent)
    args = parser.parse_args()
    print(json.dumps(verify(args.root.absolute()), indent=2, sort_keys=True))
