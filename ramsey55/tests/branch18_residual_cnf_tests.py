#!/usr/bin/env python3
"""Semantic tests for compact branch-18 residual formulas."""

from __future__ import annotations

import itertools
import random
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from branch18_residual_cnf import (  # noqa: E402
    A,
    B,
    PRIMARY_COUNT,
    build_residual,
)
from direct_ramsey_cnf import clause_is_satisfied  # noqa: E402


LINE1 = "W?CX@DDWc[PJUtlYnHDtAdeIhSYZDYn`iQeY[NWNKON|ef?"


def direct_valid(adjacency: list[int]) -> bool:
    degrees = [neighbors.bit_count() for neighbors in adjacency]
    if not all(18 <= degree <= 24 for degree in degrees):
        return False
    for vertices in itertools.combinations(range(43), 5):
        edges = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        if edges in (0, 10):
            return False
    return True


class Branch18ResidualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.instance = build_residual(LINE1)

    def test_layout(self) -> None:
        self.assertEqual(self.instance.primary_variable_count, PRIMARY_COUNT)
        self.assertEqual(PRIMARY_COUNT, 585)
        self.assertEqual(len(self.instance.counters), 84)
        self.assertGreater(len(self.instance.ramsey_clauses), 0)
        self.assertEqual(
            len(set(self.instance.ramsey_clauses)),
            len(self.instance.ramsey_clauses),
        )

    @staticmethod
    def _counters_accept(counters, primary) -> bool:
        full = dict(primary)
        for counter in counters:
            from direct_ramsey_cnf import canonical_counter_extension

            full.update(canonical_counter_extension(counter, full))
        return all(
            clause_is_satisfied(clause, full)
            for counter in counters
            for clause in counter.clauses()
        )

    def test_random_component_semantics_against_direct_graph(self) -> None:
        generator = random.Random(20260724)
        ramsey_clauses = self.instance.ramsey_clauses
        for _ in range(12):
            primary = {
                variable: bool(generator.getrandbits(1))
                for variable in range(1, PRIMARY_COUNT + 1)
            }
            adjacency = self.instance.primary_adjacency(primary)

            residual_ramsey_valid = all(
                clause_is_satisfied(clause, primary)
                for clause in ramsey_clauses
            )
            direct_ramsey_valid = True
            for vertices in itertools.combinations(range(43), 5):
                edges = sum(
                    (adjacency[left] >> right) & 1
                    for left, right in itertools.combinations(vertices, 2)
                )
                if edges in (0, 10):
                    direct_ramsey_valid = False
                    break
            self.assertEqual(residual_ramsey_valid, direct_ramsey_valid)

            degree_acceptance: list[bool] = []
            for index in range(0, len(self.instance.counters), 2):
                degree_acceptance.append(
                    self._counters_accept(
                        self.instance.counters[index : index + 2], primary
                    )
                )
            direct_degree_acceptance = [
                18 <= adjacency[vertex].bit_count() <= 24
                for vertex in (*A, *B)
            ]
            self.assertEqual(degree_acceptance, direct_degree_acceptance)

    def test_A_counter_boundaries_16_17_23_24(self) -> None:
        pair_to_variable = self.instance.pair_to_variable()
        for offset, vertex in enumerate(A):
            counters = self.instance.counters[2 * offset : 2 * offset + 2]
            incident = [
                pair_to_variable[tuple(sorted((vertex, other)))]
                for other in (*A, *B)
                if other != vertex
            ]
            self.assertEqual(len(incident), 41)
            for count in (16, 17, 23, 24):
                primary = {
                    variable: index < count
                    for index, variable in enumerate(incident)
                }
                self.assertEqual(
                    self._counters_accept(counters, primary),
                    17 <= count <= 23,
                )

    def test_B_counter_lower_and_upper_boundaries(self) -> None:
        pair_to_variable = self.instance.pair_to_variable()
        first_B_counter = 2 * len(A)
        catalog_degrees = self.instance.catalog_degree_sequence
        # The stored sequence is sorted and line 1 has degrees 9,10,11, so
        # exercise all three distinct lower/upper pairs represented.
        tested: set[int] = set()
        raw_catalog = __import__(
            "branch18_residual_cnf", fromlist=["decode_graph6_order24"]
        ).decode_graph6_order24(self.instance.catalog_graph6)
        for offset, vertex in enumerate(B):
            q = raw_catalog[offset].bit_count()
            if q in tested:
                continue
            tested.add(q)
            counters = self.instance.counters[
                first_B_counter + 2 * offset :
                first_B_counter + 2 * offset + 2
            ]
            cross = [pair_to_variable[(left, vertex)] for left in A]
            lower = q - 5
            upper = q + 1
            for count in (lower - 1, lower, upper, upper + 1):
                primary = {
                    variable: index < count
                    for index, variable in enumerate(cross)
                }
                self.assertEqual(
                    self._counters_accept(counters, primary),
                    lower <= count <= upper,
                )
        self.assertEqual(tested, {9, 10, 11})

    def test_all_zero_and_all_one_rejected(self) -> None:
        clauses = tuple(self.instance.clauses())
        for value in (False, True):
            primary = {
                variable: value
                for variable in range(1, PRIMARY_COUNT + 1)
            }
            full = self.instance.canonical_extension(primary)
            self.assertFalse(
                all(clause_is_satisfied(clause, full) for clause in clauses)
            )


if __name__ == "__main__":
    unittest.main()
