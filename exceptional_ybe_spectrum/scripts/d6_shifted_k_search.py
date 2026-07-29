#!/usr/bin/env python3
"""Search the reduced heterogeneous (3,2) ansatz for a d=6 solution.

Let A=C^2 and B=C^3.  A trace-zero Hermitian involution K on A tensor B
tensor A has size 12.  On

    A_1 tensor B_2 tensor A_2 tensor B_3 tensor A_3

define K_1=K tensor I_6 and K_2=I_6 tensor K.  A solution of

    K_1 K_2 K_1 - K_2 K_1 K_2 = (K_1-K_2)/3

blocks to an ordinary d=6 solution after adding the spectator B_1 and
regrouping B_i tensor A_i into local sites.

This program performs reproducible Grassmann-manifold searches on K.  It is a
candidate generator, not a proof of nonexistence.
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


def labels_for(symmetry: str) -> np.ndarray:
    labels = []
    for a in range(2):
        for r in range(3):
            for b in range(2):
                if symmetry == "none":
                    label = 0
                elif symmetry == "qutrit_charge":
                    label = r
                elif symmetry == "outer_parity":
                    label = (a + b) % 2
                elif symmetry == "charge_parity":
                    label = 2 * r + ((a + b) % 2)
                elif symmetry == "middle_2plus1":
                    label = int(r == 2)
                else:
                    raise ValueError(symmetry)
                labels.append(label)
    return np.asarray(labels, dtype=np.int64)


def random_involution(
    labels: np.ndarray, rng: np.random.Generator, field: str
) -> np.ndarray:
    k = np.zeros((12, 12), dtype=np.complex128)
    for label in np.unique(labels):
        indices = np.flatnonzero(labels == label)
        size = len(indices)
        if size % 2:
            raise ValueError(f"odd block size {size}")
        z = rng.normal(size=(size, size))
        if field == "complex":
            z = z + 1j * rng.normal(size=(size, size))
        q, _ = np.linalg.qr(z)
        signature = np.diag(
            np.r_[np.ones(size // 2), -np.ones(size // 2)]
        )
        k[np.ix_(indices, indices)] = q @ signature @ q.conj().T
    return k.real if field == "real" else k


def known_d4_k() -> np.ndarray:
    i = np.eye(2)
    x = np.array([[0.0, 1.0], [1.0, 0.0]])
    z = np.array([[1.0, 0.0], [0.0, -1.0]])
    j = np.array([[0.0, -1.0], [1.0, 0.0]])
    return (
        -np.kron(np.kron(z, z), z) / np.sqrt(6.0)
        - np.kron(np.kron(z, j), j) / np.sqrt(6.0)
        - np.kron(np.kron(j, j), z) / np.sqrt(6.0)
        + np.kron(np.kron(j, z), j) / np.sqrt(6.0)
        - np.kron(np.kron(x, x), x) / np.sqrt(3.0)
    )


class Problem:
    def __init__(
        self,
        operator_dimension: int,
        shift_dimension: int,
        labels: np.ndarray,
        field: str,
        overlap_trace_penalty: float,
    ):
        self.n = operator_dimension
        self.s = shift_dimension
        self.eye = np.eye(shift_dimension)
        self.mask = labels[:, None] == labels[None, :]
        self.field = field
        self.overlap_trace_penalty = overlap_trace_penalty

    def project(self, x: np.ndarray, k: np.ndarray) -> np.ndarray:
        x = np.where(self.mask, x, 0.0)
        x = (x + x.conj().T) / 2.0
        if self.field == "real":
            x = x.real
        x = (x - k @ x @ k) / 2.0
        x = np.where(self.mask, x, 0.0)
        x = (x + x.conj().T) / 2.0
        return x.real if self.field == "real" else x

    def pullback_1(self, x: np.ndarray) -> np.ndarray:
        return np.einsum(
            "isjs->ij", x.reshape(self.n, self.s, self.n, self.s)
        )

    def pullback_2(self, x: np.ndarray) -> np.ndarray:
        return np.einsum(
            "aiaj->ij", x.reshape(self.s, self.n, self.s, self.n)
        )

    def evaluate(
        self, k: np.ndarray, gradient: bool = True
    ) -> float | tuple[float, np.ndarray, float, float]:
        k1 = np.kron(k, self.eye)
        k2 = np.kron(self.eye, k)
        f = k1 @ k2 @ k1 - k2 @ k1 @ k2 - (k1 - k2) / 3.0
        value = float(np.vdot(f, f).real)
        overlap_trace = float(np.trace(k1 @ k2).real)
        if self.overlap_trace_penalty:
            value += self.overlap_trace_penalty * overlap_trace**2
        if not gradient:
            return value
        g1 = 2.0 * (
            k2 @ k1 @ f + f @ k1 @ k2 - k2 @ f @ k2 - f / 3.0
        )
        g2 = 2.0 * (
            k1 @ f @ k1 - k1 @ k2 @ f - f @ k2 @ k1 + f / 3.0
        )
        g = self.project(self.pullback_1(g1) + self.pullback_2(g2), k)
        if self.overlap_trace_penalty:
            overlap_gradient = self.pullback_1(k2) + self.pullback_2(k1)
            g += self.project(
                2.0
                * self.overlap_trace_penalty
                * overlap_trace
                * overlap_gradient,
                k,
            )
        return value, g, float(np.linalg.norm(f)), float(np.linalg.norm(g))


def emit(event: dict, output: Path | None) -> None:
    rendered = json.dumps(event, sort_keys=True)
    print(rendered, flush=True)
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("a", encoding="utf-8") as handle:
            handle.write(rendered + "\n")


def main(args: argparse.Namespace) -> int:
    if args.calibration_d4:
        n, s = 8, 4
        labels = np.zeros(n, dtype=np.int64)
        if args.initial == "known":
            k = known_d4_k()
        else:
            rng = np.random.default_rng(args.seed)
            z = rng.normal(size=(n, n))
            if args.field == "complex":
                z = z + 1j * rng.normal(size=(n, n))
            q, _ = np.linalg.qr(z)
            k = q @ np.diag(np.r_[np.ones(4), -np.ones(4)]) @ q.conj().T
    else:
        n, s = 12, 6
        labels = labels_for(args.symmetry)
        rng = np.random.default_rng(args.seed)
        k = random_involution(labels, rng, args.field)
        if args.initial == "known_d4_block":
            if args.symmetry != "middle_2plus1":
                raise ValueError(
                    "known_d4_block requires symmetry=middle_2plus1"
                )
            active = np.asarray(
                [
                    a * 6 + r * 2 + b
                    for a in range(2)
                    for r in range(2)
                    for b in range(2)
                ],
                dtype=np.int64,
            )
            k[np.ix_(active, active)] = known_d4_k()

    problem = Problem(
        n, s, labels, args.field, args.overlap_trace_penalty
    )
    output = Path(args.output) if args.output else None
    run_id = (
        f"k{n}_shift{s}_{args.field}_{args.symmetry}_{args.initial}"
        f"_seed{args.seed}"
    )
    emit(
        {
            "event": "start",
            "run_id": run_id,
            "seed": args.seed,
            "operator_dimension": n,
            "shift_dimension": s,
            "field": args.field,
            "symmetry": args.symmetry,
            "initial": args.initial,
            "block_sizes": [
                int(np.count_nonzero(labels == label))
                for label in np.unique(labels)
            ],
            "max_iterations": args.max_iterations,
            "overlap_trace_penalty": args.overlap_trace_penalty,
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "python": sys.version.replace("\n", " "),
            "platform": platform.platform(),
            "unix_time": time.time(),
        },
        output,
    )

    previous_gradient = None
    previous_direction = None
    step = 0.02
    started = time.monotonic()
    status = "max_iterations"

    for iteration in range(args.max_iterations + 1):
        value, gradient, residual, gradient_norm = problem.evaluate(k)
        if iteration % args.progress_every == 0:
            emit(
                {
                    "event": "progress",
                    "run_id": run_id,
                    "iteration": iteration,
                    "objective": value,
                    "residual_frobenius": residual,
                    "gradient_frobenius": gradient_norm,
                    "step": step,
                    "elapsed_seconds": time.monotonic() - started,
                },
                output,
            )
        if residual <= args.residual_tolerance:
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
            old_g = problem.project(previous_gradient, k)
            old_d = problem.project(previous_direction, k)
            denominator = max(
                float(np.vdot(previous_gradient, previous_gradient).real),
                np.finfo(float).tiny,
            )
            beta = max(
                0.0,
                float(np.vdot(gradient, gradient - old_g).real) / denominator,
            )
            direction = -gradient + beta * old_d
            if float(np.vdot(gradient, direction).real) >= (
                -1e-6 * gradient_norm * float(np.linalg.norm(direction))
            ):
                direction = -gradient

        derivative = float(np.vdot(gradient, direction).real)
        generator = (direction @ k - k @ direction) / 4.0
        trial_step = min(step, 0.5)
        accepted = False
        for line_iteration in range(40):
            u = expm(trial_step * generator)
            trial_k = u @ k @ u.conj().T
            trial_value = problem.evaluate(trial_k, gradient=False)
            if trial_value <= value + 1e-4 * trial_step * derivative:
                accepted = True
                break
            trial_step *= 0.5
        if not accepted:
            status = "line_search_failed"
            break
        previous_gradient = gradient
        previous_direction = direction
        k = trial_k
        step = min(1.8 * trial_step, 0.5) if line_iteration == 0 else trial_step

    value, gradient, residual, gradient_norm = problem.evaluate(k)
    final = {
        "event": "final",
        "run_id": run_id,
        "status": status,
        "iteration": iteration,
        "objective": value,
        "residual_frobenius": residual,
        "gradient_frobenius": gradient_norm,
        "hermiticity_error": float(np.linalg.norm(k - k.conj().T)),
        "involution_error": float(np.linalg.norm(k @ k - np.eye(n))),
        "trace_abs": float(abs(np.trace(k))),
        "overlap_trace": float(
            np.trace(np.kron(k, np.eye(s)) @ np.kron(np.eye(s), k)).real
        ),
        "elapsed_seconds": time.monotonic() - started,
    }
    emit(final, output)
    if residual <= args.save_threshold:
        directory = Path(args.candidate_directory)
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{run_id}.npz"
        if path.exists() and not args.overwrite_candidate:
            emit(
                {
                    "event": "candidate_preserved",
                    "run_id": run_id,
                    "path": str(path.resolve()),
                    "reason": (
                        "existing archive not overwritten; pass "
                        "--overwrite-candidate to replace it"
                    ),
                },
                output,
            )
            return 0
        np.savez_compressed(path, k=k, metadata=json.dumps(final, sort_keys=True))
        emit(
            {"event": "candidate_saved", "run_id": run_id, "path": str(path)},
            output,
        )
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--field", choices=("real", "complex"), default="complex")
    p.add_argument(
        "--symmetry",
        choices=(
            "none",
            "qutrit_charge",
            "outer_parity",
            "charge_parity",
            "middle_2plus1",
        ),
        default="none",
    )
    p.add_argument(
        "--initial",
        choices=("random", "known", "known_d4_block"),
        default="random",
    )
    p.add_argument("--calibration-d4", action="store_true")
    p.add_argument("--max-iterations", type=int, default=3000)
    p.add_argument("--progress-every", type=int, default=500)
    p.add_argument("--residual-tolerance", type=float, default=1e-10)
    p.add_argument("--gradient-tolerance", type=float, default=1e-9)
    p.add_argument("--save-threshold", type=float, default=1e-6)
    p.add_argument("--overlap-trace-penalty", type=float, default=0.0)
    p.add_argument("--candidate-directory", default="results/d6_shifted_candidates")
    p.add_argument(
        "--overwrite-candidate",
        action="store_true",
        help="replace an existing candidate archive (disabled by default)",
    )
    p.add_argument("--output")
    return p


if __name__ == "__main__":
    raise SystemExit(main(parser().parse_args()))
