import json
from pathlib import Path
import tempfile
import unittest

from verifiers import verify_anchored_local_energy_bv_barrier as MODULE


class AnchoredLocalEnergyBVBarrierTests(unittest.TestCase):
    def test_exact_barrier_moment(self):
        result = MODULE.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(
            result["off_diagonal_second_moment"],
            MODULE.Q(5767796592200083, 800000000000000),
        )
        self.assertGreater(
            result["off_diagonal_second_moment"], MODULE.Q(36, 5)
        )
        self.assertEqual(
            result["strict_excess"],
            MODULE.Q(7796592200083, 800000000000000),
        )

    def test_source_tamper_is_rejected(self):
        source = json.loads(MODULE.SOURCE_PATH.read_text())
        source["alpha"][0] = str(MODULE.Q(source["alpha"][0]) + MODULE.Q(1))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / MODULE.SOURCE_PATH.name
            path.write_text(json.dumps(source))
            with self.assertRaises(AssertionError):
                MODULE.verify(source_path=path)


if __name__ == "__main__":
    unittest.main()
