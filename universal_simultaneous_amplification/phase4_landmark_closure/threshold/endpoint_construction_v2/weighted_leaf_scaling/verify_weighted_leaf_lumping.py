#!/usr/bin/env python3
"""Definition-level exact audit of the one-heavy-leaf orbit chain."""

from __future__ import annotations

from itertools import combinations

from flint import fmpq


Q = fmpq


def add(row, target, probability):
    if probability:
        row[target] = row.get(target, Q(0)) + probability


def quotient_changes(C: int, tau, r, rule: str, state):
    h, i, leaf = state
    c = C - 1
    n = C + 1
    w = tau * C
    row = {}
    if rule == "Bd":
        total = Q(n) + (r - 1) * (h + i + leaf)
        if i < c:
            add(
                row,
                (h, i + 1, leaf),
                r * (c - i) * (Q(h) / (c + w) + Q(i, c)) / total,
            )
        if i:
            add(
                row,
                (h, i - 1, leaf),
                i * (Q(1 - h) / (c + w) + Q(c - i, c)) / total,
            )
        if not h:
            add(row, (1, i, leaf), r * (Q(i, c) + leaf) / total)
        else:
            add(row, (0, i, leaf), (Q(c - i, c) + 1 - leaf) / total)
        if h and not leaf:
            add(row, (h, i, 1), r * w / (c + w) / total)
        if not h and leaf:
            add(row, (h, i, 0), w / (c + w) / total)
    elif rule == "dB":
        if i < c:
            denominator = r * (i + h) + c - i - h
            add(
                row,
                (h, i + 1, leaf),
                Q(c - i, n) * r * (i + h) / denominator,
            )
        if i:
            denominator = r * (i - 1 + h) + c - i + 1 - h
            add(
                row,
                (h, i - 1, leaf),
                Q(i, n) * (c - i + 1 - h) / denominator,
            )
        denominator = r * i + c - i + w * (r if leaf else 1)
        if not h:
            add(
                row,
                (1, i, leaf),
                Q(1, n) * (r * i + r * w * leaf) / denominator,
            )
        else:
            add(
                row,
                (0, i, leaf),
                Q(1, n) * (c - i + w * (1 - leaf)) / denominator,
            )
        if h and not leaf:
            add(row, (h, i, 1), Q(1, n))
        if not h and leaf:
            add(row, (h, i, 0), Q(1, n))
    else:
        raise ValueError(rule)
    return row


def labelled_changes(C: int, tau, r, rule: str, mask: int):
    n = C + 1
    c = C - 1
    hub = 0
    leaf_vertex = C
    weights = [[Q(0) for _ in range(n)] for _ in range(n)]
    for left, right in combinations(range(C), 2):
        weights[left][right] = weights[right][left] = Q(1)
    weights[hub][leaf_vertex] = weights[leaf_vertex][hub] = tau * C
    degrees = [sum(row, Q(0)) for row in weights]
    mutant = [(mask >> vertex) & 1 for vertex in range(n)]
    fitness = [r if mutant[vertex] else Q(1) for vertex in range(n)]
    row = {}
    if rule == "Bd":
        total = sum(fitness, Q(0))
        for parent in range(n):
            for target in range(n):
                if weights[parent][target] and mutant[parent] != mutant[target]:
                    probability = (
                        fitness[parent]
                        / total
                        * weights[parent][target]
                        / degrees[parent]
                    )
                    add(row, mask ^ (1 << target), probability)
    else:
        for target in range(n):
            denominator = sum(
                (fitness[parent] * weights[target][parent] for parent in range(n)), Q(0)
            )
            for parent in range(n):
                if weights[target][parent] and mutant[parent] != mutant[target]:
                    probability = (
                        Q(1, n)
                        * fitness[parent]
                        * weights[target][parent]
                        / denominator
                    )
                    add(row, mask ^ (1 << target), probability)
    return row


def orbit(mask: int, C: int):
    hub = mask & 1
    ordinary = sum((mask >> vertex) & 1 for vertex in range(1, C))
    leaf = (mask >> C) & 1
    return hub, ordinary, leaf


def main() -> None:
    C = 5
    n = C + 1
    tau = Q(5, 2)
    r = Q(3, 2)
    for rule in ("Bd", "dB"):
        for mask in range(1 << n):
            aggregate = {}
            for target, probability in labelled_changes(C, tau, r, rule, mask).items():
                label = orbit(target, C)
                aggregate[label] = aggregate.get(label, Q(0)) + probability
            expected = quotient_changes(C, tau, r, rule, orbit(mask, C))
            assert aggregate == expected, (rule, mask, aggregate, expected)
    print(f"PASS exact weighted-leaf lumping: n={n}, masks={1 << n}")


if __name__ == "__main__":
    main()

