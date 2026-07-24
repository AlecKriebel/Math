#!/usr/bin/env python3
"""Exact labelled primitive-nine jet sieve for the order-three LP(333) lane.

This module has two layers:

* dependency-free reconstruction and replay of the finite algebra and any
  labelled certificate;
* an optional CP-SAT constructor, imported only when a search is requested.

The column algebra of order-three-multiplier-invariant functions over F_3
splits exactly as

    F_3[C_37]^H = F_3 x F_(3^6) x F_(3^6).

The first factor is augmentation and is already fixed by the row-sum
catalog.  The other two factors are represented by explicit irreducible
degree-six polynomials.  Thus the 13 physical column-part equations of each
primitive-nine jet digit reduce without loss to two six-coordinate field
equations.

No bounded search result is interpreted as a proof.  A catalog row is called
a survivor only after a complete 24-word labelled certificate is replayed
with exact arithmetic.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
from typing import Sequence

from verify_lp333_order3_primitive9_jet import (
    CLASS_COUNT,
    CLASSES,
    JET_LENGTH,
    MODULUS,
    P,
    ROWS,
    SIGN_PAIRS,
    ZERO_A_PLUS,
    ZERO_B_PLUS,
    complement,
    group_ring_jet,
    jet_add,
    jet_negate,
    jet_star,
    word_jet,
)
from verify_lp333_order3_quotient import (
    CANONICAL_ZERO_EXPONENTS,
    PARTS,
    ROOTS,
)


FIELD_DEGREE = 6
FIELD_SIZE = MODULUS**FIELD_DEGREE

# Low-to-high coefficients.  Both are irreducible over F_3.
FIELD_MODULI: tuple[tuple[int, ...], ...] = (
    (1, 1, 1, 2, 0, 1, 1),
    (2, 2, 1, 0, 2, 0, 1),
)

# Low-to-high minimal polynomial of the first nonzero class sum E_0 in the
# full 13-dimensional invariant algebra.  It is x*f_0*f_1.
INVARIANT_GENERATOR_POLYNOMIAL: tuple[int, ...] = (
    0,
    2,
    1,
    2,
    1,
    1,
    0,
    1,
    2,
    2,
    1,
    2,
    1,
    1,
)

Jet = tuple[int, int, int, int, int, int]
Word = tuple[int, ...]
FieldVector = tuple[int, int, int, int, int, int]
AlgebraVector = tuple[int, ...]

LABELLED_SURVIVOR_CATALOG_INDEX = 695
ROW_SUM_CATALOG_PATH = (
    Path(__file__).resolve().parent
    / "output"
    / "lp333_order3_row_sum_catalog.csv"
)
ROW_SUM_CATALOG_SHA256 = (
    "e8631dc0ae2f65c475af1c2e13429778f666a0fa8a13c9f1153d07d7883a98ea"
)
LABELLED_SURVIVOR_AGGREGATE = (
    -1, 1, -3, -1, 2, 0, 2, 0, 1,
    1, -1, -1, 2, 0, -1, -1, -1, 1,
)
LABELLED_SURVIVOR_MASKS_A = (
    49, 296, 42, 41, 208, 208, 385, 37, 97, 208, 261, 69,
)
LABELLED_SURVIVOR_MASKS_B = (
    416, 67, 100, 168, 25, 385, 328, 296, 73, 35, 49, 112,
)


def _trim(polynomial: Sequence[int]) -> list[int]:
    result = [coefficient % MODULUS for coefficient in polynomial]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def polynomial_divmod(
    dividend: Sequence[int], divisor: Sequence[int]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    left = _trim(dividend)
    right = _trim(divisor)
    if right == [0]:
        raise ZeroDivisionError("zero polynomial")
    quotient = [0] * max(1, len(left) - len(right) + 1)
    while len(left) >= len(right) and left != [0]:
        degree = len(left) - len(right)
        factor = left[-1] * pow(right[-1], -1, MODULUS) % MODULUS
        quotient[degree] = factor
        for index, coefficient in enumerate(right):
            left[degree + index] = (
                left[degree + index] - factor * coefficient
            ) % MODULUS
        left = _trim(left)
    return tuple(_trim(quotient)), tuple(_trim(left))


def polynomial_mod(
    polynomial: Sequence[int], modulus: Sequence[int]
) -> FieldVector:
    remainder = polynomial_divmod(polynomial, modulus)[1]
    return tuple((*remainder, *((0,) * (FIELD_DEGREE - len(remainder)))))  # type: ignore[return-value]


def field_add(left: FieldVector, right: FieldVector) -> FieldVector:
    return tuple(
        (left[index] + right[index]) % MODULUS
        for index in range(FIELD_DEGREE)
    )  # type: ignore[return-value]


def field_multiply(
    left: FieldVector, right: FieldVector, modulus: Sequence[int]
) -> FieldVector:
    product_coefficients = [0] * (2 * FIELD_DEGREE - 1)
    for first, left_value in enumerate(left):
        for second, right_value in enumerate(right):
            product_coefficients[first + second] += left_value * right_value
    return polynomial_mod(product_coefficients, modulus)


def field_power(
    value: FieldVector, exponent: int, modulus: Sequence[int]
) -> FieldVector:
    if exponent < 0:
        raise ValueError("the exponent must be nonnegative")
    result: FieldVector = (1, 0, 0, 0, 0, 0)
    factor = value
    while exponent:
        if exponent & 1:
            result = field_multiply(result, factor, modulus)
        factor = field_multiply(factor, factor, modulus)
        exponent >>= 1
    return result


def _physical_basis() -> tuple[tuple[int, ...], ...]:
    result = []
    for part in PARTS:
        vector = [0] * P
        for value in part:
            vector[value] = 1
        result.append(tuple(vector))
    return tuple(result)


PHYSICAL_BASIS = _physical_basis()


def physical_convolution(
    left: Sequence[int], right: Sequence[int]
) -> tuple[int, ...]:
    if len(left) != P or len(right) != P:
        raise ValueError("physical column vectors must have length 37")
    return tuple(
        sum(left[value] * right[(target - value) % P] for value in range(P))
        % MODULUS
        for target in range(P)
    )


def algebra_coordinates(physical: Sequence[int]) -> AlgebraVector:
    if len(physical) != P:
        raise ValueError("physical vector must have length 37")
    result = tuple(physical[part[0]] % MODULUS for part in PARTS)
    for part_index, part in enumerate(PARTS):
        if any(physical[value] % MODULUS != result[part_index] for value in part):
            raise ValueError("physical vector is not H-invariant")
    return result


def algebra_multiply(
    left: Sequence[int], right: Sequence[int]
) -> AlgebraVector:
    if len(left) != len(PARTS) or len(right) != len(PARTS):
        raise ValueError("invariant-algebra vectors must have length 13")
    left_physical = tuple(
        sum(left[index] * PHYSICAL_BASIS[index][value] for index in range(13))
        % MODULUS
        for value in range(P)
    )
    right_physical = tuple(
        sum(right[index] * PHYSICAL_BASIS[index][value] for index in range(13))
        % MODULUS
        for value in range(P)
    )
    return algebra_coordinates(physical_convolution(left_physical, right_physical))


def matrix_inverse_mod3(matrix: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("matrix must be square")
    augmented = [
        [value % MODULUS for value in matrix[row]]
        + [int(row == column) for column in range(size)]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if augmented[row][column]),
            None,
        )
        if pivot is None:
            raise ValueError("matrix is singular modulo three")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        inverse = pow(augmented[column][column], -1, MODULUS)
        augmented[column] = [
            value * inverse % MODULUS for value in augmented[column]
        ]
        for row in range(size):
            if row == column or not augmented[row][column]:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                (
                    augmented[row][entry]
                    - factor * augmented[column][entry]
                )
                % MODULUS
                for entry in range(2 * size)
            ]
    return tuple(tuple(row[size:]) for row in augmented)


def matrix_vector(
    matrix: Sequence[Sequence[int]], vector: Sequence[int]
) -> tuple[int, ...]:
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(len(vector)))
        % MODULUS
        for row in range(len(matrix))
    )


@lru_cache(maxsize=1)
def invariant_field_maps() -> tuple[
    tuple[FieldVector, ...], tuple[FieldVector, ...]
]:
    """Return the two exact degree-six field images of all 13 basis parts."""

    identity: AlgebraVector = (1,) + (0,) * 12
    generator: AlgebraVector = (0, 1) + (0,) * 11
    powers = [identity]
    for _ in range(1, 13):
        powers.append(algebra_multiply(powers[-1], generator))
    power_matrix = tuple(
        tuple(powers[column][row] for column in range(13))
        for row in range(13)
    )
    inverse = matrix_inverse_mod3(power_matrix)
    basis_polynomials = tuple(
        matrix_vector(
            inverse, tuple(int(row == basis) for row in range(13))
        )
        for basis in range(13)
    )
    maps = tuple(
        tuple(polynomial_mod(polynomial, modulus) for polynomial in basis_polynomials)
        for modulus in FIELD_MODULI
    )
    return maps  # type: ignore[return-value]


def verify_invariant_algebra_split() -> dict[str, object]:
    maps = invariant_field_maps()
    identity: AlgebraVector = (1,) + (0,) * 12
    generator: AlgebraVector = (0, 1) + (0,) * 11
    powers = [identity]
    for _ in range(13):
        powers.append(algebra_multiply(powers[-1], generator))
    relation = tuple(
        sum(
            coefficient * powers[degree][coordinate]
            for degree, coefficient in enumerate(
                INVARIANT_GENERATOR_POLYNOMIAL
            )
        )
        % MODULUS
        for coordinate in range(13)
    )
    if any(relation):
        raise AssertionError("the claimed generator polynomial does not vanish")

    quotient, remainder = polynomial_divmod(
        INVARIANT_GENERATOR_POLYNOMIAL, (0, 1)
    )
    if remainder != (0,):
        raise AssertionError("the invariant minimal polynomial lost its x factor")
    quotient_after_first, remainder = polynomial_divmod(quotient, FIELD_MODULI[0])
    if remainder != (0,) or quotient_after_first != FIELD_MODULI[1]:
        raise AssertionError("the invariant minimal polynomial factorization changed")

    # The augmentation factor is the zero-class coordinate modulo three:
    # every nonzero basis class has size three.  Check that augmentation
    # together with the two field maps is a bijective 13-dimensional map.
    split_matrix = (
        tuple(int(basis == 0) for basis in range(13)),
        *tuple(
            tuple(
                maps[orbit][basis][coordinate]
                for basis in range(13)
            )
            for orbit in range(2)
            for coordinate in range(FIELD_DEGREE)
        ),
    )
    matrix_inverse_mod3(split_matrix)

    # An exhaustive finite check proves that both degree-six quotients are
    # fields: every one of their 728 nonzero elements has an inverse.
    field_elements_checked = 0
    one: FieldVector = (1, 0, 0, 0, 0, 0)
    for modulus in FIELD_MODULI:
        for coefficients in product(range(MODULUS), repeat=FIELD_DEGREE):
            value: FieldVector = coefficients  # type: ignore[assignment]
            if not any(value):
                continue
            inverse = field_power(value, FIELD_SIZE - 2, modulus)
            if field_multiply(value, inverse, modulus) != one:
                raise AssertionError("a claimed field quotient has a nonunit")
            field_elements_checked += 1

    # Exhaustively verify that both maps preserve all 13^2 basis products.
    for orbit, modulus in enumerate(FIELD_MODULI):
        for left in range(13):
            for right in range(13):
                product_coordinates = algebra_multiply(
                    tuple(int(index == left) for index in range(13)),
                    tuple(int(index == right) for index in range(13)),
                )
                product_polynomial = [0] * FIELD_DEGREE
                for basis, coefficient in enumerate(product_coordinates):
                    if not coefficient:
                        continue
                    for degree, value in enumerate(maps[orbit][basis]):
                        product_polynomial[degree] += coefficient * value
                expected = tuple(
                    value % MODULUS for value in product_polynomial
                )
                actual = field_multiply(
                    maps[orbit][left], maps[orbit][right], modulus
                )
                if actual != expected:
                    raise AssertionError("a field map is not multiplicative")

    # Negation is Frobenius^3 on each F_(3^6) factor.
    for orbit, modulus in enumerate(FIELD_MODULI):
        for class_index in range(CLASS_COUNT):
            value = maps[orbit][class_index + 1]
            frobenius_cube = value
            for _ in range(3):
                frobenius_cube = field_multiply(
                    field_multiply(frobenius_cube, frobenius_cube, modulus),
                    frobenius_cube,
                    modulus,
                )
            if frobenius_cube != maps[orbit][(class_index + 6) % 12 + 1]:
                raise AssertionError("negation is not the cubic Frobenius")
    return {
        "algebra_dimension": 13,
        "split_dimensions": (1, 6, 6),
        "field_size": FIELD_SIZE,
        "generator_polynomial": INVARIANT_GENERATOR_POLYNOMIAL,
        "field_moduli": FIELD_MODULI,
        "split_rank": 13,
        "nonzero_field_elements_checked": field_elements_checked,
        "basis_products_checked": 2 * 13 * 13,
    }


def normalized_triples() -> tuple[Word, ...]:
    return tuple(
        tuple(int(row in support) for row in range(ROWS))
        for support in combinations(range(ROWS), 3)
    )


TRIPLES = normalized_triples()


def actual_word(channel: int, class_index: int, triple_mask: int) -> Word:
    if (
        not 0 <= triple_mask < (1 << ROWS)
        or bin(triple_mask).count("1") != 3
    ):
        raise ValueError("a normalized class word must be a nine-bit triple")
    normalized = tuple((triple_mask >> row) & 1 for row in range(ROWS))
    high_weight = (
        class_index % 2 == 0 if channel == 0 else class_index % 2 == 1
    )
    return complement(normalized) if high_weight else normalized


def validate_labelled_certificate(
    aggregate: Sequence[int],
    masks_a: Sequence[int],
    masks_b: Sequence[int],
) -> dict[str, object]:
    """Replay one exact labelled primitive-nine certificate."""

    if len(aggregate) != 2 * ROWS:
        raise ValueError("aggregate row word must have 18 coordinates")
    if len(masks_a) != CLASS_COUNT or len(masks_b) != CLASS_COUNT:
        raise ValueError("each channel needs twelve labelled masks")
    class_words = tuple(
        tuple(
            actual_word(channel, class_index, masks[class_index])
            for class_index in range(CLASS_COUNT)
        )
        for channel, masks in enumerate((masks_a, masks_b))
    )
    for row in range(ROWS):
        real = aggregate[2 * row]
        imag = aggregate[2 * row + 1]
        if (real - imag) % 2 or (real + imag) % 2:
            raise ValueError("aggregate coordinates have incompatible parity")
        expected_a_plus = (12 + real - imag) // 2
        expected_b_plus = (12 + real + imag) // 2
        if sum(word[row] for word in class_words[0]) != expected_a_plus:
            raise ValueError("A row margin failed")
        if sum(word[row] for word in class_words[1]) != expected_b_plus:
            raise ValueError("B row margin failed")

    # The four reversal-independent row-direction correlations are small
    # enough to check over the integers, rather than merely modulo the
    # primitive-nine jet.  Each nonzero class word occurs in three columns.
    for lag in range(1, 5):
        zero_intersection = sum(
            zero[row] * zero[(row + lag) % ROWS]
            for zero in (ZERO_A_PLUS, ZERO_B_PLUS)
            for row in range(ROWS)
        )
        class_intersection = sum(
            word[row] * word[(row + lag) % ROWS]
            for channel in class_words
            for word in channel
            for row in range(ROWS)
        )
        if zero_intersection + 3 * class_intersection != 167:
            raise ValueError("exact zero-column-lag equation failed")

    columns = []
    for channel, zero in enumerate((ZERO_A_PLUS, ZERO_B_PLUS)):
        expanded = [zero]
        for column in range(1, P):
            class_index = next(
                index for index, part in enumerate(CLASSES) if column in part
            )
            expanded.append(class_words[channel][class_index])
        columns.append(tuple(expanded))
    products = tuple(group_ring_jet(channel_columns) for channel_columns in columns)
    residuals = tuple(
        jet_add(
            jet_add(products[0][column], products[1][column]),
            jet_negate(
                (
                    167 % MODULUS if column == 0 else 0,
                    0,
                    0,
                    0,
                    0,
                    0,
                )
            ),
        )
        for column in range(P)
    )
    if any(any(residual) for residual in residuals):
        raise ValueError("primitive-nine jet equation failed")
    return {
        "class_words": 24,
        "physical_columns": 37,
        "exact_zero_column_lags": 4,
        "jet_equations": 37 * JET_LENGTH,
        "valid": True,
    }


def pinned_catalog_aggregate(index: int) -> tuple[int, ...]:
    """Load one aggregate from the exact pinned row-sum catalog."""

    payload = ROW_SUM_CATALOG_PATH.read_bytes()
    actual_hash = sha256(payload).hexdigest()
    if actual_hash != ROW_SUM_CATALOG_SHA256:
        raise AssertionError(
            f"row-sum catalog hash changed: {actual_hash} "
            f"!= {ROW_SUM_CATALOG_SHA256}"
        )
    rows = list(csv.reader(payload.decode("ascii").splitlines()))
    if not 0 <= index < len(rows) - 1:
        raise IndexError("catalog index is out of range")
    values = tuple(int(value) for value in rows[index + 1])
    if len(values) != 2 * ROWS:
        raise AssertionError("catalog row has the wrong width")
    zero = tuple(ROOTS[value] for value in CANONICAL_ZERO_EXPONENTS)
    aggregate = []
    for row, core in enumerate(zero):
        difference = (
            values[2 * row] - core[0],
            values[2 * row + 1] - core[1],
        )
        if difference[0] % 3 or difference[1] % 3:
            raise AssertionError(
                "catalog row is not the canonical zero word plus 3t"
            )
        aggregate.extend((difference[0] // 3, difference[1] // 3))
    return tuple(aggregate)


def verify_pinned_labelled_survivor() -> dict[str, object]:
    """Bind and replay the known fully labelled six-digit survivor."""

    aggregate = pinned_catalog_aggregate(LABELLED_SURVIVOR_CATALOG_INDEX)
    if aggregate != LABELLED_SURVIVOR_AGGREGATE:
        raise AssertionError("the pinned survivor aggregate changed")
    result = validate_labelled_certificate(
        aggregate,
        LABELLED_SURVIVOR_MASKS_A,
        LABELLED_SURVIVOR_MASKS_B,
    )
    return {
        "catalog_index": LABELLED_SURVIVOR_CATALOG_INDEX,
        "catalog_sha256": ROW_SUM_CATALOG_SHA256,
        **result,
    }


@dataclass
class LabelledJetModel:
    model: object
    bits: tuple[tuple[tuple[object, ...], ...], ...]
    jet_variables: tuple[object, ...]
    field_variables: tuple[object, ...]
    product_variables: tuple[object, ...]

    def exact_counts(self) -> dict[str, int]:
        proto = self.model.proto
        return {
            "primary_bits": 2 * CLASS_COUNT * ROWS,
            "word_jet_variables": len(self.jet_variables),
            "field_variables": len(self.field_variables),
            "product_variables": len(self.product_variables),
            "total_variables": len(proto.variables),
            "total_constraints": len(proto.constraints),
        }


@dataclass
class ProfileJetModel:
    model: object
    profile_variables: tuple[tuple[object, ...], ...]
    count_variables: tuple[object, ...]
    product_variables: tuple[object, ...]

    def exact_counts(self) -> dict[str, int]:
        proto = self.model.proto
        return {
            "profile_variables": sum(
                len(channel) for channel in self.profile_variables
            ),
            "count_variables": len(self.count_variables),
            "product_variables": len(self.product_variables),
            "total_variables": len(proto.variables),
            "total_constraints": len(proto.constraints),
        }


@dataclass
class UpperLiftModel:
    model: object
    bits: tuple[tuple[tuple[object, ...], ...], ...]
    upper_jet_variables: tuple[object, ...]

    def exact_counts(self) -> dict[str, int]:
        proto = self.model.proto
        return {
            "primary_bits": 2 * CLASS_COUNT * ROWS,
            "upper_jet_variables": len(self.upper_jet_variables),
            "total_variables": len(proto.variables),
            "total_constraints": len(proto.constraints),
        }


def profile_from_actual_word(
    channel: int, class_index: int, values: Sequence[int]
) -> tuple[int, int, int]:
    if len(values) != ROWS or any(value not in (0, 1) for value in values):
        raise ValueError("an actual class word must have nine binary entries")
    high_weight = (
        class_index % 2 == 0 if channel == 0 else class_index % 2 == 1
    )
    normalized = tuple(1 - value for value in values) if high_weight else tuple(values)
    if sum(normalized) != 3:
        raise ValueError("normalization did not produce a triple")
    return tuple(
        sum(normalized[row] for row in range(residue, ROWS, 3))
        for residue in range(3)
    )  # type: ignore[return-value]


def build_upper_lift_model(
    aggregate: Sequence[int],
    profiles: Sequence[Sequence[Sequence[int]]],
) -> UpperLiftModel:
    """Lift fixed degree-0/1/2 profiles through jet digits three to five.

    In ``F_3[pi]/(pi^6)``, the upper ideal ``pi^3 R`` is square-zero.
    Therefore, after the lower profiles are fixed, the remaining three jet
    equations are linear in the within-residue placements.
    """

    try:
        from ortools.sat.python import cp_model
    except ImportError as error:  # pragma: no cover - optional search layer.
        raise RuntimeError("OR-Tools is required only to build the search model") from error
    if len(aggregate) != 2 * ROWS:
        raise ValueError("aggregate row word must have 18 coordinates")
    if len(profiles) != 2 or any(len(channel) != CLASS_COUNT for channel in profiles):
        raise ValueError("profiles must have shape 2 by 12 by 3")
    normalized_profiles = tuple(
        tuple(tuple(int(value) for value in profile) for profile in channel)
        for channel in profiles
    )
    if any(
        len(profile) != 3
        or any(not 0 <= value <= 3 for value in profile)
        or sum(profile) != 3
        for channel in normalized_profiles
        for profile in channel
    ):
        raise ValueError("every normalized profile must compose three")

    model = cp_model.CpModel()
    bits: list[list[tuple[object, ...]]] = [[], []]
    forward_upper: list[list[tuple[object, ...]]] = [[], []]
    backward_upper: list[list[tuple[object, ...]]] = [[], []]
    intersections: list[list[tuple[object, ...]]] = [[], []]
    upper_variables: list[object] = []
    lower_forward = [[None] * CLASS_COUNT for _ in range(2)]
    lower_backward = [[None] * CLASS_COUNT for _ in range(2)]

    for channel in range(2):
        for class_index in range(CLASS_COUNT):
            profile = normalized_profiles[channel][class_index]
            high_weight = (
                class_index % 2 == 0
                if channel == 0
                else class_index % 2 == 1
            )
            allowed = []
            for support in combinations(range(ROWS), 3):
                normalized = tuple(int(row in support) for row in range(ROWS))
                actual_profile = tuple(
                    sum(
                        normalized[row]
                        for row in range(residue, ROWS, 3)
                    )
                    for residue in range(3)
                )
                if actual_profile != profile:
                    continue
                word = complement(normalized) if high_weight else normalized
                forward = word_jet(word)
                backward = jet_star(forward)
                signature = tuple(
                    sum(
                        word[row] * word[(row + lag) % ROWS]
                        for row in range(ROWS)
                    )
                    for lag in range(1, 5)
                )
                allowed.append(
                    (*word, *forward[3:], *backward[3:], *signature)
                )
            if not allowed:
                raise AssertionError("a normalized profile has no lifts")

            sample_support = []
            for residue, count in enumerate(profile):
                sample_support.extend(tuple(range(residue, ROWS, 3))[:count])
            sample_normalized = tuple(
                int(row in sample_support) for row in range(ROWS)
            )
            sample_word = (
                complement(sample_normalized)
                if high_weight
                else sample_normalized
            )
            sample_forward = word_jet(sample_word)
            sample_backward = jet_star(sample_forward)
            lower_forward[channel][class_index] = sample_forward[:3]
            lower_backward[channel][class_index] = sample_backward[:3]
            for row in allowed:
                candidate_word = row[:ROWS]
                candidate_forward = word_jet(candidate_word)
                candidate_backward = jet_star(candidate_forward)
                if (
                    candidate_forward[:3] != sample_forward[:3]
                    or candidate_backward[:3] != sample_backward[:3]
                ):
                    raise AssertionError("lower jet digits are not profile-invariant")

            word_bits = tuple(
                model.new_bool_var(
                    f"upper_word_c{channel}_j{class_index}_r{row}"
                )
                for row in range(ROWS)
            )
            forward_nodes = tuple(
                model.new_int_var(
                    0,
                    2,
                    f"upperjet_c{channel}_j{class_index}_d{degree}",
                )
                for degree in range(3, JET_LENGTH)
            )
            backward_nodes = tuple(
                model.new_int_var(
                    0,
                    2,
                    f"upperstar_c{channel}_j{class_index}_d{degree}",
                )
                for degree in range(3, JET_LENGTH)
            )
            signature_nodes = tuple(
                model.new_int_var(
                    0,
                    6,
                    f"uppersignature_c{channel}_j{class_index}_a{lag}",
                )
                for lag in range(1, 5)
            )
            model.add_allowed_assignments(
                (
                    *word_bits,
                    *forward_nodes,
                    *backward_nodes,
                    *signature_nodes,
                ),
                allowed,
            )
            bits[channel].append(word_bits)
            forward_upper[channel].append(forward_nodes)
            backward_upper[channel].append(backward_nodes)
            intersections[channel].append(signature_nodes)
            upper_variables.extend(
                (*forward_nodes, *backward_nodes, *signature_nodes)
            )

    for row in range(ROWS):
        real = aggregate[2 * row]
        imag = aggregate[2 * row + 1]
        model.add(
            sum(bits[0][class_index][row] for class_index in range(CLASS_COUNT))
            == (12 + real - imag) // 2
        )
        model.add(
            sum(bits[1][class_index][row] for class_index in range(CLASS_COUNT))
            == (12 + real + imag) // 2
        )
    for lag_index in range(4):
        model.add(
            sum(
                intersections[channel][class_index][lag_index]
                for channel in range(2)
                for class_index in range(CLASS_COUNT)
            )
            == 54
        )

    maps = invariant_field_maps()
    zero_forward = (word_jet(ZERO_A_PLUS), word_jet(ZERO_B_PLUS))
    zero_backward = tuple(jet_star(value) for value in zero_forward)

    for orbit, modulus in enumerate(FIELD_MODULI):
        fixed_forward = [
            [[0] * FIELD_DEGREE for _ in range(JET_LENGTH)]
            for _ in range(2)
        ]
        fixed_backward = [
            [[0] * FIELD_DEGREE for _ in range(JET_LENGTH)]
            for _ in range(2)
        ]
        for channel in range(2):
            for degree in range(JET_LENGTH):
                fixed_forward[channel][degree][0] = zero_forward[channel][degree]
                fixed_backward[channel][degree][0] = zero_backward[channel][degree]
            for class_index in range(CLASS_COUNT):
                for degree in range(3):
                    forward_digit = lower_forward[channel][class_index][degree]
                    backward_digit = lower_backward[channel][class_index][degree]
                    for coordinate in range(FIELD_DEGREE):
                        fixed_forward[channel][degree][coordinate] += (
                            maps[orbit][class_index + 1][coordinate]
                            * forward_digit
                        )
                        fixed_backward[channel][degree][coordinate] += (
                            maps[orbit][
                                (class_index + 6) % CLASS_COUNT + 1
                            ][coordinate]
                            * backward_digit
                        )
        for channel in range(2):
            for degree in range(JET_LENGTH):
                fixed_forward[channel][degree] = [
                    value % MODULUS
                    for value in fixed_forward[channel][degree]
                ]
                fixed_backward[channel][degree] = [
                    value % MODULUS
                    for value in fixed_backward[channel][degree]
                ]

        for total_degree in range(3, JET_LENGTH):
            base_values = [[0] * FIELD_DEGREE for _ in range(2)]
            for channel in range(2):
                for left_degree in range(total_degree + 1):
                    right_degree = total_degree - left_degree
                    left = tuple(fixed_forward[channel][left_degree])
                    right = tuple(fixed_backward[channel][right_degree])
                    product_value = field_multiply(left, right, modulus)
                    for coordinate in range(FIELD_DEGREE):
                        base_values[channel][coordinate] += product_value[coordinate]

            expressions: list[object] = [
                sum(base_values[channel][coordinate] for channel in range(2))
                % MODULUS
                for coordinate in range(FIELD_DEGREE)
            ]
            for channel in range(2):
                for class_index in range(CLASS_COUNT):
                    for degree in range(3, total_degree + 1):
                        other_degree = total_degree - degree
                        if other_degree > 2:
                            continue
                        forward_basis = maps[orbit][class_index + 1]
                        forward_coefficient = field_multiply(
                            forward_basis,
                            tuple(fixed_backward[channel][other_degree]),
                            modulus,
                        )
                        backward_basis = maps[orbit][
                            (class_index + 6) % CLASS_COUNT + 1
                        ]
                        backward_coefficient = field_multiply(
                            tuple(fixed_forward[channel][other_degree]),
                            backward_basis,
                            modulus,
                        )
                        for coordinate in range(FIELD_DEGREE):
                            if forward_coefficient[coordinate]:
                                expressions[coordinate] += (
                                    forward_coefficient[coordinate]
                                    * forward_upper[channel][class_index][degree - 3]
                                )
                            if backward_coefficient[coordinate]:
                                expressions[coordinate] += (
                                    backward_coefficient[coordinate]
                                    * backward_upper[channel][class_index][degree - 3]
                                )
            for coordinate, expression in enumerate(expressions):
                quotient = model.new_int_var(
                    -1000,
                    1000,
                    f"upper_equation_o{orbit}_d{total_degree}_x"
                    f"{coordinate}_quotient",
                )
                model.add(expression == 3 * quotient)
                upper_variables.append(quotient)

    return UpperLiftModel(
        model=model,
        bits=tuple(
            tuple(tuple(word) for word in channel) for channel in bits
        ),
        upper_jet_variables=tuple(upper_variables),
    )


def build_profile_jet_model(aggregate: Sequence[int]) -> ProfileJetModel:
    """Build the exact degree-0/1/2 profile quotient of the labelled jet.

    Lucas' theorem gives

        binom(r,k) = binom(r mod 3,k)  (mod 3),  k=0,1,2.

    Hence the first three jet digits depend only on the three residue counts
    of each normalized triple, not on placement inside a residue class.
    """

    try:
        from ortools.sat.python import cp_model
    except ImportError as error:  # pragma: no cover - optional search layer.
        raise RuntimeError("OR-Tools is required only to build the search model") from error
    if len(aggregate) != 2 * ROWS:
        raise ValueError("aggregate row word must have 18 coordinates")

    profiles = tuple(
        (first, second, 3 - first - second)
        for first in range(4)
        for second in range(4)
        if 0 <= 3 - first - second <= 3
    )
    if len(profiles) != 10:
        raise AssertionError("the normalized profile catalog changed")

    model = cp_model.CpModel()
    profile_variables: list[list[object]] = [[], []]
    count_nodes: list[list[tuple[object, ...]]] = [[], []]
    forward_nodes: list[list[tuple[object, ...]]] = [[], []]
    backward_nodes: list[list[tuple[object, ...]]] = [[], []]
    all_count_variables: list[object] = []
    for channel in range(2):
        for class_index in range(CLASS_COUNT):
            high_weight = (
                class_index % 2 == 0
                if channel == 0
                else class_index % 2 == 1
            )
            rows = []
            for profile_id, profile in enumerate(profiles):
                # Only the residue counts are used here.  Constructing any
                # canonical word gives their common first two jet digits.
                support = []
                for residue, count in enumerate(profile):
                    support.extend(tuple(range(residue, ROWS, 3))[:count])
                normalized_word = tuple(
                    int(row in support) for row in range(ROWS)
                )
                word = (
                    complement(normalized_word)
                    if high_weight
                    else normalized_word
                )
                counts = (
                    tuple(3 - value for value in profile)
                    if high_weight
                    else profile
                )
                forward = word_jet(word)
                backward = jet_star(forward)
                rows.append(
                    (
                        profile_id,
                        *counts,
                        forward[1],
                        forward[2],
                        backward[1],
                        backward[2],
                    )
                )
            profile_node = model.new_int_var(
                0, 9, f"profile_c{channel}_j{class_index}"
            )
            counts = tuple(
                model.new_int_var(
                    0, 3, f"count_c{channel}_j{class_index}_a{residue}"
                )
                for residue in range(3)
            )
            forward = tuple(
                model.new_int_var(
                    0, 2, f"profilejet_c{channel}_j{class_index}_d{degree}"
                )
                for degree in (1, 2)
            )
            backward = tuple(
                model.new_int_var(
                    0, 2, f"profilestar_c{channel}_j{class_index}_d{degree}"
                )
                for degree in (1, 2)
            )
            model.add_allowed_assignments(
                (profile_node, *counts, *forward, *backward), rows
            )
            profile_variables[channel].append(profile_node)
            count_nodes[channel].append(counts)
            forward_nodes[channel].append(forward)
            backward_nodes[channel].append(backward)
            all_count_variables.extend((*counts, *forward, *backward))

    for channel in range(2):
        for residue in range(3):
            target = 0
            for row in range(residue, ROWS, 3):
                real = aggregate[2 * row]
                imag = aggregate[2 * row + 1]
                target += (
                    (12 + real - imag) // 2
                    if channel == 0
                    else (12 + real + imag) // 2
                )
            model.add(
                sum(
                    count_nodes[channel][class_index][residue]
                    for class_index in range(CLASS_COUNT)
                )
                == target
            )

    maps = invariant_field_maps()
    zero_forward = (word_jet(ZERO_A_PLUS), word_jet(ZERO_B_PLUS))
    zero_backward = tuple(jet_star(value) for value in zero_forward)
    aggregate_forward = [
        [
            [[None] * FIELD_DEGREE for _ in range(3)]
            for _ in range(2)
        ]
        for _ in range(2)
    ]
    aggregate_backward = [
        [
            [[None] * FIELD_DEGREE for _ in range(3)]
            for _ in range(2)
        ]
        for _ in range(2)
    ]

    def residue(expression: object, name: str) -> object:
        value = model.new_int_var(0, 2, name)
        quotient = model.new_int_var(-1000, 1000, f"{name}_quotient")
        model.add(expression == value + 3 * quotient)
        all_count_variables.extend((value, quotient))
        return value

    for channel in range(2):
        for orbit in range(2):
            for degree in range(3):
                for coordinate in range(FIELD_DEGREE):
                    if degree == 0:
                        aggregate_forward[channel][orbit][degree][coordinate] = (
                            zero_forward[channel][0] if coordinate == 0 else 0
                        )
                        aggregate_backward[channel][orbit][degree][coordinate] = (
                            zero_backward[channel][0] if coordinate == 0 else 0
                        )
                        continue
                    forward_expression = (
                        zero_forward[channel][degree] if coordinate == 0 else 0
                    )
                    backward_expression = (
                        zero_backward[channel][degree] if coordinate == 0 else 0
                    )
                    for class_index in range(CLASS_COUNT):
                        coefficient = maps[orbit][class_index + 1][coordinate]
                        if coefficient:
                            forward_expression += (
                                coefficient
                                * forward_nodes[channel][class_index][degree - 1]
                            )
                        opposite = maps[orbit][
                            (class_index + 6) % CLASS_COUNT + 1
                        ][coordinate]
                        if opposite:
                            backward_expression += (
                                opposite
                                * backward_nodes[channel][class_index][degree - 1]
                            )
                    aggregate_forward[channel][orbit][degree][coordinate] = residue(
                        forward_expression,
                        f"profilefield_c{channel}_o{orbit}_d{degree}_x{coordinate}",
                    )
                    aggregate_backward[channel][orbit][degree][coordinate] = residue(
                        backward_expression,
                        f"profilefieldstar_c{channel}_o{orbit}_d{degree}_x{coordinate}",
                    )

    multiplication_rows = tuple(
        (left, right, left * right % MODULUS)
        for left in range(MODULUS)
        for right in range(MODULUS)
    )
    products: dict[tuple[int, int], object] = {}

    def trit_product(left: object, right: object) -> object:
        if type(left) is int and type(right) is int:
            return left * right % MODULUS
        if type(left) is int:
            return (left % MODULUS) * right
        if type(right) is int:
            return (right % MODULUS) * left
        key = tuple(sorted((left.index, right.index)))
        result = products.get(key)
        if result is None:
            result = model.new_int_var(
                0, 2, f"profile_trit_product_{key[0]}_{key[1]}"
            )
            model.add_allowed_assignments(
                (left, right, result), multiplication_rows
            )
            products[key] = result
        return result

    for orbit, modulus in enumerate(FIELD_MODULI):
        tensors = [
            [
                field_multiply(
                    tuple(int(index == left) for index in range(FIELD_DEGREE)),
                    tuple(int(index == right) for index in range(FIELD_DEGREE)),
                    modulus,
                )
                for right in range(FIELD_DEGREE)
            ]
            for left in range(FIELD_DEGREE)
        ]
        for total_degree in range(3):
            for output_coordinate in range(FIELD_DEGREE):
                terms = []
                for channel in range(2):
                    for left_degree in range(total_degree + 1):
                        right_degree = total_degree - left_degree
                        for left_coordinate in range(FIELD_DEGREE):
                            for right_coordinate in range(FIELD_DEGREE):
                                coefficient = tensors[left_coordinate][
                                    right_coordinate
                                ][output_coordinate]
                                if not coefficient:
                                    continue
                                left = aggregate_forward[channel][orbit][
                                    left_degree
                                ][left_coordinate]
                                right = aggregate_backward[channel][orbit][
                                    right_degree
                                ][right_coordinate]
                                if (
                                    type(left) is int and left % MODULUS == 0
                                ) or (
                                    type(right) is int and right % MODULUS == 0
                                ):
                                    continue
                                terms.append(
                                    coefficient * trit_product(left, right)
                                )
                target = (
                    167 % MODULUS
                    if total_degree == 0 and output_coordinate == 0
                    else 0
                )
                if not terms:
                    if target:
                        raise AssertionError("a profile target lost its terms")
                    continue
                quotient = model.new_int_var(
                    -1000,
                    1000,
                    f"profileequation_o{orbit}_d{total_degree}_x"
                    f"{output_coordinate}_quotient",
                )
                model.add(sum(terms) == target + 3 * quotient)
                all_count_variables.append(quotient)

    return ProfileJetModel(
        model=model,
        profile_variables=tuple(
            tuple(channel) for channel in profile_variables
        ),
        count_variables=tuple(all_count_variables),
        product_variables=tuple(products.values()),
    )


def build_labelled_jet_model(
    aggregate: Sequence[int],
    *,
    max_jet_degree: int = JET_LENGTH - 1,
    include_zero_column_lags: bool = True,
) -> LabelledJetModel:
    """Build the exact two-field jet model; OR-Tools is imported lazily."""

    try:
        from ortools.sat.python import cp_model
    except ImportError as error:  # pragma: no cover - optional search layer.
        raise RuntimeError("OR-Tools is required only to build the search model") from error

    if len(aggregate) != 2 * ROWS:
        raise ValueError("aggregate row word must have 18 coordinates")
    if not 0 <= max_jet_degree < JET_LENGTH:
        raise ValueError("max_jet_degree must lie between zero and five")
    model = cp_model.CpModel()
    multiplication_rows = tuple(
        (left, right, left * right % MODULUS)
        for left in range(MODULUS)
        for right in range(MODULUS)
    )

    table_by_weight: dict[int, tuple[tuple[int, ...], ...]] = {}
    for weight in (3, 6):
        rows = []
        for normalized in TRIPLES:
            word = normalized if weight == 3 else complement(normalized)
            forward = word_jet(word)
            backward = jet_star(forward)
            intersections = tuple(
                sum(
                    word[row] * word[(row + lag) % ROWS]
                    for row in range(ROWS)
                )
                for lag in range(1, 5)
            )
            rows.append(
                tuple(word) + forward[1:] + backward[1:] + intersections
            )
        table_by_weight[weight] = tuple(rows)

    bits: list[list[tuple[object, ...]]] = [[], []]
    forward_nodes: list[list[tuple[object, ...]]] = [[], []]
    backward_nodes: list[list[tuple[object, ...]]] = [[], []]
    intersection_nodes: list[list[tuple[object, ...]]] = [[], []]
    jet_variables: list[object] = []
    for channel in range(2):
        for class_index in range(CLASS_COUNT):
            weight = (
                (6 if class_index % 2 == 0 else 3)
                if channel == 0
                else (3 if class_index % 2 == 0 else 6)
            )
            word_bits = tuple(
                model.new_bool_var(
                    f"word_c{channel}_j{class_index}_r{row}"
                )
                for row in range(ROWS)
            )
            forward = tuple(
                model.new_int_var(
                    0, 2, f"jet_c{channel}_j{class_index}_d{degree}"
                )
                for degree in range(1, JET_LENGTH)
            )
            backward = tuple(
                model.new_int_var(
                    0, 2, f"star_c{channel}_j{class_index}_d{degree}"
                )
                for degree in range(1, JET_LENGTH)
            )
            intersections = tuple(
                model.new_int_var(
                    0,
                    6,
                    f"intersection_c{channel}_j{class_index}_a{lag}",
                )
                for lag in range(1, 5)
            )
            model.add_allowed_assignments(
                (*word_bits, *forward, *backward, *intersections),
                table_by_weight[weight],
            )
            bits[channel].append(word_bits)
            forward_nodes[channel].append(forward)
            backward_nodes[channel].append(backward)
            intersection_nodes[channel].append(intersections)
            jet_variables.extend((*forward, *backward))

    for row in range(ROWS):
        real = aggregate[2 * row]
        imag = aggregate[2 * row + 1]
        if (real - imag) % 2 or (real + imag) % 2:
            raise ValueError("aggregate coordinates have incompatible parity")
        model.add(
            sum(bits[0][class_index][row] for class_index in range(CLASS_COUNT))
            == (12 + real - imag) // 2
        )
        model.add(
            sum(bits[1][class_index][row] for class_index in range(CLASS_COUNT))
            == (12 + real + imag) // 2
        )
    if include_zero_column_lags:
        # Exact zero-column-lag equations.  The canonical zero column
        # contributes five intersections, while each nonzero H-orbit is
        # repeated three times:
        #
        #   5 + 3*sum_(24 class words) intersection(a) = 167.
        for lag_index in range(4):
            model.add(
                sum(
                    intersection_nodes[channel][class_index][lag_index]
                    for channel in range(2)
                    for class_index in range(CLASS_COUNT)
                )
                == 54
            )

    maps = invariant_field_maps()
    zero_forward = (word_jet(ZERO_A_PLUS), word_jet(ZERO_B_PLUS))
    zero_backward = tuple(jet_star(value) for value in zero_forward)
    field_variables: list[object] = []

    def residue(expression: object, name: str) -> object:
        value = model.new_int_var(0, 2, name)
        quotient = model.new_int_var(-1000, 1000, f"{name}_quotient")
        model.add(expression == value + 3 * quotient)
        field_variables.extend((value, quotient))
        return value

    aggregate_forward = [
        [
            [[None] * FIELD_DEGREE for _ in range(JET_LENGTH)]
            for _ in range(2)
        ]
        for _ in range(2)
    ]
    aggregate_backward = [
        [
            [[None] * FIELD_DEGREE for _ in range(JET_LENGTH)]
            for _ in range(2)
        ]
        for _ in range(2)
    ]
    for channel in range(2):
        for orbit in range(2):
            for degree in range(max_jet_degree + 1):
                for coordinate in range(FIELD_DEGREE):
                    if degree == 0:
                        aggregate_forward[channel][orbit][degree][coordinate] = (
                            zero_forward[channel][degree] if coordinate == 0 else 0
                        )
                        aggregate_backward[channel][orbit][degree][coordinate] = (
                            zero_backward[channel][degree] if coordinate == 0 else 0
                        )
                        continue
                    forward_expression = (
                        zero_forward[channel][degree] if coordinate == 0 else 0
                    )
                    backward_expression = (
                        zero_backward[channel][degree] if coordinate == 0 else 0
                    )
                    for class_index in range(CLASS_COUNT):
                        coefficient = maps[orbit][class_index + 1][coordinate]
                        if coefficient:
                            forward_expression += (
                                coefficient
                                * forward_nodes[channel][class_index][degree - 1]
                            )
                        opposite_coefficient = maps[orbit][
                            (class_index + 6) % CLASS_COUNT + 1
                        ][coordinate]
                        if opposite_coefficient:
                            backward_expression += (
                                opposite_coefficient
                                * backward_nodes[channel][class_index][degree - 1]
                            )
                    aggregate_forward[channel][orbit][degree][coordinate] = residue(
                        forward_expression,
                        f"field_c{channel}_o{orbit}_d{degree}_x{coordinate}",
                    )
                    aggregate_backward[channel][orbit][degree][coordinate] = residue(
                        backward_expression,
                        f"fieldstar_c{channel}_o{orbit}_d{degree}_x{coordinate}",
                    )

    product_variables: dict[tuple[int, int], object] = {}

    def field_product(left: object, right: object) -> object:
        if type(left) is int and type(right) is int:
            return left * right % MODULUS
        if type(left) is int:
            return (left % MODULUS) * right
        if type(right) is int:
            return (right % MODULUS) * left
        key = tuple(sorted((left.index, right.index)))
        result = product_variables.get(key)
        if result is None:
            result = model.new_int_var(0, 2, f"trit_product_{key[0]}_{key[1]}")
            model.add_allowed_assignments(
                (left, right, result), multiplication_rows
            )
            product_variables[key] = result
        return result

    for orbit, modulus in enumerate(FIELD_MODULI):
        tensors = [
            [
                field_multiply(
                    tuple(int(index == left) for index in range(FIELD_DEGREE)),
                    tuple(int(index == right) for index in range(FIELD_DEGREE)),
                    modulus,
                )
                for right in range(FIELD_DEGREE)
            ]
            for left in range(FIELD_DEGREE)
        ]
        for total_degree in range(max_jet_degree + 1):
            for output_coordinate in range(FIELD_DEGREE):
                terms = []
                for channel in range(2):
                    for left_degree in range(total_degree + 1):
                        right_degree = total_degree - left_degree
                        for left_coordinate in range(FIELD_DEGREE):
                            for right_coordinate in range(FIELD_DEGREE):
                                coefficient = tensors[left_coordinate][
                                    right_coordinate
                                ][output_coordinate]
                                if not coefficient:
                                    continue
                                left = aggregate_forward[channel][orbit][
                                    left_degree
                                ][left_coordinate]
                                right = aggregate_backward[channel][orbit][
                                    right_degree
                                ][right_coordinate]
                                if (
                                    type(left) is int and left % MODULUS == 0
                                ) or (
                                    type(right) is int and right % MODULUS == 0
                                ):
                                    continue
                                terms.append(
                                    coefficient * field_product(left, right)
                                )
                target = (
                    167 % MODULUS
                    if total_degree == 0 and output_coordinate == 0
                    else 0
                )
                if not terms:
                    if target:
                        raise AssertionError("a nonzero field target lost its terms")
                    continue
                quotient = model.new_int_var(
                    -1000,
                    1000,
                    f"equation_o{orbit}_d{total_degree}_x"
                    f"{output_coordinate}_quotient",
                )
                model.add(sum(terms) == target + 3 * quotient)
                field_variables.append(quotient)

    return LabelledJetModel(
        model=model,
        bits=tuple(
            tuple(tuple(word) for word in channel) for channel in bits
        ),
        jet_variables=tuple(jet_variables),
        field_variables=tuple(field_variables),
        product_variables=tuple(product_variables.values()),
    )


def main() -> None:
    split = verify_invariant_algebra_split()
    survivor = verify_pinned_labelled_survivor()
    print(f"split_dimensions={split['split_dimensions']}")
    print(f"field_size={split['field_size']}")
    print(f"field_moduli={split['field_moduli']}")
    print(f"split_rank={split['split_rank']}")
    print(
        "nonzero_field_elements_checked="
        f"{split['nonzero_field_elements_checked']}"
    )
    print(f"basis_products_checked={split['basis_products_checked']}")
    print(f"catalog_survivor_index={survivor['catalog_index']}")
    print(
        "exact_zero_column_lags="
        f"{survivor['exact_zero_column_lags']}"
    )
    print(f"primitive9_jet_equations={survivor['jet_equations']}")
    print("PASS: exact labelled-jet algebra and pinned survivor replayed")
    print(
        "STATUS: one certified survivor; no catalog exclusion or LP(333) "
        "asserted"
    )


if __name__ == "__main__":
    main()
