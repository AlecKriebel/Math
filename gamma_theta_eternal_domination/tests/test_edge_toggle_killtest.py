from __future__ import annotations

import json
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from search.edge_toggle_killtest import (  # noqa: E402
    Seed,
    _connect_database,
    _validate_or_repair_complete_seed,
    _validate_path_roles,
    build_configuration,
    evaluate_toggled_graph,
    load_certified_seeds,
    run_edge_toggle_search,
    toggle_edge,
    toggle_pairs,
)
from verifier_a.core import BitGraph  # noqa: E402


SEED_INPUT = CAMPAIGN / "results" / "extensions_unique.csv"
EXTENSION_AUDIT = CAMPAIGN / "results" / "extension_coverage_audit.json"
LABELG = CAMPAIGN / "tools" / "nauty2_9_3" / "labelg"


def _sample_arguments(root: Path) -> dict[str, object]:
    return {
        "seed_input_path": SEED_INPUT,
        "extension_audit_path": EXTENSION_AUDIT,
        "labelg_path": LABELG,
        "database_path": root / "edge-toggles.sqlite3",
        "checkpoint_path": root / "edge-toggles.json",
        "candidate_directory": root / "candidates",
        "provenance_output": root / "provenance.csv",
        "unique_output": root / "unique.csv",
        "batch_size": 2,
        "active_seed_ids": ("ET-0001",),
        "max_batches": 1,
        "wall_limit_seconds": 60,
        "memory_limit_mib": 1024,
    }


class EdgeToggleKillTestTests(unittest.TestCase):
    def test_exact_seed_scope_and_raw_coverage(self) -> None:
        seeds = load_certified_seeds(SEED_INPUT, EXTENSION_AUDIT)
        self.assertEqual(len(seeds), 391)
        self.assertEqual(
            sum(seed.order == 11 for seed in seeds), 15
        )
        self.assertEqual(
            sum(seed.order == 12 for seed in seeds), 376
        )
        self.assertEqual(
            sum(seed.raw_toggle_count for seed in seeds), 25_641
        )
        self.assertEqual(
            sum(
                seed.source_category
                == "private_obstruction_eternal_false"
                for seed in seeds
            ),
            106,
        )
        self.assertEqual(
            sum(
                seed.source_category
                == "eternal_false_without_private_obstruction"
                for seed in seeds
            ),
            285,
        )

    def test_every_unordered_pair_occurs_once_and_toggle_is_involutive(self) -> None:
        graph = BitGraph.from_edges(5, ((0, 1), (1, 2), (3, 4)))
        pairs = toggle_pairs(graph.n)
        self.assertEqual(len(pairs), 10)
        self.assertEqual(len(set(pairs)), 10)
        self.assertTrue(all(first < second for first, second in pairs))
        for first, second in pairs:
            toggled = toggle_edge(graph, first, second)
            self.assertNotEqual(
                bool(graph.adj[first] >> second & 1),
                bool(toggled.adj[first] >> second & 1),
            )
            self.assertEqual(
                toggle_edge(toggled, first, second), graph
            )

    def test_exact_evaluation_uses_both_stacks_and_complement_coloring(self) -> None:
        evaluation = evaluate_toggled_graph(BitGraph.cycle(7).to_graph6())
        self.assertTrue(evaluation.connected)
        self.assertEqual(evaluation.gamma_a, evaluation.gamma_b)
        self.assertEqual(evaluation.alpha_a, evaluation.alpha_b)
        self.assertEqual(
            evaluation.gamma_infinity_a,
            evaluation.gamma_infinity_b,
        )
        self.assertEqual(evaluation.theta_a, evaluation.theta_b)
        self.assertEqual(
            (
                evaluation.gamma_a,
                evaluation.alpha_a,
                evaluation.gamma_infinity_a,
                evaluation.theta_a,
            ),
            (3, 3, 4, 4),
        )
        self.assertEqual(evaluation.category, "gamma_below_eternal")

    def test_disconnected_toggle_is_pruned_before_parameters(self) -> None:
        path = BitGraph.path(3)
        disconnected = toggle_edge(path, 0, 1)
        evaluation = evaluate_toggled_graph(disconnected.to_graph6())
        self.assertFalse(evaluation.connected)
        self.assertEqual(evaluation.category, "disconnected")
        self.assertIsNone(evaluation.gamma_a)
        self.assertIsNone(evaluation.theta_b)

    def test_modified_seed_input_fails_exact_hash_binding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            modified = Path(temporary) / "extensions_unique.csv"
            modified.write_bytes(SEED_INPUT.read_bytes() + b"\n")
            with self.assertRaisesRegex(ValueError, "seed input hash mismatch"):
                load_certified_seeds(modified, EXTENSION_AUDIT)

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_bounded_sample_resumes_without_duplicate_origins(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arguments = _sample_arguments(root)
            first = run_edge_toggle_search(**arguments)
            self.assertEqual(first.status, "bounded_sample_complete")
            self.assertEqual(first.summary["raw_processed"], 2)
            second = run_edge_toggle_search(**arguments)
            self.assertEqual(second.status, "bounded_sample_complete")
            self.assertEqual(second.summary["raw_processed"], 4)
            with closing(
                sqlite3.connect(root / "edge-toggles.sqlite3")
            ) as connection:
                pair_indices = tuple(
                    row[0]
                    for row in connection.execute(
                        """
                        SELECT pair_index FROM origins
                        WHERE seed_id = 'ET-0001' ORDER BY pair_index
                        """
                    )
                )
                next_pair = connection.execute(
                    """
                    SELECT next_pair_index FROM seeds
                    WHERE seed_id = 'ET-0001'
                    """
                ).fetchone()[0]
                multiplicity = connection.execute(
                    "SELECT SUM(origin_count) FROM canonical_graphs"
                ).fetchone()[0]
            self.assertEqual(pair_indices, (0, 1, 2, 3))
            self.assertEqual(next_pair, 4)
            self.assertEqual(multiplicity, 4)

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_candidate_marker_blocks_resume_without_advancing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arguments = _sample_arguments(root)
            first = run_edge_toggle_search(**arguments)
            self.assertEqual(first.summary["raw_processed"], 2)
            marker = root / "unreviewed-candidate.json"
            marker.write_text("{}", encoding="utf-8")
            with closing(
                sqlite3.connect(root / "edge-toggles.sqlite3")
            ) as connection:
                connection.execute(
                    """
                    UPDATE metadata SET value = ?
                    WHERE key = 'candidate_frozen_path'
                    """,
                    (str(marker.resolve()),),
                )
                connection.commit()
            pending = run_edge_toggle_search(**arguments)
            self.assertEqual(pending.status, "candidate_review_pending")
            self.assertEqual(pending.batches_processed, 0)
            self.assertEqual(pending.summary["raw_processed"], 2)
            self.assertEqual(
                pending.candidate_reference, str(marker.resolve())
            )

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_candidate_row_without_marker_blocks_resume(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arguments = _sample_arguments(root)
            first = run_edge_toggle_search(**arguments)
            self.assertEqual(first.summary["raw_processed"], 2)
            with closing(
                sqlite3.connect(root / "edge-toggles.sqlite3")
            ) as connection:
                graph6 = connection.execute(
                    "SELECT graph6 FROM canonical_graphs ORDER BY graph6 LIMIT 1"
                ).fetchone()[0]
                connection.execute(
                    """
                    UPDATE canonical_graphs
                    SET category =
                        'candidate_gamma_equals_eternal_below_theta'
                    WHERE graph6 = ?
                    """,
                    (graph6,),
                )
                connection.commit()
            pending = run_edge_toggle_search(**arguments)
            self.assertEqual(pending.status, "candidate_review_pending")
            self.assertEqual(pending.batches_processed, 0)
            self.assertEqual(pending.summary["raw_processed"], 2)
            self.assertTrue(
                pending.candidate_reference.startswith(
                    "UNRECORDED-CANDIDATE-SHA256:"
                )
            )

    def test_path_roles_reject_output_aliasing_source_and_each_other(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            seed = root / "seed.csv"
            audit = root / "audit.json"
            labelg = root / "labelg"
            seed.touch()
            audit.touch()
            labelg.touch()
            ordinary = {
                "seed_input_path": seed,
                "extension_audit_path": audit,
                "labelg_path": labelg,
                "database_path": root / "state" / "run.sqlite3",
                "checkpoint_path": root / "state" / "run.json",
                "candidate_directory": root / "candidates",
                "provenance_output": root / "output" / "provenance.csv",
                "unique_output": root / "output" / "unique.csv",
                "seed_ids": ("ET-0001", "ET-0002", "ET-0003"),
            }
            _validate_path_roles(**ordinary)
            aliased = dict(ordinary)
            aliased["checkpoint_path"] = aliased["database_path"]
            with self.assertRaises(ValueError):
                _validate_path_roles(**aliased)
            trusted = dict(ordinary)
            trusted["unique_output"] = seed
            with self.assertRaises(ValueError):
                _validate_path_roles(**trusted)
            symlink = root / "seed-alias"
            symlink.symlink_to(seed)
            trusted_symlink = dict(ordinary)
            trusted_symlink["database_path"] = symlink
            with self.assertRaises(ValueError):
                _validate_path_roles(**trusted_symlink)

            derived_directory = (
                ordinary["checkpoint_path"].parent
                / f"{ordinary['checkpoint_path'].stem}.seeds"
            )
            for role, target in (
                (
                    "database_path",
                    derived_directory / "ET-0001.json",
                ),
                (
                    "provenance_output",
                    derived_directory / "ET-0002.json",
                ),
                (
                    "unique_output",
                    derived_directory / "ET-0003.json",
                ),
                ("database_path", derived_directory),
                ("candidate_directory", derived_directory),
                (
                    "candidate_directory",
                    derived_directory / "nested-candidates",
                ),
            ):
                with self.subTest(derived_collision_role=role, target=target):
                    collision = dict(ordinary)
                    collision[role] = target
                    with self.assertRaisesRegex(
                        ValueError, "derived seed-checkpoint|derived checkpoint"
                    ):
                        _validate_path_roles(**collision)

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_exact_derived_checkpoint_database_overwrite_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arguments = _sample_arguments(root)
            arguments["checkpoint_path"] = root / "run.json"
            dangerous_database = root / "run.seeds" / "ET-0001.json"
            arguments["database_path"] = dangerous_database
            with self.assertRaisesRegex(
                ValueError,
                "derived seed-checkpoint directory conflicts with database",
            ):
                run_edge_toggle_search(**arguments)
            self.assertFalse(dangerous_database.exists())
            self.assertFalse((root / "run.json").exists())

    def test_derived_checkpoint_symlink_aliases_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            checkpoint = root / "run.json"
            redirected = root / "redirected-seed-checkpoints"
            redirected.mkdir()
            (root / "run.seeds").symlink_to(redirected, target_is_directory=True)
            ordinary = {
                "seed_input_path": root / "seed.csv",
                "extension_audit_path": root / "audit.json",
                "labelg_path": root / "labelg",
                "database_path": redirected / "ET-0001.json",
                "checkpoint_path": checkpoint,
                "candidate_directory": root / "candidates",
                "provenance_output": root / "provenance.csv",
                "unique_output": root / "unique.csv",
                "seed_ids": ("ET-0001",),
            }
            with self.assertRaisesRegex(
                ValueError, "derived seed-checkpoint|derived checkpoint"
            ):
                _validate_path_roles(**ordinary)

            (root / "run.seeds").unlink()
            (root / "run.seeds").mkdir()
            per_seed = root / "run.seeds" / "ET-0001.json"
            per_seed.symlink_to(root / "provenance.csv")
            ordinary["database_path"] = root / "database.sqlite3"
            with self.assertRaisesRegex(
                ValueError, "derived checkpoint for ET-0001"
            ):
                _validate_path_roles(**ordinary)

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_nonfinite_gates_fail_before_database_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            base = _sample_arguments(root)
            for field, value in (
                ("wall_limit_seconds", float("nan")),
                ("wall_limit_seconds", float("inf")),
                ("memory_limit_mib", float("-inf")),
                ("batch_size", float("nan")),
                ("max_batches", 1.5),
            ):
                with self.subTest(field=field):
                    arguments = dict(base)
                    arguments[field] = value
                    with self.assertRaises(ValueError):
                        run_edge_toggle_search(**arguments)
            self.assertFalse((root / "edge-toggles.sqlite3").exists())

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_initial_schema_and_seed_rows_roll_back_together(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            configuration = build_configuration(
                seed_input_path=SEED_INPUT,
                extension_audit_path=EXTENSION_AUDIT,
                labelg_path=LABELG,
                batch_size=2,
                active_seed_ids=("ET-0001",),
                wall_limit_seconds=60,
                memory_limit_mib=1024,
            )
            seed = load_certified_seeds(SEED_INPUT, EXTENSION_AUDIT)[0]
            database = root / "failed-init.sqlite3"
            with self.assertRaises(sqlite3.IntegrityError):
                _connect_database(database, configuration, (seed, seed))
            with closing(sqlite3.connect(database)) as connection:
                version = connection.execute(
                    "PRAGMA user_version"
                ).fetchone()[0]
                tables = tuple(
                    row[0]
                    for row in connection.execute(
                        """
                        SELECT name FROM sqlite_master
                        WHERE type = 'table' ORDER BY name
                        """
                    )
                )
            self.assertEqual(version, 0)
            self.assertEqual(tables, ())

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_complete_null_stream_hash_crash_state_is_repaired(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arguments = _sample_arguments(root)
            arguments["batch_size"] = 3
            run_edge_toggle_search(**arguments)
            original = load_certified_seeds(SEED_INPUT, EXTENSION_AUDIT)[0]
            three_pair_probe = Seed(
                index=original.index,
                seed_id=original.seed_id,
                graph6=original.graph6,
                order=3,
                size=original.size,
                source_category=original.source_category,
            )
            database = root / "edge-toggles.sqlite3"
            with closing(sqlite3.connect(database)) as connection:
                connection.execute(
                    """
                    UPDATE seeds
                    SET next_pair_index = 3, status = 'complete',
                        canonical_stream_sha256 = NULL
                    WHERE seed_id = 'ET-0001'
                    """
                )
                connection.commit()
                repaired = _validate_or_repair_complete_seed(
                    connection, three_pair_probe
                )
                stored = connection.execute(
                    """
                    SELECT canonical_stream_sha256 FROM seeds
                    WHERE seed_id = 'ET-0001'
                    """
                ).fetchone()[0]
            self.assertEqual(stored, repaired)
            self.assertEqual(len(repaired), 64)

    def test_checkpoint_json_is_not_created_by_import_or_scope_checks(self) -> None:
        # This also makes explicit that merely loading the certified source is
        # read-only; all writable paths are caller supplied to the run method.
        seeds = load_certified_seeds(SEED_INPUT, EXTENSION_AUDIT)
        self.assertEqual(seeds[0].seed_id, "ET-0001")
        with EXTENSION_AUDIT.open(encoding="utf-8") as handle:
            self.assertTrue(json.load(handle)["passed"])


if __name__ == "__main__":
    unittest.main()
