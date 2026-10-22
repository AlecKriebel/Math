#!/usr/bin/env python3
"""Strict review gate for the pinned author packet and this audit packet.

Usage: python -I -B verify_audit.py AUTHOR_PUBLIC_DIR AUTHOR_FROZEN_ZIP
The output certifies byte membership and algebra replays, not analytic proofs.
"""
import argparse
import hashlib
import json
import pathlib
import stat
import subprocess
import sys
import tempfile
import zipfile


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def valid_name(name):
    return isinstance(name, str) and name not in ("", ".", "..") and "/" not in name and "\\" not in name


def check_directory(root, entries):
    require(root.is_dir() and not root.is_symlink(), "Root must be a real directory")
    require(all(valid_name(name) for name in entries), "Unsafe manifest member")
    paths = list(root.iterdir())
    require({p.name for p in paths} == set(entries), "Unexpected directory membership")
    for path in paths:
        require(stat.S_ISREG(path.lstat().st_mode), "Nonregular member: " + path.name)
        expected = entries[path.name]
        if expected is not None:
            require(digest(path.read_bytes()) == expected, "Byte/hash mismatch: " + path.name)


def check_zip(path, expected_digest, entries):
    require(stat.S_ISREG(path.lstat().st_mode), "ZIP must be a regular file")
    require(digest(path.read_bytes()) == expected_digest, "Author ZIP fingerprint mismatch")
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        names = [i.filename for i in infos]
        require(len(names) == len(set(names)), "Duplicate ZIP member")
        require(set(names) == set(entries), "Unexpected ZIP membership")
        require(not archive.comment, "Unexpected ZIP comment")
        for info in infos:
            mode = (info.external_attr >> 16) & 0xffff
            require(valid_name(info.filename) and not info.is_dir(), "Unsafe ZIP member")
            require(stat.S_IFMT(mode) in (0, stat.S_IFREG), "Nonregular ZIP member")
            require(not info.flag_bits & 1, "Encrypted ZIP member")
            require(digest(archive.read(info)) == entries[info.filename], "ZIP member hash mismatch")


def replay(script, record):
    with tempfile.TemporaryDirectory(prefix="gradient-audit-replay-") as cwd:
        for optimized in (False, True):
            command = [sys.executable, "-I", "-B"]
            if optimized:
                command.append("-O")
            command.append(str(script))
            proc = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True)
            require(json.loads(proc.stdout) == record, "Replay mismatch: " + script.name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("author_directory", type=pathlib.Path)
    parser.add_argument("author_zip", type=pathlib.Path)
    args = parser.parse_args()
    root = pathlib.Path(__file__).resolve().parent
    manifest = json.loads((root / "AUDIT_MANIFEST.json").read_text())
    own_entries = dict(manifest["files"])
    require("AUDIT_MANIFEST.json" not in own_entries, "Manifest must exclude itself")
    own_entries["AUDIT_MANIFEST.json"] = None
    check_directory(root, own_entries)
    baseline = json.loads((root / "AUTHOR_BASELINE.json").read_text())
    check_directory(args.author_directory, baseline["files"])
    check_zip(args.author_zip, baseline["zip"], baseline["files"])
    author_record = json.loads((args.author_directory / "EXACT_RESULTS.json").read_text())
    independent_record = json.loads((root / "INDEPENDENT_EXACT_RESULTS.json").read_text())
    replay(args.author_directory.resolve() / "verify_exact.py", author_record)
    replay(root / "verify_independent.py", independent_record)
    require(author_record["checks"] == independent_record["checks"] == 43, "Wrong control count")
    require(author_record["negative_witnesses"] == independent_record["negative_witnesses"], "Witness disagreement")
    print(json.dumps({"result": "PASS", "author_files": len(baseline["files"]),
                      "audit_payload_files": len(manifest["files"]),
                      "strict_directory_and_zip_membership": True,
                      "author_normal_and_optimized": True,
                      "independent_normal_and_optimized": True,
                      "different_cwd": True, "checks_per_suite": 43,
                      "scope": "Byte and algebra gate; analytic acceptance is in ACCEPTANCE.md; full general-potential target remains unsolved."},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
