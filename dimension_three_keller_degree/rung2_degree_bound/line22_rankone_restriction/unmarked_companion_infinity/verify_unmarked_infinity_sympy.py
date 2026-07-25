#!/usr/bin/env python3
"""Fail-closed exact certificate for the unmarked companion-at-infinity orbit.

The script reconstructs all coefficient matrices from the full 3-by-3
Jacobian determinant.  It does not load cached matrices or row reductions.
"""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: verification requires assertions; do not use -O", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

x, y, z, s = sp.symbols("x y z s")
variables = (x, y, z)
p = x**2
q = y**2 + x * z
P = (p - q) ** 2
Q = (p + q) ** 2
R = x * q

mon3 = (
    x**3,
    x**2 * y,
    x**2 * z,
    x * y**2,
    x * y * z,
    x * z**2,
    y**3,
    y**2 * z,
    y * z**2,
    z**3,
)
mon2 = (x**2, x * y, x * z, y**2, y * z, z**2)


def exact_zero(value):
    return sp.cancel(sp.expand(value)) == 0


def jac3(f, g, h):
    return sp.Matrix(
        [[sp.diff(function, variable) for variable in variables]
         for function in (f, g, h)]
    ).det()


def homogeneous_exponents(degree):
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def homogeneous_coefficients(value, degree):
    poly = sp.Poly(sp.expand(value), *variables)
    return [
        poly.coeff_monomial(x**i * y**j * z**k)
        for i, j, k in homogeneous_exponents(degree)
    ]


def coefficient_column(U, V, W):
    return sp.Matrix(
        [sp.Poly(U, *variables).coeff_monomial(monomial) for monomial in mon3]
        + [sp.Poly(V, *variables).coeff_monomial(monomial) for monomial in mon3]
        + [sp.Poly(W, *variables).coeff_monomial(monomial) for monomial in mon2]
    )


def check_top_and_raw_e7():
    uu = sp.symbols("u0:10")
    vv = sp.symbols("v0:10")
    ww = sp.symbols("w0:6")
    U = sum(uu[i] * mon3[i] for i in range(10))
    V = sum(vv[i] * mon3[i] for i in range(10))
    W = sum(ww[i] * mon2[i] for i in range(6))

    assert exact_zero(jac3(P, Q, R))
    E7 = sp.expand(jac3(P, Q, W) + jac3(P, V, R) + jac3(U, Q, R))
    delta = lambda f: 2 * y * sp.diff(f, z) - x * sp.diff(f, y)
    compact = 2 * (
        8 * x * (p - q) * (p + q) * delta(W)
        + (p + q) * (2 * p - q) * delta(U)
        - (p - q) * (2 * p + q) * delta(V)
    )
    assert exact_zero(E7 - compact)

    unknowns = uu + vv + ww
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E7, 7), unknowns
    )
    assert rhs == sp.zeros(rhs.rows, 1)
    assert matrix.shape == (36, 26)
    assert matrix.rank() == 18
    rows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 22)
    columns = (1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 14, 15, 16, 17, 18, 19, 24, 25)
    raw_minor = matrix.extract(rows, columns).det()
    assert raw_minor == 1709960483517235200

    translations = tuple(
        (
            sp.diff(P, variable),
            sp.diff(Q, variable),
            sp.diff(R, variable),
        )
        for variable in variables
    )
    directions = (
        (x**3, 0, 0),
        (x * q, 0, 0),
        (0, x**3, 0),
        (0, x * q, 0),
        (0, 0, p),
        (0, 0, q),
        translations[0],
        translations[1],
    )
    kernel_matrix = sp.Matrix.hstack(
        *(coefficient_column(*direction) for direction in directions)
    )
    assert matrix * kernel_matrix == sp.zeros(36, 8)
    assert kernel_matrix.rank() == 8
    kernel_rows = (0, 1, 2, 3, 10, 12, 20, 22)
    assert kernel_matrix.extract(kernel_rows, range(8)).det() == -8

    relation = tuple(
        sp.expand(
            translations[2][coordinate]
            + 2 * directions[0][coordinate]
            - 2 * directions[1][coordinate]
            - 2 * directions[2][coordinate]
            - 2 * directions[3][coordinate]
            - directions[4][coordinate]
        )
        for coordinate in range(3)
    )
    assert relation == (0, 0, 0)
    assert matrix.cols - matrix.rank() == kernel_matrix.rank()
    print(
        "PASS raw E7: rank 18, complete eight-dimensional kernel, "
        "minor 1709960483517235200"
    )


def check_e6_e5_exit():
    A, B, w0, w1 = sp.symbols("A B w0 w1")
    u0, uq, du1, du2, du3, du4 = sp.symbols(
        "u0 uq du1 du2 du3 du4"
    )
    v0, vq, dv1, dv2, dv3, dv4 = sp.symbols(
        "v0 vq dv1 dv2 dv3 dv4"
    )
    ell = sp.symbols("l0:9")
    U2 = (
        u0 * p
        + uq * q
        + du1 * x * y
        + du2 * x * z
        + du3 * y * z
        + du4 * z**2
    )
    V2 = (
        v0 * p
        + vq * q
        + dv1 * x * y
        + dv2 * x * z
        + dv3 * y * z
        + dv4 * z**2
    )
    H4 = sp.Matrix([P, Q, 0])
    H3 = sp.Matrix([A * x**3, B * x**3, R])
    H2 = sp.Matrix([U2, V2, w0 * p + w1 * q])
    L = sp.Matrix(3, 3, ell)
    weighted = sp.Poly(
        sp.expand(
            (
                L
                + s * H2.jacobian(variables)
                + s**2 * H3.jacobian(variables)
                + s**3 * H4.jacobian(variables)
            ).det()
        ),
        s,
    )
    assert exact_zero(weighted.coeff_monomial(s**8))
    assert exact_zero(weighted.coeff_monomial(s**7))

    E6 = weighted.coeff_monomial(s**6)
    constrained = (
        ell[7],
        ell[8],
        du1,
        du2,
        du3,
        du4,
        dv1,
        dv2,
        dv3,
        dv4,
    )
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6, 6), constrained
    )
    assert matrix.shape == (28, 10)
    assert rhs == sp.zeros(28, 1)
    assert matrix.rank() == 10
    rows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 11)
    forcing_minor = matrix.extract(rows, range(10)).det()
    assert forcing_minor == 4831838208
    solution = next(iter(sp.linsolve((matrix, rhs), constrained)))
    assert solution == (0,) * 10
    forcing = dict(zip(constrained, solution))
    assert exact_zero(E6.subs(forcing))
    assert not (
        E6.free_symbols
        & {A, B, w0, w1, u0, uq, v0, vq, ell[0], ell[1], ell[2],
           ell[3], ell[4], ell[5], ell[6]}
    )
    print(
        "PASS E6: constant rank-10 forcing minor 4831838208; "
        "all ten constrained coefficients vanish"
    )

    E5 = sp.expand(weighted.coeff_monomial(s**5).subs(forcing))
    poly5 = sp.Poly(E5, *variables)
    assert exact_zero(poly5.coeff_monomial(x**5) + 4 * (ell[1] - ell[4]))
    assert exact_zero(
        poly5.coeff_monomial(x**4 * z) + 2 * (ell[1] + ell[4])
    )
    assert exact_zero(
        poly5.coeff_monomial(x**4 * y) - 8 * (ell[2] - ell[5])
    )
    assert exact_zero(
        poly5.coeff_monomial(x**3 * y * z) - 4 * (ell[2] + ell[5])
    )
    forced_linear = {
        ell[1]: 0,
        ell[2]: 0,
        ell[4]: 0,
        ell[5]: 0,
        ell[7]: 0,
        ell[8]: 0,
    }
    assert exact_zero(E5.subs(forced_linear))
    assert exact_zero(L.det().subs(forced_linear))
    print("PASS E5: four literal pivots force columns 2 and 3 of L to vanish")


def main():
    check_top_and_raw_e7()
    check_e6_e5_exit()
    print("ALL UNMARKED COMPANION-INFINITY SYMPY CERTIFICATES PASSED")


if __name__ == "__main__":
    main()
