#!/usr/bin/env python3
"""Focused tests for the order-three profile spectral-unit theorem."""

from __future__ import annotations

import unittest

import verify_lp333_order3_spectral_units as spectral


class SpectralUnitTests(unittest.TestCase):
    def test_profile_polynomial_and_energy_sectors(self) -> None:
        result = spectral.verify_alphabet()
        self.assertEqual(
            result["certificate_sha256"],
            spectral.EXPECTED_ALPHABET_CERTIFICATE_SHA256,
        )
        self.assertEqual(
            result["energy_type_sectors"],
            (
                (0, 6, 18, 18, -486),
                (1, 8, 15, 16, 324),
                (2, 10, 12, 14, 1134),
                (3, 12, 9, 12, 1944),
                (4, 14, 6, 10, 2754),
                (5, 16, 3, 8, 3564),
                (6, 18, 0, 6, 4374),
            ),
        )

    def test_irreducibility_and_residue_primes(self) -> None:
        result = spectral.verify_field_arithmetic()
        self.assertTrue(result["phi37_shift_eisenstein"])
        self.assertEqual(result["primitive_quotient_cycles"], (6, 6))
        self.assertEqual(
            result["primitive_prime_absolute_norms"],
            (spectral.Q**12, spectral.Q**12),
        )
        self.assertEqual(
            result["certificate_sha256"],
            spectral.EXPECTED_FIELD_CERTIFICATE_SHA256,
        )

    def test_norm_gap_and_trivial_units(self) -> None:
        result = spectral.verify_norm_gap()
        self.assertEqual(
            result["primitive_norm_integer_interval"],
            (1, spectral.Q**12 - 1),
        )
        self.assertEqual(set(result["prime_valuations"].values()), {0})
        self.assertEqual(
            result["certificate_sha256"],
            spectral.EXPECTED_NORM_CERTIFICATE_SHA256,
        )

    def test_norm_gap_rejects_wrong_degree_or_threshold(self) -> None:
        with self.assertRaises(ValueError):
            spectral.product_norm_gap(11, spectral.Q, spectral.Q**12)
        with self.assertRaises(ValueError):
            spectral.product_norm_gap(12, spectral.Q - 1, spectral.Q**12)
        with self.assertRaises(ValueError):
            spectral.product_norm_gap(0, spectral.Q, spectral.Q**12)

    def test_unitary_ratio_and_single_torus(self) -> None:
        result = spectral.verify_torus()
        expected_fixed = (spectral.M - 1) ** 3
        self.assertEqual(
            result["fixed_target_primitive_torus_count"], expected_fixed
        )
        self.assertEqual(
            result["removed_boundary_count"], (2 * spectral.M - 1) ** 2
        )
        labels = tuple(
            pattern[0] for pattern in result["forbidden_old_patterns"]
        )
        self.assertEqual(
            labels, ("degenerate", "A-axis", "B-axis", "tau-zero")
        )
        self.assertEqual(
            result["certificate_sha256"],
            spectral.EXPECTED_TORUS_CERTIFICATE_SHA256,
        )

    def test_master_certificate(self) -> None:
        result = spectral.verify()
        self.assertEqual(
            result["certificate_sha256"],
            spectral.EXPECTED_MASTER_CERTIFICATE_SHA256,
        )
        self.assertIn("no profile survivor", result["status"])


if __name__ == "__main__":
    unittest.main()
