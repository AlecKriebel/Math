#!/usr/bin/env python3
"""Replay diagnostic scripts in temporary directories, leaving evidence unchanged.

MTY uses the preserved explicit-check script. WXY uses the exactly mapped,
optimization-safe derivative, never the original assertion-based script in
optimized modes. No source PDFs, dataset records, or network are required.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run_script(source, mode, output_name):
    with tempfile.TemporaryDirectory(prefix="barycentric-diagnostic-") as tmp:
        path = Path(tmp) / "diagnostic.py"
        path.write_bytes(source)
        command = [sys.executable, "-B"] + ([mode] if mode else []) + [str(path)]
        env = os.environ.copy()
        env.pop("PYTHONOPTIMIZE", None)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=300)
        generated = Path(tmp) / output_name
        data = generated.read_bytes() if generated.exists() else None
        return result, data


def main():
    # Dependencies are checked before any mathematical diagnostic is run.
    import mpmath
    import numpy
    import scipy
    import sympy
    derivation = json.loads((ROOT / "integrity/CHECKER_DERIVATION.json").read_text())
    original_map = json.loads((ROOT / "integrity/ORIGINAL_ARTIFACT_MAP.json").read_text())
    mty_pin = next(x for x in original_map["artifacts"] if x["output_path"] == "mty/check_constants.py")
    mty = (ROOT / "mty/check_constants.py").read_bytes()
    wxy = (ROOT / derivation["derived_path"]).read_bytes()
    require(digest(mty) == mty_pin["output_sha256"], "MTY checker pin mismatch")
    require(digest(wxy) == derivation["derived_sha256"], "Derived WXY checker pin mismatch")
    require(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(wxy))), "Derived WXY checker contains optimization-sensitive assertions")
    results = []
    for label, source, reference, output_name in (
        ("MTY", mty, "mty/DIAGNOSTIC_RESULTS.json", "DIAGNOSTIC_RESULTS.json"),
        ("WXY_optimization_safe", wxy, "wxy/NORMALIZATION_CHECKS.json", "NORMALIZATION_CHECKS.json"),
    ):
        expected_bytes = (ROOT / reference).read_bytes()
        expected = json.loads(expected_bytes)
        for mode in ("", "-O", "-OO"):
            result, data = run_script(source, mode, output_name)
            require(result.returncode == 0 and data is not None, label + " failed in " + (mode or "normal") + " mode: " + result.stderr[-2000:])
            value = json.loads(data)
            if label == "MTY":
                exact_keys = [k for k in expected if k != "ellipsoid_transform_quadrature"]
                require(all(value.get(k) == expected[k] for k in exact_keys), "MTY exact diagnostic result changed")
                summary = {"eigenvalue_cases": len(value["inverse_radon_eigenvalue_checks"]), "quadrature_directions": len(value["ellipsoid_transform_quadrature"])}
            else:
                require(value["exact_spectral_checks"] == expected["exact_spectral_checks"], "WXY symbolic spectral result changed")
                require(value["exact_latitude_primitives_n3_n4"] == "passed", "WXY primitive result changed")
                require([x["n"] for x in value["numerical_phase_checks"]] == [3, 4, 5, 8], "WXY quadrature dimensions changed")
                summary = {"spectral_cases": len(value["exact_spectral_checks"]), "latitude_primitives": "n=3,n=4", "maximum_quadrature_residual": max(x["residual_magnitude"] for x in value["numerical_phase_checks"])}
            results.append({"checker": label, "python_mode": mode or "normal", "status": "PASS", "generated_bytes": len(data), "generated_sha256": digest(data), "recorded_output_byte_match": data == expected_bytes, "summary": summary})
    # Deliberately force one wrong algebraic residual to check that rejection
    # remains active in all modes. This altered temporary diagnostic is never
    # used as proof evidence and is not retained.
    needle = b"residual = sp.simplify(lam - claimed)"
    require(wxy.count(needle) == 1, "Negative-control injection is not unique")
    negative = wxy.replace(needle, b"residual = sp.Integer(1)", 1)
    rejection = []
    for mode in ("", "-O", "-OO"):
        result, data = run_script(negative, mode, "NORMALIZATION_CHECKS.json")
        require(result.returncode != 0 and "AssertionError: (3, 1, 1)" in result.stderr and data is None, "WXY forced failure was not rejected in " + (mode or "normal"))
        rejection.append({"python_mode": mode or "normal", "forced_wrong_spectral_residual_rejected": True})
    print(json.dumps({"schema": "barycentric-diagnostic-replay-1", "status": "PASS", "scope": "Finite diagnostics and optimization-safety checks only; not proof certification", "versions": {"python": platform.python_version(), "sympy": sympy.__version__, "mpmath": mpmath.__version__, "scipy": scipy.__version__, "numpy": numpy.__version__}, "preserved_mty_checker_sha256": digest(mty), "derived_wxy_checker_sha256": digest(wxy), "runs": results, "wxy_negative_control": rejection, "evidence_files_modified": False}, indent=2))


if __name__ == "__main__":
    main()
