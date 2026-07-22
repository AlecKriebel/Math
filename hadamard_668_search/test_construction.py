"""Regression tests for the exact Hadamard construction helpers."""

from __future__ import annotations

import unittest

from construction import (
    pack_row,
    packed_dot,
    two_circulant_legendre,
    verify_hadamard,
)


class TwoCirculantLegendreTests(unittest.TestCase):
    def assert_hadamard(self, matrix: tuple[tuple[int, ...], ...]) -> None:
        order = len(matrix)
        self.assertTrue(all(len(row) == order for row in matrix))
        packed = tuple(pack_row(row) for row in matrix)
        for left_index, left in enumerate(packed):
            for right_index in range(left_index):
                self.assertEqual(packed_dot(left, packed[right_index], order), 0)
        verify_hadamard(matrix)

    def test_length_one_constructs_order_four(self) -> None:
        matrix = two_circulant_legendre((1,), (1,))
        self.assertEqual(len(matrix), 4)
        self.assert_hadamard(matrix)

    def test_length_three_constructs_order_eight(self) -> None:
        sequence = (-1, 1, 1)
        matrix = two_circulant_legendre(sequence, sequence)
        self.assertEqual(len(matrix), 8)
        self.assert_hadamard(matrix)

    def test_rejects_non_normalized_input(self) -> None:
        with self.assertRaises(ValueError):
            two_circulant_legendre((1, 1, 1), (-1, 1, 1))

    def test_exact_verifier_rejects_a_nonorthogonal_matrix(self) -> None:
        with self.assertRaises(ValueError):
            verify_hadamard(((1, 1), (1, 1)))


if __name__ == "__main__":
    unittest.main()
