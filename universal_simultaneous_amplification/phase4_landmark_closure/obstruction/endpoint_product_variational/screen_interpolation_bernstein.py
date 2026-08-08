#!/usr/bin/env python3
"""Deterministic exact hostile screen of interpolation Bernstein signs.

This is finite computational evidence only.  Every trial uses a connected
five-vertex integer-weight graph and exact rational polynomial arithmetic.
"""

from __future__ import annotations

import random

from verify_stationary_interpolation import even_gap_polynomial


SEED = 41771
TRIALS = 60


def random_graph(rng: random.Random, n: int = 5):
    weights = [[0] * n for _ in range(n)]
    order = list(range(n))
    rng.shuffle(order)
    # Begin with a random spanning tree, so every support is connected.
    for position in range(1, n):
        first = order[position]
        second = order[rng.randrange(position)]
        value = rng.choice([1, 2, 3, 10, 100, 1000, 10000, 100000])
        weights[first][second] = weights[second][first] = value
    density = rng.random()
    for first in range(n):
        for second in range(first + 1, n):
            if not weights[first][second] and rng.random() < density:
                value = rng.choice([1, 2, 5, 20, 200, 2000, 20000, 200000])
                weights[first][second] = weights[second][first] = value
    return tuple(tuple(row) for row in weights)


def main() -> None:
    rng = random.Random(SEED)
    for trial in range(TRIALS):
        weights = random_graph(rng)
        _, _, numerator_s, _, bernstein = even_gap_polynomial(weights)
        assert bernstein[0] == 0
        assert all(coefficient >= 0 for coefficient in bernstein)
        assert numerator_s(1) > 0
        if (trial + 1) % 10 == 0:
            print(f"PASS: {trial + 1}/{TRIALS} exact order-five screens")
    print("STATUS: finite exact screen only; universal interpolation remains OPEN")


if __name__ == "__main__":
    main()
