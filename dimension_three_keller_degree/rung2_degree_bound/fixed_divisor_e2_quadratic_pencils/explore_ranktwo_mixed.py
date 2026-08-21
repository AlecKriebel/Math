#!/usr/bin/env python3
"""Exact exploratory elimination for the rank-two, mixed e=2 orbit.

This is deliberately not yet a release verifier.  It prints complete
linear-algebra data for the unresolved C=D=0 branch without assertions
that presuppose the desired exit.
"""

from __future__ import annotations

import sympy as sp

x, y, z, scale = sp.symbols("x y z scale")
variables = (x, y, z)
p = x**2
q = y * z
P = p**2
Q = p * q
R = x * q

mon2 = tuple(
    x**i * y**j * z ** (2 - i - j)
    for i in range(2, -1, -1)
    for j in range(2 - i, -1, -1)
)
mon3 = tuple(
    x**i * y**j * z ** (3 - i - j)
    for i in range(3, -1, -1)
    for j in range(3 - i, -1, -1)
)


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


def jac3(f, g, h):
    return sp.Matrix([f, g, h]).jacobian(variables).det()


def nonzero_compatibilities(matrix, rhs):
    return [
        sp.factor((vector.T * rhs)[0])
        for vector in matrix.T.nullspace()
        if sp.expand((vector.T * rhs)[0]) != 0
    ]


def coefficient_column(direction):
    U, V, W = direction
    return sp.Matrix(
        [sp.Poly(U, *variables).coeff_monomial(monomial) for monomial in mon3]
        + [sp.Poly(V, *variables).coeff_monomial(monomial) for monomial in mon3]
        + [sp.Poly(W, *variables).coeff_monomial(monomial) for monomial in mon2]
    )


def raw_e7_data():
    u = sp.symbols("u0:10")
    v = sp.symbols("v0:10")
    w = sp.symbols("w0:6")
    U = sum(c * monomial for c, monomial in zip(u, mon3))
    V = sum(c * monomial for c, monomial in zip(v, mon3))
    W = sum(c * monomial for c, monomial in zip(w, mon2))
    E7 = sp.expand(
        jac3(P, Q, W) + jac3(P, V, R) + jac3(U, Q, R)
    )
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E7, 7), u + v + w
    )
    rows = matrix.T.rref()[1]
    columns = matrix.rref()[1]
    square = matrix.extract(rows, columns)
    print("raw E7 rank/pivots/minor:", matrix.rank(), rows, columns, square.det())
    translations = tuple(
        tuple(sp.diff(component, variable) for component in (P, Q, R))
        for variable in variables
    )
    directions = (
        (R, 0, 0),
        (0, R, 0),
        translations[0],
        translations[1],
        translations[2],
        (0, x**3, 0),
        (4 * x**2 * y, y**2 * z, 0),
        (4 * x**2 * z, y * z**2, 0),
        (0, 0, x**2),
        (0, x * y**2, y**2),
        (0, 0, y * z),
        (0, x * z**2, z**2),
    )
    kernel = sp.Matrix.hstack(
        *(coefficient_column(direction) for direction in directions)
    )
    kernel_rows = kernel.T.rref()[1]
    print(
        "raw kernel shape/rank/rows/minor/check:",
        kernel.shape,
        kernel.rank(),
        kernel_rows,
        kernel.extract(kernel_rows, range(12)).det(),
        matrix * kernel == sp.zeros(36, 12),
    )


def general_e6_data():
    A, C, D, w0, w3, w4, w5 = sp.symbols("A C D w0 w3 w4 w5")
    U = 4 * C * x**2 * y + 4 * D * x**2 * z
    V = (
        A * x**3
        + C * y**2 * z
        + D * y * z**2
        + w3 * x * y**2
        + w5 * x * z**2
    )
    W = w0 * p + w3 * y**2 + w4 * q + w5 * z**2
    a = sp.symbols("ga0:6")
    b = sp.symbols("gb0:6")
    ell = sp.symbols("gl0:9")
    H2 = sp.Matrix(
        [
            sum(c * monomial for c, monomial in zip(a, mon2)),
            sum(c * monomial for c, monomial in zip(b, mon2)),
            W,
        ]
    )
    L = sp.Matrix(3, 3, ell)
    weighted = sp.Poly(
        sp.expand(
            (
                L
                + scale * H2.jacobian(variables)
                + scale**2 * sp.Matrix([U, V, R]).jacobian(variables)
                + scale**3 * sp.Matrix([P, Q, 0]).jacobian(variables)
            ).det()
        ),
        scale,
    )
    E6 = sp.expand(weighted.coeff_monomial(scale**6))
    unknowns = a + b + ell
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6, 6), unknowns
    )
    rows = matrix.T.rref()[1]
    columns = matrix.rref()[1]
    print(
        "general E6 rank/pivots/minor:",
        matrix.rank(),
        rows,
        columns,
        matrix.extract(rows, columns).det(),
    )
    print("general E6 compatibilities:")
    for value in nonzero_compatibilities(matrix, rhs):
        print(" ", value)


def nonzero_c_branch_data(label, D_value, w5_value):
    A, C, D, w0, w4, w5 = sp.symbols("A C D w0 w4 w5")
    U = 4 * C * x**2 * y + 4 * D_value * x**2 * z
    V = (
        A * x**3
        + C * y**2 * z
        + D_value * y * z**2
        + w5_value * x * z**2
    )
    W = w0 * p + w4 * q + w5_value * z**2
    a = sp.symbols(f"{label}a0:6")
    b = sp.symbols(f"{label}b0:6")
    ell = sp.symbols(f"{label}l0:9")
    H2 = sp.Matrix(
        [
            sum(c * monomial for c, monomial in zip(a, mon2)),
            sum(c * monomial for c, monomial in zip(b, mon2)),
            W,
        ]
    )
    L = sp.Matrix(3, 3, ell)
    weighted = sp.Poly(
        sp.expand(
            (
                L
                + scale * H2.jacobian(variables)
                + scale**2 * sp.Matrix([U, V, R]).jacobian(variables)
                + scale**3 * sp.Matrix([P, Q, 0]).jacobian(variables)
            ).det()
        ),
        scale,
    )
    unknowns = a + b + ell
    E6 = sp.expand(weighted.coeff_monomial(scale**6))
    matrix6, rhs6 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6, 6), unknowns
    )
    solution6 = next(iter(sp.linsolve((matrix6, rhs6), unknowns)))
    substitutions6 = dict(zip(unknowns, solution6))
    E5 = sp.expand(
        weighted.coeff_monomial(scale**5).subs(substitutions6)
    )
    remaining = tuple(
        unknown for unknown in unknowns if unknown in E5.free_symbols
    )
    matrix5, rhs5 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E5, 5), remaining
    )
    print(
        f"{label} E6 rank / E5 shape-rank:",
        matrix6.rank(),
        matrix5.shape,
        matrix5.rank(),
    )
    print(f"{label} E5 compatibilities:")
    for value in nonzero_compatibilities(matrix5, rhs5):
        print(" ", value)


def main():
    raw_e7_data()
    general_e6_data()
    nonzero_c_branch_data("c_only", 0, sp.symbols("w5"))
    nonzero_c_branch_data("both", sp.symbols("D"), 0)
    A, w0, w3, w4, w5 = sp.symbols("A w0 w3 w4 w5")
    U = 0
    V = A * x**3 + w3 * x * y**2 + w5 * x * z**2
    W = w0 * p + w3 * y**2 + w4 * q + w5 * z**2

    a = sp.symbols("a0:6")
    b = sp.symbols("b0:6")
    ell = sp.symbols("l0:9")
    H2 = sp.Matrix(
        [
            sum(c * monomial for c, monomial in zip(a, mon2)),
            sum(c * monomial for c, monomial in zip(b, mon2)),
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
    print("top:", [sp.factor(weighted.coeff_monomial(scale**k)) for k in (9, 8, 7)])

    unknowns6 = a + b + ell
    E6 = sp.expand(weighted.coeff_monomial(scale**6))
    matrix6, rhs6 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6, 6), unknowns6
    )
    print("E6 shape/rank/nullity:", matrix6.shape, matrix6.rank(), len(unknowns6) - matrix6.rank())
    compat6 = nonzero_compatibilities(matrix6, rhs6)
    print("E6 nonzero compatibilities:")
    for value in compat6:
        print(" ", value)
    solution6 = next(iter(sp.linsolve((matrix6, rhs6), unknowns6)))
    changed6 = [
        (unknown, sp.factor(value))
        for unknown, value in zip(unknowns6, solution6)
        if sp.expand(value - unknown) != 0
    ]
    print("E6 changed variables:")
    for item in changed6:
        print(" ", item)

    substitutions6 = dict(zip(unknowns6, solution6))
    E5 = sp.factor(
        sp.expand(weighted.coeff_monomial(scale**5).subs(substitutions6))
    )
    print("E5 coefficients:")
    for exponent, value in zip(
        homogeneous_exponents(5), homogeneous_coefficients(E5, 5)
    ):
        if value != 0:
            print(" ", exponent, sp.factor(value))
    remaining = tuple(
        unknown
        for unknown in unknowns6
        if unknown in E5.free_symbols
    )
    print("E5 remaining linear candidates:", remaining)
    matrix5, rhs5 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E5, 5), remaining
    )
    print("E5 shape/rank/nullity:", matrix5.shape, matrix5.rank(), len(remaining) - matrix5.rank())
    rows5 = matrix5.T.rref()[1]
    columns5 = matrix5.rref()[1]
    print(
        "E5 rows/columns/minor:",
        rows5,
        columns5,
        matrix5.extract(rows5, columns5).det(),
    )
    compat5 = nonzero_compatibilities(matrix5, rhs5)
    print("E5 nonzero compatibilities:")
    for value in compat5:
        print(" ", value)
    solution5 = next(iter(sp.linsolve((matrix5, rhs5), remaining)))
    changed5 = [
        (unknown, sp.factor(value))
        for unknown, value in zip(remaining, solution5)
        if sp.expand(value - unknown) != 0
    ]
    print("E5 changed variables:")
    for item in changed5:
        print(" ", item)


if __name__ == "__main__":
    main()
