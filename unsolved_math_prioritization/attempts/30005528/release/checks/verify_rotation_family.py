#!/usr/bin/env python3
"""Finite exact checks for the rotation-family counterexample.

No floating point, external packages, source downloads, or exhaustive-search
claim. The all-period theorem is proved in PROOF.md, not by this script.
"""

from dataclasses import dataclass
from fractions import Fraction as Q
from math import gcd, isqrt
import json
from pathlib import Path


@dataclass(frozen=True)
class Qsqrt2:
    """The exact number a + b*sqrt(2), with rational coefficients."""

    a: Q = Q(0)
    b: Q = Q(0)

    def __add__(self, other):
        return Qsqrt2(self.a + other.a, self.b + other.b)

    def __neg__(self):
        return Qsqrt2(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        return Qsqrt2(self.a * other.a + 2 * self.b * other.b,
                      self.a * other.b + self.b * other.a)

    def scale(self, scalar):
        return Qsqrt2(self.a * scalar, self.b * scalar)

    def sign(self):
        a, b = self.a, self.b
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if (a > 0) == (b > 0):
            return 1 if a > 0 else -1
        # Opposite signs: compare |a| and |b|*sqrt(2) by squaring.
        delta = a * a - 2 * b * b
        if delta == 0:
            return 0
        return ((a > 0) - (a < 0)) * ((delta > 0) - (delta < 0))

    def record(self):
        return {"rational_coefficient": str(self.a),
                "sqrt2_coefficient": str(self.b)}


ZERO = Qsqrt2()
ONE = Qsqrt2(Q(1))
ALPHA = Qsqrt2(Q(0), Q(1))


def run_checks():
    assert ALPHA * ALPHA == Qsqrt2(Q(2))
    assert (ALPHA - ONE).sign() > 0
    assert (Qsqrt2(Q(2)) - ALPHA).sign() > 0
    assert Qsqrt2(Q(3), Q(-2)).sign() > 0
    assert Qsqrt2(Q(-3), Q(2)).sign() < 0
    reciprocal = Qsqrt2(Q(-1, 7), Q(2, 7))
    assert reciprocal * (ALPHA.scale(2) + ONE) == ONE

    approximation_samples = []
    prefix_checks = 0
    smaller_period_checks = 0
    for n in range(1, 257):
        m = isqrt(2 * n * n) + 1
        assert (m - 1) ** 2 < 2 * n * n < m ** 2
        angle = Q(m, n)
        t = Qsqrt2(angle, Q(-1))
        assert t.sign() > 0
        assert (Qsqrt2(Q(1, n)) - t).sign() > 0
        assert (ONE - t).sign() > 0
        assert ALPHA + t == Qsqrt2(angle)

        q = n // gcd(m, n)
        assert (q * angle).denominator == 1
        for candidate in range(1, q):
            assert (candidate * angle).denominator != 1
            smaller_period_checks += 1

        cost = ONE + t
        for N in (1, 2, 7, 32, 101):
            numerator = ZERO
            for _ in range(N + 1):
                numerator = numerator + cost
            mean = numerator.scale(Q(1, N))
            assert mean - cost == cost.scale(Q(1, N))
            assert (mean - cost).sign() > 0
            prefix_checks += 1

        if n in (1, 2, 3, 16, 64, 256):
            approximation_samples.append({"n": n, "m": m,
                "least_period": q, "height": t.record()})

    angle_count = 0
    for q in range(1, 129):
        for p in range(q, 3 * q + 1):
            if gcd(p, q) != 1:
                continue
            t = Qsqrt2(Q(p, q), Q(-1))
            if t.sign() < 0 or (ONE - t).sign() < 0:
                continue
            assert t.sign() > 0
            assert p * p - 2 * q * q >= 1
            assert (ALPHA + t).scale(q) == Qsqrt2(Q(p))
            lower_gap = reciprocal.scale(Q(1, q * q))
            assert (t - lower_gap).sign() >= 0
            # Rationalization identity used in inequality (5).
            assert t * (ALPHA.scale(2) + t) == Qsqrt2(Q(p*p - 2*q*q, q*q))
            angle_count += 1

    return {
        "status": "passed",
        "arithmetic": "exact fractions in Q(sqrt(2)); no floating point",
        "explicit_periodic_competitors": 256,
        "least_period_smaller_candidate_checks": smaller_period_checks,
        "source_normalization_prefix_checks": prefix_checks,
        "reduced_rational_angle_instances_denominator_at_most_128": angle_count,
        "bounded_period_gap_checks": angle_count,
        "sample_competitors": approximation_samples,
        "limitations": "Finite instances only. Infinite-period exclusion, compactness, density, and limiting assertions require the exact proof in PROOF.md."
    }


if __name__ == "__main__":
    result = run_checks()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(__file__).with_name("verification_results.json").write_text(encoded)
    print(encoded, end="")
