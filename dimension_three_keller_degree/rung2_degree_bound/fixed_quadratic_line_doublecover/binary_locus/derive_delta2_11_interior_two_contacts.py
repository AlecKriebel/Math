#!/usr/bin/env python3
"""Exact fraction-field exploration of the interior two-contact leaf."""

from __future__ import annotations

import itertools
import sympy as sp
from sympy.polys.matrices import DomainMatrix
from sympy.polys.rings import ring


p_symbol, q_symbol, w_symbol, a_symbol = sp.symbols("p q w a")
u_symbol = w_symbol**2
L_symbol = p_symbol - w_symbol * q_symbol
M_symbol = w_symbol * p_symbol - q_symbol
h_symbol = sp.expand(L_symbol * M_symbol)
P_symbol = sp.expand(h_symbol * p_symbol**2)
Q_symbol = sp.expand(h_symbol * q_symbol**2)
R_symbol = sp.expand(
    4 * w_symbol * a_symbol * p_symbol**3
    - 3 * (1 + u_symbol) * a_symbol * p_symbol**2 * q_symbol
    - 3 * (1 + u_symbol) * p_symbol * q_symbol**2
    + 4 * w_symbol * q_symbol**3
)


def jac_symbol(first, second):
    return sp.expand(
        sp.diff(first, p_symbol) * sp.diff(second, q_symbol)
        - sp.diff(first, q_symbol) * sp.diff(second, p_symbol)
    )


alpha_symbol = jac_symbol(Q_symbol, R_symbol)
beta_symbol = -jac_symbol(P_symbol, R_symbol)
gamma_symbol = jac_symbol(P_symbol, Q_symbol)
assert sp.factor(
    sp.gcd(sp.gcd(alpha_symbol, beta_symbol), gamma_symbol)
) == p_symbol * q_symbol

monomials_symbol = (
    p_symbol**2,
    p_symbol * q_symbol,
    q_symbol**2,
    p_symbol**2,
    p_symbol * q_symbol,
    q_symbol**2,
    p_symbol,
    q_symbol,
)
columns_symbol = tuple(
    alpha_symbol * monomials_symbol[index]
    if index < 3
    else beta_symbol * monomials_symbol[index]
    if index < 6
    else gamma_symbol * monomials_symbol[index]
    for index in range(8)
)
M7_symbol = sp.Matrix(
    [
        [
            sp.Poly(column, p_symbol, q_symbol).coeff_monomial(
                p_symbol ** (7 - row) * q_symbol**row
            )
            for column in columns_symbol
        ]
        for row in range(8)
    ]
)
domain_matrix = DomainMatrix.from_Matrix(M7_symbol).to_field()
rref7, pivots7 = domain_matrix.rref()
assert pivots7 == (0, 1, 2, 3, 4, 5)
rref7_matrix = rref7.to_Matrix()
basis_symbol = []
for free_column in (6, 7):
    vector = [
        -rref7_matrix[row, free_column] for row in range(6)
    ] + [sp.Integer(free_column == 6), sp.Integer(free_column == 7)]
    basis_symbol.append(vector)

K = sp.QQ.frac_field(w_symbol, a_symbol)
w = K.from_sympy(w_symbol)
a = K.from_sympy(a_symbol)
PQ, p, q = ring("p,q", K)
RR, r = ring("r", PQ)
ZZ, z = ring("z", RR)
u = w**2
L = p - w * q
M = w * p - q
h = L * M
P = h * p**2
Q = h * q**2
R = (
    4 * w * a * p**3
    - 3 * (1 + u) * a * p**2 * q
    - 3 * (1 + u) * p * q**2
    + 4 * w * q**3
)


def tangent_from_vector(vector):
    coefficients = [K.from_sympy(value) for value in vector]
    return (
        coefficients[0] * p**2
        + coefficients[1] * p * q
        + coefficients[2] * q**2,
        coefficients[3] * p**2
        + coefficients[4] * p * q
        + coefficients[5] * q**2,
        coefficients[6] * p + coefficients[7] * q,
    )


N1, N2 = tuple(tangent_from_vector(vector) for vector in basis_symbol)


def derivative_pq(value, variable):
    answer = RR.zero
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


def determinant3(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


H4 = tuple(RR(form) for form in (P, Q, PQ.zero))


def weighted_for(tangent, x5, y5):
    H3 = tuple(
        RR(form) for form in (r * tangent[0], r * tangent[1], R)
    )
    H2 = tuple(
        RR(form)
        for form in (
            PQ(x5) * r**2,
            PQ(y5) * r**2,
            r * tangent[2],
        )
    )
    J4 = jacobian(H4)
    J3 = jacobian(H3)
    J2 = jacobian(H2)
    return determinant3(
        [
            [
                z * ZZ(J2[row][column])
                + z**2 * ZZ(J3[row][column])
                + z**3 * ZZ(J4[row][column])
                for column in range(3)
            ]
            for row in range(3)
        ]
    )


def contact_column(tangent, x5=K.zero, y5=K.zero):
    weighted = weighted_for(tangent, x5, y5)
    assert weighted.coeff(z**7) == RR.zero
    e6r = weighted.coeff(z**6).coeff(r)
    return [
        e6r.coeff(p ** (5 - index) * q**index) for index in range(6)
    ]


column_X = contact_column(N1)
column_Z = contact_column(N2)
column_sum = contact_column(
    tuple(N1[index] + N2[index] for index in range(3))
)
column_Y = [
    column_sum[index] - column_X[index] - column_Z[index]
    for index in range(6)
]
column_x = contact_column((PQ.zero, PQ.zero, PQ.zero), K.one, K.zero)
column_y = contact_column((PQ.zero, PQ.zero, PQ.zero), K.zero, K.one)
contact = [
    [
        column_X[row],
        column_Y[row],
        column_Z[row],
        column_x[row],
        column_y[row],
    ]
    for row in range(6)
]


def rref_field(matrix):
    rows = [list(row) for row in matrix]
    pivots = []
    pivot_row = 0
    for column in range(len(rows[0])):
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
            if row != pivot_row and rows[row][column] != K.zero:
                multiple = rows[row][column]
                rows[row] = [
                    rows[row][index] - multiple * rows[pivot_row][index]
                    for index in range(len(rows[row]))
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, pivots


def determinant_field(matrix):
    rows = [list(row) for row in matrix]
    answer = K.one
    sign = 1
    for column in range(len(rows)):
        selected = next(
            (
                row
                for row in range(column, len(rows))
                if rows[row][column] != K.zero
            ),
            None,
        )
        if selected is None:
            return K.zero
        if selected != column:
            rows[column], rows[selected] = rows[selected], rows[column]
            sign = -sign
        pivot = rows[column][column]
        answer *= pivot
        for row in range(column + 1, len(rows)):
            if rows[row][column] != K.zero:
                multiple = rows[row][column] / pivot
                for next_column in range(column + 1, len(rows)):
                    rows[row][next_column] -= (
                        multiple * rows[column][next_column]
                    )
    return answer if sign == 1 else -answer


_contact_rref, contact_pivots = rref_field(contact)
print("contact rank", len(contact_pivots))
maximal_values = []
for omitted in range(6):
    rows = [index for index in range(6) if index != omitted]
    value = determinant_field(
        [[contact[row][column] for column in range(5)] for row in rows]
    )
    maximal_values.append(value)
    print(
        "contact omit",
        omitted,
        sp.factor(K.to_sympy(value)),
    )

EL = a * w**3 - 3 * a * w - 3 * u + 1
EM = -3 * a * u + a + w**3 - 3 * w
exceptional_minus = u - 4 * w + 1
exceptional_plus = u + 4 * w + 1
print(
    "exact open",
    [sp.factor(K.to_sympy(value)) for value in (EL, EM, exceptional_minus, exceptional_plus)],
)

Bpivot = (
    16 * a_symbol**2 * w_symbol**7
    + 48 * a_symbol**2 * w_symbol**5
    + 48 * a_symbol**2 * w_symbol**3
    + 16 * a_symbol**2 * w_symbol
    + 3 * a_symbol * w_symbol**8
    + 108 * a_symbol * w_symbol**6
    - 46 * a_symbol * w_symbol**4
    + 108 * a_symbol * w_symbol**2
    + 3 * a_symbol
    + 16 * w_symbol**7
    + 48 * w_symbol**5
    + 48 * w_symbol**3
    + 16 * w_symbol
)
K1 = (
    -36 * a_symbol * w_symbol**5
    - 8 * a_symbol * w_symbol**3
    - 36 * a_symbol * w_symbol
    + 7 * w_symbol**6
    - 27 * w_symbol**4
    - 27 * w_symbol**2
    + 7
)
K2 = (
    7 * a_symbol * w_symbol**6
    - 27 * a_symbol * w_symbol**4
    - 27 * a_symbol * w_symbol**2
    + 7 * a_symbol
    - 36 * w_symbol**5
    - 8 * w_symbol**3
    - 36 * w_symbol
)
base = (
    1024
    * w_symbol**2
    * (u_symbol + 1)
    * (u_symbol - 4 * w_symbol + 1)
    * (u_symbol + 4 * w_symbol + 1)
    / (3 * Bpivot**3)
)
maximal_expr = [sp.cancel(K.to_sympy(value)) for value in maximal_values]
residuals = [
    sp.factor(maximal_expr[0] / (base * K1)),
    sp.factor(maximal_expr[1] / (-base * w_symbol**2 * K1 * K2)),
    sp.factor(maximal_expr[2] / (-base * w_symbol**2 * K1 * K2)),
    sp.factor(maximal_expr[3] / (-base * w_symbol**2 * K1 * K2)),
    sp.factor(maximal_expr[4] / (-base * w_symbol**2 * K1 * K2)),
    sp.factor(maximal_expr[5] / (base * K2)),
]
assert all(sp.denom(value) == 1 for value in residuals)
print("K1K2 resultant", sp.factor(sp.resultant(K1, K2, a_symbol)))
print(
    "K1,Q5 resultant",
    sp.factor(sp.resultant(K1, residuals[5], a_symbol)),
)
print(
    "K2,Q0 resultant",
    sp.factor(sp.resultant(K2, residuals[0], a_symbol)),
)
resultant_pairs = (
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (0, 5),
)
resultants = [
    sp.factor(
        sp.resultant(
            residuals[first], residuals[second], a_symbol
        )
    )
    for first, second in resultant_pairs
]
for pair, value in zip(resultant_pairs, resultants):
    print("Q resultant", pair, value)
print("Q resultant gcd", sp.factor(sp.gcd_list(resultants)))

# Fresh Bpivot=0 chart.  The rows 1,...,6 and pivot columns
# (u0,u1,u2,v2,t0,t1) have determinant nonzero on w*(u+1) != 0,
# independently of a.
alternate_rows = tuple(range(1, 7))
alternate_pivots = (0, 1, 2, 5, 6, 7)
alternate_free = (3, 4)
pivot_matrix = M7_symbol.extract(alternate_rows, alternate_pivots)
alternate_basis_symbol = []
for free_column in alternate_free:
    right_hand_side = -M7_symbol.extract(
        alternate_rows, (free_column,)
    )
    solution = pivot_matrix.inv(method="DM") * right_hand_side
    vector = [sp.Integer(0) for _index in range(8)]
    for index, pivot_column in enumerate(alternate_pivots):
        vector[pivot_column] = sp.cancel(solution[index, 0])
    vector[free_column] = sp.Integer(1)
    alternate_basis_symbol.append(vector)
N1_alternate, N2_alternate = tuple(
    tangent_from_vector(vector) for vector in alternate_basis_symbol
)


def contact_from_basis(first, second):
    col_X = contact_column(first)
    col_Z = contact_column(second)
    col_sum = contact_column(
        tuple(first[index] + second[index] for index in range(3))
    )
    col_Y = [
        col_sum[index] - col_X[index] - col_Z[index]
        for index in range(6)
    ]
    return [
        [
            col_X[row],
            col_Y[row],
            col_Z[row],
            column_x[row],
            column_y[row],
        ]
        for row in range(6)
    ]


contact_alternate = contact_from_basis(N1_alternate, N2_alternate)
alternate_maximals = []
for omitted in range(6):
    rows = [index for index in range(6) if index != omitted]
    alternate_maximals.append(
        determinant_field(
            [
                [contact_alternate[row][column] for column in range(5)]
                for row in rows
            ]
        )
    )
remainders_B = []
for value in alternate_maximals:
    numerator = sp.cancel(K.to_sympy(value)).as_numer_denom()[0]
    remainders_B.append(
        sp.factor(sp.rem(numerator, Bpivot, a_symbol))
    )
print("B-chart nonzero remainders", sum(value != 0 for value in remainders_B))
B_resultants = [
    sp.factor(sp.resultant(Bpivot, value, a_symbol))
    for value in remainders_B
    if value != 0
]
print("B-chart resultant gcd", sp.factor(sp.gcd_list(B_resultants)))
first_linear_remainder = next(
    value
    for value in remainders_B
    if value != 0 and sp.degree(value, a_symbol) == 1
)
linear_poly = sp.Poly(first_linear_remainder, a_symbol)
a_B_rankdrop = sp.factor(
    -linear_poly.coeff_monomial(1)
    / linear_poly.coeff_monomial(a_symbol)
)
print("B-chart rankdrop a", a_B_rankdrop)
print(
    "B-chart substituted equation",
    sp.factor(
        sp.cancel(Bpivot.subs(a_symbol, a_B_rankdrop)).as_numer_denom()[0]
    ),
)
P16 = (
    385 * w_symbol**16
    + 9992 * w_symbol**14
    - 23012 * w_symbol**12
    + 53560 * w_symbol**10
    - 24250 * w_symbol**8
    + 53560 * w_symbol**6
    - 23012 * w_symbol**4
    + 9992 * w_symbol**2
    + 385
)
a_B_numerator, a_B_denominator = sp.cancel(a_B_rankdrop).as_numer_denom()
a_B_reduced = sp.factor(
    sp.rem(
        a_B_numerator * sp.invert(a_B_denominator, P16),
        P16,
        w_symbol,
    )
)
print("B-chart P16 reduced a", a_B_reduced)
