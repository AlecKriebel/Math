import unittest

from verifiers.verify_harmonic_combination_centered_skew import verify


class HarmonicCombinationCenteredSkewTest(unittest.TestCase):
    def test_exact_rank_cut_instances(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(
            set(result["instances"]), {"(H0+5H1)/6", "H2"}
        )
        for instance in result["instances"].values():
            self.assertLess(instance["rank_residual"], 0)
            self.assertGreater(instance["outer_band_slack"], 0)
            self.assertGreater(
                abs(instance["centered_third"]),
                instance["outer_band"],
            )


if __name__ == "__main__":
    unittest.main()
