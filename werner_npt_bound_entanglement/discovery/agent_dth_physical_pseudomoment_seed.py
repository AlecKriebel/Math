#!/usr/bin/env python3
"""Unrestricted complex physical search for the deflated Hodge inequality.

This is discovery code.  A physical point is represented by a complex
orthonormal frame ``U=(u0,u1)`` in ``H=(C^3)^tensor3``.  Its normalized
decomposable bivector and skew matrix are

    w = u0 wedge u1,
    W = (u0 u1^T-u1 u0^T)/sqrt(2).

For fixed ``U`` the support and Omega equations are linear in ``z``:

    U^* z = 0,
    g_U^T z = 0,
    (g_U)_j = Tr(D_{e_j} W).

The script eliminates ``z`` exactly at floating-point level by taking the
top eigenvector of the Hodge Gram matrix on this common kernel.  It then
maximizes

    ||D_z W||_2^2

over the complex Grassmannian.  The analytic horizontal gradient includes
the Lagrange multipliers of both eliminated constraints and is audited by a
central finite difference before any search.

The default seed is the best member of the deterministic 27-atom physical
ensemble found by overlap with the exact complete-PPT pseudomoment in a
separate invariant-coordinate scan.  That seed is stored in
``/tmp/dth_physical_seed_finite.npz``.  Random complex starts are completely
unrestricted.  Numerical output is not an exact DTH theorem or witness.
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path

import numpy as np
import scipy.linalg as la


DIMENSION = 27
TARGET = 1.0 / 8.0


def epsilon(p: int, a: int, i: int) -> int:
    positive = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    negative = ((0, 2, 1), (2, 1, 0), (1, 0, 2))
    value = (p, a, i)
    return int(value in positive) - int(value in negative)


def hodge_basis() -> np.ndarray:
    local = np.asarray([
        [
            [epsilon(p, a, i) / np.sqrt(2.0) for i in range(3)]
            for a in range(3)
        ]
        for p in range(3)
    ])
    return np.asarray([
        np.kron(np.kron(local[p], local[q]), local[r])
        for p, q, r in itertools.product(range(3), repeat=3)
    ])


HODGE = hodge_basis()
IDENTITY = np.eye(DIMENSION)


def retract(frame: np.ndarray) -> np.ndarray:
    """QR retraction with a deterministic diagonal phase convention."""
    q, r = np.linalg.qr(frame)
    diagonal = np.diag(r)
    phases = np.where(np.abs(diagonal) > 0, diagonal / np.abs(diagonal), 1)
    return q * phases.conj()


def projected_data(frame: np.ndarray, want_gradient: bool = True):
    """Return the constrained top value, vector, and horizontal gradient.

    If ``Y[j,:,a]=D_j u_a``, then

        G[j,k] = (1/2) sum_a <D_j u_a,D_k u_a>

    satisfies ``z^*Gz=||D_zW||_2^2``.  The third constraint column is
    normalized when nonzero; this removes the artificial conditioning loss
    as the cofactor vector tends to zero.
    """
    images = np.einsum("jab,bc->jac", HODGE, frame, optimize=True)
    gram = 0.5 * np.einsum(
        "jal,kal->jk", images.conj(), images, optimize=True
    )
    cofactor = np.sqrt(2.0) * np.einsum(
        "a,ja->j", frame[:, 1], images[:, :, 0], optimize=True
    )
    cofactor_norm = la.norm(cofactor)
    if cofactor_norm > 1.0e-10:
        constraints = np.column_stack(
            (frame, np.conj(cofactor) / cofactor_norm)
        )
    else:
        constraints = frame
    kernel = la.null_space(constraints.conj().T, rcond=2.0e-12)
    compressed = kernel.conj().T @ gram @ kernel
    values, vectors = la.eigh(
        compressed,
        subset_by_index=[compressed.shape[0] - 1, compressed.shape[0] - 1],
    )
    value = float(values[0])
    z = kernel @ vectors[:, 0]
    if not want_gradient:
        return value, z, cofactor

    residual = gram @ z - value * z
    multipliers = la.lstsq(
        constraints, residual, cond=1.0e-12
    )[0]
    hodge = np.tensordot(z, HODGE, axes=1)
    gradient = (hodge.conj().T @ hodge) @ frame / 2.0
    gradient[:, 0] -= np.conj(multipliers[0]) * z
    gradient[:, 1] -= np.conj(multipliers[1]) * z
    if cofactor_norm > 1.0e-10:
        omega_multiplier = multipliers[2] / cofactor_norm
        gradient[:, 0] += (
            np.sqrt(2.0) * omega_multiplier
            * np.conj(hodge @ frame[:, 1])
        )
        gradient[:, 1] -= (
            np.sqrt(2.0) * omega_multiplier
            * np.conj(hodge @ frame[:, 0])
        )
    gradient = (IDENTITY - frame @ frame.conj().T) @ gradient
    multiplier_error = la.norm(
        residual - constraints @ multipliers
    )
    return value, z, cofactor, gradient, multiplier_error


def real_inner(left: np.ndarray, right: np.ndarray) -> float:
    return float(2.0 * np.vdot(left, right).real)


def finite_difference_audit(frame: np.ndarray, rng) -> None:
    value, _, _, gradient, _ = projected_data(frame, True)
    direction = (
        rng.standard_normal(frame.shape)
        + 1j * rng.standard_normal(frame.shape)
    )
    direction = (IDENTITY - frame @ frame.conj().T) @ direction
    direction /= la.norm(direction)
    predicted = real_inner(gradient, direction)
    step = 1.0e-5
    plus = projected_data(retract(frame + step * direction), False)[0]
    minus = projected_data(retract(frame - step * direction), False)[0]
    observed = (plus - minus) / (2.0 * step)
    error = abs(predicted - observed)
    if error > 2.0e-7 * max(1.0, abs(predicted), abs(observed)):
        raise AssertionError(
            f"gradient audit failed: {predicted=} {observed=} {error=}"
        )
    print(
        "gradient audit:",
        f"value={value:.12g}",
        f"predicted={predicted:.12g}",
        f"observed={observed:.12g}",
    )


def ascend(frame: np.ndarray, iterations: int):
    """Riemannian Polak--Ribiere ascent with Armijo retraction search."""
    value, z, cofactor, gradient, _ = projected_data(frame, True)
    direction = gradient.copy()
    step = 8.0
    for iteration in range(iterations):
        norm = la.norm(gradient)
        if norm < 2.0e-10:
            break
        slope = real_inner(gradient, direction)
        if slope <= 0:
            direction = gradient.copy()
            slope = real_inner(gradient, direction)
        trial = step
        for _ in range(32):
            candidate = retract(frame + trial * direction)
            candidate_value = projected_data(candidate, False)[0]
            if candidate_value >= value + 1.0e-4 * trial * slope:
                break
            trial *= 0.5
        else:
            break

        old_frame = frame
        old_gradient = gradient
        frame = candidate
        value, z, cofactor, gradient, _ = projected_data(frame, True)
        projector = IDENTITY - frame @ frame.conj().T
        transported_gradient = projector @ old_gradient
        transported_direction = projector @ direction
        denominator = max(real_inner(old_gradient, old_gradient), 1.0e-30)
        beta = max(
            0.0,
            real_inner(
                gradient, gradient - transported_gradient
            ) / denominator,
        )
        direction = gradient + beta * transported_direction
        step = min(100.0, 1.4 * trial)
    return {
        "value": value,
        "frame": frame,
        "z": z,
        "cofactor": cofactor,
        "iterations": iteration + 1,
        "gradient_norm": la.norm(gradient),
    }


def random_frame(rng) -> np.ndarray:
    return retract(
        rng.standard_normal((DIMENSION, 2))
        + 1j * rng.standard_normal((DIMENSION, 2))
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260801)
    parser.add_argument("--starts", type=int, default=12)
    parser.add_argument("--iterations", type=int, default=800)
    parser.add_argument(
        "--physical-seed", default="/tmp/dth_physical_seed_finite.npz"
    )
    parser.add_argument(
        "--output", default="/tmp/dth_physical_unrestricted_best.npz"
    )
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    seeds = []
    if Path(args.physical_seed).exists():
        seeds.append(("pseudomoment_atom", np.load(args.physical_seed)["U"]))
    seeds.extend(
        (f"random_{index}", random_frame(rng))
        for index in range(args.starts)
    )
    finite_difference_audit(random_frame(rng), rng)
    best = None
    for name, frame in seeds:
        initial = projected_data(frame, False)[0]
        result = ascend(frame, args.iterations)
        value = result["value"]
        z = result["z"]
        support = la.norm(result["frame"].conj().T @ z)
        omega = abs(np.dot(result["cofactor"], z))
        print(
            name,
            f"initial={initial:.12g}",
            f"value={value:.15g}",
            f"deficit={TARGET-value:.8g}",
            f"iterations={result['iterations']}",
            f"gradient={result['gradient_norm']:.3g}",
            f"cofactor={la.norm(result['cofactor']):.3g}",
            f"support={support:.3g}",
            f"omega={omega:.3g}",
            flush=True,
        )
        if best is None or value > best[1]["value"]:
            best = (name, result)
    assert best is not None
    name, result = best
    np.savez(
        args.output,
        name=np.asarray(name),
        value=np.asarray(result["value"]),
        deficit=np.asarray(TARGET - result["value"]),
        U=result["frame"],
        z=result["z"],
        cofactor=result["cofactor"],
        gradient_norm=np.asarray(result["gradient_norm"]),
    )
    print(
        "best:", name,
        f"value={result['value']:.17g}",
        f"deficit={TARGET-result['value']:.17g}",
        "saved", args.output,
    )


if __name__ == "__main__":
    main()
