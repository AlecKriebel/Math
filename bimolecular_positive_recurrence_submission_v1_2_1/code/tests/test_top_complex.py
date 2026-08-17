import unittest
from fractions import Fraction

from bimolecular_pr.top_complex_dichotomy import (
    TopClassification,
    classify_top_complexes,
    validate_top_classification,
)


class TopComplexTests(unittest.TestCase):
    def classify_and_validate(self, complexes, weights, divergent):
        result = classify_top_complexes(complexes, weights, divergent)
        validate_top_classification(complexes, weights, divergent, result)
        return result

    def test_all_top_nonnegative_invariant(self):
        result = self.classify_and_validate(
            [(1, 0), (0, 1)],
            (Fraction(1, 2), Fraction(1, 2)),
            frozenset({0, 1}),
        )
        self.assertEqual(result.case, "all_top_invariant")

    def test_all_qJ_one_is_already_the_all_top_case(self):
        result = self.classify_and_validate(
            [(1, 0, 0), (1, 1, 0), (1, 0, 1)],
            (Fraction(1), Fraction(0), Fraction(0)),
            frozenset({0}),
        )
        self.assertEqual(result.case, "all_top_invariant")
        self.assertNotEqual(result.case, "K_mass_invariant")

    def test_two_divergent_particles(self):
        result = self.classify_and_validate(
            [(1, 1), (1, 0), (0, 0)],
            (Fraction(1, 2), Fraction(1, 2)),
            frozenset({0, 1}),
        )
        self.assertEqual(result.case, "two_divergent_availability")

    def test_unary_top(self):
        result = self.classify_and_validate(
            [(1, 0), (0, 1), (0, 0)],
            (Fraction(1), Fraction(0)),
            frozenset({0}),
        )
        self.assertEqual(result.case, "unary_top_availability")

    def test_service_availability(self):
        result = self.classify_and_validate(
            [(1, 1, 0), (0, 1, 0), (0, 0, 0)],
            (Fraction(1), Fraction(0), Fraction(0)),
            frozenset({0}),
        )
        self.assertEqual(result.case, "service_availability")

    def test_shared_service_species(self):
        result = self.classify_and_validate(
            [(1, 0, 1), (0, 1, 1), (0, 0, 0)],
            (Fraction(1, 2), Fraction(1, 2), Fraction(0)),
            frozenset({0, 1}),
        )
        self.assertEqual(result.case, "signed_invariant")

    def test_slower_divergent_weight_zero_is_retained(self):
        result = self.classify_and_validate(
            [(1, 0), (0, 1), (0, 0)],
            (Fraction(1), Fraction(0)),
            frozenset({0, 1}),
        )
        self.assertEqual(result.case, "unary_top_availability")

    def test_zero_weight_divergent_species_still_counts_for_availability(self):
        result = self.classify_and_validate(
            [(1, 1), (0, 1), (0, 0)],
            (Fraction(1), Fraction(0)),
            frozenset({0, 1}),
        )
        self.assertEqual(result.case, "two_divergent_availability")

    def test_species_absent_from_complexes(self):
        result = self.classify_and_validate(
            [(1, 0, 0), (0, 1, 0)],
            (Fraction(1, 2), Fraction(1, 2), Fraction(0)),
            frozenset({0, 1, 2}),
        )
        self.assertEqual(result.case, "all_top_invariant")

    def test_validator_rejects_false_availability_witness(self):
        complexes = [(1, 0), (0, 0)]
        weights = (Fraction(1), Fraction(0))
        false_certificate = TopClassification(
            "unary_top_availability",
            ((1, 0),),
            ((1, 0), (1, 0)),
        )
        with self.assertRaises(AssertionError):
            validate_top_classification(
                complexes,
                weights,
                frozenset({0}),
                false_certificate,
            )

    def test_validator_rejects_false_invariant(self):
        complexes = [(1, 0), (0, 0)]
        weights = (Fraction(1), Fraction(0))
        false_certificate = TopClassification(
            "signed_invariant",
            ((1, 0),),
            (Fraction(1), Fraction(0)),
        )
        with self.assertRaises(AssertionError):
            validate_top_classification(
                complexes,
                weights,
                frozenset({0}),
                false_certificate,
            )

    def test_validator_rejects_constant_invariant_with_wrong_divergent_sign(self):
        complexes = [(1, 0), (0, 1)]
        weights = (Fraction(1, 2), Fraction(1, 2))
        false_certificate = TopClassification(
            "signed_invariant",
            ((0, 1), (1, 0)),
            (Fraction(-1), Fraction(-1)),
        )
        with self.assertRaisesRegex(AssertionError, "negative on a divergent"):
            validate_top_classification(
                complexes,
                weights,
                frozenset({0, 1}),
                false_certificate,
            )

    def test_validator_rejects_removed_redundant_case(self):
        false_certificate = TopClassification(
            "K_mass_invariant",
            ((1, 0), (1, 1)),
            frozenset({0}),
        )
        with self.assertRaisesRegex(AssertionError, "unknown top-complex case"):
            validate_top_classification(
                [(1, 0), (1, 1)],
                (Fraction(1), Fraction(0)),
                frozenset({0}),
                false_certificate,
            )

    def test_validator_rejects_weight_support_outside_divergent_set(self):
        false_certificate = TopClassification(
            "unary_top_availability",
            ((1, 0),),
            ((1, 0), (0, 0)),
        )
        with self.assertRaisesRegex(ValueError, "support"):
            validate_top_classification(
                [(1, 0), (0, 0)],
                (Fraction(1), Fraction(0)),
                frozenset(),
                false_certificate,
            )


if __name__ == "__main__":
    unittest.main()
