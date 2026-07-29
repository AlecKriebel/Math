#!/usr/bin/env python3
"""Independent exact checks for the Weyl--Bell divisibility theorem.

The verifier builds the d=6 Bell basis and a balanced Bell-diagonal
reflection over Q(sqrt(-3)), checks its stabilizers, marginals, and the
common three-site Weyl action, and separately replays the spectral
multiplicity arithmetic at d=4 and d=6.

It does not search sign tables: the theorem eliminates all of them at once.
"""

from __future__ import annotations

from fractions import Fraction

import sympy as sp


def exact_zero(expression: sp.Expr) -> bool:
    return sp.simplify(sp.expand_complex(expression)) == 0


def zero_matrix(matrix: sp.MatrixBase) -> bool:
    return all(exact_zero(entry) for entry in matrix)


def shift_matrix(d: int) -> sp.SparseMatrix:
    return sp.SparseMatrix(
        d,
        d,
        {((j + 1) % d, j): sp.Integer(1) for j in range(d)},
    )


def diagonal_matrix(entries: list[sp.Expr]) -> sp.SparseMatrix:
    return sp.SparseMatrix.diag(*entries)


def bell_vector(d: int, zeta: sp.Expr, a: int, b: int) -> sp.SparseMatrix:
    return sp.SparseMatrix(
        d * d,
        1,
        {
            (j * d + (j + a) % d, 0): zeta ** (b * j) / sp.sqrt(d)
            for j in range(d)
        },
    )


def partial_trace_first(matrix: sp.MatrixBase, d: int) -> sp.Matrix:
    out = sp.zeros(d)
    for y in range(d):
        for yp in range(d):
            out[y, yp] = sp.simplify(
                sum(matrix[x * d + y, x * d + yp] for x in range(d))
            )
    return out


def partial_trace_second(matrix: sp.MatrixBase, d: int) -> sp.Matrix:
    out = sp.zeros(d)
    for x in range(d):
        for xp in range(d):
            out[x, xp] = sp.simplify(
                sum(matrix[x * d + y, xp * d + y] for y in range(d))
            )
    return out


def exact_d6_matrix_calibration() -> None:
    d = 6
    zeta = (sp.Integer(1) + sp.I * sp.sqrt(3)) / 2
    assert sp.expand(zeta**6) == 1
    assert all(sp.simplify(zeta**k - 1) != 0 for k in range(1, d))

    x = shift_matrix(d)
    z = diagonal_matrix([zeta**j for j in range(d)])
    pair_x = sp.kronecker_product(x, x)
    pair_z = sp.kronecker_product(z**-1, z)

    columns = []
    for a in range(d):
        for b in range(d):
            phi = bell_vector(d, zeta, a, b)
            assert zero_matrix(pair_x * phi - zeta ** (-b) * phi)
            assert zero_matrix(pair_z * phi - zeta**a * phi)
            columns.append(phi)

    bell_change = sp.SparseMatrix.hstack(*columns)
    identity_pair = sp.eye(d * d)
    assert zero_matrix(bell_change.conjugate().T * bell_change - identity_pair)

    # A concrete balanced calibration object.  It is not asserted to satisfy
    # the exceptional cubic; it checks all symmetry and standardness inputs
    # used uniformly in the theorem.
    signs = [
        1 if b < d // 2 else -1
        for a in range(d)
        for b in range(d)
    ]
    assert sum(signs) == 0
    diagonal_signs = sp.SparseMatrix.diag(*signs)
    h = sp.simplify(
        bell_change * diagonal_signs * bell_change.conjugate().T
    )
    assert zero_matrix(h - h.conjugate().T)
    assert zero_matrix(h * h - identity_pair)
    assert exact_zero(sp.trace(h))
    assert partial_trace_first(h, d) == sp.zeros(d)
    assert partial_trace_second(h, d) == sp.zeros(d)
    assert zero_matrix(h * pair_x - pair_x * h)
    assert zero_matrix(h * pair_z - pair_z * h)

    identity_site = sp.eye(d)
    s = sp.kronecker_product(h, identity_site)
    t = sp.kronecker_product(identity_site, h)
    u = s * t

    common_x = sp.kronecker_product(x, x, x)
    common_z = sp.kronecker_product(z**-1, z, z**-1)
    identity_three = sp.eye(d**3)
    assert zero_matrix(common_x * common_z - zeta * common_z * common_x)
    assert common_x**d == identity_three
    assert zero_matrix(common_z**d - identity_three)
    assert zero_matrix(u * common_x - common_x * u)
    assert zero_matrix(u * common_z - common_z * u)

    # Trace orthogonality of the d^2 common-Weyl monomials.  By the Weyl
    # relation, checking their individual traces is enough.
    for r in range(d):
        for q in range(d):
            value = sp.trace(common_x**r * common_z**q)
            target = d**3 if (r, q) == (0, 0) else 0
            assert exact_zero(value - target)

    print("[ok] exact d=6 Bell basis and balanced reflection")
    print("[ok] zero Bell marginals and both two-site stabilizers")
    print("[ok] common three-site primitive Weyl algebra")


def spectral_arithmetic(d: int) -> tuple[int, int, int]:
    dimension = d**3
    m_one = Fraction(dimension, 4)
    m_nonreal = Fraction(3 * dimension, 8)
    assert m_one.denominator == 1
    assert m_nonreal.denominator == 1
    # Trace check using lambda_+ + lambda_- = -2/3.
    assert m_one - Fraction(2, 3) * m_nonreal == 0
    assert m_one + 2 * m_nonreal == dimension
    return int(m_one), int(m_nonreal), int(m_nonreal)


def exact_spectral_calibration() -> None:
    u = sp.symbols("u")
    polynomial = sp.expand(u**3 - 1 - sp.Rational(1, 3) * (u**2 - u))
    assert sp.factor(polynomial) == (u - 1) * (3 * u**2 + 2 * u + 3) / 3

    d4 = spectral_arithmetic(4)
    d6 = spectral_arithmetic(6)
    assert d4 == (16, 24, 24)
    assert all(multiplicity % 4 == 0 for multiplicity in d4)
    assert d6 == (54, 81, 81)
    assert d6[0] % 6 == 0
    assert d6[1] % 6 == 3 and d6[2] % 6 == 3

    # Uniform 2-adic conclusion: 8 | 3d^2 iff 4 | d.
    for d in range(2, 102, 2):
        assert ((3 * d * d) % 8 == 0) == (d % 4 == 0)

    print("[ok] cubic polynomial and inverse-paired roots")
    print("[ok] d=4 multiplicity calibration: (16, 24, 24)")
    print("[ok] d=6 contradiction: (54, 81, 81), with 6 not dividing 81")
    print("[scope] no Bell-diagonal d=4 witness is claimed")


def main() -> None:
    exact_d6_matrix_calibration()
    exact_spectral_calibration()
    print("Weyl--Bell-diagonal divisibility verifier: PASS")


if __name__ == "__main__":
    main()
