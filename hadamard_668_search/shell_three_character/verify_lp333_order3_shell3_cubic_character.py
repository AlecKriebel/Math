#!/usr/bin/env python3
"""Verify the cubic characteristic-37 gate on shell-three controls.

This module is dependency-free.  It deliberately embeds only the six
previously pinned (3,9,12) primitive-nine witnesses, so it does not depend
on the larger search package or silently inherit its arithmetic.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from typing import Iterable, Sequence


P = 37
H = (1, 10, 26)
PROFILE_VALUES = (
    (-3, -3),
    (-2, -1),
    (-1, 1),
    (0, 3),
    (-1, -2),
    (0, 0),
    (1, 2),
    (1, -1),
    (2, 1),
    (3, 0),
)
TARGETS = (
    (-3, -3, -4, -2),
    (-3, -3, -2, 2),
    (-3, 0, -3, -3),
    (-3, 0, 0, 3),
    (-1, -2, -5, -1),
    (-1, -2, -4, 1),
    (0, 3, -4, -2),
    (0, 3, -2, 2),
    (1, -1, 2, -2),
    (1, -1, 4, 2),
    (1, 2, -5, -1),
    (1, 2, -4, 1),
    (2, -2, -4, -2),
    (2, -2, -2, 2),
    (2, 1, 2, -2),
    (2, 1, 4, 2),
    (3, 0, 0, -3),
    (3, 0, 3, 3),
    (4, -1, 0, 0),
    (4, 2, -4, -2),
    (4, 2, -2, 2),
    (5, 1, 0, 0),
)

# target, A profile IDs, B profile IDs, expected cubic scalar
SHELL3_CONTROLS = (
    (
        (-3, -3, -4, -2),
        (2, 4, 6, 3, 3, 5, 7, 7, 8, 3, 5, 5),
        (5, 6, 5, 5, 5, 5, 2, 5, 1, 5, 5, 5),
        31,
    ),
    (
        (-3, 0, -3, -3),
        (5, 2, 5, 1, 8, 5, 5, 9, 7, 5, 5, 5),
        (5, 6, 4, 6, 4, 5, 3, 2, 5, 5, 3, 5),
        6,
    ),
    (
        (0, 3, -4, -2),
        (5, 3, 7, 5, 5, 5, 7, 9, 8, 4, 5, 8),
        (2, 5, 8, 6, 5, 6, 5, 9, 5, 5, 5, 5),
        4,
    ),
    (
        (2, 1, 2, -2),
        (4, 9, 6, 5, 5, 5, 7, 5, 5, 5, 5, 5),
        (1, 3, 6, 1, 5, 4, 5, 3, 5, 6, 5, 4),
        14,
    ),
    (
        (3, 0, 3, 3),
        (2, 5, 4, 5, 8, 9, 5, 7, 5, 5, 7, 5),
        (4, 4, 8, 5, 1, 5, 3, 5, 9, 5, 5, 5),
        36,
    ),
    (
        (5, 1, 0, 0),
        (4, 5, 5, 7, 5, 5, 6, 8, 5, 9, 5, 2),
        (5, 1, 5, 9, 0, 5, 8, 5, 5, 2, 5, 4),
        11,
    ),
)

EXPECTED_CONTROL_HASH = (
    "906eeeb7cf10895e381ff5963e229a30dfc2f8cc8de351af4c3ab4f790bdb932"
)


def add(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return x[0] + y[0], x[1] + y[1]


def scale(n: int, x: tuple[int, int]) -> tuple[int, int]:
    return n * x[0], n * x[1]


def conjugate(x: tuple[int, int]) -> tuple[int, int]:
    return x[0] - x[1], -x[1]


def multiply(
    x: tuple[int, int], y: tuple[int, int]
) -> tuple[int, int]:
    a, b = x
    c, d = y
    return a * c - b * d, a * d + b * c - b * d


def norm(x: tuple[int, int]) -> int:
    return x[0] * x[0] - x[0] * x[1] + x[1] * x[1]


def determinant(
    x: tuple[int, int], y: tuple[int, int]
) -> int:
    return x[0] * y[1] - x[1] * y[0]


def signed_profile(
    channel: int, class_index: int, profile_id: int
) -> tuple[int, int]:
    epsilon = 1 if class_index % 2 == 0 else -1
    factor = -epsilon if channel == 0 else epsilon
    return scale(factor, PROFILE_VALUES[profile_id])


def classes() -> tuple[tuple[int, int, int], ...]:
    result = []
    seen: set[int] = set()
    for class_index in range(12):
        multiplier = pow(2, class_index, P)
        part = tuple(multiplier * h % P for h in H)
        if seen.intersection(part):
            raise AssertionError("cyclotomic classes overlap")
        seen.update(part)
        result.append(part)
    if seen != set(range(1, P)):
        raise AssertionError("cyclotomic classes do not cover F_37^*")
    return tuple(result)


CLASSES = classes()


def physical_word(
    channel: int, identifiers: Sequence[int]
) -> tuple[tuple[int, int], ...]:
    if len(identifiers) != 12:
        raise ValueError("a profile word needs twelve class identifiers")
    word: list[tuple[int, int] | None] = [None] * P
    word[0] = (-1, 0) if channel == 0 else (2, 0)
    for class_index, part in enumerate(CLASSES):
        value = signed_profile(
            channel, class_index, identifiers[class_index]
        )
        for column in part:
            word[column] = value
    if any(value is None for value in word):
        raise AssertionError("physical expansion left an empty column")
    return tuple(value for value in word if value is not None)


def correlations(
    word_a: Sequence[tuple[int, int]],
    word_b: Sequence[tuple[int, int]],
) -> tuple[tuple[int, int], ...]:
    result = []
    for lag in range(P):
        total = (0, 0)
        for word in (word_a, word_b):
            for column in range(P):
                total = add(
                    total,
                    multiply(
                        word[(column + lag) % P],
                        conjugate(word[column]),
                    ),
                )
        result.append(total)
    return tuple(result)


def cross_correlations(
    left: Sequence[tuple[int, int]],
    right: Sequence[tuple[int, int]],
) -> tuple[tuple[int, int], ...]:
    result = []
    for lag in range(P):
        total = (0, 0)
        for column in range(P):
            total = add(
                total,
                multiply(
                    left[(column + lag) % P],
                    conjugate(right[column]),
                ),
            )
        result.append(total)
    return tuple(result)


def moment(
    word: Sequence[tuple[int, int]], exponent: int
) -> tuple[int, int]:
    total = (0, 0)
    for column, value in enumerate(word):
        total = add(total, scale(pow(column, exponent, P), value))
    return total[0] % P, total[1] % P


def class_moment_word(
    word: Sequence[tuple[int, int]]
) -> tuple[int, int]:
    total = (0, 0)
    for class_index, part in enumerate(CLASSES):
        first = word[part[0]]
        if any(word[column] != first for column in part):
            raise ValueError("word is not H-invariant")
        total = add(total, scale(pow(8, class_index, P), first))
    return total[0] % P, total[1] % P


def class_moment(
    channel: int, identifiers: Sequence[int]
) -> tuple[int, int]:
    total = (0, 0)
    for class_index, profile_id in enumerate(identifiers):
        total = add(
            total,
            scale(
                pow(8, class_index, P),
                signed_profile(channel, class_index, profile_id),
            ),
        )
    return total[0] % P, total[1] % P


def aggregate(
    channel: int, identifiers: Sequence[int]
) -> tuple[int, int]:
    total = (0, 0)
    for class_index, profile_id in enumerate(identifiers):
        total = add(
            total, signed_profile(channel, class_index, profile_id)
        )
    return total


def total_at_one(
    channel: int, identifiers: Sequence[int]
) -> tuple[int, int]:
    zero = (-1, 0) if channel == 0 else (2, 0)
    return add(zero, scale(3, aggregate(channel, identifiers)))


def cubic_scalar(
    identifiers_a: Sequence[int], identifiers_b: Sequence[int]
) -> int:
    moment_a = class_moment(0, identifiers_a)
    moment_b = class_moment(1, identifiers_b)
    total_a = total_at_one(0, identifiers_a)
    total_b = total_at_one(1, identifiers_b)
    return (
        determinant(moment_a, total_a)
        + determinant(moment_b, total_b)
    ) % P


def in_three_lambda(value: tuple[int, int]) -> bool:
    a, b = value
    return a % 3 == 0 and b % 3 == 0 and (a // 3 + b // 3) % 3 == 0


def matrix_rank_mod_p(rows: Iterable[Sequence[int]], prime: int) -> int:
    matrix = [[value % prime for value in row] for row in rows]
    if not matrix:
        return 0
    columns = len(matrix[0])
    if any(len(row) != columns for row in matrix):
        raise ValueError("ragged matrix")
    rank = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(rank, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, prime)
        matrix[rank] = [
            value * inverse % prime for value in matrix[rank]
        ]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % prime
                for left, right in zip(matrix[row], matrix[rank])
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def mod_pair(value: tuple[int, int]) -> tuple[int, int]:
    return value[0] % P, value[1] % P


def weighted_cubic(
    values: Sequence[tuple[int, int]]
) -> tuple[int, int]:
    total = (0, 0)
    for lag, value in enumerate(values):
        total = add(total, scale(pow(lag, 3, P), value))
    return mod_pair(total)


def basis_word(
    part_index: int, coefficient: tuple[int, int]
) -> tuple[tuple[int, int], ...]:
    if not 0 <= part_index <= 12:
        raise ValueError("part index must lie in 0,...,12")
    word = [(0, 0)] * P
    part = (0,) if part_index == 0 else CLASSES[part_index - 1]
    for column in part:
        word[column] = coefficient
    return tuple(word)


def audit_invariant_basis() -> int:
    """Check the cubic identity on a sesquilinear invariant basis.

    The thirteen supports are {0},C_0,...,C_11.  Coefficients 1 and omega
    form a Z/37-basis of the Eisenstein coefficient ring, so the 676 ordered
    cross checks span every pair of invariant Eisenstein words.
    """

    coefficient_basis = ((1, 0), (0, 1))
    checks = 0
    for left_part in range(13):
        for right_part in range(13):
            for left_coefficient in coefficient_basis:
                for right_coefficient in coefficient_basis:
                    left = basis_word(left_part, left_coefficient)
                    right = basis_word(right_part, right_coefficient)
                    direct = weighted_cubic(
                        cross_correlations(left, right)
                    )

                    moments_left = tuple(
                        moment(left, exponent) for exponent in range(4)
                    )
                    moments_right = tuple(
                        moment(right, exponent) for exponent in range(4)
                    )
                    expanded = (0, 0)
                    for exponent, binomial in enumerate((1, 3, 3, 1)):
                        term = multiply(
                            moments_left[3 - exponent],
                            conjugate(moments_right[exponent]),
                        )
                        expanded = add(
                            expanded,
                            scale(
                                binomial if exponent % 2 == 0 else -binomial,
                                term,
                            ),
                        )
                    if direct != mod_pair(expanded):
                        raise AssertionError(
                            "cubic binomial moment identity failed on basis"
                        )

                    if moments_left[1:3] != ((0, 0), (0, 0)):
                        raise AssertionError("left invariant basis lost M1/M2")
                    if moments_right[1:3] != ((0, 0), (0, 0)):
                        raise AssertionError("right invariant basis lost M1/M2")
                    p_left = class_moment_word(left)
                    p_right = class_moment_word(right)
                    reduced = scale(
                        3,
                        add(
                            multiply(
                                p_left,
                                conjugate(moments_right[0]),
                            ),
                            scale(
                                -1,
                                multiply(
                                    moments_left[0],
                                    conjugate(p_right),
                                ),
                            ),
                        ),
                    )
                    if direct != mod_pair(reduced):
                        raise AssertionError(
                            "reduced cubic character identity failed on basis"
                        )
                    checks += 1
    if checks != 13 * 13 * 2 * 2:
        raise AssertionError("invariant basis check count changed")
    return checks


def audit_channel_conventions() -> int:
    """Check both fixed origins and all signed one-class profile states."""

    checks = 0
    for channel, origin in ((0, (-1, 0)), (1, (2, 0))):
        for class_index, part in enumerate(CLASSES):
            for profile_id in range(len(PROFILE_VALUES)):
                word = [(0, 0)] * P
                word[0] = origin
                coefficient = signed_profile(
                    channel, class_index, profile_id
                )
                for column in part:
                    word[column] = coefficient
                direct = weighted_cubic(cross_correlations(word, word))
                p_value = scale(pow(8, class_index, P), coefficient)
                m_zero = add(origin, scale(3, coefficient))
                scalar = determinant(p_value, m_zero) % P
                expected = (-3 * scalar) % P, (-6 * scalar) % P
                if direct != expected:
                    raise AssertionError(
                        "fixed-origin/channel cubic convention failed"
                    )
                checks += 1
    if checks != 2 * 12 * len(PROFILE_VALUES):
        raise AssertionError("channel convention check count changed")
    return checks


def audit_wedge_determinant() -> int:
    checks = 0
    for a in range(-2, 3):
        for b in range(-2, 3):
            for c in range(-2, 3):
                for d in range(-2, 3):
                    left = (a, b)
                    right = (c, d)
                    wedge = add(
                        multiply(left, conjugate(right)),
                        scale(
                            -1, multiply(right, conjugate(left))
                        ),
                    )
                    det = determinant(left, right)
                    if wedge != (-det, -2 * det):
                        raise AssertionError(
                            "determinant/wedge sign convention failed"
                        )
                    checks += 1
    return checks


def target_character_rank(target: Sequence[int]) -> int:
    total_a = (3 * target[0] - 1, 3 * target[1])
    total_b = (3 * target[2] + 2, 3 * target[3])
    rows = [[0] * 48 for _ in range(5)]
    for channel in range(2):
        total = total_a if channel == 0 else total_b
        for class_index in range(12):
            offset = 24 * channel + 2 * class_index
            rows[2 * channel][offset] = 1
            rows[2 * channel + 1][offset + 1] = 1
            weight = pow(8, class_index, P)
            rows[4][offset] = weight * total[1]
            rows[4][offset + 1] = -weight * total[0]
    return matrix_rank_mod_p(rows, P)


def audit_control(
    target: Sequence[int],
    identifiers_a: Sequence[int],
    identifiers_b: Sequence[int],
    expected_scalar: int,
) -> dict[str, object]:
    if tuple(target) not in TARGETS:
        raise AssertionError("control target left the 22-target catalog")
    if aggregate(0, identifiers_a) != tuple(target[:2]):
        raise AssertionError("A aggregate mismatch")
    if aggregate(1, identifiers_b) != tuple(target[2:]):
        raise AssertionError("B aggregate mismatch")
    histogram = Counter(
        norm(PROFILE_VALUES[profile_id])
        for profile_id in tuple(identifiers_a) + tuple(identifiers_b)
    )
    if (histogram[9], histogram[3], histogram[0]) != (3, 9, 12):
        raise AssertionError("control left the shell (3,9,12)")

    word_a = physical_word(0, identifiers_a)
    word_b = physical_word(1, identifiers_b)
    direct = correlations(word_a, word_b)
    if direct[0] != (167, 0):
        raise AssertionError("origin energy changed")
    if not all(in_three_lambda(value) for value in direct[1:]):
        raise AssertionError("control lost the primitive-nine ideal")

    # Direct moment checks, independent of the class-moment shortcut.
    for word in (word_a, word_b):
        if moment(word, 1) != (0, 0) or moment(word, 2) != (0, 0):
            raise AssertionError("H-invariance did not kill M1,M2")
    class_a = class_moment(0, identifiers_a)
    class_b = class_moment(1, identifiers_b)
    if moment(word_a, 3) != (
        3 * class_a[0] % P,
        3 * class_a[1] % P,
    ):
        raise AssertionError("M3(A)=3P(A) failed")
    if moment(word_b, 3) != (
        3 * class_b[0] % P,
        3 * class_b[1] % P,
    ):
        raise AssertionError("M3(B)=3P(B) failed")

    scalar = cubic_scalar(identifiers_a, identifiers_b)
    if scalar != expected_scalar or scalar == 0:
        raise AssertionError("pinned cubic obstruction changed")
    weighted_mod = weighted_cubic(direct)
    expected_weighted = (-3 * scalar) % P, (-6 * scalar) % P
    if weighted_mod != expected_weighted:
        raise AssertionError("weighted correlation/moment identity failed")

    return {
        "target": list(target),
        "cubic_scalar": scalar,
        "weighted_correlation": list(weighted_mod),
        "nonzero_ideal_parts": 36,
    }


def compact_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("ascii")).hexdigest()


def verify() -> dict[str, object]:
    if tuple(sum(pow(h, k, P) for h in H) % P for k in (1, 2, 3)) != (
        0,
        0,
        3,
    ):
        raise AssertionError("subgroup power sums changed")
    if pow(8, 12, P) != 1:
        raise AssertionError("8 does not have order twelve")
    if any(pow(8, divisor, P) == 1 for divisor in (1, 2, 3, 4, 6)):
        raise AssertionError("8 has order a proper divisor of twelve")

    ranks = tuple(target_character_rank(target) for target in TARGETS)
    if ranks != (5,) * len(TARGETS):
        raise AssertionError("cubic row is aggregate-dependent")
    invariant_basis_checks = audit_invariant_basis()
    channel_convention_checks = audit_channel_conventions()
    wedge_checks = audit_wedge_determinant()
    controls = tuple(audit_control(*control) for control in SHELL3_CONTROLS)
    control_hash = compact_hash(controls)
    if EXPECTED_CONTROL_HASH and control_hash != EXPECTED_CONTROL_HASH:
        raise AssertionError("control replay hash changed")
    return {
        "targets_rank_five": len(TARGETS),
        "invariant_basis_checks": invariant_basis_checks,
        "channel_convention_checks": channel_convention_checks,
        "wedge_checks": wedge_checks,
        "shell3_controls": len(controls),
        "cubic_scalars": [item["cubic_scalar"] for item in controls],
        "control_replay_sha256": control_hash,
    }


def main() -> None:
    result = verify()
    print(f"targets_rank_five={result['targets_rank_five']}")
    print(f"invariant_basis_checks={result['invariant_basis_checks']}")
    print(
        "channel_convention_checks="
        f"{result['channel_convention_checks']}"
    )
    print(f"wedge_checks={result['wedge_checks']}")
    print(f"shell3_controls={result['shell3_controls']}")
    print(
        "cubic_scalars="
        + ",".join(str(value) for value in result["cubic_scalars"])
    )
    print(f"control_replay_sha256={result['control_replay_sha256']}")
    print("PASS: cubic characteristic-37 gate replayed")
    print("STATUS: six fixed controls excluded; shell remains open")


if __name__ == "__main__":
    main()
