#!/usr/bin/env python3
"""Exact arithmetic checks for the quartic-cyclotomic LP(333) reduction.

This script does not search the 666 binary signs.  It verifies:

* the QPSK reformulation of a fixed-compression Legendre pair;
* that the quartic residues modulo 37 form a (37, 9, 2) difference set;
* the four exact 5 by 5 cyclotomic transition matrices;
* an explicit 9 by 5 QPSK quotient array satisfying the prescribed
  compression and every correlation equation on the two CRT coordinate
  axes.

The displayed quotient array is not a Legendre pair: the script also reports
its remaining mixed-lag defects.  All calculations use integer Gaussian
pairs, never floating point.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from itertools import product


P = 37
ROWS = 9
N = P * ROWS
PRIMITIVE_ROOT = 2

# Fourth roots of unity, represented as exact Gaussian integer pairs.
ROOTS: tuple[tuple[int, int], ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))

# Positions are (zero, C_0, C_1, C_2, C_3), where
# C_j = 2^j <2^4> in F_37^*.  This exact witness was obtained in the
# 45-phase quotient, then frozen here for dependency-free verification.
AXIS_WITNESS_EXPONENTS: tuple[tuple[int, ...], ...] = (
    (3, 3, 1, 3, 1),
    (0, 0, 2, 3, 1),
    (2, 0, 1, 3, 2),
    (2, 2, 0, 2, 0),
    (0, 0, 3, 1, 2),
    (1, 2, 0, 3, 1),
    (0, 3, 1, 2, 1),
    (1, 3, 1, 0, 3),
    (3, 2, 2, 0, 0),
)

# Retained incumbent from the bounded structured-constructor pilot.
PILOT_BEST_EXPONENTS: tuple[tuple[int, ...], ...] = (
    (3, 0, 2, 1, 3),
    (3, 3, 0, 1, 2),
    (0, 1, 2, 3, 0),
    (1, 3, 2, 3, 1),
    (0, 3, 1, 3, 1),
    (1, 0, 1, 3, 2),
    (3, 3, 1, 0, 1),
    (2, 2, 0, 2, 0),
    (1, 2, 0, 3, 1),
)

# Exact length-9 ingredients for the row-axis factorization.  All four
# COMPLEMENTARY_W_EXPONENTS sequences sum to -3i.  Negating either of them
# changes its sum to +3i without changing its autocorrelation.
PERFECT_Z_EXPONENTS = (0, 0, 0, 1, 2, 3, 1, 3, 2)
COMPLEMENTARY_W_EXPONENTS: tuple[tuple[int, ...], ...] = (
    (0, 0, 0, 2, 3, 2, 3, 3, 2),
    (0, 0, 3, 2, 3, 3, 1, 3, 2),
    (0, 0, 0, 2, 3, 2, 3, 3, 2),
    (0, 1, 3, 3, 0, 2, 3, 3, 2),
)


def add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def multiply_conjugate(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    """Return ``left * conjugate(right)`` in exact Gaussian arithmetic."""

    a, b = left
    c, d = right
    return a * c + b * d, b * c - a * d


def quartic_classes() -> tuple[frozenset[int], ...]:
    classes = tuple(
        frozenset(
            pow(PRIMITIVE_ROOT, class_index + 4 * exponent, P)
            for exponent in range(9)
        )
        for class_index in range(4)
    )
    if frozenset().union(*classes) != frozenset(range(1, P)):
        raise AssertionError("quartic classes do not partition F_37^*")
    if any(len(part) != 9 for part in classes):
        raise AssertionError("quartic class has the wrong size")
    return classes


CLASSES = quartic_classes()
PARTS: tuple[frozenset[int], ...] = (frozenset((0,)),) + CLASSES
CLASS_OF = {
    value: class_index
    for class_index, part in enumerate(CLASSES)
    for value in part
}


def legendre_symbol(value: int) -> int:
    value %= P
    if value == 0:
        return 0
    return 1 if CLASS_OF[value] % 2 == 0 else -1


def transition_matrix(class_index: int) -> tuple[tuple[int, ...], ...]:
    """Return counts ``#{c in P_k : c+b in P_l}`` for ``b in C_j``."""

    b = min(CLASSES[class_index])
    return tuple(
        tuple(
            sum(
                value in PARTS[left]
                and (value + b) % P in PARTS[right]
                for value in range(P)
            )
            for right in range(5)
        )
        for left in range(5)
    )


TRANSITION_MATRICES = tuple(transition_matrix(index) for index in range(4))


def quotient_array(
    exponents: Sequence[Sequence[int]],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Expand a 9 by 5 cyclotomic phase table to a 9 by 37 QPSK array."""

    if len(exponents) != ROWS or any(len(row) != 5 for row in exponents):
        raise ValueError("expected a 9 by 5 phase-exponent table")
    result: list[tuple[tuple[int, int], ...]] = []
    for row in exponents:
        if any(type(value) is not int or not 0 <= value < 4 for value in row):
            raise ValueError("phase exponents must lie in {0,1,2,3}")
        result.append(
            tuple(
                ROOTS[row[0 if column == 0 else CLASS_OF[column] + 1]]
                for column in range(P)
            )
        )
    return tuple(result)


def qpsk_correlation_real(
    array: Sequence[Sequence[tuple[int, int]]],
    row_lag: int,
    column_lag: int,
) -> int:
    return sum(
        multiply_conjugate(
            array[row][column],
            array[(row + row_lag) % ROWS][(column + column_lag) % P],
        )[0]
        for row in range(ROWS)
        for column in range(P)
    )


def qpsk_to_sign_pair(value: tuple[int, int]) -> tuple[int, int]:
    """Invert ``u=(A+iB)/(1+i)`` for one fourth root of unity."""

    table = {
        (1, 0): (1, 1),
        (0, 1): (-1, 1),
        (-1, 0): (-1, -1),
        (0, -1): (1, -1),
    }
    return table[value]


def phase_sum(exponents: Sequence[int]) -> tuple[int, int]:
    total = (0, 0)
    for exponent in exponents:
        total = add(total, ROOTS[exponent])
    return total


def short_autocorrelation(
    exponents: Sequence[int], lag: int
) -> tuple[int, int]:
    total = (0, 0)
    for index, exponent in enumerate(exponents):
        total = add(
            total,
            multiply_conjugate(
                ROOTS[exponent], ROOTS[exponents[(index + lag) % len(exponents)]]
            ),
        )
    return total


def verify_length9_factorization() -> tuple[int, int, int]:
    if phase_sum(PERFECT_Z_EXPONENTS) != (1, 0):
        raise AssertionError("length-9 zero-cell sequence has the wrong sum")
    if any(
        short_autocorrelation(PERFECT_Z_EXPONENTS, lag)[0] != -1
        for lag in range(1, 5)
    ):
        raise AssertionError("length-9 zero-cell sequence is not real-perfect")

    if any(phase_sum(sequence) != (0, -3) for sequence in COMPLEMENTARY_W_EXPONENTS):
        raise AssertionError("length-9 complementary sequence has the wrong sum")
    for lag in range(1, 5):
        total = (0, 0)
        for sequence in COMPLEMENTARY_W_EXPONENTS:
            total = add(total, short_autocorrelation(sequence, lag))
        if total != (0, 0):
            raise AssertionError("four length-9 sequences are not complementary")

    real_perfect_count = 0
    target_sum_count = 0
    target_signatures: set[tuple[complex, ...]] = set()
    complex_roots = (1 + 0j, 1j, -1 + 0j, -1j)
    for sequence in product(range(4), repeat=9):
        values = tuple(complex_roots[exponent] for exponent in sequence)
        total = sum(values)
        if total not in (1 + 0j, -3j):
            continue
        signature = tuple(
            sum(
                values[index] * values[(index + lag) % 9].conjugate()
                for index in range(9)
            )
            for lag in range(1, 5)
        )
        if total == 1 + 0j and all(value.real == -1 for value in signature):
            real_perfect_count += 1
        if total == -3j:
            target_sum_count += 1
            target_signatures.add(signature)
    if (real_perfect_count, target_sum_count, len(target_signatures)) != (
        972,
        7_056,
        324,
    ):
        raise AssertionError("length-9 phase enumeration fingerprint changed")
    return real_perfect_count, target_sum_count, len(target_signatures)


def verify_difference_set() -> None:
    h = CLASSES[0]
    differences = Counter((left - right) % P for left in h for right in h)
    if differences[0] != 9:
        raise AssertionError("quartic residue difference-set zero count failed")
    if any(differences[value] != 2 for value in range(1, P)):
        raise AssertionError("quartic residues are not a (37,9,2) difference set")


def verify_transition_matrices() -> None:
    expected = (
        (
            (0, 1, 0, 0, 0),
            (0, 2, 1, 2, 4),
            (0, 2, 2, 4, 1),
            (1, 2, 2, 2, 2),
            (0, 2, 4, 1, 2),
        ),
        (
            (0, 0, 1, 0, 0),
            (0, 2, 2, 4, 1),
            (0, 4, 2, 1, 2),
            (0, 1, 2, 2, 4),
            (1, 2, 2, 2, 2),
        ),
        (
            (0, 0, 0, 1, 0),
            (1, 2, 2, 2, 2),
            (0, 1, 2, 2, 4),
            (0, 2, 4, 2, 1),
            (0, 4, 1, 2, 2),
        ),
        (
            (0, 0, 0, 0, 1),
            (0, 2, 4, 1, 2),
            (1, 2, 2, 2, 2),
            (0, 4, 1, 2, 2),
            (0, 1, 2, 4, 2),
        ),
    )
    if TRANSITION_MATRICES != expected:
        raise AssertionError("quartic transition matrices changed")
    for matrix in TRANSITION_MATRICES:
        if tuple(map(sum, matrix)) != (1, 9, 9, 9, 9):
            raise AssertionError("transition-matrix row sums failed")
        if tuple(sum(matrix[row][column] for row in range(5)) for column in range(5)) != (
            1,
            9,
            9,
            9,
            9,
        ):
            raise AssertionError("transition-matrix column sums failed")


def verify_axis_witness() -> tuple[int, int]:
    array = quotient_array(AXIS_WITNESS_EXPONENTS)

    # The fixed compression in QPSK form is 1 at zero and -3i*chi(c)
    # elsewhere.
    for column in range(P):
        total = (0, 0)
        for row in range(ROWS):
            total = add(total, array[row][column])
        expected = (1, 0) if column == 0 else (0, -3 * legendre_symbol(column))
        if total != expected:
            raise AssertionError(
                f"QPSK compression failed at column {column}: {total} != {expected}"
            )

    # Check the equivalent A/B column sums independently of the QPSK sum.
    for column in range(P):
        pairs = [qpsk_to_sign_pair(array[row][column]) for row in range(ROWS)]
        sum_a = sum(pair[0] for pair in pairs)
        sum_b = sum(pair[1] for pair in pairs)
        if column == 0:
            expected_pair = (1, 1)
        else:
            character = legendre_symbol(column)
            expected_pair = (3 * character, -3 * character)
        if (sum_a, sum_b) != expected_pair:
            raise AssertionError("binary fixed compression does not match")

    # Every nonzero lag on either CRT coordinate axis is exact.
    for column_lag in range(1, P):
        value = qpsk_correlation_real(array, 0, column_lag)
        if value != -1:
            raise AssertionError(
                f"pure-column correlation {column_lag} is {value}, not -1"
            )
    for row_lag in range(1, ROWS):
        value = qpsk_correlation_real(array, row_lag, 0)
        if value != -1:
            raise AssertionError(
                f"pure-row correlation {row_lag} is {value}, not -1"
            )

    # The witness deliberately stops at the axes.  Quantify all 4*36
    # independent mixed lags rather than accidentally presenting a candidate.
    bad = 0
    energy = 0
    for row_lag in range(1, 5):
        for column_lag in range(1, P):
            residual = qpsk_correlation_real(array, row_lag, column_lag) + 1
            bad += residual != 0
            energy += residual * residual
    if (bad, energy) != (126, 13_824):
        raise AssertionError("axis-witness mixed-defect fingerprint changed")
    return bad, energy


def verify_pilot_best() -> tuple[int, int, int]:
    array = quotient_array(PILOT_BEST_EXPONENTS)
    for column in range(P):
        total = (0, 0)
        for row in range(ROWS):
            total = add(total, array[row][column])
        expected = (1, 0) if column == 0 else (0, -3 * legendre_symbol(column))
        if total != expected:
            raise AssertionError("pilot-best fixed compression failed")
    if any(
        qpsk_correlation_real(array, row_lag, 0) != -1
        for row_lag in range(1, ROWS)
    ):
        raise AssertionError("pilot best left the exact row-axis fiber")

    bad = 0
    energy = 0
    max_absolute_residual = 0
    # Pure-column lags have 18 independent representatives under sign.
    for column_lag in range(1, 19):
        residual = qpsk_correlation_real(array, 0, column_lag) + 1
        bad += residual != 0
        energy += residual * residual
        max_absolute_residual = max(max_absolute_residual, abs(residual))
    # For a nonzero row component, row lags 1..4 select one representative
    # of every sign-pair, including the four exact row-axis lags b=0.
    for row_lag in range(1, 5):
        for column_lag in range(P):
            residual = qpsk_correlation_real(array, row_lag, column_lag) + 1
            bad += residual != 0
            energy += residual * residual
            max_absolute_residual = max(max_absolute_residual, abs(residual))
    if (bad, energy, max_absolute_residual) != (126, 1_008, 6):
        raise AssertionError("pilot-best independent-lag fingerprint changed")

    representatives = tuple(min(part) for part in CLASSES)
    residual_matrix = (
        tuple(
            qpsk_correlation_real(array, 0, representatives[index]) + 1
            for index in range(2)
        ),
    ) + tuple(
        tuple(
            qpsk_correlation_real(array, row_lag, column_lag) + 1
            for column_lag in representatives
        )
        for row_lag in range(1, 5)
    )
    expected_matrix = (
        (2, -2),
        (2, 2, -2, 0),
        (2, 2, 2, 0),
        (-4, -6, -2, 0),
        (-2, 0, 2, 4),
    )
    if residual_matrix != expected_matrix:
        raise AssertionError("pilot-best quotient residual matrix changed")
    return bad, energy, max_absolute_residual


def main() -> None:
    verify_difference_set()
    verify_transition_matrices()
    z_count, w_count, signature_count = verify_length9_factorization()
    bad, energy = verify_axis_witness()
    pilot_bad, pilot_energy, pilot_max = verify_pilot_best()
    print("PASS: quartic residues mod 37 form a cyclic (37,9,2) difference set")
    print("PASS: four exact 5x5 cyclotomic transition matrices")
    print(
        "PASS: length-9 factorization "
        f"({z_count} real-perfect z; {w_count} target-sum w; "
        f"{signature_count} w signatures)"
    )
    print("PASS: fixed LP(333) compression in QPSK and binary coordinates")
    print("PASS: all 36 pure-column and 8 pure-row correlations equal -1")
    print(
        "NON-CANDIDATE: "
        f"{bad}/144 independent mixed lags remain bad; mixed energy={energy}"
    )
    print(
        "PILOT NON-CANDIDATE: "
        f"{pilot_bad}/166 independent lags bad; energy={pilot_energy}; "
        f"max residual={pilot_max}"
    )


if __name__ == "__main__":
    main()
