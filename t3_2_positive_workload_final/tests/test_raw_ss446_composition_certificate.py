import unittest

import raw_ss446_composition_certificate as ss446


class RawSS446CompositionCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = ss446.certificate()

    def test_exact_incidence_and_pair_counts(self) -> None:
        self.assertEqual(self.result["raw_ss_incidences"], 446)
        self.assertEqual(self.result["distinct_ordered_support_pairs"], 322)

    def test_exact_incidence_partition(self) -> None:
        self.assertEqual(
            self.result["incidence_branch_counts"],
            {
                "active_chart_invariant": 364,
                "exact_signed_service": 4,
                "full_deficiency_zero": 60,
                "strict_positive_invariant": 18,
            },
        )
        self.assertEqual(self.result["residual_incidences"], 0)

    def test_unique_pair_partition(self) -> None:
        self.assertEqual(
            self.result["unique_pair_branch_counts"],
            {
                "active_chart_invariant": 268,
                "exact_signed_service": 4,
                "full_deficiency_zero": 32,
                "strict_positive_invariant": 18,
            },
        )

    def test_literal_service_rows(self) -> None:
        self.assertEqual(len(self.result["service_rows"]), 4)
        self.assertTrue(
            all(row["weight"] == [1, 3, 0] for row in self.result["service_rows"])
        )
        unordered = {
            frozenset((tuple(row["first"]), tuple(row["second"])))
            for row in self.result["service_rows"]
        }
        self.assertEqual(
            unordered,
            {
                frozenset(
                    (("C", "2C"), ("0", "A", "2A", "BC"))
                ),
                frozenset(
                    (("0", "C", "2C"), ("A", "2A", "BC"))
                ),
            },
        )

    def test_frozen_fingerprints(self) -> None:
        self.assertEqual(
            self.result["raw_incidence_sha256"],
            "842920b5280d96c96e49e0b0b959d548acb2ac43a5dfee4ab110346958acc45f",
        )
        self.assertEqual(
            self.result["branch_annotated_incidence_sha256"],
            "8870e74f85a50608b2f5586c87a3dc73cf825ae292df41063b77ebae7e1924e3",
        )


if __name__ == "__main__":
    unittest.main()
