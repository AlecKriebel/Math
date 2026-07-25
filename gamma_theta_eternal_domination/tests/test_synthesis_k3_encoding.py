from __future__ import annotations

import sys
import json
import os
import subprocess
import tempfile
import unittest
from itertools import combinations
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from synthesis_k3.encoding import (  # noqa: E402
    N,
    TEMPLATES,
    build_k3_encoding,
    same_color_cut,
    validate_decoded_candidate,
)
from synthesis_k3.generate import generate, sha256_file  # noqa: E402


class K3EncodingTests(unittest.TestCase):
    def test_deterministic_variable_layout_and_well_formed_clauses(self) -> None:
        for template in TEMPLATES:
            encoding = build_k3_encoding(template)
            self.assertEqual(encoding.cnf.variable_count, 6_886)
            self.assertEqual(len(encoding.edge_variables), 66)
            self.assertEqual(len(encoding.witness_variables), 660)
            self.assertEqual(len(encoding.family_variables), 220)
            self.assertEqual(len(encoding.move_variables), 5_940)
            self.assertEqual(
                encoding.cnf.dimacs(),
                build_k3_encoding(template).cnf.dimacs(),
            )
            for clause in encoding.cnf.clauses:
                self.assertTrue(clause)
                self.assertEqual(len(clause), len(set(clause)))
                self.assertFalse(any(-literal in clause for literal in clause))
                self.assertTrue(
                    all(
                        1 <= abs(literal) <= encoding.cnf.variable_count
                        for literal in clause
                    )
                )

    def test_hole_templates_force_exact_rim_and_hub_free_clauses(self) -> None:
        for length in (5, 7, 9):
            encoding = build_k3_encoding(f"hole{length}")
            units = {clause[0] for clause in encoding.cnf.clauses if len(clause) == 1}
            rim_edges = {
                tuple(sorted((vertex, (vertex + 1) % length)))
                for vertex in range(length)
            }
            for pair in combinations(range(length), 2):
                variable = encoding.edge(*pair)
                self.assertIn(
                    variable if pair in rim_edges else -variable,
                    units,
                )
            self.assertIn(encoding.edge(0, length), units)
            self.assertIn(encoding.edge(1, length), units)
            for outside in range(length, N):
                expected = tuple(
                    -encoding.edge(outside, rim) for rim in range(length)
                )
                self.assertIn(expected, encoding.cnf.clauses)

    def test_antihole_template_forces_complement_of_c7(self) -> None:
        encoding = build_k3_encoding("antihole7")
        units = {clause[0] for clause in encoding.cnf.clauses if len(clause) == 1}
        cycle_edges = {
            tuple(sorted((vertex, (vertex + 1) % 7)))
            for vertex in range(7)
        }
        for pair in combinations(range(7), 2):
            variable = encoding.edge(*pair)
            self.assertIn(
                -variable if pair in cycle_edges else variable,
                units,
            )

    def test_coloring_cut_is_exact_same_color_edge_disjunction(self) -> None:
        encoding = build_k3_encoding("hole5")
        coloring = tuple(vertex % 3 for vertex in range(N))
        expected = tuple(
            encoding.edge(first, second)
            for first, second in combinations(range(N), 2)
            if coloring[first] == coloring[second]
        )
        self.assertEqual(same_color_cut(encoding, coloring), expected)
        with self.assertRaises(ValueError):
            same_color_cut(encoding, coloring[:-1])
        with self.assertRaises(ValueError):
            same_color_cut(encoding, (0,) * 11 + (3,))
        with self.assertRaises(ValueError):
            same_color_cut(encoding, (0,) * 11 + (True,))

    def test_move_clauses_encode_one_guard_and_selected_successor(self) -> None:
        encoding = build_k3_encoding("hole5")
        triple = (0, 2, 4)
        attacked = 7
        family_variable = encoding.family_variables[triple]
        responses = tuple(
            encoding.move_variables[(triple, attacked, guard)]
            for guard in triple
        )
        self.assertIn((-family_variable, *responses), encoding.cnf.clauses)
        for guard, response in zip(triple, responses, strict=True):
            successor = tuple(
                sorted((set(triple) - {guard}) | {attacked})
            )
            self.assertIn(
                (-response, -encoding.edge(guard, attacked)),
                encoding.cnf.clauses,
            )
            self.assertIn(
                (-response, encoding.family_variables[successor]),
                encoding.cnf.clauses,
            )

    def test_generator_round_trip_binds_installed_bytes_and_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            colorings = root / "cuts.json"
            colorings.write_text(
                json.dumps([[vertex % 3 for vertex in range(N)]]) + "\n",
                encoding="utf-8",
            )
            before = colorings.read_bytes()
            output = root / "instance.cnf"
            manifest = root / "instance.json"
            result = generate(
                template="hole5",
                output=output,
                manifest=manifest,
                colorings_path=colorings,
            )
            installed = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(installed, result)
            self.assertEqual(result["cnf_sha256"], sha256_file(output))
            self.assertEqual(
                result["colorings_sha256"], sha256_file(colorings)
            )
            self.assertEqual(colorings.read_bytes(), before)
            self.assertEqual(result["coloring_cut_count"], 1)
            self.assertEqual(result["schema_version"], 2)
            self.assertEqual(
                len(result["generator_source_manifest"]), 4
            )
            self.assertEqual(
                result["required_environment"]["PYTHONPATH"],
                str(CAMPAIGN / "src"),
            )
            self.assertEqual(
                result["working_directory"], str(CAMPAIGN)
            )
            self.assertEqual(
                result["normalized_invocation"][:2],
                ["/usr/bin/env", f"PYTHONPATH={CAMPAIGN / 'src'}"],
            )
            replay = subprocess.run(
                result["normalized_invocation"],
                cwd=result["working_directory"],
                env={},
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(replay.returncode, 0, replay.stderr)
            self.assertEqual(sha256_file(output), result["cnf_sha256"])

    def test_generator_rejects_path_aliases_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cuts = root / "cuts.json"
            cuts.write_text("[]\n", encoding="utf-8")
            original = cuts.read_bytes()
            cases = (
                (root / "same", root / "same", cuts),
                (cuts, root / "manifest.json", cuts),
                (root / "instance.cnf", cuts, cuts),
            )
            for output, manifest, colorings in cases:
                with self.subTest(output=output, manifest=manifest):
                    with self.assertRaises(ValueError):
                        generate(
                            template="hole5",
                            output=output,
                            manifest=manifest,
                            colorings_path=colorings,
                        )
                    self.assertEqual(cuts.read_bytes(), original)

            source = CAMPAIGN / "src/synthesis_k3/generate.py"
            with self.assertRaises(ValueError):
                generate(
                    template="hole5",
                    output=source,
                    manifest=root / "manifest.json",
                )

            source_alias = root / "source-alias.py"
            source_alias.symlink_to(source)
            with self.assertRaises(ValueError):
                generate(
                    template="hole5",
                    output=source_alias,
                    manifest=root / "manifest.json",
                )

            first = root / "hardlink-a"
            second = root / "hardlink-b"
            first.write_bytes(b"unchanged")
            os.link(first, second)
            with self.assertRaises(ValueError):
                generate(
                    template="hole5",
                    output=first,
                    manifest=second,
                )
            self.assertEqual(first.read_bytes(), b"unchanged")

    def test_coloring_partition_permutations_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            base = [vertex % 3 for vertex in range(N)]
            permuted = [(color + 1) % 3 for color in base]
            cuts = root / "cuts.json"
            cuts.write_text(
                json.dumps([base, permuted]) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                generate(
                    template="hole5",
                    output=root / "instance.cnf",
                    manifest=root / "manifest.json",
                    colorings_path=cuts,
                )

    def test_decoded_validator_rejects_hostile_vertex_records(self) -> None:
        encoding = build_k3_encoding("hole5")
        hostile_edges = (
            ((True, 2),),
            ((1.0, 2),),
            ((0,),),
            ((0, 1, 2),),
            ((0, 1), (1, 0)),
            ((0, 12),),
        )
        for edges in hostile_edges:
            with self.subTest(edges=edges):
                with self.assertRaises(ValueError):
                    validate_decoded_candidate(
                        encoding, edges, ((0, 1, 2),)
                    )
        hostile_families = (
            ((0, True, 2),),
            ((0, 1.0, 2),),
            ((0, 1),),
            ((0, 1, 2, 3),),
            ((0, 1, 2), (2, 1, 0)),
            ((0, 1, 12),),
        )
        for family in hostile_families:
            with self.subTest(family=family):
                with self.assertRaises(ValueError):
                    validate_decoded_candidate(encoding, (), family)


if __name__ == "__main__":
    unittest.main()
