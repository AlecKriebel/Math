"""Labelled-event implementation independent of the aggregate formulas."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction


def graph(c: int, m: int):
    n = c + m + 1
    hub = 0
    leaves = range(c + 1, n)
    neighbors = {v: [] for v in range(n)}
    clique = range(c + 1)
    for u in clique:
        for v in clique:
            if u != v:
                neighbors[u].append(v)
    for leaf in leaves:
        neighbors[hub].append(leaf)
        neighbors[leaf].append(hub)
    return neighbors


def representative(state, c: int):
    h, i, j = state
    mutants = ({0} if h else set()) | set(range(1, i + 1))
    mutants |= set(range(c + 1, c + j + 1))
    return mutants


def lump(mutants, c: int):
    ordinary_mutants = len(mutants.intersection(range(1, c + 1)))
    return (
        int(0 in mutants),
        ordinary_mutants,
        len(mutants) - int(0 in mutants) - ordinary_mutants,
    )


def microscopic_moves(rule: str, state, c: int, m: int, r: Fraction):
    neighbors = graph(c, m)
    mutants = representative(state, c)
    n = len(neighbors)
    out = defaultdict(Fraction)
    if rule == "Bd":
        total_fitness = sum(r if u in mutants else 1 for u in neighbors)
        for u in neighbors:
            reproducer_probability = (r if u in mutants else 1) / total_fitness
            for v in neighbors[u]:
                probability = reproducer_probability * Fraction(1, len(neighbors[u]))
                if (u in mutants) != (v in mutants):
                    changed = set(mutants)
                    if u in mutants:
                        changed.add(v)
                    else:
                        changed.remove(v)
                    out[lump(changed, c)] += probability
    elif rule == "dB":
        for v in neighbors:
            denominator = sum(r if u in mutants else 1 for u in neighbors[v])
            for u in neighbors[v]:
                probability = Fraction(1, n) * (r if u in mutants else 1) / denominator
                if (u in mutants) != (v in mutants):
                    changed = set(mutants)
                    if u in mutants:
                        changed.add(v)
                    else:
                        changed.remove(v)
                    out[lump(changed, c)] += probability
    else:
        raise ValueError(f"unknown update rule {rule!r}")
    return dict(out)

