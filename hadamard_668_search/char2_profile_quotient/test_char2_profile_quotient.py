#!/usr/bin/env python3
"""Dependency-free tests for the characteristic-two profile quotient."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

import verify_char2_profile_quotient as quotient

SEARCH_ROOT = Path(__file__).resolve().parent.parent
SHELL_TWO = SEARCH_ROOT / "shell_two_exact"
sys.path.insert(0, str(SHELL_TWO))
sys.path.insert(0, str(SEARCH_ROOT))

from verify_shell_two_exact_orbits import CANDIDATES  # noqa: E402
from verify_shell_two_partition_theory import (  # noqa: E402
    actual_factor,
    profile_value,
)


class CharacteristicTwoProfileTests(unittest.TestCase):
    def test_f4_field(self) -> None:
        for value in range(4):
            self.assertEqual(quotient.f4_multiply(value, 1), value)
            self.assertEqual(quotient.f4_square(quotient.f4_square(value)), value)
        for value in (1, 2, 3):
            self.assertEqual(
                quotient.f4_multiply(value, quotient.f4_square(value)), 1
            )
        self.assertEqual(tuple(map(quotient.f4_trace, range(4))), (0, 0, 1, 1))

    def test_geometry_and_opposites(self) -> None:
        self.assertEqual(len(quotient.CLASSES), 12)
        for index in range(6):
            self.assertEqual(
                {-value % quotient.P for value in quotient.CLASSES[index]},
                set(quotient.CLASSES[index + 6]),
            )

    def test_factorization(self) -> None:
        audit = quotient.factor_audit()
        self.assertEqual(audit["algebra"], "F_4 x F_(4^6) x F_(4^6)")
        self.assertEqual(audit["star_class_shift"], 5)

    def test_actual_assignment_api(self) -> None:
        zero = (0,) * 12
        result = quotient.check_profile_assignment(zero, zero)
        self.assertTrue(result["passes_unitary_quotient"])
        self.assertTrue(result["nonzero_lags_hold"])
        self.assertTrue(result["zero_lag_holds"])
        self.assertTrue(result["trivial_factor_holds"])
        altered = (1,) + zero[1:]
        self.assertFalse(
            quotient.check_profile_assignment(altered, zero)[
                "passes_unitary_quotient"
            ]
        )

    def test_assignment_api_checks_all_factors_without_optional_pins(self) -> None:
        # This pair has zero nonzero-lag signature, but its odd support and
        # augmentation violate the zero-lag and trivial factors.  It guards
        # against silently treating only the six displayed lags as unitary.
        a = (1, 3, 2, 1, 0, 1, 0, 3, 1, 0, 0, 2)
        b = (2, 0, 1, 3, 1, 0, 1, 3, 2, 2, 0, 2)
        result = quotient.check_profile_assignment(a, b)
        self.assertTrue(result["nonzero_lags_hold"])
        self.assertFalse(result["zero_lag_holds"])
        self.assertFalse(result["trivial_factor_holds"])
        self.assertFalse(result["passes_unitary_quotient"])
        self.assertFalse(result["passes_all_requested_gates"])

    def test_eisenstein_reduction_api(self) -> None:
        zero = ((0, 0),) * 12
        result = quotient.check_eisenstein_profile(zero, zero)
        self.assertTrue(result["passes_unitary_quotient"])
        self.assertEqual(quotient.reduce_eisenstein((3, -5)), 3)

    def test_five_exact_profile_representatives(self) -> None:
        for _, _, target, identifiers_a, identifiers_b in CANDIDATES:
            words = []
            for channel, identifiers in enumerate((identifiers_a, identifiers_b)):
                word = []
                for class_index, identifier in enumerate(identifiers):
                    factor = actual_factor(channel, class_index)
                    value = profile_value(identifier)
                    word.append((factor * value[0], factor * value[1]))
                words.append(tuple(word))
            result = quotient.check_eisenstein_profile(
                words[0],
                words[1],
                target_aggregate=quotient.reduce_aggregate_target(target),
                high_count=2,
            )
            self.assertTrue(result["passes_all_requested_gates"])

    def test_trace_dependency_on_target_fixtures(self) -> None:
        # Deterministic assignments with the five admissible aggregates.
        for aggregate_a, aggregate_b in ((3, 0), (1, 3), (1, 2), (2, 0), (0, 0)):
            a = [0] * 12
            b = [0] * 12
            if aggregate_a:
                a[:4] = (aggregate_a, 1, 2, 3)
            if aggregate_b:
                b[:4] = (aggregate_b, 1, 2, 3)
            result = quotient.check_profile_assignment(a, b)
            # General residuals need not vanish, but fixed augmentation and
            # unit zero-lag force their six traces to sum to zero.
            self.assertEqual(result["aggregate"], (aggregate_a, aggregate_b))
            self.assertEqual(result["total_support"] % 2, 0)
            self.assertEqual(result["trace_dependency"], 0)

    def test_certificate(self) -> None:
        certificate = quotient.verify_certificate()
        self.assertEqual(
            sum(row["multiplicity"] for row in certificate["target_residue_types"]),
            22,
        )
        for row in certificate["target_residue_types"]:
            for high in range(3):
                numerator = row["matches"][f"h{high}"]
                denominator = row["ambient"][f"h{high}"]
                self.assertGreater(numerator, 0)
                self.assertGreater(denominator, numerator)
                self.assertAlmostEqual(denominator / numerator, 2048, delta=1)


if __name__ == "__main__":
    unittest.main()
