import json
from fractions import Fraction as Q
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_common_pair_capacity_hierarchy import (
    CERTIFICATE,
    capacity_for_thresholds,
    capacity_from_p,
    verify,
)


class CommonPairCapacityHierarchyTest(unittest.TestCase):
    def test_exact_verifier(self):
        result = verify()
        self.assertEqual(
            result["local_witness_slacks"],
            (Q(-193), Q(-215), Q(-29), Q(-24)),
        )
        self.assertEqual(
            result["candidate"]["C047_residual"],
            Q(
                -346957839801844443,
                42025000000000000000,
            ),
        )

    def test_capacity_boundaries(self):
        self.assertEqual(capacity_from_p(Q(1001, 1000)), 0)
        self.assertEqual(capacity_from_p(Q(1)), 1)
        self.assertEqual(capacity_from_p(Q(751, 1000)), 1)
        self.assertEqual(capacity_from_p(Q(3, 4)), 2)
        self.assertEqual(capacity_from_p(Q(7, 10)), 2)
        self.assertEqual(capacity_from_p(Q(2, 3)), 3)
        self.assertEqual(capacity_from_p(Q(13, 20)), 3)
        self.assertEqual(capacity_from_p(Q(5, 8)), 4)
        self.assertEqual(capacity_from_p(Q(3, 5)), 4)
        self.assertEqual(capacity_from_p(Q(1, 2)), 6)
        self.assertIsNone(capacity_from_p(Q(49, 100)))
        self.assertEqual(
            capacity_for_thresholds(Q(-1), Q(1, 4)),
            (None, 0),
        )

    def test_threshold_monotonicity_samples(self):
        fixed_b = [
            capacity_for_thresholds(a, Q(1, 2))[1]
            for a in (Q(-3, 4), Q(-1, 2), Q(-1, 4), Q(0))
        ]
        self.assertEqual(fixed_b, [0, 1, 3, 6])
        # Shallower base thresholds cannot improve the bound.
        self.assertEqual(fixed_b, sorted(fixed_b))

    def test_discrete_orbit_normalization(self):
        result = verify()
        strong = next(
            row
            for row in result["candidate"]["hierarchy_rows"]
            if row["base_threshold"] == Q(-11, 25)
            and row["high_threshold"] == Q(499, 1000)
        )
        # Each unordered base-edge/third-vertex incidence gives the two
        # ordered triples (x,y,z) and (x,z,y), and alpha gives two
        # orientations per unordered base edge.
        self.assertEqual(Q(2, 41) * strong["left"], Q(438, 41))
        self.assertEqual(Q(2, 41) * strong["right"], Q(438, 41))

    def test_stored_diagnostic_tamper_is_rejected(self):
        data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        data["exact_diagnostics"]["common_pair_strong_cut"]["left"] = 220
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(AssertionError):
                verify(path)

    def test_source_hash_tamper_is_rejected(self):
        data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        data["source_audits"]["all_harmonic_witness"]["sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(AssertionError):
                verify(path)


if __name__ == "__main__":
    unittest.main()
