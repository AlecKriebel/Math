#!/usr/bin/env python3
"""Dependency-free exact primitives for the order-three LP(333) quotient.

The quotient has nine CRT rows and thirteen column parts

    {0}, C_0, ..., C_11,

where ``C_j=2^j <2^12>`` in ``F_37``.  This module reconstructs the
cyclotomic transition matrices, the 58 reversal-independent quotient
equations, the full length-333 sign sequences, and the residual sixfold
class-rotation action.  A candidate reaches disk only through
``verify_and_save_candidate``, which also checks every length-333
correlation and the bordered order-668 Hadamard matrix.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


P = 37
ROWS = 9
N = P * ROWS
CLASS_COUNT = 12
SUBGROUP_ORDER = 3
PRIMITIVE_ROOT = 2
TARGET_XOR_COUNT = N + 1
C6_DECIMATION = 226
C2_AFFINE_MULTIPLIER = 323
C2_AFFINE_TRANSLATION = 111
FALSE_CLASS_FIXED_MULTIPLIER = 260

ROOTS: tuple[tuple[int, int], ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
SIGN_PAIRS: tuple[tuple[int, int], ...] = (
    (1, 1),
    (-1, 1),
    (-1, -1),
    (1, -1),
)
PAIR_TO_EXPONENT = {
    pair: exponent for exponent, pair in enumerate(SIGN_PAIRS)
}
CANONICAL_ZERO_EXPONENTS: tuple[int, ...] = (0, 0, 0, 1, 2, 3, 1, 3, 2)

Gaussian = tuple[int, int]
Matrix = tuple[tuple[int, ...], ...]
BitTable = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class QuotientEquation:
    """One reversal-independent quotient correlation equation."""

    name: str
    row_lag: int
    column_lag: int
    matrix: Matrix


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def multiply_conjugate(left: Gaussian, right: Gaussian) -> Gaussian:
    """Return ``left*conjugate(right)`` in Gaussian integers."""

    a, b = left
    c, d = right
    return a * c + b * d, b * c - a * d


def phase_sum(exponents: Sequence[int]) -> Gaussian:
    total = (0, 0)
    for exponent in exponents:
        total = add(total, ROOTS[exponent])
    return total


def cyclotomic_classes() -> tuple[tuple[int, ...], ...]:
    """Return ``C_j=2^j <2^12>`` for ``j=0,...,11``."""

    subgroup = tuple(
        pow(PRIMITIVE_ROOT, CLASS_COUNT * exponent, P)
        for exponent in range(SUBGROUP_ORDER)
    )
    if subgroup != (1, 26, 10):
        raise AssertionError("the order-three subgroup changed")
    classes = tuple(
        tuple(
            pow(PRIMITIVE_ROOT, class_index, P) * value % P
            for value in subgroup
        )
        for class_index in range(CLASS_COUNT)
    )
    if any(len(set(part)) != SUBGROUP_ORDER for part in classes):
        raise AssertionError("an order-three class has the wrong size")
    if set().union(*(set(part) for part in classes)) != set(range(1, P)):
        raise AssertionError("order-three classes do not partition F_37^*")
    for class_index, part in enumerate(classes):
        negative = {(-value) % P for value in part}
        if negative != set(classes[(class_index + 6) % CLASS_COUNT]):
            raise AssertionError("negation must shift class indices by six")
    return classes


CLASSES = cyclotomic_classes()
PARTS: tuple[tuple[int, ...], ...] = ((0,),) + CLASSES
CLASS_OF = {
    value: class_index
    for class_index, part in enumerate(CLASSES)
    for value in part
}
PART_SIZES = (1,) + (SUBGROUP_ORDER,) * CLASS_COUNT


def transition_matrix(column_lag: int) -> Matrix:
    """Return ``#{c in P_j: c+column_lag in P_k}``."""

    if not 0 <= column_lag < P:
        raise ValueError("column lag must lie in F_37")
    return tuple(
        tuple(
            sum(
                (value + column_lag) % P in PARTS[right]
                for value in PARTS[left]
            )
            for right in range(len(PARTS))
        )
        for left in range(len(PARTS))
    )


ZERO_COLUMN_MATRIX = transition_matrix(0)
TRANSITION_MATRICES = tuple(
    transition_matrix(part[0]) for part in CLASSES
)


def quotient_equations() -> tuple[QuotientEquation, ...]:
    """Construct the 58 reversal-independent nonzero shifts."""

    equations: list[QuotientEquation] = []
    # At row lag zero, reversal pairs C_j with -C_j=C_{j+6}.
    for class_index in range(CLASS_COUNT // 2):
        equations.append(
            QuotientEquation(
                name=f"row_0_class_{class_index}",
                row_lag=0,
                column_lag=CLASSES[class_index][0],
                matrix=TRANSITION_MATRICES[class_index],
            )
        )
    # For row lags 1,...,4, reversal changes the row lag to 8,...,5,
    # so the zero column and all twelve nonzero classes remain independent.
    for row_lag in range(1, (ROWS - 1) // 2 + 1):
        equations.append(
            QuotientEquation(
                name=f"row_{row_lag}_column_0",
                row_lag=row_lag,
                column_lag=0,
                matrix=ZERO_COLUMN_MATRIX,
            )
        )
        for class_index in range(CLASS_COUNT):
            equations.append(
                QuotientEquation(
                    name=f"row_{row_lag}_class_{class_index}",
                    row_lag=row_lag,
                    column_lag=CLASSES[class_index][0],
                    matrix=TRANSITION_MATRICES[class_index],
                )
            )
    result = tuple(equations)
    if len(result) != 58:
        raise AssertionError("order-three quotient must have 58 equations")
    return result


QUOTIENT_EQUATIONS = quotient_equations()


def verify_transition_matrices() -> dict[str, int]:
    """Audit every representative, weight identity, and reversal pairing."""

    for class_index, part in enumerate(CLASSES):
        for representative in part:
            if transition_matrix(representative) != TRANSITION_MATRICES[class_index]:
                raise AssertionError("a transition matrix depends on representative")
    for matrix in (ZERO_COLUMN_MATRIX, *TRANSITION_MATRICES):
        if tuple(map(sum, matrix)) != PART_SIZES:
            raise AssertionError("a transition matrix has wrong row sums")
        if tuple(
            sum(matrix[row][column] for row in range(len(PARTS)))
            for column in range(len(PARTS))
        ) != PART_SIZES:
            raise AssertionError("a transition matrix has wrong column sums")
    for class_index in range(CLASS_COUNT):
        opposite = (class_index + 6) % CLASS_COUNT
        matrix = TRANSITION_MATRICES[class_index]
        reversed_matrix = tuple(
            tuple(
                TRANSITION_MATRICES[opposite][right][left]
                for right in range(len(PARTS))
            )
            for left in range(len(PARTS))
        )
        if matrix != reversed_matrix:
            raise AssertionError("transition matrices fail reversal")

    summed = tuple(
        tuple(
            ZERO_COLUMN_MATRIX[left][right]
            + SUBGROUP_ORDER
            * sum(matrix[left][right] for matrix in TRANSITION_MATRICES)
            for right in range(len(PARTS))
        )
        for left in range(len(PARTS))
    )
    expected = tuple(
        tuple(PART_SIZES[left] * PART_SIZES[right] for right in range(len(PARTS)))
        for left in range(len(PARTS))
    )
    if summed != expected:
        raise AssertionError("transition-matrix sum identity failed")
    return {
        "classes": len(CLASSES),
        "class_size": SUBGROUP_ORDER,
        "equations": len(QUOTIENT_EQUATIONS),
    }


def validate_quotient_exponents(
    exponents: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Validate shape, canonical zero word, and fixed class compressions."""

    normalized = tuple(tuple(row) for row in exponents)
    if len(normalized) != ROWS or any(
        len(row) != CLASS_COUNT + 1 for row in normalized
    ):
        raise ValueError("expected a 9 by 13 quotient exponent table")
    if any(
        type(exponent) is not int or not 0 <= exponent < 4
        for row in normalized
        for exponent in row
    ):
        raise ValueError("quotient entries must be exponents in {0,1,2,3}")
    if tuple(row[0] for row in normalized) != CANONICAL_ZERO_EXPONENTS:
        raise ValueError("zero column is not the canonical LP(9) core")
    for class_index in range(CLASS_COUNT):
        word = tuple(row[class_index + 1] for row in normalized)
        expected = (0, -3 if class_index % 2 == 0 else 3)
        if phase_sum(word) != expected:
            raise ValueError(
                f"class {class_index} has phase sum {phase_sum(word)}, "
                f"expected {expected}"
            )
    return normalized


def quotient_phase_table(
    exponents: Sequence[Sequence[int]],
) -> tuple[tuple[Gaussian, ...], ...]:
    normalized = validate_quotient_exponents(exponents)
    return tuple(tuple(ROOTS[value] for value in row) for row in normalized)


def expand_crt_exponents(
    exponents: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Expand a quotient to its exact 9 by 37 CRT exponent array."""

    normalized = validate_quotient_exponents(exponents)
    return tuple(
        tuple(
            normalized[row][0 if column == 0 else CLASS_OF[column] + 1]
            for column in range(P)
        )
        for row in range(ROWS)
    )


def sequence_from_crt_signs(matrix: Sequence[Sequence[int]]) -> tuple[int, ...]:
    if len(matrix) != ROWS or any(len(row) != P for row in matrix):
        raise ValueError("expected a 9 by 37 CRT sign matrix")
    result = [0] * N
    for row in range(ROWS):
        for column in range(P):
            index = column + P * ((row - column) % ROWS)
            result[index] = matrix[row][column]
    if any(value not in (-1, 1) for value in result):
        raise ValueError("CRT matrix must contain only signs")
    return tuple(result)


def expand_sign_sequences(
    exponents: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    expanded = expand_crt_exponents(exponents)
    a_matrix = tuple(
        tuple(SIGN_PAIRS[value][0] for value in row) for row in expanded
    )
    b_matrix = tuple(
        tuple(SIGN_PAIRS[value][1] for value in row) for row in expanded
    )
    return sequence_from_crt_signs(a_matrix), sequence_from_crt_signs(b_matrix)


def quotient_correlation_real(
    exponents: Sequence[Sequence[int]], equation: QuotientEquation
) -> int:
    phases = quotient_phase_table(exponents)
    return sum(
        equation.matrix[left][right]
        * multiply_conjugate(
            phases[row][left],
            phases[(row + equation.row_lag) % ROWS][right],
        )[0]
        for row in range(ROWS)
        for left in range(len(PARTS))
        for right in range(len(PARTS))
    )


def weighted_xor_count(
    exponents: Sequence[Sequence[int]], equation: QuotientEquation
) -> int:
    normalized = validate_quotient_exponents(exponents)
    pairs = tuple(
        tuple(SIGN_PAIRS[value] for value in row) for row in normalized
    )
    return sum(
        equation.matrix[left][right]
        * (
            (
                pairs[row][left][0]
                != pairs[(row + equation.row_lag) % ROWS][right][0]
            )
            + (
                pairs[row][left][1]
                != pairs[(row + equation.row_lag) % ROWS][right][1]
            )
        )
        for row in range(ROWS)
        for left in range(len(PARTS))
        for right in range(len(PARTS))
    )


def direct_crt_correlation_real(
    exponents: Sequence[Sequence[int]], row_lag: int, column_lag: int
) -> int:
    expanded = expand_crt_exponents(exponents)
    return sum(
        multiply_conjugate(
            ROOTS[expanded[row][column]],
            ROOTS[
                expanded[(row + row_lag) % ROWS][(column + column_lag) % P]
            ],
        )[0]
        for row in range(ROWS)
        for column in range(P)
    )


def quotient_replay(
    exponents: Sequence[Sequence[int]],
) -> tuple[tuple[str, int], ...]:
    """Cross-check all 58 transition, XOR, and direct CRT evaluations."""

    normalized = validate_quotient_exponents(exponents)
    result: list[tuple[str, int]] = []
    for equation in QUOTIENT_EQUATIONS:
        correlation = quotient_correlation_real(normalized, equation)
        direct = direct_crt_correlation_real(
            normalized, equation.row_lag, equation.column_lag
        )
        distance = weighted_xor_count(normalized, equation)
        if correlation != direct or distance != N - correlation:
            raise AssertionError(f"quotient replay disagrees for {equation.name}")
        result.append((equation.name, distance))
    return tuple(result)


def rotate_class_pairs(
    exponents: Sequence[Sequence[int]], shift: int
) -> tuple[tuple[int, ...], ...]:
    """Apply one of the six quotient actions induced by column decimation."""

    normalized = validate_quotient_exponents(exponents)
    shift %= CLASS_COUNT // 2
    return tuple(
        (row[0],)
        + tuple(
            row[1 + (class_index + 2 * shift) % CLASS_COUNT]
            for class_index in range(CLASS_COUNT)
        )
        for row in normalized
    )


def reflect_b_with_opposite_classes(
    exponents: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Apply the surviving B-only involution.

    The correct order-three action is

        A'(r,C_j) = A(r,C_j),
        B'(r,C_j) = B(3-r,C_{j+6}).

    The extra class shift is essential.  Omitting it gives the false affine
    multiplier 260, which does not preserve a general order-three B PAF.
    """

    normalized = validate_quotient_exponents(exponents)
    result: list[tuple[int, ...]] = []
    for row in range(ROWS):
        entries: list[int] = []
        for column in range(CLASS_COUNT + 1):
            a_sign = SIGN_PAIRS[normalized[row][column]][0]
            if column == 0:
                source_column = 0
            else:
                source_column = 1 + ((column - 1 + 6) % CLASS_COUNT)
            b_sign = SIGN_PAIRS[
                normalized[(3 - row) % ROWS][source_column]
            ][1]
            entries.append(PAIR_TO_EXPONENT[(a_sign, b_sign)])
        result.append(tuple(entries))
    reflected = tuple(result)
    validate_quotient_exponents(reflected)
    return reflected


def _fixture() -> tuple[tuple[int, ...], ...]:
    """Return a non-C6-fixed valid quotient used only for symmetry audits."""

    negative = (1, 1, 1, 3, 3, 3, 3, 3, 3)
    positive = (1, 1, 1, 1, 1, 1, 3, 3, 3)
    class_words = tuple(
        tuple(
            (negative if class_index % 2 == 0 else positive)[
                (row - class_index // 2) % ROWS
            ]
            for row in range(ROWS)
        )
        for class_index in range(CLASS_COUNT)
    )
    return tuple(
        (CANONICAL_ZERO_EXPONENTS[row],)
        + tuple(class_words[class_index][row] for class_index in range(CLASS_COUNT))
        for row in range(ROWS)
    )


def verify_c6_action() -> dict[str, int]:
    """Audit the physical decimation and the six-element quotient action."""

    if (
        C6_DECIMATION % ROWS != 1
        or C6_DECIMATION % P != 4
        or pow(C6_DECIMATION, 6, N) != 100
    ):
        raise AssertionError("the residual decimation arithmetic changed")
    fixture = _fixture()
    images = tuple(rotate_class_pairs(fixture, shift) for shift in range(6))
    if len(set(images)) != 6 or rotate_class_pairs(fixture, 6) != fixture:
        raise AssertionError("fixture does not realize a free C6 orbit")

    original = expand_crt_exponents(fixture)
    for shift, image in enumerate(images):
        expanded = expand_crt_exponents(image)
        multiplier = pow(C6_DECIMATION, shift, N)
        for index in range(N):
            row, column = index % ROWS, index % P
            source = multiplier * index % N
            if expanded[row][column] != original[source % ROWS][source % P]:
                raise AssertionError("quotient rotation disagrees with decimation")

        # Decimation permutes the complete physical correlation table.
        source_correlations = tuple(
            direct_crt_correlation_real(
                fixture,
                (multiplier * row_lag) % ROWS,
                (multiplier * column_lag) % P,
            )
            for row_lag in range(ROWS)
            for column_lag in range(P)
        )
        image_correlations = tuple(
            direct_crt_correlation_real(image, row_lag, column_lag)
            for row_lag in range(ROWS)
            for column_lag in range(P)
        )
        if image_correlations != source_correlations:
            raise AssertionError("C6 does not permute physical correlations")
    return {
        "decimation": C6_DECIMATION,
        "action_order": len(images),
        "class_step": 2,
    }


def _periodic_paf(sequence: Sequence[int], lag: int) -> int:
    return sum(
        sequence[index] * sequence[(index + lag) % N] for index in range(N)
    )


def multiplier_paf_mismatch_count(
    sequence: Sequence[int], multiplier: int
) -> int:
    """Count lags whose PAF changes under multiplication by ``multiplier``."""

    if len(sequence) != N or any(value not in (-1, 1) for value in sequence):
        raise ValueError("expected a length-333 sign sequence")
    return sum(
        _periodic_paf(sequence, lag)
        != _periodic_paf(sequence, multiplier * lag % N)
        for lag in range(N)
    )


def verify_c2_action() -> dict[str, int]:
    """Audit the corrected B reflection and its commutation with C6."""

    if (
        C2_AFFINE_MULTIPLIER % ROWS != -1 % ROWS
        or C2_AFFINE_MULTIPLIER % P != 27
        or C2_AFFINE_TRANSLATION % ROWS != 3
        or C2_AFFINE_TRANSLATION % P != 0
        or C2_AFFINE_MULTIPLIER != (-10) % N
    ):
        raise AssertionError("the corrected C2 affine arithmetic changed")
    fixture = _fixture()
    reflected = reflect_b_with_opposite_classes(fixture)
    if reflect_b_with_opposite_classes(reflected) != fixture:
        raise AssertionError("corrected B reflection is not involutive")
    for shift in range(6):
        if reflect_b_with_opposite_classes(
            rotate_class_pairs(fixture, shift)
        ) != rotate_class_pairs(reflected, shift):
            raise AssertionError("corrected C2 does not commute with C6")

    original_a, original_b = expand_sign_sequences(fixture)
    reflected_a, reflected_b = expand_sign_sequences(reflected)
    if reflected_a != original_a:
        raise AssertionError("B-only reflection changed A")
    physical_b = tuple(
        original_b[
            (
                C2_AFFINE_MULTIPLIER * index
                + C2_AFFINE_TRANSLATION
            )
            % N
        ]
        for index in range(N)
    )
    if reflected_b != physical_b:
        raise AssertionError("quotient C2 disagrees with physical affine map")
    if multiplier_paf_mismatch_count(
        original_b, C2_AFFINE_MULTIPLIER
    ) != 0:
        raise AssertionError("corrected C2 changed the B autocorrelation")
    false_mismatches = multiplier_paf_mismatch_count(
        original_b, FALSE_CLASS_FIXED_MULTIPLIER
    )
    if false_mismatches == 0:
        raise AssertionError("fixture failed to reject the false multiplier 260")
    return {
        "multiplier": C2_AFFINE_MULTIPLIER,
        "translation": C2_AFFINE_TRANSLATION,
        "class_step": 6,
        "false_multiplier": FALSE_CLASS_FIXED_MULTIPLIER,
        "false_multiplier_mismatches": false_mismatches,
    }


def full_periodic_correlation_replay(
    a: Sequence[int], b: Sequence[int]
) -> tuple[int, ...]:
    if len(a) != N or len(b) != N:
        raise ValueError("candidate sequences must both have length 333")
    correlations = tuple(
        sum(
            a[index] * a[(index + lag) % N]
            + b[index] * b[(index + lag) % N]
            for index in range(N)
        )
        for lag in range(N)
    )
    if correlations[0] != 2 * N or any(
        value != -2 for value in correlations[1:]
    ):
        raise ValueError("expanded assignment is not an LP(333)")
    return correlations


def verify_and_save_candidate(
    path: Path, exponents: Sequence[Sequence[int]]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Apply every LP(333) and H(668) gate before writing a candidate."""

    normalized = validate_quotient_exponents(exponents)
    replay = quotient_replay(normalized)
    if any(distance != TARGET_XOR_COUNT for _, distance in replay):
        raise ValueError("quotient assignment fails an exact lag equation")
    a, b = expand_sign_sequences(normalized)

    # Imports stay local so every structural verifier above remains
    # dependency-free and quick to invoke.
    from construction import two_circulant_legendre, verify_hadamard
    from legendre_333 import save_verified_candidate, verify_legendre_pair

    report = verify_legendre_pair(a, b)
    if not report.valid:
        raise ValueError("expanded assignment failed the LP(333) verifier")
    full_periodic_correlation_replay(a, b)
    verify_hadamard(two_circulant_legendre(a, b))
    save_verified_candidate(path, a, b)
    return a, b


def main() -> int:
    print(f"transition_audit={verify_transition_matrices()}")
    print(f"c6_audit={verify_c6_action()}")
    print(f"c2_audit={verify_c2_action()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
