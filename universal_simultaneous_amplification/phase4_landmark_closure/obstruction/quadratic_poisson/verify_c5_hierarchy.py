#!/usr/bin/env python3
"""Exact C5 hierarchy obstruction and cubic repair at dB fitness r=2.

This standard-library verifier constructs the geometric-union dual directly.
On a degree-two vertex of C5, the sampled union is the left neighbor, the
right neighbor, or both, each with probability 1/3.

It proves exactly that:
  * the actual C5 stationary mean is 80/39 < 32/15;
  * a nonstationary pseudo-law annihilates every quadratic generator balance
    after dihedral symmetrization but has mean 40/17 > 32/15;
  * an explicit symmetric cubic has the required pointwise drift on every
    nonempty state.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations


ORDER = 5
STATES = tuple(range(1, 1 << ORDER))
PROPER_STATES = STATES[:-1]
EDGE_MASKS = tuple(
    (1 << vertex) | (1 << ((vertex + 1) % ORDER))
    for vertex in range(ORDER)
)
NONEDGE_MASKS = tuple(
    (1 << vertex) | (1 << ((vertex + 2) % ORDER))
    for vertex in range(ORDER)
)


def popcount(mask: int) -> int:
    return bin(mask).count("1")


def occupied_count(mask: int, patterns: tuple[int, ...]) -> int:
    return sum((mask & pattern) == pattern for pattern in patterns)


def orbit_key(mask: int) -> tuple[int, int]:
    return popcount(mask), occupied_count(mask, EDGE_MASKS)


def exact_generator() -> list[list[F]]:
    generator = [[F(0) for _ in STATES] for _ in STATES]
    for state in STATES:
        for target in range(ORDER):
            if not ((state >> target) & 1):
                continue
            without_target = state & ~(1 << target)
            left = 1 << ((target - 1) % ORDER)
            right = 1 << ((target + 1) % ORDER)
            for sampled_union in (left, right, left | right):
                new_state = without_target | sampled_union
                if new_state != state:
                    generator[state - 1][new_state - 1] += F(1, 3)
        generator[state - 1][state - 1] = -sum(
            generator[state - 1][new_state - 1]
            for new_state in STATES
            if new_state != state
        )
    assert all(sum(row) == 0 for row in generator)
    return generator


def generator_action(
    generator: list[list[F]], observable: list[F]
) -> list[F]:
    return [
        sum(row[column] * observable[column] for column in range(len(STATES)))
        for row in generator
    ]


def orbit_average(values: list[F], orbit: tuple[int, int]) -> F:
    members = [state for state in STATES if orbit_key(state) == orbit]
    return sum(values[state - 1] for state in members) / len(members)


def main() -> None:
    generator = exact_generator()
    proper_orbits = tuple(sorted({orbit_key(state) for state in PROPER_STATES}))
    assert proper_orbits == (
        (1, 0),
        (2, 0),
        (2, 1),
        (3, 1),
        (3, 2),
        (4, 3),
    )

    size = [F(popcount(state)) for state in STATES]
    edges = [F(occupied_count(state, EDGE_MASKS)) for state in STATES]
    nonedges = [F(occupied_count(state, NONEDGE_MASKS)) for state in STATES]

    triple_masks = tuple(
        sum(1 << vertex for vertex in triple)
        for triple in combinations(range(ORDER), 3)
    )
    triple_one_masks = tuple(
        mask for mask in triple_masks if occupied_count(mask, EDGE_MASKS) == 1
    )
    triple_two_masks = tuple(
        mask for mask in triple_masks if occupied_count(mask, EDGE_MASKS) == 2
    )
    triple_one = [
        F(occupied_count(state, triple_one_masks)) for state in STATES
    ]
    triple_two = [
        F(occupied_count(state, triple_two_masks)) for state in STATES
    ]

    observables = (size, edges, nonedges, triple_one, triple_two)
    actions = tuple(generator_action(generator, observable) for observable in observables)
    orbit_drifts = {
        orbit: tuple(orbit_average(action, orbit) for action in actions)
        for orbit in proper_orbits + ((5, 5),)
    }
    assert all(
        all(
            action[state - 1] == orbit_drifts[orbit][observable_index]
            for state in STATES
            if orbit_key(state) == orbit
        )
        for orbit in proper_orbits + ((5, 5),)
        for observable_index, action in enumerate(actions)
    )

    # Exact actual stationary orbit law.  Verify normalization and every
    # proper-orbit stationarity equation against the lumped generator.
    actual = (F(10, 39), F(1, 3), F(5, 39), F(8, 39), F(2, 39), F(1, 39))
    assert sum(actual) == 1

    lumped = [[F(0) for _ in proper_orbits] for _ in proper_orbits]
    orbit_index = {orbit: index for index, orbit in enumerate(proper_orbits)}
    for orbit in proper_orbits:
        representative = next(
            state for state in PROPER_STATES if orbit_key(state) == orbit
        )
        row = orbit_index[orbit]
        for new_state in PROPER_STATES:
            new_orbit = orbit_key(new_state)
            column = orbit_index[new_orbit]
            if column != row:
                lumped[row][column] += generator[representative - 1][new_state - 1]
        lumped[row][row] = -sum(
            lumped[row][column]
            for column in range(len(proper_orbits))
            if column != row
        )
    assert all(sum(row) == 0 for row in lumped)
    assert all(
        sum(actual[row] * lumped[row][column] for row in range(len(actual))) == 0
        for column in range(len(actual))
    )

    actual_mean = sum(
        mass * orbit[0] for mass, orbit in zip(actual, proper_orbits)
    )
    complete_mean = F(32, 15)
    assert actual_mean == F(80, 39)
    assert complete_mean - actual_mean == F(16, 195)

    # Quadratic Farkas pseudo-law.  It is not stationary for the full chain,
    # but it annihilates the generator of every dihedrally averaged quadratic.
    pseudo = (F(0), F(101, 153), F(0), F(16, 153), F(34, 153), F(2, 153))
    assert all(mass >= 0 for mass in pseudo)
    assert sum(pseudo) == 1
    for observable_index in range(3):
        assert sum(
            mass * orbit_drifts[orbit][observable_index]
            for mass, orbit in zip(pseudo, proper_orbits)
        ) == 0
    pseudo_mean = sum(
        mass * orbit[0] for mass, orbit in zip(pseudo, proper_orbits)
    )
    assert pseudo_mean == F(40, 17)
    assert pseudo_mean - complete_mean == F(56, 255)

    # Explicit symmetric cubic certificate.  The five coefficients multiply
    # K, E, N, T1, and T2 respectively.
    cubic_coefficients = (
        -F(2069, 675),
        F(196, 135),
        F(368, 675),
        -F(26, 675),
        -F(104, 225),
    )
    expected_slacks = (
        F(22, 75),
        F(0),
        F(0),
        F(0),
        F(2, 15),
        F(0),
        F(0),
    )
    all_orbits = proper_orbits + ((5, 5),)
    slacks = tuple(
        sum(
            coefficient * drift
            for coefficient, drift in zip(cubic_coefficients, orbit_drifts[orbit])
        )
        - (F(orbit[0]) - complete_mean)
        for orbit in all_orbits
    )
    assert slacks == expected_slacks
    assert all(slack >= 0 for slack in slacks)
    pointwise_slacks = tuple(
        sum(
            coefficient * action[state - 1]
            for coefficient, action in zip(cubic_coefficients, actions)
        )
        - (F(popcount(state)) - complete_mean)
        for state in STATES
    )
    assert all(slack >= 0 for slack in pointwise_slacks)
    assert set(pointwise_slacks) == set(expected_slacks)

    print("PASS exact C5 stationary law")
    print(f"actual mean = {actual_mean}; K5 mean = {complete_mean}")
    print("PASS exact quadratic Farkas obstruction")
    print(f"pseudo mean = {pseudo_mean}; excess = {pseudo_mean - complete_mean}")
    print("PASS exact cubic pointwise certificate")
    print("orbit slacks =", slacks)


if __name__ == "__main__":
    main()
