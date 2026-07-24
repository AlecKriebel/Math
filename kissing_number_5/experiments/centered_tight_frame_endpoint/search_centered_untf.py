#!/usr/bin/env python3
"""Discovery search for centered 41-vector unit-norm tight frames in R^5.

This is deliberately a numerical discovery program.  It alternates exact
floating-point projections onto

  * unit row norms,
  * zero column sums, and
  * frame operator (41/5) I,

and minimizes a smooth approximation to the largest off-diagonal inner
product.  The resulting coordinates are not a certificate.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


N = 41
D = 5


def project_centered_untf(frame: np.ndarray, cycles: int = 100) -> np.ndarray:
    """Alternating projection onto centered equal-norm tight-frame equations."""

    answer = np.array(frame, dtype=float, copy=True)
    for _ in range(cycles):
        norms = np.linalg.norm(answer, axis=1)
        if float(np.min(norms)) < 1e-12:
            raise ValueError("row collapsed during alternating projection")
        answer /= norms[:, None]
        answer -= np.mean(answer, axis=0, keepdims=True)
        operator = answer.T @ answer
        eigenvalues, eigenvectors = np.linalg.eigh(operator)
        if float(np.min(eigenvalues)) < 1e-12:
            raise ValueError("frame lost rank during alternating projection")
        whitening = (
            eigenvectors
            @ np.diag(np.sqrt(N / D) / np.sqrt(eigenvalues))
            @ eigenvectors.T
        )
        answer = answer @ whitening
    return answer


def pair_data(frame: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    left, right = np.triu_indices(len(frame), 1)
    values = np.sum(frame[left] * frame[right], axis=1)
    return left, right, values


def smooth_energy_gradient(
    frame: np.ndarray, beta: float
) -> tuple[float, np.ndarray]:
    left, right, values = pair_data(frame)
    maximum = float(np.max(values))
    exponentials = np.exp(beta * (values - maximum))
    weights = exponentials / float(np.sum(exponentials))
    gradient = np.zeros_like(frame)
    np.add.at(gradient, left, weights[:, None] * frame[right])
    np.add.at(gradient, right, weights[:, None] * frame[left])
    return maximum + math.log(float(np.sum(exponentials))) / beta, gradient


def diagnostics(frame: np.ndarray) -> dict[str, object]:
    left, right, values = pair_data(frame)
    maximum_index = int(np.argmax(values))
    gram = frame @ frame.T
    b = np.eye(N) + np.ones((N, N)) - 2.0 * gram
    b_eigenvalues = np.linalg.eigvalsh(b)
    return {
        "maximum_inner_product": float(values[maximum_index]),
        "maximizing_pair": [
            int(left[maximum_index]),
            int(right[maximum_index]),
        ],
        "minimum_inner_product": float(np.min(values)),
        "number_above_one_half": int(np.count_nonzero(values > 0.5)),
        "maximum_unit_norm_residual": float(
            np.max(np.abs(np.diag(gram) - 1.0))
        ),
        "centroid_norm": float(np.linalg.norm(np.sum(frame, axis=0))),
        "tight_frame_frobenius_residual": float(
            np.linalg.norm(
                frame.T @ frame - (N / D) * np.eye(D), ord="fro"
            )
        ),
        "b_minimum_entry": float(np.min(b)),
        "b_row_sum_residual": float(
            np.max(np.abs(np.sum(b, axis=1) - 42.0))
        ),
        "b_spectrum_max_residual": float(
            np.max(
                np.abs(
                    b_eigenvalues
                    - np.sort(
                        np.array([-77.0 / 5.0] * 5 + [1.0] * 35 + [42.0])
                    )
                )
            )
        ),
    }


def optimize(
    frame: np.ndarray,
    beta_schedule: list[float],
    iterations: int,
    projection_cycles: int,
) -> np.ndarray:
    frame = project_centered_untf(frame, 500)
    step = 0.08
    for beta in beta_schedule:
        for _ in range(iterations):
            energy, gradient = smooth_energy_gradient(frame, beta)
            trial_step = step
            accepted = False
            for _line_search in range(18):
                trial = project_centered_untf(
                    frame - trial_step * gradient, projection_cycles
                )
                trial_energy, _ = smooth_energy_gradient(trial, beta)
                if trial_energy < energy:
                    frame = trial
                    step = min(0.3, 1.15 * trial_step)
                    accepted = True
                    break
                trial_step *= 0.5
            if not accepted:
                step = max(1e-8, 0.5 * step)
                if step == 1e-8:
                    break
    return project_centered_untf(frame, 1000)


def d5_plus_one_seed(extra: np.ndarray) -> np.ndarray:
    roots: list[np.ndarray] = []
    for i in range(D):
        for j in range(i + 1, D):
            for si in (-1.0, 1.0):
                for sj in (-1.0, 1.0):
                    row = np.zeros(D)
                    row[i] = si / math.sqrt(2.0)
                    row[j] = sj / math.sqrt(2.0)
                    roots.append(row)
    return np.vstack([np.asarray(roots), extra / np.linalg.norm(extra)])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=541041)
    parser.add_argument("--random-starts", type=int, default=24)
    parser.add_argument("--iterations", type=int, default=160)
    parser.add_argument("--projection-cycles", type=int, default=40)
    parser.add_argument(
        "--output",
        default=str(
            Path(__file__).resolve().parent
            / "results"
            / "centered_untf_search.json"
        ),
    )
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    beta_schedule = [10, 20, 40, 80, 160, 320, 640, 1280, 2560]

    starts = [
        d5_plus_one_seed(np.eye(D)[axis]) for axis in range(D)
    ]
    starts.append(d5_plus_one_seed(np.ones(D)))
    starts.extend(
        rng.normal(size=(N, D)) for _ in range(args.random_starts)
    )

    records = []
    best_value = math.inf
    best_frame: np.ndarray | None = None
    for index, initial in enumerate(starts):
        frame = optimize(
            initial,
            beta_schedule=beta_schedule,
            iterations=args.iterations,
            projection_cycles=args.projection_cycles,
        )
        record = {
            "start": index,
            "source": "D5-plus-one" if index < 6 else "asymmetric-random",
            **diagnostics(frame),
        }
        records.append(record)
        value = float(record["maximum_inner_product"])
        print(f"start={index:02d} max={value:.12f}", flush=True)
        if value < best_value:
            best_value = value
            best_frame = frame.copy()

    assert best_frame is not None
    payload = {
        "schema": "centered-41x5-untf-search-v1",
        "status": "NUMERICAL EVIDENCE ONLY",
        "seed": args.seed,
        "beta_schedule": beta_schedule,
        "iterations_per_beta": args.iterations,
        "projection_cycles_per_trial": args.projection_cycles,
        "records": records,
        "best": {
            **diagnostics(best_frame),
            "coordinates": best_frame.tolist(),
        },
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {output}", flush=True)


if __name__ == "__main__":
    main()
