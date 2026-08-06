#!/usr/bin/env python3
"""Finite-family selector and sequence-to-uniform utilities."""
from __future__ import annotations

from dataclasses import dataclass
from math import factorial, log
from pathlib import Path
import sys
from typing import Sequence

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(PROJECT))

from src.generator import Complex, Reaction  # type: ignore  # noqa:E402
from phase5_source_flag_closure.src.episode_library import (  # type: ignore  # noqa:E402
    EpisodePath,
    expected_template_drift,
    full_library,
)
from phase5_source_flag_closure.src.target_source_residual import residual  # type: ignore  # noqa:E402

State = tuple[int, ...]


@dataclass(frozen=True, slots=True)
class SelectedEpisode:
    terminal: Complex
    path: EpisodePath
    expected_drift: float


def select_episode(
    reactions: Sequence[Reaction], x: Sequence[int], carried_target: Complex
) -> SelectedEpisode:
    """Deterministically select the least-drift terminal before the episode."""
    r = residual(x, carried_target)
    library = full_library(reactions)
    candidates: list[SelectedEpisode] = []
    terminals = sorted({key[1] for key in library})
    for terminal in terminals:
        path = library[(tuple(carried_target), terminal)]
        drift, _ = expected_template_drift(reactions, r, path)
        candidates.append(SelectedEpisode(terminal, path, drift))
    return min(candidates, key=lambda item: (item.expected_drift, item.terminal))


def potential_value(x: Sequence[int], target: Sequence[int]) -> float:
    r = residual(x, target)
    return sum(log(factorial(v)) for v in r)


def finite_sublevel_bound(level: float, dimension: int, complex_count: int) -> int:
    """A crude finite cardinality bound for {V<=level} in the augmented space."""
    if dimension < 0 or complex_count < 0:
        raise ValueError("invalid dimensions")
    b = 1
    running = 0.0
    while running <= level:
        b += 1
        running += log(b)
    return complex_count * (b ** dimension)


def self_test() -> None:
    from fractions import Fraction

    reactions = (
        Reaction((0, 0), (1, 1), Fraction(1)),
        Reaction((1, 1), (0, 1), Fraction(1)),
        Reaction((0, 1), (0, 0), Fraction(1)),
    )
    selected = select_episode(reactions, (100, 0), (0, 0))
    assert selected.terminal == (0, 1)
    assert selected.expected_drift < 0
    assert finite_sublevel_bound(0.0, 2, 3) == 12


if __name__ == "__main__":
    self_test()
    print("uniformization.py self-test: OK")
