#!/usr/bin/env python3
"""Tests for the exact LP(333) three-fiber phase factorization."""

from __future__ import annotations

import unittest

import verify_lp333_order3_phase_factor as phase
from verify_lp333_order3_labeled_jet import (
    LABELLED_SURVIVOR_MASKS_A,
    LABELLED_SURVIVOR_MASKS_B,
)
from verify_lp333_order3_trit_lift import (
    TRIT_SURVIVOR_MASKS_A,
    TRIT_SURVIVOR_MASKS_B,
)


class OrderThreePhaseFactorTests(unittest.TestCase):
    def test_active_fiber_trit_is_exact_phase(self) -> None:
        result = phase.verify_local_phase_bijection()
        self.assertEqual(result["active_placement_checks"], 6)

    def test_pinned_certificate_replays_in_both_bases(self) -> None:
        result = phase.verify_certificate_factorization(
            LABELLED_SURVIVOR_MASKS_A,
            LABELLED_SURVIVOR_MASKS_B,
        )
        self.assertTrue(result["exact_factorization"])
        self.assertTrue(result["e2_is_adjoint_of_e1"])
        self.assertFalse(result["exact_integral_survivor"])

    def test_trit_certificate_replays_in_both_bases(self) -> None:
        result = phase.verify_certificate_factorization(
            TRIT_SURVIVOR_MASKS_A,
            TRIT_SURVIVOR_MASKS_B,
        )
        self.assertTrue(result["exact_factorization"])
        self.assertEqual(result["active_physical_fibers"], 167)
        self.assertFalse(result["exact_integral_survivor"])

    def test_row695_phase_frame_dimensions(self) -> None:
        result = phase.verify()
        self.assertEqual(result["pinned_profile_trits"], 54)
        self.assertEqual(result["independent_integer_conditions"], 39)
        self.assertEqual(result["mixed_column_integer_conditions"], 36)


if __name__ == "__main__":
    unittest.main()
