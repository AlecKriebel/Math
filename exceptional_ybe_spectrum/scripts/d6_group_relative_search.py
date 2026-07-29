#!/usr/bin/env python3
"""Search diagonal-regular finite-group invariant exceptional reflections.

This is a numerical candidate generator, not a nonexistence verifier.

Let G have order d and identify V with C[G].  In relative coordinates

    |x,y> -> |x,x^{-1}y>,

every operator commuting with the diagonal left-regular action and acting
trivially on the first relative-coordinate factor has the form

    H = T^*(I_d tensor h)T,

where h is an arbitrary trace-zero Hermitian involution in M_d.  We optimize
h on its Grassmann orbit.  The ansatz is tested for C_d and, at d=6, S_3.

All residuals are floating-point discovery data.  A small residual would
still require exact recognition and independent verification.
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
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def multiplication_table(group: str, order: int) -> np.ndarray:
    if group == "cyclic":
        return np.fromfunction(
            lambda a, b: (a + b) % order, (order, order), dtype=int
        ).astype(np.int64)
    if group == "klein":
        if order != 4:
            raise ValueError("the Klein four group has order four")
        return np.fromfunction(
            lambda a, b: np.bitwise_xor(a.astype(int), b.astype(int)),
            (order, order),
            dtype=int,
        ).astype(np.int64)
    if group == "s3":
        if order != 6:
            raise ValueError("S3 has order six")
        # Index r^a s^b by 3*b+a, with s r s = r^{-1}.
        table = np.empty((6, 6), dtype=np.int64)
        for b in range(2):
            for a in range(3):
                left = 3 * b + a
                for d in range(2):
                    for c in range(3):
                        right = 3 * d + c
                        product_a = (a + ((-1) ** b) * c) % 3
                        product_b = (b + d) % 2
                        table[left, right] = 3 * product_b + product_a
        return table
    raise ValueError(f"unknown group {group!r}")


def inverse_table(table: np.ndarray) -> np.ndarray:
    order = table.shape[0]
    identity_candidates = [
        e
        for e in range(order)
        if np.array_equal(table[e], np.arange(order))
        and np.array_equal(table[:, e], np.arange(order))
    ]
    if len(identity_candidates) != 1:
        raise ValueError("multiplication table has no unique identity")
    identity = identity_candidates[0]
    inverse = np.empty(order, dtype=np.int64)
    for element in range(order):
        candidates = np.flatnonzero(
            (table[element] == identity) & (table[:, element] == identity)
        )
        if len(candidates) != 1:
            raise ValueError("multiplication table has no unique inverse")
        inverse[element] = candidates[0]
    return inverse


def relative_permutation(table: np.ndarray) -> np.ndarray:
    """Map transformed index (x,g) to original pair index (x,xg)."""
    order = table.shape[0]
    return np.asarray(
        [
            order * x + int(table[x, g])
            for x in range(order)
            for g in range(order)
        ],
        dtype=np.int64,
    )


def random_involution(
    order: int, rng: np.random.Generator, field: str
) -> np.ndarray:
    z = rng.normal(size=(order, order))
    if field == "complex":
        z = z + 1j * rng.normal(size=(order, order))
    unitary, _ = np.linalg.qr(z)
    signature = np.diag(
        np.r_[np.ones(order // 2), -np.ones(order // 2)]
    )
    h = unitary @ signature @ unitary.conj().T
    return h.real if field == "real" else h


class GroupRelativeProblem:
    def __init__(
        self,
        table: np.ndarray,
        field: str,
        partial_trace_penalty: float,
    ):
        self.table = table
        self.d = table.shape[0]
        self.n = self.d * self.d
        self.eye_d = np.eye(self.d)
        self.permutation = relative_permutation(table)
        self.field = field
        self.partial_trace_penalty = partial_trace_penalty

    def lift(self, small_h: np.ndarray) -> np.ndarray:
        transformed = np.kron(self.eye_d, small_h)
        full_h = np.empty_like(transformed)
        full_h[np.ix_(self.permutation, self.permutation)] = transformed
        return full_h

    def pullback(self, full_gradient: np.ndarray) -> np.ndarray:
        transformed = full_gradient[
            np.ix_(self.permutation, self.permutation)
        ].reshape(self.d, self.d, self.d, self.d)
        # Sum diagonal blocks in the untouched first factor.
        return np.einsum("xaxb->ab", transformed)

    def partial_trace_first(self, matrix: np.ndarray) -> np.ndarray:
        d = self.d
        return np.einsum("ijil->jl", matrix.reshape(d, d, d, d))

    def partial_trace_second(self, matrix: np.ndarray) -> np.ndarray:
        d = self.d
        return np.einsum("ijkj->ik", matrix.reshape(d, d, d, d))

    def partial_trace_third_site(self, matrix: np.ndarray) -> np.ndarray:
        d = self.d
        return np.einsum(
            "abcABc->abAB", matrix.reshape(d, d, d, d, d, d)
        ).reshape(self.n, self.n)

    def partial_trace_first_site(self, matrix: np.ndarray) -> np.ndarray:
        d = self.d
        return np.einsum(
            "abcaBC->bcBC", matrix.reshape(d, d, d, d, d, d)
        ).reshape(self.n, self.n)

    def tangent_projection(
        self, matrix: np.ndarray, small_h: np.ndarray
    ) -> np.ndarray:
        matrix = (matrix + matrix.conj().T) / 2.0
        if self.field == "real":
            matrix = matrix.real
        tangent = (matrix - small_h @ matrix @ small_h) / 2.0
        tangent = (tangent + tangent.conj().T) / 2.0
        return tangent.real if self.field == "real" else tangent

    def value_gradient(
        self, small_h: np.ndarray, need_gradient: bool = True
    ):
        d = self.d
        full_h = self.lift(small_h)
        h1 = np.kron(full_h, self.eye_d)
        h2 = np.kron(self.eye_d, full_h)
        residual = (
            h1 @ h2 @ h1
            - h2 @ h1 @ h2
            - LAMBDA * (h1 - h2)
        )
        value = float(np.vdot(residual, residual).real)
        partial_first = self.partial_trace_first(full_h)
        partial_second = self.partial_trace_second(full_h)
        if self.partial_trace_penalty:
            value += self.partial_trace_penalty * float(
                np.vdot(partial_first, partial_first).real
                + np.vdot(partial_second, partial_second).real
            )
        if not need_gradient:
            return value

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
        full_gradient = self.partial_trace_third_site(
            g1
        ) + self.partial_trace_first_site(g2)
        if self.partial_trace_penalty:
            full_gradient += 2.0 * self.partial_trace_penalty * (
                np.kron(partial_second, self.eye_d)
                + np.kron(self.eye_d, partial_first)
            )
        gradient = self.tangent_projection(
            self.pullback(full_gradient), small_h
        )
        return (
            value,
            gradient,
            float(np.linalg.norm(residual)),
            full_h,
            partial_first,
            partial_second,
        )


def emit(item: dict, output: Path | None) -> None:
    rendered = json.dumps(item, sort_keys=True)
    print(rendered, flush=True)
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("a", encoding="utf-8") as handle:
            handle.write(rendered + "\n")


def diagnostics(
    problem: GroupRelativeProblem, small_h: np.ndarray
) -> dict[str, float]:
    (
        value,
        gradient,
        residual_norm,
        full_h,
        partial_first,
        partial_second,
    ) = problem.value_gradient(small_h)
    d = problem.d
    return {
        "objective": value,
        "residual_frobenius": residual_norm,
        "gradient_frobenius": float(np.linalg.norm(gradient)),
        "small_hermiticity_error": float(
            np.linalg.norm(small_h - small_h.conj().T)
        ),
        "small_involution_error": float(
            np.linalg.norm(small_h @ small_h - np.eye(d))
        ),
        "full_involution_error": float(
            np.linalg.norm(full_h @ full_h - np.eye(d * d))
        ),
        "trace_abs": float(abs(np.trace(full_h))),
        "partial_trace_first_norm": float(np.linalg.norm(partial_first)),
        "partial_trace_second_norm": float(np.linalg.norm(partial_second)),
    }


def run(args: argparse.Namespace) -> int:
    table = multiplication_table(args.group, args.order)
    inverse_table(table)
    rng = np.random.default_rng(args.seed)
    small_h = random_involution(args.order, rng, args.field)
    problem = GroupRelativeProblem(
        table, args.field, args.partial_trace_penalty
    )
    output = Path(args.output).resolve() if args.output else None
    run_id = (
        f"d{args.order}_{args.group}_relative_{args.field}"
        f"_seed{args.seed}"
    )
    metadata = {
        "event": "start",
        "run_id": run_id,
        "unix_time": time.time(),
        "order": args.order,
        "group": args.group,
        "field": args.field,
        "seed": args.seed,
        "max_iterations": args.max_iterations,
        "partial_trace_penalty": args.partial_trace_penalty,
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
    }
    emit(metadata, output)

    step = args.initial_step
    status = "max_iterations"
    start = time.monotonic()
    for iteration in range(args.max_iterations + 1):
        (
            value,
            gradient,
            residual_norm,
            _,
            _,
            _,
        ) = problem.value_gradient(small_h)
        gradient_norm = float(np.linalg.norm(gradient))
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

        direction = -gradient
        directional_derivative = -gradient_norm * gradient_norm
        generator = (direction @ small_h - small_h @ direction) / 4.0
        trial_step = min(step, args.maximum_step)
        accepted = False
        for line_search_iteration in range(args.max_line_search):
            unitary = expm(trial_step * generator)
            trial_h = unitary @ small_h @ unitary.conj().T
            trial_value = problem.value_gradient(
                trial_h, need_gradient=False
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
        small_h = trial_h
        step = (
            min(args.step_growth * trial_step, args.maximum_step)
            if line_search_iteration == 0
            else trial_step
        )

    final = {
        "event": "final",
        "run_id": run_id,
        "iteration": iteration,
        "elapsed_seconds": time.monotonic() - start,
        "status": status,
        **diagnostics(problem, small_h),
    }
    emit(final, output)
    if final["residual_frobenius"] <= args.save_threshold:
        candidate_directory = Path(args.candidate_directory).resolve()
        candidate_directory.mkdir(parents=True, exist_ok=True)
        candidate = candidate_directory / f"{run_id}.npz"
        if candidate.exists() and not args.overwrite_candidate:
            raise FileExistsError(
                f"candidate already exists: {candidate}; "
                "pass --overwrite-candidate to replace it"
            )
        np.savez_compressed(
            candidate,
            small_h=small_h,
            full_h=problem.lift(small_h),
            multiplication_table=table,
            metadata=json.dumps({**metadata, **final}, sort_keys=True),
        )
        emit(
            {
                "event": "candidate_saved",
                "run_id": run_id,
                "path": str(candidate),
            },
            output,
        )
    return 0


def gradient_check(args: argparse.Namespace) -> int:
    table = multiplication_table(args.group, args.order)
    rng = np.random.default_rng(args.seed)
    small_h = random_involution(args.order, rng, args.field)
    problem = GroupRelativeProblem(
        table, args.field, args.partial_trace_penalty
    )
    value, gradient, _, _, _, _ = problem.value_gradient(small_h)
    test = rng.normal(size=small_h.shape)
    if args.field == "complex":
        test = test + 1j * rng.normal(size=small_h.shape)
    test = problem.tangent_projection(test, small_h)
    test /= np.linalg.norm(test)
    generator = (test @ small_h - small_h @ test) / 4.0
    predicted = float(np.vdot(gradient, test).real)
    checks = []
    for epsilon in (1e-4, 1e-5, 1e-6):
        unitary = expm(epsilon * generator)
        trial_h = unitary @ small_h @ unitary.conj().T
        measured = (
            problem.value_gradient(trial_h, need_gradient=False) - value
        ) / epsilon
        checks.append(
            {
                "epsilon": epsilon,
                "analytic_derivative": predicted,
                "difference_quotient": measured,
                "absolute_error": abs(predicted - measured),
            }
        )
    print(json.dumps({"gradient_check": checks}, indent=2, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--order", type=int, default=6)
    result.add_argument(
        "--group", choices=("cyclic", "klein", "s3"), default="cyclic"
    )
    result.add_argument(
        "--field", choices=("real", "complex"), default="complex"
    )
    result.add_argument("--seed", type=int, required=True)
    result.add_argument("--max-iterations", type=int, default=1000)
    result.add_argument("--progress-every", type=int, default=100)
    result.add_argument("--initial-step", type=float, default=0.02)
    result.add_argument("--maximum-step", type=float, default=0.5)
    result.add_argument("--step-growth", type=float, default=1.8)
    result.add_argument("--armijo-constant", type=float, default=1e-4)
    result.add_argument("--max-line-search", type=int, default=40)
    result.add_argument("--partial-trace-penalty", type=float, default=1.0)
    result.add_argument("--residual-tolerance", type=float, default=1e-10)
    result.add_argument("--gradient-tolerance", type=float, default=1e-9)
    result.add_argument("--save-threshold", type=float, default=1e-5)
    result.add_argument(
        "--candidate-directory",
        default=str(PROJECT_ROOT / "results" / "d6_group_relative_candidates"),
    )
    result.add_argument("--output")
    result.add_argument("--gradient-check", action="store_true")
    result.add_argument("--overwrite-candidate", action="store_true")
    return result


if __name__ == "__main__":
    arguments = parser().parse_args()
    if arguments.order % 2:
        raise SystemExit("the reduced involution requires even group order")
    if arguments.gradient_check:
        raise SystemExit(gradient_check(arguments))
    raise SystemExit(run(arguments))
