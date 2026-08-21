#!/usr/bin/env python3
"""Discovery probe for an intrinsic n=3 determinant/support gap.

For orthonormal two-frames U,V on three qutrits, form the 2x2 endpoint
Gram on the matched rank-one matrices u_r v_r^*.  Compare its determinant
with the six one-site support determinants of the two code planes.

Floating-point output is conjecture-generation only.
"""

from __future__ import annotations

import argparse

import numpy as np


def haar_frame(rng: np.random.Generator) -> np.ndarray:
    matrix = rng.normal(size=(27, 2)) + 1j * rng.normal(size=(27, 2))
    q, r = np.linalg.qr(matrix)
    phases = np.diag(r).copy()
    phases /= np.where(np.abs(phases) > 0, np.abs(phases), 1)
    return q * phases.conj()


def apply_local_l(matrix: np.ndarray, site: int) -> np.ndarray:
    tensor = matrix.reshape((3,) * 6)
    traced = np.trace(tensor, axis1=site, axis2=site + 3)
    inserted = np.zeros_like(tensor)
    for value in range(3):
        index = [slice(None)] * 6
        index[site] = value
        index[site + 3] = value
        inserted[tuple(index)] = traced
    return (tensor - 0.5 * inserted).reshape(27, 27)


def endpoint_image(matrix: np.ndarray) -> np.ndarray:
    result = matrix
    for site in range(3):
        result = apply_local_l(result, site)
    return result


def local_support(frame: np.ndarray, site: int) -> np.ndarray:
    support = np.zeros((3, 3), dtype=complex)
    for column in range(2):
        tensor = np.moveaxis(frame[:, column].reshape(3, 3, 3), site, 0)
        flat = tensor.reshape(3, 9)
        support += flat @ flat.conj().T
    return support


def data(left: np.ndarray, right: np.ndarray) -> tuple[float, float, list[float]]:
    rank_one = [
        np.outer(left[:, index], right[:, index].conj())
        for index in range(2)
    ]
    images = [endpoint_image(matrix) for matrix in rank_one]
    gram = np.array(
        [
            [np.vdot(rank_one[row], images[column]) for column in range(2)]
            for row in range(2)
        ]
    )
    determinant = float(np.linalg.det(gram).real)
    supports = [
        float(np.linalg.det(local_support(frame, site)).real)
        for frame in (left, right)
        for site in range(3)
    ]
    return determinant, sum(supports), supports


def load_state(path: str) -> tuple[np.ndarray, np.ndarray]:
    left = np.zeros((27, 2), dtype=complex)
    right = np.zeros((27, 2), dtype=complex)
    with open(path, encoding="utf-8") as source:
        for line in source:
            fields = line.split()
            if fields and fields[0] in ("left", "right"):
                row, column = int(fields[1]), int(fields[2])
                value = complex(float(fields[3]), float(fields[4]))
                (left if fields[0] == "left" else right)[row, column] = value
    return left, right


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260729)
    parser.add_argument("--state")
    args = parser.parse_args()
    if args.state:
        determinant, support_sum, supports = data(*load_state(args.state))
        print("state determinant", determinant)
        print("state support sum", support_sum)
        print("state det/sum_support", determinant / support_sum)
        print("state supports", supports)
        return
    rng = np.random.default_rng(args.seed)

    best = (float("inf"), None)
    negative = 0
    for sample in range(args.samples):
        determinant, support_sum, supports = data(
            haar_frame(rng), haar_frame(rng)
        )
        ratio = determinant / support_sum
        if ratio < best[0]:
            best = (ratio, (sample, determinant, support_sum, supports))
        if determinant + 1e-11 < support_sum / 27:
            negative += 1

    print("best ratio det/sum_support", best[0])
    print("best data", best[1])
    print("violations of det >= sum_support/27", negative)


if __name__ == "__main__":
    main()
