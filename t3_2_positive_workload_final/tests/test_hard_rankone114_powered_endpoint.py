from __future__ import annotations

import unittest

import hard_rankone114_powered_endpoint as theorem


class HardRankone114PoweredEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = theorem.certificate()

    def test_scope(self) -> None:
        self.assertEqual((self.result["incidences"], self.result["pairs"]), (114, 38))

    def test_activation_and_correction(self) -> None:
        self.assertEqual(
            self.result["activation_histogram"],
            {
                "lower_layer_activation_needed": 2,
                "lower_top_seeded": 110,
                "top_phase_activates": 2,
            },
        )
        self.assertEqual(
            self.result["correction_histogram"],
            {
                "directed_triple_adjusted_ell": 24,
                "reversible_top_adjusted_ell": 90,
            },
        )

    def test_hashes(self) -> None:
        self.assertEqual(self.result["rows_sha256"], theorem.EXPECTED_ROWS_SHA256)
        self.assertEqual(self.result["payload_sha256"], theorem.EXPECTED_PAYLOAD_SHA256)

    def test_claim_boundary(self) -> None:
        self.assertFalse(self.result["rankone114_composition_independently_audited"])
        self.assertFalse(self.result["pair_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
