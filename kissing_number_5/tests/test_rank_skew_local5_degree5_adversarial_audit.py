import copy
from fractions import Fraction as Q
from itertools import combinations, product
import json
from pathlib import Path
import tempfile
import unittest

from verifiers.verify_local5_degree5_exact_separator import (
    verify as verify_separator,
)
from verifiers.verify_local5_degree5_necessary_rank_separator import (
    CERTIFICATE,
)


def trace_moments(matrix):
    size = len(matrix)
    trace_one = sum(matrix[i][i] for i in range(size))
    trace_two = sum(
        matrix[i][j] * matrix[j][i]
        for i in range(size)
        for j in range(size)
    )
    trace_three = sum(
        matrix[i][j] * matrix[j][k] * matrix[k][i]
        for i in range(size)
        for j in range(size)
        for k in range(size)
    )
    return trace_one, trace_two, trace_three


def centered_skew_residual(matrix, rank_bound):
    trace_one, trace_two, trace_three = trace_moments(matrix)
    variance = trace_two - trace_one**2 / rank_bound
    centered_third = (
        trace_three
        - Q(3, rank_bound) * trace_one * trace_two
        + Q(2, rank_bound**2) * trace_one**3
    )
    residual = (
        (rank_bound - 2) ** 2 * variance**3
        - rank_bound
        * (rank_bound - 1)
        * centered_third**2
    )
    return variance, centered_third, residual


class RankSkewLocal5AdversarialAuditTest(unittest.TestCase):
    def test_universal_rank_cuts_on_exact_d5_code(self):
        # Store sqrt(2) times each D5 root.  Inner products are then
        # integer dot products divided by two, so the Gram matrix is exact.
        roots = []
        for first, second in combinations(range(5), 2):
            for first_sign, second_sign in product((-1, 1), repeat=2):
                vector = [0] * 5
                vector[first] = first_sign
                vector[second] = second_sign
                roots.append(vector)
        gram = [
            [
                Q(sum(a * b for a, b in zip(left, right)), 2)
                for right in roots
            ]
            for left in roots
        ]
        self.assertEqual(len(gram), 40)
        self.assertTrue(all(gram[i][i] == 1 for i in range(40)))
        self.assertEqual(
            max(gram[i][j] for i in range(40) for j in range(i)),
            Q(1, 2),
        )

        h01 = [
            [Q(1, 6) + Q(5, 6) * entry for entry in row]
            for row in gram
        ]
        h2 = [
            [(5 * entry**2 - 1) / 4 for entry in row]
            for row in gram
        ]

        # The rank-six instance deliberately exercises the V=0 degeneracy.
        self.assertEqual(
            centered_skew_residual(h01, 6),
            (Q(0), Q(0), Q(0)),
        )
        variance, centered_third, residual = (
            centered_skew_residual(h2, 14)
        )
        self.assertEqual(variance, Q(125, 28))
        self.assertEqual(centered_third, Q(1875, 784))
        self.assertEqual(residual, Q(10546875, 896))
        self.assertGreater(residual, 0)

    def test_rejects_reversal_of_outer_band_direction(self):
        data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        data["rank_band_mode"] = "inner"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(AssertionError):
                verify_separator(path)

    def test_rejects_corrupted_active_basis(self):
        data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        data["basic_triple_indices"] = copy.copy(
            data["basic_triple_indices"]
        )
        data["basic_triple_indices"][0] = (
            data["basic_triple_indices"][1]
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(AssertionError):
                verify_separator(path)


if __name__ == "__main__":
    unittest.main()
