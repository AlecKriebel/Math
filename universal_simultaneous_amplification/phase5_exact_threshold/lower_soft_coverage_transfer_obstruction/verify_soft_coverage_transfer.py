#!/usr/bin/env python3
"""Exact replay for the soft coverage transfer obstruction."""

from __future__ import annotations

from itertools import product

import sympy as sp


def assert_zero(expr: sp.Expr) -> None:
    assert sp.factor(sp.together(expr)) == 0, sp.factor(sp.together(expr))


def symbolic_transfer() -> None:
    r, x, c = sp.symbols("r x c", positive=True)
    a = r - 1
    f = x**2 / (r - a * x)

    assert_zero(sp.diff(f, x, 2) - 2 * r**2 / (r - a * x) ** 3)
    assert_zero(x - f - r * x * (1 - x) / (r - a * x))

    # Jensen lower envelope and the total-variation envelope.
    jensen = c**2 / (r - a * c)
    tv_envelope = sp.factor(c - jensen)
    assert_zero(tv_envelope - r * c * (1 - c) / (r - a * c))

    s = sp.symbols("s", positive=True)
    c_star = s / (s + 1)
    at_star = tv_envelope.subs({c: c_star, r: s**2})
    assert_zero(at_star - s**2 / (s + 1) ** 2)

    # The tangent proof of c/(r-ac) >= c^r uses convexity of c^(-a).
    tangent_function = c ** (-a)
    assert_zero(
        sp.diff(tangent_function, c, 2)
        - a * (a + 1) * c ** (-a - 2)
    )
    assert_zero((r - a * c) - (1 + a * (1 - c)))

    d = sp.symbols("d", positive=True)
    matrix = sp.Matrix([[c, a * d], [1 - c, a * (1 - d)]]) / r
    assert_zero(sum(matrix[:, 0]) - 1 / r)
    assert_zero(sum(matrix[:, 1]) - a / r)
    assert_zero(matrix.det() - a * (c - d) / r**2)
    assert_zero(c * (a * d / c) + (1 - c) * (a * (1 - d) / (1 - c)) - a)


def occupancy_probability(m: int, ell: int, j: int) -> sp.Rational:
    return (
        sp.factorial(m)
        / sp.factorial(m - j)
        * sp.functions.combinatorial.numbers.stirling(ell, j, kind=2)
        / m**ell
    )


def exact_occupancy_transfer() -> None:
    r = sp.Rational(3, 2)
    a = r - 1

    for m in range(2, 7):
        for ell in range(1, 6):
            c_formula = sp.Rational(m - 1, m) ** ell
            c_sum = sp.S.Zero
            d_sum = sp.S.Zero
            for j in range(1, min(m, ell) + 1):
                probability = occupancy_probability(m, ell, j)
                x = sp.Rational(m - j, m)
                c_sum += probability * x
                d_sum += probability * x**2 / (r - a * x)

            assert_zero(c_sum - c_formula)

            # Direct enumeration of all labelled tester sequences.
            c_direct = sp.S.Zero
            d_direct = sp.S.Zero
            for tester in product(range(m), repeat=ell):
                x = sp.Rational(m - len(set(tester)), m)
                weight = sp.Rational(1, m**ell)
                c_direct += weight * x
                d_direct += weight * x**2 / (r - a * x)

            assert_zero(c_sum - c_direct)
            assert_zero(d_sum - d_direct)

            # Exact Jensen and collision floors.
            assert sp.factor(d_sum - c_sum**2 / (r - a * c_sum)) >= 0
            assert sp.factor(d_sum - c_sum / (r * m - a)) >= 0


def source_collision_law() -> None:
    r, m = sp.symbols("r m", positive=True)
    a = r - 1
    # Conditional A singleton probability is a geometric series whose first
    # term is 1/(rm) and ratio is a/(rm).
    collision = sp.simplify((1 / (r * m)) / (1 - a / (r * m)))
    assert_zero(collision - 1 / (r * m - a))

    # For fixed m, the singleton terms form a geometric series.  Only these
    # survive relative to a singleton clean batch at infinite tester depth.
    first = 1 / (r * m)
    ratio = a / (r * m)
    assert_zero(first / (1 - ratio) - 1 / (r * m - a))


def finite_lambda_limit() -> None:
    r, lam, y = sp.symbols("r lam y", positive=True)
    a = r - 1
    x = sp.exp(-lam)
    d = x**2 / (r - a * x)
    projective = sp.factor(a * d / x)
    assert_zero(projective - a * x / (r - a * x))

    # Weak-test logarithmic slope: relative projective retention loses r
    # times the logarithmic clean throughput to first order.
    relative = x / (r - a * x)
    assert_zero(sp.limit(sp.diff(sp.log(relative), lam), lam, 0) + r)
    assert_zero(sp.limit(sp.diff(sp.log(x), lam), lam, 0) + 1)

    # The tempting baseline-free hit posterior can be below one, but Section
    # 6 checks that this scalar is not the physical reset eigenvalue.
    hit_conditional = sp.factor((1 - d) / (1 - x))
    assert_zero(hit_conditional - (r + x) / (r - a * x))
    q_hit = sp.factor(a * hit_conditional)
    x_threshold = r * (2 - r) / (2 * a)
    assert_zero(sp.factor((q_hit - 1) * (r - a * x)) - 2 * a * (x - x_threshold))

    d_y = y**2 / (r - a * y)
    hit_y = sp.factor((1 - d_y) / (1 - y))
    assert_zero(sp.limit((hit_y - 1) / y, y, 0) - 1)


def mark_erasure() -> None:
    r, c, d, u, v = sp.symbols("r c d u v", positive=True)
    a = r - 1
    portal_split = sp.Matrix([1, a])
    retained = sp.Matrix([[u, v]])
    reset = portal_split * retained / r
    scalar = (u + a * v) / r

    assert reset.det() == 0
    assert reset.rank() == 1
    assert (reset**2 - scalar * reset).applyfunc(
        lambda entry: sp.factor(sp.together(entry))
    ) == sp.zeros(2)
    for depth in range(1, 8):
        assert (reset**depth - scalar ** (depth - 1) * reset).applyfunc(
            lambda entry: sp.factor(sp.together(entry))
        ) == sp.zeros(2)
    assert_zero(reset[1, 0] / reset[0, 0] - a)
    assert_zero(reset[1, 1] / reset[0, 1] - a)

    # The persistent-label diagonal operator is different and is the only
    # one whose pure-channel ratio powers the posterior av/u.
    persistent = sp.diag(u, a * v) / r
    for depth in range(1, 6):
        ratio = persistent[1, 1] ** depth / persistent[0, 0] ** depth
        assert_zero(ratio - (a * v / u) ** depth)

    # Exact mixed-history expansion for the hit reset.
    alpha = (1 - c) / r
    beta = a * (1 - d) / r
    for depth in range(1, 8):
        expanded = sum(
            sp.binomial(depth, j) * alpha ** (depth - j) * beta**j
            for j in range(depth + 1)
        )
        assert_zero(expanded - (alpha + beta) ** depth)

    # Deterministic-hole identities.
    x = sp.symbols("x", positive=True)
    d_x = x**2 / (r - a * x)
    alpha_x = (1 - x) / r
    beta_x = a * (1 - d_x) / r
    success = sp.factor(alpha_x + beta_x)
    posterior = sp.factor(beta_x / alpha_x)
    assert_zero(success - r * (1 - x) / (r - a * x))
    assert_zero(posterior - a * (r + x) / (r - a * x))
    assert_zero(success / (1 - x) - (1 + posterior) / r)
    assert_zero(success / (1 - x) - 1 - a * x / (r - a * x))

    # The physically composable full-geometric/clean ratio differs from the
    # posterior.  Hit is never favorable; no-hit pays the Jensen throughput
    # envelope 1/(r-ac), followed by the tangent bound c^(r-1).
    nohit_physical = (c + a * d) / (r * c)
    d_jensen = c**2 / (r - a * c)
    assert_zero(nohit_physical.subs(d, d_jensen) - 1 / (r - a * c))
    hit_physical = ((1 - c) + a * (1 - d)) / (r * (1 - c))
    assert_zero(hit_physical - 1 - a * (c - d) / (r * (1 - c)))

    m = sp.symbols("m", positive=True)
    collision_floor = 1 / (r * m - a)
    assert_zero(
        nohit_physical.subs(d, c * collision_floor) - m / (r * m - a)
    )

    # Every binary classifier contracts the persistent mark by c-d exactly.
    classifier = sp.Matrix([[c, d], [1 - c, 1 - d]])
    mark = sp.Matrix([1, -1])
    assert (classifier * mark - (c - d) * mark).applyfunc(sp.factor) == sp.zeros(2, 1)

    c1, d1, c2, d2 = sp.symbols("c1 d1 c2 d2")
    k1 = sp.Matrix([[c1, d1], [1 - c1, 1 - d1]])
    k2 = sp.Matrix([[c2, d2], [1 - c2, 1 - d2]])
    assert (
        k2 * k1 * mark - (c1 - d1) * (c2 - d2) * mark
    ).applyfunc(sp.factor) == sp.zeros(2, 1)


def main() -> None:
    symbolic_transfer()
    exact_occupancy_transfer()
    source_collision_law()
    finite_lambda_limit()
    mark_erasure()
    print("PASS exact soft clean/adverse transfer")
    print("PASS convex data-processing and total-variation envelopes")
    print("PASS exact source-collision floor")
    print("PASS finite-intensity and weak-test limits")
    print("PASS rank-one reset, mixed histories, and all-depth mark erasure")


if __name__ == "__main__":
    main()
