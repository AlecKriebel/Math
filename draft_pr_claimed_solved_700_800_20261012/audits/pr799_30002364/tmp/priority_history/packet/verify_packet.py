#!/usr/bin/env python3
"""Authenticate this closed packet against independently supplied SHA256 pins.

Before executing, hash these checker bytes with a trusted utility and compare
with the independently obtained checker pin. The internal self-check is not a
replacement for that pre-execution step. No untrusted source-cache code runs.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys


def require(value, message):
    if not value:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(path):
    absolute = Path(os.path.abspath(path))
    for member in [absolute, *absolute.parents]:
        require(not stat.S_ISLNK(member.lstat().st_mode), "symlink in path")
    return absolute


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("packet")
    parser.add_argument("manifest_sha256")
    parser.add_argument("checker_sha256")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    pattern = re.compile(r"[0-9a-f]{64}")
    require(pattern.fullmatch(args.manifest_sha256) is not None, "bad manifest pin")
    require(pattern.fullmatch(args.checker_sha256) is not None, "bad checker pin")
    checker = safe_path(__file__)
    require(digest(checker.read_bytes()) == args.checker_sha256, "checker pin mismatch")
    root = safe_path(args.packet)
    require(root.is_dir(), "packet is not a directory")
    manifest_path = safe_path(root / "MANIFEST.json")
    raw = manifest_path.read_bytes()
    require(digest(raw) == args.manifest_sha256, "manifest pin mismatch")
    manifest = json.loads(raw)
    require(set(manifest) == {"schema", "files", "directories"}, "manifest keys")
    require(manifest["schema"] == "pr799-priority-history-closed-v1", "manifest schema")
    require(manifest["directories"] == [], "unexpected manifest directories")
    rows = manifest["files"]
    names = [row["name"] for row in rows]
    require(names == sorted(set(names)) and len(names) >= 8, "file list order/uniqueness")
    require("verify_packet.py" in names and "verify_finite.py" in names, "missing checker")
    for row in rows:
        require(set(row) == {"name", "bytes", "sha256"}, "file record keys")
        name = row["name"]
        require(isinstance(name, str) and Path(name).name == name and name not in {".", "..", "MANIFEST.json"}, "unsafe file name")
        require(isinstance(row["bytes"], int) and row["bytes"] > 0, "bad size")
        require(isinstance(row["sha256"], str) and pattern.fullmatch(row["sha256"]) is not None, "bad hash")
    children = list(root.iterdir())
    require(sorted(p.name for p in children) == sorted(names + ["MANIFEST.json"]), "closed inventory mismatch")
    for child in children:
        require(stat.S_ISREG(child.lstat().st_mode), "nonregular inventory member")
    for row in rows:
        path = safe_path(root / row["name"])
        data = path.read_bytes()
        require(len(data) == row["bytes"] and digest(data) == row["sha256"], "member mismatch: " + row["name"])
    require(digest((root / "verify_packet.py").read_bytes()) == args.checker_sha256, "invoked checker is not packet checker")
    result = {"integrity": "PASS", "members": len(rows), "manifest_sha256": args.manifest_sha256}
    if args.execute:
        flags = ["-I", "-S", "-B"] + (["-O"] if sys.flags.optimize else [])
        output = subprocess.run([sys.executable, *flags, str(root / "verify_finite.py")],
                                check=True, capture_output=True, text=True, cwd=root)
        result["finite"] = json.loads(output.stdout)
        require(result["finite"]["status"] == "PASS", "finite result")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("REJECT: " + str(error), file=sys.stderr)
        sys.exit(1)
