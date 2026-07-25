from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent


def load_verifier():
    path = HERE / "verify_conditional_identity.py"
    specification = importlib.util.spec_from_file_location(
        "verify_conditional_identity", path
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class ConditionalIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_verifier()
        cls.report = cls.module.verify()

    def test_exact_conditional_and_capacity_constraints(self) -> None:
        self.assertEqual(self.report["status"], "PASS")
        self.assertEqual(self.report["conditional_base_types_checked"], 11)
        self.assertEqual(self.report["stratified_capacity_rows"], 48)
        self.assertEqual(self.report["weighted_capacity_rows"], 2)

    def test_failure_boundary_is_strict(self) -> None:
        self.assertLess(
            self.module.Q(
                self.report["known_negative_bv_order_two_minor"]
            ),
            0,
        )
        self.assertIn("not a matrix", self.report["scope"])


if __name__ == "__main__":
    unittest.main()
