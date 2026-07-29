#!/usr/bin/env python3
"""Frozen-WW search for a one-sided d=6 extension of the published d=4 H.

Let V=W+U with dimensions 4+2.  This program fixes the published
exceptional reflection on W tensor W *throughout the optimization* and
optimizes an arbitrary signature-(10,10) Hermitian involution on the full
20-dimensional orthogonal complement

    (W tensor U) + (U tensor W) + (U tensor U).

No individual complement color cell is assumed invariant.  The program is
a reproducible numerical falsifier/candidate generator, never a
nonexistence certificate.
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


COEFFICIENT = 1.0 / 3.0
DIMENSION = 6
W_DIMENSION = 4


def tensor(*matrices: np.ndarray) -> np.ndarray:
    result = np.array([[1.0]], dtype=np.complex128)
    for matrix in matrices:
        result = np.kron(result, matrix)
    return result


def published_h4() -> np.ndarray:
    identity = np.eye(2)
    x = np.array([[0.0, 1.0], [1.0, 0.0]])
    z = np.diag([1.0, -1.0])
    j = np.array([[0.0, -1.0], [1.0, 0.0]])
    return (
        -tensor(z, identity, z, z) / np.sqrt(6.0)
        - tensor(z, identity, j, j) / np.sqrt(6.0)
        - tensor(j, identity, z, j) / np.sqrt(6.0)
        + tensor(j, identity, j, z) / np.sqrt(6.0)
        - tensor(x, identity, x, x) / np.sqrt(3.0)
    )


def pair_indices() -> tuple[np.ndarray, np.ndarray]:
    fixed: list[int] = []
    complement: list[int] = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            index = DIMENSION * first + second
            if first < W_DIMENSION and second < W_DIMENSION:
                fixed.append(index)
            else:
                complement.append(index)
    return np.asarray(fixed), np.asarray(complement)


FIXED_INDICES, COMPLEMENT_INDICES = pair_indices()
FIXED_H4 = published_h4()


def assemble(complement: np.ndarray) -> np.ndarray:
    matrix = np.zeros((DIMENSION**2, DIMENSION**2), dtype=np.complex128)
    matrix[np.ix_(FIXED_INDICES, FIXED_INDICES)] = FIXED_H4
    matrix[np.ix_(COMPLEMENT_INDICES, COMPLEMENT_INDICES)] = complement
    return matrix


def random_complement(
    rng: np.random.Generator, field: str
) -> np.ndarray:
    size = len(COMPLEMENT_INDICES)
    random = rng.normal(size=(size, size))
    if field == "complex":
        random = random + 1j * rng.normal(size=(size, size))
    unitary, _ = np.linalg.qr(random)
    signature = np.diag(np.r_[np.ones(10), -np.ones(10)])
    result = unitary @ signature @ unitary.conj().T
    return result.real if field == "real" else result


def leakage_limitation_complement() -> np.ndarray:
    """The exact two-site leakage model, converted to a reflection."""
    projection = np.zeros((DIMENSION**2, DIMENSION**2), dtype=np.complex128)
    coordinate_vectors = (
        (0, 4),
        (1, 4),
        (3, 5),
        (4, 0),
        (4, 1),
        (5, 2),
        (5, 3),
        (5, 5),
    )
    for first, second in coordinate_vectors:
        index = DIMENSION * first + second
        projection[index, index] = 1.0
    for left, right in (
        ((4, 4), (2, 5)),
        ((4, 5), (2, 4)),
    ):
        left_index = DIMENSION * left[0] + left[1]
        right_index = DIMENSION * right[0] + right[1]
        for row, column in (
            (left_index, left_index),
            (left_index, right_index),
            (right_index, left_index),
            (right_index, right_index),
        ):
            projection[row, column] += 0.5
    complement_projection = projection[
        np.ix_(COMPLEMENT_INDICES, COMPLEMENT_INDICES)
    ]
    return np.eye(20) - 2.0 * complement_projection


def partial_trace_second(matrix: np.ndarray) -> np.ndarray:
    return np.einsum(
        "ijkj->ik", matrix.reshape(DIMENSION, DIMENSION, DIMENSION, DIMENSION)
    )


def partial_trace_first(matrix: np.ndarray) -> np.ndarray:
    return np.einsum(
        "ijil->jl", matrix.reshape(DIMENSION, DIMENSION, DIMENSION, DIMENSION)
    )


def pullback_trace_third(matrix: np.ndarray) -> np.ndarray:
    d = DIMENSION
    return np.einsum(
        "abcABc->abAB", matrix.reshape(d, d, d, d, d, d)
    ).reshape(d * d, d * d)


def pullback_trace_first(matrix: np.ndarray) -> np.ndarray:
    d = DIMENSION
    return np.einsum(
        "abcaBC->bcBC", matrix.reshape(d, d, d, d, d, d)
    ).reshape(d * d, d * d)


def complement_tangent(
    ambient_gradient: np.ndarray,
    complement: np.ndarray,
    field: str,
) -> np.ndarray:
    block = ambient_gradient[
        np.ix_(COMPLEMENT_INDICES, COMPLEMENT_INDICES)
    ]
    block = (block + block.conj().T) / 2.0
    if field == "real":
        block = block.real
    tangent = (block - complement @ block @ complement) / 2.0
    tangent = (tangent + tangent.conj().T) / 2.0
    return tangent.real if field == "real" else tangent


def value_gradient(
    complement: np.ndarray,
    field: str,
    partial_trace_penalty: float,
    need_gradient: bool = True,
) -> tuple[float, np.ndarray, float, float] | float:
    h = assemble(complement)
    identity = np.eye(DIMENSION)
    first = np.kron(h, identity)
    second = np.kron(identity, h)
    residual = (
        first @ second @ first
        - second @ first @ second
        - COEFFICIENT * (first - second)
    )
    residual_norm = float(np.linalg.norm(residual))
    value = residual_norm**2

    partial_second = partial_trace_second(h)
    partial_first = partial_trace_first(h)
    if partial_trace_penalty:
        value += partial_trace_penalty * float(
            np.vdot(partial_second, partial_second).real
            + np.vdot(partial_first, partial_first).real
        )
    if not need_gradient:
        return value

    gradient_first = 2.0 * (
        second @ first @ residual
        + residual @ first @ second
        - second @ residual @ second
        - COEFFICIENT * residual
    )
    gradient_second = 2.0 * (
        first @ residual @ first
        - first @ second @ residual
        - residual @ second @ first
        + COEFFICIENT * residual
    )
    ambient_gradient = pullback_trace_third(
        gradient_first
    ) + pullback_trace_first(gradient_second)
    if partial_trace_penalty:
        ambient_gradient += 2.0 * partial_trace_penalty * (
            np.kron(partial_second, identity)
            + np.kron(identity, partial_first)
        )
    tangent = complement_tangent(ambient_gradient, complement, field)
    return value, tangent, residual_norm, float(np.linalg.norm(tangent))


def leakage_diagnostics(h: np.ndarray) -> dict[str, float]:
    projection = (np.eye(DIMENSION**2) - h) / 2.0
    uu_indices = np.asarray(
        [
            DIMENSION * first + second
            for first in range(4, 6)
            for second in range(4, 6)
        ]
    )
    mixed_indices = np.asarray(
        [
            index
            for index in COMPLEMENT_INDICES
            if index not in set(uu_indices.tolist())
        ]
    )
    coupling = projection[np.ix_(mixed_indices, uu_indices)]
    uu_compression = projection[np.ix_(uu_indices, uu_indices)]
    delta_coupling = float(np.vdot(coupling, coupling).real)
    delta_variance = float(
        (
            np.trace(uu_compression)
            - np.trace(uu_compression @ uu_compression)
        ).real
    )
    return {
        "uu_mixed_coupling_frobenius": float(np.linalg.norm(coupling)),
        "delta_coupling": delta_coupling,
        "delta_variance": delta_variance,
        "uu_compression_trace": float(np.trace(uu_compression).real),
    }


def diagnostics(
    complement: np.ndarray,
    field: str,
    partial_trace_penalty: float,
) -> dict[str, float]:
    h = assemble(complement)
    value, gradient, residual_norm, gradient_norm = value_gradient(
        complement, field, partial_trace_penalty
    )
    partial_second = partial_trace_second(h)
    partial_first = partial_trace_first(h)
    return {
        "objective": value,
        "residual_frobenius": residual_norm,
        "gradient_frobenius": gradient_norm,
        "hermiticity_error": float(np.linalg.norm(h - h.conj().T)),
        "involution_error": float(np.linalg.norm(h @ h - np.eye(36))),
        "trace_abs": float(abs(np.trace(h))),
        "fixed_h4_error": float(
            np.linalg.norm(
                h[np.ix_(FIXED_INDICES, FIXED_INDICES)] - FIXED_H4
            )
        ),
        "partial_trace_first_norm": float(np.linalg.norm(partial_first)),
        "partial_trace_second_norm": float(np.linalg.norm(partial_second)),
        **leakage_diagnostics(h),
    }


def emit(event: dict[str, object], output: Path | None) -> None:
    line = json.dumps(event, sort_keys=True)
    print(line, flush=True)
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def initial_complement(args: argparse.Namespace) -> np.ndarray:
    if args.initial == "leakage_model":
        if args.field != "real":
            # A real matrix is also a valid complex initial point.
            return leakage_limitation_complement().astype(np.complex128)
        return leakage_limitation_complement().real
    rng = np.random.default_rng(args.seed)
    return random_complement(rng, args.field)


def source_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def gradient_check(args: argparse.Namespace) -> int:
    complement = initial_complement(args)
    rng = np.random.default_rng(args.seed + 1)
    ambient = rng.normal(size=(36, 36))
    if args.field == "complex":
        ambient = ambient + 1j * rng.normal(size=(36, 36))
    direction = complement_tangent(ambient, complement, args.field)
    direction /= np.linalg.norm(direction)
    value, gradient, _, _ = value_gradient(
        complement, args.field, args.partial_trace_penalty
    )
    generator = (direction @ complement - complement @ direction) / 4.0
    exact = float(np.vdot(gradient, direction).real)
    checks = []
    for epsilon in (1e-4, 1e-5, 1e-6):
        unitary_plus = expm(epsilon * generator)
        unitary_minus = expm(-epsilon * generator)
        trial_plus = (
            unitary_plus @ complement @ unitary_plus.conj().T
        )
        trial_minus = (
            unitary_minus @ complement @ unitary_minus.conj().T
        )
        forward_quotient = (
            value_gradient(
                trial_plus,
                args.field,
                args.partial_trace_penalty,
                need_gradient=False,
            )
            - value
        ) / epsilon
        central_quotient = (
            value_gradient(
                trial_plus,
                args.field,
                args.partial_trace_penalty,
                need_gradient=False,
            )
            - value_gradient(
                trial_minus,
                args.field,
                args.partial_trace_penalty,
                need_gradient=False,
            )
        ) / (2.0 * epsilon)
        checks.append(
            {
                "epsilon": epsilon,
                "forward_difference_quotient": forward_quotient,
                "central_difference_quotient": central_quotient,
                "analytic_derivative": exact,
                "forward_absolute_error": abs(forward_quotient - exact),
                "central_absolute_error": abs(central_quotient - exact),
            }
        )
    print(
        json.dumps(
            {
                "script_sha256": source_sha256(),
                "seed": args.seed,
                "field": args.field,
                "initial": args.initial,
                "partial_trace_penalty": args.partial_trace_penalty,
                "fixed_h4_error": diagnostics(
                    complement, args.field, args.partial_trace_penalty
                )["fixed_h4_error"],
                "gradient_check": checks,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def run(args: argparse.Namespace) -> int:
    complement = initial_complement(args)
    output = Path(args.output).resolve() if args.output else None
    run_id = (
        f"d6_fixed_h4_{args.field}_{args.initial}_seed{args.seed}"
        f"_pt{args.partial_trace_penalty:g}"
    )
    metadata = {
        "event": "start",
        "run_id": run_id,
        "unix_time": time.time(),
        "seed": args.seed,
        "field": args.field,
        "initial": args.initial,
        "max_iterations": args.max_iterations,
        "partial_trace_penalty": args.partial_trace_penalty,
        "script_sha256": source_sha256(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "fixed_block_size": len(FIXED_INDICES),
        "optimized_block_size": len(COMPLEMENT_INDICES),
        "optimized_signature": [10, 10],
    }
    emit(metadata, output)

    step = args.initial_step
    previous_gradient: np.ndarray | None = None
    previous_direction: np.ndarray | None = None
    start = time.monotonic()
    status = "max_iterations"

    for iteration in range(args.max_iterations + 1):
        value, gradient, residual_norm, gradient_norm = value_gradient(
            complement, args.field, args.partial_trace_penalty
        )
        if iteration % args.progress_every == 0:
            emit(
                {
                    "event": "progress",
                    "run_id": run_id,
                    "iteration": iteration,
                    "elapsed_seconds": time.monotonic() - start,
                    "objective": value,
                    "residual_frobenius": residual_norm,
                    "gradient_frobenius": gradient_norm,
                    "step": step,
                },
                output,
            )
        if residual_norm <= args.residual_tolerance:
            status = "residual_tolerance"
            break
        if gradient_norm <= args.gradient_tolerance:
            status = "stationary"
            break
        if iteration == args.max_iterations:
            break

        if previous_gradient is None:
            direction = -gradient
        else:
            transported_gradient = complement_tangent(
                assemble(previous_gradient), complement, args.field
            )
            transported_direction = complement_tangent(
                assemble(previous_direction), complement, args.field
            )
            denominator = max(
                float(np.vdot(previous_gradient, previous_gradient).real),
                np.finfo(float).tiny,
            )
            beta = max(
                0.0,
                float(
                    np.vdot(
                        gradient, gradient - transported_gradient
                    ).real
                )
                / denominator,
            )
            direction = -gradient + beta * transported_direction
            if float(np.vdot(gradient, direction).real) >= (
                -1e-6 * gradient_norm * float(np.linalg.norm(direction))
            ):
                direction = -gradient

        directional_derivative = float(np.vdot(gradient, direction).real)
        generator = (
            direction @ complement - complement @ direction
        ) / 4.0
        trial_step = min(step, args.maximum_step)
        accepted = False
        for line_search_iteration in range(args.max_line_search):
            unitary = expm(trial_step * generator)
            trial = unitary @ complement @ unitary.conj().T
            trial_value = value_gradient(
                trial,
                args.field,
                args.partial_trace_penalty,
                need_gradient=False,
            )
            if trial_value <= (
                value
                + args.armijo_constant
                * trial_step
                * directional_derivative
            ):
                accepted = True
                break
            trial_step *= 0.5
        if not accepted:
            status = "line_search_failed"
            break

        previous_gradient = gradient
        previous_direction = direction
        complement = trial
        if line_search_iteration == 0:
            step = min(args.step_growth * trial_step, args.maximum_step)
        else:
            step = trial_step

    final = {
        "event": "final",
        "run_id": run_id,
        "iteration": iteration,
        "elapsed_seconds": time.monotonic() - start,
        "status": status,
        **diagnostics(complement, args.field, args.partial_trace_penalty),
    }
    emit(final, output)

    if (
        args.save_threshold is not None
        and final["residual_frobenius"] <= args.save_threshold
    ):
        candidate = Path(args.candidate_directory) / f"{run_id}.npz"
        candidate.parent.mkdir(parents=True, exist_ok=True)
        if candidate.exists() and not args.overwrite_candidate:
            emit(
                {
                    "event": "candidate_preserved",
                    "run_id": run_id,
                    "path": str(candidate.resolve()),
                },
                output,
            )
        else:
            np.savez_compressed(
                candidate,
                h=assemble(complement),
                complement=complement,
                metadata=json.dumps({**metadata, **final}, sort_keys=True),
            )
            emit(
                {
                    "event": "candidate_saved",
                    "run_id": run_id,
                    "path": str(candidate.resolve()),
                },
                output,
            )
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--seed", type=int, required=True)
    result.add_argument("--field", choices=("real", "complex"), default="complex")
    result.add_argument(
        "--initial", choices=("random", "leakage_model"), default="random"
    )
    result.add_argument("--partial-trace-penalty", type=float, default=0.0)
    result.add_argument("--max-iterations", type=int, default=800)
    result.add_argument("--progress-every", type=int, default=200)
    result.add_argument("--initial-step", type=float, default=0.02)
    result.add_argument("--maximum-step", type=float, default=0.5)
    result.add_argument("--step-growth", type=float, default=1.8)
    result.add_argument("--armijo-constant", type=float, default=1e-4)
    result.add_argument("--max-line-search", type=int, default=40)
    result.add_argument("--residual-tolerance", type=float, default=1e-10)
    result.add_argument("--gradient-tolerance", type=float, default=1e-9)
    result.add_argument("--output")
    result.add_argument(
        "--candidate-directory", default="results/d6_fixed_h4_candidates"
    )
    result.add_argument("--save-threshold", type=float, default=1e-6)
    result.add_argument("--overwrite-candidate", action="store_true")
    result.add_argument("--gradient-check", action="store_true")
    return result


if __name__ == "__main__":
    arguments = parser().parse_args()
    if arguments.gradient_check:
        raise SystemExit(gradient_check(arguments))
    raise SystemExit(run(arguments))
