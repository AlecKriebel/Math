from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from itertools import combinations, product
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from search.order13_k3.encoding import (  # noqa: E402
    EXPECTED_FORMULAS,
    N,
    TEMPLATES,
    _is_three_colorable,
    build_base_encoding,
    build_full_encoding,
    canonicalize_color_names,
    enumerate_coloring_bank,
    positive_template_edges,
    row_is_template_proper,
)
from search.order13_k3.generate import (  # noqa: E402
    BANK_NAME,
    CHECKPOINT_NAME,
    INSTANCE_NAME,
    MANIFEST_NAME,
    PLAN_NAME,
    audit_package,
    generate_package,
    write_run_plan,
)


class Order13K3ConstructorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.encodings = {
            template: build_full_encoding(template)
            for template in TEMPLATES
        }

    def test_exact_frozen_formula_counts_and_hashes(self) -> None:
        for template, encoding in self.encodings.items():
            with self.subTest(template=template):
                payload = encoding.cnf.dimacs_bytes()
                expected = EXPECTED_FORMULAS[template]
                coloring = encoding.cnf.family_counts[
                    "complete_coloring_obstruction"
                ]
                self.assertEqual(encoding.cnf.variable_count, expected["variables"])
                self.assertEqual(len(encoding.cnf.clauses), expected["clauses"])
                self.assertEqual(encoding.cnf.literal_count, expected["literals"])
                self.assertEqual(len(encoding.coloring_bank), expected["coloring_rows"])
                self.assertEqual(
                    len(encoding.cnf.clauses) - coloring[0],
                    expected["base_clauses"],
                )
                self.assertEqual(
                    encoding.cnf.literal_count - coloring[1],
                    expected["base_literals"],
                )
                self.assertEqual(len(payload), expected["size_bytes"])
                self.assertEqual(
                    hashlib.sha256(payload).hexdigest(),
                    expected["sha256"],
                )

    def test_variable_census_and_no_heuristic_breaker_families(self) -> None:
        encoding = self.encodings["hole11"]
        self.assertEqual(len(encoding.edge_variables), 78)
        self.assertEqual(len(encoding.witness_variables), 858)
        self.assertEqual(len(encoding.family_variables), 286)
        self.assertEqual(len(encoding.move_variables), 8580)
        names = set(encoding.cnf.family_counts)
        self.assertEqual(names, set(encoding.cnf.family_sha256))
        self.assertTrue(
            all(len(digest) == 64 for digest in encoding.cnf.family_sha256.values())
        )
        self.assertFalse(
            names
            & {
                "signature_sorting",
                "rim_reflection",
                "doublelex",
                "row_lex",
                "column_lex",
            }
        )

    def test_anchor_template_and_one_guard_clause_shapes(self) -> None:
        for template in TEMPLATES:
            with self.subTest(template=template):
                encoding = build_base_encoding(template)
                length = int(template[4:])
                clauses = set(encoding.cnf.clauses)
                self.assertIn((encoding.edge(0, 1),), clauses)
                self.assertIn((encoding.edge(0, length),), clauses)
                self.assertIn((encoding.edge(1, length),), clauses)

                for state in combinations(range(N), 3):
                    for attacked in range(N):
                        self.assertEqual(
                            (state, attacked, state[0]) in encoding.move_variables,
                            attacked not in state,
                        )
                        if attacked in state:
                            continue
                        response = (
                            -encoding.family_variables[state],
                            *(
                                encoding.move_variables[(state, attacked, guard)]
                                for guard in state
                            ),
                        )
                        self.assertIn(response, clauses)
                        for guard in state:
                            move = encoding.move_variables[(state, attacked, guard)]
                            successor = tuple(
                                sorted((set(state) - {guard}) | {attacked})
                            )
                            self.assertIn(
                                (-move, -encoding.edge(guard, attacked)),
                                clauses,
                            )
                            self.assertIn(
                                (-move, encoding.family_variables[successor]),
                                clauses,
                            )

    def test_coloring_banks_are_exact_orbit_representatives(self) -> None:
        # Independent oracle: fix color(0)=0, enumerate all remaining labeled
        # rows, then canonicalize color names.  It does not reuse bank recursion.
        for template in TEMPLATES:
            with self.subTest(template=template):
                bank = enumerate_coloring_bank(template)
                self.assertEqual(bank, tuple(sorted(set(bank))))
                forced = positive_template_edges(template)
                oracle: set[tuple[int, ...]] = set()
                for tail in product(range(3), repeat=N - 1):
                    row = (0, *tail)
                    if all(row[first] != row[second] for first, second in forced):
                        oracle.add(canonicalize_color_names(row))
                self.assertEqual(set(bank), oracle)
                self.assertTrue(all(row_is_template_proper(template, row) for row in bank))

    def test_direct_candidate_coloring_oracle_distinguishes_c5_and_k4(self) -> None:
        c5 = {
            tuple(sorted((vertex, (vertex + 1) % 5)))
            for vertex in range(5)
        }
        k4 = set(combinations(range(4), 2))

        def edge_from(edges: set[tuple[int, int]]):
            return lambda first, second: tuple(sorted((first, second))) in edges

        self.assertTrue(_is_three_colorable(edge_from(c5)))
        self.assertFalse(_is_three_colorable(edge_from(k4)))

    def test_package_determinism_exhaustive_audit_and_mutations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            first = root / "first"
            second = root / "second"
            generate_package(
                template="hole11",
                output_directory=first,
                validation_gate=True,
            )
            generate_package(
                template="hole11",
                output_directory=second,
                validation_gate=True,
            )
            for name in (INSTANCE_NAME, BANK_NAME, MANIFEST_NAME):
                self.assertEqual(
                    (first / name).read_bytes(),
                    (second / name).read_bytes(),
                )
            report = audit_package(first, exhaustive=True)
            self.assertTrue(report["accepted"])
            self.assertFalse(report["solver_launched"])

            instance = first / INSTANCE_NAME
            original = instance.read_bytes()
            instance.write_bytes(original[:-1] + b" ")
            with self.assertRaises(ValueError):
                audit_package(first, exhaustive=False)
            instance.write_bytes(original)

            bank = first / BANK_NAME
            original_bank = bank.read_bytes()
            parsed = json.loads(original_bank)
            bank.write_text(
                json.dumps(parsed[:-1], indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                audit_package(first, exhaustive=False)
            bank.write_bytes(original_bank)
            self.assertTrue(audit_package(first, exhaustive=False)["accepted"])

    def test_generation_and_run_plan_are_gated_and_never_execute(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            package = root / "package"
            with self.assertRaises(PermissionError):
                generate_package(
                    template="hole11",
                    output_directory=package,
                    validation_gate=False,
                )
            self.assertFalse(package.exists())
            generate_package(
                template="hole11",
                output_directory=package,
                validation_gate=True,
            )
            marker = package / "keep"
            marker.write_bytes(b"preserve")
            with self.assertRaises(FileExistsError):
                generate_package(
                    template="hole11",
                    output_directory=package,
                    validation_gate=True,
                )
            self.assertEqual(marker.read_bytes(), b"preserve")
            marker.unlink()

            fake_solver = root / "cadical"
            fake_solver.write_bytes(b"this file must never execute\n")
            fake_solver.chmod(0o700)
            run = root / "run"
            with self.assertRaises(PermissionError):
                write_run_plan(
                    package_directory=package,
                    output_directory=run,
                    cadical_path=fake_solver,
                    validation_gate=False,
                )
            self.assertFalse(run.exists())
            plan = write_run_plan(
                package_directory=package,
                output_directory=run,
                cadical_path=fake_solver,
                validation_gate=True,
            )
            self.assertEqual(plan["status"], "READY_NOT_RUN")
            self.assertEqual(
                {entry.name for entry in run.iterdir()},
                {INSTANCE_NAME, PLAN_NAME, CHECKPOINT_NAME},
            )
            checkpoint = json.loads(
                (run / CHECKPOINT_NAME).read_text(encoding="utf-8")
            )
            self.assertEqual(checkpoint["status"], "READY_NOT_RUN")
            self.assertEqual(checkpoint["attempts"], [])


if __name__ == "__main__":
    unittest.main()
