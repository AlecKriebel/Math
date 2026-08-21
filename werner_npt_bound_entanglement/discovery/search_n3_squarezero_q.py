"""Unrestricted discovery search for the three-copy square-zero frontier.

This is not a verifier.  It minimizes Q_3(C) over

    C = U B W^*,  [U W]^*[U W] = I_4,  ||B||_2 = 1.

Hence C^2 = 0 and rank(C) <= 2.  For a fixed four-frame, the optimal
logical matrix B is obtained from an exact 4-by-4 Hermitian eigenproblem.
The outer loop uses projected gradient descent on the complex Stiefel
manifold.
"""

from __future__ import annotations

import argparse
import numpy as np


DIMS = (3, 3, 3)
D = 27


def partial_trace_one(c: np.ndarray, site: int) -> np.ndarray:
    tensor = c.reshape(DIMS + DIMS)
    reduced = np.trace(tensor, axis1=site, axis2=site + 3)
    return reduced.reshape(9, 9)


def trace_adjoint_one(reduced: np.ndarray, site: int) -> np.ndarray:
    tensor = reduced.reshape((3, 3, 3, 3))
    out = np.zeros(DIMS + DIMS, dtype=np.complex128)
    for symbol in range(3):
        sl = [slice(None)] * 6
        sl[site] = symbol
        sl[site + 3] = symbol
        out[tuple(sl)] = tensor
    return out.reshape(D, D)


def endpoint_operator(c: np.ndarray) -> np.ndarray:
    out = c
    for site in range(3):
        out = out - 0.5 * trace_adjoint_one(
            partial_trace_one(out, site), site
        )
    return out


def orthonormalize(z: np.ndarray) -> np.ndarray:
    q, r = np.linalg.qr(z)
    diagonal = np.diag(r)
    phases = np.where(
        np.abs(diagonal) > 0, diagonal / np.abs(diagonal), 1
    )
    return q * phases.conj()


def fixed_frame_bottom(z: np.ndarray) -> tuple[float, np.ndarray]:
    u, w = z[:, :2], z[:, 2:]
    units = [
        np.outer(u[:, a], w[:, b].conj())
        for a in range(2)
        for b in range(2)
    ]
    gram = np.array(
        [
            [np.vdot(e, endpoint_operator(f)) for f in units]
            for e in units
        ]
    )
    gram = (gram + gram.conj().T) / 2
    values, vectors = np.linalg.eigh(gram)
    return float(values[0]), vectors[:, 0].reshape(2, 2)


def descend(
    z: np.ndarray, steps: int, rate: float
) -> tuple[float, np.ndarray, np.ndarray]:
    best = (np.inf, z.copy(), np.zeros((2, 2), dtype=np.complex128))
    for step in range(steps):
        value, b = fixed_frame_bottom(z)
        if value < best[0]:
            best = (value, z.copy(), b.copy())
        u, w = z[:, :2], z[:, 2:]
        c = u @ b @ w.conj().T
        image = endpoint_operator(c)
        grad_u = 2 * image @ w @ b.conj().T
        grad_w = 2 * image.conj().T @ u @ b
        grad = np.column_stack((grad_u, grad_w))
        tangent = grad - z @ (
            (z.conj().T @ grad + grad.conj().T @ z) / 2
        )
        trial_rate = rate / np.sqrt(1 + step / 100)
        z = orthonormalize(z - trial_rate * tangent)
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=20)
    parser.add_argument("--steps", type=int, default=2000)
    parser.add_argument("--rate", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=20260729)
    parser.add_argument("--output", default="n3_squarezero_q_best.npz")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    global_best = (np.inf, None, None)
    for start in range(args.starts):
        z = orthonormalize(
            rng.normal(size=(D, 4)) + 1j * rng.normal(size=(D, 4))
        )
        best = descend(z, args.steps, args.rate)
        if best[0] < global_best[0]:
            global_best = best
        print(start, best[0], "global", global_best[0], flush=True)

    value, z, b = global_best
    np.savez(args.output, value=value, z=z, b=b)


if __name__ == "__main__":
    main()
