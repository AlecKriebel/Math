#!/usr/bin/env python3
"""Discovery-only cutting-plane SDP for one-sided dimension-five codes.

This script searches for the matrix polynomial in Bachoc--Vallentin's
cap-code dual.  It samples the full semialgebraic pair domain, so its output
is *not* a proof.  A useful numerical solution must subsequently be converted
to an exact SOS certificate.
"""

from __future__ import annotations

import argparse
import math

import cvxpy as cp
import numpy as np


def gegenbauer_values(dimension: int, degree: int, x: float) -> np.ndarray:
    """Normalized zonal polynomials P_0,...,P_degree on S^(dimension-1)."""

    values = np.empty(degree + 1)
    values[0] = 1.0
    if degree:
        values[1] = x
    for k in range(2, degree + 1):
        values[k] = (
            (2 * k + dimension - 4) * x * values[k - 1]
            - (k - 1) * values[k - 2]
        ) / (k + dimension - 3)
    return values


def q_values(degree: int, u: float, v: float, t: float) -> np.ndarray:
    """Polynomial Q_k^4(u,v,t), k=0,...,degree."""

    values = np.empty(degree + 1)
    values[0] = 1.0
    if degree:
        values[1] = t - u * v
    radial = (1.0 - u * u) * (1.0 - v * v)
    delta = t - u * v
    for k in range(2, degree + 1):
        values[k] = (
            2 * k * delta * values[k - 1]
            - (k - 1) * radial * values[k - 2]
        ) / (k + 1)
    return values


def coefficient_matrices(
    degree: int, u: float, v: float, t: float
) -> list[np.ndarray]:
    """Modified symmetrized Y_k^5 matrices (normalizing lambdas omitted)."""

    q = q_values(degree, u, v, t)
    answer = []
    for k in range(degree + 1):
        size = degree - k + 1
        pu = gegenbauer_values(5 + 2 * k, size - 1, u)
        pv = gegenbauer_values(5 + 2 * k, size - 1, v)
        answer.append(q[k] * (np.outer(pu, pv) + np.outer(pv, pu)) / 2)
    return answer


def feasible_t_interval(u: float, v: float) -> tuple[float, float] | None:
    radius = math.sqrt(max(0.0, (1 - u * u) * (1 - v * v)))
    low = max(-1.0, u * v - radius)
    high = min(0.5, u * v + radius)
    if low > high + 1e-14:
        return None
    return low, high


def initial_samples(
    grid: int, random_count: int, seed: int, full_boundary_grid: int
):
    off: list[tuple[float, float, float]] = []
    heights = np.linspace(0.0, 1.0, grid)
    fractions = np.linspace(0.0, 1.0, grid)
    for u in heights:
        for v in heights:
            if v < u:
                continue
            interval = feasible_t_interval(float(u), float(v))
            if interval is None:
                continue
            low, high = interval
            for alpha in fractions:
                off.append((float(u), float(v), low + float(alpha) * (high - low)))
    rng = np.random.default_rng(seed)
    for _ in range(random_count):
        u, v = np.sort(rng.random(2))
        interval = feasible_t_interval(float(u), float(v))
        if interval is None:
            continue
        low, high = interval
        # Include points biased toward both determinant boundaries.
        alpha = rng.beta(0.55, 0.55)
        off.append((float(u), float(v), low + float(alpha) * (high - low)))
    # The north-pole boundary is lower-dimensional and random sampling almost
    # surely misses it.  Here v=1 forces t=u, and feasibility requires
    # 0<=u<=1/2.
    for u in np.linspace(0.0, 0.5, 201):
        off.append((float(u), 1.0, float(u)))
    # Resolve the determinant and t=1/2 boundaries near that pole.
    for epsilon in (1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4):
        v = 1.0 - epsilon
        for u in np.linspace(0.35, 0.65, 61):
            interval = feasible_t_interval(float(u), v)
            if interval is not None:
                low, high = interval
                off.extend(((float(u), v, low), (float(u), v, high)))
    # The strongest missed constraint in the first degree-10 candidate was
    # the determinant-zero curve u=0, t=-sqrt(1-v^2), near v=.987.  Resolve
    # both sheets explicitly.  Symmetry also covers the curve v=0.
    for v in np.linspace(0.0, 1.0, 401):
        interval = feasible_t_interval(0.0, float(v))
        assert interval is not None
        low, high = interval
        off.extend(((0.0, float(v), low), (0.0, float(v), high)))
    # A second repeatedly active determinant-zero curve has u=v and
    # t=2u^2-1 (opposite equatorial projections).
    for u in np.linspace(0.0, 1.0, 401):
        interval = feasible_t_interval(float(u), float(u))
        if interval is not None:
            low, high = interval
            off.extend(
                ((float(u), float(u), low), (float(u), float(u), high))
            )
    # The determinant-zero surface is another measure-zero part of the
    # domain on which sampled optima repeatedly develop violations.  Resolve
    # both of its sheets on a substantially finer height grid.
    if full_boundary_grid:
        boundary_heights = np.unique(
            np.concatenate(
                (
                    np.linspace(0.0, 1.0, full_boundary_grid),
                    np.array([0.5]),
                    1.0 - 10.0 ** (-np.arange(1, 7, dtype=float)),
                )
            )
        )
        for u in boundary_heights:
            for v in boundary_heights:
                if v < u:
                    continue
                interval = feasible_t_interval(float(u), float(v))
                if interval is None:
                    continue
                low, high = interval
                off.extend(
                    ((float(u), float(v), low), (float(u), float(v), high))
                )
                if low <= 0.5 <= high:
                    off.append((float(u), float(v), 0.5))
    diag = np.linspace(0.0, 1.0, max(4 * grid, 41)).tolist()
    return off, diag


def solve(
    degree: int,
    off,
    diag,
    solver: str,
    tolerance: float,
    verbose: bool,
    psd_floor: float,
):
    blocks = [cp.Variable((degree - k + 1, degree - k + 1), symmetric=True)
              for k in range(degree + 1)]
    objective_height = cp.Variable()
    constraints = [
        block >> psd_floor * np.eye(block.shape[0]) for block in blocks
    ]
    for u, v, t in off:
        mats = coefficient_matrices(degree, u, v, t)
        constraints.append(
            sum(cp.sum(cp.multiply(block, mat))
                for block, mat in zip(blocks, mats, strict=True))
            <= -1
        )
    for u in diag:
        mats = coefficient_matrices(degree, u, u, 1.0)
        constraints.append(
            sum(cp.sum(cp.multiply(block, mat))
                for block, mat in zip(blocks, mats, strict=True))
            <= objective_height
        )
    problem = cp.Problem(cp.Minimize(1 + objective_height), constraints)
    kwargs = {"verbose": verbose}
    if solver.upper() == "CLARABEL":
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


def evaluate(blocks, u: float, v: float, t: float) -> float:
    mats = coefficient_matrices(len(blocks) - 1, u, v, t)
    return float(sum(np.sum(block * mat)
                     for block, mat in zip(blocks, mats, strict=True)))


def audit_random(blocks, count: int, seed: int):
    rng = np.random.default_rng(seed)
    worst = (-math.inf, None)
    for _ in range(count):
        u, v = np.sort(rng.random(2))
        interval = feasible_t_interval(float(u), float(v))
        if interval is None:
            continue
        low, high = interval
        for alpha in (rng.random(), 0.0, 1.0):
            t = low + alpha * (high - low)
            value = evaluate(blocks, float(u), float(v), t)
            if value > worst[0]:
                worst = (value, (float(u), float(v), t))
    diagonal = max(
        (evaluate(blocks, u, u, 1.0), u)
        for u in np.linspace(0.0, 1.0, 10_001)
    )
    return worst, diagonal


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, default=5)
    parser.add_argument("--grid", type=int, default=7)
    parser.add_argument("--random", type=int, default=3000)
    parser.add_argument("--audit", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=502033)
    parser.add_argument("--solver", choices=("CLARABEL", "SCS"), default="CLARABEL")
    parser.add_argument("--tolerance", type=float, default=1e-7)
    parser.add_argument("--output", default="")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--psd-floor", type=float, default=0.0)
    parser.add_argument("--full-boundary-grid", type=int, default=0)
    args = parser.parse_args()
    off, diag = initial_samples(
        args.grid, args.random, args.seed, args.full_boundary_grid
    )
    print(f"samples: off={len(off)} diag={len(diag)}", flush=True)
    status, value, blocks = solve(
        args.degree,
        off,
        diag,
        args.solver,
        args.tolerance,
        args.verbose,
        args.psd_floor,
    )
    print(f"status={status} sampled_objective={value:.12f}", flush=True)
    worst, diagonal = audit_random(blocks, args.audit, args.seed + 1)
    print(f"random_off_max={worst[0]:.12f} at {worst[1]}", flush=True)
    print(f"dense_diag_max={diagonal[0]:.12f} at {diagonal[1]:.8f}", flush=True)
    print(f"audited_rescaled_objective={1-diagonal[0]/worst[0]:.12f}", flush=True)
    if args.output:
        np.savez(args.output, **{f"F{k}": block for k, block in enumerate(blocks)})


if __name__ == "__main__":
    main()
