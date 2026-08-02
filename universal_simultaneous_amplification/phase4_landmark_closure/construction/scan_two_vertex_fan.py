#!/usr/bin/env python3
"""Generic two-vertex-module fan with two independently weighted spokes.

Each of M modules has vertices A,B joined by a unit edge.  The common hub is
joined to A with weight s_A and to B with weight s_B.  The state is the hub
type and the histogram of the four module configurations.  This contains the
paired windmill (s_A=s_B) and subdivided star (s_B=0) as boundary cases.
"""

from __future__ import annotations

import argparse

import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as spla

from scan_subdivided_fan import baseline, histograms, module, module_index, move


def transitions(state, modules, spokes, fitness, rule):
    hub, counts = state
    n = 2 * modules + 1
    spoke_a, spoke_b = spokes
    spoke_sum = spoke_a + spoke_b
    degrees = (1 + spoke_a, 1 + spoke_b)
    mutant_by_type = [
        sum(counts[index] * module(index)[vertex_type] for index in range(4))
        for vertex_type in (0, 1)
    ]
    mutant_total = hub + sum(mutant_by_type)
    result = []
    if rule == "Bd":
        total_fitness = n + (fitness - 1) * mutant_total
        hub_up = fitness / total_fitness * sum(
            mutant_by_type[x] * spokes[x] / degrees[x] for x in (0, 1)
        )
        hub_down = 1 / total_fitness * sum(
            (modules - mutant_by_type[x]) * spokes[x] / degrees[x] for x in (0, 1)
        )
        if not hub and hub_up:
            result.append(((1, counts), hub_up))
        if hub and hub_down:
            result.append(((0, counts), hub_down))
        for source, multiplicity in enumerate(counts):
            if not multiplicity:
                continue
            types = module(source)
            for x in (0, 1):
                current = types[x]
                other = types[1 - x]
                if not current:
                    rate = multiplicity * fitness / total_fitness * (
                        other / degrees[1 - x]
                        + hub * spokes[x] / (modules * spoke_sum)
                    )
                    new_types = list(types); new_types[x] = 1
                else:
                    rate = multiplicity / total_fitness * (
                        (1 - other) / degrees[1 - x]
                        + (1 - hub) * spokes[x] / (modules * spoke_sum)
                    )
                    new_types = list(types); new_types[x] = 0
                if rate:
                    result.append(((hub, move(counts, source, module_index(*new_types))), rate))
    elif rule == "dB":
        mutant_hub_mass = fitness * sum(mutant_by_type[x] * spokes[x] for x in (0, 1))
        resident_hub_mass = sum((modules - mutant_by_type[x]) * spokes[x] for x in (0, 1))
        if not hub and mutant_hub_mass:
            result.append(((1, counts), mutant_hub_mass / (n * (mutant_hub_mass + resident_hub_mass))))
        if hub and resident_hub_mass:
            result.append(((0, counts), resident_hub_mass / (n * (mutant_hub_mass + resident_hub_mass))))
        for source, multiplicity in enumerate(counts):
            if not multiplicity:
                continue
            types = module(source)
            for x in (0, 1):
                current = types[x]
                other = types[1 - x]
                mutant_mass = fitness * (other + hub * spokes[x])
                resident_mass = (1 - other) + (1 - hub) * spokes[x]
                if not current and mutant_mass:
                    new_types = list(types); new_types[x] = 1
                    rate = multiplicity / n * mutant_mass / (mutant_mass + resident_mass)
                elif current and resident_mass:
                    new_types = list(types); new_types[x] = 0
                    rate = multiplicity / n * resident_mass / (mutant_mass + resident_mass)
                else:
                    continue
                result.append(((hub, move(counts, source, module_index(*new_types))), rate))
    else:
        raise ValueError(rule)
    return result


def fixation(modules, spokes, fitness, rule):
    empty = (0, (modules, 0, 0, 0)); full = (1, (0, 0, 0, modules))
    states = [(h, c) for h in (0, 1) for c in histograms(modules) if (h, c) not in (empty, full)]
    index = {state: i for i, state in enumerate(states)}
    rows, columns, data = [], [], []
    rhs = np.zeros(len(states))
    for state, source in index.items():
        changes = transitions(state, modules, spokes, fitness, rule)
        mass = sum(p for _, p in changes)
        rows.append(source); columns.append(source); data.append(1.0)
        for target, probability in changes:
            probability /= mass
            if target == full:
                rhs[source] += probability
            elif target != empty:
                rows.append(source); columns.append(index[target]); data.append(-probability)
    matrix = sparse.csr_matrix((data, (rows, columns)), shape=(len(states),) * 2)
    values = spla.spsolve(matrix, rhs)
    residual = float(np.max(np.abs(matrix @ values - rhs)))
    initial = [
        (1, (modules, 0, 0, 0)),
        (0, (modules - 1, 0, 1, 0)),
        (0, (modules - 1, 1, 0, 0)),
    ]
    n = 2 * modules + 1
    average = (values[index[initial[0]]] + modules * values[index[initial[1]]] + modules * values[index[initial[2]]]) / n
    return float(average), residual


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--modules", type=int, required=True)
    args = parser.parse_args(); m = args.modules; n = 2 * m + 1
    fitnesses = (1.001, 1.02, 1.05, 1.1, 1.2, 1.5, 2.0)
    best = []
    grid = np.geomspace(0.01, 4.0, 31)
    for constant_a in grid:
        for constant_b in grid:
            spokes = (constant_a / m, constant_b / m)
            values = []
            for fitness in fitnesses:
                for rule in ("Bd", "dB"):
                    value, residual = fixation(m, spokes, fitness, rule)
                    if residual > 2e-8: raise AssertionError(residual)
                    values.append(value - baseline(n, fitness, rule))
            best.append((min(values), constant_a, constant_b, values))
    for score, a, b, values in sorted(best, reverse=True)[:30]:
        print(a, b, score, " ".join(f"{value:+.3e}" for value in values))


if __name__ == "__main__": main()
