#!/usr/bin/env python3
"""Relocatable offline publication integrity and bound audit replay."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def fingerprint(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main():
    manifest = json.loads((ROOT / "PUBLICATION_MANIFEST.json").read_text())
    records = {item["path"]: item for item in manifest["files"]}
    require(len(records) == len(manifest["files"]), "Duplicate publication entry")
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file()}
    require(actual == set(records) | {"PUBLICATION_MANIFEST.json"}, "Unexpected publication file set")
    mutations = 0
    for name, record in records.items():
        path = PurePosixPath(name)
        require(not path.is_absolute() and ".." not in path.parts, "Unsafe path")
        require(not any((ROOT / Path(*path.parts[:i])).is_symlink() for i in range(1, len(path.parts) + 1)), "Symlink not allowed")
        data = (ROOT / name).read_bytes()
        expected = {key: record[key] for key in ("bytes", "sha256")}
        require(fingerprint(data) == expected, "Publication integrity mismatch: " + name)
        require(bool(data), "Unexpected empty file")
        for altered in (bytes([data[0] ^ 1]) + data[1:], data[:-1], data + b"!"):
            require(fingerprint(altered) != expected, "Integrity negative control failed")
            mutations += 1
    members = 0
    for dirname, archive, prefix in (
        ("author", "hochman_4400001_PUBLIC_SAFE.zip", "4400001/"),
        ("audit", "hochman_4400001_INDEPENDENT_PUBLIC_SAFE.zip", "4400001-audit/"),
    ):
        expected = {prefix + p.relative_to(ROOT / dirname).as_posix(): p
                    for p in (ROOT / dirname).rglob("*") if p.is_file()}
        with zipfile.ZipFile(ROOT / "archives" / archive) as z:
            require(len(z.namelist()) == len(expected) and set(z.namelist()) == set(expected), "Unexpected archive members")
            for name, path in expected.items():
                require(z.read(name) == path.read_bytes(), "Archive member mismatch: " + name)
                members += 1
    command = [sys.executable, "-B", str(ROOT / "audit" / "verify_audit.py"),
               "--author-dir", str(ROOT / "author"),
               "--author-archive", str(ROOT / "archives" / "hochman_4400001_PUBLIC_SAFE.zip")]
    audit = json.loads(subprocess.check_output(command))
    require(audit["status"] == "pass" and audit["author_directory_checked"]
            and audit["author_archive_checked"], "Bound audit replay failed")
    print(json.dumps({"status": "pass", "problem_id": "4400001",
                     "publication_files_verified": len(records), "manifest_self_excluded": True,
                     "archive_members_verified": members, "integrity_mutations_rejected": mutations,
                     "bound_audit": audit,
                     "scope": "Offline byte integrity and finite controls; not formal verification of the imported extension theorem."},
                    indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
