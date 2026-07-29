#!/usr/bin/env python3
"""Reproducible searches in two operator-valued color/face ansatz families.

The two models are:

``mixed``
    V = C^c tensor C^r.  The first leg has c color sectors of dimension r.
    The second-leg color sectors are obtained from them by U tensor I_r,
    where U is a c-by-c unitary.  In the corresponding mixed pair basis, H
    has c^2 trace-zero involution blocks of size r^2.

``crossed``
    V = C^a tensor C^b.  H commutes with the first site's A color and the
    second site's B color.  For each of the a*b outer colors it has a
    trace-zero involution block on B(first) tensor A(second), of size ab=d.
    This is the exact block pattern numerically extracted from the independent
    d=4 solution, where a=b=2.

Every iterate is exactly (up to roundoff) a Hermitian trace-zero involution.
The objective is the exceptional cubic residual.  A small residual remains
numerical evidence only.
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


def random_reflection(
    size: int, rng: np.random.Generator, field: str
) -> np.ndarray:
    if size % 2:
        raise ValueError("trace-zero reflection blocks must have even size")
    z = rng.normal(size=(size, size))
    if field == "complex":
        z = z + 1j * rng.normal(size=(size, size))
    unitary, _ = np.linalg.qr(z)
    signature = np.diag(np.r_[np.ones(size // 2), -np.ones(size // 2)])
    reflection = unitary @ signature @ unitary.conj().T
    return reflection.real if field == "real" else reflection


def fourier(size: int) -> np.ndarray:
    row = np.arange(size)[:, None]
    column = np.arange(size)[None, :]
    return np.exp(2j * np.pi * row * column / size) / np.sqrt(size)


def random_unitary(
    size: int, rng: np.random.Generator, field: str
) -> np.ndarray:
    z = rng.normal(size=(size, size))
    if field == "complex":
        z = z + 1j * rng.normal(size=(size, size))
    unitary, _ = np.linalg.qr(z)
    return unitary.real if field == "real" else unitary


def partial_trace_3(a: np.ndarray, d: int) -> np.ndarray:
    return np.einsum(
        "abcABc->abAB", a.reshape(d, d, d, d, d, d)
    ).reshape(d * d, d * d)


def partial_trace_1(a: np.ndarray, d: int) -> np.ndarray:
    return np.einsum(
        "abcaBC->bcBC", a.reshape(d, d, d, d, d, d)
    ).reshape(d * d, d * d)


def partial_trace_first_local(a: np.ndarray, d: int) -> np.ndarray:
    return np.einsum("ijil->jl", a.reshape(d, d, d, d))


def partial_trace_internal(a: np.ndarray, colors: int, internal: int) -> np.ndarray:
    return np.einsum(
        "arbr->ab", a.reshape(colors, internal, colors, internal)
    )


def objective_gradient(h: np.ndarray, d: int) -> tuple[float, np.ndarray, float]:
    identity = np.eye(d, dtype=np.complex128)
    h1 = np.kron(h, identity)
    h2 = np.kron(identity, h)
    residual = h1 @ h2 @ h1 - h2 @ h1 @ h2 - (h1 - h2) / 3
    value = float(np.vdot(residual, residual).real)
    g1 = 2 * (
        h2 @ h1 @ residual
        + residual @ h1 @ h2
        - h2 @ residual @ h2
        - residual / 3
    )
    g2 = 2 * (
        h1 @ residual @ h1
        - h1 @ h2 @ residual
        - residual @ h2 @ h1
        + residual / 3
    )
    gradient = partial_trace_3(g1, d) + partial_trace_1(g2, d)
    gradient = (gradient + gradient.conj().T) / 2
    return value, gradient, float(np.linalg.norm(residual))


class FaceModel:
    def __init__(
        self,
        model: str,
        first_factor: int,
        second_factor: int,
        mixing: np.ndarray | None,
    ):
        self.model = model
        self.x = first_factor
        self.y = second_factor
        self.d = self.x * self.y
        self.mixing = mixing
        if model == "mixed":
            self.colors = self.x
            self.internal = self.y
            self.block_size = self.internal * self.internal
            self.block_labels = [
                (a, b) for a in range(self.colors) for b in range(self.colors)
            ]
        elif model == "crossed":
            self.block_size = self.d
            self.block_labels = [
                (a, b) for a in range(self.x) for b in range(self.y)
            ]
        else:
            raise ValueError(model)

    def block_indices(self, label: tuple[int, int]) -> np.ndarray:
        if self.model == "mixed":
            a, b = label
            return np.asarray(
                [
                    (a * self.internal + r) * self.d
                    + (b * self.internal + s)
                    for r in range(self.internal)
                    for s in range(self.internal)
                ],
                dtype=np.int64,
            )
        a, b = label
        return np.asarray(
            [
                (a * self.y + beta) * self.d + (alpha * self.y + b)
                for beta in range(self.y)
                for alpha in range(self.x)
            ],
            dtype=np.int64,
        )

    def pair_unitary(self) -> np.ndarray:
        if self.model == "crossed":
            return np.eye(self.d * self.d, dtype=np.complex128)
        assert self.mixing is not None
        right = np.kron(self.mixing, np.eye(self.internal))
        return np.kron(np.eye(self.d), right)

    def assemble_reference(self, blocks: list[np.ndarray]) -> np.ndarray:
        h0 = np.zeros((self.d * self.d, self.d * self.d), dtype=np.complex128)
        for label, block in zip(self.block_labels, blocks):
            indices = self.block_indices(label)
            h0[np.ix_(indices, indices)] = block
        return h0

    def assemble(self, blocks: list[np.ndarray]) -> np.ndarray:
        h0 = self.assemble_reference(blocks)
        pair_unitary = self.pair_unitary()
        return pair_unitary @ h0 @ pair_unitary.conj().T

    def block_gradients(
        self, gradient: np.ndarray, blocks: list[np.ndarray]
    ) -> tuple[list[np.ndarray], np.ndarray | None]:
        pair_unitary = self.pair_unitary()
        reference_gradient = pair_unitary.conj().T @ gradient @ pair_unitary
        directions = []
        for label, block in zip(self.block_labels, blocks):
            indices = self.block_indices(label)
            local = reference_gradient[np.ix_(indices, indices)]
            local = (local + local.conj().T) / 2
            tangent = (local - block @ local @ block) / 2
            directions.append(-tangent)

        mixing_generator = None
        if self.model == "mixed":
            h = pair_unitary @ self.assemble_reference(blocks) @ pair_unitary.conj().T
            commutator = h @ gradient - gradient @ h
            second_site = partial_trace_first_local(commutator, self.d)
            color_generator = partial_trace_internal(
                second_site, self.colors, self.internal
            )
            color_generator = (color_generator - color_generator.conj().T) / 2
            mixing_generator = color_generator
        return directions, mixing_generator

    def trial(
        self,
        blocks: list[np.ndarray],
        directions: list[np.ndarray],
        mixing_generator: np.ndarray | None,
        step: float,
        optimize_mixing: bool,
        field: str,
    ) -> tuple[list[np.ndarray], np.ndarray | None]:
        trial_blocks = []
        for block, direction in zip(blocks, directions):
            generator = (direction @ block - block @ direction) / 4
            unitary = expm(step * generator)
            trial = unitary @ block @ unitary.conj().T
            trial_blocks.append(trial.real if field == "real" else trial)
        trial_mixing = self.mixing
        if (
            optimize_mixing
            and self.model == "mixed"
            and mixing_generator is not None
        ):
            assert self.mixing is not None
            trial_mixing = expm(step * mixing_generator) @ self.mixing
        return trial_blocks, trial_mixing


def diagnostics(model: FaceModel, blocks: list[np.ndarray]) -> dict[str, float]:
    h = model.assemble(blocks)
    value, _, residual = objective_gradient(h, model.d)
    return {
        "objective": value,
        "residual_frobenius": residual,
        "hermiticity_error": float(np.linalg.norm(h - h.conj().T)),
        "involution_error": float(
            np.linalg.norm(h @ h - np.eye(model.d * model.d))
        ),
        "trace_abs": float(abs(np.trace(h))),
    }


def emit(event: dict, output: Path | None) -> None:
    rendered = json.dumps(event, sort_keys=True)
    print(rendered, flush=True)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("a", encoding="utf-8") as handle:
            handle.write(rendered + "\n")


def main(args: argparse.Namespace) -> int:
    rng = np.random.default_rng(args.seed)
    if args.model == "mixed":
        if args.mixing == "identity":
            mixing = np.eye(args.first_factor, dtype=np.complex128)
        elif args.mixing == "fourier":
            mixing = fourier(args.first_factor)
        else:
            mixing = random_unitary(args.first_factor, rng, args.field)
    else:
        mixing = None

    model = FaceModel(
        args.model, args.first_factor, args.second_factor, mixing
    )
    if model.d != args.dimension:
        raise ValueError(
            f"factor product {model.d} does not equal dimension {args.dimension}"
        )
    blocks = [
        random_reflection(model.block_size, rng, args.field)
        for _ in model.block_labels
    ]
    if args.embed_d4:
        if (
            args.model != "mixed"
            or args.first_factor != 3
            or args.second_factor != 2
        ):
            raise ValueError("--embed-d4 requires the mixed 3x2 model")
        source = np.load(args.embed_d4)
        source_blocks = source["blocks"]
        source_mixing = source["mixing"]
        if source_blocks.shape != (4, 4, 4) or source_mixing.shape != (2, 2):
            raise ValueError("the embedded candidate is not a mixed 2x2 point")
        source_by_label = {
            (a, b): source_blocks[2 * a + b]
            for a in range(2)
            for b in range(2)
        }
        for index, label in enumerate(model.block_labels):
            if label in source_by_label:
                blocks[index] = source_by_label[label]
        mixing = np.zeros((3, 3), dtype=np.complex128)
        mixing[:2, :2] = source_mixing
        mixing[2, 2] = 1
        model.mixing = mixing
    output = Path(args.output) if args.output else None
    run_id = (
        f"color_face_{args.model}_d{model.d}_{args.first_factor}x"
        f"{args.second_factor}_{args.field}_{args.mixing}"
        f"_mixopt{int(args.optimize_mixing)}_seed{args.seed}"
    )
    emit(
        {
            "event": "start",
            "run_id": run_id,
            "seed": args.seed,
            "model": args.model,
            "dimension": model.d,
            "first_factor": args.first_factor,
            "second_factor": args.second_factor,
            "block_size": model.block_size,
            "block_count": len(model.block_labels),
            "field": args.field,
            "mixing": args.mixing,
            "optimize_mixing": args.optimize_mixing,
            "embed_d4": str(args.embed_d4) if args.embed_d4 else None,
            "python": sys.version.replace("\n", " "),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
            "unix_time": time.time(),
        },
        output,
    )

    step = args.initial_step
    start = time.monotonic()
    status = "max_iterations"
    for iteration in range(args.max_iterations + 1):
        h = model.assemble(blocks)
        value, gradient, residual = objective_gradient(h, model.d)
        directions, mixing_generator = model.block_gradients(gradient, blocks)
        gradient_norm = float(
            np.sqrt(sum(np.linalg.norm(x) ** 2 for x in directions))
        )
        if args.optimize_mixing and mixing_generator is not None:
            gradient_norm = float(
                np.sqrt(gradient_norm**2 + np.linalg.norm(mixing_generator) ** 2)
            )
        if iteration % args.progress_every == 0:
            emit(
                {
                    "event": "progress",
                    "run_id": run_id,
                    "iteration": iteration,
                    "elapsed_seconds": time.monotonic() - start,
                    "objective": value,
                    "residual_frobenius": residual,
                    "gradient_frobenius": gradient_norm,
                    "step": step,
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

        accepted = False
        trial_step = min(step, args.maximum_step)
        old_mixing = model.mixing
        for line_iteration in range(args.max_line_search):
            trial_blocks, trial_mixing = model.trial(
                blocks,
                directions,
                mixing_generator,
                trial_step,
                args.optimize_mixing,
                args.field,
            )
            model.mixing = trial_mixing
            trial_h = model.assemble(trial_blocks)
            trial_value, _, _ = objective_gradient(trial_h, model.d)
            if trial_value < value:
                accepted = True
                break
            model.mixing = old_mixing
            trial_step *= 0.5
        if not accepted:
            status = "line_search_failed"
            break
        blocks = trial_blocks
        if line_iteration == 0:
            step = min(args.step_growth * trial_step, args.maximum_step)
        else:
            step = trial_step

    final = {
        "event": "final",
        "run_id": run_id,
        "iteration": iteration,
        "elapsed_seconds": time.monotonic() - start,
        "status": status,
        **diagnostics(model, blocks),
    }
    emit(final, output)
    if args.save_threshold is not None and (
        final["residual_frobenius"] <= args.save_threshold
    ):
        candidate_directory = Path(args.candidate_directory)
        candidate_directory.mkdir(parents=True, exist_ok=True)
        path = candidate_directory / f"{run_id}.npz"
        if path.exists():
            emit(
                {
                    "event": "candidate_not_saved_existing",
                    "run_id": run_id,
                    "path": str(path.resolve()),
                },
                output,
            )
            return 0
        np.savez_compressed(
            path,
            blocks=np.asarray(blocks),
            mixing=model.mixing,
            h=model.assemble(blocks),
            metadata=json.dumps(final, sort_keys=True),
        )
        emit(
            {
                "event": "candidate_saved",
                "run_id": run_id,
                "path": str(path.resolve()),
            },
            output,
        )
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--model", choices=("mixed", "crossed"), required=True)
    result.add_argument("--dimension", type=int, default=6)
    result.add_argument("--first-factor", type=int, required=True)
    result.add_argument("--second-factor", type=int, required=True)
    result.add_argument("--seed", type=int, required=True)
    result.add_argument("--field", choices=("real", "complex"), default="complex")
    result.add_argument(
        "--mixing", choices=("identity", "fourier", "random"), default="fourier"
    )
    result.add_argument("--optimize-mixing", action="store_true")
    result.add_argument("--embed-d4", type=Path)
    result.add_argument("--max-iterations", type=int, default=1000)
    result.add_argument("--progress-every", type=int, default=100)
    result.add_argument("--initial-step", type=float, default=0.02)
    result.add_argument("--maximum-step", type=float, default=0.5)
    result.add_argument("--step-growth", type=float, default=1.5)
    result.add_argument("--max-line-search", type=int, default=30)
    result.add_argument("--residual-tolerance", type=float, default=1e-10)
    result.add_argument("--gradient-tolerance", type=float, default=1e-9)
    result.add_argument("--output")
    result.add_argument(
        "--candidate-directory", default="results/color_face_candidates"
    )
    result.add_argument("--save-threshold", type=float, default=1e-6)
    return result


if __name__ == "__main__":
    raise SystemExit(main(parser().parse_args()))
