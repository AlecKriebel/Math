#!/usr/bin/env python3
"""Degree-12/13 discovery search for a sharper one-sided cap bound.

This program is deliberately separate from the certified degree-11
artifacts.  It solves sampled axisymmetric Bachoc--Vallentin dual SDPs and
then audits substantially denser deterministic and random point sets.
Floating-point output from this program is evidence only, never a proof.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
from typing import Iterable

import cvxpy as cp
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
BASE_PATH = ROOT / "experiments" / "search_one_sided_cap_sdp.py"
SPEC = importlib.util.spec_from_file_location("one_sided_base_d12", BASE_PATH)
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


def unique_points(
    points: Iterable[tuple[float, float, float]],
) -> list[tuple[float, float, float]]:
    """Deduplicate floating sampling points by their exact float triples."""

    return list(dict.fromkeys(points))


def add_symmetric_mesh(
    off: list[tuple[float, float, float]],
    u_count: int,
    alpha_count: int,
) -> None:
    maximum_height = math.sqrt(3.0) / 2.0
    heights = np.unique(
        np.concatenate(
            (
                np.linspace(0.0, 0.16, max(3, u_count // 3)),
                np.linspace(0.16, 0.45, max(3, u_count // 3)),
                np.linspace(0.45, maximum_height, max(3, u_count // 3)),
            )
        )
    )
    alphas = np.unique(
        np.concatenate(
            (
                np.linspace(0.0, 0.12, max(3, alpha_count // 3)),
                np.linspace(0.12, 0.55, max(3, alpha_count // 3)),
                np.linspace(0.55, 1.0, max(3, alpha_count // 3)),
            )
        )
    )
    for u in heights:
        interval = BASE.feasible_t_interval(float(u), float(u))
        if interval is None:
            continue
        low, high = interval
        for alpha in alphas:
            off.append((float(u), float(u), low + float(alpha) * (high - low)))


def add_mixed_mesh(
    off: list[tuple[float, float, float]],
    v_count: int,
    alpha_count: int,
) -> None:
    """Resolve asymmetric height ratios and all faces on those slices."""

    ratios = (0.0, 0.04, 0.1, 0.2, 0.35, 0.5, 0.7, 0.85, 0.95)
    heights = np.unique(
        np.concatenate(
            (
                np.linspace(0.0, 0.5, max(3, v_count // 2)),
                np.linspace(0.5, 1.0, max(3, v_count // 2)),
                1.0 - 10.0 ** (-np.arange(1, 7, dtype=float)),
            )
        )
    )
    alphas = np.unique(
        np.concatenate(
            (
                np.array([0.0, 1.0]),
                np.linspace(0.0, 0.2, max(3, alpha_count // 2)),
                np.linspace(0.2, 1.0, max(3, alpha_count // 2)),
            )
        )
    )
    for v in heights:
        for ratio in ratios:
            u = float(ratio * v)
            interval = BASE.feasible_t_interval(u, float(v))
            if interval is None:
                continue
            low, high = interval
            for alpha in alphas:
                off.append((u, float(v), low + float(alpha) * (high - low)))


def add_zero_height_mesh(
    off: list[tuple[float, float, float]],
    v_count: int,
    alpha_count: int,
) -> None:
    """Resolve the repeatedly active full slice u=0."""

    heights = np.unique(
        np.concatenate(
            (
                np.linspace(0.0, 0.8, max(3, 3 * v_count // 4)),
                np.linspace(0.8, 1.0, max(3, v_count // 4)),
            )
        )
    )
    alphas = np.unique(
        np.concatenate(
            (
                np.linspace(0.0, 0.3, max(3, alpha_count // 2)),
                np.linspace(0.3, 1.0, max(3, alpha_count // 2)),
            )
        )
    )
    for v in heights:
        interval = BASE.feasible_t_interval(0.0, float(v))
        assert interval is not None
        low, high = interval
        for alpha in alphas:
            off.append((0.0, float(v), low + float(alpha) * (high - low)))


def add_contact_mesh(
    off: list[tuple[float, float, float]], height_count: int
) -> None:
    heights = np.unique(
        np.concatenate(
            (
                np.linspace(0.0, 1.0, height_count),
                np.array([0.5, math.sqrt(3.0) / 2.0]),
            )
        )
    )
    for i, u in enumerate(heights):
        for v in heights[i:]:
            interval = BASE.feasible_t_interval(float(u), float(v))
            if interval is None:
                continue
            low, high = interval
            if low <= 0.5 <= high:
                off.append((float(u), float(v), 0.5))


def solve(
    degree: int,
    off: list[tuple[float, float, float]],
    diag: list[float],
    tolerance: float,
    psd_floor: float,
    verbose: bool,
) -> tuple[str, float, list[np.ndarray]]:
    blocks = [
        cp.Variable((degree - k + 1, degree - k + 1), symmetric=True)
        for k in range(degree + 1)
    ]
    objective_height = cp.Variable()
    constraints = [
        block >> psd_floor * np.eye(block.shape[0]) for block in blocks
    ]
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
            off_rows @ block_vector <= -1.0,
            diagonal_rows @ block_vector <= objective_height,
        )
    )
    problem = cp.Problem(cp.Minimize(1.0 + objective_height), constraints)
    value = problem.solve(
        solver="CLARABEL",
        verbose=verbose,
        tol_gap_abs=tolerance,
        tol_feas=tolerance,
        tol_gap_rel=tolerance,
        max_iter=700,
    )
    return problem.status, float(value), [block.value for block in blocks]


def update_worst(
    current: tuple[float, tuple[float, float, float] | None],
    blocks: list[np.ndarray],
    point: tuple[float, float, float],
) -> tuple[float, tuple[float, float, float] | None]:
    value = BASE.evaluate(blocks, *point)
    if value > current[0]:
        return value, point
    return current


def deterministic_audit(
    blocks: list[np.ndarray],
    symmetric_u: int,
    symmetric_alpha: int,
    mixed_v: int,
    mixed_alpha: int,
    boundary_height: int,
) -> dict[str, object]:
    """Audit lower-dimensional ridges independently of the training mesh."""

    reports: dict[str, object] = {}
    worst: tuple[float, tuple[float, float, float] | None] = (-math.inf, None)
    maximum_height = math.sqrt(3.0) / 2.0
    for u in np.linspace(0.0, maximum_height, symmetric_u):
        interval = BASE.feasible_t_interval(float(u), float(u))
        if interval is None:
            continue
        low, high = interval
        for alpha in np.linspace(0.0, 1.0, symmetric_alpha):
            worst = update_worst(
                worst,
                blocks,
                (float(u), float(u), low + float(alpha) * (high - low)),
            )
    reports["symmetric"] = {"maximum": worst[0], "point": worst[1]}

    worst = (-math.inf, None)
    audit_ratios = (0.0, 0.025, 0.075, 0.15, 0.275, 0.425, 0.6, 0.775, 0.9, 0.975)
    for v in np.linspace(0.0, 1.0, mixed_v):
        for ratio in audit_ratios:
            u = float(ratio * v)
            interval = BASE.feasible_t_interval(u, float(v))
            if interval is None:
                continue
            low, high = interval
            for alpha in np.linspace(0.0, 1.0, mixed_alpha):
                worst = update_worst(
                    worst,
                    blocks,
                    (u, float(v), low + float(alpha) * (high - low)),
                )
    reports["mixed"] = {"maximum": worst[0], "point": worst[1]}

    worst = (-math.inf, None)
    heights = np.linspace(0.0, 1.0, boundary_height)
    for i, u in enumerate(heights):
        for v in heights[i:]:
            interval = BASE.feasible_t_interval(float(u), float(v))
            if interval is None:
                continue
            low, high = interval
            worst = update_worst(worst, blocks, (float(u), float(v), low))
            worst = update_worst(worst, blocks, (float(u), float(v), high))
            if low <= 0.5 <= high:
                worst = update_worst(
                    worst, blocks, (float(u), float(v), 0.5)
                )
    reports["determinant_and_contact"] = {
        "maximum": worst[0],
        "point": worst[1],
    }
    return reports


def random_audit(
    blocks: list[np.ndarray], count: int, seed: int
) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    worst: tuple[float, tuple[float, float, float] | None] = (-math.inf, None)
    for _ in range(count):
        u, v = np.sort(rng.random(2))
        interval = BASE.feasible_t_interval(float(u), float(v))
        if interval is None:
            continue
        low, high = interval
        for alpha in (float(rng.random()), float(rng.beta(0.35, 0.35)), 0.0, 1.0):
            worst = update_worst(
                worst,
                blocks,
                (float(u), float(v), low + alpha * (high - low)),
            )
    return {"maximum": worst[0], "point": worst[1]}


def diagonal_audit(
    blocks: list[np.ndarray], count: int
) -> dict[str, object]:
    maximum, point = max(
        (BASE.evaluate(blocks, float(u), float(u), 1.0), float(u))
        for u in np.linspace(0.0, 1.0, count)
    )
    return {"maximum": maximum, "height": point}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, choices=(12, 13), required=True)
    parser.add_argument("--seed", type=int, default=512013)
    parser.add_argument("--random", type=int, default=7000)
    parser.add_argument("--grid", type=int, default=11)
    parser.add_argument("--full-boundary-grid", type=int, default=35)
    parser.add_argument("--symmetric-u", type=int, default=241)
    parser.add_argument("--symmetric-alpha", type=int, default=71)
    parser.add_argument("--mixed-v", type=int, default=101)
    parser.add_argument("--mixed-alpha", type=int, default=21)
    parser.add_argument("--zero-v", type=int, default=201)
    parser.add_argument("--zero-alpha", type=int, default=61)
    parser.add_argument("--contact-height", type=int, default=51)
    parser.add_argument("--diagonal-grid", type=int, default=501)
    parser.add_argument("--audit-random", type=int, default=100000)
    parser.add_argument("--audit-symmetric-u", type=int, default=1001)
    parser.add_argument("--audit-symmetric-alpha", type=int, default=401)
    parser.add_argument("--audit-mixed-v", type=int, default=251)
    parser.add_argument("--audit-mixed-alpha", type=int, default=101)
    parser.add_argument("--audit-boundary-height", type=int, default=151)
    parser.add_argument("--audit-diagonal", type=int, default=20001)
    parser.add_argument("--tolerance", type=float, default=3e-7)
    parser.add_argument("--psd-floor", type=float, default=1e-6)
    parser.add_argument("--output", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    off, _ = BASE.initial_samples(
        args.grid, args.random, args.seed, args.full_boundary_grid
    )
    add_symmetric_mesh(off, args.symmetric_u, args.symmetric_alpha)
    add_mixed_mesh(off, args.mixed_v, args.mixed_alpha)
    add_zero_height_mesh(off, args.zero_v, args.zero_alpha)
    add_contact_mesh(off, args.contact_height)
    off = unique_points(off)
    diag = np.linspace(0.0, 1.0, args.diagonal_grid).tolist()
    print(f"samples: off={len(off)} diag={len(diag)}", flush=True)
    status, sampled_objective, blocks = solve(
        args.degree,
        off,
        diag,
        args.tolerance,
        args.psd_floor,
        args.verbose,
    )
    print(
        f"status={status} sampled_objective={sampled_objective:.12f}",
        flush=True,
    )
    np.savez(args.output, **{f"F{k}": block for k, block in enumerate(blocks)})

    deterministic = deterministic_audit(
        blocks,
        args.audit_symmetric_u,
        args.audit_symmetric_alpha,
        args.audit_mixed_v,
        args.audit_mixed_alpha,
        args.audit_boundary_height,
    )
    random_result = random_audit(blocks, args.audit_random, args.seed + 1)
    diagonal = diagonal_audit(blocks, args.audit_diagonal)
    off_maximum = max(
        float(entry["maximum"])
        for entry in (*deterministic.values(), random_result)
    )
    audited_rescaled_objective = (
        1.0 - float(diagonal["maximum"]) / off_maximum
    )
    report = {
        "status": "NUMERICAL EVIDENCE ONLY",
        "degree": args.degree,
        "seed": args.seed,
        "sample_counts": {"off_diagonal": len(off), "diagonal": len(diag)},
        "solver": {
            "name": "CLARABEL",
            "cvxpy_version": cp.__version__,
            "numpy_version": np.__version__,
            "status": status,
            "tolerance": args.tolerance,
            "psd_floor": args.psd_floor,
            "sampled_objective": sampled_objective,
        },
        "audit": {
            "deterministic": deterministic,
            "random": random_result,
            "diagonal": diagonal,
            "worst_off_diagonal": off_maximum,
            "audited_rescaled_objective": audited_rescaled_objective,
        },
        "warning": (
            "A sampled floating-point SDP and audit do not prove a cap bound."
        ),
    }
    Path(args.report).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report["audit"], indent=2), flush=True)


if __name__ == "__main__":
    main()
