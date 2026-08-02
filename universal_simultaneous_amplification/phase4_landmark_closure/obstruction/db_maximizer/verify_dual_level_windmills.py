#!/usr/bin/env python3
"""Exact tests of two conjectured dB-dual complementary-level inequalities.

This is a verifier for a conjecture, not a proof.  It obtains stationary dual
level masses independently from exact forward fixation values and Boolean
duality.  If F_s is fixation averaged over all mutant sets of size s, then

    1-F_(n-t) = sum_(k<=t) pi_k*C(n-k,t-k)/C(n,t).

The triangular identity recovers every stationary level mass pi_k without
constructing the geometric-burst dual generator.  A labelled Möbius inversion
also checks the stronger reciprocal-degree-marked version on the windmills.
"""

from __future__ import annotations

from itertools import product
from math import comb, factorial

from flint import arb, fmpq, fmpq_mat


def solve_absorbing(states, changes, extinction, fixation):
    transient = [state for state in states if state not in (extinction, fixation)]
    index = {state: row for row, state in enumerate(transient)}
    matrix = fmpq_mat(len(transient), len(transient))
    rhs = fmpq_mat(len(transient), 1)
    for state, row in index.items():
        outgoing = changes(state)
        changing = sum((rate for _, rate in outgoing), fmpq(0))
        assert changing > 0
        matrix[row, row] = 1
        for target, rate in outgoing:
            probability = rate / changing
            if target == fixation:
                rhs[row, 0] += probability
            elif target != extinction:
                matrix[row, index[target]] -= probability
    solution = matrix.solve(rhs)
    assert matrix * solution == rhs
    values = {extinction: fmpq(0), fixation: fmpq(1)}
    values.update({state: solution[row, 0] for state, row in index.items()})
    return values


def level_masses(order, values, state_size, multiplicity):
    """Recover exact stationary dual masses from orbit fixation values."""
    averaged_fixation = []
    for size in range(order + 1):
        numerator = sum(
            (
                fmpq(multiplicity(state)) * value
                for state, value in values.items()
                if state_size(state) == size
            ),
            fmpq(0),
        )
        averaged_fixation.append(numerator / comb(order, size))

    masses = []
    for level in range(1, order + 1):
        disjoint_probability = 1 - averaged_fixation[order - level]
        mass = fmpq(comb(order, level)) * disjoint_probability
        for lower in range(1, level):
            mass -= masses[lower - 1] * comb(order - lower, level - lower)
        masses.append(mass)

    assert all(mass >= 0 for mass in masses)
    assert sum(masses, fmpq(0)) == 1
    mean = sum(
        (fmpq(level) * masses[level - 1] for level in range(1, order + 1)),
        fmpq(0),
    )
    assert mean / order == averaged_fixation[1]
    return masses, mean


def check_complementary_levels(label, order, fitness, masses):
    slacks = []
    for level in range(order // 2 + 1, order + 1):
        complement = order - level
        right = fmpq(0)
        if complement:
            right = (
                complement
                * (fitness - 1) ** (2 * level - order)
                * masses[complement - 1]
            )
        slack = right - level * masses[level - 1]
        assert slack >= 0, (label, level, slack)
        slacks.append((level, slack))
    nontrivial = [slack for level, slack in slacks if level < order]
    minimum = min(nontrivial) if nontrivial else fmpq(0)
    print(
        f"PASS {label}: complementary levels; "
        f"minimum non-full slack {float(arb(minimum)):.12g}"
    )


def heterogeneous_pair_windmill(outer, internal, fitness, return_values=False):
    blades = len(outer)
    order = 1 + 2 * blades
    extinction = (0,) * (blades + 1)
    fixation = (1,) + (2,) * blades
    states = list(product(range(2), *([range(3)] * blades)))
    outer = tuple(map(fmpq, outer))
    internal = tuple(map(fmpq, internal))

    def changes(state):
        center, *counts = state
        answer = []
        mutant_mass = sum(
            (weight * count for weight, count in zip(outer, counts)), fmpq(0)
        )
        resident_mass = sum(
            (weight * (2 - count) for weight, count in zip(outer, counts)),
            fmpq(0),
        )
        denominator = fitness * mutant_mass + resident_mass
        if not center and mutant_mass:
            answer.append(((1, *counts), fitness * mutant_mass / denominator))
        if center and resident_mass:
            answer.append(((0, *counts), resident_mass / denominator))

        for blade, (count, cross, inside) in enumerate(
            zip(counts, outer, internal)
        ):
            if count < 2:
                mutant_mass = inside * int(count == 1) + cross * center
                resident_mass = inside * int(count == 0) + cross * (1 - center)
                denominator = fitness * mutant_mass + resident_mass
                rate = (2 - count) * fitness * mutant_mass / denominator
                if rate:
                    target = list(counts)
                    target[blade] += 1
                    answer.append(((center, *target), rate))
            if count:
                mutant_mass = inside * int(count == 2) + cross * center
                resident_mass = inside * int(count == 1) + cross * (1 - center)
                denominator = fitness * mutant_mass + resident_mass
                rate = count * resident_mass / denominator
                if rate:
                    target = list(counts)
                    target[blade] -= 1
                    answer.append(((center, *target), rate))
        return answer

    values = solve_absorbing(states, changes, extinction, fixation)
    masses, mean = level_masses(
        order,
        values,
        state_size=sum,
        multiplicity=lambda state: 2 ** sum(count == 1 for count in state[1:]),
    )
    if return_values:
        return masses, mean, values
    return masses, mean


def check_marked_complementary_levels(
    label, outer, internal, fitness, orbit_values
):
    """Check the stronger reciprocal-degree-marked OPEN conjecture."""
    blades = len(outer)
    order = 1 + 2 * blades
    full = (1 << order) - 1

    def orbit(mask):
        return (
            int(bool(mask & 1)),
            *(
                int(bool(mask & (1 << (2 * blade + 1))))
                + int(bool(mask & (1 << (2 * blade + 2))))
                for blade in range(blades)
            ),
        )

    fixation = [orbit_values[orbit(mask)] for mask in range(full + 1)]
    invariant = [1 - fixation[full ^ mask] for mask in range(full + 1)]
    for bit in range(order):
        for mask in range(full + 1):
            if (mask >> bit) & 1:
                invariant[mask] -= invariant[mask ^ (1 << bit)]
    assert all(value >= 0 for value in invariant)
    assert sum(invariant, fmpq(0)) == 1

    center_degree = 2 * sum(map(fmpq, outer), fmpq(0))
    degrees = [center_degree]
    for cross, inside in zip(outer, internal):
        degrees.extend([fmpq(cross) + inside] * 2)
    marker_specs = {
        "inverse occupied": ([1 / degree for degree in degrees], False),
        "degree occupied": (degrees, False),
        "inverse holes": ([1 / degree for degree in degrees], True),
        "degree holes": (degrees, True),
    }
    minima = {}
    for marker_name, (vertex_marks, holes) in marker_specs.items():
        marked = []
        for level in range(1, order + 1):
            marked.append(
                sum(
                    (
                        invariant[mask]
                        * sum(
                            (
                                vertex_marks[vertex]
                                for vertex in range(order)
                                if bool((mask >> vertex) & 1) != holes
                            ),
                            fmpq(0),
                        )
                        for mask in range(1, full + 1)
                        if mask.bit_count() == level
                    ),
                    fmpq(0),
                )
            )

        slacks = []
        for level in range(order // 2 + 1, order + 1):
            complement = order - level
            right = fmpq(0)
            if complement:
                factor = (fitness - 1) ** (2 * level - order)
                if holes:
                    factor *= fmpq(complement**2, level**2)
                right = factor * marked[complement - 1]
            slack = right - marked[level - 1]
            assert slack >= 0, (label, marker_name, level, slack)
            if level < order:
                slacks.append(slack)
        minima[marker_name] = min(slacks) if slacks else fmpq(0)
    print(
        f"PASS {label}: four occupied/hole marker variants; minima "
        + ", ".join(
            f"{name}={float(arb(value)):.12g}"
            for name, value in minima.items()
        )
    )


def clique_core_identical_pairs(
    core_size, blades, outer, internal, fitness=fmpq(2)
):
    """Exact count chain for a clique core and exchangeable pair satellites."""
    order = core_size + 2 * blades
    distributions = [
        (x0, x1, blades - x0 - x1)
        for x0 in range(blades + 1)
        for x1 in range(blades - x0 + 1)
    ]
    extinction = (0, blades, 0, 0)
    fixation = (core_size, 0, 0, blades)
    states = [
        (core, *distribution)
        for core in range(core_size + 1)
        for distribution in distributions
    ]
    outer = fmpq(outer)
    internal = fmpq(internal)

    def changes(state):
        core, x0, x1, x2 = state
        counts = [x0, x1, x2]
        mutant_blade_vertices = x1 + 2 * x2
        resident_blade_vertices = 2 * x0 + x1
        answer = []
        if core < core_size:
            mutant_mass = core + outer * mutant_blade_vertices
            resident_mass = core_size - core - 1 + outer * resident_blade_vertices
            rate = (
                (core_size - core)
                * fitness
                * mutant_mass
                / (fitness * mutant_mass + resident_mass)
            )
            if rate:
                answer.append(((core + 1, x0, x1, x2), rate))
        if core:
            mutant_mass = core - 1 + outer * mutant_blade_vertices
            resident_mass = core_size - core + outer * resident_blade_vertices
            rate = core * resident_mass / (fitness * mutant_mass + resident_mass)
            if rate:
                answer.append(((core - 1, x0, x1, x2), rate))

        for count, number in enumerate(counts):
            if not number:
                continue
            if count < 2:
                mutant_mass = internal * count + outer * core
                resident_mass = internal * (1 - count) + outer * (core_size - core)
                rate = (
                    number
                    * (2 - count)
                    * fitness
                    * mutant_mass
                    / (fitness * mutant_mass + resident_mass)
                )
                if rate:
                    target = counts.copy()
                    target[count] -= 1
                    target[count + 1] += 1
                    answer.append(((core, *target), rate))
            if count:
                mutant_mass = internal * (count - 1) + outer * core
                resident_mass = internal * (2 - count) + outer * (core_size - core)
                rate = (
                    number
                    * count
                    * resident_mass
                    / (fitness * mutant_mass + resident_mass)
                )
                if rate:
                    target = counts.copy()
                    target[count] -= 1
                    target[count - 1] += 1
                    answer.append(((core, *target), rate))
        return answer

    def multiplicity(state):
        core, x0, x1, x2 = state
        blade_orbits = (
            factorial(blades)
            // (factorial(x0) * factorial(x1) * factorial(x2))
            * 2**x1
        )
        return comb(core_size, core) * blade_orbits

    values = solve_absorbing(states, changes, extinction, fixation)
    masses, mean = level_masses(
        order,
        values,
        state_size=lambda state: state[0] + state[2] + 2 * state[3],
        multiplicity=multiplicity,
    )
    return masses, mean


def check_exact_nonunimodality_counterexample():
    """Falsify a tempting binomial-normalized level-unimodality route."""
    order = 6
    full = (1 << order) - 1
    weights = [[fmpq(0) for _ in range(order)] for _ in range(order)]
    for left, right, weight in (
        (0, 1, 30),
        (0, 2, 4),
        (2, 4, 64),
        (4, 5, 1),
        (5, 3, 1860),
    ):
        weights[left][right] = weights[right][left] = fmpq(weight)

    def changes(state):
        answer = []
        for target in range(order):
            mutant_mass = sum(
                (
                    weights[parent][target]
                    for parent in range(order)
                    if (state >> parent) & 1
                ),
                fmpq(0),
            )
            resident_mass = sum(
                (
                    weights[parent][target]
                    for parent in range(order)
                    if not ((state >> parent) & 1)
                ),
                fmpq(0),
            )
            denominator = 2 * mutant_mass + resident_mass
            if (state >> target) & 1:
                rate = resident_mass / denominator
                target_state = state & ~(1 << target)
            else:
                rate = 2 * mutant_mass / denominator
                target_state = state | (1 << target)
            if rate:
                answer.append((target_state, rate))
        return answer

    values = solve_absorbing(list(range(full + 1)), changes, 0, full)
    masses, _ = level_masses(
        order, values, state_size=int.bit_count, multiplicity=lambda state: 1
    )
    normalized = [
        masses[level - 1] / comb(order - 1, level)
        for level in range(1, order)
    ]
    assert normalized[0] > normalized[1] < normalized[2]
    print(
        "PASS: exact failure of binomial-normalized level unimodality; "
        f"a_3-a_2={float(arb(normalized[2]-normalized[1])):.12g}"
    )


def main():
    windmills = [
        (
            "K7 windmill at r=3/2",
            (100, 10, 1),
            (600, 1200, 1800),
            fmpq(3, 2),
        ),
        (
            "K7 windmill at r=2",
            (100, 10, 1),
            (600, 1200, 1800),
            fmpq(2),
        ),
        (
            "K9 windmill at r=7/4",
            (1, 40, 2400, 200000),
            (9000000, 3800000, 2000000, 920000),
            fmpq(7, 4),
        ),
        (
            "K9 windmill at r=2",
            (1, 40, 2400, 200000),
            (9000000, 3800000, 2000000, 920000),
            fmpq(2),
        ),
        (
            "K11 windmill at r=9/5",
            (1, 6, 120, 3500, 60000),
            (9000000, 2500000, 880000, 410000, 190000),
            fmpq(9, 5),
        ),
        (
            "K11 windmill at r=2",
            (1, 6, 120, 3500, 60000),
            (9000000, 2500000, 880000, 410000, 190000),
            fmpq(2),
        ),
    ]
    for label, outer, internal, fitness in windmills:
        masses, mean, values = heterogeneous_pair_windmill(
            outer, internal, fitness, return_values=True
        )
        check_complementary_levels(label, 1 + 2 * len(outer), fitness, masses)
        check_marked_complementary_levels(
            label, outer, internal, fitness, values
        )
        if fitness == 2:
            assert 2 * mean <= 1 + 2 * len(outer)

    masses, mean = clique_core_identical_pairs(
        core_size=60,
        blades=3,
        outer=fmpq(1, 10**8),
        internal=fmpq(10**10),
    )
    check_complementary_levels("K60 core plus three extreme pairs at r=2", 66, fmpq(2), masses)
    assert 2 * mean <= 66
    print("PASS: all exact r=2 dual means are at most n/2")
    check_exact_nonunimodality_counterexample()


if __name__ == "__main__":
    main()
