#!/usr/bin/env python3
"""Copied producer portability and real excluded-source rejection controls."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

AUDIT = Path(__file__).resolve().parents[1]


def main():
    expected = hashlib.sha256((AUDIT / "publication/verification_package.zip").read_bytes()).hexdigest()
    cases = []
    with tempfile.TemporaryDirectory(prefix="producer-root-", dir=AUDIT / "root_reproduction/.cache") as tmp:
        top = Path(tmp)
        for ancestors in ("ordinary", ".cache/ancestor", "scratch/ancestor"):
            dest = top / ancestors / "audit"
            shutil.copytree(AUDIT, dest, ignore=shutil.ignore_patterns(".cache", "qa", "receipts", "package_preflight*"))
            proc = subprocess.run([sys.executable, "-B", str(dest / "publication/make_package.py")],
                                  capture_output=True, text=True,
                                  env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
            if proc.returncode or hashlib.sha256((dest / "publication/verification_package.zip").read_bytes()).hexdigest() != expected:
                raise RuntimeError("Relocated producer failed: " + ancestors + proc.stderr)
            cases.append({"control": "relocation:" + ancestors, "exact_zip": True})
        base = top / "ordinary/audit"
        for component in (".cache", "sources", "scratch", "qa", ".secrets", "named.private"):
            path = base / component / "extra.txt"
            path.parent.mkdir(exist_ok=True)
            path.write_text("excluded copied fixture\n")
        (base / "safe").mkdir()
        (base / "safe/extra.txt").write_text("safe copied fixture\n")
        (base / "through").symlink_to(base / ".cache", target_is_directory=True)
        (base / ".cache/alias").symlink_to(base / "safe", target_is_directory=True)
        (base / "leaf.txt").symlink_to(base / "safe/extra.txt")
        (top / "outside.txt").write_text("outside copied fixture\n")
        (base / "escape").symlink_to(top, target_is_directory=True)
        names = [component + "/extra.txt" for component in
                 (".cache", "sources", "scratch", "qa", ".secrets", "named.private")]
        names += ["through/extra.txt", ".cache/alias/extra.txt", "leaf.txt",
                  "escape/outside.txt", "../outside.txt", "ORIGINAL_SNAPSHOT.json"]
        for name in names:
            code = "import make_package as m; m.ROOT_FILES.append(" + repr(name) + "); m.main()"
            proc = subprocess.run([sys.executable, "-B", "-c", code], cwd=base / "publication",
                                  capture_output=True, text=True,
                                  env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
            if proc.returncode == 0:
                raise RuntimeError("Excluded or duplicate source accepted: " + name)
            if not any(s in proc.stderr for s in ("Excluded source", "Invalid relative path", "Invalid or duplicate source", "Source escapes")):
                raise RuntimeError("Rejected for an unrelated reason: " + name + proc.stderr)
            cases.append({"control": name, "required_rejection": True})
    print(json.dumps({"status": "PASS", "zip_sha256": expected,
                      "actual_controls": cases, "counts": {"exact_relocations": 3, "required_rejections": 12}},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
