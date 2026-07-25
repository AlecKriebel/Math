"""Resumable complete one-edge-toggle search around certified extension seeds.

The source universe is the exact set of 391 canonical rows in
``results/extensions_unique.csv`` whose category is either
``private_obstruction_eternal_false`` or
``eternal_false_without_private_obstruction``.  For every seed, this engine
toggles each unordered vertex pair once.  It never starts work on import, and
its CLI requires an explicit validation-gate acknowledgment.
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
import sys
import tempfile
import time
from collections import Counter
from dataclasses import asdict, dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterable, Sequence

from search.extension_killtest import (
    EXPECTED_LABELG_SHA256,
    NAUTY_ARCHIVE_SHA256,
    canonicalize_graph6_batch,
    sha256_file,
    verify_pinned_labelg,
)
from verifier_a.core import (
    BitGraph,
    EternalResult,
    alpha,
    domination_number,
    eternal_fixed_point,
    theta,
    verify_eternal_result,
)
from verifier_b import (
    Graph,
    clique_cover_number,
    domination_number as domination_number_b,
    find_eternal_family,
    independence_number,
    verify_eternal_family,
)


SCHEMA_VERSION = 1
EXPECTED_SEED_INPUT_SHA256 = (
    "e7f0ffa459d74a67a3a647e19ee5669652ff1679302b3b62daaef299ee02945e"
)
EXPECTED_EXTENSION_AUDIT_SHA256 = (
    "523b3a57ef9afac2b8c921564afcf3fcd8fdbe7719984014f3b0f8e80da8e7cb"
)
SELECTED_CATEGORIES = frozenset(
    {
        "private_obstruction_eternal_false",
        "eternal_false_without_private_obstruction",
    }
)
RUNTIME_SOURCE_RELATIVE_PATHS = (
    "src/search/edge_toggle_killtest.py",
    "src/search/extension_killtest.py",
    "src/search/private_obstruction.py",
    "src/verifier_a/core.py",
    "src/verifier_b/__init__.py",
    "src/verifier_b/graph.py",
    "src/verifier_b/invariants.py",
    "src/verifier_b/eternal.py",
)


@dataclass(frozen=True, slots=True)
class Seed:
    index: int
    seed_id: str
    graph6: str
    order: int
    size: int
    source_category: str

    @property
    def raw_toggle_count(self) -> int:
        return self.order * (self.order - 1) // 2


@dataclass(frozen=True, slots=True)
class SearchConfiguration:
    seed_input_path: str
    seed_input_sha256: str
    extension_audit_path: str
    extension_audit_sha256: str
    labelg_path: str
    labelg_sha256: str
    nauty_archive_sha256: str
    runtime_source_manifest: tuple[tuple[str, str], ...]
    runtime_source_set_sha256: str
    python_implementation: str
    python_version: str
    python_executable: str
    batch_size: int
    active_seed_ids: tuple[str, ...]
    wall_limit_seconds: float
    memory_limit_mib: float
    schema_version: int = SCHEMA_VERSION

    @property
    def digest(self) -> str:
        data = json.dumps(
            asdict(self), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True, slots=True)
class Evaluation:
    connected: bool
    gamma_a: int | None
    gamma_b: int | None
    alpha_a: int | None
    alpha_b: int | None
    gamma_infinity_a: int | None
    gamma_infinity_b: int | None
    theta_a: int | None
    theta_b: int | None
    category: str
    family_size: int | None
    family_sha256: str | None
    eternal_result_a: EternalResult | None = None
    eternal_family_b: frozenset[frozenset[int]] | None = None


@dataclass(frozen=True, slots=True)
class RunOutcome:
    status: str
    batches_processed: int
    candidate_reference: str | None
    summary: dict[str, object]


def _runtime_source_manifest() -> tuple[tuple[str, str], ...]:
    campaign = Path(__file__).resolve().parents[2]
    result = []
    for relative in RUNTIME_SOURCE_RELATIVE_PATHS:
        path = campaign / relative
        if not path.is_file():
            raise ValueError(f"runtime source is missing: {path}")
        result.append((relative, sha256_file(path)))
    return tuple(result)


def _source_set_hash(manifest: Sequence[tuple[str, str]]) -> str:
    digest = hashlib.sha256()
    for relative, file_hash in manifest:
        digest.update(f"{relative},{file_hash}\n".encode("utf-8"))
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


def load_certified_seeds(
    seed_input_path: Path,
    extension_audit_path: Path,
    *,
    require_known_hashes: bool = True,
) -> tuple[Seed, ...]:
    """Load and structurally validate the exact 391-row source universe."""

    input_hash = sha256_file(seed_input_path)
    audit_hash = sha256_file(extension_audit_path)
    if require_known_hashes:
        if input_hash != EXPECTED_SEED_INPUT_SHA256:
            raise ValueError(
                f"seed input hash mismatch: {input_hash} != "
                f"{EXPECTED_SEED_INPUT_SHA256}"
            )
        if audit_hash != EXPECTED_EXTENSION_AUDIT_SHA256:
            raise ValueError(
                f"extension audit hash mismatch: {audit_hash} != "
                f"{EXPECTED_EXTENSION_AUDIT_SHA256}"
            )

    with extension_audit_path.open(encoding="utf-8") as handle:
        audit = json.load(handle)
    if (
        audit.get("status") != "complete"
        or audit.get("passed") is not True
        or audit.get("audit_binding", {}).get("unique_sha256") != input_hash
        or audit.get("unique_canonical_graphs") != 54_216
        or audit.get("verified_origins") != 110_537
    ):
        raise ValueError("extension coverage audit does not bind a passed source")

    with seed_input_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "canonical_graph6",
            "n",
            "m",
            "gamma",
            "alpha",
            "category",
            "eternal_a",
            "eternal_b",
        }
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError("extension unique table has an unexpected schema")
        rows = list(reader)
    if len(rows) != 54_216:
        raise ValueError(f"expected 54216 unique extension rows, got {len(rows)}")

    seen: set[str] = set()
    selected: list[Seed] = []
    all_categories: Counter[str] = Counter()
    for row in rows:
        record = row["canonical_graph6"]
        if record in seen:
            raise ValueError(f"duplicate source graph6 record: {record}")
        seen.add(record)
        all_categories[row["category"]] += 1
        if row["category"] not in SELECTED_CATEGORIES:
            continue
        graph = BitGraph.from_graph6(record)
        if (
            graph.n != int(row["n"])
            or graph.size != int(row["m"])
            or not _is_connected(graph)
            or int(row["gamma"]) != 3
            or int(row["alpha"]) != 3
            or row["eternal_a"] != "0"
            or row["eternal_b"] != "0"
        ):
            raise ValueError(f"invalid selected source row: {record}")
        selected.append(
            Seed(
                index=len(selected),
                seed_id=f"ET-{len(selected) + 1:04d}",
                graph6=record,
                order=graph.n,
                size=graph.size,
                source_category=row["category"],
            )
        )

    if require_known_hashes:
        expected_categories = Counter(
            {
                "gamma_below_3": 52_447,
                "alpha_above_3": 1_378,
                "eternal_false_without_private_obstruction": 285,
                "private_obstruction_eternal_false": 106,
            }
        )
        if all_categories != expected_categories:
            raise ValueError(f"unexpected source categories: {all_categories}")
        if len(selected) != 391:
            raise ValueError(f"selected {len(selected)} seeds, expected 391")
        distribution = Counter(seed.order for seed in selected)
        if distribution != Counter({11: 15, 12: 376}):
            raise ValueError(f"unexpected seed-order distribution: {distribution}")
        if sum(seed.raw_toggle_count for seed in selected) != 25_641:
            raise AssertionError("raw edge-toggle universe must have size 25641")
    return tuple(selected)


def toggle_pairs(order: int) -> tuple[tuple[int, int], ...]:
    if type(order) is not int or order < 0:
        raise ValueError("order must be a nonnegative integer")
    return tuple(combinations(range(order), 2))


def toggle_edge(graph: BitGraph, first: int, second: int) -> BitGraph:
    if (
        type(first) is not int
        or type(second) is not int
        or not 0 <= first < second < graph.n
    ):
        raise ValueError("toggle pair must satisfy 0 <= first < second < n")
    adjacency = list(graph.adj)
    first_bit = 1 << first
    second_bit = 1 << second
    adjacency[first] ^= second_bit
    adjacency[second] ^= first_bit
    return BitGraph(graph.n, tuple(adjacency))


def _positive_finite(value: object, name: str) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value <= 0
    ):
        raise ValueError(f"{name} must be a positive finite number")
    return float(value)


def seed_checkpoint_directory(checkpoint_path: Path) -> Path:
    """Return the sole directory used for per-seed JSON checkpoints."""

    return checkpoint_path.parent / f"{checkpoint_path.stem}.seeds"


def seed_checkpoint_path(checkpoint_path: Path, seed_id: str) -> Path:
    """Return one safe per-seed checkpoint target."""

    if (
        not seed_id
        or Path(seed_id).name != seed_id
        or "/" in seed_id
        or "\\" in seed_id
    ):
        raise ValueError(f"unsafe seed identifier for checkpoint path: {seed_id!r}")
    return seed_checkpoint_directory(checkpoint_path) / f"{seed_id}.json"


def _paths_overlap(first: Path, second: Path) -> bool:
    return (
        first == second
        or first in second.parents
        or second in first.parents
    )


def _validate_path_roles(
    *,
    seed_input_path: Path,
    extension_audit_path: Path,
    labelg_path: Path,
    database_path: Path,
    checkpoint_path: Path,
    candidate_directory: Path,
    provenance_output: Path,
    unique_output: Path,
    seed_ids: Sequence[str],
) -> None:
    campaign = Path(__file__).resolve().parents[2]
    trusted = {
        "seed input": seed_input_path.resolve(),
        "extension audit": extension_audit_path.resolve(),
        "labelg": labelg_path.resolve(),
        **{
            f"runtime source {relative}": (campaign / relative).resolve()
            for relative in RUNTIME_SOURCE_RELATIVE_PATHS
        },
    }
    writable = {
        "database": database_path.resolve(),
        "checkpoint": checkpoint_path.resolve(),
        "provenance": provenance_output.resolve(),
        "unique": unique_output.resolve(),
    }
    items = tuple(writable.items())
    for index, (role, path) in enumerate(items):
        for other_role, other_path in items[index + 1 :]:
            if (
                path == other_path
                or path in other_path.parents
                or other_path in path.parents
            ):
                raise ValueError(
                    f"writable path roles conflict: {role}={path}, "
                    f"{other_role}={other_path}"
                )
        for trusted_role, trusted_path in trusted.items():
            if path == trusted_path:
                raise ValueError(
                    f"{role} aliases trusted {trusted_role}: {path}"
                )
    candidate = candidate_directory.resolve()
    for trusted_role, trusted_path in trusted.items():
        if candidate == trusted_path:
            raise ValueError(
                f"candidate directory aliases trusted {trusted_role}: {candidate}"
            )
    for role, path in writable.items():
        if candidate == path or candidate in path.parents or path in candidate.parents:
            raise ValueError(
                f"candidate directory conflicts with {role}: {candidate}, {path}"
            )

    derived_directory = seed_checkpoint_directory(checkpoint_path).resolve()
    derived_files = {
        seed_id: seed_checkpoint_path(checkpoint_path, seed_id).resolve()
        for seed_id in seed_ids
    }
    for role, path in writable.items():
        if _paths_overlap(derived_directory, path):
            raise ValueError(
                "derived seed-checkpoint directory conflicts with "
                f"{role}: {derived_directory}, {path}"
            )
        for seed_id, derived_file in derived_files.items():
            if _paths_overlap(derived_file, path):
                raise ValueError(
                    f"derived checkpoint for {seed_id} conflicts with "
                    f"{role}: {derived_file}, {path}"
                )
    if _paths_overlap(derived_directory, candidate):
        raise ValueError(
            "derived seed-checkpoint directory conflicts with candidate "
            f"directory: {derived_directory}, {candidate}"
        )
    for seed_id, derived_file in derived_files.items():
        if _paths_overlap(derived_file, candidate):
            raise ValueError(
                f"derived checkpoint for {seed_id} conflicts with candidate "
                f"directory: {derived_file}, {candidate}"
            )
    for trusted_role, trusted_path in trusted.items():
        if _paths_overlap(derived_directory, trusted_path):
            raise ValueError(
                "derived seed-checkpoint directory conflicts with trusted "
                f"{trusted_role}: {derived_directory}, {trusted_path}"
            )
        for seed_id, derived_file in derived_files.items():
            if _paths_overlap(derived_file, trusted_path):
                raise ValueError(
                    f"derived checkpoint for {seed_id} conflicts with trusted "
                    f"{trusted_role}: {derived_file}, {trusted_path}"
                )


def build_configuration(
    *,
    seed_input_path: Path,
    extension_audit_path: Path,
    labelg_path: Path,
    batch_size: int,
    active_seed_ids: Sequence[str] = (),
    wall_limit_seconds: float = 2700.0,
    memory_limit_mib: float = 1024.0,
) -> SearchConfiguration:
    if type(batch_size) is not int or batch_size < 1:
        raise ValueError("batch size must be a positive integer")
    _positive_finite(wall_limit_seconds, "wall limit")
    _positive_finite(memory_limit_mib, "memory limit")
    labelg_hash = verify_pinned_labelg(labelg_path)
    seeds = load_certified_seeds(seed_input_path, extension_audit_path)
    valid_ids = {seed.seed_id for seed in seeds}
    active = tuple(active_seed_ids)
    if len(set(active)) != len(active) or set(active) - valid_ids:
        raise ValueError("active seed identifiers are repeated or unknown")
    canonical = canonicalize_graph6_batch(
        tuple(seed.graph6 for seed in seeds), labelg_path
    )
    if canonical != tuple(seed.graph6 for seed in seeds):
        raise ValueError("selected seed table is not canonically labeled")
    manifest = _runtime_source_manifest()
    return SearchConfiguration(
        seed_input_path=str(seed_input_path.resolve()),
        seed_input_sha256=sha256_file(seed_input_path),
        extension_audit_path=str(extension_audit_path.resolve()),
        extension_audit_sha256=sha256_file(extension_audit_path),
        labelg_path=str(labelg_path.resolve()),
        labelg_sha256=labelg_hash,
        nauty_archive_sha256=NAUTY_ARCHIVE_SHA256,
        runtime_source_manifest=manifest,
        runtime_source_set_sha256=_source_set_hash(manifest),
        python_implementation=platform.python_implementation(),
        python_version=platform.python_version(),
        python_executable=str(Path(sys.executable).resolve()),
        batch_size=batch_size,
        active_seed_ids=active,
        wall_limit_seconds=wall_limit_seconds,
        memory_limit_mib=memory_limit_mib,
    )


def _normalize_mask_family(
    family: Iterable[int], order: int
) -> frozenset[frozenset[int]]:
    return frozenset(
        frozenset(vertex for vertex in range(order) if mask >> vertex & 1)
        for mask in family
    )


def _family_hash(family: Iterable[frozenset[int]]) -> str:
    digest = hashlib.sha256()
    for configuration in sorted(
        family, key=lambda value: tuple(sorted(value))
    ):
        digest.update(
            (" ".join(map(str, sorted(configuration))) + "\n").encode("ascii")
        )
    return digest.hexdigest()


def evaluate_toggled_graph(graph6: str) -> Evaluation:
    """Recompute all target parameters exactly and independently."""

    graph_a = BitGraph.from_graph6(graph6)
    if not _is_connected(graph_a):
        return Evaluation(
            False,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "disconnected",
            None,
            None,
        )
    graph_b = Graph.from_graph6(graph6)
    gamma_a = domination_number(graph_a)
    gamma_b = domination_number_b(graph_b)
    alpha_a = alpha(graph_a)
    alpha_b = independence_number(graph_b)
    if gamma_a != gamma_b or alpha_a != alpha_b:
        raise AssertionError(
            ("A/B invariant disagreement", graph6, gamma_a, gamma_b, alpha_a, alpha_b)
        )

    winning_a: EternalResult | None = None
    winning_b: frozenset[frozenset[int]] | None = None
    gamma_infinity = None
    for guard_count in range(gamma_a, graph_a.n + 1):
        result_a = eternal_fixed_point(graph_a, guard_count)
        family_b = find_eternal_family(graph_b, guard_count)
        decision_b = family_b is not None
        if result_a.exists != decision_b:
            raise AssertionError(
                ("A/B eternal decision disagreement", graph6, guard_count)
            )
        if result_a.exists:
            normalized_a = _normalize_mask_family(result_a.family, graph_a.n)
            assert family_b is not None
            if normalized_a != family_b:
                raise AssertionError(
                    ("A/B greatest-family disagreement", graph6, guard_count)
                )
            if not verify_eternal_result(graph_a, result_a):
                raise AssertionError("verifier A rejected its generated certificate")
            if not verify_eternal_family(graph_b, guard_count, family_b):
                raise AssertionError("verifier B rejected its generated family")
            gamma_infinity = guard_count
            winning_a = result_a
            winning_b = family_b
            break
    if gamma_infinity is None or winning_a is None or winning_b is None:
        raise AssertionError("full vertex set must be eternal")

    theta_a = theta(graph_a)
    theta_b = clique_cover_number(graph_b)
    if theta_a != theta_b:
        raise AssertionError(
            ("A/B clique-cover disagreement", graph6, theta_a, theta_b)
        )
    if not gamma_a <= alpha_a <= gamma_infinity <= theta_a:
        raise AssertionError(
            ("parameter chain failure", graph6, gamma_a, alpha_a, gamma_infinity, theta_a)
        )
    if gamma_a == gamma_infinity < theta_a:
        category = "candidate_gamma_equals_eternal_below_theta"
    elif gamma_a == gamma_infinity:
        category = "equality_without_theta_gap"
    else:
        category = "gamma_below_eternal"
    return Evaluation(
        True,
        gamma_a,
        gamma_b,
        alpha_a,
        alpha_b,
        gamma_infinity,
        gamma_infinity,
        theta_a,
        theta_b,
        category,
        len(winning_b),
        _family_hash(winning_b),
        winning_a,
        winning_b,
    )


def _connect_database(
    path: Path, configuration: SearchConfiguration, seeds: Sequence[Seed]
) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
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
                CREATE TABLE seeds (
                    seed_index INTEGER NOT NULL UNIQUE,
                    seed_id TEXT PRIMARY KEY,
                    graph6 TEXT NOT NULL UNIQUE,
                    n INTEGER NOT NULL,
                    m INTEGER NOT NULL,
                    source_category TEXT NOT NULL,
                    raw_expected INTEGER NOT NULL,
                    next_pair_index INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    canonical_stream_sha256 TEXT
                );
                CREATE TABLE canonical_graphs (
                    graph6 TEXT PRIMARY KEY,
                    n INTEGER NOT NULL,
                    m INTEGER NOT NULL,
                    connected INTEGER NOT NULL,
                    origin_count INTEGER NOT NULL,
                    first_seed_id TEXT NOT NULL,
                    first_pair_index INTEGER NOT NULL,
                    first_raw_graph6 TEXT NOT NULL,
                    gamma_a INTEGER,
                    gamma_b INTEGER,
                    alpha_a INTEGER,
                    alpha_b INTEGER,
                    gamma_infinity_a INTEGER,
                    gamma_infinity_b INTEGER,
                    theta_a INTEGER,
                    theta_b INTEGER,
                    category TEXT NOT NULL,
                    family_size INTEGER,
                    family_sha256 TEXT,
                    FOREIGN KEY(first_seed_id) REFERENCES seeds(seed_id)
                );
                CREATE TABLE origins (
                    seed_id TEXT NOT NULL,
                    pair_index INTEGER NOT NULL,
                    first_vertex INTEGER NOT NULL,
                    second_vertex INTEGER NOT NULL,
                    toggle_action TEXT NOT NULL,
                    raw_graph6 TEXT NOT NULL,
                    canonical_graph6 TEXT NOT NULL,
                    category TEXT NOT NULL,
                    PRIMARY KEY(seed_id, pair_index),
                    FOREIGN KEY(seed_id) REFERENCES seeds(seed_id),
                    FOREIGN KEY(canonical_graph6)
                        REFERENCES canonical_graphs(graph6)
                );
                CREATE INDEX origins_by_canonical
                    ON origins(canonical_graph6, seed_id, pair_index);
                """
            )
            metadata = {
                "configuration_json": json.dumps(
                    asdict(configuration), sort_keys=True
                ),
                "configuration_sha256": configuration.digest,
                "candidate_frozen_path": "",
            }
            connection.executemany(
                "INSERT INTO metadata(key, value) VALUES (?, ?)",
                tuple(metadata.items()),
            )
            for seed in seeds:
                connection.execute(
                    """
                    INSERT INTO seeds(
                        seed_index, seed_id, graph6, n, m, source_category,
                        raw_expected, next_pair_index, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 'pending')
                    """,
                    (
                        seed.index,
                        seed.seed_id,
                        seed.graph6,
                        seed.order,
                        seed.size,
                        seed.source_category,
                        seed.raw_toggle_count,
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
            raise ValueError("checkpoint configuration mismatch")
        stored = tuple(
            row[0]
            for row in connection.execute(
                "SELECT seed_id FROM seeds ORDER BY seed_index"
            )
        )
        if stored != tuple(seed.seed_id for seed in seeds):
            connection.close()
            raise ValueError("checkpoint seed universe mismatch")
    return connection


def _stream_hash(connection: sqlite3.Connection, seed_id: str) -> str:
    digest = hashlib.sha256()
    for (record,) in connection.execute(
        """
        SELECT canonical_graph6 FROM origins
        WHERE seed_id = ? ORDER BY pair_index
        """,
        (seed_id,),
    ):
        digest.update(record.encode("ascii") + b"\n")
    return digest.hexdigest()


def _validate_or_repair_complete_seed(
    connection: sqlite3.Connection, seed: Seed
) -> str:
    row = connection.execute(
        """
        SELECT s.next_pair_index, s.status, s.canonical_stream_sha256,
               COUNT(o.pair_index)
        FROM seeds AS s
        LEFT JOIN origins AS o ON o.seed_id = s.seed_id
        WHERE s.seed_id = ? GROUP BY s.seed_id
        """,
        (seed.seed_id,),
    ).fetchone()
    if row is None or row[1] != "complete":
        raise ValueError(f"seed is not complete: {seed.seed_id}")
    if int(row[0]) != seed.raw_toggle_count or int(row[3]) != seed.raw_toggle_count:
        raise RuntimeError(f"inconsistent completed seed: {seed.seed_id}")
    calculated = _stream_hash(connection, seed.seed_id)
    if row[2] is None:
        connection.execute(
            """
            UPDATE seeds SET canonical_stream_sha256 = ? WHERE seed_id = ?
            """,
            (calculated, seed.seed_id),
        )
        connection.commit()
    elif row[2] != calculated:
        raise RuntimeError(f"completed seed stream mismatch: {seed.seed_id}")
    return calculated


def _candidate_state(connection: sqlite3.Connection) -> dict[str, object]:
    marker_row = connection.execute(
        "SELECT value FROM metadata WHERE key = 'candidate_frozen_path'"
    ).fetchone()
    marker = None if marker_row is None or not marker_row[0] else str(marker_row[0])
    canonical_rows = tuple(
        str(row[0])
        for row in connection.execute(
            """
            SELECT graph6 FROM canonical_graphs
            WHERE category = 'candidate_gamma_equals_eternal_below_theta'
            ORDER BY graph6
            """
        )
    )
    origin_rows = tuple(
        (str(row[0]), int(row[1]), str(row[2]))
        for row in connection.execute(
            """
            SELECT seed_id, pair_index, canonical_graph6 FROM origins
            WHERE category = 'candidate_gamma_equals_eternal_below_theta'
            ORDER BY seed_id, pair_index
            """
        )
    )
    pending = marker is not None or bool(canonical_rows) or bool(origin_rows)
    reference = marker
    graph_for_reference = (
        canonical_rows[0]
        if canonical_rows
        else (origin_rows[0][2] if origin_rows else None)
    )
    if reference is None and graph_for_reference is not None:
        digest = hashlib.sha256(
            (graph_for_reference + "\n").encode("ascii")
        ).hexdigest()
        reference = f"UNRECORDED-CANDIDATE-SHA256:{digest}"
    inconsistencies = []
    if marker is not None and not canonical_rows and not origin_rows:
        inconsistencies.append("marker exists without candidate row")
    if marker is None and (canonical_rows or origin_rows):
        inconsistencies.append("candidate row exists without marker")
    if marker is not None and not Path(marker).is_file():
        inconsistencies.append("candidate marker path is missing")
    return {
        "pending": pending,
        "primary_reference": reference,
        "marker_path": marker,
        "marker_file_exists": marker is not None and Path(marker).is_file(),
        "canonical_candidate_count": len(canonical_rows),
        "origin_candidate_count": len(origin_rows),
        "canonical_candidate_graph6": list(canonical_rows),
        "origin_candidates": [
            {
                "seed_id": seed_id,
                "pair_index": pair_index,
                "canonical_graph6": graph6,
            }
            for seed_id, pair_index, graph6 in origin_rows
        ],
        "inconsistencies": inconsistencies,
    }


def _evaluation_from_row(row: Sequence[object]) -> Evaluation:
    def optional_int(value: object) -> int | None:
        return None if value is None else int(value)

    return Evaluation(
        connected=bool(row[0]),
        gamma_a=optional_int(row[1]),
        gamma_b=optional_int(row[2]),
        alpha_a=optional_int(row[3]),
        alpha_b=optional_int(row[4]),
        gamma_infinity_a=optional_int(row[5]),
        gamma_infinity_b=optional_int(row[6]),
        theta_a=optional_int(row[7]),
        theta_b=optional_int(row[8]),
        category=str(row[9]),
        family_size=optional_int(row[10]),
        family_sha256=None if row[11] is None else str(row[11]),
    )


def _insert_origin(
    connection: sqlite3.Connection,
    *,
    seed: Seed,
    pair_index: int,
    first: int,
    second: int,
    action: str,
    raw_graph6: str,
    canonical_graph6: str,
    evaluation: Evaluation | None,
) -> Evaluation:
    row = connection.execute(
        """
        SELECT connected, gamma_a, gamma_b, alpha_a, alpha_b,
               gamma_infinity_a, gamma_infinity_b, theta_a, theta_b,
               category, family_size, family_sha256
        FROM canonical_graphs WHERE graph6 = ?
        """,
        (canonical_graph6,),
    ).fetchone()
    if row is None:
        if evaluation is None:
            evaluation = evaluate_toggled_graph(canonical_graph6)
        graph = BitGraph.from_graph6(canonical_graph6)
        connection.execute(
            """
            INSERT INTO canonical_graphs(
                graph6, n, m, connected, origin_count, first_seed_id,
                first_pair_index, first_raw_graph6, gamma_a, gamma_b,
                alpha_a, alpha_b, gamma_infinity_a, gamma_infinity_b,
                theta_a, theta_b, category, family_size, family_sha256
            ) VALUES (?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                canonical_graph6,
                graph.n,
                graph.size,
                int(evaluation.connected),
                seed.seed_id,
                pair_index,
                raw_graph6,
                evaluation.gamma_a,
                evaluation.gamma_b,
                evaluation.alpha_a,
                evaluation.alpha_b,
                evaluation.gamma_infinity_a,
                evaluation.gamma_infinity_b,
                evaluation.theta_a,
                evaluation.theta_b,
                evaluation.category,
                evaluation.family_size,
                evaluation.family_sha256,
            ),
        )
    else:
        evaluation = _evaluation_from_row(row)
    connection.execute(
        """
        INSERT INTO origins(
            seed_id, pair_index, first_vertex, second_vertex, toggle_action,
            raw_graph6, canonical_graph6, category
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            seed.seed_id,
            pair_index,
            first,
            second,
            action,
            raw_graph6,
            canonical_graph6,
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


def _eternal_payload(result: EternalResult) -> dict[str, object]:
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
    seed: Seed,
    pair_index: int,
    first: int,
    second: int,
    action: str,
    raw_graph6: str,
    canonical_graph6: str,
    evaluation: Evaluation,
    configuration: SearchConfiguration,
) -> Path:
    if (
        evaluation.category
        != "candidate_gamma_equals_eternal_below_theta"
        or evaluation.eternal_result_a is None
        or evaluation.eternal_family_b is None
    ):
        raise ValueError("only a dual-solver candidate can be frozen")
    graph = BitGraph.from_graph6(canonical_graph6)
    graph_hash = hashlib.sha256(
        (canonical_graph6 + "\n").encode("ascii")
    ).hexdigest()
    payload = {
        "status": "FROZEN-UNREVIEWED-EDGE-TOGGLE-CANDIDATE",
        "warning": (
            "This is a search artifact, not a counterexample claim; the full "
            "standalone certificate protocol remains required."
        ),
        "configuration_sha256": configuration.digest,
        "seed": asdict(seed),
        "pair_index": pair_index,
        "pair": [first, second],
        "toggle_action": action,
        "raw_toggled_graph6": raw_graph6,
        "canonical_graph6": canonical_graph6,
        "canonical_graph6_sha256": graph_hash,
        "n": graph.n,
        "m": graph.size,
        "edges": [
            [u, v]
            for u in range(graph.n)
            for v in range(u + 1, graph.n)
            if graph.adj[u] >> v & 1
        ],
        "gamma": evaluation.gamma_a,
        "alpha": evaluation.alpha_a,
        "gamma_infinity": evaluation.gamma_infinity_a,
        "theta": evaluation.theta_a,
        "eternal_a": _eternal_payload(evaluation.eternal_result_a),
        "eternal_b_family": [
            list(sorted(configuration_set))
            for configuration_set in sorted(
                evaluation.eternal_family_b,
                key=lambda value: tuple(sorted(value)),
            )
        ],
        "family_sha256": evaluation.family_sha256,
        "frozen_unix": time.time(),
    }
    candidate_directory.mkdir(parents=True, exist_ok=True)
    path = candidate_directory / f"candidate-{graph_hash[:20]}.json"
    if path.exists():
        with path.open(encoding="utf-8") as handle:
            existing = json.load(handle)
        if (
            existing.get("canonical_graph6_sha256") != graph_hash
            or existing.get("configuration_sha256") != configuration.digest
        ):
            raise RuntimeError(f"candidate artifact collision: {path}")
        return path
    _atomic_json(path, payload)
    return path


def _resource_snapshot() -> dict[str, object]:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    raw = int(usage.ru_maxrss)
    mib = raw / (1024 * 1024) if platform.system() == "Darwin" else raw / 1024
    return {
        "user_cpu_seconds": usage.ru_utime,
        "system_cpu_seconds": usage.ru_stime,
        "maximum_resident_set_size_raw": raw,
        "maximum_resident_set_size_mib": mib,
        "maximum_resident_set_size_unit": (
            "bytes" if platform.system() == "Darwin" else "KiB"
        ),
    }


def summarize_database(
    connection: sqlite3.Connection,
    *,
    configuration: SearchConfiguration,
    database_path: Path,
    status: str,
    started_unix: float,
    process_started: float,
    batches_processed: int,
) -> dict[str, object]:
    raw_processed = int(
        connection.execute("SELECT COUNT(*) FROM origins").fetchone()[0]
    )
    raw_expected = int(
        connection.execute("SELECT SUM(raw_expected) FROM seeds").fetchone()[0]
    )
    categories = {
        str(row[0]): int(row[1])
        for row in connection.execute(
            """
            SELECT category, COUNT(*) FROM origins
            GROUP BY category ORDER BY category
            """
        )
    }
    unique_categories = {
        str(row[0]): int(row[1])
        for row in connection.execute(
            """
            SELECT category, COUNT(*) FROM canonical_graphs
            GROUP BY category ORDER BY category
            """
        )
    }
    candidate_state = _candidate_state(connection)
    seeds = [
        {
            "seed_id": row[0],
            "n": int(row[1]),
            "raw_expected": int(row[2]),
            "raw_processed": int(row[3]),
            "next_pair_index": int(row[4]),
            "status": row[5],
            "canonical_stream_sha256": row[6],
        }
        for row in connection.execute(
            """
            SELECT s.seed_id, s.n, s.raw_expected, COUNT(o.pair_index),
                   s.next_pair_index, s.status, s.canonical_stream_sha256
            FROM seeds AS s
            LEFT JOIN origins AS o ON o.seed_id = s.seed_id
            GROUP BY s.seed_id ORDER BY s.seed_index
            """
        )
    ]
    return {
        "status": status,
        "configuration": asdict(configuration),
        "configuration_sha256": configuration.digest,
        "database": str(database_path.resolve()),
        "database_sha256": sha256_file(database_path),
        "raw_expected": raw_expected,
        "raw_processed": raw_processed,
        "unique_canonical_graphs": int(
            connection.execute("SELECT COUNT(*) FROM canonical_graphs").fetchone()[0]
        ),
        "raw_category_counts": categories,
        "unique_category_counts": unique_categories,
        "seeds_complete": sum(row["status"] == "complete" for row in seeds),
        "seeds": seeds,
        "candidate_reference": candidate_state["primary_reference"],
        "candidate_state": candidate_state,
        "batches_processed_this_process": batches_processed,
        "started_unix_this_process": started_unix,
        "updated_unix": time.time(),
        "wall_seconds_this_process": time.perf_counter() - process_started,
        "resource_usage": _resource_snapshot(),
        "process_argv": list(sys.argv),
    }


def _checkpoint(
    path: Path,
    connection: sqlite3.Connection,
    *,
    configuration: SearchConfiguration,
    database_path: Path,
    status: str,
    started_unix: float,
    process_started: float,
    batches_processed: int,
) -> dict[str, object]:
    connection.commit()
    payload = summarize_database(
        connection,
        configuration=configuration,
        database_path=database_path,
        status=status,
        started_unix=started_unix,
        process_started=process_started,
        batches_processed=batches_processed,
    )
    _atomic_json(path, payload)
    return payload


def _write_seed_checkpoint(
    checkpoint_path: Path,
    connection: sqlite3.Connection,
    seed: Seed,
    configuration: SearchConfiguration,
) -> None:
    stream_hash = _validate_or_repair_complete_seed(connection, seed)
    path = seed_checkpoint_path(checkpoint_path, seed.seed_id)
    category_counts = {
        str(row[0]): int(row[1])
        for row in connection.execute(
            """
            SELECT category, COUNT(*) FROM origins
            WHERE seed_id = ? GROUP BY category ORDER BY category
            """,
            (seed.seed_id,),
        )
    }
    _atomic_json(
        path,
        {
            "status": "complete",
            "configuration_sha256": configuration.digest,
            "seed": asdict(seed),
            "raw_processed": seed.raw_toggle_count,
            "canonical_stream_sha256": stream_hash,
            "raw_category_counts": category_counts,
        },
    )


def audit_complete_coverage(
    connection: sqlite3.Connection, seeds: Sequence[Seed]
) -> dict[str, object]:
    errors = []
    total = 0
    for seed in seeds:
        total += seed.raw_toggle_count
        row = connection.execute(
            """
            SELECT s.next_pair_index, s.status, s.canonical_stream_sha256,
                   COUNT(o.pair_index), MIN(o.pair_index), MAX(o.pair_index)
            FROM seeds AS s
            LEFT JOIN origins AS o ON o.seed_id = s.seed_id
            WHERE s.seed_id = ? GROUP BY s.seed_id
            """,
            (seed.seed_id,),
        ).fetchone()
        if (
            row is None
            or int(row[0]) != seed.raw_toggle_count
            or row[1] != "complete"
            or int(row[3]) != seed.raw_toggle_count
            or row[4] != 0
            or row[5] != seed.raw_toggle_count - 1
            or row[2] != _stream_hash(connection, seed.seed_id)
        ):
            errors.append(f"incomplete or inconsistent seed: {seed.seed_id}")
    origin_count = int(
        connection.execute("SELECT COUNT(*) FROM origins").fetchone()[0]
    )
    multiplicity = int(
        connection.execute(
            "SELECT COALESCE(SUM(origin_count), 0) FROM canonical_graphs"
        ).fetchone()[0]
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
    if total != 25_641 or origin_count != total or multiplicity != total:
        errors.append(
            f"global count mismatch: expected={total}, origins={origin_count}, "
            f"multiplicity={multiplicity}"
        )
    if bad_multiplicities:
        errors.append(
            f"{bad_multiplicities} canonical multiplicities are inconsistent"
        )
    candidate_state = _candidate_state(connection)
    if candidate_state["pending"]:
        errors.append("candidate state is pending review")
    return {
        "passed": not errors,
        "errors": errors,
        "raw_expected": total,
        "raw_origins": origin_count,
        "stored_origin_multiplicity": multiplicity,
        "bad_canonical_multiplicity_count": bad_multiplicities,
        "candidate_state": candidate_state,
    }


def export_results(
    connection: sqlite3.Connection,
    provenance_output: Path,
    unique_output: Path,
) -> dict[str, str]:
    provenance_hash = _atomic_csv(
        provenance_output,
        (
            "seed_id",
            "pair_index",
            "first_vertex",
            "second_vertex",
            "toggle_action",
            "raw_graph6",
            "canonical_graph6",
            "category",
        ),
        connection.execute(
            """
            SELECT o.seed_id, o.pair_index, o.first_vertex, o.second_vertex,
                   o.toggle_action, o.raw_graph6, o.canonical_graph6, o.category
            FROM origins AS o JOIN seeds AS s ON s.seed_id = o.seed_id
            ORDER BY s.seed_index, o.pair_index
            """
        ),
    )
    unique_hash = _atomic_csv(
        unique_output,
        (
            "canonical_graph6",
            "n",
            "m",
            "connected",
            "origin_count",
            "first_seed_id",
            "first_pair_index",
            "first_raw_graph6",
            "gamma_a",
            "gamma_b",
            "alpha_a",
            "alpha_b",
            "gamma_infinity_a",
            "gamma_infinity_b",
            "theta_a",
            "theta_b",
            "category",
            "family_size",
            "family_sha256",
        ),
        connection.execute(
            """
            SELECT graph6, n, m, connected, origin_count, first_seed_id,
                   first_pair_index, first_raw_graph6, gamma_a, gamma_b,
                   alpha_a, alpha_b, gamma_infinity_a, gamma_infinity_b,
                   theta_a, theta_b, category, family_size, family_sha256
            FROM canonical_graphs ORDER BY n, graph6
            """
        ),
    )
    return {
        str(provenance_output.resolve()): provenance_hash,
        str(unique_output.resolve()): unique_hash,
    }


def _active_seeds(
    seeds: Sequence[Seed], active_ids: Sequence[str]
) -> tuple[Seed, ...]:
    if not active_ids:
        return tuple(seeds)
    by_id = {seed.seed_id: seed for seed in seeds}
    return tuple(by_id[seed_id] for seed_id in active_ids)


def run_edge_toggle_search(
    *,
    seed_input_path: Path,
    extension_audit_path: Path,
    labelg_path: Path,
    database_path: Path,
    checkpoint_path: Path,
    candidate_directory: Path,
    provenance_output: Path,
    unique_output: Path,
    batch_size: int = 32,
    active_seed_ids: Sequence[str] = (),
    max_batches: int | None = None,
    wall_limit_seconds: float = 2700.0,
    memory_limit_mib: float = 1024.0,
) -> RunOutcome:
    if max_batches is not None and (
        type(max_batches) is not int or max_batches < 1
    ):
        raise ValueError("max_batches must be a positive integer")
    _positive_finite(wall_limit_seconds, "wall limit")
    _positive_finite(memory_limit_mib, "memory limit")
    seeds = load_certified_seeds(seed_input_path, extension_audit_path)
    _validate_path_roles(
        seed_input_path=seed_input_path,
        extension_audit_path=extension_audit_path,
        labelg_path=labelg_path,
        database_path=database_path,
        checkpoint_path=checkpoint_path,
        candidate_directory=candidate_directory,
        provenance_output=provenance_output,
        unique_output=unique_output,
        seed_ids=tuple(seed.seed_id for seed in seeds),
    )
    configuration = build_configuration(
        seed_input_path=seed_input_path,
        extension_audit_path=extension_audit_path,
        labelg_path=labelg_path,
        batch_size=batch_size,
        active_seed_ids=active_seed_ids,
        wall_limit_seconds=wall_limit_seconds,
        memory_limit_mib=memory_limit_mib,
    )
    active = _active_seeds(seeds, configuration.active_seed_ids)
    started_unix = time.time()
    process_started = time.perf_counter()
    batches = 0
    connection = _connect_database(database_path, configuration, seeds)
    try:
        candidate_state = _candidate_state(connection)
        if candidate_state["pending"]:
            reference = str(candidate_state["primary_reference"])
            summary = _checkpoint(
                checkpoint_path,
                connection,
                configuration=configuration,
                database_path=database_path,
                status="candidate_review_pending",
                started_unix=started_unix,
                process_started=process_started,
                batches_processed=0,
            )
            return RunOutcome("candidate_review_pending", 0, reference, summary)

        stop_after_seed = False
        for seed in active:
            progress = connection.execute(
                """
                SELECT next_pair_index, status FROM seeds WHERE seed_id = ?
                """,
                (seed.seed_id,),
            ).fetchone()
            assert progress is not None
            next_index = int(progress[0])
            if progress[1] == "complete":
                _write_seed_checkpoint(
                    checkpoint_path, connection, seed, configuration
                )
                continue
            connection.execute(
                "UPDATE seeds SET status = 'running' WHERE seed_id = ?",
                (seed.seed_id,),
            )
            connection.commit()
            pairs = toggle_pairs(seed.order)
            seed_graph = BitGraph.from_graph6(seed.graph6)

            while next_index < seed.raw_toggle_count:
                end = min(seed.raw_toggle_count, next_index + batch_size)
                indexed_pairs = tuple(enumerate(pairs[next_index:end], next_index))
                raw_graphs = []
                actions = []
                for _, (first, second) in indexed_pairs:
                    deletion = bool(seed_graph.adj[first] >> second & 1)
                    actions.append("delete" if deletion else "add")
                    raw_graphs.append(
                        toggle_edge(seed_graph, first, second).to_graph6()
                    )
                canonical = canonicalize_graph6_batch(
                    tuple(raw_graphs), labelg_path
                )

                candidate_path: Path | None = None
                processed_through = next_index - 1
                connection.execute("BEGIN IMMEDIATE")
                try:
                    for (
                        (pair_index, (first, second)),
                        action,
                        raw_graph6,
                        canonical_graph6,
                    ) in zip(
                        indexed_pairs,
                        actions,
                        raw_graphs,
                        canonical,
                        strict=True,
                    ):
                        graph_row = connection.execute(
                            "SELECT 1 FROM canonical_graphs WHERE graph6 = ?",
                            (canonical_graph6,),
                        ).fetchone()
                        evaluation = None
                        if graph_row is None:
                            evaluation = evaluate_toggled_graph(canonical_graph6)
                            if (
                                evaluation.category
                                == "candidate_gamma_equals_eternal_below_theta"
                            ):
                                candidate_path = freeze_candidate(
                                    candidate_directory,
                                    seed=seed,
                                    pair_index=pair_index,
                                    first=first,
                                    second=second,
                                    action=action,
                                    raw_graph6=raw_graph6,
                                    canonical_graph6=canonical_graph6,
                                    evaluation=evaluation,
                                    configuration=configuration,
                                )
                        stored = _insert_origin(
                            connection,
                            seed=seed,
                            pair_index=pair_index,
                            first=first,
                            second=second,
                            action=action,
                            raw_graph6=raw_graph6,
                            canonical_graph6=canonical_graph6,
                            evaluation=evaluation,
                        )
                        processed_through = pair_index
                        if (
                            stored.category
                            == "candidate_gamma_equals_eternal_below_theta"
                            and candidate_path is None
                        ):
                            marker = connection.execute(
                                """
                                SELECT value FROM metadata
                                WHERE key = 'candidate_frozen_path'
                                """
                            ).fetchone()
                            if marker is None or not marker[0]:
                                raise RuntimeError(
                                    "candidate row has no frozen marker"
                                )
                            candidate_path = Path(marker[0])
                        if candidate_path is not None:
                            break

                    next_index = processed_through + 1
                    seed_complete = next_index == seed.raw_toggle_count
                    stream_hash = (
                        _stream_hash(connection, seed.seed_id)
                        if seed_complete
                        else None
                    )
                    connection.execute(
                        """
                        UPDATE seeds
                        SET next_pair_index = ?, status = ?,
                            canonical_stream_sha256 = ?
                        WHERE seed_id = ?
                        """,
                        (
                            next_index,
                            "complete" if seed_complete else "running",
                            stream_hash,
                            seed.seed_id,
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

                batches += 1
                if seed_complete:
                    _write_seed_checkpoint(
                        checkpoint_path, connection, seed, configuration
                    )
                if candidate_path is not None:
                    summary = _checkpoint(
                        checkpoint_path,
                        connection,
                        configuration=configuration,
                        database_path=database_path,
                        status="candidate_review_pending",
                        started_unix=started_unix,
                        process_started=process_started,
                        batches_processed=batches,
                    )
                    return RunOutcome(
                        "candidate_review_pending",
                        batches,
                        str(candidate_path.resolve()),
                        summary,
                    )

                status = "running"
                if max_batches is not None and batches >= max_batches:
                    status = "bounded_sample_complete"
                summary = _checkpoint(
                    checkpoint_path,
                    connection,
                    configuration=configuration,
                    database_path=database_path,
                    status=status,
                    started_unix=started_unix,
                    process_started=process_started,
                    batches_processed=batches,
                )
                if status == "bounded_sample_complete":
                    return RunOutcome(status, batches, None, summary)
                usage = float(
                    summary["resource_usage"]["maximum_resident_set_size_mib"]  # type: ignore[index]
                )
                if usage > memory_limit_mib:
                    summary = _checkpoint(
                        checkpoint_path,
                        connection,
                        configuration=configuration,
                        database_path=database_path,
                        status="memory_gate_at_batch_checkpoint",
                        started_unix=started_unix,
                        process_started=process_started,
                        batches_processed=batches,
                    )
                    return RunOutcome(
                        "memory_gate_at_batch_checkpoint", batches, None, summary
                    )
                if time.perf_counter() - process_started > wall_limit_seconds:
                    stop_after_seed = True

            _write_seed_checkpoint(
                checkpoint_path, connection, seed, configuration
            )
            if stop_after_seed:
                summary = _checkpoint(
                    checkpoint_path,
                    connection,
                    configuration=configuration,
                    database_path=database_path,
                    status="wall_gate_at_seed_checkpoint",
                    started_unix=started_unix,
                    process_started=process_started,
                    batches_processed=batches,
                )
                return RunOutcome(
                    "wall_gate_at_seed_checkpoint", batches, None, summary
                )

        candidate_state = _candidate_state(connection)
        if candidate_state["pending"]:
            reference = str(candidate_state["primary_reference"])
            summary = _checkpoint(
                checkpoint_path,
                connection,
                configuration=configuration,
                database_path=database_path,
                status="candidate_review_pending",
                started_unix=started_unix,
                process_started=process_started,
                batches_processed=batches,
            )
            return RunOutcome(
                "candidate_review_pending", batches, reference, summary
            )
        full_universe = not configuration.active_seed_ids
        status = "complete" if full_universe else "selected_seeds_complete"
        output_hashes: dict[str, str] = {}
        coverage_audit: dict[str, object] | None = None
        if status == "complete":
            coverage_audit = audit_complete_coverage(connection, seeds)
            if not coverage_audit["passed"]:
                raise AssertionError(
                    ("edge-toggle coverage audit failed", coverage_audit["errors"])
                )
            output_hashes = export_results(
                connection, provenance_output, unique_output
            )
        summary = _checkpoint(
            checkpoint_path,
            connection,
            configuration=configuration,
            database_path=database_path,
            status=status,
            started_unix=started_unix,
            process_started=process_started,
            batches_processed=batches,
        )
        if coverage_audit is not None:
            summary["coverage_audit"] = coverage_audit
            summary["output_sha256"] = output_hashes
            _atomic_json(checkpoint_path, summary)
        return RunOutcome(status, batches, None, summary)
    except BaseException:
        try:
            _checkpoint(
                checkpoint_path,
                connection,
                configuration=configuration,
                database_path=database_path,
                status="failed_at_last_committed_batch",
                started_unix=started_unix,
                process_started=process_started,
                batches_processed=batches,
            )
        finally:
            connection.close()
        raise
    finally:
        try:
            connection.close()
        except sqlite3.ProgrammingError:
            pass


def _campaign_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> None:
    campaign = _campaign_root()
    parser = argparse.ArgumentParser(
        description="Complete one-edge-toggle search around 391 extension seeds"
    )
    parser.add_argument("--validation-gate-open", action="store_true")
    parser.add_argument(
        "--seed-input",
        type=Path,
        default=campaign / "results" / "extensions_unique.csv",
    )
    parser.add_argument(
        "--extension-audit",
        type=Path,
        default=campaign / "results" / "extension_coverage_audit.json",
    )
    parser.add_argument(
        "--labelg",
        type=Path,
        default=campaign / "tools" / "nauty2_9_3" / "labelg",
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=campaign
        / "results"
        / "checkpoints"
        / "edge_toggles.sqlite3",
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=campaign / "results" / "checkpoints" / "edge_toggles.json",
    )
    parser.add_argument(
        "--candidate-dir",
        type=Path,
        default=campaign / "certificates" / "frozen_edge_toggle_candidates",
    )
    parser.add_argument(
        "--provenance-output",
        type=Path,
        default=campaign / "results" / "edge_toggles_provenance.csv",
    )
    parser.add_argument(
        "--unique-output",
        type=Path,
        default=campaign / "results" / "edge_toggles_unique.csv",
    )
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--seed-id", action="append", default=[])
    parser.add_argument("--max-batches", type=int)
    parser.add_argument("--wall-limit-seconds", type=float, default=2700.0)
    parser.add_argument("--memory-limit-mib", type=float, default=1024.0)
    arguments = parser.parse_args()
    if not arguments.validation_gate_open:
        raise SystemExit(
            "refusing to start: pass --validation-gate-open only after the "
            "campaign validation gate is explicitly opened"
        )
    outcome = run_edge_toggle_search(
        seed_input_path=arguments.seed_input,
        extension_audit_path=arguments.extension_audit,
        labelg_path=arguments.labelg,
        database_path=arguments.database,
        checkpoint_path=arguments.checkpoint,
        candidate_directory=arguments.candidate_dir,
        provenance_output=arguments.provenance_output,
        unique_output=arguments.unique_output,
        batch_size=arguments.batch_size,
        active_seed_ids=tuple(arguments.seed_id),
        max_batches=arguments.max_batches,
        wall_limit_seconds=arguments.wall_limit_seconds,
        memory_limit_mib=arguments.memory_limit_mib,
    )
    print(json.dumps(outcome.summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
