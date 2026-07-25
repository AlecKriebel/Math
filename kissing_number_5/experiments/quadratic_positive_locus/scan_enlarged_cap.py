#!/usr/bin/env python3
"""Discovery-only SDP scan for enlarged one-sided spherical caps.

The exact theorem already in the repository treats heights u >= -1/300.
This script asks whether a newly optimized axisymmetric positive kernel can
certify the substantially larger cap u >= -1/50 with objective below 41.

Every constraint here is sampled.  Neither solver status nor the independent
floating-point audit is a proof.  A promising result must be rationalized and
verified over the complete semialgebraic domain with exact arithmetic.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path

import cvxpy as cp
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
BASE_PATH = ROOT / "experiments" / "search_one_sided_cap_sdp.py"
SPEC = importlib.util.spec_from_file_location("one_sided_cap_base_qpl", BASE_PATH)
assert SPEC is not None and SPEC.loader is not None
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)


def coefficient_row(degree: int, point: tuple[float, float, float]) -> np.ndarray:
    return np.concatenate(
        [matrix.reshape(-1) for matrix in BASE.coefficient_matrices(degree, *point)]
    )


def feasible_interval(u: float, v: float) -> tuple[float, float] | None:
    radius = math.sqrt(max(0.0, (1.0 - u * u) * (1.0 - v * v)))
    low = max(-1.0, u * v - radius)
    high = min(0.5, u * v + radius)
    return None if low > high + 1e-14 else (low, high)


def initial_points(
    lower: float, grid: int, random_count: int, seed: int
) -> tuple[list[tuple[float, float, float]], list[float]]:
    """Include all important faces as well as an interior random sample."""

    points: list[tuple[float, float, float]] = []
    heights = np.unique(
        np.concatenate(
            (
                np.linspace(lower, 0.0, max(5, grid // 3)),
                np.linspace(0.0, 1.0, grid),
                np.array([lower, 0.0, 0.5, 1.0]),
            )
        )
    )
    alphas = np.linspace(0.0, 1.0, max(7, grid // 2))
    for i, u in enumerate(heights):
        for v in heights[i:]:
            interval = feasible_interval(float(u), float(v))
            if interval is None:
                continue
            low, high = interval
            points.extend(
                (float(u), float(v), low + float(a) * (high - low))
                for a in alphas
            )

    # Resolve the new face u=lower, both determinant sheets, and the contact
    # face.  This face caused the strongest violations for the old kernel.
    for v in np.linspace(lower, 1.0, 401):
        interval = feasible_interval(lower, float(v))
        if interval is None:
            continue
        low, high = interval
        points.extend(((lower, float(v), low), (lower, float(v), high)))
        if low <= 0.5 <= high:
            points.append((lower, float(v), 0.5))

    # The u=v ridge and determinant-zero sheets are measure-zero and must be
    # sampled explicitly.
    for u in np.linspace(lower, math.sqrt(3.0) / 2.0, 301):
        interval = feasible_interval(float(u), float(u))
        if interval is None:
            continue
        low, high = interval
        points.extend(
            (float(u), float(u), low + float(a) * (high - low))
            for a in np.linspace(0.0, 1.0, 41)
        )

    rng = np.random.default_rng(seed)
    for _ in range(random_count):
        u, v = np.sort(rng.uniform(lower, 1.0, 2))
        interval = feasible_interval(float(u), float(v))
        if interval is None:
            continue
        low, high = interval
        for alpha in (rng.random(), rng.beta(0.4, 0.4), 0.0, 1.0):
            points.append((float(u), float(v), low + alpha * (high - low)))

    points = list(dict.fromkeys(points))
    diagonal = np.linspace(lower, 1.0, 501).tolist()
    return points, diagonal


def solve(
    degree: int,
    off: list[tuple[float, float, float]],
    diagonal: list[float],
    psd_floor: float,
    tolerance: float,
) -> tuple[str, float, list[np.ndarray]]:
    blocks = [
        cp.Variable((degree - k + 1, degree - k + 1), symmetric=True)
        for k in range(degree + 1)
    ]
    diag_bound = cp.Variable()
    vector = cp.hstack(
        [
            cp.reshape(block, (block.shape[0] ** 2,), order="C")
            for block in blocks
        ]
    )
    off_rows = np.vstack([coefficient_row(degree, point) for point in off])
    diag_rows = np.vstack(
        [coefficient_row(degree, (u, u, 1.0)) for u in diagonal]
    )
    constraints = [
        block >> psd_floor * np.eye(block.shape[0]) for block in blocks
    ]
    constraints.extend((off_rows @ vector <= -1.0, diag_rows @ vector <= diag_bound))
    problem = cp.Problem(cp.Minimize(1.0 + diag_bound), constraints)
    value = problem.solve(
        solver="CLARABEL",
        tol_gap_abs=tolerance,
        tol_feas=tolerance,
        tol_gap_rel=tolerance,
        max_iter=600,
    )
    return problem.status, float(value), [block.value for block in blocks]


def evaluate(blocks: list[np.ndarray], point: tuple[float, float, float]) -> float:
    return BASE.evaluate(blocks, *point)


def audit(
    blocks: list[np.ndarray],
    lower: float,
    random_count: int,
    seed: int,
) -> dict[str, object]:
    """Use a sample independent of the optimization mesh."""

    rng = np.random.default_rng(seed)
    candidates: list[tuple[float, tuple[float, float, float]]] = []

    def inspect(point: tuple[float, float, float]) -> None:
        candidates.append((evaluate(blocks, point), point))

    for _ in range(random_count):
        u, v = np.sort(rng.uniform(lower, 1.0, 2))
        interval = feasible_interval(float(u), float(v))
        if interval is None:
            continue
        low, high = interval
        for alpha in (rng.random(), rng.beta(0.35, 0.35), 0.0, 1.0):
            inspect((float(u), float(v), low + alpha * (high - low)))

    for v in np.linspace(lower, 1.0, 2001):
        interval = feasible_interval(lower, float(v))
        if interval is None:
            continue
        low, high = interval
        for alpha in np.linspace(0.0, 1.0, 31):
            inspect((lower, float(v), low + float(alpha) * (high - low)))

    for u in np.linspace(lower, math.sqrt(3.0) / 2.0, 1001):
        interval = feasible_interval(float(u), float(u))
        if interval is None:
            continue
        low, high = interval
        for alpha in np.linspace(0.0, 1.0, 101):
            inspect((float(u), float(u), low + float(alpha) * (high - low)))

    candidates.sort(key=lambda item: item[0], reverse=True)
    diagonal = max(
        (evaluate(blocks, (float(u), float(u), 1.0)), float(u))
        for u in np.linspace(lower, 1.0, 20_001)
    )
    maximum, point = candidates[0]
    rescaled = math.inf if maximum >= 0.0 else 1.0 - diagonal[0] / maximum
    return {
        "off_diagonal_maximum": maximum,
        "off_diagonal_point": point,
        "diagonal_maximum": diagonal[0],
        "diagonal_height": diagonal[1],
        "rescaled_objective": rescaled,
        "top_violations": [
            {"value": value, "point": point}
            for value, point in candidates[: min(100, len(candidates))]
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lower", type=float, default=-0.02)
    parser.add_argument("--degree", type=int, default=8)
    parser.add_argument("--grid", type=int, default=19)
    parser.add_argument("--random", type=int, default=4000)
    parser.add_argument("--audit", type=int, default=40_000)
    parser.add_argument("--rounds", type=int, default=4)
    parser.add_argument("--seed", type=int, default=526221)
    parser.add_argument("--psd-floor", type=float, default=1e-6)
    parser.add_argument("--tolerance", type=float, default=2e-7)
    parser.add_argument("--output", required=True)
    parser.add_argument("--matrices", required=True)
    args = parser.parse_args()

    off, diagonal = initial_points(args.lower, args.grid, args.random, args.seed)
    reports = []
    blocks: list[np.ndarray] = []
    def checkpoint() -> None:
        if blocks:
            np.savez(
                args.matrices,
                **{f"F{k}": block for k, block in enumerate(blocks)},
            )
        payload = {
            "status": "NUMERICAL EVIDENCE ONLY",
            "warning": (
                "Sampled SDP and floating-point audits do not prove a cap bound."
            ),
            "numpy_version": np.__version__,
            "cvxpy_version": cp.__version__,
            "parameters": vars(args),
            "rounds": reports,
        }
        Path(args.output).write_text(json.dumps(payload, indent=2) + "\n")

    for round_index in range(args.rounds):
        try:
            status, sampled_objective, blocks = solve(
                args.degree,
                off,
                diagonal,
                args.psd_floor,
                args.tolerance,
            )
        except cp.error.SolverError as error:
            reports.append(
                {
                    "round": round_index,
                    "status": "SOLVER FAILURE",
                    "error": str(error),
                    "off_constraints": len(off),
                }
            )
            checkpoint()
            break
        report = audit(
            blocks,
            args.lower,
            args.audit,
            args.seed + 10_000 + round_index,
        )
        report["round"] = round_index
        report["status"] = status
        report["sampled_objective"] = sampled_objective
        report["off_constraints"] = len(off)
        reports.append(report)
        print(json.dumps(report, indent=2), flush=True)
        checkpoint()

        # Cutting planes are selected only from the independent audit.  The
        # next round is still a sampled program, hence discovery-only.
        new_points = [
            tuple(item["point"])
            for item in report["top_violations"]
            if item["value"] > -1.0001
        ]
        off.extend(new_points)
        off = list(dict.fromkeys(off))
        diagonal.append(float(report["diagonal_height"]))
        diagonal = list(dict.fromkeys(diagonal))

    checkpoint()


if __name__ == "__main__":
    main()
