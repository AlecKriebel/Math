from __future__ import annotations

import json
import inspect
import shutil
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from dataclasses import replace
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from search.extension_killtest import (  # noqa: E402
    TARGET_GUARD_COUNT,
    RUNTIME_SOURCE_RELATIVE_PATHS,
    _connect_database,
    audit_complete_coverage,
    build_configuration,
    canonicalize_graph6_batch,
    evaluate_canonical_extension,
    extend_by_neighborhood,
    load_certified_hosts,
    run_extension_search,
    runtime_source_manifest,
    validate_path_roles,
    validate_or_repair_completed_host,
    verify_pinned_labelg,
)
from verifier_a.core import BitGraph  # noqa: E402


CATALOG = CAMPAIGN / "instances" / "mmv2022_table9.csv"
PARAMETERS = CAMPAIGN / "results" / "mmv2022_parameters.csv"
LABELG = CAMPAIGN / "tools" / "nauty2_9_3" / "labelg"
NAUTY_ARCHIVE = CAMPAIGN / "tools" / "nauty2_9_3.tar.gz"


def _sample_arguments(root: Path) -> dict[str, object]:
    return {
        "catalog_path": CATALOG,
        "parameters_path": PARAMETERS,
        "labelg_path": LABELG,
        "database_path": root / "extensions.sqlite3",
        "checkpoint_path": root / "extensions.json",
        "candidate_directory": root / "candidates",
        "provenance_output": root / "provenance.csv",
        "unique_output": root / "unique.csv",
        "batch_size": 2,
        "active_host_ids": ("MMV-001",),
        "max_batches": 1,
        "wall_limit_seconds": 60,
        "memory_limit_mib": 1024,
    }


def _permuted_graph(graph: BitGraph, old_at_new: tuple[int, ...]) -> BitGraph:
    if sorted(old_at_new) != list(range(graph.n)):
        raise ValueError("not a permutation")
    new_of_old = {
        old_vertex: new_vertex
        for new_vertex, old_vertex in enumerate(old_at_new)
    }
    edges = []
    for first in range(graph.n):
        for second in range(first + 1, graph.n):
            if graph.adj[first] >> second & 1:
                edges.append((new_of_old[first], new_of_old[second]))
    return BitGraph.from_edges(graph.n, edges)


class ExtensionKillTestTests(unittest.TestCase):
    def test_certified_host_selector_and_raw_coverage(self) -> None:
        hosts = load_certified_hosts(CATALOG, PARAMETERS)
        self.assertEqual(len(hosts), 55)
        self.assertEqual(
            sum(host.raw_extension_count for host in hosts), 110_537
        )
        self.assertEqual(
            sum(
                host.gamma == 2 and host.order == 10
                for host in hosts
            ),
            2,
        )
        self.assertEqual(
            sum(
                host.gamma == 2 and host.order == 11
                for host in hosts
            ),
            51,
        )
        self.assertEqual(
            sum(
                host.gamma == 1 and host.order == 11
                for host in hosts
            ),
            2,
        )
        self.assertTrue(
            all(
                host.alpha
                == host.gamma_infinity
                == TARGET_GUARD_COUNT
                < host.theta
                for host in hosts
            )
        )

    def test_extension_uses_exact_nonempty_neighborhood(self) -> None:
        host = BitGraph.path(4)
        extension = extend_by_neighborhood(host, 0b0101)
        self.assertEqual(extension.n, 5)
        self.assertEqual(extension.adj[4], 0b0101)
        self.assertTrue(extension.adj[0] >> 4 & 1)
        self.assertFalse(extension.adj[1] >> 4 & 1)
        self.assertTrue(extension.adj[2] >> 4 & 1)
        self.assertFalse(extension.adj[3] >> 4 & 1)
        with self.assertRaises(ValueError):
            extend_by_neighborhood(host, 0)
        with self.assertRaises(ValueError):
            extend_by_neighborhood(host, 1 << host.n)

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_labelg_canonicalization_identifies_isomorphic_inputs(self) -> None:
        graph = BitGraph.from_edges(
            7,
            (
                (0, 1),
                (1, 2),
                (2, 3),
                (3, 4),
                (4, 0),
                (2, 5),
                (5, 6),
            ),
        )
        relabeled = _permuted_graph(graph, (3, 6, 1, 5, 0, 4, 2))
        first, second = canonicalize_graph6_batch(
            (graph.to_graph6(), relabeled.to_graph6()), LABELG
        )
        self.assertEqual(first, second)
        self.assertEqual(
            canonicalize_graph6_batch((first,), LABELG), (first,)
        )

    def test_c7_reaches_both_eternal_implementations(self) -> None:
        # This canonical graph is isomorphic to C7.  The private-state test
        # alone does not reject it, but both exact one-guard solvers do.
        evaluation = evaluate_canonical_extension("FCp`_")
        self.assertEqual(evaluation.gamma, 3)
        self.assertEqual(evaluation.alpha, 3)
        self.assertEqual(
            evaluation.category,
            "eternal_false_without_private_obstruction",
        )
        self.assertFalse(evaluation.eternal_a)
        self.assertFalse(evaluation.eternal_b)
        self.assertEqual(evaluation.family_a_size, 0)
        self.assertEqual(evaluation.family_b_size, 0)

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_bounded_sample_resumes_without_duplicate_origins(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            common = _sample_arguments(root)
            first = run_extension_search(**common)
            self.assertEqual(first.status, "bounded_sample_complete")
            self.assertEqual(first.summary["raw_processed"], 2)
            second = run_extension_search(**common)
            self.assertEqual(second.status, "bounded_sample_complete")
            self.assertEqual(second.summary["raw_processed"], 4)

            with closing(
                sqlite3.connect(root / "extensions.sqlite3")
            ) as connection:
                masks = tuple(
                    row[0]
                    for row in connection.execute(
                        """
                        SELECT neighborhood_mask FROM origins
                        WHERE host_id = 'MMV-001'
                        ORDER BY neighborhood_mask
                        """
                    )
                )
                next_mask = connection.execute(
                    """
                    SELECT next_mask FROM hosts WHERE catalog_id = 'MMV-001'
                    """
                ).fetchone()[0]
                multiplicity_total = connection.execute(
                    "SELECT SUM(origin_count) FROM canonical_graphs"
                ).fetchone()[0]
            self.assertEqual(masks, (1, 2, 3, 4))
            self.assertEqual(next_mask, 5)
            self.assertEqual(multiplicity_total, 4)
            with (root / "extensions.json").open(encoding="utf-8") as handle:
                snapshot = json.load(handle)
            self.assertEqual(
                snapshot["database_sha256"],
                second.summary["database_sha256"],
            )
            self.assertEqual(snapshot["raw_processed"], 4)
            self.assertEqual(
                sum(snapshot["raw_category_counts"].values()), 4
            )

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_marker_alone_blocks_every_resume_without_advancing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            common = _sample_arguments(root)
            first = run_extension_search(**common)
            self.assertEqual(first.summary["raw_processed"], 2)
            forged_marker = root / "unreviewed-candidate.json"
            with closing(
                sqlite3.connect(root / "extensions.sqlite3")
            ) as connection:
                connection.execute(
                    """
                    UPDATE metadata SET value = ?
                    WHERE key = 'candidate_frozen_path'
                    """,
                    (str(forged_marker.resolve()),),
                )
                connection.commit()

            pending = run_extension_search(**common)
            self.assertEqual(pending.status, "candidate_review_pending")
            self.assertEqual(pending.batches_processed, 0)
            self.assertEqual(pending.summary["raw_processed"], 2)
            self.assertEqual(
                pending.candidate_path, str(forged_marker.resolve())
            )
            state = pending.summary["candidate_state"]
            self.assertTrue(state["pending"])
            self.assertEqual(state["candidate_row_count"], 0)
            self.assertIn(
                "freeze marker exists without a candidate row",
                state["inconsistencies"],
            )
            self.assertIsNotNone(pending.summary["candidate_path"])

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_candidate_row_alone_blocks_resume_and_completion_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            common = _sample_arguments(root)
            first = run_extension_search(**common)
            self.assertEqual(first.summary["raw_processed"], 2)
            with closing(
                sqlite3.connect(root / "extensions.sqlite3")
            ) as connection:
                graph6 = connection.execute(
                    """
                    SELECT graph6 FROM canonical_graphs ORDER BY graph6 LIMIT 1
                    """
                ).fetchone()[0]
                connection.execute(
                    """
                    UPDATE canonical_graphs
                    SET category = 'candidate_eternal_3'
                    WHERE graph6 = ?
                    """,
                    (graph6,),
                )
                connection.commit()

            pending = run_extension_search(**common)
            self.assertEqual(pending.status, "candidate_review_pending")
            self.assertEqual(pending.batches_processed, 0)
            self.assertEqual(pending.summary["raw_processed"], 2)
            self.assertTrue(
                pending.candidate_path.startswith(
                    "UNRECORDED-CANDIDATE-SHA256:"
                )
            )
            state = pending.summary["candidate_state"]
            self.assertEqual(state["candidate_row_count"], 1)
            self.assertIn(
                "candidate row exists without a freeze marker",
                state["inconsistencies"],
            )
            self.assertIsNotNone(pending.summary["candidate_path"])

            with closing(
                sqlite3.connect(root / "extensions.sqlite3")
            ) as connection:
                audit = audit_complete_coverage(
                    connection, load_certified_hosts(CATALOG, PARAMETERS)
                )
            self.assertFalse(audit["passed"])
            self.assertTrue(audit["candidate_state"]["pending"])
            self.assertIn(
                "candidate state is pending review; completion is forbidden",
                audit["errors"],
            )

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_candidate_origin_row_alone_blocks_resume(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            common = _sample_arguments(root)
            first = run_extension_search(**common)
            self.assertEqual(first.summary["raw_processed"], 2)
            with closing(
                sqlite3.connect(root / "extensions.sqlite3")
            ) as connection:
                connection.execute(
                    """
                    UPDATE origins SET category = 'candidate_eternal_3'
                    WHERE host_id = 'MMV-001' AND neighborhood_mask = 1
                    """
                )
                connection.commit()

            pending = run_extension_search(**common)
            self.assertEqual(pending.status, "candidate_review_pending")
            self.assertEqual(pending.batches_processed, 0)
            self.assertEqual(pending.summary["raw_processed"], 2)
            state = pending.summary["candidate_state"]
            self.assertEqual(state["canonical_candidate_row_count"], 0)
            self.assertEqual(state["candidate_origin_row_count"], 1)
            self.assertIn(
                "candidate origin row exists without a canonical candidate row",
                state["inconsistencies"],
            )
            self.assertIsNotNone(pending.summary["candidate_path"])

    def test_no_candidate_continuation_override_exists(self) -> None:
        self.assertNotIn(
            "continue_after_candidate",
            inspect.signature(run_extension_search).parameters,
        )

    def test_named_directory_cannot_spoof_pinned_labelg(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "nauty2_9_3"
            directory.mkdir()
            (directory / "This_is_nauty2_9_3.txt").touch()
            shutil.copy2(
                NAUTY_ARCHIVE, directory.parent / "nauty2_9_3.tar.gz"
            )
            impostor = directory / "labelg"
            impostor.write_bytes(b"#!/bin/sh\nexit 0\n")
            impostor.chmod(0o755)
            with self.assertRaisesRegex(
                ValueError, "executable hash does not match"
            ):
                verify_pinned_labelg(impostor)

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_pinned_labelg_requires_the_bound_source_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "nauty2_9_3"
            directory.mkdir()
            (directory / "This_is_nauty2_9_3.txt").touch()
            copied = directory / "labelg"
            shutil.copy2(LABELG, copied)
            with self.assertRaisesRegex(ValueError, "source archive is missing"):
                verify_pinned_labelg(copied)

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_runtime_sources_and_python_are_bound_into_resume_digest(self) -> None:
        manifest = runtime_source_manifest()
        self.assertEqual(
            tuple(relative for relative, _ in manifest),
            RUNTIME_SOURCE_RELATIVE_PATHS,
        )
        self.assertTrue(all(len(digest) == 64 for _, digest in manifest))
        configuration = build_configuration(
            catalog_path=CATALOG,
            parameters_path=PARAMETERS,
            labelg_path=LABELG,
            batch_size=2,
            active_host_ids=("MMV-001",),
            wall_limit_seconds=60,
            memory_limit_mib=1024,
        )
        self.assertEqual(configuration.runtime_source_manifest, manifest)
        self.assertEqual(len(configuration.runtime_source_set_sha256), 64)
        self.assertTrue(configuration.python_implementation)
        self.assertTrue(configuration.python_version)
        self.assertTrue(configuration.python_executable)
        with tempfile.TemporaryDirectory() as temporary:
            database = Path(temporary) / "runtime-binding.sqlite3"
            hosts = load_certified_hosts(CATALOG, PARAMETERS)
            _connect_database(database, configuration, hosts).close()
            changed = replace(
                configuration, runtime_source_set_sha256="0" * 64
            )
            with self.assertRaisesRegex(
                ValueError, "configuration does not match"
            ):
                _connect_database(database, changed, hosts)

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_nonfinite_and_noninteger_resource_gates_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            base = _sample_arguments(root)
            cases = (
                ("wall_limit_seconds", float("nan")),
                ("wall_limit_seconds", float("inf")),
                ("wall_limit_seconds", float("-inf")),
                ("memory_limit_mib", float("nan")),
                ("memory_limit_mib", float("inf")),
                ("memory_limit_mib", float("-inf")),
                ("batch_size", float("nan")),
                ("batch_size", True),
                ("max_batches", float("inf")),
                ("max_batches", 1.5),
            )
            for field, value in cases:
                with self.subTest(field=field, value=value):
                    arguments = dict(base)
                    arguments[field] = value
                    with self.assertRaises(ValueError):
                        run_extension_search(**arguments)
            self.assertFalse((root / "extensions.sqlite3").exists())

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_legacy_complete_null_hash_state_is_repaired(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arguments = _sample_arguments(root)
            arguments["batch_size"] = 3
            run_extension_search(**arguments)
            database = root / "extensions.sqlite3"
            with closing(sqlite3.connect(database)) as connection:
                connection.execute(
                    """
                    UPDATE hosts
                    SET next_mask = 4, status = 'complete',
                        canonical_stream_sha256 = NULL
                    WHERE catalog_id = 'MMV-001'
                    """
                )
                connection.commit()
                repaired = validate_or_repair_completed_host(
                    connection, "MMV-001", 3
                )
                stored = connection.execute(
                    """
                    SELECT canonical_stream_sha256 FROM hosts
                    WHERE catalog_id = 'MMV-001'
                    """
                ).fetchone()[0]
            self.assertEqual(stored, repaired)
            self.assertEqual(len(repaired), 64)

    @unittest.skipUnless(LABELG.is_file(), "pinned labelg is not built")
    def test_schema_metadata_and_hosts_roll_back_together(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            configuration = build_configuration(
                catalog_path=CATALOG,
                parameters_path=PARAMETERS,
                labelg_path=LABELG,
                batch_size=2,
                active_host_ids=("MMV-001",),
                wall_limit_seconds=60,
                memory_limit_mib=1024,
            )
            host = load_certified_hosts(CATALOG, PARAMETERS)[0]
            database = root / "failed-initialization.sqlite3"
            with self.assertRaises(sqlite3.IntegrityError):
                _connect_database(database, configuration, (host, host))
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

    def test_conflicting_and_trusted_path_roles_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            catalog = root / "catalog.csv"
            parameters = root / "parameters.csv"
            labelg = root / "labelg"
            catalog.write_text("catalog", encoding="utf-8")
            parameters.write_text("parameters", encoding="utf-8")
            labelg.write_text("labelg", encoding="utf-8")
            ordinary = {
                "catalog_path": catalog,
                "parameters_path": parameters,
                "labelg_path": labelg,
                "database_path": root / "run" / "ledger.sqlite3",
                "checkpoint_path": root / "run" / "checkpoint.json",
                "candidate_directory": root / "candidates",
                "provenance_output": root / "output" / "provenance.csv",
                "unique_output": root / "output" / "unique.csv",
            }
            validate_path_roles(**ordinary)

            cases: list[dict[str, Path]] = []
            same_ledger = dict(ordinary)
            same_ledger["checkpoint_path"] = same_ledger["database_path"]
            cases.append(same_ledger)
            same_exports = dict(ordinary)
            same_exports["unique_output"] = same_exports["provenance_output"]
            cases.append(same_exports)
            trusted_alias = dict(ordinary)
            trusted_alias["checkpoint_path"] = catalog
            cases.append(trusted_alias)
            nested_candidate = dict(ordinary)
            nested_candidate["checkpoint_path"] = (
                nested_candidate["candidate_directory"] / "checkpoint.json"
            )
            cases.append(nested_candidate)

            symlink_alias = dict(ordinary)
            catalog_alias = root / "catalog-alias"
            catalog_alias.symlink_to(catalog)
            symlink_alias["database_path"] = catalog_alias
            cases.append(symlink_alias)

            for arguments in cases:
                with self.subTest(arguments=arguments):
                    with self.assertRaises(ValueError):
                        validate_path_roles(**arguments)


if __name__ == "__main__":
    unittest.main()
