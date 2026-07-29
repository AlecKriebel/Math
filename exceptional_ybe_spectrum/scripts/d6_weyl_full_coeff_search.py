#!/usr/bin/env python3
"""Search the full 19 x 19 real Weyl-coefficient branch at d=6.

Let A_0,...,A_18 be the traceless Hermitian local frame used by the exact
Weyl cubic near-miss.  This script searches

    H(C) = sum_{i,j=0}^{18} C[i,j] A_i tensor A_j,   C in M_19(R).

Thus H(C) is automatically Hermitian, traceless, and has zero partial trace
on either local leg.  Unlike ``d6_weyl_pairing_deformation.py``, neither the
singular values nor either Schmidt frame is fixed.

This is a numerical falsifier/discovery calculation.  A small residual is
not a proof and must be exactified and independently verified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import scipy
from scipy import optimize


D = 6
FRAME_SIZE = 19
TARGET_HS_NORM = float(D)


def matrix_units_hermitian_basis(size: int) -> list[np.ndarray]:
    """Return a deterministic Hilbert--Schmidt orthonormal Hermitian basis."""
    basis: list[np.ndarray] = []
    for row in range(size):
        diagonal = np.zeros((size, size), dtype=np.complex128)
        diagonal[row, row] = 1
        basis.append(diagonal)
    for row in range(size):
        for column in range(row + 1, size):
            symmetric = np.zeros((size, size), dtype=np.complex128)
            symmetric[row, column] = symmetric[column, row] = 1 / np.sqrt(2)
            antisymmetric = np.zeros((size, size), dtype=np.complex128)
            antisymmetric[row, column] = -1j / np.sqrt(2)
            antisymmetric[column, row] = 1j / np.sqrt(2)
            basis.extend((symmetric, antisymmetric))
    assert len(basis) == size * size
    return basis


def retained_weyl_frame() -> list[np.ndarray]:
    """Build the nineteen traceless Hermitian local directions."""
    x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    z = np.diag([1, -1]).astype(np.complex128)
    qutrit_basis = matrix_units_hermitian_basis(3)
    frame = [np.kron(z / np.sqrt(2), q) for q in qutrit_basis]
    frame.extend(np.kron(x / np.sqrt(2), q) for q in qutrit_basis)
    frame.append(np.kron(y, np.eye(3)) / np.sqrt(6))
    gram = np.array(
        [[np.trace(a.conj().T @ b) for b in frame] for a in frame]
    )
    assert len(frame) == FRAME_SIZE
    assert np.linalg.norm(gram - np.eye(FRAME_SIZE)) < 1e-12
    assert max(abs(np.trace(a)) for a in frame) < 1e-12
    return frame


@dataclass
class FullCoefficientModel:
    frame: list[np.ndarray]
    tensor_basis: np.ndarray
    identity_six: np.ndarray
    identity_thirty_six: np.ndarray

    @classmethod
    def build(cls) -> "FullCoefficientModel":
        frame = retained_weyl_frame()
        tensor_basis = np.empty(
            (FRAME_SIZE * FRAME_SIZE, D * D, D * D),
            dtype=np.complex128,
        )
        index = 0
        for left in range(FRAME_SIZE):
            for right in range(FRAME_SIZE):
                tensor_basis[index] = np.kron(frame[left], frame[right])
                index += 1
        flat_gram = np.einsum(
            "kab,lab->kl",
            tensor_basis.conj(),
            tensor_basis,
            optimize=True,
        )
        assert np.linalg.norm(
            flat_gram - np.eye(FRAME_SIZE * FRAME_SIZE)
        ) < 1e-11
        return cls(
            frame=frame,
            tensor_basis=tensor_basis,
            identity_six=np.eye(D, dtype=np.complex128),
            identity_thirty_six=np.eye(D * D, dtype=np.complex128),
        )

    @staticmethod
    def h0_coefficients() -> np.ndarray:
        coefficients = np.zeros((FRAME_SIZE, FRAME_SIZE), dtype=np.float64)
        coefficients[np.arange(18), np.arange(18)] = 2 / np.sqrt(3)
        coefficients[18, 18] = 2 * np.sqrt(3)
        return coefficients

    @staticmethod
    def anticommuting_product_coefficients() -> np.ndarray:
        """Coefficients of (Z tensor I_3) tensor (X tensor I_3)."""
        coefficients = np.zeros((FRAME_SIZE, FRAME_SIZE), dtype=np.float64)
        # In the matrix-unit qutrit basis, Z tensor I_3 has coefficient
        # sqrt(2) on the first three Z-block directions; similarly for X.
        coefficients[0:3, 9:12] = 2
        assert abs(np.linalg.norm(coefficients) - TARGET_HS_NORM) < 1e-12
        return coefficients

    def h_from_coefficients(self, coefficients: np.ndarray) -> np.ndarray:
        return np.einsum(
            "k,kab->ab",
            coefficients.reshape(-1),
            self.tensor_basis,
            optimize=True,
        )

    @staticmethod
    def partial_trace_last(matrix: np.ndarray) -> np.ndarray:
        six_indices = matrix.reshape(D, D, D, D, D, D)
        return np.einsum("abcABc->abAB", six_indices).reshape(D * D, D * D)

    @staticmethod
    def partial_trace_first(matrix: np.ndarray) -> np.ndarray:
        six_indices = matrix.reshape(D, D, D, D, D, D)
        return np.einsum("abcaBC->bcBC", six_indices).reshape(D * D, D * D)

    def residuals(
        self, coefficients: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        h = self.h_from_coefficients(coefficients)
        involution = h @ h - self.identity_thirty_six
        h_one = np.kron(h, self.identity_six)
        h_two = np.kron(self.identity_six, h)
        cubic = (
            h_one @ h_two @ h_one
            - h_two @ h_one @ h_two
            - (h_one - h_two) / 3
        )
        return h, involution, cubic

    def objective_and_gradient(
        self,
        flat_coefficients: np.ndarray,
        cubic_weight: float,
    ) -> tuple[float, np.ndarray, dict[str, float]]:
        coefficients = flat_coefficients.reshape(FRAME_SIZE, FRAME_SIZE)
        h, involution, cubic = self.residuals(coefficients)
        involution_sq = float(np.vdot(involution, involution).real)
        cubic_sq = float(np.vdot(cubic, cubic).real)
        involution_objective = involution_sq / (D * D)
        cubic_objective = cubic_sq / (D**3)
        objective = involution_objective + cubic_weight * cubic_objective

        # Frobenius adjoint derivative of ||H^2-I||_F^2.
        gradient_h = (
            2 * (h @ involution + involution @ h) / (D * D)
        )

        if cubic_weight:
            h_one = np.kron(h, self.identity_six)
            h_two = np.kron(self.identity_six, h)

            # Adjoint derivatives with respect to H_1 and H_2.
            adjoint_one = (
                cubic @ h_one @ h_two
                + h_two @ h_one @ cubic
                - h_two @ cubic @ h_two
                - cubic / 3
            )
            adjoint_two = (
                h_one @ cubic @ h_one
                - cubic @ h_two @ h_one
                - h_one @ h_two @ cubic
                + cubic / 3
            )
            scale = 2 * cubic_weight / (D**3)
            gradient_h += scale * self.partial_trace_last(adjoint_one)
            gradient_h += scale * self.partial_trace_first(adjoint_two)

        gradient = np.einsum(
            "ab,kab->k",
            gradient_h.conj(),
            self.tensor_basis,
            optimize=True,
        ).real
        diagnostics = {
            "objective": float(objective),
            "involution_objective": float(involution_objective),
            "cubic_objective": float(cubic_objective),
            "involution_norm": float(np.sqrt(involution_sq)),
            "cubic_norm": float(np.sqrt(cubic_sq)),
            "gradient_norm": float(np.linalg.norm(gradient)),
            "coefficient_norm": float(np.linalg.norm(flat_coefficients)),
            "trace_h_real": float(np.trace(h).real),
            "trace_h_imag": float(np.trace(h).imag),
            "hermiticity_norm": float(np.linalg.norm(h - h.conj().T)),
        }
        return float(objective), gradient, diagnostics

    def final_diagnostics(self, coefficients: np.ndarray) -> dict[str, object]:
        h, involution, cubic = self.residuals(coefficients)
        eigenvalues = np.linalg.eigvalsh(h)
        singular_values = np.linalg.svd(coefficients, compute_uv=False)
        block_norms = [
            [
                float(np.linalg.norm(coefficients[rows, columns]))
                for columns in (slice(0, 9), slice(9, 18), slice(18, 19))
            ]
            for rows in (slice(0, 9), slice(9, 18), slice(18, 19))
        ]
        return {
            "involution_norm": float(np.linalg.norm(involution)),
            "cubic_norm": float(np.linalg.norm(cubic)),
            "trace_h": [float(np.trace(h).real), float(np.trace(h).imag)],
            "hermiticity_norm": float(np.linalg.norm(h - h.conj().T)),
            "coefficient_norm": float(np.linalg.norm(coefficients)),
            "coefficient_rank_tolerance_1e-8": int(
                np.sum(singular_values > 1e-8)
            ),
            "coefficient_singular_values": [float(x) for x in singular_values],
            "coefficient_symmetry_norm": float(
                np.linalg.norm(coefficients - coefficients.T)
            ),
            "coefficient_block_norms_z_x_y": block_norms,
            "h_eigenvalue_min": float(eigenvalues[0]),
            "h_eigenvalue_max": float(eigenvalues[-1]),
            "h_eigenvalue_near_minus_one": int(
                np.sum(np.abs(eigenvalues + 1) < 1e-6)
            ),
            "h_eigenvalue_near_plus_one": int(
                np.sum(np.abs(eigenvalues - 1) < 1e-6)
            ),
            "h_eigenvalues": [float(x) for x in eigenvalues],
        }


def initialize_coefficients(
    model: FullCoefficientModel,
    rng: np.random.Generator,
    initialization: str,
    noise_scale: float,
    mix_fraction: float,
) -> np.ndarray:
    if initialization == "random":
        coefficients = rng.normal(size=(FRAME_SIZE, FRAME_SIZE))
        coefficients *= TARGET_HS_NORM / np.linalg.norm(coefficients)
        return coefficients
    if initialization == "h0_noise":
        perturbation = rng.normal(size=(FRAME_SIZE, FRAME_SIZE))
        perturbation *= (
            noise_scale * TARGET_HS_NORM / np.linalg.norm(perturbation)
        )
        coefficients = model.h0_coefficients() + perturbation
        coefficients *= TARGET_HS_NORM / np.linalg.norm(coefficients)
        return coefficients
    if initialization == "mix_h0_anti":
        coefficients = (
            mix_fraction * model.h0_coefficients()
            + (1 - mix_fraction)
            * model.anticommuting_product_coefficients()
        )
        perturbation = rng.normal(size=(FRAME_SIZE, FRAME_SIZE))
        perturbation *= (
            noise_scale * TARGET_HS_NORM / np.linalg.norm(perturbation)
        )
        coefficients += perturbation
        coefficients *= TARGET_HS_NORM / np.linalg.norm(coefficients)
        return coefficients
    raise ValueError(f"unknown initialization {initialization!r}")


def optimize_schedule(
    model: FullCoefficientModel,
    coefficients: np.ndarray,
    weights: list[float],
    max_iterations_per_stage: int,
) -> tuple[np.ndarray, list[dict[str, object]]]:
    stages: list[dict[str, object]] = []
    flat = coefficients.reshape(-1).copy()

    for stage_index, cubic_weight in enumerate(weights):
        stage_started = time.time()
        objective_calls = 0

        def evaluate(x: np.ndarray) -> tuple[float, np.ndarray]:
            nonlocal objective_calls
            objective_calls += 1
            objective, gradient, _ = model.objective_and_gradient(
                x, cubic_weight
            )
            return objective, gradient

        initial_objective, _, initial_diagnostics = (
            model.objective_and_gradient(flat, cubic_weight)
        )
        result = optimize.minimize(
            evaluate,
            flat,
            method="L-BFGS-B",
            jac=True,
            options={
                "maxiter": max_iterations_per_stage,
                "maxls": 40,
                "maxcor": 30,
                "ftol": 1e-15,
                "gtol": 1e-10,
            },
        )
        flat = np.asarray(result.x, dtype=np.float64)
        final_objective, _, final_diagnostics = (
            model.objective_and_gradient(flat, cubic_weight)
        )
        stages.append(
            {
                "stage_index": stage_index,
                "cubic_weight": cubic_weight,
                "initial_objective": float(initial_objective),
                "initial_diagnostics": initial_diagnostics,
                "final_objective": float(final_objective),
                "final_diagnostics": final_diagnostics,
                "iterations": int(result.nit),
                "function_gradient_calls": objective_calls,
                "status": int(result.status),
                "success": bool(result.success),
                "message": str(result.message),
                "elapsed_seconds": time.time() - stage_started,
            }
        )
    return flat.reshape(FRAME_SIZE, FRAME_SIZE), stages


def append_json_line(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument(
        "--initialization",
        choices=("random", "h0_noise", "mix_h0_anti"),
        required=True,
    )
    parser.add_argument("--noise-scale", type=float, default=0.25)
    parser.add_argument("--mix-fraction", type=float, default=0.5)
    parser.add_argument(
        "--weights",
        type=str,
        required=True,
        help="comma-separated continuation schedule of cubic weights",
    )
    parser.add_argument("--max-iterations-per-stage", type=int, default=300)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    weights = [float(item) for item in args.weights.split(",")]
    if not weights or any(weight < 0 for weight in weights):
        raise ValueError("weights must be a nonempty list of nonnegative values")

    model = FullCoefficientModel.build()
    rng = np.random.default_rng(args.seed)
    initial = initialize_coefficients(
        model,
        rng,
        initialization=args.initialization,
        noise_scale=args.noise_scale,
        mix_fraction=args.mix_fraction,
    )
    initial_diagnostics = model.final_diagnostics(initial)
    started = time.time()
    coefficients, stages = optimize_schedule(
        model,
        initial,
        weights=weights,
        max_iterations_per_stage=args.max_iterations_per_stage,
    )
    payload: dict[str, object] = {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "command": sys.argv,
        "seed": args.seed,
        "initialization": args.initialization,
        "noise_scale": args.noise_scale,
        "mix_fraction": args.mix_fraction,
        "weights": weights,
        "max_iterations_per_stage": args.max_iterations_per_stage,
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "platform": platform.platform(),
        "script_sha256": hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        "elapsed_seconds": time.time() - started,
        "initial": initial_diagnostics,
        "stages": stages,
        "final": model.final_diagnostics(coefficients),
        "coefficient_matrix": coefficients.tolist(),
        "coefficient_sha256_little_endian_float64": hashlib.sha256(
            coefficients.astype("<f8").tobytes()
        ).hexdigest(),
        "warning": (
            "Numerical exploration only. A small residual is not proof; "
            "it must be exactified and independently verified."
        ),
    }
    append_json_line(args.output, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
