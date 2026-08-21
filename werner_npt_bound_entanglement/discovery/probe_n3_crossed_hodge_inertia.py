#!/usr/local/bin/python
"""Discovery-only search for two negative crossed-Hodge directions.

At one qutrit site, form the two-copy block Gram

    beta_(a,p),(b,q) = B_2(C_ap,C_bq)

for C = X Y^*.  The experiment minimizes the middle eigenvalue of
P_- beta^Gamma P_- over unrestricted complex rank-two factors.
All conclusions from this file are numerical only.
"""

from __future__ import annotations

import argparse
import sys

import numpy as np
from scipy.optimize import minimize

from optimize_n3_haar_block_gram import (
    block_matrix,
    pack,
    rest_L,
    unblock_matrix,
    unpack,
)


def partial_transpose(z: np.ndarray) -> np.ndarray:
    return z.reshape(3, 3, 3, 3).transpose(0, 3, 2, 1).reshape(9, 9)


def hodge_frame() -> np.ndarray:
    out = []
    for a, p in ((0, 1), (0, 2), (1, 2)):
        z = np.zeros(9, dtype=complex)
        z[3 * a + p] = 1 / np.sqrt(2)
        z[3 * p + a] = -1 / np.sqrt(2)
        out.append(z)
    return np.array(out).T


HODGE = hodge_frame()


def objective(x: np.ndarray) -> tuple[float, np.ndarray]:
    left, right = unpack(x)
    c = left @ right.conj().T
    norm2 = np.vdot(c, c).real
    blocks = block_matrix(c, 0)
    transformed = block_matrix(rest_L(c, 0), 0)
    beta = blocks.conj().T @ transformed
    crossed = partial_transpose(beta)
    hodge = HODGE.conj().T @ crossed @ HODGE
    hodge = (hodge + hodge.conj().T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(hodge)
    vector = HODGE @ eigenvectors[:, 1]

    # lambda = Tr(beta Gamma(|vector><vector|)).
    coefficient = partial_transpose(np.outer(vector, vector.conj()))
    gradient_c = unblock_matrix(transformed @ coefficient, 0)
    value = eigenvalues[1].real / norm2
    gradient_c = (
        gradient_c / norm2
        - eigenvalues[1].real * c / norm2**2
    )
    gradient_left = gradient_c @ right
    gradient_right = gradient_c.conj().T @ left
    gradient = np.concatenate(
        (
            gradient_left.reshape(-1),
            gradient_right.reshape(-1),
        )
    )
    packed_gradient = np.concatenate((2 * gradient.real, 2 * gradient.imag))
    return float(value), packed_gradient


def finite_difference_check(x: np.ndarray) -> None:
    value, gradient = objective(x)
    rng = np.random.default_rng(991)
    direction = rng.normal(size=x.size)
    direction /= np.linalg.norm(direction)
    for step in (1e-4, 3e-5, 1e-5):
        numerical = (
            objective(x + step * direction)[0]
            - objective(x - step * direction)[0]
        ) / (2 * step)
        exact = np.dot(gradient, direction)
        print("gradient", step, numerical, exact, abs(numerical - exact))
    print("initial", value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--maxiter", type=int, default=1000)
    parser.add_argument("--check-gradient", action="store_true")
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    left = rng.normal(size=(27, 2)) + 1j * rng.normal(size=(27, 2))
    right = rng.normal(size=(27, 2)) + 1j * rng.normal(size=(27, 2))
    left /= np.linalg.norm(left)
    right /= np.linalg.norm(right)
    x0 = pack(left, right)
    if args.check_gradient:
        finite_difference_check(x0)
        return
    result = minimize(
        objective,
        x0,
        jac=True,
        method="L-BFGS-B",
        options={"maxiter": args.maxiter, "ftol": 1e-14, "gtol": 1e-10},
    )
    left, right = unpack(result.x)
    c = left @ right.conj().T
    blocks = block_matrix(c, 0)
    transformed = block_matrix(rest_L(c, 0), 0)
    beta = blocks.conj().T @ transformed
    hodge = HODGE.conj().T @ partial_transpose(beta) @ HODGE
    hodge = (hodge + hodge.conj().T) / 2
    print(result.message)
    print("iterations", result.nit)
    print("objective", result.fun)
    print("hodge / ||C||^2", np.linalg.eigvalsh(hodge) / np.vdot(c, c).real)
    print("C singular values", np.linalg.svd(c, compute_uv=False)[:4])


if __name__ == "__main__":
    sys.exit(main())
