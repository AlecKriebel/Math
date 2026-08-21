#!/usr/bin/env python3
"""Discovery probe for the unrestricted three-copy code output.

For a two-dimensional code W, form

    M_W = (id_2 tensor Phi^tensor3)(|Psi_W><Psi_W|)
        = A_W - |Psi_W><Psi_W| / 8.

This script tests whether the unshifted operator A_W is positive and
records the rank-one Schur scalar <Psi_W|A_W^{-1}|Psi_W>.  Floating
point output is conjecture-generation only.
"""

from __future__ import annotations

import argparse

import numpy as np


WORDS = np.asarray(
    [(a, b, c) for a in range(3) for b in range(3) for c in range(3)],
    dtype=np.int64,
)


def encode(word: np.ndarray) -> int:
    return int(9 * word[0] + 3 * word[1] + word[2])


def apply_phi_site(matrix: np.ndarray, site: int) -> np.ndarray:
    """Apply Phi(X)=Tr(X)I-X/2 on one qutrit tensor factor."""

    out = -0.5 * np.asarray(matrix, dtype=np.complex128)
    row_word = np.empty(3, dtype=np.int64)
    col_word = np.empty(3, dtype=np.int64)
    for row in range(27):
        row_word[:] = WORDS[row]
        for column in range(27):
            if WORDS[row, site] != WORDS[column, site]:
                continue
            col_word[:] = WORDS[column]
            value = 0.0j
            for traced in range(3):
                row_word[site] = traced
                col_word[site] = traced
                value += matrix[encode(row_word), encode(col_word)]
            out[row, column] += value
    return out


def phi_tensor_three(matrix: np.ndarray) -> np.ndarray:
    out = matrix
    for site in range(3):
        out = apply_phi_site(out, site)
    return out


def code_output(frame: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (M_W, A_W, |Psi_W>) for a 27 by 2 isometry."""

    output = np.zeros((54, 54), dtype=np.complex128)
    for logical_row in range(2):
        for logical_column in range(2):
            block = np.outer(
                frame[:, logical_row],
                frame[:, logical_column].conj(),
            )
            output[
                27 * logical_row : 27 * (logical_row + 1),
                27 * logical_column : 27 * (logical_column + 1),
            ] = phi_tensor_three(block)
    psi = np.concatenate((frame[:, 0], frame[:, 1]))
    unshifted = output + np.outer(psi, psi.conj()) / 8.0
    return output, unshifted, psi


def random_isometry(rng: np.random.Generator) -> np.ndarray:
    raw = rng.standard_normal((27, 2)) + 1j * rng.standard_normal((27, 2))
    return np.linalg.qr(raw)[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260729)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)

    least_a = (float("inf"), None)
    least_m = (float("inf"), None)
    largest_schur = (-float("inf"), None)
    for sample in range(args.samples):
        frame = random_isometry(rng)
        output, unshifted, psi = code_output(frame)
        eig_a = np.linalg.eigvalsh(unshifted)
        eig_m = np.linalg.eigvalsh(output)
        schur = float(
            np.vdot(psi, np.linalg.solve(unshifted, psi)).real
        )
        if eig_a[0] < least_a[0]:
            least_a = (float(eig_a[0]), sample)
        if eig_m[0] < least_m[0]:
            least_m = (float(eig_m[0]), sample)
        if schur > largest_schur[0]:
            largest_schur = (schur, sample)

    print("samples", args.samples)
    print("least lambda_min(A_W)", least_a)
    print("least lambda_min(M_W)", least_m)
    print("largest <Psi|A_W^-1|Psi>", largest_schur)


if __name__ == "__main__":
    main()
