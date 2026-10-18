#!/usr/bin/env python3
"""Finite checks for the independent reconstruction; no assertion-only guards."""

from fractions import Fraction
from math import comb, cos, sin, sqrt, log, pi
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def q_coefficients(n):
    return [0] + [(-1) ** (k + 1) * comb(n, k) for k in range(1, n + 1)]


def polynomial_value(coefficients, t):
    value = Fraction(0)
    for coefficient in reversed(coefficients):
        value = value * t + coefficient
    return value


def exact_checks():
    """Exact coefficient/integral checks, separate from the geometric-sum proof."""
    records = []
    for n in range(1, 41):
        c = q_coefficients(n)
        origin_integral = -sum((Fraction(c[k], k) for k in range(1, n + 1)), Fraction(0))
        harmonic = sum((Fraction(1, k) for k in range(1, n + 1)), Fraction(0))
        require(origin_integral == -harmonic, f"origin integral failed at n={n}")
        require(sum(c) == 1, f"boundary input value failed at n={n}")
        for t in (Fraction(0), Fraction(1, 7), Fraction(1, 2), Fraction(5, 6), Fraction(1)):
            expanded = polynomial_value(c, t)
            geometric = t * sum(((1 - t) ** j for j in range(n)), Fraction(0))
            require(expanded == geometric, f"input polynomial mismatch n={n}, t={t}")
            require(0 <= expanded <= 1, f"input bound failed n={n}, t={t}")
            from_monomials = sum((Fraction(c[k], k) * ((k + 1) * t ** k - 1)
                                  for k in range(1, n + 1)), Fraction(0))
            integral = sum((Fraction(c[k], k) * (1 - t ** k)
                            for k in range(1, n + 1)), Fraction(0))
            require(from_monomials == expanded - integral,
                    f"output polynomial mismatch n={n}, t={t}")
            require(-harmonic <= from_monomials <= 1,
                    f"output endpoint bounds failed n={n}, t={t}")
        records.append({"n": n, "harmonic_exact": str(harmonic), "origin_exact": str(origin_integral)})
    require(records[0]["origin_exact"] == "-1", "n=1 normalization failed")
    require(float(sum((Fraction(1, k) for k in range(1, 41)), Fraction(0))) > log(41),
            "harmonic growth witness failed")
    return records


def polynomial_input(n, z):
    # Direct finite geometric polynomial, without the q_n quotient.
    t = z.real * z.real + z.imag * z.imag
    return z * z * sum((1 - t) ** j for j in range(n))


def singular_input(z):
    return z / z.conjugate() if z != 0 else 0j


def numerical_pv(value_function, r, angle_count=1024, radial_count=256):
    """Direct disk integral in coordinates centered at z=r.

    The local constant is subtracted before integrating and its radial log term
    is included exactly. Circular cutoff log(epsilon) terms integrate to zero.
    This computation does not differentiate the Cauchy-potential formula.
    """
    center_value = value_function(complex(r, 0))
    total = 0j
    for a in range(angle_count):
        theta = 2 * pi * (a + 0.314159) / angle_count
        direction = complex(cos(theta), sin(theta))
        radius = -r * cos(theta) + sqrt(1 - r * r * sin(theta) ** 2)
        inner = 0j
        for j in range(radial_count):
            rho = radius * (j + 0.5) / radial_count
            zeta = r + rho * direction
            inner += (value_function(zeta) - center_value) / rho
        inner *= radius / radial_count
        total += direction.conjugate() ** 2 * (inner + center_value * log(radius))
    return -2 * total / angle_count


def expected_polynomial(n, r):
    t = r * r
    # Stable geometric integral, with integer j integrated explicitly.
    integral = sum((1 - t) ** (j + 1) / (j + 1) for j in range(n))
    return 1 - (1 - t) ** n - integral


def numerical_checks():
    records = []
    for n, r in ((1, 0.2), (2, 0.5), (5, 0.35), (10, 0.7)):
        actual = numerical_pv(lambda z, n=n: polynomial_input(n, z), r)
        expected = expected_polynomial(n, r)
        error = abs(actual - expected)
        require(error < 0.0003, f"direct polynomial PV failed n={n}, r={r}: {actual} != {expected}")
        records.append({"input": f"polynomial n={n}", "r": r,
                        "direct_pv": [actual.real, actual.imag], "formula": expected,
                        "absolute_error": error, "tolerance": 0.0003})
    for r in (0.125, 0.4, 0.75):
        actual = numerical_pv(singular_input, r)
        expected = 1 + 2 * log(r)
        error = abs(actual - expected)
        require(error < 0.01, f"direct singular-input PV failed r={r}: {actual} != {expected}")
        records.append({"input": "z/bar z", "r": r,
                        "direct_pv": [actual.real, actual.imag], "formula": expected,
                        "absolute_error": error, "tolerance": 0.01})
    return records


if __name__ == "__main__":
    exact = exact_checks()
    numerical = numerical_checks()
    print(json.dumps({"status": "PASS", "exact_cases": len(exact),
                      "exact_first": exact[0], "exact_last": exact[-1],
                      "direct_integral_checks": numerical}, indent=2))
