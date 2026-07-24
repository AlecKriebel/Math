#!/usr/bin/env python3
"""Structural tests for the order-3 maximal-cycle constructive search."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


search = load(
    "automorphism3_maxcycle_search",
    ROOT / "src" / "automorphism3_maxcycle_search.py",
)
audit = load(
    "automorphism3_maxcycle_audit",
    ROOT / "verify" / "automorphism3_maxcycle_audit.py",
)


class Automorphism3MaxcycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.edge_variable, cls.orbits = search.edge_orbits()
        cls.signatures = search.ramsey_signatures(cls.edge_variable)

    def test_exact_formula_fingerprint(self) -> None:
        self.assertEqual(len(self.edge_variable), 903)
        self.assertEqual(len(self.orbits), search.EXPECTED_VARIABLES)
        self.assertEqual(
            Counter(map(len, self.orbits)),
            Counter({3: search.EXPECTED_VARIABLES}),
        )
        self.assertEqual(len(self.signatures), search.EXPECTED_SIGNATURES)
        self.assertEqual(
            Counter(map(len, self.signatures)),
            search.EXPECTED_SIGNATURE_HISTOGRAM,
        )
        self.assertEqual(
            search.dimacs_sha256(len(self.orbits), self.signatures),
            search.EXPECTED_DIMACS_SHA256,
        )

    def test_independent_algebraic_partition_and_formula_agree(self) -> None:
        independent_table, independent_orbits = audit.independent_edge_partition(
            43, 14
        )
        independent_signatures = audit.signatures(
            43, 5, independent_table
        )
        self.assertEqual(independent_table, self.edge_variable)
        self.assertEqual(independent_orbits, self.orbits)
        self.assertEqual(independent_signatures, self.signatures)
        self.assertEqual(
            audit.dimacs_hash(len(independent_orbits), independent_signatures),
            search.EXPECTED_DIMACS_SHA256,
        )

    def test_degree_and_complement_reduction(self) -> None:
        incident = search.fixed_vertex_variables(self.edge_variable)
        self.assertEqual(len(incident), 14)
        self.assertEqual(len(set(incident)), 14)
        for t_case, expected_degree in ((6, 18), (7, 21)):
            units = search.fixed_vertex_units(t_case, self.edge_variable)
            self.assertEqual(len(units), 14)
            self.assertEqual(sum(literal > 0 for literal in units) * 3, expected_degree)
        self.assertEqual(14 - 6, 8)
        self.assertEqual(14 - 7, 7)

    def test_side_formulas_and_gluing_variable_partition(self) -> None:
        local_orbits = {}
        local_models = {}
        expected = {
            6: (51, 3_831),
            7: (70, 8_715),
            8: (92, 17_626),
        }
        for cycle_count, (variables, clauses) in expected.items():
            orbits, _, formula = search.local_side_formula(cycle_count)
            self.assertEqual(len(orbits), variables)
            self.assertEqual(len(formula), clauses)
            local_orbits[cycle_count] = orbits
            local_models[cycle_count] = (False,) * variables
        for t_case, expected_fixed in ((6, 157), (7, 154)):
            units = search.gluing_units(
                t_case,
                local_models[t_case],
                local_models[14 - t_case],
                local_orbits,
                self.edge_variable,
            )
            self.assertEqual(len(units), expected_fixed)
            self.assertEqual(len(set(map(abs, units))), expected_fixed)
            self.assertEqual(
                search.EXPECTED_VARIABLES - expected_fixed,
                3 * t_case * (14 - t_case),
            )

    def test_side_normalizer_relabeling_is_a_variable_permutation(self) -> None:
        orbits, table, _ = search.local_side_formula(6)
        model = tuple(bool(variable & 1) for variable in range(1, len(orbits) + 1))
        transformed = search.transformed_side_model(
            model,
            orbits,
            table,
            (2, 5, 1, 4, 0, 3),
            (0, 1, 2, 0, 2, 1),
            -1,
        )
        self.assertEqual(len(transformed), len(model))
        self.assertEqual(Counter(transformed), Counter(model))


if __name__ == "__main__":
    unittest.main()
