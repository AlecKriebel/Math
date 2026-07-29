#!/usr/bin/env python3
"""Explore right-frame deformations of the exact d=6 Weyl cubic solution.

The exact starting point is

    H0 = (YY + (XX + ZZ) F3) / sqrt(3),

after grouping the two qubit factors before the two qutrit factors.  In
operator-Schmidt form it has eighteen equal singular values 2/sqrt(3) and
one singular value 2*sqrt(3).  This script holds the left Schmidt frame and
the singular values fixed while replacing the right frame by O in O(19).

This is a falsifier/discovery calculation.  Numerical residuals are never
treated as proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np
import scipy
from scipy import linalg, sparse


D = 6
N_SCHMIDT = 19
DEFAULT_SEED = 26073401


def matrix_units_hermitian_basis(size: int) -> list[np.ndarray]:
    """Return a deterministic HS-orthonormal Hermitian basis of M_size."""
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


def schmidt_data() -> tuple[list[np.ndarray], np.ndarray]:
    """Build the 19 Hermitian Schmidt directions in a transparent basis."""
    x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    z = np.diag([1, -1]).astype(np.complex128)
    qutrit_basis = matrix_units_hermitian_basis(3)
    operators = [
        np.kron(z / np.sqrt(2), qutrit) for qutrit in qutrit_basis
    ]
    operators.extend(
        np.kron(x / np.sqrt(2), qutrit) for qutrit in qutrit_basis
    )
    operators.append(np.kron(y, np.eye(3)) / np.sqrt(6))
    singular_values = np.array(
        [2 / np.sqrt(3)] * 18 + [2 * np.sqrt(3)],
        dtype=np.float64,
    )
    gram = np.array(
        [
            [np.trace(first.conj().T @ second) for second in operators]
            for first in operators
        ]
    )
    assert np.linalg.norm(gram - np.eye(N_SCHMIDT)) < 1e-12
    return operators, singular_values


@dataclass
class PairingModel:
    operators: list[np.ndarray]
    singular_values: np.ndarray
    tensor_basis: np.ndarray
    identity_six: np.ndarray
    identity_thirty_six: np.ndarray

    @classmethod
    def build(cls) -> "PairingModel":
        operators, singular_values = schmidt_data()
        tensor_basis = np.empty(
            (N_SCHMIDT, N_SCHMIDT, D * D, D * D),
            dtype=np.complex128,
        )
        for left in range(N_SCHMIDT):
            for right in range(N_SCHMIDT):
                tensor_basis[left, right] = np.kron(
                    operators[left], operators[right]
                )
        return cls(
            operators=operators,
            singular_values=singular_values,
            tensor_basis=tensor_basis,
            identity_six=np.eye(D, dtype=np.complex128),
            identity_thirty_six=np.eye(D * D, dtype=np.complex128),
        )

    def h_from_pairing(self, orthogonal: np.ndarray) -> np.ndarray:
        # B_i = sum_j O_{j,i} A_j.
        return np.einsum(
            "i,ji,ijab->ab",
            self.singular_values,
            orthogonal,
            self.tensor_basis,
            optimize=True,
        )

    def residuals(
        self, orthogonal: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        h = self.h_from_pairing(orthogonal)
        involution = h @ h - self.identity_thirty_six
        h_one = np.kron(h, self.identity_six)
        h_two = np.kron(self.identity_six, h)
        cubic = (
            h_one @ h_two @ h_one
            - h_two @ h_one @ h_two
            - (h_one - h_two) / 3
        )
        return h, involution, cubic

    def objective_and_euclidean_gradient(
        self,
        orthogonal: np.ndarray,
        cubic_weight: float,
    ) -> tuple[float, np.ndarray, dict[str, float]]:
        h, involution, cubic = self.residuals(orthogonal)
        involution_sq = float(np.vdot(involution, involution).real)
        cubic_sq = float(np.vdot(cubic, cubic).real)
        objective = involution_sq / (D * D)
        objective += cubic_weight * cubic_sq / (D**3)

        # Adjoint derivative of ||H^2-I||_F^2.
        gradient_h = 2 * (
            h @ involution + involution @ h
        ) / (D * D)

        if cubic_weight:
            h_one = np.kron(h, self.identity_six)
            h_two = np.kron(self.identity_six, h)
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
            adjoint_one *= 2 * cubic_weight / (D**3)
            adjoint_two *= 2 * cubic_weight / (D**3)
            first_six = adjoint_one.reshape(D, D, D, D, D, D)
            second_six = adjoint_two.reshape(D, D, D, D, D, D)
            gradient_h += np.einsum("abcABc->abAB", first_six).reshape(
                D * D, D * D
            )
            gradient_h += np.einsum("abcaBC->bcBC", second_six).reshape(
                D * D, D * D
            )

        gradient_orthogonal = np.empty(
            (N_SCHMIDT, N_SCHMIDT), dtype=np.float64
        )
        for left in range(N_SCHMIDT):
            for right in range(N_SCHMIDT):
                gradient_orthogonal[right, left] = (
                    self.singular_values[left]
                    * np.vdot(
                        gradient_h,
                        self.tensor_basis[left, right],
                    ).real
                )
        diagnostics = {
            "objective": objective,
            "involution_norm": float(np.sqrt(involution_sq)),
            "cubic_norm": float(np.sqrt(cubic_sq)),
            "trace_h_real": float(np.trace(h).real),
            "trace_h_imag": float(np.trace(h).imag),
            "hermiticity_norm": float(np.linalg.norm(h - h.conj().T)),
        }
        return objective, gradient_orthogonal, diagnostics


def tangent_cubic_matrix(model: PairingModel) -> tuple[np.ndarray, list[tuple[int, int]]]:
    """Linearize the cubic residual along all real O(19) tangents at I."""
    orthogonal = np.eye(N_SCHMIDT)
    h, _, _ = model.residuals(orthogonal)
    h_sparse = sparse.csr_matrix(h)
    identity_sparse = sparse.eye(D, format="csr", dtype=np.complex128)
    h_one = sparse.kron(h_sparse, identity_sparse, format="csr")
    h_two = sparse.kron(identity_sparse, h_sparse, format="csr")
    sparse_operators = [sparse.csr_matrix(a) for a in model.operators]

    columns: list[np.ndarray] = []
    pairs = list(combinations(range(N_SCHMIDT), 2))
    for first, second in pairs:
        delta_h = (
            model.singular_values[first]
            * sparse.kron(
                sparse_operators[first],
                sparse_operators[second],
                format="csr",
            )
            - model.singular_values[second]
            * sparse.kron(
                sparse_operators[second],
                sparse_operators[first],
                format="csr",
            )
        )
        delta_one = sparse.kron(delta_h, identity_sparse, format="csr")
        delta_two = sparse.kron(identity_sparse, delta_h, format="csr")
        derivative = (
            delta_one @ h_two @ h_one
            + h_one @ delta_two @ h_one
            + h_one @ h_two @ delta_one
            - delta_two @ h_one @ h_two
            - h_two @ delta_one @ h_two
            - h_two @ h_one @ delta_two
            - (delta_one - delta_two) / 3
        )
        columns.append(derivative.toarray().reshape(-1))
    return np.stack(columns, axis=1), pairs


def run_tangent(model: PairingModel) -> dict[str, object]:
    started = time.time()
    jacobian, pairs = tangent_cubic_matrix(model)
    # Coefficients are real, so the real Gram matrix is Re(J^*J).
    gram = np.real(jacobian.conj().T @ jacobian)
    eigenvalues, eigenvectors = np.linalg.eigh(gram)
    eigenvalues[np.abs(eigenvalues) < 1e-12] = 0
    singular_values = np.sqrt(np.maximum(eigenvalues, 0))
    tolerance = 1e-8
    nullity = int(np.sum(singular_values < tolerance))

    pair_classes = {
        "within_z_block": [],
        "within_x_block": [],
        "cross_z_x": [],
        "involving_y_identity": [],
    }
    for column, (first, second) in enumerate(pairs):
        if second == 18:
            pair_classes["involving_y_identity"].append(column)
        elif first < 9 and second < 9:
            pair_classes["within_z_block"].append(column)
        elif first >= 9 and second >= 9:
            pair_classes["within_x_block"].append(column)
        else:
            pair_classes["cross_z_x"].append(column)

    column_norms = np.linalg.norm(jacobian, axis=0)
    class_norms = {
        name: {
            "count": len(indices),
            "minimum": float(np.min(column_norms[indices])),
            "maximum": float(np.max(column_norms[indices])),
        }
        for name, indices in pair_classes.items()
    }
    null_vectors = eigenvectors[:, :nullity]
    null_energy = {
        name: float(np.sum(np.abs(null_vectors[indices, :]) ** 2))
        for name, indices in pair_classes.items()
    }
    _, involution, _ = model.residuals(np.eye(N_SCHMIDT))
    involution_columns: list[np.ndarray] = []
    for first, second in pairs:
        delta_h = (
            model.singular_values[first]
            * model.tensor_basis[first, second]
            - model.singular_values[second]
            * model.tensor_basis[second, first]
        )
        involution_columns.append(
            (model.h_from_pairing(np.eye(N_SCHMIDT)) @ delta_h
             + delta_h @ model.h_from_pairing(np.eye(N_SCHMIDT))).reshape(-1)
        )
    involution_jacobian = np.stack(involution_columns, axis=1)
    involution_gradient = 2 * np.real(
        involution_jacobian.conj().T @ involution.reshape(-1)
    )

    pair_to_column = {pair: column for column, pair in enumerate(pairs)}
    expected_u_nine_vectors: list[np.ndarray] = []
    # Realification of u(9): [[A,-B],[B,A]], with A real skew and B
    # real symmetric.  The nineteenth (Y tensor identity) direction is fixed.
    for first in range(9):
        for second in range(first + 1, 9):
            vector = np.zeros(len(pairs))
            vector[pair_to_column[(first, second)]] = 1
            vector[pair_to_column[(9 + first, 9 + second)]] = 1
            expected_u_nine_vectors.append(vector)
    for first in range(9):
        for second in range(first, 9):
            vector = np.zeros(len(pairs))
            if first == second:
                vector[pair_to_column[(first, 9 + second)]] = 1
            else:
                vector[pair_to_column[(first, 9 + second)]] = 1
                vector[pair_to_column[(second, 9 + first)]] = 1
            expected_u_nine_vectors.append(vector)
    expected_u_nine = np.stack(expected_u_nine_vectors, axis=1)
    expected_u_nine_rank = int(np.linalg.matrix_rank(expected_u_nine))
    expected_derivative_norms = np.linalg.norm(
        jacobian @ expected_u_nine, axis=0
    )

    rng = np.random.default_rng(DEFAULT_SEED)
    finite_u_nine_samples: list[dict[str, float]] = []
    for _ in range(3):
        random_complex = rng.normal(size=(9, 9)) + 1j * rng.normal(
            size=(9, 9)
        )
        unitary, _ = np.linalg.qr(random_complex)
        realification = np.zeros((N_SCHMIDT, N_SCHMIDT))
        realification[:9, :9] = unitary.real
        realification[:9, 9:18] = -unitary.imag
        realification[9:18, :9] = unitary.imag
        realification[9:18, 9:18] = unitary.real
        realification[18, 18] = 1
        _, sample_involution, sample_cubic = model.residuals(realification)
        finite_u_nine_samples.append(
            {
                "involution_norm": float(np.linalg.norm(sample_involution)),
                "cubic_norm": float(np.linalg.norm(sample_cubic)),
            }
        )

    phase = np.exp(0.731j)
    phase_realification = np.zeros((N_SCHMIDT, N_SCHMIDT))
    phase_realification[:9, :9] = phase.real * np.eye(9)
    phase_realification[:9, 9:18] = -phase.imag * np.eye(9)
    phase_realification[9:18, :9] = phase.imag * np.eye(9)
    phase_realification[9:18, 9:18] = phase.real * np.eye(9)
    phase_realification[18, 18] = 1
    _, phase_involution, phase_cubic = model.residuals(
        phase_realification
    )

    return {
        "mode": "tangent",
        "elapsed_seconds": time.time() - started,
        "real_tangent_dimension": len(pairs),
        "cubic_jacobian_rank_at_tolerance_1e-8": len(pairs) - nullity,
        "cubic_jacobian_nullity_at_tolerance_1e-8": nullity,
        "smallest_nonzero_singular_values": [
            float(value)
            for value in singular_values[nullity : nullity + 10]
        ],
        "largest_singular_value": float(singular_values[-1]),
        "column_norms_by_pair_class": class_norms,
        "nullspace_energy_by_pair_class": null_energy,
        "expected_real_u9_subspace_dimension": expected_u_nine_rank,
        "expected_real_u9_max_cubic_derivative_norm": float(
            np.max(expected_derivative_norms)
        ),
        "generic_finite_u9_samples": finite_u_nine_samples,
        "scalar_phase_u1_sample": {
            "phase_radians": 0.731,
            "involution_norm": float(np.linalg.norm(phase_involution)),
            "cubic_norm": float(np.linalg.norm(phase_cubic)),
        },
        "involution_objective_tangent_gradient_norm": float(
            np.linalg.norm(involution_gradient)
        ),
    }


def polar_retraction(matrix: np.ndarray) -> np.ndarray:
    left, _, right = np.linalg.svd(matrix, full_matrices=False)
    return left @ right


def run_optimization(
    model: PairingModel,
    seed: int,
    cubic_weight: float,
    iterations: int,
    initial_scale: float,
) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    initial_skew = rng.normal(size=(N_SCHMIDT, N_SCHMIDT))
    initial_skew = initial_skew - initial_skew.T
    initial_skew *= initial_scale / np.linalg.norm(initial_skew)
    orthogonal = linalg.expm(initial_skew)
    started = time.time()
    history: list[dict[str, float]] = []
    accepted = 0

    for iteration in range(iterations):
        objective, euclidean_gradient, diagnostics = (
            model.objective_and_euclidean_gradient(
                orthogonal, cubic_weight=cubic_weight
            )
        )
        skew_gradient = (
            orthogonal.T @ euclidean_gradient
            - euclidean_gradient.T @ orthogonal
        ) / 2
        gradient_norm = float(np.linalg.norm(skew_gradient))
        diagnostics.update(
            {
                "iteration": iteration,
                "riemannian_gradient_norm": gradient_norm,
            }
        )
        if iteration == 0 or iteration % 25 == 0:
            history.append(diagnostics.copy())
        if gradient_norm < 1e-12:
            break

        step = min(0.2, 1 / gradient_norm)
        accepted_step = False
        for _ in range(20):
            candidate = polar_retraction(
                orthogonal - step * orthogonal @ skew_gradient
            )
            candidate_objective, _, _ = (
                model.objective_and_euclidean_gradient(
                    candidate, cubic_weight=cubic_weight
                )
            )
            if candidate_objective <= objective - 1e-4 * step * gradient_norm**2:
                orthogonal = candidate
                accepted += 1
                accepted_step = True
                break
            step /= 2
        if not accepted_step:
            break

    final_objective, _, final_diagnostics = (
        model.objective_and_euclidean_gradient(
            orthogonal, cubic_weight=cubic_weight
        )
    )
    final_h = model.h_from_pairing(orthogonal)
    eigenvalues = np.linalg.eigvalsh(final_h)
    return {
        "mode": "optimize",
        "seed": seed,
        "cubic_weight": cubic_weight,
        "iterations_requested": iterations,
        "accepted_steps": accepted,
        "initial_scale": initial_scale,
        "elapsed_seconds": time.time() - started,
        "final": final_diagnostics,
        "h_eigenvalue_min": float(eigenvalues[0]),
        "h_eigenvalue_max": float(eigenvalues[-1]),
        "h_eigenvalue_near_minus_one": int(np.sum(np.abs(eigenvalues + 1) < 1e-6)),
        "h_eigenvalue_near_plus_one": int(np.sum(np.abs(eigenvalues - 1) < 1e-6)),
        "orthogonality_norm": float(
            np.linalg.norm(orthogonal.T @ orthogonal - np.eye(N_SCHMIDT))
        ),
        "pairing_matrix": orthogonal.tolist(),
        "history": history,
        "pairing_sha256": hashlib.sha256(
            orthogonal.astype("<f8").tobytes()
        ).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("tangent", "optimize"), required=True)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--cubic-weight", type=float, default=10.0)
    parser.add_argument("--iterations", type=int, default=300)
    parser.add_argument("--initial-scale", type=float, default=1.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    model = PairingModel.build()
    h_zero, involution_zero, cubic_zero = model.residuals(
        np.eye(N_SCHMIDT)
    )
    common = {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "platform": platform.platform(),
        "h0_trace": [
            float(np.trace(h_zero).real),
            float(np.trace(h_zero).imag),
        ],
        "h0_involution_norm": float(np.linalg.norm(involution_zero)),
        "h0_cubic_norm": float(np.linalg.norm(cubic_zero)),
        "warning": "Numerical exploration only; small residuals are not proof.",
    }
    if args.mode == "tangent":
        result = run_tangent(model)
    else:
        result = run_optimization(
            model,
            seed=args.seed,
            cubic_weight=args.cubic_weight,
            iterations=args.iterations,
            initial_scale=args.initial_scale,
        )
    payload = {**common, **result}
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n")


if __name__ == "__main__":
    main()
