#!/usr/bin/env python3
"""Reproducible Grassmann-manifold searches for the d=6 exceptional YBE.

This is a falsifier/discovery program, not a nonexistence certificate.  It
keeps H exactly (up to roundoff) on the orbit of a signature-(18,18)
Hermitian involution and minimizes the squared Frobenius norm of

    H_12 H_23 H_12 - H_23 H_12 H_23 - (H_12-H_23)/3.

Several optional block symmetries test independent qubit-qutrit and
4+2-sector ansatz families.  ``one_sided_4plus2`` fixes only the
16-dimensional W tensor W cell and leaves its 20-dimensional orthogonal
complement fully mixed; unlike ``local_4plus2``, it does not assume that
U tensor U is invariant.  The analytic gradient is pulled back from the
three-site residual, projected to the appropriate symmetry commutant, and
then projected to the Grassmann tangent space.
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


def pair_labels(d: int, symmetry: str) -> np.ndarray:
    """Return a block label for each basis vector of V tensor V."""
    if symmetry == "none":
        return np.zeros(d * d, dtype=np.int64)
    if d != 6:
        raise ValueError(f"symmetry {symmetry!r} is implemented only for d=6")

    labels: list[int] = []
    for i in range(d):
        ai, ri = divmod(i, 3)
        for j in range(d):
            aj, rj = divmod(j, 3)
            if symmetry == "z3_sum":
                label = (ri + rj) % 3
            elif symmetry == "z3_difference":
                label = (ri - rj) % 3
            elif symmetry == "z2_parity":
                label = (ai + aj) % 2
            elif symmetry == "z2_z3":
                label = 3 * ((ai + aj) % 2) + ((ri + rj) % 3)
            elif symmetry == "local_4plus2":
                label = 2 * int(i >= 4) + int(j >= 4)
            elif symmetry == "one_sided_4plus2":
                label = int(not (i < 4 and j < 4))
            else:
                raise ValueError(f"unknown symmetry {symmetry!r}")
            labels.append(label)
    return np.asarray(labels, dtype=np.int64)


def random_unitary_involution(
    d: int,
    labels: np.ndarray,
    rng: np.random.Generator,
    field: str,
    initial: str,
) -> np.ndarray:
    """Construct a block-preserving trace-zero Hermitian involution."""
    n = d * d
    h = np.zeros((n, n), dtype=np.complex128)

    if initial == "manin_orthogonalized":
        if d != 6 or field != "complex" or np.unique(labels).size != 1:
            raise ValueError(
                "manin_orthogonalized requires d=6, complex field, "
                "and symmetry none"
            )
        # Orthogonally project onto the (-1)-eigenspace of the standard
        # balanced GL(3|3) Manin Hecke operator at t=exp(i*pi/6).
        # The algebraic Manin operator itself is nonnormal. Its (-1)
        # eigenvectors nevertheless have disjoint supports:
        # odd diagonals |aa>, and |ij>-t|ji> for every i<j.
        t = np.exp(1j * np.pi / 6.0)
        minus_vectors: list[np.ndarray] = []
        for odd in range(3, 6):
            vector = np.zeros(n, dtype=np.complex128)
            vector[odd * d + odd] = 1.0
            minus_vectors.append(vector)
        for first in range(d):
            for second in range(first + 1, d):
                vector = np.zeros(n, dtype=np.complex128)
                vector[first * d + second] = 1.0 / np.sqrt(2.0)
                vector[second * d + first] = -t / np.sqrt(2.0)
                minus_vectors.append(vector)
        frame = np.column_stack(minus_vectors)
        if frame.shape != (36, 18):
            raise AssertionError(f"unexpected Manin frame {frame.shape}")
        if np.linalg.norm(frame.conj().T @ frame - np.eye(18)) > 1e-12:
            raise AssertionError("Manin (-1)-frame is not orthonormal")
        projector = frame @ frame.conj().T
        h = np.eye(n, dtype=np.complex128) - 2.0 * projector

        # A small, fully recorded seed-dependent Grassmann perturbation
        # avoids drawing a conclusion from one symmetry-stationary start.
        skew_seed = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        skew_seed = skew_seed - skew_seed.conj().T
        skew_seed *= 0.05 / np.linalg.norm(skew_seed)
        perturbation = expm(skew_seed)
        return perturbation @ h @ perturbation.conj().T

    for label in np.unique(labels):
        indices = np.flatnonzero(labels == label)
        size = len(indices)
        if size % 2:
            raise ValueError(
                f"block {int(label)} has odd size {size}; half signature impossible"
            )
        z = rng.normal(size=(size, size))
        if field == "complex":
            z = z + 1j * rng.normal(size=(size, size))
        q, _ = np.linalg.qr(z)
        signature = np.diag(
            np.r_[np.ones(size // 2), -np.ones(size // 2)]
        )
        block = q @ signature @ q.conj().T
        h[np.ix_(indices, indices)] = block

    if initial == "h4_block":
        allowed_labels = (
            pair_labels(6, "local_4plus2"),
            pair_labels(6, "one_sided_4plus2"),
        )
        if d != 6 or not any(
            np.array_equal(labels, allowed) for allowed in allowed_labels
        ):
            raise ValueError(
                "h4_block requires d=6 and symmetry local_4plus2 "
                "or one_sided_4plus2"
            )
        i2 = np.eye(2)
        x = np.array([[0.0, 1.0], [1.0, 0.0]])
        z = np.array([[1.0, 0.0], [0.0, -1.0]])
        j = np.array([[0.0, -1.0], [1.0, 0.0]])

        def kron_all(*factors: np.ndarray) -> np.ndarray:
            out = np.array([[1.0]])
            for factor in factors:
                out = np.kron(out, factor)
            return out

        h4 = (
            -kron_all(z, i2, z, z) / np.sqrt(6.0)
            - kron_all(z, i2, j, j) / np.sqrt(6.0)
            - kron_all(j, i2, z, j) / np.sqrt(6.0)
            + kron_all(j, i2, j, z) / np.sqrt(6.0)
            - kron_all(x, i2, x, x) / np.sqrt(3.0)
        )
        four_by_four_indices = np.asarray(
            [i * d + j for i in range(4) for j in range(4)], dtype=np.int64
        )
        h[np.ix_(four_by_four_indices, four_by_four_indices)] = h4

    if field == "real":
        h = h.real
    return h


class ResidualProblem:
    def __init__(
        self,
        d: int,
        labels: np.ndarray,
        field: str,
        partial_trace_penalty: float,
    ):
        self.d = d
        self.n = d * d
        self.eye_d = np.eye(d)
        self.labels = labels
        self.block_mask = labels[:, None] == labels[None, :]
        self.field = field
        self.partial_trace_penalty = partial_trace_penalty

    def partial_trace_second_local(self, h: np.ndarray) -> np.ndarray:
        d = self.d
        return np.einsum("ijkj->ik", h.reshape(d, d, d, d))

    def partial_trace_first_local(self, h: np.ndarray) -> np.ndarray:
        d = self.d
        return np.einsum("ijil->jl", h.reshape(d, d, d, d))

    def partial_trace_3(self, a: np.ndarray) -> np.ndarray:
        d, n = self.d, self.n
        return np.einsum(
            "abcABc->abAB", a.reshape(d, d, d, d, d, d)
        ).reshape(n, n)

    def partial_trace_1(self, a: np.ndarray) -> np.ndarray:
        d, n = self.d, self.n
        return np.einsum(
            "abcaBC->bcBC", a.reshape(d, d, d, d, d, d)
        ).reshape(n, n)

    def tangent_projection(self, x: np.ndarray, h: np.ndarray) -> np.ndarray:
        x = np.where(self.block_mask, x, 0.0)
        x = (x + x.conj().T) / 2.0
        if self.field == "real":
            x = x.real
        tangent = (x - h @ x @ h) / 2.0
        tangent = np.where(self.block_mask, tangent, 0.0)
        tangent = (tangent + tangent.conj().T) / 2.0
        if self.field == "real":
            tangent = tangent.real
        return tangent

    def value_gradient(
        self, h: np.ndarray, need_gradient: bool = True
    ) -> tuple[float, np.ndarray, float, float] | float:
        h1 = np.kron(h, self.eye_d)
        h2 = np.kron(self.eye_d, h)
        residual = (
            h1 @ h2 @ h1
            - h2 @ h1 @ h2
            - LAMBDA * (h1 - h2)
        )
        value = float(np.vdot(residual, residual).real)
        partial_second = self.partial_trace_second_local(h)
        partial_first = self.partial_trace_first_local(h)
        if self.partial_trace_penalty:
            value += self.partial_trace_penalty * float(
                np.vdot(partial_second, partial_second).real
                + np.vdot(partial_first, partial_first).real
            )
        if not need_gradient:
            return value

        # If F is the residual, differentiating Tr(F^* F)=Tr(F^2)
        # at Hermitian H gives the following gradients with respect to H_12
        # and H_23.  Pulling them back uses the third- and first-site
        # partial traces, respectively.
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
        gradient = self.partial_trace_3(g1) + self.partial_trace_1(g2)
        if self.partial_trace_penalty:
            gradient += 2.0 * self.partial_trace_penalty * (
                np.kron(partial_second, self.eye_d)
                + np.kron(self.eye_d, partial_first)
            )
        gradient = self.tangent_projection(gradient, h)
        return (
            value,
            gradient,
            float(np.linalg.norm(residual)),
            float(np.linalg.norm(gradient)),
        )


def diagnostics(problem: ResidualProblem, h: np.ndarray) -> dict[str, float]:
    d = problem.d
    value, gradient, residual_norm, gradient_norm = problem.value_gradient(h)
    a = problem.partial_trace_second_local(h)
    b = problem.partial_trace_first_local(h)
    return {
        "objective": value,
        "residual_frobenius": residual_norm,
        "gradient_frobenius": gradient_norm,
        "hermiticity_error": float(np.linalg.norm(h - h.conj().T)),
        "involution_error": float(np.linalg.norm(h @ h - np.eye(d * d))),
        "trace_abs": float(abs(np.trace(h))),
        "partial_trace_1_scalar_deviation": float(
            np.linalg.norm(a - np.trace(a) * np.eye(d) / d)
        ),
        "partial_trace_2_scalar_deviation": float(
            np.linalg.norm(b - np.trace(b) * np.eye(d) / d)
        ),
    }


def emit(event: dict, output_path: Path | None) -> None:
    line = json.dumps(event, sort_keys=True)
    print(line, flush=True)
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def run(args: argparse.Namespace) -> int:
    labels = pair_labels(args.dimension, args.symmetry)
    rng = np.random.default_rng(args.seed)
    h = random_unitary_involution(
        args.dimension, labels, rng, args.field, args.initial
    )
    problem = ResidualProblem(
        args.dimension, labels, args.field, args.partial_trace_penalty
    )
    output_path = Path(args.output).resolve() if args.output else None

    run_id = (
        f"d{args.dimension}_{args.field}_{args.symmetry}_{args.initial}"
        f"_seed{args.seed}"
    )
    metadata = {
        "event": "start",
        "run_id": run_id,
        "unix_time": time.time(),
        "dimension": args.dimension,
        "field": args.field,
        "symmetry": args.symmetry,
        "initial": args.initial,
        "seed": args.seed,
        "max_iterations": args.max_iterations,
        "partial_trace_penalty": args.partial_trace_penalty,
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "block_sizes": [
            int(np.count_nonzero(labels == label)) for label in np.unique(labels)
        ],
    }
    emit(metadata, output_path)

    step = args.initial_step
    previous_gradient: np.ndarray | None = None
    previous_direction: np.ndarray | None = None
    start = time.monotonic()
    status = "max_iterations"

    for iteration in range(args.max_iterations + 1):
        value, gradient, residual_norm, gradient_norm = problem.value_gradient(h)

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
                output_path,
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
            transported_gradient = problem.tangent_projection(previous_gradient, h)
            transported_direction = problem.tangent_projection(previous_direction, h)
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
        generator = (direction @ h - h @ direction) / 4.0
        trial_step = min(step, args.maximum_step)
        accepted = False

        for line_search_iteration in range(args.max_line_search):
            unitary = expm(trial_step * generator)
            trial_h = unitary @ h @ unitary.conj().T
            trial_value = problem.value_gradient(trial_h, need_gradient=False)
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
        h = trial_h
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
        **diagnostics(problem, h),
    }
    emit(final, output_path)

    if args.save_threshold is not None:
        if final["residual_frobenius"] <= args.save_threshold:
            candidate_path = Path(args.candidate_directory) / f"{run_id}.npz"
            candidate_path.parent.mkdir(parents=True, exist_ok=True)
            if candidate_path.exists() and not args.overwrite_candidate:
                emit(
                    {
                        "event": "candidate_preserved",
                        "run_id": run_id,
                        "path": str(candidate_path.resolve()),
                        "reason": (
                            "existing archive not overwritten; pass "
                            "--overwrite-candidate to replace it"
                        ),
                    },
                    output_path,
                )
                return 0
            np.savez_compressed(
                candidate_path,
                h=h,
                metadata=json.dumps({**metadata, **final}, sort_keys=True),
            )
            emit(
                {
                    "event": "candidate_saved",
                    "run_id": run_id,
                    "path": str(candidate_path.resolve()),
                },
                output_path,
            )
    return 0


def gradient_check(args: argparse.Namespace) -> int:
    labels = pair_labels(args.dimension, args.symmetry)
    rng = np.random.default_rng(args.seed)
    h = random_unitary_involution(
        args.dimension, labels, rng, args.field, args.initial
    )
    problem = ResidualProblem(
        args.dimension, labels, args.field, args.partial_trace_penalty
    )
    value, gradient, _, _ = problem.value_gradient(h)
    x = rng.normal(size=h.shape)
    if args.field == "complex":
        x = x + 1j * rng.normal(size=h.shape)
    x = problem.tangent_projection(x, h)
    x /= np.linalg.norm(x)
    generator = (x @ h - h @ x) / 4.0
    exact_derivative = float(np.vdot(gradient, x).real)
    checks = []
    for epsilon in (1e-4, 1e-5, 1e-6):
        unitary = expm(epsilon * generator)
        trial_h = unitary @ h @ unitary.conj().T
        difference_quotient = (
            problem.value_gradient(trial_h, need_gradient=False) - value
        ) / epsilon
        checks.append(
            {
                "epsilon": epsilon,
                "difference_quotient": difference_quotient,
                "analytic_derivative": exact_derivative,
                "absolute_error": abs(difference_quotient - exact_derivative),
            }
        )
    print(json.dumps({"gradient_check": checks}, indent=2, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--dimension", type=int, default=6)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--field", choices=("real", "complex"), default="complex")
    p.add_argument(
        "--symmetry",
        choices=(
            "none",
            "z3_sum",
            "z3_difference",
            "z2_parity",
            "z2_z3",
            "local_4plus2",
            "one_sided_4plus2",
        ),
        default="none",
    )
    p.add_argument(
        "--initial",
        choices=("random", "h4_block", "manin_orthogonalized"),
        default="random",
    )
    p.add_argument("--max-iterations", type=int, default=2000)
    p.add_argument("--progress-every", type=int, default=100)
    p.add_argument("--initial-step", type=float, default=0.02)
    p.add_argument("--maximum-step", type=float, default=0.5)
    p.add_argument("--step-growth", type=float, default=1.8)
    p.add_argument("--armijo-constant", type=float, default=1e-4)
    p.add_argument("--partial-trace-penalty", type=float, default=0.0)
    p.add_argument("--max-line-search", type=int, default=40)
    p.add_argument("--residual-tolerance", type=float, default=1e-10)
    p.add_argument("--gradient-tolerance", type=float, default=1e-9)
    p.add_argument("--output")
    p.add_argument("--candidate-directory", default="results/d6_candidates")
    p.add_argument("--save-threshold", type=float, default=1e-5)
    p.add_argument(
        "--overwrite-candidate",
        action="store_true",
        help="replace an existing candidate archive (disabled by default)",
    )
    p.add_argument("--gradient-check", action="store_true")
    return p


if __name__ == "__main__":
    arguments = parser().parse_args()
    if arguments.dimension * arguments.dimension % 2:
        raise SystemExit("the trace-zero signature requires even d^2")
    if arguments.gradient_check:
        raise SystemExit(gradient_check(arguments))
    raise SystemExit(run(arguments))
