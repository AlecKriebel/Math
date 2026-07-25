#!/usr/bin/env python3
"""Standard-library tests for verify_h1_x_congruence.py."""

from __future__ import annotations

import unittest

from verify_h1_x_congruence import (
    COLORS,
    h1_x_from_counts,
    verify_parity_identity,
)


class H1CongruenceTest(unittest.TestCase):
    def test_all_parity_vectors(self) -> None:
        verify_parity_identity()

    def test_centered_integer_example(self) -> None:
        counts = dict.fromkeys(COLORS, 0)
        counts[-4] = 280
        counts[0] = 21
        counts[2] = 519
        self.assertEqual(h1_x_from_counts(counts), 20972)
        self.assertEqual(h1_x_from_counts(counts) % 10, 2)

    def test_noncentered_counts_are_rejected(self) -> None:
        counts = dict.fromkeys(COLORS, 0)
        counts[0] = 820
        with self.assertRaisesRegex(ValueError, "centering"):
            h1_x_from_counts(counts)

    def test_fractional_multiplicity_is_rejected(self) -> None:
        counts = dict.fromkeys(COLORS, 0)
        counts[-4] = 280
        counts[0] = 21
        counts[2] = 518.5
        counts[1] = 0.5
        with self.assertRaisesRegex(ValueError, "integers"):
            h1_x_from_counts(counts)


if __name__ == "__main__":
    unittest.main()
