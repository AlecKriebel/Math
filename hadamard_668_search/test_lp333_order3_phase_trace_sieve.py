#!/usr/bin/env python3
"""Tests for the prime-167 factorwise phase trace sieve."""

from __future__ import annotations

import unittest

import verify_lp333_order3_phase_trace_sieve as trace_sieve


class PhaseTraceSieveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = trace_sieve.verify()

    def test_pinned_composite_certificate(self) -> None:
        self.assertEqual(
            self.result["composite_sha256"],
            trace_sieve.EXPECTED_COMPOSITE_SHA256,
        )

    def test_full_algebra_proof_scope(self) -> None:
        full = self.result["full_invariant_algebra"]
        self.assertEqual(full["row_galois_ranks"], (3, 3))
        self.assertEqual(full["invariant_basis_words"], 13)
        self.assertEqual(full["origin_basis_checks"], 13)
        self.assertEqual(full["bilinear_basis_pair_checks"], 169)
        self.assertEqual(full["row_inversion_basis_checks"], 39)
        self.assertEqual(full["coefficient_trace_inverse_checks"], 169)
        self.assertEqual(full["fixed_zero_column_scalar_cuts"], 12)
        self.assertEqual(full["remaining_support_equations_after_total"], 5)

    def test_lookup_free_ninth_bit_decoder(self) -> None:
        decoder = self.result["ninth_bit_decoder"]
        self.assertEqual(decoder["full_dft_basis_checks"], 9)
        self.assertEqual(decoder["weights_checked"], (3, 6))
        self.assertEqual(decoder["physical_words_per_weight"], 84)
        self.assertEqual(decoder["distinct_primitive_values_per_weight"], 82)
        self.assertEqual(decoder["value_profile_pairs_per_weight"], 820)
        self.assertEqual(decoder["idempotent_pairs_per_weight"], 84)
        self.assertEqual(
            decoder["displayed_quadratic_equations_for_24_classes"],
            216,
        )

    def test_exhaustive_local_alphabet(self) -> None:
        local = self.result["local_alphabet"]
        self.assertEqual(local["row_words"], 84)
        self.assertEqual(local["weight_six_complements"], 84)
        self.assertEqual(local["physical_weights_checked"], (3, 6))
        self.assertEqual(local["distinct_row_values"], 82)
        self.assertEqual(local["distinct_norm_values"], 7)
        self.assertEqual(
            local["norm_trace_histogram"],
            {0: 3, 6: 54, 9: 27},
        )
        self.assertEqual(
            local["norm_cubic_polynomials_descending_mod_167"],
            {
                2: (1, 161, 9, 164),
                3: (1, 158, 18, 158),
            },
        )

    def test_physical_profile_fixture(self) -> None:
        physical = self.result["physical_support_167_fixture"]
        self.assertEqual(
            physical["profile_support_vector"],
            (37, 37, 37, 18, 19, 19),
        )
        self.assertEqual(physical["total_support"], 167)
        self.assertEqual(physical["zero_trace_cuts_passed"], 6)
        self.assertEqual(physical["support_parseval_cuts_passed"], 6)

    def test_profile_equations_are_not_implied_by_cone(self) -> None:
        negative = self.result["negative_cone_fixture"]
        self.assertTrue(negative["nonzero_full_norm_cone_fixture"])
        self.assertEqual(negative["total_support_form_mod_167"], 0)
        self.assertEqual(
            negative["individual_support_forms"],
            (1, 0, 0, 56, 89, 21),
        )
        self.assertEqual(
            negative["failed_profile_support_indices"],
            (0, 1, 2, 3, 4, 5),
        )


if __name__ == "__main__":
    unittest.main()
