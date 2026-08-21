#!/usr/bin/env python3
"""Exploration of the rank-two fixed-divisor triple companion."""

from __future__ import annotations

import sympy as sp

x, y, z, scale = sp.symbols("x y z scale")
variables = (x, y, z)
p, q = x**2, y * z
P, Q, R = p**2, p * q, x**3
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


def coefficient_column(direction):
    U, V, W = direction
    return sp.Matrix(
        [sp.Poly(U, *variables).coeff_monomial(m) for m in mon3]
        + [sp.Poly(V, *variables).coeff_monomial(m) for m in mon3]
        + [sp.Poly(W, *variables).coeff_monomial(m) for m in mon2]
    )


def nonzero_pairs(matrix, rhs):
    return [
        (vector, sp.factor((vector.T * rhs)[0]))
        for vector in matrix.T.nullspace()
        if sp.expand((vector.T * rhs)[0]) != 0
    ]


def weighted_data(U, V, W, prefix):
    a = sp.symbols(f"{prefix}a0:6")
    b = sp.symbols(f"{prefix}b0:6")
    ell = sp.symbols(f"{prefix}l0:9")
    H2 = sp.Matrix(
        [
            sum(c * m for c, m in zip(a, mon2)),
            sum(c * m for c, m in zip(b, mon2)),
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
    return weighted, a, b, ell, L


def raw():
    u = sp.symbols("u0:10")
    v = sp.symbols("v0:10")
    w = sp.symbols("w0:6")
    U0 = sum(c * m for c, m in zip(u, mon3))
    V0 = sum(c * m for c, m in zip(v, mon3))
    W0 = sum(c * m for c, m in zip(w, mon2))
    E7 = sp.expand(
        jac3(P, Q, W0) + jac3(P, V0, R) + jac3(U0, Q, R)
    )
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E7, 7), u + v + w
    )
    rows, columns = matrix.T.rref()[1], matrix.rref()[1]
    print(
        "raw rank/minor:",
        matrix.rank(),
        rows,
        columns,
        matrix.extract(rows, columns).det(),
    )

    translations = tuple(
        tuple(sp.diff(component, variable) for component in (P, Q, R))
        for variable in variables
    )
    w1, w2, w3, w4, w5, A = sp.symbols("w1 w2 w3 w4 w5 A")
    directions = (
        (R, 0, 0),
        (0, R, 0),
        translations[0],
        translations[1],
        translations[2],
        (sp.Rational(4, 3) * x**2 * y, 0, x * y),
        (sp.Rational(4, 3) * x**2 * z, 0, x * z),
        (sp.Rational(4, 3) * x * y**2, 0, y**2),
        (0, 0, y * z),
        (sp.Rational(4, 3) * x * z**2, 0, z**2),
        (x * y * z, 0, 0),
        (0, x * y**2, 0),
        (0, x * y * z, 0),
        (0, x * z**2, 0),
        (0, y**3, 0),
        (0, y**2 * z, 0),
        (0, y * z**2, 0),
        (0, z**3, 0),
    )
    kernel = sp.Matrix.hstack(
        *(coefficient_column(direction) for direction in directions)
    )
    kernel_rows = kernel.T.rref()[1]
    print(
        "kernel rank/rows/minor/check:",
        kernel.rank(),
        kernel_rows,
        kernel.extract(kernel_rows, range(18)).det(),
        matrix * kernel == sp.zeros(36, 18),
    )


def lower():
    A = sp.symbols("A")
    w1, w2, w3, w4, w5 = sp.symbols("w1:6")
    B1, B2, B3, B4, B5, B6, B7 = sp.symbols("B1:8")
    U = A * x * y * z + sp.Rational(4, 3) * (
        w1 * x**2 * y
        + w2 * x**2 * z
        + w3 * x * y**2
        + w5 * x * z**2
    )
    V = (
        B1 * x * y**2
        + B2 * x * y * z
        + B3 * x * z**2
        + B4 * y**3
        + B5 * y**2 * z
        + B6 * y * z**2
        + B7 * z**3
    )
    W = w1 * x * y + w2 * x * z + w3 * y**2 + w4 * y * z + w5 * z**2
    a = sp.symbols("a0:6")
    b = sp.symbols("b0:6")
    ell = sp.symbols("l0:9")
    H2 = sp.Matrix(
        [
            sum(c * m for c, m in zip(a, mon2)),
            sum(c * m for c, m in zip(b, mon2)),
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
    print(
        "top:",
        [sp.factor(weighted.coeff_monomial(scale**k)) for k in (9, 8, 7)],
    )
    unknowns = a + b + ell
    E6 = sp.expand(weighted.coeff_monomial(scale**6))
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6, 6), unknowns
    )
    rows, columns = matrix.T.rref()[1], matrix.rref()[1]
    print(
        "E6 rank/minor:",
        matrix.rank(),
        rows,
        columns,
        sp.factor(matrix.extract(rows, columns).det()),
    )
    print("E6 compatibility:")
    for vector, value in nonzero_pairs(matrix, rhs):
        denominators = [
            sp.factor(sp.together(entry).as_numer_denom()[1])
            for entry in vector
            if entry != 0
        ]
        print(
            " ",
            value,
            "den=",
            sp.factor(sp.lcm(denominators)) if denominators else 1,
        )


def branch(label, U, V, W):
    weighted, a, b, ell, L = weighted_data(U, V, W, label)
    unknowns = a + b + ell
    E6 = sp.expand(weighted.coeff_monomial(scale**6))
    matrix6, rhs6 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6, 6), unknowns
    )
    compat6 = nonzero_pairs(matrix6, rhs6)
    print(label, "E6 rank/compat:", matrix6.rank(), [v for _, v in compat6])
    if compat6:
        return
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
        label,
        "E5 remaining/shape/rank:",
        remaining,
        matrix5.shape,
        matrix5.rank(),
    )
    rows, columns = matrix5.T.rref()[1], matrix5.rref()[1]
    if rows and columns:
        print(
            label,
            "E5 pivots/minor:",
            rows,
            columns,
            sp.factor(matrix5.extract(rows, columns).det()),
        )
    print(label, "E5 compat:")
    for vector, value in nonzero_pairs(matrix5, rhs5):
        denominators = [
            sp.factor(sp.together(entry).as_numer_denom()[1])
            for entry in vector
            if entry != 0
        ]
        print(
            " ",
            value,
            "den=",
            sp.factor(sp.lcm(denominators)) if denominators else 1,
        )


def deep_branch(label, U, V, W):
    weighted, a, b, ell, L = weighted_data(U, V, W, label)
    unknowns = a + b + ell
    substitutions = {}
    for degree in (6, 5):
        identity = sp.expand(
            weighted.coeff_monomial(scale**degree).subs(substitutions)
        )
        remaining = tuple(
            unknown for unknown in unknowns if unknown in identity.free_symbols
        )
        matrix, rhs = sp.linear_eq_to_matrix(
            homogeneous_coefficients(identity, degree), remaining
        )
        print(
            label,
            f"E{degree} remaining/shape/rank:",
            remaining,
            matrix.shape,
            matrix.rank(),
        )
        pairs = nonzero_pairs(matrix, rhs)
        print(label, f"E{degree} compat:", [value for _, value in pairs])
        if pairs:
            return
        solution = next(iter(sp.linsolve((matrix, rhs), remaining)))
        substitutions |= dict(zip(remaining, solution))
        print(
            label,
            f"E{degree} changed:",
            [
                (unknown, sp.factor(value))
                for unknown, value in zip(remaining, solution)
                if sp.expand(value - unknown) != 0
            ],
        )
    print(label, "L/det after E5:", L.subs(substitutions), sp.factor(L.det().subs(substitutions)))
    E4 = sp.expand(
        weighted.coeff_monomial(scale**4).subs(substitutions)
    )
    print(label, "E4 nonzero coefficients:")
    for exponent, value in zip(
        homogeneous_exponents(4), homogeneous_coefficients(E4, 4)
    ):
        if value != 0:
            print(" ", exponent, sp.factor(value))
def branches():
    A, K = sp.symbols("A K")
    w1, w2 = sp.symbols("w1 w2")
    B1, B2, B3, B4, B5, B6, B7 = sp.symbols("B1:8")

    w4_open = (9 * A - K) / 12
    M_open = (9 * A - 2 * K) / 3
    U_open = A * x * y * z + sp.Rational(4, 3) * (
        w1 * x**2 * y + w2 * x**2 * z
    )
    V_open = (
        B1 * x * y**2
        + B2 * x * y * z
        + B3 * x * z**2
        - M_open * w1 / K * y**2 * z
        - M_open * w2 / K * y * z**2
    )
    W_open = w1 * x * y + w2 * x * z + w4_open * y * z
    branch("k_open", U_open, V_open, W_open)

    U_k0 = A * x * y * z
    V_k0 = (
        B1 * x * y**2
        + B2 * x * y * z
        + B3 * x * z**2
        + B4 * y**3
        + B5 * y**2 * z
        + B6 * y * z**2
        + B7 * z**3
    )
    W_k0 = sp.Rational(3, 4) * A * y * z
    branch("k0_a_open", U_k0, V_k0, W_k0)

    U_origin = sp.Rational(4, 3) * (
        w1 * x**2 * y + w2 * x**2 * z
    )
    V_origin = (
        B1 * x * y**2
        + B2 * x * y * z
        + B3 * x * z**2
        + B4 * y**3
        + B5 * y**2 * z
        + B6 * y * z**2
        + B7 * z**3
    )
    W_origin = w1 * x * y + w2 * x * z
    branch("k_a_zero", U_origin, V_origin, W_origin)

    A0, B0, w0 = sp.symbols("A0 B0 w0")
    deep_branch(
        "aligned",
        A0 * x * y * z,
        B0 * x * y * z,
        w0 * y * z,
    )

    Ar, Br1, Br2, Br3 = sp.symbols("Ar Br1 Br2 Br3")
    deep_branch(
        "res_2",
        Ar * x * y * z,
        Br1 * x * y**2 + Br2 * x * y * z + Br3 * x * z**2,
        sp.Rational(3, 8) * Ar * y * z,
    )
    deep_branch(
        "res_1",
        Ar * x * y * z,
        Br1 * x * y**2 + Br2 * x * y * z + Br3 * x * z**2,
        0,
    )
    deep_branch(
        "aligned_k0",
        Ar * x * y * z,
        Br2 * x * y * z,
        sp.Rational(3, 4) * Ar * y * z,
    )

    s0, r0, C0 = sp.symbols("s0 r0 C0")
    O1, O2, O3 = sp.symbols("O1 O2 O3")
    deep_branch(
        "origin_wopen",
        sp.Rational(4, 3) * s0 * (x**2 * y + r0 * x**2 * z),
        (
            O1 * x * y**2
            + O2 * x * y * z
            + O3 * x * z**2
            + C0 * y**3
            + (3 * C0 * r0 + sp.Rational(2, 3) * s0) * y**2 * z
            + (
                3 * C0 * r0**2
                + sp.Rational(2, 3) * r0 * s0
            )
            * y
            * z**2
            + C0 * r0**3 * z**3
        ),
        s0 * x * y + r0 * s0 * x * z,
    )
    deep_branch(
        "origin_wopen_r0",
        sp.Rational(4, 3) * s0 * x**2 * y,
        (
            O1 * x * y**2
            + O2 * x * y * z
            + O3 * x * z**2
            + C0 * y**3
            + sp.Rational(2, 3) * s0 * y**2 * z
        ),
        s0 * x * y,
    )
    deep_branch(
        "origin_wopen_c0",
        sp.Rational(4, 3) * s0 * (x**2 * y + r0 * x**2 * z),
        (
            O1 * x * y**2
            + O2 * x * y * z
            + O3 * x * z**2
            + sp.Rational(2, 3) * s0 * y**2 * z
            + sp.Rational(2, 3) * r0 * s0 * y * z**2
        ),
        s0 * x * y + r0 * s0 * x * z,
    )
    deep_branch(
        "origin_wopen_c0r0",
        sp.Rational(4, 3) * s0 * x**2 * y,
        (
            O1 * x * y**2
            + O2 * x * y * z
            + O3 * x * z**2
            + sp.Rational(2, 3) * s0 * y**2 * z
        ),
        s0 * x * y,
    )

    Z1, Z2, Z3, Z4, Z5, Z6, Z7 = sp.symbols("Z1:8")
    deep_branch(
        "origin_zero",
        0,
        (
            Z1 * x * y**2
            + Z2 * x * y * z
            + Z3 * x * z**2
            + Z4 * y**3
            + Z5 * y**2 * z
            + Z6 * y * z**2
            + Z7 * z**3
        ),
        0,
    )


if __name__ == "__main__":
    raw()
    lower()
    branches()
