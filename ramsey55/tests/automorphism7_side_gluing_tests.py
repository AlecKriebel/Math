#!/usr/bin/env python3
"""No-production controls for the automorphism-7 side-gluing runner."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import automorphism7_side_gluing_pilot as pilot  # noqa: E402
from graph_io import decode_graph6, encode_graph6  # noqa: E402
from residual_completion_glucose import parse_dimacs  # noqa: E402


METADATA = ROOT / "certificates" / "order43_automorphism7_six_cycles.metadata.json"
CNF = ROOT / "certificates" / "order43_automorphism7_six_cycles.cnf"


class Automorphism7SideGluingTests(unittest.TestCase):
    def test_local_orbit_formula_and_pinned_digests(self) -> None:
        orbits, table = pilot.side_edge_orbits()
        clauses = pilot.side_formula(table)
        self.assertEqual(len(orbits), 30)
        self.assertEqual(Counter(map(len, orbits)), {7: 30})
        self.assertEqual(len(table), 210)
        self.assertEqual(sum(clause[0] < 0 for clause in clauses), 843)
        self.assertEqual(sum(clause[0] > 0 for clause in clauses), 2775)
        self.assertEqual(
            pilot.sha256_lines(
                [" ".join(map(str, clause)) for clause in clauses]
            ),
            "f59be7024c4b15cba7238da38d865a4f8ea8dd631ed5c096300054679cd65c96",
        )

    def test_side_model_and_complement_have_required_semantics(self) -> None:
        _, table = pilot.side_edge_orbits()
        clauses = pilot.side_formula(table)
        model = pilot.diverse_side_models(clauses, 1, 20261101)[0]
        edge = lambda left, right: model[
            table[tuple(sorted((left, right)))] - 1
        ]
        self.assertFalse(
            any(
                all(edge(left, right) for left, right in itertools.combinations(vertices, 2))
                for vertices in itertools.combinations(range(21), 4)
            )
        )
        self.assertFalse(
            any(
                all(
                    not edge(left, right)
                    for left, right in itertools.combinations(vertices, 2)
                )
                for vertices in itertools.combinations(range(21), 5)
            )
        )
        # Actual B is the complement of this model. Thus an independent
        # 4-set in B is a K4 here, and a K5 in B is an I5 here.

    def test_global_partition_is_exactly_66_fixed_63_free(self) -> None:
        metadata = json.loads(METADATA.read_text(encoding="utf-8"))
        edge_variables = pilot.global_edge_table(metadata)
        side_orbits, _ = pilot.side_edge_orbits()
        map_a = [edge_variables[orbit[0]] for orbit in side_orbits]
        map_b = [
            edge_variables[
                (orbit[0][0] + pilot.SIDE_ORDER, orbit[0][1] + pilot.SIDE_ORDER)
            ]
            for orbit in side_orbits
        ]
        fixed = sorted(
            {
                variable
                for (left, right), variable in edge_variables.items()
                if right == pilot.ORDER - 1
            },
            key=lambda variable: min(
                left
                for (left, right), observed in edge_variables.items()
                if right == pilot.ORDER - 1 and observed == variable
            ),
        )
        self.assertEqual(fixed, [39, 71, 96, 114, 125, 129])
        self.assertEqual(len(set(fixed + map_a + map_b)), 66)
        self.assertEqual(
            len(set(range(1, 130)) - set(fixed + map_a + map_b)), 63
        )

    def test_pair_schedule_is_unique_balanced_and_pinned(self) -> None:
        pairs = pilot.deterministic_pairs(64, 256)
        self.assertEqual(len(pairs), len(set(pairs)), 256)
        self.assertEqual(set(Counter(left for left, _ in pairs).values()), {4})
        self.assertEqual(set(Counter(right for _, right in pairs).values()), {4})
        self.assertEqual(
            pilot.sha256_lines([f"{left},{right}" for left, right in pairs]),
            "e6da298b77008bcb68a3c6cc67dc40376accd98ce4a96a2edb238e654d38b6fb",
        )

    def test_complete_model_decoder_rejects_partial_or_ambiguous_models(
        self,
    ) -> None:
        complete = list(range(1, 130))
        truth = pilot.complete_model_truth(complete, 129)
        self.assertEqual(len(truth), 129)
        with self.assertRaisesRegex(ValueError, "complete"):
            pilot.complete_model_truth(complete[:-1], 129)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            pilot.complete_model_truth(complete[:-1] + [1], 129)
        with self.assertRaisesRegex(ValueError, "out of range"):
            pilot.complete_model_truth(complete[:-1] + [130], 129)

    def test_global_decode_round_trip_preserves_the_c7_action(self) -> None:
        metadata = json.loads(METADATA.read_text(encoding="utf-8"))
        edge_variables = pilot.global_edge_table(metadata)
        truth = {variable: variable % 3 == 0 for variable in range(1, 130)}
        adjacency = pilot.decode_global_graph(truth, edge_variables)
        self.assertEqual(decode_graph6(encode_graph6(adjacency)), adjacency)
        permutation = metadata["permutation"]
        for left in range(43):
            for right in range(left + 1, 43):
                image = tuple(sorted((permutation[left], permutation[right])))
                self.assertEqual(
                    (adjacency[left] >> right) & 1,
                    (adjacency[image[0]] >> image[1]) & 1,
                )

    def test_a_b_units_satisfy_every_fully_assigned_global_clause(self) -> None:
        metadata = json.loads(METADATA.read_text(encoding="utf-8"))
        edge_variables = pilot.global_edge_table(metadata)
        side_orbits, table = pilot.side_edge_orbits()
        side_model = pilot.diverse_side_models(
            pilot.side_formula(table), 1, 20261101
        )[0]
        map_a = [edge_variables[orbit[0]] for orbit in side_orbits]
        map_b = [
            edge_variables[
                (orbit[0][0] + pilot.SIDE_ORDER, orbit[0][1] + pilot.SIDE_ORDER)
            ]
            for orbit in side_orbits
        ]
        fixed = [39, 71, 96, 114, 125, 129]
        units = fixed[:3] + [-variable for variable in fixed[3:]]
        units.extend(
            variable if value else -variable
            for variable, value in zip(map_a, side_model)
        )
        units.extend(
            -variable if value else variable
            for variable, value in zip(map_b, side_model)
        )
        values = {abs(literal): literal > 0 for literal in units}
        _, clauses = parse_dimacs(CNF)
        fully_assigned = [
            clause
            for clause in clauses
            if all(abs(literal) in values for literal in clause)
        ]
        self.assertEqual(len(fully_assigned), 14_472)
        self.assertTrue(
            all(
                any(values[abs(literal)] == (literal > 0) for literal in clause)
                for clause in fully_assigned
            )
        )

    def test_toolchain_hashes_are_actually_enforced(self) -> None:
        paths = [
            Path(pilot.inspect.getfile(pilot.pysat_solvers)),
            Path(str(pilot.pysolvers.__file__)),
            Path(sys.executable),
        ]
        plan = {
            "pysat_version": pilot.pysat.__version__,
            "toolchain_sha256": {
                "pysat_solvers_py": pilot.sha256_file(paths[0]),
                "pysolvers_extension": pilot.sha256_file(paths[1]),
                "python": pilot.sha256_file(paths[2]),
            },
        }
        checked = pilot.validate_toolchain(plan)
        self.assertEqual(checked["sha256"], plan["toolchain_sha256"])
        plan["toolchain_sha256"]["python"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "toolchain hash mismatch"):
            pilot.validate_toolchain(plan)

    def test_storage_gate_relation_and_free_space_are_enforced(self) -> None:
        output = ROOT / "results" / "global_exact" / "audit-only-summary.json"
        candidate = (
            ROOT / "results" / "best_candidates" / "audit-only-candidate.g6"
        )
        plan = {
            "storage_gate": {
                "maximum_new_artifact_bytes": 1,
                "minimum_free_bytes_after_completion": 1,
                "required_prelaunch_free_bytes": 2,
            }
        }
        self.assertGreater(
            pilot.validate_storage_gate(plan, output, candidate)[
                "available_prelaunch_free_bytes"
            ],
            2,
        )
        plan["storage_gate"]["required_prelaunch_free_bytes"] = 3
        with self.assertRaisesRegex(ValueError, "full artifact cap"):
            pilot.validate_storage_gate(plan, output, candidate)

    def test_42_vertex_control_is_rejected_by_43_vertex_binding(self) -> None:
        result = pilot.verify_candidate(
            ROOT / "data" / "r55_42some.g6",
            ROOT / "verify" / "exhaustive_verify.py",
            ROOT / "build" / "bitset_verify",
        )
        self.assertFalse(result["valid"])
        self.assertEqual(result["python"]["json"]["n"], 42)
        self.assertEqual(result["cpp"]["json"]["n"], 42)


if __name__ == "__main__":
    unittest.main()
