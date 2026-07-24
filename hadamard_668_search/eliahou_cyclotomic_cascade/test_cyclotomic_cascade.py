#!/usr/bin/env python3
"""Focused tests for the Eliahou cyclotomic support cascade."""

from __future__ import annotations

import json
from pathlib import Path
from random import Random
import subprocess
import tempfile
import unittest

import verify_cyclotomic_cascade as cascade


def negacyclic_norm(row: tuple[int, ...]) -> tuple[int, ...]:
    modulus = len(row)
    result = [0] * modulus
    for left, left_value in enumerate(row):
        for right, right_value in enumerate(row):
            exponent = left - right
            sign = 1
            if exponent < 0:
                exponent += modulus
                sign = -1
            result[exponent] += sign * left_value * right_value
    return tuple(result)


class CyclotomicCascadeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.expected = json.loads(
            cascade.EXPECTED_PATH.read_text(encoding="utf-8")
        )

    def test_canonical_case_order(self) -> None:
        labels = [
            f"{block}{index}" for block, index in cascade.canonical_cases()
        ]
        self.assertEqual(labels, self.expected["case_labels"])
        self.assertEqual(len(labels), 30)

    def test_independent_phi4_census(self) -> None:
        counts, joins = cascade.independent_phi4_census()
        self.assertEqual(counts, self.expected["phi4_support_counts"])
        self.assertEqual(
            joins, self.expected["phi4_joined_signature_counts"]
        )

    def test_refined_gaussian_frontier_census(self) -> None:
        actual = cascade.refined_gaussian_frontier_census()
        self.assertEqual(
            actual, self.expected["refined_gaussian_frontier"]
        )
        collision = actual["collision"]
        self.assertEqual(collision["common_coarse_state"], [1, 2])
        self.assertNotEqual(
            collision["support_a_mod6_removal"],
            collision["support_b_mod6_removal"],
        )

    def test_norm_reduction_is_a_ring_homomorphism(self) -> None:
        rng = Random(6684212)
        for modulus in (2, 6, 14):
            for _ in range(12):
                row = tuple(rng.randrange(-3, 4) for _ in range(42))
                reduced_row = cascade.reduce_negacyclic(row, modulus)
                direct = negacyclic_norm(reduced_row)
                reduced_norm = cascade.reduce_negacyclic(
                    negacyclic_norm(row), modulus
                )
                self.assertEqual(direct, reduced_norm)

    def test_cpp_algebra_self_test(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="h668-cyclotomic-test-"
        ) as temporary:
            binary = Path(temporary) / "audit"
            cascade.compile_engine(binary)
            completed = subprocess.run(
                [str(binary), "--self-test"],
                check=True,
                stdout=subprocess.PIPE,
                text=True,
            )
        self.assertIn("PASS", completed.stdout)


if __name__ == "__main__":
    unittest.main()
