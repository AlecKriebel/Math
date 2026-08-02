#!/usr/bin/env python3
"""Branching-limit search for a dense center with triangle satellites.

Let ``c`` center vertices form a clique and let ``M/c -> mu``.  Satellite
vertex ``v`` has total outer degree ``h_v`` to the center; the actual center
degree is ``D``, so its internal clique degree is
``D-mu*sum(h)``.  The early-mutant limit is one center branching type coupled
to finite-state mutant colonies in otherwise resident triangles.  The PGF
fixed point is solved directly for each update rule.

This calculation includes the resident-satellite load omitted by the simpler
early-escape filter.  A positive survival comparison is still reconnaissance
until post-establishment fixation is controlled.
"""

from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.optimize import differential_evolution

from search_early_escape import local_success


def survival(
    fitness: float,
    delta: float,
    outer_degree: np.ndarray,
    center_degree: float,
    module_ratio: float,
    rule: str,
):
    h = np.asarray(outer_degree, dtype=float)
    internal_center = center_degree - module_ratio * float(h.sum())
    if internal_center <= 0:
        raise ValueError("negative center internal degree")
    triangle_degree = np.array((1.0 + delta, 2.0 * delta, 1.0 + delta))

    if rule == "Bd":
        death = internal_center / center_degree + module_ratio * float(
            np.sum(h / (triangle_degree + h))
        )
        center_birth = fitness * internal_center / center_degree
        module_birth = fitness * module_ratio * h / center_degree
    elif rule == "dB":
        death = 1.0
        center_birth = fitness * internal_center / center_degree
        module_birth = fitness * module_ratio * h / (triangle_degree + h)
    else:
        raise ValueError(rule)

    extinction = 0.0
    singleton_survival = np.zeros(3)
    for _ in range(10000):
        mark = 1.0 - extinction
        _, residual, values = local_success(
            fitness,
            delta,
            h,
            center_degree,
            rule,
            mark_probability=mark,
        )
        if residual > 2e-7:
            raise FloatingPointError(residual)
        singleton_survival = np.array([values[(1 << v) - 1] for v in range(3)])
        new_extinction = death / (
            death
            + center_birth * (1.0 - extinction)
            + float(module_birth @ singleton_survival)
        )
        if abs(new_extinction - extinction) < 2e-13:
            extinction = new_extinction
            break
        extinction = new_extinction
    else:
        raise FloatingPointError("PGF iteration did not converge")

    # Recompute colonies at the converged center-extinction probability.
    _, residual, values = local_success(
        fitness,
        delta,
        h,
        center_degree,
        rule,
        mark_probability=1.0 - extinction,
    )
    if residual > 2e-7:
        raise FloatingPointError(residual)
    singleton_survival = np.array([values[(1 << v) - 1] for v in range(3)])
    uniform = (
        (1.0 - extinction) + module_ratio * float(singleton_survival.sum())
    ) / (1.0 + 3.0 * module_ratio)
    return float(uniform), float(1.0 - extinction), singleton_survival


def decode(vector: np.ndarray):
    delta = math.exp(float(vector[0]))
    h = np.exp(np.asarray(vector[1:4], dtype=float))
    center_degree = math.exp(float(vector[4]))
    capacity = center_degree / float(h.sum())
    fraction = 1.0 / (1.0 + math.exp(-float(vector[5])))
    module_ratio = 0.999 * capacity * fraction
    return delta, h, center_degree, module_ratio


def evaluate(fitness: float, vector: np.ndarray):
    delta, h, center_degree, module_ratio = decode(vector)
    bd = survival(fitness, delta, h, center_degree, module_ratio, "Bd")
    db = survival(fitness, delta, h, center_degree, module_ratio, "dB")
    baseline = 1.0 - 1.0 / fitness
    return (
        min(bd[0] - baseline, db[0] - baseline),
        bd,
        db,
        delta,
        h,
        center_degree,
        module_ratio,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fitness", type=float, default=1.55)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=260)
    parser.add_argument("--popsize", type=int, default=16)
    args = parser.parse_args()

    def objective(vector):
        try:
            return -evaluate(args.fitness, vector)[0]
        except (np.linalg.LinAlgError, FloatingPointError, ValueError, OverflowError):
            return 100.0

    result = differential_evolution(
        objective,
        [(-14.0, 6.0)] * 5 + [(-10.0, 10.0)],
        seed=args.seed,
        maxiter=args.iterations,
        popsize=args.popsize,
        polish=True,
        tol=1e-10,
        workers=1,
        updating="immediate",
        disp=True,
    )
    score, bd, db, delta, h, center_degree, module_ratio = evaluate(
        args.fitness, result.x
    )
    print(f"RESULT r={args.fitness} score={score:+.12g}")
    print(f"rho_branch=({bd[0]:.12g},{db[0]:.12g}) baseline={1-1/args.fitness:.12g}")
    print(f"center_survival=({bd[1]:.12g},{db[1]:.12g})")
    print("satellite_Bd", " ".join(f"{x:.12g}" for x in bd[2]))
    print("satellite_dB", " ".join(f"{x:.12g}" for x in db[2]))
    print(f"delta={delta:.12g} D={center_degree:.12g} mu={module_ratio:.12g}")
    print(f"center_internal={center_degree-module_ratio*h.sum():.12g}")
    print("h", " ".join(f"{x:.12g}" for x in h))


if __name__ == "__main__":
    main()
