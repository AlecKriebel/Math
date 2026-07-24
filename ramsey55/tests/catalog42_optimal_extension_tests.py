#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

from catalog42_optimal_extension_certificate import (  # noqa: E402
    extend_graph,
    extension_constraints,
    homogeneous_five_sets,
    model_cost,
    parse_model,
)
from catalog42_optimal_extension_check import (  # noqa: E402
    extension_constraints as independent_constraints,
)
from graph_io import decode_graph6  # noqa: E402


MODELS = {
    42: [
        "111111111011010000110000001110010111100000",
        "111111111011000000110000001110010111100000",
    ],
    256: [
        "111111111000010111001000011111101000000000",
        "111111111000010111001000010111101000000000",
    ],
}


class Catalog42OptimalExtensionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lines = [
            line.strip()
            for line in (ROOT / "data" / "r55_42some.g6")
            .read_text(encoding="ascii")
            .splitlines()
            if line.strip() and not line.startswith("#")
        ]

    def test_independent_constraint_reconstruction(self) -> None:
        for line_number, expected_count in [(42, 2318), (256, 2331)]:
            core = decode_graph6(self.lines[line_number - 1])
            production = extension_constraints(core)
            independent = independent_constraints(core)
            self.assertEqual(production, independent)
            self.assertEqual(len(production), expected_count)

    def test_recorded_models_have_exactly_two_full_conflicts(self) -> None:
        for line_number, bitstrings in MODELS.items():
            core = decode_graph6(self.lines[line_number - 1])
            constraints = extension_constraints(core)
            for bits in bitstrings:
                model = parse_model(bits, 42)
                self.assertEqual(model_cost(model, constraints), 2)
                conflicts = homogeneous_five_sets(extend_graph(core, model))
                self.assertEqual(len(conflicts), 2)
                self.assertTrue(all(42 in vertices for _, vertices in conflicts))
                violated = [
                    (kind, vertices + (42,))
                    for kind, vertices, clause in constraints
                    if not any(
                        model[abs(literal) - 1] == (literal > 0)
                        for literal in clause
                    )
                ]
                self.assertEqual(violated, conflicts)


if __name__ == "__main__":
    unittest.main()
