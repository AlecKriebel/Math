#!/usr/bin/env python3
"""Independent exact audit of the root-marked tree transform.

The program constructs the two labelled-arrow generators directly from an
undirected rational weight matrix, solves their stationary equations over
``Fraction``, and forms the rank-marked Markov-tree polynomials.  It checks
the exact logarithmic-derivative identity and preserves a small integer
counterexample to the tempting all-marking strengthening.  Nothing in this
file assumes the still-open inequality at the physical mark ``z=1``.
"""

from __future__ import annotations

from fractions import Fraction as F
from math import comb


A = F(1, 2)


def generators(weights: tuple[tuple[int, ...], ...]) -> tuple[list[list[F]], list[list[F]]]:
    """Return the Bd-arrow generator L and arrow-reversed generator C."""
    n = len(weights)
    size = (1 << n) - 1
    degree = [sum(row) for row in weights]
    assert all(value > 0 for value in degree)
    p = [[F(weights[i][j], degree[i]) for j in range(n)] for i in range(n)]
    left = [[F(0) for _ in range(size)] for _ in range(size)]
    reverse = [[F(0) for _ in range(size)] for _ in range(size)]

    def add(matrix: list[list[F]], row: int, column: int, rate: F) -> None:
        if row != column:
            matrix[row][column] += rate

    for state in range(1, size + 1):
        row = state - 1
        for target in range(n):
            if not (state >> target) & 1:
                continue
            for source in range(n):
                neutral = (state & ~(1 << target)) | (1 << source)
                selective = state | (1 << source)
                add(left, row, neutral - 1, p[source][target])
                add(left, row, selective - 1, A * p[source][target])
                add(reverse, row, neutral - 1, p[target][source])
                add(reverse, row, selective - 1, A * p[target][source])
    for matrix in (left, reverse):
        for row in range(size):
            matrix[row][row] = -sum(
                (matrix[row][column] for column in range(size) if column != row),
                F(0),
            )
            assert sum(matrix[row], F(0)) == 0
    return left, reverse


def solve(matrix: list[list[F]], right: list[F]) -> list[F]:
    """Solve a nonsingular rational system by pivoted Gauss--Jordan."""
    n = len(matrix)
    work = [matrix[i][:] + [right[i]] for i in range(n)]
    for column in range(n):
        pivot = next(row for row in range(column, n) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        value = work[column][column]
        work[column] = [entry / value for entry in work[column]]
        for row in range(n):
            if row == column or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                work[row][j] - multiplier * work[column][j]
                for j in range(n + 1)
            ]
    return [work[i][-1] for i in range(n)]


def stationary(generator: list[list[F]]) -> list[F]:
    """Solve pi Q=0, sum(pi)=1 exactly."""
    n = len(generator)
    system = [[generator[column][row] for column in range(n)] for row in range(n)]
    system[-1] = [F(1) for _ in range(n)]
    right = [F(0) for _ in range(n)]
    right[-1] = F(1)
    answer = solve(system, right)
    assert all(value > 0 for value in answer)
    assert sum(answer, F(0)) == 1
    for column in range(n):
        assert sum((answer[row] * generator[row][column] for row in range(n)), F(0)) == 0
    return answer


def rank_polynomial(stationary_law: list[F], n: int) -> list[F]:
    coefficients = [F(0) for _ in range(n + 1)]
    for state, mass in enumerate(stationary_law, 1):
        coefficients[state.bit_count()] += mass
    assert sum(coefficients, F(0)) == 1
    return coefficients


def midpoint_polynomial(n: int) -> list[F]:
    """An unnormalised root polynomial for mu(S)=2^(-|S|)."""
    return [F(0)] + [F(comb(n, rank), 2**rank) for rank in range(1, n + 1)]


def marked_mean(coefficients: list[F], mark: F = F(1)) -> F:
    denominator = sum((value * mark**rank for rank, value in enumerate(coefficients)), F(0))
    numerator = sum(
        (rank * value * mark**rank for rank, value in enumerate(coefficients)), F(0)
    )
    return numerator / denominator


def derivative_numerator(
    midpoint: list[F], left: list[F], reverse: list[F]
) -> list[F]:
    """Numerator of z d/dz log(U^2/(L C)).

    If U_k,L_i,C_j are the input coefficients, the coefficient of z^m is

        sum_{i+j+k=m} (3k-m) U_k L_i C_j.

    Multiplying any input polynomial by a positive scalar only multiplies
    the output by a positive scalar.
    """
    n = len(midpoint) - 1
    answer = [F(0) for _ in range(3 * n + 1)]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(1, n + 1):
                total = i + j + k
                answer[total] += (3 * k - total) * midpoint[k] * left[i] * reverse[j]
    return answer


def evaluate(coefficients: list[F], value: F) -> F:
    answer = F(0)
    for coefficient in reversed(coefficients):
        answer = answer * value + coefficient
    return answer


def orientation_data(weights: tuple[tuple[int, ...], ...]):
    n = len(weights)
    left_generator, reverse_generator = generators(weights)
    left = rank_polynomial(stationary(left_generator), n)
    reverse = rank_polynomial(stationary(reverse_generator), n)
    midpoint = midpoint_polynomial(n)
    numerator = derivative_numerator(midpoint, left, reverse)
    gap = 2 * marked_mean(midpoint) - marked_mean(left) - marked_mean(reverse)
    # This cross-multiplication is the exact root-polynomial identity at z=1.
    assert (gap > 0) == (evaluate(numerator, F(1)) > 0)
    return left, reverse, midpoint, numerator, gap


def main() -> None:
    path = (
        (0, 0, 1),
        (0, 0, 1),
        (1, 1, 0),
    )
    left, reverse, midpoint, numerator, gap = orientation_data(path)
    assert left == [F(0), F(273, 448), F(150, 448), F(25, 448)]
    assert reverse == [F(0), F(96, 140), F(39, 140), F(5, 140)]
    assert midpoint == [F(0), F(3, 2), F(3, 4), F(1, 8)]
    assert gap == F(243, 5320)
    # After a positive rescaling, this is exactly
    # 9 z (25 z^4+320 z^3+1449 z^2+2706 z+1548).
    assert all(value > 0 for value in numerator[4:9])

    # Ordinary real-rootedness is already false at the reversible baseline:
    # the nonzero factor of the P3 midpoint polynomial is z^2+6z+12,
    # whose discriminant is -12.
    assert midpoint[1] / midpoint[3] == 12
    assert midpoint[2] / midpoint[3] == 6
    assert 6**2 - 4 * 12 == -12

    five_star = tuple(
        tuple(1 if (i == 4) != (j == 4) else 0 for j in range(5))
        for i in range(5)
    )
    _, _, _, star_numerator, star_gap = orientation_data(five_star)
    assert star_gap == F(14979081573, 95582481995)
    assert all(value >= 0 for value in star_numerator)

    # A connected integer-weight order-five graph exactly refutes the
    # coefficientwise/all-z strengthening.  Edges, in lexicographic subset
    # order, are 01=1000, 02=1, 04=10, 13=1000, 14=10000,
    # 23=1, 24=1000, 34=1; edges 03 and 12 are absent.
    coefficient_witness = (
        (0, 1000, 1, 0, 10),
        (1000, 0, 0, 1000, 10000),
        (1, 0, 0, 1, 1000),
        (0, 1000, 1, 0, 1),
        (10, 10000, 1000, 1, 0),
    )
    _, _, _, witness_numerator, witness_gap = orientation_data(coefficient_witness)
    assert witness_numerator[4] < 0
    assert evaluate(witness_numerator, F(1, 10000)) < 0
    # Crucially, the physical-mark endpoint inequality still has the correct
    # strict sign on this witness.
    assert witness_gap > 0

    print("PASS: exact root-marked logarithmic-derivative identity")
    print("PASS: P3 physical-mark gap = 243/5320")
    print("PASS: midpoint root polynomial is not real-rooted already on P3")
    print("PASS: K1,4 transform has nonnegative monomial coefficients")
    print("PASS: exact all-z strengthening counterexample has N_4 < 0")
    print("physical-mark gap on all-z witness:", witness_gap)


if __name__ == "__main__":
    main()
