#!/usr/bin/env python3
"""Numerical falsifier that searches the exact equality variety at d=4.

This is discovery code, not a proof.  It fixes A0=diag(1,i,-1,-i),
parameterizes A1=Q diag(1,i,-1,-i) Q^* (so A1 is automatically an
order-four unitary), and solves the exact-maximizer kernel constraints

    (A0^* A1)^4 = -I,
    polar(A0+i^y A1)^4 = I,  y=0,1,2,3.

The final scalar residual asks for a non-Weyl component with
sum_j |(A1^2)_{jj}|^2=1.  Scanning this target was how the nonuniform
component was exposed.  The released proof replaces the dense numerical
representative by a gauge-equivalent sparse weighted shift.  It does not
depend on this script.
"""
from __future__ import annotations
import argparse
import numpy as np
from scipy.linalg import expm, polar
from scipy.optimize import least_squares

D = 4
I4 = np.eye(D, dtype=complex)
A0 = np.diag([1, 1j, -1, -1j]).astype(complex)
ROOTS = np.array([1, 1j, -1, -1j], dtype=complex)


def hermitian_from_real(x: np.ndarray) -> np.ndarray:
    """Map 16 real coordinates to a 4x4 Hermitian matrix."""
    H = np.zeros((D, D), dtype=complex)
    H[np.diag_indices(D)] = x[:D]
    k = D
    for i in range(D):
        for j in range(i + 1, D):
            H[i, j] = x[k] + 1j * x[k + 1]
            H[j, i] = x[k] - 1j * x[k + 1]
            k += 2
    return H


def fourth_power(A: np.ndarray) -> np.ndarray:
    A2 = A @ A
    return A2 @ A2


def strategy(x: np.ndarray):
    Q = expm(1j * hermitian_from_real(x))
    A1 = Q @ np.diag(ROOTS) @ Q.conj().T
    U = A0.conj().T @ A1
    V = [polar(A0 + (1j**y) * A1)[0] for y in range(D)]
    return A1, U, V


def residual(x: np.ndarray, defect_target: float) -> np.ndarray:
    A1, U, V = strategy(x)
    matrices = [fourth_power(U) + I4]
    matrices += [fourth_power(Vy) - I4 for Vy in V]
    flat = np.concatenate([
        np.concatenate((M.real.ravel(), M.imag.ravel())) for M in matrices
    ])
    defect = float(np.sum(np.abs(np.diag(A1 @ A1)) ** 2))
    return np.r_[flat, 0.1 * (defect - defect_target)]


def target_probabilities(A1: np.ndarray) -> np.ndarray:
    """p(a,b|x=1,y=4) for Phi_4 and B4=conj(A0)."""
    probs = np.empty((D, D), dtype=float)
    powers = [np.linalg.matrix_power(A1, r) for r in range(D)]
    for a in range(D):
        Pa = sum((1j ** (-a * r)) * powers[r] for r in range(D)) / D
        for b in range(D):
            probs[a, b] = Pa[(-b) % D, (-b) % D].real / D
    return probs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--restarts", type=int, default=4)
    ap.add_argument("--max-nfev", type=int, default=5000)
    ap.add_argument("--defect-target", type=float, default=1.0)
    args = ap.parse_args()

    best = None
    for restart in range(args.restarts):
        rng = np.random.default_rng(args.seed + restart)
        x0 = rng.normal(scale=0.8, size=16)
        result = least_squares(
            residual,
            x0,
            args=(args.defect_target,),
            max_nfev=args.max_nfev,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        A1, U, V = strategy(result.x)
        matrix_residual = np.linalg.norm(residual(result.x, args.defect_target)[:-1])
        defect = float(np.sum(np.abs(np.diag(A1 @ A1)) ** 2))
        score = matrix_residual + abs(defect - args.defect_target)
        print(f"restart={restart} residual={matrix_residual:.3e} defect={defect:.12f}")
        if best is None or score < best[0]:
            best = (score, A1, matrix_residual, defect)

    _, A1, matrix_residual, defect = best
    probs = target_probabilities(A1)
    np.set_printoptions(precision=10, suppress=True)
    print("\nBest |A1| (the 1/2,1/sqrt(2),1/2 pattern is recognizable):")
    print(np.abs(A1))
    print("\nTarget probability table:")
    print(probs)
    print(f"max probability = {probs.max():.12f}; uniform value = {1/16:.12f}")
    if matrix_residual < 1e-8 and probs.max() > 1 / 16 + 1e-6:
        print("NUMERICAL CANDIDATE FOUND. verify_exact.py checks the simplified exact representative.")
    else:
        print("No certified conclusion: this script is numerical discovery only.")


if __name__ == "__main__":
    main()
