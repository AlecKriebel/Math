#!/usr/bin/env python3
"""Independent hostile verification of the D4-DN-1CC exclusion.

The verifier does not import either primary implementation.  It retains
all lower coefficients from the start and obtains the contact line through
a global constant-pivot elimination.
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


h = (p + q) ** 2
P = sp.expand(h * p**2)
Q = sp.expand(h * q**2)
R = sp.expand((p + q) * (2 * p**2 + p * q + 2 * q**2))
alpha = jac2(Q, R)
beta = -jac2(P, R)
gamma = jac2(P, Q)

# Independently computed E7 bases.  The first basis controls the r^2
# derivative block and the second the r derivative block.
sx = (
    (-(3 * p + 2 * q) / 3, (2 * p + 3 * q) / 3, 0),
    (4 * (6 * p + 5 * q) / 45, 4 * p / 45, 1),
)
sy = (
    (-p * (3 * p + 2 * q) / 3, p * (2 * p + 3 * q) / 3, 0),
    (
        (2 * p - 3 * q) * (3 * p + 2 * q) / 9,
        -(2 * p - 3 * q) * (2 * p + 3 * q) / 9,
        0,
    ),
    (4 * p * (6 * p + 5 * q) / 45, 4 * p**2 / 45, p),
    (4 * (3 * p**2 + 20 * p * q + 15 * q**2) / 135, -8 * p**2 / 135, q),
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


def check_normal_form_and_e7() -> None:
    assert sp.factor(alpha) == -6 * p * q * (p + q) ** 2 * (2 * p + 3 * q)
    assert sp.factor(beta) == -6 * p * q * (p + q) ** 2 * (3 * p + 2 * q)
    assert sp.factor(gamma) == 8 * p * q * (p + q) ** 4
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

    # The residual involution fixes this rational normal form exactly.
    assert h.xreplace({p: q, q: p}) == h
    assert R.xreplace({p: q, q: p}) == R
    print("D4_DN1CC_HOSTILE_NORMAL_FORM_E7_PASS")


def check_full_contact_line() -> sp.Symbol:
    assert e6_matrix.shape == (28, 18)

    # A global constant pivot eliminates five lower variables without any
    # contact-dependent division.
    pivot_rows = (1, 3, 4, 6, 7)
    pivot_columns = (0, 1, 2, 3, 5)
    assert e6_matrix.extract(pivot_rows, pivot_columns).det() == 2332800
    selected_equations = tuple(e6_equations[index] for index in pivot_rows)
    _, constant_substitution = exact_linear_solution(
        selected_equations, e6_variables
    )
    residuals = tuple(
        sp.factor(equation.subs(constant_substitution))
        for equation in e6_equations
    )

    first_x = (15 * x0 + 2 * x1) ** 2
    second_x = 225 * x0**2 + 56 * x1**2
    assert has_scalar_associate(residuals, first_x)
    assert has_scalar_associate(residuals, second_x)
    assert sp.factor(
        second_x.subs({x1: -sp.Rational(15, 2) * x0}) - 3375 * x0**2
    ) == 0

    x_zero = {x0: 0, x1: 0}
    residuals_x_zero = tuple(sp.factor(value.subs(x_zero)) for value in residuals)
    first_y = (45 * y0 - 30 * y1 + 6 * y2 - 4 * y3) ** 2
    second_y = (3 * y1 - 2 * y3) ** 2
    assert has_scalar_associate(residuals_x_zero, first_y)
    assert has_scalar_associate(residuals_x_zero, second_y)

    two_linear = {
        y1: sp.Rational(2, 3) * y3,
        y0: (-2 * y2 + 8 * y3) / 15,
    }
    residuals_two_linear = tuple(
        sp.factor(value.subs(x_zero).subs(two_linear)) for value in residuals
    )
    assert has_scalar_associate(residuals_two_linear, (y2 + y3) ** 2)

    k = sp.symbols("k")
    contact_line = {
        x0: 0,
        x1: 0,
        y0: sp.Rational(2, 3) * k,
        y1: sp.Rational(2, 3) * k,
        y2: -k,
        y3: k,
    }
    explicit_lower = {variable: 0 for variable in e6_variables}
    explicit_lower[a[5]] = k**2 / 45
    explicit_lower[b[5]] = k**2 / 45
    assert all(
        sp.factor(equation.subs(contact_line).subs(explicit_lower)) == 0
        for equation in e6_equations
    )
    assert sp.factor(
        U1.subs(contact_line) + sp.Rational(2, 3) * k * p * (p + q)
    ) == 0
    assert sp.factor(
        V1.subs(contact_line) - sp.Rational(2, 3) * k * q * (p + q)
    ) == 0
    assert sp.factor(T1.subs(contact_line) - k * (-p + q)) == 0
    print("D4_DN1CC_HOSTILE_FULL_CONTACT_LINE_PASS")
    return k


def contact_line_substitution(k: sp.Symbol) -> dict[sp.Symbol, sp.Expr]:
    return {
        x0: 0,
        x1: 0,
        y0: sp.Rational(2, 3) * k,
        y1: sp.Rational(2, 3) * k,
        y2: -k,
        y3: k,
    }


def check_two_rank_charts_and_e4(k: sp.Symbol) -> None:
    line = contact_line_substitution(k)
    equations_line = tuple(sp.factor(value.subs(line)) for value in e6_equations)
    matrix_line = e6_matrix.subs(line)
    rhs_line = e6_rhs.subs(line)
    augmented_line = matrix_line.row_join(rhs_line)
    assert matrix_line.rank() == 6
    assert augmented_line.rank() == 6

    pivot_rows = (1, 3, 4, 6, 7, 10)
    pivot_columns = (0, 1, 2, 3, 5, 7)
    assert sp.factor(
        matrix_line.extract(pivot_rows, pivot_columns).det()
        + 13996800 * k
    ) == 0

    # This complete solve is over Q(k), hence belongs only to k != 0.
    _, generic_substitution = exact_linear_solution(
        equations_line, e6_variables
    )
    raw_e4 = dict(
        zip(exponents(4), coefficients(determinant.coeff_monomial(w**4), 4))
    )
    generic_e4 = {
        exponent: sp.factor(
            value.subs(line).subs(generic_substitution)
        )
        for exponent, value in raw_e4.items()
    }
    expected = sp.Rational(16, 135) * k**4
    assert generic_e4[(1, 0, 3)] == expected
    assert generic_e4[(0, 1, 3)] == expected

    # Recompute the only omitted pivot k=0 from the original equations.
    origin = {k: 0}
    origin_equations = tuple(value.subs(origin) for value in equations_line)
    origin_matrix = matrix_line.subs(origin)
    origin_rhs = rhs_line.subs(origin)
    assert origin_matrix.rank() == 5
    assert origin_matrix.row_join(origin_rhs).rank() == 5
    rank, origin_substitution = exact_linear_solution(
        origin_equations, e6_variables
    )
    assert rank == 5
    origin_e4 = {
        exponent: sp.factor(
            value.subs(line).subs(origin).subs(origin_substitution)
        )
        for exponent, value in raw_e4.items()
    }
    assert origin_e4[(3, 0, 1)] == sp.Rational(2, 135) * (
        15 * b[4] + 2 * ell[8]
    ) ** 2
    assert origin_e4[(0, 3, 1)] == sp.Rational(10, 27) * (
        3 * b[4] - 2 * ell[8]
    ) ** 2

    forced_zero = {b[4]: 0, ell[8]: 0}
    for variable in (a[2], a[4], a[5], b[2], b[4], b[5]):
        assert sp.factor(
            origin_substitution[variable].subs(forced_zero)
        ) == 0

    assert all(
        sp.factor(value.subs({x0: 0, x1: 0})) == 0
        for value in (U2, V2, T2)
    )
    assert all(
        sp.factor(value.subs({y0: 0, y1: 0, y2: 0, y3: 0})) == 0
        for value in (U1, V1, T1)
    )
    print("D4_DN1CC_HOSTILE_E4_AND_ORIGIN_PASS_6_5")


def main() -> None:
    check_normal_form_and_e7()
    k = check_full_contact_line()
    check_two_rank_charts_and_e4(k)
    print("D4_DN1CC_HOSTILE_AUDIT_EXACT_PASS")


if __name__ == "__main__":
    main()
