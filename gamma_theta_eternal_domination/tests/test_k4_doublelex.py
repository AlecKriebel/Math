from __future__ import annotations

import ast
from hashlib import sha256
from itertools import product
from pathlib import Path
import unittest

from search import k4_doublelex


CAMPAIGN_ROOT = Path(__file__).resolve().parents[1]
PARENT_PATH = (
    CAMPAIGN_ROOT / "instances/order12_k4_connected_parent/instance.cnf"
)
SOURCE_PATH = CAMPAIGN_ROOT / "src/search/k4_doublelex.py"


class K4DoubleLexTests(unittest.TestCase):
    def test_eight_bit_comparator_truth_table(self) -> None:
        clauses = k4_doublelex.comparator_clauses(0, 1)
        left_variables = tuple(
            k4_doublelex._edge(0, outer) for outer in k4_doublelex.OUTER
        )
        right_variables = tuple(
            k4_doublelex._edge(1, outer) for outer in k4_doublelex.OUTER
        )
        for assignment in product((False, True), repeat=16):
            values = dict(
                zip(
                    left_variables + right_variables,
                    assignment,
                    strict=True,
                )
            )
            observed = all(
                any(
                    values[abs(literal)] == (literal > 0)
                    for literal in clause
                )
                for clause in clauses
            )
            expected = assignment[:8] <= assignment[8:]
            self.assertEqual(observed, expected, assignment)

    def test_exact_parent_and_suffix(self) -> None:
        parent = PARENT_PATH.read_bytes()
        output = k4_doublelex.build_doublelex_payload(parent)
        parent_first_newline = parent.index(b"\n")
        output_first_newline = output.index(b"\n")
        self.assertEqual(
            output[:output_first_newline],
            (
                f"p cnf {k4_doublelex.DOUBLELEX_VARIABLE_COUNT} "
                f"{k4_doublelex.DOUBLELEX_CLAUSE_COUNT}"
            ).encode("ascii"),
        )
        self.assertEqual(
            output[output_first_newline + 1 :][
                : len(parent) - parent_first_newline - 1
            ],
            parent[parent_first_newline + 1 :],
        )
        lines = output.decode("ascii").splitlines()
        self.assertEqual(
            len(lines), k4_doublelex.DOUBLELEX_CLAUSE_COUNT + 1
        )
        literal_count = sum(len(line.split()) - 1 for line in lines[1:])
        self.assertEqual(
            literal_count, k4_doublelex.DOUBLELEX_LITERAL_COUNT
        )
        self.assertEqual(
            sha256(output).hexdigest(),
            "14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7",
        )

    def test_parent_mutations_are_rejected(self) -> None:
        parent = PARENT_PATH.read_bytes()
        mutated = bytearray(parent)
        mutated[-3] = ord("1") if mutated[-3] != ord("1") else ord("2")
        with self.assertRaises(ValueError):
            k4_doublelex.build_doublelex_payload(bytes(mutated))
        with self.assertRaises(ValueError):
            k4_doublelex.build_doublelex_payload(parent + b"c extra\n")

    def test_module_imports_no_campaign_encoder_or_runner(self) -> None:
        tree = ast.parse(SOURCE_PATH.read_text(encoding="utf-8"))
        forbidden = {
            "synthesis_k4",
            "search.k4_production",
            "verifier_k4_aggregate",
        }
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        self.assertTrue(forbidden.isdisjoint(imported), imported)


if __name__ == "__main__":
    unittest.main()
