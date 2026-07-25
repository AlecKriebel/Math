import copy
import json
from pathlib import Path
import tempfile
import unittest

try:
    from . import check_results
except ImportError:  # Support direct execution from this directory.
    import check_results


class TightFrameRound8Tests(unittest.TestCase):
    def test_all_artifacts(self):
        result = check_results.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["cyclic_pairs_checked"], 190)
        self.assertEqual(result["cyclic_feasible_pairs"], 0)
        self.assertEqual(result["cyclic_switchable_pairs"], 0)
        self.assertFalse(result["d5_partition_into_eight_bases"])
        self.assertGreater(
            result["best_general_maximum_inner_product"], 0.5
        )

    def test_coordinate_tamper_is_rejected(self):
        data = json.loads(check_results.RESULT_PATH.read_text())
        tampered = copy.deepcopy(data)
        tampered["best_general"]["coordinates"][0][0] += 0.01
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(tampered))
            with self.assertRaises(AssertionError):
                check_results.verify(path)

    def test_cyclic_sign_switch_witness_tamper_is_rejected(self):
        data = json.loads(check_results.checker.RESULT_PATH.read_text())
        tampered = copy.deepcopy(data)
        witness = tampered["pairs"][0][
            "sign_switch_obstruction_difference"
        ]
        tampered["pairs"][0]["sign_switch_obstruction_difference"] = (
            witness % 20 + 1
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered-cyclic.json"
            path.write_text(json.dumps(tampered))
            with self.assertRaises(AssertionError):
                check_results.checker.verify(path)


if __name__ == "__main__":
    unittest.main()
