#!/usr/bin/env python3
"""Probe scalar upper bounds for the square-zero feature concurrence.

For orthogonal two-frames U,W in three qutrits, compress

    R = sum_{i<j} A_i A_j,  A_i=(I-F_i)/2,

to the logical product frame |a,b> -> u_a tensor w_b.  The conjectured
bound is homogeneous_concurrence(R) <= 1/2.  This script compares that
quantity with simple trace moments.  All output is floating point and
is discovery evidence only.
"""

from __future__ import annotations

import argparse

import numpy as np


WORDS = np.asarray(
    [(a, b, c) for a in range(3) for b in range(3) for c in range(3)],
    dtype=np.int64,
)
PAIR_WORDS = np.asarray(
    [
        tuple(WORDS[left]) + tuple(WORDS[right])
        for left in range(27)
        for right in range(27)
    ],
    dtype=np.int64,
)


def swap_permutation(site: int) -> np.ndarray:
    words = PAIR_WORDS.copy()
    words[:, [site, site + 3]] = words[:, [site + 3, site]]
    left = 9 * words[:, 0] + 3 * words[:, 1] + words[:, 2]
    right = 9 * words[:, 3] + 3 * words[:, 4] + words[:, 5]
    return 27 * left + right


SWAPS = [swap_permutation(site) for site in range(3)]


def antisymmetrize(vector: np.ndarray, site: int) -> np.ndarray:
    return 0.5 * (vector - vector[SWAPS[site]])


def feature(frame_u: np.ndarray, frame_w: np.ndarray) -> np.ndarray:
    columns = np.column_stack(
        [
            np.kron(frame_u[:, a], frame_w[:, b])
            for a in range(2)
            for b in range(2)
        ]
    )
    out = np.zeros((4, 4), dtype=np.complex128)
    for first, second in ((0, 1), (0, 2), (1, 2)):
        image = np.column_stack(
            [
                antisymmetrize(
                    antisymmetrize(columns[:, label], first),
                    second,
                )
                for label in range(4)
            ]
        )
        out += image.conj().T @ image
    return 0.5 * (out + out.conj().T)


SPIN = np.asarray(
    [[0, 0, 0, 1], [0, 0, -1, 0], [0, -1, 0, 0], [1, 0, 0, 0]],
    dtype=np.complex128,
)


def spin_flip(matrix: np.ndarray) -> np.ndarray:
    return SPIN @ matrix.conj() @ SPIN


def concurrence(matrix: np.ndarray) -> tuple[float, np.ndarray]:
    roots = np.linalg.eigvals(matrix @ spin_flip(matrix))
    roots = np.sort(
        np.sqrt(np.maximum(0.0, roots.real))
    )[::-1]
    return max(0.0, float(roots[0] - roots[1:].sum())), roots


def random_orthogonal_frames(
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    raw = rng.standard_normal((27, 4)) + 1j * rng.standard_normal((27, 4))
    frame = np.linalg.qr(raw)[0]
    return frame[:, :2], frame[:, 2:]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260729)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)

    maxima = {
        "concurrence": (-np.inf, None),
        "trace_R_tilde_R": (-np.inf, None),
        "trace_R": (-np.inf, None),
        "operator_norm": (-np.inf, None),
    }
    for sample in range(args.samples):
        frame_u, frame_w = random_orthogonal_frames(rng)
        matrix = feature(frame_u, frame_w)
        value, _ = concurrence(matrix)
        metrics = {
            "concurrence": value,
            "trace_R_tilde_R": float(
                np.trace(matrix @ spin_flip(matrix)).real
            ),
            "trace_R": float(np.trace(matrix).real),
            "operator_norm": float(np.linalg.eigvalsh(matrix)[-1]),
        }
        for key, metric in metrics.items():
            if metric > maxima[key][0]:
                maxima[key] = (metric, sample)
    for key, value in maxima.items():
        print(key, value)


if __name__ == "__main__":
    main()
