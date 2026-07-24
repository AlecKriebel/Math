#!/usr/bin/env python3
"""Verify the characteristic-37 transfer theorem for order-three LP(333).

The order-three H-invariant Eisenstein group ring has dimension thirteen.
Modulo 37, the substitution x=exp(u), v=u^3 identifies it with
F_37[omega][v]/(v^13).  The group involution becomes

    F(v) -> conjugate(F(-v)).

This verifier reconstructs the resulting thirteen coefficient equations,
proves the transfer matrix invertible, and checks the formula directly
against physical and cyclotomic correlations on 373 deterministic fixtures.
It also replays 22 explicit profile witnesses showing that the previous local
mod-3 sieve, the aggregate and energy conditions, and the first two new
transfer coefficients are jointly feasible on every row-sum shard.

These are modular necessary conditions.  No witness in this file is an
LP(333) candidate.
"""

from __future__ import annotations

from collections import Counter
import csv
from hashlib import sha256
import json
from math import factorial
from pathlib import Path
from typing import Iterator, Sequence


P = 37
MODULUS = 37
CLASS_COUNT = 12
PRIMITIVE_ROOT = 2

ROOTS: tuple[tuple[int, int], ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
CANONICAL_ZERO_EXPONENTS: tuple[int, ...] = (0, 0, 0, 1, 2, 3, 1, 3, 2)

CATALOG_RELATIVE_PATH = Path("output/lp333_order3_row_sum_catalog.csv")
CATALOG_SHA256 = (
    "e8631dc0ae2f65c475af1c2e13429778f666a0fa8a13c9f1153d07d7883a98ea"
)
CATALOG_DATA_ROWS = 1_756

EXPECTED_TRANSFER_HASH = (
    "6054140458c5995d454fe1ab58269faa1b6f293e2dc901e64c01b3ee3623d2a0"
)
EXPECTED_FIXTURE_HASH = (
    "ade17851177daefcaefb416f9f52f7fbc417a4684499f2b648b4d5c0d37a103b"
)
EXPECTED_PAIRED_WITNESS_HASH = (
    "8b5040dbec2d5089e926519e6006672629e3bb110d0a48221c771ac9eddad3a6"
)

Eisenstein = tuple[int, int]  # a+b*omega, omega^2+omega+1=0.
Profile = tuple[int, int, int]
Target = tuple[int, int, int, int]


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def require_hash(label: str, value: object, expected: str) -> str:
    actual = compact_hash(value)
    if expected and actual != expected:
        raise AssertionError(f"{label} hash changed: {actual} != {expected}")
    return actual


def e_reduce(value: Eisenstein) -> Eisenstein:
    return value[0] % MODULUS, value[1] % MODULUS


def e_add(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    return (left[0] + right[0]) % MODULUS, (
        left[1] + right[1]
    ) % MODULUS


def e_scale(factor: int, value: Eisenstein) -> Eisenstein:
    return factor * value[0] % MODULUS, factor * value[1] % MODULUS


def e_conjugate(value: Eisenstein) -> Eisenstein:
    # conjugate(a+b*omega)=a+b*omega^2=(a-b)-b*omega.
    return (value[0] - value[1]) % MODULUS, (-value[1]) % MODULUS


def e_multiply(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    a, b = left
    c, d = right
    return (a * c - b * d) % MODULUS, (
        a * d + b * c - b * d
    ) % MODULUS


def e_norm_integer(value: Eisenstein) -> int:
    a, b = value
    return a * a - a * b + b * b


def profiles() -> tuple[Profile, ...]:
    result = tuple(
        (first, second, 3 - first - second)
        for first in range(4)
        for second in range(4)
        if 0 <= 3 - first - second <= 3
    )
    if len(result) != 10:
        raise AssertionError("the profile catalog must have size ten")
    return result


PROFILES = profiles()


def profile_eisenstein(profile: Profile) -> Eisenstein:
    first, second, third = profile
    return first - third, second - third


def profile_norm(profile_id: int) -> int:
    return e_norm_integer(profile_eisenstein(PROFILES[profile_id]))


def signed_profile_integer(
    channel: int, class_index: int, profile_id: int
) -> Eisenstein:
    if channel not in (0, 1):
        raise ValueError("channel must identify A or B")
    if not 0 <= class_index < CLASS_COUNT:
        raise ValueError("class index outside 0,...,11")
    if not 0 <= profile_id < len(PROFILES):
        raise ValueError("profile ID outside 0,...,9")
    epsilon = 1 if class_index % 2 == 0 else -1
    factor = -epsilon if channel == 0 else epsilon
    value = profile_eisenstein(PROFILES[profile_id])
    return factor * value[0], factor * value[1]


def signed_profile(
    channel: int, class_index: int, profile_id: int
) -> Eisenstein:
    return e_reduce(signed_profile_integer(channel, class_index, profile_id))


def cyclotomic_classes() -> tuple[tuple[int, ...], ...]:
    subgroup = tuple(pow(PRIMITIVE_ROOT, 12 * exponent, P) for exponent in range(3))
    if subgroup != (1, 26, 10):
        raise AssertionError("the order-three subgroup changed")
    classes = tuple(
        tuple((pow(PRIMITIVE_ROOT, index, P) * value) % P for value in subgroup)
        for index in range(CLASS_COUNT)
    )
    if set().union(*(set(part) for part in classes)) != set(range(1, P)):
        raise AssertionError("the classes no longer partition F_37^*")
    for index, part in enumerate(classes):
        if {(-value) % P for value in part} != set(classes[(index + 6) % 12]):
            raise AssertionError("class negation no longer shifts by six")
    return classes


CLASSES = cyclotomic_classes()
PARTS: tuple[tuple[int, ...], ...] = ((0,),) + CLASSES
CLASS_OF = {
    value: class_index
    for class_index, part in enumerate(CLASSES)
    for value in part
}


def transition_matrix(class_index: int) -> tuple[tuple[int, ...], ...]:
    representative = CLASSES[class_index][0]
    part_sets = tuple(map(set, PARTS))
    return tuple(
        tuple(
            sum(
                (value + representative) % P in part_sets[right]
                for value in PARTS[left]
            )
            for right in range(13)
        )
        for left in range(13)
    )


TRANSITION_MATRICES = tuple(transition_matrix(index) for index in range(12))


def factorial_inverse(index: int) -> int:
    if not 0 <= index < P:
        raise ValueError("factorial index must be below the characteristic")
    return pow(factorial(index) % P, -1, P)


TRANSFER_FACTORS: tuple[int, ...] = (1,) + tuple(
    3 * factorial_inverse(3 * index) % P for index in range(1, 13)
)


def transfer_matrix() -> tuple[tuple[int, ...], ...]:
    """Map the zero/class basis to the v=u^3 coefficient basis."""

    rows = [(1,) + (3,) * CLASS_COUNT]
    for frequency in range(1, 13):
        rows.append(
            (0,)
            + tuple(
                TRANSFER_FACTORS[frequency]
                * pow(8, class_index * frequency, P)
                % P
                for class_index in range(CLASS_COUNT)
            )
        )
    return tuple(rows)


TRANSFER_MATRIX = transfer_matrix()


def matrix_rank_and_determinant(
    matrix: Sequence[Sequence[int]],
) -> tuple[int, int]:
    work = [list(value % P for value in row) for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    rank = 0
    determinant = 1
    sign = 1
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        if pivot != rank:
            work[pivot], work[rank] = work[rank], work[pivot]
            sign = -sign
        pivot_value = work[rank][column]
        determinant = determinant * pivot_value % P
        inverse = pow(pivot_value, -1, P)
        work[rank] = [value * inverse % P for value in work[rank]]
        for row in range(row_count):
            if row == rank:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * right) % P
                    for left, right in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == row_count:
            break
    if row_count != column_count or rank != row_count:
        determinant = 0
    else:
        determinant = determinant * sign % P
    return rank, determinant


def matrix_inverse(
    matrix: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("matrix must be square")
    work = [
        [value % P for value in row]
        + [1 if row_index == column else 0 for column in range(size)]
        for row_index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            raise AssertionError("the transfer matrix is singular")
        work[column], work[pivot] = work[pivot], work[column]
        inverse = pow(work[column][column], -1, P)
        work[column] = [value * inverse % P for value in work[column]]
        for row in range(size):
            if row == column:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * right) % P
                    for left, right in zip(work[row], work[column])
                ]
    return tuple(tuple(row[size:]) for row in work)


TRANSFER_INVERSE = matrix_inverse(TRANSFER_MATRIX)


def scalar_matrix_vector(
    matrix: Sequence[Sequence[int]], vector: Sequence[int]
) -> tuple[int, ...]:
    return tuple(
        sum(coefficient * value for coefficient, value in zip(row, vector))
        % P
        for row in matrix
    )


def verify_transfer_linear_algebra() -> dict[str, object]:
    rank, determinant = matrix_rank_and_determinant(TRANSFER_MATRIX)
    if rank != 13 or determinant == 0:
        raise AssertionError("the characteristic-37 transfer is not invertible")
    for basis_index in range(13):
        basis = tuple(1 if index == basis_index else 0 for index in range(13))
        transformed = scalar_matrix_vector(TRANSFER_MATRIX, basis)
        recovered = scalar_matrix_vector(TRANSFER_INVERSE, transformed)
        if recovered != basis:
            raise AssertionError("the transfer inverse failed on a basis vector")

    if pow(8, 12, P) != 1 or any(pow(8, index, P) == 1 for index in range(1, 12)):
        raise AssertionError("8 must be a primitive twelfth root modulo 37")
    if (pow(10, 2, P) + 10 + 1) % P != 0:
        raise AssertionError("10 must realize omega modulo 37")
    if (pow(26, 2, P) + 26 + 1) % P != 0:
        raise AssertionError("26 must realize conjugate(omega) modulo 37")

    payload = (
        CLASSES,
        TRANSFER_FACTORS,
        TRANSFER_MATRIX,
        rank,
        determinant,
    )
    transfer_hash = require_hash(
        "characteristic-37 transfer", payload, EXPECTED_TRANSFER_HASH
    )
    return {
        "rank": rank,
        "determinant": determinant,
        "transfer_hash": transfer_hash,
        "dimension": 13,
    }


def class_coefficients(channel: int, profile_ids: Sequence[int]) -> tuple[Eisenstein, ...]:
    if len(profile_ids) != CLASS_COUNT:
        raise ValueError("expected twelve profile IDs")
    return tuple(
        signed_profile(channel, class_index, profile_id)
        for class_index, profile_id in enumerate(profile_ids)
    )


def expanded_sequence(
    zero: Eisenstein, coefficients: Sequence[Eisenstein]
) -> tuple[Eisenstein, ...]:
    if len(coefficients) != CLASS_COUNT:
        raise ValueError("expected twelve class coefficients")
    return tuple(
        e_reduce(zero) if column == 0 else coefficients[CLASS_OF[column]]
        for column in range(P)
    )


def polynomial_group_correlation(
    a_sequence: Sequence[Eisenstein],
    b_sequence: Sequence[Eisenstein],
) -> tuple[Eisenstein, ...]:
    """Return coefficients of A(x)A*(x)+B(x)B*(x)."""

    if len(a_sequence) != P or len(b_sequence) != P:
        raise ValueError("group sequences must have length 37")
    result = []
    for exponent in range(P):
        total = (0, 0)
        for sequence in (a_sequence, b_sequence):
            for left_index in range(P):
                right_index = (left_index - exponent) % P
                total = e_add(
                    total,
                    e_multiply(
                        sequence[left_index],
                        e_conjugate(sequence[right_index]),
                    ),
                )
        result.append(total)
    return tuple(result)


def quotient_correlation(
    a_parts: Sequence[Eisenstein],
    b_parts: Sequence[Eisenstein],
    class_index: int,
) -> Eisenstein:
    """Evaluate shift +b for b in C_class_index via transition counts."""

    matrix = TRANSITION_MATRICES[class_index]
    total = (0, 0)
    for values in (a_parts, b_parts):
        for left in range(13):
            for right, count in enumerate(matrix[left]):
                if count:
                    total = e_add(
                        total,
                        e_scale(
                            count,
                            e_multiply(
                                values[left],
                                e_conjugate(values[right]),
                            ),
                        ),
                    )
    return total


def direct_log_transfer(
    coefficients: Sequence[Eisenstein],
) -> tuple[Eisenstein, ...]:
    """Substitute x=exp(u), v=u^3 into one H-invariant polynomial."""

    if len(coefficients) != P:
        raise ValueError("expected 37 group coefficients")
    result = []
    for frequency in range(13):
        degree = 3 * frequency
        inverse_factorial = factorial_inverse(degree)
        total = (0, 0)
        for exponent, value in enumerate(coefficients):
            weight = pow(exponent, degree, P) if degree else 1
            total = e_add(
                total,
                e_scale(weight * inverse_factorial, value),
            )
        result.append(total)
    return tuple(result)


def class_log_transfer(
    zero: Eisenstein, coefficients: Sequence[Eisenstein]
) -> tuple[Eisenstein, ...]:
    if len(coefficients) != CLASS_COUNT:
        raise ValueError("expected twelve class coefficients")
    result = [
        e_add(e_reduce(zero), e_scale(3, sum_eisenstein(coefficients)))
    ]
    for frequency in range(1, 13):
        total = (0, 0)
        for class_index, value in enumerate(coefficients):
            weight = (
                TRANSFER_FACTORS[frequency]
                * pow(8, class_index * frequency, P)
            )
            total = e_add(total, e_scale(weight, value))
        result.append(total)
    return tuple(result)


def sum_eisenstein(values: Sequence[Eisenstein]) -> Eisenstein:
    total = (0, 0)
    for value in values:
        total = e_add(total, value)
    return total


def norm_transfer(
    a_transfer: Sequence[Eisenstein],
    b_transfer: Sequence[Eisenstein],
) -> tuple[Eisenstein, ...]:
    if len(a_transfer) != 13 or len(b_transfer) != 13:
        raise ValueError("transfer words must have length thirteen")
    result = []
    for degree in range(13):
        total = (0, 0)
        for word in (a_transfer, b_transfer):
            for left_degree in range(degree + 1):
                right_degree = degree - left_degree
                sign = -1 if right_degree % 2 else 1
                total = e_add(
                    total,
                    e_scale(
                        sign,
                        e_multiply(
                            word[left_degree],
                            e_conjugate(word[right_degree]),
                        ),
                    ),
                )
        result.append(total)
    return tuple(result)


def nonmultiple_moments_vanish(
    coefficients: Sequence[Eisenstein],
) -> None:
    for degree in range(1, 37):
        if degree % 3 == 0:
            continue
        total = (0, 0)
        inverse_factorial = factorial_inverse(degree)
        for exponent, value in enumerate(coefficients):
            total = e_add(
                total,
                e_scale(
                    pow(exponent, degree, P) * inverse_factorial,
                    value,
                ),
            )
        if total != (0, 0):
            raise AssertionError("an H-invariant nonmultiple moment survived")


def fixture_catalog() -> tuple[tuple[str, tuple[int, ...], tuple[int, ...]], ...]:
    base = (5,) * CLASS_COUNT  # profile 5 is (1,1,1), hence z=0.
    fixtures: list[tuple[str, tuple[int, ...], tuple[int, ...]]] = [
        ("zero", base, base)
    ]
    for channel in range(2):
        for class_index in range(CLASS_COUNT):
            for profile_id in range(10):
                a_ids = list(base)
                b_ids = list(base)
                target = a_ids if channel == 0 else b_ids
                target[class_index] = profile_id
                fixtures.append(
                    (
                        f"single_{channel}_{class_index}_{profile_id}",
                        tuple(a_ids),
                        tuple(b_ids),
                    )
                )
    for a_id in range(10):
        for b_id in range(10):
            a_ids = list(base)
            b_ids = list(base)
            a_ids[0] = a_id
            b_ids[7] = b_id
            fixtures.append((f"pair_{a_id}_{b_id}", tuple(a_ids), tuple(b_ids)))
    for seed in range(32):
        a_ids = tuple((seed * 7 + 3 * index + index * index) % 10 for index in range(12))
        b_ids = tuple((seed * 9 + 5 * index + 2 * index * index) % 10 for index in range(12))
        fixtures.append((f"dense_{seed}", a_ids, b_ids))
    if len(fixtures) != 373:
        raise AssertionError("the deterministic fixture count changed")
    return tuple(fixtures)


FIXTURES = fixture_catalog()


def verify_fixture_equivalence() -> dict[str, object]:
    zero_a = (-1, 0)
    zero_b = (2, 0)
    checks = 0
    for _, a_ids, b_ids in FIXTURES:
        a_classes = class_coefficients(0, a_ids)
        b_classes = class_coefficients(1, b_ids)
        a_sequence = expanded_sequence(zero_a, a_classes)
        b_sequence = expanded_sequence(zero_b, b_classes)

        nonmultiple_moments_vanish(a_sequence)
        nonmultiple_moments_vanish(b_sequence)
        a_direct = direct_log_transfer(a_sequence)
        b_direct = direct_log_transfer(b_sequence)
        a_short = class_log_transfer(zero_a, a_classes)
        b_short = class_log_transfer(zero_b, b_classes)
        if a_direct != a_short or b_direct != b_short:
            raise AssertionError("class and physical logarithmic transforms differ")

        group_correlation = polynomial_group_correlation(a_sequence, b_sequence)
        direct_transfer = direct_log_transfer(group_correlation)
        short_transfer = norm_transfer(a_short, b_short)
        if direct_transfer != short_transfer:
            raise AssertionError("the characteristic-37 norm formula failed")

        # Audit both the physical +b orientation and all transition matrices.
        a_parts = (e_reduce(zero_a),) + a_classes
        b_parts = (e_reduce(zero_b),) + b_classes
        for class_index, part in enumerate(CLASSES):
            representative = part[0]
            physical = (0, 0)
            for sequence in (a_sequence, b_sequence):
                for column in range(P):
                    physical = e_add(
                        physical,
                        e_multiply(
                            sequence[column],
                            e_conjugate(sequence[(column + representative) % P]),
                        ),
                    )
            quotient = quotient_correlation(
                a_parts, b_parts, class_index
            )
            if physical != quotient:
                raise AssertionError("a cyclotomic transition equation changed")
            if physical != group_correlation[(-representative) % P]:
                raise AssertionError("the group-ring correlation orientation changed")

        for class_index, part in enumerate(CLASSES):
            values = {group_correlation[value] for value in part}
            if len(values) != 1:
                raise AssertionError("a group correlation is not H-invariant")
        checks += 1

    fixture_payload = tuple(
        (name, a_ids, b_ids) for name, a_ids, b_ids in FIXTURES
    )
    fixture_hash = require_hash(
        "characteristic-37 fixtures", fixture_payload, EXPECTED_FIXTURE_HASH
    )
    return {
        "fixtures": len(FIXTURES),
        "fixture_hash": fixture_hash,
        "physical_transfer_checks": checks,
        "cyclotomic_equations_per_fixture": 12,
    }


# Each entry is
#   (class-aggregate target, twelve A profile IDs, twelve B profile IDs).
# The witnesses satisfy the aggregate, total norm 54, local mod-3 opposite-
# class condition, and characteristic-37 transfer coefficients 1 and 2.
# They do not satisfy all thirteen transfer coefficients.
PAIRED_LAYER_WITNESSES: tuple[
    tuple[Target, tuple[int, ...], tuple[int, ...]], ...
] = (
    ((-3, -3, -4, -2), (9, 5, 3, 0, 5, 6, 5, 5, 0, 5, 5, 4), (1, 5, 5, 5, 5, 7, 7, 5, 5, 5, 5, 8)),
    ((-3, -3, -2, 2), (4, 9, 3, 0, 9, 5, 7, 5, 5, 5, 5, 5), (6, 9, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)),
    ((-3, 0, -3, -3), (5, 5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 3), (5, 3, 5, 5, 5, 9, 5, 5, 9, 5, 5, 9)),
    ((-3, 0, 0, 3), (0, 5, 0, 5, 5, 5, 5, 0, 5, 5, 9, 0), (5, 5, 5, 5, 5, 5, 3, 5, 5, 5, 5, 5)),
    ((-1, -2, -5, -1), (7, 6, 9, 9, 3, 5, 6, 5, 5, 5, 5, 5), (7, 7, 5, 5, 5, 5, 1, 5, 5, 5, 5, 9)),
    ((-1, -2, -4, 1), (9, 5, 5, 8, 5, 3, 3, 5, 1, 4, 6, 5), (5, 9, 5, 5, 5, 5, 5, 5, 6, 5, 1, 5)),
    ((0, 3, -4, -2), (6, 9, 0, 3, 9, 5, 8, 5, 5, 5, 5, 5), (4, 9, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)),
    ((0, 3, -2, 2), (3, 7, 9, 2, 0, 5, 4, 5, 5, 2, 5, 5), (5, 6, 5, 5, 5, 5, 2, 5, 3, 5, 5, 5)),
    ((1, -1, 2, -2), (8, 9, 4, 1, 5, 5, 4, 5, 5, 5, 3, 5), (5, 5, 9, 5, 5, 5, 5, 5, 1, 8, 9, 5)),
    ((1, -1, 4, 2), (5, 5, 5, 5, 5, 5, 3, 6, 5, 5, 5, 5), (5, 5, 5, 1, 8, 3, 3, 7, 9, 7, 4, 5)),
    ((1, 2, -5, -1), (5, 2, 4, 0, 2, 5, 5, 2, 0, 5, 2, 5), (0, 9, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5)),
    ((1, 2, -4, 1), (5, 5, 5, 1, 0, 9, 6, 5, 9, 5, 5, 6), (2, 5, 5, 7, 5, 4, 5, 5, 0, 5, 5, 5)),
    ((2, -2, -4, -2), (2, 5, 5, 9, 5, 0, 5, 5, 5, 6, 5, 5), (4, 5, 5, 8, 5, 2, 5, 5, 3, 5, 0, 4)),
    ((2, -2, -2, 2), (5, 7, 1, 4, 5, 5, 5, 5, 5, 5, 5, 5), (5, 9, 5, 8, 9, 5, 5, 4, 2, 5, 0, 0)),
    ((2, 1, 2, -2), (5, 5, 4, 5, 5, 5, 5, 5, 5, 9, 4, 0), (7, 5, 4, 5, 7, 5, 7, 0, 5, 9, 5, 5)),
    ((2, 1, 4, 2), (5, 5, 5, 5, 5, 2, 5, 4, 5, 8, 5, 8), (6, 0, 8, 2, 4, 8, 7, 4, 8, 7, 4, 8)),
    ((3, 0, 0, -3), (4, 2, 3, 9, 9, 9, 6, 6, 5, 5, 5, 5), (7, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)),
    ((3, 0, 3, 3), (5, 9, 5, 3, 0, 0, 3, 5, 5, 5, 5, 5), (5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5)),
    ((4, -1, 0, 0), (5, 5, 2, 5, 5, 5, 5, 9, 5, 5, 5, 5), (0, 0, 1, 5, 5, 5, 5, 3, 2, 5, 5, 0)),
    ((4, 2, -4, -2), (5, 5, 7, 9, 9, 9, 1, 5, 5, 5, 5, 5), (5, 8, 5, 3, 5, 5, 6, 8, 2, 5, 5, 5)),
    ((4, 2, -2, 2), (1, 5, 5, 5, 5, 5, 5, 3, 5, 9, 2, 1), (6, 5, 5, 5, 1, 5, 0, 5, 3, 5, 5, 1)),
    ((5, 1, 0, 0), (5, 5, 5, 5, 5, 8, 5, 5, 5, 9, 5, 5), (3, 5, 9, 5, 0, 6, 5, 5, 5, 5, 3, 2)),
)


def row_sum_targets(catalog_path: Path | None = None) -> tuple[Target, ...]:
    path = (
        catalog_path
        if catalog_path is not None
        else Path(__file__).resolve().parent / CATALOG_RELATIVE_PATH
    )
    payload = path.read_bytes()
    if sha256(payload).hexdigest() != CATALOG_SHA256:
        raise AssertionError("the row-sum catalog byte hash changed")
    rows = list(csv.DictReader(payload.decode("ascii").splitlines()))
    if len(rows) != CATALOG_DATA_ROWS:
        raise AssertionError("the row-sum catalog row count changed")
    zero = tuple(ROOTS[exponent] for exponent in CANONICAL_ZERO_EXPONENTS)
    targets: set[Target] = set()
    for row in rows:
        row_sum = tuple(
            (int(row[f"s{index}_real"]), int(row[f"s{index}_imag"]))
            for index in range(9)
        )
        t_values = []
        for value, zero_value in zip(row_sum, zero):
            difference = value[0] - zero_value[0], value[1] - zero_value[1]
            if difference[0] % 3 or difference[1] % 3:
                raise AssertionError("a row-sum word is not x+3t")
            t_values.append((difference[0] // 3, difference[1] // 3))
        aggregate = tuple(
            tuple(
                sum(t_values[index][coordinate] for index in range(residue, 9, 3))
                for coordinate in (0, 1)
            )
            for residue in range(3)
        )
        a_binary = tuple(real - imag for real, imag in aggregate)
        b_binary = tuple(real + imag for real, imag in aggregate)
        targets.add(
            (
                (a_binary[0] - a_binary[2]) // 2,
                (a_binary[1] - a_binary[2]) // 2,
                (b_binary[0] - b_binary[2]) // 2,
                (b_binary[1] - b_binary[2]) // 2,
            )
        )
    if len(targets) != 22:
        raise AssertionError("the row-sum catalog no longer has 22 targets")
    return tuple(sorted(targets))


def pair_signature(left_id: int, right_id: int) -> Eisenstein:
    left = profile_eisenstein(PROFILES[left_id])
    right = profile_eisenstein(PROFILES[right_id])
    value = (
        left[0] - left[1] + right[0],
        -left[1] + right[1],
    )
    return value[0] % 3, value[1] % 3


def verify_paired_layer_witnesses() -> dict[str, object]:
    targets = set(row_sum_targets())
    witness_targets: set[Target] = set()
    higher_bad_histogram: Counter[int] = Counter()
    for target, a_ids, b_ids in PAIRED_LAYER_WITNESSES:
        if target in witness_targets:
            raise AssertionError("the paired-layer witness table has a duplicate")
        witness_targets.add(target)
        if len(a_ids) != 12 or len(b_ids) != 12:
            raise AssertionError("a paired-layer witness has the wrong length")

        aggregate_values = []
        for channel, identifiers in enumerate((a_ids, b_ids)):
            total = (0, 0)
            for class_index, profile_id in enumerate(identifiers):
                value = signed_profile_integer(channel, class_index, profile_id)
                total = total[0] + value[0], total[1] + value[1]
            aggregate_values.extend(total)
        if tuple(aggregate_values) != target:
            raise AssertionError("a paired-layer witness has the wrong aggregate")

        total_energy = sum(profile_norm(value) for value in (*a_ids, *b_ids))
        if total_energy != 54:
            raise AssertionError("a paired-layer witness has the wrong energy")
        for class_index in range(6):
            if pair_signature(
                a_ids[class_index], a_ids[class_index + 6]
            ) != pair_signature(
                b_ids[class_index], b_ids[class_index + 6]
            ):
                raise AssertionError("a paired-layer witness fails the mod-3 sieve")

        full_a = (-1 + 3 * target[0], 3 * target[1])
        full_b = (2 + 3 * target[2], 3 * target[3])
        if e_norm_integer(full_a) + e_norm_integer(full_b) != 167:
            raise AssertionError("a paired-layer target lost norm 167")

        a_transfer = class_log_transfer(
            (-1, 0), class_coefficients(0, a_ids)
        )
        b_transfer = class_log_transfer(
            (2, 0), class_coefficients(1, b_ids)
        )
        combined = norm_transfer(a_transfer, b_transfer)
        if combined[0] != (167 % P, 0):
            raise AssertionError("a paired-layer witness lost the origin target")
        if combined[1] != (0, 0) or combined[2] != (0, 0):
            raise AssertionError("a paired-layer witness fails coefficient one or two")
        higher_bad = sum(value != (0, 0) for value in combined[3:])
        if higher_bad == 0:
            raise AssertionError("a paired-layer witness was mislabelled as partial")
        higher_bad_histogram[higher_bad] += 1

    if witness_targets != targets:
        raise AssertionError("the paired-layer witnesses do not cover all 22 shards")
    witness_hash = require_hash(
        "paired characteristic-37 witnesses",
        PAIRED_LAYER_WITNESSES,
        EXPECTED_PAIRED_WITNESS_HASH,
    )
    return {
        "aggregate_shards": len(targets),
        "surviving_first_two_coefficients": len(witness_targets),
        "higher_bad_histogram": tuple(sorted(higher_bad_histogram.items())),
        "paired_witness_hash": witness_hash,
        "is_full_mod37_witness": False,
    }


def verify_all() -> dict[str, object]:
    return {
        "linear_algebra": verify_transfer_linear_algebra(),
        "fixtures": verify_fixture_equivalence(),
        "paired": verify_paired_layer_witnesses(),
    }


def main() -> None:
    result = verify_all()
    linear = result["linear_algebra"]
    fixtures = result["fixtures"]
    paired = result["paired"]
    print(f"transfer_dimension={linear['dimension']}")
    print(f"transfer_rank={linear['rank']}")
    print(f"transfer_determinant_mod37={linear['determinant']}")
    print(f"transfer_hash={linear['transfer_hash']}")
    print(f"fixture_count={fixtures['fixtures']}")
    print(f"fixture_hash={fixtures['fixture_hash']}")
    print(
        "cyclotomic_equations_checked="
        f"{fixtures['fixtures'] * fixtures['cyclotomic_equations_per_fixture']}"
    )
    print(
        "paired_layer_shards="
        f"{paired['surviving_first_two_coefficients']}/"
        f"{paired['aggregate_shards']}"
    )
    print(f"higher_bad_histogram={paired['higher_bad_histogram']}")
    print(f"paired_witness_hash={paired['paired_witness_hash']}")
    print("PASS: characteristic-37 logarithmic transfer replayed")
    print("STATUS: first two transfer coefficients leave all 22 shards alive")
    print("STATUS: no LP(333) or H(668) candidate")


if __name__ == "__main__":
    main()
