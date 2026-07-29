#!/usr/bin/env python3
"""Search all nine standardness-compatible three-color cell-rank orbits.

The left and right one-site color algebras each have three rank-two atoms.
Their relative position is an arbitrary unitary in U(6).  In the associated
mixed pair basis, the negative ranks of the nine four-dimensional cells form
a matrix in {0,...,4}^{3x3} with all row and column sums equal to six.

There are 217 labelled matrices and nine orbits under independent row and
column permutations, transpose, and complementation.  This script searches
one declared canonical representative at a time.  Its output is discovery
evidence only.
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
import d6_threecolor_full_relative_search as uniform


CELL_RANK_PATTERNS = (
    ((0, 2, 4), (2, 2, 2), (4, 2, 0)),
    ((0, 2, 4), (2, 3, 1), (4, 1, 1)),
    ((0, 2, 4), (2, 4, 0), (4, 0, 2)),
    ((0, 2, 4), (3, 2, 1), (3, 2, 1)),
    ((0, 3, 3), (3, 0, 3), (3, 3, 0)),
    ((0, 3, 3), (3, 1, 2), (3, 2, 1)),
    ((1, 2, 3), (2, 2, 2), (3, 2, 1)),
    ((1, 2, 3), (2, 3, 1), (3, 1, 2)),
    ((2, 2, 2), (2, 2, 2), (2, 2, 2)),
)


def random_reflection_with_negative_rank(
    size: int, negative_rank: int, rng: np.random.Generator
) -> np.ndarray:
    if not 0 <= negative_rank <= size:
        raise ValueError("negative rank outside the block")
    if negative_rank == 0:
        return np.eye(size, dtype=np.complex128)
    if negative_rank == size:
        return -np.eye(size, dtype=np.complex128)
    unitary = base.random_unitary(size, rng, "complex")
    signature = np.diag(
        np.r_[np.ones(size - negative_rank), -np.ones(negative_rank)]
    )
    return unitary @ signature @ unitary.conj().T


def main(args: argparse.Namespace) -> int:
    rng = np.random.default_rng(args.seed)
    d = 6
    mixing = base.random_unitary(d, rng, "complex")
    model = uniform.FullRelativeModel(3, 2, mixing)
    rank_pattern = CELL_RANK_PATTERNS[args.rank_pattern_index]
    blocks = [
        random_reflection_with_negative_rank(4, rank_pattern[a][b], rng)
        for a, b in model.block_labels
    ]

    output = Path(args.output)
    run_id = (
        f"d6_threecolor_rankpattern{args.rank_pattern_index}_"
        f"seed{args.seed}"
    )
    uniform.emit(
        {
            "event": "start",
            "run_id": run_id,
            "seed": args.seed,
            "dimension": d,
            "cell_negative_rank_pattern": rank_pattern,
            "rank_pattern_index": args.rank_pattern_index,
            "relative_unitary": "U(6)",
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
            uniform.emit(
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
    uniform.emit(final, output)

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
        uniform.emit(
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
        "--rank-pattern-index",
        type=int,
        choices=range(len(CELL_RANK_PATTERNS)),
        required=True,
    )
    result.add_argument("--max-iterations", type=int, default=800)
    result.add_argument("--progress-every", type=int, default=200)
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
        "d6_threecolor_rankpattern_candidates",
    )
    result.add_argument("--output", required=True)
    return result


if __name__ == "__main__":
    raise SystemExit(main(parser().parse_args()))
