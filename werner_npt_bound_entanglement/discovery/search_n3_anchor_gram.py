#!/usr/bin/env python3
"""Floating-point search for violations of the n=3 anchored Gram inequality.

Discovery only.  The optimized quotient is

    |B_3(P_w, |u><v|)|^2 /
    (Q_3(P_w) Q_3(|u><v|)).
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import minimize


def make_phi(local: int):
    copies = 3
    dimension = local**copies
    words = np.array(
        list(itertools.product(range(local), repeat=copies)), dtype=int
    )

    maps = []
    for mask in range(1 << copies):
        keep = [i for i in range(copies) if not (mask >> i) & 1]
        retained = np.zeros(dimension, dtype=int)
        for site in keep:
            retained = local * retained + words[:, site]
        compatible = np.ones((dimension, dimension), dtype=bool)
        for site in range(copies):
            if (mask >> site) & 1:
                compatible &= (
                    words[:, site, None] == words[None, :, site]
                )
        maps.append((retained, compatible, local ** len(keep)))

    def phi(matrix: np.ndarray) -> np.ndarray:
        out = np.zeros_like(matrix)
        for mask, (retained, compatible, size) in enumerate(maps):
            reduced = np.zeros((size, size), dtype=complex)
            rows, columns = np.nonzero(compatible)
            np.add.at(
                reduced,
                (retained[rows], retained[columns]),
                matrix[rows, columns],
            )
            embedded = (
                compatible
                * reduced[retained[:, None], retained[None, :]]
            )
            out += (-0.5) ** bin(mask).count("1") * embedded
        return out

    return dimension, phi


def unpack(point: np.ndarray, dimension: int, orthonormal: bool = False):
    vectors = []
    for block in range(3):
        start = 2 * block * dimension
        vector = (
            point[start : start + dimension]
            + 1j
            * point[start + dimension : start + 2 * dimension]
        )
        vector /= np.linalg.norm(vector)
        vectors.append(vector)
    if not orthonormal:
        return vectors
    frame = np.stack(vectors, axis=1)
    q, r = np.linalg.qr(frame)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1)
    q *= phases.conj()
    return [q[:, column] for column in range(3)]


def quotient(
    point: np.ndarray, dimension: int, phi, orthonormal: bool = False
) -> float:
    w, u, v = unpack(point, dimension, orthonormal)
    projection = np.outer(w, w.conj())
    rank_one = np.outer(u, v.conj())
    image_projection = phi(projection)
    image_rank_one = phi(rank_one)
    a = np.vdot(projection, image_projection).real
    b = np.vdot(rank_one, image_rank_one).real
    z = np.vdot(projection, image_rank_one)
    return float(abs(z) ** 2 / (a * b))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", type=int, default=2)
    parser.add_argument("--starts", type=int, default=10)
    parser.add_argument("--iterations", type=int, default=500)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--orthonormal", action="store_true")
    args = parser.parse_args()
    dimension, phi = make_phi(args.local)
    rng = np.random.default_rng(args.seed)
    best = (0.0, None)
    for start in range(args.starts):
        initial = rng.normal(size=6 * dimension)
        result = minimize(
            lambda point: -quotient(
                point, dimension, phi, args.orthonormal
            ),
            initial,
            method="L-BFGS-B",
            options={"maxiter": args.iterations, "ftol": 1e-13},
        )
        value = quotient(result.x, dimension, phi, args.orthonormal)
        if value > best[0]:
            best = value, result.x.copy()
        print(start, value, result.success, result.nit, flush=True)
    print("best", best[0])
    if best[1] is not None:
        np.savez(
            "n3_anchor_gram_best.npz",
            point=best[1],
            local=args.local,
            quotient=best[0],
        )


if __name__ == "__main__":
    main()
