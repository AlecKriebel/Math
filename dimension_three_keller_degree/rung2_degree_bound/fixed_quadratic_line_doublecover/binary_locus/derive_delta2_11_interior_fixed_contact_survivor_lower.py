#!/usr/bin/env python3
"""Exact lower-equation exploration for the quartic fixed/contact survivor.

The coefficient field is Q(w)/(V(w^2)), where

    V(u) = 515*u^4 - 548*u^3 + 162*u^2 - 324*u + 243.

No numerical embedding is selected.  The surviving E6 contact-kernel
coordinate X is invertible in this field, so the tangent is normalized
to (c1,c2)=(1,Y/X).
"""

from __future__ import annotations

import sympy as sp
from sympy.polys.rings import ring


w_symbol = sp.symbols("w")
W = sp.Poly(
    515 * w_symbol**8
    - 548 * w_symbol**6
    + 162 * w_symbol**4
    - 324 * w_symbol**2
    + 243,
    w_symbol,
)
K = sp.QQ.alg_field_from_poly(W, alias="w")
w = K.convert(K.ext)
one = K.one


def field_fraction(numerator, denominator):
    """Return numerator/denominator in K, with an exact zero check."""

    assert denominator != K.zero
    return numerator * denominator**-1


u = w**2
F0 = 7 * u**3 + 45 * u**2 - 75 * u + 15
J = 55 * u**3 + 9 * u**2 - 3 * u - 21
NX = (
    49 * u**5
    - 987 * u**4
    - 3126 * u**3
    + 4650 * u**2
    + 405 * u
    - 1215
)
NY = (
    343 * u**5
    - 165 * u**4
    + 1734 * u**3
    + 150 * u**2
    - 2925 * u
    + 1215
)
X = -field_fraction(
    NX,
    64 * w**5 * (11 * u - 9) * F0**2 * J,
)
Y = -field_fraction(
    NY,
    32 * w**4 * (u + 1) * (11 * u - 9) * F0**2 * J,
)
Z = -field_fraction(
    (u - 3) * (107 * u**4 - 90 * u**3 + 120 * u**2 - 150 * u + 45),
    2 * w**3 * (u + 1) ** 2 * (11 * u - 9) * F0**2 * J,
)
x5_kernel = field_fraction(
    (5 * u - 3) * (12 * u**3 - 5 * u**2 + 6 * u - 9),
    u * (u + 1) ** 2 * (11 * u - 9),
)

assert X != K.zero
assert Y**2 == X * Z
rho = field_fraction(Y, X)
x5_value = field_fraction(x5_kernel, X)
y5_value = field_fraction(one, X)
assert rho**2 == field_fraction(Z, X)


unknown_names = (
    *(f"x{index}" for index in range(5)),
    *(f"y{index}" for index in range(5)),
    *(f"t{index}" for index in range(3)),
    *(f"u{index}" for index in range(4)),
    *(f"v{index}" for index in range(4)),
    *(f"l{index}" for index in range(9)),
)
C = K.poly_ring(*unknown_names)
coefficient_variables = dict(zip(unknown_names, C.gens))
PQR2, p, q = ring("p,q", C)
PQR, r = ring("r", PQR2)
ZPOLY, z = ring("z", PQR)

# Coerce every fixed field coefficient into the innermost coefficient
# ring before combining it with p,q,r-polynomials.
w = C(w)
rho = C(rho)
x5_value = C(x5_value)
y5_value = C(y5_value)
F0 = C(F0)
J = C(J)


def binary(prefix, degree):
    return sum(
        coefficient_variables[f"{prefix}{index}"]
        * p ** (degree - index)
        * q**index
        for index in range(degree + 1)
    )


def derivative_pq(value, variable):
    """Differentiate an element of PQR=PQR2[r] in p or q."""

    answer = PQR.zero
    for (r_degree,), coefficient in value.terms():
        answer += coefficient.diff(variable) * r**r_degree
    return answer


def jacobian(forms):
    return [
        [
            derivative_pq(form, p),
            derivative_pq(form, q),
            form.diff(r),
        ]
        for form in forms
    ]


def determinant(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


L = p - w * q
M = w * p - q
h = L * M
Kpoly = 7 * w**6 + 9 * w**4 - 3 * w**2 - 5
A = -Kpoly
T = 4 * w * (3 * w**2 - 1)
R = L * (
    A * p**2
    + (1 - 3 * w**2) * T * p * q
    + 4 * w * T * q**2
)

N1u = -4 * w * (
    87 * p**2 * w**8
    + 52 * p**2 * w**6
    - 270 * p**2 * w**4
    + 36 * p**2 * w**2
    + 15 * p**2
    - 154 * p * q * w**7
    + 258 * p * q * w**5
    + 114 * p * q * w**3
    - 42 * p * q * w
    + 72 * q**2 * w**6
    - 240 * q**2 * w**4
    + 72 * q**2 * w**2
)
N1v = -4 * q * w * (
    82 * p * w**7
    - 90 * p * w**5
    + 54 * p * w**3
    - 30 * p * w
    + 5 * q * w**8
    - 12 * q * w**6
    + 6 * q * w**4
    - 60 * q * w**2
    + 45 * q
)
N1t = 4 * p * w**2 * F0 * J

N2u = (
    7 * p**2 * w**10
    - 177 * p**2 * w**8
    + 534 * p**2 * w**6
    - 210 * p**2 * w**4
    + 51 * p**2 * w**2
    - 45 * p**2
    - 154 * p * q * w**9
    - 472 * p * q * w**7
    - 12 * p * q * w**5
    + 264 * p * q * w**3
    - 42 * p * q * w
    + 112 * q**2 * w**8
    + 432 * q**2 * w**6
    - 240 * q**2 * w**4
    - 48 * q**2 * w**2
)
N2v = q * (
    42 * p * w**9
    - 72 * p * w**7
    - 180 * p * w**5
    + 24 * p * w**3
    + 90 * p * w
    - 35 * q * w**10
    - 259 * q * w**8
    + 354 * q * w**6
    + 186 * q * w**4
    - 15 * q * w**2
    - 135 * q
)
N2t = 4 * q * w**2 * F0 * J

Nu = N1u + rho * N2u
Nv = N1v + rho * N2v
Nt = N1t + rho * N2t

H4 = tuple(PQR(form) for form in (h * p**2, h * q**2, PQR2.zero))
H3 = tuple(
    PQR(form)
    for form in (
        binary("u", 3) + r * Nu,
        binary("v", 3) + r * Nv,
        R,
    )
)
H2 = tuple(
    PQR(form)
    for form in (
        binary("x", 2)
        + r
        * (
            coefficient_variables["x3"] * p
            + coefficient_variables["x4"] * q
        )
        + PQR2(x5_value) * r**2,
        binary("y", 2)
        + r
        * (
            coefficient_variables["y3"] * p
            + coefficient_variables["y4"] * q
        )
        + PQR2(y5_value) * r**2,
        binary("t", 2) + r * Nt,
    )
)
J4 = jacobian(H4)
J3 = jacobian(H3)
J2 = jacobian(H2)
L0 = [
    [coefficient_variables[f"l{3 * row + column}"] for column in range(3)]
    for row in range(3)
]

weighted_matrix = [
    [
        ZPOLY(PQR(PQR2(L0[row][column])))
        + z * ZPOLY(J2[row][column])
        + z**2 * ZPOLY(J3[row][column])
        + z**3 * ZPOLY(J4[row][column])
        for column in range(3)
    ]
    for row in range(3)
]
weighted = determinant(weighted_matrix)

assert weighted.coeff(z**8) == PQR.zero
assert weighted.coeff(z**7) == PQR.zero
E6 = weighted.coeff(z**6)
assert E6.coeff(r) == PQR2.zero
assert all(
    coefficient == PQR2.zero
    for (r_degree,), coefficient in E6.terms()
    if r_degree != 0
)
print("PASS exact quartic-field E7 and E6 contact equations")


def homogeneous_coefficients(value, degree):
    return [
        value.coeff(p ** (degree - index) * q**index)
        for index in range(degree + 1)
    ]


def assert_linear(equations):
    for equation in equations:
        for monomial, _coefficient in equation.terms():
            assert sum(monomial) <= 1


E6constant = E6.coeff(PQR.one)
equations6 = homogeneous_coefficients(E6constant, 6)
assert_linear(equations6)
active6 = [
    variable
    for variable in C.gens
    if any(equation.coeff(variable) != K.zero for equation in equations6)
]
print("E6 active", [str(variable) for variable in active6])


def rref_solve(equations, variables):
    """RREF a linear system over K and return pivot substitutions in C."""

    rows = []
    for equation in equations:
        constant = equation.coeff(C.one)
        rows.append(
            [equation.coeff(variable) for variable in variables] + [-constant]
        )
    pivot_columns = []
    pivot_row = 0
    for column in range(len(variables)):
        selected = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if rows[row][column] != K.zero
            ),
            None,
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        inverse = rows[pivot_row][column] ** -1
        rows[pivot_row] = [entry * inverse for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row:
                continue
            multiplier = rows[row][column]
            if multiplier != K.zero:
                rows[row] = [
                    rows[row][index] - multiplier * rows[pivot_row][index]
                    for index in range(len(rows[row]))
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    for row in rows:
        if all(entry == K.zero for entry in row[:-1]):
            assert row[-1] == K.zero
    substitutions = {}
    for row, column in enumerate(pivot_columns):
        expression = C(rows[row][-1])
        for free_column, variable in enumerate(variables):
            if free_column not in pivot_columns and rows[row][free_column] != K.zero:
                expression -= C(rows[row][free_column]) * variable
        substitutions[variables[column]] = expression
    return pivot_columns, substitutions


pivots6, substitution6 = rref_solve(equations6, active6)
print("E6 rank", len(pivots6), "of", len(active6))
print(
    "E6 pivots",
    [str(active6[index]) for index in pivots6],
)


def compose_coefficient(value, substitutions):
    return value.compose(substitutions) if substitutions else value


def compose_pq(value, substitutions):
    answer = PQR2.zero
    for monomial, coefficient in value.terms():
        answer += compose_coefficient(coefficient, substitutions) * (
            p ** monomial[0] * q ** monomial[1]
        )
    return answer


E5 = weighted.coeff(z**5)
print("E5 r-degree", E5.degree())
e5_r2_p3 = E5.coeff(r**2).coeff(p**3)
assert len(e5_r2_p3.terms()) == 1
assert e5_r2_p3.terms()[0][0] == (0,) * len(C.gens)
e5_r2_p3_field = e5_r2_p3.terms()[0][1]
e5_r2_p3_polynomial = sp.Poly(
    sum(
        coefficient * w_symbol ** (len(e5_r2_p3_field.to_sympy_list()) - 1 - index)
        for index, coefficient in enumerate(e5_r2_p3_field.to_sympy_list())
    ),
    w_symbol,
)
e5_r2_p3_primitive = e5_r2_p3_polynomial.clear_denoms()[1].primitive()[1]
assert e5_r2_p3_primitive != 0
print("E5 [r^2 p^3] primitive remainder", e5_r2_p3_primitive.as_expr())
for p_degree in range(2, -1, -1):
    q_degree = 3 - p_degree
    coefficient_ring_value = E5.coeff(r**2).coeff(
        p**p_degree * q**q_degree
    )
    assert len(coefficient_ring_value.terms()) == 1
    field_value = coefficient_ring_value.terms()[0][1]
    polynomial = sp.Poly(
        sum(
            coefficient * w_symbol ** (len(field_value.to_sympy_list()) - 1 - index)
            for index, coefficient in enumerate(field_value.to_sympy_list())
        ),
        w_symbol,
    )
    primitive = polynomial.clear_denoms()[1].primitive()[1]
    print(
        f"E5 [r^2 p^{p_degree} q^{q_degree}] primitive remainder",
        primitive.as_expr(),
    )
for (r_degree,), coefficient in E5.terms():
    raw_degrees = [
        max((sum(term) for term, _entry in value.terms()), default=-1)
        for _monomial, value in coefficient.terms()
    ]
    print(
        "E5 raw r^",
        r_degree,
        "max coefficient-variable degree",
        max(raw_degrees, default=-1),
    )
    after = compose_pq(coefficient, substitution6)
    nonzero_coefficients = [
        (monomial, value)
        for monomial, value in after.terms()
        if value != C.zero
    ]
    print(
        "E5 r^",
        r_degree,
        "pq terms",
        len(nonzero_coefficients),
        "max coefficient-variable degree",
        max(
            (
                max(sum(term) for term, _entry in value.terms())
                if value
                else -1
            )
            for _monomial, value in nonzero_coefficients
        )
        if nonzero_coefficients
        else -1,
    )
