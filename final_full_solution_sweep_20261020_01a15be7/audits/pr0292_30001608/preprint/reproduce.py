#!/usr/bin/env python3
"""Read-only package validation and isolated reproduction, Python 3.11+."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify(root):
    manifest = load(root / "MANIFEST.json")
    expected = {row["path"] for row in manifest["files"]}
    require(len(expected) == len(manifest["files"]), "Repeated manifest path")
    actual = set()
    for path in root.rglob("*"):
        require(not path.is_symlink(), f"Symlink in package: {path}")
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    require(actual == expected | {"MANIFEST.json"}, "Missing or unlisted package files")
    for row in manifest["files"]:
        rel = Path(row["path"])
        require(not rel.is_absolute() and ".." not in rel.parts, "Unsafe manifest path")
        content = (root / rel).read_bytes()
        require(len(content) == row["bytes"], f"Size mismatch: {rel}")
        require(hashlib.sha256(content).hexdigest() == row["sha256"], f"Hash mismatch: {rel}")
    return len(expected)


def execute(root, script, *arguments, failure_marker=None):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("PYTHONOPTIMIZE", None)
    proc = subprocess.run([sys.executable, str(root / script), *arguments],
                          cwd=root, env=env, text=True, capture_output=True)
    if failure_marker is not None:
        require(proc.returncode != 0 and failure_marker in proc.stderr,
                f"Negative control failed to reject: {script}")
        return {"expected_rejection": True, "marker": failure_marker}
    require(proc.returncode == 0, f"Reproduction failed: {script}\n{proc.stderr}")
    return json.loads(proc.stdout)


def simulation_equal(actual, expected):
    """Only Monte Carlo diagnostic floats admit platform roundoff tolerance."""
    if isinstance(expected, dict):
        return isinstance(actual, dict) and actual.keys() == expected.keys() and all(
            simulation_equal(actual[key], value) for key, value in expected.items())
    if isinstance(expected, list):
        return isinstance(actual, list) and len(actual) == len(expected) and all(
            simulation_equal(a, b) for a, b in zip(actual, expected))
    if isinstance(expected, float):
        return isinstance(actual, (int, float)) and math.isfinite(actual) and math.isclose(
            actual, expected, rel_tol=1e-10, abs_tol=1e-10)
    return actual == expected


def main():
    require(sys.version_info >= (3, 11), "Python 3.11 or newer is required")
    require(not sys.flags.optimize, "Run without -O: historical controls use assert")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--integrity-only", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    count = verify(root)
    if args.integrity_only:
        print(json.dumps({"status": "PASS_INTEGRITY_ONLY", "hashed_files": count}))
        return
    results = []
    with tempfile.TemporaryDirectory(prefix="dfc-stability-reproduction-") as temporary:
        work = Path(temporary) / "dfc_stability_verification"
        shutil.copytree(root, work)
        result = execute(work, "original/verify_package.py")
        require(result["status"] == "PASS" and result["evidence_checks"] == 72,
                "Original manifest-chain checks changed")
        results.append({"check": "original_manifest_chain", "evidence_checks": 72})
        for number in range(1, 5):
            result = execute(work, f"original/checks/turn{number}_checks.py")
            require(result == load(work / f"original/checks/turn{number}_output.json"),
                    f"Original turn {number} output changed")
            results.append({"check": f"original_turn_{number}", "assertions": result["assertions"]})
        result = execute(work, "original/checks/independent_review_portable.py")
        require(result == load(work / "original/review/independent_checks.json"),
                "Original portable independent-check output changed")
        results.append({"check": "original_independent", "assertions": result["total_assertions"]})
        result = execute(work, "reviews/foster_recheck_02/verify_evidence.py")
        require(result["hashed_files_checked"] == 58, "Fresh Foster evidence-chain mismatch")
        results.append({"check": "foster_evidence_chain", "hashed_files": 58})
        result = execute(work, "reviews/foster_recheck_02/exact_falsification.py")
        require(result == load(work / "reviews/foster_recheck_02/exact_falsification_output.json"),
                "Independent tridiagonal/exact-boundary output changed")
        results.append({"check": "independent_tridiagonal", "assertions": result["assertions"],
                        "negative_controls": len(result["negative_controls"])})
        expected = load(work / "reviews/source_recheck_02/CONTROL_RESULTS.json")
        execute(work, "reviews/source_recheck_02/independent_controls.py")
        actual = load(work / "reviews/source_recheck_02/CONTROL_RESULTS.json")
        for value in (actual, expected):
            for field in ("started_utc", "finished_utc", "elapsed_seconds"):
                value.pop(field)
        simulation = actual.pop("finite_horizon_diagnostic")
        expected_simulation = expected.pop("finite_horizon_diagnostic")
        require(actual == expected, "Independent exact source/model controls changed")
        require(simulation_equal(simulation, expected_simulation),
                "Seeded finite-horizon diagnostic changed beyond stated rounding tolerance")
        results.append({"check": "independent_source_model", "exact_states": 1635,
                        "negative_controls": 4, "simulation": "reproduced diagnostic only"})
        for script, output in (("identity_controls.py", "identity_controls.stdout"),
                               ("theorem_transfer_control.py", "theorem_transfer_control.stdout")):
            result = execute(work, f"reviews/priority_recheck_02/{script}")
            expected = load(work / f"reviews/priority_recheck_02/{output}")
            result.pop("utc")
            expected.pop("utc")
            require(result == expected, f"Protocol/transfer control changed: {script}")
            results.append({"check": script, "matched_frozen_output": True})
        results.append(execute(work, "reviews/priority_recheck_02/identity_controls.py",
                               "--false-identity",
                               failure_marker="EXPECTED_REJECTION: Common Chunk is not DFC"))
    require(verify(root) == count, "Frozen package changed during reproduction")
    print(json.dumps({"status": "PASS_COMPLETE_REPRODUCTION", "hashed_files": count,
                      "checks": results,
                      "scope": "Finite exact controls and one labelled simulation. The universal theorem is proved analytically in main.tex."}, indent=2))


if __name__ == "__main__":
    main()
