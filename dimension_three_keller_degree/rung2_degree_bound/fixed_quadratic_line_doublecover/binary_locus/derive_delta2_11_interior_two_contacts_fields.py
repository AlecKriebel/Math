#!/usr/bin/env python3
"""Exact-field contact/E5 tests for two-contact rank-drop branches."""

from __future__ import annotations

import sympy as sp
from sympy.polys.rings import ring


w_symbol = sp.symbols("w")
u_symbol = w_symbol**2
c_even = 7 * w_symbol**6 - 27 * w_symbol**4 - 27 * w_symbol**2 + 7
b_odd = -36 * w_symbol**5 - 8 * w_symbol**3 - 36 * w_symbol


def rref(matrix, field):
    rows = [list(row) for row in matrix]
    pivots = []
    pivot_row = 0
    for column in range(len(rows[0])):
        selected = next(
            (
                row
                for row in range(pivot_row, len(rows))
                if rows[row][column] != field.zero
            ),
            None,
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        inverse = rows[pivot_row][column] ** -1
        rows[pivot_row] = [entry * inverse for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row != pivot_row and rows[row][column] != field.zero:
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


def nullspace(matrix, field):
    reduced, pivots = rref(matrix, field)
    free = [
        column for column in range(len(matrix[0])) if column not in pivots
    ]
    basis = []
    for free_column in free:
        vector = [field.zero for _column in range(len(matrix[0]))]
        vector[free_column] = field.one
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        basis.append(vector)
    return basis, pivots


def determinant3(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def evaluate_rational(expression, field, generator):
    numerator, denominator = sp.cancel(expression).as_numer_denom()

    def evaluate_polynomial(value):
        answer = field.zero
        for coefficient in sp.Poly(value, w_symbol, domain=sp.QQ).all_coeffs():
            answer = answer * generator + field.convert(coefficient)
        return answer

    return evaluate_polynomial(numerator) / evaluate_polynomial(denominator)


def analyze(label, modulus, a_expression):
    K = sp.QQ.alg_field_from_poly(sp.Poly(modulus, w_symbol), alias="w")
    w = K.convert(K.ext)
    a = evaluate_rational(a_expression, K, w)
    u = w**2
    exact_open = (
        w,
        u - 1,
        a * w**3 - 3 * a * w - 3 * u + 1,
        -3 * a * u + a + w**3 - 3 * w,
        u - 4 * w + 1,
        u + 4 * w + 1,
    )
    assert all(value != K.zero for value in exact_open)

    PQ, p, q = ring("p,q", K)
    RR, r = ring("r", PQ)
    ZZ, z = ring("z", RR)
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

    def jac(first, second):
        return first.diff(p) * second.diff(q) - first.diff(q) * second.diff(p)

    alpha = jac(Q, R)
    beta = -jac(P, R)
    gamma = jac(P, Q)
    monomials = (p**2, p * q, q**2, p**2, p * q, q**2, p, q)
    columns7 = tuple(
        alpha * monomials[index]
        if index < 3
        else beta * monomials[index]
        if index < 6
        else gamma * monomials[index]
        for index in range(8)
    )
    matrix7 = [
        [
            column.coeff(p ** (7 - row) * q**row)
            for column in columns7
        ]
        for row in range(8)
    ]
    basis7, pivots7 = nullspace(matrix7, K)
    assert len(pivots7) == 6
    assert len(basis7) == 2

    tangents = []
    for vector in basis7:
        tangents.append(
            (
                vector[0] * p**2 + vector[1] * p * q + vector[2] * q**2,
                vector[3] * p**2 + vector[4] * p * q + vector[5] * q**2,
                vector[6] * p + vector[7] * q,
            )
        )
    N1, N2 = tangents

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
            e6r.coeff(p ** (5 - index) * q**index)
            for index in range(6)
        ]

    column_X = contact_column(N1)
    column_Z = contact_column(N2)
    summed = tuple(N1[index] + N2[index] for index in range(3))
    column_sum = contact_column(summed)
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
    contact_kernel, contact_pivots = nullspace(contact, K)

    constant_columns = (
        alpha * p,
        alpha * q,
        beta * p,
        beta * q,
        gamma,
    )
    constant_matrix = [
        [
            column.coeff(p ** (6 - row) * q**row)
            for column in constant_columns
        ]
        for row in range(7)
    ]
    _constant_kernel, constant_pivots = nullspace(constant_matrix, K)
    assert len(constant_pivots) == 5

    if len(contact_pivots) == 5:
        outcome = "contact rank 5"
    elif len(contact_pivots) == 4:
        assert len(contact_kernel) == 1
        vector = contact_kernel[0]
        obstruction = vector[1] ** 2 - vector[0] * vector[2]
        if obstruction != K.zero:
            outcome = "contact rank 4, non-Veronese"
        else:
            if vector[0] != K.zero:
                tangent = tuple(
                    N1[index] + vector[1] / vector[0] * N2[index]
                    for index in range(3)
                )
                x5_actual = vector[3] / vector[0]
                y5_actual = vector[4] / vector[0]
            else:
                assert vector[2] != K.zero
                tangent = tuple(
                    vector[1] / vector[2] * N1[index] + N2[index]
                    for index in range(3)
                )
                x5_actual = vector[3] / vector[2]
                y5_actual = vector[4] / vector[2]
            weighted = weighted_for(tangent, x5_actual, y5_actual)
            e5r2 = weighted.coeff(z**5).coeff(r**2)
            e5_coefficients = [
                e5r2.coeff(p ** (3 - index) * q**index)
                for index in range(4)
            ]
            if any(value != K.zero for value in e5_coefficients):
                first = next(
                    index
                    for index, value in enumerate(e5_coefficients)
                    if value != K.zero
                )
                outcome = f"Veronese, killed by E5 coefficient {first}"
            else:
                outcome = "GENUINE E5 SURVIVOR"
    elif len(contact_pivots) == 3:
        assert len(contact_kernel) == 2
        first, second = contact_kernel
        obstruction_coefficients = (
            first[1] ** 2 - first[0] * first[2],
            2 * first[1] * second[1]
            - first[0] * second[2]
            - second[0] * first[2],
            second[1] ** 2 - second[0] * second[2],
        )
        print(
            "RANK3 OBSTRUCTION",
            label,
            tuple(K.to_sympy(value) for value in obstruction_coefficients),
        )
        assert obstruction_coefficients[0] == K.zero
        assert obstruction_coefficients[1] == K.zero
        assert obstruction_coefficients[2] != K.zero
        vector = first
        if vector[0] != K.zero:
            tangent = tuple(
                N1[index] + vector[1] / vector[0] * N2[index]
                for index in range(3)
            )
            x5_actual = vector[3] / vector[0]
            y5_actual = vector[4] / vector[0]
        else:
            assert vector[2] != K.zero
            tangent = tuple(
                vector[1] / vector[2] * N1[index] + N2[index]
                for index in range(3)
            )
            x5_actual = vector[3] / vector[2]
            y5_actual = vector[4] / vector[2]
        weighted = weighted_for(tangent, x5_actual, y5_actual)
        print(
            "RANK3 UNIQUE LIFT",
            label,
            "tangent",
            tuple(
                tuple(
                    (monomial, K.to_sympy(value))
                    for monomial, value in form.terms()
                )
                for form in tangent
            ),
            "x5,y5",
            K.to_sympy(x5_actual),
            K.to_sympy(y5_actual),
        )
        e5r2 = weighted.coeff(z**5).coeff(r**2)
        e5_coefficients = [
            e5r2.coeff(p ** (3 - index) * q**index)
            for index in range(4)
        ]
        if any(value != K.zero for value in e5_coefficients):
            first_nonzero = next(
                index
                for index, value in enumerate(e5_coefficients)
                if value != K.zero
            )
            outcome = (
                "contact rank 3, unique Veronese tangent, "
                f"killed by E5 coefficient {first_nonzero}"
            )
        else:
            outcome = "contact rank 3, unique Veronese GENUINE E5 SURVIVOR"
    else:
        outcome = f"contact rank {len(contact_pivots)} NEEDS ANALYSIS"
    print(
        "RESULT",
        label,
        "degree",
        sp.Poly(modulus, w_symbol).degree(),
        outcome,
        "constant rank 5",
    )
    return {
        "label": label,
        "degree": sp.Poly(modulus, w_symbol).degree(),
        "contact_rank": len(contact_pivots),
        "constant_rank": len(constant_pivots),
        "outcome": outcome,
    }


Sminus = (
    7 * w_symbol**6
    - 36 * w_symbol**5
    - 27 * w_symbol**4
    - 8 * w_symbol**3
    - 27 * w_symbol**2
    - 36 * w_symbol
    + 7
)
Splus = (
    7 * w_symbol**6
    + 36 * w_symbol**5
    - 27 * w_symbol**4
    + 8 * w_symbol**3
    - 27 * w_symbol**2
    + 36 * w_symbol
    + 7
)
G0 = (
    7 * w_symbol**8
    - 156 * w_symbol**6
    + 66 * w_symbol**4
    - 12 * w_symbol**2
    + 15
)
G0reciprocal = (
    15 * w_symbol**8
    - 12 * w_symbol**6
    + 66 * w_symbol**4
    - 156 * w_symbol**2
    + 7
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
a_P16 = (
    -w_symbol
    * (
        2626085 * w_symbol**14
        + 67753107 * w_symbol**12
        - 167139687 * w_symbol**10
        + 396647791 * w_symbol**8
        - 228766929 * w_symbol**6
        + 398117721 * w_symbol**4
        - 168036781 * w_symbol**2
        + 83754213
    )
    / 14417920
)
a_K1 = sp.cancel(-c_even / b_odd)

field_results = [
    analyze("K1=K2, a=1", Sminus, sp.Integer(1)),
    analyze("K1=K2, a=-1", Splus, sp.Integer(-1)),
]
# The two K1/Q5 octics are exactly EL=0 and EM=0 after a=-c/b,
# hence are routed delta>=3 boundaries rather than exact-open leaves.
# At u=-1 the common-Q solutions a=+/-w likewise make EM or EL
# vanish.  The remaining common-Q branch has reciprocal roots in the
# existing quartic field; the branch swap identifies them.
# The reciprocal-quartic solutions are also EL=0 or EM=0, so are routed.
field_results.extend(
    [
        analyze("B=0, u=-1, a=0", w_symbol**2 + 1, sp.Integer(0)),
        analyze("B=0, P16", P16, a_P16),
    ]
)
