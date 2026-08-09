#!/usr/bin/env python3
"""Exact refutation of the vertex-forgotten oriented rank-current cone.

This is *not* a graph or a rank-pair pseudoflow.  It is an exact feasible
point of the scalar relaxation retaining only rank mass flow, the stationary
mass/cut recurrences, event-moment bounds, and the oriented gain bounds.  Its
flux exceeds the K_3 baseline, proving that those scalar consequences cannot
establish the universal endpoint without the individual vertex balances.
"""

from fractions import Fraction as Q


N = 3
Z = Q(5, 9)

# Indices zero and N are absent boundary entries and are fixed to zero.
A = (Q(0), Q(5, 6), Q(5, 9), Q(0))
R = (Q(0), Q(4, 9), Q(5, 18), Q(0))
C = (Q(0), Q(2, 9), Q(5, 18), Q(0))
Q_PLUS = (Q(0), Q(1, 12), Q(0), Q(0))
Q_MINUS = (Q(0), Q(0), Q(5, 36), Q(0))
X_M = (Q(0), Q(1, 4), Q(5, 18), Q(0))
Y_M = (Q(0), Q(2, 9), Q(5, 18), Q(0))
X_C = (Q(0), Q(1, 4), Q(5, 18), Q(0))
Y_C = (Q(0), Q(2, 9), Q(0), Q(0))


def main() -> None:
    # Rank mass flow.
    for k in range(1, N + 1):
        residual = Q(int(k == 1)) + A[k - 1] + (R[k + 1] if k < N else 0)
        residual -= (A[k] if k < N else 0) + (R[k] if k < N else 0)
        residual -= Z * int(k == N)
        assert residual == 0

    # Rank-labelled stationary-mass and cut contractions.  The k=0
    # equations are structural empty-boundary cancellations.
    for k in range(N + 1):
        mass_residual = Q(1, N) * int(k == 1)
        if k:
            mass_residual += X_M[k - 1] + C[k - 1] + Q_PLUS[k - 1]
        if k < N:
            mass_residual += Y_M[k + 1] + Q_MINUS[k + 1] - C[k + 1]
            mass_residual -= X_M[k] + Y_M[k]
        mass_residual -= Z * int(k == N)
        assert mass_residual == 0

        cut_residual = Q(1, N) * int(k == 1)
        if k:
            cut_residual += X_C[k - 1] + 3 * Q_PLUS[k - 1] - C[k - 1]
        if k < N:
            cut_residual += Y_C[k + 1] + 3 * Q_MINUS[k + 1] - C[k + 1]
            cut_residual -= X_C[k] + Y_C[k]
        assert cut_residual == 0

    # Every retained scalar positivity/event-moment constraint.
    for k in range(1, N):
        assert 0 <= X_M[k] <= A[k]
        assert 0 <= Y_M[k] <= R[k]
        assert 0 <= X_C[k] <= X_M[k]
        assert X_C[k] <= A[k] - X_M[k]
        assert 0 <= Y_C[k] <= Y_M[k]
        assert Y_C[k] <= R[k] - Y_M[k]
        assert 0 <= Q_PLUS[k] <= C[k]
        assert 0 <= 2 * Q_MINUS[k] <= C[k]

    # Exact singleton/top structural identities used by the relaxation.
    assert Q_MINUS[1] == 0 and Q_PLUS[N - 1] == 0
    assert X_M[1] == X_C[1]
    assert Y_M[1] == Y_C[1] == C[1]
    assert X_M[N - 1] == A[N - 1] - C[N - 1]
    assert X_C[N - 1] == C[N - 1]

    baseline = Q(4, 9)
    assert Z == Q(5, 9) > baseline
    assert sum(Q_PLUS) + sum(Q_MINUS) == Z - Q(1, N)
    assert sum(C) == Q(3, 2) * Z - Q(1, N)
    print("oriented scalar rank-current cone refutation: PASS")
    print("exact relaxed flux: 5/9")
    print("K_3 baseline: 4/9")
    print("this is a scalar-cone point, not a graph pseudoflow")


if __name__ == "__main__":
    main()
