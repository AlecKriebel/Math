#!/usr/bin/env python3
"""Exhaustive small-instance semantic tests for the direct Ramsey CNF."""

from __future__ import annotations

import itertools
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

from direct_ramsey_cnf import (  # noqa: E402
    allocate_sequential_counter,
    build_direct_instance,
    canonical_counter_extension,
    clause_is_satisfied,
    degree_bounds,
    edge_for_variable,
    variable_for_edge,
)
from direct_ramsey_cnf_check import independent_counter  # noqa: E402


def direct_is_ramsey_graph(order: int, bits: tuple[bool, ...]) -> bool:
    for vertices in itertools.combinations(range(order), 5):
        values = [
            bits[variable_for_edge(order, left, right) - 1]
            for left, right in itertools.combinations(vertices, 2)
        ]
        if all(values) or not any(values):
            return False
    return True


def has_auxiliary_extension(
    clauses: tuple[tuple[int, ...], ...],
    primary: dict[int, bool],
    auxiliaries: tuple[int, ...],
) -> bool:
    for values in itertools.product((False, True), repeat=len(auxiliaries)):
        assignment = dict(primary)
        assignment.update(zip(auxiliaries, values))
        if all(clause_is_satisfied(clause, assignment) for clause in clauses):
            return True
    return False


class DirectRamseyCnfTests(unittest.TestCase):
    def test_edge_variable_mapping_is_bijective(self) -> None:
        for order in range(2, 15):
            observed = []
            for left, right in itertools.combinations(range(order), 2):
                variable = variable_for_edge(order, left, right)
                observed.append(variable)
                self.assertEqual(edge_for_variable(order, variable), (left, right))
            self.assertEqual(observed, list(range(1, math.comb(order, 2) + 1)))

    def test_degree_bounds_for_order_43(self) -> None:
        self.assertEqual(degree_bounds(43), (18, 24))
        instance = build_direct_instance(43)
        self.assertEqual(instance.primary_variable_count, 903)
        self.assertEqual(instance.five_subset_count, 962_598)
        self.assertEqual(instance.ramsey_clause_count, 1_925_196)
        self.assertEqual(instance.degree_clause_count, 126_936)
        self.assertEqual(instance.auxiliary_variable_count, 64_500)
        self.assertEqual(instance.variable_count, 65_403)
        self.assertEqual(instance.clause_count, 2_052_132)

    def test_exhaustive_sequential_counter_semantics(self) -> None:
        checked_primary_assignments = 0
        checked_counter_instances = 0
        for input_count in range(0, 5):
            positive = tuple(range(1, input_count + 1))
            signs_to_test = (
                positive,
                tuple(
                    variable if variable % 2 else -variable
                    for variable in positive
                ),
            )
            for literals in signs_to_test:
                for bound in range(-1, input_count + 2):
                    counter, _ = allocate_sequential_counter(
                        literals,
                        bound,
                        input_count + 1,
                        "exhaustive_test",
                    )
                    clauses = tuple(counter.clauses())
                    auxiliaries = tuple(
                        variable for row in counter.rows for variable in row
                    )
                    checked_counter_instances += 1
                    for bits in itertools.product(
                        (False, True), repeat=input_count
                    ):
                        primary = {
                            variable: value
                            for variable, value in enumerate(bits, start=1)
                        }
                        true_inputs = sum(
                            primary[abs(literal)] == (literal > 0)
                            for literal in literals
                        )
                        expected = true_inputs <= bound
                        actual = has_auxiliary_extension(
                            clauses, primary, auxiliaries
                        )
                        self.assertEqual(
                            actual,
                            expected,
                            (input_count, literals, bound, bits),
                        )
                        if expected:
                            witness = dict(primary)
                            witness.update(
                                canonical_counter_extension(counter, primary)
                            )
                            self.assertTrue(
                                all(
                                    clause_is_satisfied(clause, witness)
                                    for clause in clauses
                                )
                            )
                        checked_primary_assignments += 1
        self.assertEqual(checked_counter_instances, 50)
        self.assertEqual(checked_primary_assignments, 382)

    def test_exhaustive_independent_checker_counter_semantics(self) -> None:
        checked_primary_assignments = 0
        for input_count in range(0, 5):
            inputs = tuple(range(1, input_count + 1))
            for literals in (
                inputs,
                tuple(
                    variable if variable % 2 else -variable
                    for variable in inputs
                ),
            ):
                for bound in range(-1, input_count + 2):
                    clauses_list, next_variable = independent_counter(
                        literals, bound, input_count + 1
                    )
                    clauses = tuple(clauses_list)
                    auxiliaries = tuple(
                        range(input_count + 1, next_variable)
                    )
                    for bits in itertools.product(
                        (False, True), repeat=input_count
                    ):
                        primary = dict(enumerate(bits, start=1))
                        true_inputs = sum(
                            primary[abs(literal)] == (literal > 0)
                            for literal in literals
                        )
                        self.assertEqual(
                            has_auxiliary_extension(
                                clauses, primary, auxiliaries
                            ),
                            true_inputs <= bound,
                            (input_count, literals, bound, bits),
                        )
                        checked_primary_assignments += 1
        self.assertEqual(checked_primary_assignments, 382)

    def test_exhaustive_all_graphs_through_order_six(self) -> None:
        checked_graphs = 0
        for order in range(0, 7):
            instance = build_direct_instance(order)
            self.assertEqual(instance.auxiliary_variable_count, 0)
            clauses = tuple(instance.clauses())
            for bits in itertools.product(
                (False, True), repeat=instance.primary_variable_count
            ):
                assignment = {
                    variable: value
                    for variable, value in enumerate(bits, start=1)
                }
                actual = all(
                    clause_is_satisfied(clause, assignment)
                    for clause in clauses
                )
                self.assertEqual(actual, direct_is_ramsey_graph(order, bits))
                checked_graphs += 1
        self.assertEqual(checked_graphs, 33_868)

    def test_five_set_clause_pair_is_exact(self) -> None:
        instance = build_direct_instance(5)
        clauses = tuple(instance.clauses())
        self.assertEqual(len(clauses), 2)
        self.assertEqual(tuple(map(len, clauses)), (10, 10))
        self.assertEqual(clauses[0], tuple(range(-1, -11, -1)))
        self.assertEqual(clauses[1], tuple(range(1, 11)))

    def test_generation_is_deterministic(self) -> None:
        first = build_direct_instance(27)
        second = build_direct_instance(27)
        self.assertEqual(first, second)
        self.assertEqual(
            tuple(first.clauses()),
            tuple(second.clauses()),
        )


if __name__ == "__main__":
    unittest.main()
