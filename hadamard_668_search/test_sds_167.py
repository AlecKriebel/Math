from __future__ import annotations

import unittest

from construction import goethals_seidel, verify_hadamard
from sds_167 import ROW_SUM_PROFILES, validate_cyclic_sds
from verify_sds_167 import verify_payload


class CyclicSds167Tests(unittest.TestCase):
    def test_order_167_profiles(self) -> None:
        self.assertEqual(len(ROW_SUM_PROFILES), 10)
        self.assertEqual(ROW_SUM_PROFILES[0], (1, 1, 15, 21))
        self.assertEqual(ROW_SUM_PROFILES[-1], (7, 13, 15, 15))

    def test_small_exact_cyclic_sds_constructs_h12(self) -> None:
        fixture = (
            (1, 1, 1),
            (1, 1, -1),
            (1, -1, 1),
            (-1, 1, 1),
        )
        candidate = validate_cyclic_sds(fixture, 3)
        matrix = goethals_seidel(candidate)
        self.assertEqual(len(matrix), 12)
        verify_hadamard(matrix)

    def test_strict_verifier_rejects_small_fixture(self) -> None:
        fixture = (
            (1, 1, 1),
            (1, 1, -1),
            (1, -1, 1),
            (-1, 1, 1),
        )
        with self.assertRaisesRegex(ValueError, "order must be exactly 167"):
            verify_payload(
                {
                    "kind": "cyclic_sds_167",
                    "order": 3,
                    "hadamard_order": 12,
                    "row_sums": [sum(sequence) for sequence in fixture],
                    "sequences": [list(sequence) for sequence in fixture],
                }
            )


if __name__ == "__main__":
    unittest.main()
