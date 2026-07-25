from __future__ import annotations

import ast
import csv
from contextlib import closing
from dataclasses import dataclass
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile
import unittest


CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from coverage_checker.audit import (  # noqa: E402
    AuditError,
    AuditPaths,
    AuditPolicy,
    CHECKER_SOURCE_PATHS,
    EMPTY_SHA256,
    PROVENANCE_HEADER,
    UNIQUE_HEADER,
    run_postrun_audit,
)
from coverage_checker.catalog import (  # noqa: E402
    CATALOG_HEADER,
    PARAMETERS_HEADER,
    PRODUCTION_POLICY,
    UniversePolicy,
    load_host_universe,
    sha256_file,
)
from coverage_checker.graph import Graph  # noqa: E402


def _canonical_json_digest(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def _write_csv(
    path: Path, header: tuple[str, ...], rows: list[tuple[object, ...]]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def _canonical_small(graph: Graph) -> str:
    return min(
        graph.relabel(permutation).to_graph6()
        for permutation in itertools.permutations(range(graph.order))
    )


@dataclass(frozen=True)
class Fixture:
    paths: AuditPaths
    policy: AuditPolicy
    mask_to_canonical: dict[int, str]


def _create_fixture(
    root: Path,
    *,
    raw_mismatch: bool = False,
    nonisomorphic_canonical: bool = False,
    multiplicity_adjustment: int = 0,
    active_host_ids: tuple[str, ...] = (),
    omit_mask: int | None = None,
) -> Fixture:
    for relative in CHECKER_SOURCE_PATHS:
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(CAMPAIGN / relative, destination)
    runtime_relative = "src/search/extension_killtest.py"
    runtime_path = root / runtime_relative
    runtime_path.parent.mkdir(parents=True, exist_ok=True)
    runtime_path.write_text("# synthetic bound engine\n", encoding="ascii")

    labelg = root / "tools" / "nauty2_9_3" / "labelg"
    labelg.parent.mkdir(parents=True)
    labelg.write_bytes(b"synthetic labelg executable\n")
    archive = root / "tools" / "nauty2_9_3.tar.gz"
    archive.write_bytes(b"synthetic nauty archive\n")

    host = Graph.from_edges(3, ((0, 1), (1, 2)))
    catalog = root / "catalog.csv"
    parameters = root / "parameters.csv"
    _write_csv(
        catalog,
        CATALOG_HEADER,
        [("TEST-001", 3, host.to_graph6(), "synthetic fixture")],
    )
    _write_csv(
        parameters,
        PARAMETERS_HEADER,
        [
            (
                "TEST-001",
                3,
                2,
                host.to_graph6(),
                1,
                2,
                2,
                2,
                3,
                "1",
                1,
                "0 2",
                "0 2",
                1,
                EMPTY_SHA256,
            )
        ],
    )
    universe = UniversePolicy(
        catalog_sha256=sha256_file(catalog),
        parameters_sha256=sha256_file(parameters),
        input_rows=1,
        selected_hosts=1,
        raw_origins=7,
        target_guard_count=2,
        distribution=((3, 1, 1),),
    )
    policy = AuditPolicy(
        universe=universe,
        labelg_sha256=sha256_file(labelg),
        nauty_archive_sha256=sha256_file(archive),
        runtime_source_paths=(runtime_relative,),
    )

    raw_by_mask = {
        mask: host.add_extension(mask).to_graph6() for mask in range(1, 8)
    }
    canonical_by_mask = {
        mask: _canonical_small(Graph.from_graph6(raw))
        for mask, raw in raw_by_mask.items()
    }
    if raw_mismatch:
        raw_by_mask[1] = raw_by_mask[2]
        canonical_by_mask[1] = canonical_by_mask[2]
    if nonisomorphic_canonical:
        # Masks one and two both have three edges, but give P4 and K1,3.
        if canonical_by_mask[1] == canonical_by_mask[2]:
            raise AssertionError("fixture graphs unexpectedly isomorphic")
        canonical_by_mask[1] = canonical_by_mask[2]

    grouped: dict[str, list[int]] = {}
    active_masks = tuple(
        mask for mask in range(1, 8) if mask != omit_mask
    )
    for mask in active_masks:
        grouped.setdefault(canonical_by_mask[mask], []).append(mask)
    database = root / "extensions.sqlite3"
    configuration_manifest = [
        [runtime_relative, sha256_file(runtime_path)]
    ]
    configuration = {
        "catalog_path": str(catalog.resolve()),
        "catalog_sha256": sha256_file(catalog),
        "parameters_path": str(parameters.resolve()),
        "parameters_sha256": sha256_file(parameters),
        "labelg_path": str(labelg.resolve()),
        "labelg_sha256": sha256_file(labelg),
        "nauty_archive_sha256": sha256_file(archive),
        "engine_sha256": sha256_file(runtime_path),
        "runtime_source_manifest": configuration_manifest,
        "runtime_source_set_sha256": hashlib.sha256(
            (
                f"{runtime_relative} {sha256_file(runtime_path)}\n"
            ).encode("ascii")
        ).hexdigest(),
        "python_implementation": "CPython",
        "python_version": ".".join(map(str, sys.version_info[:3])),
        "python_executable": str(Path(sys.executable).resolve()),
        "batch_size": 2,
        "active_host_ids": list(active_host_ids),
        "wall_limit_seconds": 60.0,
        "memory_limit_mib": 1024.0,
        "target_guard_count": 2,
        "schema_version": 1,
    }
    configuration_digest = _canonical_json_digest(configuration)
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(
            """
            CREATE TABLE metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE hosts (
                host_index INTEGER NOT NULL UNIQUE,
                catalog_id TEXT PRIMARY KEY,
                n INTEGER NOT NULL,
                graph6 TEXT NOT NULL,
                gamma INTEGER NOT NULL,
                alpha INTEGER NOT NULL,
                gamma_infinity INTEGER NOT NULL,
                theta INTEGER NOT NULL,
                raw_expected INTEGER NOT NULL,
                next_mask INTEGER NOT NULL,
                status TEXT NOT NULL,
                canonical_stream_sha256 TEXT
            );
            CREATE TABLE canonical_graphs (
                graph6 TEXT PRIMARY KEY,
                n INTEGER NOT NULL,
                m INTEGER NOT NULL,
                first_host_id TEXT NOT NULL,
                first_neighborhood_mask INTEGER NOT NULL,
                first_raw_graph6 TEXT NOT NULL,
                origin_count INTEGER NOT NULL,
                gamma INTEGER NOT NULL,
                alpha INTEGER NOT NULL,
                category TEXT NOT NULL,
                private_obstruction_json TEXT,
                eternal_a INTEGER,
                eternal_b INTEGER,
                family_a_size INTEGER,
                family_b_size INTEGER,
                family_a_sha256 TEXT,
                family_b_sha256 TEXT,
                FOREIGN KEY(first_host_id) REFERENCES hosts(catalog_id)
            );
            CREATE TABLE origins (
                host_id TEXT NOT NULL,
                neighborhood_mask INTEGER NOT NULL,
                neighborhood_size INTEGER NOT NULL,
                raw_graph6 TEXT NOT NULL,
                canonical_graph6 TEXT NOT NULL,
                gamma_delta INTEGER NOT NULL,
                alpha_delta INTEGER NOT NULL,
                category TEXT NOT NULL,
                PRIMARY KEY(host_id, neighborhood_mask),
                FOREIGN KEY(host_id) REFERENCES hosts(catalog_id),
                FOREIGN KEY(canonical_graph6) REFERENCES canonical_graphs(graph6)
            );
            """
        )
        connection.executemany(
            "INSERT INTO metadata(key, value) VALUES (?, ?)",
            (
                (
                    "configuration_json",
                    json.dumps(configuration, sort_keys=True),
                ),
                ("configuration_sha256", configuration_digest),
                ("candidate_frozen_path", ""),
            ),
        )
        stream = hashlib.sha256()
        for mask in active_masks:
            stream.update(canonical_by_mask[mask].encode("ascii") + b"\n")
        connection.execute(
            """
            INSERT INTO hosts VALUES (
                0, 'TEST-001', 3, ?, 1, 2, 2, 3, 7, 8, 'complete', ?
            )
            """,
            (host.to_graph6(), stream.hexdigest()),
        )
        for canonical, masks in grouped.items():
            first = min(masks)
            graph = Graph.from_graph6(canonical)
            origin_count = len(masks)
            if canonical == sorted(grouped)[0]:
                origin_count += multiplicity_adjustment
            connection.execute(
                """
                INSERT INTO canonical_graphs VALUES (
                    ?, ?, ?, 'TEST-001', ?, ?, ?, 1, 3,
                    'gamma_below_3', NULL, NULL, NULL, NULL, NULL, NULL, NULL
                )
                """,
                (
                    canonical,
                    graph.order,
                    graph.size,
                    first,
                    raw_by_mask[first],
                    origin_count,
                ),
            )
        for mask in active_masks:
            connection.execute(
                """
                INSERT INTO origins VALUES (
                    'TEST-001', ?, ?, ?, ?, 0, 1, 'gamma_below_3'
                )
                """,
                (
                    mask,
                    mask.bit_count(),
                    raw_by_mask[mask],
                    canonical_by_mask[mask],
                ),
            )
        connection.execute("PRAGMA user_version = 1")
        connection.commit()

    provenance = root / "provenance.csv"
    unique = root / "unique.csv"
    with closing(sqlite3.connect(database)) as connection:
        _write_csv(
            provenance,
            PROVENANCE_HEADER,
            list(
                connection.execute(
                    """
                    SELECT o.host_id, o.neighborhood_mask,
                           o.neighborhood_size, o.raw_graph6,
                           o.canonical_graph6, o.gamma_delta,
                           o.alpha_delta, o.category
                    FROM origins AS o JOIN hosts AS h
                      ON h.catalog_id = o.host_id
                    ORDER BY h.host_index, o.neighborhood_mask
                    """
                )
            ),
        )
        _write_csv(
            unique,
            UNIQUE_HEADER,
            list(
                connection.execute(
                    """
                    SELECT graph6, n, m, origin_count, first_host_id,
                           first_neighborhood_mask, first_raw_graph6, gamma,
                           alpha, category, private_obstruction_json,
                           eternal_a, eternal_b, family_a_size, family_b_size,
                           family_a_sha256, family_b_sha256
                    FROM canonical_graphs ORDER BY n, graph6
                    """
                )
            ),
        )
        stream_hash = connection.execute(
            "SELECT canonical_stream_sha256 FROM hosts"
        ).fetchone()[0]
        unique_count = connection.execute(
            "SELECT COUNT(*) FROM canonical_graphs"
        ).fetchone()[0]

    checkpoint = root / "checkpoint.json"
    database_hash = sha256_file(database)
    checkpoint_payload = {
        "status": "complete",
        "configuration": configuration,
        "configuration_sha256": configuration_digest,
        "database": str(database.resolve()),
        "database_sha256": database_hash,
        "raw_expected": 7,
        "raw_processed": 7,
        "unique_canonical_graphs": unique_count,
        "hosts_complete": 1,
        "candidate_path": None,
        "candidate_state": {"pending": False},
        "coverage_audit": {
            "passed": True,
            "errors": [],
            "raw_expected": 7,
            "raw_origins": 7,
            "stored_origin_multiplicity": 7,
            "bad_canonical_multiplicity_count": 0,
            "host_canonical_stream_sha256": {"TEST-001": stream_hash},
        },
        "hosts": [
            {
                "catalog_id": "TEST-001",
                "raw_expected": 7,
                "raw_processed": 7,
                "next_mask": 8,
                "status": "complete",
                "canonical_stream_sha256": stream_hash,
            }
        ],
        "output_sha256": {
            str(provenance.resolve()): sha256_file(provenance),
            str(unique.resolve()): sha256_file(unique),
        },
    }
    checkpoint.write_text(
        json.dumps(checkpoint_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    paths = AuditPaths(
        campaign_root=root,
        catalog=catalog,
        parameters=parameters,
        database=database,
        checkpoint=checkpoint,
        provenance_csv=provenance,
        unique_csv=unique,
        state_database=root / "audit-state.sqlite3",
        report=root / "audit-report.json",
    )
    return Fixture(paths, policy, canonical_by_mask)


class CoverageAuditTests(unittest.TestCase):
    def test_resumable_end_to_end_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = _create_fixture(Path(temporary))
            first = run_postrun_audit(
                paths=fixture.paths,
                policy=fixture.policy,
                checkpoint_interval=2,
                max_new_origins=3,
            )
            self.assertEqual(first.status, "in_progress")
            self.assertEqual(first.verified_origins, 3)
            second = run_postrun_audit(
                paths=fixture.paths,
                policy=fixture.policy,
                checkpoint_interval=2,
                max_new_origins=2,
            )
            self.assertEqual(second.verified_origins, 5)
            final = run_postrun_audit(
                paths=fixture.paths,
                policy=fixture.policy,
                checkpoint_interval=2,
            )
            self.assertEqual(final.status, "complete")
            self.assertEqual(final.verified_origins, 7)
            self.assertIsNotNone(final.unique_canonical_graphs)
            report = json.loads(fixture.paths.report.read_text())
            self.assertTrue(report["passed"])
            self.assertEqual(report["origin_chain_sha256"], final.origin_chain_sha256)
            self.assertEqual(
                report["state_database_sha256"],
                sha256_file(fixture.paths.state_database),
            )

            repeated = run_postrun_audit(
                paths=fixture.paths, policy=fixture.policy
            )
            self.assertEqual(repeated.status, "complete")
            self.assertEqual(repeated.origin_chain_sha256, final.origin_chain_sha256)

    def test_rejects_wrong_raw_host_mask_reconstruction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = _create_fixture(Path(temporary), raw_mismatch=True)
            with self.assertRaisesRegex(AuditError, "raw reconstruction"):
                run_postrun_audit(paths=fixture.paths, policy=fixture.policy)

    def test_rejects_a_missing_mask_in_the_middle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = _create_fixture(Path(temporary), omit_mask=4)
            with self.assertRaisesRegex(AuditError, "origins|gap/reordering"):
                run_postrun_audit(paths=fixture.paths, policy=fixture.policy)

    def test_rejects_nonisomorphic_raw_to_canonical_pair(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = _create_fixture(
                Path(temporary), nonisomorphic_canonical=True
            )
            with self.assertRaisesRegex(AuditError, "not isomorphic"):
                run_postrun_audit(paths=fixture.paths, policy=fixture.policy)

    def test_rejects_canonical_multiplicity_corruption(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = _create_fixture(
                Path(temporary), multiplicity_adjustment=1
            )
            with self.assertRaisesRegex(AuditError, "multiplicity"):
                run_postrun_audit(paths=fixture.paths, policy=fixture.policy)

    def test_rejects_full_run_configuration_with_active_shard(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = _create_fixture(
                Path(temporary), active_host_ids=("TEST-001",)
            )
            with self.assertRaisesRegex(AuditError, "host shard"):
                run_postrun_audit(paths=fixture.paths, policy=fixture.policy)

    def test_rejects_csv_change_even_when_checkpoint_hash_is_rebound(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = _create_fixture(Path(temporary))
            rows: list[list[str]]
            with fixture.paths.provenance_csv.open(
                encoding="utf-8", newline=""
            ) as handle:
                rows = list(csv.reader(handle))
            rows[1][6] = "999"
            with fixture.paths.provenance_csv.open(
                "w", encoding="utf-8", newline=""
            ) as handle:
                csv.writer(handle).writerows(rows)
            checkpoint = json.loads(fixture.paths.checkpoint.read_text())
            checkpoint["output_sha256"][
                str(fixture.paths.provenance_csv.resolve())
            ] = sha256_file(fixture.paths.provenance_csv)
            fixture.paths.checkpoint.write_text(
                json.dumps(checkpoint, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(AuditError, "CSV row"):
                run_postrun_audit(paths=fixture.paths, policy=fixture.policy)

    def test_rejects_live_sqlite_companion_and_bad_resource_controls(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = _create_fixture(Path(temporary))
            companion = Path(str(fixture.paths.database) + "-wal")
            companion.write_bytes(b"not quiescent")
            with self.assertRaisesRegex(AuditError, "companion"):
                run_postrun_audit(paths=fixture.paths, policy=fixture.policy)
            companion.unlink()
            for kwargs in (
                {"checkpoint_interval": 0},
                {"checkpoint_interval": True},
                {"max_new_origins": 0},
                {"wall_limit_seconds": float("nan")},
                {"memory_limit_mib": float("inf")},
            ):
                with self.subTest(kwargs=kwargs):
                    with self.assertRaises(AuditError):
                        run_postrun_audit(
                            paths=fixture.paths,
                            policy=fixture.policy,
                            **kwargs,
                        )

    def test_resume_replays_and_rejects_a_tampered_mapping_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = _create_fixture(Path(temporary))
            partial = run_postrun_audit(
                paths=fixture.paths,
                policy=fixture.policy,
                max_new_origins=3,
            )
            self.assertEqual(partial.status, "in_progress")
            with closing(sqlite3.connect(fixture.paths.state_database)) as state:
                state.execute(
                    """
                    UPDATE origin_receipts SET mapping_json = '[0,0,0,0]'
                    WHERE host_index = 0 AND neighborhood_mask = 1
                    """
                )
                state.commit()
            with self.assertRaisesRegex(AuditError, "isomorphism|mapping"):
                run_postrun_audit(paths=fixture.paths, policy=fixture.policy)


class ProductionUniverseTests(unittest.TestCase):
    def test_independent_catalog_join_is_exactly_55_and_110537(self) -> None:
        hosts = load_host_universe(
            CAMPAIGN / "instances" / "mmv2022_table9.csv",
            CAMPAIGN / "results" / "mmv2022_parameters.csv",
            policy=PRODUCTION_POLICY,
        )
        self.assertEqual(len(hosts), 55)
        self.assertEqual(sum(host.raw_expected for host in hosts), 110_537)
        distribution: dict[tuple[int, int], int] = {}
        for host in hosts:
            key = (host.order, host.gamma)
            distribution[key] = distribution.get(key, 0) + 1
        self.assertEqual(
            distribution,
            {(10, 2): 2, (11, 1): 2, (11, 2): 51},
        )

    def test_checker_has_no_search_or_campaign_verifier_import(self) -> None:
        forbidden: list[tuple[str, str]] = []
        for path in sorted(
            (CAMPAIGN / "src" / "coverage_checker").glob("*.py")
        ):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                modules: tuple[str, ...] = ()
                if isinstance(node, ast.Import):
                    modules = tuple(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module is not None:
                    modules = (node.module,)
                for module in modules:
                    if module == "search" or module.startswith(
                        ("search.", "verifier_a", "verifier_b")
                    ):
                        forbidden.append((path.name, module))
        self.assertEqual(forbidden, [])


if __name__ == "__main__":
    unittest.main()
