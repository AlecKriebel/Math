#!/usr/bin/env python3
"""Exact labelled-state audit of the exchangeable multiportal lumping.

This verifier is deliberately independent of ``check_finite_multiportal``.
For a rational instance it constructs every labelled mutant subset, sums the
atomic Bd and dB changing rates by orbit, and compares those sums with a
separate exact implementation of the displayed three-count formulas.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations


State = tuple[int, int, int]


def graph(
    blade_count: int,
    portal_count: int,
    load: Fraction,
    theta: Fraction,
) -> list[list[Fraction]]:
    vertex_count = portal_count + 2 * blade_count
    weights = [
        [Fraction(0) for _ in range(vertex_count)]
        for _ in range(vertex_count)
    ]

    def edge(i: int, j: int, weight: Fraction) -> None:
        weights[i][j] = weight
        weights[j][i] = weight

    portal_edge = 2 * load * theta / (portal_count - 1)
    for first in range(portal_count):
        for second in range(first + 1, portal_count):
            edge(first, second, portal_edge)

    blade_edge = load / blade_count
    for blade in range(blade_count):
        first = portal_count + 2 * blade
        second = first + 1
        edge(first, second, Fraction(1))
        for portal in range(portal_count):
            edge(portal, first, blade_edge)
            edge(portal, second, blade_edge)
    return weights


def orbit(
    mutants: frozenset[int], blade_count: int, portal_count: int
) -> State:
    mutant_portals = sum(portal in mutants for portal in range(portal_count))
    resident_blades = 0
    heterotypic_blades = 0
    for blade in range(blade_count):
        first = portal_count + 2 * blade
        mutant_endpoints = int(first in mutants) + int(first + 1 in mutants)
        resident_blades += int(mutant_endpoints == 0)
        heterotypic_blades += int(mutant_endpoints == 1)
    return mutant_portals, resident_blades, heterotypic_blades


def labelled_rates(
    mutants: frozenset[int],
    weights: list[list[Fraction]],
    fitness: Fraction,
    rule: str,
) -> dict[frozenset[int], Fraction]:
    vertex_count = len(weights)
    degree = [sum(row) for row in weights]
    out: dict[frozenset[int], Fraction] = defaultdict(Fraction)

    if rule == "Bd":
        for parent in range(vertex_count):
            parent_mutant = parent in mutants
            parent_fitness = fitness if parent_mutant else Fraction(1)
            for target in range(vertex_count):
                if weights[parent][target] == 0:
                    continue
                if (target in mutants) == parent_mutant:
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
        for target in range(vertex_count):
            denominator = sum(
                (fitness if parent in mutants else Fraction(1))
                * weights[parent][target]
                for parent in range(vertex_count)
            )
            target_mutant = target in mutants
            for parent in range(vertex_count):
                if weights[parent][target] == 0:
                    continue
                if (parent in mutants) == target_mutant:
                    continue
                changed = set(mutants)
                if parent in mutants:
                    changed.add(target)
                    parent_fitness = fitness
                else:
                    changed.remove(target)
                    parent_fitness = Fraction(1)
                out[frozenset(changed)] += (
                    parent_fitness
                    * weights[parent][target]
                    / denominator
                )
    else:
        raise ValueError(rule)
    return dict(out)


def add(out: dict[State, Fraction], state: State, rate: Fraction) -> None:
    if rate:
        out[state] += rate


def formula_bd(
    state: State,
    blade_count: int,
    portal_count: int,
    fitness: Fraction,
    load: Fraction,
    theta: Fraction,
) -> dict[State, Fraction]:
    k, z, u = state
    mutant_blades = blade_count - z - u
    mutant_blade_vertices = u + 2 * mutant_blades
    resident_blade_vertices = 2 * z + u
    attachment = load / blade_count
    portal_edge = 2 * load * theta / (portal_count - 1)
    blade_degree = 1 + portal_count * attachment
    portal_degree = 2 * load + (portal_count - 1) * portal_edge
    out: dict[State, Fraction] = defaultdict(Fraction)

    if k < portal_count:
        portal_gain = (
            fitness * k * (portal_count - k) * portal_edge / portal_degree
        )
        blade_gain = (
            fitness
            * mutant_blade_vertices
            * (portal_count - k)
            * attachment
            / blade_degree
        )
        add(out, (k + 1, z, u), portal_gain + blade_gain)
    if k > 0:
        portal_loss = k * (portal_count - k) * portal_edge / portal_degree
        blade_loss = (
            resident_blade_vertices * k * attachment / blade_degree
        )
        add(out, (k - 1, z, u), portal_loss + blade_loss)

    if k > 0:
        if z:
            add(
                out,
                (k, z - 1, u + 1),
                fitness * k * 2 * z * attachment / portal_degree,
            )
        if u:
            add(
                out,
                (k, z, u - 1),
                fitness * k * u * attachment / portal_degree,
            )
    if k < portal_count:
        if mutant_blades:
            add(
                out,
                (k, z, u + 1),
                (portal_count - k)
                * 2
                * mutant_blades
                * attachment
                / portal_degree,
            )
        if u:
            add(
                out,
                (k, z + 1, u - 1),
                (portal_count - k) * u * attachment / portal_degree,
            )
    if u:
        add(out, (k, z, u - 1), fitness * u / blade_degree)
        add(out, (k, z + 1, u - 1), u / blade_degree)
    return dict(out)


def formula_db(
    state: State,
    blade_count: int,
    portal_count: int,
    fitness: Fraction,
    load: Fraction,
    theta: Fraction,
) -> dict[State, Fraction]:
    k, z, u = state
    mutant_blades = blade_count - z - u
    mutant_blade_vertices = u + 2 * mutant_blades
    resident_blade_vertices = 2 * z + u
    attachment = load / blade_count
    portal_edge = 2 * load * theta / (portal_count - 1)
    out: dict[State, Fraction] = defaultdict(Fraction)

    if k < portal_count:
        mutant_mass = fitness * (
            mutant_blade_vertices * attachment + k * portal_edge
        )
        resident_mass = (
            resident_blade_vertices * attachment
            + (portal_count - k - 1) * portal_edge
        )
        add(
            out,
            (k + 1, z, u),
            (portal_count - k) * mutant_mass / (mutant_mass + resident_mass),
        )
    if k > 0:
        mutant_mass = fitness * (
            mutant_blade_vertices * attachment + (k - 1) * portal_edge
        )
        resident_mass = (
            resident_blade_vertices * attachment
            + (portal_count - k) * portal_edge
        )
        add(
            out,
            (k - 1, z, u),
            k * resident_mass / (mutant_mass + resident_mass),
        )

    if z:
        mutant_mass = fitness * k * attachment
        resident_mass = 1 + (portal_count - k) * attachment
        add(
            out,
            (k, z - 1, u + 1),
            2 * z * mutant_mass / (mutant_mass + resident_mass),
        )
    if mutant_blades:
        mutant_mass = fitness * (1 + k * attachment)
        resident_mass = (portal_count - k) * attachment
        add(
            out,
            (k, z, u + 1),
            2
            * mutant_blades
            * resident_mass
            / (mutant_mass + resident_mass),
        )
    if u:
        mutant_mass = fitness * (1 + k * attachment)
        resident_mass = (portal_count - k) * attachment
        add(
            out,
            (k, z, u - 1),
            u * mutant_mass / (mutant_mass + resident_mass),
        )
        mutant_mass = fitness * k * attachment
        resident_mass = 1 + (portal_count - k) * attachment
        add(
            out,
            (k, z + 1, u - 1),
            u * resident_mass / (mutant_mass + resident_mass),
        )
    return dict(out)


def aggregate(
    rates: dict[frozenset[int], Fraction],
    blade_count: int,
    portal_count: int,
) -> dict[State, Fraction]:
    out: dict[State, Fraction] = defaultdict(Fraction)
    for target, rate in rates.items():
        out[orbit(target, blade_count, portal_count)] += rate
    return dict(out)


def check(rule: str) -> None:
    blade_count = 3
    portal_count = 3
    fitness = Fraction(8, 5)
    load = Fraction(7, 20)
    theta = Fraction(2, 3)
    weights = graph(blade_count, portal_count, load, theta)
    by_orbit: dict[State, dict[State, Fraction]] = {}
    vertex_count = len(weights)

    for size in range(vertex_count + 1):
        for vertices in combinations(range(vertex_count), size):
            mutants = frozenset(vertices)
            key = orbit(mutants, blade_count, portal_count)
            actual = aggregate(
                labelled_rates(mutants, weights, fitness, rule),
                blade_count,
                portal_count,
            )
            expected = (
                formula_bd(
                    key,
                    blade_count,
                    portal_count,
                    fitness,
                    load,
                    theta,
                )
                if rule == "Bd"
                else formula_db(
                    key,
                    blade_count,
                    portal_count,
                    fitness,
                    load,
                    theta,
                )
            )
            if actual != expected:
                raise AssertionError((rule, mutants, key, actual, expected))
            if key in by_orbit and actual != by_orbit[key]:
                raise AssertionError((rule, "not strongly lumpable", key))
            by_orbit[key] = actual

    print(
        f"PASS {rule}: all {2**vertex_count} labelled subsets agree exactly "
        f"with the {len(by_orbit)} orbit generators"
    )


def main() -> None:
    check("Bd")
    check("dB")
    print("ALL EXACT MULTIPORTAL FINITE-LUMPING CHECKS PASS")


if __name__ == "__main__":
    main()
