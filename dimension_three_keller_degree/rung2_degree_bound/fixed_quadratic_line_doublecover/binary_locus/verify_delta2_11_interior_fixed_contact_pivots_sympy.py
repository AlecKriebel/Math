#!/usr/bin/env python3
"""Fresh exact SymPy bases for four internal fixed/contact chart artifacts."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp
from sympy.polys.rings import ring


w_symbol = sp.symbols("w")


def rref(matrix, field):
    rows = [list(row) for row in matrix]
    if not rows:
        return rows, []
    pivot_columns = []
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
            if row == pivot_row:
                continue
            multiplier = rows[row][column]
            if multiplier != field.zero:
                rows[row] = [
                    rows[row][index] - multiplier * rows[pivot_row][index]
                    for index in range(len(rows[row]))
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, pivot_columns


def nullspace(matrix, field):
    reduced, pivots = rref(matrix, field)
    free_columns = [
        column for column in range(len(matrix[0])) if column not in pivots
    ]
    basis = []
    for free in free_columns:
        vector = [field.zero for _column in range(len(matrix[0]))]
        vector[free] = field.one
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free]
        basis.append(vector)
    return basis, pivots


def determinant(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def analyze(label, modulus, chart):
    K = sp.QQ.alg_field_from_poly(sp.Poly(modulus, w_symbol), alias="w")
    w = K.convert(K.ext)
    u = w**2
    if chart == "D":
        A = 9 * u**2 - 6 * u + 1
        T = 16 * w
    elif chart == "H":
        A = -(7 * u**3 + 9 * u**2 - 3 * u - 5)
        T = 4 * w * (3 * u - 1)
    else:
        raise ValueError(chart)

    # The exact open for this leaf.
    exact_open = (
        w,
        u - 1,
        u - 3,
        A + T * (w**3 + w),
        -A * w + 3 * T * u - 5 * T,
        A * u - 3 * A + 12 * T * w**3 - 4 * T * w,
    )
    assert all(value != K.zero for value in exact_open)

    PQ, p, q = ring("p,q", K)
    L = p - w * q
    M = w * p - q
    h = L * M
    P = h * p**2
    Q = h * q**2
    R = L * (
        A * p**2 + (1 - 3 * u) * T * p * q + 4 * w * T * q**2
    )

    def jac(first, second):
        return first.diff(p) * second.diff(q) - first.diff(q) * second.diff(p)

    alpha = jac(Q, R)
    beta = -jac(P, R)
    gamma = jac(P, Q)
    u_monomials = (p**2, p * q, q**2)
    v_monomials = (p**2, p * q, q**2)
    t_monomials = (p, q)
    columns7 = tuple(
        alpha * monomial for monomial in u_monomials
    ) + tuple(
        beta * monomial for monomial in v_monomials
    ) + tuple(
        gamma * monomial for monomial in t_monomials
    )
    matrix7 = [
        [
            column.coeff(p ** (7 - index) * q**index)
            for column in columns7
        ]
        for index in range(8)
    ]
    basis7, pivots7 = nullspace(matrix7, K)
    assert len(pivots7) == 6
    assert len(basis7) == 2

    C = K.poly_ring("c1", "c2", "x5", "y5")
    c1, c2, x5, y5 = C.gens
    PQC, pc, qc = ring("p,q", C)
    RC, rc = ring("r", PQC)
    ZC, zc = ring("z", RC)
    wc = C(w)
    uc = wc**2
    Ac = C(A)
    Tc = C(T)
    Lc = pc - wc * qc
    Mc = wc * pc - qc
    hc = Lc * Mc
    Pc = hc * pc**2
    Qc = hc * qc**2
    Rcubic = Lc * (
        Ac * pc**2
        + (1 - 3 * uc) * Tc * pc * qc
        + 4 * wc * Tc * qc**2
    )

    def tangent_form(vector, offset, monomials):
        converted = (
            (pc**2, pc * qc, qc**2)
            if len(monomials) == 3
            else (pc, qc)
        )
        return sum(
            C(vector[offset + index]) * converted[index]
            for index in range(len(converted))
        )

    tangent_basis = []
    for vector in basis7:
        tangent_basis.append(
            (
                tangent_form(vector, 0, u_monomials),
                tangent_form(vector, 3, v_monomials),
                tangent_form(vector, 6, t_monomials),
            )
        )
    tangent = tuple(
        c1 * tangent_basis[0][index] + c2 * tangent_basis[1][index]
        for index in range(3)
    )
    H4 = tuple(RC(form) for form in (Pc, Qc, PQC.zero))
    H3 = tuple(
        RC(form)
        for form in (rc * tangent[0], rc * tangent[1], Rcubic)
    )
    H2 = tuple(
        RC(form)
        for form in (
            PQC(x5) * rc**2,
            PQC(y5) * rc**2,
            rc * tangent[2],
        )
    )

    def derivative_pq(value, variable):
        answer = RC.zero
        for (r_degree,), coefficient in value.terms():
            answer += coefficient.diff(variable) * rc**r_degree
        return answer

    def jacobian(forms):
        return [
            [
                derivative_pq(form, pc),
                derivative_pq(form, qc),
                form.diff(rc),
            ]
            for form in forms
        ]

    J4 = jacobian(H4)
    J3 = jacobian(H3)
    J2 = jacobian(H2)
    weighted = determinant(
        [
            [
                zc * ZC(J2[row][column])
                + zc**2 * ZC(J3[row][column])
                + zc**3 * ZC(J4[row][column])
                for column in range(3)
            ]
            for row in range(3)
        ]
    )
    assert weighted.coeff(zc**7) == RC.zero
    e6r = weighted.coeff(zc**6).coeff(rc)
    equations6 = [
        e6r.coeff(pc ** (5 - index) * qc**index) for index in range(6)
    ]
    contact = [
        [
            equation.coeff(c1**2),
            equation.coeff(c1 * c2),
            equation.coeff(c2**2),
            equation.coeff(x5),
            equation.coeff(y5),
        ]
        for equation in equations6
    ]
    kernel, contact_pivots = nullspace(contact, K)

    constant_columns = (
        alpha * p,
        alpha * q,
        beta * p,
        beta * q,
        gamma,
    )
    constant_matrix = [
        [
            column.coeff(p ** (6 - index) * q**index)
            for column in constant_columns
        ]
        for index in range(7)
    ]
    _constant_kernel, constant_pivots = nullspace(constant_matrix, K)
    assert len(constant_pivots) == 5

    if len(contact_pivots) == 5:
        assert not kernel
        outcome = "contact rank 5"
    else:
        assert len(contact_pivots) == 4
        assert len(kernel) == 1
        vector = kernel[0]
        obstruction = vector[1] ** 2 - vector[0] * vector[2]
        assert obstruction != K.zero
        outcome = "contact rank 4, non-Veronese kernel"
    print(
        "PASS",
        label,
        "E7 rank 6;",
        outcome + ";",
        "constant rank 5",
    )


analyze("D=0,u=-1", w_symbol**2 + 1, "D")
analyze("D=0,u=3/5", 5 * w_symbol**2 - 3, "D")
analyze("H=0,u=9/11", 11 * w_symbol**2 - 9, "H")
analyze(
    "D=H=0,J(u)=0",
    55 * w_symbol**6 + 9 * w_symbol**4 - 3 * w_symbol**2 - 21,
    "D",
)
print("ALL INTERIOR FIXED/CONTACT PIVOT CHECKS PASSED")
