"""Complete, resumable one-vertex-extension search around the MMV near-misses.

The mathematical search universe is specified in
``math/extension_search_scope.md``.  This program deliberately has no
heuristic sampling mode in its command-line entry point: it reads the
certified 2022 catalog, selects exactly the 55 hosts with
``alpha = gamma_infinity = 3 < theta``, and enumerates every nonempty
neighborhood of the added vertex.

Progress and provenance live in an ACID SQLite database.  A batch transaction
inserts the raw origins, globally deduplicated canonical graphs, exact filter
outcomes, and the next neighborhood mask together.  Replaying after a crash
therefore cannot omit or double-count an origin.  Atomic JSON snapshots are
human-readable mirrors, not the source of truth.

The full campaign is guarded by the explicit ``--validation-gate-open`` flag.
Unit tests call the library API on a bounded sample; importing this module
never starts a search.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import resource
import sqlite3
import subprocess
import sys
import tempfile
import time
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Iterator, Sequence

from search.private_obstruction import (
    PrivateObstruction,
    find_private_obstruction,
    verify_private_obstruction,
)
from verifier_a.core import (
    BitGraph,
    EternalResult,
    alpha,
    domination_number,
    eternal_fixed_point,
    verify_eternal_result,
)
from verifier_b import Graph, find_eternal_family, verify_eternal_family


SCHEMA_VERSION = 1
EXPECTED_CATALOG_SHA256 = (
    "801f054853d07652c795fb16217425869f857d7f5d74e427165d554faf4eae1d"
)
EXPECTED_PARAMETERS_SHA256 = (
    "ef74175dfd81542a167feed5a2d7f66be723846993642fb65344d08655b594c6"
)
EXPECTED_LABELG_SHA256 = (
    "ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0"
)
NAUTY_ARCHIVE_SHA256 = (
    "9fc4edae04f88a0f5883985be3b39cf7f898fd6cc96e96b9ee25452743cc1b5b"
)
TARGET_GUARD_COUNT = 3
RUNTIME_SOURCE_RELATIVE_PATHS = (
    "src/search/extension_killtest.py",
    "src/search/private_obstruction.py",
    "src/verifier_a/core.py",
    "src/verifier_b/__init__.py",
    "src/verifier_b/graph.py",
    "src/verifier_b/invariants.py",
    "src/verifier_b/eternal.py",
)


@dataclass(frozen=True, slots=True)
class Host:
    index: int
    catalog_id: str
    order: int
    graph6: str
    gamma: int
    alpha: int
    gamma_infinity: int
    theta: int

    @property
    def raw_extension_count(self) -> int:
        return (1 << self.order) - 1


@dataclass(frozen=True, slots=True)
class SearchConfiguration:
    catalog_path: str
    catalog_sha256: str
    parameters_path: str
    parameters_sha256: str
    labelg_path: str
    labelg_sha256: str
    nauty_archive_sha256: str
    engine_sha256: str
    runtime_source_manifest: tuple[tuple[str, str], ...]
    runtime_source_set_sha256: str
    python_implementation: str
    python_version: str
    python_executable: str
    batch_size: int
    active_host_ids: tuple[str, ...]
    wall_limit_seconds: float
    memory_limit_mib: float
    target_guard_count: int = TARGET_GUARD_COUNT
    schema_version: int = SCHEMA_VERSION

    @property
    def digest(self) -> str:
        encoded = json.dumps(
            asdict(self), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class Evaluation:
    gamma: int
    alpha: int
    category: str
    private_obstruction_json: str | None
    eternal_a: bool | None
    eternal_b: bool | None
    family_a_size: int | None
    family_b_size: int | None
    family_a_sha256: str | None
    family_b_sha256: str | None
    eternal_result_a: EternalResult | None = None
    eternal_family_b: frozenset[frozenset[int]] | None = None


@dataclass(frozen=True, slots=True)
class RunOutcome:
    status: str
    batches_processed: int
    candidate_path: str | None
    summary: dict[str, object]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def runtime_source_manifest() -> tuple[tuple[str, str], ...]:
    """Bind every campaign source module used to evaluate an extension."""

    campaign_root = Path(__file__).resolve().parents[2]
    records: list[tuple[str, str]] = []
    for relative in RUNTIME_SOURCE_RELATIVE_PATHS:
        path = campaign_root / relative
        if not path.is_file():
            raise ValueError(f"runtime source dependency is missing: {path}")
        records.append((relative, sha256_file(path)))
    return tuple(records)


def _runtime_source_set_sha256(
    manifest: Sequence[tuple[str, str]],
) -> str:
    digest = hashlib.sha256()
    for relative, source_hash in manifest:
        digest.update(f"{relative} {source_hash}\n".encode("ascii"))
    return digest.hexdigest()


def _atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".partial", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _atomic_csv(
    path: Path, header: Sequence[str], rows: Iterable[Sequence[object]]
) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".partial", dir=path.parent
    )
    try:
        with os.fdopen(
            descriptor, "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.writer(handle)
            writer.writerow(header)
            writer.writerows(rows)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise
    return sha256_file(path)


def _read_csv_by_key(path: Path, key: str) -> tuple[list[str], dict[str, dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or key not in reader.fieldnames:
            raise ValueError(f"{path} has no {key!r} column")
        rows: dict[str, dict[str, str]] = {}
        order: list[str] = []
        for row in reader:
            identifier = row[key]
            if not identifier:
                raise ValueError(f"{path} contains an empty {key}")
            if identifier in rows:
                raise ValueError(f"{path} repeats {identifier}")
            rows[identifier] = dict(row)
            order.append(identifier)
    return order, rows


def _is_connected(graph: BitGraph) -> bool:
    if graph.n == 0:
        return False
    reached = 1
    frontier = 1
    while frontier:
        bit = frontier & -frontier
        frontier ^= bit
        vertex = bit.bit_length() - 1
        new = graph.adj[vertex] & ~reached
        reached |= new
        frontier |= new
    return reached == graph.full


def load_certified_hosts(
    catalog_path: Path,
    parameters_path: Path,
    *,
    require_known_hashes: bool = True,
    expected_selected: int = 55,
) -> tuple[Host, ...]:
    """Join the certified files and select the exact MMV near-miss universe."""

    if require_known_hashes:
        catalog_hash = sha256_file(catalog_path)
        parameter_hash = sha256_file(parameters_path)
        if catalog_hash != EXPECTED_CATALOG_SHA256:
            raise ValueError(
                "MMV catalog hash mismatch: "
                f"{catalog_hash} != {EXPECTED_CATALOG_SHA256}"
            )
        if parameter_hash != EXPECTED_PARAMETERS_SHA256:
            raise ValueError(
                "MMV parameter hash mismatch: "
                f"{parameter_hash} != {EXPECTED_PARAMETERS_SHA256}"
            )

    catalog_order, catalog = _read_csv_by_key(catalog_path, "catalog_id")
    parameter_order, parameters = _read_csv_by_key(
        parameters_path, "catalog_id"
    )
    if set(catalog) != set(parameters):
        raise ValueError("catalog and parameter identifiers differ")
    if catalog_order != parameter_order:
        raise ValueError("catalog and parameter row orders differ")
    if require_known_hashes and len(catalog_order) != 56:
        raise ValueError("the certified MMV catalog must contain 56 records")

    selected: list[Host] = []
    seen_graphs: set[str] = set()
    for identifier in catalog_order:
        catalog_row = catalog[identifier]
        parameter_row = parameters[identifier]
        if catalog_row["graph6"] != parameter_row["graph6"]:
            raise ValueError(f"graph6 mismatch for {identifier}")
        if int(catalog_row["n"]) != int(parameter_row["n"]):
            raise ValueError(f"order mismatch for {identifier}")
        graph6 = catalog_row["graph6"]
        if graph6 in seen_graphs:
            raise ValueError(f"duplicate catalog graph {graph6}")
        seen_graphs.add(graph6)

        independence = int(parameter_row["alpha"])
        gamma_infinity = int(
            parameter_row["gamma_infinity_one_guard"]
        )
        cover = int(parameter_row["theta"])
        if not (
            independence == TARGET_GUARD_COUNT
            and gamma_infinity == TARGET_GUARD_COUNT
            and gamma_infinity < cover
        ):
            continue
        graph = BitGraph.from_graph6(graph6)
        if graph.n != int(catalog_row["n"]) or not _is_connected(graph):
            raise ValueError(f"invalid connected host record {identifier}")
        selected.append(
            Host(
                index=len(selected),
                catalog_id=identifier,
                order=graph.n,
                graph6=graph6,
                gamma=int(parameter_row["gamma"]),
                alpha=independence,
                gamma_infinity=gamma_infinity,
                theta=cover,
            )
        )

    if len(selected) != expected_selected:
        raise ValueError(
            f"selected {len(selected)} hosts, expected {expected_selected}"
        )
    if require_known_hashes:
        distribution = Counter(
            (host.order, host.gamma, host.alpha, host.gamma_infinity, host.theta)
            for host in selected
        )
        expected_distribution = Counter(
            {
                (10, 2, 3, 3, 4): 2,
                (11, 2, 3, 3, 4): 51,
                (11, 1, 3, 3, 4): 2,
            }
        )
        if distribution != expected_distribution:
            raise ValueError(
                f"unexpected selected-host distribution: {distribution}"
            )
        if sum(host.raw_extension_count for host in selected) != 110_537:
            raise AssertionError("raw extension universe must have size 110537")
    return tuple(selected)


def verify_pinned_labelg(labelg_path: Path) -> str:
    """Require the locally bootstrapped nauty/Traces 2.9.3 ``labelg``."""

    resolved = labelg_path.resolve()
    if not resolved.is_file() or not os.access(resolved, os.X_OK):
        raise ValueError(f"labelg is not executable: {resolved}")
    marker = resolved.parent / "This_is_nauty2_9_3.txt"
    # The upstream version marker is intentionally an empty file; its name
    # and the extracted directory name carry the release identifier.
    if not marker.is_file() or resolved.parent.name != "nauty2_9_3":
        raise ValueError(f"labelg is not from the pinned 2.9.3 tree: {resolved}")
    archive = resolved.parent.parent / "nauty2_9_3.tar.gz"
    if not archive.is_file():
        raise ValueError(f"pinned nauty source archive is missing: {archive}")
    if sha256_file(archive) != NAUTY_ARCHIVE_SHA256:
        raise ValueError("local nauty archive hash does not match the pin")
    executable_hash = sha256_file(resolved)
    if executable_hash != EXPECTED_LABELG_SHA256:
        raise ValueError(
            "labelg executable hash does not match the audited local build: "
            f"{executable_hash} != {EXPECTED_LABELG_SHA256}"
        )
    return executable_hash


def _positive_finite_gate(value: object, name: str) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value <= 0
    ):
        raise ValueError(f"{name} must be a positive finite number")
    return float(value)


def validate_path_roles(
    *,
    catalog_path: Path,
    parameters_path: Path,
    labelg_path: Path,
    database_path: Path,
    checkpoint_path: Path,
    candidate_directory: Path,
    provenance_output: Path,
    unique_output: Path,
) -> None:
    """Reject resolved aliases that could overwrite trusted or distinct data."""

    campaign_root = Path(__file__).resolve().parents[2]
    trusted = {
        "catalog": catalog_path.resolve(),
        "parameters": parameters_path.resolve(),
        "labelg": labelg_path.resolve(),
        **{
            f"runtime source {relative}": (campaign_root / relative).resolve()
            for relative in RUNTIME_SOURCE_RELATIVE_PATHS
        },
    }
    writable_files = {
        "database": database_path.resolve(),
        "checkpoint": checkpoint_path.resolve(),
        "provenance": provenance_output.resolve(),
        "unique": unique_output.resolve(),
    }
    by_path: dict[Path, list[str]] = {}
    for role, path in writable_files.items():
        by_path.setdefault(path, []).append(role)
    collisions = {
        path: roles for path, roles in by_path.items() if len(roles) > 1
    }
    if collisions:
        description = "; ".join(
            f"{path}: {','.join(sorted(roles))}"
            for path, roles in sorted(
                collisions.items(), key=lambda item: str(item[0])
            )
        )
        raise ValueError(f"writable path roles alias: {description}")
    writable_items = tuple(writable_files.items())
    for index, (first_role, first_path) in enumerate(writable_items):
        for second_role, second_path in writable_items[index + 1 :]:
            if first_path in second_path.parents or second_path in first_path.parents:
                raise ValueError(
                    f"writable path roles overlap: {first_role}={first_path}, "
                    f"{second_role}={second_path}"
                )

    for writable_role, writable_path in writable_files.items():
        for trusted_role, trusted_path in trusted.items():
            if writable_path == trusted_path:
                raise ValueError(
                    f"{writable_role} aliases trusted {trusted_role}: "
                    f"{writable_path}"
                )

    candidate_path = candidate_directory.resolve()
    for trusted_role, trusted_path in trusted.items():
        if candidate_path == trusted_path:
            raise ValueError(
                f"candidate directory aliases trusted {trusted_role}: "
                f"{candidate_path}"
            )
    for writable_role, writable_path in writable_files.items():
        if candidate_path == writable_path:
            raise ValueError(
                f"candidate directory aliases {writable_role}: {candidate_path}"
            )
        try:
            writable_path.relative_to(candidate_path)
        except ValueError:
            pass
        else:
            raise ValueError(
                f"{writable_role} is inside the candidate directory: "
                f"{writable_path}"
            )
        if writable_path in candidate_path.parents:
            raise ValueError(
                f"candidate directory is inside {writable_role}: "
                f"{candidate_path}"
            )


def build_configuration(
    *,
    catalog_path: Path,
    parameters_path: Path,
    labelg_path: Path,
    batch_size: int,
    active_host_ids: Sequence[str] = (),
    wall_limit_seconds: float = 2700.0,
    memory_limit_mib: float = 1024.0,
) -> SearchConfiguration:
    if type(batch_size) is not int or batch_size < 1:
        raise ValueError("batch size must be positive")
    _positive_finite_gate(wall_limit_seconds, "wall limit")
    _positive_finite_gate(memory_limit_mib, "memory limit")
    verify_pinned_labelg(labelg_path)
    hosts = load_certified_hosts(catalog_path, parameters_path)
    valid_ids = {host.catalog_id for host in hosts}
    active = tuple(active_host_ids)
    if len(set(active)) != len(active):
        raise ValueError("active host identifiers must be unique")
    unknown = set(active) - valid_ids
    if unknown:
        raise ValueError(f"unknown active hosts: {sorted(unknown)}")
    source_manifest = runtime_source_manifest()
    source_hashes = dict(source_manifest)
    return SearchConfiguration(
        catalog_path=str(catalog_path.resolve()),
        catalog_sha256=sha256_file(catalog_path),
        parameters_path=str(parameters_path.resolve()),
        parameters_sha256=sha256_file(parameters_path),
        labelg_path=str(labelg_path.resolve()),
        labelg_sha256=sha256_file(labelg_path),
        nauty_archive_sha256=NAUTY_ARCHIVE_SHA256,
        engine_sha256=source_hashes["src/search/extension_killtest.py"],
        runtime_source_manifest=source_manifest,
        runtime_source_set_sha256=_runtime_source_set_sha256(source_manifest),
        python_implementation=platform.python_implementation(),
        python_version=platform.python_version(),
        python_executable=str(Path(sys.executable).resolve()),
        batch_size=batch_size,
        active_host_ids=active,
        wall_limit_seconds=wall_limit_seconds,
        memory_limit_mib=memory_limit_mib,
    )


def extend_by_neighborhood(host: BitGraph, neighborhood_mask: int) -> BitGraph:
    """Add vertex ``host.n`` adjacent to exactly ``neighborhood_mask``."""

    if (
        type(neighborhood_mask) is not int
        or neighborhood_mask <= 0
        or neighborhood_mask & ~host.full
    ):
        raise ValueError("extension neighborhood must be a nonempty host subset")
    new_bit = 1 << host.n
    adjacency = list(host.adj)
    for vertex in range(host.n):
        if neighborhood_mask >> vertex & 1:
            adjacency[vertex] |= new_bit
    adjacency.append(neighborhood_mask)
    return BitGraph(host.n + 1, tuple(adjacency))


def canonicalize_graph6_batch(
    records: Sequence[str], labelg_path: Path
) -> tuple[str, ...]:
    """Canonicalize in input order with one single-threaded ``labelg`` call."""

    if not records:
        return ()
    command = [str(labelg_path.resolve()), "-q", "-g"]
    completed = subprocess.run(
        command,
        input="".join(record + "\n" for record in records),
        text=True,
        encoding="ascii",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"labelg exited {completed.returncode}: {completed.stderr.strip()}"
        )
    canonical = tuple(
        line.strip() for line in completed.stdout.splitlines() if line.strip()
    )
    if len(canonical) != len(records):
        raise RuntimeError(
            f"labelg returned {len(canonical)} graphs for {len(records)} inputs"
        )
    for original, labeled in zip(records, canonical, strict=True):
        input_graph = BitGraph.from_graph6(original)
        output_graph = BitGraph.from_graph6(labeled)
        if (
            input_graph.n != output_graph.n
            or input_graph.size != output_graph.size
        ):
            raise RuntimeError("labelg changed graph order or size")
    return canonical


def _configuration_digest_bitmasks(family: Iterable[int]) -> str:
    digest = hashlib.sha256()
    for configuration in sorted(family):
        digest.update(f"{configuration:x}\n".encode("ascii"))
    return digest.hexdigest()


def _configuration_digest_sets(
    family: Iterable[frozenset[int]],
) -> str:
    digest = hashlib.sha256()
    for configuration in sorted(family, key=lambda value: tuple(sorted(value))):
        digest.update(
            (" ".join(map(str, sorted(configuration))) + "\n").encode("ascii")
        )
    return digest.hexdigest()


def _obstruction_payload(
    obstruction: PrivateObstruction | None,
) -> str | None:
    if obstruction is None:
        return None
    return json.dumps(
        {
            "independent_set_mask": obstruction.independent_set,
            "attack": obstruction.attack,
            "failed_guards": [
                {
                    "guard": record.guard,
                    "newly_undominated": record.newly_undominated,
                }
                for record in obstruction.failed_guards
            ],
        },
        sort_keys=True,
        separators=(",", ":"),
    )


def evaluate_canonical_extension(graph6: str) -> Evaluation:
    """Apply exact target filters and both independent one-guard decisions."""

    graph_a = BitGraph.from_graph6(graph6)
    gamma_value = domination_number(graph_a)
    alpha_value = alpha(graph_a)
    if gamma_value < TARGET_GUARD_COUNT:
        return Evaluation(
            gamma_value,
            alpha_value,
            "gamma_below_3",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )
    if gamma_value > TARGET_GUARD_COUNT:
        raise AssertionError(
            "selected-host extension violates inherited gamma <= 3 bound"
        )
    if alpha_value != TARGET_GUARD_COUNT:
        if alpha_value < TARGET_GUARD_COUNT or alpha_value > 4:
            raise AssertionError(
                "selected-host extension violates 3 <= alpha <= 4"
            )
        return Evaluation(
            gamma_value,
            alpha_value,
            "alpha_above_3",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )

    obstruction = find_private_obstruction(graph_a)
    if obstruction is not None and not verify_private_obstruction(
        graph_a, obstruction
    ):
        raise AssertionError("private-obstruction producer failed its checker")

    result_a = eternal_fixed_point(graph_a, TARGET_GUARD_COUNT)
    graph_b = Graph.from_graph6(graph6)
    family_b = find_eternal_family(graph_b, TARGET_GUARD_COUNT)
    decision_a = result_a.exists
    decision_b = family_b is not None
    if decision_a != decision_b:
        raise AssertionError(
            ("independent eternal decisions disagree", graph6, decision_a, decision_b)
        )
    normalized_a = frozenset(
        frozenset(
            vertex
            for vertex in range(graph_a.n)
            if configuration >> vertex & 1
        )
        for configuration in result_a.family
    )
    normalized_b = family_b or frozenset()
    if normalized_a != normalized_b:
        raise AssertionError(
            (
                "independent greatest eternal families disagree",
                graph6,
                len(normalized_a),
                len(normalized_b),
            )
        )
    if obstruction is not None and decision_a:
        raise AssertionError("private obstruction contradicts eternal decision")
    if decision_a and not verify_eternal_result(graph_a, result_a):
        raise AssertionError("verifier A rejected its generated certificate")
    if decision_b and not verify_eternal_family(
        graph_b, TARGET_GUARD_COUNT, normalized_b
    ):
        raise AssertionError("verifier B rejected its generated family")

    if decision_a:
        category = "candidate_eternal_3"
    elif obstruction is not None:
        category = "private_obstruction_eternal_false"
    else:
        category = "eternal_false_without_private_obstruction"
    return Evaluation(
        gamma_value,
        alpha_value,
        category,
        _obstruction_payload(obstruction),
        decision_a,
        decision_b,
        len(result_a.family),
        len(normalized_b),
        _configuration_digest_bitmasks(result_a.family),
        _configuration_digest_sets(normalized_b),
        result_a,
        normalized_b,
    )


def _connect_database(
    database_path: Path,
    configuration: SearchConfiguration,
    hosts: Sequence[Host],
) -> sqlite3.Connection:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = DELETE")
    connection.execute("PRAGMA synchronous = FULL")
    version = int(connection.execute("PRAGMA user_version").fetchone()[0])
    if version not in (0, SCHEMA_VERSION):
        connection.close()
        raise ValueError(f"unsupported database schema version {version}")
    if version == 0:
        try:
            connection.executescript(
                """
            BEGIN IMMEDIATE;
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
            CREATE INDEX origins_by_canonical
                ON origins(canonical_graph6, host_id, neighborhood_mask);
            """
            )
            connection.execute(
                "INSERT INTO metadata(key, value) VALUES (?, ?)",
                (
                    "configuration_json",
                    json.dumps(asdict(configuration), sort_keys=True),
                ),
            )
            connection.execute(
                "INSERT INTO metadata(key, value) VALUES (?, ?)",
                ("configuration_sha256", configuration.digest),
            )
            connection.execute(
                "INSERT INTO metadata(key, value) VALUES (?, ?)",
                ("candidate_frozen_path", ""),
            )
            for host in hosts:
                connection.execute(
                    """
                    INSERT INTO hosts(
                        host_index, catalog_id, n, graph6, gamma, alpha,
                        gamma_infinity, theta, raw_expected, next_mask, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 'pending')
                    """,
                    (
                        host.index,
                        host.catalog_id,
                        host.order,
                        host.graph6,
                        host.gamma,
                        host.alpha,
                        host.gamma_infinity,
                        host.theta,
                        host.raw_extension_count,
                    ),
                )
            connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
            connection.commit()
        except BaseException:
            connection.rollback()
            connection.close()
            raise
    else:
        row = connection.execute(
            "SELECT value FROM metadata WHERE key = 'configuration_sha256'"
        ).fetchone()
        if row is None or row[0] != configuration.digest:
            connection.close()
            raise ValueError(
                "search configuration does not match the existing checkpoint"
            )
        stored_hosts = tuple(
            row[0]
            for row in connection.execute(
                "SELECT catalog_id FROM hosts ORDER BY host_index"
            )
        )
        if stored_hosts != tuple(host.catalog_id for host in hosts):
            connection.close()
            raise ValueError("host universe does not match the existing checkpoint")
    return connection


def _host_stream_hash(
    connection: sqlite3.Connection, host_id: str
) -> str:
    digest = hashlib.sha256()
    for (record,) in connection.execute(
        """
        SELECT canonical_graph6 FROM origins
        WHERE host_id = ?
        ORDER BY neighborhood_mask
        """,
        (host_id,),
    ):
        digest.update(record.encode("ascii") + b"\n")
    return digest.hexdigest()


def validate_or_repair_completed_host(
    connection: sqlite3.Connection,
    host_id: str,
    raw_expected: int,
) -> str:
    """Validate a completed host and repair only the legacy NULL-hash window."""

    row = connection.execute(
        """
        SELECT h.next_mask, h.status, h.canonical_stream_sha256,
               COUNT(o.neighborhood_mask)
        FROM hosts AS h
        LEFT JOIN origins AS o ON o.host_id = h.catalog_id
        WHERE h.catalog_id = ?
        GROUP BY h.catalog_id
        """,
        (host_id,),
    ).fetchone()
    if row is None or row[1] != "complete":
        raise ValueError(f"host is not marked complete: {host_id}")
    next_mask, _, stored_hash, raw_count = row
    if int(next_mask) != raw_expected + 1 or int(raw_count) != raw_expected:
        raise RuntimeError(
            f"inconsistent completed host {host_id}: next_mask={next_mask}, "
            f"raw_count={raw_count}, expected={raw_expected}"
        )
    calculated_hash = _host_stream_hash(connection, host_id)
    if stored_hash is None:
        connection.execute(
            """
            UPDATE hosts SET canonical_stream_sha256 = ?
            WHERE catalog_id = ?
            """,
            (calculated_hash, host_id),
        )
        connection.commit()
    elif stored_hash != calculated_hash:
        raise RuntimeError(
            f"completed host canonical stream hash mismatch: {host_id}"
        )
    return calculated_hash


def _resource_snapshot() -> dict[str, object]:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    raw = int(usage.ru_maxrss)
    resident_mib = raw / (1024 * 1024) if platform.system() == "Darwin" else raw / 1024
    return {
        "user_cpu_seconds": usage.ru_utime,
        "system_cpu_seconds": usage.ru_stime,
        "maximum_resident_set_size_raw": raw,
        "maximum_resident_set_size_mib": resident_mib,
        "maximum_resident_set_size_unit": (
            "bytes" if platform.system() == "Darwin" else "KiB"
        ),
    }


def inspect_candidate_state(
    connection: sqlite3.Connection,
) -> dict[str, object]:
    """Return candidate state from both redundant fail-closed indicators."""

    marker_row = connection.execute(
        "SELECT value FROM metadata WHERE key = 'candidate_frozen_path'"
    ).fetchone()
    marker_path = (
        None
        if marker_row is None or not marker_row[0]
        else str(marker_row[0])
    )
    graph_records = tuple(
        str(row[0])
        for row in connection.execute(
            """
            SELECT graph6 FROM canonical_graphs
            WHERE category = 'candidate_eternal_3'
            ORDER BY graph6
            """
        )
    )
    candidate_rows = [
        {
            "graph6": graph6,
            "graph6_sha256": hashlib.sha256(
                (graph6 + "\n").encode("ascii")
            ).hexdigest(),
        }
        for graph6 in graph_records
    ]
    origin_records = tuple(
        (str(row[0]), int(row[1]), str(row[2]))
        for row in connection.execute(
            """
            SELECT host_id, neighborhood_mask, canonical_graph6
            FROM origins
            WHERE category = 'candidate_eternal_3'
            ORDER BY host_id, neighborhood_mask
            """
        )
    )
    candidate_origin_rows = [
        {
            "host_id": host_id,
            "neighborhood_mask": neighborhood_mask,
            "canonical_graph6": canonical_graph6,
            "canonical_graph6_sha256": hashlib.sha256(
                (canonical_graph6 + "\n").encode("ascii")
            ).hexdigest(),
        }
        for host_id, neighborhood_mask, canonical_graph6 in origin_records
    ]
    inconsistencies: list[str] = []
    if marker_path is not None and not graph_records and not origin_records:
        inconsistencies.append("freeze marker exists without a candidate row")
    if (graph_records or origin_records) and marker_path is None:
        inconsistencies.append("candidate row exists without a freeze marker")
    canonical_candidate_set = set(graph_records)
    origin_candidate_set = {record[2] for record in origin_records}
    if origin_candidate_set - canonical_candidate_set:
        inconsistencies.append(
            "candidate origin row exists without a canonical candidate row"
        )
    if canonical_candidate_set - origin_candidate_set:
        inconsistencies.append(
            "canonical candidate row exists without a candidate origin row"
        )
    if marker_path is not None and not Path(marker_path).is_file():
        inconsistencies.append("freeze marker path does not name an existing file")
    pending = marker_path is not None or bool(graph_records) or bool(origin_records)
    primary_reference = marker_path
    if primary_reference is None and candidate_rows:
        primary_reference = (
            "UNRECORDED-CANDIDATE-SHA256:"
            + str(candidate_rows[0]["graph6_sha256"])
        )
    if primary_reference is None and candidate_origin_rows:
        primary_reference = (
            "UNRECORDED-CANDIDATE-SHA256:"
            + str(candidate_origin_rows[0]["canonical_graph6_sha256"])
        )
    return {
        "pending": pending,
        "marker_path": marker_path,
        "marker_file_exists": (
            marker_path is not None and Path(marker_path).is_file()
        ),
        "candidate_row_count": len(candidate_rows) + len(candidate_origin_rows),
        "canonical_candidate_row_count": len(candidate_rows),
        "candidate_origin_row_count": len(candidate_origin_rows),
        "candidate_rows": candidate_rows,
        "candidate_origin_rows": candidate_origin_rows,
        "inconsistencies": inconsistencies,
        "primary_reference": primary_reference,
    }


def summarize_database(
    connection: sqlite3.Connection,
    *,
    configuration: SearchConfiguration,
    database_path: Path,
    status: str,
    started_unix: float,
    process_started_counter: float,
    batches_processed: int,
) -> dict[str, object]:
    raw_processed = int(
        connection.execute("SELECT COUNT(*) FROM origins").fetchone()[0]
    )
    raw_expected = int(
        connection.execute("SELECT SUM(raw_expected) FROM hosts").fetchone()[0]
    )
    unique_count = int(
        connection.execute("SELECT COUNT(*) FROM canonical_graphs").fetchone()[0]
    )
    unique_categories = {
        row[0]: int(row[1])
        for row in connection.execute(
            """
            SELECT category, COUNT(*) FROM canonical_graphs
            GROUP BY category ORDER BY category
            """
        )
    }
    raw_categories = {
        row[0]: int(row[1])
        for row in connection.execute(
            """
            SELECT category, COUNT(*) FROM origins
            GROUP BY category ORDER BY category
            """
        )
    }
    parameter_deltas = {
        f"gamma_delta={row[0]},alpha_delta={row[1]}": int(row[2])
        for row in connection.execute(
            """
            SELECT gamma_delta, alpha_delta, COUNT(*) FROM origins
            GROUP BY gamma_delta, alpha_delta
            ORDER BY gamma_delta, alpha_delta
            """
        )
    }
    hosts_payload = [
        {
            "catalog_id": row[0],
            "n": int(row[1]),
            "raw_expected": int(row[2]),
            "raw_processed": int(row[3]),
            "next_mask": int(row[4]),
            "status": row[5],
            "canonical_stream_sha256": row[6],
        }
        for row in connection.execute(
            """
            SELECT h.catalog_id, h.n, h.raw_expected, COUNT(o.neighborhood_mask),
                   h.next_mask, h.status, h.canonical_stream_sha256
            FROM hosts AS h
            LEFT JOIN origins AS o ON o.host_id = h.catalog_id
            GROUP BY h.catalog_id
            ORDER BY h.host_index
            """
        )
    ]
    candidate_state = inspect_candidate_state(connection)
    payload: dict[str, object] = {
        "status": status,
        "configuration": asdict(configuration),
        "configuration_sha256": configuration.digest,
        "database": str(database_path.resolve()),
        "database_sha256": sha256_file(database_path),
        "raw_expected": raw_expected,
        "raw_processed": raw_processed,
        "unique_canonical_graphs": unique_count,
        "raw_category_counts": raw_categories,
        "unique_category_counts": unique_categories,
        "raw_parameter_delta_counts": parameter_deltas,
        "hosts": hosts_payload,
        "hosts_complete": sum(row["status"] == "complete" for row in hosts_payload),
        "batches_processed_this_process": batches_processed,
        "started_unix_this_process": started_unix,
        "updated_unix": time.time(),
        "wall_seconds_this_process": time.perf_counter()
        - process_started_counter,
        "resource_usage": _resource_snapshot(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "process_argv": list(sys.argv),
        "candidate_path": candidate_state["primary_reference"],
        "candidate_state": candidate_state,
    }
    return payload


def _write_host_checkpoint(
    checkpoint_path: Path,
    connection: sqlite3.Connection,
    host: Host,
    configuration: SearchConfiguration,
) -> Path:
    category_counts = {
        row[0]: int(row[1])
        for row in connection.execute(
            """
            SELECT category, COUNT(*) FROM origins
            WHERE host_id = ?
            GROUP BY category ORDER BY category
            """,
            (host.catalog_id,),
        )
    }
    unique_count = int(
        connection.execute(
            """
            SELECT COUNT(DISTINCT canonical_graph6) FROM origins
            WHERE host_id = ?
            """,
            (host.catalog_id,),
        ).fetchone()[0]
    )
    stream_hash = _host_stream_hash(connection, host.catalog_id)
    path = (
        checkpoint_path.parent
        / f"{checkpoint_path.stem}.hosts"
        / f"{host.catalog_id}.json"
    )
    _atomic_json(
        path,
        {
            "status": "complete",
            "configuration_sha256": configuration.digest,
            "host": asdict(host),
            "raw_processed": host.raw_extension_count,
            "unique_within_host": unique_count,
            "raw_category_counts": category_counts,
            "canonical_stream_sha256": stream_hash,
            "updated_unix": time.time(),
        },
    )
    return path


def _eternal_a_payload(result: EternalResult) -> dict[str, object]:
    return {
        "k": result.k,
        "family_masks": list(sorted(result.family)),
        "responses": [
            {
                "source_mask": source,
                "attack": attack,
                "guard": guard,
                "successor_mask": successor,
            }
            for (source, attack), (guard, successor) in sorted(
                result.responses.items()
            )
        ],
        "rounds": result.rounds,
    }


def freeze_candidate(
    candidate_directory: Path,
    *,
    host: Host,
    neighborhood_mask: int,
    raw_graph6: str,
    canonical_graph6: str,
    evaluation: Evaluation,
    configuration: SearchConfiguration,
) -> Path:
    """Atomically preserve a first-search witness before any later analysis."""

    if (
        evaluation.category != "candidate_eternal_3"
        or evaluation.eternal_result_a is None
        or evaluation.eternal_family_b is None
    ):
        raise ValueError("only an independently agreed candidate can be frozen")
    graph = BitGraph.from_graph6(canonical_graph6)
    graph_digest = hashlib.sha256(
        (canonical_graph6 + "\n").encode("ascii")
    ).hexdigest()
    payload: dict[str, object] = {
        "status": "FROZEN-UNREVIEWED-CANDIDATE",
        "warning": (
            "This search artifact is not a conjecture-resolution claim until "
            "the independent counterexample certificate protocol is complete."
        ),
        "configuration_sha256": configuration.digest,
        "host": asdict(host),
        "neighborhood_mask": neighborhood_mask,
        "neighborhood_vertices": [
            vertex
            for vertex in range(host.order)
            if neighborhood_mask >> vertex & 1
        ],
        "raw_extension_graph6": raw_graph6,
        "canonical_graph6": canonical_graph6,
        "canonical_graph6_sha256": graph_digest,
        "n": graph.n,
        "m": graph.size,
        "edges": [
            [first, second]
            for first in range(graph.n)
            for second in range(first + 1, graph.n)
            if graph.adj[first] >> second & 1
        ],
        "gamma": evaluation.gamma,
        "alpha": evaluation.alpha,
        "theta_lower_bound": host.theta,
        "theta_lower_bound_reason": (
            "the raw extension contains the selected host as an induced "
            "subgraph; theta is induced-subgraph monotone"
        ),
        "eternal_a": _eternal_a_payload(evaluation.eternal_result_a),
        "eternal_b_family": [
            list(sorted(configuration))
            for configuration in sorted(
                evaluation.eternal_family_b,
                key=lambda value: tuple(sorted(value)),
            )
        ],
        "family_a_sha256": evaluation.family_a_sha256,
        "family_b_sha256": evaluation.family_b_sha256,
        "frozen_unix": time.time(),
    }
    candidate_directory.mkdir(parents=True, exist_ok=True)
    path = candidate_directory / f"candidate-{graph_digest[:20]}.json"
    if path.exists():
        with path.open(encoding="utf-8") as handle:
            existing = json.load(handle)
        if existing.get("canonical_graph6_sha256") != graph_digest:
            raise RuntimeError(f"candidate freeze collision at {path}")
        return path
    _atomic_json(path, payload)
    return path


def _insert_origin_and_graph(
    connection: sqlite3.Connection,
    *,
    host: Host,
    neighborhood_mask: int,
    raw_graph6: str,
    canonical_graph6: str,
    evaluation: Evaluation | None,
) -> Evaluation:
    existing_origin = connection.execute(
        """
        SELECT canonical_graph6 FROM origins
        WHERE host_id = ? AND neighborhood_mask = ?
        """,
        (host.catalog_id, neighborhood_mask),
    ).fetchone()
    if existing_origin is not None:
        if existing_origin[0] != canonical_graph6:
            raise RuntimeError("replayed origin has a different canonical label")
        row = connection.execute(
            """
            SELECT gamma, alpha, category, private_obstruction_json,
                   eternal_a, eternal_b, family_a_size, family_b_size,
                   family_a_sha256, family_b_sha256
            FROM canonical_graphs WHERE graph6 = ?
            """,
            (canonical_graph6,),
        ).fetchone()
        assert row is not None
        return _evaluation_from_row(row)

    graph_row = connection.execute(
        """
        SELECT gamma, alpha, category, private_obstruction_json,
               eternal_a, eternal_b, family_a_size, family_b_size,
               family_a_sha256, family_b_sha256
        FROM canonical_graphs WHERE graph6 = ?
        """,
        (canonical_graph6,),
    ).fetchone()
    if graph_row is None:
        if evaluation is None:
            evaluation = evaluate_canonical_extension(canonical_graph6)
        canonical_graph = BitGraph.from_graph6(canonical_graph6)
        connection.execute(
            """
            INSERT INTO canonical_graphs(
                graph6, n, m, first_host_id, first_neighborhood_mask,
                first_raw_graph6, origin_count, gamma, alpha, category,
                private_obstruction_json, eternal_a, eternal_b,
                family_a_size, family_b_size, family_a_sha256, family_b_sha256
            ) VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                canonical_graph6,
                canonical_graph.n,
                canonical_graph.size,
                host.catalog_id,
                neighborhood_mask,
                raw_graph6,
                evaluation.gamma,
                evaluation.alpha,
                evaluation.category,
                evaluation.private_obstruction_json,
                _optional_bool_as_int(evaluation.eternal_a),
                _optional_bool_as_int(evaluation.eternal_b),
                evaluation.family_a_size,
                evaluation.family_b_size,
                evaluation.family_a_sha256,
                evaluation.family_b_sha256,
            ),
        )
    else:
        evaluation = _evaluation_from_row(graph_row)

    connection.execute(
        """
        INSERT INTO origins(
            host_id, neighborhood_mask, neighborhood_size, raw_graph6,
            canonical_graph6, gamma_delta, alpha_delta, category
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            host.catalog_id,
            neighborhood_mask,
            neighborhood_mask.bit_count(),
            raw_graph6,
            canonical_graph6,
            evaluation.gamma - host.gamma,
            evaluation.alpha - host.alpha,
            evaluation.category,
        ),
    )
    connection.execute(
        """
        UPDATE canonical_graphs SET origin_count = origin_count + 1
        WHERE graph6 = ?
        """,
        (canonical_graph6,),
    )
    return evaluation


def _optional_bool_as_int(value: bool | None) -> int | None:
    return None if value is None else int(value)


def _optional_int_as_bool(value: int | None) -> bool | None:
    return None if value is None else bool(value)


def _evaluation_from_row(row: Sequence[object]) -> Evaluation:
    return Evaluation(
        gamma=int(row[0]),
        alpha=int(row[1]),
        category=str(row[2]),
        private_obstruction_json=(
            None if row[3] is None else str(row[3])
        ),
        eternal_a=_optional_int_as_bool(
            None if row[4] is None else int(row[4])
        ),
        eternal_b=_optional_int_as_bool(
            None if row[5] is None else int(row[5])
        ),
        family_a_size=None if row[6] is None else int(row[6]),
        family_b_size=None if row[7] is None else int(row[7]),
        family_a_sha256=None if row[8] is None else str(row[8]),
        family_b_sha256=None if row[9] is None else str(row[9]),
    )


def _active_hosts(
    hosts: Sequence[Host], active_host_ids: Sequence[str]
) -> tuple[Host, ...]:
    if not active_host_ids:
        return tuple(hosts)
    by_id = {host.catalog_id: host for host in hosts}
    return tuple(by_id[identifier] for identifier in active_host_ids)


def _update_readable_checkpoint(
    checkpoint_path: Path,
    connection: sqlite3.Connection,
    *,
    configuration: SearchConfiguration,
    database_path: Path,
    status: str,
    started_unix: float,
    process_started_counter: float,
    batches_processed: int,
) -> dict[str, object]:
    connection.commit()
    payload = summarize_database(
        connection,
        configuration=configuration,
        database_path=database_path,
        status=status,
        started_unix=started_unix,
        process_started_counter=process_started_counter,
        batches_processed=batches_processed,
    )
    _atomic_json(checkpoint_path, payload)
    return payload


def audit_complete_coverage(
    connection: sqlite3.Connection,
    hosts: Sequence[Host],
) -> dict[str, object]:
    """Check ledger coverage and multiplicities without trusting summaries."""

    errors: list[str] = []
    total_expected = 0
    total_origins = 0
    host_hashes: dict[str, str] = {}
    for host in hosts:
        total_expected += host.raw_extension_count
        row = connection.execute(
            """
            SELECT h.next_mask, h.status, h.canonical_stream_sha256,
                   COUNT(o.neighborhood_mask), MIN(o.neighborhood_mask),
                   MAX(o.neighborhood_mask)
            FROM hosts AS h
            LEFT JOIN origins AS o ON o.host_id = h.catalog_id
            WHERE h.catalog_id = ?
            GROUP BY h.catalog_id
            """,
            (host.catalog_id,),
        ).fetchone()
        if row is None:
            errors.append(f"missing host {host.catalog_id}")
            continue
        next_mask, status, stored_hash, count, minimum, maximum = row
        count = int(count)
        total_origins += count
        if (
            count != host.raw_extension_count
            or int(next_mask) != host.raw_extension_count + 1
            or status != "complete"
            or minimum != 1
            or maximum != host.raw_extension_count
        ):
            errors.append(
                f"incomplete mask interval for {host.catalog_id}: "
                f"count={count}, next={next_mask}, status={status}, "
                f"range={minimum}..{maximum}"
            )
        calculated_hash = _host_stream_hash(connection, host.catalog_id)
        host_hashes[host.catalog_id] = calculated_hash
        if stored_hash != calculated_hash:
            errors.append(f"canonical stream hash mismatch for {host.catalog_id}")

    stored_multiplicity = int(
        connection.execute(
            "SELECT COALESCE(SUM(origin_count), 0) FROM canonical_graphs"
        ).fetchone()[0]
    )
    actual_multiplicity = int(
        connection.execute("SELECT COUNT(*) FROM origins").fetchone()[0]
    )
    if stored_multiplicity != actual_multiplicity:
        errors.append(
            "global origin multiplicity mismatch: "
            f"{stored_multiplicity} != {actual_multiplicity}"
        )
    bad_multiplicities = int(
        connection.execute(
            """
            SELECT COUNT(*) FROM (
                SELECT g.graph6
                FROM canonical_graphs AS g
                LEFT JOIN origins AS o ON o.canonical_graph6 = g.graph6
                GROUP BY g.graph6
                HAVING g.origin_count != COUNT(o.canonical_graph6)
            )
            """
        ).fetchone()[0]
    )
    if bad_multiplicities:
        errors.append(
            f"{bad_multiplicities} canonical multiplicities are inconsistent"
        )
    if total_expected != 110_537:
        errors.append(f"host universe expects {total_expected}, not 110537")
    if total_origins != total_expected:
        errors.append(
            f"ledger has {total_origins} origins, expected {total_expected}"
        )
    candidate_state = inspect_candidate_state(connection)
    if candidate_state["pending"]:
        errors.append(
            "candidate state is pending review; completion is forbidden"
        )
    return {
        "passed": not errors,
        "errors": errors,
        "raw_expected": total_expected,
        "raw_origins": total_origins,
        "stored_origin_multiplicity": stored_multiplicity,
        "bad_canonical_multiplicity_count": bad_multiplicities,
        "host_canonical_stream_sha256": host_hashes,
        "candidate_state": candidate_state,
    }


def run_extension_search(
    *,
    catalog_path: Path,
    parameters_path: Path,
    labelg_path: Path,
    database_path: Path,
    checkpoint_path: Path,
    candidate_directory: Path,
    provenance_output: Path,
    unique_output: Path,
    batch_size: int = 256,
    active_host_ids: Sequence[str] = (),
    max_batches: int | None = None,
    wall_limit_seconds: float = 2700.0,
    memory_limit_mib: float = 1024.0,
) -> RunOutcome:
    """Run or resume a complete search (or an explicitly delimited test shard)."""

    if (
        max_batches is not None
        and (type(max_batches) is not int or max_batches < 1)
    ):
        raise ValueError("max_batches must be positive when supplied")
    _positive_finite_gate(wall_limit_seconds, "wall limit")
    _positive_finite_gate(memory_limit_mib, "memory limit")
    validate_path_roles(
        catalog_path=catalog_path,
        parameters_path=parameters_path,
        labelg_path=labelg_path,
        database_path=database_path,
        checkpoint_path=checkpoint_path,
        candidate_directory=candidate_directory,
        provenance_output=provenance_output,
        unique_output=unique_output,
    )
    hosts = load_certified_hosts(catalog_path, parameters_path)
    configuration = build_configuration(
        catalog_path=catalog_path,
        parameters_path=parameters_path,
        labelg_path=labelg_path,
        batch_size=batch_size,
        active_host_ids=active_host_ids,
        wall_limit_seconds=wall_limit_seconds,
        memory_limit_mib=memory_limit_mib,
    )
    active_hosts = _active_hosts(hosts, configuration.active_host_ids)
    started_unix = time.time()
    process_started_counter = time.perf_counter()
    batches_processed = 0
    connection = _connect_database(database_path, configuration, hosts)
    try:
        candidate_state = inspect_candidate_state(connection)
        if candidate_state["pending"]:
            candidate_reference = str(candidate_state["primary_reference"])
            summary = _update_readable_checkpoint(
                checkpoint_path,
                connection,
                configuration=configuration,
                database_path=database_path,
                status="candidate_review_pending",
                started_unix=started_unix,
                process_started_counter=process_started_counter,
                batches_processed=0,
            )
            return RunOutcome(
                "candidate_review_pending",
                0,
                candidate_reference,
                summary,
            )

        stop_after_current_host = False
        for host in active_hosts:
            progress = connection.execute(
                """
                SELECT next_mask, status, canonical_stream_sha256
                FROM hosts WHERE catalog_id = ?
                """,
                (host.catalog_id,),
            ).fetchone()
            assert progress is not None
            next_mask = int(progress[0])
            if progress[1] == "complete":
                validate_or_repair_completed_host(
                    connection, host.catalog_id, host.raw_extension_count
                )
                _write_host_checkpoint(
                    checkpoint_path, connection, host, configuration
                )
                continue
            connection.execute(
                "UPDATE hosts SET status = 'running' WHERE catalog_id = ?",
                (host.catalog_id,),
            )
            connection.commit()

            while next_mask <= host.raw_extension_count:
                final_mask = min(
                    host.raw_extension_count, next_mask + batch_size - 1
                )
                masks = tuple(range(next_mask, final_mask + 1))
                host_graph = BitGraph.from_graph6(host.graph6)
                raw_graphs = tuple(
                    extend_by_neighborhood(host_graph, mask).to_graph6()
                    for mask in masks
                )
                canonical_graphs = canonicalize_graph6_batch(
                    raw_graphs, labelg_path
                )

                candidate_path: Path | None = None
                processed_through = next_mask - 1
                connection.execute("BEGIN IMMEDIATE")
                try:
                    for mask, raw_graph6, canonical_graph6 in zip(
                        masks, raw_graphs, canonical_graphs, strict=True
                    ):
                        existing = connection.execute(
                            """
                            SELECT 1 FROM origins
                            WHERE host_id = ? AND neighborhood_mask = ?
                            """,
                            (host.catalog_id, mask),
                        ).fetchone()
                        evaluation: Evaluation | None = None
                        if existing is None:
                            graph_exists = connection.execute(
                                """
                                SELECT 1 FROM canonical_graphs WHERE graph6 = ?
                                """,
                                (canonical_graph6,),
                            ).fetchone()
                            if graph_exists is None:
                                evaluation = evaluate_canonical_extension(
                                    canonical_graph6
                                )
                                if evaluation.category == "candidate_eternal_3":
                                    candidate_path = freeze_candidate(
                                        candidate_directory,
                                        host=host,
                                        neighborhood_mask=mask,
                                        raw_graph6=raw_graph6,
                                        canonical_graph6=canonical_graph6,
                                        evaluation=evaluation,
                                        configuration=configuration,
                                    )
                        stored_evaluation = _insert_origin_and_graph(
                            connection,
                            host=host,
                            neighborhood_mask=mask,
                            raw_graph6=raw_graph6,
                            canonical_graph6=canonical_graph6,
                            evaluation=evaluation,
                        )
                        processed_through = mask
                        if (
                            stored_evaluation.category == "candidate_eternal_3"
                            and candidate_path is None
                        ):
                            # A duplicate of a previously frozen candidate.
                            row = connection.execute(
                                """
                                SELECT value FROM metadata
                                WHERE key = 'candidate_frozen_path'
                                """
                            ).fetchone()
                            if row is not None and row[0]:
                                candidate_path = Path(row[0])
                        if candidate_path is not None:
                            break

                    next_mask = processed_through + 1
                    host_complete = next_mask > host.raw_extension_count
                    stream_hash = (
                        _host_stream_hash(connection, host.catalog_id)
                        if host_complete
                        else None
                    )
                    connection.execute(
                        """
                        UPDATE hosts
                        SET next_mask = ?, status = ?,
                            canonical_stream_sha256 = ?
                        WHERE catalog_id = ?
                        """,
                        (
                            next_mask,
                            "complete" if host_complete else "running",
                            stream_hash,
                            host.catalog_id,
                        ),
                    )
                    if candidate_path is not None:
                        connection.execute(
                            """
                            UPDATE metadata SET value = ?
                            WHERE key = 'candidate_frozen_path'
                            """,
                            (str(candidate_path.resolve()),),
                        )
                    connection.commit()
                except BaseException:
                    connection.rollback()
                    raise

                if next_mask > host.raw_extension_count:
                    validate_or_repair_completed_host(
                        connection, host.catalog_id, host.raw_extension_count
                    )
                    _write_host_checkpoint(
                        checkpoint_path, connection, host, configuration
                    )

                batches_processed += 1
                if candidate_path is not None:
                    summary = _update_readable_checkpoint(
                        checkpoint_path,
                        connection,
                        configuration=configuration,
                        database_path=database_path,
                        status="candidate_review_pending",
                        started_unix=started_unix,
                        process_started_counter=process_started_counter,
                        batches_processed=batches_processed,
                    )
                    return RunOutcome(
                        "candidate_review_pending",
                        batches_processed,
                        str(candidate_path.resolve()),
                        summary,
                    )

                status = "running"
                if max_batches is not None and batches_processed >= max_batches:
                    status = "bounded_sample_complete"
                summary = _update_readable_checkpoint(
                    checkpoint_path,
                    connection,
                    configuration=configuration,
                    database_path=database_path,
                    status=status,
                    started_unix=started_unix,
                    process_started_counter=process_started_counter,
                    batches_processed=batches_processed,
                )
                if status == "bounded_sample_complete":
                    return RunOutcome(status, batches_processed, None, summary)

                usage_mib = float(
                    summary["resource_usage"]["maximum_resident_set_size_mib"]  # type: ignore[index]
                )
                if usage_mib > memory_limit_mib:
                    summary = _update_readable_checkpoint(
                        checkpoint_path,
                        connection,
                        configuration=configuration,
                        database_path=database_path,
                        status="memory_gate_at_batch_checkpoint",
                        started_unix=started_unix,
                        process_started_counter=process_started_counter,
                        batches_processed=batches_processed,
                    )
                    return RunOutcome(
                        "memory_gate_at_batch_checkpoint",
                        batches_processed,
                        None,
                        summary,
                    )
                if (
                    time.perf_counter() - process_started_counter
                    > wall_limit_seconds
                ):
                    stop_after_current_host = True

            validate_or_repair_completed_host(
                connection, host.catalog_id, host.raw_extension_count
            )
            _write_host_checkpoint(
                checkpoint_path, connection, host, configuration
            )
            if stop_after_current_host:
                summary = _update_readable_checkpoint(
                    checkpoint_path,
                    connection,
                    configuration=configuration,
                    database_path=database_path,
                    status="wall_gate_at_host_checkpoint",
                    started_unix=started_unix,
                    process_started_counter=process_started_counter,
                    batches_processed=batches_processed,
                )
                return RunOutcome(
                    "wall_gate_at_host_checkpoint",
                    batches_processed,
                    None,
                    summary,
                )

        all_active_complete = all(
            connection.execute(
                "SELECT status FROM hosts WHERE catalog_id = ?",
                (host.catalog_id,),
            ).fetchone()[0]
            == "complete"
            for host in active_hosts
        )
        candidate_state = inspect_candidate_state(connection)
        if candidate_state["pending"]:
            candidate_reference = str(candidate_state["primary_reference"])
            summary = _update_readable_checkpoint(
                checkpoint_path,
                connection,
                configuration=configuration,
                database_path=database_path,
                status="candidate_review_pending",
                started_unix=started_unix,
                process_started_counter=process_started_counter,
                batches_processed=batches_processed,
            )
            return RunOutcome(
                "candidate_review_pending",
                batches_processed,
                candidate_reference,
                summary,
            )
        full_universe = not configuration.active_host_ids
        status = (
            "complete"
            if all_active_complete and full_universe
            else "selected_hosts_complete"
        )
        output_hashes: dict[str, str] = {}
        if status == "complete":
            coverage_audit = audit_complete_coverage(connection, hosts)
            if not coverage_audit["passed"]:
                raise AssertionError(
                    ("complete-coverage audit failed", coverage_audit["errors"])
                )
            output_hashes = export_results(
                connection,
                provenance_output=provenance_output,
                unique_output=unique_output,
            )
        summary = _update_readable_checkpoint(
            checkpoint_path,
            connection,
            configuration=configuration,
            database_path=database_path,
            status=status,
            started_unix=started_unix,
            process_started_counter=process_started_counter,
            batches_processed=batches_processed,
        )
        if output_hashes:
            summary["coverage_audit"] = coverage_audit
            summary["output_sha256"] = output_hashes
            _atomic_json(checkpoint_path, summary)
        return RunOutcome(status, batches_processed, None, summary)
    except BaseException:
        try:
            _update_readable_checkpoint(
                checkpoint_path,
                connection,
                configuration=configuration,
                database_path=database_path,
                status="failed_at_last_committed_batch",
                started_unix=started_unix,
                process_started_counter=process_started_counter,
                batches_processed=batches_processed,
            )
        finally:
            connection.close()
        raise
    finally:
        try:
            connection.close()
        except sqlite3.ProgrammingError:
            pass


def export_results(
    connection: sqlite3.Connection,
    *,
    provenance_output: Path,
    unique_output: Path,
) -> dict[str, str]:
    provenance_header = (
        "host_id",
        "neighborhood_mask",
        "neighborhood_size",
        "raw_graph6",
        "canonical_graph6",
        "gamma_delta",
        "alpha_delta",
        "category",
    )
    provenance_rows = connection.execute(
        """
        SELECT o.host_id, o.neighborhood_mask, o.neighborhood_size,
               o.raw_graph6, o.canonical_graph6, o.gamma_delta,
               o.alpha_delta, o.category
        FROM origins AS o
        JOIN hosts AS h ON h.catalog_id = o.host_id
        ORDER BY h.host_index, o.neighborhood_mask
        """
    )
    provenance_hash = _atomic_csv(
        provenance_output, provenance_header, provenance_rows
    )
    unique_header = (
        "canonical_graph6",
        "n",
        "m",
        "origin_count",
        "first_host_id",
        "first_neighborhood_mask",
        "first_raw_graph6",
        "gamma",
        "alpha",
        "category",
        "private_obstruction_json",
        "eternal_a",
        "eternal_b",
        "family_a_size",
        "family_b_size",
        "family_a_sha256",
        "family_b_sha256",
    )
    unique_rows = connection.execute(
        """
        SELECT graph6, n, m, origin_count, first_host_id,
               first_neighborhood_mask, first_raw_graph6, gamma, alpha,
               category, private_obstruction_json, eternal_a, eternal_b,
               family_a_size, family_b_size, family_a_sha256, family_b_sha256
        FROM canonical_graphs ORDER BY n, graph6
        """
    )
    unique_hash = _atomic_csv(unique_output, unique_header, unique_rows)
    return {
        str(provenance_output.resolve()): provenance_hash,
        str(unique_output.resolve()): unique_hash,
    }


def _default_campaign_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> None:
    campaign = _default_campaign_root()
    parser = argparse.ArgumentParser(
        description=(
            "Complete one-vertex-extension kill test around the 55 certified "
            "MMV near-miss hosts."
        )
    )
    parser.add_argument(
        "--validation-gate-open",
        action="store_true",
        help="required acknowledgment that the first-72-hour validation gate opened",
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=campaign / "instances" / "mmv2022_table9.csv",
    )
    parser.add_argument(
        "--parameters",
        type=Path,
        default=campaign / "results" / "mmv2022_parameters.csv",
    )
    parser.add_argument(
        "--labelg",
        type=Path,
        default=campaign / "tools" / "nauty2_9_3" / "labelg",
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=campaign / "results" / "checkpoints" / "extensions.sqlite3",
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=campaign / "results" / "checkpoints" / "extensions.json",
    )
    parser.add_argument(
        "--candidate-dir",
        type=Path,
        default=campaign / "certificates" / "frozen_candidates",
    )
    parser.add_argument(
        "--provenance-output",
        type=Path,
        default=campaign / "results" / "extensions_provenance.csv",
    )
    parser.add_argument(
        "--unique-output",
        type=Path,
        default=campaign / "results" / "extensions_unique.csv",
    )
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument(
        "--host-id",
        action="append",
        default=[],
        help=(
            "development shard only; repeat to select hosts. Omit for the "
            "complete 55-host universe."
        ),
    )
    parser.add_argument(
        "--max-batches",
        type=int,
        help="development stop after this many newly processed batches",
    )
    parser.add_argument("--wall-limit-seconds", type=float, default=2700.0)
    parser.add_argument("--memory-limit-mib", type=float, default=1024.0)
    arguments = parser.parse_args()
    if not arguments.validation_gate_open:
        raise SystemExit(
            "refusing to start: root must declare the validation gate open, "
            "then pass --validation-gate-open"
        )

    outcome = run_extension_search(
        catalog_path=arguments.catalog,
        parameters_path=arguments.parameters,
        labelg_path=arguments.labelg,
        database_path=arguments.database,
        checkpoint_path=arguments.checkpoint,
        candidate_directory=arguments.candidate_dir,
        provenance_output=arguments.provenance_output,
        unique_output=arguments.unique_output,
        batch_size=arguments.batch_size,
        active_host_ids=tuple(arguments.host_id),
        max_batches=arguments.max_batches,
        wall_limit_seconds=arguments.wall_limit_seconds,
        memory_limit_mib=arguments.memory_limit_mib,
    )
    print(json.dumps(outcome.summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
