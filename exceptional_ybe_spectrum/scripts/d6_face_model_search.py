#!/usr/bin/env python3
"""Numerical search in a controlled-reflection/face ansatz.

This is a discovery program, not a nonexistence verifier.

Write V = C^2 tensor C^m, d = 2m.  Given an orthonormal basis
psi_1,...,psi_d of V and Bloch-sphere reflections

    A_j = (n_j . sigma) tensor I_m,

put

    H = sum_j A_j tensor |psi_j><psi_j|.

Hermiticity, H^2=I, and Tr(H)=0 hold identically.  We optimize the
exceptional cubic residual over the unitary basis and the d Bloch vectors.
A soft penalty on sum_j n_j encourages the automatically necessary second
partial-trace condition.  Any possible output must still be exactified and
independently verified.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import expm


LAMBDA = 1.0 / 3.0
PAULI = np.asarray(
    [
        [[0.0, 1.0], [1.0, 0.0]],
        [[0.0, -1.0j], [1.0j, 0.0]],
        [[1.0, 0.0], [0.0, -1.0]],
    ],
    dtype=np.complex128,
)


def random_unitary(d: int, rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(d, d)) + 1.0j * rng.normal(size=(d, d))
    q, r = np.linalg.qr(z)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1.0)
    return q @ np.diag(phases.conj())


def random_bloch_vectors(d: int, rng: np.random.Generator) -> np.ndarray:
    vectors = rng.normal(size=(d, 3))
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


def build_h(unitary: np.ndarray, vectors: np.ndarray) -> np.ndarray:
    d = unitary.shape[0]
    if d % 2:
        raise ValueError("the face ansatz requires even local dimension")
    m = d // 2
    identity_m = np.eye(m)
    h = np.zeros((d * d, d * d), dtype=np.complex128)
    for j in range(d):
        reflection = sum(vectors[j, k] * PAULI[k] for k in range(3))
        reflection = np.kron(reflection, identity_m)
        psi = unitary[:, j]
        projection = np.outer(psi, psi.conj())
        h += np.kron(reflection, projection)
    return h


def partial_trace_first(a: np.ndarray, d: int) -> np.ndarray:
    return np.einsum("ijil->jl", a.reshape(d, d, d, d))


def partial_trace_third(a: np.ndarray, d: int) -> np.ndarray:
    return np.einsum(
        "abcABc->abAB", a.reshape(d, d, d, d, d, d)
    ).reshape(d * d, d * d)


def partial_trace_first_site(a: np.ndarray, d: int) -> np.ndarray:
    return np.einsum(
        "abcaBC->bcBC", a.reshape(d, d, d, d, d, d)
    ).reshape(d * d, d * d)


def value_and_gradient_h(h: np.ndarray, d: int) -> tuple[float, np.ndarray, float]:
    identity_d = np.eye(d)
    h1 = np.kron(h, identity_d)
    h2 = np.kron(identity_d, h)
    residual = (
        h1 @ h2 @ h1
        - h2 @ h1 @ h2
        - LAMBDA * (h1 - h2)
    )
    value = float(np.vdot(residual, residual).real)

    g1 = 2.0 * (
        h2 @ h1 @ residual
        + residual @ h1 @ h2
        - h2 @ residual @ h2
        - LAMBDA * residual
    )
    g2 = 2.0 * (
        h1 @ residual @ h1
        - h1 @ h2 @ residual
        - residual @ h2 @ h1
        + LAMBDA * residual
    )
    gradient = partial_trace_third(g1, d) + partial_trace_first_site(g2, d)
    gradient = (gradient + gradient.conj().T) / 2.0
    return value, gradient, float(np.linalg.norm(residual))


def parameter_gradients(
    h: np.ndarray,
    gradient_h: np.ndarray,
    unitary: np.ndarray,
    vectors: np.ndarray,
    standardness_penalty: float,
) -> tuple[np.ndarray, np.ndarray, float]:
    d = unitary.shape[0]
    m = d // 2
    identity_m = np.eye(m)

    # If U -> exp(tK)U, then H -> (I tensor exp(tK)) H
    # (I tensor exp(-tK)).  The anti-Hermitian matrix below is the
    # steepest-descent generator for the real Hilbert--Schmidt metric.
    commutator = h @ gradient_h - gradient_h @ h
    generator = partial_trace_first(commutator, d)
    generator = (generator - generator.conj().T) / 2.0

    vector_gradient = np.zeros_like(vectors)
    reshaped = gradient_h.reshape(d, d, d, d)
    for j in range(d):
        psi = unitary[:, j]
        # Contract the second-site legs against |psi_j><psi_j|.
        left_gradient = np.einsum(
            "arbs,r,s->ab", reshaped, psi.conj(), psi, optimize=True
        )
        for k in range(3):
            direction = np.kron(PAULI[k], identity_m)
            vector_gradient[j, k] = float(
                np.trace(left_gradient.conj().T @ direction).real
            )

    vector_sum = np.sum(vectors, axis=0)
    penalty_value = standardness_penalty * float(vector_sum @ vector_sum)
    if standardness_penalty:
        vector_gradient += 2.0 * standardness_penalty * vector_sum

    # Tangent projection for the product of Bloch spheres.
    vector_gradient -= (
        np.sum(vector_gradient * vectors, axis=1, keepdims=True) * vectors
    )
    return generator, vector_gradient, penalty_value


def objective(
    unitary: np.ndarray,
    vectors: np.ndarray,
    standardness_penalty: float,
    need_gradient: bool,
):
    h = build_h(unitary, vectors)
    value, gradient_h, residual_norm = value_and_gradient_h(h, unitary.shape[0])
    generator, vector_gradient, penalty_value = parameter_gradients(
        h, gradient_h, unitary, vectors, standardness_penalty
    )
    total = value + penalty_value
    if need_gradient:
        return total, h, residual_norm, generator, vector_gradient
    return total, h, residual_norm


def diagnostics(h: np.ndarray, vectors: np.ndarray, residual_norm: float) -> dict:
    d = vectors.shape[0]
    tr_first = partial_trace_first(h, d)
    tr_second = np.einsum("ijkj->ik", h.reshape(d, d, d, d))
    return {
        "residual_frobenius": residual_norm,
        "hermiticity_error": float(np.linalg.norm(h - h.conj().T)),
        "involution_error": float(np.linalg.norm(h @ h - np.eye(d * d))),
        "trace_abs": float(abs(np.trace(h))),
        "partial_trace_first_norm": float(np.linalg.norm(tr_first)),
        "partial_trace_second_norm": float(np.linalg.norm(tr_second)),
        "bloch_sum_norm": float(np.linalg.norm(np.sum(vectors, axis=0))),
    }


def emit(item: dict, output: Path | None) -> None:
    line = json.dumps(item, sort_keys=True)
    print(line, flush=True)
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def run(args: argparse.Namespace) -> int:
    d = args.dimension
    if d % 2:
        raise ValueError("dimension must be even")
    rng = np.random.default_rng(args.seed)
    unitary = random_unitary(d, rng)
    vectors = random_bloch_vectors(d, rng)
    output = Path(args.output).resolve() if args.output else None
    run_id = f"d{d}_face_seed{args.seed}"

    emit(
        {
            "event": "start",
            "run_id": run_id,
            "unix_time": time.time(),
            "dimension": d,
            "seed": args.seed,
            "max_iterations": args.max_iterations,
            "standardness_penalty": args.standardness_penalty,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "python": sys.version.replace("\n", " "),
            "platform": platform.platform(),
        },
        output,
    )

    start = time.monotonic()
    step = args.initial_step
    status = "max_iterations"
    for iteration in range(args.max_iterations + 1):
        total, h, residual_norm, generator, vector_gradient = objective(
            unitary, vectors, args.standardness_penalty, True
        )
        gradient_norm_sq = float(
            np.vdot(generator, generator).real
            + np.vdot(vector_gradient, vector_gradient).real
        )
        if iteration % args.progress_every == 0:
            emit(
                {
                    "event": "progress",
                    "run_id": run_id,
                    "iteration": iteration,
                    "elapsed_seconds": time.monotonic() - start,
                    "objective": total,
                    "residual_frobenius": residual_norm,
                    "parameter_gradient_norm": gradient_norm_sq**0.5,
                    "step": step,
                },
                output,
            )
        if residual_norm <= args.residual_tolerance:
            status = "residual_tolerance"
            break
        if gradient_norm_sq**0.5 <= args.gradient_tolerance:
            status = "stationary"
            break
        if iteration == args.max_iterations:
            break

        accepted = False
        trial_step = step
        while trial_step >= args.minimum_step:
            trial_unitary = expm(trial_step * generator) @ unitary
            trial_vectors = vectors - trial_step * vector_gradient
            trial_vectors /= np.linalg.norm(
                trial_vectors, axis=1, keepdims=True
            )
            trial_total, _, _ = objective(
                trial_unitary,
                trial_vectors,
                args.standardness_penalty,
                False,
            )
            if trial_total <= total - args.armijo * trial_step * gradient_norm_sq:
                unitary = trial_unitary
                vectors = trial_vectors
                step = min(args.maximum_step, 1.4 * trial_step)
                accepted = True
                break
            trial_step *= 0.5
        if not accepted:
            status = "line_search_failed"
            break

    total, h, residual_norm, generator, vector_gradient = objective(
        unitary, vectors, args.standardness_penalty, True
    )
    final = {
        "event": "final",
        "run_id": run_id,
        "status": status,
        "iteration": iteration,
        "elapsed_seconds": time.monotonic() - start,
        "objective": total,
        "parameter_gradient_norm": float(
            (
                np.vdot(generator, generator).real
                + np.vdot(vector_gradient, vector_gradient).real
            )
            ** 0.5
        ),
        **diagnostics(h, vectors, residual_norm),
    }
    emit(final, output)

    if residual_norm <= args.save_threshold:
        candidate_dir = Path(args.candidate_dir).resolve()
        candidate_dir.mkdir(parents=True, exist_ok=True)
        candidate = candidate_dir / f"{run_id}.npz"
        if candidate.exists() and not args.overwrite_candidate:
            raise FileExistsError(
                f"candidate already exists: {candidate}; "
                "pass --overwrite-candidate to replace it"
            )
        np.savez_compressed(
            candidate,
            h=h,
            unitary=unitary,
            bloch_vectors=vectors,
            metadata=json.dumps(final, sort_keys=True),
        )
        emit(
            {"event": "candidate_saved", "run_id": run_id, "path": str(candidate)},
            output,
        )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimension", type=int, default=6)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--max-iterations", type=int, default=1500)
    parser.add_argument("--standardness-penalty", type=float, default=10.0)
    parser.add_argument("--initial-step", type=float, default=0.05)
    parser.add_argument("--maximum-step", type=float, default=0.5)
    parser.add_argument("--minimum-step", type=float, default=1e-14)
    parser.add_argument("--armijo", type=float, default=1e-4)
    parser.add_argument("--gradient-tolerance", type=float, default=1e-10)
    parser.add_argument("--residual-tolerance", type=float, default=1e-9)
    parser.add_argument("--save-threshold", type=float, default=1e-6)
    parser.add_argument("--progress-every", type=int, default=100)
    parser.add_argument(
        "--output",
        default="results/d6_face_model_runs.jsonl",
    )
    parser.add_argument(
        "--candidate-dir",
        default="results/d6_face_candidates",
    )
    parser.add_argument("--overwrite-candidate", action="store_true")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
