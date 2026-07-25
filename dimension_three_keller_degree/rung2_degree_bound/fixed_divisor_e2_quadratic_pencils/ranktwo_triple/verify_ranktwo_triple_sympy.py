#!/usr/bin/env python3
"""Exact branch certificate for the rank-two e=2 triple companion."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: verification requires assertions; do not use -O", file=sys.stderr)
    raise SystemExit(2)

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


def coefficient(value, monomial):
    return sp.Poly(sp.expand(value), *variables).coeff_monomial(monomial)


def coefficient_column(direction):
    U, V, W = direction
    return sp.Matrix(
        [coefficient(U, monomial) for monomial in mon3]
        + [coefficient(V, monomial) for monomial in mon3]
        + [coefficient(W, monomial) for monomial in mon2]
    )


def nonzero_pairs(matrix, rhs):
    return [
        (vector, sp.factor((vector.T * rhs)[0]))
        for vector in matrix.T.nullspace()
        if not exact_zero((vector.T * rhs)[0])
    ]


def associate(value, target):
    if exact_zero(value) or exact_zero(target):
        return exact_zero(value) and exact_zero(target)
    ratio = sp.cancel(value / target)
    return not ratio.free_symbols and ratio != 0


def polynomial_left_pair(matrix, rhs, vector):
    denominators = [
        sp.together(entry).as_numer_denom()[1]
        for entry in vector
        if not exact_zero(entry)
    ]
    denominator = sp.factor(sp.lcm(denominators)) if denominators else sp.Integer(1)
    polynomial_vector = vector.applyfunc(
        lambda entry: sp.cancel(denominator * entry)
    )
    assert all(
        sp.together(entry).as_numer_denom()[1] in (1, -1)
        for entry in polynomial_vector
    )
    assert all(
        exact_zero(entry) for entry in matrix.T * polynomial_vector
    )
    return polynomial_vector, sp.factor((polynomial_vector.T * rhs)[0])


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
    assert all(
        exact_zero(weighted.coeff_monomial(scale**degree))
        for degree in (9, 8, 7)
    )
    return weighted, a, b, ell, L


def solve_identity(weighted, unknowns, degree, substitutions=None):
    substitutions = substitutions or {}
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
    if pairs:
        return identity, remaining, matrix, rhs, pairs, None
    solution = next(iter(sp.linsolve((matrix, rhs), remaining)))
    solution_map = dict(zip(remaining, solution))
    assert exact_zero(identity.subs(solution_map))
    return identity, remaining, matrix, rhs, pairs, solution_map


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
    rows = (1, 2, 3, 5, 6, 7, 8, 9)
    columns = (1, 2, 3, 5, 6, 7, 8, 9)
    assert exact_zero(jac3(P, Q, R))
    assert matrix.shape == (36, 26)
    assert rhs == sp.zeros(36, 1)
    assert matrix.rank() == 8
    assert matrix.extract(rows, columns).det() == 236196

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
    kernel_rows = (
        0, 1, 2, 3, 4, 5, 10, 11, 12,
        13, 14, 15, 16, 17, 18, 19, 20, 24,
    )
    assert matrix * kernel == sp.zeros(36, 18)
    assert kernel.rank() == 18
    assert (
        kernel.extract(kernel_rows, range(18)).det()
        == sp.Rational(256, 27)
    )
    assert matrix.cols - matrix.rank() == kernel.cols
    print(
        "PASS raw E7: rank 8, complete 18-dimensional kernel, "
        "five legal gauges and thirteen normals"
    )


def general_e6_certificate():
    A = sp.symbols("gA")
    w1, w2, w3, w4, w5 = sp.symbols("gw1:6")
    B1, B2, B3, B4, B5, B6, B7 = sp.symbols("gB1:8")
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
    weighted, a, b, ell, _ = weighted_data(U, V, W, "g")
    unknowns = a + b + ell
    E6 = weighted.coeff_monomial(scale**6)
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6, 6), unknowns
    )
    assert matrix.rank() == 4
    assert matrix.extract((1, 2, 3, 5), (1, 2, 3, 5)).det() == 324
    values = [value for _, value in nonzero_pairs(matrix, rhs)]
    assert len(values) == 8
    assert any(associate(value, w3**2) for value in values)
    assert any(associate(value, w5**2) for value in values)

    K = 9 * A - 12 * w4
    M = -3 * A + 8 * w4
    reduced = [
        sp.factor(value.subs({w3: 0, w5: 0}))
        for value in values
        if not exact_zero(value.subs({w3: 0, w5: 0}))
    ]
    targets = (K * B4, K * B5 + M * w1, K * B6 + M * w2, K * B7)
    assert len(reduced) == 4
    assert all(
        any(associate(value, target) for value in reduced)
        for target in targets
    )
    print(
        "PASS E6: w3=w5=0 and exact K/M compatibility branch"
    )


def k_open_e5_certificate():
    A, K = sp.symbols("oA oK")
    w1, w2 = sp.symbols("ow1 ow2")
    B1, B2, B3 = sp.symbols("oB1 oB2 oB3")
    w4 = (9 * A - K) / 12
    M = (9 * A - 2 * K) / 3
    U = A * x * y * z + sp.Rational(4, 3) * (
        w1 * x**2 * y + w2 * x**2 * z
    )
    V = (
        B1 * x * y**2
        + B2 * x * y * z
        + B3 * x * z**2
        - M * w1 / K * y**2 * z
        - M * w2 / K * y * z**2
    )
    W = w1 * x * y + w2 * x * z + w4 * y * z
    weighted, a, b, ell, _ = weighted_data(U, V, W, "o")
    unknowns = a + b + ell
    _, _, matrix6, rhs6, pairs6, solution6 = solve_identity(
        weighted, unknowns, 6
    )
    assert matrix6.rank() == 4 and not pairs6
    _, _, matrix5, rhs5, pairs5, _ = solve_identity(
        weighted, unknowns, 5, solution6
    )
    assert matrix5.rank() == 6
    values = [value for _, value in pairs5]
    S = (9 * A - 2 * K) * (9 * A - K)
    T = -S
    targets = (
        w1 * (3 * B1 * K + 4 * w1**2),
        w2 * (3 * B3 * K + 4 * w2**2),
        B1 * T + 4 * K * w1**2,
        B3 * T + 4 * K * w2**2,
        A * w1 * S / K,
        A * w2 * S / K,
    )
    assert len(values) == 6
    assert all(
        any(associate(value, target) for value in values)
        for target in targets
    )

    H = 81 * A**2 - 27 * A * K + 5 * K**2
    tB, tw = sp.symbols("tB tw")
    resultant = sp.factor(
        sp.resultant(
            3 * tB * K + 4 * tw**2,
            tB * T + 4 * K * tw**2,
            tB,
        )
    )
    assert exact_zero(resultant - 4 * tw**2 * H)
    assert H.subs(A, 0) == 5 * K**2
    assert exact_zero(H.subs(A, 2 * K / 9) - 3 * K**2)
    assert exact_zero(H.subs(A, K / 9) - 3 * K**2)
    # Thus K!=0 and the last compatibility force w1=w2=0.
    # The remaining equations are B1*S=B3*S=0.
    assert exact_zero(
        (B1 * T + 4 * K * w1**2).subs(w1, 0) + B1 * S
    )
    assert exact_zero(
        (B3 * T + 4 * K * w2**2).subs(w2, 0) + B3 * S
    )
    print(
        "PASS K!=0 E5: resultant forces w1=w2=0; "
        "only two S=0 resonances remain"
    )


def aligned_k_nonzero_exit():
    A, B, w = sp.symbols("aA aB aw")
    U, V, W = A * x * y * z, B * x * y * z, w * y * z
    weighted, a, b, ell, L = weighted_data(U, V, W, "a")
    unknowns = a + b + ell
    _, _, matrix6, _, pairs6, solution6 = solve_identity(
        weighted, unknowns, 6
    )
    assert matrix6.rank() == 4 and not pairs6
    _, _, matrix5, _, pairs5, solution5 = solve_identity(
        weighted, unknowns, 5, solution6
    )
    assert matrix5.rank() == 6 and not pairs5
    substitutions = solution6 | solution5
    D0 = -3 * A + 4 * w
    assert exact_zero(substitutions[ell[7]])
    assert exact_zero(substitutions[ell[8]])
    E4 = sp.expand(
        weighted.coeff_monomial(scale**4).subs(substitutions)
    )
    c_y = coefficient(E4, x**3 * y)
    c_z = coefficient(E4, x**3 * z)
    common = 3 * B * D0 + 9 * a[4]
    assert exact_zero(c_y - (D0**2 * ell[4] + common * ell[1]) / D0)
    assert exact_zero(c_z + (D0**2 * ell[5] + common * ell[2]) / D0)
    minor = ell[1] * ell[5] - ell[2] * ell[4]
    assert exact_zero(
        ell[1] * (-D0 * c_z)
        - ell[2] * (D0 * c_y)
        - D0**2 * minor
    )
    assert exact_zero(L.det().subs(substitutions) - ell[6] * minor)
    print(
        "PASS aligned K!=0 branch: two E4 equations force det(L)=0"
    )


def resonance_two_exit():
    A, B1, B2, B3 = sp.symbols("r2A r2B1 r2B2 r2B3")
    U = A * x * y * z
    V = B1 * x * y**2 + B2 * x * y * z + B3 * x * z**2
    W = sp.Rational(3, 8) * A * y * z
    weighted, a, b, ell, _ = weighted_data(U, V, W, "r2")
    unknowns = a + b + ell
    _, _, matrix6, _, pairs6, solution6 = solve_identity(
        weighted, unknowns, 6
    )
    assert matrix6.rank() == 4 and not pairs6
    _, _, matrix5, _, pairs5, solution5 = solve_identity(
        weighted, unknowns, 5, solution6
    )
    assert matrix5.rank() == 4 and not pairs5
    E4 = sp.expand(
        weighted.coeff_monomial(scale**4)
        .subs(solution6)
        .subs(solution5)
    )
    assert coefficient(E4, z**4) == sp.Rational(3, 8) * A**2 * B3**2

    # The preceding square disposes of the chart B3 != 0 (and, after the
    # y/z involution, the chart B1 != 0).  At B1=B3=0 the generic aligned
    # E5 pivot vanishes, so this residual branch requires a fresh solve.
    B = sp.symbols("r2alignedB")
    weighted0, a0, b0, ell0, L0 = weighted_data(
        A * x * y * z,
        B * x * y * z,
        sp.Rational(3, 8) * A * y * z,
        "r2aligned",
    )
    unknowns0 = a0 + b0 + ell0
    _, _, matrix60, _, pairs60, solution60 = solve_identity(
        weighted0, unknowns0, 6
    )
    assert matrix60.rank() == 4 and not pairs60
    _, _, matrix50, _, pairs50, solution50 = solve_identity(
        weighted0, unknowns0, 5, solution60
    )
    assert matrix50.rank() == 4 and not pairs50
    substitutions0 = solution60 | solution50
    E40 = sp.expand(
        weighted0.coeff_monomial(scale**4).subs(substitutions0)
    )
    square_y = coefficient(E40, x**2 * y**2)
    square_z = coefficient(E40, x**2 * z**2)
    assert exact_zero(square_y + sp.Rational(4, 3) * ell0[7] ** 2)
    assert exact_zero(square_z - sp.Rational(4, 3) * ell0[8] ** 2)
    reduced = {ell0[7]: 0, ell0[8]: 0}
    c_y = sp.expand(coefficient(E40, x**3 * y).subs(reduced))
    c_z = sp.expand(coefficient(E40, x**3 * z).subs(reduced))
    T = 3 * B - 6 * a0[4] / A
    assert exact_zero(c_y - (T * ell0[1] - sp.Rational(3, 2) * A * ell0[4]))
    assert exact_zero(c_z - (-T * ell0[2] + sp.Rational(3, 2) * A * ell0[5]))
    minor = ell0[1] * ell0[5] - ell0[2] * ell0[4]
    assert exact_zero(
        ell0[1] * c_z + ell0[2] * c_y
        - sp.Rational(3, 2) * A * minor
    )
    assert exact_zero(
        L0.det().subs(substitutions0).subs(reduced) - ell0[6] * minor
    )
    print(
        "PASS 9A=2K resonance: after y/z symmetry, "
        "the z^4 square handles a nonzero end; a fresh rank-four aligned "
        "solve forces det(L)=0 at B1=B3=0"
    )


def resonance_one_exit():
    A, B1, B2, B3 = sp.symbols("r1A r1B1 r1B2 r1B3")
    U = A * x * y * z
    V = B1 * x * y**2 + B2 * x * y * z + B3 * x * z**2
    W = 0
    weighted, a, b, ell, L = weighted_data(U, V, W, "r1")
    unknowns = a + b + ell
    _, _, matrix6, _, pairs6, solution6 = solve_identity(
        weighted, unknowns, 6
    )
    assert matrix6.rank() == 4 and not pairs6
    _, _, matrix5, _, pairs5, solution5 = solve_identity(
        weighted, unknowns, 5, solution6
    )
    assert matrix5.rank() == 6 and not pairs5
    substitutions = solution6 | solution5
    assert exact_zero(substitutions[ell[7]])
    assert exact_zero(substitutions[ell[8]])
    E4 = sp.expand(
        weighted.coeff_monomial(scale**4).subs(substitutions)
    )
    c_y = coefficient(E4, x**3 * y)
    c_z = coefficient(E4, x**3 * z)
    assert exact_zero(
        c_y + 3 * (A * B3 * ell[4] - b[5] * ell[1]) / B3
    )
    assert exact_zero(
        c_z - 3 * (A * B3 * ell[5] - b[5] * ell[2]) / B3
    )
    minor = ell[1] * ell[5] - ell[2] * ell[4]
    assert exact_zero(
        ell[1] * (B3 * c_z / 3)
        + ell[2] * (B3 * c_y / 3)
        - A * B3 * minor
    )
    assert exact_zero(L.det().subs(substitutions) - ell[6] * minor)
    print(
        "PASS 9A=K resonance: localized E4 pair forces det(L)=0"
    )


def k_zero_a_nonzero_exit():
    A = sp.symbols("zA")
    B1, B2, B3, B4, B5, B6, B7 = sp.symbols("zB1:8")
    U = A * x * y * z
    V = (
        B1 * x * y**2
        + B2 * x * y * z
        + B3 * x * z**2
        + B4 * y**3
        + B5 * y**2 * z
        + B6 * y * z**2
        + B7 * z**3
    )
    W = sp.Rational(3, 4) * A * y * z
    weighted, a, b, ell, _ = weighted_data(U, V, W, "z")
    unknowns = a + b + ell
    _, _, matrix6, _, pairs6, solution6 = solve_identity(
        weighted, unknowns, 6
    )
    assert matrix6.rank() == 4 and not pairs6
    _, _, matrix5, _, pairs5, _ = solve_identity(
        weighted, unknowns, 5, solution6
    )
    values = [value for _, value in pairs5]
    targets = (A**2 * B1, A**2 * B3, A**2 * B4, A**2 * B5, A**2 * B6, A**2 * B7)
    assert len(values) == 6
    assert all(
        any(associate(value, target) for value in values)
        for target in targets
    )

    U0, V0, W0 = A * x * y * z, B2 * x * y * z, W
    weighted0, a0, b0, ell0, L0 = weighted_data(U0, V0, W0, "z0")
    unknowns0 = a0 + b0 + ell0
    _, _, matrix60, _, pairs60, solution60 = solve_identity(
        weighted0, unknowns0, 6
    )
    assert matrix60.rank() == 4 and not pairs60
    _, _, matrix50, _, pairs50, solution50 = solve_identity(
        weighted0, unknowns0, 5, solution60
    )
    assert matrix50.rank() == 4 and not pairs50
    substitutions = solution60 | solution50
    assert all(
        exact_zero(substitutions[entry])
        for entry in (ell0[1], ell0[2], ell0[7], ell0[8])
    )
    assert exact_zero(L0.det().subs(substitutions))
    print(
        "PASS K=0,A!=0: E5 kills six B parameters and then det(L)"
    )


def origin_e5_compatibility():
    w1, w2 = sp.symbols("cw1 cw2")
    B1, B2, B3, B4, B5, B6, B7 = sp.symbols("cB1:8")
    U = sp.Rational(4, 3) * (w1 * x**2 * y + w2 * x**2 * z)
    V = (
        B1 * x * y**2
        + B2 * x * y * z
        + B3 * x * z**2
        + B4 * y**3
        + B5 * y**2 * z
        + B6 * y * z**2
        + B7 * z**3
    )
    W = w1 * x * y + w2 * x * z
    weighted, a, b, ell, _ = weighted_data(U, V, W, "c")
    unknowns = a + b + ell
    _, _, matrix6, _, pairs6, solution6 = solve_identity(
        weighted, unknowns, 6
    )
    assert matrix6.rank() == 4 and not pairs6
    _, _, matrix5, rhs5, pairs5, _ = solve_identity(
        weighted, unknowns, 5, solution6
    )
    targets = (
        w1**2 * (9 * B4 * w2 - 3 * B5 * w1 + 2 * w1**2),
        w1 * (9 * B4 * w2**2 - 3 * B6 * w1**2 + 2 * w1**2 * w2),
        -B4 * w2**3 + B7 * w1**3,
    )
    polynomials = []
    for vector, _ in pairs5:
        _, polynomial = polynomial_left_pair(matrix5, rhs5, vector)
        polynomials.append(polynomial)
    assert all(
        any(associate(polynomial, target) for polynomial in polynomials)
        for target in targets
    )
    print(
        "PASS K=A=0 E5: three polynomial syzygies give the "
        "complete necessary cubic-tail parametrization"
    )


def origin_open_contradiction():
    s, r, C = sp.symbols("os or oC")
    B1, B2, B3 = sp.symbols("o1 o2 o3")
    U = sp.Rational(4, 3) * s * (x**2 * y + r * x**2 * z)
    V = (
        B1 * x * y**2
        + B2 * x * y * z
        + B3 * x * z**2
        + C * y**3
        + (3 * C * r + sp.Rational(2, 3) * s) * y**2 * z
        + (3 * C * r**2 + sp.Rational(2, 3) * r * s) * y * z**2
        + C * r**3 * z**3
    )
    W = s * x * y + r * s * x * z
    weighted, a, b, ell, _ = weighted_data(U, V, W, "oo")
    unknowns = a + b + ell
    _, _, matrix6, _, pairs6, solution6 = solve_identity(
        weighted, unknowns, 6
    )
    assert matrix6.rank() == 4 and not pairs6
    _, _, matrix5, _, pairs5, solution5 = solve_identity(
        weighted, unknowns, 5, solution6
    )
    assert matrix5.rank() == 5 and not pairs5
    E4 = sp.expand(
        weighted.coeff_monomial(scale**4)
        .subs(solution6)
        .subs(solution5)
    )
    assert coefficient(E4, y**4) == sp.Rational(4, 27) * s**4
    print(
        "PASS K=A=0, C*r*s!=0: literal E4 coefficient is 4*s^4/27"
    )


def origin_rankdrop_contradictions():
    s, r, C = sp.symbols("ds dr dC")
    B1, B2, B3 = sp.symbols("d1 d2 d3")

    # C=0 is a division-free rank-drop chart: one literal polynomial
    # E5 left relation has right side -4*s^3/9.
    Uc = sp.Rational(4, 3) * s * (x**2 * y + r * x**2 * z)
    Vc = (
        B1 * x * y**2
        + B2 * x * y * z
        + B3 * x * z**2
        + sp.Rational(2, 3) * s * y**2 * z
        + sp.Rational(2, 3) * r * s * y * z**2
    )
    Wc = s * x * y + r * s * x * z
    weightedc, ac, bc, ellc, _ = weighted_data(Uc, Vc, Wc, "c_zero")
    unknownsc = ac + bc + ellc
    _, _, matrix6c, _, pairs6c, solution6c = solve_identity(
        weightedc, unknownsc, 6
    )
    assert matrix6c.rank() == 4 and not pairs6c
    _, _, matrix5c, _, pairs5c, _ = solve_identity(
        weightedc, unknownsc, 5, solution6c
    )
    assert matrix5c.rank() == 4
    assert any(associate(value, s**3) for _, value in pairs5c)

    # On r=0 with C!=0, the preceding generic left vector is localized
    # at B3.  Its fixed pivot and cleared right side show that it is valid
    # only on B3!=0.
    Ur = sp.Rational(4, 3) * s * x**2 * y
    Vr = (
        B1 * x * y**2
        + B2 * x * y * z
        + B3 * x * z**2
        + C * y**3
        + sp.Rational(2, 3) * s * y**2 * z
    )
    Wr = s * x * y
    weightedr, ar, br, ellr, _ = weighted_data(Ur, Vr, Wr, "r_zero")
    unknownsr = ar + br + ellr
    _, _, matrix6r, _, pairs6r, solution6r = solve_identity(
        weightedr, unknownsr, 6
    )
    assert matrix6r.rank() == 4 and not pairs6r
    _, _, matrix5r, rhs5r, pairs5r, _ = solve_identity(
        weightedr, unknownsr, 5, solution6r
    )
    assert matrix5r.rank() == 4
    assert exact_zero(
        matrix5r.extract((1, 2, 3, 5), (0, 1, 3, 5)).det()
        + 96 * B3 * s**2
    )
    localized_pairs = []
    for vector, value in pairs5r:
        polynomial_vector, polynomial = polynomial_left_pair(
            matrix5r, rhs5r, vector
        )
        denominators = [
            sp.together(entry).as_numer_denom()[1]
            for entry in vector
            if not exact_zero(entry)
        ]
        denominator = sp.factor(sp.lcm(denominators))
        localized_pairs.append((denominator, polynomial, value))
        assert all(
            exact_zero(entry) for entry in matrix5r.T * polynomial_vector
        )
    assert any(
        associate(denominator, B3)
        and associate(polynomial, B3 * s**3)
        and associate(value, s**3)
        for denominator, polynomial, value in localized_pairs
    )

    # The missing B3=0 leaf is rebuilt before solving.  Its E5 system has
    # a C*s^2 pivot and no compatibility obstruction; E4 then contradicts
    # s!=0 directly.
    Vr0 = Vr.subs(B3, 0)
    weighted0, a0, b0, ell0, _ = weighted_data(Ur, Vr0, Wr, "r_zero_b3_zero")
    unknowns0 = a0 + b0 + ell0
    _, _, matrix60, _, pairs60, solution60 = solve_identity(
        weighted0, unknowns0, 6
    )
    assert matrix60.rank() == 4 and not pairs60
    _, _, matrix50, _, pairs50, solution50 = solve_identity(
        weighted0, unknowns0, 5, solution60
    )
    assert matrix50.rank() == 4 and not pairs50
    assert exact_zero(
        matrix50.extract((1, 2, 3, 6), (0, 1, 3, 5)).det()
        - 144 * C * s**2
    )
    E40 = sp.expand(
        weighted0.coeff_monomial(scale**4)
        .subs(solution60)
        .subs(solution50)
    )
    assert coefficient(E40, y**4) == sp.Rational(4, 27) * s**4
    assert exact_zero(
        coefficient(E40, y**3 * z) + 8 * s**5 / (243 * C)
    )
    print(
        "PASS K=A=0 rank drops: C=0 is division-free; r=0,B3!=0 "
        "uses its explicit B3 pivot; the fresh B3=0 leaf exits at E4"
    )


def origin_zero_exit():
    B1, B2, B3, B4, B5, B6, B7 = sp.symbols("nB1:8")
    U, W = 0, 0
    V = (
        B1 * x * y**2
        + B2 * x * y * z
        + B3 * x * z**2
        + B4 * y**3
        + B5 * y**2 * z
        + B6 * y * z**2
        + B7 * z**3
    )
    weighted, a, b, ell, L = weighted_data(U, V, W, "n")
    unknowns = a + b + ell
    _, _, matrix6, _, pairs6, solution6 = solve_identity(
        weighted, unknowns, 6
    )
    assert matrix6.rank() == 4 and not pairs6
    E5 = sp.expand(
        weighted.coeff_monomial(scale**5).subs(solution6)
    )
    literal_e5 = {
        x**4 * y: 3 * ell[1],
        x**4 * z: -3 * ell[2],
        x**3 * y**2: -6 * B1 * a[4],
        x**3 * z**2: 6 * B3 * a[4],
        x**2 * y**3: -9 * B4 * a[4],
        x**2 * y**2 * z: -3 * B5 * a[4],
        x**2 * y * z**2: 3 * B6 * a[4],
        x**2 * z**3: 9 * B7 * a[4],
    }
    assert all(
        exact_zero(coefficient(E5, monomial) - value)
        for monomial, value in literal_e5.items()
    )

    # The first two literal rows globally force ell_12=ell_13=0,
    # without using a parameter-dependent E5 pivot.
    common = solution6 | {ell[1]: 0, ell[2]: 0}

    # If a_4=0, two pure E4 squares kill the remaining entries of the
    # third row.
    E4_zero = sp.expand(
        weighted.coeff_monomial(scale**4).subs(common).subs(a[4], 0)
    )
    assert exact_zero(
        coefficient(E4_zero, x**2 * y**2)
        + sp.Rational(4, 3) * ell[7] ** 2
    )
    assert exact_zero(
        coefficient(E4_zero, x**2 * z**2)
        - sp.Rational(4, 3) * ell[8] ** 2
    )

    # If a_4!=0, the six product rows kill every coefficient of V
    # except B2.  Rebuild that leaf before reading its E4 coefficients.
    transverse_zero = {
        B1: 0,
        B3: 0,
        B4: 0,
        B5: 0,
        B6: 0,
        B7: 0,
    }
    E4_open = sp.expand(
        weighted.coeff_monomial(scale**4)
        .subs(common)
        .subs(transverse_zero)
    )
    assert exact_zero(
        coefficient(E4_open, x * y**2 * z) - 2 * a[4] * ell[7]
    )
    assert exact_zero(
        coefficient(E4_open, x * y * z**2) + 2 * a[4] * ell[8]
    )
    assert exact_zero(
        L.det().subs(common).subs({ell[7]: 0, ell[8]: 0})
    )
    print(
        "PASS K=A=w1=w2=0: global literal E5 split and fresh E4 "
        "squares/linear rows force det(L)=0"
    )


def symmetry_certificate():
    swap = {y: z, z: y}
    assert exact_zero(P.xreplace(swap) - P)
    assert exact_zero(Q.xreplace(swap) - Q)
    assert exact_zero(R.xreplace(swap) - R)
    print("PASS y/z involution used only to choose a nonzero marked end")


def main():
    raw_e7_certificate()
    general_e6_certificate()
    k_open_e5_certificate()
    aligned_k_nonzero_exit()
    resonance_two_exit()
    resonance_one_exit()
    k_zero_a_nonzero_exit()
    origin_e5_compatibility()
    origin_open_contradiction()
    origin_rankdrop_contradictions()
    origin_zero_exit()
    symmetry_certificate()
    print("ALL RANK-TWO e=2 TRIPLE-COMPANION SYMPY CERTIFICATES PASSED")


if __name__ == "__main__":
    main()
