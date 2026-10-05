#!/usr/bin/env python3
"""Exact finite controls for the independent peripheral audit.

All matrix arithmetic uses Fraction. These are falsification controls, not a
finite-dimensional approximation to the spectrum on C(U). No source checker
or source reviewer is imported or executed. Output remains in this directory.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import sys


def mat(rows):
    return [[F(x) for x in row] for row in rows]


def eye(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def mul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def power(a, n):
    r = eye(len(a))
    while n:
        if n % 2:
            r = mul(r, a)
        a = mul(a, a)
        n //= 2
    return r


def sub(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def norm_inf(a):
    return max(sum(abs(x) for x in row) for row in a)


def strings(a):
    return [[str(x) for x in row] for row in a]


checks = []


def record(name, **evidence):
    checks.append({"name": name, "passed": True, **evidence})


# Oblique projection: ||x||_* = ||T x||_infinity, not the Euclidean norm.
t = mat([[1, 2], [0, 1]])
ti = mat([[1, -2], [0, 1]])
d = mat([[1, 0], [0, F(1, 2)]])
p0 = mat([[1, 0], [0, 0]])
a = mul(mul(ti, d), t)
p = mul(mul(ti, p0), t)
assert a == mat([[1, 1], [0, F(1, 2)]])
assert p == mat([[1, 2], [0, 0]])
assert mul(p, p) == p and mul(a, p) == mul(p, a)
assert norm_inf(mul(mul(t, a), ti)) == 1
assert norm_inf(mul(mul(t, p), ti)) == 1
gaps = {}
for n in (1, 2, 10, 40):
    expected = mat([[1, 2 * (1 - F(1, 2) ** n)], [0, F(1, 2) ** n]])
    assert power(a, n) == expected
    gap = norm_inf(mul(mul(t, sub(expected, p)), ti))
    assert gap == F(1, 2) ** n
    gaps[str(n)] = str(gap)
record("oblique_projection_in_adapted_complex_norm", A=strings(a), P=strings(p),
       norm_definition="max(|x+2y|,|y|)", adapted_A_norm="1",
       adapted_P_norm="1", euclidean_P_norm_squared="5", power_gap=gaps)

# Stable nontrivial Jordan block together with peripheral phase -1.
t3 = mat([[1, 2, 3], [0, 1, 0], [0, 0, 1]])
ti3 = mat([[1, -2, -3], [0, 1, 0], [0, 0, 1]])
d3 = mat([[-1, 0, 0], [0, F(1, 2), F(1, 4)], [0, 0, F(1, 2)]])
p03 = mat([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
a3 = mul(mul(ti3, d3), t3)
p3 = mul(mul(ti3, p03), t3)
assert norm_inf(d3) == 1
stable_gaps = {}
for n in (2, 4, 10, 40):
    expected = mat([[(-1) ** n, 0, 0],
                    [0, F(1, 2) ** n, n * F(1, 4) * F(1, 2) ** (n - 1)],
                    [0, 0, F(1, 2) ** n]])
    assert power(d3, n) == expected
    transformed_gap = mul(mul(t3, sub(power(a3, n), p3)), ti3)
    gap = norm_inf(transformed_gap)
    assert gap == F(1, 2) ** n * (1 + F(n, 2))
    stable_gaps[str(n)] = str(gap)
assert power(d3, 41)[0][0] == -1
record("even_recurrence_with_stable_Jordan_and_nonorthogonal_P",
       A=strings(a3), P=strings(p3), even_power_gap=stable_gaps,
       odd_power_warning="odd powers approach -P; the full sequence does not approach P")

# Forbidden peripheral Jordan candidate grows and cannot be contractive in any norm.
j = mat([[1, 1], [0, 1]])
for n in (1, 2, 100):
    assert power(j, n) == mat([[1, n], [0, 1]])
record("peripheral_Jordan_countercandidate_excluded", power_formula="J^n=[[1,n],[0,1]]",
       proof_reference="INDEPENDENT_PROOF.md Section 1, reverse triangle inequality")

# Finite eigenvalue groups are encoded as exponents in roots of unity.
group4 = {(p1 - q1 + 2 * (p2 - q2)) % 4
          for p1 in range(5) for q1 in range(5)
          for p2 in range(5) for q2 in range(5)}
assert group4 == {0, 1, 2, 3}
record("monomial_weights_for_i_and_minus_one", root_order=4,
       generated_exponents=sorted(group4), negative_exponents="realized by conjugates")

# Gamma is fourth roots, lambda is a primitive eighth root outside Gamma.
# Work in Q[zeta_8], reducing zeta_8^(e+4)=-zeta_8^e, so exact averages vanish.
cesaro = []
for mu_exp in (0, 2, 4, 6):
    ratio_exp = (mu_exp - 1) % 8
    coeffs = Counter()
    for n in range(8):
        e = (n * ratio_exp) % 8
        coeffs[e % 4] += 1 if e < 4 else -1
    assert all(coeffs[e] == 0 for e in range(4))
    cesaro.append({"mu_exponent_mod8": mu_exp,
                   "lambda_exponent_mod8": 1, "sum_reduced_coefficients": [coeffs[e] for e in range(4)]})
record("exact_Cesaro_exclusion_outside_finite_Gamma", average_length=8, controls=cesaro,
       limitation="The dense-group case is proved by fixed-polynomial approximation, not sampled here.")

# Nilpotent remainder after exactly two powers, including all-zero E.
dn = mat([[1, 0, 0], [0, 0, F(1, 2)], [0, 0, 0]])
pn = mat([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
assert norm_inf(dn) == 1 and power(dn, 2) == pn
assert mul(mat([[0, 0, 1]]), dn) == mat([[0, 0, 0]])
all_nil = mat([[0, F(1, 2)], [0, 0]])
assert power(all_nil, 2) == mat([[0, 0], [0, 0]])
record("nilpotent_peripheral_split_and_E_zero", mixed_A=strings(dn),
       mixed_A_squared=strings(pn), zero_eigenfunction="f(x)=x_3",
       all_nilpotent_A=strings(all_nil), all_nilpotent_A_squared=strings(power(all_nil, 2)),
       A_zero_CU_spectrum="{0,1} for k>=1, by independent projection proof")

here = Path(__file__).resolve().parent
original = here.parent / "original_source_authentication_20261005/original_attempt/CLASSIFICATION.md"
source_hash = hashlib.sha256(original.read_bytes()).hexdigest()
assert source_hash == "0abd5dd0918905b3a6c1e9c62a57097645bba6334cb625a4a4e88f2c12c4416b"
result = {
    "schema": "pr91-independent-peripheral-controls/v1",
    "UTC": datetime.now(timezone.utc).isoformat(), "actual_process_PID": os.getpid(),
    "python": sys.version, "cwd": str(Path.cwd()), "script": str(Path(__file__).resolve()),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "original_classification_SHA256": source_hash,
    "immutable_head": "2ea84c5de45cb92783b5b55057af1f52590be6bf",
    "author_review_imported_or_executed": False,
    "source_checker_imported_or_executed": False,
    "finite_controls_only": True, "check_count": len(checks),
    "all_passed": all(item["passed"] for item in checks), "checks": checks,
}
(here / "CHECK_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"UTC": result["UTC"], "actual_process_PID": result["actual_process_PID"],
                  "check_count": len(checks), "all_passed": result["all_passed"],
                  "result_path": str(here / "CHECK_RESULTS.json")}, indent=2))
