import copy
import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_common_pair_capacity_stratified_dual import (
    CERTIFICATE,
    verify,
)


class CommonPairCapacityStratifiedDualTests(unittest.TestCase):
    def test_exact_dual(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertGreater(result["right_hand_side"], 0)
        self.assertTrue(
            all(value < 0 for value in result["combined_coefficients"])
        )

    def check_tamper_rejected(self, mutate):
        data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        altered = copy.deepcopy(data)
        mutate(altered)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "altered.json"
            path.write_text(json.dumps(altered), encoding="utf-8")
            with self.assertRaises(AssertionError):
                verify(path)

    def test_wrong_capacity_upper_rejected(self):
        self.check_tamper_rejected(
            lambda data: data["stratified_capacity_rows"][0].__setitem__(
                "upper", 132
            )
        )

    def test_wrong_bv_constant_rejected(self):
        self.check_tamper_rejected(
            lambda data: data["bv_scalar_directions"][1].__setitem__(
                "constant", "0"
            )
        )

    def test_wrong_farkas_value_rejected(self):
        self.check_tamper_rejected(
            lambda data: data["exact_diagnostics"].__setitem__(
                "positive_right_hand_side", "1"
            )
        )


if __name__ == "__main__":
    unittest.main()
