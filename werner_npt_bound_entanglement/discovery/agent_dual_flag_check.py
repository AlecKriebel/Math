#!/usr/bin/env python3
"""Exact check of the rank-two positive flag-dilation identity (E15)."""

import sympy as sp


D_LOCAL = 3
HALF = sp.Rational(1, 2)


def matrix_unit(i: int, j: int) -> sp.Matrix:
    out = sp.zeros(D_LOCAL)
    out[i, j] = 1
    return out


def hs_inner(a: sp.Matrix, b: sp.Matrix) -> sp.Expr:
    return sp.trace(a.conjugate().T * b)


def b_one(a: sp.Matrix, b: sp.Matrix) -> sp.Expr:
    """Polarized endpoint form for one copy."""
    return sp.simplify(
        hs_inner(a, b)
        - HALF * sp.conjugate(sp.trace(a)) * sp.trace(b)
    )


def q_one(a: sp.Matrix) -> sp.Expr:
    return b_one(a, a)


def partial_trace_two_factor(a: sp.Matrix, factor: int) -> sp.Matrix:
    d = D_LOCAL
    out = sp.zeros(d)
    if factor == 0:
        for j in range(d):
            for ell in range(d):
                out[j, ell] = sum(a[i * d + j, i * d + ell]
                                  for i in range(d))
    elif factor == 1:
        for i in range(d):
            for k in range(d):
                out[i, k] = sum(a[i * d + j, k * d + j]
                                for j in range(d))
    else:
        raise ValueError("factor must be 0 or 1")
    return out


def q_two(a: sp.Matrix) -> sp.Expr:
    tr0 = partial_trace_two_factor(a, 0)
    tr1 = partial_trace_two_factor(a, 1)
    return sp.simplify(
        hs_inner(a, a)
        - HALF * hs_inner(tr0, tr0)
        - HALF * hs_inner(tr1, tr1)
        + HALF**2 * sp.conjugate(sp.trace(a)) * sp.trace(a)
    )


def main() -> None:
    # D maps |1>,|2> isometrically onto |0>,|1>.
    d_map = matrix_unit(0, 1) + matrix_unit(1, 2)
    p_right = d_map.conjugate().T * d_map
    p_left = d_map * d_map.conjugate().T

    p = sp.Integer(2)
    q = sp.Integer(3)
    root_pq = sp.sqrt(p * q)
    e00 = matrix_unit(0, 0)
    e01 = matrix_unit(0, 1)
    e10 = matrix_unit(1, 0)
    e11 = matrix_unit(1, 1)
    dilation = (
        p * sp.kronecker_product(e00, p_right)
        + root_pq * sp.kronecker_product(e01, d_map.conjugate().T)
        + root_pq * sp.kronecker_product(e10, d_map)
        + q * sp.kronecker_product(e11, p_left)
    )

    a_right = q_one(p_right)
    a_left = q_one(p_left)
    mixed = b_one(p_right, p_left)
    q_d = q_one(d_map)
    rhs = sp.simplify(
        HALF * p**2 * a_right
        + HALF * q**2 * a_left
        + 2 * p * q * q_d
        - p * q * sp.re(mixed)
    )
    lhs = q_two(dilation)

    assert dilation.rank() == 2
    assert dilation == dilation.conjugate().T
    assert lhs == rhs

    print("rank(E) =", dilation.rank())
    print("E is Hermitian:", dilation == dilation.conjugate().T)
    print("Q_2(E) =", lhs)
    print("right side of (E15) =", rhs)


if __name__ == "__main__":
    main()
