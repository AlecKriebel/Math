from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import random
import tempfile
import unittest
from unittest import mock


HERE = Path(__file__).resolve().parent
PATH = HERE / "verify_direct_k9_triangle_extension.py"
SPEC = importlib.util.spec_from_file_location("verify_direct_k9", PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class DirectK9TriangleExtensionTests(unittest.TestCase):
    def test_bareiss_determinant_against_fraction_gaussian(self) -> None:
        def reference(matrix: tuple[tuple[int, ...], ...]) -> int:
            work = [[Q(value) for value in row] for row in matrix]
            answer = Q(1)
            for column in range(len(work)):
                pivot = next(
                    (
                        row
                        for row in range(column, len(work))
                        if work[row][column]
                    ),
                    None,
                )
                if pivot is None:
                    return 0
                if pivot != column:
                    work[column], work[pivot] = work[pivot], work[column]
                    answer = -answer
                value = work[column][column]
                answer *= value
                for other_column in range(column, len(work)):
                    work[column][other_column] /= value
                for row in range(column + 1, len(work)):
                    multiplier = work[row][column]
                    for other_column in range(column, len(work)):
                        work[row][other_column] -= (
                            multiplier * work[column][other_column]
                        )
            assert answer.denominator == 1
            return answer.numerator

        generator = random.Random(20260723)
        for size in range(1, 10):
            for _trial in range(20):
                matrix = tuple(
                    tuple(generator.randrange(-5, 6) for _ in range(size))
                    for _ in range(size)
                )
                self.assertEqual(VERIFY.determinant(matrix), reference(matrix))

    def test_exact_extension(self) -> None:
        result = VERIFY.verify()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["positive_atoms"], 51)
        self.assertEqual(
            result[
                "all_sixth_through_ninth_order_principal_determinants"
            ],
            0,
        )

    def test_tampered_weight_is_rejected(self) -> None:
        data = json.loads(VERIFY.CERTIFICATE_PATH.read_text())
        data["atoms"][0]["weight"] = str(
            Q(data["atoms"][0]["weight"]) + Q(1, 10**12)
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with mock.patch.object(VERIFY, "CERTIFICATE_PATH", path):
                with self.assertRaises(AssertionError):
                    VERIFY.verify()

    def test_tampered_edge_is_rejected(self) -> None:
        data = json.loads(VERIFY.CERTIFICATE_PATH.read_text())
        data["atoms"][0][VERIFY.EDGE_KEY][0] = 0
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data))
            with mock.patch.object(VERIFY, "CERTIFICATE_PATH", path):
                with self.assertRaises(AssertionError):
                    VERIFY.verify()


if __name__ == "__main__":
    unittest.main()
