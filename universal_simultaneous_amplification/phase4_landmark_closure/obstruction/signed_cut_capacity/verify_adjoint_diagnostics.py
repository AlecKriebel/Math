#!/usr/bin/env python3
"""Exact certificates for adjoint-density diagnostics at `r=3/2`.

The script verifies five small counterexamples to overly strong pointwise,
levelwise, or rankwise inequalities.  It also checks the exact
weighted-adjoint density equations, the rank-boundary integration identity,
and the two-level flux identity on the same graphs.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp


SOURCE = Path(__file__).parents[1] / "verify_exact_duals.py"
SPEC = importlib.util.spec_from_file_location("exact_duals", SOURCE)
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

R = sp.Rational(3, 2)
A_PARAMETER = R - 1


def data(weights: list[list[int]]):
    n = len(weights)
    full = (1 << n) - 1
    degrees = [sum(row) for row in weights]
    p = [
        [sp.Rational(weights[i][j], degrees[i]) for j in range(n)]
        for i in range(n)
    ]
    l_gen = MOD.dual_generator(weights, R, "Bd")
    c_gen = MOD.reversed_arrow_generator(weights, R)
    pi_l = MOD.stationary(l_gen)
    pi_c = MOD.stationary(c_gen)
    z = (1 + A_PARAMETER) ** n - 1
    f = [
        sp.cancel(pi_l[state - 1] * z / A_PARAMETER ** state.bit_count())
        for state in range(1, full + 1)
    ]
    g = [
        sp.cancel(pi_c[state - 1] * z / A_PARAMETER ** state.bit_count())
        for state in range(1, full + 1)
    ]
    return p, l_gen, c_gen, pi_l, pi_c, f, g


def cuts(p, state: int):
    n = len(p)
    row_cut = sum(
        p[i][j]
        for i in range(n)
        for j in range(n)
        if (state >> i) & 1 and not ((state >> j) & 1)
    )
    reverse_cut = sum(
        p[i][j]
        for i in range(n)
        for j in range(n)
        if not ((state >> i) & 1) and (state >> j) & 1
    )
    return sp.cancel(row_cut), sp.cancel(reverse_cut)


def verify_entropy(weights: list[list[int]]) -> None:
    p, l_gen, c_gen, pi_l, pi_c, f, g = data(weights)
    full = (1 << len(weights)) - 1
    v = []
    for state in range(1, full + 1):
        row_cut, reverse_cut = cuts(p, state)
        v.append(R * (row_cut - reverse_cut))

    # The adjoint defect is the additive zero-sum vertex potential
    # V(A)=r sum_{i in A}(1-t_i), t_i=sum_j P_ji.
    q = [
        sp.cancel(1 - sum(p[j][i] for j in range(len(p))))
        for i in range(len(p))
    ]
    assert sp.cancel(sum(q)) == 0
    for state in range(1, full + 1):
        additive_v = R * sum(
            q[i] for i in range(len(p)) if (state >> i) & 1
        )
        assert sp.cancel(v[state - 1] - additive_v) == 0
    for k in range(1, len(p) + 1):
        assert sp.cancel(sum(
            v[state - 1]
            for state in range(1, full + 1)
            if state.bit_count() == k
        )) == 0

    # Pointwise density equations implied by the weighted adjoint.
    f_vector = sp.Matrix(f)
    g_vector = sp.Matrix(g)
    assert c_gen * f_vector == -sp.diag(*v) * f_vector
    assert l_gen * g_vector == sp.diag(*v) * g_vector

    # The companion note derives the entropy inequalities term by term from
    # these equations and x-1-log(x)>=0.  Avoid asking a CAS to simplify huge
    # exact logarithmic expressions: the finite symbolic component is the
    # rational density equation checked above.
    assert sp.cancel(sum(pi_c[i] * v[i] for i in range(full))) <= 0
    assert sp.cancel(sum(pi_l[i] * v[i] for i in range(full))) >= 0

    # Exact rank-boundary integration by parts behind (6b), checked with
    # rational test functions.  Its specialization to log(g) and log(f)
    # is then formal termwise algebra.
    for generator, pi, psi in (
        (l_gen, pi_l, g),
        (c_gen, pi_c, f),
    ):
        q_psi = generator * sp.Matrix(psi)
        for k in range(1, len(p) + 1):
            inside = [
                state
                for state in range(1, full + 1)
                if state.bit_count() == k
            ]
            outside = [
                state
                for state in range(1, full + 1)
                if state.bit_count() != k
            ]
            lhs = sum(
                pi[state - 1] * q_psi[state - 1]
                for state in inside
            )
            rhs = sum(
                pi[state - 1] * generator[state - 1, other - 1]
                * psi[other - 1]
                - pi[other - 1] * generator[other - 1, state - 1]
                * psi[state - 1]
                for state in inside
                for other in outside
            )
            assert sp.cancel(lhs - rhs) == 0


def verify_flux(weights: list[list[int]]) -> None:
    p, _, _, _, _, f, g = data(weights)
    n = len(weights)
    full = (1 << n) - 1
    for k in range(1, n):
        left = 0
        symmetric_flux = 0
        for state in range(1, full + 1):
            if state.bit_count() == k:
                row_cut, reverse_cut = cuts(p, state)
                left += (row_cut - reverse_cut) * (
                    f[state - 1] - g[state - 1]
                )
                symmetric_flux += (row_cut + reverse_cut) / 2 * (
                    f[state - 1] + g[state - 1]
                )
            elif state.bit_count() == k + 1:
                row_cut, _ = cuts(p, state)
                internal = k + 1 - row_cut
                symmetric_flux -= internal * (
                    f[state - 1] + g[state - 1]
                )
        assert sp.cancel(left - 2 * symmetric_flux) == 0


def main() -> None:
    triangle = [[0, 1, 4], [1, 0, 2], [4, 2, 0]]
    _, _, _, _, _, f, g = data(triangle)
    level_one_f = sum(f[state - 1] for state in (1, 2, 4)) / 3
    level_one_g = sum(g[state - 1] for state in (1, 2, 4)) / 3
    level_product_gap = sp.factor(level_one_f * level_one_g - 1)
    assert level_product_gap == sp.Rational(
        1163361305883, 19038384631138
    )

    star = [
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
    ]
    p, _, _, _, _, f, g = data(star)
    state = 7
    row_cut, reverse_cut = cuts(p, state)
    pointwise_tilt = sp.factor(
        (f[state - 1] - g[state - 1])
        * R
        * (row_cut - reverse_cut)
    )
    assert pointwise_tilt == -sp.Rational(15080, 76923)

    order_five = [
        [0, 1, 60000, 500000, 1500000],
        [1, 0, 1000000, 70000, 250],
        [60000, 1000000, 0, 1, 2],
        [500000, 70000, 1, 0, 6000],
        [1500000, 250, 2, 6000, 0],
    ]
    _, _, _, _, _, f, g = data(order_five)
    pointwise_product_gap = sp.factor(f[7] * g[7] - 1)
    assert pointwise_product_gap > 0
    assert sp.Rational(49, 10000) < pointwise_product_gap < sp.Rational(1, 200)

    star_five = [[0] * 5 for _ in range(5)]
    for leaf in range(1, 5):
        star_five[0][leaf] = star_five[leaf][0] = 1
    _, _, _, pi_l, pi_c, f, g = data(star_five)
    rank = []
    for k in range(1, 6):
        states = [state for state in range(1, 32) if state.bit_count() == k]
        rank.append(
            sp.cancel(sum(f[state - 1] + g[state - 1] for state in states)
                      / len(states))
        )
    assert sp.factor(rank[3] - rank[2]) == sp.Rational(
        126581643, 905995090
    )
    mean_l = sum(pi_l[state - 1] * state.bit_count() for state in range(1, 32))
    mean_c = sum(pi_c[state - 1] * state.bit_count() for state in range(1, 32))
    mean_k = sp.Rational(5) * A_PARAMETER * (1 + A_PARAMETER) ** 4 / (
        (1 + A_PARAMETER) ** 5 - 1
    )
    assert sp.factor(2 * mean_k - mean_l - mean_c) == sp.Rational(
        14979081573, 95582481995
    )

    pair_graph = [
        [0, 1, 1, 2],
        [1, 0, 3, 1],
        [1, 3, 0, 2],
        [2, 1, 2, 0],
    ]
    p, _, _, pi_l, _, _, _ = data(pair_graph)
    q = [sp.cancel(1 - sum(p[j][i] for j in range(4))) for i in range(4)]
    singleton_mass = sum(pi_l[(1 << i) - 1] for i in range(4))
    inclusion = [
        sp.cancel(pi_l[(1 << i) - 1] / singleton_mass)
        for i in range(4)
    ]
    pairwise_alignment = sp.factor(
        (q[1] - q[3]) * (inclusion[1] - inclusion[3])
    )
    assert pairwise_alignment == -sp.Rational(
        46269978481148084, 249339373524498200277
    )
    assert sp.factor(sum(q[i] * inclusion[i] for i in range(4))) > 0

    for graph in (triangle, star):
        verify_entropy(graph)
        verify_flux(graph)
    verify_flux(order_five)

    print("PASS: exact n=3 level-mean product counterexample")
    print("PASS: exact n=4 pointwise tilt-sign counterexample")
    print("PASS: exact n=5 pointwise density-product counterexample")
    print("PASS: exact K_1,4 rank-MLR counterexample with positive mean gap")
    print("PASS: exact n=4 pairwise vertex-marginal counterexample")
    print("PASS: weighted-adjoint entropy identities")
    print("PASS: additive zero-sum vertex potential")
    print("PASS: exact rank-boundary integration identity")
    print("PASS: two-level signed-flux identity")


if __name__ == "__main__":
    main()
