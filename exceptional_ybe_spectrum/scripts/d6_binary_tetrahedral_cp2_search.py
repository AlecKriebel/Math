#!/usr/bin/env python3
"""Search the complete CP^2 branch of the binary-tetrahedral d=6 ansatz.

This is a numerical candidate generator, not a nonexistence proof.

Let A=C^2 be the defining representation of 2T and B=C^3 its tetrahedral
rotation representation.  The 2T-module A tensor B tensor A decomposes as

    1 + 1' + 1'' + 3 + 3 + 3.

Up to taking the complementary eigenspace, every balanced equivariant
involution whose positive eigenspace contains all three singlets is

    K(z) = 2(P_diag + W(z)W(z)^*) - I,       [z] in CP^2,

where W(z) is a rank-three equivariant isometry.  We optimize the complete
four-real-dimensional CP^2, including complex phases, for the shifted cubic
relation with K_1=K tensor I_6 and K_2=I_6 tensor K.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQRT2 = np.sqrt(2.0)

X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=np.complex128)
Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)
EPS = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=np.complex128)


def vec_pair(matrix: np.ndarray) -> np.ndarray:
    return matrix.reshape(4)


def embed_pair_b(pair_state: np.ndarray, b: int) -> np.ndarray:
    out = np.zeros(12, dtype=np.complex128)
    for a in range(2):
        for c in range(2):
            out[(a * 3 + b) * 2 + c] = pair_state[2 * a + c]
    return out


def invariant_isometries():
    singlet = vec_pair(EPS / SQRT2)
    triplet = [vec_pair(pauli @ EPS / SQRT2) for pauli in (X, Y, Z)]
    u0 = np.column_stack([embed_pair_b(singlet, k) for k in range(3)])
    u1_columns = []
    u2_columns = []
    levi = np.zeros((3, 3, 3), dtype=int)
    levi[0, 1, 2] = levi[1, 2, 0] = levi[2, 0, 1] = 1
    levi[0, 2, 1] = levi[2, 1, 0] = levi[1, 0, 2] = -1
    for k in range(3):
        anti = np.zeros(12, dtype=np.complex128)
        sym = np.zeros(12, dtype=np.complex128)
        for p in range(3):
            for b in range(3):
                anti += levi[k, p, b] * embed_pair_b(triplet[p], b) / SQRT2
                if k != p and k != b and p != b:
                    sym += embed_pair_b(triplet[p], b) / SQRT2
        u1_columns.append(anti)
        u2_columns.append(sym)
    u1 = np.column_stack(u1_columns)
    u2 = np.column_stack(u2_columns)
    diag = np.column_stack(
        [embed_pair_b(triplet[k], k) for k in range(3)]
    )
    full = np.column_stack((diag, u0, u1, u2))
    if np.linalg.norm(full.conj().T @ full - np.eye(12)) > 1.0e-13:
        raise RuntimeError("invariant decomposition basis is not unitary")
    return diag, (u0, u1, u2)


P_DIAG, U_COPIES = invariant_isometries()
P_DIAG = P_DIAG @ P_DIAG.conj().T
I6 = np.eye(6, dtype=np.complex128)
I12 = np.eye(12, dtype=np.complex128)


def cp2_coordinates(parameters: np.ndarray):
    theta1, theta2, phi1, phi2 = parameters
    c1, s1 = np.cos(theta1), np.sin(theta1)
    c2, s2 = np.cos(theta2), np.sin(theta2)
    e1, e2 = np.exp(1.0j * phi1), np.exp(1.0j * phi2)
    z = np.array([c1, s1 * c2 * e1, s1 * s2 * e2])
    derivatives = np.array(
        [
            [-s1, c1 * c2 * e1, c1 * s2 * e2],
            [0.0, -s1 * s2 * e1, s1 * c2 * e2],
            [0.0, 1.0j * z[1], 0.0],
            [0.0, 0.0, 1.0j * z[2]],
        ],
        dtype=np.complex128,
    )
    return z, derivatives


def k_and_derivatives(parameters: np.ndarray):
    z, dz = cp2_coordinates(parameters)
    w = sum(z[j] * U_COPIES[j] for j in range(3))
    p = P_DIAG + w @ w.conj().T
    k = 2.0 * p - I12
    derivatives = []
    for direction in dz:
        dw = sum(direction[j] * U_COPIES[j] for j in range(3))
        derivatives.append(2.0 * (dw @ w.conj().T + w @ dw.conj().T))
    return k, derivatives, z


def pullback_1(matrix: np.ndarray) -> np.ndarray:
    return np.einsum("isjs->ij", matrix.reshape(12, 6, 12, 6))


def pullback_2(matrix: np.ndarray) -> np.ndarray:
    return np.einsum("aiaj->ij", matrix.reshape(6, 12, 6, 12))


def objective_gradient(parameters: np.ndarray):
    k, derivatives, _ = k_and_derivatives(parameters)
    k1 = np.kron(k, I6)
    k2 = np.kron(I6, k)
    f = k1 @ k2 @ k1 - k2 @ k1 @ k2 - (k1 - k2) / 3.0
    value = float(np.vdot(f, f).real / 72.0)
    g1 = 2.0 * (
        k2 @ k1 @ f + f @ k1 @ k2 - k2 @ f @ k2 - f / 3.0
    )
    g2 = 2.0 * (
        k1 @ f @ k1 - k1 @ k2 @ f - f @ k2 @ k1 + f / 3.0
    )
    euclidean = pullback_1(g1) + pullback_2(g2)
    gradient = np.asarray(
        [np.vdot(euclidean, dk).real / 72.0 for dk in derivatives]
    )
    return value, gradient


def diagnostics(parameters: np.ndarray):
    k, _, z = k_and_derivatives(parameters)
    k1 = np.kron(k, I6)
    k2 = np.kron(I6, k)
    f = k1 @ k2 @ k1 - k2 @ k1 @ k2 - (k1 - k2) / 3.0
    return {
        "objective_normalized": float(np.vdot(f, f).real / 72.0),
        "residual_frobenius": float(np.linalg.norm(f)),
        "gradient_norm": float(np.linalg.norm(objective_gradient(parameters)[1])),
        "involution_defect": float(np.linalg.norm(k @ k - I12)),
        "hermiticity_defect": float(np.linalg.norm(k - k.conj().T)),
        "trace_real": float(np.trace(k).real),
        "trace_imag": float(np.trace(k).imag),
        "z": [[float(x.real), float(x.imag)] for x in z],
        "parameters": [float(x) for x in parameters],
    }


def random_parameters(rng: np.random.Generator):
    z = rng.normal(size=3) + 1.0j * rng.normal(size=3)
    z /= np.linalg.norm(z)
    z *= np.exp(-1.0j * np.angle(z[0]))
    theta1 = np.arccos(np.clip(abs(z[0]), 0.0, 1.0))
    theta2 = np.arctan2(abs(z[2]), abs(z[1]))
    return np.array(
        [theta1, theta2, np.angle(z[1]), np.angle(z[2])], dtype=float
    )


def emit(event: dict, output: Path | None):
    rendered = json.dumps(event, sort_keys=True)
    print(rendered, flush=True)
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("a", encoding="utf-8") as handle:
            handle.write(rendered + "\n")


def source_sha256():
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def run_gradient_check(seed: int):
    rng = np.random.default_rng(seed)
    parameters = random_parameters(rng)
    value, analytic = objective_gradient(parameters)
    finite = np.zeros(4)
    step = 1.0e-6
    for j in range(4):
        plus = parameters.copy()
        minus = parameters.copy()
        plus[j] += step
        minus[j] -= step
        finite[j] = (
            objective_gradient(plus)[0] - objective_gradient(minus)[0]
        ) / (2.0 * step)
    relative = np.linalg.norm(analytic - finite) / max(
        1.0, np.linalg.norm(analytic), np.linalg.norm(finite)
    )
    print(
        json.dumps(
            {
                "event": "gradient_check",
                "seed": seed,
                "objective_normalized": value,
                "analytic": analytic.tolist(),
                "finite_difference": finite.tolist(),
                "relative_error": float(relative),
                "source_sha256": source_sha256(),
            },
            sort_keys=True,
        )
    )


def run_search(args):
    output = Path(args.output) if args.output else None
    emit(
        {
            "event": "metadata",
            "ansatz": "binary_tetrahedral_CP2_full_complex",
            "seed_start": args.seed_start,
            "seed_end": args.seed_end,
            "max_iterations": args.max_iterations,
            "gradient_tolerance": args.gradient_tolerance,
            "function_tolerance": args.function_tolerance,
            "source_sha256": source_sha256(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "python": sys.version.replace("\n", " "),
            "platform": platform.platform(),
            "unix_time": time.time(),
        },
        output,
    )
    for seed in range(args.seed_start, args.seed_end + 1):
        rng = np.random.default_rng(seed)
        initial = random_parameters(rng)
        started = time.monotonic()
        result = minimize(
            objective_gradient,
            initial,
            method="L-BFGS-B",
            jac=True,
            bounds=[
                (0.0, np.pi / 2.0),
                (0.0, np.pi / 2.0),
                (-np.pi, np.pi),
                (-np.pi, np.pi),
            ],
            options={
                "maxiter": args.max_iterations,
                "gtol": args.gradient_tolerance,
                "ftol": args.function_tolerance,
                "maxls": 100,
            },
        )
        event = {
            "event": "final",
            "seed": seed,
            "success": bool(result.success),
            "status": int(result.status),
            "message": str(result.message),
            "iterations": int(result.nit),
            "function_evaluations": int(result.nfev),
            "elapsed_seconds": time.monotonic() - started,
        }
        event.update(diagnostics(np.asarray(result.x)))
        emit(event, output)
        if event["residual_frobenius"] <= args.candidate_tolerance:
            emit(
                {
                    "event": "candidate_threshold",
                    "seed": seed,
                    "candidate_tolerance": args.candidate_tolerance,
                },
                output,
            )


def parser():
    p = argparse.ArgumentParser()
    p.add_argument("--gradient-check", action="store_true")
    p.add_argument("--seed", type=int, default=26074000)
    p.add_argument("--seed-start", type=int, default=26074001)
    p.add_argument("--seed-end", type=int, default=26074064)
    p.add_argument("--max-iterations", type=int, default=1000)
    p.add_argument("--gradient-tolerance", type=float, default=1.0e-12)
    p.add_argument("--function-tolerance", type=float, default=1.0e-15)
    p.add_argument("--candidate-tolerance", type=float, default=1.0e-10)
    p.add_argument("--output")
    return p


if __name__ == "__main__":
    args = parser().parse_args()
    if args.gradient_check:
        run_gradient_check(args.seed)
    else:
        run_search(args)
