#!/usr/bin/env python3
"""Independent finite checks for the cyclic Bell certificate.

This program deliberately separates three things:

* finite exact symbolic identities;
* finite floating-point stress tests;
* the all-dimensional analytic proof described in ``certificate.json``.

Passing this program is evidence against transcription and implementation
errors.  It is not a formal machine verification of the theorem for all d.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parent
CERTIFICATE_PATH = ROOT / "certificate.json"


class VerificationError(AssertionError):
    """Raised when a certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def dagger(matrix: np.ndarray) -> np.ndarray:
    return matrix.conj().T


def relative_residual(left: np.ndarray, right: np.ndarray) -> float:
    scale = max(1.0, float(np.linalg.norm(left)), float(np.linalg.norm(right)))
    return float(np.linalg.norm(left - right) / scale)


def psd_sqrt(matrix: np.ndarray) -> np.ndarray:
    hermitian = (matrix + dagger(matrix)) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    scale = max(1.0, float(np.max(np.abs(eigenvalues))))
    require(
        float(np.min(eigenvalues)) >= -5e-12 * scale,
        f"matrix is not numerically positive semidefinite: {eigenvalues}",
    )
    roots = np.sqrt(np.maximum(eigenvalues, 0.0))
    return (eigenvectors * roots) @ dagger(eigenvectors)


def matrix_absolute(matrix: np.ndarray) -> np.ndarray:
    return psd_sqrt(dagger(matrix) @ matrix)


def random_unitary(rng: np.random.Generator, dimension: int) -> np.ndarray:
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    q, r = np.linalg.qr(raw)
    diagonal = np.diag(r)
    phases = np.ones(dimension, dtype=complex)
    nonzero = np.abs(diagonal) > 0
    phases[nonzero] = np.conj(diagonal[nonzero] / np.abs(diagonal[nonzero]))
    return q * phases


def fixed_rank_matrix(
    rng: np.random.Generator, dimension: int, rank: int
) -> np.ndarray:
    require(0 <= rank <= dimension, "invalid requested rank")
    if rank == 0:
        return np.zeros((dimension, dimension), dtype=complex)
    left = rng.normal(size=(dimension, rank)) + 1j * rng.normal(
        size=(dimension, rank)
    )
    right = rng.normal(size=(rank, dimension)) + 1j * rng.normal(
        size=(rank, dimension)
    )
    return left @ right


def unitary_polar_data(
    matrix: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return a unitary polar factor and both absolute values/square roots.

    For a singular square matrix, the full SVD selects a unitary extension of
    the polar partial isometry.  This is convenient for the finite check,
    although the analytic SOS identity only needs the partial isometry itself.
    """

    left, singular_values, right_h = np.linalg.svd(matrix, full_matrices=True)
    polar = left @ right_h
    singular_diagonal = np.diag(singular_values)
    root_diagonal = np.diag(np.sqrt(singular_values))
    abs_matrix = dagger(right_h) @ singular_diagonal @ right_h
    abs_adjoint = left @ singular_diagonal @ dagger(left)
    root_abs_matrix = dagger(right_h) @ root_diagonal @ right_h
    root_abs_adjoint = left @ root_diagonal @ dagger(left)
    return polar, abs_matrix, abs_adjoint, root_abs_matrix, root_abs_adjoint


def load_certificate(path: Path = CERTIFICATE_PATH) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data.get("schema_version") == 1, "unsupported certificate schema")
    disclaimer = data["executable_verification"]["disclaimer"].lower()
    require("not a formal machine proof" in disclaimer, "scope disclaimer missing")
    require(
        "analytic argument" in disclaimer,
        "certificate must identify the analytic proof as load-bearing",
    )
    return data


def check_exact_symbolic(max_d: int = 12) -> dict[str, int]:
    """Check a finite list of exact identities with SymPy/integer arithmetic."""

    require(max_d >= 6, "exact checks require max_d >= 6")
    closed_forms = {
        2: 2 * sp.sqrt(2),
        3: sp.Integer(4),
        4: 2 * sp.sqrt(4 + 2 * sp.sqrt(2)),
        5: 2 * (1 + sp.sqrt(5)),
        6: 2 * (sp.sqrt(6) + sp.sqrt(2)),
    }
    for d, expected in closed_forms.items():
        actual = 2 / sp.sin(sp.pi / (2 * d))
        require(
            sp.simplify(actual - expected) == 0,
            f"closed form failed at d={d}: {actual} != {expected}",
        )

    a = sp.symbols("a")
    for d in range(2, max_d + 1):
        cyclic_shift = sp.zeros(d)
        for column in range(d):
            cyclic_shift[(column + 1) % d, column] = 1
        determinant = (sp.eye(d) + a * cyclic_shift).det(method="domain-ge")
        product_polynomial = sp.expand(determinant - (1 - (-a) ** d))
        require(
            product_polynomial == 0,
            f"roots-of-unity product polynomial failed at d={d}",
        )

        # omega^(d(d-1)/2) = exp(pi i(d-1)) = (-1)^(d-1).
        weyl_exponent = d * (d - 1) // 2
        require(
            sp.simplify(
                sp.exp(2 * sp.pi * sp.I * sp.Rational(weyl_exponent, d))
                - (-1) ** (d - 1)
            )
            == 0,
            f"Weyl parity identity failed at d={d}",
        )
        require(
            1 - ((-1) ** d) * ((-1) ** (d - 1)) == 2,
            f"positive orbit product failed at d={d}",
        )

    return {"closed_forms": len(closed_forms), "product_instances": max_d - 1}


def check_polar_sos_random(
    *,
    seed: int = 2606213621,
    max_dimension: int = 6,
    tolerance: float = 2e-10,
) -> dict[str, float | int]:
    """Stress-test the exact polar SOS identity, including singular C."""

    rng = np.random.default_rng(seed)
    max_residual = 0.0
    checks = 0
    singular_checks = 0

    for alice_dimension in range(1, max_dimension + 1):
        ranks = sorted(
            {
                0,
                1 if alice_dimension >= 1 else 0,
                max(0, alice_dimension - 1),
                alice_dimension,
            }
        )
        for rank in ranks:
            c = fixed_rank_matrix(rng, alice_dimension, rank)
            bob_dimension = 1 + ((alice_dimension + rank) % max_dimension)
            b = random_unitary(rng, bob_dimension)
            (
                polar,
                abs_c,
                abs_c_adjoint,
                root_abs_c,
                root_abs_c_adjoint,
            ) = unitary_polar_data(c)

            identity_b = np.eye(bob_dimension, dtype=complex)
            lhs = np.kron((abs_c + abs_c_adjoint) / 2, identity_b)
            c_tensor_b = np.kron(c, b)
            lhs -= (c_tensor_b + dagger(c_tensor_b)) / 2

            p = np.kron(root_abs_c_adjoint, identity_b) - np.kron(
                polar @ root_abs_c, b
            )
            rhs = dagger(p) @ p / 2
            residual = relative_residual(lhs, rhs)
            max_residual = max(max_residual, residual)
            checks += 1
            singular_checks += int(rank < alice_dimension)

            require(
                relative_residual(polar @ abs_c, c) <= tolerance,
                f"polar factorization failed for dim={alice_dimension}, rank={rank}",
            )
            require(
                relative_residual(dagger(polar) @ polar, np.eye(alice_dimension))
                <= tolerance,
                f"unitary polar extension failed for dim={alice_dimension}, rank={rank}",
            )
            require(
                residual <= tolerance,
                f"polar SOS failed for dim={alice_dimension}, rank={rank}: "
                f"{residual:.3e}",
            )

    return {
        "checks": checks,
        "singular_checks": singular_checks,
        "max_relative_residual": max_residual,
    }


def check_global_certificate_random(
    *,
    seed: int = 2606213630,
    min_d: int = 2,
    max_d: int = 6,
    trials_per_d: int = 2,
    tolerance: float = 2e-10,
) -> dict[str, float | int]:
    """Assemble and test the complete global positive-factor certificate.

    The observables here are arbitrary Haar-style random unitaries; no order-d
    relations are imposed.  Alice and Bob dimensions vary independently.
    """

    require(2 <= min_d <= max_d, "invalid global-certificate d range")
    require(trials_per_d >= 1, "trials_per_d must be positive")
    rng = np.random.default_rng(seed)
    max_factorization_residual = 0.0
    smallest_lhs_eigenvalue = math.inf
    smallest_functional_deficit_eigenvalue = math.inf
    checks = 0

    for d in range(min_d, max_d + 1):
        omega = np.exp(2j * np.pi / d)
        lambda_d = 2 / math.sin(math.pi / (2 * d))
        for trial in range(trials_per_d):
            alice_dimension = 2 + ((d + trial) % 4)
            bob_dimension = 2 + ((d + 2 * trial) % 3)
            identity_a = np.eye(alice_dimension, dtype=complex)
            identity_b = np.eye(bob_dimension, dtype=complex)
            identity_ab = np.eye(
                alice_dimension * bob_dimension, dtype=complex
            )

            a_zero = random_unitary(rng, alice_dimension)
            a_one = random_unitary(rng, alice_dimension)
            observables_b = [
                random_unitary(rng, bob_dimension) for _ in range(d)
            ]
            relative_unitary = dagger(a_zero) @ a_one

            bell = np.zeros_like(identity_ab)
            functional_sum = np.zeros_like(identity_a)
            polar_factors: list[np.ndarray] = []

            for y, b_y in enumerate(observables_b):
                n_y = identity_a + omega**y * relative_unitary
                functional_sum += matrix_absolute(n_y)

                c_y = a_zero + omega**y * a_one
                term = np.kron(c_y, b_y)
                bell += (term + dagger(term)) / 2

                (
                    polar,
                    _,
                    _,
                    root_abs_c,
                    root_abs_c_adjoint,
                ) = unitary_polar_data(c_y)
                p_y = np.kron(root_abs_c_adjoint, identity_b) - np.kron(
                    polar @ root_abs_c, b_y
                )
                polar_factors.append(p_y)

            functional_deficit = (
                lambda_d * identity_a - functional_sum
            )
            functional_deficit = (
                functional_deficit + dagger(functional_deficit)
            ) / 2
            functional_deficit_minimum = float(
                np.linalg.eigvalsh(functional_deficit)[0]
            )
            smallest_functional_deficit_eigenvalue = min(
                smallest_functional_deficit_eigenvalue,
                functional_deficit_minimum,
            )
            require(
                functional_deficit_minimum >= -tolerance,
                f"F_d(U) exceeded lambda_d I at d={d}, trial={trial}: "
                f"{functional_deficit_minimum:.3e}",
            )
            g = psd_sqrt(functional_deficit)

            rhs = sum(
                (dagger(p_y) @ p_y for p_y in polar_factors),
                start=np.zeros_like(identity_ab),
            ) / 2
            q_one = np.kron(g, identity_b)
            q_two = np.kron(g @ dagger(a_zero), identity_b)
            rhs += (dagger(q_one) @ q_one + dagger(q_two) @ q_two) / 2

            lhs = lambda_d * identity_ab - bell
            lhs = (lhs + dagger(lhs)) / 2
            factorization_residual = relative_residual(lhs, rhs)
            lhs_minimum = float(np.linalg.eigvalsh(lhs)[0])
            max_factorization_residual = max(
                max_factorization_residual, factorization_residual
            )
            smallest_lhs_eigenvalue = min(
                smallest_lhs_eigenvalue, lhs_minimum
            )
            checks += 1

            require(
                factorization_residual <= tolerance,
                f"global SOS factorization failed at d={d}, trial={trial}: "
                f"{factorization_residual:.3e}",
            )
            require(
                lhs_minimum >= -tolerance,
                f"global Bell deficit is not positive at d={d}, trial={trial}: "
                f"{lhs_minimum:.3e}",
            )

    return {
        "checks": checks,
        "dimensions_d": max_d - min_d + 1,
        "max_factorization_residual": max_factorization_residual,
        "smallest_lhs_eigenvalue": smallest_lhs_eigenvalue,
        "smallest_functional_deficit_eigenvalue": (
            smallest_functional_deficit_eigenvalue
        ),
    }


def scalar_sum(d: int, z: complex) -> float:
    omega = np.exp(2j * np.pi / d)
    return float(sum(abs(1 + omega**y * z) for y in range(d)))


def scalar_maximizers(d: int) -> np.ndarray:
    angles = (np.pi * (d - 1) + 2 * np.pi * np.arange(d)) / d
    return np.exp(1j * angles)


def check_scalar_maximum(
    max_d: int = 12,
    *,
    grid_size: int = 8192,
    tolerance: float = 2e-10,
) -> dict[str, float | int]:
    """Check the finite scalar instances and their complete equality sets."""

    max_excess = 0.0
    max_equality_residual = 0.0
    equality_points = 0

    grid = np.exp(2j * np.pi * np.arange(grid_size) / grid_size)
    for d in range(2, max_d + 1):
        target = 2 / math.sin(math.pi / (2 * d))
        sign = (-1) ** (d - 1)
        maximizers = scalar_maximizers(d)
        require(len(maximizers) == d, f"wrong equality-set size at d={d}")

        for z in maximizers:
            power_residual = abs(z**d - sign)
            value_residual = abs(scalar_sum(d, complex(z)) - target)
            max_equality_residual = max(
                max_equality_residual, power_residual, value_residual
            )
            equality_points += 1
            require(
                power_residual <= tolerance and value_residual <= tolerance,
                f"scalar equality case failed at d={d}",
            )

        sampled_maximum = max(scalar_sum(d, complex(z)) for z in grid)
        excess = sampled_maximum - target
        max_excess = max(max_excess, excess)
        require(
            excess <= tolerance,
            f"sampled scalar bound exceeded at d={d}: {excess:.3e}",
        )

        # A half-step perturbation avoids the finite equality set and checks
        # strictness at a deterministic point in every intervening arc.
        perturbation = np.exp(1j * np.pi / (2 * d))
        for z in maximizers:
            require(
                scalar_sum(d, complex(z * perturbation)) < target - 1e-8,
                f"strict scalar inequality check failed at d={d}",
            )

    return {
        "dimensions": max_d - 1,
        "equality_points": equality_points,
        "grid_points_per_dimension": grid_size,
        "max_sampled_excess": max_excess,
        "max_equality_residual": max_equality_residual,
    }


def weyl_operators(d: int) -> tuple[complex, np.ndarray, np.ndarray]:
    require(d >= 2, "d must be at least 2")
    omega = np.exp(2j * np.pi / d)
    z = np.diag(omega ** np.arange(d)).astype(complex)
    x = np.roll(np.eye(d, dtype=complex), 1, axis=0)
    return omega, z, x


def spectrum_match_residual(
    eigenvalues: np.ndarray, expected: np.ndarray
) -> tuple[float, set[int]]:
    distances = np.abs(eigenvalues[:, None] - expected[None, :])
    labels = np.argmin(distances, axis=1)
    residual = float(np.max(distances[np.arange(len(eigenvalues)), labels]))
    return residual, {int(label) for label in labels}


def explicit_strategy(
    d: int,
) -> tuple[complex, np.ndarray, np.ndarray, np.ndarray, list[np.ndarray]]:
    omega, z, x = weyl_operators(d)
    identity = np.eye(d, dtype=complex)
    w = dagger(z) @ x
    observables_b: list[np.ndarray] = []

    for y in range(d):
        n_y = identity + omega**y * w
        h_y = matrix_absolute(n_y)
        polar_c_y = z @ n_y @ np.linalg.inv(h_y)
        # If C_y=V_y|C_y|, maximally-entangled trace duality calls for
        # B_y=(V_y^*)^T=conjugate(V_y).
        observables_b.append(polar_c_y.conj())

    return omega, z, x, w, observables_b


def check_weyl_and_bob(
    max_d: int = 12,
    *,
    matrix_tolerance: float = 2e-10,
    spectrum_tolerance: float = 2e-9,
) -> dict[str, float | int]:
    """Check the equality spectrum and the load-bearing order-d argument."""

    max_matrix_residual = 0.0
    max_spectrum_residual = 0.0
    max_originating_strategy_residual = 0.0
    min_h_eigenvalue = math.inf
    bob_observables = 0

    for d in range(2, max_d + 1):
        omega, z, x, w, observables_b = explicit_strategy(d)
        identity = np.eye(d, dtype=complex)
        target = 2 / math.sin(math.pi / (2 * d))

        commutation = relative_residual(z @ x, omega * x @ z)
        conjugation = relative_residual(z @ w @ dagger(z), omega * w)
        power = relative_residual(
            np.linalg.matrix_power(w, d), ((-1) ** (d - 1)) * identity
        )
        max_matrix_residual = max(
            max_matrix_residual, commutation, conjugation, power
        )
        require(
            max(commutation, conjugation, power) <= matrix_tolerance,
            f"Weyl identities failed at d={d}",
        )

        expected_w_spectrum = scalar_maximizers(d)
        w_spectrum_residual, w_labels = spectrum_match_residual(
            np.linalg.eigvals(w), expected_w_spectrum
        )
        max_spectrum_residual = max(max_spectrum_residual, w_spectrum_residual)
        require(
            w_spectrum_residual <= spectrum_tolerance
            and w_labels == set(range(d)),
            f"W has the wrong full maximizing spectrum at d={d}",
        )

        functional_sum = np.zeros((d, d), dtype=complex)
        for y in range(d):
            n_y = identity + omega**y * w
            normality = relative_residual(dagger(n_y) @ n_y, n_y @ dagger(n_y))
            h_y = matrix_absolute(n_y)
            min_h_eigenvalue = min(
                min_h_eigenvalue, float(np.min(np.linalg.eigvalsh(h_y)))
            )
            require(
                normality <= matrix_tolerance,
                f"N_y is not normal at d={d}, y={y}",
            )
            require(
                float(np.min(np.linalg.eigvalsh(h_y))) > 1e-9,
                f"H_y is singular at d={d}, y={y}",
            )
            functional_sum += h_y

        functional_residual = relative_residual(
            functional_sum, target * identity
        )
        max_matrix_residual = max(max_matrix_residual, functional_residual)
        require(
            functional_residual <= matrix_tolerance,
            f"functional-calculus equality failed at d={d}",
        )

        # This is the omitted weighted-shift link in the supplied draft:
        # the phase accumulated around the complete W orbit is exactly +1.
        w_eigenvalues = np.linalg.eigvals(w)
        phase_product = np.prod(
            (1 + w_eigenvalues) / np.abs(1 + w_eigenvalues)
        )
        numerator_product = np.prod(1 + w_eigenvalues)
        phase_residual = abs(phase_product - 1)
        numerator_residual = abs(numerator_product - 2)
        max_matrix_residual = max(
            max_matrix_residual, phase_residual, numerator_residual
        )
        require(
            phase_residual <= spectrum_tolerance
            and numerator_residual <= spectrum_tolerance,
            f"weighted-shift orbit product failed at d={d}",
        )

        _, _, _, _, b_zero_list = explicit_strategy(d)
        b_zero = b_zero_list[0]
        v_zero = b_zero.conj()
        roots_of_unity = np.exp(2j * np.pi * np.arange(d) / d)

        for y, b_y in enumerate(observables_b):
            bob_observables += 1
            v_y = b_y.conj()
            conjugate_v_zero = (
                np.linalg.matrix_power(z, y)
                @ v_zero
                @ np.linalg.matrix_power(dagger(z), y)
            )
            y_conjugacy = relative_residual(v_y, conjugate_v_zero)
            unitarity = relative_residual(dagger(b_y) @ b_y, identity)
            order = relative_residual(np.linalg.matrix_power(b_y, d), identity)
            spectrum_residual, spectrum_labels = spectrum_match_residual(
                np.linalg.eigvals(b_y), roots_of_unity
            )
            max_matrix_residual = max(
                max_matrix_residual, y_conjugacy, unitarity, order
            )
            max_spectrum_residual = max(
                max_spectrum_residual, spectrum_residual
            )
            require(
                y_conjugacy <= matrix_tolerance,
                f"V_y conjugacy failed at d={d}, y={y}",
            )
            require(
                unitarity <= matrix_tolerance,
                f"B_y unitarity failed at d={d}, y={y}",
            )
            require(
                order <= matrix_tolerance,
                f"B_y^d=I failed at d={d}, y={y}",
            )
            require(
                spectrum_residual <= spectrum_tolerance
                and spectrum_labels == set(range(d)),
                f"B_y lacks the complete d-th-root spectrum at d={d}, y={y}",
            )

            # Compare with Eqs. (15) and (45) of arXiv:2606.21362v3.
            paper_b_y = np.zeros((d, d), dtype=complex)
            for k in range(d):
                coefficient = (
                    (-1) ** k
                    * omega ** (k * (k + 1) // 2)
                    * omega ** (-y * (1 + k))
                    / (d * np.sin(np.pi * (k + 0.5) / d))
                )
                paper_b_y += (
                    coefficient
                    * np.linalg.matrix_power(x, k + 1)
                    @ np.linalg.matrix_power(z, k)
                )
            paper_match = relative_residual(b_y, paper_b_y)
            max_originating_strategy_residual = max(
                max_originating_strategy_residual, paper_match
            )
            require(
                paper_match <= spectrum_tolerance,
                f"polar B_y does not match the originating formula at "
                f"d={d}, y={y}",
            )

    return {
        "dimensions": max_d - 1,
        "bob_observables": bob_observables,
        "max_matrix_residual": max_matrix_residual,
        "max_spectrum_residual": max_spectrum_residual,
        "max_originating_strategy_residual": (
            max_originating_strategy_residual
        ),
        "smallest_checked_H_eigenvalue": min_h_eigenvalue,
    }


def check_bell_values(
    max_d: int = 12, *, tolerance: float = 2e-10
) -> dict[str, float | int]:
    """Build each finite Bell matrix and check exact-strategy saturation."""

    max_value_residual = 0.0
    max_vector_residual = 0.0
    max_top_eigenvalue_residual = 0.0

    for d in range(2, max_d + 1):
        omega, z, x, _, observables_b = explicit_strategy(d)
        bell = np.zeros((d * d, d * d), dtype=complex)
        for y, b_y in enumerate(observables_b):
            c_y = z + omega**y * x
            term = np.kron(c_y, b_y)
            bell += (term + dagger(term)) / 2

        phi = np.eye(d, dtype=complex).reshape(d * d) / math.sqrt(d)
        target = 2 / math.sin(math.pi / (2 * d))
        value = float(np.vdot(phi, bell @ phi).real)
        value_residual = abs(value - target)
        vector_residual = float(np.linalg.norm(bell @ phi - target * phi))
        top_eigenvalue = float(np.linalg.eigvalsh(bell)[-1])
        top_eigenvalue_residual = abs(top_eigenvalue - target)

        max_value_residual = max(max_value_residual, value_residual)
        max_vector_residual = max(max_vector_residual, vector_residual)
        max_top_eigenvalue_residual = max(
            max_top_eigenvalue_residual, top_eigenvalue_residual
        )
        require(
            relative_residual(bell, dagger(bell)) <= tolerance,
            f"Bell matrix is not Hermitian at d={d}",
        )
        require(
            value_residual <= tolerance,
            f"Bell expectation failed at d={d}: {value} != {target}",
        )
        require(
            vector_residual <= tolerance,
            f"Phi_d is not a maximizing eigenvector at d={d}",
        )
        require(
            top_eigenvalue_residual <= tolerance,
            f"fixed-strategy Bell top eigenvalue failed at d={d}",
        )

    return {
        "dimensions": max_d - 1,
        "max_value_residual": max_value_residual,
        "max_vector_residual": max_vector_residual,
        "max_top_eigenvalue_residual": max_top_eigenvalue_residual,
    }


def run_all(max_d: int | None = None) -> dict[str, dict[str, float | int]]:
    certificate = load_certificate()
    config = certificate["executable_verification"]
    selected_max_d = max_d or int(config["default_max_d"])
    require(selected_max_d >= 6, "max_d must be at least 6")
    tolerances = config["tolerances"]

    return {
        "exact_symbolic": check_exact_symbolic(selected_max_d),
        "polar_sos": check_polar_sos_random(
            seed=int(config["random_seed"]),
            tolerance=float(tolerances["matrix"]),
        ),
        "global_certificate": check_global_certificate_random(
            seed=int(config["random_seed"]) + 9,
            tolerance=float(tolerances["matrix"]),
        ),
        "scalar": check_scalar_maximum(
            selected_max_d, tolerance=float(tolerances["scalar"])
        ),
        "weyl_and_bob": check_weyl_and_bob(
            selected_max_d,
            matrix_tolerance=float(tolerances["matrix"]),
            spectrum_tolerance=float(tolerances["spectrum"]),
        ),
        "bell_values": check_bell_values(
            selected_max_d, tolerance=float(tolerances["matrix"])
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-d",
        type=int,
        default=None,
        help="largest finite dimension to check (default: certificate value 12)",
    )
    args = parser.parse_args()

    certificate = load_certificate()
    print("SCOPE:", certificate["executable_verification"]["disclaimer"])
    results = run_all(args.max_d)
    for name, result in results.items():
        metrics = ", ".join(f"{key}={value}" for key, value in result.items())
        print(f"PASS [{name}]: {metrics}")
    print(
        "OVERALL PASS: finite symbolic and numerical certificate checks succeeded; "
        "the analytic proof remains the all-dimensional justification."
    )


if __name__ == "__main__":
    main()
