"""Exact and floating lumped chains for a weighted clique with pendants.

The hub ``H`` and ``c`` ordinary vertices induce a unit-weight clique.
Each of ``m`` leaves is joined only to ``H`` by a common weight ``w>0``.
A state ``(h,i,j)`` records the hub type and the numbers of mutant ordinary
vertices and mutant leaves.  Only type-changing moves are returned.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from typing import Dict, Iterable, Tuple, TypeVar


State = Tuple[int, int, int]
Number = TypeVar("Number", Fraction, float)


def states(c: int, m: int) -> Iterable[State]:
    for h in (0, 1):
        for i in range(c + 1):
            for j in range(m + 1):
                yield h, i, j


def absorbing_states(c: int, m: int) -> tuple[State, State]:
    return (0, 0, 0), (1, c, m)


def _add(out, target: State, probability) -> None:
    if probability:
        out[target] += probability


def bd_moves(state: State, c: int, m: int, r, w):
    """Type-changing Bd transition probabilities from ``state``."""
    h, i, j = state
    n = c + m + 1
    mutants = h + i + j
    total_fitness = n + (r - 1) * mutants
    hub_degree = c + m * w
    zero = r - r
    one = r / r
    out = defaultdict(lambda: zero)

    # The pendant weight cancels when a leaf reproduces, since H is its only
    # target.  It remains in H's target probabilities through hub_degree.
    if h == 0:
        _add(out, (1, i, j), r * (one * i / c + j) / total_fitness)
    else:
        _add(
            out,
            (0, i, j),
            (one * (c - i) / c + (m - j)) / total_fitness,
        )

    if i < c:
        _add(
            out,
            (h, i + 1, j),
            r * (c - i) * (h / hub_degree + one * i / c) / total_fitness,
        )
    if i > 0:
        _add(
            out,
            (h, i - 1, j),
            i
            * ((1 - h) / hub_degree + one * (c - i) / c)
            / total_fitness,
        )
    if j < m:
        _add(
            out,
            (h, i, j + 1),
            r * h * w * (m - j) / (hub_degree * total_fitness),
        )
    if j > 0:
        _add(
            out,
            (h, i, j - 1),
            (1 - h) * w * j / (hub_degree * total_fitness),
        )
    return dict(out)


def db_moves(state: State, c: int, m: int, r, w):
    """Type-changing dB transition probabilities from ``state``."""
    h, i, j = state
    n = c + m + 1
    zero = r - r
    one = r / r
    out = defaultdict(lambda: zero)

    mutant_hub_weight = i + w * j
    resident_hub_weight = c - i + w * (m - j)
    hub_denominator = r * mutant_hub_weight + resident_hub_weight
    if h == 0 and mutant_hub_weight:
        _add(
            out,
            (1, i, j),
            r * mutant_hub_weight / (n * hub_denominator),
        )
    if h == 1 and resident_hub_weight:
        _add(
            out,
            (0, i, j),
            resident_hub_weight / (n * hub_denominator),
        )

    if i < c:
        mutant_neighbors = h + i
        resident_neighbors = c - h - i
        if mutant_neighbors:
            _add(
                out,
                (h, i + 1, j),
                (c - i)
                * r
                * mutant_neighbors
                / (n * (r * mutant_neighbors + resident_neighbors)),
            )
    if i > 0:
        mutant_neighbors = h + i - 1
        resident_neighbors = c - h - i + 1
        if resident_neighbors:
            _add(
                out,
                (h, i - 1, j),
                i
                * resident_neighbors
                / (n * (r * mutant_neighbors + resident_neighbors)),
            )

    # A leaf has H as its only competitor, so w cancels from these rows.
    if j < m and h == 1:
        _add(out, (h, i, j + 1), one * (m - j) / n)
    if j > 0 and h == 0:
        _add(out, (h, i, j - 1), one * j / n)
    return dict(out)


def moves(rule: str, state: State, c: int, m: int, r, w):
    if rule == "Bd":
        return bd_moves(state, c, m, r, w)
    if rule == "dB":
        return db_moves(state, c, m, r, w)
    raise ValueError(rule)


def complete_baseline(rule: str, n: int, r):
    one = r / r
    if rule == "Bd":
        return (1 - 1 / r) / (1 - r ** (-n))
    if rule == "dB":
        return one * (n - 1) / n * (1 - 1 / r) / (1 - r ** (-(n - 1)))
    raise ValueError(rule)
