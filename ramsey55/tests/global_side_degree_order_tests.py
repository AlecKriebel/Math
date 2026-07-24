#!/usr/bin/env python3
"""Tests for exact side-wise degree ordering."""

from __future__ import annotations

import itertools
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

import global_side_degree_order as production
import global_side_degree_order_check as checker
from direct_ramsey_cnf import (
    allocate_sequential_counter,
    canonical_counter_extension,
)


class SideDegreeOrderTests(unittest.TestCase):
    def test_reverse_clauses_make_small_counter_exact(self) -> None:
        self.assertTrue(checker.exhaustive_reverse_semantics(6))

    def test_canonical_extensions_satisfy_reverse_clauses(self) -> None:
        counter, _ = allocate_sequential_counter(
            (1, 2, 3, 4, 5), 3, 6, "test"
        )
        reverse = tuple(production.reverse_counter_clauses(counter))
        for values in itertools.product((False, True), repeat=5):
            primary = {index + 1: value for index, value in enumerate(values)}
            assignment = dict(primary)
            assignment.update(canonical_counter_extension(counter, primary))
            self.assertTrue(
                all(
                    any(
                        assignment[abs(literal)] == (literal > 0)
                        for literal in clause
                    )
                    for clause in reverse
                )
            )

    def test_expected_side_comparator_count(self) -> None:
        counters = production.edge_counters()
        for degree in production.BRANCH_DEGREES:
            clauses = tuple(
                production.degree_order_clauses(degree, counters)
            )
            self.assertEqual(
                len(clauses), 40 * (production.ORDER - 1 - 2 * degree)
            )

    def test_plan_cross_checks_independently(self) -> None:
        plan = production.build_plan()
        self.assertEqual(
            plan["reverse_clause_count"],
            sum(
                1
                for counter in production.edge_counters()
                for _ in production.reverse_counter_clauses(counter)
            ),
        )
        self.assertEqual(
            [branch["degree"] for branch in plan["branches"]],
            list(production.BRANCH_DEGREES),
        )

    def test_checker_rejects_plan_tamper(self) -> None:
        plan = production.build_plan()
        plan["branches"][0]["degree_order_clause_count"] += 1
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            path.write_text(json.dumps(plan), encoding="utf-8")
            result = checker.check_plan(path)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "degree_order_clause_count mismatch" in error
                for error in result["errors"]
            )
        )


if __name__ == "__main__":
    unittest.main()
