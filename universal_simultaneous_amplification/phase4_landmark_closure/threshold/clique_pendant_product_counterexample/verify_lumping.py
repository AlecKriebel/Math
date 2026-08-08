#!/usr/bin/env python3
"""Independent microscopic verification of every lumped transition formula."""

from __future__ import annotations

from fractions import Fraction

from microscopic import microscopic_moves
from model import moves, states


def main() -> None:
    # Exhaust every state of the counterexample and several smaller graphs and
    # fitnesses.  This code does not use the aggregate-rate derivation.
    cases = [
        (2, 1, Fraction(3, 2)),
        (3, 2, Fraction(7, 5)),
        (4, 3, Fraction(2)),
        (32, 4, Fraction(3, 2)),
    ]
    checks = 0
    for c, m, r in cases:
        for rule in ("Bd", "dB"):
            for state in states(c, m):
                direct = microscopic_moves(rule, state, c, m, r)
                aggregate = moves(rule, state, c, m, r)
                assert direct == aggregate, (c, m, r, rule, state, direct, aggregate)
                assert sum(direct.values(), Fraction()) <= 1
                checks += 1
    print(f"PASS: {checks} exact microscopic/lumped transition comparisons")


if __name__ == "__main__":
    main()
