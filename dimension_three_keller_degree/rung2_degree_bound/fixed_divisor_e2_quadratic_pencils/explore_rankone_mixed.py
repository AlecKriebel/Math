#!/usr/bin/env python3
"""Exact exploratory elimination for the rank-one, mixed e=2 orbit."""

from __future__ import annotations

import sympy as sp

x, y, z, scale = sp.symbols("x y z scale")
variables = (x, y, z)
p = x**2
q = y**2 + x * z
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


def nonzero_compatibilities(matrix, rhs):
    return [
        sp.factor((vector.T * rhs)[0])
        for vector in matrix.T.nullspace()
        if sp.expand((vector.T * rhs)[0]) != 0
    ]


def jac3(f, g, h):
    return sp.Matrix([f, g, h]).jacobian(variables).det()


def coefficient_column(direction):
    U, V, W = direction
    return sp.Matrix(
        [sp.Poly(U, *variables).coeff_monomial(monomial) for monomial in mon3]
        + [sp.Poly(V, *variables).coeff_monomial(monomial) for monomial in mon3]
        + [sp.Poly(W, *variables).coeff_monomial(monomial) for monomial in mon2]
    )


def raw_e7():
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
    print(
        "raw E7 rank/minor:",
        matrix.rank(),
        rows,
        columns,
        matrix.extract(rows, columns).det(),
    )
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
        (4 * x**2 * y, y * q, 0),
        (4 * x**2 * z, z * q, 0),
        (0, 0, x**2),
        (0, x**2 * z, x * z),
        (0, -x**2 * z, y**2),
        (0, x * y * z, y * z),
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


def weighted_data(U, V, W, prefix):
    a = sp.symbols(f"{prefix}a0:6")
    b = sp.symbols(f"{prefix}b0:6")
    ell = sp.symbols(f"{prefix}l0:9")
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
    return weighted, a, b, ell, L


def general_e6():
    C, D, w0, w2, w3, w4, w5 = sp.symbols(
        "C D w0 w2 w3 w4 w5"
    )
    U = 4 * C * x**2 * y + 4 * D * x**2 * z
    V = (
        C * y * q
        + D * z * q
        + (w2 - w3) * x**2 * z
        + w4 * x * y * z
        + w5 * x * z**2
    )
    W = w0 * p + w2 * x * z + w3 * y**2 + w4 * y * z + w5 * z**2
    weighted, a, b, ell, _ = weighted_data(U, V, W, "g")
    unknowns = a + b + ell
    E6 = sp.expand(weighted.coeff_monomial(scale**6))
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6, 6), unknowns
    )
    rows = matrix.T.rref()[1]
    columns = matrix.rref()[1]
    print(
        "general E6 rank/minor:",
        matrix.rank(),
        rows,
        columns,
        matrix.extract(rows, columns).det(),
    )
    print("general E6 compatibilities:")
    for value in nonzero_compatibilities(matrix, rhs):
        print(" ", value)


def branch(label, substitutions):
    C, D, w0, w2, w3, w4, w5 = sp.symbols(
        "C D w0 w2 w3 w4 w5"
    )
    U = (4 * C * x**2 * y + 4 * D * x**2 * z).subs(substitutions)
    V = (
        C * y * q
        + D * z * q
        + (w2 - w3) * x**2 * z
        + w4 * x * y * z
        + w5 * x * z**2
    ).subs(substitutions)
    W = (
        w0 * p + w2 * x * z + w3 * y**2 + w4 * y * z + w5 * z**2
    ).subs(substitutions)
    weighted, a, b, ell, L = weighted_data(U, V, W, label)
    unknowns = a + b + ell
    E6 = sp.expand(weighted.coeff_monomial(scale**6))
    matrix6, rhs6 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6, 6), unknowns
    )
    compat6 = nonzero_compatibilities(matrix6, rhs6)
    print(label, "E6 rank/compat:", matrix6.rank(), compat6)
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
    compat5 = nonzero_compatibilities(matrix5, rhs5)
    print(
        label,
        "E5 remaining/shape/rank:",
        remaining,
        matrix5.shape,
        matrix5.rank(),
    )
    if matrix5.rank():
        rows5 = matrix5.T.rref()[1]
        columns5 = matrix5.rref()[1]
        print(
            label,
            "E5 pivot rows/columns/minor:",
            rows5,
            columns5,
            sp.factor(matrix5.extract(rows5, columns5).det()),
        )
    print(label, "E5 compatibilities:")
    left_vectors = matrix5.T.nullspace()
    nonzero_index = 0
    for vector in left_vectors:
        value = sp.factor((vector.T * rhs5)[0])
        if value == 0:
            continue
        denominators = [
            sp.factor(sp.together(entry).as_numer_denom()[1])
            for entry in vector
            if entry != 0
        ]
        print(
            " ",
            value,
            "vector_den_lcm=",
            sp.factor(sp.lcm(denominators)) if denominators else 1,
        )
        nonzero_index += 1
    if compat5:
        return
    solution5 = next(iter(sp.linsolve((matrix5, rhs5), remaining)))
    substitutions5 = substitutions6 | dict(zip(remaining, solution5))
    print(
        label,
        "E5 changed:",
        [
            (unknown, sp.factor(value))
            for unknown, value in zip(remaining, solution5)
            if sp.expand(value - unknown) != 0
        ],
    )
    print(label, "L after E5:")
    print(sp.simplify(L.subs(substitutions5)))
    print(label, "det L:", sp.factor(L.det().subs(substitutions5)))
    E4 = sp.expand(
        weighted.coeff_monomial(scale**4).subs(substitutions5)
    )
    remaining4 = tuple(
        unknown for unknown in unknowns if unknown in E4.free_symbols
    )
    try:
        matrix4, rhs4 = sp.linear_eq_to_matrix(
            homogeneous_coefficients(E4, 4), remaining4
        )
    except Exception:
        print(label, "E4 nonlinear coefficients:")
        for exponent, value in zip(
            homogeneous_exponents(4), homogeneous_coefficients(E4, 4)
        ):
            if value != 0:
                print(" ", exponent, sp.factor(value))
        return
    print(
        label,
        "E4 remaining/shape/rank:",
        remaining4,
        matrix4.shape,
        matrix4.rank(),
    )
    print(label, "E4 compatibilities:")
    for value in nonzero_compatibilities(matrix4, rhs4):
        print(" ", value)


def main():
    C, D, w2, w3, w4, w5 = sp.symbols("C D w2 w3 w4 w5")
    raw_e7()
    general_e6()
    # Compatibility branches:
    # D*w5=0 and C*w5+D*w4=0.
    branch("d_nonzero_w4w5_zero", {w4: 0, w5: 0})
    branch("d_zero_c_nonzero", {D: 0, w5: 0})
    branch("d_zero_c_w4_eq_c", {D: 0, w5: 0, w4: C})
    branch("c_d_zero", {C: 0, D: 0})
    branch("c_d_w4_zero", {C: 0, D: 0, w4: 0})
    branch("c_d_w4w5_zero", {C: 0, D: 0, w4: 0, w5: 0})
    branch(
        "c_d_w4w5_d_zero",
        {C: 0, D: 0, w4: 0, w5: 0, w2: w3},
    )


if __name__ == "__main__":
    main()
