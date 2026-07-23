#!/usr/bin/env python3
"""Exact small-neighborhood scanner for parity-feasible ``BS(84,83)`` states.

The variable-q local engine preserves four ordinary sums, four alternating
sums, and (in its parity mode) the 83 endpoint-product equations.  Relative
to a parity-feasible checkpoint, every same-margin candidate at Hamming
distance ``2*r`` is a union of ``r`` disjoint sign exchanges inside the eight
sequence/parity classes.  The endpoint equations give an 83-bit linear
syndrome for each exchange.

This module exhaustively enumerates the zero-syndrome unions for ``r <= 3``,
deduplicates the resulting sign vectors, and evaluates their exact integer
correlation energy.  It is a bounded proof procedure, not a global search.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Sequence

from variable_q_base import LONG, SHORT, base_correlations
from verify_variable_q import extract_candidate


LENGTHS = (LONG, LONG, SHORT, SHORT)
LAST_LAG = LONG - 1
FlipKey = tuple[int, int, int, int]


@dataclass(frozen=True)
class Exchange:
    """One margin-preserving exchange of unlike signs."""

    which: int
    positive: int
    negative: int
    syndrome: int
    delta: tuple[int, ...]


@dataclass(frozen=True)
class DistanceResult:
    exchanges: int
    candidates: int
    minimum_energy: int
    minimizers: int
    best_key: FlipKey


@dataclass(frozen=True)
class NeighborhoodResult:
    initial_energy: int
    distances: tuple[DistanceResult, ...]

    @property
    def best_positive_energy(self) -> int:
        return min(result.minimum_energy for result in self.distances)

    @property
    def exact_found(self) -> bool:
        return self.best_positive_energy == 0

    @property
    def strict_local_minimum(self) -> bool:
        return self.initial_energy < self.best_positive_energy


def immutable_base(
    sequences: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    if len(sequences) != 4:
        raise ValueError("exactly four sequences are required")
    result = tuple(tuple(sequence) for sequence in sequences)
    if tuple(map(len, result)) != LENGTHS:
        raise ValueError(f"sequence lengths must be {LENGTHS}")
    if any(value not in (-1, 1) for sequence in result for value in sequence):
        raise ValueError("all entries must be signs")
    return result  # type: ignore[return-value]


def half_residuals(sequences: Sequence[Sequence[int]]) -> tuple[int, ...]:
    """Return one half of every positive-lag base correlation."""

    values = base_correlations(*immutable_base(sequences))[1:]
    if any(value % 2 for value in values):
        raise AssertionError("base correlations should all be even")
    return tuple(value // 2 for value in values)


def flip_delta(
    sequence: Sequence[int], flipped: Iterable[int], last_lag: int = LAST_LAG
) -> tuple[int, ...]:
    """Exact change in half-correlations caused by flipping coordinates.

    Only edges with exactly one flipped endpoint change sign.  Dividing their
    correlation change by two leaves minus the original endpoint product.
    Entry zero is retained for convenient lag indexing.
    """

    flipped_set = frozenset(flipped)
    if any(not 0 <= position < len(sequence) for position in flipped_set):
        raise ValueError("flipped coordinate is out of range")
    result = [0] * (last_lag + 1)
    for position in flipped_set:
        for other in range(len(sequence)):
            if other in flipped_set:
                continue
            lag = abs(position - other)
            if 0 < lag <= last_lag:
                result[lag] -= sequence[position] * sequence[other]
    return tuple(result)


def delta_syndrome(delta: Sequence[int]) -> int:
    """Pack the parities of positive-lag half-correlation changes."""

    return sum((value & 1) << (lag - 1) for lag, value in enumerate(delta) if lag)


def legal_exchanges(sequences: Sequence[Sequence[int]]) -> tuple[Exchange, ...]:
    """List every exchange preserving ordinary and alternating margins."""

    base = immutable_base(sequences)
    result = []
    for which, sequence in enumerate(base):
        for parity in (0, 1):
            positive = tuple(
                index
                for index in range(parity, len(sequence), 2)
                if sequence[index] == 1
            )
            negative = tuple(
                index
                for index in range(parity, len(sequence), 2)
                if sequence[index] == -1
            )
            for left in positive:
                for right in negative:
                    delta = flip_delta(sequence, (left, right))
                    result.append(
                        Exchange(
                            which,
                            left,
                            right,
                            delta_syndrome(delta),
                            delta,
                        )
                    )
    return tuple(result)


def exchange_union(exchanges: Sequence[Exchange]) -> FlipKey | None:
    """Return the union's four flip masks, or ``None`` if endpoints overlap."""

    masks = [0, 0, 0, 0]
    for exchange in exchanges:
        bit_pair = (1 << exchange.positive) | (1 << exchange.negative)
        if masks[exchange.which] & bit_pair:
            return None
        masks[exchange.which] |= bit_pair
    return tuple(masks)  # type: ignore[return-value]


def zero_syndrome_flip_keys(
    sequences: Sequence[Sequence[int]], exchanges: int
) -> tuple[FlipKey, ...]:
    """Enumerate distinct zero-syndrome vectors made from 1--3 exchanges.

    Completeness follows because any same-margin vector pairs its flipped
    ``+1`` and ``-1`` positions independently inside each sequence/parity
    class.  The syndrome of a disjoint union is the XOR of its exchanges.
    """

    if exchanges not in (1, 2, 3):
        raise ValueError("the exact enumerator supports 1, 2, or 3 exchanges")
    swaps = legal_exchanges(sequences)
    return tuple(sorted(_zero_syndrome_representatives(swaps, exchanges)))


def _zero_syndrome_representatives(
    swaps: Sequence[Exchange], exchanges: int
) -> dict[FlipKey, tuple[Exchange, ...]]:
    """Map every final flip vector to one exchange decomposition."""

    if exchanges not in (1, 2, 3):
        raise ValueError("the exact enumerator supports 1, 2, or 3 exchanges")
    buckets: dict[int, list[int]] = defaultdict(list)
    for index, swap in enumerate(swaps):
        buckets[swap.syndrome].append(index)

    representatives: dict[FlipKey, tuple[Exchange, ...]] = {}
    if exchanges == 1:
        for index in buckets.get(0, ()):
            decomposition = (swaps[index],)
            key = exchange_union(decomposition)
            assert key is not None
            representatives.setdefault(key, decomposition)
    elif exchanges == 2:
        for bucket in buckets.values():
            for ordinal, left in enumerate(bucket):
                for right in bucket[ordinal + 1 :]:
                    decomposition = (swaps[left], swaps[right])
                    key = exchange_union(decomposition)
                    if key is not None:
                        representatives.setdefault(key, decomposition)
    else:
        for left, first in enumerate(swaps):
            for middle in range(left + 1, len(swaps)):
                target = first.syndrome ^ swaps[middle].syndrome
                for right in buckets.get(target, ()):
                    if right <= middle:
                        continue
                    decomposition = (first, swaps[middle], swaps[right])
                    key = exchange_union(decomposition)
                    if key is not None:
                        representatives.setdefault(key, decomposition)
    return representatives


def exchange_union_delta(
    sequences: Sequence[Sequence[int]], exchanges: Sequence[Exchange]
) -> tuple[int, ...]:
    """Combine precomputed exchange deltas, including quadratic cross terms."""

    base = immutable_base(sequences)
    if exchange_union(exchanges) is None:
        raise ValueError("exchange endpoints overlap")
    return _exchange_union_delta(base, exchanges)


def _exchange_union_delta(
    base: tuple[tuple[int, ...], ...], exchanges: Sequence[Exchange]
) -> tuple[int, ...]:
    result = [0] * (LAST_LAG + 1)
    for exchange in exchanges:
        for lag in range(1, LAST_LAG + 1):
            result[lag] += exchange.delta[lag]
    # Each individual delta treats the endpoints of every other exchange as
    # unflipped.  If two exchanges lie in the same sequence, their cross edge
    # was therefore changed twice in the sum but is unchanged in the union.
    for ordinal, left in enumerate(exchanges):
        for right in exchanges[ordinal + 1 :]:
            if left.which != right.which:
                continue
            sequence = base[left.which]
            for first in (left.positive, left.negative):
                for second in (right.positive, right.negative):
                    lag = abs(first - second)
                    result[lag] += 2 * sequence[first] * sequence[second]
    return tuple(result)


def apply_flip_key(
    sequences: Sequence[Sequence[int]], key: FlipKey
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    base = immutable_base(sequences)
    if len(key) != 4:
        raise ValueError("a flip key must contain four masks")
    if any(
        mask < 0 or mask >> len(sequence)
        for mask, sequence in zip(key, base, strict=True)
    ):
        raise ValueError("flip mask is out of range")
    return tuple(
        tuple(
            -value if (mask >> index) & 1 else value
            for index, value in enumerate(sequence)
        )
        for sequence, mask in zip(base, key, strict=True)
    )  # type: ignore[return-value]


def key_delta(
    sequences: Sequence[Sequence[int]], key: FlipKey
) -> tuple[int, ...]:
    """Compute a flip key's exact half-correlation delta."""

    base = immutable_base(sequences)
    result = [0] * (LAST_LAG + 1)
    for which, mask in enumerate(key):
        positions = tuple(
            index for index in range(len(base[which])) if (mask >> index) & 1
        )
        delta = flip_delta(base[which], positions)
        for lag in range(1, LAST_LAG + 1):
            result[lag] += delta[lag]
    return tuple(result)


def scan_neighborhood(
    sequences: Sequence[Sequence[int]], max_exchanges: int = 3
) -> NeighborhoodResult:
    """Exactly minimize half-correlation energy through ``max_exchanges``."""

    if not 1 <= max_exchanges <= 3:
        raise ValueError("max_exchanges must be in 1..3")
    base = immutable_base(sequences)
    residual = half_residuals(base)
    if any(value & 1 for value in residual):
        raise ValueError("the starting candidate is not endpoint-parity feasible")
    initial_energy = sum(value * value for value in residual)
    swaps = legal_exchanges(base)
    distances = []
    for count in range(1, max_exchanges + 1):
        representatives = _zero_syndrome_representatives(swaps, count)
        if not representatives:
            raise ValueError(f"no zero-syndrome candidates at exchange count {count}")
        best_energy: int | None = None
        best_key: FlipKey | None = None
        minimizers = 0
        for key, decomposition in representatives.items():
            delta = _exchange_union_delta(base, decomposition)[1:]
            energy = sum(
                (value + change) * (value + change)
                for value, change in zip(residual, delta, strict=True)
            )
            if best_energy is None or energy < best_energy:
                best_energy = energy
                best_key = key
                minimizers = 1
            elif energy == best_energy:
                minimizers += 1
        assert best_energy is not None and best_key is not None
        distances.append(
            DistanceResult(
                count,
                len(representatives),
                best_energy,
                minimizers,
                best_key,
            )
        )
    return NeighborhoodResult(initial_energy, tuple(distances))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--max-exchanges", type=int, choices=(1, 2, 3), default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw = args.candidate.read_bytes()
    payload: Any = json.loads(raw)
    a, b, c, d, _s, _q = extract_candidate(payload)
    result = scan_neighborhood((a, b, c, d), args.max_exchanges)
    print(f"candidate={args.candidate}")
    print(f"sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"initial_energy_half={result.initial_energy}")
    for distance in result.distances:
        print(
            f"exchanges={distance.exchanges} "
            f"hamming_distance={2 * distance.exchanges} "
            f"candidates={distance.candidates} "
            f"minimum_energy_half={distance.minimum_energy} "
            f"minimizers={distance.minimizers}"
        )
    print(f"best_positive_energy_half={result.best_positive_energy}")
    print(f"strict_local_minimum={str(result.strict_local_minimum).lower()}")
    print(f"exact_found={str(result.exact_found).lower()}")
    # A completed negative bounded scan is still a successful invocation.
    # ``exact_found`` is reported explicitly and is not encoded in the status.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
