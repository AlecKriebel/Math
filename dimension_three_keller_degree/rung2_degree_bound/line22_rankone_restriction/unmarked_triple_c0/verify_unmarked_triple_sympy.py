#!/usr/bin/env python3
"""Exact certificate for the unmarked triple-companion c=0 orbit."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: verification requires assertions; do not use -O", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

x, y, z, scale = sp.symbols("x y z scale")
variables = (x, y, z)
p = x**2
q = y**2 + x * z
P = (p - q) ** 2
Q = (p + q) ** 2
R = x**3

mon3 = tuple(
    x**i * y**j * z ** (3 - i - j)
    for i in range(3, -1, -1)
    for j in range(3 - i, -1, -1)
)
mon2 = tuple(
    x**i * y**j * z ** (2 - i - j)
    for i in range(2, -1, -1)
    for j in range(2 - i, -1, -1)
)


def exact_zero(value):
    return sp.cancel(sp.expand(value)) == 0


def jac3(f, g, h):
    return sp.Matrix([f, g, h]).jacobian(variables).det()


def homogeneous_exponents(degree):
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def homogeneous_coefficients(value, degree):
    polynomial = sp.Poly(sp.expand(value), *variables)
    return [
        polynomial.coeff_monomial(x**i * y**j * z**k)
        for i, j, k in homogeneous_exponents(degree)
    ]


def coefficient_column(direction):
    U, V, W = direction
    return sp.Matrix(
        [sp.Poly(U, *variables).coeff_monomial(monomial) for monomial in mon3]
        + [
            sp.Poly(V, *variables).coeff_monomial(monomial)
            for monomial in mon3
        ]
        + [
            sp.Poly(W, *variables).coeff_monomial(monomial)
            for monomial in mon2
        ]
    )


def has_associate(polynomials, target):
    return any(
        exact_zero(polynomial - target) or exact_zero(polynomial + target)
        for polynomial in polynomials
    )


def raw_e7_certificate():
    u = sp.symbols("u0:10")
    v = sp.symbols("v0:10")
    w = sp.symbols("w0:6")
    U = sum(coefficient * monomial for coefficient, monomial in zip(u, mon3))
    V = sum(coefficient * monomial for coefficient, monomial in zip(v, mon3))
    W = sum(coefficient * monomial for coefficient, monomial in zip(w, mon2))
    E7 = sp.expand(
        jac3(P, Q, W) + jac3(P, V, R) + jac3(U, Q, R)
    )
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E7, 7), u + v + w
    )

    assert exact_zero(jac3(P, Q, R))
    assert matrix.shape == (36, 26)
    assert rhs == sp.zeros(36, 1)
    assert matrix.rank() == 16
    rows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17)
    columns = (1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 14, 15, 18, 19, 24, 25)
    assert (
        matrix.extract(rows, columns).det()
        == 3194799993706229268480
    )

    translations = tuple(
        tuple(sp.diff(component, variable) for component in (P, Q, R))
        for variable in variables
    )
    directions = (
        (x**3, 0, 0),
        (0, x**3, 0),
        translations[1],
        translations[2],
        translations[0],
        (-z * (p - q), z * (p + q), 0),
        (0, 0, p),
        (sp.Rational(8, 3) * y * (p - q), 0, x * y),
        (sp.Rational(8, 3) * z * (p - q), 0, x * z),
        (-sp.Rational(8, 3) * z * (p - q), 0, y**2),
    )
    kernel = sp.Matrix.hstack(
        *(coefficient_column(direction) for direction in directions)
    )
    assert matrix * kernel == sp.zeros(36, 10)
    assert kernel.rank() == 10
    kernel_rows = (0, 1, 2, 3, 10, 11, 12, 13, 20, 22)
    assert kernel.extract(kernel_rows, range(10)).det() == -sp.Rational(
        4096, 9
    )
    assert matrix.cols - matrix.rank() == kernel.cols
    print(
        "PASS E7: rank 16, complete ten-dimensional kernel, "
        "legal five-direction gauge"
    )


def lower_exit_certificate():
    S, w0, w1, w2, w3 = sp.symbols("S w0 w1 w2 w3")
    U = (p - q) * (
        sp.Rational(8, 3) * w1 * y
        + (-S + sp.Rational(8, 3) * (w2 - w3)) * z
    )
    V = S * z * (p + q)
    W = w0 * p + w1 * x * y + w2 * x * z + w3 * y**2

    a = sp.symbols("a0:6")
    b = sp.symbols("b0:6")
    ell = sp.symbols("l0:9")
    H2 = sp.Matrix(
        [
            sum(coefficient * monomial for coefficient, monomial in zip(a, mon2)),
            sum(coefficient * monomial for coefficient, monomial in zip(b, mon2)),
            W,
        ]
    )
    H3 = sp.Matrix([U, V, R])
    H4 = sp.Matrix([P, Q, 0])
    L = sp.Matrix(3, 3, ell)
    weighted = sp.Poly(
        sp.expand(
            (
                L
                + scale * H2.jacobian(variables)
                + scale**2 * H3.jacobian(variables)
                + scale**3 * H4.jacobian(variables)
            ).det()
        ),
        scale,
    )
    assert exact_zero(weighted.coeff_monomial(scale**8))
    assert exact_zero(weighted.coeff_monomial(scale**7))

    E6 = sp.expand(weighted.coeff_monomial(scale**6))
    constrained = a[1:] + b[1:] + ell[7:]
    matrix6, rhs6 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6, 6), constrained
    )
    assert matrix6.shape == (28, 12)
    assert matrix6.rank() == 10
    rows6 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 11)
    columns6 = (0, 1, 3, 4, 5, 6, 8, 9, 10, 11)
    assert (
        matrix6.extract(rows6, columns6).det() == 7925422620672
    )

    compat6 = [
        sp.factor((vector.T * rhs6)[0])
        for vector in matrix6.T.nullspace()
        if not exact_zero((vector.T * rhs6)[0])
    ]
    difference = w2 - w3
    assert has_associate(compat6, sp.Rational(16, 3) * w1 * difference)
    assert has_associate(
        compat6, -sp.Rational(32, 3) * difference**2
    )

    E6_reduced = sp.expand(E6.subs(w3, w2))
    matrix6r, rhs6r = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6_reduced, 6), constrained
    )
    assert matrix6r.rank() == 10
    solution6 = next(iter(sp.linsolve((matrix6r, rhs6r), constrained)))
    expected6 = (
        0,
        a[3] - sp.Rational(16, 9) * w1**2,
        a[3],
        -sp.Rational(4, 3) * S * w1,
        S**2 / 4,
        0,
        b[3],
        b[3],
        0,
        S**2 / 4,
        sp.Rational(2, 3) * w1 * (w0 - w2),
        S * w2 / 2 - w1**2 / 6,
    )
    assert all(
        exact_zero(actual - expected)
        for actual, expected in zip(solution6, expected6)
    )
    substitutions6 = {w3: w2}
    substitutions6.update(dict(zip(constrained, solution6)))
    assert exact_zero(E6.subs(substitutions6))
    print(
        "PASS E6: constant rank-10 minor, compatibility w2=w3, "
        "complete affine solve"
    )

    E5 = sp.expand(
        weighted.coeff_monomial(scale**5).subs(substitutions6)
    )
    lower5 = (
        a[0],
        a[3],
        b[0],
        b[3],
        ell[1],
        ell[2],
        ell[4],
        ell[5],
        ell[6],
    )
    matrix5, rhs5 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E5, 5), lower5
    )
    assert matrix5.rank() == 5
    compat5 = [
        sp.factor((vector.T * rhs5)[0])
        for vector in matrix5.T.nullspace()
        if not exact_zero((vector.T * rhs5)[0])
    ]
    assert has_associate(compat5, sp.Rational(8, 9) * w1**3)

    E5_reduced = sp.expand(E5.subs(w1, 0))
    expected_residual = 6 * x**2 * (
        S * a[3] * (x**2 * y + x * y * z + y**3)
        + S * b[3] * (x**2 * y - x * y * z - y**3)
        + ell[1] * (x**3 + x**2 * z + x * y**2)
        - 2 * ell[2] * (x**2 * y + x * y * z + y**3)
        + ell[4] * (x**3 - x**2 * z - x * y**2)
        - 2 * ell[5] * (x**2 * y - x * y * z - y**3)
    )
    assert exact_zero(E5_reduced - expected_residual)

    last_linear = (ell[1], ell[2], ell[4], ell[5])
    matrix5r, rhs5r = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E5_reduced, 5), last_linear
    )
    rows5 = (0, 1, 2, 4)
    assert matrix5r.extract(rows5, range(4)).det() == 20736
    solution5 = next(iter(sp.linsolve((matrix5r, rhs5r), last_linear)))
    expected5 = (0, S * a[3] / 2, 0, S * b[3] / 2)
    assert all(
        exact_zero(actual - expected)
        for actual, expected in zip(solution5, expected5)
    )
    final_substitutions = substitutions6 | {w1: 0}
    final_substitutions.update(dict(zip(last_linear, solution5)))
    assert exact_zero(weighted.coeff_monomial(scale**5).subs(final_substitutions))
    assert exact_zero(L.det().subs(final_substitutions))
    assert all(
        exact_zero(entry.subs(final_substitutions))
        for entry in (ell[1], ell[4], ell[7])
    )
    print(
        "PASS E5: compatibility w1=0; constant four-pivot solve "
        "zeros the second column of L"
    )


def main():
    raw_e7_certificate()
    lower_exit_certificate()
    print("ALL UNMARKED TRIPLE c=0 SYMPY CERTIFICATES PASSED")


if __name__ == "__main__":
    main()
