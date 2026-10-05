#!/usr/bin/env python3
"""Verify the audit's byte binding and reproduce the finite author controls.

This does not verify source truth or the historical coefficient theorem.
Keep the frozen author/ and audit/ directories beside each other.
"""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_entries(base, entries, extra):
    names = []
    for entry in entries:
        name = entry["path"]
        relative = Path(name)
        require(not relative.is_absolute() and len(relative.parts) == 1,
                "Unsafe audit-bound filename")
        path = base / relative
        require(path.is_file() and not path.is_symlink(), f"Not a regular file: {name}")
        raw = path.read_bytes()
        require(len(raw) == entry["bytes"], f"Size mismatch: {name}")
        require(sha256(raw).hexdigest() == entry["sha256"], f"Hash mismatch: {name}")
        names.append(name)
    require(len(names) == len(set(names)), "Duplicate manifest entry")
    require({p.name for p in base.iterdir()} == set(names) | set(extra),
            "Unexpected directory contents")


def main():
    audit = Path(__file__).resolve().parent
    author = audit.parent / "author"
    binding = json.loads((audit / "AUDIT_BINDING.json").read_text())
    author_manifest_raw = (author / "AUTHOR_MANIFEST.json").read_bytes()
    require(sha256(author_manifest_raw).hexdigest() == binding["author_manifest_sha256"],
            "Author freeze changed")
    author_manifest = json.loads(author_manifest_raw)
    check_entries(author, author_manifest["files"], ["AUTHOR_MANIFEST.json"])
    audit_manifest = json.loads((audit / "AUDIT_MANIFEST.json").read_text())
    check_entries(audit, audit_manifest["files"], ["AUDIT_MANIFEST.json"])
    result = subprocess.run([sys.executable, "-B", str(author / "verify.py")],
                            check=True, capture_output=True)
    require(result.stdout == (author / "EXPECTED_CHECKS.json").read_bytes(),
            "Finite controls no longer match frozen expected bytes")
    require(result.stdout == (audit / "ACTUAL_CHECKS.json").read_bytes(),
            "Finite controls no longer match audit receipt")
    controls = json.loads(result.stdout)
    require(controls["all_passed"] and controls["total_checks"] == 162,
            "Unexpected finite control result")
    print(json.dumps({"all_passed": True, "author_files": 8,
                      "audit_files": len(audit_manifest["files"]) + 1,
                      "finite_controls": 162, "checks_byte_exact": True,
                      "source_truth_verified_by_this_script": False,
                      "historical_theorem_proved_by_this_script": False},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
