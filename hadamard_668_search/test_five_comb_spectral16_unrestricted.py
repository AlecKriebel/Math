#!/usr/bin/env python3
"""Checks for the primitive-16th-root common-type relaxation."""

from __future__ import annotations

import cmath
import unittest

from check_five_comb_mub_reductions import (
    QUARTETS,
    SHIFTS,
    VECTORS,
    position_incidence,
)
from search_five_comb_spectral16_unrestricted import (
    FULL_PROJECTIVE_SLOT_STATES,
    FULL_MOD4_TARGET,
    ROOT_ORDERS,
    build_model,
    full_mod4_syndrome,
    root_weight,
    spectral_norm_coefficients,
)
from search_five_comb_unrestricted_projective_cp_sat import scalar_carrier


class Spectral16Tests(unittest.TestCase):
    def test_exact_coordinates_match_complex_evaluation(self) -> None:
        sequences = (
            tuple(1 if (7 * index + 2) % 11 < 6 else -1 for index in range(84)),
            tuple(1 if (5 * index + 1) % 13 < 7 else -1 for index in range(84)),
            tuple(1 if (9 * index + 3) % 17 < 8 else -1 for index in range(83)),
            tuple(1 if (4 * index + 6) % 19 < 10 else -1 for index in range(83)),
        )
        for order in ROOT_ORDERS:
            coefficients = spectral_norm_coefficients(sequences, order)
            if order == 1:
                reconstructed = complex(coefficients[0])
                root = 1.0 + 0.0j
            else:
                root = cmath.exp(2j * cmath.pi / order)
                reconstructed = sum(
                    coefficient * root**power
                    for power, coefficient in enumerate(coefficients)
                )
            direct = sum(
                abs(
                    sum(
                        coefficient * root**position
                        for position, coefficient in enumerate(sequence)
                    )
                )
                ** 2
                for sequence in sequences
            )
            self.assertAlmostEqual(reconstructed.real, direct, places=7)
            self.assertAlmostEqual(reconstructed.imag, 0.0, places=7)

    def test_full_incidence_is_type_orientation_independent(self) -> None:
        for quartet in QUARTETS:
            for slot, shift in enumerate(SHIFTS):
                for label, vector in enumerate(VECTORS):
                    expected = FULL_PROJECTIVE_SLOT_STATES[slot][label]
                    for carrier_type in range(8):
                        carrier = scalar_carrier(
                            quartet, slot, carrier_type
                        )
                        for orientation in (-1, 1):
                            actual = 0
                            for row in range(4):
                                for position, coefficient in carrier.items():
                                    if (
                                        orientation
                                        * vector[row]
                                        * coefficient
                                        < 0
                                    ):
                                        actual ^= position_incidence(
                                            row, position
                                        )
                            self.assertEqual(actual, expected)

    def test_root_weights_are_exact_power_basis_vectors(self) -> None:
        for order in ROOT_ORDERS:
            root = (
                1.0 + 0.0j
                if order == 1
                else cmath.exp(2j * cmath.pi / order)
            )
            for position in range(-32, 33):
                weight = root_weight(order, position)
                reconstructed = sum(
                    coefficient * root**power
                    for power, coefficient in enumerate(weight)
                )
                self.assertAlmostEqual(
                    reconstructed.real, (root**position).real, places=12
                )
                self.assertAlmostEqual(
                    reconstructed.imag, (root**position).imag, places=12
                )

    def test_model_is_valid(self) -> None:
        model, *_ = build_model(39, ROOT_ORDERS)
        self.assertEqual(model.validate(), "")

    def test_known_low_root_witness_has_physical_mod4_fiber(self) -> None:
        labels = (0, 4, 5, 1, 2, 6, 7, 3)
        holes = (0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1)
        self.assertEqual(
            full_mod4_syndrome(labels, holes),
            FULL_MOD4_TARGET,
        )


if __name__ == "__main__":
    unittest.main()
