"""Adversarial discovery test for a square-zero determinant bound.

This is not a verifier.  For orthogonal two-planes U,W in three
qutrits, let G be the 4-by-4 endpoint Gram on Hom(W,U), and let
rho_i^U, rho_i^W be their one-site plane marginals.  The candidate is

    det(G) >= (243/1024) sum_i det(rho_i^U) det(rho_i^W).

The script minimizes the defect over a complex 27-by-4 Stiefel frame.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

import numpy as np
from scipy.optimize import minimize

from search_n3_squarezero_q import endpoint_operator, orthonormalize


SHARP = float(Fraction(243, 1024))


def unpack(x: np.ndarray) -> np.ndarray:
    z = (x[:108] + 1j * x[108:]).reshape(27, 4)
    return orthonormalize(z)


def plane_marginal(frame: np.ndarray, site: int) -> np.ndarray:
    out = np.zeros((3, 3), dtype=np.complex128)
    axes = tuple(j for j in range(3) if j != site)
    for column in range(2):
        vector = frame[:, column].reshape(3, 3, 3)
        out += np.tensordot(vector, vector.conj(), axes=(axes, axes))
    return out


def gram(frame: np.ndarray) -> np.ndarray:
    u, w = frame[:, :2], frame[:, 2:]
    units = [
        np.outer(u[:, a], w[:, b].conj())
        for a in range(2)
        for b in range(2)
    ]
    out = np.array(
        [
            [np.vdot(e, endpoint_operator(f)) for f in units]
            for e in units
        ]
    )
    return (out + out.conj().T) / 2


def defect_from_frame(frame: np.ndarray) -> float:
    u, w = frame[:, :2], frame[:, 2:]
    marginal_term = sum(
        np.linalg.det(plane_marginal(u, site)).real
        * np.linalg.det(plane_marginal(w, site)).real
        for site in range(3)
    )
    return float(np.linalg.det(gram(frame)).real - SHARP * marginal_term)


def objective(x: np.ndarray) -> float:
    return defect_from_frame(unpack(x))


def ghz_equality_frame() -> np.ndarray:
    omega = np.exp(2j * np.pi / 3)

    def state(a: int, b: int, phase: int) -> np.ndarray:
        out = np.zeros(27, dtype=np.complex128)
        for j in range(3):
            index = (j * 3 + (j + a) % 3) * 3 + (j + b) % 3
            out[index] = omega ** (phase * j) / np.sqrt(3)
        return out

    labels = ((0, 0, 0), (0, 0, 1), (1, 2, 2), (2, 1, 2))
    return np.column_stack([state(*label) for label in labels])


def coordinates(frame: np.ndarray) -> np.ndarray:
    return np.r_[frame.real.ravel(), frame.imag.ravel()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=8)
    parser.add_argument("--iterations", type=int, default=60)
    parser.add_argument("--noise", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=20260729)
    parser.add_argument("--output", default="n3_squarezero_det_bound_best.npz")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    exact_frame = ghz_equality_frame()
    print("GHZ equality defect", defect_from_frame(exact_frame))
    best = (defect_from_frame(exact_frame), exact_frame)

    for start in range(args.starts):
        if start == 0:
            frame = exact_frame
        elif start < args.starts // 2:
            frame = orthonormalize(
                exact_frame
                + args.noise
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

        result = minimize(
            objective,
            coordinates(frame),
            method="L-BFGS-B",
            options={
                "maxiter": args.iterations,
                "ftol": 1e-14,
                "gtol": 1e-9,
                "maxls": 50,
            },
        )
        candidate = unpack(result.x)
        value = defect_from_frame(candidate)
        if value < best[0]:
            best = (value, candidate)
        print(start, value, "global", best[0], result.message, flush=True)

    np.savez(args.output, defect=best[0], z=best[1])


if __name__ == "__main__":
    main()
