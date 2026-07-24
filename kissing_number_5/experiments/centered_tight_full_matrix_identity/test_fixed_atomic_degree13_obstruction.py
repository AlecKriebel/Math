from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent


def load_verifier():
    path = HERE / "verify_fixed_atomic_degree13_obstruction.py"
    specification = importlib.util.spec_from_file_location(
        "verify_fixed_atomic_degree13_obstruction", path
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


class FixedAtomicDegreeThirteenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_verifier()
        cls.report = cls.module.verify()

    def test_exact_dual_separator(self) -> None:
        self.assertEqual(self.report["status"], "PASS")
        self.assertGreater(
            self.module.Q(self.report["minimum_orbit_slack"]),
            0,
        )
        self.assertLess(
            self.module.Q(self.report["dual_objective"]),
            0,
        )
        self.assertEqual(self.report["dual_gram_factors"], 18)

    def test_scope_is_explicitly_restricted(self) -> None:
        self.assertIn("fixed eleven-node", self.report["scope"])
        self.assertIn(
            "not a universal centered-code obstruction",
            self.report["scope"],
        )


if __name__ == "__main__":
    unittest.main()
