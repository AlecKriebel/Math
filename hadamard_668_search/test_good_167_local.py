from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from verify_good_167_local import verify_local_checkpoint


HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "output" / "good_167_local_smoke.json"


class Good167LocalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(FIXTURE.read_text())

    def test_local_checkpoint_is_verified_as_nonexact(self) -> None:
        self.assertEqual(
            verify_local_checkpoint(self.payload),
            {
                "energy": 1928,
                "bad_lags": 70,
                "max_abs_quarter": 10,
                "s_weight": 43,
            },
        )

    def test_mask_and_residual_tampering_are_rejected(self) -> None:
        wrong_s = copy.deepcopy(self.payload)
        wrong_s["s_mask"] = "0x" + format(int(wrong_s["s_mask"], 16) ^ 2, "021x")
        with self.assertRaisesRegex(ValueError, "S is not C xor D"):
            verify_local_checkpoint(wrong_s)

        wrong_residual = copy.deepcopy(self.payload)
        wrong_residual["quarter_residuals"][17] += 1
        with self.assertRaisesRegex(ValueError, "quarter_residuals"):
            verify_local_checkpoint(wrong_residual)

    def test_exact_firewall_and_strict_types(self) -> None:
        mislabeled = copy.deepcopy(self.payload)
        mislabeled["exact"] = True
        with self.assertRaisesRegex(ValueError, "nonexact near misses"):
            verify_local_checkpoint(mislabeled)

        boolean_energy = copy.deepcopy(self.payload)
        boolean_energy["energy"] = True
        with self.assertRaisesRegex(ValueError, "energy must be an integer"):
            verify_local_checkpoint(boolean_energy)

    def test_noncanonical_mask_is_rejected(self) -> None:
        shortened = copy.deepcopy(self.payload)
        shortened["a_mask"] = shortened["a_mask"][:2] + shortened["a_mask"][3:]
        with self.assertRaisesRegex(ValueError, "canonical fixed-width"):
            verify_local_checkpoint(shortened)


if __name__ == "__main__":
    unittest.main()
