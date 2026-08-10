from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import one_active_phase_shape as shape


class OneActivePhaseShapeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = shape.certificate()

    def test_candidate_scope(self):
        self.assertEqual(self.result["candidate_pairs"], 1227)
        self.assertEqual(self.result["candidate_incidences"], 3297)

    def test_only_countable_shape_is_one_dimensional_open(self):
        self.assertEqual(self.result["wholly_top_incidences"], 222)
        self.assertEqual(self.result["wholly_top_pairs"], 74)
        self.assertEqual(
            self.result["only_wholly_top_shape"],
            "one-dimensional open pair {0,U}",
        )
        self.assertTrue(
            all(shape._is_open_pair(row) for row in self.result["rows"])
        )

    def test_certificate_is_claim_neutral(self):
        self.assertFalse(self.result["analytic_theorem_certified"])
        self.assertEqual(
            self.result["rows_sha256"],
            shape.EXPECTED_ROWS_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
