#!/usr/bin/env python3
"""Exact limitation model for the commuting-square/projective-descent route.

This constructs a faithful H_3(3,6) pair p,q on C^4 tensor C^2 such that

    p = p_0 tensor I_2,
    E_last(alg(p,q)) = alg(p_0),

and p,q obey the exceptional projection cubic.  Thus the first nontrivial
Markov commuting square exists already at formal local dimension d=2, even
though q is not I_2 tensor p_0 and no ordinary d=2 localizer exists.

All arithmetic is exact in Q(sqrt(2),sqrt(3),i).
"""

from __future__ import annotations

import sympy as sp


def projection(v: sp.Matrix) -> sp.Matrix:
    return v * v.conjugate().T


def partial_trace_last_qubit(a: sp.Matrix) -> sp.Matrix:
    """Unnormalized partial trace C^2_A tensor C^2_B tensor C^2_C -> AB."""

    out = sp.zeros(4)
    for aa in range(2):
        for bb in range(2):
            for ap in range(2):
                for bp in range(2):
                    out[2 * aa + bb, 2 * ap + bp] = sp.simplify(
                        sum(
                            a[4 * aa + 2 * bb + cc, 4 * ap + 2 * bp + cc]
                            for cc in range(2)
                        )
                    )
    return out


def is_zero(a: sp.Matrix) -> bool:
    return all(sp.simplify(x) == 0 for x in a)


def main() -> None:
    ii = sp.I
    sqrt2 = sp.sqrt(2)
    sqrt3 = sp.sqrt(3)
    omega = (-1 + ii * sqrt3) / 2

    # Bell basis on B tensor C.
    phi_plus = sp.Matrix([1, 0, 0, 1]) / sqrt2
    phi_minus = sp.Matrix([1, 0, 0, -1]) / sqrt2
    psi_plus = sp.Matrix([0, 1, 1, 0]) / sqrt2
    psi_minus = sp.Matrix([0, 1, -1, 0]) / sqrt2

    u = projection(phi_plus)
    t = (
        projection(phi_minus)
        + omega * projection(psi_plus)
        + omega**2 * projection(psi_minus)
    )

    # Relative to the first qubit A, h_1=diag(I_4,-I_4).  The common
    # (+,+) and (-,-) lines are both the Bell line C phi_plus.  The three
    # generic two-projection blocks have reflection angle c=-1/3, and t
    # supplies arbitrary phases 1,omega,omega^2 between their two sides.
    a = -sp.eye(4) / 3 + 4 * u / 3
    d = sp.eye(4) / 3 - 4 * u / 3
    off = 2 * sqrt2 * t / 3
    h2 = a.row_join(off).col_join(off.conjugate().T.row_join(d))
    h1 = sp.diag(*([1] * 4 + [-1] * 4))

    ident8 = sp.eye(8)
    p = (ident8 - h1) / 2
    q = (ident8 - h2) / 2
    p0 = sp.diag(0, 0, 1, 1)

    assert sp.simplify(omega**2 + omega + 1) == 0
    assert h2 == h2.conjugate().T
    assert is_zero(h1 * h1 - ident8)
    assert is_zero(h2 * h2 - ident8)
    assert sp.trace(h1) == 0
    assert sp.trace(h2) == 0

    h_residual = sp.simplify(
        h1 * h2 * h1 - h2 * h1 * h2 - sp.Rational(1, 3) * (h1 - h2)
    )
    p_residual = sp.simplify(
        p * q * p - q * p * q - sp.Rational(1, 3) * (p - q)
    )
    assert is_zero(h_residual)
    assert is_zero(p_residual)
    assert p.rank() == q.rank() == 4
    assert is_zero(p - sp.kronecker_product(p0, sp.eye(2)))

    # E_C=(1/2)Tr_C is the trace-preserving expectation M_8 -> M_4.
    assert is_zero(partial_trace_last_qubit(h2))
    assert partial_trace_last_qubit(q) == sp.eye(4)

    # A basis for alg(p,q).  Every expected image is in span{I_4,p_0}.
    basis = [ident8, p, q, p * q, q * p, p * q * p]
    basis_rank = sp.Matrix.hstack(*(x.reshape(64, 1) for x in basis)).rank()
    assert basis_rank == 6
    expected_partial_traces = [
        2 * sp.eye(4),
        2 * p0,
        sp.eye(4),
        p0,
        p0,
        p0,
    ]
    for x, expected in zip(basis, expected_partial_traces):
        assert partial_trace_last_qubit(x) == expected

    # Faithful H_3 block data: one (+,+) endpoint, one (-,-) endpoint,
    # and three generic 2D blocks with P-angle squared 1/3.
    pqp_spectrum = (p * q * p).eigenvals()
    assert pqp_spectrum == {sp.Integer(0): 4, sp.Integer(1): 1, sp.Rational(1, 3): 3}

    # The model is deliberately not tensor-local with the same p_0.
    q_local_candidate = sp.kronecker_product(sp.eye(2), p0)
    local_defect_sq = sp.simplify(
        sp.trace((q - q_local_candidate).conjugate().T * (q - q_local_candidate))
    )
    assert local_defect_sq == 4

    # Inclusion-matrix arithmetic after spectator amplification by
    # (C^s)^{tensor n}.  Rows are the two H_2 simples and columns are the
    # endpoint, generic M_2, endpoint H_3 simples.
    ss = sp.symbols("s", integer=True, positive=True)
    inclusion = sp.Matrix([[1, 1, 0], [0, 1, 1]])
    mult2 = sp.Matrix([2 * ss**2, 2 * ss**2])
    mult3 = sp.Matrix([ss**3, 3 * ss**3, ss**3])
    assert inclusion * mult3 == 2 * ss * mult2
    assert sum(mult2) == (2 * ss) ** 2
    assert sp.Matrix([1, 2, 1]).dot(mult3) == (2 * ss) ** 3

    print("Exact d=2 first commuting-square limitation model")
    print("field = Q(sqrt(2),sqrt(3),i)")
    print("rank(p) = rank(q) = 4")
    print("dim alg(p,q) = 6")
    print("h cubic residual = 0")
    print("projection cubic residual = 0")
    print("Tr_C(h2) = 0")
    print("Tr_C(q) = I_4")
    print("E_C(alg(p,q)) = alg(p0)")
    print("spectrum multiplicities of p q p = {0:4, 1/3:3, 1:1}")
    print("||q - I_2 tensor p0||_HS^2 = 4")
    print("amplified inclusion identity G m3 = (2s) m2 holds for every s >= 1")
    print("ordinary d=2 tensor locality is intentionally absent")


if __name__ == "__main__":
    main()
