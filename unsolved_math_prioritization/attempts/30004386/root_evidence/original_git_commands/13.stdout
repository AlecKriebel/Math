"""Exact diagnostics for normalization and coefficient approximations.

This is not a numerical proof of an LDP. The resolution is the cited theorem.
"""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import hashlib
import json

assertions = 0


def check(condition):
    global assertions
    assertions += 1
    assert condition


# Squared coefficients suffice: signs and square roots do not affect these checks.
families = {
    "Gaussian limit": lambda j: Q(0),
    "one uniform, boundary": lambda j: Q(1) if j == 1 else Q(0),
    "finite interior": lambda j: [Q(1, 4), Q(1, 9)][j-1] if j <= 2 else Q(0),
    "infinite interior": lambda j: Q(1, 4**j),
    "infinite norm-one boundary": lambda j: Q(3, 4**j),
}
dimensions = [2, 3, 4, 7, 9, 16, 25, 49, 100, 256, 1024]
summaries = []
for name, coefficient_square in families.items():
    for n in dimensions:
        m = isqrt(n)
        check(0 < m < n)
        first = [coefficient_square(j) for j in range(1, m + 1)]
        retained = sum(first, Q(0))
        check(Q(0) <= retained <= Q(1))
        filler_square = (1 - retained) / (n - m)
        check(filler_square >= 0)
        check(filler_square <= Q(1, n - m))
        check(retained + (n - m) * filler_square == 1)
        # Every finite E_n projection has the required variance exactly.
        check((retained + (n - m) * filler_square) / 3 == Q(1, 3))
        arranged = sorted(first + [filler_square] * (n - m), reverse=True)
        # Any retained coordinate exceeding the fillers stays at its sorted position.
        for j, value in enumerate(first):
            if value > filler_square:
                check(arranged[j] == value)
        # Lindeberg-tail fourth-power control, stated in squared-coefficient form.
        check((n - m) * filler_square**2 <= Q(1, n - m))
    summaries.append({"family": name, "dimensions": dimensions})

for norm_square in [Q(0), Q(1, 4), Q(13, 36), Q(1, 3), Q(99, 100), Q(1)]:
    variance = norm_square / 3 + (1 - norm_square) / 3
    check(variance == Q(1, 3))
    check(variance != Q(1))

# Fourth cumulant of Uniform[-1,1], and Gaussian normalization controls.
check(Q(1, 5) - 3 * Q(1, 3)**2 == Q(-2, 15))

root = Path(__file__).resolve().parent
result = {
    "all_passed": True,
    "assertions": assertions,
    "coefficient_families": summaries,
    "variance": "1/3",
    "arithmetic": "exact rational squared coefficients; no floating-point simulation",
    "source_status_sha256": hashlib.sha256((root / "SOURCE_STATUS.md").read_bytes()).hexdigest(),
    "scope": "Normalization and finite approximation diagnostics; published Theorem A supplies the LDP.",
}
(root / "check_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
