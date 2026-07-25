#!/usr/bin/env python3
"""Fail-closed exact certificate for the unmarked c=3 resonance orbit."""

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
R = x * (p - 3 * q)
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


def nonzero_coefficients(value):
    return [
        coefficient
        for _, coefficient in sp.Poly(sp.expand(value), *variables).terms()
    ]


def coefficient_column(U, V, W):
    return sp.Matrix(
        [sp.Poly(U, *variables).coeff_monomial(monomial) for monomial in mon3]
        + [sp.Poly(V, *variables).coeff_monomial(monomial) for monomial in mon3]
        + [sp.Poly(W, *variables).coeff_monomial(monomial) for monomial in mon2]
    )


def check_raw_e7_and_gauge():
    uu = sp.symbols("r_u0:10")
    vv = sp.symbols("r_v0:10")
    ww = sp.symbols("r_w0:6")
    U = sum(uu[i] * mon3[i] for i in range(10))
    V = sum(vv[i] * mon3[i] for i in range(10))
    W = sum(ww[i] * mon2[i] for i in range(6))
    assert exact_zero(jac3(P, Q, R))
    E7 = sp.expand(jac3(P, Q, W) + jac3(P, V, R) + jac3(U, Q, R))
    delta = lambda f: 2 * y * sp.diff(f, z) - x * sp.diff(f, y)
    compact = 2 * (
        8 * x * (p - q) * (p + q) * delta(W)
        + 3 * (p + q) * (q - 3 * p) * delta(U)
        + 3 * (p - q) * (p + q) * delta(V)
    )
    assert exact_zero(E7 - compact)
    unknowns = uu + vv + ww
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E7, 7), unknowns
    )
    assert rhs == sp.zeros(36, 1)
    assert matrix.shape == (36, 26)
    assert matrix.rank() == 14
    rows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15)
    columns = (1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 14, 15, 18, 19)
    assert matrix.extract(rows, columns).det() == -1039973956284579840

    tau_x = (sp.diff(P, x), sp.diff(Q, x), sp.diff(R, x))
    tau_y = (sp.diff(P, y), sp.diff(Q, y), sp.diff(R, y))
    gauge = (
        (R, 0, 0),
        (0, R, 0),
        tau_x,
        tau_y,
    )
    quotient = (
        (x * q, 0, 0),
        (0, x * q, 0),
        (y * (p - q), y * (3 * p - q), 0),
        (z * (p - q), z * (3 * p - q), 0),
        (0, 0, p),
        (0, 8 * x**2 * z, 3 * y**2),
        (0, -8 * x * y * z, 3 * y * z),
        (0, -8 * x * z**2, 3 * z**2),
    )
    kernel_matrix = sp.Matrix.hstack(
        *(coefficient_column(*direction) for direction in gauge + quotient)
    )
    assert matrix * kernel_matrix == sp.zeros(36, 12)
    assert kernel_matrix.rank() == 12
    kernel_rows = (0, 1, 2, 3, 10, 11, 12, 13, 14, 15, 20, 22)
    assert kernel_matrix.extract(kernel_rows, range(12)).det() == 49152
    assert matrix.cols - matrix.rank() == kernel_matrix.rank()

    gauge_coordinates = sp.Matrix(
        [
            [
                sp.Poly(direction[0], *variables).coeff_monomial(x**3)
                for direction in gauge
            ],
            [
                sp.Poly(direction[1], *variables).coeff_monomial(x**3)
                for direction in gauge
            ],
            [
                sp.Poly(direction[2], *variables).coeff_monomial(x * y)
                for direction in gauge
            ],
            [
                sp.Poly(direction[2], *variables).coeff_monomial(x * z)
                for direction in gauge
            ],
        ]
    )
    assert gauge_coordinates.det() == -36
    print(
        "PASS raw E7: rank 14, complete 12-dimensional kernel, "
        "and division-free four-coordinate gauge"
    )


def polynomial_left_pairings(matrix, rhs):
    output = []
    for vector in matrix.T.nullspace():
        denominators = [
            sp.together(item).as_numer_denom()[1] for item in vector
        ]
        common = sp.lcm(denominators)
        cleared = sp.Matrix([sp.cancel(common * item) for item in vector])
        assert all(exact_zero(item) for item in matrix.T * cleared)
        pairing = sp.factor(sp.expand(cleared.dot(rhs)))
        if pairing != 0:
            output.append(pairing)
    return output


def check_e6_compatibility_and_exit():
    A, B, C, D, e, f, g, w = sp.symbols("A B C D e f g w")
    u0, uq, u1, u2, u3, u4 = sp.symbols("u0 uq u1 u2 u3 u4")
    v0, vq, v1, v2, v3, v4 = sp.symbols("v0 vq v1 v2 v3 v4")
    ell = sp.symbols("l0:9")
    U3 = A * x * q + C * y * (p - q) + D * z * (p - q)
    V3 = (
        B * x * q
        + C * y * (3 * p - q)
        + D * z * (3 * p - q)
        + 8 * e * x**2 * z
        - 8 * f * x * y * z
        - 8 * g * x * z**2
    )
    W2 = w * p + 3 * e * y**2 + 3 * f * y * z + 3 * g * z**2
    U2 = u0 * p + uq * q + u1 * x * y + u2 * x * z + u3 * y * z + u4 * z**2
    V2 = v0 * p + vq * q + v1 * x * y + v2 * x * z + v3 * y * z + v4 * z**2
    H4 = sp.Matrix([P, Q, 0])
    H3 = sp.Matrix([U3, V3, R])
    H2 = sp.Matrix([U2, V2, W2])
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
    E6 = sp.expand(weighted.coeff_monomial(s**6))
    lower = (
        u0,
        uq,
        u1,
        u2,
        u3,
        u4,
        v0,
        vq,
        v1,
        v2,
        v3,
        v4,
        ell[7],
        ell[8],
    )
    def compatibility(substitutions):
        specialized = sp.expand(E6.subs(substitutions))
        matrix, rhs = sp.linear_eq_to_matrix(
            nonzero_coefficients(specialized), lower
        )
        return matrix, rhs, polynomial_left_pairings(matrix, rhs)

    matrix0, rhs0, pairs0 = compatibility({})
    assert matrix0.shape == (24, 14)
    assert matrix0.rank() == 8
    assert matrix0.rank() < matrix0.row_join(rhs0).rank()
    assert len(pairs0) == 16
    assert exact_zero(pairs0[11] + 192 * g**2)
    poly6 = sp.Poly(E6, *variables)
    assert exact_zero(
        poly6.coeff_monomial(x * y * z**4) - 192 * g**2
    )

    _, _, pairs1 = compatibility({g: 0})
    assert len(pairs1) == 11
    assert exact_zero(pairs1[5] - pairs1[10] - 144 * f**2)
    poly6g = sp.Poly(E6.subs(g, 0), *variables)
    assert exact_zero(
        -poly6g.coeff_monomial(x**2 * y * z**3)
        + poly6g.coeff_monomial(y**5 * z)
        - 144 * f**2
    )

    _, _, pairs2 = compatibility({g: 0, f: 0})
    assert len(pairs2) == 10
    assert exact_zero(pairs2[3] + pairs2[4] - 48 * (D + 2 * e) ** 2)
    poly6gf = sp.Poly(E6.subs({g: 0, f: 0}), *variables)
    assert exact_zero(
        poly6gf.coeff_monomial(x**4 * y * z)
        - poly6gf.coeff_monomial(x**3 * y**3)
        - 2 * poly6gf.coeff_monomial(x**3 * y * z**2)
        + poly6gf.coeff_monomial(x**2 * y**3 * z)
        + poly6gf.coeff_monomial(x**2 * y * z**3)
        + 48 * (D + 2 * e) ** 2
    )

    _, _, pairs3 = compatibility({g: 0, f: 0, D: -2 * e})
    assert len(pairs3) == 10
    assert exact_zero(pairs3[3] + 24 * C**2)
    poly6gfd = sp.Poly(
        E6.subs({g: 0, f: 0, D: -2 * e}), *variables
    )
    assert exact_zero(
        poly6gfd.coeff_monomial(x**5 * y)
        - poly6gfd.coeff_monomial(x**3 * y**3)
        - poly6gfd.coeff_monomial(x**3 * y * z**2)
        + poly6gfd.coeff_monomial(x**2 * y**3 * z)
        - 24 * C**2
    )
    print(
        "PASS E6 compatibility: g=f=C=0 and D=-2e by staged "
        "division-free square certificates"
    )

    surviving = {g: 0, f: 0, D: -2 * e, C: 0}
    E6s = sp.expand(E6.subs(surviving))
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6s, 6), lower
    )
    assert matrix.shape == (28, 14)
    assert matrix.rank() == 8
    rows = (0, 1, 2, 3, 4, 5, 6, 8)
    columns = (2, 3, 4, 5, 8, 9, 10, 11)
    assert matrix.extract(rows, columns).det() == 5159780352
    solution = next(iter(sp.linsolve((matrix, rhs), lower)))
    expected = (
        u0,
        uq,
        0,
        A * e,
        0,
        e**2,
        v0,
        vq,
        -sp.Rational(8, 3) * ell[7],
        B * e + 8 * e**2 - sp.Rational(8, 3) * ell[8],
        0,
        e**2,
        ell[7],
        ell[8],
    )
    assert all(exact_zero(solution[i] - expected[i]) for i in range(14))
    lower_solution = {
        lower[i]: solution[i]
        for i in range(14)
        if solution[i] != lower[i]
    }
    assert exact_zero(E6s.subs(lower_solution))
    print("PASS surviving E6 branch: constant rank-8 minor and complete solve")

    E5 = sp.expand(
        weighted.coeff_monomial(s**5)
        .subs(surviving)
        .subs(lower_solution)
    )
    poly5 = sp.Poly(E5, *variables)
    c_x5 = poly5.coeff_monomial(x**5)
    c_x4z = poly5.coeff_monomial(x**4 * z)
    c_x3z2 = poly5.coeff_monomial(x**3 * z**2)
    column2_matrix, column2_rhs = sp.linear_eq_to_matrix(
        (c_x5, c_x4z, c_x3z2), (ell[1], ell[4], ell[7])
    )
    assert column2_rhs == sp.zeros(3, 1)
    resonance = -6 * A + 3 * B + 48 * e + 16 * w
    assert exact_zero(column2_matrix.det() + 96 * resonance)

    # If ell_32=0, c_x4z and c_x3z2 successively force ell_12=ell_22=0.
    assert exact_zero(c_x4z.subs(ell[7], 0) - 12 * ell[1])
    assert exact_zero(
        c_x3z2.subs({ell[7]: 0, ell[1]: 0}) - 6 * ell[4]
    )

    branch = {B: 2 * A - 16 * e - sp.Rational(16, 3) * w}
    E5b = sp.expand(E5.subs(branch))
    e5_matrix, e5_rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E5b, 5),
        (ell[1], ell[2], ell[4], ell[5]),
    )
    assert e5_matrix.rank() == 4
    assert e5_matrix.extract((0, 1, 2, 4), range(4)).det() == 20736
    e5_solution = {
        ell[1]: -A * ell[7] / 2,
        ell[4]: (-15 * A + 96 * e + 32 * w) * ell[7] / 18,
        ell[2]: A * (3 * e**2 - ell[8]) / 2 + e * uq,
        ell[5]: (
            (15 * A - 96 * e - 32 * w) * (3 * e**2 - ell[8]) / 18
            + e * vq
        ),
    }
    assert exact_zero(E5b.subs(e5_solution))
    print(
        "PASS E5: off the resonance determinant column 2 vanishes; "
        "on it the displayed numeric-pivot solve is complete"
    )

    E4 = sp.expand(
        weighted.coeff_monomial(s**4)
        .subs(surviving)
        .subs(lower_solution)
        .subs(branch)
        .subs(e5_solution)
    )
    poly4 = sp.Poly(E4, *variables)
    assert exact_zero(
        poly4.coeff_monomial(x**2 * z**2)
        - sp.Rational(16, 3) * ell[7] * (3 * e**2 - ell[8])
    )
    E4b = sp.expand(E4.subs(ell[8], 3 * e**2))
    assert exact_zero(
        sp.Poly(E4b, *variables).coeff_monomial(x**3 * y)
        - sp.Rational(16, 3) * ell[7] ** 2
    )
    print("PASS E4: two literal pivots force ell_32=0 and hence det L=0")


def main():
    check_raw_e7_and_gauge()
    check_e6_compatibility_and_exit()
    print("ALL UNMARKED c=3 RESONANCE SYMPY CERTIFICATES PASSED")


if __name__ == "__main__":
    main()
