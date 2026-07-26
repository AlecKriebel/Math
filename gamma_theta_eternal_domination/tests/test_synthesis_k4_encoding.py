from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from itertools import combinations, product
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from synthesis_k4.encoding import (  # noqa: E402
    ANCHOR,
    N,
    OUTER,
    build_k4_encoding,
    clause_is_true,
    normalized_four_color_clause,
    signature_comparator_clauses,
)
from synthesis_k4.generate import generate, sha256_file  # noqa: E402


class K4EncodingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = build_k4_encoding(
            include_coloring_bank=False,
            include_signature_breaker=False,
        )
        cls.full = build_k4_encoding()

    def test_exact_variable_and_formula_census(self) -> None:
        encoding = self.full
        self.assertEqual(len(encoding.edge_variables), 66)
        self.assertEqual(len(encoding.witness_variables), 1_980)
        self.assertEqual(len(encoding.family_variables), 495)
        self.assertEqual(len(encoding.move_variables), 15_840)
        self.assertEqual(encoding.cnf.variable_count, 18_381)
        self.assertEqual(len(self.base.cnf.clauses), 49_101)
        self.assertEqual(self.base.cnf.literal_count, 196_290)
        self.assertEqual(len(encoding.cnf.clauses), 114_742)
        self.assertEqual(encoding.cnf.literal_count, 1_180_016)

    def test_exact_clause_family_census(self) -> None:
        observed = {
            record.name: (record.clause_count, record.literal_count)
            for record in self.full.clause_families
        }
        expected = {
            "no_k5": (792, 7_920),
            "triple_witness_existence": (220, 1_980),
            "triple_witness_implications": (5_940, 11_880),
            "anchored_k4": (6, 6),
            "connected_g_cuts": (2_047, 67_584),
            "selected_state_domination": (3_960, 19_800),
            "family_nonempty": (1, 495),
            "move_edge_and_successor": (31_680, 63_360),
            "attack_response_disjunctions": (3_960, 19_800),
            "h_k4_to_family": (495, 3_465),
            "complete_anchored_four_color_bank": (65_536, 983_040),
            "outer_signature_order": (105, 686),
        }
        self.assertEqual(observed, expected)
        cursor = 0
        for record in self.full.clause_families:
            self.assertEqual(record.first_clause, cursor)
            cursor += record.clause_count
        self.assertEqual(cursor, len(self.full.cnf.clauses))

    def test_all_clauses_are_well_formed(self) -> None:
        for clause in self.full.cnf.clauses:
            self.assertTrue(clause)
            self.assertEqual(len(clause), len(set(clause)))
            self.assertFalse(any(-literal in clause for literal in clause))
            self.assertTrue(
                all(
                    1 <= abs(literal) <= self.full.cnf.variable_count
                    for literal in clause
                )
            )

    def test_anchor_and_one_guard_move_clauses(self) -> None:
        units = {
            clause[0] for clause in self.base.cnf.clauses if len(clause) == 1
        }
        for first, second in combinations(ANCHOR, 2):
            self.assertIn(self.base.edge(first, second), units)

        state = (0, 2, 4, 7)
        attacked = 9
        selected = self.base.family_variables[state]
        responses = tuple(
            self.base.move_variables[(state, attacked, guard)]
            for guard in state
        )
        self.assertIn((-selected, *responses), self.base.cnf.clauses)
        for guard, move in zip(state, responses, strict=True):
            successor = tuple(sorted((set(state) - {guard}) | {attacked}))
            self.assertIn(
                (-move, -self.base.edge(guard, attacked)),
                self.base.cnf.clauses,
            )
            self.assertIn(
                (-move, self.base.family_variables[successor]),
                self.base.cnf.clauses,
            )

    def test_complete_coloring_bank_rows_are_exact(self) -> None:
        bank = next(
            record
            for record in self.full.clause_families
            if record.name == "complete_anchored_four_color_bank"
        )
        rows = self.full.cnf.clauses[
            bank.first_clause : bank.first_clause + bank.clause_count
        ]
        self.assertEqual(len(rows), 4 ** len(OUTER))
        for index in (0, 1, 255, 4_096, len(rows) - 1):
            digits: list[int] = []
            value = index
            for power in range(len(OUTER) - 1, -1, -1):
                base = 4**power
                digits.append(value // base)
                value %= base
            coloring = ANCHOR + tuple(digits)
            self.assertEqual(
                rows[index],
                normalized_four_color_clause(self.full, coloring),
            )
        self.assertEqual(sum(map(len, rows)), 983_040)

    def test_signature_comparator_exhaustive_truth_table(self) -> None:
        clauses = signature_comparator_clauses(self.full, 4, 5)
        self.assertEqual(len(clauses), 15)
        self.assertEqual(sum(map(len, clauses)), 98)
        for left_bits in product((False, True), repeat=4):
            for right_bits in product((False, True), repeat=4):
                assignment: dict[int, bool] = {}
                for coordinate in range(4):
                    assignment[self.full.edge(coordinate, 4)] = left_bits[
                        coordinate
                    ]
                    assignment[self.full.edge(coordinate, 5)] = right_bits[
                        coordinate
                    ]
                accepted = all(
                    clause_is_true(clause, assignment) for clause in clauses
                )
                self.assertEqual(
                    accepted,
                    left_bits <= right_bits,
                    (left_bits, right_bits),
                )

    def test_generator_installs_exact_modes_and_replays(self) -> None:
        expected = {
            "base": (49_101, 196_290),
            "bank": (114_637, 1_179_330),
            "full": (114_742, 1_180_016),
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for mode, census in expected.items():
                with self.subTest(mode=mode):
                    output = root / f"{mode}.cnf"
                    manifest = root / f"{mode}.json"
                    result = generate(
                        output=output,
                        manifest=manifest,
                        mode=mode,
                    )
                    self.assertEqual(result, json.loads(manifest.read_text()))
                    self.assertEqual(result["claim_status"], "NO_MATHEMATICAL_CLAIM")
                    self.assertEqual(
                        (result["clause_count"], result["literal_count"]),
                        census,
                    )
                    self.assertEqual(result["cnf_sha256"], sha256_file(output))
                    self.assertEqual(
                        result["variable_count"],
                        18_381,
                    )
                    original_cnf = output.read_bytes()
                    replay = subprocess.run(
                        result["normalized_invocation"],
                        cwd=result["working_directory"],
                        env={},
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=30,
                        check=False,
                    )
                    self.assertEqual(replay.returncode, 0, replay.stderr)
                    self.assertEqual(output.read_bytes(), original_cnf)
                    self.assertEqual(
                        json.loads(manifest.read_text()),
                        result,
                    )

    def test_generator_rejects_path_aliases(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            same = root / "same"
            with self.assertRaises(ValueError):
                generate(output=same, manifest=same)

            first = root / "first"
            second = root / "second"
            first.write_bytes(b"unchanged")
            os.link(first, second)
            with self.assertRaises(ValueError):
                generate(output=first, manifest=second)
            self.assertEqual(first.read_bytes(), b"unchanged")

            source = CAMPAIGN / "src/synthesis_k4/encoding.py"
            with self.assertRaises(ValueError):
                generate(output=source, manifest=root / "manifest.json")

    def test_bad_color_rows_and_signature_vertices_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            normalized_four_color_clause(self.full, ANCHOR + (0,) * 7)
        with self.assertRaises(ValueError):
            normalized_four_color_clause(
                self.full, (1, 0, 2, 3) + (0,) * 8
            )
        with self.assertRaises(ValueError):
            normalized_four_color_clause(
                self.full, ANCHOR + (0,) * 7 + (True,)
            )
        with self.assertRaises(ValueError):
            signature_comparator_clauses(self.full, 0, 5)
        with self.assertRaises(ValueError):
            signature_comparator_clauses(self.full, 4, 4)


if __name__ == "__main__":
    unittest.main()
