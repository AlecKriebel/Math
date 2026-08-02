#!/usr/bin/env python3
"""Exact certificate for an eleven-vertex dB amplifier at r=9/5.

This is a five-blade windmill.  Ordered by blade, the two equal center edges
and the internal blade edge have weights

    outer    = (1, 6, 120, 3500, 60000),
    internal = (9000000, 2500000, 880000, 410000, 190000).

The program checks all 2048 labelled transition rows against the 486-state
blade-count chain, then solves the 484 transient equations over Q using FLINT.
"""

from __future__ import annotations

from itertools import product

from flint import arb, fmpq, fmpq_mat


R = fmpq(9, 5)
BLADES = 5
SIZE = 2 * BLADES + 1
PAIRS = tuple((2 * blade + 1, 2 * blade + 2) for blade in range(BLADES))
OUTER = (1, 6, 120, 3500, 60000)
INTERNAL = (9000000, 2500000, 880000, 410000, 190000)


def graph_weights():
    weights = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
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
            rate = fmpq(resident_mass) / denominator
            target_mask = mask & ~(1 << target)
        else:
            rate = R * mutant_mass / denominator
            target_mask = mask | (1 << target)
        if rate:
            changes.append((target_mask, rate))
    return changes


def macro_changes(state):
    center, *counts = state
    changes = []
    mutant_mass = sum(outer * count for outer, count in zip(OUTER, counts))
    resident_mass = sum(outer * (2 - count) for outer, count in zip(OUTER, counts))
    denominator = R * mutant_mass + resident_mass
    if center == 0 and mutant_mass:
        changes.append(((1, *counts), R * mutant_mass / denominator))
    if center == 1 and resident_mass:
        changes.append(((0, *counts), fmpq(resident_mass) / denominator))

    for blade, (count, outer, internal) in enumerate(zip(counts, OUTER, INTERNAL)):
        if count < 2:
            mutant_mass = internal * int(count == 1) + outer * center
            resident_mass = internal * int(count == 0) + outer * (1 - center)
            denominator = R * mutant_mass + resident_mass
            rate = (2 - count) * R * mutant_mass / denominator
            if rate:
                updated = list(counts); updated[blade] += 1
                changes.append(((center, *updated), rate))
        if count > 0:
            mutant_mass = internal * int(count == 2) + outer * center
            resident_mass = internal * int(count == 1) + outer * (1 - center)
            denominator = R * mutant_mass + resident_mass
            rate = count * resident_mass / denominator
            if rate:
                updated = list(counts); updated[blade] -= 1
                changes.append(((center, *updated), rate))
    return changes


def aggregate(changes, map_target):
    answer = {}
    for target, rate in changes:
        key = map_target(target)
        answer[key] = answer.get(key, fmpq(0)) + rate
    return answer


def solve_macro():
    extinction = (0,) * (BLADES + 1)
    fixation_state = (1,) + (2,) * BLADES
    transient = [
        state
        for state in product(range(2), *([range(3)] * BLADES))
        if state not in (extinction, fixation_state)
    ]
    index = {state: row for row, state in enumerate(transient)}
    matrix = fmpq_mat(len(transient), len(transient))
    rhs = fmpq_mat(len(transient), 1)
    for state, row in index.items():
        changes = macro_changes(state)
        changing = sum((rate for _, rate in changes), fmpq(0))
        assert changing > 0
        matrix[row, row] = 1
        for target, rate in changes:
            probability = rate / changing
            if target == fixation_state:
                rhs[row, 0] += probability
            elif target != extinction:
                matrix[row, index[target]] -= probability
    solution = matrix.solve(rhs)
    assert matrix * solution == rhs
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
    center_singleton = solution[index[(1,) + (0,) * BLADES], 0]
    blade_singletons = [
        solution[index[(0,) + tuple(int(q == blade) for q in range(BLADES))], 0]
        for blade in range(BLADES)
    ]
    rho = (
        center_singleton
        + 2 * sum(blade_singletons, fmpq(0))
    ) / SIZE
    complete = (
        fmpq(SIZE - 1, SIZE)
        * (1 - 1 / R)
        / (1 - R ** (-(SIZE - 1)))
    )
    excess = rho - complete
    assert complete == fmpq(1937102445, 4780900817)
    assert excess > 0

    print("PASS exact labelled/lumped transition agreement: 2048 states")
    print("PASS exact orbit solve: 484 transient states")
    print(f"rho_dB(K_11,9/5) = {complete}")
    print(f"decimal rho_dB(G,9/5) = {float(arb(rho)):.18g}")
    print(f"decimal positive excess = {float(arb(excess)):.18g}")
    print("exact excess height in bits =", excess.height_bits())


if __name__ == "__main__":
    main()
