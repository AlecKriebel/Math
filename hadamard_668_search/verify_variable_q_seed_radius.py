#!/usr/bin/env python3
"""Dependency-free proof that Eliahou's seed has no exact BS neighbor at r<=8."""

from __future__ import annotations

from itertools import product

from seed import ELIAHOU_Q, ELIAHOU_S
from variable_q_base import (
    MARGIN_SHARDS,
    alternating_sum,
    base_quad_products,
    sign_sum,
    special_to_base,
)


SEED = special_to_base(ELIAHOU_S, ELIAHOU_Q)


def raw_margin_images():
    for shard, (ordinary, alternating) in enumerate(MARGIN_SHARDS):
        for swap_long, swap_short in product((False, True), repeat=2):
            order = [0, 1, 2, 3]
            if swap_long:
                order[0], order[1] = order[1], order[0]
            if swap_short:
                order[2], order[3] = order[3], order[2]
            pairs = [(ordinary[index], alternating[index]) for index in order]
            for negations in product((-1, 1), repeat=4):
                signed = [
                    (row_sum * sign, alt_sum * sign)
                    for (row_sum, alt_sum), sign in zip(
                        pairs, negations, strict=True
                    )
                ]
                for reverse_a, reverse_b in product((-1, 1), repeat=2):
                    raw = signed.copy()
                    raw[0] = (raw[0][0], raw[0][1] * reverse_a)
                    raw[1] = (raw[1][0], raw[1][1] * reverse_b)
                    yield shard, tuple(raw)


def distance_to_margins(target: tuple[tuple[int, int], ...]) -> int:
    current = tuple(
        (sign_sum(sequence), alternating_sum(sequence)) for sequence in SEED
    )
    return sum(
        (
            abs((row_sum + alt_sum) - (current_row + current_alt))
            + abs((row_sum - alt_sum) - (current_row - current_alt))
        )
        // 4
        for (row_sum, alt_sum), (current_row, current_alt) in zip(
            target, current, strict=True
        )
    )


def verify() -> None:
    best = 10**9
    witnesses: set[tuple[int, tuple[tuple[int, int], ...]]] = set()
    for shard, margins in raw_margin_images():
        distance = distance_to_margins(margins)
        record = shard, margins
        if distance < best:
            best = distance
            witnesses = {record}
        elif distance == best:
            witnesses.add(record)
    expected = {
        (287, ((-18, 18), (0, 0), (3, 1), (-1, -3)))
    }
    if best != 8 or witnesses != expected:
        raise AssertionError(
            f"unexpected margin-distance result: distance={best}, witnesses={witnesses}"
        )

    long_products, short_products = base_quad_products(*SEED)
    if long_products != (-1,) + (1,) * 41 or short_products != (1,) * 41:
        raise AssertionError("published seed should already satisfy all BS quad products")

    # The unique minimum changes only A's odd-coordinate sum, from -2 to -18.
    # Hence it flips eight currently positive odd A coordinates and no others.
    # Every long endpoint pair {j,83-j} has exactly one odd coordinate, so
    # these eight distinct flips toggle eight already-correct quad products.
    target = next(iter(expected))[1]
    current_a_odd = (sign_sum(SEED[0]) - alternating_sum(SEED[0])) // 2
    target_a_odd = (target[0][0] - target[0][1]) // 2
    if current_a_odd != -2 or target_a_odd != -18:
        raise AssertionError("unexpected A odd-class sums")
    if (current_a_odd - target_a_odd) // 2 != 8:
        raise AssertionError("the minimum should require eight positive-to-negative flips")
    odd_positions = tuple(range(1, len(SEED[0]), 2))
    if len({min(index, 83 - index) for index in odd_positions}) != 42:
        raise AssertionError("odd A coordinates should occupy distinct long quads")


def main() -> None:
    verify()
    print("PASS: exhaustive raw margin images have minimum seed distance 8")
    print("PASS: the unique distance-8 margin pattern breaks BS quad parity")
    print("RESULT: no exact BS(84,83) lies within distance 8 of Eliahou's seed")


if __name__ == "__main__":
    main()
