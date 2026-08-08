#!/usr/bin/env python3
"""Exact audit of the pin pure-birth inverse and renewal factorization.

This verifier is finite support for the all-N algebra proved in
``PIN_PURE_BIRTH_RENEWAL.md``.  It checks the exact factorization

    D = B^{-1} A = R diag(I, U^{-1}) C,

where U is a stochastic upper-bidiagonal pure-birth kernel, and verifies
the resulting nonnegative Markov-renewal factorization of every binary
pin word in a representative exact range.  It also records the first
failures of two tempting pointwise/TP strengthenings.
"""

from __future__ import annotations

from fractions import Fraction as Q
from itertools import product
from math import comb

import sympy as sp

from verify_standard_pin_one_crossing import (
    category_operator,
    operator_matrix,
)


def pure_birth(N: int) -> sp.Matrix:
    U = sp.zeros(N)
    for index in range(N):
        rank = index + 1
        U[index, index] = sp.Rational((N + 1) * rank - N, N * N)
        if rank < N:
            U[index, index + 1] = sp.Rational(
                (N + 1) * (N - rank), N * N
            )
    assert all(sum(U[row, column] for column in range(N)) == 1 for row in range(N))
    return U


def range_maps(N: int) -> tuple[sp.Matrix, sp.Matrix]:
    """Return positive embedding R and coordinate selector C."""

    dimension = 3 * N - 1
    R = sp.zeros(dimension, 2 * N)
    C = sp.zeros(2 * N, dimension)
    for index in range(N):
        R[index, index] = 1
        R[N + index, N + index] = 1
        C[index, index] = 1
        C[N + index, N + index] = 1
    for index in range(N - 1):
        # A range function satisfies O_k=I_(k+1).
        R[2 * N + index, N + index + 1] = 1
    assert C * R == sp.eye(2 * N)
    return R, C


def exact_initial_reward(
    states: list[tuple[str, int]], N: int
) -> tuple[sp.Matrix, sp.Matrix]:
    pi = [sp.Rational(comb(N - 1, k - 1), 2 ** (N - 1)) for k in range(1, N + 1)]
    nu = sp.Matrix([[
        sp.Rational({"A": 1, "I": rank, "O": N - rank}[kind], N + 1)
        * pi[rank - 1]
        for kind, rank in states
    ]])
    H = sp.Matrix([sp.Rational(1, rank) for _kind, rank in states])
    assert sum(nu) == 1
    return nu, H


def gap_vector(word: tuple[int, ...]) -> tuple[int, ...]:
    """Encode a 0=B,1=A word by B-run lengths around its A letters."""

    assert 1 in word
    gaps = []
    current = 0
    for letter in word:
        if letter:
            gaps.append(current)
            current = 0
        else:
            current += 1
    gaps.append(current)
    return tuple(gaps)


def direct_word(nu: sp.Matrix, A: sp.Matrix, B: sp.Matrix, H: sp.Matrix,
                word: tuple[int, ...]) -> sp.Expr:
    vector = H
    for letter in reversed(word):
        vector = (A if letter else B) * vector
    return sp.factor((nu * vector)[0])


def renewal_word(nu: sp.Matrix, A: sp.Matrix, B: sp.Matrix, H: sp.Matrix,
                 R: sp.Matrix, C: sp.Matrix, word: tuple[int, ...]) -> sp.Expr:
    gaps = gap_vector(word)
    row = nu * (B ** gaps[0]) * A * R
    for gap in gaps[1:-1]:
        row = row * C * (B ** gap) * A * R
    return sp.factor((row * C * (B ** gaps[-1]) * H)[0])


def all_exact_audits() -> None:
    word_count = 0
    for N in range(2, 9):
        states, A_operator = category_operator(N, Q(1))
        _, B_operator = category_operator(N, Q(1, N * N))
        A = operator_matrix(A_operator)
        B = operator_matrix(B_operator)
        D = B.inv() * A
        U = pure_birth(N)
        T = U.inv()
        R, C = range_maps(N)
        S = sp.diag(sp.eye(N), T)

        assert D == R * S * C
        assert B * D == A
        assert D * R == R * S
        assert all(value >= 0 for value in U)

        # Explicit alternating inverse formula.
        for k in range(1, N + 1):
            for ell in range(1, N + 1):
                expected = sp.Integer(0)
                if ell >= k:
                    expected = (
                        (-1) ** (ell - k)
                        * N**2
                        * (N + 1) ** (ell - k)
                        * sp.factorial(N - k)
                        / sp.factorial(N - ell)
                        / sp.prod((N + 1) * j - N for j in range(k, ell + 1))
                    )
                assert sp.factor(T[k - 1, ell - 1] - expected) == 0

        # Mixture factorization with the physical reset residual included.
        for p in (sp.Rational(0), sp.Rational(1, N + 1), sp.Rational(2, 3), sp.Rational(1)):
            Vp = p * sp.eye(N) + (1 - p) * U
            reduced_V = sp.diag(sp.eye(N), Vp)
            PW = sp.eye(3 * N - 1) - R * C
            left = (1 - p) * B + p * A
            right = A * R * reduced_V * C + (1 - p) * B * PW
            assert left == right

        nu, H = exact_initial_reward(states, N)
        transformed_nu = nu * sp.Matrix.hstack(
            R,
            sp.Matrix.vstack(sp.zeros(2 * N, N - 1), sp.eye(N - 1)),
        )
        for k in range(1, N + 1):
            pi = sp.Rational(comb(N - 1, k - 1), 2 ** (N - 1))
            assert transformed_nu[0, k - 1] == pi / (N + 1)
            assert transformed_nu[0, N + k - 1] == (2 * k - 1) * pi / (N + 1)
        for k in range(1, N):
            assert transformed_nu[0, 2 * N + k - 1] == (
                (N - k)
                * sp.Rational(comb(N - 1, k - 1), 2 ** (N - 1))
                / (N + 1)
            )

        # Every reduced gap kernel is nonnegative and stochastic because
        # C B^g A R is a composition of positive Markov maps.
        one = sp.ones(2 * N, 1)
        for gap in range(9):
            G = C * (B ** gap) * A * R
            assert all(value >= 0 for value in G)
            assert G * one == one

        if N <= 5:
            for length in range(1, 8):
                for word in product((0, 1), repeat=length):
                    if 1 not in word:
                        continue
                    assert direct_word(nu, A, B, H, word) == renewal_word(
                        nu, A, B, H, R, C, word
                    )
                    word_count += 1

    assert word_count == 988


def hostile_boundaries() -> None:
    # The pointwise cone U^{-1}Z>=0 fails first at N=4 on A^2 H.
    N = 4
    states, A_operator = category_operator(N, Q(1))
    _, B_operator = category_operator(N, Q(1, N * N))
    A = operator_matrix(A_operator)
    B = operator_matrix(B_operator)
    U = pure_birth(N)
    H = sp.Matrix([sp.Rational(1, rank) for _kind, rank in states])
    response = A * A * H
    I_values = response[N:2 * N, :]
    assert (U.inv() * I_values)[0] == -sp.Rational(2213, 9216)

    # Even the most local renewal split is not entrywise positive.
    R, C = range_maps(N=3)
    _, A3_operator = category_operator(3, Q(1))
    _, B3_operator = category_operator(3, Q(1, 9))
    A3 = operator_matrix(A3_operator)
    B3 = operator_matrix(B3_operator)
    G0 = C * A3 * R
    G1 = C * B3 * A3 * R
    split = G0 * G0 - G1
    assert split[0, 4] == -sp.Rational(2, 9)

    # The one-versus-rest conditional reward sequence is not log-convex,
    # even though its needed first-difference/quotient signs survive.
    nu3, H3 = exact_initial_reward(list(category_operator(3, Q(1))[0]), 3)
    controls = [H3]
    for time in range(1, 19):
        previous = controls
        controls = []
        for count in range(time + 1):
            value = sp.zeros(len(H3), 1)
            if count < time:
                value += sp.Rational(time - count, time) * B3 * previous[count]
            if count:
                value += sp.Rational(count, time) * A3 * previous[count - 1]
            controls.append(value)
    psi = [(nu3 * value)[0] for value in controls]
    log_convex_defect = sp.factor(psi[17] ** 2 - psi[16] * psi[18])
    assert log_convex_defect == sp.Rational(
        392199485892499790434361171,
        170435555370257609364945286201344,
    ) > 0


def main() -> None:
    all_exact_audits()
    hostile_boundaries()
    print("PASS (EXACT FINITE): pure-birth inverse N=2..8")
    print("PASS (EXACT FINITE): 988 binary words match renewal factorization")
    print(
        "EXACTLY REFUTED: pointwise U^{-1} cone, local gap-split positivity, "
        "and conditional log-convexity"
    )
    print("OPEN: ballot/TP sign after summing complete gap compositions")


if __name__ == "__main__":
    main()
