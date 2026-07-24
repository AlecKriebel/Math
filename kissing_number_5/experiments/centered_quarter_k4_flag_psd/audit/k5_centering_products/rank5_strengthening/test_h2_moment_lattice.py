#!/usr/bin/env python3
"""Standard-library tests for verify_h2_moment_lattice.py."""

from __future__ import annotations

import unittest

from verify_h2_moment_lattice import (
    COLORS,
    invariants,
    verify_exact_scaling,
)


def example_counts() -> dict[int, int]:
    counts = dict.fromkeys(COLORS, 0)
    counts[-4] = 280
    counts[0] = 21
    counts[2] = 519
    return counts


class H2MomentLatticeTest(unittest.TestCase):
    def test_exact_forms_and_congruences(self) -> None:
        s, r, x, y = invariants(example_counts(), 0)
        verify_exact_scaling(s, r)
        self.assertEqual(s % 30, 10)
        self.assertEqual(x % 210, 82)
        q = sum(
            color * color * multiplicity
            for color, multiplicity in example_counts().items()
        )
        x1 = 5 * q - 11_808
        self.assertEqual((x - 21 * x1 - 40) % 2100, 0)
        self.assertEqual(y % 210, 66)
        self.assertEqual((y - 10 * x - 2) % 49, 0)

    def test_any_multiple_of_thirty_for_r(self) -> None:
        for r in (-300, -30, 0, 30, 1230):
            s, checked_r, _, _ = invariants(example_counts(), r)
            self.assertEqual(checked_r, r)
            verify_exact_scaling(s, checked_r)

    def test_bad_triple_divisibility_is_rejected(self) -> None:
        for tampered_r in (5, 6, 29, 31):
            with self.subTest(tampered_r=tampered_r):
                with self.assertRaisesRegex(ValueError, "divisible by 30"):
                    invariants(example_counts(), tampered_r)

    def test_wrong_pair_mass_is_rejected(self) -> None:
        counts = example_counts()
        counts[0] -= 1
        with self.assertRaisesRegex(ValueError, "820"):
            invariants(counts, 0)

    def test_fractional_pair_count_is_rejected(self) -> None:
        counts = example_counts()
        counts[0] -= 0.5
        counts[1] += 0.5
        with self.assertRaisesRegex(ValueError, "integers"):
            invariants(counts, 0)

    def test_noncentered_pair_counts_are_rejected(self) -> None:
        counts = dict.fromkeys(COLORS, 0)
        counts[0] = 820
        with self.assertRaisesRegex(ValueError, "sum to -82"):
            invariants(counts, 0)


if __name__ == "__main__":
    unittest.main()
