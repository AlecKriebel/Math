#!/usr/bin/env python3
"""Rebuild the current package in relocated checkouts; preserve canonical files."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

AUDIT = Path(__file__).resolve().parent
PROGRAM = AUDIT.parent.parent


def main():
    expected = hashlib.sha256((AUDIT / "publication/verification_package.zip").read_bytes()).hexdigest()
    records = []
    with tempfile.TemporaryDirectory(prefix="pr570-producer-regression-", dir=PROGRAM / "tmp") as td:
        root = Path(td)

        def checkout(name):
            dest = root / name
            shutil.copytree(AUDIT, dest, ignore=shutil.ignore_patterns(
                ".cache", "qa", "__pycache__", "scratch", "receipts", "package_preflight*"))
            return dest

        def run(dest):
            return subprocess.run(["python3", str(dest / "publication/make_package.py")],
                                  capture_output=True, text=True)

        for name in ("ordinary/checkout", ".cache/checkout", "scratch/checkout"):
            dest = checkout(name)
            proc = run(dest)
            assert proc.returncode == 0, proc.stderr
            actual = hashlib.sha256((dest / "publication/verification_package.zip").read_bytes()).hexdigest()
            assert actual == expected, (name, actual, expected)
            records.append({"case": name, "status": "PASS", "zip_sha256": actual})

        for name, relative, reason in (
                ("cache_payload", ".cache/control.md", "Excluded source"),
                ("private_payload", "control.private.md", "Invalid or duplicate source"),
                ("traversal_payload", "../control.md", "Invalid relative path")):
            dest = checkout(name)
            snap = dest / "ORIGINAL_SNAPSHOT.json"
            obj = json.loads(snap.read_text())
            path = dest / "original" / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("excluded material control\n")
            obj["files"].append({"path": relative, "size": 1, "sha256": "0" * 64})
            snap.write_text(json.dumps(obj))
            proc = run(dest)
            assert proc.returncode != 0 and reason in proc.stderr, proc.stderr
            records.append({"case": name, "status": "REJECTED_AS_REQUIRED"})

        dest = checkout("parent_symlink_escape")
        shutil.rmtree(dest / "root_reproduction")
        outside = root / "outside"
        outside.mkdir()
        (outside / "control.json").write_text("{}\n")
        (dest / "root_reproduction").symlink_to(outside, target_is_directory=True)
        proc = run(dest)
        assert proc.returncode != 0 and "Source escapes the audit" in proc.stderr, proc.stderr
        records.append({"case": "parent_symlink_escape", "status": "REJECTED_AS_REQUIRED"})

        dest = checkout("leaf_symlink")
        selected = dest / "publication/weighted_centers.tex"
        selected.unlink()
        selected.symlink_to(outside / "control.json")
        proc = run(dest)
        assert proc.returncode != 0 and "Invalid or duplicate source" in proc.stderr, proc.stderr
        records.append({"case": "leaf_symlink", "status": "REJECTED_AS_REQUIRED"})
    print(json.dumps({"status": "PASS", "expected_zip_sha256": expected,
                      "canonical_files_modified": False, "cases": records}, indent=2))


if __name__ == "__main__":
    main()
