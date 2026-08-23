#!/usr/bin/env python3
"""Exact audit for the canonical r=2 active determinant.

This verifier proves the displayed symbolic triangle certificate and checks
the distinction between the true collision coefficient and the stronger
promotion coefficient.  It does not prove the all-order determinant sign.
"""

from __future__ import annotations

import sympy as sp


class CertificateFailure(RuntimeError):
    """Raised when an explicit certificate check fails."""


def require(condition, detail="certificate check failed"):
    """Raise a failure that remains active under optimized Python."""
    if not condition:
        raise CertificateFailure(str(detail))


def active_kernel(P):
    """Return the exact forward active kernel K_P=R A_P."""
    n = len(P)
    states = [
        (B, v)
        for v in range(n)
        for B in range(1, 1 << n)
        if not ((B >> v) & 1)
    ]
    index = {state: position for position, state in enumerate(states)}
    kernel = sp.zeros(len(states))
    for source, (B, v) in enumerate(states):
        b = B.bit_count()
        for i in range(n):
            if P[v][i] == 0:
                continue
            kernel[source, index[B | (1 << i), v]] += P[v][i] / 2
        for w in range(n):
            if not ((B >> w) & 1):
                continue
            C = B & ~(1 << w)
            for i in range(n):
                if P[w][i] == 0:
                    continue
                kernel[source, index[C | (1 << i), w]] += P[w][i] / (2 * b)
        require(sp.factor(sum(kernel[source, j] for j in range(len(states)))) == 1)
    return states, kernel


def cofactors(kernel):
    laplacian = sp.eye(kernel.rows) - kernel
    return [
        sp.factor(laplacian.minor_submatrix(root, root).det(method="domain-ge"))
        for root in range(kernel.rows)
    ]


def triangle_audit():
    a, b, c = sp.symbols("a b c", positive=True)
    weights = (
        (0, a, b),
        (a, 0, c),
        (b, c, 0),
    )
    P = [
        [sp.Integer(0) if i == j else weights[i][j] / sum(weights[i])
         for j in range(3)]
        for i in range(3)
    ]
    states, kernel = active_kernel(P)
    require(len(states) == 9)
    trees = cofactors(kernel)
    partition = sp.factor(sum(trees))
    harmonic = [sp.Rational(1, B.bit_count()) for B, _ in states]
    reward = sp.factor(sum(tree * value for tree, value in zip(trees, harmonic)))

    collision_coefficient = sp.factor(reward - sp.Rational(3, 4) * partition)
    cleared = sp.factor(
        collision_coefficient
        * sp.Integer(4096)
        * (a + b) ** 2
        * (a + c) ** 2
        * (b + c) ** 2
        / 3
    )

    def q(x, y, z):
        return (
            16 * x**2 * y**2
            + 20 * x * y * (x + y) * z
            + 19 * x * y * z**2
            + 12 * (x + y) * z**3
        )

    certificate = sp.expand(
        (a - b) ** 2 * q(a, b, c)
        + (b - c) ** 2 * q(b, c, a)
        + (c - a) ** 2 * q(c, a, b)
    )
    require(sp.expand(cleared - certificate) == 0)
    require(sp.Poly(certificate, a, b, c).coeff_monomial(a**2 * b**2 * c**2) == -114)

    # Promotion has the larger threshold c_P=3/4+(R-3/2)/24 for n=3.
    row_square = sum(P[i][j] ** 2 for i in range(3) for j in range(3))
    c_P = sp.Rational(3, 4) + (row_square - sp.Rational(3, 2)) / 24
    promotion_coefficient = sp.factor(reward - c_P * partition)
    require(sp.factor(
        collision_coefficient
        - promotion_coefficient
        - (c_P - sp.Rational(3, 4)) * partition
    ) == 0)
    require(sp.factor(c_P.subs({a: 1, b: 2, c: 3}) - sp.Rational(3, 4)) > 0)

    # Check the coefficient-of-epsilon identity independently after exact
    # rational specialization.  Expanding the fully symbolic 9x9 determinant
    # is needlessly expensive; the cofactor formula above already holds over
    # QQ(a,b,c), while these tests audit the matrix orientation convention.
    epsilon = sp.symbols("epsilon")
    diagonal = sp.diag(*[
        value - sp.Rational(3, 4) for value in harmonic
    ])
    for values in ({a: 1, b: 2, c: 3}, {a: 2, b: 5, c: 7}):
        specialized = (sp.eye(kernel.rows) - kernel + epsilon * diagonal).subs(values)
        determinant = specialized.det(method="domain-ge")
        expected = collision_coefficient.subs(values)
        require(sp.factor(sp.expand(determinant).coeff(epsilon, 1) - expected) == 0)

    print("PASS: nine-state active-tree determinant reconstructed symbolically")
    print("PASS: true triangle collision numerator is a centered positive certificate")
    print("PASS: raw edge-monomial coefficient positivity is exactly false")
    print("PASS: promotion and collision coefficients are distinct with the proved direction")


if __name__ == "__main__":
    triangle_audit()
    print("OPEN: universal active-tree collision coefficient")
