#!/usr/bin/env python3
"""Exact labelled-state audit of the two-portal lumped generators.

This verifier deliberately does not import the finite lumped implementation.
It constructs every labelled mutant subset for a rational test instance,
aggregates the atomic Bd and dB rates by orbit, and compares them with a
separate exact implementation of the displayed count formulas.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations


State = tuple[int, int, int]


def graph(s: int, c: Fraction, theta: Fraction) -> list[list[Fraction]]:
    n = 2 + 2 * s
    weights = [[Fraction(0) for _ in range(n)] for _ in range(n)]

    def edge(i: int, j: int, weight: Fraction) -> None:
        weights[i][j] = weight
        weights[j][i] = weight

    edge(0, 1, 2 * c * theta)
    for blade in range(s):
        x = 2 + 2 * blade
        y = x + 1
        edge(x, y, Fraction(1))
        for portal in (0, 1):
            edge(portal, x, c / s)
            edge(portal, y, c / s)
    return weights


def orbit(mutants: frozenset[int], s: int) -> State:
    portal_count = int(0 in mutants) + int(1 in mutants)
    resident = 0
    heterotypic = 0
    for blade in range(s):
        x = 2 + 2 * blade
        count = int(x in mutants) + int(x + 1 in mutants)
        resident += int(count == 0)
        heterotypic += int(count == 1)
    return portal_count, resident, heterotypic


def labelled_rates(
    mutants: frozenset[int],
    weights: list[list[Fraction]],
    fitness: Fraction,
    rule: str,
) -> dict[frozenset[int], Fraction]:
    n = len(weights)
    degree = [sum(row) for row in weights]
    out: dict[frozenset[int], Fraction] = defaultdict(Fraction)
    if rule == "Bd":
        for parent in range(n):
            parent_mutant = parent in mutants
            parent_fitness = fitness if parent_mutant else Fraction(1)
            for target in range(n):
                if weights[parent][target] == 0 or ((target in mutants) == parent_mutant):
                    continue
                changed = set(mutants)
                if parent_mutant:
                    changed.add(target)
                else:
                    changed.remove(target)
                out[frozenset(changed)] += (
                    parent_fitness * weights[parent][target] / degree[parent]
                )
    elif rule == "dB":
        for target in range(n):
            denominator = sum(
                (fitness if source in mutants else Fraction(1)) * weights[source][target]
                for source in range(n)
            )
            target_mutant = target in mutants
            for parent in range(n):
                if weights[parent][target] == 0 or ((parent in mutants) == target_mutant):
                    continue
                changed = set(mutants)
                if parent in mutants:
                    changed.add(target)
                    parent_fitness = fitness
                else:
                    changed.remove(target)
                    parent_fitness = Fraction(1)
                out[frozenset(changed)] += (
                    parent_fitness * weights[parent][target] / denominator
                )
    else:
        raise ValueError(rule)
    return dict(out)


def add(out: dict[State, Fraction], state: State, rate: Fraction) -> None:
    if rate:
        out[state] += rate


def formula_bd(
    state: State, s: int, fitness: Fraction, c: Fraction, theta: Fraction
) -> dict[State, Fraction]:
    k, z, u = state
    v = s - z - u
    a = c / s
    portal_edge = 2 * c * theta
    blade_degree = 1 + 2 * a
    portal_degree = 2 * c + portal_edge
    out: dict[State, Fraction] = defaultdict(Fraction)

    if k < 2:
        cross = fitness * portal_edge / portal_degree if k == 1 else Fraction(0)
        blades = fitness * (u + 2 * v) * (2 - k) * a / blade_degree
        add(out, (k + 1, z, u), cross + blades)
    if k > 0:
        cross = portal_edge / portal_degree if k == 1 else Fraction(0)
        blades = (2 * z + u) * k * a / blade_degree
        add(out, (k - 1, z, u), cross + blades)
    if k > 0:
        if z:
            add(out, (k, z - 1, u + 1), fitness * k * 2 * z * a / portal_degree)
        if u:
            add(out, (k, z, u - 1), fitness * k * u * a / portal_degree)
    if k < 2:
        if v:
            add(out, (k, z, u + 1), (2 - k) * 2 * v * a / portal_degree)
        if u:
            add(out, (k, z + 1, u - 1), (2 - k) * u * a / portal_degree)
    if u:
        add(out, (k, z, u - 1), fitness * u / blade_degree)
        add(out, (k, z + 1, u - 1), u / blade_degree)
    return dict(out)


def formula_db(
    state: State, s: int, fitness: Fraction, c: Fraction, theta: Fraction
) -> dict[State, Fraction]:
    k, z, u = state
    v = s - z - u
    a = c / s
    portal_edge = 2 * c * theta
    mutant_vertices = u + 2 * v
    resident_vertices = 2 * z + u
    out: dict[State, Fraction] = defaultdict(Fraction)

    if k < 2:
        other_mutant = int(k == 1)
        mutant_mass = fitness * (mutant_vertices * a + other_mutant * portal_edge)
        resident_mass = resident_vertices * a + (1 - other_mutant) * portal_edge
        add(out, (k + 1, z, u), (2 - k) * mutant_mass / (mutant_mass + resident_mass))
    if k > 0:
        other_mutant = int(k == 2)
        mutant_mass = fitness * (mutant_vertices * a + other_mutant * portal_edge)
        resident_mass = resident_vertices * a + (1 - other_mutant) * portal_edge
        add(out, (k - 1, z, u), k * resident_mass / (mutant_mass + resident_mass))
    if z:
        mutant_mass = fitness * k * a
        resident_mass = 1 + (2 - k) * a
        add(out, (k, z - 1, u + 1), 2 * z * mutant_mass / (mutant_mass + resident_mass))
    if v:
        mutant_mass = fitness * (1 + k * a)
        resident_mass = (2 - k) * a
        add(out, (k, z, u + 1), 2 * v * resident_mass / (mutant_mass + resident_mass))
    if u:
        mutant_mass = fitness * (1 + k * a)
        resident_mass = (2 - k) * a
        add(out, (k, z, u - 1), u * mutant_mass / (mutant_mass + resident_mass))
        mutant_mass = fitness * k * a
        resident_mass = 1 + (2 - k) * a
        add(out, (k, z + 1, u - 1), u * resident_mass / (mutant_mass + resident_mass))
    return dict(out)


def aggregate(
    rates: dict[frozenset[int], Fraction], s: int
) -> dict[State, Fraction]:
    out: dict[State, Fraction] = defaultdict(Fraction)
    for target, rate in rates.items():
        out[orbit(target, s)] += rate
    return dict(out)


def check(rule: str) -> None:
    s = 3
    fitness = Fraction(8, 5)
    c = Fraction(2, 5)
    theta = Fraction(3, 7)
    weights = graph(s, c, theta)
    by_orbit: dict[State, dict[State, Fraction]] = {}
    n = len(weights)
    for size in range(n + 1):
        for vertices in combinations(range(n), size):
            mutants = frozenset(vertices)
            key = orbit(mutants, s)
            actual = aggregate(labelled_rates(mutants, weights, fitness, rule), s)
            expected = (
                formula_bd(key, s, fitness, c, theta)
                if rule == "Bd"
                else formula_db(key, s, fitness, c, theta)
            )
            if actual != expected:
                raise AssertionError((rule, mutants, key, actual, expected))
            if key in by_orbit and actual != by_orbit[key]:
                raise AssertionError((rule, "not strongly lumpable", key))
            by_orbit[key] = actual
    print(
        f"PASS {rule}: all {2**n} labelled subsets agree exactly with "
        f"the {len(by_orbit)} orbit generators"
    )


def main() -> None:
    check("Bd")
    check("dB")
    print("ALL EXACT FINITE-LUMPING CHECKS PASS")


if __name__ == "__main__":
    main()
