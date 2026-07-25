from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent


def load_verifier():
    path = HERE / "verify_conditional_bv_degree12.py"
    specification = importlib.util.spec_from_file_location(
        "verify_conditional_bv_degree12", path
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class ConditionalBVDegreeTwelveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_verifier()
        cls.report = cls.module.verify()

    def test_exact_relaxation_certificate(self) -> None:
        self.assertEqual(self.report["status"], "PASS")
        self.assertEqual(self.report["conditional_rows_checked"], 45)
        self.assertEqual(self.report["stratified_capacity_rows"], 48)
        self.assertEqual(self.report["weighted_capacity_rows"], 2)
        self.assertEqual(self.report["maximum_bv_degree_verified"], 12)
        self.assertGreater(
            self.module.Q(self.report["minimum_bv_ldl_pivot"]),
            0,
        )

    def test_precise_degree_thirteen_failure(self) -> None:
        self.assertEqual(
            self.report["degree_13_negative_principal_indices"],
            [2, 7, 10],
        )
        self.assertLess(
            self.module.Q(
                self.report["degree_13_negative_principal_minor"]
            ),
            0,
        )
        self.assertIn("not a labeled matrix", self.report["scope"])


if __name__ == "__main__":
    unittest.main()
