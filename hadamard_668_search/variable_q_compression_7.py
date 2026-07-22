#!/usr/bin/env python3
"""Exact factor-12 (compressed-length-7) invariants for ``BS(84,83)``.

The length-83 sequences are padded by a trailing zero and all four sequences
are treated periodically at length 84.  Compression modulo seven exposes the
primitive seventh roots of unity, which are not present in the order-3,
order-4, and order-6 spectral constraints.

This is a necessary-condition layer, not a construction of a base sequence.
The explicit witnesses below prove that the compression alone eliminates no
margin shard.
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable, Sequence
from itertools import product

from variable_q_base import LONG, MARGIN_SHARDS, ROW_SUM_PROFILES, SHORT
from variable_q_compression import pad_to_period, periodic_autocorrelation


PERIOD = 84
FACTOR = 12
COMPRESSED_LENGTH = 7
ENERGY = 2 * (LONG + SHORT)
TARGET_SIGNATURE = (ENERGY, 0, 0, 0)

EVEN_CELL_VALUES = tuple(range(-12, 13, 2))
ODD_CELL_VALUES = tuple(range(-11, 12, 2))


def compress_modulo_seven(sequence: Sequence[int]) -> tuple[int, ...]:
    """Compress a length-84 vector along its 12 cosets modulo seven."""

    values = pad_to_period(sequence)
    return tuple(
        sum(values[residue::COMPRESSED_LENGTH])
        for residue in range(COMPRESSED_LENGTH)
    )


def compressed_signature_seven(vector: Sequence[int]) -> tuple[int, int, int, int]:
    """Return the independent length-seven PAF values at lags 0 through 3."""

    values = tuple(vector)
    if len(values) != COMPRESSED_LENGTH:
        raise ValueError("compressed vector must have length seven")
    return tuple(periodic_autocorrelation(values, lag) for lag in range(4))  # type: ignore[return-value]


def factor12_compression_identity(sequence: Sequence[int]) -> tuple[int, ...]:
    """Check the factor-12 periodic compression theorem exactly."""

    values = pad_to_period(sequence)
    compressed = compress_modulo_seven(values)
    left = tuple(
        periodic_autocorrelation(compressed, lag)
        for lag in range(COMPRESSED_LENGTH)
    )
    right = tuple(
        sum(
            periodic_autocorrelation(values, lag + COMPRESSED_LENGTH * multiple)
            for multiple in range(FACTOR)
        )
        for lag in range(COMPRESSED_LENGTH)
    )
    if left != right:
        raise AssertionError("factor-12 periodic compression identity failed")
    return left


def factor12_cell_alphabets(length: int) -> tuple[tuple[int, ...], ...]:
    """Return the exact alphabet of each length-seven compressed cell."""

    if length == LONG:
        return (EVEN_CELL_VALUES,) * COMPRESSED_LENGTH
    if length == SHORT:
        # The appended index 83 is 6 modulo 7.  That cell contains eleven
        # signs and the distinguished zero; the other cells contain twelve.
        return (EVEN_CELL_VALUES,) * 6 + (ODD_CELL_VALUES,)
    raise ValueError(f"length must be {LONG} or {SHORT}")


def within_cell_alternating_sums(
    length: int, residue: int, cell_sum: int
) -> tuple[int, ...]:
    """Return all internal alternating sums realizing one compressed cell.

    Since seven is odd, the sign of an original coordinate alternates as one
    moves through a residue cell.  Cells with twelve signs split into six
    even-``t`` and six odd-``t`` signs.  The last short cell splits 6 versus 5.
    """

    alphabets = factor12_cell_alphabets(length)
    if not 0 <= residue < COMPRESSED_LENGTH:
        raise ValueError("residue must be in 0..6")
    if cell_sum not in alphabets[residue]:
        return ()
    even_count = 6
    odd_count = 5 if length == SHORT and residue == 6 else 6
    even_sums = range(-even_count, even_count + 1, 2)
    odd_sums = range(-odd_count, odd_count + 1, 2)
    return tuple(
        sorted(
            {
                even_sum - odd_sum
                for even_sum in even_sums
                for odd_sum in odd_sums
                if even_sum + odd_sum == cell_sum
            }
        )
    )


def alternating_margin_liftable(
    vector: Sequence[int], length: int, target: int
) -> bool:
    """Decide exactly whether a compressed vector can realize margin ``T``."""

    values = tuple(vector)
    if len(values) != COMPRESSED_LENGTH:
        raise ValueError("compressed vector must have length seven")
    attainable = {0}
    for residue, cell_sum in enumerate(values):
        internal = within_cell_alternating_sums(length, residue, cell_sum)
        if not internal:
            return False
        sign = 1 if residue % 2 == 0 else -1
        attainable = {
            partial + sign * contribution
            for partial in attainable
            for contribution in internal
        }
    return target in attainable


def add_signatures(*signatures: Sequence[int]) -> tuple[int, ...]:
    if not signatures:
        raise ValueError("at least one signature is required")
    if any(len(signature) != 4 for signature in signatures):
        raise ValueError("every signature must have four entries")
    return tuple(sum(signature[index] for signature in signatures) for index in range(4))


def _conjugate_elementary_symmetric(
    constant: int, linear: int, quadratic: int
) -> tuple[int, int, int]:
    """Elementary symmetric values over roots of ``t^3+t^2-2t-1``."""

    a = constant
    b = linear
    c = quadratic
    first = 3 * a - b + 5 * c
    sum_of_squares = (
        3 * a * a
        + 5 * b * b
        + 13 * c * c
        - 2 * a * b
        + 10 * a * c
        - 8 * b * c
    )
    numerator = first * first - sum_of_squares
    if numerator % 2:
        raise AssertionError("nonintegral conjugate pair sum")
    second = numerator // 2

    # Determinant of multiplication by a+b*t+c*t^2 in the basis 1,t,t^2.
    m00, m01, m02 = a, c, b - c
    m10, m11, m12 = b, a + 2 * c, 2 * b - c
    m20, m21, m22 = c, b - c, a - b + 3 * c
    third = (
        m00 * (m11 * m22 - m12 * m21)
        - m01 * (m10 * m22 - m12 * m20)
        + m02 * (m10 * m21 - m11 * m20)
    )
    return first, second, third


def primitive_seven_psds_within_bound(
    signature: Sequence[int], bound: int = ENERGY
) -> bool:
    """Test ``0 <= PSD <= bound`` at all primitive seventh roots exactly.

    If ``t=2*cos(2*pi/7)``, its three conjugates satisfy
    ``t^3+t^2-2*t-1=0``.  The PSD represented by ``(p0,p1,p2,p3)`` reduces to
    ``a+b*t+c*t^2``.  Three real conjugates are all nonnegative exactly when
    their three elementary symmetric functions are nonnegative.
    """

    if len(signature) != 4:
        raise ValueError("compressed signature must have four entries")
    p0, p1, p2, p3 = signature
    a = p0 - 2 * p2 + p3
    b = p1 - p3
    c = p2 - p3
    lower = _conjugate_elementary_symmetric(a, b, c)
    upper = _conjugate_elementary_symmetric(bound - a, -b, -c)
    return all(value >= 0 for value in (*lower, *upper))


# One exact compressed quadruple for each of the 12 ordinary row-sum profiles.
# Each was found by the 28-cell CP model and is verified independently below.
ORDINARY_PROFILE_WITNESSES: dict[
    tuple[int, int, int, int], tuple[tuple[int, ...], ...]
] = {
    (4, 2, 17, 5): (
        (-2, 4, -2, 2, -2, 4, 0),
        (-6, -2, 2, 0, 4, 2, 2),
        (0, -4, 10, 4, 2, 2, 3),
        (-6, 0, 0, 2, 2, 4, 3),
    ),
    (6, 0, 17, 3): (
        (-4, 0, 2, 2, 2, 2, 2),
        (-8, 0, 0, 2, 2, 2, 2),
        (0, 0, 10, 2, 2, 2, 1),
        (-8, 2, 2, -2, 4, 2, 3),
    ),
    (8, 6, 15, 3): (
        (2, 0, 2, -10, 6, 6, 2),
        (-6, 2, 2, 2, 2, 2, 2),
        (4, 2, 2, 2, 2, 2, 1),
        (0, -6, 2, 2, 2, 2, 1),
    ),
    (10, 0, 15, 3): (
        (4, -6, 0, 6, 2, 4, 0),
        (-8, 0, 4, 0, 0, 2, 2),
        (0, 6, 4, 2, 2, -2, 3),
        (0, -6, 4, 2, 2, 2, -1),
    ),
    (10, 4, 13, 7): (
        (0, 0, 0, 2, 6, 0, 2),
        (-2, -2, 10, 2, 0, -2, -2),
        (4, 2, 2, 0, 2, 2, 1),
        (2, -2, 8, -6, -2, 4, 3),
    ),
    (10, 8, 11, 7): (
        (4, 12, -8, -2, 0, 2, 2),
        (-4, 2, 2, 2, 2, 2, 2),
        (4, -2, 2, 2, 2, 2, 1),
        (0, -2, 2, 2, 2, 2, 1),
    ),
    (10, 8, 13, 1): (
        (2, -6, 0, 4, 2, 6, 2),
        (-4, 2, 2, 2, 2, 2, 2),
        (-4, 2, 6, 2, 4, -2, 5),
        (-8, 2, 4, 0, 0, 2, 1),
    ),
    (12, 10, 9, 3): (
        (-2, 4, 4, -6, 4, 2, 6),
        (4, -2, -2, 0, 8, -2, 4),
        (0, -2, -2, 4, 4, 4, 1),
        (-4, 0, 0, 2, 2, 4, -1),
    ),
    (14, 4, 11, 1): (
        (4, 4, -2, 6, 2, 0, 0),
        (-10, 2, 2, 4, 2, 2, 2),
        (0, 6, 2, 4, 0, 4, -5),
        (-2, 0, 2, 0, 2, 2, -3),
    ),
    (14, 8, 7, 5): (
        (4, 4, -10, 4, 4, 4, 4),
        (-2, 4, -4, 2, 4, 2, 2),
        (-2, 4, 2, 2, 0, 2, -1),
        (2, 0, -4, 0, 4, 2, 1),
    ),
    (16, 2, 7, 5): (
        (0, 2, -4, 4, 4, 2, 8),
        (-6, -4, 2, 4, -2, 4, 4),
        (-2, -2, 0, 4, 0, 6, 1),
        (0, 2, -4, 4, 0, 0, 3),
    ),
    (18, 0, 3, 1): (
        (4, 4, -4, 6, 2, 4, 2),
        (-8, -2, 2, 2, 2, 2, 2),
        (-8, 2, 2, 2, 2, 2, 1),
        (0, 2, -6, 2, 2, 2, -1),
    ),
}


# Exact enumeration counts after p0 <= 334 and after all primitive-seven
# PSDs are additionally required to lie in [0,334].
SIGNATURE_FILTER_COUNTS_LONG = {
    0: (27173, 4388),
    2: (50128, 7764),
    4: (47698, 7785),
    6: (47989, 7764),
    8: (44530, 7749),
    10: (43828, 7722),
    12: (39801, 7704),
    14: (23261, 4397),
    16: (33399, 7650),
    18: (31212, 7563),
}
SIGNATURE_FILTER_COUNTS_SHORT = {
    1: (338355, 52429),
    3: (333837, 52467),
    5: (326970, 52343),
    7: (180578, 28485),
    9: (301098, 52202),
    11: (283933, 52059),
    13: (264701, 51628),
    15: (241762, 51412),
    17: (220068, 51159),
}


def verify_profile_witness(
    ordinary: tuple[int, int, int, int],
    witness: Sequence[Sequence[int]],
) -> None:
    """Verify one exact compressed quadruple without trusting the CP model."""

    values = tuple(tuple(vector) for vector in witness)
    if len(values) != 4:
        raise AssertionError("a compressed witness must have four vectors")
    lengths = (LONG, LONG, SHORT, SHORT)
    for vector, length, target in zip(values, lengths, ordinary, strict=True):
        if len(vector) != COMPRESSED_LENGTH:
            raise AssertionError("compressed witness vector has wrong length")
        if sum(vector) != target:
            raise AssertionError("compressed witness has wrong ordinary sum")
        if any(
            value not in alphabet
            for value, alphabet in zip(
                vector, factor12_cell_alphabets(length), strict=True
            )
        ):
            raise AssertionError("compressed witness violates a cell alphabet")
        signature = compressed_signature_seven(vector)
        if signature[0] > ENERGY or not primitive_seven_psds_within_bound(signature):
            raise AssertionError("compressed witness violates an individual PSD bound")
    if add_signatures(*(compressed_signature_seven(vector) for vector in values)) != TARGET_SIGNATURE:
        raise AssertionError("compressed witness violates the complementary PAF target")


def verify_all_shards_survive() -> None:
    """Mechanically verify a factor-12 witness for every margin shard."""

    if set(ORDINARY_PROFILE_WITNESSES) != set(ROW_SUM_PROFILES):
        raise AssertionError("factor-12 witness table does not cover all profiles")
    for ordinary, witness in ORDINARY_PROFILE_WITNESSES.items():
        verify_profile_witness(ordinary, witness)
    lengths = (LONG, LONG, SHORT, SHORT)
    for ordinary, alternating in MARGIN_SHARDS:
        witness = ORDINARY_PROFILE_WITNESSES[ordinary]
        if not all(
            alternating_margin_liftable(vector, length, target)
            for vector, length, target in zip(
                witness, lengths, alternating, strict=True
            )
        ):
            raise AssertionError(
                f"factor-12 witness failed alternating lift for {ordinary}, {alternating}"
            )


def signature_filter_counts(length: int, ordinary_sum: int) -> tuple[int, int]:
    """Recompute one exact raw/admissible signature count (slow, bounded)."""

    alphabets = factor12_cell_alphabets(length)
    left = tuple(product(*alphabets[:3]))
    right_by_sum: dict[int, list[tuple[int, ...]]] = {}
    for right in product(*alphabets[3:]):
        right_by_sum.setdefault(sum(right), []).append(right)
    raw: set[tuple[int, ...]] = set()
    admissible: set[tuple[int, ...]] = set()
    for prefix in left:
        for suffix in right_by_sum.get(ordinary_sum - sum(prefix), ()):  # type: ignore[arg-type]
            signature = compressed_signature_seven(prefix + suffix)
            if signature[0] > ENERGY:
                continue
            raw.add(signature)
            if primitive_seven_psds_within_bound(signature):
                admissible.add(signature)
    return len(raw), len(admissible)


def self_test() -> None:
    long = tuple(1 if (19 * index + 3) % 31 < 16 else -1 for index in range(LONG))
    short = tuple(1 if (23 * index + 7) % 37 < 18 else -1 for index in range(SHORT))
    factor12_compression_identity(long)
    factor12_compression_identity(short)
    verify_all_shards_survive()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--count-length", type=int, choices=(LONG, SHORT))
    parser.add_argument("--ordinary-sum", type=int)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        self_test()
        print("PASS factor-12 compression and all 288 shard witnesses")
    if args.count_length is not None:
        if args.ordinary_sum is None:
            raise SystemExit("--count-length requires --ordinary-sum")
        print(signature_filter_counts(args.count_length, args.ordinary_sum))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
