#!/usr/bin/env python3
"""Exact replay for the Lorentz cone and unmarked affinity obstruction."""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
TRACE_DIR = HERE.parent / "rhyb_minimal_product_trace"
sys.path.insert(0, str(TRACE_DIR))

from verify_singleton_root_schur import row, singleton_trace  # noqa: E402


Q = sp.Rational


def verify_lorentz_algebra():
    A, B, D, q, x = sp.symbols("A B D q x", positive=True)
    t = A + B
    u = sp.sqrt(t**2 + D**2)
    lhs = sp.cosh(A) * sp.cosh(B) * sp.cosh(D) + sp.sinh(A) * sp.sinh(B)

    # First reduction in the proof of (14).
    assert sp.simplify(
        lhs
        - sp.cosh(t)
        - sp.cosh(A) * sp.cosh(B) * (sp.cosh(D) - 1)
    ) == 0
    assert sp.simplify(
        2 * sp.cosh(A) * sp.cosh(B)
        - sp.cosh(t)
        - sp.cosh(A - B)
    ) == 0

    # Concavity of Phi(x)=log(sinh(sqrt(x))/sqrt(x)).
    Phi = sp.log(sp.sinh(sp.sqrt(x)) / sp.sqrt(x))
    expected_second = -(
        q / sp.tanh(q) + q**2 / sp.sinh(q) ** 2 - 2
    ) / (4 * q**4)
    assert sp.simplify(sp.diff(Phi, x, 2).subs(x, q**2) - expected_second) == 0

    M = q * sp.sinh(q) * sp.cosh(q) + q**2 - 2 * sp.sinh(q) ** 2
    assert all(sp.simplify(sp.diff(M, q, order).subs(q, 0)) == 0 for order in range(4))
    assert sp.simplify(sp.diff(M, q, 4) - 16 * q * sp.sinh(q) * sp.cosh(q)) == 0

    # The final derivative comparison (23).
    lower = sp.cosh(t) + sp.sinh(t) / t * (sp.cosh(D) - 1)
    expected_derivative = sp.sinh(t) / t * sp.sinh(D) - D / u * sp.sinh(u)
    assert sp.simplify(sp.diff(lower - sp.cosh(u), D) - expected_derivative) == 0
    assert sp.simplify((lower - sp.cosh(u)).subs(D, 0)) == 0

    # Exact rapidity rewriting of the pair criterion.
    alpha, beta, delta, epsilon, target = sp.symbols(
        "alpha beta delta epsilon target", positive=True
    )
    hi = target * sp.cosh(alpha) ** 2
    hj = target * sp.cosh(beta) ** 2
    pair_margin = (
        sp.sqrt(hi * hj) * sp.cosh(delta)
        + sp.sqrt((hi - target) * (hj - target))
        - target * sp.cosh(epsilon)
    )
    # Parameter positivity fixes the square-root branches.
    rewritten = target * (
        sp.cosh(alpha) * sp.cosh(beta) * sp.cosh(delta)
        + sp.sinh(alpha) * sp.sinh(beta)
        - sp.cosh(epsilon)
    )
    branch_substitution = {
        sp.sqrt(sp.sinh(alpha) ** 2): sp.sinh(alpha),
        sp.sqrt(sp.sinh(beta) ** 2): sp.sinh(beta),
        sp.sqrt(sp.cosh(alpha) ** 2 * sp.cosh(beta) ** 2): sp.cosh(alpha) * sp.cosh(beta),
    }
    assert sp.simplify(sp.expand_power_base(pair_margin / target, force=True).xreplace(branch_substitution) - rewritten / target) == 0


def verify_kac_pair_algebra():
    r, bar_b, bar_d, lb_i, lb_j, ld_i, ld_j, ei, ej = sp.symbols(
        "r bar_b bar_d lb_i lb_j ld_i ld_j ei ej", positive=True
    )
    rb_i, rb_j = bar_b / lb_i, bar_b / lb_j
    rd_i, rd_j = bar_d / ld_i, bar_d / ld_j
    target = r**3 * bar_b * bar_d
    hi = lb_i * ld_i

    assert sp.factor(hi / target - 1 / (r**3 * rb_i * rd_i)) == 0
    root_orientation = sp.factor(
        (lb_i * ej * ld_j) / (lb_j * ei * ld_i)
    )
    cycle_orientation = sp.factor(
        (ej / ei) * (rb_j * rd_i) / (rb_i * rd_j)
    )
    assert sp.factor(root_orientation - cycle_orientation) == 0


def verify_generic_affinity_identities():
    xb1, xb2, xd1, xd2 = sp.symbols("xb1 xb2 xd1 xd2", nonnegative=True)
    f0, f1, f2 = sp.symbols("f0 f1 f2")
    b = [xb1**2, xb2**2]
    d = [xd1**2, xd2**2]
    h = [xb1 * xd1, xb2 * xd2]
    diagonal = -sum(b + d) / 2

    row_sum = diagonal + sum(h)
    claimed_killing = -sum((xb - xd) ** 2 for xb, xd in zip([xb1, xb2], [xd1, xd2])) / 2
    assert sp.expand(row_sum - claimed_killing) == 0

    Hf = diagonal * f0 + h[0] * f1 + h[1] * f2
    average_drift = (
        (-(b[0] + b[1]) * f0 + b[0] * f1 + b[1] * f2)
        + (-(d[0] + d[1]) * f0 + d[0] * f1 + d[1] * f2)
    ) / 2
    square_loss = sum(
        (xb - xd) ** 2 * fj / 2
        for xb, xd, fj in zip([xb1, xb2], [xd1, xd2], [f1, f2])
    )
    assert sp.expand(Hf - average_drift + square_loss) == 0

    difference_form = sum(hj * (fj - f0) for hj, fj in zip(h, [f1, f2])) + f0 * row_sum
    assert sp.expand(Hf - difference_form) == 0


def verify_marked_two_by_two_cocycles():
    ell1, ell2, wc1, wc2, t = sp.symbols(
        "ell1 ell2 wc1 wc2 t", positive=True
    )
    y1, y2 = sp.symbols("y1 y2", real=True)
    diagonal = lambda ell: sp.diag(sp.sqrt(ell), 1 / sp.sqrt(ell))
    assert diagonal(ell1) * diagonal(ell2) == diagonal(ell1 * ell2)

    wc = wc1 * wc2
    wl = wc * ell1 * ell2
    assert sp.simplify(
        sp.sqrt(wl * wc) * diagonal(wl / wc) - sp.diag(wl, wc)
    ) == sp.zeros(2)

    triangular = lambda weight, reward: weight * sp.Matrix(
        [[1, reward], [0, 1]]
    )
    assert sp.expand(
        triangular(wc1, y1) * triangular(wc2, y2)
        - triangular(wc1 * wc2, y1 + y2)
    ) == sp.zeros(2)
    assert sp.diff(sp.exp(t * (y1 + y2)), t).subs(t, 0) == y1 + y2


def verify_set_support():
    """Truth-table replay of the loopless update support, not a graph scan."""

    for order in range(2, 8):
        universe = set(range(order))
        for mask in range(1, 1 << order):
            state = {vertex for vertex in universe if mask & (1 << vertex)}
            all_bd = set()
            all_db = set()
            for target in state:
                sources = universe - {target}
                neutral = {
                    frozenset((state - {target}) | {source})
                    for source in sources
                }
                selective = {
                    frozenset(state | {source})
                    for source in sources
                }
                db = {
                    frozenset((state - {target}) | sample_set)
                    for sample_mask in range(1, 1 << order)
                    for sample_set in [
                        {
                            vertex
                            for vertex in sources
                            if sample_mask & (1 << vertex)
                        }
                    ]
                    if sample_set
                }
                all_bd |= neutral | selective
                all_db |= db
                common = (neutral | selective) & db
                assert all(len(endpoint) <= len(state) for endpoint in common)
                if len(state) == 1:
                    assert all(len(endpoint) == 1 for endpoint in common)
                growing_selective = {
                    endpoint for endpoint in selective if len(endpoint) > len(state)
                }
                assert growing_selective.isdisjoint(db)

            # Generator entries sum over every occupied update target.  This
            # global intersection therefore also audits coincidences produced
            # by different Bd and dB targets.
            common_generator_endpoints = all_bd & all_db
            assert all(
                len(endpoint) <= len(state)
                for endpoint in common_generator_endpoints
            )
            if len(state) == 1:
                assert all(
                    len(endpoint) == 1
                    for endpoint in common_generator_endpoints
                )


def verify_active_p3_kac_data():
    weights = (
        (0, 1, 0),
        (1, 0, 1),
        (0, 1, 0),
    )
    fitness = Q(3, 2)
    bd = singleton_trace(weights, fitness, "Bd")
    db = singleton_trace(weights, fitness, "dB")

    assert bd["lambda"] == row([16, 7, 16]) / 39
    assert db["lambda"] == row([3, 7, 3]) / 13
    assert bd["bar_phi"] == Q(200, 819)
    assert db["bar_phi"] == Q(2, 39)

    kac_b = [sp.factor(bd["bar_phi"] / bd["lambda"][0, i]) for i in range(3)]
    kac_d = [sp.factor(db["bar_phi"] / db["lambda"][0, i]) for i in range(3)]
    assert kac_b == [Q(25, 42), Q(200, 147), Q(25, 42)]
    assert kac_d == [Q(2, 9), Q(2, 21), Q(2, 9)]
    assert all(value > 0 for value in kac_b + kac_d)


def main():
    verify_lorentz_algebra()
    verify_kac_pair_algebra()
    verify_generic_affinity_identities()
    verify_marked_two_by_two_cocycles()
    verify_set_support()
    verify_active_p3_kac_data()
    print("PASS: Lorentz rapidity comparison algebra")
    print("PASS: Kac return-cycle pair normalization")
    print("PASS: geometric-mean killing and drift squares")
    print("PASS: canonical marked two-by-two cocycle identities")
    print("PASS: unmarked common support is rank-nonincreasing")
    print("PASS: singleton-to-higher-rank affinity block is zero")
    print("PASS: active unweighted-P3 Kac rewards are strictly positive")
    print("OPEN: physical two-root Lorentz cone and universal MP")


if __name__ == "__main__":
    main()
