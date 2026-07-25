#!/usr/bin/env python3
"""Search for 41 kissing points inside fixed quadratic positive loci.

This is a deterministic-seed, floating-point construction experiment.  It
uses projected Adam on (S^4)^N with a log-sum-exp approximation to the
largest pairwise inner product and a penalty for q(x)<=margin.  Output is
NUMERICAL EVIDENCE ONLY, even when every printed inequality has slack.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


def family_data(name: str) -> tuple[np.ndarray, np.ndarray]:
    """Return diagonal A and b for q(x)=x^T A x+b^T x."""

    if name == "belt":
        return np.array([1.0, 1.0, 1.0, 1.0, -4.0]), np.zeros(5)
    if name == "two_caps":
        return np.array([-1.0, -1.0, -1.0, -1.0, 4.0]), np.zeros(5)
    if name == "shifted_cap":
        return (
            np.array([1.0, 1.0, 1.0, 1.0, -4.0]),
            np.array([0.0, 0.0, 0.0, 0.0, 5.0]),
        )
    raise ValueError(name)


def q_values(x: np.ndarray, diagonal: np.ndarray, linear: np.ndarray) -> np.ndarray:
    return np.sum(diagonal * x * x, axis=1) + x @ linear


def initialize(
    rng: np.random.Generator,
    number: int,
    diagonal: np.ndarray,
    linear: np.ndarray,
    margin: float,
) -> np.ndarray:
    """Rejection sample from q>margin; the three tested loci have ample mass."""

    points: list[np.ndarray] = []
    while len(points) < number:
        batch = rng.normal(size=(max(256, 4 * number), 5))
        batch /= np.linalg.norm(batch, axis=1)[:, None]
        accepted = batch[q_values(batch, diagonal, linear) > 5.0 * margin]
        points.extend(accepted)
    return np.vstack(points[:number])


def objective_gradient(
    x: np.ndarray,
    diagonal: np.ndarray,
    linear: np.ndarray,
    temperature: float,
    margin: float,
    penalty: float,
) -> tuple[float, np.ndarray]:
    number = len(x)
    ii, jj = np.triu_indices(number, 1)
    dots = np.sum(x[ii] * x[jj], axis=1)
    shifted = dots / temperature
    shifted -= np.max(shifted)
    weights = np.exp(shifted)
    weights /= np.sum(weights)
    smooth_max = temperature * (
        math.log(float(np.sum(np.exp(dots / temperature - np.max(dots / temperature)))))
        + float(np.max(dots / temperature))
    )
    gradient = np.zeros_like(x)
    np.add.at(gradient, ii, weights[:, None] * x[jj])
    np.add.at(gradient, jj, weights[:, None] * x[ii])

    values = q_values(x, diagonal, linear)
    deficits = np.maximum(0.0, margin - values)
    loss = smooth_max + penalty * float(np.mean(deficits * deficits))
    q_gradient = 2.0 * diagonal * x + linear
    gradient -= (
        2.0 * penalty / number * deficits[:, None] * q_gradient
    )
    gradient -= np.sum(gradient * x, axis=1)[:, None] * x
    return loss, gradient


def optimize(
    seed: int,
    family: str,
    number: int,
    iterations: int,
    margin: float,
) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    diagonal, linear = family_data(family)
    x = initialize(rng, number, diagonal, linear, margin)
    first = np.zeros_like(x)
    second = np.zeros_like(x)
    best: tuple[float, np.ndarray] | None = None

    for step in range(1, iterations + 1):
        fraction = (step - 1) / max(1, iterations - 1)
        temperature = 0.04 * (0.004 / 0.04) ** fraction
        learning_rate = 0.025 * (0.003 / 0.025) ** fraction
        penalty = 200.0 * (2000.0 / 200.0) ** fraction
        _, gradient = objective_gradient(
            x, diagonal, linear, temperature, margin, penalty
        )
        first = 0.9 * first + 0.1 * gradient
        second = 0.999 * second + 0.001 * gradient * gradient
        first_hat = first / (1.0 - 0.9**step)
        second_hat = second / (1.0 - 0.999**step)
        x -= learning_rate * first_hat / (np.sqrt(second_hat) + 1e-8)
        x /= np.linalg.norm(x, axis=1)[:, None]

        if step % 50 == 0 or step == iterations:
            gram = x @ x.T
            np.fill_diagonal(gram, -math.inf)
            maximum = float(np.max(gram))
            minimum_q = float(np.min(q_values(x, diagonal, linear)))
            score = maximum + 1000.0 * max(0.0, margin - minimum_q)
            if best is None or score < best[0]:
                best = score, x.copy()

    assert best is not None
    x = best[1]
    gram = x @ x.T
    np.fill_diagonal(gram, -math.inf)
    eigenvalues = np.linalg.eigvalsh(x @ x.T)
    return {
        "seed": seed,
        "family": family,
        "maximum_inner_product": float(np.max(gram)),
        "minimum_q": float(np.min(q_values(x, diagonal, linear))),
        "frame_eigenvalues": np.linalg.eigvalsh(x.T @ x).tolist(),
        "gram_positive_eigenvalues": eigenvalues[-5:].tolist(),
        "coordinate_checksum": float(np.sum(np.arange(1, number + 1)[:, None] * x)),
        "coordinates": x.tolist(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--families", default="belt,two_caps,shifted_cap"
    )
    parser.add_argument("--number", type=int, default=41)
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--iterations", type=int, default=6000)
    parser.add_argument("--margin", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=527041)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    all_results: dict[str, list[dict[str, object]]] = {}
    for family_index, family in enumerate(args.families.split(",")):
        results = []
        for start in range(args.starts):
            result = optimize(
                args.seed + 1000 * family_index + start,
                family,
                args.number,
                args.iterations,
                args.margin,
            )
            results.append(result)
            print(
                family,
                start,
                result["maximum_inner_product"],
                result["minimum_q"],
                flush=True,
            )
        results.sort(key=lambda result: result["maximum_inner_product"])
        all_results[family] = results

    payload = {
        "status": "NUMERICAL EVIDENCE ONLY",
        "warning": (
            "Floating-point near-configurations neither construct an exact code "
            "nor prove nonexistence."
        ),
        "numpy_version": np.__version__,
        "parameters": vars(args),
        "results": all_results,
    }
    Path(args.output).write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
