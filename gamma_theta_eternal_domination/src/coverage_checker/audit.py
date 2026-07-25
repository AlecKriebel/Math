"""Streaming independent audit of a completed extension-search ledger.

No code in this module imports ``search.extension_killtest``, verifier A, or
verifier B.  The search database is opened immutable/read-only.  A separate
SQLite state file checkpoints independently reconstructed origin counts so a
110,537-origin audit can resume after interruption.
"""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from hashlib import sha256
from itertools import zip_longest
import json
import math
import os
from pathlib import Path, PurePosixPath
import platform
import re
import resource
import sqlite3
import tempfile
import time
from typing import Iterable, Iterator, Mapping, Sequence

from .catalog import (
    HostRecord,
    PRODUCTION_POLICY,
    UniversePolicy,
    load_host_universe,
    sha256_file,
)
from .graph import Graph, Graph6Error, find_isomorphism


SEARCH_SCHEMA_VERSION = 1
AUDIT_STATE_SCHEMA_VERSION = 1
AUDIT_FORMAT = "gamma-theta-extension-postrun-audit-v1"
ORIGIN_CHAIN_DOMAIN = b"gamma-theta-extension-origin-chain-v1\0"
EMPTY_SHA256 = sha256(b"").hexdigest()
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")

PINNED_LABELG_SHA256 = (
    "ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0"
)
PINNED_NAUTY_ARCHIVE_SHA256 = (
    "9fc4edae04f88a0f5883985be3b39cf7f898fd6cc96e96b9ee25452743cc1b5b"
)
SEARCH_RUNTIME_PATHS = (
    "src/search/extension_killtest.py",
    "src/search/private_obstruction.py",
    "src/verifier_a/core.py",
    "src/verifier_b/__init__.py",
    "src/verifier_b/graph.py",
    "src/verifier_b/invariants.py",
    "src/verifier_b/eternal.py",
)
CHECKER_SOURCE_PATHS = (
    "src/coverage_checker/__init__.py",
    "src/coverage_checker/graph.py",
    "src/coverage_checker/catalog.py",
    "src/coverage_checker/audit.py",
    "src/coverage_checker/cli.py",
)
CONFIGURATION_KEYS = frozenset(
    {
        "catalog_path",
        "catalog_sha256",
        "parameters_path",
        "parameters_sha256",
        "labelg_path",
        "labelg_sha256",
        "nauty_archive_sha256",
        "engine_sha256",
        "runtime_source_manifest",
        "runtime_source_set_sha256",
        "python_implementation",
        "python_version",
        "python_executable",
        "batch_size",
        "active_host_ids",
        "wall_limit_seconds",
        "memory_limit_mib",
        "target_guard_count",
        "schema_version",
    }
)
PROVENANCE_HEADER = (
    "host_id",
    "neighborhood_mask",
    "neighborhood_size",
    "raw_graph6",
    "canonical_graph6",
    "gamma_delta",
    "alpha_delta",
    "category",
)
UNIQUE_HEADER = (
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
SEARCH_TABLE_COLUMNS = {
    "metadata": ("key", "value"),
    "hosts": (
        "host_index",
        "catalog_id",
        "n",
        "graph6",
        "gamma",
        "alpha",
        "gamma_infinity",
        "theta",
        "raw_expected",
        "next_mask",
        "status",
        "canonical_stream_sha256",
    ),
    "canonical_graphs": (
        "graph6",
        "n",
        "m",
        "first_host_id",
        "first_neighborhood_mask",
        "first_raw_graph6",
        "origin_count",
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
    ),
    "origins": (
        "host_id",
        "neighborhood_mask",
        "neighborhood_size",
        "raw_graph6",
        "canonical_graph6",
        "gamma_delta",
        "alpha_delta",
        "category",
    ),
}
STATE_TABLE_COLUMNS = {
    "metadata": ("key", "value"),
    "progress": (
        "singleton",
        "status",
        "last_host_index",
        "last_mask",
        "verified_origins",
        "origin_chain_sha256",
    ),
    "canonical_counts": (
        "graph6",
        "origin_count",
        "first_host_index",
        "first_host_id",
        "first_neighborhood_mask",
        "first_raw_graph6",
    ),
    "origin_receipts": (
        "host_index",
        "host_id",
        "neighborhood_mask",
        "raw_graph6",
        "canonical_graph6",
        "mapping_json",
        "chain_sha256",
    ),
}


class AuditError(RuntimeError):
    """A post-run artifact failed a strict coverage or binding check."""


@dataclass(frozen=True, slots=True)
class AuditPolicy:
    universe: UniversePolicy = PRODUCTION_POLICY
    labelg_sha256: str = PINNED_LABELG_SHA256
    nauty_archive_sha256: str = PINNED_NAUTY_ARCHIVE_SHA256
    runtime_source_paths: tuple[str, ...] = SEARCH_RUNTIME_PATHS


PRODUCTION_AUDIT_POLICY = AuditPolicy()


@dataclass(frozen=True, slots=True)
class AuditPaths:
    campaign_root: Path
    catalog: Path
    parameters: Path
    database: Path
    checkpoint: Path
    provenance_csv: Path
    unique_csv: Path
    state_database: Path
    report: Path


@dataclass(frozen=True, slots=True)
class AuditOutcome:
    status: str
    verified_origins: int
    expected_origins: int
    unique_canonical_graphs: int | None
    report_path: str
    origin_chain_sha256: str


def _strict_json_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if not isinstance(key, str) or key in result:
            raise AuditError(f"duplicate or non-string JSON object key: {key!r}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> object:
    raise AuditError(f"non-finite JSON constant: {value}")


def strict_json_loads(text: str, label: str) -> object:
    try:
        return json.loads(
            text,
            object_pairs_hook=_strict_json_pairs,
            parse_constant=_reject_json_constant,
        )
    except (json.JSONDecodeError, UnicodeError, RecursionError) as error:
        raise AuditError(f"invalid JSON in {label}: {error}") from error


def strict_json_file(path: Path) -> object:
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise AuditError(f"cannot read JSON {path}: {error}") from error
    try:
        text = raw.decode("utf-8")
    except UnicodeError as error:
        raise AuditError(f"JSON is not UTF-8: {path}") from error
    return strict_json_loads(text, str(path))


def _canonical_json(value: object) -> bytes:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
    except (TypeError, ValueError, RecursionError) as error:
        raise AuditError(f"value is not canonical-JSON serializable: {error}") from error


def _json_sha256(value: object) -> str:
    return sha256(_canonical_json(value)).hexdigest()


def _require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or SHA256_PATTERN.fullmatch(value) is None:
        raise AuditError(f"{label} is not a lowercase SHA-256 digest")
    return value


def _require_exact_int(value: object, label: str, *, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise AuditError(f"{label} is not an integer")
    if minimum is not None and value < minimum:
        raise AuditError(f"{label} is below {minimum}")
    return value


def _require_positive_finite(value: object, label: str) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value <= 0
    ):
        raise AuditError(f"{label} is not a positive finite number")
    return float(value)


def _require_mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise AuditError(f"{label} is not a JSON object")
    return value


def _resolve(path: Path) -> Path:
    try:
        return path.expanduser().resolve()
    except OSError as error:
        raise AuditError(f"cannot resolve {path}: {error}") from error


def _regular_file(path: Path, label: str) -> Path:
    resolved = _resolve(path)
    if not resolved.is_file():
        raise AuditError(f"{label} is not a regular file: {resolved}")
    return resolved


def _validate_path_roles(paths: AuditPaths) -> AuditPaths:
    resolved = AuditPaths(**{field: _resolve(getattr(paths, field)) for field in asdict(paths)})
    read_roles = {
        "catalog": resolved.catalog,
        "parameters": resolved.parameters,
        "database": resolved.database,
        "checkpoint": resolved.checkpoint,
        "provenance": resolved.provenance_csv,
        "unique": resolved.unique_csv,
    }
    write_roles = {
        "audit state": resolved.state_database,
        "report": resolved.report,
    }
    all_roles = {**read_roles, **write_roles}
    reverse: dict[Path, list[str]] = {}
    for role, path in all_roles.items():
        reverse.setdefault(path, []).append(role)
    collisions = {
        path: roles for path, roles in reverse.items() if len(roles) > 1
    }
    if collisions:
        raise AuditError(f"audit path roles alias: {collisions!r}")
    for role, path in read_roles.items():
        _regular_file(path, role)
    trusted_sources = {
        _resolve(
            resolved.campaign_root / Path(*PurePosixPath(relative).parts)
        )
        for relative in CHECKER_SOURCE_PATHS + SEARCH_RUNTIME_PATHS
    }
    for role, path in write_roles.items():
        if path in trusted_sources:
            raise AuditError(f"{role} aliases a trusted source file: {path}")
    return resolved


def _rss_mib() -> float:
    raw = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return raw / (1024 * 1024) if platform.system() == "Darwin" else raw / 1024


def _atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".partial", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(
                json.dumps(
                    value,
                    indent=2,
                    sort_keys=True,
                    ensure_ascii=True,
                    allow_nan=False,
                ).encode("ascii")
            )
            handle.write(b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _source_manifest(
    campaign_root: Path, relative_paths: Sequence[str]
) -> tuple[tuple[str, str], ...]:
    root = _resolve(campaign_root)
    records: list[tuple[str, str]] = []
    seen: set[str] = set()
    for relative in relative_paths:
        if not isinstance(relative, str) or relative in seen:
            raise AuditError(f"duplicate/non-string source path: {relative!r}")
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts or "." in pure.parts:
            raise AuditError(f"unsafe source path: {relative!r}")
        seen.add(relative)
        path = _regular_file(root / Path(*pure.parts), f"source {relative}")
        try:
            path.relative_to(root)
        except ValueError as error:
            raise AuditError(f"source escapes campaign root: {relative}") from error
        records.append((relative, sha256_file(path)))
    return tuple(records)


def _manifest_sha256(manifest: Sequence[tuple[str, str]]) -> str:
    digest = sha256()
    for relative, source_hash in manifest:
        digest.update(f"{relative} {source_hash}\n".encode("ascii"))
    return digest.hexdigest()


def _reject_live_sqlite_companions(database_path: Path) -> None:
    """Require a quiescent single-file DELETE-journal checkpoint."""

    for suffix in ("-wal", "-shm", "-journal"):
        companion = Path(str(database_path) + suffix)
        if companion.exists():
            raise AuditError(
                f"live SQLite companion prevents immutable audit: {companion}"
            )


def _open_immutable_database(database_path: Path) -> sqlite3.Connection:
    _reject_live_sqlite_companions(database_path)
    uri = database_path.as_uri() + "?mode=ro&immutable=1"
    connection: sqlite3.Connection | None = None
    try:
        connection = sqlite3.connect(uri, uri=True)
        connection.execute("PRAGMA query_only = ON")
    except sqlite3.Error as error:
        if connection is not None:
            connection.close()
        raise AuditError(f"cannot open immutable search database: {error}") from error
    return connection


def _table_columns(
    connection: sqlite3.Connection, table: str
) -> tuple[str, ...]:
    try:
        return tuple(
            str(row[1])
            for row in connection.execute(f'PRAGMA table_info("{table}")')
        )
    except sqlite3.Error as error:
        raise AuditError(f"cannot inspect table {table}: {error}") from error


def _validate_exact_tables(
    connection: sqlite3.Connection,
    expected: Mapping[str, tuple[str, ...]],
    *,
    label: str,
) -> None:
    try:
        actual_tables = tuple(
            str(row[0])
            for row in connection.execute(
                """
                SELECT name FROM sqlite_master
                WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name
                """
            )
        )
    except sqlite3.Error as error:
        raise AuditError(f"cannot list {label} tables: {error}") from error
    if actual_tables != tuple(sorted(expected)):
        raise AuditError(
            f"{label} tables differ: {actual_tables!r} != "
            f"{tuple(sorted(expected))!r}"
        )
    for table, columns in expected.items():
        actual_columns = _table_columns(connection, table)
        if actual_columns != columns:
            raise AuditError(
                f"{label}.{table} columns differ: {actual_columns!r} != "
                f"{columns!r}"
            )


def _validate_search_schema(connection: sqlite3.Connection) -> None:
    try:
        version = connection.execute("PRAGMA user_version").fetchone()
        if version is None or type(version[0]) is not int:
            raise AuditError("search database has no integer schema version")
        if version[0] != SEARCH_SCHEMA_VERSION:
            raise AuditError(
                f"search schema version is {version[0]}, "
                f"expected {SEARCH_SCHEMA_VERSION}"
            )
        integrity = tuple(connection.execute("PRAGMA integrity_check"))
        if integrity != (("ok",),):
            raise AuditError(f"SQLite integrity check failed: {integrity!r}")
        foreign_errors = tuple(connection.execute("PRAGMA foreign_key_check"))
        if foreign_errors:
            raise AuditError(
                f"SQLite foreign-key check failed: {foreign_errors[:5]!r}"
            )
    except sqlite3.Error as error:
        raise AuditError(f"cannot validate search SQLite schema: {error}") from error
    _validate_exact_tables(
        connection, SEARCH_TABLE_COLUMNS, label="search database"
    )


def _read_metadata(connection: sqlite3.Connection) -> dict[str, str]:
    try:
        rows = tuple(connection.execute("SELECT key, value FROM metadata"))
    except sqlite3.Error as error:
        raise AuditError(f"cannot read search metadata: {error}") from error
    metadata: dict[str, str] = {}
    for key, value in rows:
        if not isinstance(key, str) or not isinstance(value, str) or key in metadata:
            raise AuditError("search metadata has duplicate or non-text fields")
        metadata[key] = value
    expected = {
        "configuration_json",
        "configuration_sha256",
        "candidate_frozen_path",
    }
    if set(metadata) != expected:
        raise AuditError(
            f"search metadata keys differ: {set(metadata)!r} != {expected!r}"
        )
    if metadata["candidate_frozen_path"] != "":
        raise AuditError("completed negative audit cannot have a candidate marker")
    return metadata


def _configuration_from_metadata(
    metadata: Mapping[str, str],
    *,
    paths: AuditPaths,
    policy: AuditPolicy,
) -> tuple[dict[str, object], str]:
    parsed = strict_json_loads(
        metadata["configuration_json"], "database configuration_json"
    )
    configuration = _require_mapping(parsed, "database configuration")
    if set(configuration) != CONFIGURATION_KEYS:
        raise AuditError(
            "configuration key set differs: "
            f"{set(configuration)!r} != {CONFIGURATION_KEYS!r}"
        )
    digest = _json_sha256(configuration)
    stored_digest = _require_sha256(
        metadata["configuration_sha256"], "metadata configuration SHA-256"
    )
    if digest != stored_digest:
        raise AuditError(
            f"configuration digest mismatch: {digest} != {stored_digest}"
        )

    expected_path_bindings = {
        "catalog_path": paths.catalog,
        "parameters_path": paths.parameters,
    }
    for key, expected_path in expected_path_bindings.items():
        value = configuration[key]
        if not isinstance(value, str) or _resolve(Path(value)) != expected_path:
            raise AuditError(
                f"configuration {key} does not bind supplied path "
                f"{expected_path}"
            )
    catalog_hash = sha256_file(paths.catalog)
    parameter_hash = sha256_file(paths.parameters)
    if configuration["catalog_sha256"] != catalog_hash:
        raise AuditError("configuration catalog hash does not bind catalog bytes")
    if configuration["parameters_sha256"] != parameter_hash:
        raise AuditError(
            "configuration parameter hash does not bind parameter bytes"
        )
    if catalog_hash != policy.universe.catalog_sha256:
        raise AuditError("configuration uses an unrecognized catalog")
    if parameter_hash != policy.universe.parameters_sha256:
        raise AuditError("configuration uses an unrecognized parameter table")

    labelg_value = configuration["labelg_path"]
    if not isinstance(labelg_value, str):
        raise AuditError("configuration labelg_path is not text")
    labelg_path = _regular_file(Path(labelg_value), "configured labelg")
    labelg_hash = sha256_file(labelg_path)
    if (
        configuration["labelg_sha256"] != labelg_hash
        or labelg_hash != policy.labelg_sha256
    ):
        raise AuditError("configured labelg does not match its independent pin")
    archive_path = labelg_path.parent.parent / "nauty2_9_3.tar.gz"
    archive_hash = sha256_file(_regular_file(archive_path, "nauty archive"))
    if (
        configuration["nauty_archive_sha256"] != archive_hash
        or archive_hash != policy.nauty_archive_sha256
    ):
        raise AuditError("configured nauty archive does not match its pin")

    raw_manifest = configuration["runtime_source_manifest"]
    if not isinstance(raw_manifest, list):
        raise AuditError("runtime_source_manifest is not an array")
    stored_manifest: list[tuple[str, str]] = []
    for index, item in enumerate(raw_manifest):
        if (
            not isinstance(item, list)
            or len(item) != 2
            or not isinstance(item[0], str)
        ):
            raise AuditError(f"malformed runtime manifest record {index}")
        stored_manifest.append(
            (item[0], _require_sha256(item[1], f"runtime manifest hash {index}"))
        )
    actual_manifest = _source_manifest(
        paths.campaign_root, policy.runtime_source_paths
    )
    if tuple(stored_manifest) != actual_manifest:
        raise AuditError(
            "runtime source manifest differs from current bound source bytes"
        )
    manifest_digest = _manifest_sha256(stored_manifest)
    if configuration["runtime_source_set_sha256"] != manifest_digest:
        raise AuditError("runtime source-set digest mismatch")
    source_hashes = dict(stored_manifest)
    engine_path = "src/search/extension_killtest.py"
    if (
        engine_path not in source_hashes
        or configuration["engine_sha256"] != source_hashes[engine_path]
    ):
        raise AuditError("engine hash is not bound to the runtime manifest")

    if _require_exact_int(
        configuration["schema_version"], "configuration schema_version"
    ) != SEARCH_SCHEMA_VERSION:
        raise AuditError("configuration schema_version is not one")
    if _require_exact_int(
        configuration["target_guard_count"],
        "configuration target_guard_count",
    ) != policy.universe.target_guard_count:
        raise AuditError("configuration target guard count differs")
    _require_exact_int(
        configuration["batch_size"], "configuration batch_size", minimum=1
    )
    _require_positive_finite(
        configuration["wall_limit_seconds"],
        "configuration wall_limit_seconds",
    )
    _require_positive_finite(
        configuration["memory_limit_mib"],
        "configuration memory_limit_mib",
    )
    if configuration["active_host_ids"] != []:
        raise AuditError("configuration is a host shard, not the full universe")
    for key in (
        "python_implementation",
        "python_version",
        "python_executable",
    ):
        if not isinstance(configuration[key], str) or not configuration[key]:
            raise AuditError(f"configuration {key} is empty or non-text")
    if not _resolve(Path(str(configuration["python_executable"]))).is_file():
        raise AuditError("configured Python executable is no longer present")
    trusted_runtime_paths = {
        _resolve(paths.campaign_root / Path(*PurePosixPath(relative).parts))
        for relative, _source_hash in stored_manifest
    }
    trusted_runtime_paths.update(
        {
            labelg_path,
            _resolve(archive_path),
            _resolve(Path(str(configuration["python_executable"]))),
        }
    )
    for role, writable in (
        ("audit state", paths.state_database),
        ("report", paths.report),
    ):
        if writable in trusted_runtime_paths:
            raise AuditError(
                f"{role} aliases a configured runtime artifact: {writable}"
            )
    return configuration, digest


def _validate_checkpoint(
    checkpoint: object,
    *,
    configuration: Mapping[str, object],
    configuration_digest: str,
    paths: AuditPaths,
    database_sha256: str,
    policy: AuditPolicy,
) -> dict[str, object]:
    payload = _require_mapping(checkpoint, "checkpoint")
    if payload.get("status") != "complete":
        raise AuditError("checkpoint status is not complete")
    if payload.get("configuration_sha256") != configuration_digest:
        raise AuditError("checkpoint configuration digest mismatch")
    if payload.get("configuration") != configuration:
        raise AuditError("checkpoint configuration object differs from database")
    if payload.get("database_sha256") != database_sha256:
        raise AuditError("checkpoint database hash differs from immutable bytes")
    database_name = payload.get("database")
    if (
        not isinstance(database_name, str)
        or _resolve(Path(database_name)) != paths.database
    ):
        raise AuditError("checkpoint database path binding differs")
    if _require_exact_int(
        payload.get("raw_expected"), "checkpoint raw_expected"
    ) != policy.universe.raw_origins:
        raise AuditError("checkpoint raw_expected differs")
    if _require_exact_int(
        payload.get("raw_processed"), "checkpoint raw_processed"
    ) != policy.universe.raw_origins:
        raise AuditError("checkpoint raw_processed differs")
    if _require_exact_int(
        payload.get("hosts_complete"), "checkpoint hosts_complete"
    ) != policy.universe.selected_hosts:
        raise AuditError("checkpoint hosts_complete differs")
    candidate_state = _require_mapping(
        payload.get("candidate_state"), "checkpoint candidate_state"
    )
    if candidate_state.get("pending") is not False:
        raise AuditError("checkpoint has pending candidate state")
    if payload.get("candidate_path") is not None:
        raise AuditError("checkpoint has a candidate path")
    coverage = _require_mapping(
        payload.get("coverage_audit"), "checkpoint coverage_audit"
    )
    if coverage.get("passed") is not True or coverage.get("errors") != []:
        raise AuditError("search's internal coverage audit did not pass cleanly")
    coverage_counts = (
        _require_exact_int(
            coverage.get("raw_expected"), "coverage raw_expected"
        ),
        _require_exact_int(
            coverage.get("raw_origins"), "coverage raw_origins"
        ),
        _require_exact_int(
            coverage.get("stored_origin_multiplicity"),
            "coverage stored_origin_multiplicity",
        ),
    )
    if coverage_counts != (policy.universe.raw_origins,) * 3:
        raise AuditError("checkpoint internal coverage totals differ")

    expected_exports = {
        str(paths.provenance_csv): sha256_file(paths.provenance_csv),
        str(paths.unique_csv): sha256_file(paths.unique_csv),
    }
    output_hashes = _require_mapping(
        payload.get("output_sha256"), "checkpoint output_sha256"
    )
    if output_hashes != expected_exports:
        raise AuditError(
            f"checkpoint export hashes differ: {output_hashes!r} != "
            f"{expected_exports!r}"
        )
    return payload


def _validate_database_hosts(
    connection: sqlite3.Connection, hosts: Sequence[HostRecord]
) -> None:
    try:
        rows = tuple(
            connection.execute(
                """
                SELECT host_index, catalog_id, n, graph6, gamma, alpha,
                       gamma_infinity, theta, raw_expected, next_mask,
                       status, canonical_stream_sha256
                FROM hosts ORDER BY host_index
                """
            )
        )
    except sqlite3.Error as error:
        raise AuditError(f"cannot read database hosts: {error}") from error
    if len(rows) != len(hosts):
        raise AuditError(
            f"database has {len(rows)} hosts, expected {len(hosts)}"
        )
    for expected, row in zip(hosts, rows, strict=True):
        fixed = row[:11]
        expected_fixed = (
            expected.index,
            expected.catalog_id,
            expected.order,
            expected.graph6,
            expected.gamma,
            expected.alpha,
            expected.gamma_infinity,
            expected.theta,
            expected.raw_expected,
            expected.raw_expected + 1,
            "complete",
        )
        if fixed != expected_fixed:
            raise AuditError(
                f"database host row differs for {expected.catalog_id}: "
                f"{fixed!r} != {expected_fixed!r}"
            )
        _require_sha256(
            row[11], f"{expected.catalog_id} canonical stream SHA-256"
        )
    expected_origins = sum(host.raw_expected for host in hosts)
    origin_count = connection.execute(
        "SELECT COUNT(*) FROM origins"
    ).fetchone()
    if (
        origin_count is None
        or type(origin_count[0]) is not int
        or origin_count[0] != expected_origins
    ):
        raise AuditError(
            f"database has "
            f"{None if origin_count is None else origin_count[0]} origins, "
            f"expected {expected_origins}"
        )
    candidate_count = connection.execute(
        """
        SELECT
          (SELECT COUNT(*) FROM canonical_graphs
           WHERE category = 'candidate_eternal_3')
          +
          (SELECT COUNT(*) FROM origins
           WHERE category = 'candidate_eternal_3')
        """
    ).fetchone()
    if candidate_count is None or candidate_count[0] != 0:
        raise AuditError("completed database contains a candidate row")


def _audit_binding(
    *,
    paths: AuditPaths,
    policy: AuditPolicy,
    configuration_digest: str,
    database_sha256: str,
) -> tuple[dict[str, object], str]:
    checker_manifest = _source_manifest(
        paths.campaign_root, CHECKER_SOURCE_PATHS
    )
    binding: dict[str, object] = {
        "format": AUDIT_FORMAT,
        "audit_state_schema_version": AUDIT_STATE_SCHEMA_VERSION,
        "database_path": str(paths.database),
        "database_sha256": database_sha256,
        "checkpoint_path": str(paths.checkpoint),
        "checkpoint_sha256": sha256_file(paths.checkpoint),
        "catalog_path": str(paths.catalog),
        "catalog_sha256": sha256_file(paths.catalog),
        "parameters_path": str(paths.parameters),
        "parameters_sha256": sha256_file(paths.parameters),
        "provenance_path": str(paths.provenance_csv),
        "provenance_sha256": sha256_file(paths.provenance_csv),
        "unique_path": str(paths.unique_csv),
        "unique_sha256": sha256_file(paths.unique_csv),
        "configuration_sha256": configuration_digest,
        "expected_hosts": policy.universe.selected_hosts,
        "expected_origins": policy.universe.raw_origins,
        "checker_source_manifest": [list(item) for item in checker_manifest],
        "checker_source_set_sha256": _manifest_sha256(checker_manifest),
    }
    return binding, _json_sha256(binding)


def _initialize_or_open_state(
    state_path: Path,
    *,
    binding: Mapping[str, object],
    binding_digest: str,
) -> sqlite3.Connection:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        connection = sqlite3.connect(state_path)
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = DELETE")
        connection.execute("PRAGMA synchronous = FULL")
        version = connection.execute("PRAGMA user_version").fetchone()[0]
    except sqlite3.Error as error:
        raise AuditError(f"cannot open audit state database: {error}") from error
    if version == 0:
        try:
            connection.executescript(
                """
                BEGIN IMMEDIATE;
                CREATE TABLE metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE progress (
                    singleton INTEGER PRIMARY KEY CHECK(singleton = 1),
                    status TEXT NOT NULL,
                    last_host_index INTEGER NOT NULL,
                    last_mask INTEGER NOT NULL,
                    verified_origins INTEGER NOT NULL,
                    origin_chain_sha256 TEXT NOT NULL
                );
                CREATE TABLE canonical_counts (
                    graph6 TEXT PRIMARY KEY,
                    origin_count INTEGER NOT NULL,
                    first_host_index INTEGER NOT NULL,
                    first_host_id TEXT NOT NULL,
                    first_neighborhood_mask INTEGER NOT NULL,
                    first_raw_graph6 TEXT NOT NULL
                );
                CREATE TABLE origin_receipts (
                    host_index INTEGER NOT NULL,
                    host_id TEXT NOT NULL,
                    neighborhood_mask INTEGER NOT NULL,
                    raw_graph6 TEXT NOT NULL,
                    canonical_graph6 TEXT NOT NULL,
                    mapping_json TEXT NOT NULL,
                    chain_sha256 TEXT NOT NULL,
                    PRIMARY KEY(host_index, neighborhood_mask)
                );
                """
            )
            connection.execute(
                "INSERT INTO metadata(key, value) VALUES (?, ?)",
                (
                    "binding_json",
                    json.dumps(binding, sort_keys=True, ensure_ascii=True),
                ),
            )
            connection.execute(
                "INSERT INTO metadata(key, value) VALUES (?, ?)",
                ("binding_sha256", binding_digest),
            )
            connection.execute(
                """
                INSERT INTO progress(
                    singleton, status, last_host_index, last_mask,
                    verified_origins, origin_chain_sha256
                ) VALUES (1, 'origins_pending', -1, 0, 0, ?)
                """,
                (sha256(ORIGIN_CHAIN_DOMAIN).hexdigest(),),
            )
            connection.execute(
                f"PRAGMA user_version = {AUDIT_STATE_SCHEMA_VERSION}"
            )
            connection.commit()
        except BaseException:
            connection.rollback()
            connection.close()
            raise
    elif version != AUDIT_STATE_SCHEMA_VERSION:
        connection.close()
        raise AuditError(
            f"audit state version is {version}, "
            f"expected {AUDIT_STATE_SCHEMA_VERSION}"
        )
    try:
        _validate_exact_tables(
            connection, STATE_TABLE_COLUMNS, label="audit state"
        )
        metadata_rows = tuple(
            connection.execute("SELECT key, value FROM metadata ORDER BY key")
        )
        if tuple(key for key, _ in metadata_rows) != (
            "binding_json",
            "binding_sha256",
        ):
            raise AuditError("audit state metadata keys differ")
        metadata = {str(key): str(value) for key, value in metadata_rows}
        stored_binding = strict_json_loads(
            metadata["binding_json"], "audit state binding_json"
        )
        if stored_binding != binding:
            raise AuditError("audit state is bound to different input artifacts")
        if (
            metadata["binding_sha256"] != binding_digest
            or _json_sha256(stored_binding) != binding_digest
        ):
            raise AuditError("audit state binding digest mismatch")
        return connection
    except BaseException:
        connection.close()
        raise


def _progress(
    state: sqlite3.Connection,
) -> tuple[str, int, int, int, str]:
    row = state.execute(
        """
        SELECT status, last_host_index, last_mask, verified_origins,
               origin_chain_sha256
        FROM progress WHERE singleton = 1
        """
    ).fetchone()
    if row is None or len(row) != 5:
        raise AuditError("audit state has no unique progress row")
    status, host_index, mask, count, chain = row
    if status not in ("origins_pending", "origins_complete", "complete"):
        raise AuditError(f"unknown audit progress status: {status!r}")
    if (
        not isinstance(status, str)
        or type(host_index) is not int
        or type(mask) is not int
        or type(count) is not int
    ):
        raise AuditError("audit progress has invalid SQLite types")
    chain = _require_sha256(chain, "audit origin chain")
    return status, host_index, mask, count, chain


def _expected_count_at_position(
    hosts: Sequence[HostRecord], last_host_index: int, last_mask: int
) -> int:
    if last_host_index == -1:
        if last_mask != 0:
            raise AuditError("initial audit position has nonzero mask")
        return 0
    if not 0 <= last_host_index < len(hosts):
        raise AuditError("audit progress host index is out of range")
    host = hosts[last_host_index]
    if not 1 <= last_mask <= host.raw_expected:
        raise AuditError("audit progress mask is out of range")
    return (
        sum(item.raw_expected for item in hosts[:last_host_index])
        + last_mask
    )


def _validate_state_consistency(
    state: sqlite3.Connection, hosts: Sequence[HostRecord]
) -> tuple[str, int, int, int, str]:
    progress = _progress(state)
    status, host_index, mask, count, chain = progress
    expected_count = _expected_count_at_position(hosts, host_index, mask)
    if count != expected_count:
        raise AuditError(
            f"audit progress count {count} differs from position "
            f"count {expected_count}"
        )
    totals = state.execute(
        """
        SELECT COALESCE(SUM(origin_count), 0), COUNT(*),
               COALESCE(MIN(origin_count), 0)
        FROM canonical_counts
        """
    ).fetchone()
    if (
        totals is None
        or type(totals[0]) is not int
        or totals[0] != count
        or (totals[1] and totals[2] < 1)
    ):
        raise AuditError("audit canonical-count checkpoint is inconsistent")
    receipt_count = state.execute(
        "SELECT COUNT(*) FROM origin_receipts"
    ).fetchone()
    if receipt_count is None or receipt_count[0] != count:
        raise AuditError("audit receipt count differs from progress")
    bad_count_rows = state.execute(
        """
        SELECT COUNT(*) FROM (
            SELECT c.graph6
            FROM canonical_counts AS c
            LEFT JOIN origin_receipts AS r
              ON r.canonical_graph6 = c.graph6
            GROUP BY c.graph6
            HAVING c.origin_count != COUNT(r.canonical_graph6)
        )
        """
    ).fetchone()
    extra_receipt_keys = state.execute(
        """
        SELECT COUNT(*) FROM (
            SELECT DISTINCT r.canonical_graph6
            FROM origin_receipts AS r
            LEFT JOIN canonical_counts AS c ON c.graph6 = r.canonical_graph6
            WHERE c.graph6 IS NULL
        )
        """
    ).fetchone()
    if (
        bad_count_rows is None
        or bad_count_rows[0] != 0
        or extra_receipt_keys is None
        or extra_receipt_keys[0] != 0
    ):
        raise AuditError("audit receipt multiplicities differ from counts")
    if status in ("origins_complete", "complete") and count != sum(
        host.raw_expected for host in hosts
    ):
        raise AuditError("audit state claims completion before the final origin")
    return progress


def _next_position(
    hosts: Sequence[HostRecord], host_index: int, mask: int
) -> tuple[int, int] | None:
    if host_index == -1:
        return (0, 1) if hosts else None
    host = hosts[host_index]
    if mask < host.raw_expected:
        return host_index, mask + 1
    if host_index + 1 < len(hosts):
        return host_index + 1, 1
    return None


def _origin_chain_step(previous_hex: str, payload: object) -> str:
    return sha256(
        bytes.fromhex(previous_hex) + b"\0" + _canonical_json(payload)
    ).hexdigest()


def _origin_rows_after(
    connection: sqlite3.Connection, host_index: int, mask: int
) -> Iterator[tuple[object, ...]]:
    try:
        cursor = connection.execute(
            """
            SELECT h.host_index, o.host_id, o.neighborhood_mask,
                   o.neighborhood_size, o.raw_graph6, o.canonical_graph6,
                   o.gamma_delta, o.alpha_delta, o.category,
                   g.gamma, g.alpha, g.category
            FROM origins AS o
            JOIN hosts AS h ON h.catalog_id = o.host_id
            JOIN canonical_graphs AS g ON g.graph6 = o.canonical_graph6
            WHERE h.host_index > ?
               OR (h.host_index = ? AND o.neighborhood_mask > ?)
            ORDER BY h.host_index, o.neighborhood_mask
            """,
            (host_index, host_index, mask),
        )
    except sqlite3.Error as error:
        raise AuditError(f"cannot stream origin ledger: {error}") from error
    try:
        while True:
            try:
                row = cursor.fetchone()
            except sqlite3.Error as error:
                raise AuditError(
                    f"cannot stream origin ledger: {error}"
                ) from error
            if row is None:
                break
            yield row
    finally:
        try:
            cursor.close()
        except sqlite3.Error:
            pass


def _require_sqlite_int(value: object, label: str) -> int:
    if type(value) is not int:
        raise AuditError(f"{label} is not stored as an SQLite integer")
    return value


def _require_sqlite_text(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise AuditError(f"{label} is not stored as SQLite text")
    return value


def _verify_origin(
    row: tuple[object, ...],
    *,
    host: HostRecord,
    expected_mask: int,
    recorded_mapping: tuple[int, ...] | None = None,
) -> tuple[str, str, tuple[int, ...], dict[str, object]]:
    if len(row) != 12:
        raise AuditError("origin query returned the wrong column count")
    host_index = _require_sqlite_int(row[0], "origin host_index")
    host_id = _require_sqlite_text(row[1], "origin host_id")
    mask = _require_sqlite_int(row[2], "origin neighborhood_mask")
    neighborhood_size = _require_sqlite_int(
        row[3], "origin neighborhood_size"
    )
    raw_graph6 = _require_sqlite_text(row[4], "origin raw_graph6")
    canonical_graph6 = _require_sqlite_text(
        row[5], "origin canonical_graph6"
    )
    gamma_delta = _require_sqlite_int(row[6], "origin gamma_delta")
    alpha_delta = _require_sqlite_int(row[7], "origin alpha_delta")
    origin_category = _require_sqlite_text(row[8], "origin category")
    canonical_gamma = _require_sqlite_int(row[9], "canonical gamma")
    canonical_alpha = _require_sqlite_int(row[10], "canonical alpha")
    canonical_category = _require_sqlite_text(row[11], "canonical category")

    if (
        host_index != host.index
        or host_id != host.catalog_id
        or mask != expected_mask
    ):
        raise AuditError(
            "origin sequence gap/reordering: "
            f"got {(host_index, host_id, mask)!r}, expected "
            f"{(host.index, host.catalog_id, expected_mask)!r}"
        )
    if not 1 <= mask <= host.raw_expected:
        raise AuditError(f"origin mask is out of range for {host.catalog_id}")
    if neighborhood_size != mask.bit_count():
        raise AuditError(
            f"origin neighborhood size differs at {host.catalog_id}/{mask}"
        )
    if origin_category != canonical_category:
        raise AuditError(
            f"origin/canonical category differs at {host.catalog_id}/{mask}"
        )
    if gamma_delta != canonical_gamma - host.gamma:
        raise AuditError(
            f"gamma delta differs at {host.catalog_id}/{mask}"
        )
    if alpha_delta != canonical_alpha - host.alpha:
        raise AuditError(
            f"alpha delta differs at {host.catalog_id}/{mask}"
        )

    try:
        expected_graph = host.graph.add_extension(mask)
        raw_graph = Graph.from_graph6(raw_graph6)
        canonical_graph = Graph.from_graph6(canonical_graph6)
    except (Graph6Error, ValueError, TypeError) as error:
        raise AuditError(
            f"malformed graph at {host.catalog_id}/{mask}: {error}"
        ) from error
    if expected_graph != raw_graph or expected_graph.to_graph6() != raw_graph6:
        raise AuditError(
            f"raw reconstruction differs at {host.catalog_id}/{mask}"
        )
    if raw_graph.order > 12 or canonical_graph.order > 12:
        raise AuditError("independent isomorphism checker is bounded to n <= 12")
    if (
        raw_graph.order != canonical_graph.order
        or raw_graph.size != canonical_graph.size
    ):
        raise AuditError(
            f"raw/canonical order or size differs at {host.catalog_id}/{mask}"
        )
    if canonical_graph.to_graph6() != canonical_graph6:
        raise AuditError(
            f"canonical graph6 is not strict headerless syntax at "
            f"{host.catalog_id}/{mask}"
        )
    if recorded_mapping is None:
        mapping = find_isomorphism(raw_graph, canonical_graph)
        if mapping is None:
            raise AuditError(
                f"raw/canonical pair is not isomorphic at "
                f"{host.catalog_id}/{mask}"
            )
    else:
        mapping = recorded_mapping
        if (
            len(mapping) != raw_graph.order
            or any(type(vertex) is not int for vertex in mapping)
            or set(mapping) != set(range(raw_graph.order))
            or raw_graph.relabel(mapping) != canonical_graph
        ):
            raise AuditError(
                f"stored isomorphism receipt is invalid at "
                f"{host.catalog_id}/{mask}"
            )
    if len(mapping) != raw_graph.order:
        raise AuditError("isomorphism backtracker returned a malformed mapping")
    chain_payload: dict[str, object] = {
        "host_index": host.index,
        "host_id": host.catalog_id,
        "neighborhood_mask": mask,
        "neighborhood_size": neighborhood_size,
        "raw_graph6": raw_graph6,
        "canonical_graph6": canonical_graph6,
        "gamma_delta": gamma_delta,
        "alpha_delta": alpha_delta,
        "category": origin_category,
        "raw_to_canonical_mapping": list(mapping),
    }
    return raw_graph6, canonical_graph6, mapping, chain_payload


def _record_verified_origin(
    state: sqlite3.Connection,
    *,
    host: HostRecord,
    mask: int,
    raw_graph6: str,
    canonical_graph6: str,
    mapping: tuple[int, ...],
    verified_count: int,
    origin_chain: str,
) -> None:
    state.execute(
        """
        INSERT INTO origin_receipts(
            host_index, host_id, neighborhood_mask, raw_graph6,
            canonical_graph6, mapping_json, chain_sha256
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            host.index,
            host.catalog_id,
            mask,
            raw_graph6,
            canonical_graph6,
            json.dumps(list(mapping), separators=(",", ":")),
            origin_chain,
        ),
    )
    state.execute(
        """
        INSERT INTO canonical_counts(
            graph6, origin_count, first_host_index, first_host_id,
            first_neighborhood_mask, first_raw_graph6
        ) VALUES (?, 1, ?, ?, ?, ?)
        ON CONFLICT(graph6) DO UPDATE SET
            origin_count = canonical_counts.origin_count + 1
        """,
        (
            canonical_graph6,
            host.index,
            host.catalog_id,
            mask,
            raw_graph6,
        ),
    )
    state.execute(
        """
        UPDATE progress
        SET status = 'origins_pending', last_host_index = ?, last_mask = ?,
            verified_origins = ?, origin_chain_sha256 = ?
        WHERE singleton = 1
        """,
        (host.index, mask, verified_count, origin_chain),
    )
    if state.execute("SELECT changes()").fetchone()[0] != 1:
        raise AuditError("audit progress update did not affect one row")


def _validate_prior_receipts(
    search: sqlite3.Connection,
    state: sqlite3.Connection,
    *,
    hosts: Sequence[HostRecord],
) -> None:
    """Cheaply replay stored mapping witnesses before trusting resume state."""

    _status, _last_host, _last_mask, verified, expected_chain = (
        _validate_state_consistency(state, hosts)
    )
    if verified == 0:
        if expected_chain != sha256(ORIGIN_CHAIN_DOMAIN).hexdigest():
            raise AuditError("empty audit state has a noninitial chain digest")
        return
    search_rows = _origin_rows_after(search, -1, 0)
    receipts = state.execute(
        """
        SELECT host_index, host_id, neighborhood_mask, raw_graph6,
               canonical_graph6, mapping_json, chain_sha256
        FROM origin_receipts
        ORDER BY host_index, neighborhood_mask
        """
    )
    expected_position: tuple[int, int] | None = (0, 1)
    chain = sha256(ORIGIN_CHAIN_DOMAIN).hexdigest()
    seen = 0
    try:
        for receipt in receipts:
            if expected_position is None:
                raise AuditError("audit state has receipts beyond the universe")
            try:
                database_row = next(search_rows)
            except StopIteration as error:
                raise AuditError(
                    "search ledger is shorter than audit receipt prefix"
                ) from error
            host_index, mask = expected_position
            host = hosts[host_index]
            receipt_host_index = _require_sqlite_int(
                receipt[0], "receipt host index"
            )
            receipt_host_id = _require_sqlite_text(
                receipt[1], "receipt host id"
            )
            receipt_mask = _require_sqlite_int(receipt[2], "receipt mask")
            receipt_raw = _require_sqlite_text(receipt[3], "receipt raw graph6")
            receipt_canonical = _require_sqlite_text(
                receipt[4], "receipt canonical graph6"
            )
            mapping_text = _require_sqlite_text(
                receipt[5], "receipt mapping JSON"
            )
            receipt_chain = _require_sha256(receipt[6], "receipt chain")
            if (
                receipt_host_index != host_index
                or receipt_host_id != host.catalog_id
                or receipt_mask != mask
            ):
                raise AuditError(
                    "audit receipt sequence has a gap or reordering"
                )
            mapping_value = strict_json_loads(
                mapping_text,
                f"receipt mapping {receipt_host_id}/{receipt_mask}",
            )
            if (
                not isinstance(mapping_value, list)
                or any(type(vertex) is not int for vertex in mapping_value)
                or _canonical_json(mapping_value).decode("ascii") != mapping_text
            ):
                raise AuditError("audit receipt mapping JSON is malformed")
            raw, canonical, _mapping, payload = _verify_origin(
                database_row,
                host=host,
                expected_mask=mask,
                recorded_mapping=tuple(mapping_value),
            )
            if raw != receipt_raw or canonical != receipt_canonical:
                raise AuditError("audit receipt graph records differ from ledger")
            chain = _origin_chain_step(chain, payload)
            if chain != receipt_chain:
                raise AuditError("audit receipt chain digest differs")
            seen += 1
            expected_position = _next_position(hosts, host_index, mask)
    finally:
        search_rows.close()
    if seen != verified or chain != expected_chain:
        raise AuditError("audit receipt prefix does not bind progress")

    bad_first = state.execute(
        """
        SELECT COUNT(*) FROM canonical_counts AS c
        WHERE
            NOT EXISTS (
                SELECT 1 FROM origin_receipts AS r
                WHERE r.canonical_graph6 = c.graph6
                  AND r.host_index = c.first_host_index
                  AND r.host_id = c.first_host_id
                  AND r.neighborhood_mask = c.first_neighborhood_mask
                  AND r.raw_graph6 = c.first_raw_graph6
            )
            OR EXISTS (
                SELECT 1 FROM origin_receipts AS earlier
                WHERE earlier.canonical_graph6 = c.graph6
                  AND (
                      earlier.host_index < c.first_host_index
                      OR (
                          earlier.host_index = c.first_host_index
                          AND earlier.neighborhood_mask
                              < c.first_neighborhood_mask
                      )
                  )
            )
        """
    )
    # The query above deliberately references no search-engine table.  Keep a
    # separate explicit check below because SQLite reports a missing receipt
    # as a normal count, not an integrity error.
    bad_first_row = bad_first.fetchone()
    if bad_first_row is None or bad_first_row[0] != 0:
        raise AuditError("audit canonical first-origin receipt differs")


def _audit_origins(
    search: sqlite3.Connection,
    state: sqlite3.Connection,
    *,
    hosts: Sequence[HostRecord],
    checkpoint_interval: int,
    max_new_origins: int | None,
    wall_limit_seconds: float,
    memory_limit_mib: float,
    started: float,
) -> tuple[str, int, str]:
    if type(checkpoint_interval) is not int or checkpoint_interval < 1:
        raise AuditError("checkpoint_interval must be a positive integer")
    if max_new_origins is not None and (
        type(max_new_origins) is not int or max_new_origins < 1
    ):
        raise AuditError("max_new_origins must be a positive integer or None")
    _require_positive_finite(wall_limit_seconds, "audit wall limit")
    _require_positive_finite(memory_limit_mib, "audit memory limit")

    status, last_host, last_mask, verified, chain = _validate_state_consistency(
        state, hosts
    )
    expected_total = sum(host.raw_expected for host in hosts)
    if status in ("origins_complete", "complete"):
        return status, verified, chain

    expected = _next_position(hosts, last_host, last_mask)
    newly_verified = 0
    since_commit = 0
    in_transaction = False
    try:
        for row in _origin_rows_after(search, last_host, last_mask):
            if expected is None:
                raise AuditError("origin ledger has records beyond full universe")
            expected_host_index, expected_mask = expected
            host = hosts[expected_host_index]
            if not in_transaction:
                state.execute("BEGIN IMMEDIATE")
                in_transaction = True
            raw, canonical, _mapping, payload = _verify_origin(
                row, host=host, expected_mask=expected_mask
            )
            verified += 1
            newly_verified += 1
            since_commit += 1
            chain = _origin_chain_step(chain, payload)
            _record_verified_origin(
                state,
                host=host,
                mask=expected_mask,
                raw_graph6=raw,
                canonical_graph6=canonical,
                mapping=_mapping,
                verified_count=verified,
                origin_chain=chain,
            )
            last_host, last_mask = expected
            expected = _next_position(hosts, last_host, last_mask)

            reached_batch = since_commit >= checkpoint_interval
            reached_limit = (
                max_new_origins is not None
                and newly_verified >= max_new_origins
            )
            resource_stop = (
                time.monotonic() - started >= wall_limit_seconds
                or _rss_mib() >= memory_limit_mib
            )
            if reached_batch or reached_limit or resource_stop:
                state.commit()
                in_transaction = False
                since_commit = 0
                _validate_state_consistency(state, hosts)
            if reached_limit or resource_stop:
                return "in_progress", verified, chain

        if in_transaction:
            state.commit()
            in_transaction = False
        if expected is not None:
            raise AuditError(
                "origin ledger ended before expected "
                f"{hosts[expected[0]].catalog_id}/{expected[1]}"
            )
        if verified != expected_total:
            raise AuditError(
                f"verified {verified} origins, expected {expected_total}"
            )
        state.execute(
            "UPDATE progress SET status = 'origins_complete' WHERE singleton = 1"
        )
        state.commit()
        _validate_state_consistency(state, hosts)
        return "origins_complete", verified, chain
    except BaseException:
        if in_transaction:
            state.rollback()
        raise


def _validate_optional_hash(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _require_sha256(value, label)


def _validate_evaluation_row(row: tuple[object, ...]) -> tuple[str, int]:
    if len(row) != len(UNIQUE_HEADER):
        raise AuditError("canonical evaluation query returned wrong width")
    graph6 = _require_sqlite_text(row[0], "canonical graph6")
    order = _require_sqlite_int(row[1], "canonical n")
    size = _require_sqlite_int(row[2], "canonical m")
    origin_count = _require_sqlite_int(row[3], "canonical origin_count")
    _require_sqlite_text(row[4], "canonical first_host_id")
    _require_sqlite_int(row[5], "canonical first_neighborhood_mask")
    _require_sqlite_text(row[6], "canonical first_raw_graph6")
    gamma = _require_sqlite_int(row[7], "canonical gamma")
    alpha = _require_sqlite_int(row[8], "canonical alpha")
    category = _require_sqlite_text(row[9], "canonical category")
    private = row[10]
    eternal_a = row[11]
    eternal_b = row[12]
    family_a_size = row[13]
    family_b_size = row[14]
    family_a_hash = _validate_optional_hash(row[15], "family A hash")
    family_b_hash = _validate_optional_hash(row[16], "family B hash")

    try:
        graph = Graph.from_graph6(graph6)
    except (Graph6Error, ValueError, TypeError) as error:
        raise AuditError(f"invalid canonical graph6 {graph6!r}: {error}") from error
    if (
        graph.order != order
        or graph.size != size
        or graph.to_graph6() != graph6
        or not 1 <= origin_count
    ):
        raise AuditError(f"canonical graph metadata differs for {graph6}")
    if graph.order > 12:
        raise AuditError("canonical graph exceeds checker order limit")
    optional_fields = (
        eternal_a,
        eternal_b,
        family_a_size,
        family_b_size,
        family_a_hash,
        family_b_hash,
    )
    if category == "gamma_below_3":
        if not (1 <= gamma < 3 and 3 <= alpha <= 4):
            raise AuditError(f"gamma_below_3 parameters differ for {graph6}")
        if private is not None or any(value is not None for value in optional_fields):
            raise AuditError(f"unevaluated gamma category has payload for {graph6}")
    elif category == "alpha_above_3":
        if gamma != 3 or alpha != 4:
            raise AuditError(f"alpha_above_3 parameters differ for {graph6}")
        if private is not None or any(value is not None for value in optional_fields):
            raise AuditError(f"unevaluated alpha category has payload for {graph6}")
    elif category in (
        "private_obstruction_eternal_false",
        "eternal_false_without_private_obstruction",
    ):
        if gamma != 3 or alpha != 3:
            raise AuditError(f"eternal-false parameters differ for {graph6}")
        if (
            eternal_a != 0
            or eternal_b != 0
            or family_a_size != 0
            or family_b_size != 0
            or family_a_hash != EMPTY_SHA256
            or family_b_hash != EMPTY_SHA256
        ):
            raise AuditError(f"eternal-false payload differs for {graph6}")
        if category == "private_obstruction_eternal_false":
            if not isinstance(private, str):
                raise AuditError(f"private obstruction is absent for {graph6}")
            parsed = strict_json_loads(private, f"private obstruction {graph6}")
            if _canonical_json(parsed).decode("ascii") != private:
                raise AuditError(
                    f"private obstruction JSON is not canonical for {graph6}"
                )
        elif private is not None:
            raise AuditError(f"unexpected private obstruction for {graph6}")
    elif category == "candidate_eternal_3":
        raise AuditError("completed negative database contains a candidate")
    else:
        raise AuditError(f"unknown canonical category {category!r}")
    return graph6, origin_count


def _canonical_rows(
    connection: sqlite3.Connection,
) -> Iterator[tuple[object, ...]]:
    yield from connection.execute(
        """
        SELECT graph6, n, m, origin_count, first_host_id,
               first_neighborhood_mask, first_raw_graph6, gamma, alpha,
               category, private_obstruction_json, eternal_a, eternal_b,
               family_a_size, family_b_size, family_a_sha256, family_b_sha256
        FROM canonical_graphs ORDER BY graph6
        """
    )


def _audit_canonical_evaluations(
    search: sqlite3.Connection,
    state: sqlite3.Connection,
    *,
    hosts: Sequence[HostRecord],
    expected_origins: int,
) -> tuple[int, int]:
    state_rows = state.execute(
        """
        SELECT graph6, origin_count, first_host_index, first_host_id,
               first_neighborhood_mask, first_raw_graph6
        FROM canonical_counts ORDER BY graph6
        """
    )
    sentinel = object()
    unique_count = 0
    multiplicity = 0
    for database_row, state_row in zip_longest(
        _canonical_rows(search), state_rows, fillvalue=sentinel
    ):
        if database_row is sentinel or state_row is sentinel:
            raise AuditError(
                "canonical evaluation keys differ from reconstructed keys"
            )
        if not isinstance(database_row, tuple) or not isinstance(
            state_row, tuple
        ):
            raise AuditError("canonical cursors returned malformed rows")
        graph6, origin_count = _validate_evaluation_row(database_row)
        state_graph6 = _require_sqlite_text(
            state_row[0], "state canonical graph6"
        )
        state_count = _require_sqlite_int(
            state_row[1], "state canonical origin_count"
        )
        state_first_index = _require_sqlite_int(
            state_row[2], "state first host index"
        )
        state_first_host = _require_sqlite_text(
            state_row[3], "state first host id"
        )
        state_first_mask = _require_sqlite_int(
            state_row[4], "state first mask"
        )
        state_first_raw = _require_sqlite_text(
            state_row[5], "state first raw graph6"
        )
        if graph6 != state_graph6 or origin_count != state_count:
            raise AuditError(f"canonical multiplicity differs for {graph6}")
        if (
            database_row[4] != state_first_host
            or database_row[5] != state_first_mask
            or database_row[6] != state_first_raw
        ):
            raise AuditError(
                f"first-evaluation provenance differs for {graph6}"
            )
        if (
            not 0 <= state_first_index < len(hosts)
            or hosts[state_first_index].catalog_id != state_first_host
        ):
            raise AuditError(f"first host index differs for {graph6}")
        unique_count += 1
        multiplicity += origin_count
    if multiplicity != expected_origins:
        raise AuditError(
            f"canonical multiplicities total {multiplicity}, "
            f"expected {expected_origins}"
        )
    return unique_count, multiplicity


def _audit_host_stream_hashes(
    search: sqlite3.Connection, hosts: Sequence[HostRecord]
) -> dict[str, str]:
    results: dict[str, str] = {}
    for host in hosts:
        digest = sha256()
        count = 0
        for row in search.execute(
            """
            SELECT canonical_graph6 FROM origins
            WHERE host_id = ? ORDER BY neighborhood_mask
            """,
            (host.catalog_id,),
        ):
            canonical = _require_sqlite_text(
                row[0], f"{host.catalog_id} canonical stream"
            )
            digest.update(canonical.encode("ascii") + b"\n")
            count += 1
        if count != host.raw_expected:
            raise AuditError(
                f"{host.catalog_id} stream has {count} records, "
                f"expected {host.raw_expected}"
            )
        calculated = digest.hexdigest()
        stored = search.execute(
            """
            SELECT canonical_stream_sha256 FROM hosts WHERE catalog_id = ?
            """,
            (host.catalog_id,),
        ).fetchone()
        if stored is None or stored[0] != calculated:
            raise AuditError(
                f"{host.catalog_id} canonical stream hash differs"
            )
        results[host.catalog_id] = calculated
    return results


def _csv_rows(path: Path, header: tuple[str, ...]) -> Iterator[tuple[str, ...]]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle, strict=True)
            try:
                actual = tuple(next(reader))
            except StopIteration as error:
                raise AuditError(f"empty CSV export: {path}") from error
            if actual != header:
                raise AuditError(
                    f"CSV header differs for {path}: {actual!r} != {header!r}"
                )
            for line_number, values in enumerate(reader, 2):
                if len(values) != len(header):
                    raise AuditError(
                        f"{path}:{line_number} has wrong field count"
                    )
                yield tuple(values)
    except (OSError, UnicodeError, csv.Error) as error:
        raise AuditError(f"cannot stream CSV {path}: {error}") from error


def _csv_value(value: object) -> str:
    if value is None:
        return ""
    if type(value) is int:
        return str(value)
    if isinstance(value, str):
        return value
    raise AuditError(f"database export value has unsupported type: {type(value)}")


def _compare_export(
    path: Path,
    header: tuple[str, ...],
    database_rows: Iterable[tuple[object, ...]],
) -> int:
    sentinel = object()
    count = 0
    for file_row, database_row in zip_longest(
        _csv_rows(path, header), database_rows, fillvalue=sentinel
    ):
        if file_row is sentinel or database_row is sentinel:
            raise AuditError(f"CSV row count differs from database: {path}")
        if not isinstance(file_row, tuple) or not isinstance(
            database_row, tuple
        ):
            raise AuditError("CSV/database cursor returned malformed rows")
        expected = tuple(_csv_value(value) for value in database_row)
        if file_row != expected:
            raise AuditError(
                f"CSV row {count + 2} differs from database in {path}"
            )
        count += 1
    return count


def _audit_exports(
    search: sqlite3.Connection,
    *,
    paths: AuditPaths,
    expected_origins: int,
    expected_unique: int,
) -> tuple[int, int]:
    provenance_rows = search.execute(
        """
        SELECT o.host_id, o.neighborhood_mask, o.neighborhood_size,
               o.raw_graph6, o.canonical_graph6, o.gamma_delta,
               o.alpha_delta, o.category
        FROM origins AS o
        JOIN hosts AS h ON h.catalog_id = o.host_id
        ORDER BY h.host_index, o.neighborhood_mask
        """
    )
    provenance_count = _compare_export(
        paths.provenance_csv, PROVENANCE_HEADER, provenance_rows
    )
    unique_rows = search.execute(
        """
        SELECT graph6, n, m, origin_count, first_host_id,
               first_neighborhood_mask, first_raw_graph6, gamma, alpha,
               category, private_obstruction_json, eternal_a, eternal_b,
               family_a_size, family_b_size, family_a_sha256, family_b_sha256
        FROM canonical_graphs ORDER BY n, graph6
        """
    )
    unique_count = _compare_export(
        paths.unique_csv, UNIQUE_HEADER, unique_rows
    )
    if provenance_count != expected_origins:
        raise AuditError(
            f"provenance export has {provenance_count} rows, "
            f"expected {expected_origins}"
        )
    if unique_count != expected_unique:
        raise AuditError(
            f"unique export has {unique_count} rows, expected {expected_unique}"
        )
    return provenance_count, unique_count


def _final_checkpoint_crosscheck(
    checkpoint: Mapping[str, object],
    *,
    unique_count: int,
    stream_hashes: Mapping[str, str],
    expected_origins: int,
) -> None:
    if _require_exact_int(
        checkpoint.get("unique_canonical_graphs"),
        "checkpoint unique_canonical_graphs",
    ) != unique_count:
        raise AuditError("checkpoint unique canonical count differs")
    coverage = _require_mapping(
        checkpoint.get("coverage_audit"), "checkpoint coverage_audit"
    )
    if _require_exact_int(
        coverage.get("bad_canonical_multiplicity_count"),
        "checkpoint bad multiplicity count",
    ) != 0:
        raise AuditError("checkpoint reports bad canonical multiplicities")
    if _require_exact_int(
        coverage.get("stored_origin_multiplicity"),
        "checkpoint stored multiplicity",
    ) != expected_origins:
        raise AuditError("checkpoint multiplicity total differs")
    if coverage.get("host_canonical_stream_sha256") != dict(stream_hashes):
        raise AuditError("checkpoint host stream-hash map differs")
    hosts_payload = checkpoint.get("hosts")
    if not isinstance(hosts_payload, list) or len(hosts_payload) != len(
        stream_hashes
    ):
        raise AuditError("checkpoint host summary has wrong shape")
    summarized_streams: dict[str, str] = {}
    for item in hosts_payload:
        row = _require_mapping(item, "checkpoint host summary row")
        identifier = row.get("catalog_id")
        stream_hash = row.get("canonical_stream_sha256")
        if (
            not isinstance(identifier, str)
            or identifier in summarized_streams
        ):
            raise AuditError("checkpoint host summaries repeat an identifier")
        summarized_streams[identifier] = _require_sha256(
            stream_hash, f"checkpoint host stream {identifier}"
        )
        raw_expected = _require_exact_int(
            row.get("raw_expected"), f"{identifier} raw_expected"
        )
        raw_processed = _require_exact_int(
            row.get("raw_processed"), f"{identifier} raw_processed"
        )
        next_mask = _require_exact_int(
            row.get("next_mask"), f"{identifier} next_mask"
        )
        if (
            row.get("status") != "complete"
            or raw_expected != raw_processed
            or next_mask != raw_expected + 1
        ):
            raise AuditError(f"checkpoint host summary incomplete: {identifier}")
    if summarized_streams != dict(stream_hashes):
        raise AuditError("checkpoint host summaries have different stream hashes")


def _report_payload(
    *,
    status: str,
    paths: AuditPaths,
    policy: AuditPolicy,
    binding: Mapping[str, object],
    binding_digest: str,
    configuration_digest: str,
    database_sha256: str,
    verified_origins: int,
    origin_chain_sha256: str,
    unique_count: int | None,
    started_unix: float,
    started_monotonic: float,
    stream_hashes: Mapping[str, str] | None = None,
) -> dict[str, object]:
    return {
        "format": AUDIT_FORMAT,
        "status": status,
        "passed": status == "complete",
        "warning": (
            "This checker certifies the delimited extension-search artifact "
            "only; it does not resolve the universal gamma-theta conjecture."
        ),
        "configuration_sha256": configuration_digest,
        "audit_binding_sha256": binding_digest,
        "audit_binding": dict(binding),
        "database_sha256": database_sha256,
        "state_database": str(paths.state_database),
        "state_database_sha256": sha256_file(paths.state_database),
        "expected_hosts": policy.universe.selected_hosts,
        "expected_origins": policy.universe.raw_origins,
        "verified_origins": verified_origins,
        "unique_canonical_graphs": unique_count,
        "origin_chain_sha256": origin_chain_sha256,
        "host_canonical_stream_sha256": (
            None if stream_hashes is None else dict(stream_hashes)
        ),
        "checker_limitations": [
            (
                "The exact isomorphism implementation accepts ordinary "
                "graph6 records only and is deliberately bounded to order 12."
            ),
            (
                "The ledger proves one stored evaluation row per canonical "
                "graph6 key; without an execution trace it cannot prove how "
                "many times an evaluator routine was called at run time."
            ),
            (
                "Raw-to-canonical isomorphism rules out a nonisomorphic "
                "collision. The checker does not independently derive a "
                "canonical normal form or compare every pair of distinct "
                "canonical keys; redundant isomorphic keys would cause extra "
                "evaluations, not omitted origins."
            ),
            (
                "The checker validates evaluation-record consistency but "
                "does not re-run gamma, alpha, or eternal-domination solvers."
            ),
        ],
        "started_unix": started_unix,
        "finished_unix": time.time(),
        "wall_seconds": time.monotonic() - started_monotonic,
        "maximum_resident_set_size_mib": _rss_mib(),
        "checker_python": platform.python_version(),
    }


def _verify_inputs_unchanged(
    *,
    metadata: Mapping[str, str],
    original_configuration: Mapping[str, object],
    original_configuration_digest: str,
    original_binding: Mapping[str, object],
    original_binding_digest: str,
    paths: AuditPaths,
    policy: AuditPolicy,
    database_sha256: str,
) -> None:
    actual_database_hash = sha256_file(paths.database)
    if actual_database_hash != database_sha256:
        raise AuditError("search database changed during immutable audit")
    current_configuration, current_digest = _configuration_from_metadata(
        metadata, paths=paths, policy=policy
    )
    if (
        current_digest != original_configuration_digest
        or current_configuration != original_configuration
    ):
        raise AuditError("search configuration binding changed during audit")
    current_binding, current_binding_digest = _audit_binding(
        paths=paths,
        policy=policy,
        configuration_digest=current_digest,
        database_sha256=actual_database_hash,
    )
    if (
        current_binding_digest != original_binding_digest
        or current_binding != original_binding
    ):
        raise AuditError("an immutable audit input changed during audit")


def run_postrun_audit(
    *,
    paths: AuditPaths,
    policy: AuditPolicy = PRODUCTION_AUDIT_POLICY,
    checkpoint_interval: int = 256,
    max_new_origins: int | None = None,
    wall_limit_seconds: float = 2700.0,
    memory_limit_mib: float = 1024.0,
) -> AuditOutcome:
    """Audit or resume the immutable post-run artifact.

    Returning ``in_progress`` is a clean, checkpointed resource stop.  A
    ``complete`` return means all independent reconstruction, isomorphism,
    multiplicity, configuration, checkpoint, and CSV checks passed.
    Any inconsistency raises :class:`AuditError`; no partial state is promoted.
    """

    if type(checkpoint_interval) is not int or checkpoint_interval < 1:
        raise AuditError("checkpoint_interval must be a positive integer")
    if max_new_origins is not None and (
        type(max_new_origins) is not int or max_new_origins < 1
    ):
        raise AuditError("max_new_origins must be a positive integer or None")
    _require_positive_finite(wall_limit_seconds, "audit wall limit")
    _require_positive_finite(memory_limit_mib, "audit memory limit")
    started_unix = time.time()
    started_monotonic = time.monotonic()
    resolved = _validate_path_roles(paths)
    try:
        database_sha256 = sha256_file(resolved.database)
        hosts = load_host_universe(
            resolved.catalog, resolved.parameters, policy=policy.universe
        )
    except (OSError, UnicodeError, ValueError) as error:
        if isinstance(error, AuditError):
            raise
        raise AuditError(f"cannot bind the host universe: {error}") from error

    search = _open_immutable_database(resolved.database)
    state: sqlite3.Connection | None = None
    try:
        _validate_search_schema(search)
        metadata = _read_metadata(search)
        configuration, configuration_digest = _configuration_from_metadata(
            metadata, paths=resolved, policy=policy
        )
        checkpoint_payload = _validate_checkpoint(
            strict_json_file(resolved.checkpoint),
            configuration=configuration,
            configuration_digest=configuration_digest,
            paths=resolved,
            database_sha256=database_sha256,
            policy=policy,
        )
        _validate_database_hosts(search, hosts)
        binding, binding_digest = _audit_binding(
            paths=resolved,
            policy=policy,
            configuration_digest=configuration_digest,
            database_sha256=database_sha256,
        )
        state = _initialize_or_open_state(
            resolved.state_database,
            binding=binding,
            binding_digest=binding_digest,
        )
        _validate_prior_receipts(search, state, hosts=hosts)
        origin_status, verified, origin_chain = _audit_origins(
            search,
            state,
            hosts=hosts,
            checkpoint_interval=checkpoint_interval,
            max_new_origins=max_new_origins,
            wall_limit_seconds=wall_limit_seconds,
            memory_limit_mib=memory_limit_mib,
            started=started_monotonic,
        )
        if origin_status == "in_progress":
            _verify_inputs_unchanged(
                metadata=metadata,
                original_configuration=configuration,
                original_configuration_digest=configuration_digest,
                original_binding=binding,
                original_binding_digest=binding_digest,
                paths=resolved,
                policy=policy,
                database_sha256=database_sha256,
            )
            report = _report_payload(
                status="in_progress",
                paths=resolved,
                policy=policy,
                binding=binding,
                binding_digest=binding_digest,
                configuration_digest=configuration_digest,
                database_sha256=database_sha256,
                verified_origins=verified,
                origin_chain_sha256=origin_chain,
                unique_count=None,
                started_unix=started_unix,
                started_monotonic=started_monotonic,
            )
            _atomic_json(resolved.report, report)
            return AuditOutcome(
                "in_progress",
                verified,
                policy.universe.raw_origins,
                None,
                str(resolved.report),
                origin_chain,
            )

        unique_count, multiplicity = _audit_canonical_evaluations(
            search,
            state,
            hosts=hosts,
            expected_origins=policy.universe.raw_origins,
        )
        if multiplicity != policy.universe.raw_origins:
            raise AuditError("independent multiplicity total differs")
        stream_hashes = _audit_host_stream_hashes(search, hosts)
        _audit_exports(
            search,
            paths=resolved,
            expected_origins=policy.universe.raw_origins,
            expected_unique=unique_count,
        )
        _final_checkpoint_crosscheck(
            checkpoint_payload,
            unique_count=unique_count,
            stream_hashes=stream_hashes,
            expected_origins=policy.universe.raw_origins,
        )
        _verify_inputs_unchanged(
            metadata=metadata,
            original_configuration=configuration,
            original_configuration_digest=configuration_digest,
            original_binding=binding,
            original_binding_digest=binding_digest,
            paths=resolved,
            policy=policy,
            database_sha256=database_sha256,
        )
        state.execute("UPDATE progress SET status = 'complete' WHERE singleton = 1")
        state.commit()
        status, _, _, verified, origin_chain = _validate_state_consistency(
            state, hosts
        )
        if status != "complete":
            raise AuditError("audit state did not enter complete status")
        report = _report_payload(
            status="complete",
            paths=resolved,
            policy=policy,
            binding=binding,
            binding_digest=binding_digest,
            configuration_digest=configuration_digest,
            database_sha256=database_sha256,
            verified_origins=verified,
            origin_chain_sha256=origin_chain,
            unique_count=unique_count,
            started_unix=started_unix,
            started_monotonic=started_monotonic,
            stream_hashes=stream_hashes,
        )
        _atomic_json(resolved.report, report)
        return AuditOutcome(
            "complete",
            verified,
            policy.universe.raw_origins,
            unique_count,
            str(resolved.report),
            origin_chain,
        )
    except (sqlite3.Error, OSError, UnicodeError) as error:
        raise AuditError(f"post-run audit failed closed: {error}") from error
    finally:
        if state is not None:
            state.close()
        search.close()
