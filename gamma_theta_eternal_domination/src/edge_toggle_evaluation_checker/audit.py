"""Certificate-producing third mathematical audit of edge-toggle unique rows."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from hashlib import sha256
from itertools import zip_longest
import json
import os
from pathlib import Path, PurePosixPath
import platform
import resource
import sqlite3
import tempfile
import time
from typing import Iterator, Mapping, Sequence

from coverage_checker.graph import Graph, Graph6Error

from .math_core import (
    build_domination_proof,
    build_fixed_point_proof,
    deserialize_blockers,
    deserialize_rounds,
    serialize_blockers,
    serialize_rounds,
    verify_complete_empty_trace,
    verify_domination_proof,
)


FORMAT = "gamma-theta-edge-toggle-third-math-audit-v1"
CERTIFICATE_FORMAT = "gamma-theta-edge-toggle-third-math-certificates-v1"
EXPECTED_ROWS = 19_136
EXPECTED_ORIGINS = 25_641
EXPECTED_COVERAGE_REPORT_SHA256 = (
    "82c6918faec2105340205730a3e128d4be05b5c57190a58519e68b4cfe733679"
)
EXPECTED_PARSER_SHA256 = (
    "cb60b10295aaa1e0a723e9fb3b1ecf497c461082bdcc8066044a664b4d76e731"
)
SHA256_LENGTH = 64
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
TABLE_COLUMNS = {
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
    "canonical_graphs": ("graph6",) + UNIQUE_HEADER[1:],
    "origins": (
        "seed_id",
        "pair_index",
        "first_vertex",
        "second_vertex",
        "toggle_action",
        "raw_graph6",
        "canonical_graph6",
        "category",
    ),
}
SOURCE_PATHS = (
    "src/coverage_checker/graph.py",
    "src/edge_toggle_evaluation_checker/__init__.py",
    "src/edge_toggle_evaluation_checker/__main__.py",
    "src/edge_toggle_evaluation_checker/math_core.py",
    "src/edge_toggle_evaluation_checker/audit.py",
    "src/edge_toggle_evaluation_checker/cli.py",
    "src/edge_toggle_evaluation_checker/PROTOCOL.md",
    "tests/test_edge_toggle_evaluation_math.py",
    "tests/test_edge_toggle_evaluation_audit.py",
)
PARSER_PATH = "src/coverage_checker/graph.py"


class ThirdAuditError(RuntimeError):
    """A mathematical certificate or one of its byte bindings failed."""


@dataclass(frozen=True, slots=True)
class AuditPaths:
    campaign_root: Path
    database: Path
    checkpoint: Path
    provenance_csv: Path
    unique_csv: Path
    coverage_report: Path
    certificate: Path
    report: Path


@dataclass(frozen=True, slots=True)
class LedgerRow:
    index: int
    values: tuple[object, ...]
    graph: Graph

    @property
    def graph6(self) -> str:
        return str(self.values[0])


@dataclass(frozen=True, slots=True)
class AuditSummary:
    rows: int
    origins: int
    gamma_2_rows: int
    gamma_3_rows: int
    initial_dominating_configurations: int
    deletion_rounds: int
    deletion_records: int
    maximum_initial_configurations: int
    maximum_deletion_rounds: int
    row_stream_sha256: str
    stored_parameter_census: dict[str, int]


def _strict_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if not isinstance(key, str) or key in result:
            raise ThirdAuditError(f"duplicate or non-text JSON key: {key!r}")
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise ThirdAuditError(f"non-finite JSON value: {value}")


def strict_json_loads(text: str, label: str) -> object:
    try:
        return json.loads(
            text,
            object_pairs_hook=_strict_pairs,
            parse_constant=_reject_constant,
        )
    except (json.JSONDecodeError, UnicodeError, RecursionError) as error:
        raise ThirdAuditError(f"invalid JSON in {label}: {error}") from error


def strict_json_file(path: Path) -> object:
    try:
        return strict_json_loads(path.read_text(encoding="utf-8"), str(path))
    except OSError as error:
        raise ThirdAuditError(f"cannot read JSON {path}: {error}") from error


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
        raise ThirdAuditError(f"value is not canonical JSON: {error}") from error


def _json_sha256(value: object) -> str:
    return sha256(_canonical_json(value)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = sha256()
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1 << 20), b""):
                digest.update(block)
    except OSError as error:
        raise ThirdAuditError(f"cannot hash {path}: {error}") from error
    return digest.hexdigest()


def _require_mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ThirdAuditError(f"{label} is not an object")
    return value


def _require_int(value: object, label: str, minimum: int | None = None) -> int:
    if type(value) is not int or (minimum is not None and value < minimum):
        raise ThirdAuditError(f"{label} is not a valid integer")
    return value


def _require_sha(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != SHA256_LENGTH
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ThirdAuditError(f"{label} is not a lowercase SHA-256")
    return value


def _resolve(path: Path) -> Path:
    try:
        return path.expanduser().resolve()
    except OSError as error:
        raise ThirdAuditError(f"cannot resolve {path}: {error}") from error


def _regular(path: Path, label: str) -> Path:
    resolved = _resolve(path)
    if not resolved.is_file():
        raise ThirdAuditError(f"{label} is not a regular file: {resolved}")
    return resolved


def _source_manifest(root: Path) -> tuple[tuple[str, str], ...]:
    root = _resolve(root)
    records: list[tuple[str, str]] = []
    for relative in SOURCE_PATHS:
        pure = PurePosixPath(relative)
        if pure.is_absolute() or "." in pure.parts or ".." in pure.parts:
            raise ThirdAuditError(f"unsafe source path: {relative}")
        path = _regular(root / Path(*pure.parts), f"source {relative}")
        try:
            path.relative_to(root)
        except ValueError as error:
            raise ThirdAuditError(f"source escapes root: {relative}") from error
        records.append((relative, sha256_file(path)))
    return tuple(records)


def _manifest_sha256(records: Sequence[tuple[str, str]]) -> str:
    digest = sha256()
    for relative, file_digest in records:
        digest.update(f"{relative} {file_digest}\n".encode("ascii"))
    return digest.hexdigest()


def _atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
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
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _rss_mib() -> float:
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def _validate_paths(paths: AuditPaths, *, verify_only: bool) -> AuditPaths:
    resolved = AuditPaths(
        **{
            key: _resolve(value)
            for key, value in asdict(paths).items()
        }
    )
    inputs = {
        "database": resolved.database,
        "checkpoint": resolved.checkpoint,
        "provenance": resolved.provenance_csv,
        "unique": resolved.unique_csv,
        "coverage report": resolved.coverage_report,
    }
    outputs = {
        "certificate": resolved.certificate,
        "report": resolved.report,
    }
    reverse: dict[Path, list[str]] = {}
    for role, path in {**inputs, **outputs}.items():
        reverse.setdefault(path, []).append(role)
    collisions = {path: roles for path, roles in reverse.items() if len(roles) > 1}
    if collisions:
        raise ThirdAuditError(f"path roles alias: {collisions!r}")
    for role, path in inputs.items():
        _regular(path, role)
    if verify_only:
        _regular(resolved.certificate, "certificate")
        _regular(resolved.report, "report")
    trusted = {
        _resolve(resolved.campaign_root / relative)
        for relative in SOURCE_PATHS + (PARSER_PATH,)
    }
    for role, path in outputs.items():
        if path in trusted:
            raise ThirdAuditError(f"{role} aliases trusted source: {path}")
    return resolved


def _reject_companions(database: Path) -> None:
    for suffix in ("-wal", "-shm", "-journal"):
        companion = Path(str(database) + suffix)
        if companion.exists():
            raise ThirdAuditError(f"live SQLite companion exists: {companion}")


def _open_database(database: Path) -> sqlite3.Connection:
    _reject_companions(database)
    try:
        connection = sqlite3.connect(
            database.as_uri() + "?mode=ro&immutable=1", uri=True
        )
        connection.execute("PRAGMA query_only=ON")
        return connection
    except sqlite3.Error as error:
        raise ThirdAuditError(f"cannot open immutable database: {error}") from error


def _validate_database(connection: sqlite3.Connection) -> None:
    try:
        version = connection.execute("PRAGMA user_version").fetchone()
        if version != (1,):
            raise ThirdAuditError(f"database schema version differs: {version}")
        if tuple(connection.execute("PRAGMA integrity_check")) != (("ok",),):
            raise ThirdAuditError("database integrity check failed")
        if tuple(connection.execute("PRAGMA foreign_key_check")):
            raise ThirdAuditError("database foreign-key check failed")
        tables = tuple(
            row[0]
            for row in connection.execute(
                """
                SELECT name FROM sqlite_master
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name
                """
            )
        )
        if tables != tuple(sorted(TABLE_COLUMNS)):
            raise ThirdAuditError(f"database table set differs: {tables!r}")
        for table, expected in TABLE_COLUMNS.items():
            actual = tuple(
                row[1]
                for row in connection.execute(f'PRAGMA table_info("{table}")')
            )
            if actual != expected:
                raise ThirdAuditError(f"columns differ for {table}: {actual!r}")
    except sqlite3.Error as error:
        raise ThirdAuditError(f"database validation failed: {error}") from error


def _validate_checkpoint(paths: AuditPaths, hashes: Mapping[str, str]) -> None:
    checkpoint = _require_mapping(
        strict_json_file(paths.checkpoint), "search checkpoint"
    )
    if checkpoint.get("status") != "complete":
        raise ThirdAuditError("search checkpoint is not complete")
    if checkpoint.get("database") != str(paths.database):
        raise ThirdAuditError("search checkpoint database path differs")
    if checkpoint.get("database_sha256") != hashes["database"]:
        raise ThirdAuditError("search checkpoint database hash differs")
    if (
        checkpoint.get("raw_expected") != EXPECTED_ORIGINS
        or checkpoint.get("raw_processed") != EXPECTED_ORIGINS
    ):
        raise ThirdAuditError("search checkpoint origin counts differ")
    candidate = _require_mapping(
        checkpoint.get("candidate_state"), "checkpoint candidate state"
    )
    if candidate.get("pending") is not False or checkpoint.get(
        "candidate_reference"
    ) is not None:
        raise ThirdAuditError("search checkpoint has a pending candidate")
    coverage = _require_mapping(
        checkpoint.get("coverage_audit"), "checkpoint coverage"
    )
    if (
        coverage.get("passed") is not True
        or coverage.get("errors") != []
        or coverage.get("raw_expected") != EXPECTED_ORIGINS
        or coverage.get("raw_origins") != EXPECTED_ORIGINS
        or coverage.get("stored_origin_multiplicity") != EXPECTED_ORIGINS
    ):
        raise ThirdAuditError("search checkpoint internal coverage differs")
    expected_exports = {
        str(paths.provenance_csv): hashes["provenance_csv"],
        str(paths.unique_csv): hashes["unique_csv"],
    }
    if checkpoint.get("output_sha256") != expected_exports:
        raise ThirdAuditError("search checkpoint export hashes differ")


def _validate_coverage_report(
    paths: AuditPaths, hashes: Mapping[str, str]
) -> dict[str, object]:
    if hashes["coverage_report"] != EXPECTED_COVERAGE_REPORT_SHA256:
        raise ThirdAuditError("edge-toggle coverage-report pin differs")
    report = _require_mapping(
        strict_json_file(paths.coverage_report), "coverage report"
    )
    if (
        report.get("format") != "gamma-theta-edge-toggle-postrun-audit-v1"
        or report.get("passed") is not True
        or report.get("expected_origins") != EXPECTED_ORIGINS
        or report.get("verified_origins") != EXPECTED_ORIGINS
        or report.get("unique_canonical_graphs") != EXPECTED_ROWS
    ):
        raise ThirdAuditError("coverage report does not certify the expected ledger")
    binding = _require_mapping(report.get("binding"), "coverage binding")
    if _json_sha256(binding) != report.get("binding_sha256"):
        raise ThirdAuditError("coverage report binding digest differs")
    expected = {
        "search_database_sha256": hashes["database"],
        "search_checkpoint_sha256": hashes["checkpoint"],
        "provenance_csv_sha256": hashes["provenance_csv"],
        "unique_csv_sha256": hashes["unique_csv"],
    }
    for key, value in expected.items():
        if binding.get(key) != value:
            raise ThirdAuditError(f"coverage report does not bind {key}")
    return report


def collect_binding(paths: AuditPaths) -> dict[str, object]:
    parser = _regular(paths.campaign_root / PARSER_PATH, "strict graph6 parser")
    parser_hash = sha256_file(parser)
    if parser_hash != EXPECTED_PARSER_SHA256:
        raise ThirdAuditError("strict graph6 parser hash differs from frozen pin")
    hashes = {
        "database": sha256_file(paths.database),
        "checkpoint": sha256_file(paths.checkpoint),
        "provenance_csv": sha256_file(paths.provenance_csv),
        "unique_csv": sha256_file(paths.unique_csv),
        "coverage_report": sha256_file(paths.coverage_report),
    }
    _validate_checkpoint(paths, hashes)
    coverage = _validate_coverage_report(paths, hashes)
    source_manifest = _source_manifest(paths.campaign_root)
    return {
        "format": FORMAT,
        "expected_rows": EXPECTED_ROWS,
        "expected_origins": EXPECTED_ORIGINS,
        "paths": {
            "database": str(paths.database),
            "checkpoint": str(paths.checkpoint),
            "provenance_csv": str(paths.provenance_csv),
            "unique_csv": str(paths.unique_csv),
            "coverage_report": str(paths.coverage_report),
        },
        "sha256": hashes,
        "coverage_binding_sha256": coverage["binding_sha256"],
        "coverage_origin_chain_sha256": coverage["origin_chain_sha256"],
        "parser": {"path": PARSER_PATH, "sha256": parser_hash},
        "checker_source_manifest": [list(item) for item in source_manifest],
        "checker_source_set_sha256": _manifest_sha256(source_manifest),
    }


def _as_database_text(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise ThirdAuditError(f"{label} is not SQLite text")
    return value


def _as_database_int(value: object, label: str) -> int:
    if type(value) is not int:
        raise ThirdAuditError(f"{label} is not an SQLite integer")
    return value


def _csv_value(value: object) -> str:
    if value is None:
        return ""
    if type(value) is int:
        return str(value)
    if isinstance(value, str):
        return value
    raise ThirdAuditError(f"unsupported CSV value type: {type(value)}")


def iter_ledger_rows(
    connection: sqlite3.Connection, unique_csv: Path
) -> Iterator[LedgerRow]:
    try:
        cursor = connection.execute(
            """
            SELECT graph6, n, m, connected, origin_count, first_seed_id,
                   first_pair_index, first_raw_graph6, gamma_a, gamma_b,
                   alpha_a, alpha_b, gamma_infinity_a, gamma_infinity_b,
                   theta_a, theta_b, category, family_size, family_sha256
            FROM canonical_graphs ORDER BY n, graph6
            """
        )
        handle = unique_csv.open("r", encoding="utf-8", newline="")
    except (sqlite3.Error, OSError) as error:
        raise ThirdAuditError(f"cannot stream unique ledger: {error}") from error
    try:
        reader = csv.reader(handle, strict=True)
        try:
            header = tuple(next(reader))
        except StopIteration as error:
            raise ThirdAuditError("unique CSV is empty") from error
        if header != UNIQUE_HEADER:
            raise ThirdAuditError(f"unique CSV header differs: {header!r}")
        sentinel = object()
        count = 0
        for database_row, csv_row in zip_longest(
            cursor, reader, fillvalue=sentinel
        ):
            if database_row is sentinel or csv_row is sentinel:
                raise ThirdAuditError("unique CSV/database row counts differ")
            if not isinstance(database_row, tuple) or not isinstance(csv_row, list):
                raise ThirdAuditError("unique ledger cursor returned malformed row")
            expected_csv = tuple(_csv_value(value) for value in database_row)
            if tuple(csv_row) != expected_csv:
                raise ThirdAuditError(f"unique CSV differs at row {count}")
            graph6 = _as_database_text(database_row[0], "canonical graph6")
            order = _as_database_int(database_row[1], "canonical order")
            size = _as_database_int(database_row[2], "canonical size")
            if (
                _as_database_int(database_row[3], "connected") != 1
                or _as_database_int(database_row[4], "origin count") < 1
            ):
                raise ThirdAuditError(f"row {count} is disconnected or unused")
            try:
                graph = Graph.from_graph6(graph6)
            except (Graph6Error, ValueError, TypeError) as error:
                raise ThirdAuditError(f"row {count} has invalid graph6") from error
            if (
                graph.order != order
                or graph.size != size
                or graph.to_graph6() != graph6
            ):
                raise ThirdAuditError(f"row {count} graph metadata differs")
            for left, right, name in (
                (8, 9, "gamma"),
                (10, 11, "alpha"),
                (12, 13, "gamma infinity"),
                (14, 15, "theta"),
            ):
                first = _as_database_int(database_row[left], f"row {count} {name} A")
                second = _as_database_int(database_row[right], f"row {count} {name} B")
                if first != second:
                    raise ThirdAuditError(f"row {count} stored {name} disagrees")
            _as_database_text(database_row[16], "category")
            _as_database_int(database_row[17], "family size")
            _require_sha(database_row[18], "family hash")
            yield LedgerRow(count, database_row, graph)
            count += 1
        if count != EXPECTED_ROWS:
            raise ThirdAuditError(
                f"unique ledger has {count} rows, expected {EXPECTED_ROWS}"
            )
    except (OSError, UnicodeError, csv.Error, sqlite3.Error) as error:
        if isinstance(error, ThirdAuditError):
            raise
        raise ThirdAuditError(f"cannot stream unique ledger: {error}") from error
    finally:
        handle.close()
        cursor.close()


def _parameter_key(row: LedgerRow) -> str:
    values = row.values
    return (
        f"gamma={values[8]},alpha={values[10]},"
        f"gamma_infinity={values[12]},theta={values[14]},"
        f"category={values[16]}"
    )


def _check_reconciliation(row: LedgerRow, gamma: int) -> None:
    values = row.values
    stored_gamma = _as_database_int(values[8], "stored gamma")
    stored_eternal = _as_database_int(values[12], "stored gamma infinity")
    category = _as_database_text(values[16], "stored category")
    if stored_gamma != gamma:
        raise ThirdAuditError(
            f"row {row.index} independently has gamma={gamma}, "
            f"stored gamma={stored_gamma}"
        )
    if stored_eternal <= gamma or category != "gamma_below_eternal":
        raise ThirdAuditError(f"row {row.index} stored category is inconsistent")


def _base_record(row: LedgerRow) -> dict[str, object]:
    return {
        "graph6": row.graph6,
        "ledger_row_sha256": _json_sha256(list(row.values)),
        "row_index": row.index,
        "type": "row",
    }


def generate_record(row: LedgerRow) -> dict[str, object]:
    domination = build_domination_proof(row.graph)
    _check_reconciliation(row, domination.gamma)
    fixed_point = build_fixed_point_proof(row.graph, domination.gamma)
    if fixed_point.initial_count < 1:
        raise ThirdAuditError(
            f"row {row.index} has no initial dominating configuration"
        )
    if fixed_point.surviving_configurations:
        raise ThirdAuditError(
            f"row {row.index} has a nonempty k=gamma fixed point"
        )
    if not verify_complete_empty_trace(
        row.graph,
        domination.gamma,
        fixed_point.deletion_rounds,
        fixed_point.trace_sha256,
        fixed_point.initial_count,
    ):
        raise ThirdAuditError(f"row {row.index} generated trace failed replay")
    record = _base_record(row)
    record.update(
        {
            "deletion_rounds": serialize_rounds(
                fixed_point.deletion_rounds
            ),
            "deletion_trace_sha256": fixed_point.trace_sha256,
            "dominating_witness_mask": domination.dominating_witness_mask,
            "gamma": domination.gamma,
            "initial_dominating_configurations": fixed_point.initial_count,
            "lower_blockers": serialize_blockers(domination.lower_blockers),
        }
    )
    return record


ROW_KEYS = {
    "deletion_rounds",
    "deletion_trace_sha256",
    "dominating_witness_mask",
    "gamma",
    "graph6",
    "initial_dominating_configurations",
    "ledger_row_sha256",
    "lower_blockers",
    "row_index",
    "type",
}


def verify_record(row: LedgerRow, value: object) -> tuple[int, int, int]:
    record = _require_mapping(value, f"certificate row {row.index}")
    if set(record) != ROW_KEYS:
        raise ThirdAuditError(f"certificate row {row.index} key set differs")
    for key, expected in _base_record(row).items():
        if record.get(key) != expected:
            raise ThirdAuditError(f"certificate row {row.index} false {key}")
    gamma = _require_int(record.get("gamma"), "certificate gamma")
    dominating = _require_int(
        record.get("dominating_witness_mask"), "dominating witness"
    )
    try:
        blockers = deserialize_blockers(record.get("lower_blockers"))
        rounds = deserialize_rounds(record.get("deletion_rounds"))
    except ValueError as error:
        raise ThirdAuditError(
            f"certificate row {row.index} malformed proof payload"
        ) from error
    if not verify_domination_proof(row.graph, gamma, dominating, blockers):
        raise ThirdAuditError(
            f"certificate row {row.index} domination proof is false"
        )
    _check_reconciliation(row, gamma)
    initial = _require_int(
        record.get("initial_dominating_configurations"),
        "initial configuration count",
        minimum=1,
    )
    trace_hash = _require_sha(
        record.get("deletion_trace_sha256"), "deletion trace hash"
    )
    if (
        sum(len(round_) for round_ in rounds) != initial
        or not verify_complete_empty_trace(
            row.graph, gamma, rounds, trace_hash, initial
        )
    ):
        raise ThirdAuditError(
            f"certificate row {row.index} empty fixed-point proof is false"
        )
    return gamma, initial, len(rounds)


class _SummaryBuilder:
    def __init__(self) -> None:
        self.rows = 0
        self.origins = 0
        self.gamma_2_rows = 0
        self.gamma_3_rows = 0
        self.initial = 0
        self.rounds = 0
        self.deletions = 0
        self.maximum_initial = 0
        self.maximum_rounds = 0
        self.parameters: dict[str, int] = {}

    def add(
        self, row: LedgerRow, gamma: int, initial: int, rounds: int
    ) -> None:
        self.rows += 1
        self.origins += _as_database_int(row.values[4], "origin count")
        if gamma == 2:
            self.gamma_2_rows += 1
        elif gamma == 3:
            self.gamma_3_rows += 1
        else:
            raise ThirdAuditError("independent gamma outside two or three")
        self.initial += initial
        self.rounds += rounds
        self.deletions += initial
        self.maximum_initial = max(self.maximum_initial, initial)
        self.maximum_rounds = max(self.maximum_rounds, rounds)
        key = _parameter_key(row)
        self.parameters[key] = self.parameters.get(key, 0) + 1

    def finish(self, stream_hash: str) -> AuditSummary:
        if self.rows != EXPECTED_ROWS or self.origins != EXPECTED_ORIGINS:
            raise ThirdAuditError(
                f"summary universe differs: rows={self.rows}, "
                f"origins={self.origins}"
            )
        return AuditSummary(
            rows=self.rows,
            origins=self.origins,
            gamma_2_rows=self.gamma_2_rows,
            gamma_3_rows=self.gamma_3_rows,
            initial_dominating_configurations=self.initial,
            deletion_rounds=self.rounds,
            deletion_records=self.deletions,
            maximum_initial_configurations=self.maximum_initial,
            maximum_deletion_rounds=self.maximum_rounds,
            row_stream_sha256=stream_hash,
            stored_parameter_census=dict(sorted(self.parameters.items())),
        )


def _write_json_line(handle: object, value: object) -> bytes:
    line = _canonical_json(value) + b"\n"
    handle.write(line)  # type: ignore[attr-defined]
    return line


def _header(binding: Mapping[str, object]) -> dict[str, object]:
    return {
        "binding": dict(binding),
        "binding_sha256": _json_sha256(binding),
        "expected_rows": EXPECTED_ROWS,
        "format": CERTIFICATE_FORMAT,
        "type": "header",
    }


def generate_certificate(
    connection: sqlite3.Connection,
    unique_csv: Path,
    destination: Path,
    binding: Mapping[str, object],
) -> AuditSummary:
    builder = _SummaryBuilder()
    row_digest = sha256()
    with destination.open("wb") as handle:
        _write_json_line(handle, _header(binding))
        for row in iter_ledger_rows(connection, unique_csv):
            record = generate_record(row)
            line = _write_json_line(handle, record)
            row_digest.update(line)
            gamma = int(record["gamma"])
            initial = int(record["initial_dominating_configurations"])
            rounds = len(record["deletion_rounds"])  # type: ignore[arg-type]
            builder.add(row, gamma, initial, rounds)
        summary = builder.finish(row_digest.hexdigest())
        footer = {
            "format": CERTIFICATE_FORMAT,
            "summary": asdict(summary),
            "type": "footer",
        }
        _write_json_line(handle, footer)
        handle.flush()
        os.fsync(handle.fileno())
    return summary


def _read_json_line(handle: object, label: str) -> tuple[object, bytes]:
    line = handle.readline()  # type: ignore[attr-defined]
    if not isinstance(line, bytes) or not line:
        raise ThirdAuditError(f"certificate is truncated at {label}")
    if not line.endswith(b"\n") or line in (b"\n", b"\r\n"):
        raise ThirdAuditError(f"certificate line is malformed at {label}")
    try:
        text = line.decode("ascii")
    except UnicodeError as error:
        raise ThirdAuditError(f"certificate is non-ASCII at {label}") from error
    value = strict_json_loads(text, label)
    if _canonical_json(value) + b"\n" != line:
        raise ThirdAuditError(f"certificate line is noncanonical at {label}")
    return value, line


def verify_certificate(
    connection: sqlite3.Connection,
    unique_csv: Path,
    certificate: Path,
    binding: Mapping[str, object],
) -> AuditSummary:
    builder = _SummaryBuilder()
    row_digest = sha256()
    try:
        handle = certificate.open("rb")
    except OSError as error:
        raise ThirdAuditError(f"cannot open certificate: {error}") from error
    with handle:
        header_value, _ = _read_json_line(handle, "header")
        if header_value != _header(binding):
            raise ThirdAuditError("certificate header binding differs")
        for row in iter_ledger_rows(connection, unique_csv):
            value, line = _read_json_line(handle, f"row {row.index}")
            gamma, initial, rounds = verify_record(row, value)
            row_digest.update(line)
            builder.add(row, gamma, initial, rounds)
        summary = builder.finish(row_digest.hexdigest())
        footer_value, _ = _read_json_line(handle, "footer")
        expected_footer = {
            "format": CERTIFICATE_FORMAT,
            "summary": asdict(summary),
            "type": "footer",
        }
        if footer_value != expected_footer:
            raise ThirdAuditError("certificate footer summary differs")
        if handle.read(1):
            raise ThirdAuditError("certificate has trailing content")
    return summary


def _validate_inputs_unchanged(
    paths: AuditPaths, initial_binding: Mapping[str, object]
) -> None:
    if collect_binding(paths) != initial_binding:
        raise ThirdAuditError("a bound input or checker source changed during audit")


def _report_core(
    *,
    paths: AuditPaths,
    binding: Mapping[str, object],
    summary: AuditSummary,
) -> dict[str, object]:
    return {
        "format": FORMAT,
        "status": "complete",
        "passed": True,
        "scope": (
            "All 19,136 canonical rows in the completed edge-toggle unique "
            "ledger; this is not all graphs of order 12."
        ),
        "binding": dict(binding),
        "binding_sha256": _json_sha256(binding),
        "certificate_path": str(paths.certificate),
        "certificate_sha256": sha256_file(paths.certificate),
        "certificate_size_bytes": paths.certificate.stat().st_size,
        "summary": asdict(summary),
        "model": {
            "attacks": "unoccupied vertices only",
            "movement": "exactly one guard along one edge to the attack",
            "configurations": "ordinary vertex subsets",
            "successor_requirement": "successor dominates and remains active",
            "fixed_point": "complete simultaneous greatest-fixed-point deletion",
        },
        "limitations": [
            (
                "This audit proves gamma < gamma_infinity for the 19,136 "
                "stored canonical keys; edge-toggle universe coverage is "
                "delegated to the separately bound coverage audit."
            ),
            (
                "It does not enumerate all graphs of order 11 or 12 and "
                "does not resolve the universal gamma-theta conjecture."
            ),
            (
                "Stored alpha, theta, and exact gamma-infinity values are "
                "reconciled as ledger fields but are not independently "
                "proved here; only gamma and gamma-infinity > gamma are."
            ),
            (
                "The strict graph6 parser is reused from a separately frozen "
                "file and is cryptographically pinned in the binding."
            ),
        ],
    }


def _validate_existing_report(
    paths: AuditPaths,
    binding: Mapping[str, object],
    summary: AuditSummary,
) -> dict[str, object]:
    report = _require_mapping(strict_json_file(paths.report), "third audit report")
    expected = _report_core(paths=paths, binding=binding, summary=summary)
    for key, value in expected.items():
        if report.get(key) != value:
            raise ThirdAuditError(f"existing report differs at {key}")
    if report.get("status") != "complete" or report.get("passed") is not True:
        raise ThirdAuditError("existing report is not passing")
    return report


def run_audit(paths: AuditPaths, *, verify_only: bool = False) -> dict[str, object]:
    started_wall = time.monotonic()
    started_unix = time.time()
    started_usage = resource.getrusage(resource.RUSAGE_SELF)
    resolved = _validate_paths(paths, verify_only=verify_only)
    binding = collect_binding(resolved)
    connection = _open_database(resolved.database)
    try:
        _validate_database(connection)
        if verify_only:
            replay_started = time.monotonic()
            summary = verify_certificate(
                connection,
                resolved.unique_csv,
                resolved.certificate,
                binding,
            )
            _validate_inputs_unchanged(resolved, binding)
            report = _validate_existing_report(
                resolved, binding, summary
            )
            return {
                "status": "complete",
                "mode": "verify-only",
                "rows": summary.rows,
                "certificate_sha256": report["certificate_sha256"],
                "replay_seconds": time.monotonic() - replay_started,
            }

        resolved.certificate.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=resolved.certificate.name + ".",
            suffix=".partial",
            dir=resolved.certificate.parent,
        )
        os.close(descriptor)
        temporary = Path(temporary_name)
        phase_seconds: dict[str, float] = {}
        try:
            phase = time.monotonic()
            generated = generate_certificate(
                connection, resolved.unique_csv, temporary, binding
            )
            phase_seconds["generation"] = time.monotonic() - phase
            phase = time.monotonic()
            first_replay = verify_certificate(
                connection, resolved.unique_csv, temporary, binding
            )
            phase_seconds["temporary_replay"] = time.monotonic() - phase
            if first_replay != generated:
                raise ThirdAuditError("temporary replay summary differs")
            os.replace(temporary, resolved.certificate)
            phase = time.monotonic()
            second_replay = verify_certificate(
                connection, resolved.unique_csv, resolved.certificate, binding
            )
            phase_seconds["installed_replay"] = time.monotonic() - phase
            if second_replay != generated:
                raise ThirdAuditError("installed replay summary differs")
        except BaseException:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
            raise
        _validate_inputs_unchanged(resolved, binding)
        usage = resource.getrusage(resource.RUSAGE_SELF)
        report = _report_core(
            paths=resolved, binding=binding, summary=generated
        )
        report.update(
            {
                "started_unix": started_unix,
                "finished_unix": time.time(),
                "wall_seconds": time.monotonic() - started_wall,
                "phase_seconds": phase_seconds,
                "resource_usage": {
                    "maximum_resident_set_size_mib": _rss_mib(),
                    "user_cpu_seconds": usage.ru_utime - started_usage.ru_utime,
                    "system_cpu_seconds": usage.ru_stime - started_usage.ru_stime,
                    "python": platform.python_version(),
                },
                "replay_count_during_generation": 2,
            }
        )
        _atomic_json(resolved.report, report)
        return report
    except (sqlite3.Error, OSError, UnicodeError) as error:
        if isinstance(error, ThirdAuditError):
            raise
        raise ThirdAuditError(f"third audit failed closed: {error}") from error
    finally:
        connection.close()


__all__ = [
    "AuditPaths",
    "AuditSummary",
    "CERTIFICATE_FORMAT",
    "EXPECTED_ORIGINS",
    "EXPECTED_ROWS",
    "FORMAT",
    "LedgerRow",
    "ThirdAuditError",
    "collect_binding",
    "generate_record",
    "iter_ledger_rows",
    "run_audit",
    "sha256_file",
    "strict_json_loads",
    "verify_record",
]
