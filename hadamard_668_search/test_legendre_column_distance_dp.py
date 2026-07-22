"""Tests for the exact cyclic column-margin distance transfer DP."""

from __future__ import annotations

from itertools import product
import unittest

from legendre_333 import FIXED_PLUS_COUNTS_A, FIXED_PLUS_COUNTS_B, N
from legendre_column_distance_dp import (
    edgewise_column_distance_bounds,
    exact_column_distance_spectrum,
    independent_column_distance_spectrum,
    layered_cyclic_distance_spectrum,
    verify_fixed_margin_spectra,
)


def brute_force_layered_spectrum(
    column_weights: tuple[int, ...], row_shift: int, row_count: int
) -> tuple[int, ...]:
    masks_by_column = tuple(
        tuple(
            mask
            for mask in range(1 << row_count)
            if mask.bit_count() == weight
        )
        for weight in column_weights
    )
    result: set[int] = set()
    for masks in product(*masks_by_column):
        distance = 0
        for index, left in enumerate(masks):
            right = masks[(index + 1) % len(masks)]
            for row in range(row_count):
                distance += ((left >> row) & 1) != (
                    (right >> ((row + row_shift) % row_count)) & 1
                )
        result.add(distance)
    return tuple(sorted(result))


class ExactColumnDistanceDpTests(unittest.TestCase):
    def test_transfer_dp_matches_complete_toy_enumeration(self) -> None:
        weights = (1, 2, 1, 2)
        for row_shift in range(3):
            self.assertEqual(
                layered_cyclic_distance_spectrum(weights, row_shift, 3),
                brute_force_layered_spectrum(weights, row_shift, 3),
            )

    def test_transfer_dp_matches_all_small_profiles(self) -> None:
        checked = 0
        for row_count in range(2, 5):
            for column_count in range(1, 5):
                for weights in product(
                    range(row_count + 1), repeat=column_count
                ):
                    for row_shift in range(row_count):
                        self.assertEqual(
                            layered_cyclic_distance_spectrum(
                                weights, row_shift, row_count
                            ),
                            brute_force_layered_spectrum(
                                weights, row_shift, row_count
                            ),
                        )
                        checked += 1
        self.assertEqual(checked, 4_380)

    def test_fixed_margins_have_full_even_edgewise_spectra(self) -> None:
        for plus_counts in (FIXED_PLUS_COUNTS_A, FIXED_PLUS_COUNTS_B):
            for lag in range(1, (N + 1) // 2):
                spectrum = exact_column_distance_spectrum(plus_counts, lag)
                lower, upper = edgewise_column_distance_bounds(plus_counts, lag)
                self.assertEqual(spectrum, tuple(range(lower, upper + 1, 2)))

    def test_summary_certifies_no_hidden_tightening(self) -> None:
        self.assertEqual(
            verify_fixed_margin_spectra(),
            {
                "sequence_lag_cases_checked": 332,
                "exact_bound_improvements": 0,
                "spectra_with_even_gaps": 0,
            },
        )

    def test_independent_columns_match_complete_toy_enumeration(self) -> None:
        weights = (1, 2, 1)
        for row_shift in range(3):
            expected = {
                sum(
                    sum(
                        ((mask >> row) & 1)
                        != ((mask >> ((row + row_shift) % 3)) & 1)
                        for row in range(3)
                    )
                    for mask in masks
                )
                for masks in product(
                    *(
                        tuple(
                            mask
                            for mask in range(1 << 3)
                            if mask.bit_count() == weight
                        )
                        for weight in weights
                    )
                )
            }
            self.assertEqual(
                independent_column_distance_spectrum(weights, row_shift, 3),
                tuple(sorted(expected)),
            )


if __name__ == "__main__":
    unittest.main()
