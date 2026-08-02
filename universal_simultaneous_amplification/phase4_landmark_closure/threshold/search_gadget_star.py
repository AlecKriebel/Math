#!/usr/bin/env python3
"""Search internal gadgets for a separated star-of-gadgets construction.

Cross-gadget edges are complete bipartite and asymptotically weaker than every
internal edge.  The script first solves each internal subset chain directly,
then evaluates the exact limiting star-chain formula.  Floating-point search
results remain reconnaissance until their timescale limit and signs are proved.
"""

from __future__ import annotations

import argparse
import math
import random
from collections import defaultdict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "phase3_asymptotic"))
from scan_lumpable import _gauss_seidel  # noqa: E402


Matrix = list[list[float]]


def fixation_singletons(weights: Matrix, fitness: float, rule: str) -> list[float]:
    n = len(weights)
    degree = [sum(row) for row in weights]
    full = (1 << n) - 1
    states = [tuple((mask >> i) & 1 for i in range(n)) for mask in range(1 << n)]
    rows: list[list[tuple[int, float]]] = []
    for mask in range(1 << n):
        if mask in (0, full):
            rows.append([])
            continue
        changes: dict[int, float] = defaultdict(float)
        mutant_count = mask.bit_count()
        if rule == "Bd":
            total = n + (fitness - 1.0) * mutant_count
            for parent in range(n):
                parent_mutant = bool(mask >> parent & 1)
                parent_fitness = fitness if parent_mutant else 1.0
                for target, weight in enumerate(weights[parent]):
                    if not weight or parent_mutant == bool(mask >> target & 1):
                        continue
                    new = mask | (1 << target) if parent_mutant else mask & ~(1 << target)
                    changes[new] += parent_fitness * weight / (total * degree[parent])
        elif rule == "dB":
            for target in range(n):
                target_mutant = bool(mask >> target & 1)
                mutant_mass = sum(
                    weights[parent][target]
                    for parent in range(n)
                    if mask >> parent & 1
                )
                resident_mass = degree[target] - mutant_mass
                denominator = fitness * mutant_mass + resident_mass
                if target_mutant and resident_mass:
                    changes[mask & ~(1 << target)] += resident_mass / (n * denominator)
                elif not target_mutant and mutant_mass:
                    changes[mask | (1 << target)] += fitness * mutant_mass / (n * denominator)
        else:
            raise ValueError(rule)
        mass = sum(changes.values())
        rows.append([(target, p / mass) for target, p in changes.items()])
    values, _, _ = _gauss_seidel(states, rows, 0, full, tolerance=2e-13)
    return [values[1 << i] for i in range(n)]


def gadget_parameters(weights: Matrix, fitness: float) -> tuple[float, float, float, float]:
    """Return initial establishment and effective-selection data for both rules."""
    degree = [sum(row) for row in weights]
    n = len(weights)
    bd_forward = fixation_singletons(weights, fitness, "Bd")
    bd_reverse = fixation_singletons(weights, 1.0 / fitness, "Bd")
    db_forward = fixation_singletons(weights, fitness, "dB")
    db_reverse = fixation_singletons(weights, 1.0 / fitness, "dB")
    a_bd = sum(bd_forward) / n
    b_bd = sum(bd_reverse) / n
    a_db_initial = sum(db_forward) / n
    inverse_degree_total = sum(1.0 / d for d in degree)
    a_db_invade = sum(x / d for x, d in zip(db_forward, degree)) / inverse_degree_total
    b_db_invade = sum(x / d for x, d in zip(db_reverse, degree)) / inverse_degree_total
    q_bd = fitness * a_bd / b_bd
    q_db = fitness * fitness * a_db_invade / b_db_invade
    return a_bd, a_db_initial, q_bd, q_db


def limiting_deltas(
    parameters: tuple[float, float, float, float], fitness: float, z: float
) -> tuple[float, float]:
    """Return limiting graph-minus-large-complete deltas for a fixed scale ratio."""
    a_bd, a_db_initial, q_bd, q_db = parameters
    gamma_bd = (q_bd + z) / (q_bd * (q_bd * z + 1.0))
    gamma_db = (q_db * z + 1.0) / (q_db * (q_db + z))
    macro_bd = max(0.0, 1.0 - gamma_bd)
    macro_db = max(0.0, 1.0 - gamma_db)
    baseline = 1.0 - 1.0 / fitness
    return a_bd * macro_bd - baseline, a_db_initial * macro_db - baseline


def path_weights(edge_weights: list[float]) -> Matrix:
    n = len(edge_weights) + 1
    weights = [[0.0] * n for _ in range(n)]
    for i, value in enumerate(edge_weights):
        weights[i][i + 1] = weights[i + 1][i] = value
    return weights


def random_reflected_gadget(n: int, rng: random.Random) -> Matrix:
    orbits: dict[tuple[tuple[int, int], ...], float] = {}
    weights = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            orbit = tuple(sorted(((i, j), (n - 1 - j, n - 1 - i))))
            if orbit not in orbits:
                # A substantial fraction of near-zero values discovers sparse limits.
                orbits[orbit] = math.exp(rng.uniform(-7.0, 7.0))
            weights[i][j] = weights[j][i] = orbits[orbit]
    return weights


def scan(n: int, fitness: float, samples: int, seed: int) -> None:
    rng = random.Random(seed)
    best: list[tuple[float, float, tuple[float, float], Matrix]] = []
    z_values = [math.exp(-5.0 + 10.0 * i / 100) for i in range(101)]
    candidates = [path_weights([5.0, 1.0, 1.0, 5.0])] if n == 5 else []
    candidates.extend(random_reflected_gadget(n, rng) for _ in range(samples))
    for sample, weights in enumerate(candidates):
        parameters = gadget_parameters(weights, fitness)
        for z in z_values:
            delta = limiting_deltas(parameters, fitness, z)
            record = (min(delta), z, delta, weights)
            best.append(record)
        best.sort(reverse=True, key=lambda item: item[0])
        del best[30:]
        if sample % 25 == 0 or best[0][0] > 0:
            score, z, delta, _ = best[0]
            print(
                f"sample={sample} score={score:+.10g} z={z:.8g} "
                f"Bd={delta[0]:+.10g} dB={delta[1]:+.10g}",
                flush=True,
            )
        if best[0][0] > 1e-8:
            break
    score, z, delta, weights = best[0]
    print("BEST", score, z, delta)
    for row in weights:
        print(" ".join(f"{x:.12g}" for x in row))


def star_macro_singletons(
    module_count: int, effective_fitness: float, scale_ratio: float, orientation: str
) -> tuple[float, float]:
    """Leaf- and center-start fixation in the effective two-state star chain."""
    m, q, z = module_count, effective_fitness, scale_ratio
    q = min(1.0e50, max(1.0e-50, q))
    source_a = q * z / (q * z + 1.0)
    source_b = q / (q + z)
    if orientation == "source":
        a, b = source_a, source_b
    elif orientation == "target":
        a, b = source_b, source_a
    else:
        raise ValueError(orientation)
    gamma = (1.0 - a) / b
    # D = a(1+gamma+...+gamma^(m-2))+gamma^(m-1).
    power = 1.0
    denominator = 0.0
    for _ in range(max(0, m - 1)):
        denominator += a * power
        power *= gamma
    denominator += power
    return a / denominator, b / denominator


def hierarchy_fixation(
    fitness: float, module_count: int, scale_ratios: list[float]
) -> tuple[float, float]:
    """Separated-scale recursive stars built from a two-vertex base module."""
    r, m = fitness, module_count
    # Uniform forward/reverse fixation; nu denotes inverse-degree invasion law.
    bd_a = r / (r + 1.0)
    db_a = db_nu_a = 0.5
    q_bd = q_db = r * r
    for z in scale_ratios:
        leaf_a, center_a = star_macro_singletons(m, q_bd, z, "source")
        leaf_b, center_b = star_macro_singletons(m, 1.0 / q_bd, z, "source")
        macro_a = (m * leaf_a + center_a) / (m + 1.0)
        macro_b = (m * leaf_b + center_b) / (m + 1.0)
        bd_a *= macro_a
        q_bd = min(1.0e50, q_bd * macro_a / max(macro_b, 1.0e-300))

        leaf_a, center_a = star_macro_singletons(m, q_db, z, "target")
        leaf_b, center_b = star_macro_singletons(m, 1.0 / q_db, z, "target")
        uniform_a = (m * leaf_a + center_a) / (m + 1.0)
        nu_a = (m * leaf_a + center_a / z) / (m + 1.0 / z)
        nu_b = (m * leaf_b + center_b / z) / (m + 1.0 / z)
        db_a *= uniform_a
        db_nu_a *= nu_a
        q_db = min(1.0e50, q_db * nu_a / max(nu_b, 1.0e-300))
    return bd_a, db_a


def scan_hierarchy(fitness: float, samples: int, seed: int) -> None:
    rng = random.Random(seed)
    baseline = 1.0 - 1.0 / fitness
    best = None
    for sample in range(samples):
        m = rng.choice((2, 3, 4, 5, 8, 12))
        period = rng.choice((1, 2, 3, 4))
        pattern = [math.exp(rng.uniform(-4.0, 4.0)) for _ in range(period)]
        levels = rng.choice((4, 6, 8, 10, 12, 16))
        ratios = [pattern[i % period] for i in range(levels)]
        values = hierarchy_fixation(fitness, m, ratios)
        delta = values[0] - baseline, values[1] - baseline
        record = min(delta), m, pattern, levels, delta, values
        if best is None or record[0] > best[0]:
            best = record
            print("HIERARCHY", sample, best, flush=True)
        if record[0] > 1e-10:
            break


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--fitness", type=float, default=1.1)
    parser.add_argument("--samples", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--hierarchy", action="store_true")
    args = parser.parse_args()
    if args.hierarchy:
        scan_hierarchy(args.fitness, args.samples, args.seed)
    else:
        scan(args.n, args.fitness, args.samples, args.seed)


if __name__ == "__main__":
    main()
