#!/usr/bin/env python3
"""Independent hostile reconstruction of the D4-SF-11CC exclusion.

This does not import the primary verifier.  Its contact-plane necessity
proof uses a constant 5-by-5 pivot and residual equations, rather than the
coefficient combinations used in the primary certificate.
"""

from __future__ import annotations

import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, w = sp.symbols("p q r w")
coordinates = (p, q, r)


def jac2(first: sp.Expr, second: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.diff(first, p) * sp.diff(second, q)
        - sp.diff(first, q) * sp.diff(second, p)
    )


def exponents(degree: int) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def coefficients(polynomial: sp.Expr, degree: int) -> tuple[sp.Expr, ...]:
    expanded = sp.Poly(sp.expand(polynomial), p, q, r)
    return tuple(
        expanded.coeff_monomial(p**i * q**j * r**k)
        for i, j, k in exponents(degree)
    )


def binary_coefficients(polynomial: sp.Expr, degree: int) -> tuple[sp.Expr, ...]:
    expanded = sp.Poly(sp.expand(polynomial), p, q)
    return tuple(
        expanded.coeff_monomial(p ** (degree - j) * q**j)
        for j in range(degree + 1)
    )


def syzygy_nullity(
    alpha: sp.Expr, beta: sp.Expr, gamma: sp.Expr, degree: int
) -> int:
    avars = sp.symbols(f"ha{degree}_0:{degree + 1}")
    bvars = sp.symbols(f"hb{degree}_0:{degree + 1}")
    cvars = sp.symbols(f"hc{degree}_0:{degree}")
    first = sum(
        avars[j] * p ** (degree - j) * q**j for j in range(degree + 1)
    )
    second = sum(
        bvars[j] * p ** (degree - j) * q**j for j in range(degree + 1)
    )
    third = sum(
        cvars[j] * p ** (degree - 1 - j) * q**j for j in range(degree)
    )
    variables = avars + bvars + cvars
    matrix, rhs = sp.linear_eq_to_matrix(
        binary_coefficients(alpha * first + beta * second + gamma * third, 5 + degree),
        variables,
    )
    assert rhs == sp.zeros(matrix.rows, 1)
    return len(variables) - matrix.rank()


def exact_linear_solution(
    equations: tuple[sp.Expr, ...], variables: tuple[sp.Symbol, ...]
) -> tuple[int, dict[sp.Symbol, sp.Expr]]:
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    rank = matrix.rank()
    assert rank == matrix.row_join(rhs).rank()
    solution = tuple(next(iter(sp.linsolve((matrix, rhs), variables))))
    substitution = dict(zip(variables, solution))
    assert all(sp.cancel(equation.subs(substitution)) == 0 for equation in equations)
    return rank, substitution


def has_scalar_associate(
    polynomials: tuple[sp.Expr, ...], target: sp.Expr
) -> bool:
    for polynomial in polynomials:
        if polynomial == 0:
            continue
        quotient = sp.cancel(polynomial / target)
        if quotient != 0 and not quotient.free_symbols:
            return True
    return False


def quotient_reduce(expression: sp.Expr, variable: sp.Symbol, modulus: sp.Expr) -> sp.Expr:
    numerator, denominator = sp.fraction(sp.cancel(expression))
    reduced_numerator = sp.Poly(numerator, variable).rem(
        sp.Poly(modulus, variable)
    ).as_expr()
    reduced_denominator = sp.Poly(denominator, variable).rem(
        sp.Poly(modulus, variable)
    ).as_expr()
    return sp.cancel(reduced_numerator / reduced_denominator)


def check_orbit_normalization() -> None:
    rho = sp.symbols("rho")
    modulus = rho**2 - 4 * rho + 1
    rho_inverse = 4 - rho
    z = rho**2
    canonical_h = (p - rho * q) * (p - rho_inverse * q)
    canonical_residual = (z + 1) * p + 4 * rho * q

    assert quotient_reduce(rho * rho_inverse - 1, rho, modulus) == 0
    assert quotient_reduce(z**2 - 14 * z + 1, rho, modulus) == 0
    assert quotient_reduce(
        canonical_h - (p**2 - 4 * p * q + q**2), rho, modulus
    ) == 0
    assert quotient_reduce(
        canonical_residual - 4 * rho * (p + q), rho, modulus
    ) == 0

    # The other square-root sign is obtained by q -> -q.
    negative_rho = -rho
    negative_h = (p - negative_rho * q) * (
        p + rho_inverse * q
    )
    negative_residual = (negative_rho**2 + 1) * p + 4 * negative_rho * q
    assert quotient_reduce(
        negative_h.subs(q, -q) - canonical_h, rho, modulus
    ) == 0
    assert quotient_reduce(
        negative_residual.subs(q, -q) - canonical_residual,
        rho,
        modulus,
    ) == 0

    # Meanwhile rho -> rho^-1 preserves h and changes the residual only by a
    # unit, so the two roots of z^2-14z+1 are not separate orbits.
    reciprocal_residual = (rho ** (-2) + 1) * p + 4 * rho ** (-1) * q
    assert quotient_reduce(
        reciprocal_residual
        - rho ** (-2) * canonical_residual,
        rho,
        modulus,
    ) == 0
    print("D4_SF_11CC_HOSTILE_ORBIT_NORMALIZATION_PASS")


h = p**2 - 4 * p * q + q**2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand(h * (p + q))
alpha = jac2(Q, R)
beta = -jac2(P, R)
gamma = jac2(P, Q)

sx = (
    (-(3 * p - q) / 3, -(p - 3 * q) / 3, 0),
    ((15 * p - 4 * q) / 9, p / 9, 1),
)
sy = (
    (-p * (3 * p - q) / 3, -p * (p - 3 * q) / 3, 0),
    (
        -(p + 3 * q) * (3 * p - q) / 9,
        -(p - 3 * q) * (p + 3 * q) / 9,
        0,
    ),
    (p * (15 * p - 4 * q) / 9, p**2 / 9, p),
    ((3 * p**2 + 44 * p * q - 12 * q**2) / 27, p**2 / 27, q),
)

x0, x1 = sp.symbols("x0 x1")
y0, y1, y2, y3 = sp.symbols("y0 y1 y2 y3")
contact_variables = (x0, x1, y0, y1, y2, y3)

U2 = x0 * sx[0][0] + x1 * sx[1][0]
V2 = x0 * sx[0][1] + x1 * sx[1][1]
T2 = x0 * sx[0][2] + x1 * sx[1][2]
U1 = sum(coefficient * triple[0] for coefficient, triple in zip((y0, y1, y2, y3), sy))
V1 = sum(coefficient * triple[1] for coefficient, triple in zip((y0, y1, y2, y3), sy))
T1 = sum(coefficient * triple[2] for coefficient, triple in zip((y0, y1, y2, y3), sy))

u = sp.symbols("u0:4")
v = sp.symbols("v0:4")
t = sp.symbols("t0:3")
a = sp.symbols("a0:6")
b = sp.symbols("b0:6")
ell = sp.symbols("ell0:9")

binary_cubics = (p**3, p**2 * q, p * q**2, q**3)
binary_quadratics = (p**2, p * q, q**2)
ternary_quadratics = (p**2, p * q, p * r, q**2, q * r, r**2)

U0 = sum(coefficient * monomial for coefficient, monomial in zip(u, binary_cubics))
V0 = sum(coefficient * monomial for coefficient, monomial in zip(v, binary_cubics))
T0 = sum(coefficient * monomial for coefficient, monomial in zip(t, binary_quadratics))
A = sum(coefficient * monomial for coefficient, monomial in zip(a, ternary_quadratics))
B = sum(coefficient * monomial for coefficient, monomial in zip(b, ternary_quadratics))
linear = sp.Matrix(3, 3, ell)

U = U0 + r * U1 + sp.Rational(1, 2) * r**2 * U2
V = V0 + r * V1 + sp.Rational(1, 2) * r**2 * V2
T = T0 + r * T1 + sp.Rational(1, 2) * r**2 * T2

determinant = sp.Poly(
    sp.expand(
        (
            linear
            + w * sp.Matrix((A, B, T)).jacobian(coordinates)
            + w**2 * sp.Matrix((U, V, R)).jacobian(coordinates)
            + w**3 * sp.Matrix((P, Q, 0)).jacobian(coordinates)
        ).det()
    ),
    w,
)

e6_equations = coefficients(determinant.coeff_monomial(w**6), 6)
e6_variables = (
    a[2],
    a[4],
    a[5],
    b[2],
    b[4],
    b[5],
    ell[8],
) + u + v + t
e6_matrix, e6_rhs = sp.linear_eq_to_matrix(e6_equations, e6_variables)


def check_full_contact_plane() -> None:
    gcd = sp.gcd(
        sp.gcd(sp.Poly(alpha, p, q), sp.Poly(beta, p, q)),
        sp.Poly(gamma, p, q),
    )
    assert gcd.total_degree() == 4
    assert sp.cancel(gcd.as_expr() / (2 * p * q * h)).free_symbols == set()
    assert syzygy_nullity(alpha, beta, gamma, 0) == 0
    assert syzygy_nullity(alpha, beta, gamma, 1) == 2
    assert syzygy_nullity(alpha, beta, gamma, 2) == 4
    for triple in sx + sy:
        assert sp.factor(
            alpha * triple[0] + beta * triple[1] + gamma * triple[2]
        ) == 0

    assert all(
        determinant.coeff_monomial(w**degree) == 0 for degree in (9, 8, 7)
    )
    assert e6_matrix.shape == (28, 18)

    # Five globally constant pivots eliminate five lower variables with no
    # parameter division.  This is deliberately different from the primary
    # coefficient-combination proof.
    pivot_rows = (1, 3, 4, 6, 7)
    pivot_columns = (0, 1, 2, 3, 5)
    pivot = e6_matrix.extract(pivot_rows, pivot_columns)
    assert pivot.det() == -5971968
    selected_equations = tuple(e6_equations[index] for index in pivot_rows)
    _, constant_substitution = exact_linear_solution(
        selected_equations, e6_variables
    )
    residuals = tuple(
        sp.factor(equation.subs(constant_substitution))
        for equation in e6_equations
    )

    first_x = (3 * x0 - x1) ** 2
    second_x = (3 * x0 - 2 * x1) * (3 * x0 + 2 * x1)
    assert has_scalar_associate(residuals, first_x)
    assert has_scalar_associate(residuals, second_x)

    x_zero = {x0: 0, x1: 0}
    residuals_x_zero = tuple(sp.factor(value.subs(x_zero)) for value in residuals)
    first_y = (9 * y0 + 3 * y1 - 3 * y2 - y3) ** 2
    second_y = (3 * y1 - 4 * y3) ** 2
    assert has_scalar_associate(residuals_x_zero, first_y)
    assert has_scalar_associate(residuals_x_zero, second_y)

    # Necessity follows in characteristic zero:
    # first_x=second_x=0 => x0=x1=0, then first_y=second_y=0.
    assert sp.factor(second_x.subs({x1: 3 * x0}) + 27 * x0**2) == 0

    m, n = sp.symbols("m n")
    contact_plane = {
        x0: 0,
        x1: 0,
        y0: (m - n) / 3,
        y1: sp.Rational(4, 3) * n,
        y2: m,
        y3: n,
    }
    explicit_lower = {variable: 0 for variable in e6_variables}
    explicit_lower[a[5]] = -(m**2 + 3 * n**2) / 36
    explicit_lower[b[5]] = -(3 * m**2 + n**2) / 36
    assert all(
        sp.factor(equation.subs(contact_plane).subs(explicit_lower)) == 0
        for equation in e6_equations
    )
    print("D4_SF_11CC_HOSTILE_FULL_CONTACT_PLANE_PASS")


def build_plane_lower_system():
    m, n = sp.symbols("m n")
    plane = {
        x0: 0,
        x1: 0,
        y0: (m - n) / 3,
        y1: sp.Rational(4, 3) * n,
        y2: m,
        y3: n,
    }
    equations6 = tuple(sp.factor(equation.subs(plane)) for equation in e6_equations)
    matrix6 = e6_matrix.subs(plane)
    rhs6 = e6_rhs.subs(plane)
    return m, n, plane, equations6, matrix6, rhs6


def check_rank_charts_and_e5() -> None:
    m, n, plane, equations6, matrix6, rhs6 = build_plane_lower_system()
    augmented6 = matrix6.row_join(rhs6)
    delta = m**2 - 4 * m * n + n**2

    assert matrix6.rank() == 7
    assert augmented6.rank() == 7
    pivot_rows = (1, 3, 4, 6, 7, 10, 15)
    pivot_columns = (0, 1, 2, 3, 5, 7, 8)
    maximal_minor = sp.factor(
        matrix6.extract(pivot_rows, pivot_columns).det()
    )
    assert sp.cancel(maximal_minor / delta).free_symbols == set()
    assert maximal_minor != 0

    root3 = sp.sqrt(3)
    for ratio in (2 + root3, 2 - root3):
        conic = {m: ratio, n: 1}
        conic_matrix = matrix6.subs(conic)
        conic_rhs = rhs6.subs(conic)
        assert conic_matrix.rank() == 6
        assert conic_matrix.row_join(conic_rhs).rank() == 6

    origin = {m: 0, n: 0}
    origin_matrix = matrix6.subs(origin)
    origin_rhs = rhs6.subs(origin)
    assert origin_matrix.rank() == 5
    assert origin_matrix.row_join(origin_rhs).rank() == 5

    # A complete generic solve proves that the two E5 obstructions are
    # independent of every free lower coefficient.
    _, generic_substitution = exact_linear_solution(equations6, e6_variables)
    raw_e5 = coefficients(determinant.coeff_monomial(w**5), 5)
    e5_generic = tuple(
        sp.factor(value.subs(plane).subs(generic_substitution))
        for value in raw_e5
    )
    coefficient_by_exponent = dict(zip(exponents(5), e5_generic))
    f = 7 * m**3 - 6 * m**2 * n + 3 * m * n**2 - 2 * n**3
    g = 2 * m**3 - 3 * m**2 * n + 6 * m * n**2 - 7 * n**3
    assert sp.factor(
        coefficient_by_exponent[(2, 1, 2)] + sp.Rational(4, 9) * f
    ) == 0
    assert sp.factor(
        coefficient_by_exponent[(1, 2, 2)] - sp.Rational(4, 9) * g
    ) == 0
    assert sp.factor(sp.resultant(f, g, m)) == -46656 * n**9
    assert sp.factor(sp.resultant(f, g, n)) == 46656 * m**9

    # Re-solve both algebraic conic points without the generic pivot.
    raw_e5_dict = dict(zip(exponents(5), raw_e5))
    for ratio in (2 + root3, 2 - root3):
        conic = {m: ratio, n: 1}
        conic_equations = tuple(value.subs(conic) for value in equations6)
        rank, conic_substitution = exact_linear_solution(
            conic_equations, e6_variables
        )
        assert rank == 6
        first = sp.simplify(
            raw_e5_dict[(2, 1, 2)]
            .subs(plane)
            .subs(conic)
            .subs(conic_substitution)
        )
        second = sp.simplify(
            raw_e5_dict[(1, 2, 2)]
            .subs(plane)
            .subs(conic)
            .subs(conic_substitution)
        )
        assert sp.simplify(first + sp.Rational(4, 9) * f.subs(conic)) == 0
        assert sp.simplify(second - sp.Rational(4, 9) * g.subs(conic)) == 0
        assert first != 0 and second != 0

    print("D4_SF_11CC_HOSTILE_RANK_AND_E5_PASS_7_6_5")


def check_origin_and_binary_exit() -> None:
    m, n, plane, equations6, _, _ = build_plane_lower_system()
    origin = {m: 0, n: 0}
    origin_equations = tuple(value.subs(origin) for value in equations6)
    rank, origin_substitution = exact_linear_solution(
        origin_equations, e6_variables
    )
    assert rank == 5

    raw_e4 = dict(
        zip(exponents(4), coefficients(determinant.coeff_monomial(w**4), 4))
    )
    descended_e4 = {
        exponent: sp.factor(
            value.subs(plane).subs(origin).subs(origin_substitution)
        )
        for exponent, value in raw_e4.items()
    }
    assert descended_e4[(3, 0, 1)] == sp.Rational(8, 27) * (
        3 * b[4] - ell[8]
    ) ** 2
    assert descended_e4[(0, 3, 1)] == sp.Rational(8, 27) * (
        3 * b[4] - 4 * ell[8]
    ) ** 2

    forced_zero = {b[4]: 0, ell[8]: 0}
    for variable in (a[2], a[4], a[5], b[2], b[4], b[5]):
        assert sp.factor(
            origin_substitution[variable].subs(forced_zero)
        ) == 0

    # This is exactly the algebra needed before the conceptual Moh exit:
    # x=y=0 removes all r-dependence in H3_1,H3_2,H2_3, and the six
    # assertions above remove it from H2_1,H2_2.
    assert all(sp.factor(value.subs({x0: 0, x1: 0})) == 0 for value in (U2, V2, T2))
    assert all(
        sp.factor(value.subs({y0: 0, y1: 0, y2: 0, y3: 0})) == 0
        for value in (U1, V1, T1)
    )
    print("D4_SF_11CC_HOSTILE_ORIGIN_BINARY_COLLAPSE_PASS")


def main() -> None:
    check_orbit_normalization()
    check_full_contact_plane()
    check_rank_charts_and_e5()
    check_origin_and_binary_exit()
    print("D4_SF_11CC_HOSTILE_AUDIT_EXACT_PASS")


if __name__ == "__main__":
    main()
