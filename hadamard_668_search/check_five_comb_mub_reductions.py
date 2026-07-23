#!/usr/bin/env python3
"""Exact algebraic reductions for five-comb carrier packing.

The checker studies two finite group-labeling constructions:

* the original octet geometry, expressed as ordered orthogonal pairs from
  the two projective H4 bases; and
* four-copy polarized complementary quartets, using either one projective
  sign column per slot or an affine Pauli signed-permutation action.

Only the 14 uncovered coefficients are treated as variables.  Their exact
modulo-four image has rank six, so consistency is decided by compact integer
bit signatures.  No arbitrary carrier or sequence signs are searched.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations_with_replacement, permutations, product


LONG = 84
SHORT = 83
LENGTHS = (LONG, LONG, SHORT, SHORT)
SHIFTS = (0, 1, 2, 3, 20, 21, 22, 23)
HOLES = (
    (40, 41, 82, 83),
    (40, 41, 82, 83),
    (40, 41, 82),
    (40, 41, 82),
)
HOLE_POSITIONS = tuple(
    (row, position)
    for row, positions in enumerate(HOLES)
    for position in positions
)

H4 = (
    (1, 1, 1, 1),
    (1, -1, 1, -1),
    (1, 1, -1, -1),
    (1, -1, -1, 1),
)
MUB_TWIST = (1, 1, 1, -1)


def parity(value: int) -> int:
    return value.bit_count() & 1


def position_incidence(row: int, position: int) -> int:
    """Return the 83-bit mod-4 effect of toggling one sequence entry."""

    length = LENGTHS[row]
    return sum(
        (
            ((position + lag < length) ^ (position >= lag))
            << (lag - 1)
        )
        for lag in range(1, 84)
    )


def xor_basis(vectors: tuple[int, ...]) -> dict[int, int]:
    basis: dict[int, int] = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in basis:
                vector ^= basis[pivot]
            else:
                basis[pivot] = vector
                break
    return basis


HOLE_BASIS = xor_basis(
    tuple(position_incidence(*position) for position in HOLE_POSITIONS)
)


def quotient(vector: int) -> int:
    for pivot in sorted(HOLE_BASIS, reverse=True):
        if (vector >> pivot) & 1:
            vector ^= HOLE_BASIS[pivot]
    return vector


POSITION_QUOTIENTS = {
    (row, position): quotient(position_incidence(row, position))
    for row, length in enumerate(LENGTHS)
    for position in range(length)
}
TARGET = quotient((1 << 83) - 1)


def general_linear_3() -> tuple[tuple[int, int, int], ...]:
    result = tuple(
        (first, second, third)
        for first in range(1, 8)
        for second in range(1, 8)
        if second != first
        for third in range(1, 8)
        if third not in (first, second, first ^ second)
    )
    if len(result) != 168:
        raise AssertionError("GL(3,2) should have order 168")
    return result


GL3 = general_linear_3()


def apply_linear(matrix: tuple[int, int, int], value: int) -> int:
    return (
        (matrix[0] if value & 1 else 0)
        ^ (matrix[1] if value & 2 else 0)
        ^ (matrix[2] if value & 4 else 0)
    )


def projective_vectors() -> tuple[tuple[int, ...], ...]:
    result = tuple(
        tuple(
            H4[row][column] * (MUB_TWIST[row] if basis else 1)
            for row in range(4)
        )
        for basis in range(2)
        for column in range(4)
    )
    for left in range(8):
        for right in range(8):
            inner = sum(
                result[left][row] * result[right][row] for row in range(4)
            )
            if left // 4 == right // 4 and left != right and inner:
                raise AssertionError("a projective H4 basis is not orthogonal")
            if left // 4 != right // 4 and abs(inner) != 2:
                raise AssertionError("the two H4 bases are not mutually unbiased")
    return result


VECTORS = projective_vectors()


def slot_syndrome(
    shift: int,
    first: tuple[int, ...],
    second: tuple[int, ...],
) -> int:
    result = 0
    for tooth in range(5):
        for row in range(4):
            if first[row] < 0:
                result ^= POSITION_QUOTIENTS[(row, shift + 4 * tooth)]
            if second[row] < 0:
                result ^= POSITION_QUOTIENTS[(row, shift + 42 + 4 * tooth)]
    return result


def verify_octet_orthogonal_pair_reduction() -> None:
    """Count all projective orthogonal-pair mod-4 survivors exactly."""

    options: list[tuple[tuple[int, int, int, int], ...]] = []
    for slot, shift in enumerate(SHIFTS):
        original_column = slot % 4
        states = []
        for basis in range(2):
            for first_column in range(4):
                for second_column in range(4):
                    if second_column == first_column:
                        continue
                    first_label = 4 * basis + first_column
                    second_label = 4 * basis + second_column
                    states.append(
                        (
                            basis,
                            first_column,
                            second_column,
                            slot_syndrome(
                                shift,
                                VECTORS[first_label],
                                VECTORS[second_label],
                            ),
                            int(basis != 0 or first_column != original_column),
                        )
                    )
        if len(states) != 24:
            raise AssertionError("an orthogonal slot should have 24 projective states")
        options.append(tuple(states))

    left: defaultdict[int, Counter[tuple[int, int]]]
    left = defaultdict(Counter)
    for choices in product(range(24), repeat=4):
        syndrome = 0
        changed = 0
        opposite = 0
        for slot, choice in enumerate(choices):
            state = options[slot][choice]
            opposite += state[0]
            changed += state[4]
            syndrome ^= state[3]
        left[syndrome][(changed, opposite)] += 1

    distribution: Counter[tuple[int, int]] = Counter()
    for choices in product(range(24), repeat=4):
        syndrome = TARGET
        changed = 0
        opposite = 0
        for slot, choice in enumerate(choices, 4):
            state = options[slot][choice]
            opposite += state[0]
            changed += state[4]
            syndrome ^= state[3]
        for (left_changed, left_opposite), multiplicity in left.get(
            syndrome, {}
        ).items():
            distribution[
                (changed + left_changed, opposite + left_opposite)
            ] += multiplicity

    by_changed = Counter()
    for (changed, _opposite), multiplicity in distribution.items():
        by_changed[changed] += multiplicity
    if sum(distribution.values()) != 32_768:
        raise AssertionError("orthogonal-pair survivor count changed")
    if by_changed != Counter(
        {4: 320, 5: 2_048, 6: 6_784, 7: 11_776, 8: 11_840}
    ):
        raise AssertionError("minimum first-column change distribution changed")


def normalized_words() -> tuple[tuple[int, ...], ...]:
    return tuple(
        (1,) + tail for tail in product((-1, 1), repeat=4)
    )


WORDS = normalized_words()


def word_signature(word: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum(word[index] * word[index + lag] for index in range(5 - lag))
        for lag in range(1, 5)
    )


def complementary_quartets() -> tuple[tuple[int, int, int, int], ...]:
    signatures = tuple(word_signature(word) for word in WORDS)
    for size in range(1, 4):
        if any(
            all(
                sum(signatures[index][lag] for index in indices) == 0
                for lag in range(4)
            )
            for indices in combinations_with_replacement(range(16), size)
        ):
            raise AssertionError("a normalized complementary family below four exists")
    result = tuple(
        indices
        for indices in combinations_with_replacement(range(16), 4)
        if all(
            sum(signatures[index][lag] for index in indices) == 0
            for lag in range(4)
        )
    )
    if len(result) != 48:
        raise AssertionError("normalized complementary-quartet count changed")
    return result


QUARTETS = complementary_quartets()


def affine_labeling(
    labeling: tuple[int, ...],
) -> tuple[tuple[int, int, int], int] | None:
    """Recover an affine F_2^3 labeling, or return None."""

    translation = labeling[0]
    matrix = (
        labeling[1] ^ translation,
        labeling[2] ^ translation,
        labeling[4] ^ translation,
    )
    if all(
        labeling[slot] == apply_linear(matrix, slot) ^ translation
        for slot in range(8)
    ):
        return matrix, translation
    return None


def row_sign_representative(labeling: tuple[int, ...]) -> tuple[int, ...]:
    """Canonicalize the free action labeling[slot] -> labeling[slot] XOR b."""

    return min(
        tuple(label ^ translation for label in labeling)
        for translation in range(8)
    )


def projective_slot_states() -> tuple[tuple[int, ...], ...]:
    """Return each slot/label's exact image in the hole quotient."""

    return tuple(
        tuple(slot_syndrome(shift, vector, vector) for vector in VECTORS)
        for shift in SHIFTS
    )


PROJECTIVE_SLOT_STATES = projective_slot_states()


def common_type_projective_rref() -> tuple[tuple[tuple[int, ...], int], ...]:
    """Return the reduced GF(2) equations on the 24 projective-label bits.

    Variable ``3*slot + bit`` is bit ``bit`` of that slot's label.  The
    projective vectors form the character group of ``F_2^3``, so every
    slot syndrome is affine-linear in these three bits.  The returned
    equations are the exact modulo-four condition after quotienting the
    fourteen holes.
    """

    width = 24
    for slot, states in enumerate(PROJECTIVE_SLOT_STATES):
        for label in range(8):
            recovered = states[0]
            for bit in range(3):
                if (label >> bit) & 1:
                    recovered ^= states[1 << bit] ^ states[0]
            if recovered != states[label]:
                raise AssertionError(
                    f"slot {slot} syndrome is not affine in label bits"
                )

    baseline = TARGET
    for states in PROJECTIVE_SLOT_STATES:
        baseline ^= states[0]

    rows: list[int] = []
    for quotient_bit in range(83):
        coefficients = 0
        for slot, states in enumerate(PROJECTIVE_SLOT_STATES):
            for bit in range(3):
                delta = states[1 << bit] ^ states[0]
                if (delta >> quotient_bit) & 1:
                    coefficients ^= 1 << (3 * slot + bit)
        right_hand_side = (baseline >> quotient_bit) & 1
        if not coefficients:
            if right_hand_side:
                raise AssertionError("the projective quotient is inconsistent")
            continue
        rows.append(coefficients | (right_hand_side << width))

    rank = 0
    for column in range(width):
        pivot = next(
            (
                index
                for index in range(rank, len(rows))
                if (rows[index] >> column) & 1
            ),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for index in range(len(rows)):
            if index != rank and (rows[index] >> column) & 1:
                rows[index] ^= rows[rank]
        rank += 1

    reduced = tuple(
        (
            tuple(
                variable
                for variable in range(width)
                if (row >> variable) & 1
            ),
            (row >> width) & 1,
        )
        for row in rows
        if row & ((1 << width) - 1)
    )
    # Duplicate zero rows are the only rows below the rank after reduction.
    if len(reduced) != rank:
        raise AssertionError("unexpected duplicate row in projective RREF")
    return reduced


PROJECTIVE_RREF = common_type_projective_rref()


def verify_common_type_bijection_reduction() -> None:
    """Find every bijective two-MUB map surviving the hole quotient."""

    state = PROJECTIVE_SLOT_STATES
    expected_rref = (
        ((0, 15), 0),
        ((2, 14), 0),
        ((3, 15), 0),
        ((5, 15, 21, 23), 0),
        ((6, 21), 0),
        ((8, 18, 20, 21), 0),
        ((9, 18), 0),
        ((11, 15, 17, 18), 0),
        ((12, 15), 0),
    )
    if PROJECTIVE_RREF != expected_rref:
        raise AssertionError("unrestricted projective RREF changed")
    affine_hits = []
    for matrix in GL3:
        for translation in range(8):
            syndrome = TARGET
            for slot in range(8):
                syndrome ^= state[slot][
                    apply_linear(matrix, slot) ^ translation
                ]
            if syndrome == 0:
                affine_hits.append((matrix, translation))

    expected_matrices = {
        (4, 5, 2),
        (4, 7, 2),
        (6, 5, 2),
        (6, 7, 2),
    }
    if (
        len(HOLE_BASIS) != 6
        or len(affine_hits) != 32
        or {
            matrix for matrix, _translation in affine_hits
        } != expected_matrices
        or any(
            {
                translation
                for hit_matrix, translation in affine_hits
                if hit_matrix == matrix
            }
            != set(range(8))
            for matrix in expected_matrices
        )
    ):
        raise AssertionError("affine two-MUB modulo-four slice changed")

    bijective_hits = []
    for labeling in permutations(range(8)):
        syndrome = TARGET
        for slot, label in enumerate(labeling):
            syndrome ^= state[slot][label]
        if syndrome == 0:
            bijective_hits.append(labeling)

    recovered_affine = tuple(
        labeling
        for labeling in bijective_hits
        if affine_labeling(labeling) is not None
    )
    representatives = {
        row_sign_representative(labeling) for labeling in bijective_hits
    }
    orbit_sizes = Counter(
        row_sign_representative(labeling) for labeling in bijective_hits
    )
    affine_representatives = {
        row_sign_representative(labeling) for labeling in recovered_affine
    }
    base_linear_map = (4, 5, 2)
    shear_family: set[tuple[int, ...]] = set()
    affine_shear_family: set[tuple[int, ...]] = set()
    for first, second, quadratic in product(range(2), repeat=3):
        for translation in range(8):
            labels = []
            for slot in range(8):
                x0 = slot & 1
                x1 = (slot >> 1) & 1
                shear = (
                    first * x0
                    ^ second * x1
                    ^ quadratic * x0 * x1
                )
                labels.append(
                    apply_linear(base_linear_map, slot)
                    ^ (2 if shear else 0)
                    ^ translation
                )
            labeling = tuple(labels)
            shear_family.add(labeling)
            if quadratic == 0:
                affine_shear_family.add(labeling)
    if (
        len(bijective_hits) != 64
        or len(recovered_affine) != 32
        or len(representatives) != 8
        or set(orbit_sizes.values()) != {8}
        or len(affine_representatives) != 4
        or len(representatives - affine_representatives) != 4
        or set(bijective_hits) != shear_family
        or set(recovered_affine) != affine_shear_family
    ):
        raise AssertionError("bijective two-MUB modulo-four quotient changed")

    # The complete projective problem is also small after a four-plus-four
    # meet in the middle: eight choices at each of eight slots.
    left = Counter(
        state[0][a] ^ state[1][b] ^ state[2][c] ^ state[3][d]
        for a, b, c, d in product(range(8), repeat=4)
    )
    unrestricted = sum(
        left[
            TARGET
            ^ state[4][a]
            ^ state[5][b]
            ^ state[6][c]
            ^ state[7][d]
        ]
        for a, b, c, d in product(range(8), repeat=4)
    )
    if unrestricted != 32_768:
        raise AssertionError("unrestricted projective survivor count changed")


def general_linear_injections_3_to_4() -> tuple[tuple[int, int, int], ...]:
    result = tuple(
        (first, second, third)
        for first in range(1, 16)
        for second in range(1, 16)
        if second != first
        for third in range(1, 16)
        if third not in (first, second, first ^ second)
    )
    if len(result) != 2_520:
        raise AssertionError("unexpected number of F2^3 -> F2^4 injections")
    return result


INJECTIONS_3_TO_4 = general_linear_injections_3_to_4()


def pauli_column(
    quartet: tuple[int, int, int, int],
    label: int,
    tooth: int,
) -> tuple[int, ...]:
    translation = label & 3
    character = label >> 2
    return tuple(
        (-1 if parity(character & row) else 1)
        * WORDS[quartet[row ^ translation]][tooth]
        for row in range(4)
    )


def verify_pauli_affine_exclusion() -> None:
    """Exclude every affine Pauli signed-permutation quartet action mod 4."""

    survivors = 0
    for quartet in QUARTETS:
        state = []
        for shift in SHIFTS:
            labels = []
            for label in range(16):
                syndrome = 0
                for tooth in range(5):
                    vector = pauli_column(quartet, label, tooth)
                    for row, value in enumerate(vector):
                        if value < 0:
                            syndrome ^= POSITION_QUOTIENTS[
                                (row, shift + 4 * tooth)
                            ]
                            syndrome ^= POSITION_QUOTIENTS[
                                (row, shift + 42 + 4 * tooth)
                            ]
                labels.append(syndrome)
            state.append(tuple(labels))

        for matrix in INJECTIONS_3_TO_4:
            for translation in range(16):
                syndrome = TARGET
                for slot in range(8):
                    syndrome ^= state[slot][
                        apply_linear(matrix, slot) ^ translation
                    ]
                survivors += syndrome == 0
    if survivors:
        raise AssertionError("an affine Pauli quartet action survived modulo four")


def verify_fixed_h4_spectral_no_go() -> None:
    """Pin the sum-of-two-squares obstruction for a pure H4 core."""

    if any(
        left * left + right * right == 83
        for left in range(-83, 84)
        for right in range(-83, 84)
    ):
        raise AssertionError("83 unexpectedly became a sum of two squares")


def main() -> None:
    verify_fixed_h4_spectral_no_go()
    verify_octet_orthogonal_pair_reduction()
    verify_common_type_bijection_reduction()
    verify_pauli_affine_exclusion()
    print("PASS: 48 normalized complementary length-5 quartets")
    print("PASS: 14-hole modulo-4 image has rank 6 and fibers of size 256")
    print(
        "PASS: octet orthogonal-pair quotient has 32,768 survivors; "
        "at least four first-lobe columns must change"
    )
    print(
        "PASS: common-type two-MUB bijections: "
        "64/40,320 before the row-sign quotient, 8 after "
        "(4 affine and 4 quadratic-shear non-affine); "
        "32,768/8^8 without the affine restriction"
    )
    print(
        "PASS: 1,935,360 affine Pauli signed-permutation quartet actions "
        "excluded modulo 4"
    )


if __name__ == "__main__":
    main()
