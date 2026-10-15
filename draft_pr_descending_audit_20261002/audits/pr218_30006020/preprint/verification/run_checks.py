#!/usr/bin/env python3
"""Replay finite controls, without network access or third-party dependencies.

The scripts are unmodified historical controls. Each runs with assertions
enabled in a separate temporary directory. Passing is finite evidence, not a
proof of a limit theorem or of any imported geometric theorem.
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import platform
import subprocess
import sys
import tempfile


ROOT = pathlib.Path(__file__).resolve().parent
CASES = (
    ("author_exact", "controls/author_exact.py", "expected/author_exact.json"),
    ("partition_exact", "controls/partition_exact.py", "expected/partition_exact.json"),
    ("labelled_permutations", "controls/labelled_permutations.py", "expected/labelled_permutations.json"),
    ("dvv_geometry", "controls/dvv_geometry.py", "expected/dvv_geometry_exact.json"),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def verify_payload():
    manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text())
    rows = manifest["files"]
    seen = set()
    for row in rows:
        name = row["path"]
        require(name not in seen, "Duplicate manifest entry: " + name)
        seen.add(name)
        path = (ROOT / name).resolve()
        require(path.is_relative_to(ROOT), "Path outside package: " + name)
        require(path.is_file(), "Missing payload: " + name)
        data = path.read_bytes()
        require(len(data) == row["bytes"], "Size mismatch: " + name)
        require(hashlib.sha256(data).hexdigest() == row["sha256"],
                "SHA-256 mismatch: " + name)
    for _, program, expected in CASES:
        require(program in seen and expected in seen,
                "Control or expected receipt absent from manifest")
    require("run_checks.py" in seen, "Runner absent from manifest")
    return len(rows)


def replay(name, program, expected_file):
    expected = json.loads((ROOT / expected_file).read_text())
    with tempfile.TemporaryDirectory(prefix="pr218-" + name + "-") as work:
        # -I ignores PYTHON* environment settings, including PYTHONOPTIMIZE.
        # No -O flag is passed: assertions in the preserved controls are active.
        call = subprocess.run(
            [sys.executable, "-I", "-B", str(ROOT / program)],
            cwd=work, text=True, capture_output=True, timeout=300, check=False,
        )
        require(call.returncode == 0,
                name + " failed:\n" + call.stderr + "\n" + call.stdout)
        require(not call.stderr.strip(), name + " wrote unexpected stderr")
        actual = json.loads(call.stdout)
        require(actual.get("status") == "PASS", name + " did not report PASS")
        if name == "dvv_geometry":
            # The preserved DVV program also prints ordinary floating-point
            # diagnostics. Only its rational records are receipt comparisons.
            exact = {"status": actual["status"],
                     "exact_records": actual["exact_records"]}
            require(exact == expected, name + " exact receipt changed")
            written = json.loads((pathlib.Path(work) / "EXACT_CHECK_RESULTS.json").read_text())
            require(written == actual, name + " stdout/file receipt disagree")
            cases = sum(row["compositions"] for row in exact["exact_records"])
            require(cases == 123, "Unexpected DVV composition coverage")
            return {
                "name": name, "status": "PASS",
                "rational_composition_cases": cases,
                "genus_range": [2, 5], "maximum_loops": 3,
                "additional_rational_controls":
                    "odd-binomial sums, prefactor ratios and six reference values",
                "floating_outputs_not_certified": {
                    "eta": actual["eta"],
                    "error_exponent_before_logs": actual["error_exponent_before_logs"],
                    "large_prefactor_ratios": actual["large_prefactor_ratios"],
                },
            }
        require(actual == expected, name + " exact receipt changed")
        result = {"name": name, "status": "PASS",
                  "exact_assertions": actual.get("total_exact_assertions",
                                                  actual.get("exact_assertions"))}
        if name == "labelled_permutations":
            result["labelled_permutations_traversed"] = actual["labelled_permutations_traversed"]
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=pathlib.Path,
                        help="also save the run receipt outside the sealed package")
    args = parser.parse_args()
    if args.receipt:
        require(not args.receipt.resolve().is_relative_to(ROOT),
                "Save a new receipt outside the sealed package")
    payload_files = verify_payload()
    results = [replay(*case) for case in CASES]
    require(sum(row.get("exact_assertions", 0) for row in results) == 7100,
            "Unexpected counted exact assertions")
    receipt = {
        "status": "PASS", "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": platform.python_version(), "implementation": platform.python_implementation(),
        "platform": platform.platform(), "third_party_dependencies": [],
        "sealed_payload_files_verified": payload_files,
        "counted_exact_assertions_excluding_dvv": 7100,
        "dvv_rational_composition_cases": 123,
        "results": results,
        "limits": "Finite regression and algebra controls only. No asymptotic, geometric-input, novelty, or publication certificate.",
    }
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.TimeoutExpired) as error:
        print("FAIL: " + str(error), file=sys.stderr)
        sys.exit(1)
