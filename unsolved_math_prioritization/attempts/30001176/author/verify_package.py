#!/usr/bin/env python3
"""Fail-closed inventory, hash, pre-execution code-pin and finite-result replay."""

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    # The release is deliberately flat. No directory, symlink, FIFO, socket,
    # device or unexpected regular file is silently skipped.
    actual = set()
    for path in root.iterdir():
        mode = path.lstat().st_mode
        require(stat.S_ISREG(mode), "nonregular inventory node: " + path.name)
        require(path.name != "__pycache__", "forbidden cache node")
        actual.add(path.name)
    manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    require(manifest.get("schema") == 1, "manifest schema")
    expected = manifest["files"]
    require(isinstance(expected, dict), "manifest files")
    require(actual == set(expected) | {"MANIFEST.json"}, "inventory mismatch")
    for name, item in expected.items():
        require(Path(name).name == name and name not in ("", ".", ".."), "unsafe manifest name")
        data = (root / name).read_bytes()
        require(len(data) == item["bytes"] and digest(data) == item["sha256"], "hash mismatch: " + name)
    pins = json.loads((root / "CODE_PINS.json").read_text(encoding="utf-8"))
    require(set(pins["files"]) == {"check_controls.py", "verify_package.py", "test_package.py"},
            "code-pin inventory mismatch")
    for name, pin in pins["files"].items():
        data = (root / name).read_bytes()
        require(digest(data) == pin["sha256"] and len(data) == pin["bytes"], "code pin mismatch: " + name)
    # Only after the inventory and independent code pins have passed, execute.
    cmd = [sys.executable, "-B"]
    if sys.flags.optimize:
        cmd.append("-O")
    cmd.append(str(root / "check_controls.py"))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run(cmd, cwd=root, env=env, capture_output=True, check=False)
    require(result.returncode == 0, "control replay failed: " + result.stderr.decode(errors="replace"))
    require(result.stdout == (root / "CONTROL_RESULTS.json").read_bytes(), "control output mismatch")
    report = json.loads(result.stdout)
    print(json.dumps({"status": "PASS", "problem_id": "30001176",
                      "manifest_sha256": digest((root / "MANIFEST.json").read_bytes()),
                      "inventory_files": len(actual), "finite_checks": report["total_checks"]},
                     sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("FAIL: " + str(error), file=sys.stderr)
        sys.exit(1)
