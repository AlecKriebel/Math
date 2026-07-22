#!/usr/bin/env python3
"""Exclude a raw Hamming ball around Eliahou's seed by margins and quads.

Every exact ``BS(84,83)`` has one of the finitely enumerated ordinary and
alternating margin vectors.  Moreover, its paired-endpoint products agree
with those of Eliahou's published seed.  Consequently, the transition from
the seed to an exact base sequence flips an even number of signs in every
four-coordinate endpoint quad.

This verifier first enumerates every raw labelled margin target whose
unconstrained Hamming distance from the seed is at most ``radius``.  A small
dynamic program then computes the minimum number of flips attaining each
target while preserving all endpoint-quad products.  If none is attainable
within the radius, no exact base sequence lies in the full raw ball.  The
calculation is dependency-free apart from the repository's checked data.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Sequence

from variable_q_base import base_quad_products
from verify_variable_q_seed_radius import (
    SEED,
    distance_to_margins,
    raw_margin_images,
)


Delta = tuple[int, int, int, int]
MarginPair = tuple[int, int]
MarginTarget = tuple[MarginPair, MarginPair, MarginPair, MarginPair]


@dataclass(frozen=True)
class TargetCheck:
    shard: int
    margin_distance: int
    target: MarginTarget
    long_distance: int | None
    short_distance: int | None

    @property
    def quad_distance(self) -> int | None:
        if self.long_distance is None or self.short_distance is None:
            return None
        return self.long_distance + self.short_distance


@dataclass(frozen=True)
class RadiusCheck:
    radius: int
    long_states: int
    short_states: int
    targets: tuple[TargetCheck, ...]

    @property
    def excluded(self) -> bool:
        return all(
            record.quad_distance is None or record.quad_distance > self.radius
            for record in self.targets
        )


def coordinate_class_sums(sequence: Sequence[int]) -> tuple[int, int]:
    """Return the even-coordinate and odd-coordinate sign sums."""

    return sum(sequence[::2]), sum(sequence[1::2])


def _local_options(
    cells: Sequence[tuple[int, int]], *, require_even_cardinality: bool
) -> tuple[tuple[Delta, int], ...]:
    """Return minimum-cost margin deltas for one quad or centre pair.

    Each cell is ``(coordinate_class, seed_sign)``.  Flipping a sign ``x``
    changes half of its class sum by ``-x``.  Higher-cost masks producing the
    same local delta can be discarded because the verifier asks for a ball,
    not an exact-distance sphere.
    """

    best: dict[Delta, int] = {}
    for mask in range(1 << len(cells)):
        cost = mask.bit_count()
        if require_even_cardinality and cost % 2:
            continue
        delta = [0, 0, 0, 0]
        for index, (coordinate_class, seed_sign) in enumerate(cells):
            if mask >> index & 1:
                delta[coordinate_class] -= seed_sign
        key = tuple(delta)  # type: ignore[assignment]
        previous = best.get(key)
        if previous is None or cost < previous:
            best[key] = cost
    return tuple(sorted(best.items()))


def quad_preserving_distances(
    first: Sequence[int], second: Sequence[int], radius: int
) -> dict[Delta, int]:
    """Map four class-sum deltas to their minimum quad-preserving distance.

    The four classes are ``first-even``, ``first-odd``, ``second-even``, and
    ``second-odd``.  Paired endpoints must contain an even number of flips.
    For odd lengths, the two unpaired central coordinates are unrestricted.
    Only states of cost at most ``radius`` are retained.
    """

    if radius < 0:
        raise ValueError("radius must be nonnegative")
    if len(first) != len(second):
        raise ValueError("paired sequences must have equal lengths")
    if any(value not in (-1, 1) for value in (*first, *second)):
        raise ValueError("paired sequences must contain only signs")

    states: dict[Delta, int] = {(0, 0, 0, 0): 0}
    length = len(first)
    for left in range(length // 2):
        right = length - 1 - left
        cells = tuple(
            (sequence_offset + coordinate % 2, sequence[coordinate])
            for sequence_offset, sequence in ((0, first), (2, second))
            for coordinate in (left, right)
        )
        states = _extend_states(
            states,
            _local_options(cells, require_even_cardinality=True),
            radius,
        )

    if length % 2:
        centre = length // 2
        cells = (
            (centre % 2, first[centre]),
            (2 + centre % 2, second[centre]),
        )
        states = _extend_states(
            states,
            _local_options(cells, require_even_cardinality=False),
            radius,
        )
    return states


def _extend_states(
    states: dict[Delta, int],
    options: Sequence[tuple[Delta, int]],
    radius: int,
) -> dict[Delta, int]:
    result: dict[Delta, int] = {}
    for state, state_cost in states.items():
        for delta, option_cost in options:
            cost = state_cost + option_cost
            if cost > radius:
                continue
            target = tuple(
                value + change for value, change in zip(state, delta, strict=True)
            )
            previous = result.get(target)
            if previous is None or cost < previous:
                result[target] = cost
    return result


def target_class_delta(
    target: MarginTarget, sequence_indices: tuple[int, int]
) -> Delta:
    """Return required half-class-sum changes for two seed sequences."""

    result: list[int] = []
    for index in sequence_indices:
        ordinary, alternating = target[index]
        if (ordinary + alternating) % 2 or (ordinary - alternating) % 2:
            raise ValueError("ordinary/alternating margins have incompatible parity")
        desired = (
            (ordinary + alternating) // 2,
            (ordinary - alternating) // 2,
        )
        current = coordinate_class_sums(SEED[index])
        changes = tuple(
            wanted - present
            for wanted, present in zip(desired, current, strict=True)
        )
        if any(change % 2 for change in changes):
            raise ValueError("target class sums are unreachable by sign flips")
        result.extend(change // 2 for change in changes)
    return tuple(result)  # type: ignore[return-value]


def raw_margin_targets(radius: int) -> tuple[tuple[int, int, MarginTarget], ...]:
    """Return distinct raw margin targets with margin distance at most radius."""

    if radius < 0:
        raise ValueError("radius must be nonnegative")
    records: set[tuple[int, int, MarginTarget]] = set()
    for shard, target in raw_margin_images():
        distance = distance_to_margins(target)
        if distance <= radius:
            records.add((distance, shard, target))
    return tuple(sorted((shard, distance, target) for distance, shard, target in records))


def check_radius(radius: int) -> RadiusCheck:
    """Run the exact margin-plus-quad exclusion calculation."""

    seed_long, seed_short = base_quad_products(*SEED)
    if seed_long != (-1,) + (1,) * 41 or seed_short != (1,) * 41:
        raise AssertionError("published seed does not have the required quad products")

    long_distances = quad_preserving_distances(SEED[0], SEED[1], radius)
    short_distances = quad_preserving_distances(SEED[2], SEED[3], radius)
    records = []
    for shard, distance, target in raw_margin_targets(radius):
        records.append(
            TargetCheck(
                shard=shard,
                margin_distance=distance,
                target=target,
                long_distance=long_distances.get(target_class_delta(target, (0, 1))),
                short_distance=short_distances.get(target_class_delta(target, (2, 3))),
            )
        )
    return RadiusCheck(
        radius=radius,
        long_states=len(long_distances),
        short_states=len(short_distances),
        targets=tuple(records),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--radius", type=int, default=13)
    parser.add_argument(
        "--verbose", action="store_true", help="print every raw margin target"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.radius < 0:
        print("error=radius must be nonnegative")
        return 2
    result = check_radius(args.radius)
    print(f"radius={result.radius}")
    print(f"long_states={result.long_states}")
    print(f"short_states={result.short_states}")
    print(f"raw_margin_targets={len(result.targets)}")
    survivors = tuple(
        record
        for record in result.targets
        if record.quad_distance is not None
        and record.quad_distance <= result.radius
    )
    print(f"margin_plus_quad_survivors={len(survivors)}")
    if args.verbose:
        for record in result.targets:
            quad = record.quad_distance
            quad_text = f"{quad}" if quad is not None else f">{result.radius}"
            print(
                f"shard={record.shard} margin_distance={record.margin_distance} "
                f"quad_distance={quad_text} target={record.target}"
            )
    if result.excluded:
        print(
            "PASS: no exact BS(84,83) lies within raw Hamming distance "
            f"{result.radius} of Eliahou's published seed"
        )
        return 0
    print("INCONCLUSIVE: at least one margin-plus-quad target survives")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
