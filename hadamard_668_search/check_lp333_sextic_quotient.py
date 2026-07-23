#!/usr/bin/env python3
"""Dependency-free exact checks for the sextic-cyclotomic LP(333) lane.

The checker reconstructs every finite object used by the lane:

* the order-six subgroup of ``F_37^*`` and its six cosets;
* the six exact 7 by 7 cyclotomic transition matrices;
* the 34 reversal-inequivalent quotient lag equations;
* the short length-nine row-axis catalog;
* an explicit 9 by 7 phase skeleton and its full 333-cell expansion;
* two exact obstructions to tempting smaller subfamilies.

The displayed skeleton is deliberately a non-candidate.  It satisfies the
fixed compression and both coordinate axes, but not all mixed lags.  All
correlations below use exact Gaussian-integer arithmetic.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from typing import Sequence


P = 37
ROWS = 9
N = P * ROWS
PRIMITIVE_ROOT = 2

# Fourth roots of unity as exact Gaussian pairs.
ROOTS: tuple[tuple[int, int], ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
REAL_PHASE_DIFFERENCE = (1, 0, -1, 0)

# Compact-JSON fingerprints supplied with the independently derived lane.
EXPECTED_CLASSES_HASH = (
    "2dd47bcbd01b4d59c6b44fd60d4034eb247557017cabd6983d09aa03d6aca293"
)
EXPECTED_MATRICES_HASH = (
    "995968188a4d5ad6242891808a1ca15be500d9d3cc2ec267a8db802d01257c49"
)
EXPECTED_SKELETON_HASH = (
    "e00542e3fbe8da61888553c567462386740d948a92723ef8375b7060ce6cb9b1"
)
EXPECTED_RESIDUAL_HASH = (
    "6fdcd7a7f1a659c5292e2970296e4f32288458fdaab35517dcd5cd6cb0b3b755"
)

# Columns are (0, C_0, ..., C_5), and entries are exponents of i.
SKELETON_EXPONENTS: tuple[tuple[int, ...], ...] = (
    (1, 3, 1, 2, 1, 3, 0),
    (3, 1, 3, 3, 2, 0, 2),
    (0, 2, 1, 2, 1, 3, 0),
    (0, 3, 2, 0, 0, 2, 1),
    (1, 3, 1, 0, 2, 2, 0),
    (2, 3, 0, 1, 2, 3, 1),
    (1, 3, 2, 3, 1, 0, 1),
    (3, 0, 0, 3, 0, 1, 2),
    (3, 1, 1, 3, 0, 3, 2),
)

EXPECTED_MIXED_RESIDUALS: tuple[tuple[int, ...], ...] = (
    (6, 0, 2, -4, 6, -8),
    (0, 0, -8, 6, 4, 4),
    (2, -4, -4, -8, 0, 8),
    (-8, 4, 10, 6, -10, -4),
)


def compact_json(value: object) -> str:
    """Return the exact serialization used by every pinned SHA-256 hash."""

    return json.dumps(value, separators=(",", ":"))


def compact_hash(value: object) -> str:
    return sha256(compact_json(value).encode("ascii")).hexdigest()


def require_hash(label: str, value: object, expected: str) -> None:
    actual = compact_hash(value)
    if actual != expected:
        raise AssertionError(
            f"{label} compact-JSON hash changed: {actual} != {expected}; "
            f"serialization={compact_json(value)}"
        )


def add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def multiply_conjugate(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    """Return ``left * conjugate(right)`` exactly."""

    a, b = left
    c, d = right
    return a * c + b * d, b * c - a * d


def phase_sum(exponents: Sequence[int]) -> tuple[int, int]:
    total = (0, 0)
    for exponent in exponents:
        total = add(total, ROOTS[exponent])
    return total


def real_paf_exponents(exponents: Sequence[int], lag: int) -> int:
    length = len(exponents)
    return sum(
        REAL_PHASE_DIFFERENCE[
            (exponents[index] - exponents[(index + lag) % length]) % 4
        ]
        for index in range(length)
    )


def sextic_classes() -> tuple[tuple[int, ...], ...]:
    """Return ``C_j=2^j <2^6>`` in canonical orbit order."""

    subgroup = tuple(pow(PRIMITIVE_ROOT, 6 * exponent, P) for exponent in range(6))
    if subgroup != (1, 27, 26, 36, 10, 11):
        raise AssertionError("the reconstructed order-six subgroup changed")
    classes = tuple(
        tuple((pow(PRIMITIVE_ROOT, class_index, P) * value) % P for value in subgroup)
        for class_index in range(6)
    )
    if any(len(set(part)) != 6 for part in classes):
        raise AssertionError("a sextic class does not have six elements")
    if set().union(*(set(part) for part in classes)) != set(range(1, P)):
        raise AssertionError("the sextic classes do not partition F_37^*")
    return classes


CLASSES = sextic_classes()
PARTS: tuple[tuple[int, ...], ...] = ((0,),) + CLASSES
CLASS_OF = {
    value: class_index
    for class_index, part in enumerate(CLASSES)
    for value in part
}


def transition_matrix(class_index: int) -> tuple[tuple[int, ...], ...]:
    """Return ``#{c in P_k : c+b in P_l}`` for one ``b in C_s``."""

    representative = CLASSES[class_index][0]
    return tuple(
        tuple(
            sum(
                (value + representative) % P in PARTS[right]
                for value in PARTS[left]
            )
            for right in range(7)
        )
        for left in range(7)
    )


TRANSITION_MATRICES = tuple(transition_matrix(index) for index in range(6))
ZERO_COLUMN_MATRIX: tuple[tuple[int, ...], ...] = tuple(
    tuple((1 if row == 0 else 6) if row == column else 0 for column in range(7))
    for row in range(7)
)


def verify_classes_and_matrices() -> tuple[int, int]:
    multiplier = tuple(pow(64, exponent, N) for exponent in range(6))
    if multiplier != (1, 64, 100, 73, 10, 307):
        raise AssertionError("order-six multiplier subgroup modulo 333 changed")
    if pow(64, 6, N) != 1 or any(value % ROWS != 1 for value in multiplier):
        raise AssertionError("multiplier subgroup does not fix the CRT row axis")
    if tuple(value % P for value in multiplier) != CLASSES[0]:
        raise AssertionError("multiplier subgroup does not induce H on F_37")

    require_hash("sextic classes", CLASSES, EXPECTED_CLASSES_HASH)
    require_hash(
        "sextic transition matrices",
        TRANSITION_MATRICES,
        EXPECTED_MATRICES_HASH,
    )

    sizes = (1, 6, 6, 6, 6, 6, 6)
    for class_index, matrix in enumerate(TRANSITION_MATRICES):
        if tuple(map(sum, matrix)) != sizes:
            raise AssertionError(f"M_{class_index} has wrong row sums")
        if tuple(
            sum(matrix[row][column] for row in range(7)) for column in range(7)
        ) != sizes:
            raise AssertionError(f"M_{class_index} has wrong column sums")

        # Reconstruct with every representative, not just the pinned first one.
        for representative in CLASSES[class_index]:
            rebuilt = tuple(
                tuple(
                    sum(
                        (value + representative) % P in PARTS[right]
                        for value in PARTS[left]
                    )
                    for right in range(7)
                )
                for left in range(7)
            )
            if rebuilt != matrix:
                raise AssertionError("transition counts are not class-invariant")

    # Since -1=2^18 lies in C_0, every C_s is closed under negation.  Thus
    # all six a=0 column equations survive independently.  For a=1,...,4
    # there is one zero-column equation and six nonzero-column equations.
    if pow(PRIMITIVE_ROOT, 18, P) != P - 1 or P - 1 not in CLASSES[0]:
        raise AssertionError("-1 unexpectedly left the sextic subgroup")
    pure_column_equations = len(CLASSES)
    nonzero_row_equations = 4 * (1 + len(CLASSES))
    equation_count = pure_column_equations + nonzero_row_equations
    if equation_count != 34:
        raise AssertionError("sextic quotient equation count changed")
    return equation_count, sum(sum(map(sum, matrix)) for matrix in TRANSITION_MATRICES)


@lru_cache(maxsize=1)
def enumerate_length9_catalog() -> tuple[
    int,
    int,
    int,
    tuple[tuple[tuple[int, ...], int], ...],
    int,
    int,
]:
    """Enumerate the short row-axis objects in one pass through ``4^9``."""

    z_formal_counts: Counter[tuple[int, ...]] = Counter()
    w_count = 0
    w_signatures: set[tuple[int, ...]] = set()
    formal_multisets = {
        (-1, -1, -1, -1),
        (-7, -1, -1, 5),
        (-7, -7, 5, 5),
    }

    for word in product(range(4), repeat=9):
        total = phase_sum(word)
        if total != (1, 0) and total != (0, -3):
            continue
        signature = tuple(real_paf_exponents(word, lag) for lag in range(1, 5))
        if total == (1, 0):
            ordered = tuple(sorted(signature))
            if ordered in formal_multisets:
                z_formal_counts[ordered] += 1
        else:
            w_count += 1
            w_signatures.add(signature)

    signatures = tuple(sorted(w_signatures))
    triple_counts: Counter[tuple[int, ...]] = Counter()
    for left in signatures:
        for middle in signatures:
            for right in signatures:
                triple_counts[
                    tuple(left[i] + middle[i] + right[i] for i in range(4))
                ] += 1
    ordered_sextuples = sum(
        count
        * triple_counts.get(tuple(-coordinate for coordinate in vector), 0)
        for vector, count in triple_counts.items()
    )
    compatible_mitm_vectors = sum(
        tuple(-coordinate for coordinate in vector) in triple_counts
        for vector in triple_counts
    )

    return (
        z_formal_counts[(-1, -1, -1, -1)],
        w_count,
        len(signatures),
        tuple(sorted(z_formal_counts.items())),
        ordered_sextuples,
        compatible_mitm_vectors,
    )


def verify_row_axis_lemma() -> tuple[int, int, int, int, int]:
    # If R_a+6S_a=-1, then -9<=R_a<=9 gives R_a in {-7,-1,5}.
    allowed_r = tuple(
        value for value in range(-9, 10) if (value + 1) % 6 == 0
    )
    if allowed_r != (-7, -1, 5):
        raise AssertionError("formal zero-cell PAF values changed")

    # sum(z)=1 gives 9+2*sum_{a=1}^4 R_a=1.  Enumerating the three
    # allowed values subject only to this identity gives three multisets.
    formal_multisets = {
        tuple(sorted(values))
        for values in product(allowed_r, repeat=4)
        if sum(values) == -4
    }
    expected_formal = {
        (-1, -1, -1, -1),
        (-7, -1, -1, 5),
        (-7, -7, 5, 5),
    }
    if formal_multisets != expected_formal:
        raise AssertionError("formal row-axis multisets changed")

    (
        z_count,
        w_count,
        signature_count,
        observed_z_multisets,
        ordered_sextuples,
        mitm_vectors,
    ) = enumerate_length9_catalog()
    if observed_z_multisets != (((-1, -1, -1, -1), 972),):
        raise AssertionError(
            f"length-9 zero-cell enumeration changed: {observed_z_multisets}"
        )
    if (z_count, w_count, signature_count) != (972, 7_056, 28):
        raise AssertionError("length-9 row-axis catalog fingerprint changed")
    if (ordered_sextuples, mitm_vectors) != (1_658_700, 298):
        raise AssertionError(
            "six-column complementary signature count changed: "
            f"{ordered_sextuples}, {mitm_vectors}"
        )
    return z_count, w_count, signature_count, ordered_sextuples, mitm_vectors


def quotient_phase_table(
    exponents: Sequence[Sequence[int]],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if len(exponents) != ROWS or any(len(row) != 7 for row in exponents):
        raise ValueError("expected a 9 by 7 exponent table")
    if any(
        type(exponent) is not int or not 0 <= exponent < 4
        for row in exponents
        for exponent in row
    ):
        raise ValueError("phase exponents must lie in {0,1,2,3}")
    return tuple(tuple(ROOTS[exponent] for exponent in row) for row in exponents)


def expand_crt_array(
    exponents: Sequence[Sequence[int]],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    quotient = quotient_phase_table(exponents)
    return tuple(
        tuple(
            quotient[row][0 if column == 0 else CLASS_OF[column] + 1]
            for column in range(P)
        )
        for row in range(ROWS)
    )


def expand_length333(
    array: Sequence[Sequence[tuple[int, int]]],
) -> tuple[tuple[int, int], ...]:
    """Use the CRT bijection ``n -> (n mod 9,n mod 37)``."""

    sequence = tuple(array[index % ROWS][index % P] for index in range(N))
    if len({(index % ROWS, index % P) for index in range(N)}) != N:
        raise AssertionError("CRT coordinates are not bijective")
    return sequence


def qpsk_to_sign_pair(value: tuple[int, int]) -> tuple[int, int]:
    return {
        (1, 0): (1, 1),
        (0, 1): (-1, 1),
        (-1, 0): (-1, -1),
        (0, -1): (1, -1),
    }[value]


def crt_correlation_real(
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


def sequence_correlation_real(
    sequence: Sequence[tuple[int, int]], lag: int
) -> int:
    return sum(
        multiply_conjugate(
            sequence[index], sequence[(index + lag) % len(sequence)]
        )[0]
        for index in range(len(sequence))
    )


def quotient_correlation_real(
    quotient: Sequence[Sequence[tuple[int, int]]],
    row_lag: int,
    matrix: Sequence[Sequence[int]],
) -> int:
    return sum(
        matrix[left][right]
        * multiply_conjugate(
            quotient[row][left],
            quotient[(row + row_lag) % ROWS][right],
        )[0]
        for row in range(ROWS)
        for left in range(7)
        for right in range(7)
    )


def verify_skeleton() -> tuple[int, int, int, int, int, int]:
    require_hash("sextic skeleton", SKELETON_EXPONENTS, EXPECTED_SKELETON_HASH)
    quotient = quotient_phase_table(SKELETON_EXPONENTS)
    array = expand_crt_array(SKELETON_EXPONENTS)
    sequence = expand_length333(array)

    # Verify the seven quotient sums and all 37 physical column sums.
    for column_index in range(7):
        total = (0, 0)
        for row in range(ROWS):
            total = add(total, quotient[row][column_index])
        expected = (
            (1, 0)
            if column_index == 0
            else (0, -3 * ((-1) ** (column_index - 1)))
        )
        if total != expected:
            raise AssertionError(
                f"quotient compression failed in column {column_index}"
            )

    for column in range(P):
        total = (0, 0)
        for row in range(ROWS):
            total = add(total, array[row][column])
        character = 0 if column == 0 else (-1) ** CLASS_OF[column]
        expected = (1, 0) if column == 0 else (0, -3 * character)
        if total != expected:
            raise AssertionError(f"physical compression failed at {column}")

        sign_pairs = [qpsk_to_sign_pair(array[row][column]) for row in range(ROWS)]
        binary_sum = (
            sum(pair[0] for pair in sign_pairs),
            sum(pair[1] for pair in sign_pairs),
        )
        binary_expected = (1, 1) if column == 0 else (
            3 * character,
            -3 * character,
        )
        if binary_sum != binary_expected:
            raise AssertionError("binary fixed compression changed")

    # The quotient matrices and the direct 333-cell expansion must agree at
    # every CRT lag, including every representative within a sextic class.
    for row_lag in range(ROWS):
        direct_zero = crt_correlation_real(array, row_lag, 0)
        quotient_zero = quotient_correlation_real(
            quotient, row_lag, ZERO_COLUMN_MATRIX
        )
        if direct_zero != quotient_zero:
            raise AssertionError("zero-column quotient expansion disagrees")
        for class_index, matrix in enumerate(TRANSITION_MATRICES):
            quotient_value = quotient_correlation_real(quotient, row_lag, matrix)
            for column_lag in CLASSES[class_index]:
                direct = crt_correlation_real(array, row_lag, column_lag)
                if direct != quotient_value:
                    raise AssertionError("sextic quotient expansion disagrees")

    # Check that flattening through CRT preserves every cyclic correlation.
    for lag in range(N):
        direct = sequence_correlation_real(sequence, lag)
        crt = crt_correlation_real(array, lag % ROWS, lag % P)
        if direct != crt:
            raise AssertionError(f"length-333 CRT replay failed at lag {lag}")

    pure_column = [
        sequence_correlation_real(sequence, lag)
        for lag in range(1, N)
        if lag % ROWS == 0
    ]
    pure_row = [
        sequence_correlation_real(sequence, lag)
        for lag in range(1, N)
        if lag % P == 0
    ]
    if len(pure_column) != 36 or any(value != -1 for value in pure_column):
        raise AssertionError("not all 36 oriented pure-column lags are exact")
    if len(pure_row) != 8 or any(value != -1 for value in pure_row):
        raise AssertionError("not all eight oriented pure-row lags are exact")

    residuals = tuple(
        tuple(
            quotient_correlation_real(
                quotient, row_lag, TRANSITION_MATRICES[class_index]
            )
            + 1
            for class_index in range(6)
        )
        for row_lag in range(1, 5)
    )
    if residuals != EXPECTED_MIXED_RESIDUALS:
        raise AssertionError(f"mixed residual matrix changed: {residuals}")
    require_hash("mixed residual matrix", residuals, EXPECTED_RESIDUAL_HASH)

    quotient_bad = sum(value != 0 for row in residuals for value in row)
    quotient_energy = sum(value * value for row in residuals for value in row)
    quotient_maximum = max(abs(value) for row in residuals for value in row)
    if (quotient_bad, quotient_energy, quotient_maximum) != (20, 784, 10):
        raise AssertionError("quotient residual fingerprint changed")

    independent_residuals = tuple(
        sequence_correlation_real(sequence, lag) + 1 for lag in range(1, 167)
    )
    mixed_residuals = tuple(
        residual
        for lag, residual in enumerate(independent_residuals, start=1)
        if lag % ROWS != 0 and lag % P != 0
    )
    if len(mixed_residuals) != 144:
        raise AssertionError("wrong number of independent mixed physical lags")
    physical_bad = sum(value != 0 for value in mixed_residuals)
    physical_energy = sum(value * value for value in mixed_residuals)
    physical_maximum = max(abs(value) for value in mixed_residuals)
    if (physical_bad, physical_energy, physical_maximum) != (120, 4_704, 10):
        raise AssertionError("physical mixed-lag fingerprint changed")
    if any(
        residual != 0
        for lag, residual in enumerate(independent_residuals, start=1)
        if lag % ROWS == 0 or lag % P == 0
    ):
        raise AssertionError("an independent pure-axis residual is nonzero")

    return (
        quotient_bad,
        quotient_energy,
        quotient_maximum,
        physical_bad,
        physical_energy,
        physical_maximum,
    )


def quadratic_transition_matrices() -> tuple[
    tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]
]:
    squares = tuple(pow(PRIMITIVE_ROOT, 2 * exponent, P) for exponent in range(18))
    square_set = set(squares)
    nonsquares = tuple(value for value in range(1, P) if value not in square_set)
    parts = ((0,), squares, nonsquares)
    matrices = []
    for representative in (squares[0], nonsquares[0]):
        matrices.append(
            tuple(
                tuple(
                    sum(
                        (value + representative) % P in parts[right]
                        for value in parts[left]
                    )
                    for right in range(3)
                )
                for left in range(3)
            )
        )
    return matrices[0], matrices[1]


def verify_quadratic_residue_obstruction() -> tuple[int, int]:
    """Exclude the order-18 (quadratic/nonquadratic) quotient."""

    square_matrix, nonsquare_matrix = quadratic_transition_matrices()
    expected = (
        ((0, 1, 0), (1, 8, 9), (0, 9, 9)),
        ((0, 0, 1), (0, 9, 9), (1, 9, 8)),
    )
    if (square_matrix, nonsquare_matrix) != expected:
        raise AssertionError("quadratic transition matrices changed")

    # For one CRT row with phases z,x,y, direct expansion of these matrices
    # is respectively 17+2 Re(z conj x)+18 Re(x conj y) and the y analogue.
    for z, x, y in product(ROOTS, repeat=3):
        row = (z, x, y)
        direct_square = sum(
            square_matrix[left][right]
            * multiply_conjugate(row[left], row[right])[0]
            for left in range(3)
            for right in range(3)
        )
        direct_nonsquare = sum(
            nonsquare_matrix[left][right]
            * multiply_conjugate(row[left], row[right])[0]
            for left in range(3)
            for right in range(3)
        )
        ix = multiply_conjugate(z, x)[0]
        iy = multiply_conjugate(z, y)[0]
        cross = multiply_conjugate(x, y)[0]
        if direct_square != 17 + 2 * ix + 18 * cross:
            raise AssertionError("quadratic square-class identity failed")
        if direct_nonsquare != 17 + 2 * iy + 18 * cross:
            raise AssertionError("quadratic nonsquare-class identity failed")

    # Summing nine rows and imposing both pure-column targets -1 gives
    # I_x+9J=I_y+9J=-77.  Since I_x,I_y,J lie in [-9,9], only J=-9,-8.
    possible_j = tuple(
        j
        for j in range(-9, 10)
        if -9 <= -77 - 9 * j <= 9
    )
    if possible_j != (-9, -8):
        raise AssertionError("quadratic obstruction bound changed")

    # J=-9 forces y=-x pointwise.  The two equations require
    # I_x=I_y=4, while y=-x forces I_y=-I_x.
    if -77 - 9 * (-9) != 4:
        raise AssertionError("J=-9 endpoint value changed")

    # J=-8 forces eight y=-x relations and one y=+/- i*x relation.  The
    # compression sums sum(x)=-3i and sum(y)=+3i would require the exceptional
    # correction x+y to vanish, which never occurs in that relation.
    multiplicity_patterns = tuple(
        (negative, zero, positive)
        for negative in range(10)
        for zero in range(10 - negative)
        for positive in (9 - negative - zero,)
        if -negative + positive == -8
    )
    if multiplicity_patterns != ((8, 1, 0),):
        raise AssertionError("J=-8 real-part multiplicities changed")
    exceptional_corrections = {
        add(x, ROOTS[(ROOTS.index(x) + quarter_turn) % 4])
        for x in ROOTS
        for quarter_turn in (-1, 1)
    }
    if (0, 0) in exceptional_corrections:
        raise AssertionError("J=-8 exceptional correction unexpectedly vanished")
    if -77 - 9 * (-8) != -5:
        raise AssertionError("J=-8 endpoint value changed")
    return possible_j


def discrete_log_table() -> dict[int, int]:
    table: dict[int, int] = {}
    value = 1
    for exponent in range(P - 1):
        if value in table:
            raise AssertionError("2 is not primitive modulo 37")
        table[value] = exponent
        value = value * PRIMITIVE_ROOT % P
    if value != 1 or len(table) != P - 1:
        raise AssertionError("discrete-log table is incomplete")
    return table


def verify_shift_template_obstruction() -> tuple[int, ...]:
    """Exclude ``u(r,c)=chi(c)w(r-log_2(c) mod 9)`` for ``c != 0``."""

    logarithm = discrete_log_table()

    # For c,c+b nonzero, put d=log(c+b)-log(c) mod 9.  The signed count
    # multiplying Re PAF_w(a-d) is (-1,0,...,0), for every b.
    expected_kernel = (-1,) + (0,) * 8
    for column_lag in range(1, P):
        kernel = [0] * ROWS
        for column in range(1, P):
            shifted = (column + column_lag) % P
            if shifted == 0:
                continue
            sign = (-1) ** (
                logarithm[column] + logarithm[shifted]
            )
            displacement = (
                logarithm[shifted] - logarithm[column]
            ) % ROWS
            kernel[displacement] += sign
        if tuple(kernel) != expected_kernel:
            raise AssertionError(
                f"shift-template character kernel changed at b={column_lag}"
            )

    # Exponents e and e+9 give column lags with the same shift mod 9 and
    # opposite quadratic character.  Their endpoint contributions therefore
    # have opposite signs, while the bulk is identical.  If both correlations
    # were -1, the bulk would be -1.  At row lag zero it is instead
    # -Re PAF_w(0)=-9 for every QPSK word w.
    for exponent in range(9):
        first = pow(PRIMITIVE_ROOT, exponent, P)
        second = pow(PRIMITIVE_ROOT, exponent + 9, P)
        if logarithm[first] % ROWS != logarithm[second] % ROWS:
            raise AssertionError("paired shift-template lags lost their shift")
        if (-1) ** logarithm[first] == (-1) ** logarithm[second]:
            raise AssertionError("paired shift-template lags have equal character")
    if -ROWS == -1:
        raise AssertionError("impossible shift-template target became possible")
    return expected_kernel


def main() -> None:
    equation_count, transition_mass = verify_classes_and_matrices()
    (
        z_count,
        w_count,
        signature_count,
        ordered_sextuples,
        mitm_vectors,
    ) = verify_row_axis_lemma()
    (
        quotient_bad,
        quotient_energy,
        quotient_maximum,
        physical_bad,
        physical_energy,
        physical_maximum,
    ) = verify_skeleton()
    possible_j = verify_quadratic_residue_obstruction()
    kernel = verify_shift_template_obstruction()

    print("PASS: sextic classes and six exact 7x7 transition matrices")
    print(
        f"PASS: {equation_count} reversal-inequivalent quotient equations "
        f"(transition mass {transition_mass})"
    )
    print(
        "PASS: row-axis catalog "
        f"({z_count} LP(9) zero words; {w_count} target-sum words; "
        f"{signature_count} real signatures)"
    )
    print(
        "PASS: complementary signature assembly "
        f"({ordered_sextuples} ordered sextuples; {mitm_vectors} MITM vectors)"
    )
    print("PASS: fixed compression and all 44 oriented pure-axis correlations")
    print(
        "NON-CANDIDATE: "
        f"{quotient_bad}/24 mixed quotient cells bad; energy={quotient_energy}; "
        f"max residual={quotient_maximum}"
    )
    print(
        "NON-CANDIDATE: "
        f"{physical_bad}/144 independent mixed lags bad; "
        f"energy={physical_energy}; max residual={physical_maximum}"
    )
    print(f"PASS: order-18 quadratic quotient excluded (only J={possible_j})")
    print(f"PASS: logarithmic shift template excluded (kernel={kernel})")


if __name__ == "__main__":
    main()
