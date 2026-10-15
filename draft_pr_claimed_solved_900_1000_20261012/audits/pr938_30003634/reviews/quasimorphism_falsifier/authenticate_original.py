#!/usr/bin/env python3
"""Read-only, stdout-only authentication; every trust pin is supplied externally."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

PREFIX = "unsolved_math_prioritization/attempts/30003634/"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def checked_path(path):
    path = Path(path).absolute()
    for component in (path, *path.parents):
        require(not component.is_symlink(), "symlink component: " + str(component))
    return path


def verify(args):
    require(bool(re.fullmatch(r"[0-9a-f]{40}", args.head)), "invalid head pin")
    require(bool(re.fullmatch(r"[0-9a-f]{64}", args.inventory_sha256)), "invalid inventory pin")
    inventory = checked_path(args.inventory)
    data = inventory.read_bytes()
    require(sha(data) == args.inventory_sha256, "inventory hash mismatch")
    record = json.loads(data)
    require(record.get("head") == args.head, "inventory head mismatch")
    files = record.get("files")
    require(isinstance(files, dict) and len(files) == 44, "inventory count/type mismatch")
    repo = checked_path(args.repo)
    copied = checked_path(args.copy)
    tree = subprocess.run(["git", "ls-tree", "-rz", "--full-tree", args.head, "--", PREFIX],
                          cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    actual = {}
    for row in tree.split(b"\0"):
        if not row:
            continue
        meta, raw_path = row.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        require(kind == "blob" and mode in ("100644", "100755"), "non-regular Git entry")
        actual[raw_path.decode()] = oid
    require(set(actual) == set(files), "Git/inventory path-set mismatch")
    rows = []
    for relative, expected in sorted(files.items()):
        require(isinstance(relative, str) and relative.startswith(PREFIX), "unexpected path")
        parts = PurePosixPath(relative)
        require(not parts.is_absolute() and ".." not in parts.parts, "unsafe relative path")
        require(isinstance(expected, str) and bool(re.fullmatch(r"[0-9a-f]{64}", expected)), "invalid file pin")
        disk = checked_path(copied / relative)
        require(disk.is_file(), "missing regular copied file: " + relative)
        disk_bytes = disk.read_bytes()
        blob = subprocess.run(["git", "cat-file", "blob", actual[relative]], cwd=repo,
                              check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
        require(sha(blob) == expected, "Git blob hash mismatch: " + relative)
        require(sha(disk_bytes) == expected and disk_bytes == blob, "disk mismatch: " + relative)
        rows.append({"path": relative, "sha256": expected, "bytes": len(blob), "git_blob": actual[relative]})
    return {"status": "PASS", "head": args.head, "inventory_sha256": args.inventory_sha256,
            "count": len(rows), "optimization": sys.flags.optimize,
            "git_equals_disk_equals_inventory": True, "files": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("repo", "copy", "inventory", "inventory-sha256", "head"):
        parser.add_argument("--" + key, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args), indent=2))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
