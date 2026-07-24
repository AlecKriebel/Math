#!/usr/bin/env python3
"""Discovery-only axisymmetric SDP search for an antipodal-pair belt.

Fixing an antipodal pair +/-e forces every remaining kissing-code point to
have height u=<e,x> in [-1/2,1/2].  This script searches for a positive-kernel
dual bounding the number of points in that belt.  Sampled feasibility is not
a proof; a promising output must be converted to rational Gram factors and
audited on the full semialgebraic domain by an exact verifier.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
from pathlib import Path

import cvxpy as cp
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "experiments" / "search_one_sided_cap_sdp.py"
SPEC = importlib.util.spec_from_file_location("one_sided_base", BASE_PATH)
assert SPEC is not None and SPEC.loader is not None
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)


def feasible_t_interval(u: float, v: float) -> tuple[float, float] | None:
    radius = math.sqrt(max(0.0, (1.0 - u * u) * (1.0 - v * v)))
    low = max(-1.0, u * v - radius)
    high = min(0.5, u * v + radius)
    if low > high + 1e-14:
        return None
    return low, high


def add_segment(
    samples: list[tuple[float, float, float]],
    u: float,
    v: float,
    alphas,
) -> None:
    interval = feasible_t_interval(float(u), float(v))
    if interval is None:
        return
    low, high = interval
    for alpha in alphas:
        samples.append(
            (float(u), float(v), low + float(alpha) * (high - low))
        )


def initial_samples(
    grid: int,
    random_count: int,
    seed: int,
    boundary_grid: int,
    ridge_grid: int,
    ridge_alpha_grid: int,
) -> tuple[list[tuple[float, float, float]], list[float]]:
    off: list[tuple[float, float, float]] = []
    heights = np.linspace(-0.5, 0.5, grid)
    alphas = np.linspace(0.0, 1.0, grid)
    for u in heights:
        for v in heights:
            if v < u:
                continue
            add_segment(off, float(u), float(v), alphas)

    rng = np.random.default_rng(seed)
    for _ in range(random_count):
        u, v = np.sort(rng.uniform(-0.5, 0.5, 2))
        interval = feasible_t_interval(float(u), float(v))
        assert interval is not None
        low, high = interval
        alpha = rng.beta(0.55, 0.55)
        off.append((float(u), float(v), low + float(alpha) * (high - low)))

    # Complete determinant sheets and the contact sheet on a dense height grid.
    boundary_heights = np.linspace(-0.5, 0.5, boundary_grid)
    for u in boundary_heights:
        for v in boundary_heights:
            if v < u:
                continue
            interval = feasible_t_interval(float(u), float(v))
            assert interval is not None
            low, high = interval
            off.extend(
                ((float(u), float(v), low), (float(u), float(v), high))
            )
            if low <= 0.5 <= high:
                off.append((float(u), float(v), 0.5))

    # Resolve both same-sign and mixed-sign symmetry planes throughout their
    # interiors, not only on determinant-zero boundaries.
    ridge_heights = np.linspace(-0.5, 0.5, ridge_grid)
    ridge_alphas = np.unique(
        np.concatenate(
            (
                np.linspace(0.0, 0.2, max(2, ridge_alpha_grid // 2)),
                np.linspace(0.2, 1.0, max(2, ridge_alpha_grid // 2)),
            )
        )
    )
    for u in ridge_heights:
        add_segment(off, float(u), float(u), ridge_alphas)
        a, b = sorted((float(u), float(-u)))
        add_segment(off, a, b, ridge_alphas)

    # The belt walls and equatorial axis are lower-dimensional and are missed
    # almost surely by random samples.  Sample their full t intervals.
    for v in ridge_heights:
        for u in (-0.5, 0.0, 0.5):
            a, b = sorted((float(u), float(v)))
            add_segment(off, a, b, ridge_alphas)

    # Exact duplicate removal reduces redundant conic constraints without
    # changing the deterministic sampled problem.
    off = list(dict.fromkeys(off))
    diag = np.linspace(-0.5, 0.5, max(4 * grid + 1, 101)).tolist()
    return off, diag


def solve(
    degree: int,
    off,
    diag,
    tolerance: float,
    psd_floor: float,
    solver: str,
    verbose: bool,
):
    blocks = [
        cp.Variable((degree - k + 1, degree - k + 1), symmetric=True)
        for k in range(degree + 1)
    ]
    objective_height = cp.Variable()
    constraints = [
        block >> psd_floor * np.eye(block.shape[0]) for block in blocks
    ]
    for u, v, t in off:
        matrices = BASE.coefficient_matrices(degree, u, v, t)
        constraints.append(
            sum(
                cp.sum(cp.multiply(block, matrix))
                for block, matrix in zip(blocks, matrices, strict=True)
            )
            <= -1
        )
    for u in diag:
        matrices = BASE.coefficient_matrices(degree, u, u, 1.0)
        constraints.append(
            sum(
                cp.sum(cp.multiply(block, matrix))
                for block, matrix in zip(blocks, matrices, strict=True)
            )
            <= objective_height
        )
    problem = cp.Problem(cp.Minimize(1 + objective_height), constraints)
    kwargs = {"verbose": verbose}
    if solver == "CLARABEL":
        kwargs.update(
            tol_gap_abs=tolerance,
            tol_feas=tolerance,
            tol_gap_rel=tolerance,
            max_iter=500,
        )
    else:
        kwargs.update(eps=tolerance, max_iters=200_000)
    value = problem.solve(solver=solver, **kwargs)
    return problem.status, value, [block.value for block in blocks]


def audit_random(blocks, count: int, seed: int):
    rng = np.random.default_rng(seed)
    worst = (-math.inf, None)
    for _ in range(count):
        u, v = np.sort(rng.uniform(-0.5, 0.5, 2))
        low, high = feasible_t_interval(float(u), float(v))
        for alpha in (rng.random(), 0.0, 1.0):
            t = low + float(alpha) * (high - low)
            value = BASE.evaluate(blocks, float(u), float(v), t)
            if value > worst[0]:
                worst = value, (float(u), float(v), t)
    diagonal = max(
        (BASE.evaluate(blocks, u, u, 1.0), u)
        for u in np.linspace(-0.5, 0.5, 10_001)
    )
    return worst, diagonal


def audit_special_surfaces(blocks, height_grid: int, alpha_grid: int):
    worst = (-math.inf, None, None)
    heights = np.linspace(-0.5, 0.5, height_grid)
    alphas = np.linspace(0.0, 1.0, alpha_grid)
    for label in ("equal", "opposite", "wall-low", "wall-high", "axis"):
        for u in heights:
            if label == "equal":
                a, b = float(u), float(u)
            elif label == "opposite":
                a, b = sorted((float(u), float(-u)))
            elif label == "wall-low":
                a, b = -0.5, float(u)
            elif label == "wall-high":
                a, b = sorted((0.5, float(u)))
            else:
                a, b = sorted((0.0, float(u)))
            low, high = feasible_t_interval(a, b)
            for alpha in alphas:
                t = low + float(alpha) * (high - low)
                value = BASE.evaluate(blocks, a, b, t)
                if value > worst[0]:
                    worst = value, (a, b, t), label
    return worst


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, default=8)
    parser.add_argument("--grid", type=int, default=9)
    parser.add_argument("--random", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=521001)
    parser.add_argument("--boundary-grid", type=int, default=25)
    parser.add_argument("--ridge-grid", type=int, default=81)
    parser.add_argument("--ridge-alpha-grid", type=int, default=31)
    parser.add_argument("--audit", type=int, default=100000)
    parser.add_argument("--audit-surface-height-grid", type=int, default=401)
    parser.add_argument("--audit-surface-alpha-grid", type=int, default=201)
    parser.add_argument("--tolerance", type=float, default=1e-5)
    parser.add_argument("--psd-floor", type=float, default=1e-4)
    parser.add_argument("--solver", choices=("CLARABEL", "SCS"), default="CLARABEL")
    parser.add_argument("--output", required=True)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    off, diag = initial_samples(
        args.grid,
        args.random,
        args.seed,
        args.boundary_grid,
        args.ridge_grid,
        args.ridge_alpha_grid,
    )
    print(f"samples: off={len(off)} diag={len(diag)}", flush=True)
    status, value, blocks = solve(
        args.degree,
        off,
        diag,
        args.tolerance,
        args.psd_floor,
        args.solver,
        args.verbose,
    )
    print(f"status={status} sampled_objective={value:.12f}", flush=True)
    np.savez(args.output, **{f"F{k}": block for k, block in enumerate(blocks)})
    print(f"saved={args.output}", flush=True)
    worst, diagonal = audit_random(blocks, args.audit, args.seed + 1)
    special = audit_special_surfaces(
        blocks,
        args.audit_surface_height_grid,
        args.audit_surface_alpha_grid,
    )
    global_max = max(worst[0], special[0])
    print(f"random_off_max={worst[0]:.12f} at {worst[1]}", flush=True)
    print(
        f"special_off_max={special[0]:.12f} at {special[1]} "
        f"surface={special[2]}",
        flush=True,
    )
    print(f"dense_diag_max={diagonal[0]:.12f} at {diagonal[1]:.8f}", flush=True)
    print(
        f"audited_rescaled_objective={1-diagonal[0]/global_max:.12f}",
        flush=True,
    )


if __name__ == "__main__":
    main()
