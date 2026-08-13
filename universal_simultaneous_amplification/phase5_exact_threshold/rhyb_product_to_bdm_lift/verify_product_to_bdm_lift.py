#!/usr/bin/env python3
"""Exact algebraic replay of the minimal-product-to-BDM lift.

This script checks only identities used in the proof.  It performs no graph
enumeration or optimization and does not assert the still-open minimal
stationary product inequality.
"""

from __future__ import annotations

import sympy as sp


def convexification() -> None:
    c, B, D, eta, eps = sp.symbols(
        "c B D eta eps", positive=True
    )
    # The sign assumptions B<0 or D<=0 are imposed in the prose.  Use
    # independent positive magnitudes to replay the two boundary cases.
    beta, delta = sp.symbols("beta delta", positive=True)
    leaf = sp.Matrix([1 / c, -1])
    pair = sp.Matrix([-eta / c, eta])

    v_leaf_case = sp.Matrix([-beta, D])
    L_leaf = sp.factor(v_leaf_case[1] + c * v_leaf_case[0])
    at_boundary = sp.simplify(v_leaf_case + c * beta * leaf)
    assert at_boundary == sp.Matrix([0, L_leaf])
    strict_leaf = sp.simplify(v_leaf_case + (c * beta + eps) * leaf)
    assert strict_leaf == sp.Matrix([eps / c, L_leaf - eps])

    v_pair_case = sp.Matrix([B, -delta])
    L_pair = sp.factor(v_pair_case[1] + c * v_pair_case[0])
    at_boundary = sp.simplify(v_pair_case + delta / eta * pair)
    assert sp.simplify(at_boundary - sp.Matrix([L_pair / c, 0])) == sp.zeros(2, 1)
    strict_pair = sp.simplify(v_pair_case + (delta / eta + eps) * pair)
    assert sp.simplify(
        strict_pair - sp.Matrix([L_pair / c - eps * eta / c, eps * eta])
    ) == sp.zeros(2, 1)
    assert sp.simplify(leaf[1] + c * leaf[0]) == 0
    assert sp.simplify(pair[1] + c * pair[0]) == 0


def complete_reciprocal() -> None:
    r = sp.symbols("r", positive=True)
    C = sp.symbols("C", integer=True, positive=True)
    s = 1 / r

    bd_complete = (1 - 1 / s) / (1 - s ** (-C))
    db_complete = (1 - 1 / s) * (1 - 1 / C) / (1 - s ** (1 - C))
    assert sp.factor(bd_complete - (r - 1) / (r**C - 1)) == 0
    assert sp.factor(
        db_complete - (r - 1) * (1 - 1 / C) / (r ** (C - 1) - 1)
    ) == 0


def gate_clock_invariance() -> None:
    tau, favorable, adverse = sp.symbols(
        "tau favorable adverse", positive=True
    )
    probability = sp.factor(tau * favorable / (tau * favorable + tau * adverse))
    assert sp.factor(probability - favorable / (favorable + adverse)) == 0
    odds = sp.factor((tau * favorable) / (tau * adverse))
    assert sp.factor(odds - favorable / adverse) == 0


def response_scale_contradiction() -> None:
    r, p, delta, VB, VD, eB, qD = sp.symbols(
        "r p delta VB VD eB qD", positive=True
    )
    rho_b = p + p * delta * VB
    rho_d = p + p * delta * VD
    rhs = sp.factor(r**3 * (rho_b - p) * (rho_d - p))
    assert rhs == r**3 * p**2 * delta**2 * VB * VD

    # q_B = delta^2*e_B with e_B -> 0; only q_D <= 1 is needed.
    q_product = sp.factor((delta**2 * eB) * qD)
    assert q_product == delta**2 * eB * qD


def main() -> None:
    convexification()
    complete_reciprocal()
    gate_clock_invariance()
    response_scale_contradiction()
    print("PASS: leaf and tangent-pair convexification identities")
    print("PASS: exact reciprocal complete-core formulas")
    print("PASS: common cut clock preserves two-rate gate odds")
    print("PASS: response-scale MP contradiction algebra")
    print("OPEN: universal minimal stationary product / MPER sign")


if __name__ == "__main__":
    main()
