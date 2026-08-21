"""Riemannian search for the square-zero product-determinant conjecture.

Discovery code only.  For a complex orthonormal four-frame Z=(U,W),
minimize

    log det H(U,W)
      - sum_i [log det rho_i^U + log det rho_i^W].

The conjectured sharp minimum is log(3^18 / 2^22).  The implementation
uses the exact first variation of log det H and projected gradient
descent on the complex Stiefel manifold.  If H ever ceases to be
positive definite, the frame is saved immediately because it is a
square-zero Werner counterexample.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

import numpy as np

from search_n3_squarezero_det_bound import (
    ghz_equality_frame,
    gram,
    plane_marginal,
)
from search_n3_squarezero_q import endpoint_operator, orthonormalize


SHARP_RATIO = float(Fraction(3**18, 2**22))


def apply_local(
    matrix: np.ndarray, frame: np.ndarray, site: int
) -> np.ndarray:
    """Apply a three-by-three matrix at one physical site."""
    out = np.empty_like(frame)
    for column in range(frame.shape[1]):
        tensor = frame[:, column].reshape(3, 3, 3)
        acted = np.tensordot(matrix, tensor, axes=(1, site))
        out[:, column] = np.moveaxis(acted, 0, site).reshape(27)
    return out


def objective_and_gradient(
    frame: np.ndarray,
) -> tuple[float, np.ndarray, np.ndarray]:
    """Return log-ratio, Euclidean gradient, and H eigenvalues."""
    u, w = frame[:, :2], frame[:, 2:]
    h = gram(frame)
    values, vectors = np.linalg.eigh(h)
    if values[0] <= 0:
        return -np.inf, np.zeros_like(frame), values

    objective = float(np.log(values).sum())
    grad_u = np.zeros_like(u)
    grad_w = np.zeros_like(w)

    # H^{-1} = sum_t value_t^{-1} |vector_t><vector_t|.  Each
    # quadratic vector_t^* H vector_t is Q_3(U B_t W^*), whose
    # first variation has the standard rank-factor gradients.
    for value, vector in zip(values, vectors.T):
        b = vector.reshape(2, 2)
        c = u @ b @ w.conj().T
        image = endpoint_operator(c)
        weight = 1.0 / value
        grad_u += 2 * weight * image @ w @ b.conj().T
        grad_w += 2 * weight * image.conj().T @ u @ b

    for side, gradient in ((u, grad_u), (w, grad_w)):
        for site in range(3):
            rho = plane_marginal(side, site)
            sign, logdet = np.linalg.slogdet(rho)
            if sign <= 0:
                return np.inf, np.zeros_like(frame), values
            objective -= float(logdet.real)
            gradient -= 2 * apply_local(np.linalg.inv(rho), side, site)

    euclidean = np.column_stack((grad_u, grad_w))
    return objective, euclidean, values


def tangent_projection(
    frame: np.ndarray, gradient: np.ndarray
) -> np.ndarray:
    normal = (
        frame.conj().T @ gradient + gradient.conj().T @ frame
    ) / 2
    return gradient - frame @ normal


def check_gradient(frame: np.ndarray, seed: int) -> None:
    rng = np.random.default_rng(seed)
    value, gradient, _ = objective_and_gradient(frame)
    direction = rng.normal(size=frame.shape) + 1j * rng.normal(
        size=frame.shape
    )
    direction = tangent_projection(frame, direction)
    direction /= np.linalg.norm(direction)
    predicted = float(np.vdot(gradient, direction).real)
    for epsilon in (1e-4, 3e-5, 1e-5):
        plus = orthonormalize(frame + epsilon * direction)
        minus = orthonormalize(frame - epsilon * direction)
        vp = objective_and_gradient(plus)[0]
        vm = objective_and_gradient(minus)[0]
        measured = (vp - vm) / (2 * epsilon)
        print(
            "gradient check",
            epsilon,
            "predicted",
            predicted,
            "measured",
            measured,
            "error",
            abs(predicted - measured),
        )
    print("base objective", value, "sharp", np.log(SHARP_RATIO))


def descend(
    frame: np.ndarray, steps: int, rate: float
) -> tuple[float, np.ndarray, np.ndarray]:
    best = (np.inf, frame.copy(), np.zeros(4))
    current, _, current_eigenvalues = objective_and_gradient(frame)
    for step in range(steps):
        value, gradient, eigenvalues = objective_and_gradient(frame)
        if value < best[0]:
            best = (value, frame.copy(), eigenvalues.copy())
        if not np.isfinite(value):
            return best
        tangent = tangent_projection(frame, gradient)
        norm = np.linalg.norm(tangent)
        if norm < 1e-10:
            break

        trial_rate = rate
        accepted = False
        for _ in range(24):
            trial = orthonormalize(frame - trial_rate * tangent)
            trial_value, _, trial_eigenvalues = objective_and_gradient(
                trial
            )
            if trial_eigenvalues[0] <= 0:
                return trial_value, trial, trial_eigenvalues
            if trial_value <= value - 1e-4 * trial_rate * norm**2:
                frame = trial
                current = trial_value
                current_eigenvalues = trial_eigenvalues
                accepted = True
                break
            trial_rate *= 0.5
        if not accepted:
            break
        if step % 100 == 0:
            print(
                " step",
                step,
                "objective",
                current,
                "ratio",
                np.exp(current),
                "mineig",
                current_eigenvalues[0],
                flush=True,
            )
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=20)
    parser.add_argument("--steps", type=int, default=1200)
    parser.add_argument("--rate", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=20260730)
    parser.add_argument(
        "--output", default="n3_squarezero_logdet_ratio_best.npz"
    )
    parser.add_argument("--check-gradient", action="store_true")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    ghz = ghz_equality_frame()
    if args.check_gradient:
        random_frame = orthonormalize(
            rng.normal(size=(27, 4)) + 1j * rng.normal(size=(27, 4))
        )
        check_gradient(random_frame, args.seed + 1)

    global_best = (
        objective_and_gradient(ghz)[0],
        ghz,
        np.linalg.eigvalsh(gram(ghz)),
    )
    print(
        "GHZ objective",
        global_best[0],
        "ratio",
        np.exp(global_best[0]),
        "sharp",
        SHARP_RATIO,
    )

    for start in range(args.starts):
        if start == 0:
            frame = ghz
        elif start < max(2, args.starts // 4):
            frame = orthonormalize(
                ghz
                + 0.1
                * (
                    rng.normal(size=(27, 4))
                    + 1j * rng.normal(size=(27, 4))
                )
            )
        else:
            frame = orthonormalize(
                rng.normal(size=(27, 4))
                + 1j * rng.normal(size=(27, 4))
            )
        result = descend(frame, args.steps, args.rate)
        if result[0] < global_best[0]:
            global_best = result
        print(
            "start",
            start,
            "objective",
            result[0],
            "ratio",
            np.exp(result[0]) if np.isfinite(result[0]) else result[0],
            "mineig",
            result[2][0],
            "global ratio",
            np.exp(global_best[0]),
            flush=True,
        )
        if result[2][0] <= 0:
            break

    value, frame, eigenvalues = global_best
    np.savez(
        args.output,
        objective=value,
        ratio=np.exp(value),
        z=frame,
        eigenvalues=eigenvalues,
    )


if __name__ == "__main__":
    main()
