#!/usr/bin/env python3
"""Well-founded rank for one finite target-following episode.

There is no global flag-cycle problem in the final proof.  The only active
rank is the number of designated edges remaining.  A designated event lowers
it by one; any other event terminates the episode.
"""
from __future__ import annotations


def next_rank(current: int, designated_fired: bool) -> int | None:
    if current < 0:
        raise ValueError("rank must be nonnegative")
    if not designated_fired:
        return None
    if current == 0:
        return None
    return current - 1


def verify_well_founded(length: int) -> None:
    rank = length
    seen = []
    while rank is not None:
        seen.append(rank)
        rank = next_rank(rank, True)
    if seen != list(range(length, -1, -1)):
        raise AssertionError("rank did not decrease exactly")


def self_test() -> None:
    verify_well_founded(7)
    assert next_rank(5, False) is None


if __name__ == "__main__":
    self_test()
    print("regime_rank.py self-test: OK")
