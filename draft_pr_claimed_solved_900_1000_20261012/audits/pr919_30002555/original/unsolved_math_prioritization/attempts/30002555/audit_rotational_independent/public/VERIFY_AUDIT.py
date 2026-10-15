#!/usr/bin/env python3
"""Verify this source-free audit and replay its independent controls.

Usage: python -B VERIFY_AUDIT.py EXPECTED_AUDIT_MANIFEST_SHA256 AUTHOR_PACKET
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def need(value, message):
    if not value:
        raise RuntimeError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "Duplicate JSON key.")
        result[key] = value
    return result


def main():
    need(len(sys.argv) == 3, "Provide expected audit manifest digest and author packet directory.")
    expected, author = sys.argv[1:]
    need(re.fullmatch(r"[a-f0-9]{64}", expected) is not None, "Invalid expected digest.")
    root = Path(__file__).resolve().parent
    path = root / "MANIFEST.json"
    need(path.is_file() and not path.is_symlink(), "Missing or linked manifest.")
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == expected, "Audit manifest anchor mismatch.")
    manifest = json.loads(raw, object_pairs_hook=unique)
    need(manifest["schema"] == "veech-ends-independent-audit-v1", "Wrong schema.")
    names = {"MANIFEST.json"}
    for item in manifest["files"]:
        name = item["path"]
        need(isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9_.-]+", name) is not None, "Unsafe name.")
        need(name not in names and name not in (".", ".."), "Duplicate or unsafe path.")
        names.add(name)
        member = root / name
        need(member.is_file() and not member.is_symlink(), "Missing or linked member.")
        data = member.read_bytes()
        need(type(item["bytes"]) is int and len(data) == item["bytes"], "Size mismatch.")
        need(hashlib.sha256(data).hexdigest() == item["sha256"], "Digest mismatch.")
    need({p.name for p in root.iterdir()} == names, "Unexpected inventory.")
    receipt = (root / "INDEPENDENT_RESULTS.json").read_bytes()
    for flags in ([], ["-O"]):
        result = subprocess.run([sys.executable, *flags, "-B", str(root / "INDEPENDENT_CHECKS.py"), author], capture_output=True)
        need(result.returncode == 0, "Independent replay failed: " + result.stderr.decode(errors="replace"))
        need(result.stdout == receipt, "Independent receipt mismatch.")
    print(json.dumps({"status": "PASS", "audit_manifest_sha256": expected,
                      "author_manifest_sha256": manifest["author_manifest_sha256"],
                      "verified_member_count": len(names) - 1,
                      "independent_controls_per_mode": json.loads(receipt)["total_controls"],
                      "replay_modes": ["ordinary", "optimized"]}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
