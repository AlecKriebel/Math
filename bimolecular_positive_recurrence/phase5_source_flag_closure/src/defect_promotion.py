#!/usr/bin/env python3
"""Finite-episode overshoot and defect-containment bounds."""
from __future__ import annotations

from typing import Sequence


def coordinate_overshoot_bound(max_molecularity: int, jump_count: int) -> int:
    if max_molecularity < 0 or jump_count < 0:
        raise ValueError("bounds must be nonnegative")
    return max_molecularity * jump_count


def verify_endpoint_bound(
    start: Sequence[int], endpoint: Sequence[int], jump_count: int, max_molecularity: int = 2
) -> None:
    bound = coordinate_overshoot_bound(max_molecularity, jump_count)
    if any(abs(a - b) > bound for a, b in zip(start, endpoint)):
        raise AssertionError("episode endpoint exceeds the deterministic overshoot bound")


def self_test() -> None:
    assert coordinate_overshoot_bound(2, 5) == 10
    verify_endpoint_bound((100, 0), (96, 4), 2)


if __name__ == "__main__":
    self_test()
    print("defect_promotion.py self-test: OK")
