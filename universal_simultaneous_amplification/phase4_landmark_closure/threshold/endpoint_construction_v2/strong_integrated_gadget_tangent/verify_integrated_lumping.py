#!/usr/bin/env python3
"""Exact labelled audit of the strong integrated core/gadget orbit chain."""

from __future__ import annotations

from itertools import combinations

from flint import fmpq


Q = fmpq


def add(row, target, probability):
    if probability:
        row[target] = row.get(target, Q(0)) + probability


def quotient_changes(C, internal, portal, r, rule, state):
    core_mutants, mask = state
    order = len(portal)
    n = C + order
    mutant = [(mask >> vertex) & 1 for vertex in range(order)]
    portal_sum = sum(portal, Q(0))
    core_degree = C - 1 + portal_sum
    gadget_degree = [
        C * (portal[vertex] + sum(internal[vertex], Q(0)))
        for vertex in range(order)
    ]
    row = {}

    if rule == "Bd":
        total = Q(n) + (r - 1) * (core_mutants + sum(mutant))
        if core_mutants < C:
            rate = r * core_mutants * (C - core_mutants) / core_degree
            rate += sum(
                (
                    r
                    * (C - core_mutants)
                    * portal[vertex]
                    / gadget_degree[vertex]
                    if mutant[vertex]
                    else Q(0)
                )
                for vertex in range(order)
            )
            add(row, (core_mutants + 1, mask), rate / total)
        if core_mutants:
            rate = core_mutants * (C - core_mutants) / core_degree
            rate += sum(
                (
                    core_mutants * portal[vertex] / gadget_degree[vertex]
                    if not mutant[vertex]
                    else Q(0)
                )
                for vertex in range(order)
            )
            add(row, (core_mutants - 1, mask), rate / total)
        for target in range(order):
            if not mutant[target]:
                rate = r * core_mutants * portal[target] / core_degree
                rate += sum(
                    (
                        r * C * internal[parent][target] / gadget_degree[parent]
                        if mutant[parent]
                        else Q(0)
                    )
                    for parent in range(order)
                )
                add(row, (core_mutants, mask ^ (1 << target)), rate / total)
            else:
                rate = (C - core_mutants) * portal[target] / core_degree
                rate += sum(
                    (
                        C * internal[parent][target] / gadget_degree[parent]
                        if not mutant[parent]
                        else Q(0)
                    )
                    for parent in range(order)
                )
                add(row, (core_mutants, mask ^ (1 << target)), rate / total)
    elif rule == "dB":
        gadget_fitness_load = sum(
            portal[vertex] * (r if mutant[vertex] else 1)
            for vertex in range(order)
        )
        if core_mutants < C:
            denominator = r * core_mutants + C - core_mutants - 1 + gadget_fitness_load
            mutant_load = r * (
                core_mutants
                + sum(portal[vertex] for vertex in range(order) if mutant[vertex])
            )
            add(
                row,
                (core_mutants + 1, mask),
                Q(C - core_mutants, n) * mutant_load / denominator,
            )
        if core_mutants:
            denominator = (
                r * (core_mutants - 1) + C - core_mutants + gadget_fitness_load
            )
            resident_load = C - core_mutants + sum(
                portal[vertex] for vertex in range(order) if not mutant[vertex]
            )
            add(
                row,
                (core_mutants - 1, mask),
                Q(core_mutants, n) * resident_load / denominator,
            )
        for target in range(order):
            denominator = portal[target] * (
                r * core_mutants + C - core_mutants
            ) + C * sum(
                internal[target][parent] * (r if mutant[parent] else 1)
                for parent in range(order)
            )
            if not mutant[target]:
                mutant_load = r * (
                    core_mutants * portal[target]
                    + C
                    * sum(
                        internal[target][parent]
                        for parent in range(order)
                        if mutant[parent]
                    )
                )
                add(
                    row,
                    (core_mutants, mask ^ (1 << target)),
                    Q(1, n) * mutant_load / denominator,
                )
            else:
                resident_load = (C - core_mutants) * portal[target] + C * sum(
                    internal[target][parent]
                    for parent in range(order)
                    if not mutant[parent]
                )
                add(
                    row,
                    (core_mutants, mask ^ (1 << target)),
                    Q(1, n) * resident_load / denominator,
                )
    else:
        raise ValueError(rule)
    return row


def labelled_changes(C, internal, portal, r, rule, mask):
    order = len(portal)
    n = C + order
    weights = [[Q(0) for _ in range(n)] for _ in range(n)]
    for left, right in combinations(range(C), 2):
        weights[left][right] = weights[right][left] = Q(1)
    for core in range(C):
        for gadget in range(order):
            weights[core][C + gadget] = weights[C + gadget][core] = portal[gadget]
    for left, right in combinations(range(order), 2):
        weights[C + left][C + right] = weights[C + right][C + left] = (
            C * internal[left][right]
        )
    degrees = [sum(row, Q(0)) for row in weights]
    mutant = [(mask >> vertex) & 1 for vertex in range(n)]
    fitness = [r if mutant[vertex] else Q(1) for vertex in range(n)]
    row = {}
    if rule == "Bd":
        total = sum(fitness, Q(0))
        for parent in range(n):
            for target in range(n):
                if weights[parent][target] and mutant[parent] != mutant[target]:
                    add(
                        row,
                        mask ^ (1 << target),
                        fitness[parent]
                        / total
                        * weights[parent][target]
                        / degrees[parent],
                    )
    else:
        for target in range(n):
            denominator = sum(
                (fitness[parent] * weights[target][parent] for parent in range(n)), Q(0)
            )
            for parent in range(n):
                if weights[target][parent] and mutant[parent] != mutant[target]:
                    add(
                        row,
                        mask ^ (1 << target),
                        Q(1, n)
                        * fitness[parent]
                        * weights[target][parent]
                        / denominator,
                    )
    return row


def orbit(mask, C, order):
    core = sum((mask >> vertex) & 1 for vertex in range(C))
    gadget = sum(((mask >> (C + vertex)) & 1) << vertex for vertex in range(order))
    return core, gadget


def main() -> None:
    C = 4
    internal = [
        [Q(0), Q(1, 2), Q(2, 3)],
        [Q(1, 2), Q(0), Q(3, 5)],
        [Q(2, 3), Q(3, 5), Q(0)],
    ]
    portal = [Q(1), Q(2), Q(1, 3)]
    order = len(portal)
    n = C + order
    r = Q(3, 2)
    for rule in ("Bd", "dB"):
        for mask in range(1 << n):
            aggregate = {}
            for target, probability in labelled_changes(
                C, internal, portal, r, rule, mask
            ).items():
                label = orbit(target, C, order)
                aggregate[label] = aggregate.get(label, Q(0)) + probability
            expected = quotient_changes(
                C, internal, portal, r, rule, orbit(mask, C, order)
            )
            assert aggregate == expected, (rule, mask, aggregate, expected)
    print(f"PASS exact integrated-gadget lumping: n={n}, masks={1 << n}")


if __name__ == "__main__":
    main()
