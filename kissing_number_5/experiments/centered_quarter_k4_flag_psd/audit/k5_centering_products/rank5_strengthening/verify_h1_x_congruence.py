#!/usr/bin/env python3
"""Dependency-free verifier for the exact centered H1 congruence."""

from __future__ import annotations

from itertools import product
from typing import Mapping


COLORS = tuple(range(-4, 3))


def h1_x_from_counts(counts: Mapping[int, int]) -> int:
    """Compute X after checking exact unordered-pair and centering data."""

    if set(counts) != set(COLORS):
        raise ValueError(f"counts must have exactly the colors {COLORS}")
    if any(not isinstance(counts[color], int) or counts[color] < 0 for color in COLORS):
        raise ValueError("all multiplicities must be nonnegative integers")
    if sum(counts.values()) != 820:
        raise ValueError("41 points have exactly 820 unordered pairs")
    if sum(color * counts[color] for color in COLORS) != -82:
        raise ValueError("the counts do not satisfy exact centering")
    q = sum(color * color * counts[color] for color in COLORS)
    if q % 2:
        raise AssertionError("centering should force Q even")
    x = 5 * q - 11808
    if x % 10 != 2:
        raise AssertionError("the H1 branch must be 2 modulo 10")
    return x


def verify_parity_identity() -> None:
    """Exhaust all parity vectors; no numerical or optimization dependency."""

    for parities in product((0, 1), repeat=len(COLORS)):
        centered_parity = sum(
            color * parity
            for color, parity in zip(COLORS, parities, strict=True)
        ) % 2
        q_parity = sum(
            color * color * parity
            for color, parity in zip(COLORS, parities, strict=True)
        ) % 2
        if centered_parity != q_parity:
            raise AssertionError((parities, centered_parity, q_parity))


def main() -> None:
    verify_parity_identity()
    example = dict.fromkeys(COLORS, 0)
    example[-4] = 280
    example[0] = 21
    example[2] = 519
    x = h1_x_from_counts(example)
    assert x == 20972
    assert 13 % 10 != x % 10
    print("verified: every centered quarter-grid branch has X == 2 (mod 10)")


if __name__ == "__main__":
    main()
