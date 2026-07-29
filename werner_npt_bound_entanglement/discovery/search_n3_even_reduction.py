#!/usr/bin/env python3
"""Discovery search for a negative cyclic even-reduction form.

The variable is a Frobenius-normalized rank-two matrix

    C = U diag(s_1,s_2) V^*,

where U,V are complex 27-by-2 Stiefel frames and s lies on the positive
quarter circle.  Floating-point output is discovery evidence only.
"""

from __future__ import annotations

import argparse

import numpy as np


def trace_replace_site(matrix: np.ndarray, site: int) -> np.ndarray:
    tensor = matrix.reshape((3,) * 6)
    other = [i for i in range(3) if i != site]
    permutation = [site, *other, 3 + site, *(3 + i for i in other)]
    moved = tensor.transpose(permutation).reshape(3, 9, 3, 9)
    reduced = np.trace(moved, axis1=0, axis2=2)
    replaced = np.einsum("ab,ij->aibj", np.eye(3), reduced)
    inverse = np.argsort(permutation)
    return (
        replaced.reshape((3,) * 6)
        .transpose(inverse)
        .reshape(27, 27)
    )


def reduction(matrix: np.ndarray, site: int) -> np.ndarray:
    return trace_replace_site(matrix, site) - matrix


def even_map(matrix: np.ndarray) -> np.ndarray:
    reductions = [reduction(matrix, site) for site in range(3)]
    return (
        reduction(reductions[0], 1)
        + reduction(reductions[0], 2)
        + reduction(reductions[1], 2)
    )


def retract(frame: np.ndarray) -> np.ndarray:
    q, r = np.linalg.qr(frame)
    return q * np.exp(-1j * np.angle(np.diag(r)))[None, :]


def tangent(frame: np.ndarray, gradient: np.ndarray) -> np.ndarray:
    gram = frame.conj().T @ gradient
    return gradient - frame @ ((gram + gram.conj().T) / 2)


def evaluate(
    left: np.ndarray,
    right: np.ndarray,
    singular: np.ndarray,
    need_gradient: bool,
    corrected: bool = False,
) -> tuple[
    float,
    tuple[np.ndarray, np.ndarray, np.ndarray] | None,
    np.ndarray,
]:
    matrix = (left * singular) @ right.conj().T
    image = even_map(matrix)
    value = float(np.vdot(matrix, image).real)
    if corrected:
        trace = np.trace(matrix)
        image = image - 0.5 * trace * np.eye(27)
        value += 0.5 * (
            float(np.sum(singular)) ** 2 - abs(trace) ** 2
        )
    if not need_gradient:
        return value, None, matrix
    left_gradient = tangent(
        left, 2 * image @ (right * singular)
    )
    right_gradient = tangent(
        right, 2 * image.conj().T @ (left * singular)
    )
    singular_gradient = 2 * np.real(
        np.diag(left.conj().T @ image @ right)
    )
    if corrected:
        singular_gradient += np.sum(singular)
    singular_gradient -= (
        singular @ singular_gradient
    ) * singular
    return (
        value,
        (left_gradient, right_gradient, singular_gradient),
        matrix,
    )


def optimize(
    seed: int, iterations: int, initial_step: float, corrected: bool
) -> tuple[float, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    left = retract(
        rng.normal(size=(27, 2)) + 1j * rng.normal(size=(27, 2))
    )
    right = retract(
        rng.normal(size=(27, 2)) + 1j * rng.normal(size=(27, 2))
    )
    singular = rng.random(2) + 0.2
    singular /= np.linalg.norm(singular)
    step = initial_step
    best = float("inf")
    best_matrix = np.empty((27, 27), dtype=complex)
    best_singular = singular.copy()
    for iteration in range(iterations):
        value, gradients, matrix = evaluate(
            left, right, singular, True, corrected
        )
        assert gradients is not None
        if value < best:
            best = value
            best_matrix = matrix.copy()
            best_singular = singular.copy()
        norm_squared = (
            np.vdot(gradients[0], gradients[0]).real
            + np.vdot(gradients[1], gradients[1]).real
            + gradients[2] @ gradients[2]
        )
        if iteration % 100 == 0:
            print(
                f"seed={seed} iter={iteration} E={value:.15g} "
                f"s={singular} grad2={norm_squared:.3e}",
                flush=True,
            )
        if norm_squared < 1e-22:
            break
        accepted = False
        trial = step
        for _ in range(30):
            candidate_left = retract(left - trial * gradients[0])
            candidate_right = retract(right - trial * gradients[1])
            candidate_singular = np.maximum(
                singular - trial * gradients[2], 1e-10
            )
            candidate_singular /= np.linalg.norm(
                candidate_singular
            )
            candidate, _, _ = evaluate(
                candidate_left,
                candidate_right,
                candidate_singular,
                False,
                corrected,
            )
            if candidate <= value - 1e-6 * trial * norm_squared:
                left = candidate_left
                right = candidate_right
                singular = candidate_singular
                step = min(initial_step, 1.2 * trial)
                accepted = True
                break
            trial *= 0.5
        if not accepted:
            break
    return best, best_singular, best_matrix


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--restarts", type=int, default=10)
    parser.add_argument("--iterations", type=int, default=3000)
    parser.add_argument("--step", type=float, default=0.05)
    parser.add_argument("--corrected", action="store_true")
    args = parser.parse_args()
    overall = (float("inf"), None, None, None)
    for offset in range(args.restarts):
        seed = args.seed + offset
        value, singular, matrix = optimize(
            seed, args.iterations, args.step, args.corrected
        )
        print("RESULT", seed, value, singular, flush=True)
        if value < overall[0]:
            overall = (value, seed, singular, matrix)
    print("OVERALL", overall[:3], flush=True)
    if overall[0] < -1e-8:
        np.save("/tmp/n3_even_negative.npy", overall[3])


if __name__ == "__main__":
    main()
