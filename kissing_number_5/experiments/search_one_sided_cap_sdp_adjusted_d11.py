#!/usr/bin/env python3
"""Adjusted degree-11 one-sided cap-SDP discovery search.

This is a discovery program, not a verifier.  The first degree-11 candidate
missed an interior ridge on the symmetry plane u=v.  This version adds a
dense tensor mesh on that plane and batches all sampled linear inequalities
into matrix products so that the enlarged problem remains tractable.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import cvxpy as cp
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "experiments" / "search_one_sided_cap_sdp.py"
SPEC = importlib.util.spec_from_file_location("one_sided_base", BASE_PATH)
assert SPEC is not None and SPEC.loader is not None
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)


def coefficient_row(degree: int, u: float, v: float, t: float) -> np.ndarray:
    return np.concatenate(
        [
            matrix.reshape(-1)
            for matrix in BASE.coefficient_matrices(degree, u, v, t)
        ]
    )


def add_symmetric_interior_mesh(
    off: list[tuple[float, float, float]],
    u_grid: int,
    alpha_grid: int,
) -> None:
    """Add u=v points, with extra resolution near the previously missed ridge."""

    maximum_height = np.sqrt(3.0) / 2.0
    heights = np.unique(
        np.concatenate(
            (
                np.linspace(0.0, 0.25, max(2, 2 * u_grid // 3)),
                np.linspace(0.25, maximum_height, max(2, u_grid // 3)),
            )
        )
    )
    alphas = np.unique(
        np.concatenate(
            (
                np.linspace(0.0, 0.2, max(2, 3 * alpha_grid // 4)),
                np.linspace(0.2, 1.0, max(2, alpha_grid // 4)),
            )
        )
    )
    for u in heights:
        interval = BASE.feasible_t_interval(float(u), float(u))
        if interval is None:
            continue
        low, high = interval
        for alpha in alphas:
            off.append(
                (
                    float(u),
                    float(u),
                    low + float(alpha) * (high - low),
                )
            )


def solve_batched(
    degree: int,
    off: list[tuple[float, float, float]],
    diag: list[float],
    tolerance: float,
    psd_floor: float,
    warm_start_path: str,
    verbose: bool,
    formulation: str,
):
    blocks = [
        cp.Variable((degree - k + 1, degree - k + 1), symmetric=True)
        for k in range(degree + 1)
    ]
    objective_height = cp.Variable()
    constraints = [
        block >> psd_floor * np.eye(block.shape[0]) for block in blocks
    ]
    if formulation == "batched":
        block_vector = cp.hstack(
            [
                cp.reshape(block, (block.shape[0] ** 2,), order="C")
                for block in blocks
            ]
        )
        off_rows = np.vstack(
            [coefficient_row(degree, u, v, t) for u, v, t in off]
        )
        diagonal_rows = np.vstack(
            [coefficient_row(degree, u, u, 1.0) for u in diag]
        )
        constraints.extend(
            (
                off_rows @ block_vector <= -1,
                diagonal_rows @ block_vector <= objective_height,
            )
        )
    else:
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
    if warm_start_path:
        source = np.load(warm_start_path)
        for k, block in enumerate(blocks):
            block.value = source[f"F{k}"]
    value = problem.solve(
        solver="CLARABEL",
        verbose=verbose,
        warm_start=bool(warm_start_path),
        tol_gap_abs=tolerance,
        tol_feas=tolerance,
        tol_gap_rel=tolerance,
        max_iter=500,
    )
    return problem.status, value, [block.value for block in blocks]


def audit_symmetric_plane(blocks, u_grid: int, alpha_grid: int):
    worst = (-np.inf, None)
    maximum_height = np.sqrt(3.0) / 2.0
    for u in np.linspace(0.0, maximum_height, u_grid):
        interval = BASE.feasible_t_interval(float(u), float(u))
        if interval is None:
            continue
        low, high = interval
        for alpha in np.linspace(0.0, 1.0, alpha_grid):
            t = low + float(alpha) * (high - low)
            value = BASE.evaluate(blocks, float(u), float(u), t)
            if value > worst[0]:
                worst = value, (float(u), float(u), t)
    return worst


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=511041)
    parser.add_argument("--random", type=int, default=5000)
    parser.add_argument("--grid", type=int, default=10)
    parser.add_argument("--full-boundary-grid", type=int, default=31)
    parser.add_argument("--symmetric-u-grid", type=int, default=301)
    parser.add_argument("--symmetric-alpha-grid", type=int, default=81)
    parser.add_argument("--diagonal-grid", type=int, default=401)
    parser.add_argument("--audit", type=int, default=200000)
    parser.add_argument("--audit-symmetric-u-grid", type=int, default=1001)
    parser.add_argument("--audit-symmetric-alpha-grid", type=int, default=501)
    parser.add_argument("--tolerance", type=float, default=1e-5)
    parser.add_argument("--psd-floor", type=float, default=1e-4)
    parser.add_argument("--warm-start", default="")
    parser.add_argument(
        "--formulation", choices=("batched", "scalar"), default="batched"
    )
    parser.add_argument("--output", required=True)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    degree = 11
    off, _ = BASE.initial_samples(
        args.grid, args.random, args.seed, args.full_boundary_grid
    )
    add_symmetric_interior_mesh(
        off, args.symmetric_u_grid, args.symmetric_alpha_grid
    )
    diag = np.linspace(0.0, 1.0, args.diagonal_grid).tolist()
    print(f"samples: off={len(off)} diag={len(diag)}", flush=True)
    status, value, blocks = solve_batched(
        degree,
        off,
        diag,
        args.tolerance,
        args.psd_floor,
        args.warm_start,
        args.verbose,
        args.formulation,
    )
    print(f"status={status} sampled_objective={value:.12f}", flush=True)
    np.savez(args.output, **{f"F{k}": block for k, block in enumerate(blocks)})
    print(f"saved={args.output}", flush=True)

    worst, diagonal = BASE.audit_random(blocks, args.audit, args.seed + 1)
    symmetric = audit_symmetric_plane(
        blocks,
        args.audit_symmetric_u_grid,
        args.audit_symmetric_alpha_grid,
    )
    print(f"random_off_max={worst[0]:.12f} at {worst[1]}", flush=True)
    print(f"symmetric_off_max={symmetric[0]:.12f} at {symmetric[1]}", flush=True)
    print(f"dense_diag_max={diagonal[0]:.12f} at {diagonal[1]:.8f}", flush=True)
    global_sample_max = max(worst[0], symmetric[0])
    print(
        "audited_rescaled_objective="
        f"{1-diagonal[0]/global_sample_max:.12f}",
        flush=True,
    )


if __name__ == "__main__":
    main()
