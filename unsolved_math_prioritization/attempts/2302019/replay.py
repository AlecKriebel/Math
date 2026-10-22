#!/usr/bin/env python3
"""Authenticate both independent freezes and replay their finite controls.

Requires unoptimized Python 3 and mpmath 1.3.0. No network or source files.
Authenticate PUBLICATION_MANIFEST.json against a separately recorded digest.
"""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
AUTHOR = "6584a3d052edae771b709241b7ee909e7684efe318c0045e7ad36118f6008f12"
AUDIT = "13356d28cf40480b72aafdd1a69a97074522d2bc6c9da2cadb6b17b518db9710"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root, name, expected_digest=None):
    manifest = root / name
    if expected_digest:
        require(digest(manifest) == expected_digest, "external manifest binding: " + name)
    data = json.loads(manifest.read_text(encoding="utf-8"))
    entries = data["files"]
    require(isinstance(entries, list) and entries, "empty or invalid inventory")
    paths = [e["path"] for e in entries]
    require(paths == sorted(set(paths)), "duplicate or unsorted inventory")
    actual = []
    for path in root.rglob("*"):
        require(not path.is_symlink(), "symbolic link: " + str(path))
        if path.is_file():
            actual.append(path.relative_to(root).as_posix())
        else:
            require(path.is_dir(), "nonregular entry: " + str(path))
    require(sorted(actual) == sorted(paths + [name]), "missing or unlisted file: " + name)
    for entry in entries:
        require(set(entry) == {"path", "bytes", "sha256"}, "invalid entry fields")
        path = PurePosixPath(entry["path"])
        require(not path.is_absolute() and ".." not in path.parts and str(path) == entry["path"], "unsafe path")
        content = (root / path).read_bytes()
        require(len(content) == entry["bytes"], "byte count: " + str(path))
        require(hashlib.sha256(content).hexdigest() == entry["sha256"], "digest: " + str(path))
    return len(entries)


def run(script):
    env = dict(os.environ)
    env.pop("PYTHONOPTIMIZE", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run([sys.executable, "-B", str(ROOT / script)],
                            cwd=ROOT, env=env, capture_output=True, text=True)
    require(result.returncode == 0, script + " failed:\n" + result.stderr)
    return result.stdout


def main():
    require(__debug__, "Run without Python optimization (-O/-OO are rejected).")
    count = inventory(ROOT, "PUBLICATION_MANIFEST.json")
    require(inventory(ROOT / "author", "AUTHOR_MANIFEST.json", AUTHOR) == 8, "author inventory size")
    require(inventory(ROOT / "audit", "AUDIT_MANIFEST.json", AUDIT) == 6, "audit inventory size")
    math_output = run("author/verify_math.py")
    require(math_output.encode() == (ROOT / "author/EXPECTED_CHECKS.json").read_bytes(), "author replay mismatch")
    integrity_output = json.loads(run("author/verify_integrity.py"))
    audit_output = json.loads(run("audit/replay_audit.py"))
    expected_audit = json.loads((ROOT / "audit/AUDIT_CHECKS.json").read_text())
    # Python version is provenance, not a portable arithmetic expectation.
    actual_python = audit_output.pop("python_version")
    historical_python = expected_audit.pop("python_version")
    require(audit_output == expected_audit, "audit replay mismatch beyond Python provenance")
    inventory(ROOT, "PUBLICATION_MANIFEST.json")
    print(json.dumps({
        "status": "PASS_FROZEN_INVENTORIES_AND_FINITE_REPLAY",
        "problem_id": 2302019,
        "target_status": "unsolved",
        "historical_turns": "5/5",
        "publication_inventory_files": count,
        "publication_manifest_sha256": digest(ROOT / "PUBLICATION_MANIFEST.json"),
        "author_manifest_sha256": AUTHOR,
        "audit_manifest_sha256": AUDIT,
        "author_integrity": integrity_output,
        "author_exact_controls": audit_output["author_replay"]["exact_rational_controls"],
        "author_float_smoke_controls": audit_output["author_replay"]["floating_point_smoke_controls"],
        "audit_float_smoke_controls": audit_output["independent_numerical_checks"]["checks_passed"],
        "adversarial_integrity_controls": audit_output["adversarial_integrity_controls_passed"],
        "author_optimization_guards": len(audit_output["optimization_guards"]),
        "coherent_rewrite_control": audit_output["coherent_rewrite_control"],
        "replay_python_version": actual_python,
        "historical_audit_python_version": historical_python,
        "limits": "Finite controls supplement written proofs; no certified quadrature, novelty claim, or sharp nonreal-bound solution."
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
