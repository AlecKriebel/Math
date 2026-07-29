#!/usr/bin/env python3
"""Search for braided subspaces of the exact d=8 amplification.

Let H4 be the published exceptional involution on C^4 tensor C^4 and
let H8 = H4 boxtimes I_2.  A rank-r local projection Q defines a
square-invariant subspace precisely when

    [H8, Q tensor Q] = 0.

The optimization is over the complex Grassmannian of rank-r projections
in C^8.  It uses the exact Euclidean gradient of the squared commutator
and an exponential Grassmann retraction with Armijo backtracking.

Numerical output is discovery evidence only.  A zero residual would still
need exact recognition and a separate exact verifier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import expm


def matrices() -> tuple[np.ndarray, np.ndarray]:
    identity = np.eye(2, dtype=np.complex128)
    x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    j = np.array([[0, -1], [1, 0]], dtype=np.complex128)

    def word(*letters: np.ndarray) -> np.ndarray:
        result = np.array([[1]], dtype=np.complex128)
        for letter in letters:
            result = np.kron(result, letter)
        return result

    h4 = (
        -word(z, identity, z, z) / np.sqrt(6)
        - word(z, identity, j, j) / np.sqrt(6)
        - word(j, identity, z, j) / np.sqrt(6)
        + word(j, identity, j, z) / np.sqrt(6)
        - word(x, identity, x, x) / np.sqrt(3)
    )

    # np.kron(h4, I_4) initially has factor order A1,A2,C1,C2.
    # Move it to the site order (A1,C1),(A2,C2).
    grouped = np.kron(h4, np.eye(4, dtype=np.complex128))
    tensor = grouped.reshape(4, 4, 2, 2, 4, 4, 2, 2)
    h8 = tensor.transpose(0, 2, 1, 3, 4, 6, 5, 7).reshape(64, 64)

    assert np.linalg.norm(h4 - h4.conj().T) < 1e-12
    assert np.linalg.norm(h4 @ h4 - np.eye(16)) < 1e-12
    assert np.linalg.norm(h8 - h8.conj().T) < 1e-12
    assert np.linalg.norm(h8 @ h8 - np.eye(64)) < 1e-12
    return h4, h8


def random_projection(
    rng: np.random.Generator, dimension: int, rank: int
) -> np.ndarray:
    matrix = (
        rng.standard_normal((dimension, rank))
        + 1j * rng.standard_normal((dimension, rank))
    )
    frame, triangular = np.linalg.qr(matrix)
    phases = np.diag(triangular)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1)
    frame = frame * phases.conj()
    return frame @ frame.conj().T


def objective_and_gradient(
    projection: np.ndarray, interaction: np.ndarray
) -> tuple[float, np.ndarray]:
    pair_projection = np.kron(projection, projection)
    commutator = interaction @ pair_projection - pair_projection @ interaction
    objective = float(
        np.vdot(commutator, commutator).real / interaction.shape[0]
    )

    # For the unnormalized objective,
    # grad_A ||[H,A]||_F^2 = 4(A-H A H).
    pair_gradient = 4 * (
        pair_projection - interaction @ pair_projection @ interaction
    ) / interaction.shape[0]
    tensor_gradient = pair_gradient.reshape(8, 8, 8, 8)
    first = np.einsum(
        "ikjl,lk->ij", tensor_gradient, projection, optimize=True
    )
    second = np.einsum(
        "jkil,ij->kl", tensor_gradient, projection, optimize=True
    )
    gradient = first + second
    gradient = (gradient + gradient.conj().T) / 2
    return objective, gradient


def tangent_gradient(
    projection: np.ndarray, gradient: np.ndarray
) -> np.ndarray:
    complement = np.eye(projection.shape[0]) - projection
    result = (
        projection @ gradient @ complement
        + complement @ gradient @ projection
    )
    return (result + result.conj().T) / 2


def retract(
    projection: np.ndarray, gradient: np.ndarray, step: float
) -> np.ndarray:
    generator = projection @ gradient - gradient @ projection
    unitary = expm(step * generator)
    result = unitary @ projection @ unitary.conj().T
    return (result + result.conj().T) / 2


def gradient_check(
    projection: np.ndarray,
    interaction: np.ndarray,
    rng: np.random.Generator,
) -> float:
    objective, gradient = objective_and_gradient(projection, interaction)
    random_hermitian = (
        rng.standard_normal((8, 8))
        + 1j * rng.standard_normal((8, 8))
    )
    random_hermitian = (
        random_hermitian + random_hermitian.conj().T
    ) / 2
    direction = tangent_gradient(projection, random_hermitian)
    generator = direction @ projection - projection @ direction

    epsilon = 1e-6
    plus_unitary = expm(epsilon * generator)
    minus_unitary = expm(-epsilon * generator)
    plus_projection = plus_unitary @ projection @ plus_unitary.conj().T
    minus_projection = minus_unitary @ projection @ minus_unitary.conj().T
    plus = objective_and_gradient(plus_projection, interaction)[0]
    minus = objective_and_gradient(minus_projection, interaction)[0]
    finite_difference = (plus - minus) / (2 * epsilon)

    actual_direction = generator @ projection - projection @ generator
    analytic = float(
        np.vdot(gradient, actual_direction).real
    )
    scale = max(1.0, abs(finite_difference), abs(analytic), abs(objective))
    return abs(finite_difference - analytic) / scale


def optimize(
    initial: np.ndarray,
    interaction: np.ndarray,
    maximum_iterations: int,
    tolerance: float,
) -> tuple[np.ndarray, dict[str, float | int | str]]:
    projection = initial
    objective, gradient = objective_and_gradient(projection, interaction)
    initial_objective = objective
    accepted_steps = 0
    status = "maximum_iterations"

    for iteration in range(maximum_iterations):
        tangent = tangent_gradient(projection, gradient)
        gradient_norm = float(np.linalg.norm(tangent))
        if objective <= tolerance:
            status = "objective_tolerance"
            break
        if gradient_norm <= 1e-11:
            status = "stationary"
            break

        directional_derivative = -(gradient_norm**2)
        step = 1.0
        accepted = False
        for _ in range(30):
            candidate = retract(projection, gradient, step)
            candidate_objective, candidate_gradient = objective_and_gradient(
                candidate, interaction
            )
            if candidate_objective <= (
                objective + 1e-4 * step * directional_derivative
            ):
                projection = candidate
                objective = candidate_objective
                gradient = candidate_gradient
                accepted_steps += 1
                accepted = True
                break
            step *= 0.5
        if not accepted:
            status = "line_search_failed"
            break
    else:
        iteration = maximum_iterations - 1

    eigenvalues = np.linalg.eigvalsh(projection)
    return projection, {
        "initial_objective": initial_objective,
        "final_objective": objective,
        "tangent_gradient_norm": float(
            np.linalg.norm(tangent_gradient(projection, gradient))
        ),
        "iterations": iteration + 1,
        "accepted_steps": accepted_steps,
        "status": status,
        "projection_idempotence": float(
            np.linalg.norm(projection @ projection - projection)
        ),
        "projection_trace": float(np.trace(projection).real),
        "eigenvalue_min": float(eigenvalues[0]),
        "eigenvalue_max": float(eigenvalues[-1]),
    }


def source_hash() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rank", type=int, choices=range(1, 8), required=True)
    parser.add_argument("--seed-start", type=int, required=True)
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--maximum-iterations", type=int, default=2000)
    parser.add_argument("--tolerance", type=float, default=1e-24)
    parser.add_argument("--gradient-check", action="store_true")
    parser.add_argument(
        "--output-jsonl",
        type=Path,
        help="optional path for an exact copy of every emitted JSON record",
    )
    args = parser.parse_args()

    emitted: list[str] = []

    def emit(record: dict[str, object]) -> None:
        line = json.dumps(record, sort_keys=True)
        emitted.append(line)
        print(line, flush=True)

    _, interaction = matrices()
    metadata = {
        "kind": "metadata",
        "rank": args.rank,
        "seed_start": args.seed_start,
        "runs": args.runs,
        "maximum_iterations": args.maximum_iterations,
        "tolerance": args.tolerance,
        "source_sha256": source_hash(),
        "python": sys.version.replace("\n", " "),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "platform": platform.platform(),
    }
    emit(metadata)

    if args.gradient_check:
        rng = np.random.default_rng(args.seed_start)
        projection = random_projection(rng, 8, args.rank)
        error = gradient_check(projection, interaction, rng)
        emit(
            {
                "kind": "gradient_check",
                "relative_error": error,
                "seed": args.seed_start,
            }
        )
        if error > 1e-7:
            raise RuntimeError(f"gradient check failed: {error}")

    for offset in range(args.runs):
        seed = args.seed_start + offset
        rng = np.random.default_rng(seed)
        initial = random_projection(rng, 8, args.rank)
        started = time.time()
        projection, result = optimize(
            initial,
            interaction,
            args.maximum_iterations,
            args.tolerance,
        )
        result.update(
            {
                "kind": "run",
                "seed": seed,
                "elapsed_seconds": time.time() - started,
                "projection_sha256": hashlib.sha256(
                    np.ascontiguousarray(projection).view(np.uint8)
                ).hexdigest(),
            }
        )
        emit(result)

    if args.output_jsonl is not None:
        args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
        args.output_jsonl.write_text("\n".join(emitted) + "\n")


if __name__ == "__main__":
    main()
