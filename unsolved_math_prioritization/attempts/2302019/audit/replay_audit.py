#!/usr/bin/env python3
"""Fresh audit controls for the separately frozen author packet.

This script does not modify the author packet. All mutations use temporary
copies. Numerical tests require mpmath and are expressly non-certified.
"""
import hashlib
import json
import math
from pathlib import Path
import platform
import runpy
import shutil
import subprocess
import sys
import tempfile

EXPECTED = "6584a3d052edae771b709241b7ee909e7684efe318c0045e7ad36118f6008f12"
ROOT = Path(__file__).resolve().parent.parent / "author"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(value, message):
    if not value:
        raise RuntimeError(message)


def execute(root, script, optimized=False):
    args = [sys.executable] + (["-O"] if optimized else [])
    result = subprocess.run(args + [str(root / script)],
                            capture_output=True, text=True, check=False)
    return result


def mutate_copy(name, mutator, expected_fragment):
    with tempfile.TemporaryDirectory(prefix="rank674-audit-") as temp:
        copy = Path(temp) / "author"
        shutil.copytree(ROOT, copy)
        mutator(copy)
        result = execute(copy, "verify_integrity.py")
        require(result.returncode != 0, name + " accepted")
        require(expected_fragment in result.stderr, name + " wrong rejection")
        return {"control": name, "rejected": True,
                "rejection": expected_fragment}


def edit_manifest(root, transform):
    path = root / "AUTHOR_MANIFEST.json"
    data = json.loads(path.read_text())
    transform(data)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def same_length_change(root):
    path = root / "PROOFS.md"
    b = path.read_bytes()
    path.write_bytes(b.replace(b"# Problem", b"# problem", 1))


def main():
    require(__debug__, "Run without Python optimization")
    require(digest(ROOT / "AUTHOR_MANIFEST.json") == EXPECTED,
            "Wrong externally authenticated author manifest")
    original_math = execute(ROOT, "verify_math.py")
    require(original_math.returncode == 0, "Author math replay failed")
    require(original_math.stdout == (ROOT / "EXPECTED_CHECKS.json").read_text(),
            "Author replay output mismatch")
    original_integrity = execute(ROOT, "verify_integrity.py")
    require(original_integrity.returncode == 0, "Author integrity replay failed")

    controls = [mutate_copy("same-length proof corruption", same_length_change,
                            "digest: PROOFS.md"),
                mutate_copy("missing listed file",
                            lambda r: (r / "PROOFS.md").unlink(),
                            "unexpected or missing file"),
                mutate_copy("extra unlisted file",
                            lambda r: (r / "extra.txt").write_text("audit test"),
                            "unexpected or missing file"),
                mutate_copy("duplicate manifest path",
                            lambda r: edit_manifest(r, lambda d:
                                d["files"].append(dict(d["files"][0]))),
                            "file order or duplicate path"),
                mutate_copy("symbolic link in packet",
                            lambda r: (r / "link.txt").symlink_to("PROOFS.md"),
                            "symlink in author packet"),
                mutate_copy("false byte count",
                            lambda r: edit_manifest(r, lambda d:
                                d["files"][0].update(bytes=d["files"][0]["bytes"]+1)),
                            "byte count: EXPECTED_CHECKS.json")]

    optimization = []
    for script in ("verify_math.py", "verify_integrity.py"):
        result = execute(ROOT, script, optimized=True)
        require(result.returncode != 0 and "assertions are required" in result.stderr,
                "Optimization guard failure: " + script)
        optimization.append({"script": script, "optimization_rejected": True})

    # A file-plus-manifest rewrite can pass internal consistency. The
    # separately authenticated manifest digest must reject that rewrite.
    with tempfile.TemporaryDirectory(prefix="rank674-binding-") as temp:
        copy = Path(temp) / "author"
        shutil.copytree(ROOT, copy)
        same_length_change(copy)
        def rehash(data):
            for entry in data["files"]:
                if entry["path"] == "PROOFS.md":
                    entry["sha256"] = digest(copy / "PROOFS.md")
        edit_manifest(copy, rehash)
        require(execute(copy, "verify_integrity.py").returncode == 0,
                "Expected internally consistent forgery did not pass")
        require(digest(copy / "AUTHOR_MANIFEST.json") != EXPECTED,
                "External binding failed to distinguish rewritten packet")

    import mpmath as mp
    mp.mp.dps = 70
    high_precision_checks = 0
    numerical_points = 0
    def check(value, message):
        nonlocal high_precision_checks
        require(value, message)
        high_precision_checks += 1

    # Independently evaluate the primitive using the sine integral, rather
    # than the author's coefficient recurrence. Remove its apparent pole.
    def primitive(a, z):
        if z == 0:
            return mp.mpf(0)
        return mp.si(2*a*z)/a - mp.sin(a*z)**2/(a*a*z)

    author = runpy.run_path(str(ROOT / "verify_math.py"))
    for z in (0, mp.mpf("0.01"), mp.mpf("-8"), 8,
              mp.mpc("-2", "0.1"), mp.mpc("0.5", "2"),
              mp.mpc("3", "-2")):
        reference = primitive(mp.mpf("0.25"), z)
        actual = author["integrated_sinc"](0.25, complex(z))
        check(abs(actual-reference) < mp.mpf("1e-13"), "Primitive comparison")

    ratios = [mp.mpf(t) for t in
              ("0.000001", "0.01", "0.2", "0.5", "0.99", "0.99999999")]
    min_D_over_d = mp.inf
    max_witness_over_ramp = mp.mpf(0)
    for r in ratios:
        L = 1-r
        delta = min(r, 1-r)
        def witness(z):
            return r + delta/(2*mp.pi)*primitive(mp.mpf("0.25"), z)
        gap = witness(1)-r
        check(gap > mp.mpf(9025)/73728*delta, "Strict rational witness gap")
        check(witness(-1) < r < witness(1), "Finite real asymmetry")
        for x in (-5, mp.mpf("-0.1"), 0, L/4, L/2, L, 2):
            for y in map(mp.mpf, ("0.0001", "0.03", "0.5", "5")):
                numerical_points += 1
                z = mp.mpc(x, y)
                theta = mp.arg(z)
                log_step = y + theta/mp.pi*mp.log(r)
                # t=x+y*tan(u) makes the Poisson measure exactly du.
                lo, hi = mp.atan(-x/y), mp.atan((L-x)/y)
                def integrand(u):
                    t = x+y*mp.tan(u)
                    return -mp.log(r+t)/mp.pi
                D = mp.quad(integrand, [lo, (lo+hi)/2, hi])
                d = L*y*mp.log(2/(r+1))/(2*mp.pi*((abs(x)+L/2)**2+y*y))
                log_ramp = log_step-D
                check(D >= d > 0, "Positive explicit ramp penalty")
                check(log_ramp < log_step, "Strict step improvement")
                check(mp.log(r)+y <= log_ramp+mp.mpf("1e-60"),
                      "Ramp not below admissible exponential lower bound")
                ratio = abs(witness(z))*mp.exp(-log_ramp)
                check(ratio <= 1+mp.mpf("1e-60"), "Witness exceeds ramp")
                check(abs(witness(z.conjugate())-witness(z).conjugate())
                      < mp.mpf("1e-60"), "Lower-half-plane reflection")
                min_D_over_d = min(min_D_over_d, D/d)
                max_witness_over_ramp = max(max_witness_over_ramp, ratio)

    require(digest(ROOT / "AUTHOR_MANIFEST.json") == EXPECTED,
            "Author manifest changed during audit")
    final_integrity = execute(ROOT, "verify_integrity.py")
    require(final_integrity.returncode == 0, "Author bytes changed during audit")
    output = {
        "audit_id": "2302019-independent-reconstruction-audit-20261005-v1",
        "author_manifest_sha256": EXPECTED,
        "author_replay": json.loads(original_math.stdout),
        "author_integrity": json.loads(original_integrity.stdout),
        "adversarial_integrity_controls": controls,
        "adversarial_integrity_controls_passed": len(controls),
        "optimization_guards": optimization,
        "coherent_rewrite_control": {
            "internal_consistency_passed_as_expected": True,
            "external_manifest_binding_rejected": True},
        "independent_numerical_checks": {
            "status": "NON-CERTIFIED SMOKE ONLY",
            "mpmath_version": mp.__version__,
            "decimal_precision": mp.mp.dps,
            "parameter_ratios": [str(r) for r in ratios],
            "upper_half_plane_points": numerical_points,
            "checks_passed": high_precision_checks,
            "minimum_D_over_d": mp.nstr(min_D_over_d, 20),
            "maximum_witness_over_ramp": mp.nstr(max_witness_over_ramp, 20),
            "method": "Sine-integral primitive and angular-variable adaptive quadrature"},
        "python_version": platform.python_version(),
        "final_author_integrity_passed": True,
        "limitations": "Finite controls are not proofs of normality, recurrence, global caps, or the sharp target. No interval-arithmetic or quadrature error certification."
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
