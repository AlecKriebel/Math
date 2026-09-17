"""Regression tests of the checker. No matrix search is performed."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verify_matrix import verify


def fixture(name):
    return json.loads((ROOT / "certificates" / name).read_text())["matrix"]


class MatrixCheckerTests(unittest.TestCase):
    def setUp(self):
        self.A = fixture("source_two_rows.json")

    def test_source_control(self):
        r = verify(self.A, min_rows=2, expected_N=840)
        self.assertTrue(r["valid"])
        self.assertEqual(r["row_sums"], [840, 840])
        self.assertEqual(r["column_products"], [840] * 10)
        self.assertEqual(r["distinct_entry_count"], 20)

    def test_source_not_target_dimensions(self):
        self.assertFalse(verify(self.A)["valid"])

    def test_row_permutation(self):
        self.assertTrue(verify(self.A[::-1], min_rows=2)["valid"])

    def test_column_permutation(self):
        self.assertTrue(verify([r[::-1] for r in self.A], min_rows=2)["valid"])

    def test_wrong_declared_N(self):
        self.assertFalse(verify(self.A, min_rows=2, expected_N=841)["valid"])

    def test_float_declared_N(self):
        self.assertFalse(verify(self.A, min_rows=2, expected_N=840.0)["valid"])

    def test_bool_declared_N(self):
        self.assertFalse(verify(self.A, min_rows=2, expected_N=True)["valid"])

    def test_negative_declared_N(self):
        self.assertFalse(verify(self.A, min_rows=2, expected_N=-840)["valid"])

    def test_empty_matrix(self):
        self.assertFalse(verify([])["valid"])

    def test_empty_rows(self):
        self.assertFalse(verify([[], [], []])["valid"])

    def test_one_column(self):
        self.assertFalse(verify([[1], [2], [3]])["valid"])

    def test_one_row(self):
        self.assertFalse(verify([[1, 2, 3]])["valid"])

    def test_ragged(self):
        self.assertFalse(verify([[1,2],[3],[4,5]])["valid"])

    def test_null(self):
        self.assertFalse(verify(None)["valid"])

    def test_nonarray_row(self):
        self.assertFalse(verify([[1,2],3,[4,5]])["valid"])

    def test_zero(self):
        self.A[0][0] = 0
        self.assertFalse(verify(self.A, min_rows=2)["valid"])

    def test_negative(self):
        self.A[0][0] = -2
        self.assertFalse(verify(self.A, min_rows=2)["valid"])

    def test_float_entry(self):
        self.A[0][0] = 2.0
        self.assertFalse(verify(self.A, min_rows=2)["valid"])

    def test_boolean_entry(self):
        self.A[0][0] = True
        self.assertFalse(verify(self.A, min_rows=2)["valid"])

    def test_string_entry(self):
        self.A[0][0] = "2"
        self.assertFalse(verify(self.A, min_rows=2)["valid"])

    def test_repeated_entries_with_all_equalities(self):
        r = verify(fixture("repeated_three_rows.json"))
        self.assertTrue(r["all_sums_and_products_equal_N"])
        self.assertFalse(r["globally_distinct"])
        self.assertFalse(r["valid"])

    def test_ordinary_three_rows(self):
        r = verify(fixture("ordinary_three_rows.json"))
        self.assertEqual(r["row_sums"], [24]*3)
        self.assertEqual(r["column_products"], [840]*2)
        self.assertTrue(r["globally_distinct"])
        self.assertFalse(r["valid"])

    def test_ordinary_two_rows(self):
        r = verify(fixture("ordinary_two_rows.json"), min_rows=2)
        self.assertEqual(r["row_sums"], [26]*2)
        self.assertEqual(r["column_products"], [60]*3)
        self.assertFalse(r["valid"])

    def test_uniform_scaling_does_not_preserve_equality(self):
        r = verify(fixture("scaled_source.json"), min_rows=2)
        self.assertEqual(r["row_sums"], [1680]*2)
        self.assertEqual(r["column_products"], [3360]*10)
        self.assertTrue(r["globally_distinct"])
        self.assertFalse(r["valid"])

    def test_modified_entry(self):
        self.assertFalse(verify(fixture("corrupted_source.json"), min_rows=2)["valid"])

    def test_same_rows_wrong_columns(self):
        self.A[0][0], self.A[0][1] = self.A[0][1], self.A[0][0]
        r = verify(self.A, min_rows=2)
        self.assertTrue(r["equal_row_sums"])
        self.assertFalse(r["equal_column_products"])
        self.assertFalse(r["valid"])

    def test_same_columns_wrong_rows(self):
        self.A[0][0], self.A[1][0] = self.A[1][0], self.A[0][0]
        r = verify(self.A, min_rows=2)
        self.assertTrue(r["equal_column_products"])
        self.assertFalse(r["equal_row_sums"])
        self.assertFalse(r["valid"])

    def test_arbitrary_precision(self):
        scale = 10**100
        r = verify([[scale*x for x in row] for row in self.A], min_rows=2)
        self.assertEqual(r["row_sums"], [840*scale]*2)
        self.assertEqual(r["column_products"], [840*scale*scale]*10)
        self.assertFalse(r["valid"])

    def test_cli_source(self):
        p = subprocess.run([sys.executable, str(ROOT/'src/verify_matrix.py'),
                            str(ROOT/'certificates/source_two_rows.json'), '--min-rows', '2'],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0)
        self.assertTrue(json.loads(p.stdout)["valid"])

    def test_cli_negative(self):
        p = subprocess.run([sys.executable, str(ROOT/'src/verify_matrix.py'),
                            str(ROOT/'certificates/repeated_three_rows.json')],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertFalse(json.loads(p.stdout)["valid"])

    def test_cli_malformed_json(self):
        p = subprocess.run([sys.executable, str(ROOT/'src/verify_matrix.py'), '-'],
                           input='not json', capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertFalse(json.loads(p.stdout)["valid"])

    def test_cli_null_declared_N(self):
        p = subprocess.run([sys.executable, str(ROOT/'src/verify_matrix.py'), '-', '--min-rows', '2'],
                           input=json.dumps({"matrix": self.A, "N": None}),
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertFalse(json.loads(p.stdout)["valid"])

    def test_bad_minimum_raises(self):
        with self.assertRaises(ValueError):
            verify(self.A, min_rows=0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
