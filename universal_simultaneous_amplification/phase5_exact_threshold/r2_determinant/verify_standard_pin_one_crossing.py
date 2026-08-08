#!/usr/bin/env python3
"""Exact finite audit of the common-pin count sign pattern.

The distinguished pin leaves only ``3N-1`` active-state orbits.  This
script constructs their two exact operators:

* ``A``: every ordinary source points to the distinguished pin;
* ``B``: the average of all other pin operators.

It independently checks the lump against labelled active chains at small
orders and then audits, over exact rationals, two observed sign-regularity
patterns for the conditional pin-count controls ``psi[t,c]``:

* ``Delta psi[t,c]`` changes sign at most once, from negative to positive;
* ``Delta^2 psi[t,c]`` changes sign at most once, from positive to negative.

The finite audit is not an all-order proof.  The exact derivative and
binomial covariance identities explain why the second pattern, together
with the positive terminal slope, would prove the standard-sector sign.
"""

from __future__ import annotations

from fractions import Fraction as Q
from math import comb

import sympy as sp

from verify_standard_pin_bernstein import (
    Operator,
    active_operator,
    add_scaled,
    apply,
    dot,
    operator_average,
    replacement_pin,
)


Category = tuple[str, int]


def category_states(N: int) -> list[Category]:
    return [
        (kind, rank)
        for kind in ("A", "I", "O")
        for rank in range(1, N + 1)
        if not (kind == "O" and rank == N)
    ]


def category_operator(N: int, alpha: Q) -> tuple[list[Category], Operator]:
    """Build the exact stabilizer quotient for a two-class replacement row.

    Row ``x`` is uniform on the ``N`` ordinary vertices.  From an ordinary
    source, the probability of choosing ``x`` is ``alpha`` and the
    probability of each of the other ``N-1`` ordinary targets is ``beta``.
    """

    beta = (1 - alpha) / (N - 1)
    states = category_states(N)
    index = {state: position for position, state in enumerate(states)}
    operator: Operator = []

    for kind, rank in states:
        row: dict[int, Q] = {}

        def add(target_kind: str, target_rank: int, mass: Q) -> None:
            if not mass:
                return
            target = index[(target_kind, target_rank)]
            row[target] = row.get(target, Q(0)) + mass

        if kind == "A":
            add("A", rank, Q(rank, 2 * N))
            if rank < N:
                add("A", rank + 1, Q(N - rank, 2 * N))
            add("I", rank, alpha / 2)
            if rank > 1:
                add("O", rank - 1, Q(rank - 1, 2) * beta)
            if rank < N:
                add("O", rank, Q(N - rank, 2) * beta)

        elif kind == "I":
            add("I", rank, (alpha + (rank - 1) * beta) / 2)
            if rank < N:
                add("I", rank + 1, Q(N - rank, 2) * beta)
            if rank > 1:
                add("A", rank - 1, Q(rank - 1, 2 * rank * N))
            add("A", rank, Q(N - rank + 1, 2 * rank * N))
            if rank > 1:
                add(
                    "I",
                    rank - 1,
                    Q(rank - 1, 2 * rank) * (alpha + (rank - 2) * beta),
                )
            add(
                "I",
                rank,
                Q((rank - 1) * (N - rank + 1), 2 * rank) * beta,
            )

        else:
            add("I", rank + 1, alpha / 2)
            add("O", rank, Q(rank, 2) * beta)
            if rank < N - 1:
                add("O", rank + 1, Q(N - rank - 1, 2) * beta)
            add("I", rank, alpha / 2)
            if rank > 1:
                add("O", rank - 1, Q(rank - 1, 2) * beta)
            add("O", rank, Q(N - rank, 2) * beta)

        assert sum(row.values(), Q(0)) == 1
        operator.append(row)
    return states, operator


def category_of(labelled_state: tuple[int, int], pin: int = 0) -> Category:
    Bset, target = labelled_state
    rank = Bset.bit_count()
    if target == pin:
        return "A", rank
    if (Bset >> pin) & 1:
        return "I", rank
    return "O", rank


def aggregate_row(
    row: dict[int, Q],
    labelled_states: list[tuple[int, int]],
    category_index: dict[Category, int],
) -> dict[int, Q]:
    answer: dict[int, Q] = {}
    for target, mass in row.items():
        orbit = category_index[category_of(labelled_states[target])]
        answer[orbit] = answer.get(orbit, Q(0)) + mass
    return {target: mass for target, mass in answer.items() if mass}


def labelled_lump_audit() -> None:
    """Independently compare the quotient with every labelled row."""

    for n in range(3, 6):
        N = n - 1
        categories, A = category_operator(N, Q(1))
        _, B = category_operator(N, Q(1, N * N))
        category_index = {state: position for position, state in enumerate(categories)}

        labelled_states, labelled_A = active_operator(replacement_pin(n, 0))
        other_operators = [
            active_operator(replacement_pin(n, pin))[1]
            for pin in range(1, n)
        ]
        labelled_B = operator_average(other_operators)

        for source, state in enumerate(labelled_states):
            orbit = category_index[category_of(state)]
            assert aggregate_row(
                labelled_A[source], labelled_states, category_index
            ) == A[orbit]
            assert aggregate_row(
                labelled_B[source], labelled_states, category_index
            ) == B[orbit]


def ordered_signs(values: list[Q], direction: str) -> bool:
    signs = [1 if value > 0 else -1 if value < 0 else 0 for value in values]
    signs = [sign for sign in signs if sign]
    if direction == "up":
        return all(left <= right for left, right in zip(signs, signs[1:]))
    assert direction == "down"
    return all(left >= right for left, right in zip(signs, signs[1:]))


def binomial_weight(order: int, count: int, p: Q) -> Q:
    return Q(comb(order, count)) * p**count * (1 - p) ** (order - count)


def operator_matrix(operator: Operator) -> sp.Matrix:
    dimension = len(operator)
    return sp.Matrix(
        [
            [
                sp.Rational(
                    operator[row].get(column, Q(0)).numerator,
                    operator[row].get(column, Q(0)).denominator,
                )
                for column in range(dimension)
            ]
            for row in range(dimension)
        ]
    )


def generalized_pencil_audit() -> None:
    """Check the exact binomial generalized eigensystem and factorization."""

    for N in range(2, 8):
        states, A_operator = category_operator(N, Q(1))
        _, B_operator = category_operator(N, Q(1, N * N))
        A = operator_matrix(A_operator)
        B = operator_matrix(B_operator)
        index = {state: position for position, state in enumerate(states)}
        vectors: list[sp.Matrix] = []
        eigenvalues: list[sp.Rational] = []

        # The distinguished-pin operator never outputs an O state.
        for rank in range(1, N):
            vector = sp.zeros(len(states), 1)
            vector[index[("O", rank)]] = 1
            assert A * vector == sp.zeros(len(states), 1)
            vectors.append(vector)
            eigenvalues.append(sp.Rational(0))

        # All columns leading into A, and the total I/O column, are
        # independent of the ordinary-row parameter.
        for rank in range(1, N + 1):
            vector = sp.zeros(len(states), 1)
            vector[index[("A", rank)]] = 1
            assert A * vector == B * vector
            vectors.append(vector)
            eigenvalues.append(sp.Rational(1))
        constant_io = sp.zeros(len(states), 1)
        for kind, rank in states:
            if kind != "A":
                constant_io[index[(kind, rank)]] = 1
        assert A * constant_io == B * constant_io
        vectors.append(constant_io)
        eigenvalues.append(sp.Rational(1))

        for degree in range(1, N):
            vector = sp.zeros(len(states), 1)
            for rank in range(1, N + 1):
                vector[index[("I", rank)]] = comb(N - rank, degree)
            for rank in range(1, N):
                vector[index[("O", rank)]] = comb(N - rank - 1, degree)
            eigenvalue = sp.Rational(
                N * N, N * N - (N + 1) * degree
            )
            assert A * vector == eigenvalue * B * vector
            vectors.append(vector)
            eigenvalues.append(eigenvalue)

        basis = sp.Matrix.hstack(*vectors)
        assert basis.det() != 0
        assert B.det() != 0
        diagonal = sp.diag(*eigenvalues)
        assert A * basis == B * basis * diagonal
        # Therefore A-zB=B*basis*(diagonal-zI)*basis^{-1}; the displayed
        # generalized eigenvalues give the complete determinant factor.


def exact_screen() -> tuple[int, int, int, int]:
    first_negative_order = 0
    first_negative_time = 0
    first_negative_count = 0
    checked_pairs = 0

    for n in range(3, 9):
        N = n - 1
        categories, A = category_operator(N, Q(1))
        _, B = category_operator(N, Q(1, N * N))
        p0 = Q(1, n)
        nu = [
            Q(comb(N - 1, rank - 1), 2 ** (N - 1))
            * Q({"A": 1, "I": rank, "O": N - rank}[kind], N + 1)
            for kind, rank in categories
        ]
        H = [Q(1, rank) for _kind, rank in categories]

        controls = [H]
        for time in range(1, 51):
            previous = controls
            controls = []
            for count in range(time + 1):
                B_part = apply(B, previous[count]) if count < time else None
                A_part = apply(A, previous[count - 1]) if count else None
                controls.append(
                    add_scaled(
                        B_part,
                        Q(time - count, time),
                        A_part,
                        Q(count, time),
                    )
                )

            psi = [dot(nu, vector) for vector in controls]
            first = [psi[count + 1] - psi[count] for count in range(time)]
            assert ordered_signs(first, "up")

            # Label symmetry makes the directional derivative vanish at the
            # uniform pin law.  This is checked from the count controls, not
            # inserted as a formal symmetry assumption.
            derivative = time * sum(
                binomial_weight(time - 1, count, p0) * value
                for count, value in enumerate(first)
            )
            assert derivative == 0
            if time < 2:
                continue

            # Divide the symmetry root from Phi_t'/t in the Bernstein
            # basis.  Positivity of these quotient controls is weaker than
            # pointwise one-crossing of the first differences and already
            # proves that the uniform pin frequency is a ray minimum.
            order = time - 1
            quotient_controls: list[Q] = []
            for count in range(order):
                previous = quotient_controls[count - 1] if count else Q(0)
                value = (
                    (1 - p0) * Q(count, order) * previous - first[count]
                ) / (p0 * Q(order - count, order))
                quotient_controls.append(value)
            assert first[-1] == (1 - p0) * quotient_controls[-1]
            assert all(value > 0 for value in quotient_controls)
            second = [
                first[count + 1] - first[count]
                for count in range(time - 1)
            ]
            assert ordered_signs(second, "down")
            assert first[-1] > 0

            weighted_second = sum(
                binomial_weight(time - 2, count, p0) * value
                for count, value in enumerate(second)
            )
            assert weighted_second > 0

            # Exact binomial score/covariance identity for Phi''(p0).
            score_covariance = Q(0)
            score_mean = Q(0)
            for count, value in enumerate(psi):
                centered = count - time * p0
                krawtchouk_two = (
                    centered**2
                    - (1 - 2 * p0) * centered
                    - time * p0 * (1 - p0)
                )
                weight = binomial_weight(time, count, p0)
                score_covariance += weight * value * krawtchouk_two
                score_mean += weight * krawtchouk_two
            assert score_mean == 0
            assert score_covariance == (
                time
                * (time - 1)
                * p0**2
                * (1 - p0) ** 2
                * weighted_second
            )

            negatives = [count for count, value in enumerate(second) if value < 0]
            if negatives and not first_negative_order:
                first_negative_order = n
                first_negative_time = time
                first_negative_count = negatives[0]
            checked_pairs += 1

    return (
        checked_pairs,
        first_negative_order,
        first_negative_time,
        first_negative_count,
    )


def main() -> None:
    labelled_lump_audit()
    generalized_pencil_audit()
    checked, order, time, count = exact_screen()
    assert (order, time, count) == (5, 21, 19)
    print("PASS: 3N-1 quotient agrees with every labelled row for 3<=n<=5")
    print("PASS: exact first differences have one -to+ sign change")
    print("PASS: exact curvatures have one +to- sign change")
    print("PASS: exact Phi'(1/n)=0 and binomial covariance identity")
    print("PASS: exact positive Bernstein controls after dividing Phi' by p-1/n")
    print("PASS: exact generalized-pencil factorization for 2<=N<=7")
    print(f"EXACT FINITE SCREEN: {checked} pairs with 3<=n<=8 and 2<=t<=50")
    print("FIRST NEGATIVE CURVATURE: n=5, t=21, c=19")
    print("OPEN: prove both sign-regularity statements for arbitrary n,t")


if __name__ == "__main__":
    main()
