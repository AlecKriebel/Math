#!/usr/bin/env python3
"""Exact candidate exclusion certificate for canonical D4-SF-21C."""

from __future__ import annotations

import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, w = sp.symbols("p q r w")
coords = (p, q, r)
root = sp.sqrt(-5)


def jac2(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p))


def exponents(degree):
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def coefficients(poly, degree):
    pp = sp.Poly(sp.expand(poly), p, q, r)
    return {
        exponent: pp.coeff_monomial(
            p ** exponent[0] * q ** exponent[1] * r ** exponent[2]
        )
        for exponent in exponents(degree)
    }


def binary_coefficients(poly, degree):
    pp = sp.Poly(sp.expand(poly), p, q)
    return tuple(
        pp.coeff_monomial(p ** (degree - j) * q**j)
        for j in range(degree + 1)
    )


def syzygy_basis(alpha, beta, gamma, degree):
    avars = sp.symbols(f"sa{degree}_0:{degree + 1}")
    bvars = sp.symbols(f"sb{degree}_0:{degree + 1}")
    cvars = sp.symbols(f"sc{degree}_0:{degree}")
    aa = sum(avars[j] * p ** (degree - j) * q**j for j in range(degree + 1))
    bb = sum(bvars[j] * p ** (degree - j) * q**j for j in range(degree + 1))
    cc = sum(cvars[j] * p ** (degree - 1 - j) * q**j for j in range(degree))
    variables = avars + bvars + cvars
    matrix, rhs = sp.linear_eq_to_matrix(
        binary_coefficients(alpha * aa + beta * bb + gamma * cc, 5 + degree),
        variables,
    )
    assert rhs == sp.zeros(matrix.rows, 1)
    triples = []
    for vector in matrix.nullspace():
        substitution = dict(zip(variables, vector))
        triples.append(
            (
                sp.expand(aa.subs(substitution)),
                sp.expand(bb.subs(substitution)),
                sp.expand(cc.subs(substitution)),
            )
        )
    return tuple(triples)


def solve_linear(equations, variables):
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    assert matrix.rank() == matrix.row_join(rhs).rank()
    solution = tuple(next(iter(sp.linsolve((matrix, rhs), variables))))
    substitution = dict(zip(variables, solution))
    assert all(sp.cancel(equation.subs(substitution)) == 0 for equation in equations)
    return matrix, solution, substitution


def solve_linear_by_pivots(
    equations, variables, expected_rank, rank_probe=None
):
    """Solve only a certified pivot block, leaving all other variables free."""
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    probe = matrix if rank_probe is None else matrix.subs(rank_probe)
    pivot_columns = tuple(probe.rref()[1])
    pivot_rows = tuple(probe.T.rref()[1])
    assert len(pivot_columns) == expected_rank
    assert len(pivot_rows) == expected_rank
    free_columns = tuple(
        index for index in range(len(variables)) if index not in pivot_columns
    )
    pivot_matrix = matrix.extract(pivot_rows, pivot_columns)
    free_matrix = matrix.extract(pivot_rows, free_columns)
    free_vector = sp.Matrix([variables[index] for index in free_columns])
    effective_rhs = rhs.extract(pivot_rows, (0,)) - free_matrix * free_vector
    pivot_values = pivot_matrix.inv() * effective_rhs
    substitution = {
        variables[column]: sp.cancel(pivot_values[index])
        for index, column in enumerate(pivot_columns)
    }
    solution = tuple(sp.cancel(variable.subs(substitution)) for variable in variables)
    assert all(
        sp.cancel(equation.subs(substitution)) == 0 for equation in equations
    )
    return matrix, solution, substitution, pivot_rows, pivot_columns


X = p - root * q
Y = root * p - q
h = sp.expand(X * Y)
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand(X**2 * Y)
alpha = jac2(Q, R)
beta = -jac2(P, R)
gamma = jac2(P, Q)


def check_incidence():
    gcd = sp.gcd(
        sp.gcd(sp.Poly(alpha, p, q, extension=root), sp.Poly(beta, p, q, extension=root)),
        sp.Poly(gamma, p, q, extension=root),
    )
    assert gcd.total_degree() == 4
    expected_gcd = sp.Poly(sp.expand(p * X**2 * Y), p, q, extension=root)
    assert gcd.exquo(expected_gcd).as_expr().free_symbols == set()
    assert sp.Matrix([binary_coefficients(alpha, 5), binary_coefficients(beta, 5)]).rank() == 2
    print("D4_SF_21C_INCIDENCE_PASS")


def build_full_determinant():
    sx = syzygy_basis(alpha, beta, gamma, 1)
    sy = syzygy_basis(alpha, beta, gamma, 2)
    assert len(sx) == 2 and len(sy) == 4

    x = sp.symbols("x0:2")
    y = sp.symbols("y0:4")
    U2 = sum(x[index] * sx[index][0] for index in range(2))
    V2 = sum(x[index] * sx[index][1] for index in range(2))
    T2 = sum(x[index] * sx[index][2] for index in range(2))
    U1 = sum(y[index] * sy[index][0] for index in range(4))
    V1 = sum(y[index] * sy[index][1] for index in range(4))
    T1 = sum(y[index] * sy[index][2] for index in range(4))

    mon3 = (p**3, p**2 * q, p * q**2, q**3)
    mon2 = (p**2, p * q, p * r, q**2, q * r, r**2)
    mon2_binary = (p**2, p * q, q**2)
    u = sp.symbols("u0:4")
    v = sp.symbols("v0:4")
    t = sp.symbols("t0:3")
    a = sp.symbols("a0:6")
    b = sp.symbols("b0:6")
    ell = sp.symbols("l0:9")

    U0 = sum(u[index] * mon3[index] for index in range(4))
    V0 = sum(v[index] * mon3[index] for index in range(4))
    T0 = sum(t[index] * mon2_binary[index] for index in range(3))
    A = sum(a[index] * mon2[index] for index in range(6))
    B = sum(b[index] * mon2[index] for index in range(6))
    linear = sp.Matrix(3, 3, ell)

    H2 = sp.Matrix(
        [
            A,
            B,
            T0 + r * T1 + sp.Rational(1, 2) * r**2 * T2,
        ]
    )
    H3 = sp.Matrix(
        [
            U0 + r * U1 + sp.Rational(1, 2) * r**2 * U2,
            V0 + r * V1 + sp.Rational(1, 2) * r**2 * V2,
            R,
        ]
    )
    H4 = sp.Matrix([P, Q, 0])
    determinant = sp.Poly(
        sp.expand(
            (
                linear
                + w * H2.jacobian(coords)
                + w**2 * H3.jacobian(coords)
                + w**3 * H4.jacobian(coords)
            ).det()
        ),
        w,
    )
    assert all(determinant.coeff_monomial(w**degree) == 0 for degree in (9, 8, 7))
    variables = (a[2], a[4], a[5], b[2], b[4], b[5], ell[8]) + u + v + t
    return {
        "determinant": determinant,
        "x": x,
        "y": y,
        "variables": variables,
        "a": a,
        "b": b,
        "ell": ell,
    }


def check_contact_and_lower():
    data = build_full_determinant()
    determinant = data["determinant"]
    x0, x1 = data["x"]
    y0, y1, y2, y3 = data["y"]
    variables = data["variables"]
    b, ell = data["b"], data["ell"]

    e6_general = coefficients(determinant.coeff_monomial(w**6), 6)
    high_x = tuple(
        value
        for exponent, value in e6_general.items()
        if exponent[2] == 3 and value != 0
    )
    x_basis = sp.groebner(
        high_x, x0, x1, extension=root, order="lex"
    )
    expected_x = (x0**2, x0 * x1, x1**2)
    assert all(x_basis.reduce(value)[1] == 0 for value in expected_x)
    expected_x_basis = sp.groebner(
        expected_x, x0, x1, extension=root, order="lex"
    )
    assert all(expected_x_basis.reduce(value)[1] == 0 for value in high_x)

    x_zero = {x0: 0, x1: 0}
    e6_xzero = tuple(value.subs(x_zero) for value in e6_general.values())
    matrix_y, rhs_y = sp.linear_eq_to_matrix(e6_xzero, variables)
    nonzero_rows = tuple(
        index
        for index in range(matrix_y.rows)
        if any(matrix_y[index, column] != 0 for column in range(matrix_y.cols))
        or rhs_y[index] != 0
    )
    reduced_matrix = matrix_y.extract(nonzero_rows, range(matrix_y.cols))
    reduced_rhs = rhs_y.extract(nonzero_rows, (0,))
    assert reduced_matrix.shape == (13, 18)
    assert reduced_matrix.rank() == 9
    compatibility = []
    for left in reduced_matrix.T.nullspace():
        numerator = sp.factor(
            sp.together((left.T * reduced_rhs)[0]).as_numer_denom()[0],
            extension=root,
        )
        if numerator != 0:
            compatibility.append(numerator)
    assert len(compatibility) == 4

    y_groebner = sp.groebner(
        compatibility, y0, y1, y2, y3, extension=root, order="grevlex"
    )
    force_y1 = (15 * y1 - 4 * root * y3) ** 2
    force_y2 = (5 * y2 - root * y3) ** 2
    assert y_groebner.reduce(force_y1)[1] == 0
    assert y_groebner.reduce(force_y2)[1] == 0

    m, n = sp.symbols("m n")
    contact = {
        x0: 0,
        x1: 0,
        y0: m,
        y1: 4 * root * n / 15,
        y2: root * n / 5,
        y3: n,
    }
    assert all(sp.factor(value.subs(contact), extension=root) == 0 for value in compatibility)
    print("D4_SF_21C_CONTACT_PLANE_PASS")

    contact_determinant = sp.Poly(sp.expand(determinant.as_expr().subs(contact)), w)
    e6 = coefficients(contact_determinant.coeff_monomial(w**6), 6)
    e6_equations = tuple(e6.values())
    (
        matrix6,
        generic_solution,
        generic_substitution,
        pivot_rows,
        pivot_columns,
    ) = solve_linear_by_pivots(
        e6_equations, variables, expected_rank=7, rank_probe={m: 1, n: 0}
    )
    pivot_determinant = sp.factor(
        matrix6.extract(pivot_rows, pivot_columns).det(), extension=root
    )
    rank_factor = (m - n / 3) * (m + n / 6)
    assert sp.cancel(pivot_determinant / rank_factor).free_symbols == set()

    raw_e5 = coefficients(contact_determinant.coeff_monomial(w**5), 5)
    generic_e5 = {
        exponent: sp.cancel(raw_e5[exponent].subs(generic_substitution))
        for exponent in ((2, 1, 2), (1, 2, 2))
    }
    f = 135 * m**3 + 135 * m**2 * n - 9 * m * n**2 + n**3
    g = 135 * m**3 + 18 * m * n**2 - 2 * n**3
    assert sp.simplify(generic_e5[(2, 1, 2)] - 8 * root * f / 225) == 0
    assert sp.simplify(generic_e5[(1, 2, 2)] + 4 * g / 45) == 0
    assert sp.factor(sp.resultant(f, g, m)) == -1793613375 * n**9
    assert sp.factor(sp.resultant(f, g, n)) == 1793613375 * m**9

    boundary_data = (
        ({m: 1, n: 3}, (3, 0, 2), -sp.Rational(108, 5)),
        ({m: -1, n: 6}, (3, 0, 2), -sp.Rational(108, 5)),
    )
    for specialization, exponent, expected in boundary_data:
        boundary_e6 = tuple(value.subs(specialization) for value in e6_equations)
        (
            boundary_matrix,
            _,
            boundary_substitution,
            _,
            _,
        ) = solve_linear_by_pivots(
            boundary_e6, variables, expected_rank=6
        )
        obstruction = sp.simplify(
            raw_e5[exponent].subs(specialization).subs(boundary_substitution)
        )
        assert obstruction == expected

    zero = {m: 0, n: 0}
    zero_e6 = tuple(value.subs(zero) for value in e6_equations)
    (
        zero_matrix,
        zero_solution,
        zero_substitution,
        _,
        _,
    ) = solve_linear_by_pivots(zero_e6, variables, expected_rank=5)
    raw_e4 = coefficients(contact_determinant.coeff_monomial(w**4), 4)
    zero_e4 = {
        exponent: sp.factor(
            raw_e4[exponent].subs(zero).subs(zero_substitution), extension=root
        )
        for exponent in ((3, 0, 1), (2, 1, 1))
    }
    assert zero_e4[(3, 0, 1)] == 12 * b[4] ** 2
    assert sp.factor(
        zero_e4[(2, 1, 1)].subs({b[4]: 0})
        - sp.Rational(8, 3) * root * ell[8] ** 2,
        extension=root,
    ) == 0

    descended = dict(zip(variables, zero_solution))
    forced = {b[4]: 0, ell[8]: 0}
    nonbinary_quadratic = (
        data["a"][2],
        data["a"][4],
        data["a"][5],
        b[2],
        b[4],
        b[5],
    )
    assert all(
        sp.factor(descended[variable].subs(forced), extension=root) == 0
        for variable in nonbinary_quadratic
    )
    print("D4_SF_21C_E5_E4_DESCENT_PASS")


def main():
    check_incidence()
    check_contact_and_lower()
    print("D4_SF_21C_SYMPY_STRICT_PASS")


if __name__ == "__main__":
    main()
