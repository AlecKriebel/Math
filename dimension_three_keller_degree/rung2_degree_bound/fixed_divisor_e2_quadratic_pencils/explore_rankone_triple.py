#!/usr/bin/env python3
"""Exploration of the rank-one fixed-divisor triple companion."""

from __future__ import annotations

import sympy as sp

x, y, z, scale = sp.symbols("x y z scale")
variables = (x, y, z)
p, q = x**2, y**2 + x * z
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
    normals = (
        (x * q, 0, 0),
        (sp.Rational(4, 3) * x**2 * y, 0, x * y),
        (sp.Rational(4, 3) * x**2 * z, 0, x * z),
        (sp.Rational(4, 3) * x * y**2, 0, y**2),
        (sp.Rational(4, 3) * x * y * z, 0, y * z),
        (sp.Rational(4, 3) * x * z**2, 0, z**2),
        (0, x**2 * z, 0),
        (0, x * y**2, 0),
        (0, x * y * z, 0),
        (0, x * z**2, 0),
        (0, y**3, 0),
        (0, y**2 * z, 0),
        (0, y * z**2, 0),
        (0, z**3, 0),
    )
    directions = (
        (R, 0, 0),
        (0, R, 0),
        translations[0],
        translations[1],
    ) + normals
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
    print(
        "translation z equals target shear:",
        coefficient_column(translations[2])
        == coefficient_column((0, R, 0)),
    )


def lower():
    A = sp.symbols("A")
    w1, w2, w3, w4, w5 = sp.symbols("w1:6")
    C0, C1, C2, C3, C4, C5, C6, C7 = sp.symbols("C0:8")
    W = w1 * x * y + w2 * x * z + w3 * y**2 + w4 * y * z + w5 * z**2
    U = A * x * q + sp.Rational(4, 3) * x * W
    V = (
        C0 * x**2 * z
        + C1 * x * y**2
        + C2 * x * y * z
        + C3 * x * z**2
        + C4 * y**3
        + C5 * y**2 * z
        + C6 * y * z**2
        + C7 * z**3
    )
    weighted, a, b, ell, L = weighted_data(U, V, W, "g")
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
    pairs6 = nonzero_pairs(matrix6, rhs6)
    print(label, "E6 rank/compat:", matrix6.rank(), [v for _, v in pairs6])
    if pairs6:
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
    if label == "a_open":
        print(label, "E5 literal coefficients:")
        for exponent, value in zip(
            homogeneous_exponents(5), homogeneous_coefficients(E5, 5)
        ):
            if value != 0:
                print(" ", exponent, sp.factor(value))
        return
    rows, columns = matrix5.T.rref()[1], matrix5.rref()[1]
    if rows and columns:
        print(
            label,
            "E5 pivots/minor:",
            rows,
            columns,
            sp.factor(matrix5.extract(rows, columns).det()),
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
        pairs = nonzero_pairs(matrix, rhs)
        print(
            label,
            f"E{degree} remaining/rank/compat:",
            remaining,
            matrix.rank(),
            [value for _, value in pairs],
        )
        if pairs:
            return
        solution = next(iter(sp.linsolve((matrix, rhs), remaining)))
        solution_map = dict(zip(remaining, solution))
        substitutions |= solution_map
        print(
            label,
            f"E{degree} changed:",
            [
                (unknown, sp.factor(value))
                for unknown, value in zip(remaining, solution)
                if sp.expand(value - unknown) != 0
            ],
        )
    print(
        label,
        "L/det after E5:",
        L.subs(substitutions),
        sp.factor(L.det().subs(substitutions)),
    )
    E4 = sp.expand(
        weighted.coeff_monomial(scale**4).subs(substitutions)
    )
    print(label, "E4 nonzero coefficients:")
    for exponent, value in zip(
        homogeneous_exponents(4), homogeneous_coefficients(E4, 4)
    ):
        if value != 0:
            print(" ", exponent, sp.factor(value))


def a0_w3_generic_lower():
    """Continue the localized s*(C0-C1) != 0 branch through E3."""
    s, C0, C1 = sp.symbols("s C0 C1")
    U = sp.Rational(4, 3) * s * x * q
    V = C0 * x**2 * z + C1 * x * y**2
    W = s * q
    weighted, a, b, ell, L = weighted_data(U, V, W, "sg")
    d = C0 - C1
    substitutions = {
        a[1]: 0,
        a[2]: ell[2] / d + sp.Rational(4, 3) * s * d,
        a[4]: 0,
        a[5]: 0,
        a[3]: ell[2] / d,
        ell[1]: 0,
        ell[7]: 0,
        ell[8]: s * d,
        b[1]: 0,
        b[3]: b[2] - C1 * d,
        b[4]: 0,
        b[5]: 0,
    }
    for degree in (6, 5, 4):
        residual = sp.expand(
            weighted.coeff_monomial(scale**degree).subs(substitutions)
        )
        print(
            "a0_w3_generic_manual",
            f"E{degree} zero:",
            residual == 0,
        )
        if degree == 5 and residual != 0:
            print(
                "a0_w3_generic_manual E5 residual:",
                [
                    (e, sp.factor(c))
                    for e, c in zip(
                        homogeneous_exponents(5),
                        homogeneous_coefficients(residual, 5),
                    )
                    if c != 0
                ],
            )
    residual = sp.expand(
        weighted.coeff_monomial(scale**3).subs(substitutions)
    )
    print("a0_w3_generic_manual E3:")
    for exponent, value in zip(
        homogeneous_exponents(3), homogeneous_coefficients(residual, 3)
    ):
        if value != 0:
            print(" ", exponent, sp.factor(value))
    print(
        "a0_w3_generic_manual det:",
        sp.factor(L.det().subs(substitutions)),
    )


def branches():
    A = sp.symbols("A")
    w1, w2, w3 = sp.symbols("w1 w2 w3")
    C0, C1, C2, C3, C4, C5, C6, C7 = sp.symbols("C0:8")

    W_open = w1 * x * y + w2 * x * z + w3 * y**2
    U_open = A * x * q + sp.Rational(4, 3) * x * W_open
    V_open = (
        C0 * x**2 * z
        + C1 * x * y**2
        + C2 * x * y * z
        + C3 * x * z**2
        + w1 * (3 * A - 4 * w3) / (9 * A) * y**3
        + (w2 - w3) * (3 * A - 4 * w3) / (9 * A) * y**2 * z
    )
    branch("a_open", U_open, V_open, W_open)

    s = sp.symbols("s")
    W_res = s * q
    U_res = sp.Rational(4, 3) * s * x * q
    V_all = (
        C0 * x**2 * z
        + C1 * x * y**2
        + C2 * x * y * z
        + C3 * x * z**2
        + C4 * y**3
        + C5 * y**2 * z
        + C6 * y * z**2
        + C7 * z**3
    )
    branch("a0_w3_open", U_res, V_all, W_res)

    W_origin = w1 * x * y + w2 * x * z
    U_origin = sp.Rational(4, 3) * x * W_origin
    branch("a_w3_zero", U_origin, V_all, W_origin)

    deep_branch(
        "a0_w3_reduced",
        sp.Rational(4, 3) * s * x * q,
        C0 * x**2 * z + C1 * x * y**2,
        s * q,
    )
    C = sp.symbols("C")
    deep_branch(
        "a0_w3_equal",
        sp.Rational(4, 3) * s * x * q,
        C * x * q,
        s * q,
    )

    deep_branch(
        "origin_zero",
        0,
        V_all,
        0,
    )
    r = sp.symbols("r")
    deep_branch(
        "a0_w3zero_w1zero",
        sp.Rational(4, 3) * r * x**2 * z,
        V_all - C4 * y**3,
        r * x * z,
    )
    deep_branch(
        "a0_w3zero_w2zero",
        sp.Rational(4, 3) * r * x**2 * y,
        V_all - C5 * y**2 * z - C6 * y * z**2 - C7 * z**3,
        r * x * y,
    )
    deep_branch(
        "a0_w3zero_w2zero_c3zero",
        sp.Rational(4, 3) * r * x**2 * y,
        (
            C0 * x**2 * z
            + C1 * x * y**2
            + C2 * x * y * z
            + C4 * y**3
        ),
        r * x * y,
    )
    t, k = sp.symbols("t k")
    V_w12_generic = (
        C0 * x**2 * z
        + C1 * x * y**2
        + C2 * x * y * z
        + C3 * x * z**2
        + k * y**3
        + (3 * k - sp.Rational(4, 3) * r) * t * y**2 * z
        + (3 * k - 2 * r) * t**2 * y * z**2
        + (k - sp.Rational(2, 3) * r) * t**3 * z**3
    )
    deep_branch(
        "a0_w3zero_w12_generic",
        sp.Rational(4, 3) * r * x**2 * (y + t * z),
        V_w12_generic,
        r * x * (y + t * z),
    )
    deep_branch(
        "a0_w3zero_w12_resonance",
        sp.Rational(4, 3) * r * x**2 * (y + t * z),
        V_w12_generic.subs(k, sp.Rational(2, 3) * r),
        r * x * (y + t * z),
    )
    deep_branch(
        "a_nonzero_wzero_c3",
        A * x * q,
        C0 * x**2 * z + C1 * x * y**2 + C3 * x * z**2,
        0,
    )
    deep_branch(
        "a_nonzero_wzero_aligned",
        A * x * q,
        C0 * x**2 * z + C1 * x * y**2,
        0,
    )
    a0_w3_generic_lower()


if __name__ == "__main__":
    raw()
    lower()
    branches()
