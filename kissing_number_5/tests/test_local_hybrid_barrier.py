import importlib.util
from fractions import Fraction
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "verifiers" / "verify_local_hybrid_barrier.py"
SPEC = importlib.util.spec_from_file_location(
    "verify_local_hybrid_barrier", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class LocalHybridBarrierTests(unittest.TestCase):
    def test_exact_witness(self):
        result = MODULE.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["mass"], 41)
        self.assertEqual(result["minimum_moment"], Fraction(29759, 656000))
        self.assertEqual(result["minimum_moment_degree"], 2)
        self.assertEqual(result["pfender_margin"], Fraction(4707, 20500))
        self.assertEqual(result["rank_deficit_margin"], Fraction(337, 1000))

    def test_integer_wedge_envelope(self):
        self.assertEqual(MODULE.integer_wedge_minimum(176, 41), 294)
        self.assertEqual(MODULE.integer_wedge_minimum(170, 41), 270)
        for total_degree in range(0, 206):
            quotient, remainder = divmod(total_degree, 41)
            degrees = [quotient + 1] * remainder + [quotient] * (41 - remainder)
            self.assertEqual(
                MODULE.integer_wedge_minimum(total_degree, 41),
                sum(degree * (degree - 1) // 2 for degree in degrees),
            )

    def test_threshold_boundaries_are_included(self):
        size, nodes, counts, _, _ = MODULE.load_certificate()
        self.assertEqual(size, 41)
        deep_at_point_seven, _ = MODULE.threshold_values(
            Fraction(49, 100), nodes, counts
        )
        deep_just_above = MODULE.threshold_values(
            Fraction(490001, 1000000), nodes, counts
        )[0]
        self.assertEqual(deep_at_point_seven, 176)
        self.assertEqual(deep_just_above, 170)


if __name__ == "__main__":
    unittest.main()
