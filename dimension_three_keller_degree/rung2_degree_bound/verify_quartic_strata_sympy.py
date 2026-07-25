#!/usr/bin/python3
"""Exact regressions for the quartic leading-stratum theorems.

The geometric divisor and Hilbert--Burch arguments are proved in the notes.
This script independently checks their determinant, adjugate, syzygy, and
sharpness identities.
"""

from __future__ import annotations

import sympy as sp


def coefficient(expression: sp.Expr, variable: sp.Symbol, degree: int) -> sp.Expr:
    return sp.Poly(sp.expand(expression), variable).coeff_monomial(variable**degree)


def line_14_determinant_checks() -> None:
    t = sp.symbols("t")
    pp, pq, qp, qq = sp.symbols("Pp Pq Qp Qq")
    up, uq, ur, vp, vq, vr = sp.symbols("Up Uq Ur Vp Vq Vr")
    rp, rq, rr = sp.symbols("Rp Rq Rr")
    ap, aq, ar, bp, bq, br, wp, wq, wr = sp.symbols(
        "Ap Aq Ar Bp Bq Br Wp Wq Wr"
    )
    linear_entries = sp.symbols("l11:14 l21:24 l31:34")

    L = sp.Matrix(3, 3, linear_entries)
    A = sp.Matrix([[ap, aq, ar], [bp, bq, br], [wp, wq, wr]])
    B = sp.Matrix([[up, uq, ur], [vp, vq, vr], [rp, rq, rr]])
    C = sp.Matrix([[pp, pq, 0], [qp, qq, 0], [0, 0, 0]])
    c = pp * qq - pq * qp
    a = qp * rq - qq * rp
    b = pp * rq - pq * rp

    determinant = sp.expand((L + t * A + t**2 * B + t**3 * C).det())
    assert sp.expand(coefficient(determinant, t, 8) - c * rr) == 0

    B_r_binary = B.subs(rr, 0)
    determinant_7 = sp.expand(
        (L + t * A + t**2 * B_r_binary + t**3 * C).det()
    )
    expected_7 = c * wr + a * ur - b * vr
    assert sp.expand(coefficient(determinant_7, t, 7) - expected_7) == 0

    B_binary = B_r_binary.subs({ur: 0, vr: 0})
    A_w_binary = A.subs(wr, 0)
    determinant_6 = sp.expand(
        (L + t * A_w_binary + t**2 * B_binary + t**3 * C).det()
    )
    expected_6 = c * L[2, 2] + a * ar - b * br
    assert sp.expand(coefficient(determinant_6, t, 6) - expected_6) == 0


def line_22_and_conic_checks() -> None:
    p, q = sp.symbols("p q")
    p_vector = sp.Matrix(sp.symbols("p1:4"))
    q_vector = sp.Matrix(sp.symbols("q1:4"))
    r_vector = sp.Matrix(sp.symbols("r1:4"))
    a1p, a1q, a2p, a2q = sp.symbols("a1p a1q a2p a2q")

    row_1 = (a1p * p_vector + a1q * q_vector).T
    row_2 = (a2p * p_vector + a2q * q_vector).T
    chain_determinant = sp.Matrix.vstack(row_1, row_2, r_vector.T).det()
    expected_chain = (a1p * a2q - a1q * a2p) * sp.Matrix.vstack(
        p_vector.T, q_vector.T, r_vector.T
    ).det()
    assert sp.expand(chain_determinant - expected_chain) == 0

    C = sp.Matrix.vstack(
        (2 * p * p_vector).T,
        (q * p_vector + p * q_vector).T,
        (2 * q * q_vector).T,
    )
    D = p_vector.cross(q_vector)
    n = sp.Matrix([q**2, -2 * p * q, p**2])
    assert sp.simplify(C.adjugate() - 2 * D * n.T) == sp.zeros(3)

    ell, emm = sp.symbols("ell emm")
    tangent = sp.Matrix([2 * p * ell, q * ell + p * emm, 2 * q * emm])
    assert sp.expand((n.T * tangent)[0]) == 0
    theta = q * ell - p * emm
    ver_small = sp.Matrix([ell**2, ell * emm, emm**2])
    assert sp.expand((n.T * ver_small)[0] - theta**2) == 0

    ell_vector = sp.Matrix(sp.symbols("ell1:4"))
    emm_vector = sp.Matrix(sp.symbols("emm1:4"))
    h_values = sp.Matrix(sp.symbols("h1:4"))
    h_gradients = [
        sp.Matrix(
            sp.symbols(
                f"h{index}1 h{index}2 h{index}3"
            )
        )
        for index in range(1, 4)
    ]
    A = sp.Matrix.vstack(
        h_gradients[0].T, h_gradients[1].T, h_gradients[2].T
    )
    B = sp.Matrix.vstack(
        (2 * ell * p_vector + 2 * p * ell_vector).T,
        (
            ell * q_vector
            + q * ell_vector
            + emm * p_vector
            + p * emm_vector
        ).T,
        (2 * emm * q_vector + 2 * q * emm_vector).T,
    )
    scale = sp.symbols("scale")
    conic_determinant = sp.expand((scale * A + scale**2 * B + scale**3 * C).det())

    n_gradients = [
        2 * q * q_vector,
        -2 * (q * p_vector + p * q_vector),
        2 * p * p_vector,
    ]
    gradient_n_dot_h = sum(
        (h_values[index] * n_gradients[index] + n[index] * h_gradients[index]
         for index in range(3)),
        sp.zeros(3, 1),
    )
    gradient_theta = (
        ell * q_vector
        + q * ell_vector
        - emm * p_vector
        - p * emm_vector
    )
    expected_degree_7 = 2 * D.dot(
        gradient_n_dot_h - 2 * theta * gradient_theta
    )
    assert sp.expand(
        coefficient(conic_determinant, scale, 7) - expected_degree_7
    ) == 0


def conic_degree_six_exclusion_checks() -> None:
    a_entries = sp.symbols("a0:9")
    A = sp.Matrix(3, 3, a_entries)
    b_1 = sp.Matrix(sp.symbols("b10:13"))
    b_2 = sp.Matrix(sp.symbols("b20:23"))
    k_1 = sp.Matrix(sp.symbols("k10:13"))
    k_2 = sp.Matrix(sp.symbols("k20:23"))
    updated = A + b_1 * k_1.T + b_2 * k_2.T
    rank_two_formula = (
        A.det()
        + (k_1.T * A.adjugate() * b_1)[0]
        + (k_2.T * A.adjugate() * b_2)[0]
        + (b_1.cross(b_2)).dot(A * k_1.cross(k_2))
    )
    assert sp.expand(updated.det() - rank_two_formula) == 0

    x, y, z = sp.symbols("x y z")
    variables = (x, y, z)

    def gradient(form: sp.Expr) -> sp.Matrix:
        return sp.Matrix([sp.diff(form, variable) for variable in variables])

    def coefficient_rank(first: sp.Expr, second: sp.Expr) -> int:
        d_vector = gradient(first).cross(gradient(second))
        normal = sp.Matrix([second**2, -2 * first * second, first**2])
        equation = sp.Poly(
            sp.expand((normal.T * A * d_vector)[0]), *variables
        )
        matrix, _ = sp.linear_eq_to_matrix(equation.coeffs(), a_entries)
        return matrix.rank()

    # One exact representative of each self-adjoint Jordan type.
    cases = (
        (y**2 + 2 * z**2, x**2 + y**2 + z**2),
        (y**2 + z**2, 2 * x * y + z**2),
        (2 * y * z, 2 * x * z + y**2),
    )
    assert [coefficient_rank(p_form, q_form) for p_form, q_form in cases] == [
        9,
        9,
        9,
    ]


def sharpness_and_gcd_checks() -> None:
    x, y, z = sp.symbols("x y z")
    p = x**2
    q = y * z
    R = x**3
    D = sp.Matrix([sp.diff(p, variable) for variable in (x, y, z)]).cross(
        sp.Matrix([sp.diff(q, variable) for variable in (x, y, z)])
    )
    assert sp.expand(
        sum(D[index] * sp.diff(R, variable) for index, variable in enumerate((x, y, z)))
    ) == 0

    p0, q0 = sp.symbols("p0 q0")
    P = p0**4 + q0**4
    Q = p0**3 * q0 + 2 * p0 * q0**3
    R0 = p0**3 + p0 * q0**2 + q0**3

    def jacobian_2(first: sp.Expr, second: sp.Expr) -> sp.Expr:
        return sp.expand(
            sp.diff(first, p0) * sp.diff(second, q0)
            - sp.diff(first, q0) * sp.diff(second, p0)
        )

    a = jacobian_2(Q, R0)
    b = jacobian_2(P, R0)
    c = jacobian_2(P, Q)
    assert sp.gcd(sp.gcd(a, b), c) == 1


def quadratic_coordinate_check() -> None:
    x, y, z = sp.symbols("x y z")
    a, b, c, d, e, beta = sp.symbols("a b c d e beta", nonzero=True)
    g = a * x**2 + b * x * y + c * y**2 + d * x + e * y
    T = sp.Matrix([x, y, g + beta * z])
    assert sp.expand(T.jacobian((x, y, z)).det() - beta) == 0
    inverse_z = (sp.symbols("w") - g) / beta
    assert sp.expand((g + beta * inverse_z) - sp.symbols("w")) == 0


if __name__ == "__main__":
    line_14_determinant_checks()
    line_22_and_conic_checks()
    conic_degree_six_exclusion_checks()
    sharpness_and_gcd_checks()
    quadratic_coordinate_check()
    print("PASS: exact quartic leading-stratum regressions")
