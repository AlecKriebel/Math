"""Regression tests for the finite cyclic Bell certificate checker."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import verify_certificate as verifier  # noqa: E402


class CertificateTests(unittest.TestCase):
    max_d = 12

    def test_scope_disclaimer(self) -> None:
        certificate = verifier.load_certificate()
        disclaimer = certificate["executable_verification"]["disclaimer"]
        self.assertIn("not a formal machine proof", disclaimer.lower())
        self.assertIn("analytic argument", disclaimer.lower())

    def test_finite_exact_symbolic_identities(self) -> None:
        result = verifier.check_exact_symbolic(self.max_d)
        self.assertEqual(result["closed_forms"], 5)
        self.assertEqual(result["product_instances"], self.max_d - 1)

    def test_random_polar_sos_including_singular_matrices(self) -> None:
        result = verifier.check_polar_sos_random()
        self.assertGreaterEqual(result["singular_checks"], 1)
        self.assertLessEqual(result["max_relative_residual"], 2e-10)

    def test_complete_global_certificate_for_arbitrary_unitaries(self) -> None:
        result = verifier.check_global_certificate_random()
        self.assertEqual(result["dimensions_d"], 5)
        self.assertEqual(result["checks"], 10)
        self.assertLessEqual(result["max_factorization_residual"], 2e-10)
        self.assertGreaterEqual(result["smallest_lhs_eigenvalue"], -2e-10)
        self.assertGreaterEqual(
            result["smallest_functional_deficit_eigenvalue"], -2e-10
        )

    def test_scalar_maximum_and_all_equality_roots(self) -> None:
        result = verifier.check_scalar_maximum(self.max_d)
        expected_points = sum(range(2, self.max_d + 1))
        self.assertEqual(result["equality_points"], expected_points)
        self.assertLessEqual(result["max_equality_residual"], 2e-10)

    def test_weyl_spectrum_and_bob_order(self) -> None:
        result = verifier.check_weyl_and_bob(self.max_d)
        expected_observables = sum(range(2, self.max_d + 1))
        self.assertEqual(result["bob_observables"], expected_observables)
        self.assertLessEqual(result["max_matrix_residual"], 2e-10)
        self.assertLessEqual(result["max_spectrum_residual"], 2e-9)
        self.assertLessEqual(
            result["max_originating_strategy_residual"], 2e-9
        )
        self.assertGreater(result["smallest_checked_H_eigenvalue"], 0)

    def test_bell_values(self) -> None:
        result = verifier.check_bell_values(self.max_d)
        self.assertLessEqual(result["max_value_residual"], 2e-10)
        self.assertLessEqual(result["max_vector_residual"], 2e-10)
        self.assertLessEqual(result["max_top_eigenvalue_residual"], 2e-10)


if __name__ == "__main__":
    unittest.main()
