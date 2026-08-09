#!/usr/bin/env python3
"""Independent exact verifier for TRUE_INVERSE_RANK_PHASE_CONTRACTION.md.

Only Python Fraction and SymPy exact arithmetic are used.  This file does
not import a discovery script or another verifier.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import comb

import sympy as sp


State = tuple[str, int]


def zeros(rows: int, cols: int) -> list[list[F]]:
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def matvec(matrix: list[list[F]], vector: list[F]) -> list[F]:
    return [
        sum((entry * value for entry, value in zip(row, vector)), F(0))
        for row in matrix
    ]


def row_times(row: list[F], matrix: list[list[F]]) -> list[F]:
    return [
        sum((row[i] * matrix[i][j] for i in range(len(row))), F(0))
        for j in range(len(matrix[0]))
    ]


def matmul(left: list[list[F]], right: list[list[F]]) -> list[list[F]]:
    return [row_times(row, right) for row in left]


def inverse(matrix: list[list[F]]) -> list[list[F]]:
    n = len(matrix)
    augmented = [
        matrix[i][:] + [F(int(i == j)) for j in range(n)] for i in range(n)
    ]
    for col in range(n):
        pivot = next(row for row in range(col, n) if augmented[row][col])
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        scale = augmented[col][col]
        augmented[col] = [value / scale for value in augmented[col]]
        for row in range(n):
            if row == col or augmented[row][col] == 0:
                continue
            scale = augmented[row][col]
            augmented[row] = [
                x - scale * y for x, y in zip(augmented[row], augmented[col])
            ]
    return [row[n:] for row in augmented]


def identity_minus(matrix: list[list[F]]) -> list[list[F]]:
    return [
        [F(int(i == j)) - matrix[i][j] for j in range(len(matrix))]
        for i in range(len(matrix))
    ]


def quotient(N: int):
    states = (
        [("P", k) for k in range(1, N)]
        + [("Q", k) for k in range(1, N + 1)]
        + [("R", k) for k in range(1, N)]
    )
    index = {state: i for i, state in enumerate(states)}
    H = zeros(len(states), len(states))

    def add(source: State, target: State, mass: F) -> None:
        if mass and target in index:
            H[index[source]][index[target]] += mass

    for k in range(1, N):
        add(("P", k), ("P", k), F(k, 2 * N))
        add(("P", k), ("P", k + 1), F(N - k - 1, 2 * N))
        add(("P", k), ("Q", k + 1), F(1, 2 * N))

    for k in range(1, N + 1):
        add(("Q", k), ("Q", k), F(k * k - 1, 2 * k * N))
        add(("Q", k), ("Q", k + 1), F(N - k, 2 * N))
        add(("Q", k), ("P", k - 1), -F(k - 1, 2 * k * N))
        add(("Q", k), ("P", k), -F(N - k, 2 * k * N))
        add(("Q", k), ("R", k - 1), -F((k - 1) ** 2, 2 * k * N))
        add(("Q", k), ("R", k), -F((k - 1) * (N - k), 2 * k * N))

    for k in range(1, N):
        add(
            ("R", k),
            ("R", k),
            F(k, 2 * N) + F((k - 1) * (N - k), 2 * k * N),
        )
        add(("R", k), ("R", k + 1), F(N - k - 1, 2 * N))
        add(("R", k), ("R", k - 1), F((k - 1) ** 2, 2 * k * N))
        add(("R", k), ("Q", k), F(1, 2 * k * N))
        add(("R", k), ("P", k - 1), F(k - 1, 2 * k * N))
        add(("R", k), ("P", k), F(N - k, 2 * k * N))

    source = [F(0) for _ in states]
    for k in range(1, N):
        source[index[("R", k)]] = F(comb(N - 2, k - 1), 2 ** (N - 2))
    return states, H, source


def blocks(N: int):
    states, H, source = quotient(N)
    index = {state: i for i, state in enumerate(states)}
    good = [("P", k) for k in range(1, N)] + [
        ("R", k) for k in range(1, N)
    ]
    bad = [("Q", k) for k in range(1, N + 1)]
    S = [[H[index[a]][index[b]] for b in good] for a in good]
    C = [[H[index[a]][index[b]] for b in bad] for a in good]
    D = [[-H[index[a]][index[b]] for b in good] for a in bad]
    Q = [[H[index[a]][index[b]] for b in bad] for a in bad]
    s = [source[index[a]] for a in good]
    return states, H, good, bad, S, C, D, Q, s


def reward(N: int, good: list[State], bad: list[State]):
    gS = []
    for kind, k in good:
        if kind == "P":
            gS.append(F(1, k * (k + 1)))
        elif k == 1:
            gS.append(F(N, 2))
        else:
            gS.append(
                F(N, k * k * (k + 1)) + F(N + 1, (k - 1) * k * k)
            )
    q = []
    for _kind, k in bad:
        if k == 1:
            q.append(F(N - 1, 2))
        else:
            q.append(
                F(
                    2 * (N + 1) * k + 1 - k * k,
                    (k - 1) * k * k * (k + 1),
                )
            )
    return gS, [-x for x in q], q


def exact_data(N: int):
    _states, _H, good, bad, S, C, D, Q, source = blocks(N)
    gS, gQ, q = reward(N, good, bad)
    RS = inverse(identity_minus(S))
    RQ = inverse(identity_minus(Q))

    W = [F(N * N)] + [F(2 * N, k * (k - 1)) for k in range(2, N + 1)]
    rQ = [x - y for x, y in zip(matvec(identity_minus(Q), W), q)]
    expected_rQ = [F(N * N - N + 1)] + [
        F(N - 1, k * (k - 1)) for k in range(2, N + 1)
    ]
    assert rQ == expected_rQ

    rS = [x - y for x, y in zip(gS, matvec(C, W))]
    expected_rS = []
    for kind, k in good:
        if kind == "P" or k == 1:
            expected_rS.append(F(0))
        else:
            expected_rS.append(F(2 * N, (k - 1) * k * (k + 1)))
    assert rS == expected_rS

    h = matvec(RQ, rQ)
    assert all(x <= y <= z for x, y, z in zip(rQ, h, W))
    bar = [x + y for x, y in zip(rS, matvec(C, h))]
    direct_bar = [x + y for x, y in zip(gS, matvec(C, matvec(RQ, gQ)))]
    assert bar == direct_bar
    f0 = matvec(RS, bar)
    A = matmul(matmul(matmul(RS, C), RQ), D)
    return good, S, C, D, Q, source, f0, A


def phase_audit(max_N: int = 20) -> None:
    for N in range(2, max_N + 1):
        good, S, C, D, Q, _source, f0, A = exact_data(N)
        V = [F(N) if k == 1 else F(4 * N, k * k) + F(2, N) for k in range(1, N)]
        v = [V[k - 1] for _kind, k in good]
        hat = V + [V[-1]]
        RQ = inverse(identity_minus(Q))
        RS = inverse(identity_minus(S))

        bad_phase = matvec(RQ, matvec(D, v))
        assert all(x <= F(6, 5) * y for x, y in zip(bad_phase, hat))
        good_phase = matvec(RS, matvec(C, hat))
        if N >= 3:
            assert all(x <= F(2, N + 1) * y for x, y in zip(good_phase, v))
        Av = matvec(A, v)
        if N >= 3:
            assert all(x <= F(12, 5 * (N + 1)) * y for x, y in zip(Av, v))

        assert all(F(0) < x <= y for x, y in zip(f0, v))
        good_index = {state: i for i, state in enumerate(good)}
        if N >= 3:
            assert all(
                f0[good_index[("R", k)]] >= V[k - 1] / 3
                for k in range(1, N)
            )
    print(f"PASS (EXACT): coboundary and phase inequalities N=2..{max_N}")


def polynomial_audit() -> None:
    N, k, a, b = sp.symbols("N k a b", integer=True, nonnegative=True)
    V = lambda x: 4 * N / x**2 + sp.Rational(2, 1) / N
    v1 = N
    diag_q = (2 * k * N - k**2 + 1) / (2 * k * N)
    up_q = (N - k) / (2 * N)
    q_gap = sp.factor(
        sp.Rational(6, 5) * (diag_q * V(k) - up_q * V(k + 1))
        - ((k - 1) * V(k - 1) + (N - k) * V(k)) / (2 * N)
    )

    rdiag = k / (2 * N) + (k - 1) * (N - k) / (2 * k * N)
    rminus = (k - 1) ** 2 / (2 * k * N)
    rplus = (N - k - 1) / (2 * N)
    pminus = (k - 1) / (2 * k * N)
    pzero = (N - k) / (2 * k * N)
    c = 2 / (N + 1)
    d = 1 / (N + 1)
    good_gap = sp.factor(
        c
        * (
            (1 - rdiag) * V(k)
            - rminus * V(k - 1)
            - rplus * V(k + 1)
        )
        - d * (pminus * V(k - 1) + pzero * V(k))
        - V(k) / (2 * k * N)
    )
    upper_reward = 2 * N / ((k - 1) * k * (k + 1)) + 1 / (k**2 * (k - 1))
    upper_gap = sp.factor(
        (1 - rdiag) * V(k)
        - rminus * V(k - 1)
        - rplus * V(k + 1)
        - d * (pminus * V(k - 1) + pzero * V(k))
        - upper_reward
    )
    lower_reward = 2 * N / ((k - 1) * k * (k + 1)) + (N - 1) / (
        2 * k**2 * N * (k - 1)
    )
    lower_gap = sp.factor(
        lower_reward
        - sp.Rational(1, 3)
        * (
            (1 - rdiag) * V(k)
            - rminus * V(k - 1)
            - rplus * V(k + 1)
        )
    )

    for name, expression in (
        ("P_Q", q_gap),
        ("P_G", good_gap),
        ("P_U", upper_gap),
        ("P_L", lower_gap),
    ):
        shifted = sp.factor(expression.subs(N, k + 1 + b).subs(k, a + 3))
        numerator, denominator = sp.together(shifted).as_numer_denom()
        polynomial = sp.Poly(sp.expand(numerator), a, b)
        assert all(coefficient > 0 for coefficient in polynomial.coeffs()), name
        assert denominator.subs({a: 0, b: 0}) > 0

    q1 = sp.factor(
        sp.Rational(6, 5) * (v1 - (N - 1) * V(2) / (2 * N))
        - (N - 1) * v1 / (2 * N)
    )
    q2 = sp.factor(
        sp.Rational(6, 5)
        * ((4 * N - 3) * V(2) / (4 * N) - (N - 2) * V(3) / (2 * N))
        - (v1 + (N - 2) * V(2)) / (2 * N)
    )
    qtop = sp.factor(
        sp.Rational(6, 5) * (N**2 + 1) * V(N - 1) / (2 * N**2)
        - (N - 1) * V(N - 1) / (2 * N)
    )
    assert q1 == (N**3 + 11 * N**2 - 12 * N + 12) / (10 * N**2)
    assert q2 == (13 * N**3 + 4 * N**2 + 6 * N + 78) / (30 * N**2)
    assert qtop == (N + 2) * (N + 3) * (3 * N**2 - 2 * N + 1) / (
        5 * N**3 * (N - 1) ** 2
    )

    qpen = sp.factor(
        sp.Rational(6, 5)
        * (
            N * V(N - 1) / (2 * (N - 1))
            - V(N - 1) / (2 * N)
        )
        - ((N - 2) * V(N - 2) + V(N - 1)) / (2 * N)
    )
    expected_qpen = (
        3 * N**5 - 16 * N**4 + 26 * N**3 - 20 * N**2 - 3 * N - 2
    ) / (5 * N**2 * (N - 2) * (N - 1) ** 3)
    assert sp.factor(qpen - expected_qpen) == 0
    m = sp.symbols("m", nonnegative=True)
    shifted_qpen = sp.Poly(
        sp.expand(
            (3 * N**5 - 16 * N**4 + 26 * N**3 - 20 * N**2 - 3 * N - 2).subs(
                N, m + 4
            )
        ),
        m,
    )
    assert all(coefficient > 0 for coefficient in shifted_qpen.coeffs())

    print("PASS (SYMBOLIC): all coefficient and boundary certificates")


def small_schur_audit() -> None:
    expected = {
        2: F(12, 11),
        3: F(81, 40),
        4: F(212530, 85971),
        5: F(2934635, 1154592),
        6: F(278688977, 116460105),
        7: F(16076420403337, 7482829355520),
        8: F(5269741961413, 2799362256600),
    }
    for N, target in expected.items():
        _good, _S, _C, _D, _Q, source, f0, A = exact_data(N)
        inverse_I_plus_A = inverse(
            [
                [F(int(i == j)) + A[i][j] for j in range(len(A))]
                for i in range(len(A))
            ]
        )
        response = matvec(inverse_I_plus_A, f0)
        scalar = sum((x * y for x, y in zip(source, response)), F(0))
        assert scalar == target > 0
    print("PASS (EXACT): small-N Schur responses N=2..8")


if __name__ == "__main__":
    phase_audit()
    polynomial_audit()
    small_schur_audit()
    print("ALL TRUE-INVERSE-RANK PHASE-CONTRACTION CHECKS PASSED")
