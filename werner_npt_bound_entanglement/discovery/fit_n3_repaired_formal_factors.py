#!/usr/bin/env python3
"""Fit the repaired formal n=3 block Grams by common rank-two factors.

Discovery code only.  The variables are fully complex arrays

    X, Y in C^(3 x 9 x 2),
    C[p,q] = X[p] Y[q]^*.

The residual imposes the exact Hilbert--Schmidt and two-copy endpoint
Gram tables from notes/agent_n3_repaired_formal_one_pauli.md.  A
whitening residual X^*X=I removes the noncompact logical gauge; every
rank-two realization admits that gauge.
"""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import least_squares


def endpoint_two(blocks: np.ndarray) -> np.ndarray:
    """Apply L tensor L to an array of 9-by-9 matrices."""

    lead = blocks.shape[:-2]
    tensor = blocks.reshape(lead + (3, 3, 3, 3))
    out = tensor.copy()

    # L on the first qutrit: subtract I/2 times the simultaneous
    # row/column trace at axes (0,2) of the four physical axes.
    trace_first = np.einsum("...abad->...bd", out)
    adj_first = np.zeros_like(out)
    for symbol in range(3):
        adj_first[..., symbol, :, symbol, :] = trace_first
    out -= 0.5 * adj_first

    # L on the second qutrit.  The first application has already been
    # made, so this composes the two commuting maps.
    trace_second = np.einsum("...abcb->...ac", out)
    adj_second = np.zeros_like(out)
    for symbol in range(3):
        adj_second[..., :, symbol, :, symbol] = trace_second
    out -= 0.5 * adj_second
    return out.reshape(lead + (9, 9))


def target_tables() -> tuple[np.ndarray, np.ndarray]:
    norm = np.eye(9, dtype=np.complex128) / 9.0
    beta = np.zeros((9, 9), dtype=np.complex128)
    for p in range(3):
        for r in range(3):
            beta[3 * p + p, 3 * r + r] = 1.0 / 36.0
    for p in range(3):
        for q in range(3):
            if p != q:
                beta[3 * p + q, 3 * p + q] = 1.0 / 180.0
    return norm, beta


N_TARGET, BETA_TARGET = target_tables()


def unpack(real_variables: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    half = real_variables.size // 2
    complex_variables = (
        real_variables[:half] + 1j * real_variables[half:]
    )
    x = complex_variables[:54].reshape(3, 9, 2)
    y = complex_variables[54:].reshape(3, 9, 2)
    return x, y


def pack(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    values = np.concatenate((x.reshape(-1), y.reshape(-1)))
    return np.concatenate((values.real, values.imag))


def factors_to_tables(
    x: np.ndarray, y: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    blocks = np.einsum("pia,qja->pqij", x, np.conjugate(y))
    flat = blocks.reshape(9, 81)
    norm = np.einsum("ik,jk->ij", np.conjugate(flat), flat)
    image = endpoint_two(blocks).reshape(9, 81)
    beta = np.einsum("ik,jk->ij", np.conjugate(flat), image)
    return norm, beta


def complex_residual(matrix: np.ndarray) -> np.ndarray:
    return np.concatenate((matrix.real.reshape(-1), matrix.imag.reshape(-1)))


NORM_WEIGHT = 1.0
BETA_WEIGHT = 1.0
WHITE_WEIGHT = 0.2
BALANCED_FRAMES = False
ZERO_PAULI = False


def balanced_factors(
    real_variables: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Map four raw 9-by-3 arrays to four orthonormal frames.

    This is the exact H=Z=0, lambda=1/2 slice.  It enforces the target
    ordinary block Gram identically.
    """

    half = real_variables.size // 2
    values = real_variables[:half] + 1j * real_variables[half:]
    raw_frames = values.reshape(2, 9, 6)
    frames = np.asarray([np.linalg.qr(frame)[0] for frame in raw_frames])
    x = np.empty((3, 9, 2), dtype=np.complex128)
    y = np.empty((3, 9, 2), dtype=np.complex128)
    x[:, :, 0] = frames[0, :, :3].T / np.sqrt(3.0)
    x[:, :, 1] = frames[0, :, 3:].T / np.sqrt(3.0)
    y[:, :, 0] = frames[1, :, :3].T / np.sqrt(6.0)
    y[:, :, 1] = frames[1, :, 3:].T / np.sqrt(6.0)
    return x, y


def zero_pauli_factors(
    real_variables: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Exact H=0 ordinary-Gram parametrization.

    The X columns form one orthogonal six-frame.  The two Y column
    triples are separate three-frames and may have arbitrary crossed
    Gram.  The last real variable parametrizes 0 < lambda < 1.
    """

    theta = real_variables[-1]
    lam = 1.0 / (1.0 + np.exp(-theta))
    body = real_variables[:-1]
    half = body.size // 2
    values = body[:half] + 1j * body[half:]
    x_raw = values[:54].reshape(9, 6)
    y0_raw = values[54:81].reshape(9, 3)
    y1_raw = values[81:].reshape(9, 3)
    x_frame = np.linalg.qr(x_raw)[0]
    y0_frame = np.linalg.qr(y0_raw)[0]
    y1_frame = np.linalg.qr(y1_raw)[0]
    x = np.empty((3, 9, 2), dtype=np.complex128)
    y = np.empty((3, 9, 2), dtype=np.complex128)
    x[:, :, 0] = x_frame[:, :3].T / np.sqrt(3.0)
    x[:, :, 1] = x_frame[:, 3:].T / np.sqrt(3.0)
    y[:, :, 0] = np.sqrt(lam / 3.0) * y0_frame.T
    y[:, :, 1] = np.sqrt((1.0 - lam) / 3.0) * y1_frame.T
    return x, y


def residual(real_variables: np.ndarray) -> np.ndarray:
    if ZERO_PAULI:
        x, y = zero_pauli_factors(real_variables)
    elif BALANCED_FRAMES:
        x, y = balanced_factors(real_variables)
    else:
        x, y = unpack(real_variables)
    norm, beta = factors_to_tables(x, y)
    x_flat = x.reshape(27, 2)
    whitening = np.conjugate(x_flat).T @ x_flat - np.eye(2)
    # Equal weights put the two prescribed Gram tables on their natural
    # absolute scale.  Whitening is weighted mildly because it is gauge,
    # not extra physical data.
    return np.concatenate(
        (
            NORM_WEIGHT * complex_residual(norm - N_TARGET),
            BETA_WEIGHT * complex_residual(beta - BETA_TARGET),
            WHITE_WEIGHT * complex_residual(whitening),
        )
    )


def random_start(rng: np.random.Generator) -> np.ndarray:
    if ZERO_PAULI:
        values = rng.normal(size=108) + 1j * rng.normal(size=108)
        body = np.concatenate((values.real, values.imag))
        return np.concatenate((body, np.zeros(1)))
    if BALANCED_FRAMES:
        values = rng.normal(size=(2, 9, 6)) + 1j * rng.normal(
            size=(2, 9, 6)
        )
        values = values.reshape(-1)
        return np.concatenate((values.real, values.imag))
    x = rng.normal(size=(27, 2)) + 1j * rng.normal(size=(27, 2))
    x = np.linalg.qr(x)[0].reshape(3, 9, 2)
    y = rng.normal(size=(3, 9, 2)) + 1j * rng.normal(size=(3, 9, 2))
    # The target full coefficient matrix has norm one.  With whitened X,
    # this asks for ||Y||_HS=1.
    y /= np.linalg.norm(y)
    return pack(x, y)


def diagnostics(real_variables: np.ndarray) -> dict[str, float]:
    if ZERO_PAULI:
        x, y = zero_pauli_factors(real_variables)
    elif BALANCED_FRAMES:
        x, y = balanced_factors(real_variables)
    else:
        x, y = unpack(real_variables)
    norm, beta = factors_to_tables(x, y)
    x_flat = x.reshape(27, 2)
    y_flat = y.reshape(27, 2)
    norm_error = np.linalg.norm(norm - N_TARGET)
    beta_error = np.linalg.norm(beta - BETA_TARGET)
    x_white = np.linalg.norm(np.conjugate(x_flat).T @ x_flat - np.eye(2))
    full = x_flat @ np.conjugate(y_flat).T
    return {
        "residual": float(np.linalg.norm(residual(real_variables))),
        "norm_error": float(norm_error),
        "beta_error": float(beta_error),
        "x_whitening": float(x_white),
        "rank2_singular_1": float(np.linalg.svd(full, compute_uv=False)[0]),
        "rank2_singular_2": float(np.linalg.svd(full, compute_uv=False)[1]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--starts", type=int, default=4)
    parser.add_argument("--max-nfev", type=int, default=300)
    parser.add_argument("--seed", type=int, default=20260730)
    parser.add_argument("--norm-weight", type=float, default=1.0)
    parser.add_argument("--beta-weight", type=float, default=1.0)
    parser.add_argument("--white-weight", type=float, default=0.2)
    parser.add_argument("--balanced-frames", action="store_true")
    parser.add_argument("--zero-pauli", action="store_true")
    parser.add_argument(
        "--output", default="n3_repaired_formal_factor_fit.npz"
    )
    args = parser.parse_args()
    global NORM_WEIGHT, BETA_WEIGHT, WHITE_WEIGHT, BALANCED_FRAMES, ZERO_PAULI
    NORM_WEIGHT = args.norm_weight
    BETA_WEIGHT = args.beta_weight
    WHITE_WEIGHT = args.white_weight
    BALANCED_FRAMES = args.balanced_frames
    ZERO_PAULI = args.zero_pauli

    rng = np.random.default_rng(args.seed)
    best = None
    for start in range(args.starts):
        result = least_squares(
            residual,
            random_start(rng),
            method="trf",
            jac="2-point",
            max_nfev=args.max_nfev,
            verbose=0,
            ftol=1e-13,
            xtol=1e-13,
            gtol=1e-13,
        )
        info = diagnostics(result.x)
        print(start, result.status, result.nfev, info, flush=True)
        if best is None or info["residual"] < best[0]:
            best = (info["residual"], result.x.copy(), info)

    assert best is not None
    np.savez(args.output, variables=best[1], **best[2])
    print("best", best[2])


if __name__ == "__main__":
    main()
