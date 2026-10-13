#!/usr/bin/env python3
"""Verify the reader bytes and reproduce its two finite mathematical checks.

Python 3 standard library only. This is a byte-integrity and execution check,
not formal verification of any mathematical proof or an OS security sandbox.
The source scripts deliberately retain their accepted bytes and assertions.
"""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


PAIRS = (
    ("check_metric_identities.py", "CHECK_RESULTS.json"),
    ("check_adversarial_sanity.py", "ADVERSARIAL_CHECK_RESULTS.json"),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_manifest(root):
    manifest_path = root / "MANIFEST.json"
    require(not manifest_path.is_symlink(), "Manifest must not be a symlink")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["self_excluded"] == "MANIFEST.json", "Unexpected self exclusion")
    records = manifest["files"]
    names = [record["path"] for record in records]
    require(len(names) == len(set(names)), "Duplicate manifest names")
    require(names == sorted(names), "Manifest names must be sorted")
    require(all(Path(name).name == name and name not in (".", "..", "MANIFEST.json")
                for name in names), "Reader filenames must be flat and relative")
    expected = set(names) | {"MANIFEST.json"}
    require({item.name for item in root.iterdir()} == expected,
            "Reader has missing or unlisted files")
    for record in records:
        path = root / record["path"]
        require(path.is_file() and not path.is_symlink(),
                "Reader contains a non-file or symlink: " + record["path"])
        data = path.read_bytes()
        require(len(data) == record["bytes"], "Byte count mismatch: " + record["path"])
        require(digest(data) == record["sha256"], "SHA256 mismatch: " + record["path"])
    require(manifest["file_count_excluding_manifest"] == len(records),
            "Manifest file count mismatch")
    require(manifest["total_bytes_excluding_manifest"] == sum(r["bytes"] for r in records),
            "Manifest total byte count mismatch")


def main():
    require(sys.flags.optimize == 0 and __debug__,
            "Run without -O or -OO; the unchanged mathematical scripts use assertions")
    require(sys.flags.isolated == 1 and sys.dont_write_bytecode,
            "Run this verifier with python3 -I -B verify_reader.py")
    root = Path(__file__).resolve().parent
    verify_manifest(root)
    reproduced = []
    with tempfile.TemporaryDirectory(prefix="harmonic-circle-checks-") as temporary:
        work = Path(temporary)
        for script, expected_output in PAIRS:
            shutil.copyfile(root / script, work / script)
            shutil.copyfile(root / expected_output, work / expected_output)
        initial_files = {path.name for path in work.iterdir()}
        env = {"PATH": os.defpath, "LC_ALL": "C", "HOME": str(work)}
        for script, expected_output in PAIRS:
            run = subprocess.run(
                [sys.executable, "-I", "-B", script],
                cwd=work, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                check=False, timeout=120,
            )
            require(run.returncode == 0, script + " failed: " +
                    run.stderr.decode("utf-8", errors="replace"))
            require(not run.stderr, script + " produced unexpected standard error")
            expected = (work / expected_output).read_bytes()
            require(run.stdout == expected, script + " output differs from accepted bytes")
            require(json.loads(run.stdout)["result"] == "passed", script + " did not pass")
            reproduced.append({
                "script": script,
                "expected_output": expected_output,
                "result": "passed",
                "stdout_byte_identical": True,
                "stdout_bytes": len(run.stdout),
                "stdout_sha256": digest(run.stdout),
            })
        require({path.name for path in work.iterdir()} == initial_files,
                "A check generated unexpected files")
        for name in initial_files:
            require((work / name).read_bytes() == (root / name).read_bytes(),
                    "A check changed a copied input: " + name)
    verify_manifest(root)
    report = {
        "result": "passed",
        "manifest_bytes_and_complete_file_list": "verified before and after checks",
        "check_runs": reproduced,
        "isolation": {
            "python_flags": ["-I", "-B"],
            "optimization_disabled": True,
            "fresh_temporary_working_directory": True,
            "only_scripts_and_expected_outputs_copied": True,
            "minimal_subprocess_environment": True,
            "external_inputs_or_packages_required": False,
            "network_calls_in_check_scripts": False,
            "operating_system_security_sandbox_claimed": False,
        },
        "scope": "Exact finite algebraic sanity checks and byte integrity only; not formal or global proof verification.",
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
