#!/usr/bin/env python3
"""Discovery search for a negative Hermitian inertia-(2,2) operator.

For an orthonormal four-frame V, form the endpoint Gram matrix of the
four spectral projectors.  Its least eigenvector gives the best
Hilbert--Schmidt-normalized Hermitian operator diagonal in that frame.
Only iterates whose least eigenvector has at most two positive and at
most two negative entries are relevant to the inertia-(2,2) conjecture.

Floating-point output is not a certificate.
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


def endpoint_map(matrix: np.ndarray) -> np.ndarray:
    maps = [matrix]
    for site in range(3):
        old = list(maps)
        maps.extend(trace_replace_site(value, site) for value in old)
    value = np.zeros_like(matrix)
    for mask, image in enumerate(maps):
        value += (-0.5) ** mask.bit_count() * image
    return value


def retract(frame: np.ndarray) -> np.ndarray:
    q, r = np.linalg.qr(frame)
    return q * np.exp(-1j * np.angle(np.diag(r)))[None, :]


def tangent(frame: np.ndarray, gradient: np.ndarray) -> np.ndarray:
    gram = frame.conj().T @ gradient
    return gradient - frame @ ((gram + gram.conj().T) / 2)


def evaluate(
    frame: np.ndarray,
) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    projectors = [
        np.outer(frame[:, index], frame[:, index].conj())
        for index in range(4)
    ]
    images = [endpoint_map(projector) for projector in projectors]
    gram = np.array(
        [
            [np.vdot(projectors[i], images[j]).real for j in range(4)]
            for i in range(4)
        ]
    )
    values, vectors = np.linalg.eigh((gram + gram.T) / 2)
    weights = vectors[:, 0]
    operator = sum(
        weights[index] * projectors[index] for index in range(4)
    )
    image = endpoint_map(operator)
    gradient = tangent(
        frame,
        4 * image @ frame @ np.diag(weights),
    )
    return float(values[0]), weights, gram, gradient


def search(
    seed: int, iterations: int, initial_step: float
) -> tuple[float, np.ndarray]:
    rng = np.random.default_rng(seed)
    frame = retract(
        rng.normal(size=(27, 4)) + 1j * rng.normal(size=(27, 4))
    )
    step = initial_step
    best = evaluate(frame)[0]
    best_weights = evaluate(frame)[1]
    for iteration in range(iterations):
        value, weights, _, gradient = evaluate(frame)
        if value < best:
            best = value
            best_weights = weights.copy()
        norm_squared = float(np.vdot(gradient, gradient).real)
        if iteration % 50 == 0:
            signs = (
                int(np.sum(weights > 1e-9)),
                int(np.sum(weights < -1e-9)),
            )
            print(
                f"seed={seed} iter={iteration} value={value:.15g} "
                f"signs={signs} weights={weights} grad2={norm_squared:.3e}"
            )
        if norm_squared < 1e-20:
            break
        accepted = False
        trial = step
        for _ in range(30):
            candidate = retract(frame - trial * gradient)
            candidate_value = evaluate(candidate)[0]
            if candidate_value <= value - 1e-5 * trial * norm_squared:
                frame = candidate
                step = min(initial_step, 1.25 * trial)
                accepted = True
                break
            trial *= 0.5
        if not accepted:
            break
    return best, best_weights


def constrained_search(
    seed: int, iterations: int, initial_step: float
) -> tuple[float, np.ndarray]:
    """Joint descent with the spectral signs fixed to (+,+,-,-)."""
    rng = np.random.default_rng(seed)
    frame = retract(
        rng.normal(size=(27, 4)) + 1j * rng.normal(size=(27, 4))
    )
    signs = np.array([1.0, 1.0, -1.0, -1.0])
    magnitudes = rng.random(4) + 0.2
    magnitudes /= np.linalg.norm(magnitudes)
    step = initial_step
    best = float("inf")
    best_weights = signs * magnitudes
    for iteration in range(iterations):
        projectors = [
            np.outer(frame[:, index], frame[:, index].conj())
            for index in range(4)
        ]
        images = [endpoint_map(projector) for projector in projectors]
        gram = np.array(
            [
                [
                    np.vdot(projectors[i], images[j]).real
                    for j in range(4)
                ]
                for i in range(4)
            ]
        )
        gram = (gram + gram.T) / 2
        weights = signs * magnitudes
        value = float(weights @ gram @ weights)
        operator = sum(
            weights[index] * projectors[index] for index in range(4)
        )
        image = endpoint_map(operator)
        frame_gradient = tangent(
            frame, 4 * image @ frame @ np.diag(weights)
        )
        magnitude_gradient = 2 * signs * (gram @ weights)
        magnitude_gradient -= (
            magnitudes @ magnitude_gradient
        ) * magnitudes
        norm_squared = float(
            np.vdot(frame_gradient, frame_gradient).real
            + magnitude_gradient @ magnitude_gradient
        )
        if value < best:
            best = value
            best_weights = weights.copy()
        if iteration % 50 == 0:
            print(
                f"fixed seed={seed} iter={iteration} "
                f"value={value:.15g} weights={weights} "
                f"grad2={norm_squared:.3e}"
            )
        if norm_squared < 1e-20:
            break
        accepted = False
        trial = step
        for _ in range(30):
            candidate_frame = retract(frame - trial * frame_gradient)
            candidate_magnitudes = np.maximum(
                magnitudes - trial * magnitude_gradient, 1e-12
            )
            candidate_magnitudes /= np.linalg.norm(
                candidate_magnitudes
            )
            candidate_weights = signs * candidate_magnitudes
            candidate_projectors = [
                np.outer(
                    candidate_frame[:, index],
                    candidate_frame[:, index].conj(),
                )
                for index in range(4)
            ]
            candidate_images = [
                endpoint_map(projector)
                for projector in candidate_projectors
            ]
            candidate_gram = np.array(
                [
                    [
                        np.vdot(
                            candidate_projectors[i],
                            candidate_images[j],
                        ).real
                        for j in range(4)
                    ]
                    for i in range(4)
                ]
            )
            candidate_value = float(
                candidate_weights @ candidate_gram @ candidate_weights
            )
            if candidate_value <= value - 1e-5 * trial * norm_squared:
                frame = candidate_frame
                magnitudes = candidate_magnitudes
                step = min(initial_step, 1.25 * trial)
                accepted = True
                break
            trial *= 0.5
        if not accepted:
            break
    return best, best_weights


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--restarts", type=int, default=10)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--step", type=float, default=0.05)
    parser.add_argument("--fixed-signs", action="store_true")
    args = parser.parse_args()
    overall = (float("inf"), None, None)
    for offset in range(args.restarts):
        runner = constrained_search if args.fixed_signs else search
        value, weights = runner(
            args.seed + offset, args.iterations, args.step
        )
        signs = (
            int(np.sum(weights > 1e-9)),
            int(np.sum(weights < -1e-9)),
        )
        print(
            f"restart={offset} best={value:.15g} "
            f"signs={signs} weights={weights}"
        )
        if value < overall[0]:
            overall = (value, args.seed + offset, weights)
    print("overall", overall)


if __name__ == "__main__":
    main()
