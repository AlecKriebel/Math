#!/usr/bin/env python3
"""Tests for the resumable LP(333) profile-CRT constructor."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from ortools.sat.python import cp_model

from search_lp333_order3_profile_crt import (
    CORRELATION_COORDINATE_BOUND,
    MAX_MEMORY_MIB,
    MAX_EXACT_NORM9_PROFILE_COUNT,
    PROFILE_STATE_COUNT,
    QUARTET_ASSIGNMENT_COUNT,
    QUARTET_COARSE_STATE_COUNT,
    TIGHT_CORRELATION_COORDINATE_BOUND,
    VARIABLE_ORDER,
    add_assignment_nogood,
    add_sparse_shell_cut,
    audit_correlation_coordinate_bound,
    audit_quartet_state_census,
    build_profile_crt_model,
    compact_hash,
    configure_solver,
    load_or_create_checkpoint,
    model_fingerprint,
    new_checkpoint,
    semantic_manifest,
    run_self_test,
    save_checkpoint,
    split_cube,
    target_stabilizer_elements,
    target_modes,
)
from verify_lp333_order3_char37_transfer import profile_norm, row_sum_targets
from verify_lp333_order3_profile9 import profile_correlation_table
from verify_lp333_order3_profile9_shards import PROFILE9_SHARD_WITNESSES
from verify_lp333_order3_profile_crt_candidate import (
    audit_profile_crt_candidate,
    load_candidate,
    load_candidates,
    prime167_profile_replay,
)
from verify_lp333_order3_profile_crt import exact_profile_residuals
from verify_lp333_order3_profile_zero_symmetry import (
    transform_assignment,
)


class ProfileCRTConstructorTests(unittest.TestCase):
    def test_target_orbit_modes(self) -> None:
        modes = target_modes()
        self.assertEqual(len(modes["formal"]), 7)
        self.assertEqual(len(modes["lift"]), 12)
        self.assertEqual(len(modes["all"]), 22)
        self.assertEqual(len(set(modes["formal"])), 7)
        self.assertTrue(set(modes["formal"]) <= set(modes["lift"]))
        self.assertTrue(set(modes["lift"]) <= set(modes["all"]))

    def test_coordinate_bound_contains_exact_cauchy_disk(self) -> None:
        audit = audit_correlation_coordinate_bound()
        self.assertEqual(audit["cauchy_norm_bound"], 167**2)
        self.assertEqual(
            audit["tight_coordinate_bound"],
            TIGHT_CORRELATION_COORDINATE_BOUND,
        )
        self.assertEqual(
            audit["model_coordinate_bound"], CORRELATION_COORDINATE_BOUND
        )
        self.assertEqual(TIGHT_CORRELATION_COORDINATE_BOUND, 192)
        self.assertEqual(
            CORRELATION_COORDINATE_BOUND,
            TIGHT_CORRELATION_COORDINATE_BOUND,
        )

    def test_target_stabilizer_lex_keeps_one_exact_orbit_image(self) -> None:
        target, identifiers_a, identifiers_b = next(
            witness
            for witness in PROFILE9_SHARD_WITNESSES
            if len(target_stabilizer_elements(witness[0])) == 11
        )
        elements = ((0, False, False),) + target_stabilizer_elements(target)
        images = tuple(
            transform_assignment(
                identifiers_a,
                identifiers_b,
                rotation=rotation,
                star_a=star_a,
                star_b=star_b,
            )
            for rotation, star_a, star_b in elements
        )
        canonical_a, canonical_b = min(
            images, key=lambda value: value[0] + value[1]
        )
        bundle = build_profile_crt_model(
            target,
            enforce_crt=False,
            break_rotation_symmetry=True,
        )
        self.assertEqual(len(bundle.symmetry_elements), 11)
        for channel, identifiers in enumerate((canonical_a, canonical_b)):
            for class_index, value in enumerate(identifiers):
                bundle.model.add(
                    bundle.identifiers[channel][class_index] == value
                )
        solver = configure_solver(time_limit=5.0, max_memory_mib=256)
        self.assertIn(
            solver.solve(bundle.model), (cp_model.FEASIBLE, cp_model.OPTIMAL)
        )

    def test_quartet_state_census(self) -> None:
        census = audit_quartet_state_census()
        self.assertEqual(
            census["quartet_assignments"], QUARTET_ASSIGNMENT_COUNT
        )
        self.assertEqual(
            census["quartet_coarse_states"], QUARTET_COARSE_STATE_COUNT
        )
        self.assertEqual(census["two_layer_energy_bounded_states"], 96_104)
        self.assertEqual(
            census["two_layer_energy_bounded_prefixes"], 10_934_035
        )

    def test_exact_sparse_shell_cut_removes_h5_fixture(self) -> None:
        target, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[1]
        weak = build_profile_crt_model(
            target,
            enforce_crt=False,
            break_rotation_symmetry=False,
        )
        for channel, identifiers in enumerate(
            (identifiers_a, identifiers_b)
        ):
            for class_index, value in enumerate(identifiers):
                weak.model.add(
                    weak.identifiers[channel][class_index] == value
                )
        solver = configure_solver(time_limit=5.0, max_memory_mib=256)
        self.assertIn(
            solver.solve(weak.model), (cp_model.FEASIBLE, cp_model.OPTIMAL)
        )
        self.assertEqual(
            sum(
                solver.value(flag)
                for word in weak.norm9_flags
                for flag in word
            ),
            5,
        )

        cut = build_profile_crt_model(
            target,
            enforce_crt=False,
            break_rotation_symmetry=False,
        )
        add_sparse_shell_cut(cut.model, cut.norm9_flags)
        for channel, identifiers in enumerate(
            (identifiers_a, identifiers_b)
        ):
            for class_index, value in enumerate(identifiers):
                cut.model.add(
                    cut.identifiers[channel][class_index] == value
                )
        cut_solver = configure_solver(time_limit=5.0, max_memory_mib=256)
        self.assertEqual(cut_solver.solve(cut.model), cp_model.INFEASIBLE)
        self.assertEqual(MAX_EXACT_NORM9_PROFILE_COUNT, 2)

    def test_variable_order_is_complete(self) -> None:
        self.assertEqual(len(VARIABLE_ORDER), 24)
        self.assertEqual(
            set(VARIABLE_ORDER),
            {(channel, index) for channel in range(2) for index in range(12)},
        )
        for block_start in range(0, 24, 4):
            block = VARIABLE_ORDER[block_start : block_start + 4]
            self.assertEqual(block[0][0], 0)
            self.assertEqual(block[1][0], 0)
            self.assertEqual(block[2][0], 1)
            self.assertEqual(block[3][0], 1)
            self.assertEqual(block[1][1], block[0][1] + 6)
            self.assertEqual(block[3][1], block[2][1] + 6)

    def test_cp_correlation_matches_exact_fixture(self) -> None:
        result = run_self_test(512)
        self.assertTrue(result["model_matches_exact_replay"])
        self.assertEqual(result["correlation_parts_checked"], 13)
        self.assertEqual(result["known_bad_fixture_full_status"], "INFEASIBLE")
        self.assertEqual(result["exact_zero_scalar_equations"], 12)
        self.assertEqual(result["correlation_coordinate_bound"], 192)
        self.assertFalse(result["solver_memory_parameter_is_hard_rss_limit"])
        self.assertEqual(result["solver_workers"], 1)
        self.assertLessEqual(result["solver_memory_limit_mib"], 512)

    def test_fixed_fixture_table_without_crt(self) -> None:
        target, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[0]
        bundle = build_profile_crt_model(
            target,
            enforce_crt=False,
            break_rotation_symmetry=False,
        )
        for channel, identifiers in enumerate((identifiers_a, identifiers_b)):
            for class_index, value in enumerate(identifiers):
                bundle.model.add(
                    bundle.identifiers[channel][class_index] == value
                )
        solver = configure_solver(time_limit=5.0, max_memory_mib=256)
        status = solver.solve(bundle.model)
        self.assertIn(status, (cp_model.FEASIBLE, cp_model.OPTIMAL))
        model_table = tuple(
            (
                0 if isinstance(real, int) else solver.value(real),
                0 if isinstance(omega, int) else solver.value(omega),
            )
            for real, omega in zip(
                bundle.correlation_real, bundle.correlation_omega
            )
        )
        self.assertEqual(
            model_table,
            profile_correlation_table(identifiers_a, identifiers_b),
        )

    def test_norm_nine_top_four_shell_cut(self) -> None:
        self.assertEqual(MAX_EXACT_NORM9_PROFILE_COUNT, 2)
        for witness_index, expected_high_count in (
            (0, 3),
            (4, 4),
            (1, 5),
            (3, 6),
        ):
            target, identifiers_a, identifiers_b = (
                PROFILE9_SHARD_WITNESSES[witness_index]
            )
            self.assertEqual(
                sum(
                    profile_norm(identifier) == 9
                    for identifier in identifiers_a + identifiers_b
                ),
                expected_high_count,
            )
            bundle = build_profile_crt_model(
                target,
                enforce_crt=False,
                break_rotation_symmetry=False,
            )
            add_sparse_shell_cut(bundle.model, bundle.norm9_flags)
            for channel, identifiers in enumerate(
                (identifiers_a, identifiers_b)
            ):
                for class_index, value in enumerate(identifiers):
                    bundle.model.add(
                        bundle.identifiers[channel][class_index] == value
                    )
            solver = configure_solver(time_limit=5.0, max_memory_mib=256)
            self.assertEqual(solver.solve(bundle.model), cp_model.INFEASIBLE)

    def test_complete_assignment_nogood_is_exact(self) -> None:
        target, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[0]
        bundle = build_profile_crt_model(
            target,
            enforce_crt=False,
            break_rotation_symmetry=False,
        )
        add_assignment_nogood(
            bundle.model,
            bundle.identifiers,
            identifiers_a,
            identifiers_b,
            "fixture",
        )
        for channel, identifiers in enumerate((identifiers_a, identifiers_b)):
            for class_index, value in enumerate(identifiers):
                bundle.model.add(
                    bundle.identifiers[channel][class_index] == value
                )
        solver = configure_solver(time_limit=5.0, max_memory_mib=256)
        self.assertEqual(solver.solve(bundle.model), cp_model.INFEASIBLE)

    def test_exact_replay_rejects_known_nonzero_profile(self) -> None:
        target, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[0]
        with self.assertRaisesRegex(
            ValueError, "characteristic-37 transfer coefficient"
        ):
            audit_profile_crt_candidate(target, identifiers_a, identifiers_b)

    def test_cube_split_is_disjoint_and_complete(self) -> None:
        cube = {"target_index": 3, "prefix": (2, 7)}
        children = split_cube(cube)
        self.assertEqual(len(children), PROFILE_STATE_COUNT)
        self.assertEqual(
            {tuple(child["prefix"]) for child in children},
            {(2, 7, value) for value in range(PROFILE_STATE_COUNT)},
        )
        self.assertTrue(all(child["target_index"] == 3 for child in children))

    def test_checkpoint_roundtrip_and_fingerprint_guard(self) -> None:
        indices = target_modes()["formal"]
        checkpoint = new_checkpoint(indices, True)
        self.assertEqual(len(checkpoint["pending_cubes"]), 7)
        self.assertEqual(
            checkpoint["model_fingerprint"],
            model_fingerprint(indices, True),
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            save_checkpoint(path, checkpoint)
            replay = load_or_create_checkpoint(path, indices, True)
            self.assertEqual(
                replay["model_fingerprint"],
                checkpoint["model_fingerprint"],
            )
            with self.assertRaisesRegex(
                ValueError, "mathematical configuration mismatch"
            ):
                load_or_create_checkpoint(path, (0,), True)
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["selected_target_indices"][0] = True
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "exact integer"):
                load_or_create_checkpoint(path, indices, True)

    def test_checkpoint_rejects_hash_consistent_invalid_persisted_candidate(
        self,
    ) -> None:
        target, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[0]
        target_index = row_sum_targets().index(target)
        checkpoint = new_checkpoint((target_index,), True)
        survivor_hash = compact_hash(
            (target, identifiers_a, identifiers_b)
        )
        checkpoint["candidates"] = [
            {
                "survivor_sha256": survivor_hash,
                "target_index": target_index,
                "target": target,
                "profiles_a": identifiers_a,
                "profiles_b": identifiers_b,
                "exact_replay": {
                    "certificate_sha256": "0" * 64,
                },
            }
        ]
        checkpoint["candidate_sha256"] = [survivor_hash]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            save_checkpoint(path, checkpoint)
            with self.assertRaisesRegex(
                ValueError, "failed detached exact replay"
            ):
                load_or_create_checkpoint(path, (target_index,), True)

    def test_semantic_fingerprint_covers_sources_tables_and_solver(self) -> None:
        manifest = semantic_manifest()
        self.assertIn("ortools_version", manifest)
        self.assertIn("table_sha256", manifest)
        self.assertIn(
            "search_lp333_order3_profile_crt.py",
            manifest["python_source_sha256"],
        )
        self.assertIn(
            "verify_lp333_order3_profile_penultimate_shell.py",
            manifest["python_source_sha256"],
        )
        self.assertIn(
            "verify_lp333_order3_profile_shell_four.cpp",
            manifest["python_source_sha256"],
        )
        self.assertIn(
            "shell_three_mod27/"
            "verify_lp333_order3_profile_shell_three_mod27.cpp",
            manifest["python_source_sha256"],
        )
        self.assertEqual(
            manifest["quartet_census"],
            {"assignments": 3334, "coarse_states": 1409},
        )

    def test_semantic_fingerprint_pins_replay_dependency_closure(self) -> None:
        manifest = semantic_manifest()
        source_hashes = manifest["python_source_sha256"]
        self.assertTrue(
            {
                "verify_lp333_order3_integral9.py",
                "verify_lp333_order3_labeled_jet.py",
                "verify_lp333_order3_primitive9_jet.py",
                "verify_lp333_order3_quotient.py",
                "verify_lp333_order3_trit_lift.py",
            }
            <= set(source_hashes)
        )
        self.assertEqual(
            manifest["effective_profile_semantics"],
            {
                "column_modulus": 37,
                "row_count": 9,
                "zero_eisenstein": ((-1, 0), (2, 0)),
                "max_exact_norm9_profile_count": 2,
            },
        )

    def test_candidate_json_loader(self) -> None:
        target, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[0]
        payload = {
            "candidate": {
                "target": list(target),
                "profiles_a": list(identifiers_a),
                "profiles_b": list(identifiers_b),
            }
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(
                load_candidate(path), (target, identifiers_a, identifiers_b)
            )
            self.assertEqual(
                load_candidates(path),
                ((target, identifiers_a, identifiers_b),),
            )
            payload["candidate"]["profiles_a"][0] = True
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "exact integer"):
                load_candidate(path)

    def test_candidate_json_rejects_duplicate_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.json"
            path.write_text(
                '{"target":[0,0,0,0],"target":[0,0,0,0],'
                '"profiles_a":[],"profiles_b":[]}',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                load_candidate(path)

    def test_prime167_third_reconstruction_matches_integer_word(self) -> None:
        _, identifiers_a, identifiers_b = PROFILE9_SHARD_WITNESSES[0]
        correlations, adjusted = prime167_profile_replay(
            identifiers_a, identifiers_b
        )
        self.assertEqual(correlations[0], (167, 0))
        self.assertEqual(
            adjusted, exact_profile_residuals(identifiers_a, identifiers_b)
        )

    def test_memory_ceiling_is_enforced(self) -> None:
        configure_solver(time_limit=1.0, max_memory_mib=MAX_MEMORY_MIB)
        with self.assertRaisesRegex(ValueError, r"\[1,4096\]"):
            configure_solver(
                time_limit=1.0, max_memory_mib=MAX_MEMORY_MIB + 1
            )


if __name__ == "__main__":
    unittest.main()
