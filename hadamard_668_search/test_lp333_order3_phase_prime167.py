#!/usr/bin/env python3
"""Tests for full prime-167 exactness of the six-sequence phase frame."""

from __future__ import annotations

import unittest

import verify_lp333_order3_phase_prime167 as phase167


class PhasePrime167Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = phase167.verify()

    def test_equality_orbits(self) -> None:
        result = self.result["equality_orbits"]
        self.assertEqual(
            (
                result["diagonal_nonzero_lag_orbit"],
                result["cross_zero_lag_orbit"],
                result["cross_nonzero_lag_orbit"],
            ),
            (37, 3, 111),
        )
        self.assertEqual(result["twisted_orbit_scalar"], phase167.E_OMEGA2)
        self.assertEqual(result["support_remainders"], (19, 2, 56))
        self.assertEqual(
            result["certificate_sha256"],
            phase167.EXPECTED_ORBIT_CERTIFICATE_SHA256,
        )

    def test_support_167_fixtures(self) -> None:
        result = self.result["phase_fixtures"]
        self.assertEqual(result["fixtures"], 3)
        self.assertEqual(result["support_per_fixture"], 167)
        self.assertEqual(result["active_nonzero_class_fibers"], 54)
        self.assertEqual(result["active_zero_column_fibers"], 5)
        self.assertTrue(result["exact_modular_predicates_agree"])
        self.assertEqual(
            result["certificate_sha256"],
            phase167.EXPECTED_FRAME_CERTIFICATE_SHA256,
        )

    def test_complete_crt_equations(self) -> None:
        result = self.result["crt_equations"]
        self.assertEqual(result["fixtures"], 3)
        self.assertEqual(result["trivial_equations"], 2)
        self.assertEqual(result["primitive_equations_over_E"], 3)
        self.assertEqual(result["star_frobenius_exponents"], (5, 7))
        self.assertEqual(
            result["certificate_sha256"],
            phase167.EXPECTED_CRT_CERTIFICATE_SHA256,
        )

    def test_primitive_plane_annihilator(self) -> None:
        result = self.result["primitive_plane"]
        self.assertEqual(result["generic_orbit_plane_rank"], 3)
        self.assertEqual(result["generic_annihilator_dimension"], 3)
        self.assertEqual(result["maximum_equation_rank"], 3)
        self.assertTrue(result["explicit_annihilator_fixture"])
        self.assertEqual(
            result["certificate_sha256"],
            phase167.EXPECTED_PLANE_CERTIFICATE_SHA256,
        )

    def test_ninth_root_recombination(self) -> None:
        result = self.result["recombined_split"]
        self.assertEqual(result["phi9_degree"], 6)
        self.assertEqual(
            result["invariant_algebra"],
            "F_(167^6) x F_(167^12)^6",
        )
        self.assertEqual(result["primitive_factor_count"], 6)
        self.assertEqual(
            result["primitive_q_orbit_sizes"],
            (6, 6, 6, 6, 6, 6),
        )
        self.assertEqual(
            result["invariant_dimension_over_coefficient_field"],
            13,
        )
        self.assertEqual(result["class_indicator_rank"], 13)
        self.assertTrue(result["recombination_identity_checked"])
        self.assertEqual(len(result["recombination_identity_sha256"]), 64)
        self.assertEqual(result["star_basis_words"], 13)
        self.assertEqual(result["star_pair_count"], 3)
        self.assertEqual(result["star_frobenius_exponents"], (3, 9))
        self.assertEqual(result["scalar_equation_count_over_f_167"], 39)
        self.assertEqual(result["trivial_branches"], ("zero", "nonzero"))
        self.assertEqual(
            result["primitive_branches_per_pair"],
            ("degenerate", "nondegenerate"),
        )
        self.assertEqual(result["nondegenerate_parameter_fixtures"], 3)
        expected_trivial = (
            1 + (phase167.P**6 - 1) * (phase167.P**3 + 1)
        )
        expected_pair = (
            phase167.P**24
            + (phase167.P**24 - 1) * phase167.P**12
        )
        self.assertEqual(
            result["trivial_branch_counts"],
            (1, (phase167.P**6 - 1) * (phase167.P**3 + 1)),
        )
        self.assertEqual(
            result["primitive_branch_counts_per_pair"],
            (
                phase167.P**24,
                (phase167.P**24 - 1) * phase167.P**12,
            ),
        )
        self.assertEqual(result["trivial_solution_count"], expected_trivial)
        self.assertEqual(result["one_pair_solution_count"], expected_pair)
        self.assertEqual(
            result["full_solution_count"],
            expected_trivial * expected_pair**3,
        )
        self.assertEqual(
            result["certificate_sha256"],
            phase167.EXPECTED_RECOMBINED_CERTIFICATE_SHA256,
        )

    def test_local_fixture_shape_and_twist(self) -> None:
        frame = phase167.locally_valid_phase_frame(9)
        self.assertEqual(len(frame), 6)
        self.assertTrue(all(len(word) == 37 for word in frame))
        self.assertEqual(
            sum(value != phase167.E_ZERO for word in frame for value in word),
            167,
        )
        twisted = frame
        for _ in range(3):
            twisted = phase167.twist_exact_frame(twisted)
        expected = tuple(
            phase167.scale_exact_word(phase167.E_OMEGA2, word)
            for word in frame
        )
        self.assertEqual(twisted, expected)


if __name__ == "__main__":
    unittest.main()
