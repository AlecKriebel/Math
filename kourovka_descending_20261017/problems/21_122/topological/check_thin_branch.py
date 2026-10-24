"""Exact finite checks of the non-word topological obstruction.

Uses bit zero as coordinate 1. This checks f_n compatibility and the exact
one-splitting-fiber geometry; it does not test or claim a group word example.
"""

import json
from datetime import datetime, timezone


def first_nonzero(a: int) -> int:
    return a & -a


def check(max_n: int = 15) -> dict:
    levels = []
    for n in range(1, max_n + 1):
        image = {first_nonzero(a) for a in range(1 << n)}
        expected = {0} | {1 << i for i in range(n)}
        assert image == expected
        mask = (1 << n) - 1
        image_next = {first_nonzero(a) for a in range(1 << (n + 1))}
        fibers = {y: {z for z in image_next if z & mask == y} for y in image}
        assert fibers[0] == {0, 1 << n}
        assert all(fibers[y] == {y} for y in image if y)
        assert all(
            first_nonzero(a) & mask == first_nonzero(a & mask)
            for a in range(1 << (n + 1))
        )
        # On an exponent-two group, the claimed power compatibility is parity.
        for a in range(1 << n):
            for m in range(-2, 3):
                assert first_nonzero(a if m % 2 else 0) == (
                    first_nonzero(a) if m % 2 else 0
                )
        levels.append({"n": n, "image_size": len(image), "splitting_fibers": 1})
    assert first_nonzero(1 ^ 2) != first_nonzero(1) ^ first_nonzero(2)
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "passed",
        "claim": "Non-word compact-map obstruction only; no solution of 21.122",
        "levels": levels,
        "nonhomomorphism_witness": [1, 2],
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
