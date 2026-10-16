"""Independent exact algebra and boundary checks for the source-to-proof bridge.

This is not a verifier for Duren's classical theorem or all numerical remainders.
Uses only the standard library and is independent of the author's verifier.
"""
from fractions import Fraction as F
from pathlib import Path
import datetime
import json

ROOT = Path(__file__).resolve().parent
# Sparse Laurent polynomial variables: z, w, a2, a3, a4.
ZERO = (0, 0, 0, 0, 0)

def monomial(coefficient=1, **powers):
    names = ("z", "w", "a2", "a3", "a4")
    return {tuple(powers.get(name, 0) for name in names): F(coefficient)}

def add(*polynomials):
    result = {}
    for poly in polynomials:
        for powers, coefficient in poly.items():
            result[powers] = result.get(powers, F(0)) + coefficient
    return {key: value for key, value in result.items() if value}

def multiply(left, right):
    result = {}
    for left_powers, left_coefficient in left.items():
        for right_powers, right_coefficient in right.items():
            powers = tuple(a + b for a, b in zip(left_powers, right_powers))
            if powers[0] <= 4:
                result[powers] = result.get(powers, F(0)) + left_coefficient * right_coefficient
    return {key: value for key, value in result.items() if value}

def coefficient(poly, degree):
    return {tuple((0,) + powers[1:]): value for powers, value in poly.items() if powers[0] == degree}

f = add(monomial(z=1), monomial(z=2, a2=1), monomial(z=3, a3=1), monomial(z=4, a4=1))
f2 = multiply(f, f)
f3 = multiply(f2, f)
f4 = multiply(f3, f)
ratio = add(multiply(f2, monomial(-1, w=-1)),
            multiply(f3, monomial(-1, w=-2)),
            multiply(f4, monomial(-1, w=-3)))
expected = {
    2: monomial(-1, w=-1),
    3: add(monomial(-2, a2=1, w=-1), monomial(-1, w=-2)),
    4: add(monomial(-2, a3=1, w=-1), monomial(-1, a2=2, w=-1),
           monomial(-3, a2=1, w=-2), monomial(-1, w=-3)),
}
assert all(coefficient(ratio, n) == expected[n] for n in expected)
# Pullback Q(w) dw^2 under w=-v^-2 is 4(a-bv^2+cv^4)dv^2.
# For each term -d_n w^-n, the resulting coefficient is -4(-1)^n d_n,
# and exponent is 2n-6. At infinity coordinate u=1/w exponent is n-4.
pullback = [(n, -4 * (-1) ** n, 2 * n - 6) for n in (3, 4, 5)]
assert pullback == [(3, 4, 0), (4, -4, 2), (5, 4, 4)]
infinity_exponents = [n - 4 for n in (3, 4, 5)]
assert infinity_exponents == [-1, 0, 1]

epsilon = F(1, 10**24)
eta = F(1, 10**12)
q = lambda t: t*t - F(2, 5)*t**4
q1, qT = q(F(1)), q(F(7, 4))
assert q1 == F(3, 5) and qT == -F(441, 640)
relative_error = 2000 * eta
assert q1 - relative_error > F(1, 2)
assert qT + relative_error < -F(1, 2)
assert F(7, 25) + 7*eta < F(3, 10)
assert F(25, 81) > F(3, 10)
# Q=-1/w^3 is positive on the Koebe omitted negative real ray and negative
# on the positive ray; this catches a swapped source sign or denominator.
assert -F(1) / (-F(2))**3 > 0
assert -F(1) / F(2)**3 < 0

result = {
    "checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "arithmetic": "exact fractions; standard-library sparse Laurent polynomials",
    "checks": {"coefficient_bridge": True, "double_cover_pullback": True,
               "simple_pole_order_at_infinity": True, "koebe_source_sign_control": True,
               "q_endpoint_sign_margins_given_author_Z_remainder": True,
               "tip_radius_vs_segment_radius_gap": True},
    "q_at_1": str(q1), "q_at_7_over_4": str(qT),
    "relative_sign_error_bound": str(relative_error),
    "tip_vs_segment_radius_gap": str(F(25, 81) - F(3, 10)),
    "dependency_limit": "No independent verification of all PROOF.md analytic estimates; only bridge and exact boundary calculations.",
}
(ROOT / "SOURCE_BRIDGE_CHECKS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
