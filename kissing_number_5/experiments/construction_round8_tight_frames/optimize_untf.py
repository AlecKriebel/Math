#!/usr/bin/env python3
"""Numerical construction search on structured and general 41x5 UNTFs.

The seven-bases-plus-simplex family is exactly UNTF by construction.  The
general search uses alternating row-normalization and frame-whitening as a
numerical retraction onto the equal-norm Stiefel intersection.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm


N = 41
D = 5
ROOT = Path(__file__).resolve().parents[2]
RESULT_PATH = (
    ROOT
    / "experiments"
    / "construction_round8_tight_frames"
    / "results"
    / "untf_optimization.json"
)


def regular_simplex() -> np.ndarray:
    """Six unit vectors in R^5 with mutual inner product -1/5."""

    helmert = np.zeros((6, 5))
    for column in range(5):
        denominator = math.sqrt((column + 1) * (column + 2))
        helmert[: column + 1, column] = 1.0 / denominator
        helmert[column + 1, column] = -(column + 1) / denominator
    simplex = math.sqrt(6.0 / 5.0) * helmert
    assert np.max(np.abs(np.diag(simplex @ simplex.T) - 1.0)) < 1e-14
    return simplex


def random_orthogonal(rng: np.random.Generator) -> np.ndarray:
    q, r = np.linalg.qr(rng.normal(size=(D, D)))
    q = q @ np.diag(np.sign(np.diag(r)))
    return q


def assemble_union(rotations: list[np.ndarray]) -> tuple[np.ndarray, list[slice]]:
    assert len(rotations) == 7
    bases = [np.eye(D)] + rotations[:6]
    simplex = regular_simplex() @ rotations[6]
    groups = bases + [simplex]
    slices = []
    start = 0
    for group in groups:
        slices.append(slice(start, start + len(group)))
        start += len(group)
    frame = np.vstack(groups)
    assert frame.shape == (N, D)
    return frame, slices


def cross_pairs(slices: list[slice]) -> tuple[np.ndarray, np.ndarray]:
    group_of = np.empty(N, dtype=int)
    for group, current_slice in enumerate(slices):
        group_of[current_slice] = group
    left, right = [], []
    for i in range(N):
        for j in range(i + 1, N):
            if group_of[i] != group_of[j]:
                left.append(i)
                right.append(j)
    return np.asarray(left), np.asarray(right)


def smooth_energy_and_gradient(
    frame: np.ndarray,
    beta: float,
    pairs: tuple[np.ndarray, np.ndarray] | None = None,
) -> tuple[float, np.ndarray]:
    if pairs is None:
        left, right = np.triu_indices(len(frame), 1)
    else:
        left, right = pairs
    values = np.sum(frame[left] * frame[right], axis=1)
    maximum = float(np.max(values))
    exponentials = np.exp(beta * (values - maximum))
    total = float(np.sum(exponentials))
    weights = exponentials / total
    gradient = np.zeros_like(frame)
    np.add.at(gradient, left, weights[:, None] * frame[right])
    np.add.at(gradient, right, weights[:, None] * frame[left])
    energy = maximum + math.log(total) / beta
    return energy, gradient


def max_inner_product(frame: np.ndarray) -> tuple[float, tuple[int, int]]:
    gram = frame @ frame.T
    np.fill_diagonal(gram, -np.inf)
    index = int(np.argmax(gram))
    i, j = divmod(index, len(frame))
    return float(gram[i, j]), (i, j)


def frame_diagnostics(frame: np.ndarray) -> dict[str, float | list[int]]:
    maximum, pair = max_inner_product(frame)
    row_residual = float(
        np.max(np.abs(np.sum(frame * frame, axis=1) - 1.0))
    )
    tight_residual = float(
        np.linalg.norm(
            frame.T @ frame - (len(frame) / D) * np.eye(D), ord="fro"
        )
    )
    return {
        "maximum_inner_product": maximum,
        "maximizing_pair": list(pair),
        "maximum_unit_norm_residual": row_residual,
        "tight_frame_frobenius_residual": tight_residual,
    }


def optimize_union(
    rotations: list[np.ndarray],
    beta_schedule: list[float],
    iterations: int,
) -> tuple[list[np.ndarray], np.ndarray]:
    frame, slices = assemble_union(rotations)
    pairs = cross_pairs(slices)
    step = 0.4
    for beta in beta_schedule:
        for _ in range(iterations):
            frame, slices = assemble_union(rotations)
            energy, gradient = smooth_energy_and_gradient(frame, beta, pairs)
            tangent_generators = []
            squared_norm = 0.0
            for variable_index, group_index in enumerate(range(1, 8)):
                base = np.eye(D) if group_index < 7 else regular_simplex()
                group_gradient = gradient[slices[group_index]]
                euclidean = base.T @ group_gradient
                q = rotations[variable_index]
                ambient = q.T @ euclidean
                skew = (ambient - ambient.T) / 2.0
                tangent_generators.append(skew)
                squared_norm += float(np.sum(skew * skew))
            if squared_norm < 1e-22:
                break
            trial_step = step
            accepted = False
            for _line_search in range(18):
                trial = [
                    q @ expm(-trial_step * skew)
                    for q, skew in zip(
                        rotations, tangent_generators, strict=True
                    )
                ]
                trial_frame, _ = assemble_union(trial)
                trial_energy, _ = smooth_energy_and_gradient(
                    trial_frame, beta, pairs
                )
                if trial_energy <= energy - 1e-4 * trial_step * squared_norm:
                    rotations = trial
                    step = min(1.0, trial_step * 1.25)
                    accepted = True
                    break
                trial_step *= 0.5
            if not accepted:
                step = max(1e-7, step * 0.5)
                if step == 1e-7:
                    break
    return rotations, assemble_union(rotations)[0]


def project_untf(frame: np.ndarray, cycles: int = 100) -> np.ndarray:
    answer = np.array(frame, dtype=float, copy=True)
    for _ in range(cycles):
        answer /= np.linalg.norm(answer, axis=1)[:, None]
        gram = answer.T @ answer
        eigenvalues, eigenvectors = np.linalg.eigh(gram)
        whitening = (
            eigenvectors
            @ np.diag(np.sqrt(N / D) / np.sqrt(eigenvalues))
            @ eigenvectors.T
        )
        answer = answer @ whitening
    return answer


def optimize_general(
    frame: np.ndarray,
    beta_schedule: list[float],
    iterations: int,
) -> np.ndarray:
    frame = project_untf(frame, 200)
    step = 0.08
    for beta in beta_schedule:
        for _ in range(iterations):
            energy, gradient = smooth_energy_and_gradient(frame, beta)
            trial_step = step
            accepted = False
            for _line_search in range(16):
                trial = project_untf(frame - trial_step * gradient, 30)
                trial_energy, _ = smooth_energy_and_gradient(trial, beta)
                if trial_energy < energy:
                    frame = trial
                    step = min(0.3, trial_step * 1.15)
                    accepted = True
                    break
                trial_step *= 0.5
            if not accepted:
                step = max(1e-7, step * 0.5)
                if step == 1e-7:
                    break
    return project_untf(frame, 500)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=528041)
    parser.add_argument("--union-starts", type=int, default=16)
    parser.add_argument("--general-starts", type=int, default=12)
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--output", default=str(RESULT_PATH))
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    beta_schedule = [10, 20, 40, 80, 160, 320, 640, 1280]

    union_records = []
    best_union_frame = None
    best_union_value = math.inf
    for start in range(args.union_starts):
        rotations = [random_orthogonal(rng) for _ in range(7)]
        _rotations, frame = optimize_union(
            rotations, beta_schedule, args.iterations
        )
        diagnostics = frame_diagnostics(frame)
        union_records.append({"start": start, **diagnostics})
        value = diagnostics["maximum_inner_product"]
        print(f"union start={start} max={value:.12f}", flush=True)
        if value < best_union_value:
            best_union_value = value
            best_union_frame = frame.copy()

    assert best_union_frame is not None
    general_records = []
    best_general_frame = best_union_frame.copy()
    best_general_value = best_union_value
    starts = [best_union_frame]
    starts.extend(
        project_untf(rng.normal(size=(N, D)), 200)
        for _ in range(args.general_starts)
    )
    for start, initial in enumerate(starts):
        frame = optimize_general(initial, beta_schedule, args.iterations)
        diagnostics = frame_diagnostics(frame)
        general_records.append({"start": start, **diagnostics})
        value = diagnostics["maximum_inner_product"]
        print(f"general start={start} max={value:.12f}", flush=True)
        if value < best_general_value:
            best_general_value = value
            best_general_frame = frame.copy()

    data = {
        "schema": "numerical-untf-41x5-search-v1",
        "status": "NUMERICAL EVIDENCE ONLY",
        "seed": args.seed,
        "beta_schedule": beta_schedule,
        "iterations_per_beta": args.iterations,
        "union_starts": union_records,
        "general_starts": general_records,
        "best_union": {
            **frame_diagnostics(best_union_frame),
            "coordinates": best_union_frame.tolist(),
        },
        "best_general": {
            **frame_diagnostics(best_general_frame),
            "coordinates": best_general_frame.tolist(),
        },
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2) + "\n")
    print(f"wrote {output}", flush=True)


if __name__ == "__main__":
    main()
