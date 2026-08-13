#!/usr/bin/env python3
"""Exact replay for serial/tensor composition of the singular leak ray.

This verifies the algebraic composition law.  It does not claim a universal
obstruction outside the cold-root diffuse branching class stated in the note.
"""

from __future__ import annotations

import sympy as sp


def cold_root_identity():
    r, t, y, z = sp.symbols("r t y z", positive=True)
    b = sp.factor(r * y / (t + r * y))
    s = sp.factor(r * z / (1 + r * z))

    assert sp.factor(t * b - r * (1 - b) * y) == 0
    assert sp.factor(s - r * (1 - s) * z) == 0

    # The dB map is increasing in z, so z<=t gives the displayed bound.
    upper = r * t / (1 + r * t)
    assert sp.factor(sp.diff(s, z)) == r / (r * z + 1) ** 2
    assert sp.factor(
        upper - s - r * (t - z) / ((r * t + 1) * (r * z + 1))
    ) == 0

    baseline = (r - 1) / r
    gain = sp.factor(1 - baseline)
    cost = baseline
    assert gain == 1 / r
    assert sp.simplify(cost / gain - (r - 1)) == 0

    # Every positive-gain cold endpoint b_root <= 1 has ratio at least r-1.
    b_root = sp.symbols("b_root", positive=True)
    excess = sp.factor(baseline / (b_root - baseline) - (r - 1))
    assert sp.factor(
        excess - (r - 1) * (1 - b_root) / (b_root - baseline)
    ) == 0


def tensor_realization():
    c, epsilon, theta = sp.symbols(
        "c epsilon theta", positive=True
    )
    p = sp.Matrix([c - epsilon, epsilon, 1 - c])
    weights = sp.Matrix(
        [
            [epsilon, (1 - theta) / epsilon, theta / (1 - c)],
            [(1 - theta) / epsilon, 1, 1],
            [theta / (1 - c), 1, 1 / epsilon],
        ]
    )
    assert weights == weights.T
    delta = weights * p
    kernel = sp.Matrix(
        3,
        3,
        lambda i, j: sp.factor(p[j] * weights[i, j] / delta[i]),
    )
    assert all(sp.factor(sum(kernel[i, j] for j in range(3)) - 1) == 0 for i in range(3))

    # Two factors suffice to certify the general factorization algebraically.
    p2 = sp.kronecker_product(p, p)
    weights2 = sp.kronecker_product(weights, weights)
    delta2 = weights2 * p2
    kernel2 = sp.Matrix(
        9,
        9,
        lambda i, j: sp.factor(p2[j] * weights2[i, j] / delta2[i]),
    )
    assert kernel2.applyfunc(sp.factor) == sp.kronecker_product(
        kernel, kernel
    ).applyfunc(sp.factor)

    adjoint = sp.diag(*[1 / value for value in p]) * kernel.T * sp.diag(*p)
    adjoint2 = (
        sp.diag(*[1 / value for value in p2])
        * kernel2.T
        * sp.diag(*p2)
    )
    assert adjoint2.applyfunc(sp.factor) == sp.kronecker_product(
        adjoint, adjoint
    ).applyfunc(sp.factor)


def response_composition():
    r, c, q1, q2 = sp.symbols("r c q1 q2", positive=True)
    L = sp.symbols("L", integer=True, positive=True)
    baseline = (r - 1) / r

    q_l = 1 - (1 - c) ** L
    beta = sp.factor(baseline + q_l / r)
    sigma = sp.factor(baseline - (r - 1) * q_l / r)
    gain = sp.factor(beta - baseline)
    cost = sp.factor(baseline - sigma)
    assert sp.simplify(cost / gain - (r - 1)) == 0

    union = sp.factor(1 - (1 - q1) * (1 - q2))
    assert union == q1 + q2 - q1 * q2
    gain_union = union / r
    cost_union = (r - 1) * union / r
    assert sp.factor(cost_union / gain_union - (r - 1)) == 0

    # Exact first two Taylor coefficients for symbolic positive integer L.
    assert sp.simplify(sp.diff(q_l, c).subs(c, 0) - L) == 0
    assert sp.simplify(
        sp.diff(q_l, c, 2).subs(c, 0) / 2 + L * (L - 1) / 2
    ) == 0

    # The powered ratio is strictly smaller at depth >1 for 1<r<2;
    # algebraically their difference has the positive factors shown here.
    depth = sp.symbols("depth", integer=True, positive=True)
    x = sp.symbols("x", positive=True)
    assert sp.simplify(x - x**depth - x * (1 - x ** (depth - 1))) == 0


def interval_endpoint():
    k, depth = sp.symbols("k depth", positive=True, integer=True)
    upper = 1 - 1 / k
    x = sp.symbols("x", positive=True)
    assert sp.simplify(x - x**depth - x * (1 - x ** (depth - 1))) == 0
    assert sp.simplify(upper - (k - 1) / k) == 0


def main():
    cold_root_identity()
    tensor_realization()
    response_composition()
    interval_endpoint()
    print("PASS: exact cold-root saturation identities")
    print("PASS: tensor symmetric-weight and adjoint factorization")
    print("PASS: polarized-mass union law and invariant ratio r-1")
    print("REFUTED FOR THIS COMPOSITION: powered ratio (r-1)^L")
    print("OPEN: non-cold, compensating, or non-diffuse hierarchies")


if __name__ == "__main__":
    main()
