#!/usr/bin/env python3
"""Exact theorem certificate for the rank-one e=2 triple companion."""

from __future__ import annotations

import sys
from itertools import product

if not __debug__:
    print("FAIL: verification requires assertions; do not use -O", file=sys.stderr)
    raise SystemExit(2)

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


def exact_zero(value: sp.Expr) -> bool:
    return sp.cancel(sp.expand(value)) == 0


def compose(
    substitutions: dict[sp.Symbol, sp.Expr],
    later: dict[sp.Symbol, sp.Expr],
) -> dict[sp.Symbol, sp.Expr]:
    result = {
        variable: sp.cancel(sp.sympify(value).subs(later, simultaneous=True))
        for variable, value in substitutions.items()
    }
    result.update(later)
    return result


def homogeneous_exponents(degree: int):
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def homogeneous_coefficients(value: sp.Expr, degree: int):
    polynomial = sp.Poly(sp.expand(value), *variables)
    return [
        polynomial.coeff_monomial(x**i * y**j * z**k)
        for i, j, k in homogeneous_exponents(degree)
    ]


def coefficient(value: sp.Expr, monomial: sp.Expr) -> sp.Expr:
    return sp.Poly(sp.expand(value), *variables).coeff_monomial(monomial)


def jac3(f: sp.Expr, g: sp.Expr, h: sp.Expr) -> sp.Expr:
    return sp.Matrix([f, g, h]).jacobian(variables).det()


def coefficient_column(direction) -> sp.Matrix:
    U, V, W = direction
    return sp.Matrix(
        [coefficient(U, monomial) for monomial in mon3]
        + [coefficient(V, monomial) for monomial in mon3]
        + [coefficient(W, monomial) for monomial in mon2]
    )


def associate(value: sp.Expr, target: sp.Expr) -> bool:
    if exact_zero(value) or exact_zero(target):
        return exact_zero(value) and exact_zero(target)
    ratio = sp.cancel(value / target)
    return not ratio.free_symbols and ratio != 0


def nonzero_pairs(matrix: sp.Matrix, rhs: sp.Matrix):
    return [
        (vector, sp.factor((vector.T * rhs)[0]))
        for vector in matrix.T.nullspace()
        if not exact_zero((vector.T * rhs)[0])
    ]


def cleared_left_pairs(matrix: sp.Matrix, rhs: sp.Matrix):
    pairs = []
    for vector in matrix.T.nullspace():
        denominators = [
            sp.together(entry).as_numer_denom()[1]
            for entry in vector
            if not exact_zero(entry)
        ]
        denominator = (
            sp.factor(sp.lcm(denominators)) if denominators else sp.Integer(1)
        )
        polynomial_vector = vector.applyfunc(
            lambda entry: sp.cancel(denominator * entry)
        )
        assert all(
            exact_zero(entry) for entry in matrix.T * polynomial_vector
        )
        assert all(
            sp.together(entry).as_numer_denom()[1] in (1, -1)
            for entry in polynomial_vector
        )
        value = sp.factor((polynomial_vector.T * rhs)[0])
        if not exact_zero(value):
            pairs.append((polynomial_vector, value))
    return pairs


def weighted_data(U: sp.Expr, V: sp.Expr, W: sp.Expr, prefix: str):
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


def identity_data(
    weighted: sp.Poly,
    unknowns: tuple[sp.Symbol, ...],
    degree: int,
    substitutions: dict[sp.Symbol, sp.Expr] | None = None,
):
    substitutions = substitutions or {}
    identity = sp.expand(
        weighted.coeff_monomial(scale**degree).subs(substitutions)
    )
    remaining = tuple(
        variable for variable in unknowns if variable in identity.free_symbols
    )
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(identity, degree), remaining
    )
    return identity, remaining, matrix, rhs


def solve_linear_identity(
    weighted: sp.Poly,
    unknowns: tuple[sp.Symbol, ...],
    degree: int,
    substitutions: dict[sp.Symbol, sp.Expr] | None = None,
):
    identity, remaining, matrix, rhs = identity_data(
        weighted, unknowns, degree, substitutions
    )
    assert not nonzero_pairs(matrix, rhs)
    solution = next(iter(sp.linsolve((matrix, rhs), remaining)))
    solution_map = dict(zip(remaining, solution))
    assert exact_zero(identity.subs(solution_map))
    return identity, remaining, matrix, rhs, solution_map


def raw_e7_certificate() -> None:
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
    rows = (0, 1, 2, 3, 4, 5, 6, 8)
    columns = (1, 2, 4, 5, 6, 7, 8, 9)
    assert matrix.shape == (36, 26)
    assert rhs == sp.zeros(36, 1)
    assert matrix.rank() == 8
    assert matrix.extract(rows, columns).det() == 1889568

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
    kernel_rows = (
        0, 1, 2, 3, 4, 5, 10, 11, 12,
        13, 14, 15, 16, 17, 18, 19, 20, 22,
    )
    assert matrix * kernel == sp.zeros(36, 18)
    assert kernel.rank() == 18
    assert (
        kernel.extract(kernel_rows, range(18)).det()
        == sp.Rational(512, 27)
    )
    assert matrix.cols - matrix.rank() == kernel.cols
    assert coefficient_column(translations[2]) == coefficient_column(
        (0, R, 0)
    )
    print(
        "PASS raw E7: rank 8/nullity 18, complete four-gauge normal"
    )


def general_e6_certificate() -> None:
    A = sp.symbols("gA")
    w1, w2, w3, w4, w5 = sp.symbols("gw1:6")
    C = sp.symbols("gC0:8")
    W = w1 * x * y + w2 * x * z + w3 * y**2 + w4 * y * z + w5 * z**2
    U = A * x * q + sp.Rational(4, 3) * x * W
    V = (
        C[0] * x**2 * z
        + C[1] * x * y**2
        + C[2] * x * y * z
        + C[3] * x * z**2
        + C[4] * y**3
        + C[5] * y**2 * z
        + C[6] * y * z**2
        + C[7] * z**3
    )
    weighted, a, b, ell, _ = weighted_data(U, V, W, "g")
    unknowns = a + b + ell
    _, _, matrix, rhs = identity_data(weighted, unknowns, 6)
    assert matrix.rank() == 4
    assert matrix.extract((0, 1, 2, 4), (0, 1, 3, 4)).det() == 648
    values = [value for _, value in cleared_left_pairs(matrix, rhs)]
    assert any(associate(value, w5**2) for value in values)
    assert any(
        associate(value.subs(w5, 0), w4**2)
        for value in values
        if not exact_zero(value.subs(w5, 0))
    )
    reduced = [
        sp.factor(value.subs({w4: 0, w5: 0}))
        for value in values
        if not exact_zero(value.subs({w4: 0, w5: 0}))
    ]
    targets = (
        9 * A * C[4] + w1 * (-3 * A + 4 * w3),
        A * C[6],
        9 * A * C[5] + (w3 - w2) * (3 * A - 4 * w3),
        A * C[7],
    )
    assert all(
        any(associate(value, target) for value in reduced)
        for target in targets
    )
    print(
        "PASS E6: w4=w5=0 and the four reduced compatibility equations"
    )


def a0_w3_open_certificate() -> None:
    s = sp.symbols("os")
    C = sp.symbols("oC0:8")
    U = sp.Rational(4, 3) * s * x * q
    V = (
        C[0] * x**2 * z
        + C[1] * x * y**2
        + C[2] * x * y * z
        + C[3] * x * z**2
        + C[4] * y**3
        + C[5] * y**2 * z
        + C[6] * y * z**2
        + C[7] * z**3
    )
    W = s * q
    weighted, a, b, ell, _ = weighted_data(U, V, W, "o")
    unknowns = a + b + ell
    _, _, matrix6, _, solution6 = solve_linear_identity(
        weighted, unknowns, 6
    )
    assert matrix6.rank() == 4
    _, _, matrix5, rhs5 = identity_data(
        weighted, unknowns, 5, solution6
    )
    values = [value for _, value in cleared_left_pairs(matrix5, rhs5)]
    targets = (
        s**2 * C[6],
        s**2 * (2 * C[2] - 3 * C[4]),
        s**2 * C[3],
        s**2 * C[5],
        s**2 * C[7],
        s**2 * C[2] * (C[2] - C[4]),
    )
    assert all(
        any(associate(value, target) for value in values)
        for target in targets
    )
    # With s != 0, these imply C2=...=C7=0: the linear relation
    # 2*C2=3*C4 and C2*(C2-C4)=0 leave only C2=C4=0.

    C0, C1 = sp.symbols("dC0 dC1")
    U0 = sp.Rational(4, 3) * s * x * q
    V0 = C0 * x**2 * z + C1 * x * y**2
    weighted0, aa, bb, ll, L0 = weighted_data(U0, V0, W, "d")
    lower0 = aa + bb + ll

    # Rank-drop D=C0-C1=0: E5 itself zeros the two right columns
    # needed for invertibility.
    equal_weighted = sp.Poly(
        weighted0.as_expr().subs(C0, C1), scale
    )
    _, _, _, _, equal6 = solve_linear_identity(
        equal_weighted, lower0, 6
    )
    _, remaining5, matrix5eq, _, equal5 = solve_linear_identity(
        equal_weighted, lower0, 5, equal6
    )
    assert matrix5eq.rank() == 4
    assert set(remaining5) == {ll[1], ll[2], ll[7], ll[8]}
    assert all(exact_zero(equal5[entry]) for entry in remaining5)
    equal_subs = compose(equal6, equal5)
    assert exact_zero(L0.det().subs(C0, C1).subs(equal_subs))

    # D != 0, r=a3 != 0.  Recompute with r external before solving:
    # the E4 pivot below proves completeness only on the r-open chart.
    D, r = sp.symbols("dD dr")
    parametrized_weighted = sp.Poly(
        weighted0.as_expr().subs({C0: C1 + D}), scale
    )
    parametrized_L = L0.subs({C0: C1 + D})
    r_weighted = sp.Poly(
        parametrized_weighted.as_expr().subs(aa[3], r), scale
    )
    r_lower = tuple(variable for variable in lower0 if variable != aa[3])
    r_subs = {aa[3]: r}
    for degree in (6, 5):
        _, _, _, _, r_solution = solve_linear_identity(
            r_weighted, r_lower, degree, r_subs
        )
        r_subs = compose(r_subs, r_solution)
    _, r_remaining4, r_matrix4, _ = identity_data(
        r_weighted, r_lower, 4, r_subs
    )
    assert r_remaining4 == (bb[1], bb[2], bb[3], bb[4], bb[5])
    assert r_matrix4.rank() == 4
    assert (
        r_matrix4.extract((0, 1, 2, 4), (0, 1, 3, 4)).det()
        == 648 * r**4
    )
    _, _, _, _, r_solution4 = solve_linear_identity(
        r_weighted, r_lower, 4, r_subs
    )
    assert exact_zero(r_solution4[bb[1]])
    assert exact_zero(r_solution4[bb[2]] - C1 * D - bb[3])
    assert exact_zero(r_solution4[bb[4]])
    assert exact_zero(r_solution4[bb[5]])
    r_subs = compose(r_subs, r_solution4)
    assert all(
        exact_zero(
            r_weighted.coeff_monomial(scale**degree).subs(r_subs)
        )
        for degree in (6, 5, 4)
    )
    E3 = sp.expand(
        r_weighted.coeff_monomial(scale**3).subs(r_subs)
    )
    assert exact_zero(
        coefficient(E3, x**2 * z) - sp.Rational(4, 3) * s**2 * ll[4]
    )
    assert exact_zero(
        coefficient(E3, x * y**2) - sp.Rational(4, 3) * s**2 * ll[4]
    )
    assert exact_zero(
        parametrized_L.det().subs(r_subs)
        - D * ll[4] * (s * ll[0] - r * ll[6])
    )

    # Fresh rank drop r=a3=0.  The r-open E4 solve above cannot be
    # specialized because its completeness minor is 648*r**4.
    zero_r_weighted = sp.Poly(
        parametrized_weighted.as_expr().subs(aa[3], 0), scale
    )
    zero_r_lower = tuple(
        variable for variable in lower0 if variable != aa[3]
    )
    zero_r_subs = {aa[3]: sp.Integer(0)}
    for degree in (6, 5):
        _, _, _, _, zero_r_solution = solve_linear_identity(
            zero_r_weighted, zero_r_lower, degree, zero_r_subs
        )
        zero_r_subs = compose(zero_r_subs, zero_r_solution)
    _, zero_r_remaining4, zero_r_matrix4, _ = identity_data(
        zero_r_weighted, zero_r_lower, 4, zero_r_subs
    )
    assert zero_r_remaining4 == (
        bb[1], bb[2], bb[3], bb[4], bb[5]
    )
    assert zero_r_matrix4.rank() == 4
    assert (
        zero_r_matrix4.extract((2, 4, 5, 8), (0, 1, 3, 4)).det()
        == sp.Rational(2048, 81) * s**8
    )
    _, _, _, _, zero_r_solution4 = solve_linear_identity(
        zero_r_weighted, zero_r_lower, 4, zero_r_subs
    )
    assert exact_zero(zero_r_solution4[bb[1]])
    assert exact_zero(zero_r_solution4[bb[2]] - C1 * D - bb[3])
    assert exact_zero(zero_r_solution4[bb[4]])
    assert exact_zero(zero_r_solution4[bb[5]])
    zero_r_subs = compose(zero_r_subs, zero_r_solution4)
    E3_zero_r = sp.expand(
        zero_r_weighted.coeff_monomial(scale**3).subs(zero_r_subs)
    )
    assert exact_zero(
        coefficient(E3_zero_r, x**2 * z)
        - sp.Rational(4, 3) * s**2 * ll[4]
    )
    assert exact_zero(
        coefficient(E3_zero_r, x * y**2)
        - sp.Rational(4, 3) * s**2 * ll[4]
    )
    assert exact_zero(
        parametrized_L.det().subs(zero_r_subs)
        - D * ll[0] * ll[4] * s
    )
    print(
        "PASS A=0,w3!=0: E5 tail collapse; D=0 exits at E5 "
        "and both D!=0 a3 charts exit at E3"
    )


def a0_origin_certificate() -> None:
    C = sp.symbols("rC0:8")
    V = (
        C[0] * x**2 * z
        + C[1] * x * y**2
        + C[2] * x * y * z
        + C[3] * x * z**2
        + C[4] * y**3
        + C[5] * y**2 * z
        + C[6] * y * z**2
        + C[7] * z**3
    )
    weighted, a, b, ell, L = weighted_data(0, V, 0, "r")
    unknowns = a + b + ell
    _, _, matrix6, _, solution6 = solve_linear_identity(
        weighted, unknowns, 6
    )
    assert matrix6.rank() == 4
    E5 = sp.expand(
        weighted.coeff_monomial(scale**5).subs(solution6)
    )
    expected = {
        x**5: 3 * ell[1],
        x**4 * y: 6 * ((C[0] - C[1]) * a[3] - ell[2]),
        x**4 * z: -3 * C[2] * a[3],
        x**3 * y**2: 3 * a[3] * (2 * C[2] - 3 * C[4]),
        x**3 * y * z: 6 * a[3] * (2 * C[3] - C[5]),
        x**3 * z**2: -3 * C[6] * a[3],
        x**2 * y**3: 6 * C[5] * a[3],
        x**2 * y**2 * z: 12 * C[6] * a[3],
        x**2 * y * z**2: 18 * C[7] * a[3],
    }
    assert all(
        exact_zero(coefficient(E5, monomial) - value)
        for monomial, value in expected.items()
    )
    assert exact_zero(
        E5 - sum(value * monomial for monomial, value in expected.items())
    )

    # Branch a3=0.
    zero_subs = compose(
        solution6, {a[3]: 0, ell[1]: 0, ell[2]: 0}
    )
    assert exact_zero(
        weighted.coeff_monomial(scale**5).subs(zero_subs)
    )
    E4zero = sp.expand(
        weighted.coeff_monomial(scale**4).subs(zero_subs)
    )
    e_square_8 = coefficient(E4zero, x**2 * y * z)
    e_square_7 = coefficient(E4zero, x**3 * y)
    assert exact_zero(e_square_8 - sp.Rational(8, 3) * ell[8] ** 2)
    assert exact_zero(
        e_square_7
        - sp.Rational(4, 3)
        * (3 * a[0] * ell[8] - 2 * ell[6] * ell[8] - ell[7] ** 2)
    )
    terminal_zero = compose(zero_subs, {ell[8]: 0, ell[7]: 0})
    assert exact_zero(L.det().subs(terminal_zero))

    # Branch a3 != 0.  The literal E5 rows force C2=...=C7=0;
    # this parametrization is the complete fresh E4 solve and remains
    # polynomial at D=C0-C1=0.
    C1, D, r = sp.symbols("sC1 sD sr")
    Vspecial = (C1 + D) * x**2 * z + C1 * x * y**2
    special, aa, bb, ll, LL = weighted_data(0, Vspecial, 0, "s")
    special_subs = {
        aa[1]: 0,
        aa[2]: r,
        aa[3]: r,
        aa[4]: 0,
        aa[5]: 0,
        bb[1]: 0,
        bb[3]: bb[2] - C1 * D,
        bb[4]: 0,
        bb[5]: 0,
        ll[1]: 0,
        ll[2]: D * r,
        ll[7]: 0,
        ll[8]: 0,
    }
    assert all(
        exact_zero(
            special.coeff_monomial(scale**degree).subs(special_subs)
        )
        for degree in (6, 5, 4)
    )
    E3special = sp.expand(
        special.coeff_monomial(scale**3).subs(special_subs)
    )
    e30 = coefficient(E3special, x**3)
    assert exact_zero(e30 + 3 * r * ll[4])
    det_special = sp.expand(LL.det().subs(special_subs))
    assert exact_zero(3 * det_special - D * ll[6] * e30)
    print(
        "PASS A=0 origin: explicit a3=0 and a3!=0 rank-drop exits"
    )


def a0_axis_reduction_and_xz_certificate() -> None:
    shear, w1, w2 = sp.symbols("sh w1 w2")
    y_image = y + shear * x
    z_image = z - 2 * shear * y - shear**2 * x
    assert exact_zero(y_image**2 + x * z_image - q)
    transformed_W = sp.expand(
        x * (w1 * y_image + w2 * z_image)
    )
    expected_W = x * (
        (w1 - 2 * shear * w2) * y
        + w2 * z
        + (shear * w1 - shear**2 * w2) * x
    )
    assert exact_zero(transformed_W - expected_W)
    open_shear = sp.Rational(1, 2) * w1 / w2
    assert exact_zero(
        coefficient(transformed_W.subs(shear, open_shear), x * y)
    )
    assert exact_zero(
        coefficient(transformed_W.subs(shear, open_shear), x**2)
        - w1**2 / (4 * w2)
    )
    tx = tuple(sp.diff(component, x) for component in (P, Q, R))
    assert all(
        exact_zero(left - right)
        for left, right in zip(
            (
                sp.Rational(4, 3) * x**3,
                0,
                x**2,
            ),
            (
                tx[0] / 3,
                tx[1] / 3
                - sp.Rational(2, 3) * x * y**2
                - x**2 * z,
                tx[2] / 3,
            ),
        )
    )

    s = sp.symbols("zs")
    C = sp.symbols("zC0:8")

    def top(
        C4_value: sp.Expr,
        C6_value: sp.Expr = C[6],
        C5_value: sp.Expr = C[5],
        C7_value: sp.Expr = C[7],
    ):
        U = sp.Rational(4, 3) * s * x**2 * z
        V = (
            C[0] * x**2 * z
            + C[1] * x * y**2
            + C[2] * x * y * z
            + C[3] * x * z**2
            + C4_value * y**3
            + C5_value * y**2 * z
            + C6_value * y * z**2
            + C7_value * z**3
        )
        return weighted_data(U, V, s * x * z, "z")

    weighted, a, b, ell, _ = top(C[4])
    unknowns = a + b + ell
    _, _, _, _, solution6 = solve_linear_identity(
        weighted, unknowns, 6
    )
    _, _, matrix5, rhs5 = identity_data(
        weighted, unknowns, 5, solution6
    )
    values = [value for _, value in cleared_left_pairs(matrix5, rhs5)]
    assert any(associate(value, C[4] * s**3) for value in values)

    # The C4=0 specialization has a fresh rank drop; recompute it rather
    # than specializing a generic pivot solve.
    weighted0, aa, bb, ll, _ = top(0)
    lower0 = aa + bb + ll
    _, _, _, _, solution60 = solve_linear_identity(
        weighted0, lower0, 6
    )
    _, _, matrix50, rhs50 = identity_data(
        weighted0, lower0, 5, solution60
    )
    values0 = [value for _, value in cleared_left_pairs(matrix50, rhs50)]
    assert any(associate(value, C[6] * s**3) for value in values0)

    weighted00, aaa, bbb, lll, _ = top(0, 0)
    lower00 = aaa + bbb + lll
    _, _, _, _, solution600 = solve_linear_identity(
        weighted00, lower00, 6
    )
    _, _, matrix500, rhs500 = identity_data(
        weighted00, lower00, 5, solution600
    )
    values00 = [value for _, value in cleared_left_pairs(matrix500, rhs500)]
    assert any(
        associate(value, s**3 * (3 * C[5] - 2 * s))
        for value in values00
    )

    weighted000, a4, b4, l4, _ = top(0, 0, sp.Rational(2, 3) * s)
    lower000 = a4 + b4 + l4
    _, _, _, _, solution6000 = solve_linear_identity(
        weighted000, lower000, 6
    )
    _, _, matrix5000, rhs5000 = identity_data(
        weighted000, lower000, 5, solution6000
    )
    values000 = [
        value for _, value in cleared_left_pairs(matrix5000, rhs5000)
    ]
    assert not values000
    _, rem5000, m5000, _, sol5000 = solve_linear_identity(
        weighted000, lower000, 5, solution6000
    )
    terminal = compose(solution6000, sol5000)
    assert m5000.rank() == 5
    E4terminal = sp.expand(
        weighted000.coeff_monomial(scale**4).subs(terminal)
    )
    assert exact_zero(
        coefficient(E4terminal, y * z**3) + sp.Rational(8, 27) * s**4
    )

    weighted0000, a5, b5, l5, _ = top(
        0, 0, sp.Rational(2, 3) * s, 0
    )
    lower0000 = a5 + b5 + l5
    _, _, _, _, solution60000 = solve_linear_identity(
        weighted0000, lower0000, 6
    )
    _, _, matrix50000, rhs50000 = identity_data(
        weighted0000, lower0000, 5, solution60000
    )
    values0000 = [
        value for _, value in cleared_left_pairs(matrix50000, rhs50000)
    ]
    assert any(associate(value, s**3) for value in values0000)
    print(
        "PASS A=0 xz axis: all E5 rank drops, then literal E4 exit"
    )


def a0_axis_xy_certificate() -> None:
    s = sp.symbols("ys")
    C = sp.symbols("yC0:8")

    def top(
        C2_value: sp.Expr = C[2],
        C3_value: sp.Expr = C[3],
        C4_value: sp.Expr = C[4],
        C5_value: sp.Expr = C[5],
        C6_value: sp.Expr = C[6],
        C7_value: sp.Expr = C[7],
        prefix: str = "y",
    ):
        U = sp.Rational(4, 3) * s * x**2 * y
        V = (
            C[0] * x**2 * z
            + C[1] * x * y**2
            + C2_value * x * y * z
            + C3_value * x * z**2
            + C4_value * y**3
            + C5_value * y**2 * z
            + C6_value * y * z**2
            + C7_value * z**3
        )
        return weighted_data(U, V, s * x * y, prefix)

    weighted, a, b, ell, _ = top()
    unknowns = a + b + ell
    _, _, _, _, solution6 = solve_linear_identity(
        weighted, unknowns, 6
    )
    _, _, matrix5, rhs5 = identity_data(
        weighted, unknowns, 5, solution6
    )
    values = [value for _, value in cleared_left_pairs(matrix5, rhs5)]
    targets = (
        s**3 * (2 * C[3] - C[5]),
        s**3 * C[6],
        s**3 * C[5],
        s**3 * C[7],
    )
    assert all(
        any(associate(value, target) for value in values)
        for target in targets
    )
    # Thus s!=0 gives C3=C5=C6=C7=0.

    # The h=2s-3C4=0 rank drop is recomputed before any localization.
    hzero, ah, bh, lh, _ = top(
        C3_value=0,
        C4_value=sp.Rational(2, 3) * s,
        C5_value=0,
        C6_value=0,
        C7_value=0,
        prefix="h",
    )
    lower_h = ah + bh + lh
    _, _, _, _, h6 = solve_linear_identity(hzero, lower_h, 6)
    _, _, h5matrix, h5rhs = identity_data(hzero, lower_h, 5, h6)
    hvalues = [value for _, value in cleared_left_pairs(h5matrix, h5rhs)]
    assert any(associate(value, s**3) for value in hvalues)

    # Work on h!=0.  This is a denominator-free chart after multiplying
    # all displayed identities by powers of h.
    h = sp.symbols("yh")
    reduced, aa, bb, ll, LL = top(
        C3_value=0,
        C4_value=(2 * s - h) / 3,
        C5_value=0,
        C6_value=0,
        C7_value=0,
        prefix="u",
    )
    k = 4 * s**3 / (3 * h)
    substitutions = {
        aa[1]: sp.Rational(4, 3) * ll[7],
        aa[3]: 2 * s**2 * (3 * h - 2 * s) / (27 * h),
        aa[2]: -k / 9 + sp.Rational(4, 3) * ll[8],
        aa[4]: 0,
        aa[5]: 0,
        ll[1]: 2 * s * (3 * aa[0] - 2 * ll[6]) / 9,
        ll[2]: -4
        * s
        * (3 * h * ll[7] + (C[0] - C[1]) * s**2)
        / (27 * h),
        ll[8]: -(2 * s - 3 * C[2]) * s**2 / (9 * h),
    }
    assert all(
        exact_zero(
            reduced.coeff_monomial(scale**degree).subs(substitutions)
        )
        for degree in (6, 5)
    )
    E4 = sp.expand(
        reduced.coeff_monomial(scale**4).subs(substitutions)
    )
    selected = (ll[0], bb[3], bb[4], bb[5])
    matrix4, rhs4 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E4, 4), selected
    )
    assert matrix4.rank() == 4
    pivot_rows = matrix4.T.rref()[1]
    assert pivot_rows == (0, 1, 2, 4)
    pivot_solution = next(
        iter(
            sp.linsolve(
                (
                    matrix4.extract(pivot_rows, range(4)),
                    rhs4.extract(pivot_rows, (0,)),
                ),
                selected,
            )
        )
    )
    substitutions = compose(
        substitutions, dict(zip(selected, pivot_solution))
    )
    E4res = sp.expand(
        reduced.coeff_monomial(scale**4).subs(substitutions)
    )
    comp_a = C[1] * s**2 * (s - h) + (3 * h**2 + 2 * s**2) * ll[7]
    comp_b = (3 * h + 2 * s) * (-6 * C[2] - 3 * h + 4 * s)
    assert exact_zero(
        E4res
        + sp.Rational(4, 9) * s * comp_a * x**2 * y**2 / h
        + sp.Rational(4, 243) * s**4 * comp_b * x * y**3 / h**2
    )

    # First E4 factor: 3h+2s=0.  The other compatibility gives
    # l7=-C1*s/2.
    first = compose(
        substitutions,
        {h: -sp.Rational(2, 3) * s, ll[7]: -C[1] * s / 2},
    )
    assert exact_zero(
        reduced.coeff_monomial(scale**4).subs(first)
    )
    E3first = sp.expand(
        reduced.coeff_monomial(scale**3).subs(first)
    )
    square_c2 = coefficient(E3first, x * z**2)
    assert exact_zero(
        square_c2
        + sp.Rational(2, 9) * s**3 * (s - C[2]) ** 2
    )
    first = compose(first, {C[2]: s})
    E3first = sp.expand(
        reduced.coeff_monomial(scale**3).subs(first)
    )
    selected3 = (bb[0], bb[2], ll[4], ll[5])
    matrix3, rhs3 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E3first, 3), selected3
    )
    assert matrix3.rank() == 3
    rows3 = matrix3.T.rref()[1]
    solution3 = next(
        iter(
            sp.linsolve(
                (
                    matrix3.extract(rows3, range(4)),
                    rhs3.extract(rows3, (0,)),
                ),
                selected3,
            )
        )
    )
    first = compose(first, dict(zip(selected3, solution3)))
    E3res = sp.factor(
        reduced.coeff_monomial(scale**3).subs(first)
    )
    assert exact_zero(
        E3res
        - sp.Rational(2, 9)
        * C[1]
        * s**3
        * (2 * C[0] - 3 * C[1])
        * x
        * y**2
    )

    # Subbranch C1=0.  E2 gives C0=0 and l6=0; E1 then gives b1=0.
    zero = compose(first, {C[1]: 0})
    E2zero = sp.expand(
        reduced.coeff_monomial(scale**2).subs(zero)
    )
    assert exact_zero(
        coefficient(E2zero, y * z)
        + sp.Rational(4, 27) * C[0] ** 2 * s**4
    )
    zero = compose(zero, {C[0]: 0})
    E2zero = sp.expand(
        reduced.coeff_monomial(scale**2).subs(zero)
    )
    assert exact_zero(
        coefficient(E2zero, x * y)
        - sp.Rational(8, 27) * s**2 * ll[6] ** 2
    )
    zero = compose(zero, {ll[6]: 0})
    E2zero = sp.expand(
        reduced.coeff_monomial(scale**2).subs(zero)
    )
    assert exact_zero(
        coefficient(E2zero, x**2)
        - s**2 * (2 * s * ll[3] - 3 * aa[0] * bb[1]) / 9
    )
    zero = compose(
        zero, {ll[3]: 3 * aa[0] * bb[1] / (2 * s)}
    )
    assert exact_zero(
        reduced.coeff_monomial(scale**2).subs(zero)
    )
    E1zero = sp.expand(
        reduced.coeff_monomial(scale).subs(zero)
    )
    assert exact_zero(
        coefficient(E1zero, x)
        + sp.Rational(2, 9) * s**3 * bb[1] ** 2
    )
    zero = compose(zero, {bb[1]: 0})
    assert exact_zero(LL.det().subs(zero))

    # Subbranch 2*C0=3*C1.  The C1=0 overlap was just handled.
    ratio = compose(first, {C[0]: sp.Rational(3, 2) * C[1]})
    E2ratio = sp.expand(
        reduced.coeff_monomial(scale**2).subs(ratio)
    )
    assert exact_zero(
        coefficient(E2ratio, x * z)
        + C[1] * s**3 * (3 * C[1] ** 2 + 4 * ll[6]) / 18
    )
    ratio = compose(
        ratio,
        {
            ll[6]: -sp.Rational(3, 4) * C[1] ** 2,
        },
    )
    E2ratio = sp.expand(
        reduced.coeff_monomial(scale**2).subs(ratio)
    )
    assert exact_zero(
        coefficient(E2ratio, x * y)
        + sp.Rational(2, 9) * bb[1] * C[1] * s**3
    )
    ratio = compose(ratio, {bb[1]: 0})
    E2ratio = sp.expand(
        reduced.coeff_monomial(scale**2).subs(ratio)
    )
    assert exact_zero(
        coefficient(E2ratio, x**2)
        - s**2 * (2 * s * ll[3] - 3 * C[1] * ll[4]) / 9
    )
    ratio = compose(
        ratio, {ll[3]: 3 * C[1] * ll[4] / (2 * s)}
    )
    assert exact_zero(
        reduced.coeff_monomial(scale**2).subs(ratio)
    )
    assert exact_zero(LL.det().subs(ratio))

    # Second E4 factor: C2=(4s-3h)/6.
    G = 3 * h**2 + 2 * s**2
    second = compose(
        substitutions, {C[2]: (4 * s - 3 * h) / 6}
    )

    # G != 0: solve the remaining compatibility.  E3 is a square
    # forcing 3h+2s=0, already covered by the first factor.
    gopen = compose(
        second,
        {ll[7]: -C[1] * s**2 * (s - h) / G},
    )
    assert exact_zero(
        reduced.coeff_monomial(scale**4).subs(gopen)
    )
    E3gopen = sp.expand(
        reduced.coeff_monomial(scale**3).subs(gopen)
    )
    assert exact_zero(
        coefficient(E3gopen, x * z**2)
        - s**4 * (3 * h + 2 * s) ** 2 / (243 * h)
    )

    # G=0: since Res_h(G,s-h)=5s^2, the E4 compatibility forces C1=0.
    assert sp.resultant(G, s - h, h) == 5 * s**2
    gzero = compose(second, {C[1]: 0})
    E4gzero = sp.expand(
        reduced.coeff_monomial(scale**4).subs(gzero)
    )
    for value in homogeneous_coefficients(E4gzero, 4):
        numerator = sp.together(value).as_numer_denom()[0]
        remainder = sp.rem(sp.Poly(numerator, h), sp.Poly(G, h)).as_expr()
        assert exact_zero(remainder)
    E3gzero = sp.expand(
        reduced.coeff_monomial(scale**3).subs(gzero)
    )
    xz2_numerator = sp.together(
        coefficient(E3gzero, x * z**2)
    ).as_numer_denom()[0]
    remainder = sp.factor(
        sp.rem(sp.Poly(xz2_numerator, h), sp.Poly(G, h)).as_expr()
    )
    assert associate(remainder, s**5 * (s - 6 * h))
    assert sp.expand(G.subs(s, 6 * h)) == 75 * h**2

    print(
        "PASS A=0 xy axis: every E5/E4 rank drop and both "
        "E4-factor descendants"
    )


def aopen_top_and_zero_certificate() -> None:
    # A != 0 is normalized to A=1 by X -> A*X and target scaling
    # diag(A^-4,A^-4,A^-3); no root extraction occurs.
    A = sp.symbols("nA", nonzero=True)
    assert exact_zero(A ** -4 * (A * x) ** 4 - P)
    scaled_Q = A ** -4 * (
        (A * x) ** 2 * ((A * y) ** 2 + (A * x) * (A * z))
    )
    assert exact_zero(scaled_Q - Q)
    assert exact_zero(A ** -3 * (A * x) ** 3 - R)
    assert exact_zero(
        A ** -4
        * (A * (A * x) * ((A * y) ** 2 + (A * x) * (A * z)))
        - x * q
    )

    w, v, s = sp.symbols("nw nv ns")
    C = sp.symbols("nC0:4")
    W = w * x * y + v * x * z + s * y**2
    U = x * q + sp.Rational(4, 3) * x * W
    V = (
        C[0] * x**2 * z
        + C[1] * x * y**2
        + C[2] * x * y * z
        + C[3] * x * z**2
        + w * (3 - 4 * s) * y**3 / 9
        + (v - s) * (3 - 4 * s) * y**2 * z / 9
    )
    weighted, a, b, ell, L = weighted_data(U, V, W, "n")
    unknowns = a + b + ell
    _, _, _, _, solution6 = solve_linear_identity(
        weighted, unknowns, 6
    )
    E5 = sp.expand(
        weighted.coeff_monomial(scale**5).subs(solution6)
    )
    assert exact_zero(
        coefficient(E5, y**5)
        - sp.Rational(2, 27)
        * s
        * (v - s)
        * (4 * s - 3)
        * (4 * s + 3)
    )

    zero_weighted = sp.Poly(weighted.as_expr().subs(s, 0), scale)
    _, _, _, _, zero6 = solve_linear_identity(
        zero_weighted, unknowns, 6
    )
    _, _, zero5matrix, zero5rhs = identity_data(
        zero_weighted, unknowns, 5, zero6
    )
    zero_values = [
        value for _, value in cleared_left_pairs(zero5matrix, zero5rhs)
    ]
    assert any(associate(value, v**2) for value in zero_values)

    axis_weighted = sp.Poly(zero_weighted.as_expr().subs(v, 0), scale)
    _, _, _, _, axis6 = solve_linear_identity(
        axis_weighted, unknowns, 6
    )
    _, _, axis5matrix, axis5rhs = identity_data(
        axis_weighted, unknowns, 5, axis6
    )
    axis_values = [
        value for _, value in cleared_left_pairs(axis5matrix, axis5rhs)
    ]
    assert any(associate(value, w * C[3]) for value in axis_values)

    # W=0: use the raw E5 rows, without localizing by any C_i.
    W0 = sp.Poly(axis_weighted.as_expr().subs(w, 0), scale)
    _, _, _, _, W06 = solve_linear_identity(W0, unknowns, 6)
    W0E5 = sp.expand(W0.coeff_monomial(scale**5).subs(W06))
    X = 3 * C[1] * C[2] - 3 * C[2] * a[3] - 3 * b[4]
    assert exact_zero(coefficient(W0E5, x**2 * y**3) + 2 * ell[8])
    assert exact_zero(coefficient(W0E5, x**4 * z) - X - ell[7])
    assert exact_zero(coefficient(W0E5, x**3 * y**2) + 2 * X - ell[7])

    H2first = sum(c * monomial for c, monomial in zip(a, mon2))
    H2second = sum(c * monomial for c, monomial in zip(b, mon2))
    F1 = P + x * q + H2first + ell[0] * x + ell[1] * y + ell[2] * z
    F2 = (
        Q
        + C[0] * x**2 * z
        + C[1] * x * y**2
        + C[2] * x * y * z
        + C[3] * x * z**2
        + H2second
        + ell[3] * x
        + ell[4] * y
        + ell[5] * z
    )
    F3 = R + ell[6] * x
    determinant = sp.Matrix([F1, F2, F3]).jacobian(variables).det()
    minor = sp.diff(F1, y) * sp.diff(F2, z) - sp.diff(F1, z) * sp.diff(F2, y)
    assert exact_zero(determinant - (3 * x**2 + ell[6]) * minor)

    # w!=0 gives C3=0.  Recompute the E5 solve on that chart.
    open_weighted = sp.Poly(
        axis_weighted.as_expr().subs({w: sp.Symbol("ww"), C[3]: 0}),
        scale,
    )
    ww = next(symbol for symbol in open_weighted.free_symbols if symbol.name == "ww")
    _, _, _, _, open6 = solve_linear_identity(
        open_weighted, unknowns, 6
    )
    _, _, _, _, open5 = solve_linear_identity(
        open_weighted, unknowns, 5, open6
    )
    open_subs = compose(open6, open5)
    E4open = sp.expand(
        open_weighted.coeff_monomial(scale**4).subs(open_subs)
    )
    e_y4 = coefficient(E4open, y**4)
    e_x2z2 = coefficient(E4open, x**2 * z**2)
    assert exact_zero(e_y4 - ww**2 * (ww - 6 * C[2]) / 3)
    assert exact_zero(
        e_x2z2
        + ww * (2 * ww - 3 * C[2]) * (ww - C[2]) / 3
    )
    assert exact_zero(
        e_x2z2.subs(C[2], ww / 6) + sp.Rational(5, 12) * ww**3
    )
    print(
        "PASS A!=0 top cover and w3=0: W=0 factor or literal E4 exit"
    )


def aopen_equal_certificate() -> None:
    w, s = sp.symbols("ew es")
    C0, C1, C2, C3 = sp.symbols("eC0 eC1 eC2 eC3")
    W = w * x * y + s * q
    U = x * q + sp.Rational(4, 3) * x * W
    V = (
        C0 * x**2 * z
        + C1 * x * y**2
        + C2 * x * y * z
        + C3 * x * z**2
        + w * (3 - 4 * s) * y**3 / 9
    )
    weighted, a, b, ell, L = weighted_data(U, V, W, "e")
    unknowns = a + b + ell
    _, _, _, _, solution6 = solve_linear_identity(
        weighted, unknowns, 6
    )
    _, _, matrix5, rhs5 = identity_data(
        weighted, unknowns, 5, solution6
    )
    values = [value for _, value in cleared_left_pairs(matrix5, rhs5)]
    assert any(
        associate(value, C3 * s * (4 * s - 3)) for value in values
    )
    assert any(
        associate(
            value,
            s * (4 * s - 3) * (6 * C2 + 4 * s * w - w),
        )
        for value in values
    )
    reduced_values = [
        sp.factor(
            value.subs({C3: 0, C2: w * (1 - 4 * s) / 6})
        )
        for value in values
    ]
    assert any(
        associate(value, s * w * (4 * s - 3) * (4 * s + 3))
        for value in reduced_values
    )

    # Away from s=0,+/-3/4 this leaves w=C2=C3=0.
    aligned = sp.Poly(
        weighted.as_expr().subs({w: 0, C2: 0, C3: 0}), scale
    )
    C, D = sp.symbols("eC eD")

    d_open = sp.Poly(
        aligned.as_expr().subs({C0: C + D, C1: C}), scale
    )
    _, _, _, _, d6 = solve_linear_identity(d_open, unknowns, 6)
    _, _, _, _, d5 = solve_linear_identity(
        d_open, unknowns, 5, d6
    )
    dsubs = compose(d6, d5)
    assert exact_zero(dsubs[ell[7]])
    assert exact_zero(dsubs[ell[8]] - s * D)
    E4d = sp.expand(d_open.coeff_monomial(scale**4).subs(dsubs))
    assert exact_zero(
        coefficient(E4d, x**3 * z) - ell[1] * s * (4 * s - 3) / 3
    )
    E4d_l1 = sp.expand(E4d.subs(ell[1], 0))
    assert exact_zero(coefficient(E4d_l1, x**4) + 3 * ell[4])
    assert exact_zero(
        L.det().subs({ell[1]: 0, ell[4]: 0, ell[7]: 0})
    )

    d_zero = sp.Poly(
        aligned.as_expr().subs({C0: C, C1: C}), scale
    )
    _, _, _, _, z6 = solve_linear_identity(d_zero, unknowns, 6)
    _, _, _, _, z5 = solve_linear_identity(
        d_zero, unknowns, 5, z6
    )
    zsubs = compose(z6, z5)
    assert exact_zero(zsubs[ell[7]])
    assert exact_zero(zsubs[ell[8]])
    E4z = sp.expand(d_zero.coeff_monomial(scale**4).subs(zsubs))
    assert exact_zero(
        coefficient(E4z, x**3 * z) - ell[1] * s * (4 * s - 3) / 3
    )
    assert exact_zero(
        coefficient(E4z, x**2 * y * z)
        + 2 * ell[2] * s * (4 * s - 3) / 3
    )
    assert exact_zero(
        L.det().subs(
            {ell[1]: 0, ell[2]: 0, ell[7]: 0, ell[8]: 0}
        )
    )
    print(
        "PASS A!=0 equal branch away from plus/minus: both D charts singular"
    )


def aopen_minus_certificate() -> None:
    w, v = sp.symbols("mw mv")
    C0, C1, C2, C3 = sp.symbols("mC0 mC1 mC2 mC3")
    W = w * x * y + v * x * z - sp.Rational(3, 4) * y**2
    U = x * q + sp.Rational(4, 3) * x * W
    V = (
        C0 * x**2 * z
        + C1 * x * y**2
        + C2 * x * y * z
        + C3 * x * z**2
        + sp.Rational(2, 3) * w * y**3
        + (sp.Rational(2, 3) * v + sp.Rational(1, 2)) * y**2 * z
    )
    weighted, a, b, ell, L = weighted_data(U, V, W, "m")
    unknowns = a + b + ell
    _, _, _, _, solution6 = solve_linear_identity(
        weighted, unknowns, 6
    )
    _, _, matrix5, rhs5 = identity_data(
        weighted, unknowns, 5, solution6
    )
    values = [value for _, value in cleared_left_pairs(matrix5, rhs5)]
    C2eq = -9 * C2 + 4 * w * v + 9 * w
    C3eq = -72 * C3 + 16 * v**2 + 72 * v + 45
    assert any(associate(value, C2eq) for value in values)
    assert any(associate(value, C3eq) for value in values)
    reduced_values = [
        sp.factor(
            value.subs(
                {
                    C2: w * (4 * v + 9) / 9,
                    C3: (16 * v**2 + 72 * v + 45) / 72,
                }
            )
        )
        for value in values
    ]
    assert any(
        associate(value, (4 * v + 3) ** 3)
        for value in reduced_values
    )

    diagonal = sp.Poly(
        weighted.as_expr().subs(
            {v: -sp.Rational(3, 4), C2: sp.Rational(2, 3) * w, C3: 0}
        ),
        scale,
    )
    C, D = sp.symbols("mC mD")

    open_d = sp.Poly(
        diagonal.as_expr().subs({w: sp.Symbol("mw0"), C0: C + D, C1: C}),
        scale,
    )
    mw0 = next(
        symbol for symbol in open_d.free_symbols if symbol.name == "mw0"
    )
    _, _, _, _, od6 = solve_linear_identity(open_d, unknowns, 6)
    _, _, _, _, od5 = solve_linear_identity(open_d, unknowns, 5, od6)
    odsubs = compose(od6, od5)
    E4od = sp.expand(open_d.coeff_monomial(scale**4).subs(odsubs))
    assert exact_zero(
        coefficient(E4od, x**2 * y * z)
        - coefficient(E4od, x * y**3)
        - sp.Rational(10, 81) * mw0**4
    )

    open_zero = sp.Poly(
        diagonal.as_expr().subs({w: mw0, C0: C, C1: C}), scale
    )
    _, _, _, _, oz6 = solve_linear_identity(open_zero, unknowns, 6)
    _, _, _, _, oz5 = solve_linear_identity(
        open_zero, unknowns, 5, oz6
    )
    ozsubs = compose(oz6, oz5)
    E4oz = sp.expand(
        open_zero.coeff_monomial(scale**4).subs(ozsubs)
    )
    assert exact_zero(
        coefficient(E4oz, x**2 * y * z)
        - coefficient(E4oz, x * y**3)
        - sp.Rational(10, 81) * mw0**4
    )

    aligned_d = sp.Poly(
        diagonal.as_expr().subs({w: 0, C0: C + D, C1: C}), scale
    )
    _, _, _, _, ad6 = solve_linear_identity(aligned_d, unknowns, 6)
    _, _, _, _, ad5 = solve_linear_identity(
        aligned_d, unknowns, 5, ad6
    )
    adsubs = compose(ad6, ad5)
    assert exact_zero(adsubs[ell[7]])
    assert exact_zero(adsubs[ell[8]] + sp.Rational(3, 4) * D)
    E4ad = sp.expand(
        aligned_d.coeff_monomial(scale**4).subs(adsubs)
    )
    assert exact_zero(
        coefficient(E4ad, x**3 * z) - sp.Rational(3, 2) * ell[1]
    )
    assert exact_zero(
        coefficient(E4ad.subs(ell[1], 0), x**4) + 3 * ell[4]
    )
    assert exact_zero(
        L.det().subs({ell[1]: 0, ell[4]: 0, ell[7]: 0})
    )

    aligned_zero = sp.Poly(
        diagonal.as_expr().subs({w: 0, C0: C, C1: C}), scale
    )
    _, _, _, _, az6 = solve_linear_identity(
        aligned_zero, unknowns, 6
    )
    _, _, _, _, az5 = solve_linear_identity(
        aligned_zero, unknowns, 5, az6
    )
    azsubs = compose(az6, az5)
    assert exact_zero(azsubs[ell[7]])
    assert exact_zero(azsubs[ell[8]])
    E4az = sp.expand(
        aligned_zero.coeff_monomial(scale**4).subs(azsubs)
    )
    assert exact_zero(
        coefficient(E4az, x**3 * z) - sp.Rational(3, 2) * ell[1]
    )
    assert exact_zero(
        coefficient(E4az, x**2 * y * z) + 3 * ell[2]
    )
    assert exact_zero(
        L.det().subs(
            {ell[1]: 0, ell[2]: 0, ell[7]: 0, ell[8]: 0}
        )
    )
    print("PASS A!=0 minus resonance: all D and w rank drops")


def aopen_plus_certificate() -> None:
    w1, w2 = sp.symbols("pw1 pw2")
    C0, C1, C2, C3 = sp.symbols("pC0 pC1 pC2 pC3")
    W = w1 * x * y + w2 * x * z + sp.Rational(3, 4) * y**2
    U = x * q + sp.Rational(4, 3) * x * W
    V = (
        C0 * x**2 * z
        + C1 * x * y**2
        + C2 * x * y * z
        + C3 * x * z**2
    )
    weighted, a, b, ell, L = weighted_data(U, V, W, "p")
    unknowns = a + b + ell
    _, _, _, _, solution6 = solve_linear_identity(
        weighted, unknowns, 6
    )
    _, _, matrix5, rhs5 = identity_data(
        weighted, unknowns, 5, solution6
    )
    values = [value for _, value in cleared_left_pairs(matrix5, rhs5)]
    assert any(associate(value, (4 * w2 - 3) ** 2) for value in values)

    diagonal = sp.Poly(
        weighted.as_expr().subs(w2, sp.Rational(3, 4)), scale
    )
    _, _, _, _, diag6 = solve_linear_identity(
        diagonal, unknowns, 6
    )
    _, _, diag5matrix, diag5rhs = identity_data(
        diagonal, unknowns, 5, diag6
    )
    diag_values = [
        value for _, value in cleared_left_pairs(diag5matrix, diag5rhs)
    ]
    assert any(associate(value, w1 * C3) for value in diag_values)
    assert any(
        associate(value, w1 * (3 * C2 + w1)) for value in diag_values
    )

    wopen = sp.Symbol("pww")
    open_weighted = sp.Poly(
        diagonal.as_expr().subs({w1: wopen, C2: -wopen / 3, C3: 0}),
        scale,
    )
    _, _, _, _, open6 = solve_linear_identity(
        open_weighted, unknowns, 6
    )
    _, _, _, _, open5 = solve_linear_identity(
        open_weighted, unknowns, 5, open6
    )
    E4open = sp.expand(
        open_weighted.coeff_monomial(scale**4).subs(
            compose(open6, open5)
        )
    )
    assert exact_zero(
        coefficient(E4open, y**3 * z) + wopen**2 / 2
    )

    zero_weighted = sp.Poly(diagonal.as_expr().subs(w1, 0), scale)
    G = sp.Symbol("pG")
    c3_weighted = sp.Poly(
        zero_weighted.as_expr().subs(C3, G), scale
    )
    _, _, _, _, c36 = solve_linear_identity(
        c3_weighted, unknowns, 6
    )
    _, _, _, _, c35 = solve_linear_identity(
        c3_weighted, unknowns, 5, c36
    )
    E4c3 = sp.expand(
        c3_weighted.coeff_monomial(scale**4).subs(
            compose(c36, c35)
        )
    )
    assert exact_zero(coefficient(E4c3, y * z**3) - 3 * G**2)

    H = sp.Symbol("pH")
    c2_weighted = sp.Poly(
        zero_weighted.as_expr().subs({C3: 0, C2: H}), scale
    )
    _, _, _, _, c26 = solve_linear_identity(
        c2_weighted, unknowns, 6
    )
    _, _, _, _, c25 = solve_linear_identity(
        c2_weighted, unknowns, 5, c26
    )
    E4c2 = sp.expand(
        c2_weighted.coeff_monomial(scale**4).subs(
            compose(c26, c25)
        )
    )
    assert exact_zero(
        coefficient(E4c2, y**3 * z) - sp.Rational(3, 2) * H**2
    )

    # Final aligned chart, D=C0-C1 != 0.
    C, D, t, r, h = sp.symbols("pC pD pt pr ph")
    aligned_d = sp.Poly(
        zero_weighted.as_expr().subs(
            {C0: C + D, C1: C, C2: 0, C3: 0}
        ),
        scale,
    )
    d_subs = {
        a[1]: sp.Rational(4, 3) * t,
        a[2]: C + D - h / D + sp.Rational(4, 3) * r,
        a[3]: C - h / D,
        a[4]: 0,
        a[5]: 0,
        b[1]: ell[1],
        b[2]: b[3] + ell[2] + h,
        b[4]: 0,
        b[5]: 0,
        ell[7]: t,
        ell[8]: r,
    }
    assert all(
        exact_zero(
            aligned_d.coeff_monomial(scale**degree).subs(d_subs)
        )
        for degree in (6, 5)
    )
    E4d = sp.expand(
        aligned_d.coeff_monomial(scale**4).subs(d_subs)
    )
    poly_P = -3 * C * D - 3 * D**2 + 4 * D * r + 6 * h
    poly_Q = -3 * C * D + 6 * D**2 - 8 * D * r + 6 * h
    poly_H = -C * D + 2 * h
    assert exact_zero(
        coefficient(E4d, x**3 * z) + t * poly_P / (3 * D)
    )
    assert exact_zero(
        coefficient(E4d, x**2 * y**2) + t * poly_Q / (3 * D)
    )
    assert exact_zero(
        coefficient(E4d, x**2 * y * z)
        + (3 * D - 4 * r) * poly_P / (6 * D)
    )
    assert exact_zero(
        coefficient(E4d, x * y**3)
        + (3 * D - 4 * r) * poly_H / (2 * D)
    )
    assert exact_zero(poly_P - poly_Q - 3 * D * (4 * r - 3 * D))

    l4_value = t * (-6 * a[0] + 4 * ell[6]) / 9 + h * ell[1] / D
    l5_value = (
        D * b[3]
        - C * h
        + h**2 / D
        + h * ell[2] / D
        + sp.Rational(2, 9) * t**2
    )
    after4 = compose(
        d_subs,
        {
            r: sp.Rational(3, 4) * D,
            ell[4]: l4_value,
            ell[5]: l5_value,
        },
    )
    E4after = sp.expand(
        aligned_d.coeff_monomial(scale**4).subs(after4)
    )
    assert exact_zero(
        coefficient(E4after, x**3 * z) + t * poly_H / D
    )
    assert exact_zero(
        coefficient(E4after, x**2 * y**2) + t * poly_H / D
    )

    # t != 0 gives H=0 and the E3 contradiction.
    topen = compose(after4, {h: C * D / 2})
    E3t = sp.expand(
        aligned_d.coeff_monomial(scale**3).subs(topen)
    )
    assert exact_zero(
        coefficient(E3t, x * y * z) + sp.Rational(2, 3) * t**2
    )

    # t=0: det L has the factor l1.  On l1!=0, E3 gives H=0;
    # E3 x^3 and E2 xz then determine a0 and l2.
    tzero = compose(after4, {t: 0})
    assert exact_zero(L.det().subs(tzero).subs(ell[1], 0))
    E3t0 = sp.expand(
        aligned_d.coeff_monomial(scale**3).subs(tzero)
    )
    assert exact_zero(
        coefficient(E3t0, x**2 * z)
        - 3 * ell[1] * poly_H / (4 * D)
    )
    a0_value = C**2 / 2 - 2 * b[3] + sp.Rational(2, 3) * ell[6]
    lower = compose(
        tzero,
        {
            h: C * D / 2,
            a[0]: a0_value,
            ell[2]: C * D / 2,
        },
    )
    E2lower = sp.expand(
        aligned_d.coeff_monomial(scale**2).subs(lower)
    )
    assert exact_zero(
        coefficient(E2lower, x * y) + sp.Rational(3, 4) * ell[1] ** 2
    )

    # Fresh D=0 chart.
    aligned_zero = sp.Poly(
        zero_weighted.as_expr().subs(
            {C0: C, C1: C, C2: 0, C3: 0}
        ),
        scale,
    )
    z_subs = {
        a[1]: sp.Rational(4, 3) * t,
        a[2]: a[3] + sp.Rational(4, 3) * r,
        a[4]: 0,
        a[5]: 0,
        b[1]: ell[1],
        b[2]: b[3] + ell[2],
        b[4]: 0,
        b[5]: 0,
        ell[7]: t,
        ell[8]: r,
    }
    assert all(
        exact_zero(
            aligned_zero.coeff_monomial(scale**degree).subs(z_subs)
        )
        for degree in (6, 5)
    )
    E4z = sp.expand(
        aligned_zero.coeff_monomial(scale**4).subs(z_subs)
    )
    alpha = C - 2 * a[3]
    assert exact_zero(
        coefficient(E4z, x**3 * z) + t * (3 * alpha + 4 * r) / 3
    )
    assert exact_zero(
        coefficient(E4z, x**2 * y**2) + t * (3 * alpha - 8 * r) / 3
    )
    assert exact_zero(
        coefficient(E4z, x**2 * y * z)
        - 2 * r * (3 * alpha + 4 * r) / 3
    )
    assert exact_zero(
        coefficient(E4z, x * y**3) - 2 * r * alpha
    )
    zl4 = (C - a[3]) * ell[1] + t * (-6 * a[0] + 4 * ell[6]) / 9
    zl5 = (C - a[3]) * ell[2] + sp.Rational(2, 9) * t**2
    zafter = compose(
        z_subs, {r: 0, ell[4]: zl4, ell[5]: zl5}
    )
    assert exact_zero(L.det().subs(zafter).subs(t, 0))
    ztopen = compose(zafter, {a[3]: C / 2})
    E3zt = sp.expand(
        aligned_zero.coeff_monomial(scale**3).subs(ztopen)
    )
    assert exact_zero(
        coefficient(E3zt, x * y * z) + sp.Rational(2, 3) * t**2
    )
    print("PASS A!=0 plus resonance: every open and aligned D chart")


if __name__ == "__main__":
    raw_e7_certificate()
    general_e6_certificate()
    a0_w3_open_certificate()
    a0_origin_certificate()
    a0_axis_reduction_and_xz_certificate()
    a0_axis_xy_certificate()
    aopen_top_and_zero_certificate()
    aopen_equal_certificate()
    aopen_minus_certificate()
    aopen_plus_certificate()
    print("all rank-one e=2 triple-companion certificates passed")
