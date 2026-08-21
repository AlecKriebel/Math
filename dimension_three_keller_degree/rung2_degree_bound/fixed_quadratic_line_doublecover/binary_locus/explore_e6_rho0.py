#!/usr/bin/env python3
"""Exact E6 rank exploration after a zero E7 tangent."""

import sympy as sp

p, q, r = sp.symbols("p q r")
vp, vq, wp, wq, vr, wr, ell = sp.symbols(
    "vp vq wp wq vr wr ell"
)


def coefficient_rows(value, variables):
    poly = sp.Poly(sp.expand(value), p, q, r)
    rows = [coefficient for _, coefficient in poly.terms()]
    matrix, rhs = sp.linear_eq_to_matrix(rows, variables)
    assert rhs == sp.zeros(len(rows), 1)
    return matrix


def ranks(h, R):
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    D = sp.Matrix(
        [[sp.diff(P, p), sp.diff(P, q)],
         [sp.diff(Q, p), sp.diff(Q, q)]]
    )
    v = sp.Matrix(
        [vp * p + vq * q + vr * r, wp * p + wq * q + wr * r]
    )
    grad = sp.Matrix([[sp.diff(R, p), sp.diff(R, q)]])
    equation = sp.expand(D.det() * ell - (grad * D.adjugate() * v)[0])
    rpart = sp.Poly(equation, r).coeff_monomial(r)
    zero = sp.Poly(equation, r).coeff_monomial(1)
    return (
        coefficient_rows(rpart, (vr, wr)).rank(),
        coefficient_rows(zero, (vp, vq, wp, wq, ell)).rank(),
    )


samples = (
    (p * q, p**3 + q**3, "pq transverse"),
    (p * (p + q), p**3 + p**2 * q + q**3, "one branch transverse"),
    (
        p**2 + q**2,
        p**3 + 2 * p**2 * q + 3 * p * q**2 + 4 * q**3,
        "interior generic",
    ),
    (p**2 + q**2, p**3 + p**2 * q + q**3, "interior split 1"),
    (p**2 + q**2, p**3 + q**3, "interior split 2"),
)
for h, R, label in samples:
    print(label, ranks(h, R))
