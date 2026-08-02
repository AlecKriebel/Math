#!/usr/bin/env python3
"""Exact certificate for a seven-vertex dB amplifier at r=3/2.

The graph is a three-blade windmill.  Vertex 0 is the center and the
three blades are pairs (1,2), (3,4), (5,6).  Both vertices of blade q
join the center with weight b_q and the internal pair has weight a_q:

    b = (100, 10, 1),       a = (600, 1200, 1800).

All arithmetic below is over the rationals.  We independently build the
126-state labelled chain and the 52-state orbit-lumped chain, solve both,
and compare their uniformly initialized fixation probability with K_7.
"""

from __future__ import annotations

from itertools import product

import sympy as sp


R = sp.Rational(3, 2)
SIZE = 7
FULL = (1 << SIZE) - 1
BLADES = ((1, 2), (3, 4), (5, 6))
OUTER = tuple(map(sp.Rational, (100, 10, 1)))
INTERNAL = tuple(map(sp.Rational, (600, 1200, 1800)))


def graph_weights():
    weights = [[sp.Rational(0) for _ in range(SIZE)] for _ in range(SIZE)]
    for (left, right), outer, internal in zip(BLADES, OUTER, INTERNAL):
        weights[left][right] = weights[right][left] = internal
        weights[0][left] = weights[left][0] = outer
        weights[0][right] = weights[right][0] = outer
    return weights


def micro_changes(mask: int, weights):
    """Unnormalised type-changing dB rates; the common factor 1/7 is omitted."""
    answer = []
    for target in range(SIZE):
        mutant_mass = sum(
            weights[parent][target]
            for parent in range(SIZE)
            if mask & (1 << parent)
        )
        resident_mass = sum(
            weights[parent][target]
            for parent in range(SIZE)
            if not (mask & (1 << parent))
        )
        denominator = R * mutant_mass + resident_mass
        assert denominator > 0
        if mask & (1 << target):
            rate = resident_mass / denominator
            new_mask = mask & ~(1 << target)
        else:
            rate = R * mutant_mass / denominator
            new_mask = mask | (1 << target)
        if rate:
            answer.append((new_mask, sp.cancel(rate)))
    return answer


def orbit(mask: int):
    return (
        int(bool(mask & 1)),
        *(int(bool(mask & (1 << left))) + int(bool(mask & (1 << right)))
          for left, right in BLADES),
    )


def lumped_changes(state):
    """Unnormalised changing rates derived directly from the dB rule."""
    center, *counts = state
    answer = []

    mutant_mass = sum(outer * count for outer, count in zip(OUTER, counts))
    resident_mass = sum(outer * (2 - count) for outer, count in zip(OUTER, counts))
    denominator = R * mutant_mass + resident_mass
    if center == 0 and mutant_mass:
        answer.append(((1, *counts), sp.cancel(R * mutant_mass / denominator)))
    if center == 1 and resident_mass:
        answer.append(((0, *counts), sp.cancel(resident_mass / denominator)))

    for blade, (count, outer, internal) in enumerate(
        zip(counts, OUTER, INTERNAL)
    ):
        if count < 2:
            # For a resident target, its partner is mutant exactly when count=1.
            mutant_mass = internal * int(count == 1) + outer * center
            resident_mass = internal * int(count == 0) + outer * (1 - center)
            denominator = R * mutant_mass + resident_mass
            rate = (2 - count) * R * mutant_mass / denominator
            if rate:
                updated = list(counts)
                updated[blade] += 1
                answer.append(((center, *updated), sp.cancel(rate)))
        if count > 0:
            # For a mutant target, its partner is mutant exactly when count=2.
            mutant_mass = internal * int(count == 2) + outer * center
            resident_mass = internal * int(count == 1) + outer * (1 - center)
            denominator = R * mutant_mass + resident_mass
            rate = count * resident_mass / denominator
            if rate:
                updated = list(counts)
                updated[blade] -= 1
                answer.append(((center, *updated), sp.cancel(rate)))
    return answer


def aggregate(changes, map_state):
    total = {}
    for target, rate in changes:
        key = map_state(target)
        total[key] = sp.cancel(total.get(key, 0) + rate)
    return total


def solve_chain(states, changes, extinction, fixation):
    transient = [state for state in states if state not in (extinction, fixation)]
    index = {state: row for row, state in enumerate(transient)}
    matrix = sp.eye(len(transient))
    rhs = sp.zeros(len(transient), 1)
    for state, row in index.items():
        outgoing = changes(state)
        total = sum(rate for _, rate in outgoing)
        assert total > 0
        for target, rate in outgoing:
            probability = sp.cancel(rate / total)
            assert probability > 0
            if target == fixation:
                rhs[row] += probability
            elif target != extinction:
                matrix[row, index[target]] -= probability
    solution = tuple(next(iter(sp.linsolve((matrix, rhs)))))
    assert matrix * sp.Matrix(solution) == rhs
    return index, solution


def main():
    weights = graph_weights()
    assert all(sum(row) > 0 for row in weights)
    # Every vertex reaches 0 in at most one edge, so the support is connected.
    assert all(weights[0][vertex] > 0 for vertex in range(1, SIZE))

    # Exact strong lumpability check: aggregate every labelled state's rates
    # and compare with the closed count-state equations.
    for mask in range(1 << SIZE):
        micro = aggregate(micro_changes(mask, weights), orbit)
        macro = aggregate(lumped_changes(orbit(mask)), lambda state: state)
        assert micro == macro, (mask, micro, macro)

    macro_states = list(product(range(2), range(3), range(3), range(3)))
    macro_extinction = (0, 0, 0, 0)
    macro_fixation = (1, 2, 2, 2)
    macro_index, macro_solution = solve_chain(
        macro_states, lumped_changes, macro_extinction, macro_fixation
    )
    center_singleton = macro_solution[macro_index[(1, 0, 0, 0)]]
    blade_singletons = [
        macro_solution[
            macro_index[(0, *(1 if candidate == blade else 0 for candidate in range(3)))]
        ]
        for blade in range(3)
    ]
    rho_macro = sp.cancel((center_singleton + 2 * sum(blade_singletons)) / SIZE)

    micro_states = list(range(1 << SIZE))
    micro_index, micro_solution = solve_chain(
        micro_states,
        lambda mask: micro_changes(mask, weights),
        0,
        FULL,
    )
    rho_micro = sp.cancel(
        sum(micro_solution[micro_index[1 << vertex]] for vertex in range(SIZE))
        / SIZE
    )
    assert rho_micro == rho_macro

    complete = sp.cancel(
        sp.Rational(SIZE - 1, SIZE)
        * (1 - 1 / R)
        / (1 - R ** (-(SIZE - 1)))
    )
    excess = sp.cancel(rho_macro - complete)
    assert excess > 0

    print("PASS exact labelled/lumped transition agreement: 128 states")
    print("PASS exact absorbing solves: 126 and 52 transient states")
    print(f"rho_dB(G,3/2) = {rho_macro}")
    print(f"rho_dB(K_7,3/2) = {complete}")
    print(f"positive excess = {excess}")
    print(f"decimal rho = {sp.N(rho_macro, 16)}")
    print(f"decimal excess = {sp.N(excess, 16)}")


if __name__ == "__main__":
    main()
