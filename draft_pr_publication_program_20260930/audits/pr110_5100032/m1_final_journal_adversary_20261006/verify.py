"""Bounded, exact controls for the independent journal-final comparison."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import math
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def require(condition, explanation):
    if not condition:
        raise RuntimeError(explanation)


def main():
    pins = json.loads((ROOT / "INPUT_PINS.json").read_text())
    checked = []
    for entry in pins["inputs"] + pins["private_auxiliaries"]:
        path = Path(entry["path"])
        data = path.read_bytes()
        require(len(data) == entry["bytes"], f"Size changed: {path}")
        require(hashlib.sha256(data).hexdigest() == entry["sha256"], f"Hash changed: {path}")
        checked.append(path.name)

    for entry in pins.get("git_blob_context_inputs", []):
        data = subprocess.check_output(["git", "show", entry["spec"]],
                                       cwd=entry["repository"])
        require(len(data) == entry["bytes"], "Git context size changed")
        require(hashlib.sha256(data).hexdigest() == entry["sha256"],
                "Git context hash changed")
        checked.append(entry["spec"])

    rotation_cases = []
    for n in (3, 5, 7, 9, 11):
        for p in range(1, n):
            if math.gcd(p, n) != 1:
                continue
            # At x=0, every phase N*(j*p/N) is an integer: cosine equals 1.
            phases = [n * Fraction(j * p, n) for j in range(n)]
            require(all(t.denominator == 1 for t in phases), "Nonintegral cosine phase")
            require(Fraction(n, 2).denominator == 2, "Missing odd half-turn sign change")
            # g+ = 3 and g- = 1 throughout this orbit, both strictly positive.
            plus_sum, minus_sum = 3 * n, n
            require(plus_sum - minus_sum == 2 * n, "Wrong finite-sum obstruction")
            rotation_cases.append({"primitive_period": n, "step_numerator": p,
                                   "phase_x": 0, "plus_sum": plus_sum,
                                   "minus_sum": minus_sum})

    # a=3,b=2,lambda=1,P=(sqrt(8),2/3): products and squared normals are rational.
    focal_radius_product = Fraction(41, 9)
    j_squared = Fraction(1, 36)
    normal_squared = Fraction(41, 324)
    actual_cosine = 2 * j_squared / normal_squared - 1
    printed_cosine = 1 / (2 * focal_radius_product) - 1
    require(actual_cosine == Fraction(-23, 41), "Reflection cosine control failed")
    require(printed_cosine == Fraction(-73, 82), "Printed cosine control failed")
    require(actual_cosine != printed_cosine, "Expected mismatch missing")
    # Divide kappa^(2/3) by (ab)^(2/3); no irrational arithmetic is needed.
    normalized_curvature = 1 / focal_radius_product
    from_correct_cosine = (1 + actual_cosine) / (2 * j_squared * 36)
    require(normalized_curvature == from_correct_cosine == Fraction(9, 41),
            "Curvature identity control failed")

    report = (ROOT / "REPORT.md").read_text()
    verdict = json.loads((ROOT / "VERDICT.json").read_text())
    require("bounded" in report.lower(), "Missing scope qualification")
    require(verdict["direct_covering_theorem_found"] is False, "Verdict drift")
    require(verdict["exact_claim_proof_citation_found"] is False, "Citation verdict drift")
    require(verdict["spatial_rule_suffices_for_odd_finite_sums"] is False, "Transfer verdict drift")
    print(json.dumps({"status": "PASS", "python": sys.version,
                      "optimization": sys.flags.optimize,
                      "full_byte_pins_checked": len(checked),
                      "rotation_cases": rotation_cases,
                      "reflection_control": {"actual_cosine": str(actual_cosine),
                                              "printed_cosine": str(printed_cosine),
                                              "normalized_curvature": str(normalized_curvature)},
                      "envelope_limit": "Pin and exact-control verification; human-readable mathematical comparison is not machine-certified."},
                     sort_keys=True))


if __name__ == "__main__":
    main()
