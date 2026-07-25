#!/usr/bin/env python3
"""Exact certificates for the two marked-critical mixed companion orbits."""

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
P = p**2
Q = q**2
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


def raw_certificate(label, R):
    u = sp.symbols(f"{label}u0:10")
    v = sp.symbols(f"{label}v0:10")
    w = sp.symbols(f"{label}w0:6")
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
    assert rhs == sp.zeros(36, 1)
    assert matrix.shape == (36, 26)
    assert matrix.rank() == 18
    rows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 19)
    columns = (1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 14, 15, 16, 17, 18, 19, 24, 25)
    assert matrix.extract(rows, columns).det() == -5343626510991360

    translations = tuple(
        tuple(sp.diff(component, variable) for component in (P, Q, R))
        for variable in variables
    )
    if label == "other":
        normals = (
            (0, x**3, 0),
            (0, 2 * z * q, x * z),
            (0, -2 * z * q, y**2),
        )
        expected_minor = 32
    else:
        normals = (
            (0, 0, p),
            (0, -2 * z * q, x * z),
            (0, 2 * z * q, y**2),
        )
        expected_minor = 64
    directions = (
        (R, 0, 0),
        (0, R, 0),
        translations[0],
        translations[1],
        translations[2],
    ) + normals
    kernel = sp.Matrix.hstack(
        *(coefficient_column(direction) for direction in directions)
    )
    assert matrix * kernel == sp.zeros(36, 8)
    assert kernel.rank() == 8
    kernel_rows = (0, 2, 10, 12, 14, 15, 20, 22)
    assert (
        kernel.extract(kernel_rows, range(8)).det() == expected_minor
    )
    assert matrix.cols - matrix.rank() == kernel.cols
    print(
        f"PASS {label} E7: rank 18 and complete five-gauge/"
        "three-normal kernel"
    )


def lower_certificate(label, R):
    w0, w2, w3, A = sp.symbols(f"{label}w0 {label}w2 {label}w3 {label}A")
    difference = w2 - w3
    if label == "other":
        H3 = sp.Matrix([0, A * x**3 + 2 * difference * z * q, R])
        W = w2 * x * z + w3 * y**2
        sign = 1
        expected6_minor = -100663296
        expected5_minor = 256
        rows6 = (0, 1, 2, 3, 4, 5, 6, 8, 9, 13)
        rows5 = (0, 1, 5, 8)
    else:
        H3 = sp.Matrix([0, -2 * difference * z * q, R])
        W = w0 * p + w2 * x * z + w3 * y**2
        sign = -1
        expected6_minor = 2717908992
        expected5_minor = 2304
        rows6 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 11)
        rows5 = (0, 1, 2, 4)

    a = sp.symbols(f"{label}a0:6")
    b = sp.symbols(f"{label}b0:6")
    ell = sp.symbols(f"{label}l0:9")
    H2 = sp.Matrix(
        [
            sum(coefficient * monomial for coefficient, monomial in zip(a, mon2)),
            sum(coefficient * monomial for coefficient, monomial in zip(b, mon2)),
            W,
        ]
    )
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
    columns6 = (0, 1, 3, 4, 5, 6, 8, 9, 10, 11)
    assert (
        matrix6.extract(rows6, columns6).det() == expected6_minor
    )
    solution6 = next(iter(sp.linsolve((matrix6, rhs6), constrained)))
    expected6 = (
        0,
        a[3],
        a[3],
        0,
        0,
        0,
        b[3],
        b[3],
        0,
        difference**2,
        0,
        sign * w3 * difference,
    )
    assert all(
        exact_zero(actual - expected)
        for actual, expected in zip(solution6, expected6)
    )
    substitutions6 = dict(zip(constrained, solution6))
    assert exact_zero(E6.subs(substitutions6))

    E5 = sp.expand(
        weighted.coeff_monomial(scale**5).subs(substitutions6)
    )
    last_linear = (ell[1], ell[2], ell[4], ell[5])
    matrix5, rhs5 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E5, 5), last_linear
    )
    assert matrix5.rank() == 4
    assert (
        matrix5.extract(rows5, range(4)).det() == expected5_minor
    )
    solution5 = next(iter(sp.linsolve((matrix5, rhs5), last_linear)))
    expected5 = (
        0,
        sign * a[3] * difference,
        0,
        sign * b[3] * difference,
    )
    assert all(
        exact_zero(actual - expected)
        for actual, expected in zip(solution5, expected5)
    )
    substitutions5 = substitutions6 | dict(zip(last_linear, solution5))
    assert exact_zero(
        weighted.coeff_monomial(scale**5).subs(substitutions5)
    )
    assert all(
        exact_zero(entry.subs(substitutions5))
        for entry in (ell[1], ell[4], ell[7])
    )
    assert exact_zero(L.det().subs(substitutions5))
    print(
        f"PASS {label} E6/E5: constant complete solves zero "
        "the second column of L"
    )


def main():
    cases = (("other", x * q), ("distinct", x * (p - q)))
    for label, R in cases:
        raw_certificate(label, R)
        lower_certificate(label, R)
    print("ALL MARKED-CRITICAL MIXED-ORBIT SYMPY CERTIFICATES PASSED")


if __name__ == "__main__":
    main()
