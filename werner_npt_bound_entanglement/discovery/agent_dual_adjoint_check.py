#!/usr/bin/env python3
"""Exact check of the adjoint-mixed normalizing-swap obstruction.

For W = I - |Phi><Phi| and two W-replicas, this verifies

    Q(D) = -2,    Q(D S) = +2,

where D = C1 tensor C2 - C2 tensor C1 and C1,C2 are two orthogonal
rank-one projections.  All arithmetic is exact SymPy arithmetic.
"""

import sympy as sp


D_LOCAL = 3


def matrix_unit(i: int, j: int) -> sp.Matrix:
    out = sp.zeros(D_LOCAL)
    out[i, j] = 1
    return out


def hs_norm_squared(a: sp.Matrix) -> sp.Expr:
    return sp.trace(a.conjugate().T * a)


def partial_trace_two_factor(a: sp.Matrix, factor: int) -> sp.Matrix:
    """Partial trace of a coefficient matrix on (C^d) tensor (C^d)."""
    d = D_LOCAL
    out = sp.zeros(d)
    if factor == 0:
        # Trace the first tensor factor; retain the second.
        for j in range(d):
            for ell in range(d):
                out[j, ell] = sum(a[i * d + j, i * d + ell]
                                  for i in range(d))
    elif factor == 1:
        # Trace the second tensor factor; retain the first.
        for i in range(d):
            for k in range(d):
                out[i, k] = sum(a[i * d + j, k * d + j]
                                for j in range(d))
    else:
        raise ValueError("factor must be 0 or 1")
    return out


def q_two_replicas(a: sp.Matrix) -> sp.Expr:
    """Expectation of (I-|Phi><Phi|) tensor-square."""
    tr0 = partial_trace_two_factor(a, 0)
    tr1 = partial_trace_two_factor(a, 1)
    return sp.simplify(
        hs_norm_squared(a)
        - hs_norm_squared(tr0)
        - hs_norm_squared(tr1)
        + sp.conjugate(sp.trace(a)) * sp.trace(a)
    )


def swap_matrix() -> sp.Matrix:
    d = D_LOCAL
    out = sp.zeros(d * d)
    for i in range(d):
        for j in range(d):
            out[j * d + i, i * d + j] = 1
    return out


def main() -> None:
    c1 = matrix_unit(0, 0)
    c2 = matrix_unit(1, 1)
    d_cross = sp.kronecker_product(c1, c2) - sp.kronecker_product(c2, c1)
    normal = d_cross * swap_matrix()

    assert d_cross.rank() == 2
    assert normal.rank() == 2
    assert normal.conjugate().T == -normal
    assert q_two_replicas(d_cross) == -2
    assert q_two_replicas(normal) == 2

    print("rank(D) =", d_cross.rank())
    print("rank(D S) =", normal.rank())
    print("(D S)^dagger = -(D S):", normal.conjugate().T == -normal)
    print("Q(D) =", q_two_replicas(d_cross))
    print("Q(D S) =", q_two_replicas(normal))


if __name__ == "__main__":
    main()
