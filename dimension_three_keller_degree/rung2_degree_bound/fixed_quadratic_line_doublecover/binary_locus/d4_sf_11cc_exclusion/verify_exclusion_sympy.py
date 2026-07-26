#!/usr/bin/env python3
"""Exact exclusion certificate for the canonical D4-SF-11CC family.

The script reconstructs the relevant weighted determinant identities from
scratch.  It first proves that the full E6 contact variety is one plane,
then shows that E5 collapses that plane to the origin, and finally shows
that E4 removes every nonbinary quadratic coefficient.
"""

from __future__ import annotations

import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, w = sp.symbols("p q r w")
coords = (p, q, r)


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


def syzygy_nullity(alpha, beta, gamma, degree):
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
    return len(variables) - matrix.rank()


def solve_linear(equations, variables):
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    assert matrix.rank() == matrix.row_join(rhs).rank()
    solution = tuple(next(iter(sp.linsolve((matrix, rhs), variables))))
    substitution = dict(zip(variables, solution))
    assert all(sp.cancel(equation.subs(substitution)) == 0 for equation in equations)
    return matrix.rank(), solution, substitution


h = p**2 - 4 * p * q + q**2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand(h * (p + q))
alpha = jac2(Q, R)
beta = -jac2(P, R)
gamma = jac2(P, Q)


def check_incidence():
    gcd = sp.gcd(
        sp.gcd(sp.Poly(alpha, p, q), sp.Poly(beta, p, q)),
        sp.Poly(gamma, p, q),
    )
    assert sp.cancel(gcd.as_expr() / (2 * p * q * h)).free_symbols == set()
    assert gcd.total_degree() == 4
    assert sp.Matrix([binary_coefficients(alpha, 5), binary_coefficients(beta, 5)]).rank() == 2
    assert syzygy_nullity(alpha, beta, gamma, 1) == 2
    assert syzygy_nullity(alpha, beta, gamma, 2) == 4
    print("D4_SF_11CC_INCIDENCE_PASS")


sx = (
    (-(3 * p - q) / 3, -(p - 3 * q) / 3, 0),
    ((15 * p - 4 * q) / 9, p / 9, 1),
)
sy = (
    (-p * (3 * p - q) / 3, -p * (p - 3 * q) / 3, 0),
    (-(p + 3 * q) * (3 * p - q) / 9, -(p - 3 * q) * (p + 3 * q) / 9, 0),
    (p * (15 * p - 4 * q) / 9, p**2 / 9, p),
    ((3 * p**2 + 44 * p * q - 12 * q**2) / 27, p**2 / 27, q),
)


def check_contact_plane():
    for triple in sx + sy:
        assert sp.factor(alpha * triple[0] + beta * triple[1] + gamma * triple[2]) == 0

    x0, x1 = sp.symbols("x0 x1")
    y0, y1, y2, y3 = sp.symbols("y0 y1 y2 y3")
    xs, ys = (x0, x1), (y0, y1, y2, y3)

    U2 = sum(xs[index] * sx[index][0] for index in range(2))
    V2 = sum(xs[index] * sx[index][1] for index in range(2))
    T2 = sum(xs[index] * sx[index][2] for index in range(2))
    U1 = sum(ys[index] * sy[index][0] for index in range(4))
    V1 = sum(ys[index] * sy[index][1] for index in range(4))
    T1 = sum(ys[index] * sy[index][2] for index in range(4))

    bu = sp.symbols("bu0:4")
    bv = sp.symbols("bv0:4")
    bt = sp.symbols("bt0:3")
    binary_cubics = (p**3, p**2 * q, p * q**2, q**3)
    binary_quadratics = (p**2, p * q, q**2)
    U0 = sum(bu[index] * binary_cubics[index] for index in range(4))
    V0 = sum(bv[index] * binary_cubics[index] for index in range(4))
    T0 = sum(bt[index] * binary_quadratics[index] for index in range(3))
    U = sp.expand(U0 + r * U1 + sp.Rational(1, 2) * r**2 * U2)
    V = sp.expand(V0 + r * V1 + sp.Rational(1, 2) * r**2 * V2)
    T = sp.expand(T0 + r * T1 + sp.Rational(1, 2) * r**2 * T2)

    aa0, aa1, aa2, bb0, bb1, bb2, l33 = sp.symbols(
        "aa0 aa1 aa2 bb0 bb1 bb2 l33"
    )
    A = r * (aa0 * p + aa1 * q) + aa2 * r**2
    B = r * (bb0 * p + bb1 * q) + bb2 * r**2
    linear = sp.zeros(3)
    linear[2, 2] = l33
    determinant = sp.Poly(
        sp.expand(
            (
                linear
                + w * sp.Matrix([A, B, T]).jacobian(coords)
                + w**2 * sp.Matrix([U, V, R]).jacobian(coords)
                + w**3 * sp.Matrix([P, Q, 0]).jacobian(coords)
            ).det()
        ),
        w,
    )
    assert determinant.coeff_monomial(w**7) == 0
    e6 = coefficients(determinant.coeff_monomial(w**6), 6)
    ordered = tuple(e6[exponent] for exponent in exponents(6))

    force_x0 = sp.factor(sp.Rational(27, 4) * ordered[9])
    force_x1 = sp.factor(27 * ordered[9] + sp.Rational(27, 4) * ordered[13])
    force_y0 = sp.factor(sp.Rational(243, 8) * ordered[2])
    force_y1 = sp.factor(
        189 * ordered[2]
        + sp.Rational(405, 8) * ordered[4]
        + sp.Rational(27, 2) * ordered[7]
        + sp.Rational(27, 8) * ordered[11]
    )
    assert sp.factor(force_x0 - (3 * x0 - x1) ** 2) == 0
    assert sp.factor(force_x1 - (3 * x0 - 4 * x1) ** 2) == 0
    x_zero = {x0: 0, x1: 0}
    assert sp.factor(
        force_y0.subs(x_zero) - (9 * y0 + 3 * y1 - 3 * y2 - y3) ** 2
    ) == 0
    assert sp.factor(force_y1.subs(x_zero) - (3 * y1 - 4 * y3) ** 2) == 0

    plane = {
        x0: 0,
        x1: 0,
        y0: (y2 - y3) / 3,
        y1: sp.Rational(4, 3) * y3,
        aa0: 0,
        aa1: 0,
        aa2: -(y2**2 + 3 * y3**2) / 36,
        bb0: 0,
        bb1: 0,
        bb2: -(3 * y2**2 + y3**2) / 36,
        l33: 0,
    }
    plane.update({variable: 0 for variable in bu + bv + bt})
    assert all(sp.factor(value.subs(plane)) == 0 for value in ordered)

    expected_u = p * (4 * y2 * p - y2 * q + y3 * q) / 3
    expected_v = q * (y2 * p - y3 * p + 4 * y3 * q) / 3
    expected_t = y2 * p + y3 * q
    assert sp.factor(U1.subs(plane) - expected_u) == 0
    assert sp.factor(V1.subs(plane) - expected_v) == 0
    assert sp.factor(T1.subs(plane) - expected_t) == 0
    print("D4_SF_11CC_CONTACT_PLANE_PASS")


def check_lower_descent():
    m, n = sp.symbols("m n")
    u = sp.symbols("u0:4")
    v = sp.symbols("v0:4")
    t = sp.symbols("t0:3")
    a = sp.symbols("a0:6")
    b = sp.symbols("b0:6")
    ell = sp.symbols("l0:9")

    mon3 = (p**3, p**2 * q, p * q**2, q**3)
    mon2 = (p**2, p * q, p * r, q**2, q * r, r**2)
    mon2_binary = (p**2, p * q, q**2)
    U0 = sum(u[index] * mon3[index] for index in range(4))
    V0 = sum(v[index] * mon3[index] for index in range(4))
    T0 = sum(t[index] * mon2_binary[index] for index in range(3))
    A = sum(a[index] * mon2[index] for index in range(6))
    B = sum(b[index] * mon2[index] for index in range(6))
    linear = sp.Matrix(3, 3, ell)

    U1 = p * (4 * m * p - m * q + n * q) / 3
    V1 = q * (m * p - n * p + 4 * n * q) / 3
    T1 = m * p + n * q
    H2 = sp.Matrix([A, B, T0 + r * T1])
    H3 = sp.Matrix([U0 + r * U1, V0 + r * V1, R])
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

    e6 = coefficients(determinant.coeff_monomial(w**6), 6)
    solve_variables = (
        a[2],
        a[4],
        a[5],
        b[2],
        b[4],
        b[5],
        ell[8],
    ) + u + v + t
    e6_equations = tuple(e6.values())
    matrix6, _ = sp.linear_eq_to_matrix(e6_equations, solve_variables)
    rank6, solution6, substitution6 = solve_linear(e6_equations, solve_variables)
    assert rank6 == 7
    pivot_rows = (1, 3, 4, 6, 7, 10, 15)
    pivot_columns = (0, 1, 2, 3, 5, 7, 8)
    rank_drop = m**2 - 4 * m * n + n**2
    pivot_determinant = sp.factor(
        matrix6.extract(pivot_rows, pivot_columns).det()
    )
    assert sp.cancel(pivot_determinant / rank_drop).free_symbols == set(), (
        pivot_determinant,
        rank_drop,
    )
    assert pivot_determinant.subs({m: 1, n: 0}) != 0

    raw_e5 = coefficients(determinant.coeff_monomial(w**5), 5)
    e5 = {
        exponent: sp.factor(value.subs(substitution6))
        for exponent, value in raw_e5.items()
    }
    f = 7 * m**3 - 6 * m**2 * n + 3 * m * n**2 - 2 * n**3
    g = 2 * m**3 - 3 * m**2 * n + 6 * m * n**2 - 7 * n**3
    assert sp.factor(e5[(2, 1, 2)] + sp.Rational(4, 9) * f) == 0
    assert sp.factor(e5[(1, 2, 2)] - sp.Rational(4, 9) * g) == 0
    assert sp.factor(sp.resultant(f, g, m)) == -46656 * n**9
    assert sp.factor(sp.resultant(f, g, n)) == 46656 * m**9

    root3 = sp.sqrt(3)
    conic_contact = {m: 2 + root3, n: 1}
    conic_e6 = tuple(value.subs(conic_contact) for value in e6_equations)
    conic_rank, conic_solution, conic_substitution = solve_linear(
        conic_e6, solve_variables
    )
    assert conic_rank == 6
    conic_first = sp.simplify(
        raw_e5[(2, 1, 2)].subs(conic_contact).subs(conic_substitution)
    )
    conic_second = sp.simplify(
        raw_e5[(1, 2, 2)].subs(conic_contact).subs(conic_substitution)
    )
    assert conic_first == -64 - sp.Rational(112, 3) * root3
    assert conic_second == 16 + sp.Rational(32, 3) * root3
    assert conic_first != 0 and conic_second != 0

    zero_contact = {m: 0, n: 0}
    zero_e6 = tuple(value.subs(zero_contact) for value in e6_equations)
    zero_rank, zero_solution, zero_substitution = solve_linear(
        zero_e6, solve_variables
    )
    assert zero_rank == 5
    raw_e4 = coefficients(determinant.coeff_monomial(w**4), 4)
    zero_e4 = {
        exponent: sp.factor(
            value.subs(zero_contact).subs(zero_substitution)
        )
        for exponent, value in raw_e4.items()
    }
    assert zero_e4[(3, 0, 1)] == sp.Rational(8, 27) * (
        3 * b[4] - ell[8]
    ) ** 2
    assert zero_e4[(0, 3, 1)] == sp.Rational(8, 27) * (
        3 * b[4] - 4 * ell[8]
    ) ** 2

    forced_zero = {b[4]: 0, ell[8]: 0}
    nonbinary_quadratic = (a[2], a[4], a[5], b[2], b[4], b[5])
    descended_solution = dict(zip(solve_variables, zero_solution))
    assert all(
        sp.factor(descended_solution[variable].subs(forced_zero)) == 0
        for variable in nonbinary_quadratic
    )
    print("D4_SF_11CC_E5_E4_DESCENT_PASS")


def main():
    check_incidence()
    check_contact_plane()
    check_lower_descent()
    print("D4_SF_11CC_SYMPY_STRICT_PASS")


if __name__ == "__main__":
    main()
