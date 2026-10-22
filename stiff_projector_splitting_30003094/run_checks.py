"""Replay the four NUMERICAL corroborations in a fresh temporary directory.

This is not a formal proof checker or exact-arithmetic certificate. Installed
NumPy, SciPy and mpmath are required; no source documents or datasets are used.
"""
import datetime
import decimal
import hashlib
import importlib.metadata
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time


CASES = [
    ("check_affine_counterexample.py", "affine_counterexample_results.json"),
    ("check_subclass_identities.py", "subclass_identity_results.json"),
    ("audit_exact_subflows.py", "audit_exact_subflows_results.json"),
    ("check_strang_obstruction.py", "strang_obstruction_results.json"),
]
TOLERANCES = {
    "numpy_scipy_result_comparison": {"absolute": "1e-12", "relative": "1e-10"},
    "mpmath_result_comparison": {"absolute": "1e-45", "relative": "1e-12"},
    "literal_vs_rearranged_residual_maximum": "1e-40",
    "literal_affine_identity_residual_maximum": "1e-40",
    "rank_two_identity_residual_maximum": "1e-10",
    "rank_two_local_bound_slack": "1e-12",
    "strang_identity_residual_maximum": "1e-50",
    "strang_lsk_bound_slack": "1e-50",
}
D = decimal.Decimal
decimal.getcontext().prec = 80
decimal.getcontext().Emax = 999999999
decimal.getcontext().Emin = -999999999


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def compare(actual, expected, atol, rtol, location="result"):
    """Exact structure/discrete fields; tolerant finite numeric values."""
    if isinstance(expected, dict):
        require(isinstance(actual, dict) and actual.keys() == expected.keys(),
                "JSON object keys differ at " + location)
        for key in expected:
            compare(actual[key], expected[key], atol, rtol, location + "." + key)
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(actual) == len(expected),
                "JSON list differs at " + location)
        for i, value in enumerate(expected):
            compare(actual[i], value, atol, rtol, location + "[" + str(i) + "]")
    elif isinstance(expected, (bool, int)) or expected is None:
        require(type(actual) is type(expected) and actual == expected,
                "Discrete value differs at " + location)
    else:
        numeric = isinstance(expected, float)
        if isinstance(expected, str):
            try:
                D(expected)
                numeric = True
            except decimal.InvalidOperation:
                pass
        if numeric:
            require(type(actual) is type(expected), "Numeric type differs at " + location)
            a, b = D(str(actual)), D(str(expected))
            require(a.is_finite() and b.is_finite(), "Nonfinite value at " + location)
            require(abs(a-b) <= atol + rtol * max(abs(a), abs(b)),
                    "Numerical comparison failed at " + location)
        else:
            require(actual == expected, "Text differs at " + location)


def semantic_checks(script, result):
    if script == "check_affine_counterexample.py":
        require(len(result["cases"]) == 9, "Expected nine affine examples")
        for row in result["cases"]:
            require(D(str(row["literal_vs_stable"])) < D("1e-40"),
                    "Literal versus rearranged subflows disagree")
            require(row["k_norm"] > 0, "Zero tested K endpoint")
        return {"cases": 9, "maximum_literal_vs_stable_residual":
                max(row["literal_vs_stable"] for row in result["cases"]),
                "last_sequence_error": result["cases"][-1]["error"]}
    if script == "check_subclass_identities.py":
        require(result["all_pass"] is True and result["seed"] == 1829,
                "Rank-two regression status differs")
        require(len(result["checks"]) == 24, "Expected 24 rank-two trials")
        largest = 0.0
        for row in result["checks"]:
            residual = max(row[key] for key in
                           ("linear_exactness_error", "right_identity_error", "left_identity_error"))
            require(residual < 1e-10, "Rank-two identity discrepancy")
            require(row["bound_pass"] is True and
                    row["left_local_error"] <= row["left_bound"] + 1e-12,
                    "Conditional local-bound regression failed")
            largest = max(largest, residual)
        return {"trials": 24, "maximum_identity_residual": largest,
                "conditional_local_bound_passes": 24}
    if script == "audit_exact_subflows.py":
        for name in ("two_sided", "one_sided", "vanishing_rough_initial_perturbation"):
            require(len(result[name]) == 3, "Expected three cases per literal-subflow family")
        largest = D(0)
        for name in ("one_sided", "vanishing_rough_initial_perturbation"):
            for row in result[name]:
                for key in ("K_formula_residual", "S_cancellation_residual", "projection_identity_residual"):
                    value = D(row[key])
                    require(value >= 0 and value < D("1e-40"), "Affine identity residual exceeds tolerance")
                    largest = max(largest, value)
        return {"cases": 9, "maximum_affine_identity_residual": str(largest),
                "two_sided_error_at_n300": result["two_sided"][-1]["error"],
                "one_sided_error_at_n300": result["one_sided"][-1]["error"],
                "rough_initializer_error_at_n10000": result["vanishing_rough_initial_perturbation"][-1]["error"]}
    require(script == "check_strang_obstruction.py", "Unrecognized checker")
    require(result["all_pass"] is True and len(result["checks"]) == 4, "Expected four Strang trials")
    for row in result["checks"]:
        require(D(row["LSK_endpoint_identity_residual"]) < D("1e-50"), "Strang endpoint identity discrepancy")
        require(D(row["LSK_error"]) <= D(row["LSK_error_bound"]) + D("1e-50"), "Strang LSK bound failed")
        require(row["first_S_positive"] is True and row["second_S_positive"] is True
                and row["all_QR_endpoints_nonzero"] is True, "Tested Strang rank check failed")
    return {"cases": 4, "strang_error_at_n300": result["checks"][-1]["Strang_error"],
            "tested_scalar_and_qr_endpoint_checks": "PASS; interval rank preservation is proved analytically"}


def main():
    require(__debug__, "Assertions must remain enabled; do not use -O or -OO")
    root = pathlib.Path(__file__).resolve().parent
    versions = {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "mpmath")}
    recorded = {"numpy": "2.3.5", "scipy": "1.17.0", "mpmath": "1.3.0"}
    started = time.monotonic()
    checks = []
    with tempfile.TemporaryDirectory(prefix="stiff-projector-replay-") as tmp:
        work = pathlib.Path(tmp)
        for script, _ in CASES:
            shutil.copyfile(root / script, work / script)
        for script, result_file in CASES:
            expected_bytes = (root / result_file).read_bytes()
            expected = json.loads(expected_bytes)
            # -I omits the script directory: add only this fresh, whitelisted
            # temporary directory so the Strang checker can import its sibling.
            command = ("import runpy,sys; sys.path.insert(0,'.'); "
                       "runpy.run_path(" + repr(script) + ",run_name='__main__')")
            done = subprocess.run([sys.executable, "-I", "-B", "-c", command],
                                  cwd=work, text=True, capture_output=True,
                                  timeout=600, check=False)
            require(done.returncode == 0, "Checker failed: " + script + "\n" + done.stderr)
            require(not done.stderr, "Unexpected checker stderr: " + script + "\n" + done.stderr)
            actual = json.loads(done.stdout)
            key = "numpy_scipy_result_comparison" if script == "check_subclass_identities.py" else "mpmath_result_comparison"
            tolerance = TOLERANCES[key]
            compare(actual, expected, D(tolerance["absolute"]), D(tolerance["relative"]))
            summary = semantic_checks(script, actual)
            checks.append({
                "script": script,
                "script_sha256": hashlib.sha256((root / script).read_bytes()).hexdigest(),
                "result_file": result_file,
                "reference_result_sha256": hashlib.sha256(expected_bytes).hexdigest(),
                "exit_code": done.returncode,
                "stderr": done.stderr,
                "stdout_sha256": hashlib.sha256(done.stdout.encode()).hexdigest(),
                "exact_json_match_this_run": actual == expected,
                "numerical_agreement_within_tolerances": True,
                "comparison_tolerance": tolerance,
                "semantic_checks": summary,
            })
        require({p.name for p in work.iterdir()} == {script for script, _ in CASES},
                "Checker wrote an unexpected file")
    print(json.dumps({
        "status": "PASS",
        "checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python_version": sys.version.split()[0],
        "dependencies": versions,
        "matches_recorded_dependency_versions": versions == recorded,
        "execution": "Fresh temporary directory containing only four checker scripts; subprocesses use Python -I -B and installed site packages. Only that temporary directory is re-added for the Strang sibling import. Checker scripts make no network requests and use no external datasets or source documents. Package is not modified.",
        "elapsed_seconds": round(time.monotonic()-started, 3),
        "tolerances": TOLERANCES,
        "checks": checks,
        "claim_limit": "NUMERICAL corroboration only, using floating-point and arbitrary-precision matrix exponentials. Not exact-arithmetic, interval, symbolic, or formal proof certificates. Analytic proofs and the mathematical audit are the acceptance basis; original problem remains UNSOLVED (5/5 avenues).",
    }, indent=2))


if __name__ == "__main__":
    main()
