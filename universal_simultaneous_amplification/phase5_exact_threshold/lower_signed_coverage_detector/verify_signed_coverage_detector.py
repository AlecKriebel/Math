#!/usr/bin/env python3
"""Exact checks for SIGNED_COVERAGE_DETECTOR.md."""

from fractions import Fraction

import sympy as sp


def check_symbolic_identities() -> None:
    m, s, a = sp.symbols("m s a", positive=True)
    r = 1 + a

    anchored_uniform = r * m / (m + a) - 1
    assert sp.factor(anchored_uniform - a * (m - 1) / (m + a)) == 0

    selective_uniform = a * m / (m + a) - a / r
    expected_selective = a**2 * (m - 1) / (r * (m + a))
    assert sp.factor(selective_uniform - expected_selective) == 0

    lam = (s - 1) / (m - 1)
    phi_s = r * (s / m) / (1 + a * s / m)
    phi_one = r * (1 / m) / (1 + a / m)
    theta = (m / s) * (phi_s - lam - (1 - lam) * phi_one)
    theta_factored = a * m * (s - 1) * (m - s) / (
        s * (m + a) * (m + a * s)
    )
    assert sp.factor(theta - theta_factored) == 0

    # Complete-Bd-harmonic chord limit, equation (46).
    geom_inverse_moment = 1 / (1 + r * a)
    chord_limit = 1 / r - geom_inverse_moment
    assert sp.factor(chord_limit - a**2 / (r * (1 + r * a))) == 0

    # The finite complete-dB increment ratio is not the Bd ratio 1/r.
    k = sp.symbols("k", positive=True)
    db_ratio = (m - 1 + a * k) / (r * (m - 1 + a * (k - 1)))
    assert sp.factor(db_ratio - 1 / r - a / (r * (m - 1 + a * (k - 1)))) == 0


def coverage(z: frozenset[int], b: frozenset[int]) -> int:
    return int(bool(z & b))


def check_signed_representation() -> None:
    for m in range(2, 9):
        universe = frozenset(range(m))
        for mask in range(1 << m):
            b = frozenset(i for i in range(m) if mask & (1 << i))
            g = len(b) - int(bool(b))
            signed = sum(coverage(frozenset({i}), b) for i in universe)
            signed -= coverage(universe, b)
            assert g == signed


def choose(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    return sp.binomial(n, k)


def check_surrogate_positivity() -> None:
    for m in range(3, 13):
        for s in range(2, m):
            lam = Fraction(s - 1, m - 1)
            for k in range(m + 1):
                if k == 0:
                    h_s = Fraction(0)
                    h_cluster = Fraction(0)
                else:
                    h_s = Fraction(
                        choose(m, s) - choose(m - k, s), choose(m, s)
                    )
                    h_cluster = lam + (1 - lam) * Fraction(k, m)
                f = Fraction(m, s) * (h_s - h_cluster)
                assert f >= 0
                if k in (0, 1, m):
                    assert f == 0
                elif 2 <= k <= m - 1:
                    assert f > 0


if __name__ == "__main__":
    check_symbolic_identities()
    check_signed_representation()
    check_surrogate_positivity()
    print("all signed coverage detector checks passed")
