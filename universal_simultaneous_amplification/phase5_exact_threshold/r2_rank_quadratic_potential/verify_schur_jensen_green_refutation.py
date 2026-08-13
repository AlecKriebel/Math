#!/usr/bin/env python3
"""Exact true-Green refutation of the scalar Schur--Jensen closure.

The theorem-side lower bound

    kappa*C - Q >= kappa*C - Q2 + (D - C^2/V)/4

is valid pointwise.  This script proves that the Green integral of its
right-hand side can nevertheless be negative.  All arithmetic uses
``fractions.Fraction``; no stored occupation vector or numerical solver is
used.  The original endpoint residual is positive on the same graph.
"""

from __future__ import annotations

from fractions import Fraction as F


WEIGHTS = (
    (0, 1, 1, 2),
    (1, 0, 3, 2),
    (1, 3, 0, 1),
    (2, 2, 1, 0),
)

N = len(WEIGHTS)
FULL = (1 << N) - 1
TRANSIENT = tuple(range(1, FULL))
INDEX = {state: index for index, state in enumerate(TRANSIENT)}
DEGREE = tuple(sum(row) for row in WEIGHTS)
TOTAL_DEGREE = sum(DEGREE)
PI = tuple(F(value, TOTAL_DEGREE) for value in DEGREE)
P = tuple(
    tuple(F(WEIGHTS[i][j], DEGREE[i]) for j in range(N))
    for i in range(N)
)
KAPPA = F(5, 11)
COMPLETE_FIXATION = F(3, 7)

EXPECTED_ENVELOPE_INTEGRAL = F(
    -1252850194080656479947059,
    438686742569162737630780800,
)
EXPECTED_TARGET_INTEGRAL = F(
    518083999004788499,
    236310462491468830872,
)
EXPECTED_FIXATION = F(
    4529438568157799647,
    10741384658703128676,
)


def solve_linear(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    """Solve one nonsingular rational system by Gauss--Jordan elimination."""

    size = len(rhs)
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(size):
        pivot = next(
            row for row in range(column, size) if augmented[row][column]
        )
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column or not augmented[row][column]:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                left - scale * right
                for left, right in zip(augmented[row], augmented[column])
            ]
    return [row[-1] for row in augmented]


def bit(state: int, vertex: int) -> int:
    return (state >> vertex) & 1


def x_vector(state: int) -> tuple[F, ...]:
    return tuple(
        sum(P[i][j] * bit(state, j) for j in range(N))
        for i in range(N)
    )


def rates(state: int) -> tuple[tuple[int, F], ...]:
    x = x_vector(state)
    return tuple(
        (
            state ^ (1 << vertex),
            (1 - x[vertex]) / (1 + x[vertex])
            if bit(state, vertex)
            else 2 * x[vertex] / (1 + x[vertex]),
        )
        for vertex in range(N)
    )


def generator_matrix() -> tuple[list[list[F]], list[F]]:
    matrix = [[F(0) for _ in TRANSIENT] for _ in TRANSIENT]
    fixation_rates = [F(0) for _ in TRANSIENT]
    for state in TRANSIENT:
        row = INDEX[state]
        outgoing = rates(state)
        matrix[row][row] -= sum(rate for _, rate in outgoing)
        for target, rate in outgoing:
            if target in INDEX:
                matrix[row][INDEX[target]] += rate
            elif target == FULL:
                fixation_rates[row] += rate
    return matrix, fixation_rates


def scalar_data(state: int) -> tuple[F, F, F, F, F]:
    """Return M, C, D, the true gain Q, and its two-level envelope Q2."""

    x = x_vector(state)
    mass = sum(PI[i] * bit(state, i) for i in range(N))
    cut = sum(
        PI[i] * bit(state, i) * (1 - x[i]) for i in range(N)
    )
    prediction_error = sum(
        PI[i] * (bit(state, i) - x[i]) ** 2 for i in range(N)
    )

    def selection(value: F) -> F:
        return value * (1 - value) / (1 + value)

    gain = sum(PI[i] * selection(x[i]) for i in range(N))
    outside_mean = cut / (1 - mass)
    inside_mean = 1 - cut / mass
    two_level_gain = (
        (1 - mass) * selection(outside_mean)
        + mass * selection(inside_mean)
    )
    return mass, cut, prediction_error, gain, two_level_gain


def envelope(state: int) -> F:
    mass, cut, prediction_error, _, two_level_gain = scalar_data(state)
    variance = mass * (1 - mass)
    return (
        KAPPA * cut
        - two_level_gain
        + (prediction_error - cut * cut / variance) / 4
    )


def target(state: int) -> F:
    _, cut, _, gain, _ = scalar_data(state)
    return KAPPA * cut - gain


def generator(state: int, values: tuple[F, ...]) -> F:
    return sum(
        rate * (values[next_state] - values[state])
        for next_state, rate in rates(state)
    )


def main() -> None:
    assert WEIGHTS == tuple(tuple(row) for row in zip(*WEIGHTS))
    assert all(WEIGHTS[i][i] == 0 for i in range(N))
    assert PI == (F(1, 5), F(3, 10), F(1, 4), F(1, 4))
    assert all(sum(row) == 1 for row in P)
    assert all(
        PI[i] * P[i][j] == PI[j] * P[j][i]
        for i in range(N)
        for j in range(N)
    )

    matrix, fixation_rates = generator_matrix()
    source = [
        F(1, N) if state.bit_count() == 1 else F(0)
        for state in TRANSIENT
    ]
    transpose = [
        [matrix[column][row] for column in range(len(TRANSIENT))]
        for row in range(len(TRANSIENT))
    ]
    occupation = solve_linear(transpose, [-value for value in source])
    harmonic = solve_linear(matrix, [-value for value in fixation_rates])

    assert all(value > 0 for value in occupation)
    for state in TRANSIENT:
        column = INDEX[state]
        assert sum(
            occupation[row] * matrix[row][column]
            for row in range(len(TRANSIENT))
        ) == -source[column]

    # Replay the valid pointwise strong-Jensen lower bound independently.
    assert all(target(state) >= envelope(state) for state in TRANSIENT)

    envelope_integral = sum(
        occupation[INDEX[state]] * envelope(state) for state in TRANSIENT
    )
    target_integral = sum(
        occupation[INDEX[state]] * target(state) for state in TRANSIENT
    )
    fixation = sum(harmonic[INDEX[1 << vertex]] for vertex in range(N)) / N
    assert envelope_integral == EXPECTED_ENVELOPE_INTEGRAL < 0
    assert target_integral == EXPECTED_TARGET_INTEGRAL > 0
    assert fixation == EXPECTED_FIXATION < COMPLETE_FIXATION
    assert target_integral == F(7, 22) * (COMPLETE_FIXATION - fixation)

    # Equality on each K4 rank forces this profile.  Replay all three rank
    # equations before applying the same profile to the witness graph.
    radial_profile = (F(0), F(0), F(1, 132), F(1, 88), F(0))
    complete_envelope = (F(0), F(-1, 88), F(1, 660), F(3, 220), F(0))
    for rank in range(1, N):
        up_rate = F(2 * rank * (N - rank), N - 1 + rank)
        down_rate = F(rank * (N - rank), N + rank - 2)
        assert complete_envelope[rank] + up_rate * (
            radial_profile[rank + 1] - radial_profile[rank]
        ) + down_rate * (
            radial_profile[rank - 1] - radial_profile[rank]
        ) == 0

    # The complete-normalized profile fails pointwise on the witness graph.
    radial_values = tuple(
        radial_profile[state.bit_count()] for state in range(FULL + 1)
    )
    complete_residual_at_singleton_zero = (
        envelope(1) + generator(1, radial_values)
    )
    assert complete_residual_at_singleton_zero == F(-9973, 554400) < 0

    # More generally, every neutral coboundary has zero Green integral.
    assert radial_values[0] == radial_values[FULL] == 0
    assert sum(radial_values[1 << vertex] for vertex in range(N)) == 0
    assert sum(
        occupation[INDEX[state]] * generator(state, radial_values)
        for state in TRANSIENT
    ) == 0

    print("Schur--Jensen true-Green refutation: PASS")
    print("graph edges (01,02,03,12,13,23)=(1,1,2,3,2,1)")
    print(f"integrated sufficient envelope = {envelope_integral}")
    print(f"integrated original target = {target_integral}")
    print(f"fixation = {fixation} < 3/7")
    print(
        "complete-normalized Bellman residual at {0} = "
        f"{complete_residual_at_singleton_zero}"
    )


if __name__ == "__main__":
    main()
