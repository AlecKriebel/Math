#!/usr/bin/env python3
"""Search the rank-two three-color branch with an arbitrary U(6) position.

This strictly broadens the earlier ``mixed 3x2`` search:

* the nine 4x4 blocks are still signature-(2,2) reflections;
* the relative position of the two rank-two color decompositions is now an
  arbitrary unitary in U(6), rather than U(3) tensor I_2.

The output is discovery evidence only.  A small residual would still need
exact reconstruction and an independent verifier.
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

import color_face_d6_search as base


class FullRelativeModel(base.FaceModel):
    def __init__(self, colors: int, internal: int, mixing: np.ndarray):
        super().__init__("mixed", colors, internal, mixing)
        if mixing.shape != (self.d, self.d):
            raise ValueError("full relative unitary has the wrong shape")

    def pair_unitary(self) -> np.ndarray:
        assert self.mixing is not None
        return np.kron(np.eye(self.d), self.mixing)

    def block_gradients(
        self, gradient: np.ndarray, blocks: list[np.ndarray]
    ) -> tuple[list[np.ndarray], np.ndarray]:
        pair_unitary = self.pair_unitary()
        reference_gradient = pair_unitary.conj().T @ gradient @ pair_unitary
        directions = []
        for label, block in zip(self.block_labels, blocks):
            indices = self.block_indices(label)
            local = reference_gradient[np.ix_(indices, indices)]
            local = (local + local.conj().T) / 2
            tangent = (local - block @ local @ block) / 2
            directions.append(-tangent)

        h = pair_unitary @ self.assemble_reference(blocks) @ pair_unitary.conj().T
        commutator = h @ gradient - gradient @ h
        generator = base.partial_trace_first_local(commutator, self.d)
        generator = (generator - generator.conj().T) / 2
        return directions, generator

    def trial_full(
        self,
        blocks: list[np.ndarray],
        directions: list[np.ndarray],
        mixing_generator: np.ndarray,
        step: float,
    ) -> tuple[list[np.ndarray], np.ndarray]:
        trial_blocks = []
        for block, direction in zip(blocks, directions):
            generator = (direction @ block - block @ direction) / 4
            unitary = expm(step * generator)
            trial_blocks.append(unitary @ block @ unitary.conj().T)
        assert self.mixing is not None
        trial_mixing = expm(step * mixing_generator) @ self.mixing
        return trial_blocks, trial_mixing


def emit(event: dict, output: Path) -> None:
    line = json.dumps(event, sort_keys=True)
    print(line, flush=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def main(args: argparse.Namespace) -> int:
    rng = np.random.default_rng(args.seed)
    d = args.colors * args.internal
    if d != 6:
        raise ValueError("this falsifier is configured for d=6")

    if args.mixing == "lifted_fourier":
        mixing = np.kron(
            base.fourier(args.colors), np.eye(args.internal)
        )
    else:
        mixing = base.random_unitary(d, rng, "complex")
    model = FullRelativeModel(args.colors, args.internal, mixing)
    blocks = [
        base.random_reflection(model.block_size, rng, "complex")
        for _ in model.block_labels
    ]

    output = Path(args.output)
    run_id = (
        f"d6_threecolor_fullU6_{args.mixing}_seed{args.seed}"
    )
    emit(
        {
            "event": "start",
            "run_id": run_id,
            "seed": args.seed,
            "dimension": d,
            "colors": args.colors,
            "internal": args.internal,
            "block_count": len(blocks),
            "block_signature": [2, 2],
            "relative_unitary": "U(6)",
            "initial_mixing": args.mixing,
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
        value, gradient, residual = base.objective_gradient(h, d)
        directions, mixing_generator = model.block_gradients(gradient, blocks)
        gradient_norm = float(
            np.sqrt(
                sum(np.linalg.norm(x) ** 2 for x in directions)
                + np.linalg.norm(mixing_generator) ** 2
            )
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

        old_mixing = model.mixing
        accepted = False
        trial_step = min(step, args.maximum_step)
        for line_iteration in range(args.max_line_search):
            trial_blocks, trial_mixing = model.trial_full(
                blocks, directions, mixing_generator, trial_step
            )
            model.mixing = trial_mixing
            trial_h = model.assemble(trial_blocks)
            trial_value, _, _ = base.objective_gradient(trial_h, d)
            if trial_value < value:
                accepted = True
                break
            model.mixing = old_mixing
            trial_step *= 0.5
        if not accepted:
            status = "line_search_failed"
            break
        blocks = trial_blocks
        step = (
            min(args.step_growth * trial_step, args.maximum_step)
            if line_iteration == 0
            else trial_step
        )

    h = model.assemble(blocks)
    value, _, residual = base.objective_gradient(h, d)
    partial_left = np.linalg.norm(
        np.einsum("iaja->ij", h.reshape(d, d, d, d))
    )
    partial_right = np.linalg.norm(
        np.einsum("iaib->ab", h.reshape(d, d, d, d))
    )
    final = {
        "event": "final",
        "run_id": run_id,
        "iteration": iteration,
        "elapsed_seconds": time.monotonic() - start,
        "status": status,
        "objective": value,
        "residual_frobenius": residual,
        "gradient_frobenius": gradient_norm,
        "partial_trace_left_frobenius": float(partial_left),
        "partial_trace_right_frobenius": float(partial_right),
        "unitarity_of_relative_position": float(
            np.linalg.norm(model.mixing.conj().T @ model.mixing - np.eye(d))
        ),
    }
    emit(final, output)

    if residual <= args.save_threshold:
        candidate = Path(args.candidate_directory) / f"{run_id}.npz"
        candidate.parent.mkdir(parents=True, exist_ok=True)
        if candidate.exists():
            raise FileExistsError(candidate)
        np.savez_compressed(
            candidate,
            h=h,
            blocks=np.asarray(blocks),
            mixing=model.mixing,
            metadata=json.dumps(final, sort_keys=True),
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
    result.add_argument(
        "--mixing", choices=("random", "lifted_fourier"), required=True
    )
    result.add_argument("--colors", type=int, default=3)
    result.add_argument("--internal", type=int, default=2)
    result.add_argument("--max-iterations", type=int, default=1000)
    result.add_argument("--progress-every", type=int, default=100)
    result.add_argument("--initial-step", type=float, default=0.02)
    result.add_argument("--maximum-step", type=float, default=0.5)
    result.add_argument("--step-growth", type=float, default=1.5)
    result.add_argument("--max-line-search", type=int, default=30)
    result.add_argument("--residual-tolerance", type=float, default=1e-10)
    result.add_argument("--gradient-tolerance", type=float, default=1e-9)
    result.add_argument("--save-threshold", type=float, default=1e-6)
    result.add_argument(
        "--candidate-directory",
        default="exceptional_ybe_spectrum/results/"
        "d6_threecolor_full_relative_candidates",
    )
    result.add_argument("--output", required=True)
    return result


if __name__ == "__main__":
    raise SystemExit(main(parser().parse_args()))
