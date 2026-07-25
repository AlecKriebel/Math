"""Independent resumable post-run audit for the edge-toggle search.

The production ledger is opened immutable and read-only.  This module never
imports the search engine, verifier A, verifier B, or the earlier extension
coverage checker.  Its only writes are a separate SQLite receipt ledger and
an atomic JSON report.
"""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import asdict, dataclass
from hashlib import sha256
from itertools import combinations, zip_longest
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

from .graph import Graph, Graph6Error, find_isomorphism, verify_isomorphism


SEARCH_SCHEMA_VERSION = 1
STATE_SCHEMA_VERSION = 1
AUDIT_FORMAT = "gamma-theta-edge-toggle-postrun-audit-v1"
CHAIN_DOMAIN = b"gamma-theta-edge-toggle-origin-chain-v1\0"
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")

SEED_INPUT_SHA256 = (
    "e7f0ffa459d74a67a3a647e19ee5669652ff1679302b3b62daaef299ee02945e"
)
EXTENSION_COVERAGE_AUDIT_SHA256 = (
    "523b3a57ef9afac2b8c921564afcf3fcd8fdbe7719984014f3b0f8e80da8e7cb"
)
EXTENSION_EVALUATION_AUDIT_SHA256 = (
    "75c999e19fb3e877083e4612dd2550079480ad610b67a5caefb0fbf6d303678e"
)
PINNED_LABELG_SHA256 = (
    "ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0"
)
PINNED_NAUTY_ARCHIVE_SHA256 = (
    "9fc4edae04f88a0f5883985be3b39cf7f898fd6cc96e96b9ee25452743cc1b5b"
)
PINNED_ENGINE_SHA256 = (
    "f1fdcb6f61426920e347aa81d64ea9e95dbae094956762cf42bbc637cb3f4336"
)

SELECTED_CATEGORIES = frozenset(
    {
        "private_obstruction_eternal_false",
        "eternal_false_without_private_obstruction",
    }
)
EXPECTED_SEED_CATEGORY_COUNTS = Counter(
    {
        "private_obstruction_eternal_false": 106,
        "eternal_false_without_private_obstruction": 285,
    }
)
EXPECTED_SOURCE_CATEGORY_COUNTS = Counter(
    {
        "gamma_below_3": 52_447,
        "alpha_above_3": 1_378,
        "eternal_false_without_private_obstruction": 285,
        "private_obstruction_eternal_false": 106,
    }
)
EXPECTED_ORDER_COUNTS = Counter({11: 15, 12: 376})
EXPECTED_ORIGINS = 25_641

SEARCH_RUNTIME_PATHS = (
    "src/search/edge_toggle_killtest.py",
    "src/search/extension_killtest.py",
    "src/search/private_obstruction.py",
    "src/verifier_a/core.py",
    "src/verifier_b/__init__.py",
    "src/verifier_b/graph.py",
    "src/verifier_b/invariants.py",
    "src/verifier_b/eternal.py",
)
CHECKER_SOURCE_PATHS = (
    "src/edge_toggle_coverage_checker/__init__.py",
    "src/edge_toggle_coverage_checker/graph.py",
    "src/edge_toggle_coverage_checker/audit.py",
    "src/edge_toggle_coverage_checker/cli.py",
    "src/edge_toggle_coverage_checker/__main__.py",
    "src/edge_toggle_coverage_checker/PROTOCOL.md",
)
CONFIGURATION_KEYS = frozenset(
    {
        "seed_input_path",
        "seed_input_sha256",
        "extension_audit_path",
        "extension_audit_sha256",
        "labelg_path",
        "labelg_sha256",
        "nauty_archive_sha256",
        "runtime_source_manifest",
        "runtime_source_set_sha256",
        "python_implementation",
        "python_version",
        "python_executable",
        "batch_size",
        "active_seed_ids",
        "wall_limit_seconds",
        "memory_limit_mib",
        "schema_version",
    }
)
SEED_INPUT_HEADER = (
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
PROVENANCE_HEADER = (
    "seed_id",
    "pair_index",
    "first_vertex",
    "second_vertex",
    "toggle_action",
    "raw_graph6",
    "canonical_graph6",
    "category",
)
UNIQUE_HEADER = (
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
)
SEARCH_TABLE_COLUMNS = {
    "metadata": ("key", "value"),
    "seeds": (
        "seed_index",
        "seed_id",
        "graph6",
        "n",
        "m",
        "source_category",
        "raw_expected",
        "next_pair_index",
        "status",
        "canonical_stream_sha256",
    ),
    "canonical_graphs": (
        "graph6",
        *UNIQUE_HEADER[1:],
    ),
    "origins": PROVENANCE_HEADER,
}
STATE_TABLE_COLUMNS = {
    "metadata": ("key", "value"),
    "progress": (
        "singleton",
        "status",
        "verified_origins",
        "origin_chain_sha256",
    ),
    "canonical_counts": (
        "graph6",
        "origin_count",
        "first_global_index",
        "first_seed_index",
        "first_seed_id",
        "first_pair_index",
        "first_raw_graph6",
    ),
    "origin_receipts": (
        "global_index",
        "seed_index",
        "seed_id",
        "pair_index",
        "first_vertex",
        "second_vertex",
        "toggle_action",
        "raw_graph6",
        "canonical_graph6",
        "category",
        "mapping_json",
        "chain_sha256",
    ),
}


class AuditError(RuntimeError):
    """A strict post-run coverage or binding check failed."""


@dataclass(frozen=True, slots=True)
class Seed:
    index: int
    seed_id: str
    graph6: str
    order: int
    size: int
    source_category: str

    @property
    def pairs(self) -> tuple[tuple[int, int], ...]:
        return tuple(combinations(range(self.order), 2))

    @property
    def raw_expected(self) -> int:
        return self.order * (self.order - 1) // 2


@dataclass(frozen=True, slots=True)
class AuditPaths:
    campaign_root: Path
    seed_input: Path
    extension_coverage_audit: Path
    extension_evaluation_audit: Path
    database: Path
    checkpoint: Path
    provenance_csv: Path
    unique_csv: Path
    candidate_directory: Path
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


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def _strict_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if not isinstance(key, str) or key in result:
            raise AuditError(f"duplicate or non-string JSON key: {key!r}")
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise AuditError(f"non-finite JSON constant: {value}")


def strict_json_file(path: Path) -> object:
    try:
        text = path.read_bytes().decode("utf-8")
        return json.loads(
            text,
            object_pairs_hook=_strict_pairs,
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise AuditError(f"invalid JSON file {path}: {error}") from error


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
        raise AuditError(f"value is not canonical JSON: {error}") from error


def _json_sha256(value: object) -> str:
    return sha256(_canonical_json(value)).hexdigest()


def _require_mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, dict):
        raise AuditError(f"{label} is not a JSON object")
    return value


def _require_int(
    value: object, label: str, *, minimum: int | None = None
) -> int:
    if type(value) is not int or (minimum is not None and value < minimum):
        raise AuditError(f"{label} is not an admissible integer")
    return value


def _require_decimal_int(
    value: object, label: str, *, minimum: int | None = None
) -> int:
    if not isinstance(value, str) or not value or (
        len(value) > 1 and value[0] == "0"
    ):
        raise AuditError(f"{label} is not canonical decimal text")
    if not value.isascii() or not value.isdigit():
        raise AuditError(f"{label} is not nonnegative decimal text")
    result = int(value)
    if minimum is not None and result < minimum:
        raise AuditError(f"{label} is below its minimum")
    return result


def _require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise AuditError(f"{label} is not a lowercase SHA-256 digest")
    return value


def _positive_finite(value: object, label: str) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value <= 0
    ):
        raise AuditError(f"{label} must be a positive finite number")
    return float(value)


def _regular_file(path: Path, label: str) -> Path:
    resolved = path.resolve()
    if not resolved.is_file():
        raise AuditError(f"{label} is not a regular file: {resolved}")
    return resolved


def _source_manifest(
    campaign_root: Path, relative_paths: Sequence[str]
) -> tuple[tuple[str, str], ...]:
    result = []
    for relative in relative_paths:
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts:
            raise AuditError(f"unsafe source-manifest path: {relative}")
        path = _regular_file(
            campaign_root / Path(*pure.parts), f"source {relative}"
        )
        result.append((relative, sha256_file(path)))
    return tuple(result)


def _manifest_sha256(manifest: Iterable[tuple[str, str]]) -> str:
    digest = sha256()
    for relative, file_hash in manifest:
        digest.update(f"{relative},{file_hash}\n".encode("utf-8"))
    return digest.hexdigest()


def _atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".partial", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(
                value,
                handle,
                indent=2,
                sort_keys=True,
                allow_nan=False,
            )
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _resource_usage() -> dict[str, object]:
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


def _validate_extension_audits(paths: AuditPaths) -> None:
    seed_hash = sha256_file(paths.seed_input)
    coverage_hash = sha256_file(paths.extension_coverage_audit)
    evaluation_hash = sha256_file(paths.extension_evaluation_audit)
    if seed_hash != SEED_INPUT_SHA256:
        raise AuditError("extension seed table differs from its exact byte pin")
    if coverage_hash != EXTENSION_COVERAGE_AUDIT_SHA256:
        raise AuditError("extension coverage audit differs from its byte pin")
    if evaluation_hash != EXTENSION_EVALUATION_AUDIT_SHA256:
        raise AuditError("extension evaluation audit differs from its byte pin")

    coverage = _require_mapping(
        strict_json_file(paths.extension_coverage_audit),
        "extension coverage audit",
    )
    if (
        coverage.get("format") != "gamma-theta-extension-postrun-audit-v1"
        or coverage.get("status") != "complete"
        or coverage.get("passed") is not True
        or coverage.get("verified_origins") != 110_537
        or coverage.get("unique_canonical_graphs") != 54_216
    ):
        raise AuditError("extension coverage audit is not a passed exact audit")
    coverage_binding = _require_mapping(
        coverage.get("audit_binding"), "extension coverage binding"
    )
    if (
        coverage_binding.get("unique_sha256") != seed_hash
        or coverage.get("audit_binding_sha256")
        != _json_sha256(dict(coverage_binding))
    ):
        raise AuditError("extension coverage audit does not bind the seed table")

    evaluation = _require_mapping(
        strict_json_file(paths.extension_evaluation_audit),
        "extension evaluation audit",
    )
    if (
        evaluation.get("format")
        != "gamma-theta-extension-mathematical-audit-v1"
        or evaluation.get("status") != "complete"
        or evaluation.get("passed") is not True
        or evaluation.get("replay_passed") is not True
        or evaluation.get("row_count") != 54_216
        or evaluation.get("category_counts")
        != dict(EXPECTED_SOURCE_CATEGORY_COUNTS)
    ):
        raise AuditError("extension evaluation audit is not a passed exact audit")
    evaluation_binding = _require_mapping(
        evaluation.get("binding"), "extension evaluation binding"
    )
    if (
        evaluation_binding.get("unique_csv_sha256") != seed_hash
        or evaluation_binding.get("coverage_report_sha256") != coverage_hash
        or evaluation.get("mathematical_discharge")
        != {
            "alpha_above_3_rows_gamma_3_alpha_4": 1_378,
            "eternal_false_rows_gamma_alpha_3_empty_one_guard_gfp": 391,
            "gamma_below_3_rows": 52_447,
            "surviving_counterexample_candidates": 0,
        }
    ):
        raise AuditError("extension evaluation audit does not discharge 391 seeds")


def load_seed_universe(paths: AuditPaths) -> tuple[Seed, ...]:
    """Independently select and validate the exact 391 source rows."""

    _validate_extension_audits(paths)
    try:
        handle = paths.seed_input.open(encoding="utf-8", newline="")
    except OSError as error:
        raise AuditError(f"cannot read extension seed table: {error}") from error
    with handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header != list(SEED_INPUT_HEADER):
            raise AuditError("extension seed table header differs")
        selected: list[Seed] = []
        all_categories: Counter[str] = Counter()
        seen: set[str] = set()
        row_count = 0
        for row_count, row in enumerate(reader, 1):
            if len(row) != len(SEED_INPUT_HEADER):
                raise AuditError(f"malformed extension row {row_count}")
            values = dict(zip(SEED_INPUT_HEADER, row, strict=True))
            graph6 = values["canonical_graph6"]
            if graph6 in seen:
                raise AuditError(f"duplicate extension canonical key: {graph6}")
            seen.add(graph6)
            try:
                graph = Graph.from_graph6(graph6)
            except (Graph6Error, ValueError) as error:
                raise AuditError(
                    f"invalid extension graph6 at row {row_count}: {error}"
                ) from error
            order = _require_decimal_int(values["n"], f"row {row_count} n")
            size = _require_decimal_int(values["m"], f"row {row_count} m")
            category = values["category"]
            all_categories[category] += 1
            if graph.order != order or graph.size != size:
                raise AuditError(f"extension row {row_count} graph metadata differs")
            if category not in SELECTED_CATEGORIES:
                continue
            gamma = _require_decimal_int(
                values["gamma"], f"row {row_count} gamma"
            )
            alpha = _require_decimal_int(
                values["alpha"], f"row {row_count} alpha"
            )
            if (
                gamma != 3
                or alpha != 3
                or values["eternal_a"] != "0"
                or values["eternal_b"] != "0"
                or not graph.is_connected()
            ):
                raise AuditError(f"selected extension row {row_count} is invalid")
            selected.append(
                Seed(
                    index=len(selected),
                    seed_id=f"ET-{len(selected) + 1:04d}",
                    graph6=graph6,
                    order=order,
                    size=size,
                    source_category=category,
                )
            )
    if row_count != 54_216:
        raise AuditError(
            f"extension seed table has {row_count} rows rather than 54216"
        )
    if all_categories != EXPECTED_SOURCE_CATEGORY_COUNTS:
        raise AuditError(f"source category census differs: {all_categories}")
    seeds = tuple(selected)
    if len(seeds) != 391:
        raise AuditError(f"selected {len(seeds)} seeds rather than 391")
    if Counter(seed.source_category for seed in seeds) != (
        EXPECTED_SEED_CATEGORY_COUNTS
    ):
        raise AuditError("selected seed categories differ")
    if Counter(seed.order for seed in seeds) != EXPECTED_ORDER_COUNTS:
        raise AuditError("selected seed order distribution differs")
    if sum(seed.raw_expected for seed in seeds) != EXPECTED_ORIGINS:
        raise AuditError("selected pair universe does not total 25641")
    return seeds


def _validate_path_roles(paths: AuditPaths) -> AuditPaths:
    resolved = AuditPaths(
        **{
            field: value.resolve()
            for field, value in asdict(paths).items()
        }
    )
    inputs = {
        "seed input": resolved.seed_input,
        "extension coverage audit": resolved.extension_coverage_audit,
        "extension evaluation audit": resolved.extension_evaluation_audit,
        "database": resolved.database,
        "checkpoint": resolved.checkpoint,
        "provenance": resolved.provenance_csv,
        "unique": resolved.unique_csv,
    }
    for label, path in inputs.items():
        _regular_file(path, label)
    if resolved.state_database == resolved.report:
        raise AuditError("audit state and report paths alias")
    for role, writable in (
        ("audit state", resolved.state_database),
        ("audit report", resolved.report),
    ):
        for input_role, input_path in inputs.items():
            if writable == input_path:
                raise AuditError(f"{role} aliases {input_role}")
    if resolved.state_database in resolved.report.parents or (
        resolved.report in resolved.state_database.parents
    ):
        raise AuditError("audit state and report paths nest")
    candidate = resolved.candidate_directory
    for role, writable in (
        ("audit state", resolved.state_database),
        ("audit report", resolved.report),
    ):
        if (
            candidate == writable
            or candidate in writable.parents
            or writable in candidate.parents
        ):
            raise AuditError(f"candidate directory conflicts with {role}")
    return resolved


def _validate_configuration(
    *,
    paths: AuditPaths,
    raw_json: str,
    stored_digest: str,
) -> tuple[dict[str, object], str, tuple[tuple[str, str], ...]]:
    try:
        configuration = json.loads(
            raw_json,
            object_pairs_hook=_strict_pairs,
            parse_constant=_reject_constant,
        )
    except (json.JSONDecodeError, UnicodeError, RecursionError) as error:
        raise AuditError(f"invalid configuration JSON: {error}") from error
    config = dict(_require_mapping(configuration, "search configuration"))
    if frozenset(config) != CONFIGURATION_KEYS:
        raise AuditError("search configuration has an unexpected key set")
    digest = _json_sha256(config)
    if stored_digest != digest:
        raise AuditError("search configuration digest differs")
    if (
        Path(str(config["seed_input_path"])).resolve() != paths.seed_input
        or config["seed_input_sha256"] != SEED_INPUT_SHA256
        or Path(str(config["extension_audit_path"])).resolve()
        != paths.extension_coverage_audit
        or config["extension_audit_sha256"]
        != EXTENSION_COVERAGE_AUDIT_SHA256
    ):
        raise AuditError("search configuration input binding differs")
    if config["active_seed_ids"] != []:
        raise AuditError("search configuration is a seed shard")
    if _require_int(config["schema_version"], "schema version") != 1:
        raise AuditError("search configuration schema differs")
    _require_int(config["batch_size"], "batch size", minimum=1)
    _positive_finite(config["wall_limit_seconds"], "wall limit")
    _positive_finite(config["memory_limit_mib"], "memory limit")
    for key in ("python_implementation", "python_version", "python_executable"):
        if not isinstance(config[key], str) or not config[key]:
            raise AuditError(f"configuration {key} is invalid")
    if not Path(str(config["python_executable"])).resolve().is_file():
        raise AuditError("configured Python executable no longer exists")

    labelg = _regular_file(Path(str(config["labelg_path"])), "configured labelg")
    if (
        config["labelg_sha256"] != PINNED_LABELG_SHA256
        or sha256_file(labelg) != PINNED_LABELG_SHA256
    ):
        raise AuditError("configured labelg differs from the independent pin")
    archive = _regular_file(
        labelg.parent.parent / "nauty2_9_3.tar.gz", "nauty source archive"
    )
    if (
        config["nauty_archive_sha256"] != PINNED_NAUTY_ARCHIVE_SHA256
        or sha256_file(archive) != PINNED_NAUTY_ARCHIVE_SHA256
    ):
        raise AuditError("nauty archive differs from the independent pin")

    raw_manifest = config["runtime_source_manifest"]
    if not isinstance(raw_manifest, list):
        raise AuditError("runtime source manifest is not an array")
    stored_manifest: list[tuple[str, str]] = []
    for index, item in enumerate(raw_manifest):
        if (
            not isinstance(item, list)
            or len(item) != 2
            or not isinstance(item[0], str)
        ):
            raise AuditError(f"malformed runtime source record {index}")
        stored_manifest.append(
            (item[0], _require_sha256(item[1], f"runtime source hash {index}"))
        )
    actual_manifest = _source_manifest(paths.campaign_root, SEARCH_RUNTIME_PATHS)
    if tuple(stored_manifest) != actual_manifest:
        raise AuditError("runtime source manifest differs from current bytes")
    if config["runtime_source_set_sha256"] != _manifest_sha256(stored_manifest):
        raise AuditError("runtime source-set hash differs")
    source_hashes = dict(stored_manifest)
    if source_hashes.get(SEARCH_RUNTIME_PATHS[0]) != PINNED_ENGINE_SHA256:
        raise AuditError("edge-toggle engine differs from the accepted pin")
    return config, digest, tuple(stored_manifest)


def _open_immutable_database(path: Path) -> sqlite3.Connection:
    for suffix in ("-journal", "-wal", "-shm"):
        companion = Path(str(path) + suffix)
        if companion.exists():
            raise AuditError(
                f"refusing mutable/in-flight database companion: {companion}"
            )
    uri = path.as_uri() + "?mode=ro&immutable=1"
    try:
        connection = sqlite3.connect(uri, uri=True)
        connection.execute("PRAGMA query_only = ON")
    except sqlite3.Error as error:
        raise AuditError(f"cannot open immutable search database: {error}") from error
    try:
        integrity = connection.execute("PRAGMA integrity_check").fetchall()
        if integrity != [("ok",)]:
            raise AuditError(f"search database integrity failure: {integrity}")
        foreign = connection.execute("PRAGMA foreign_key_check").fetchall()
        if foreign:
            raise AuditError(f"search database foreign-key failure: {foreign[:3]}")
        if connection.execute("PRAGMA user_version").fetchone() != (
            SEARCH_SCHEMA_VERSION,
        ):
            raise AuditError("search database schema version differs")
        tables = {
            str(row[0])
            for row in connection.execute(
                """
                SELECT name FROM sqlite_master
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                """
            )
        }
        if tables != set(SEARCH_TABLE_COLUMNS):
            raise AuditError(f"search database table set differs: {tables}")
        for table, expected in SEARCH_TABLE_COLUMNS.items():
            actual = tuple(
                str(row[1])
                for row in connection.execute(f'PRAGMA table_info("{table}")')
            )
            if actual != expected:
                raise AuditError(
                    f"search database columns differ for {table}: {actual}"
                )
    except BaseException:
        connection.close()
        raise
    return connection


def _database_metadata(
    connection: sqlite3.Connection,
) -> tuple[str, str, str]:
    rows = tuple(connection.execute("SELECT key, value FROM metadata ORDER BY key"))
    expected_keys = (
        "candidate_frozen_path",
        "configuration_json",
        "configuration_sha256",
    )
    if tuple(row[0] for row in rows) != expected_keys:
        raise AuditError("search metadata key set differs")
    values = {str(key): str(value) for key, value in rows}
    return (
        values["configuration_json"],
        values["configuration_sha256"],
        values["candidate_frozen_path"],
    )


def _validate_checkpoint(
    *,
    paths: AuditPaths,
    checkpoint: object,
    configuration: Mapping[str, object],
    configuration_sha256: str,
    database_sha256: str,
    seeds: Sequence[Seed],
) -> dict[str, object]:
    payload = dict(_require_mapping(checkpoint, "edge-toggle checkpoint"))
    if payload.get("status") != "complete":
        raise AuditError("edge-toggle checkpoint is not complete")
    if (
        payload.get("configuration") != configuration
        or payload.get("configuration_sha256") != configuration_sha256
    ):
        raise AuditError("checkpoint configuration binding differs")
    if payload.get("database_sha256") != database_sha256:
        raise AuditError("checkpoint database byte hash differs")
    if (
        not isinstance(payload.get("database"), str)
        or Path(str(payload["database"])).resolve() != paths.database
    ):
        raise AuditError("checkpoint database path differs")
    for key, expected in (
        ("raw_expected", EXPECTED_ORIGINS),
        ("raw_processed", EXPECTED_ORIGINS),
        ("seeds_complete", len(seeds)),
    ):
        if payload.get(key) != expected:
            raise AuditError(f"checkpoint {key} differs from {expected}")

    candidate = _require_mapping(
        payload.get("candidate_state"), "checkpoint candidate state"
    )
    if (
        candidate.get("pending") is not False
        or candidate.get("primary_reference") is not None
        or candidate.get("marker_path") is not None
        or candidate.get("marker_file_exists") is not False
        or candidate.get("canonical_candidate_count") != 0
        or candidate.get("origin_candidate_count") != 0
        or candidate.get("canonical_candidate_graph6") != []
        or candidate.get("origin_candidates") != []
        or candidate.get("inconsistencies") != []
        or payload.get("candidate_reference") is not None
    ):
        raise AuditError("checkpoint contains candidate state")

    coverage = _require_mapping(
        payload.get("coverage_audit"), "internal search coverage audit"
    )
    if (
        coverage.get("passed") is not True
        or coverage.get("errors") != []
        or coverage.get("raw_expected") != EXPECTED_ORIGINS
        or coverage.get("raw_origins") != EXPECTED_ORIGINS
        or coverage.get("stored_origin_multiplicity") != EXPECTED_ORIGINS
        or coverage.get("bad_canonical_multiplicity_count") != 0
    ):
        raise AuditError("internal search coverage audit did not pass exactly")
    output_hashes = _require_mapping(
        payload.get("output_sha256"), "checkpoint output hashes"
    )
    expected_hashes = {
        str(paths.provenance_csv): sha256_file(paths.provenance_csv),
        str(paths.unique_csv): sha256_file(paths.unique_csv),
    }
    if output_hashes != expected_hashes:
        raise AuditError("checkpoint output hashes differ from current exports")
    rows = payload.get("seeds")
    if not isinstance(rows, list) or len(rows) != len(seeds):
        raise AuditError("checkpoint seed summary differs")
    for seed, row_value in zip(seeds, rows, strict=True):
        row = _require_mapping(row_value, f"checkpoint seed {seed.seed_id}")
        if (
            row.get("seed_id") != seed.seed_id
            or row.get("n") != seed.order
            or row.get("raw_expected") != seed.raw_expected
            or row.get("raw_processed") != seed.raw_expected
            or row.get("next_pair_index") != seed.raw_expected
            or row.get("status") != "complete"
        ):
            raise AuditError(f"checkpoint seed row differs for {seed.seed_id}")
        _require_sha256(
            row.get("canonical_stream_sha256"),
            f"checkpoint stream hash {seed.seed_id}",
        )
    return payload


def _validate_database_seed_rows(
    connection: sqlite3.Connection, seeds: Sequence[Seed]
) -> None:
    rows = tuple(
        connection.execute(
            """
            SELECT seed_index, seed_id, graph6, n, m, source_category,
                   raw_expected, next_pair_index, status,
                   canonical_stream_sha256
            FROM seeds ORDER BY seed_index
            """
        )
    )
    if len(rows) != len(seeds):
        raise AuditError(f"database has {len(rows)} seeds rather than 391")
    for seed, row in zip(seeds, rows, strict=True):
        expected = (
            seed.index,
            seed.seed_id,
            seed.graph6,
            seed.order,
            seed.size,
            seed.source_category,
            seed.raw_expected,
            seed.raw_expected,
            "complete",
        )
        if row[:9] != expected:
            raise AuditError(f"database seed row differs for {seed.seed_id}")
        _require_sha256(row[9], f"database stream hash {seed.seed_id}")
    count = connection.execute("SELECT COUNT(*) FROM origins").fetchone()
    if count != (EXPECTED_ORIGINS,):
        raise AuditError(f"database origin count differs: {count}")


def _validate_no_candidate_freeze(
    connection: sqlite3.Connection,
    marker: str,
    candidate_directory: Path,
) -> None:
    if marker:
        raise AuditError("database has a frozen-candidate marker")
    candidate_category = "candidate_gamma_equals_eternal_below_theta"
    counts = connection.execute(
        """
        SELECT
          (SELECT COUNT(*) FROM canonical_graphs WHERE category = ?),
          (SELECT COUNT(*) FROM origins WHERE category = ?)
        """,
        (candidate_category, candidate_category),
    ).fetchone()
    if counts != (0, 0):
        raise AuditError(f"database contains candidate rows: {counts}")
    if candidate_directory.exists():
        if not candidate_directory.is_dir():
            raise AuditError("candidate path exists but is not a directory")
        try:
            first_entry = next(candidate_directory.iterdir(), None)
        except OSError as error:
            raise AuditError(f"cannot inspect candidate directory: {error}") from error
        if first_entry is not None:
            raise AuditError(
                f"candidate-freeze directory is not empty: {first_entry}"
            )


def _audit_binding(
    *,
    paths: AuditPaths,
    configuration_sha256: str,
    database_sha256: str,
    checkpoint_sha256: str,
    search_manifest: Sequence[tuple[str, str]],
) -> tuple[dict[str, object], str]:
    checker_manifest = _source_manifest(paths.campaign_root, CHECKER_SOURCE_PATHS)
    binding: dict[str, object] = {
        "format": AUDIT_FORMAT,
        "state_schema_version": STATE_SCHEMA_VERSION,
        "seed_input_sha256": sha256_file(paths.seed_input),
        "extension_coverage_audit_sha256": sha256_file(
            paths.extension_coverage_audit
        ),
        "extension_evaluation_audit_sha256": sha256_file(
            paths.extension_evaluation_audit
        ),
        "search_database_sha256": database_sha256,
        "search_checkpoint_sha256": checkpoint_sha256,
        "provenance_csv_sha256": sha256_file(paths.provenance_csv),
        "unique_csv_sha256": sha256_file(paths.unique_csv),
        "configuration_sha256": configuration_sha256,
        "search_runtime_source_manifest": [list(item) for item in search_manifest],
        "search_runtime_source_set_sha256": _manifest_sha256(search_manifest),
        "checker_source_manifest": [list(item) for item in checker_manifest],
        "checker_source_set_sha256": _manifest_sha256(checker_manifest),
        "paths": {
            "seed_input": str(paths.seed_input),
            "extension_coverage_audit": str(paths.extension_coverage_audit),
            "extension_evaluation_audit": str(
                paths.extension_evaluation_audit
            ),
            "database": str(paths.database),
            "checkpoint": str(paths.checkpoint),
            "provenance_csv": str(paths.provenance_csv),
            "unique_csv": str(paths.unique_csv),
            "candidate_directory": str(paths.candidate_directory),
            "state_database": str(paths.state_database),
            "report": str(paths.report),
        },
    }
    return binding, _json_sha256(binding)


def _connect_state(
    path: Path, binding: Mapping[str, object], binding_sha256: str
) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = DELETE")
    connection.execute("PRAGMA synchronous = FULL")
    version = int(connection.execute("PRAGMA user_version").fetchone()[0])
    if version not in (0, STATE_SCHEMA_VERSION):
        connection.close()
        raise AuditError(f"unsupported audit-state schema {version}")
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
                    verified_origins INTEGER NOT NULL,
                    origin_chain_sha256 TEXT NOT NULL
                );
                CREATE TABLE canonical_counts (
                    graph6 TEXT PRIMARY KEY,
                    origin_count INTEGER NOT NULL,
                    first_global_index INTEGER NOT NULL,
                    first_seed_index INTEGER NOT NULL,
                    first_seed_id TEXT NOT NULL,
                    first_pair_index INTEGER NOT NULL,
                    first_raw_graph6 TEXT NOT NULL
                );
                CREATE TABLE origin_receipts (
                    global_index INTEGER PRIMARY KEY,
                    seed_index INTEGER NOT NULL,
                    seed_id TEXT NOT NULL,
                    pair_index INTEGER NOT NULL,
                    first_vertex INTEGER NOT NULL,
                    second_vertex INTEGER NOT NULL,
                    toggle_action TEXT NOT NULL,
                    raw_graph6 TEXT NOT NULL,
                    canonical_graph6 TEXT NOT NULL,
                    category TEXT NOT NULL,
                    mapping_json TEXT NOT NULL,
                    chain_sha256 TEXT NOT NULL,
                    UNIQUE(seed_id, pair_index)
                );
                """
            )
            initial_chain = sha256(CHAIN_DOMAIN).hexdigest()
            connection.executemany(
                "INSERT INTO metadata(key, value) VALUES (?, ?)",
                (
                    (
                        "binding_json",
                        json.dumps(binding, sort_keys=True, separators=(",", ":")),
                    ),
                    ("binding_sha256", binding_sha256),
                ),
            )
            connection.execute(
                """
                INSERT INTO progress(
                    singleton, status, verified_origins, origin_chain_sha256
                ) VALUES (1, 'in_progress', 0, ?)
                """,
                (initial_chain,),
            )
            connection.execute(f"PRAGMA user_version = {STATE_SCHEMA_VERSION}")
            connection.commit()
        except BaseException:
            connection.rollback()
            connection.close()
            raise
    else:
        integrity = connection.execute("PRAGMA integrity_check").fetchall()
        if integrity != [("ok",)]:
            connection.close()
            raise AuditError(f"audit-state integrity failure: {integrity}")
        tables = {
            str(row[0])
            for row in connection.execute(
                """
                SELECT name FROM sqlite_master
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                """
            )
        }
        if tables != set(STATE_TABLE_COLUMNS):
            connection.close()
            raise AuditError("audit-state table set differs")
        for table, expected in STATE_TABLE_COLUMNS.items():
            actual = tuple(
                str(row[1])
                for row in connection.execute(f'PRAGMA table_info("{table}")')
            )
            if actual != expected:
                connection.close()
                raise AuditError(f"audit-state columns differ for {table}")
        rows = dict(connection.execute("SELECT key, value FROM metadata"))
        expected_json = json.dumps(binding, sort_keys=True, separators=(",", ":"))
        if rows != {
            "binding_json": expected_json,
            "binding_sha256": binding_sha256,
        }:
            connection.close()
            raise AuditError("audit-state binding differs from immutable inputs")
    return connection


def _expected_origins(
    seeds: Sequence[Seed],
) -> tuple[tuple[int, Seed, int, int, int], ...]:
    result: list[tuple[int, Seed, int, int, int]] = []
    for seed in seeds:
        for pair_index, (first, second) in enumerate(seed.pairs):
            result.append((len(result), seed, pair_index, first, second))
    if len(result) != EXPECTED_ORIGINS:
        raise AuditError("independent origin schedule does not total 25641")
    return tuple(result)


def _production_origins(
    connection: sqlite3.Connection,
) -> tuple[tuple[object, ...], ...]:
    rows = tuple(
        connection.execute(
            """
            SELECT s.seed_index, o.seed_id, o.pair_index, o.first_vertex,
                   o.second_vertex, o.toggle_action, o.raw_graph6,
                   o.canonical_graph6, o.category
            FROM origins AS o JOIN seeds AS s ON s.seed_id = o.seed_id
            ORDER BY s.seed_index, o.pair_index
            """
        )
    )
    if len(rows) != EXPECTED_ORIGINS:
        raise AuditError(f"database yielded {len(rows)} ordered origins")
    return rows


def _validate_origin(
    expected: tuple[int, Seed, int, int, int],
    row: Sequence[object],
    *,
    stored_mapping: Sequence[int] | None = None,
) -> tuple[str, str, str, tuple[int, ...]]:
    global_index, seed, pair_index, first, second = expected
    if len(row) != 9:
        raise AuditError(f"origin {global_index} has the wrong row width")
    if row[:5] != (
        seed.index,
        seed.seed_id,
        pair_index,
        first,
        second,
    ):
        raise AuditError(
            f"origin schedule differs at global index {global_index}: {row[:5]}"
        )
    seed_graph = Graph.from_graph6(seed.graph6)
    expected_action = (
        "delete" if seed_graph.has_edge(first, second) else "add"
    )
    if row[5] != expected_action:
        raise AuditError(f"origin {global_index} toggle action differs")
    raw_graph = seed_graph.toggled(first, second)
    raw_graph6 = raw_graph.to_graph6()
    if row[6] != raw_graph6:
        raise AuditError(f"origin {global_index} raw graph reconstruction differs")
    if not isinstance(row[7], str):
        raise AuditError(f"origin {global_index} canonical key is not text")
    try:
        canonical = Graph.from_graph6(row[7])
    except (Graph6Error, ValueError) as error:
        raise AuditError(
            f"origin {global_index} has invalid canonical graph6: {error}"
        ) from error
    if canonical.to_graph6() != row[7]:
        raise AuditError(f"origin {global_index} canonical key is not headerless")
    if raw_graph.order != canonical.order or raw_graph.size != canonical.size:
        raise AuditError(f"origin {global_index} canonical metadata differs")
    if not isinstance(row[8], str) or not row[8]:
        raise AuditError(f"origin {global_index} category is invalid")
    if stored_mapping is None:
        mapping = find_isomorphism(raw_graph, canonical)
        if mapping is None:
            raise AuditError(
                f"origin {global_index} raw/canonical graphs are nonisomorphic"
            )
    else:
        mapping = tuple(stored_mapping)
        if not verify_isomorphism(raw_graph, canonical, mapping):
            raise AuditError(
                f"origin {global_index} stored mapping is not an isomorphism"
            )
    return expected_action, raw_graph6, str(row[7]), mapping


def _chain_step(
    previous_hex: str,
    *,
    global_index: int,
    seed_index: int,
    seed_id: str,
    pair_index: int,
    first: int,
    second: int,
    action: str,
    raw_graph6: str,
    canonical_graph6: str,
    category: str,
    mapping: Sequence[int],
) -> str:
    previous = bytes.fromhex(
        _require_sha256(previous_hex, "origin chain predecessor")
    )
    receipt = {
        "global_index": global_index,
        "seed_index": seed_index,
        "seed_id": seed_id,
        "pair_index": pair_index,
        "first_vertex": first,
        "second_vertex": second,
        "toggle_action": action,
        "raw_graph6": raw_graph6,
        "canonical_graph6": canonical_graph6,
        "category": category,
        "mapping": list(mapping),
    }
    return sha256(previous + _canonical_json(receipt)).hexdigest()


def _state_counts(
    connection: sqlite3.Connection,
) -> dict[str, tuple[int, int, int, str, int, str]]:
    return {
        str(row[0]): (
            int(row[1]),
            int(row[2]),
            int(row[3]),
            str(row[4]),
            int(row[5]),
            str(row[6]),
        )
        for row in connection.execute(
            """
            SELECT graph6, origin_count, first_global_index, first_seed_index,
                   first_seed_id, first_pair_index, first_raw_graph6
            FROM canonical_counts ORDER BY graph6
            """
        )
    }


def _replay_state(
    state: sqlite3.Connection,
    expected: Sequence[tuple[int, Seed, int, int, int]],
    production_rows: Sequence[Sequence[object]],
) -> tuple[
    int,
    str,
    dict[str, tuple[int, int, int, str, int, str]],
    str,
]:
    progress = state.execute(
        """
        SELECT status, verified_origins, origin_chain_sha256
        FROM progress WHERE singleton = 1
        """
    ).fetchone()
    if progress is None:
        raise AuditError("audit state has no progress row")
    status = str(progress[0])
    verified = _require_int(
        progress[1], "audit verified origin count", minimum=0
    )
    if status not in ("in_progress", "complete") or verified > EXPECTED_ORIGINS:
        raise AuditError("audit progress row is invalid")
    receipts = tuple(
        state.execute(
            """
            SELECT global_index, seed_index, seed_id, pair_index, first_vertex,
                   second_vertex, toggle_action, raw_graph6, canonical_graph6,
                   category, mapping_json, chain_sha256
            FROM origin_receipts ORDER BY global_index
            """
        )
    )
    if len(receipts) != verified:
        raise AuditError("audit receipt count differs from progress")
    chain = sha256(CHAIN_DOMAIN).hexdigest()
    counts: dict[str, tuple[int, int, int, str, int, str]] = {}
    for index, receipt in enumerate(receipts):
        if receipt[0] != index:
            raise AuditError(f"audit receipt sequence skips index {index}")
        try:
            mapping_value = json.loads(
                str(receipt[10]),
                object_pairs_hook=_strict_pairs,
                parse_constant=_reject_constant,
            )
        except (json.JSONDecodeError, RecursionError) as error:
            raise AuditError(f"invalid mapping receipt {index}: {error}") from error
        if (
            not isinstance(mapping_value, list)
            or any(type(value) is not int for value in mapping_value)
        ):
            raise AuditError(f"mapping receipt {index} is malformed")
        action, raw_graph6, canonical_graph6, mapping = _validate_origin(
            expected[index],
            production_rows[index],
            stored_mapping=mapping_value,
        )
        _, seed, pair_index, first, second = expected[index]
        category = str(production_rows[index][8])
        fixed = (
            seed.index,
            seed.seed_id,
            pair_index,
            first,
            second,
            action,
            raw_graph6,
            canonical_graph6,
            category,
            json.dumps(list(mapping), separators=(",", ":")),
        )
        if receipt[1:11] != fixed:
            raise AuditError(f"audit receipt fields differ at index {index}")
        chain = _chain_step(
            chain,
            global_index=index,
            seed_index=seed.index,
            seed_id=seed.seed_id,
            pair_index=pair_index,
            first=first,
            second=second,
            action=action,
            raw_graph6=raw_graph6,
            canonical_graph6=canonical_graph6,
            category=category,
            mapping=mapping,
        )
        if receipt[11] != chain:
            raise AuditError(f"audit receipt chain differs at index {index}")
        if canonical_graph6 in counts:
            prior = counts[canonical_graph6]
            counts[canonical_graph6] = (prior[0] + 1, *prior[1:])
        else:
            counts[canonical_graph6] = (
                1,
                index,
                seed.index,
                seed.seed_id,
                pair_index,
                raw_graph6,
            )
    if chain != progress[2]:
        raise AuditError("audit progress chain differs from replay")
    if counts != _state_counts(state):
        raise AuditError("audit canonical counts differ from receipt replay")
    return verified, chain, counts, status


def _store_origin_receipt(
    state: sqlite3.Connection,
    *,
    expected: tuple[int, Seed, int, int, int],
    action: str,
    raw_graph6: str,
    canonical_graph6: str,
    category: str,
    mapping: Sequence[int],
    chain: str,
) -> None:
    global_index, seed, pair_index, first, second = expected
    mapping_json = json.dumps(list(mapping), separators=(",", ":"))
    state.execute(
        """
        INSERT INTO origin_receipts(
            global_index, seed_index, seed_id, pair_index, first_vertex,
            second_vertex, toggle_action, raw_graph6, canonical_graph6,
            category, mapping_json, chain_sha256
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            global_index,
            seed.index,
            seed.seed_id,
            pair_index,
            first,
            second,
            action,
            raw_graph6,
            canonical_graph6,
            category,
            mapping_json,
            chain,
        ),
    )
    state.execute(
        """
        INSERT INTO canonical_counts(
            graph6, origin_count, first_global_index, first_seed_index,
            first_seed_id, first_pair_index, first_raw_graph6
        ) VALUES (?, 1, ?, ?, ?, ?, ?)
        ON CONFLICT(graph6) DO UPDATE SET
            origin_count = canonical_counts.origin_count + 1
        """,
        (
            canonical_graph6,
            global_index,
            seed.index,
            seed.seed_id,
            pair_index,
            raw_graph6,
        ),
    )


def _optional_int(value: object, label: str) -> int | None:
    if value is None:
        return None
    return _require_int(value, label, minimum=0)


def _validate_canonical_rows(
    connection: sqlite3.Connection,
    counts: Mapping[str, tuple[int, int, int, str, int, str]],
) -> dict[str, int]:
    rows = tuple(
        connection.execute(
            """
            SELECT graph6, n, m, connected, origin_count, first_seed_id,
                   first_pair_index, first_raw_graph6, gamma_a, gamma_b,
                   alpha_a, alpha_b, gamma_infinity_a, gamma_infinity_b,
                   theta_a, theta_b, category, family_size, family_sha256
            FROM canonical_graphs ORDER BY n, graph6
            """
        )
    )
    if len(rows) != len(counts):
        raise AuditError(
            f"canonical row count {len(rows)} differs from reconstructed "
            f"key count {len(counts)}"
        )
    category_counts: Counter[str] = Counter()
    seen: set[str] = set()
    for row_index, row in enumerate(rows):
        graph6 = str(row[0])
        if graph6 in seen or graph6 not in counts:
            raise AuditError(f"unexpected canonical key at row {row_index}")
        seen.add(graph6)
        graph = Graph.from_graph6(graph6)
        if graph.to_graph6() != graph6:
            raise AuditError(f"canonical row {row_index} is not headerless graph6")
        connected = int(graph.is_connected())
        reconstructed = counts[graph6]
        if (
            row[1] != graph.order
            or row[2] != graph.size
            or row[3] != connected
            or row[4] != reconstructed[0]
            or row[5] != reconstructed[3]
            or row[6] != reconstructed[4]
            or row[7] != reconstructed[5]
        ):
            raise AuditError(f"canonical metadata differs for {graph6}")
        parameters = tuple(
            _optional_int(value, f"canonical parameter {graph6}")
            for value in row[8:16]
        )
        category = str(row[16])
        family_size = _optional_int(row[17], f"family size {graph6}")
        family_hash = row[18]
        if not connected:
            if (
                category != "disconnected"
                or any(value is not None for value in parameters)
                or family_size is not None
                or family_hash is not None
            ):
                raise AuditError(f"disconnected canonical row is inconsistent: {graph6}")
        else:
            (
                gamma_a,
                gamma_b,
                alpha_a,
                alpha_b,
                eternal_a,
                eternal_b,
                theta_a,
                theta_b,
            ) = parameters
            if (
                None in parameters
                or gamma_a != gamma_b
                or alpha_a != alpha_b
                or eternal_a != eternal_b
                or theta_a != theta_b
                or not gamma_a <= alpha_a <= eternal_a <= theta_a
                or family_size is None
                or family_size < 1
            ):
                raise AuditError(f"connected canonical parameters differ: {graph6}")
            _require_sha256(family_hash, f"family hash {graph6}")
            expected_category = (
                "candidate_gamma_equals_eternal_below_theta"
                if gamma_a == eternal_a < theta_a
                else (
                    "equality_without_theta_gap"
                    if gamma_a == eternal_a
                    else "gamma_below_eternal"
                )
            )
            if category != expected_category:
                raise AuditError(f"canonical category logic differs: {graph6}")
        if category == "candidate_gamma_equals_eternal_below_theta":
            raise AuditError(f"candidate canonical row exists: {graph6}")
        category_counts[category] += 1
    if seen != set(counts):
        raise AuditError("canonical table omits reconstructed keys")
    mismatch = connection.execute(
        """
        SELECT COUNT(*) FROM origins AS o
        JOIN canonical_graphs AS g ON g.graph6 = o.canonical_graph6
        WHERE o.category != g.category
        """
    ).fetchone()
    if mismatch != (0,):
        raise AuditError("origin categories disagree with canonical rows")
    if sum(category_counts.values()) != len(counts):
        raise AssertionError("canonical category accounting failed")
    return dict(sorted(category_counts.items()))


def _validate_stream_hashes(
    connection: sqlite3.Connection,
    checkpoint: Mapping[str, object],
    seeds: Sequence[Seed],
    production_rows: Sequence[Sequence[object]],
) -> dict[str, str]:
    checkpoint_rows = checkpoint["seeds"]
    assert isinstance(checkpoint_rows, list)
    by_seed: dict[str, list[str]] = {seed.seed_id: [] for seed in seeds}
    for row in production_rows:
        by_seed[str(row[1])].append(str(row[7]))
    result: dict[str, str] = {}
    for seed, checkpoint_value in zip(seeds, checkpoint_rows, strict=True):
        digest = sha256()
        for graph6 in by_seed[seed.seed_id]:
            digest.update(graph6.encode("ascii") + b"\n")
        calculated = digest.hexdigest()
        database_value = connection.execute(
            """
            SELECT canonical_stream_sha256 FROM seeds WHERE seed_id = ?
            """,
            (seed.seed_id,),
        ).fetchone()
        checkpoint_row = _require_mapping(
            checkpoint_value, f"checkpoint stream row {seed.seed_id}"
        )
        if (
            database_value != (calculated,)
            or checkpoint_row.get("canonical_stream_sha256") != calculated
        ):
            raise AuditError(f"canonical stream hash differs for {seed.seed_id}")
        result[seed.seed_id] = calculated
    return result


def _csv_rows(path: Path, expected_header: Sequence[str]) -> Iterator[list[str]]:
    try:
        handle = path.open(encoding="utf-8", newline="")
    except OSError as error:
        raise AuditError(f"cannot read CSV {path}: {error}") from error
    with handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header != list(expected_header):
            raise AuditError(f"CSV header differs for {path}")
        for index, row in enumerate(reader):
            if len(row) != len(expected_header):
                raise AuditError(f"CSV row {index} has wrong width in {path}")
            yield row


def _validate_exports(connection: sqlite3.Connection, paths: AuditPaths) -> None:
    sentinel = object()
    provenance_database = connection.execute(
        """
        SELECT o.seed_id, o.pair_index, o.first_vertex, o.second_vertex,
               o.toggle_action, o.raw_graph6, o.canonical_graph6, o.category
        FROM origins AS o JOIN seeds AS s ON s.seed_id = o.seed_id
        ORDER BY s.seed_index, o.pair_index
        """
    )
    for index, (database_row, csv_row) in enumerate(
        zip_longest(
            provenance_database,
            _csv_rows(paths.provenance_csv, PROVENANCE_HEADER),
            fillvalue=sentinel,
        )
    ):
        if database_row is sentinel or csv_row is sentinel:
            raise AuditError("provenance CSV row count differs from database")
        expected = ["" if value is None else str(value) for value in database_row]
        if csv_row != expected:
            raise AuditError(f"provenance CSV differs at row {index}")

    unique_database = connection.execute(
        """
        SELECT graph6, n, m, connected, origin_count, first_seed_id,
               first_pair_index, first_raw_graph6, gamma_a, gamma_b,
               alpha_a, alpha_b, gamma_infinity_a, gamma_infinity_b,
               theta_a, theta_b, category, family_size, family_sha256
        FROM canonical_graphs ORDER BY n, graph6
        """
    )
    for index, (database_row, csv_row) in enumerate(
        zip_longest(
            unique_database,
            _csv_rows(paths.unique_csv, UNIQUE_HEADER),
            fillvalue=sentinel,
        )
    ):
        if database_row is sentinel or csv_row is sentinel:
            raise AuditError("unique CSV row count differs from database")
        expected = ["" if value is None else str(value) for value in database_row]
        if csv_row != expected:
            raise AuditError(f"unique CSV differs at row {index}")


def _report_payload(
    *,
    status: str,
    paths: AuditPaths,
    binding: Mapping[str, object],
    binding_sha256: str,
    verified: int,
    chain: str,
    unique_count: int | None,
    started_unix: float,
    started_counter: float,
    state_sha256: str,
    category_counts: Mapping[str, int] | None = None,
    stream_hashes: Mapping[str, str] | None = None,
) -> dict[str, object]:
    return {
        "format": AUDIT_FORMAT,
        "status": status,
        "passed": status == "complete",
        "warning": (
            "This certifies only the delimited 25,641-origin edge-toggle "
            "artifact; it does not resolve the universal gamma-theta conjecture."
        ),
        "expected_origins": EXPECTED_ORIGINS,
        "verified_origins": verified,
        "unique_canonical_graphs": unique_count,
        "origin_chain_sha256": chain,
        "unique_category_counts": (
            None if category_counts is None else dict(category_counts)
        ),
        "seed_canonical_stream_sha256": (
            None if stream_hashes is None else dict(stream_hashes)
        ),
        "binding": dict(binding),
        "binding_sha256": binding_sha256,
        "state_database": str(paths.state_database),
        "state_database_sha256": state_sha256,
        "checker_python": platform.python_version(),
        "started_unix": started_unix,
        "finished_unix": time.time(),
        "wall_seconds": time.perf_counter() - started_counter,
        "resource_usage": _resource_usage(),
        "checker_limitations": [
            (
                "The checker proves coverage, raw reconstruction, and an exact "
                "isomorphism from every raw toggle to its stored key; it does "
                "not independently derive a canonical normal form."
            ),
            (
                "Stored parameter equalities and category logic are checked "
                "for consistency, but gamma, alpha, eternal domination, and "
                "theta are left to the separately written mathematical checker."
            ),
            (
                "The production ledger has one evaluation row per key but no "
                "call trace, so it cannot prove the exact number of evaluator "
                "function invocations."
            ),
        ],
    }


def run_audit(
    *,
    paths: AuditPaths,
    checkpoint_interval: int = 256,
    max_new_origins: int | None = None,
    wall_limit_seconds: float = 2700.0,
    memory_limit_mib: float = 1024.0,
) -> AuditOutcome:
    """Audit a completed production run, resuming an independent receipt log."""

    if type(checkpoint_interval) is not int or checkpoint_interval < 1:
        raise AuditError("checkpoint interval must be a positive integer")
    if max_new_origins is not None and (
        type(max_new_origins) is not int or max_new_origins < 1
    ):
        raise AuditError("max-new-origins must be a positive integer")
    wall_limit = _positive_finite(wall_limit_seconds, "audit wall limit")
    memory_limit = _positive_finite(memory_limit_mib, "audit memory limit")
    paths = _validate_path_roles(paths)
    started_unix = time.time()
    started_counter = time.perf_counter()

    seeds = load_seed_universe(paths)
    expected = _expected_origins(seeds)
    database_sha256 = sha256_file(paths.database)
    checkpoint_sha256 = sha256_file(paths.checkpoint)
    connection = _open_immutable_database(paths.database)
    state: sqlite3.Connection | None = None
    status = "in_progress"
    verified = 0
    chain = sha256(CHAIN_DOMAIN).hexdigest()
    counts: dict[str, tuple[int, int, int, str, int, str]] = {}
    category_counts: dict[str, int] | None = None
    stream_hashes: dict[str, str] | None = None
    binding: dict[str, object]
    binding_sha256: str
    try:
        raw_config, stored_config_digest, candidate_marker = _database_metadata(
            connection
        )
        configuration, configuration_sha256, search_manifest = (
            _validate_configuration(
                paths=paths,
                raw_json=raw_config,
                stored_digest=stored_config_digest,
            )
        )
        checkpoint = _validate_checkpoint(
            paths=paths,
            checkpoint=strict_json_file(paths.checkpoint),
            configuration=configuration,
            configuration_sha256=configuration_sha256,
            database_sha256=database_sha256,
            seeds=seeds,
        )
        _validate_database_seed_rows(connection, seeds)
        _validate_no_candidate_freeze(
            connection, candidate_marker, paths.candidate_directory
        )
        binding, binding_sha256 = _audit_binding(
            paths=paths,
            configuration_sha256=configuration_sha256,
            database_sha256=database_sha256,
            checkpoint_sha256=checkpoint_sha256,
            search_manifest=search_manifest,
        )
        state = _connect_state(paths.state_database, binding, binding_sha256)
        production_rows = _production_origins(connection)
        verified, chain, counts, prior_status = _replay_state(
            state, expected, production_rows
        )
        if prior_status == "complete" and verified != EXPECTED_ORIGINS:
            raise AuditError("complete audit state has incomplete receipts")

        new_origins = 0
        batch_open = False
        while verified < EXPECTED_ORIGINS:
            if not batch_open:
                state.execute("BEGIN IMMEDIATE")
                batch_open = True
            origin_expected = expected[verified]
            row = production_rows[verified]
            action, raw_graph6, canonical_graph6, mapping = _validate_origin(
                origin_expected, row
            )
            global_index, seed, pair_index, first, second = origin_expected
            category = str(row[8])
            chain = _chain_step(
                chain,
                global_index=global_index,
                seed_index=seed.index,
                seed_id=seed.seed_id,
                pair_index=pair_index,
                first=first,
                second=second,
                action=action,
                raw_graph6=raw_graph6,
                canonical_graph6=canonical_graph6,
                category=category,
                mapping=mapping,
            )
            _store_origin_receipt(
                state,
                expected=origin_expected,
                action=action,
                raw_graph6=raw_graph6,
                canonical_graph6=canonical_graph6,
                category=category,
                mapping=mapping,
                chain=chain,
            )
            verified += 1
            new_origins += 1
            should_commit = (
                verified == EXPECTED_ORIGINS
                or verified % checkpoint_interval == 0
                or (
                    max_new_origins is not None
                    and new_origins >= max_new_origins
                )
            )
            if not should_commit:
                continue
            state.execute(
                """
                UPDATE progress
                SET status = 'in_progress', verified_origins = ?,
                    origin_chain_sha256 = ?
                WHERE singleton = 1
                """,
                (verified, chain),
            )
            state.commit()
            batch_open = False
            counts = _state_counts(state)
            if max_new_origins is not None and new_origins >= max_new_origins:
                status = "in_progress_bounded"
                break
            if time.perf_counter() - started_counter >= wall_limit:
                status = "in_progress_wall_limit"
                break
            usage = _resource_usage()
            if float(usage["maximum_resident_set_size_mib"]) > memory_limit:
                status = "in_progress_memory_limit"
                break
        if batch_open:
            state.rollback()
            raise AssertionError("uncommitted audit batch escaped processing loop")

        if verified == EXPECTED_ORIGINS:
            counts = _state_counts(state)
            category_counts = _validate_canonical_rows(connection, counts)
            stream_hashes = _validate_stream_hashes(
                connection, checkpoint, seeds, production_rows
            )
            _validate_exports(connection, paths)
            mismatch_binding, mismatch_digest = _audit_binding(
                paths=paths,
                configuration_sha256=configuration_sha256,
                database_sha256=sha256_file(paths.database),
                checkpoint_sha256=sha256_file(paths.checkpoint),
                search_manifest=_source_manifest(
                    paths.campaign_root, SEARCH_RUNTIME_PATHS
                ),
            )
            if mismatch_binding != binding or mismatch_digest != binding_sha256:
                raise AuditError("bound inputs changed while the audit was running")
            state.execute(
                """
                UPDATE progress SET status = 'complete',
                    verified_origins = ?, origin_chain_sha256 = ?
                WHERE singleton = 1
                """,
                (verified, chain),
            )
            state.commit()
            status = "complete"
        elif status == "in_progress":
            status = "in_progress_checkpoint"
    finally:
        connection.close()
        if state is not None:
            state.close()

    state_sha256 = sha256_file(paths.state_database)
    unique_count = len(counts) if counts else (0 if verified == 0 else None)
    report = _report_payload(
        status=status,
        paths=paths,
        binding=binding,
        binding_sha256=binding_sha256,
        verified=verified,
        chain=chain,
        unique_count=unique_count,
        started_unix=started_unix,
        started_counter=started_counter,
        state_sha256=state_sha256,
        category_counts=category_counts,
        stream_hashes=stream_hashes,
    )
    _atomic_json(paths.report, report)
    return AuditOutcome(
        status=status,
        verified_origins=verified,
        expected_origins=EXPECTED_ORIGINS,
        unique_canonical_graphs=unique_count,
        report_path=str(paths.report),
        origin_chain_sha256=chain,
    )
