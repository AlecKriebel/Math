#!/usr/bin/env python3
"""Exact branch-tree certificate for the marked triple-companion orbit."""

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


def coefficient(value, monomial):
    return sp.Poly(sp.expand(value), *variables).coeff_monomial(monomial)


def weighted_determinant(U, V, W):
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
    determinant = sp.Poly(
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
    return determinant, a, b, ell, L


def solve_linear(identity, degree, unknowns):
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(identity, degree), unknowns
    )
    solution = next(iter(sp.linsolve((matrix, rhs), unknowns)))
    return matrix, rhs, solution


def raw_e7_certificate():
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
    assert exact_zero(jac3(P, Q, R))
    assert matrix.shape == (36, 26)
    assert rhs == sp.zeros(36, 1)
    assert matrix.rank() == 8
    rows = (2, 4, 5, 7, 8, 9, 11, 13)
    columns = (1, 2, 4, 5, 6, 7, 8, 9)
    assert matrix.extract(rows, columns).det() == 483729408

    translations = tuple(
        tuple(sp.diff(component, variable) for component in (P, Q, R))
        for variable in variables
    )
    directions = (
        (x**3, 0, 0),
        (0, x**3, 0),
        translations[0],
        translations[1],
        translations[2],
        (x * q, 0, 0),
        (sp.Rational(4, 3) * x**2 * y, 0, x * y),
        (sp.Rational(4, 3) * x**2 * z, 0, x * z),
        (-sp.Rational(4, 3) * x**2 * z, 0, y**2),
        (sp.Rational(4, 3) * x * y * z, 0, y * z),
        (sp.Rational(4, 3) * x * z**2, 0, z**2),
        (0, x**2 * y, 0),
        (0, x**2 * z, 0),
        (0, x * y * z, 0),
        (0, x * z**2, 0),
        (0, y**2 * z, 0),
        (0, y * z**2, 0),
        (0, z**3, 0),
    )
    kernel = sp.Matrix.hstack(
        *(coefficient_column(direction) for direction in directions)
    )
    assert matrix * kernel == sp.zeros(36, 18)
    assert kernel.rank() == 18
    kernel_rows = (
        0, 1, 2, 3, 4, 5, 10, 11, 12,
        13, 14, 15, 16, 17, 18, 19, 20, 22,
    )
    assert kernel.extract(kernel_rows, range(18)).det() == -sp.Rational(
        2048, 27
    )
    assert matrix.cols - matrix.rank() == kernel.cols
    print(
        "PASS raw E7: rank 8, complete 18-dimensional kernel, "
        "five legal gauge directions"
    )


def general_e6_compatibility():
    A = sp.symbols("A")
    w1, w2, w3, w4, w5 = sp.symbols("w1:6")
    B = sp.symbols("B1:8")
    U = A * x * q + sp.Rational(4, 3) * (
        w1 * x**2 * y
        + (w2 - w3) * x**2 * z
        + w4 * x * y * z
        + w5 * x * z**2
    )
    V = (
        B[0] * x**2 * y
        + B[1] * x**2 * z
        + B[2] * x * y * z
        + B[3] * x * z**2
        + B[4] * y**2 * z
        + B[5] * y * z**2
        + B[6] * z**3
    )
    W = w1 * x * y + w2 * x * z + w3 * y**2 + w4 * y * z + w5 * z**2
    weighted, a, b, ell, _ = weighted_determinant(U, V, W)
    assert exact_zero(weighted.coeff_monomial(scale**8))
    assert exact_zero(weighted.coeff_monomial(scale**7))
    E6 = sp.expand(weighted.coeff_monomial(scale**6))
    constrained = a + b + ell[7:]
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6, 6), constrained
    )
    assert matrix.shape == (28, 14)
    assert matrix.rank() == 4
    assert matrix.extract((2, 4, 5, 8), (1, 2, 4, 5)).det() == 10368
    compat = [
        sp.factor((vector.T * rhs)[0])
        for vector in matrix.T.nullspace()
        if not exact_zero((vector.T * rhs)[0])
    ]
    difference = w2 - w3
    K = 4 * w3 - 3 * A
    assert has_associate(compat, -sp.Rational(32, 3) * w5**2)
    assert has_associate(
        compat, -sp.Rational(8, 3) * (3 * A * w5 + 2 * w4**2)
    )
    assert has_associate(compat, -4 * A * w4)
    assert has_associate(
        compat, -sp.Rational(4, 3) * (3 * A * difference + 4 * w1 * w4)
    )
    assert has_associate(compat, -B[0] * K)
    assert has_associate(compat, -4 * K * (B[3] - B[4]))
    assert has_associate(compat, 3 * (K * B[5] + 2 * A * w1))
    assert has_associate(compat, 2 * (-K * B[5] + 3 * A * w1))

    # Prove sufficiency as well as necessity: after w4=w5=0, every
    # left-kernel compatibility polynomial reduces to zero modulo exactly
    # the eight displayed generators.
    generators = (
        A * w1,
        A * difference,
        K * B[0],
        K * B[1],
        K * B[2],
        K * (B[3] - B[4]),
        K * B[5],
        K * B[6],
    )
    groebner = sp.groebner(
        generators, *B, w1, w2, A, w3, order="grevlex"
    )
    for polynomial in compat:
        reduced = sp.together(
            polynomial.subs({w4: 0, w5: 0})
        ).as_numer_denom()[0]
        assert exact_zero(groebner.reduce(reduced)[1])
    print(
        "PASS E6 compatibility: w4=w5=0 and exact A/K branch ideal"
    )


def open_branch_extra_compatibility():
    C, w1, difference, w = sp.symbols("C w1 difference w")
    U = sp.Rational(4, 3) * (
        w1 * x**2 * y + difference * x**2 * z
    )
    V = C * z * q
    W = w1 * x * y + (difference + w) * x * z + w * y**2
    weighted, a, b, ell, _ = weighted_determinant(U, V, W)
    E6 = sp.expand(weighted.coeff_monomial(scale**6))
    constrained = a + b + ell[7:]
    matrix6, rhs6, solution6 = solve_linear(E6, 6, constrained)
    substitutions6 = dict(zip(constrained, solution6))
    assert exact_zero(E6.subs(substitutions6))
    E5 = sp.expand(
        weighted.coeff_monomial(scale**5).subs(substitutions6)
    )
    free = tuple(symbol for symbol in constrained if symbol not in substitutions6)
    # `solution6` retains free symbols as themselves, so use every lower
    # coefficient not genuinely changed.
    changed = {
        symbol: value
        for symbol, value in substitutions6.items()
        if not exact_zero(symbol - value)
    }
    free = tuple(symbol for symbol in constrained if symbol not in changed)
    matrix5, rhs5 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E5, 5), free
    )
    compat = [
        sp.factor((vector.T * rhs5)[0])
        for vector in matrix5.T.nullspace()
        if not exact_zero((vector.T * rhs5)[0])
    ]
    assert has_associate(compat, -sp.Rational(8, 9) * w1**3)
    assert has_associate(
        compat, sp.Rational(16, 9) * difference**3
    )
    print("PASS open K branch: A=0 leaf forces w1=difference=0")


def reduced_open_branch():
    A, C, w = sp.symbols("A C w")
    weighted, a, b, ell, L = weighted_determinant(
        A * x * q, C * z * q, w * q
    )
    all_lower = a + b + ell
    matrix6, rhs6, solution6 = solve_linear(
        sp.expand(weighted.coeff_monomial(scale**6)), 6, all_lower
    )
    substitutions6 = {
        symbol: value
        for symbol, value in zip(all_lower, solution6)
        if not exact_zero(symbol - value)
    }
    expected6 = {
        a[1]: sp.Rational(4, 3) * ell[7],
        a[2]: a[3] + sp.Rational(4, 3) * ell[8]
        + A * C / 2 - sp.Rational(2, 3) * C * w,
        a[4]: 0,
        a[5]: 0,
    }
    assert all(
        exact_zero(substitutions6[key] - value)
        for key, value in expected6.items()
    )
    assert exact_zero(
        weighted.coeff_monomial(scale**6).subs(substitutions6)
    )

    E5 = sp.expand(
        weighted.coeff_monomial(scale**5).subs(substitutions6)
    )
    free5 = tuple(symbol for symbol in all_lower if symbol not in substitutions6)
    matrix5, _, solution5 = solve_linear(E5, 5, free5)
    K = 4 * w - 3 * A
    generic_e5_minor = sp.factor(
        matrix5.extract(
            (0, 1, 2, 3, 4, 5, 6, 8),
            (1, 3, 4, 6, 7, 9, 15, 16),
        ).det()
    )
    generic_e5_unit = sp.factor(generic_e5_minor / (C * A**2 * K**4))
    assert generic_e5_unit.is_Rational and generic_e5_unit != 0
    substitutions5 = {
        symbol: value
        for symbol, value in zip(free5, solution5)
        if not exact_zero(symbol - value)
    }
    # This chart is localized at A*C*K != 0.
    expected5 = {
        a[3]: 2 * ell[2] / C,
        b[1]: 0,
        b[2]: b[3],
        b[4]: 0,
        b[5]: C**2 / 4,
        ell[1]: 0,
        ell[7]: 0,
        ell[8]: C * w / 2,
    }
    assert all(
        exact_zero(substitutions5[key] - value)
        for key, value in expected5.items()
    )
    combined5 = substitutions6 | substitutions5
    assert exact_zero(weighted.coeff_monomial(scale**5).subs(combined5))

    E4 = sp.expand(
        weighted.coeff_monomial(scale**4).subs(combined5)
    )
    free4 = tuple(
        symbol for symbol in all_lower if symbol not in combined5
    )
    matrix4, _, solution4 = solve_linear(E4, 4, free4)
    generic_e4_minor = sp.factor(
        matrix4.extract((0, 1), (2, 6)).det()
    )
    generic_e4_unit = sp.factor(generic_e4_minor / (C * K**2))
    assert generic_e4_unit.is_Rational and generic_e4_unit != 0
    substitutions4 = {
        symbol: value
        for symbol, value in zip(free4, solution4)
        if not exact_zero(symbol - value)
    }
    assert exact_zero(substitutions4[ell[4]])
    combined4 = combined5 | substitutions4
    assert exact_zero(weighted.coeff_monomial(scale**4).subs(combined4))
    assert exact_zero(L.det().subs(combined4))

    # The generic E5 pivot contains A.  Rebuild A=0,C!=0 literally.
    weighted_a0, aa, bb, ll, LL = weighted_determinant(
        0, C * z * q, w * q
    )
    lower_a0 = aa + bb + ll
    E6_a0 = sp.expand(weighted_a0.coeff_monomial(scale**6))
    matrix6_a0, _, solution6_a0 = solve_linear(E6_a0, 6, lower_a0)
    assert matrix6_a0.rank() == 4
    substitutions6_a0 = {
        symbol: value
        for symbol, value in zip(lower_a0, solution6_a0)
        if not exact_zero(symbol - value)
    }
    assert exact_zero(E6_a0.subs(substitutions6_a0))
    E5_a0 = sp.expand(
        weighted_a0.coeff_monomial(scale**5).subs(substitutions6_a0)
    )
    free5_a0 = tuple(
        symbol for symbol in lower_a0 if symbol not in substitutions6_a0
    )
    matrix5_a0, _, solution5_a0 = solve_linear(E5_a0, 5, free5_a0)
    assert matrix5_a0.rank() == 6
    a0_e5_minor = sp.factor(
        matrix5_a0.extract(
            (0, 1, 2, 3, 4, 6),
            (1, 3, 4, 6, 7, 9),
        ).det()
    )
    a0_e5_unit = sp.factor(a0_e5_minor / (C * w**4))
    assert a0_e5_unit.is_Rational and a0_e5_unit != 0
    substitutions5_a0 = {
        symbol: value
        for symbol, value in zip(free5_a0, solution5_a0)
        if not exact_zero(symbol - value)
    }
    expected5_a0 = {
        aa[3]: 2 * ll[2] / C,
        bb[1]: 0,
        bb[2]: bb[3],
        bb[4]: 0,
        bb[5]: C**2 / 4,
        ll[1]: 0,
    }
    assert all(
        exact_zero(substitutions5_a0[key] - value)
        for key, value in expected5_a0.items()
    )
    assert ll[7] not in substitutions5_a0
    assert ll[8] not in substitutions5_a0
    combined5_a0 = substitutions6_a0 | substitutions5_a0
    assert exact_zero(
        weighted_a0.coeff_monomial(scale**5).subs(combined5_a0)
    )
    E4_a0 = sp.expand(
        weighted_a0.coeff_monomial(scale**4).subs(combined5_a0)
    )
    assert exact_zero(
        coefficient(E4_a0, y**3 * z)
        - sp.Rational(4, 3) * (2 * ll[8] - w * C) ** 2
    )
    E4_a0_l33 = sp.expand(E4_a0.subs(ll[8], w * C / 2))
    assert exact_zero(
        coefficient(E4_a0_l33, x**2 * y * z)
        + sp.Rational(8, 3) * ll[7] ** 2
    )
    E4_a0_l32 = sp.expand(E4_a0_l33.subs(ll[7], 0))
    assert exact_zero(
        coefficient(E4_a0_l32, x**4) - 4 * w * ll[4]
    )
    assert exact_zero(
        LL.det().subs(
            combined5_a0
            | {ll[8]: w * C / 2, ll[7]: 0, ll[4]: 0}
        )
    )

    # C=0 is handled without dividing by C or K.
    E5_zero = sp.expand(E5.subs(C, 0))
    assert exact_zero(coefficient(E5_zero, x**5) - K * b[1])
    assert exact_zero(
        coefficient(E5_zero, x**4 * y) + 2 * K * (b[2] - b[3])
    )
    assert exact_zero(
        coefficient(E5_zero, x**4 * z) - (K * b[4] + 6 * ell[1])
    )
    assert exact_zero(
        coefficient(E5_zero, x**3 * y**2)
        + 2 * (K * b[4] - 3 * ell[1])
    )
    assert exact_zero(
        coefficient(E5_zero, x**3 * y * z)
        + 4 * (K * b[5] + 3 * ell[2])
    )
    assert exact_zero(
        coefficient(E5_zero, x**2 * y**3) + 12 * ell[2]
    )
    zero_c_sub = {
        C: 0,
        b[1]: 0,
        b[2]: b[3],
        b[4]: 0,
        b[5]: 0,
        ell[1]: 0,
        ell[2]: 0,
    }
    # If A != 0, E5 itself forces the last row entries to zero.
    assert exact_zero(
        coefficient(E5_zero, y**5) - 4 * A * ell[8]
    )
    assert exact_zero(
        coefficient(E5_zero, x * y**4) + 2 * A * ell[7]
    )
    assert exact_zero(
        L.det().subs(zero_c_sub | {ell[7]: 0, ell[8]: 0})
    )

    # If A=0, E4 gives the two squares, still without division.
    E4_zero = sp.expand(
        weighted.coeff_monomial(scale**4).subs(
            substitutions6 | zero_c_sub | {A: 0}
        ).subs({C: 0, A: 0})
    )
    square33 = sp.factor(
        coefficient(E4_zero, y**3 * z)
        - sp.Rational(16, 3) * ell[8] ** 2
    )
    assert exact_zero(square33), square33
    square32 = sp.factor(
        coefficient(E4_zero.subs(ell[8], 0), x * y**3)
        + sp.Rational(8, 3) * ell[7] ** 2
    )
    assert exact_zero(square32), square32
    assert exact_zero(
        L.det().subs(
            zero_c_sub | {A: 0, ell[7]: 0, ell[8]: 0}
        )
    )
    print(
        "PASS K!=0 branch: generic, fresh A=0, and C=0 leaves close"
    )


def resonant_nonzero_A_branch():
    A = sp.symbols("A")
    B = sp.symbols("B1:8")
    V_general = (
        B[0] * x**2 * y
        + B[1] * x**2 * z
        + B[2] * x * y * z
        + B[3] * x * z**2
        + B[4] * y**2 * z
        + B[5] * y * z**2
        + B[6] * z**3
    )
    weighted, a, b, ell, _ = weighted_determinant(
        A * x * q, V_general, sp.Rational(3, 4) * A * q
    )
    all_lower = a + b + ell
    _, _, solution6 = solve_linear(
        sp.expand(weighted.coeff_monomial(scale**6)), 6, all_lower
    )
    substitutions6 = {
        symbol: value
        for symbol, value in zip(all_lower, solution6)
        if not exact_zero(symbol - value)
    }
    E5_general = sp.expand(
        weighted.coeff_monomial(scale**5).subs(substitutions6)
    )
    free5 = tuple(symbol for symbol in all_lower if symbol not in substitutions6)
    matrix5, rhs5 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E5_general, 5), free5
    )
    compat5 = [
        sp.factor((vector.T * rhs5)[0])
        for vector in matrix5.T.nullspace()
        if not exact_zero((vector.T * rhs5)[0])
    ]
    assert has_associate(compat5, sp.Rational(9, 4) * A**2 * B[2])
    assert has_associate(
        compat5, -3 * A**2 * (B[3] - B[4])
    )
    assert has_associate(compat5, 3 * A**2 * B[5])
    assert has_associate(compat5, sp.Rational(9, 2) * A**2 * B[6])

    # Reduced V, first on the two open charts B1!=0 and
    # B1=0,B2!=0.  Their pivots are recorded before the closed chart is
    # rebuilt.
    B1, B2, C = sp.symbols("B1 B2 C")
    V = B1 * x**2 * y + B2 * x**2 * z + C * z * q
    weighted, a, b, ell, L = weighted_determinant(
        A * x * q, V, sp.Rational(3, 4) * A * q
    )
    all_lower = a + b + ell
    E6 = sp.expand(weighted.coeff_monomial(scale**6))
    matrix6, _, solution6 = solve_linear(E6, 6, all_lower)
    assert matrix6.rank() == 4
    substitutions6 = {
        symbol: value
        for symbol, value in zip(all_lower, solution6)
        if not exact_zero(symbol - value)
    }
    assert exact_zero(E6.subs(substitutions6))

    E5 = sp.expand(
        weighted.coeff_monomial(scale**5).subs(substitutions6)
    )
    free6 = tuple(
        symbol for symbol in all_lower if symbol not in substitutions6
    )
    matrix5, _, solution5 = solve_linear(E5, 5, free6)
    assert exact_zero(
        matrix5.extract(
            (0, 2, 4, 5, 8), (1, 9, 10, 15, 16)
        ).det()
        + 1728 * A**2 * B1
    )
    assert exact_zero(
        matrix5.subs(B1, 0).extract(
            (1, 2, 4, 5, 8), (1, 9, 10, 15, 16)
        ).det()
        - 3456 * A**2 * B2
    )
    substitutions5 = {
        symbol: value
        for symbol, value in zip(free6, solution5)
        if not exact_zero(symbol - value)
    }
    combined5 = substitutions6 | substitutions5
    assert exact_zero(E5.subs(substitutions5))

    E4 = sp.expand(
        weighted.coeff_monomial(scale**4).subs(combined5)
    )
    free5 = tuple(
        symbol for symbol in all_lower if symbol not in combined5
    )
    matrix4, _, solution4 = solve_linear(E4, 4, free5)
    assert exact_zero(
        matrix4.extract(
            (0, 2, 4, 5, 8), (0, 2, 3, 5, 6)
        ).det()
        - sp.Rational(243, 64) * A**9 * B1
    )
    assert exact_zero(
        matrix4.subs(B1, 0).extract(
            (1, 2, 4, 5, 8), (0, 2, 3, 5, 6)
        ).det()
        + sp.Rational(243, 32) * A**9 * B2
    )
    substitutions4 = {
        symbol: value
        for symbol, value in zip(free5, solution4)
        if not exact_zero(symbol - value)
    }
    combined4 = combined5 | substitutions4
    assert exact_zero(E4.subs(substitutions4))

    E3 = sp.expand(
        weighted.coeff_monomial(scale**3).subs(combined4)
    )
    assert exact_zero(
        coefficient(E3, x * y * z)
        - coefficient(E3, y**3)
        + sp.Rational(3, 8) * A**3 * B2**2
    )
    assert exact_zero(
        coefficient(E3.subs(B2, 0), x**2 * y)
        - sp.Rational(3, 16) * A**3 * B1**2
    )
    print(
        "PASS resonant open charts: explicit B1/B2 pivots and E3 squares"
    )

    # Closed chart B1=B2=0,C=0: rebuild before solving.
    weighted_c0, ac0, bc0, lc0, Lc0 = weighted_determinant(
        A * x * q, 0, sp.Rational(3, 4) * A * q
    )
    lower_c0 = ac0 + bc0 + lc0
    E6_c0 = sp.expand(weighted_c0.coeff_monomial(scale**6))
    _, _, solution6_c0 = solve_linear(E6_c0, 6, lower_c0)
    substitutions6_c0 = {
        symbol: value
        for symbol, value in zip(lower_c0, solution6_c0)
        if not exact_zero(symbol - value)
    }
    assert exact_zero(E6_c0.subs(substitutions6_c0))
    E5_c0 = sp.expand(
        weighted_c0.coeff_monomial(scale**5).subs(substitutions6_c0)
    )
    free6_c0 = tuple(
        symbol for symbol in lower_c0 if symbol not in substitutions6_c0
    )
    matrix5_c0, _, solution5_c0 = solve_linear(E5_c0, 5, free6_c0)
    assert exact_zero(
        matrix5_c0.extract(
            (2, 4, 5, 8), (9, 10, 15, 16)
        ).det()
        - 576 * A**2
    )
    substitutions5_c0 = {
        symbol: value
        for symbol, value in zip(free6_c0, solution5_c0)
        if not exact_zero(symbol - value)
    }
    assert all(
        exact_zero(substitutions5_c0[symbol])
        for symbol in (lc0[1], lc0[2], lc0[7], lc0[8])
    )
    combined_c0 = substitutions6_c0 | substitutions5_c0
    assert exact_zero(E5_c0.subs(substitutions5_c0))
    assert exact_zero(Lc0.det().subs(combined_c0))

    # Closed chart B1=B2=0,C!=0.  Here l13 is free and must not
    # be specialized from the preceding B1/B2 charts.
    weighted_exc, ae, be, le, Le = weighted_determinant(
        A * x * q, C * z * q, sp.Rational(3, 4) * A * q
    )
    lower_exc = ae + be + le
    E6_exc = sp.expand(weighted_exc.coeff_monomial(scale**6))
    _, _, solution6_exc = solve_linear(E6_exc, 6, lower_exc)
    substitutions6_exc = {
        symbol: value
        for symbol, value in zip(lower_exc, solution6_exc)
        if not exact_zero(symbol - value)
    }
    assert exact_zero(E6_exc.subs(substitutions6_exc))
    E5_exc = sp.expand(
        weighted_exc.coeff_monomial(scale**5).subs(substitutions6_exc)
    )
    free6_exc = tuple(
        symbol for symbol in lower_exc if symbol not in substitutions6_exc
    )
    matrix5_exc, _, solution5_exc = solve_linear(E5_exc, 5, free6_exc)
    assert exact_zero(
        matrix5_exc.extract(
            (2, 4, 5, 8), (1, 9, 15, 16)
        ).det()
        - 288 * A**2 * C
    )
    substitutions5_exc = {
        symbol: value
        for symbol, value in zip(free6_exc, solution5_exc)
        if not exact_zero(symbol - value)
    }
    expected_exc = {
        ae[3]: 2 * le[2] / C,
        le[1]: 0,
        le[7]: 0,
        le[8]: sp.Rational(3, 8) * A * C,
    }
    assert all(
        exact_zero(substitutions5_exc[key] - value)
        for key, value in expected_exc.items()
    )
    assert le[2] not in substitutions5_exc
    combined5_exc = substitutions6_exc | substitutions5_exc
    assert exact_zero(E5_exc.subs(substitutions5_exc))

    E4_exc = sp.expand(
        weighted_exc.coeff_monomial(scale**4).subs(combined5_exc)
    )
    variables4_exc = (be[1], be[2], be[4], be[5])
    matrix4_exc, _, solution4_exc = solve_linear(
        E4_exc, 4, variables4_exc
    )
    assert exact_zero(
        matrix4_exc.extract((2, 5, 6, 8), (0, 1, 2, 3)).det()
        + sp.Rational(81, 32) * A**8
    )
    assert tuple(solution4_exc) == (0, be[3], 0, C**2 / 4)
    substitutions4_exc = dict(zip(variables4_exc, solution4_exc))
    assert exact_zero(E4_exc.subs(substitutions4_exc))
    E3_exc = sp.expand(
        weighted_exc.coeff_monomial(scale**3)
        .subs(combined5_exc)
        .subs(substitutions4_exc)
    )
    assert exact_zero(
        coefficient(E3_exc, x**2 * z)
        - sp.Rational(3, 4) * A**2 * le[4]
    )
    assert exact_zero(
        Le.det().subs(combined5_exc | substitutions4_exc | {le[4]: 0})
    )
    print(
        "PASS K=0,A!=0 branch: fresh closed C leaves close with l13 free"
    )


def resonant_zero_A_branch():
    w1, w2 = sp.symbols("w1 w2")
    B = sp.symbols("B1:8")
    V = (
        B[0] * x**2 * y
        + B[1] * x**2 * z
        + B[2] * x * y * z
        + B[3] * x * z**2
        + B[4] * y**2 * z
        + B[5] * y * z**2
        + B[6] * z**3
    )
    U = sp.Rational(4, 3) * (w1 * x**2 * y + w2 * x**2 * z)
    W = w1 * x * y + w2 * x * z
    weighted, a, b, ell, _ = weighted_determinant(U, V, W)
    all_lower = a + b + ell
    _, _, solution6 = solve_linear(
        sp.expand(weighted.coeff_monomial(scale**6)), 6, all_lower
    )
    substitutions6 = {
        symbol: value
        for symbol, value in zip(all_lower, solution6)
        if not exact_zero(symbol - value)
    }
    E5 = sp.expand(
        weighted.coeff_monomial(scale**5).subs(substitutions6)
    )
    free5 = tuple(symbol for symbol in all_lower if symbol not in substitutions6)
    matrix5, rhs5 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E5, 5), free5
    )
    compat5 = [
        sp.factor((vector.T * rhs5)[0])
        for vector in matrix5.T.nullspace()
        if not exact_zero((vector.T * rhs5)[0])
    ]
    assert has_associate(compat5, -sp.Rational(8, 9) * w1**3)
    assert has_associate(compat5, sp.Rational(16, 9) * w2**3)
    assert exact_zero(
        2 * coefficient(E5, x**2 * y**2 * z)
        + 3 * coefficient(E5, x * y**4)
        + 8 * coefficient(E5, x**3 * z**2)
        - sp.Rational(40, 9) * w1**3
    )
    assert exact_zero(
        coefficient(E5, x * y * z**3)
        + sp.Rational(16, 9) * w2**3
    )

    # Rebuild after w1=w2=0 and retain all seven coefficients of V.
    weighted, a, b, ell, L = weighted_determinant(0, V, 0)
    all_lower = a + b + ell
    E6_zero = sp.expand(weighted.coeff_monomial(scale**6))
    matrix6_zero, _, solution6 = solve_linear(
        E6_zero, 6, all_lower
    )
    assert matrix6_zero.rank() == 4
    substitutions = {
        symbol: value
        for symbol, value in zip(all_lower, solution6)
        if not exact_zero(symbol - value)
    }
    assert exact_zero(E6_zero.subs(substitutions))
    E5_zero = sp.expand(
        weighted.coeff_monomial(scale**5).subs(substitutions)
    )
    assert exact_zero(coefficient(E5_zero, x**5) + 3 * B[0] * a[3])
    assert exact_zero(coefficient(E5_zero, x**4 * y) - 6 * B[1] * a[3])
    assert exact_zero(
        coefficient(E5_zero, x**3 * y**2)
        - coefficient(E5_zero, x**4 * z)
        - 9 * B[2] * a[3]
    )
    assert exact_zero(
        coefficient(E5_zero, x**3 * y * z)
        - coefficient(E5_zero, x**2 * y**3)
        - 12 * (B[3] - B[4]) * a[3]
    )
    assert exact_zero(
        coefficient(E5_zero, x**3 * z**2) + 3 * B[5] * a[3]
    )
    assert exact_zero(
        coefficient(E5_zero, x**2 * y**2 * z) - 12 * B[5] * a[3]
    )
    assert exact_zero(
        coefficient(E5_zero, x**2 * y * z**2) - 18 * B[6] * a[3]
    )

    # Leaf a3=0.  The paired E5 rows force l12=l13=0.
    a3_zero = {a[3]: 0, ell[1]: 0, ell[2]: 0}
    assert exact_zero(E5_zero.subs(a3_zero))
    E4_a3_zero = sp.expand(
        weighted.coeff_monomial(scale**4).subs(substitutions | a3_zero)
    )
    assert exact_zero(
        coefficient(E4_a3_zero, y**3 * z)
        - sp.Rational(16, 3) * ell[8] ** 2
    )
    assert exact_zero(
        coefficient(E4_a3_zero.subs(ell[8], 0), x * y**3)
        + sp.Rational(8, 3) * ell[7] ** 2
    )
    assert exact_zero(
        L.det().subs(
            substitutions
            | a3_zero
            | {ell[7]: 0, ell[8]: 0}
        )
    )

    # Leaf a3!=0.  The literal product equations above force the unique
    # exceptional shape V=C*z*q and l13=C*a3/2.
    C = sp.symbols("C")
    weighted_exc, ae, be, le, Le = weighted_determinant(
        0, C * z * q, 0
    )
    lower_exc = ae + be + le
    E6_exc = sp.expand(weighted_exc.coeff_monomial(scale**6))
    _, _, solution6_exc = solve_linear(E6_exc, 6, lower_exc)
    substitutions6_exc = {
        symbol: value
        for symbol, value in zip(lower_exc, solution6_exc)
        if not exact_zero(symbol - value)
    }
    assert exact_zero(E6_exc.subs(substitutions6_exc))
    E5_exc = sp.expand(
        weighted_exc.coeff_monomial(scale**5).subs(substitutions6_exc)
    )
    free6_exc = tuple(
        symbol for symbol in lower_exc if symbol not in substitutions6_exc
    )
    matrix5_exc, _ = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E5_exc, 5), free6_exc
    )
    assert exact_zero(
        matrix5_exc.extract((2, 4), (1, 9)).det() + 36 * C
    )
    exceptional_e5 = {le[1]: 0, le[2]: C * ae[3] / 2}
    assert exact_zero(E5_exc.subs(exceptional_e5))

    E4_exc = sp.expand(
        weighted_exc.coeff_monomial(scale**4).subs(
            substitutions6_exc | exceptional_e5
        )
    )
    assert exact_zero(
        coefficient(E4_exc, y**3 * z)
        - sp.Rational(16, 3) * le[8] ** 2
    )
    assert exact_zero(
        coefficient(E4_exc.subs(le[8], 0), x * y**3)
        + sp.Rational(8, 3) * le[7] ** 2
    )
    E4_exc_squares = sp.expand(E4_exc.subs({le[7]: 0, le[8]: 0}))
    variables4 = (be[1], be[2], be[4], be[5])
    matrix4, _, solution4 = solve_linear(E4_exc_squares, 4, variables4)
    assert exact_zero(
        matrix4.extract((0, 1, 2, 4), (0, 1, 2, 3)).det()
        - 648 * ae[3] ** 4
    )
    assert tuple(solution4) == (0, be[3], 0, C**2 / 4)
    substitutions4 = dict(zip(variables4, solution4))
    assert exact_zero(E4_exc_squares.subs(substitutions4))
    E3_exc = sp.expand(
        weighted_exc.coeff_monomial(scale**3)
        .subs(substitutions6_exc | exceptional_e5)
        .subs({le[7]: 0, le[8]: 0})
        .subs(substitutions4)
    )
    assert exact_zero(
        coefficient(E3_exc, x**3) + 3 * ae[3] * le[4]
    )
    assert exact_zero(
        Le.det().subs(
            substitutions6_exc
            | exceptional_e5
            | substitutions4
            | {le[7]: 0, le[8]: 0, le[4]: 0}
        )
    )

    # The C=0 exceptional shape is V=0 and has l13=0 before the
    # square exit, so no division by C is used.
    V_zero = {symbol: 0 for symbol in B}
    assert exact_zero(
        E5_zero.subs(V_zero | {ell[1]: 0, ell[2]: 0})
    )
    assert exact_zero(
        L.det().subs(
            substitutions
            | V_zero
            | {ell[1]: 0, ell[2]: 0, ell[7]: 0, ell[8]: 0}
        )
    )
    print(
        "PASS K=A=0 branch: arbitrary V and exceptional C*z*q leaves close"
    )


def main():
    raw_e7_certificate()
    general_e6_compatibility()
    open_branch_extra_compatibility()
    reduced_open_branch()
    resonant_nonzero_A_branch()
    resonant_zero_A_branch()
    print("ALL MARKED TRIPLE-ORBIT SYMPY CERTIFICATES PASSED")


if __name__ == "__main__":
    main()
