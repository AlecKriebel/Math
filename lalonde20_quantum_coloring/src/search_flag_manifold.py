#!/usr/bin/env python3
"""Exploratory fixed-rank search on products of complex flag manifolds.

This script is deliberately *not* a verifier.  Every row is an exact projective
measurement to floating-point precision because it is represented as a unitary
conjugate of fixed coordinate blocks.  The optimized energy is

    sum_{(v,w) in E(H), c} Tr(P[v,c] P[w,c]),

which is nonnegative and vanishes exactly at the edge-orthogonality relations.
Near-zero output is only a reconstruction lead, never a mathematical result.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np
import scipy.linalg


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_data import ADJ20, E20, V20  # noqa: E402


def haar_unitary(d: int, rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    q, r = np.linalg.qr(z)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1.0)
    return q @ np.diag(np.conjugate(phases))


def blocks_from_unitary(unitary: np.ndarray, ranks: tuple[int, int, int, int]):
    cuts = np.cumsum((0,) + ranks)
    return np.stack(
        [
            unitary[:, cuts[c] : cuts[c + 1]]
            @ unitary[:, cuts[c] : cuts[c + 1]].conj().T
            for c in range(4)
        ]
    )


def all_projectors(unitaries: np.ndarray, ranks: np.ndarray) -> np.ndarray:
    return np.stack(
        [blocks_from_unitary(unitaries[v - 1], tuple(int(x) for x in ranks[v - 1]))
         for v in V20]
    )


def energy(projectors: np.ndarray) -> float:
    value = 0.0
    for v, w in E20:
        value += float(
            np.real(np.einsum("cij,cji->", projectors[v - 1], projectors[w - 1]))
        )
    return value


def local_energy(v: int, pv: np.ndarray, projectors: np.ndarray) -> float:
    value = 0.0
    for w in ADJ20[v]:
        value += float(
            np.real(np.einsum("cij,cji->", pv, projectors[w - 1]))
        )
    return value


def vertex_gradient(v: int, projectors: np.ndarray) -> np.ndarray:
    neighbour_sums = np.sum(
        [projectors[w - 1] for w in ADJ20[v]], axis=0
    )
    gradient = np.zeros_like(projectors[0, 0])
    for c in range(4):
        p = projectors[v - 1, c]
        s = neighbour_sums[c]
        gradient += p @ s - s @ p
    # Suppress accumulated roundoff in the anti-Hermitian tangent.
    return (gradient - gradient.conj().T) / 2


def optimize(
    d: int,
    ranks: np.ndarray,
    seed: int,
    sweeps: int,
    initial_step: float,
    tolerance: float,
):
    rng = np.random.default_rng(seed)
    unitaries = np.stack([haar_unitary(d, rng) for _ in V20])
    projectors = all_projectors(unitaries, ranks)
    step_scale = initial_step
    history = [energy(projectors)]

    for sweep in range(sweeps):
        moved = 0
        for index in rng.permutation(len(V20)):
            v = int(index + 1)
            gradient = vertex_gradient(v, projectors)
            norm = float(np.linalg.norm(gradient))
            if norm < 1e-14:
                continue
            old_local = local_energy(v, projectors[v - 1], projectors)
            step = step_scale / max(1.0, norm)
            accepted = False
            for _ in range(18):
                candidate_u = scipy.linalg.expm(step * gradient) @ unitaries[v - 1]
                candidate_p = blocks_from_unitary(
                    candidate_u, tuple(int(x) for x in ranks[v - 1])
                )
                candidate_local = local_energy(v, candidate_p, projectors)
                if candidate_local < old_local - 1e-13 * max(1.0, old_local):
                    unitaries[v - 1] = candidate_u
                    projectors[v - 1] = candidate_p
                    accepted = True
                    moved += 1
                    break
                step *= 0.5
            if not accepted:
                continue

        current = energy(projectors)
        history.append(current)
        if sweep % 25 == 0 or current < tolerance:
            print(
                f"seed={seed} d={d} sweep={sweep:5d} "
                f"energy={current:.16e} moved={moved} step={step_scale:.3g}",
                flush=True,
            )
        if current < tolerance:
            break
        if moved < len(V20) // 4:
            step_scale *= 0.8
        elif moved > 3 * len(V20) // 4:
            step_scale = min(initial_step, step_scale * 1.02)

    return unitaries, projectors, np.asarray(history)


def uniform_ranks(d: int) -> np.ndarray:
    if d % 4:
        raise ValueError("the uniform profile requires d divisible by four")
    return np.full((20, 4), d // 4, dtype=int)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimension", "-d", type=int, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--sweeps", type=int, default=1000)
    parser.add_argument("--step", type=float, default=0.5)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    parser.add_argument("--output", type=pathlib.Path)
    args = parser.parse_args()

    ranks = uniform_ranks(args.dimension)
    unitaries, projectors, history = optimize(
        args.dimension,
        ranks,
        args.seed,
        args.sweeps,
        args.step,
        args.tolerance,
    )
    result = {
        "dimension": args.dimension,
        "seed": args.seed,
        "sweeps_completed": len(history) - 1,
        "initial_energy": float(history[0]),
        "final_energy": float(history[-1]),
        "ranks": ranks.tolist(),
        "warning": "Exploratory floating-point data; not a certificate.",
    }
    print(json.dumps(result, indent=2))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            args.output,
            unitaries=unitaries,
            projectors=projectors,
            history=history,
            metadata=json.dumps(result, sort_keys=True),
        )


if __name__ == "__main__":
    main()
