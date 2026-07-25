from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent


def load_verifier():
    path = HERE / "verify_sign_rank_counterexample.py"
    specification = importlib.util.spec_from_file_location(
        "verify_sign_rank_counterexample", path
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class SignRankCounterexampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = load_verifier().verify()

    def test_exact_rank_counterexample(self) -> None:
        self.assertEqual(self.report["status"], "PASS")
        self.assertEqual(self.report["matrix_order"], 41)
        self.assertEqual(self.report["w_off_diagonal_values"], [0, 2])
        self.assertEqual(self.report["m_rank"], 17)
        self.assertEqual(self.report["m_inertia"], [1, 16, 24])
        self.assertEqual(self.report["rank_half_bound_refuted_by"], 4)

    def test_common_source_is_separated(self) -> None:
        separator = self.report["common_source_separator"]
        self.assertEqual(separator["h2_trace_square_upper"], "923/8")
        self.assertEqual(separator["h2_rank_trace_lower"], "1681/14")
        self.assertEqual(separator["gap"], "263/56")

    def test_scope_does_not_overclaim(self) -> None:
        self.assertIn("not a spherical-code Gram matrix", self.report["scope"])


if __name__ == "__main__":
    unittest.main()
