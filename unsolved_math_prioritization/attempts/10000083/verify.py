#!/usr/bin/env python3
"""Exact boundary controls. This does NOT verify the Dubroff--Kahn theorem."""
from fractions import Fraction
import json


def cover_probability(adjacency, start, steps):
    n = len(adjacency)
    states = {(start, 1 << start): Fraction(1)}
    for _ in range(steps):
        nxt = {}
        for (v, seen), mass in states.items():
            neighbors = adjacency[v] or [v]  # absorbing isolated-vertex convention
            for w in neighbors:
                key = (w, seen | (1 << w))
                nxt[key] = nxt.get(key, Fraction(0)) + mass / len(neighbors)
        assert sum(nxt.values()) == 1
        states = nxt
    return sum((mass for (_, seen), mass in states.items()
                if seen == (1 << n) - 1), Fraction(0))


def main():
    checks = []
    for start in [0, 1]:
        for steps in [1, 2, 3]:
            value = cover_probability([[1], [0]], start, steps)
            assert value == 1
            checks.append({"graph": "K2", "start": start, "steps": steps,
                           "probability": str(value)})
    assert cover_probability([[]], 0, 0) == 1
    assert cover_probability([[1], [0], []], 0, 10) == 0
    assert cover_probability([[1, 2], [0, 2], [0, 1]], 0, 2) == Fraction(1, 2)
    # Exact concrete illustration, not a replacement for the symbolic c<1 argument.
    assert Fraction(99, 100) ** 2 < 1
    print(json.dumps({"scope": "finite boundary controls only; no asymptotic theorem verification",
                      "checks": checks, "additional_assertions": 4,
                      "result": "PASS"}, indent=2))


if __name__ == "__main__":
    main()
