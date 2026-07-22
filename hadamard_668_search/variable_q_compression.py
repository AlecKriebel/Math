#!/usr/bin/env python3
"""Exact factor-14 compression for the ``BS(84,83)`` search.

Pad each length-83 sequence with one trailing zero and regard all four
sequences as periodic sequences of length 84.  Compression modulo 6 maps a
length-84 vector ``x`` to

    X_j = sum(x[j + 6*t] for t in range(14)),  0 <= j < 6.

For an exact base sequence the four compressed periodic autocorrelations
sum to ``(334, 0, 0, 0)`` at lags 0, 1, 2, and 3.  This module enumerates the
compressed vectors compatible with a margin shard and performs the exact
four-way signature join.  It is a necessary-condition engine: a surviving
compressed quadruple is not itself a base sequence.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from collections.abc import Iterable, Sequence
from functools import lru_cache
import json
from pathlib import Path

from variable_q_base import LONG, MARGIN_SHARDS, SHORT


PERIOD = 84
COMPRESSED_LENGTH = 6
ENERGY = 2 * (LONG + SHORT)
TARGET_SIGNATURE = (ENERGY, 0, 0, 0)


def pad_to_period(sequence: Sequence[int]) -> tuple[int, ...]:
    """Return a length-84 vector, appending the distinguished zero if needed."""

    values = tuple(sequence)
    if len(values) == PERIOD:
        return values
    if len(values) == SHORT:
        return values + (0,)
    raise ValueError(f"expected length {SHORT} or {PERIOD}, got {len(values)}")


def compress_modulo_six(sequence: Sequence[int]) -> tuple[int, ...]:
    """Compress a length-84 vector along the 14 cosets modulo six."""

    values = pad_to_period(sequence)
    return tuple(sum(values[residue::COMPRESSED_LENGTH]) for residue in range(6))


def periodic_autocorrelation(sequence: Sequence[int], lag: int) -> int:
    values = tuple(sequence)
    if not values:
        raise ValueError("periodic autocorrelation needs a nonempty sequence")
    lag %= len(values)
    return sum(value * values[(index + lag) % len(values)] for index, value in enumerate(values))


def compressed_signature(vector: Sequence[int]) -> tuple[int, int, int, int]:
    """Return the independent length-six PAF values at lags 0 through 3."""

    values = tuple(vector)
    if len(values) != COMPRESSED_LENGTH:
        raise ValueError("compressed vector must have length six")
    return tuple(periodic_autocorrelation(values, lag) for lag in range(4))  # type: ignore[return-value]


def compressed_psds(signature: Sequence[int]) -> tuple[int, int, int, int]:
    """Return the four distinct Fourier powers of a real length-six vector."""

    if len(signature) != 4:
        raise ValueError("compressed signature must have four entries")
    p0, p1, p2, p3 = signature
    return (
        p0 + 2 * p1 + 2 * p2 + p3,
        p0 + p1 - p2 - p3,
        p0 - p1 - p2 + p3,
        p0 - 2 * p1 + 2 * p2 - p3,
    )


def compression_identity(sequence: Sequence[int]) -> tuple[int, ...]:
    """Check the periodic compression theorem and return its common side."""

    values = pad_to_period(sequence)
    compressed = compress_modulo_six(values)
    left = tuple(periodic_autocorrelation(compressed, lag) for lag in range(6))
    right = tuple(
        sum(periodic_autocorrelation(values, lag + 6 * multiple) for multiple in range(14))
        for lag in range(6)
    )
    if left != right:
        raise AssertionError("factor-14 periodic compression identity failed")
    return left


def cell_alphabets(length: int) -> tuple[tuple[int, ...], ...]:
    """Return the exact integer alphabet of each compressed residue cell."""

    even = tuple(range(-14, 15, 2))
    if length == LONG:
        return (even,) * 6
    if length == SHORT:
        # Index 83 is the appended zero and lies in residue class 5.
        odd = tuple(range(-13, 14, 2))
        return (even,) * 5 + (odd,)
    raise ValueError(f"length must be {LONG} or {SHORT}")


def _triples_with_sum(
    alphabets: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]],
    target: int,
) -> tuple[tuple[int, int, int], ...]:
    last_values = set(alphabets[2])
    result = []
    for first in alphabets[0]:
        for second in alphabets[1]:
            third = target - first - second
            if third in last_values:
                result.append((first, second, third))
    return tuple(result)


@lru_cache(maxsize=None)
def compression_candidates(
    length: int,
    ordinary_sum: int,
    alternating_sum: int,
) -> tuple[tuple[int, ...], ...]:
    """Enumerate all individually admissible compressed vectors.

    The alphabets and two margins are exact.  The PAF energy and Fourier
    bounds are necessary because four nonnegative contributions must total
    ``334`` in an exact complementary quadruple.
    """

    alphabets = cell_alphabets(length)
    if (ordinary_sum + alternating_sum) % 2:
        return ()
    even_target = (ordinary_sum + alternating_sum) // 2
    odd_target = (ordinary_sum - alternating_sum) // 2
    even = _triples_with_sum((alphabets[0], alphabets[2], alphabets[4]), even_target)
    odd = _triples_with_sum((alphabets[1], alphabets[3], alphabets[5]), odd_target)

    result = []
    for x0, x2, x4 in even:
        for x1, x3, x5 in odd:
            vector = (x0, x1, x2, x3, x4, x5)
            signature = compressed_signature(vector)
            if signature[0] > ENERGY:
                continue
            psds = compressed_psds(signature)
            if any(value < 0 or value > ENERGY for value in psds):
                continue
            # Frequencies zero and three are fixed by the selected margins.
            if psds[0] != ordinary_sum * ordinary_sum:
                raise AssertionError("ordinary compressed PSD mismatch")
            if psds[3] != alternating_sum * alternating_sum:
                raise AssertionError("alternating compressed PSD mismatch")
            result.append(vector)
    return tuple(result)


def signature_counts(candidates: Iterable[Sequence[int]]) -> Counter[tuple[int, ...]]:
    return Counter(compressed_signature(candidate) for candidate in candidates)


def add_signatures(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def subtract_signature(total: Sequence[int], part: Sequence[int]) -> tuple[int, ...]:
    return tuple(a - b for a, b in zip(total, part, strict=True))


def shard_compression_analysis(shard_index: int) -> dict[str, object]:
    """Perform the exact factor-14 signature join for one margin shard."""

    if not 0 <= shard_index < len(MARGIN_SHARDS):
        raise ValueError(f"shard must be in 0..{len(MARGIN_SHARDS) - 1}")
    ordinary, alternating = MARGIN_SHARDS[shard_index]
    lengths = (LONG, LONG, SHORT, SHORT)
    candidate_sets = tuple(
        compression_candidates(length, row_sum, alt_sum)
        for length, row_sum, alt_sum in zip(lengths, ordinary, alternating, strict=True)
    )
    counts = tuple(signature_counts(candidates) for candidates in candidate_sets)

    pair_maps: list[dict[tuple[int, ...], list[tuple[tuple[int, ...], tuple[int, ...]]]]] = []
    for left_counts, right_counts in ((counts[0], counts[1]), (counts[2], counts[3])):
        pairs: dict[
            tuple[int, ...], list[tuple[tuple[int, ...], tuple[int, ...]]]
        ] = defaultdict(list)
        for left in left_counts:
            for right in right_counts:
                pairs[add_signatures(left, right)].append((left, right))
        pair_maps.append(dict(pairs))

    ab_pairs, cd_pairs = pair_maps
    matching_sums = []
    signature_quadruples = 0
    compressed_quadruples = 0
    surviving: list[set[tuple[int, ...]]] = [set() for _ in range(4)]
    for ab_sum, ab_list in ab_pairs.items():
        cd_sum = subtract_signature(TARGET_SIGNATURE, ab_sum)
        cd_list = cd_pairs.get(cd_sum)
        if cd_list is None:
            continue
        matching_sums.append(ab_sum)
        signature_quadruples += len(ab_list) * len(cd_list)
        ab_weight = sum(counts[0][left] * counts[1][right] for left, right in ab_list)
        cd_weight = sum(counts[2][left] * counts[3][right] for left, right in cd_list)
        compressed_quadruples += ab_weight * cd_weight
        for left, right in ab_list:
            surviving[0].add(left)
            surviving[1].add(right)
        for left, right in cd_list:
            surviving[2].add(left)
            surviving[3].add(right)

    return {
        "shard": shard_index,
        "ordinary_sums": ordinary,
        "alternating_sums": alternating,
        "candidate_counts": tuple(len(candidates) for candidates in candidate_sets),
        "signature_counts": tuple(len(count) for count in counts),
        "pair_sum_counts": (len(ab_pairs), len(cd_pairs)),
        "matching_pair_sum_count": len(matching_sums),
        "signature_quadruple_count": signature_quadruples,
        "compressed_quadruple_count": compressed_quadruples,
        "surviving_signature_counts": tuple(len(values) for values in surviving),
        "compression_feasible": bool(matching_sums),
    }


def self_test() -> None:
    # Deterministic nonsymmetric values exercise every original coordinate.
    long = tuple(1 if (19 * index + 3) % 31 < 16 else -1 for index in range(LONG))
    short = tuple(1 if (23 * index + 7) % 37 < 18 else -1 for index in range(SHORT))
    compression_identity(long)
    compression_identity(short)

    for length, sequence in ((LONG, long), (SHORT, short)):
        compressed = compress_modulo_six(sequence)
        if sum(compressed) != sum(sequence):
            raise AssertionError("ordinary margin was not preserved")
        alternating = sum(value if index % 2 == 0 else -value for index, value in enumerate(sequence))
        compressed_alternating = sum(
            value if index % 2 == 0 else -value for index, value in enumerate(compressed)
        )
        if compressed_alternating != alternating:
            raise AssertionError("alternating margin was not preserved")
        alphabets = cell_alphabets(length)
        if any(value not in alphabet for value, alphabet in zip(compressed, alphabets, strict=True)):
            raise AssertionError("compressed value is outside its exact alphabet")

    signature = compressed_signature((1, 2, 3, 4, 5, 6))
    if compressed_psds(signature) != (21 * 21, 36, 12, 9):
        raise AssertionError("length-six Fourier formulas failed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shard", type=int, default=235)
    parser.add_argument("--all-shards", action="store_true")
    parser.add_argument("--output", type=Path, help="optional JSON report")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        self_test()
        print("PASS factor-14 compression identity and Fourier formulas")
    shards = range(len(MARGIN_SHARDS)) if args.all_shards else (args.shard,)
    analyses = [shard_compression_analysis(shard) for shard in shards]
    payload: object = analyses if args.all_shards else analyses[0]
    rendered = json.dumps(payload, indent=2)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
