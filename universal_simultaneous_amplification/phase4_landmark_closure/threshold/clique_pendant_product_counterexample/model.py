"""Exact lumped chains for the clique-with-pendants graph.

Vertices consist of one hub, ``c`` ordinary clique vertices, and ``m``
pendant leaves.  The hub and the ordinary vertices induce K_{c+1}; every
leaf is adjacent only to the hub.  A lumped state is ``(h, i, j)`` where
``h`` is the hub type and ``i,j`` count mutant ordinary vertices and leaves.

All probabilities in this module are :class:`fractions.Fraction` objects.
Only type-changing moves are returned; the omitted mass is the self-loop.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from typing import Dict, Iterable, Tuple


State = Tuple[int, int, int]


def states(c: int, m: int) -> Iterable[State]:
    for h in (0, 1):
        for i in range(c + 1):
            for j in range(m + 1):
                yield (h, i, j)


def absorbing_states(c: int, m: int) -> tuple[State, State]:
    return (0, 0, 0), (1, c, m)


def _add(out: Dict[State, Fraction], target: State, probability: Fraction) -> None:
    if probability:
        out[target] += probability


def bd_moves(state: State, c: int, m: int, r: Fraction) -> Dict[State, Fraction]:
    """Type-changing Bd transition probabilities from ``state``."""
    h, i, j = state
    n = c + m + 1
    mutants = h + i + j
    total_fitness = Fraction(n) + (r - 1) * mutants
    hub_degree = c + m
    out: Dict[State, Fraction] = defaultdict(Fraction)

    if h == 0:
        _add(out, (1, i, j), r * (Fraction(i, c) + j) / total_fitness)
    else:
        _add(
            out,
            (0, i, j),
            (Fraction(c - i, c) + (m - j)) / total_fitness,
        )

    _add(
        out,
        (h, i + 1, j),
        r
        * (c - i)
        * (Fraction(h, hub_degree) + Fraction(i, c))
        / total_fitness,
    ) if i < c else None
    _add(
        out,
        (h, i - 1, j),
        i
        * (Fraction(1 - h, hub_degree) + Fraction(c - i, c))
        / total_fitness,
    ) if i > 0 else None

    if j < m:
        _add(
            out,
            (h, i, j + 1),
            r * h * Fraction(m - j, hub_degree) / total_fitness,
        )
    if j > 0:
        _add(
            out,
            (h, i, j - 1),
            (1 - h) * Fraction(j, hub_degree) / total_fitness,
        )
    return dict(out)


def db_moves(state: State, c: int, m: int, r: Fraction) -> Dict[State, Fraction]:
    """Type-changing dB transition probabilities from ``state``."""
    h, i, j = state
    n = c + m + 1
    out: Dict[State, Fraction] = defaultdict(Fraction)

    mutant_hub_neighbors = i + j
    resident_hub_neighbors = c + m - i - j
    hub_denominator = r * mutant_hub_neighbors + resident_hub_neighbors
    if h == 0 and mutant_hub_neighbors:
        _add(
            out,
            (1, i, j),
            Fraction(1, n) * r * mutant_hub_neighbors / hub_denominator,
        )
    if h == 1 and resident_hub_neighbors:
        _add(
            out,
            (0, i, j),
            Fraction(1, n) * resident_hub_neighbors / hub_denominator,
        )

    if i < c:
        mutant_neighbors = h + i
        resident_neighbors = c - h - i
        if mutant_neighbors:
            _add(
                out,
                (h, i + 1, j),
                Fraction(c - i, n)
                * r
                * mutant_neighbors
                / (r * mutant_neighbors + resident_neighbors),
            )
    if i > 0:
        mutant_neighbors_after_death = h + i - 1
        resident_neighbors = c - h - i + 1
        if resident_neighbors:
            _add(
                out,
                (h, i - 1, j),
                Fraction(i, n)
                * resident_neighbors
                / (r * mutant_neighbors_after_death + resident_neighbors),
            )

    if j < m and h == 1:
        _add(out, (h, i, j + 1), Fraction(m - j, n))
    if j > 0 and h == 0:
        _add(out, (h, i, j - 1), Fraction(j, n))
    return dict(out)


def moves(
    rule: str, state: State, c: int, m: int, r: Fraction
) -> Dict[State, Fraction]:
    if rule == "Bd":
        return bd_moves(state, c, m, r)
    if rule == "dB":
        return db_moves(state, c, m, r)
    raise ValueError(f"unknown update rule {rule!r}")


def complete_baseline(rule: str, n: int, r: Fraction) -> Fraction:
    """Uniform-singleton fixation probability on loopless unit K_n."""
    if rule == "Bd":
        return (1 - 1 / r) / (1 - r ** (-n))
    if rule == "dB":
        return Fraction(n - 1, n) * (1 - 1 / r) / (1 - r ** (-(n - 1)))
    raise ValueError(f"unknown update rule {rule!r}")

