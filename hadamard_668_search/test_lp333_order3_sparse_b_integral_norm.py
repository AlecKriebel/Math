#!/usr/bin/env python3
"""Focused regressions for the integral sparse-B norm certificate."""

from __future__ import annotations

import unittest

from verify_lp333_order3_sparse_b_integral_norm import (
    CASES,
    CLASS_ORDER_RESIDUE_RANKS,
    EPSILON_PARITY,
    EXPECTED_CERTIFICATE_SHA256,
    HASSE_UNIT_NORM_PARITY,
    allocation_classes,
    verify,
)


class SparseBIntegralNormTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = verify()

    def test_all_integral_allocations_are_replayed(self) -> None:
        self.assertEqual(
            tuple(len(allocation_classes(case)) for case in CASES),
            (8, 4, 4, 2),
        )
        self.assertEqual(
            tuple(case["principal_allocations"] for case in CASES),
            (0, 0, 4, 0),
        )

    def test_principal_row_has_odd_unit_norm_parity(self) -> None:
        self.assertEqual(
            EPSILON_PARITY,
            (0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0),
        )
        self.assertNotEqual(EPSILON_PARITY, (0,) * 11)
        self.assertNotEqual(EPSILON_PARITY, HASSE_UNIT_NORM_PARITY)

    def test_class_generator_has_exact_order_certificate(self) -> None:
        self.assertEqual(
            CLASS_ORDER_RESIDUE_RANKS,
            ((2, 96, 12, 13), (3, 96, 12, 13)),
        )
        self.assertEqual(self.result["class_generator_order"], 12)

    def test_sparse_sector_is_closed(self) -> None:
        self.assertEqual(self.result["new_integral_obstruction"], 84)
        self.assertEqual(self.result["total_sparse_words"], 396)
        self.assertTrue(self.result["energy_six_sector_closed"])

    def test_certificate_hash(self) -> None:
        self.assertEqual(
            self.result["certificate_sha256"],
            EXPECTED_CERTIFICATE_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
