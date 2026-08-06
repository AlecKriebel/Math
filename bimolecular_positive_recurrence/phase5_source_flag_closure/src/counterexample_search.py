#!/usr/bin/env python3
"""Targeted finite falsification search for the Phase-V mechanism.

This is not used as proof.  It enumerates small directed complex cycles,
several rational rate vectors, and anisotropic population scalings, looking
for a divergent family on which every terminal-template drift remains
nonnegative.  None of the calibrated cases survives at the largest scale.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(PROJECT))

from src.generator import Reaction  # type: ignore  # noqa:E402
from phase5_source_flag_closure.src.source_rate_flag import bimolecular_complexes  # type: ignore  # noqa:E402
from phase5_source_flag_closure.src.uniformization import select_episode  # type: ignore  # noqa:E402


def targeted_search(limit_cycles: int = 20) -> dict[str, int | float]:
    C = bimolecular_complexes(2)
    ratesets = ((1, 1, 1), (1, 2, 5), (7, 1, 3))
    exponents = ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2))
    from phase5_source_flag_closure.src.source_rate_flag import top_availability_or_conservation
    tested = 0
    nonconservative_nonnegative = 0
    conservation_incompatible = 0
    worst_nonconservative = float("-inf")
    cycles = 0
    for nodes in permutations(C, 3):
        if len(set(nodes)) < 3:
            continue
        cycles += 1
        if cycles > limit_cycles:
            break
        for rates in ratesets:
            reactions = tuple(
                Reaction(nodes[k], nodes[(k + 1) % 3], Fraction(rates[k]))
                for k in range(3)
            )
            for a, b in exponents:
                I = {i for i, exponent in enumerate((a, b)) if exponent > 0}
                cert = top_availability_or_conservation(
                    nodes, I, (Fraction(a), Fraction(b))
                )
                n = 200
                residual = (n**a if a else 0, n**b if b else 0)
                for target in nodes:
                    x = tuple(residual[i] + target[i] for i in range(2))
                    chosen = select_episode(reactions, x, target)
                    tested += 1
                    if cert.conservation is not None:
                        if chosen.expected_drift >= 0:
                            conservation_incompatible += 1
                    else:
                        worst_nonconservative = max(
                            worst_nonconservative, chosen.expected_drift
                        )
                        if chosen.expected_drift >= 0:
                            nonconservative_nonnegative += 1
    return {
        "cycles": min(cycles, limit_cycles),
        "states_tested": tested,
        "nonconservative_nonnegative_selected_drifts": nonconservative_nonnegative,
        "conservation_incompatible_nonnegative_drifts": conservation_incompatible,
        "largest_nonconservative_selected_drift": worst_nonconservative,
    }


def self_test() -> None:
    report = targeted_search(10)
    assert report["states_tested"] > 0


if __name__ == "__main__":
    print(json.dumps(targeted_search(), indent=2, sort_keys=True))
