#!/usr/bin/env python3
"""Exact certificate for a nine-vertex dB amplifier at r=7/4.

The graph is a four-blade windmill.  Each blade is a pair of exchangeable
vertices.  The center weights and internal blade weights, ordered from blade
zero through blade three, are

    outer    = (1, 40, 2400, 200000),
    internal = (9000000, 3800000, 2000000, 920000).

The verifier constructs all 512 labelled-state transition rows and checks
their aggregation against the 162 orbit states.  It then solves the 160
transient orbit equations exactly over Q and compares with K_9.
"""

from __future__ import annotations

from itertools import product

import sympy as sp


R = sp.Rational(7, 4)
BLADES = 4
SIZE = 2 * BLADES + 1
FULL = (1 << SIZE) - 1
PAIRS = tuple((2 * blade + 1, 2 * blade + 2) for blade in range(BLADES))
OUTER = tuple(map(sp.Integer, (1, 40, 2400, 200000)))
INTERNAL = tuple(map(sp.Integer, (9000000, 3800000, 2000000, 920000)))


def graph_weights():
    weights = [[sp.Integer(0) for _ in range(SIZE)] for _ in range(SIZE)]
    for (left, right), outer, internal in zip(PAIRS, OUTER, INTERNAL):
        weights[0][left] = weights[left][0] = outer
        weights[0][right] = weights[right][0] = outer
        weights[left][right] = weights[right][left] = internal
    return weights


def orbit(mask: int):
    return (
        int(bool(mask & 1)),
        *(int(bool(mask & (1 << left))) + int(bool(mask & (1 << right)))
          for left, right in PAIRS),
    )


def micro_changes(mask: int, weights):
    changes = []
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
            target_mask = mask & ~(1 << target)
        else:
            rate = R * mutant_mass / denominator
            target_mask = mask | (1 << target)
        if rate:
            changes.append((target_mask, sp.cancel(rate)))
    return changes


def macro_changes(state):
    center, *counts = state
    changes = []
    mutant_mass = sum(outer * count for outer, count in zip(OUTER, counts))
    resident_mass = sum(outer * (2 - count) for outer, count in zip(OUTER, counts))
    denominator = R * mutant_mass + resident_mass
    if center == 0 and mutant_mass:
        changes.append(((1, *counts), sp.cancel(R * mutant_mass / denominator)))
    if center == 1 and resident_mass:
        changes.append(((0, *counts), sp.cancel(resident_mass / denominator)))

    for blade, (count, outer, internal) in enumerate(zip(counts, OUTER, INTERNAL)):
        if count < 2:
            mutant_mass = internal * int(count == 1) + outer * center
            resident_mass = internal * int(count == 0) + outer * (1 - center)
            denominator = R * mutant_mass + resident_mass
            rate = (2 - count) * R * mutant_mass / denominator
            if rate:
                updated = list(counts); updated[blade] += 1
                changes.append(((center, *updated), sp.cancel(rate)))
        if count > 0:
            mutant_mass = internal * int(count == 2) + outer * center
            resident_mass = internal * int(count == 1) + outer * (1 - center)
            denominator = R * mutant_mass + resident_mass
            rate = count * resident_mass / denominator
            if rate:
                updated = list(counts); updated[blade] -= 1
                changes.append(((center, *updated), sp.cancel(rate)))
    return changes


def aggregate(changes, map_target):
    answer = {}
    for target, rate in changes:
        key = map_target(target)
        answer[key] = sp.cancel(answer.get(key, 0) + rate)
    return answer


def solve_macro():
    extinction = (0,) * (BLADES + 1)
    fixation_state = (1,) + (2,) * BLADES
    all_states = list(product(range(2), *([range(3)] * BLADES)))
    transient = [state for state in all_states if state not in (extinction, fixation_state)]
    index = {state: row for row, state in enumerate(transient)}
    entries = {}
    rhs = [sp.Integer(0)] * len(transient)
    for state, row in index.items():
        changes = macro_changes(state)
        changing = sum(rate for _, rate in changes)
        assert changing > 0
        entries[(row, row)] = sp.Integer(1)
        for target, rate in changes:
            probability = sp.cancel(rate / changing)
            if target == fixation_state:
                rhs[row] += probability
            elif target != extinction:
                column = index[target]
                entries[(row, column)] = entries.get((row, column), 0) - probability
    matrix = sp.MutableSparseMatrix(len(transient), len(transient), entries)
    solution = tuple(next(iter(sp.linsolve((matrix, sp.Matrix(rhs))))))
    assert matrix * sp.Matrix(solution) == sp.Matrix(rhs)
    return index, solution


def main():
    weights = graph_weights()
    assert all(sum(row) > 0 for row in weights)
    assert all(weights[0][vertex] > 0 for vertex in range(1, SIZE))

    for mask in range(1 << SIZE):
        labelled = aggregate(micro_changes(mask, weights), orbit)
        lumped = aggregate(macro_changes(orbit(mask)), lambda state: state)
        assert labelled == lumped, (mask, labelled, lumped)

    index, solution = solve_macro()
    center_singleton = solution[index[(1,) + (0,) * BLADES]]
    blade_singletons = [
        solution[index[(0,) + tuple(int(q == blade) for q in range(BLADES))]]
        for blade in range(BLADES)
    ]
    rho = sp.cancel((center_singleton + 2 * sum(blade_singletons)) / SIZE)
    complete = sp.cancel(
        sp.Rational(SIZE - 1, SIZE)
        * (1 - 1 / R)
        / (1 - R ** (-(SIZE - 1)))
    )
    excess = sp.cancel(rho - complete)
    assert complete == sp.Rational(6588344, 17097795)
    assert excess > 0

    print("PASS exact labelled/lumped transition agreement: 512 states")
    print("PASS exact orbit solve: 160 transient states")
    print(f"rho_dB(K_9,7/4) = {complete}")
    print(f"decimal rho_dB(G,7/4) = {sp.N(rho, 18)}")
    print(f"decimal positive excess = {sp.N(excess, 18)}")
    print(
        "exact excess numerator/denominator digits =",
        len(str(sp.numer(excess))), len(str(sp.denom(excess))),
    )


if __name__ == "__main__":
    main()
