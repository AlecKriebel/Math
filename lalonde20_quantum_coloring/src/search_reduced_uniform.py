#!/usr/bin/env python3
"""Exploratory search inside the uniform fixed-color normal-form ansatz.

For rank ``r`` and a complex structure ``S`` with ``S**2 = -I``, the twenty
block-column frames below give an exact rank-r projective orthogonal
representation of G19 on C^(3r).  Four copies are embedded into the four apex
complements in C^(4r).  Optimization only varies those four embeddings; hence
all fixed-color edge constraints and all apex constraints remain exact, while
the objective measures same-vertex cross-color overlap.

This is numerical reconnaissance, not a certificate.
"""

from __future__ import annotations

import argparse
import json
import pathlib

import numpy as np
import scipy.linalg


def haar_unitary(d: int, rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    q, r = np.linalg.qr(z)
    diagonal = np.diag(r)
    phases = np.where(np.abs(diagonal) > 0, diagonal / np.abs(diagonal), 1.0)
    return q @ np.diag(np.conjugate(phases))


def projection_from_blocks(blocks: tuple[np.ndarray, np.ndarray, np.ndarray]):
    frame = np.vstack(blocks)
    gram = frame.conj().T @ frame
    return frame @ np.linalg.solve(gram, frame.conj().T)


def normal_form_projectors(s: np.ndarray) -> np.ndarray:
    r = s.shape[0]
    identity = np.eye(r, dtype=complex)
    zero = np.zeros((r, r), dtype=complex)
    adjoint = s.conj().T
    blocks = (
        (identity, zero, zero),
        (zero, identity, zero),
        (zero, zero, identity),
        (identity, identity, zero),
        (identity, -identity, zero),
        (identity, zero, identity),
        (identity, zero, -identity),
        (zero, identity, identity),
        (zero, identity, -identity),
        (identity, identity, identity),
        (identity, identity, -identity),
        (identity, -identity, identity),
        (identity, -identity, -identity),
        (identity, zero, s),
        (zero, identity, s),
        (identity, -s, zero),
        (identity, identity, adjoint),
        (identity, -adjoint, adjoint),
        (identity, -adjoint, identity),
    )
    return np.stack([projection_from_blocks(entry) for entry in blocks])


def triangular_complex_structure(r: int, parameter: float) -> np.ndarray:
    if r % 2:
        raise ValueError("the triangular family uses an even rank")
    pair = np.array([[1j, parameter], [0.0, -1j]], dtype=complex)
    return scipy.linalg.block_diag(*([pair] * (r // 2)))


def apex_complement_embedding(color: int, r: int) -> np.ndarray:
    d = 4 * r
    keep = [index for index in range(d) if index // r != color]
    embedding = np.zeros((d, 3 * r), dtype=complex)
    embedding[keep, np.arange(3 * r)] = 1.0
    return embedding


def ambient_projectors(
    coordinate_projectors: np.ndarray,
    embeddings: list[np.ndarray],
    unitaries: np.ndarray,
) -> np.ndarray:
    result = []
    for color in range(4):
        w = embeddings[color] @ unitaries[color]
        result.append(np.einsum("ij,vjk,lk->vil", w, coordinate_projectors, w.conj()))
    # color, vertex, ambient row, ambient column
    return np.stack(result)


def overlap_energy(projectors: np.ndarray) -> float:
    value = 0.0
    for c in range(4):
        for e in range(c):
            value += float(
                np.real(np.einsum("vij,vji->", projectors[c], projectors[e]))
            )
    return value


def color_local_energy(color: int, candidate: np.ndarray, projectors: np.ndarray):
    value = 0.0
    for other in range(4):
        if other != color:
            value += float(
                np.real(np.einsum("vij,vji->", candidate, projectors[other]))
            )
    return value


def optimize(
    rank: int,
    parameter: float,
    seed: int,
    sweeps: int,
    initial_step: float,
    tolerance: float,
):
    rng = np.random.default_rng(seed)
    s = triangular_complex_structure(rank, parameter)
    coordinate = normal_form_projectors(s)
    fixed_color_edge_error = 0.0
    # The explicit graph is duplicated here only as an internal ansatz audit.
    from graph_data import E19

    for v, w in E19:
        fixed_color_edge_error = max(
            fixed_color_edge_error,
            float(np.linalg.norm(coordinate[v - 1] @ coordinate[w - 1])),
        )
    if fixed_color_edge_error > 1e-10:
        raise RuntimeError(f"normal-form edge audit failed: {fixed_color_edge_error}")

    embeddings = [apex_complement_embedding(c, rank) for c in range(4)]
    unitaries = np.stack([haar_unitary(3 * rank, rng) for _ in range(4)])
    projectors = ambient_projectors(coordinate, embeddings, unitaries)
    history = [overlap_energy(projectors)]
    step_scale = initial_step

    for sweep in range(sweeps):
        moved = 0
        for color in rng.permutation(4):
            color = int(color)
            w = embeddings[color] @ unitaries[color]
            gradient = np.zeros((3 * rank, 3 * rank), dtype=complex)
            for vertex in range(19):
                ambient_sum = sum(
                    projectors[other, vertex]
                    for other in range(4)
                    if other != color
                )
                p = unitaries[color] @ coordinate[vertex] @ unitaries[color].conj().T
                compressed = embeddings[color].conj().T @ ambient_sum @ embeddings[color]
                gradient += p @ compressed - compressed @ p
            gradient = (gradient - gradient.conj().T) / 2
            norm = float(np.linalg.norm(gradient))
            if norm < 1e-14:
                continue
            old_local = color_local_energy(color, projectors[color], projectors)
            step = step_scale / max(1.0, norm)
            for _ in range(20):
                candidate_u = scipy.linalg.expm(step * gradient) @ unitaries[color]
                candidate_w = embeddings[color] @ candidate_u
                candidate_p = np.einsum(
                    "ij,vjk,lk->vil",
                    candidate_w,
                    coordinate,
                    candidate_w.conj(),
                )
                new_local = color_local_energy(color, candidate_p, projectors)
                if new_local < old_local - 1e-13 * max(1.0, old_local):
                    unitaries[color] = candidate_u
                    projectors[color] = candidate_p
                    moved += 1
                    break
                step *= 0.5

        current = overlap_energy(projectors)
        history.append(current)
        if sweep % 25 == 0 or current < tolerance:
            print(
                f"rank={rank} t={parameter:g} seed={seed} sweep={sweep:5d} "
                f"energy={current:.16e} moved={moved}",
                flush=True,
            )
        if current < tolerance:
            break
        if moved < 2:
            step_scale *= 0.8

    return s, coordinate, unitaries, projectors, np.asarray(history)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rank", "-r", type=int, default=2)
    parser.add_argument("--parameter", "-t", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--sweeps", type=int, default=1000)
    parser.add_argument("--step", type=float, default=1.0)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    parser.add_argument("--output", type=pathlib.Path)
    args = parser.parse_args()
    result = optimize(
        args.rank,
        args.parameter,
        args.seed,
        args.sweeps,
        args.step,
        args.tolerance,
    )
    s, coordinate, unitaries, projectors, history = result
    metadata = {
        "rank": args.rank,
        "dimension": 4 * args.rank,
        "parameter": args.parameter,
        "seed": args.seed,
        "sweeps_completed": len(history) - 1,
        "initial_energy": float(history[0]),
        "final_energy": float(history[-1]),
        "warning": "Exploratory floating-point data; not a certificate.",
    }
    print(json.dumps(metadata, indent=2))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            args.output,
            complex_structure=s,
            coordinate_projectors=coordinate,
            unitaries=unitaries,
            projectors=projectors,
            history=history,
            metadata=json.dumps(metadata, sort_keys=True),
        )


if __name__ == "__main__":
    main()
