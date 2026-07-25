"""Independent mathematical audit of every completed extension-search row.

This module deliberately imports no search module and neither verifier A nor
verifier B.  It uses only the frozen bounded graph6 parser from
``coverage_checker.graph`` and the definition-level routines in
``evaluation_checker.math_core``.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from hashlib import sha256
import json
import math
import os
from pathlib import Path, PurePosixPath
import platform
import re
import resource
import tempfile
import time
from typing import Iterable, Iterator, Mapping, Sequence

from coverage_checker.graph import Graph, Graph6Error

from .math_core import (
    configuration_from_mask,
    deserialize_deletion_rounds,
    dominating_configurations,
    failed_dominating_pair_witnesses,
    find_private_obstruction,
    first_dominating_set,
    first_independent_set,
    greatest_fixed_point,
    is_dominating,
    is_independent,
    mask_of,
    nonindependent_subset_witnesses,
    serialize_deletion_rounds,
    verify_empty_fixed_point_trace,
    verify_private_obstruction,
    witness_digest,
)


CERTIFICATE_FORMAT = "gamma-theta-extension-mathematical-certificates-v1"
REPORT_FORMAT = "gamma-theta-extension-mathematical-audit-v1"
EMPTY_SHA256 = sha256(b"").hexdigest()
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
DECIMAL_PATTERN = re.compile(r"(?:0|[1-9][0-9]*)\Z")
HOST_PATTERN = re.compile(r"MMV-[0-9]{3}\Z")

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

CATEGORY_GAMMA = "gamma_below_3"
CATEGORY_ALPHA = "alpha_above_3"
CATEGORY_ETERNAL = "eternal_false_without_private_obstruction"
CATEGORY_PRIVATE = "private_obstruction_eternal_false"
CATEGORIES = (
    CATEGORY_GAMMA,
    CATEGORY_ALPHA,
    CATEGORY_ETERNAL,
    CATEGORY_PRIVATE,
)

PRODUCTION_CATEGORY_COUNTS = (
    (CATEGORY_GAMMA, 52_447),
    (CATEGORY_ALPHA, 1_378),
    (CATEGORY_ETERNAL, 285),
    (CATEGORY_PRIVATE, 106),
)

CHECKER_SOURCE_PATHS = (
    "src/evaluation_checker/__init__.py",
    "src/evaluation_checker/math_core.py",
    "src/evaluation_checker/audit.py",
    "src/evaluation_checker/cli.py",
    "src/evaluation_checker/__main__.py",
    "src/evaluation_checker/PROTOCOL.md",
    "src/coverage_checker/graph.py",
)


class EvaluationAuditError(RuntimeError):
    """A binding, row, certificate, or mathematical check failed."""


@dataclass(frozen=True, slots=True)
class EvaluationPolicy:
    expected_rows: int
    expected_category_counts: tuple[tuple[str, int], ...]
    expected_origins: int | None = None
    allowed_orders: tuple[int, ...] | None = None

    def category_counts(self) -> dict[str, int]:
        result = dict(self.expected_category_counts)
        if (
            len(result) != len(self.expected_category_counts)
            or any(category not in CATEGORIES for category in result)
            or any(type(count) is not int or count < 0 for count in result.values())
            or sum(result.values()) != self.expected_rows
        ):
            raise EvaluationAuditError("invalid evaluation policy")
        return result


PRODUCTION_POLICY = EvaluationPolicy(
    expected_rows=54_216,
    expected_category_counts=PRODUCTION_CATEGORY_COUNTS,
    expected_origins=110_537,
    allowed_orders=(11, 12),
)


@dataclass(frozen=True, slots=True)
class EvaluationPaths:
    campaign_root: Path
    unique_csv: Path
    provenance_csv: Path
    database: Path
    checkpoint: Path
    coverage_report: Path
    coverage_state_database: Path
    certificate: Path
    report: Path


@dataclass(frozen=True, slots=True)
class EvaluationSummary:
    row_count: int
    category_counts: tuple[tuple[str, int], ...]
    record_lines_sha256: str
    certificate_sha256: str


@dataclass(frozen=True, slots=True)
class UniqueRow:
    index: int
    values: Mapping[str, str]
    graph: Graph
    gamma: int
    alpha: int
    category: str
    stored_private_obstruction: (
        tuple[int, int, tuple[tuple[int, int], ...]] | None
    )


def _strict_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if not isinstance(key, str) or key in result:
            raise EvaluationAuditError(
                f"duplicate or non-string JSON key: {key!r}"
            )
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise EvaluationAuditError(f"non-finite JSON constant: {value}")


def strict_json_loads(text: str, label: str) -> object:
    try:
        return json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except (json.JSONDecodeError, UnicodeError, RecursionError) as error:
        raise EvaluationAuditError(f"invalid JSON in {label}: {error}") from error


def strict_json_file(path: Path) -> object:
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise EvaluationAuditError(f"cannot read JSON {path}: {error}") from error
    try:
        return strict_json_loads(raw.decode("utf-8"), str(path))
    except UnicodeError as error:
        raise EvaluationAuditError(f"JSON is not UTF-8: {path}") from error


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
        raise EvaluationAuditError(
            f"value is not canonical-JSON serializable: {error}"
        ) from error


def _json_sha256(value: object) -> str:
    return sha256(_canonical_json(value)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = sha256()
    try:
        with path.open("rb") as handle:
            while block := handle.read(1024 * 1024):
                digest.update(block)
    except OSError as error:
        raise EvaluationAuditError(f"cannot hash {path}: {error}") from error
    return digest.hexdigest()


def _require_mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise EvaluationAuditError(f"{label} is not a JSON object")
    return value


def _require_exact_int(
    value: object, label: str, *, minimum: int | None = None
) -> int:
    if type(value) is not int or (minimum is not None and value < minimum):
        raise EvaluationAuditError(f"{label} is not a valid integer")
    return value


def _require_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or SHA256_PATTERN.fullmatch(value) is None:
        raise EvaluationAuditError(f"{label} is not a lowercase SHA-256")
    return value


def _parse_decimal(value: str, label: str, *, minimum: int = 0) -> int:
    if not isinstance(value, str) or DECIMAL_PATTERN.fullmatch(value) is None:
        raise EvaluationAuditError(f"{label} is not canonical decimal text")
    result = int(value)
    if result < minimum:
        raise EvaluationAuditError(f"{label} is below {minimum}")
    return result


def _resolve(path: Path) -> Path:
    try:
        return path.expanduser().resolve()
    except OSError as error:
        raise EvaluationAuditError(f"cannot resolve {path}: {error}") from error


def _require_file(path: Path, label: str) -> Path:
    result = _resolve(path)
    if not result.is_file():
        raise EvaluationAuditError(f"{label} is not a regular file: {result}")
    return result


def _manifest(
    campaign_root: Path, relative_paths: Sequence[str]
) -> tuple[tuple[str, str], ...]:
    root = _resolve(campaign_root)
    result: list[tuple[str, str]] = []
    seen: set[str] = set()
    for relative in relative_paths:
        if not isinstance(relative, str) or relative in seen:
            raise EvaluationAuditError(f"duplicate source path: {relative!r}")
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts or "." in pure.parts:
            raise EvaluationAuditError(f"unsafe source path: {relative!r}")
        seen.add(relative)
        source = _require_file(
            root / Path(*pure.parts), f"checker source {relative}"
        )
        try:
            source.relative_to(root)
        except ValueError as error:
            raise EvaluationAuditError(
                f"checker source escapes campaign root: {relative}"
            ) from error
        result.append((relative, sha256_file(source)))
    return tuple(result)


def _manifest_sha256(manifest: Sequence[tuple[str, str]]) -> str:
    digest = sha256()
    for relative, source_hash in manifest:
        digest.update(f"{relative} {source_hash}\n".encode("ascii"))
    return digest.hexdigest()


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


def _private_obstruction_from_json(
    text: str, label: str
) -> tuple[int, int, tuple[tuple[int, int], ...]]:
    parsed = _require_mapping(strict_json_loads(text, label), label)
    expected = {"attack", "failed_guards", "independent_set_mask"}
    if set(parsed) != expected:
        raise EvaluationAuditError(f"{label} has unexpected keys")
    state_mask = _require_exact_int(
        parsed["independent_set_mask"],
        f"{label}.independent_set_mask",
        minimum=0,
    )
    attacked = _require_exact_int(
        parsed["attack"], f"{label}.attack", minimum=0
    )
    raw_failed = parsed["failed_guards"]
    if not isinstance(raw_failed, list) or not raw_failed:
        raise EvaluationAuditError(f"{label}.failed_guards is not nonempty")
    failed: list[tuple[int, int]] = []
    for position, value in enumerate(raw_failed):
        record = _require_mapping(value, f"{label}.failed_guards[{position}]")
        if set(record) != {"guard", "newly_undominated"}:
            raise EvaluationAuditError(
                f"{label}.failed_guards[{position}] has unexpected keys"
            )
        failed.append(
            (
                _require_exact_int(
                    record["guard"],
                    f"{label}.failed_guards[{position}].guard",
                    minimum=0,
                ),
                _require_exact_int(
                    record["newly_undominated"],
                    f"{label}.failed_guards[{position}].newly_undominated",
                    minimum=0,
                ),
            )
        )
    return state_mask, attacked, tuple(failed)


def _iter_unique_rows(
    unique_csv: Path, policy: EvaluationPolicy
) -> Iterator[UniqueRow]:
    previous_graph6: str | None = None
    seen = 0
    try:
        with unique_csv.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle, strict=True)
            try:
                header = next(reader)
            except StopIteration as error:
                raise EvaluationAuditError("unique CSV is empty") from error
            if tuple(header) != UNIQUE_HEADER:
                raise EvaluationAuditError(
                    f"unique CSV header differs: {tuple(header)!r}"
                )
            for seen, fields in enumerate(reader, start=1):
                if len(fields) != len(UNIQUE_HEADER):
                    raise EvaluationAuditError(
                        f"unique CSV row {seen} has {len(fields)} fields"
                    )
                values = dict(zip(UNIQUE_HEADER, fields, strict=True))
                graph6 = values["canonical_graph6"]
                if previous_graph6 is not None and graph6 <= previous_graph6:
                    raise EvaluationAuditError(
                        f"unique CSV row {seen} is duplicate or out of order"
                    )
                previous_graph6 = graph6
                try:
                    graph = Graph.from_graph6(graph6)
                except (Graph6Error, ValueError) as error:
                    raise EvaluationAuditError(
                        f"row {seen} has invalid canonical graph6: {error}"
                    ) from error
                if graph.to_graph6() != graph6:
                    raise EvaluationAuditError(
                        f"row {seen} graph6 is not strict headerless form"
                    )
                order = _parse_decimal(values["n"], f"row {seen} n")
                size = _parse_decimal(values["m"], f"row {seen} m")
                if order != graph.order or size != graph.size:
                    raise EvaluationAuditError(
                        f"row {seen} graph order/size fields are false"
                    )
                if (
                    policy.allowed_orders is not None
                    and order not in policy.allowed_orders
                ):
                    raise EvaluationAuditError(
                        f"row {seen} order is outside policy"
                    )
                _parse_decimal(
                    values["origin_count"], f"row {seen} origin_count", minimum=1
                )
                if HOST_PATTERN.fullmatch(values["first_host_id"]) is None:
                    raise EvaluationAuditError(
                        f"row {seen} has malformed first_host_id"
                    )
                neighborhood_mask = _parse_decimal(
                    values["first_neighborhood_mask"],
                    f"row {seen} first_neighborhood_mask",
                    minimum=1,
                )
                if neighborhood_mask >= 1 << max(0, order - 1):
                    raise EvaluationAuditError(
                        f"row {seen} extension neighborhood is outside host"
                    )
                try:
                    raw_graph = Graph.from_graph6(values["first_raw_graph6"])
                except (Graph6Error, ValueError) as error:
                    raise EvaluationAuditError(
                        f"row {seen} has invalid first_raw_graph6: {error}"
                    ) from error
                if (
                    raw_graph.order != order
                    or raw_graph.to_graph6() != values["first_raw_graph6"]
                ):
                    raise EvaluationAuditError(
                        f"row {seen} first raw graph has wrong order/syntax"
                    )

                gamma = _parse_decimal(
                    values["gamma"], f"row {seen} gamma", minimum=1
                )
                alpha = _parse_decimal(
                    values["alpha"], f"row {seen} alpha", minimum=1
                )
                category = values["category"]
                if category not in CATEGORIES:
                    raise EvaluationAuditError(
                        f"row {seen} has unknown category {category!r}"
                    )
                stored_private = None
                empty_evaluation = (
                    values["eternal_a"],
                    values["eternal_b"],
                    values["family_a_size"],
                    values["family_b_size"],
                    values["family_a_sha256"],
                    values["family_b_sha256"],
                )
                if category == CATEGORY_GAMMA:
                    if (
                        gamma not in (1, 2)
                        or alpha not in (3, 4)
                        or values["private_obstruction_json"] != ""
                        or any(empty_evaluation)
                    ):
                        raise EvaluationAuditError(
                            f"row {seen} gamma category fields are inconsistent"
                        )
                elif category == CATEGORY_ALPHA:
                    if (
                        (gamma, alpha) != (3, 4)
                        or values["private_obstruction_json"] != ""
                        or any(empty_evaluation)
                    ):
                        raise EvaluationAuditError(
                            f"row {seen} alpha category fields are inconsistent"
                        )
                else:
                    expected_evaluation = (
                        "0",
                        "0",
                        "0",
                        "0",
                        EMPTY_SHA256,
                        EMPTY_SHA256,
                    )
                    if (
                        (gamma, alpha) != (3, 3)
                        or empty_evaluation != expected_evaluation
                    ):
                        raise EvaluationAuditError(
                            f"row {seen} eternal category fields are inconsistent"
                        )
                    private_text = values["private_obstruction_json"]
                    if category == CATEGORY_PRIVATE:
                        if not private_text:
                            raise EvaluationAuditError(
                                f"row {seen} lacks its private obstruction"
                            )
                        stored_private = _private_obstruction_from_json(
                            private_text,
                            f"row {seen} private_obstruction_json",
                        )
                    elif private_text:
                        raise EvaluationAuditError(
                            f"row {seen} has an unexpected private obstruction"
                        )
                yield UniqueRow(
                    index=seen,
                    values=values,
                    graph=graph,
                    gamma=gamma,
                    alpha=alpha,
                    category=category,
                    stored_private_obstruction=stored_private,
                )
    except (OSError, csv.Error, UnicodeError) as error:
        raise EvaluationAuditError(
            f"cannot read unique CSV {unique_csv}: {error}"
        ) from error
    if seen != policy.expected_rows:
        raise EvaluationAuditError(
            f"unique CSV has {seen} rows, expected {policy.expected_rows}"
        )


def _base_record(row: UniqueRow) -> dict[str, object]:
    return {
        "category": row.category,
        "graph6": row.values["canonical_graph6"],
        "row": row.index,
        "type": "row",
    }


def _generate_record(row: UniqueRow) -> dict[str, object]:
    graph = row.graph
    record = _base_record(row)
    if row.category == CATEGORY_GAMMA:
        witness = first_dominating_set(graph, 1, 2)
        if witness is None or len(witness) != row.gamma:
            raise EvaluationAuditError(
                f"row {row.index} recorded gamma below 3 is false"
            )
        record.update(
            {
                "dominating_mask": mask_of(witness),
                "recorded_gamma": row.gamma,
            }
        )
        return record

    pair_failures = failed_dominating_pair_witnesses(graph)
    dominating_triple = first_dominating_set(graph, 3, 3)
    if pair_failures is None or dominating_triple is None:
        raise EvaluationAuditError(
            f"row {row.index} does not have domination number 3"
        )
    record.update(
        {
            "dominating_mask": mask_of(dominating_triple),
            "pair_failure_count": len(pair_failures),
            "pair_failure_sha256": witness_digest(pair_failures),
        }
    )

    if row.category == CATEGORY_ALPHA:
        independent_four = first_independent_set(graph, 4)
        size_five_failures = nonindependent_subset_witnesses(graph, 5)
        if independent_four is None or size_five_failures is None:
            raise EvaluationAuditError(
                f"row {row.index} does not have independence number 4"
            )
        record.update(
            {
                "independent_mask": mask_of(independent_four),
                "size5_edge_count": len(size_five_failures),
                "size5_edge_sha256": witness_digest(size_five_failures),
            }
        )
        return record

    independent_three = first_independent_set(graph, 3)
    size_four_failures = nonindependent_subset_witnesses(graph, 4)
    if independent_three is None or size_four_failures is None:
        raise EvaluationAuditError(
            f"row {row.index} does not have independence number 3"
        )
    computed_private = find_private_obstruction(graph, 3)
    if row.category == CATEGORY_PRIVATE:
        if (
            computed_private is None
            or row.stored_private_obstruction is None
            or not verify_private_obstruction(
                graph, 3, row.stored_private_obstruction
            )
        ):
            raise EvaluationAuditError(
                f"row {row.index} private obstruction is false"
            )
    elif computed_private is not None:
        raise EvaluationAuditError(
            f"row {row.index} falsely claims no private obstruction"
        )

    fixed_point = greatest_fixed_point(graph, 3)
    if fixed_point.family or not verify_empty_fixed_point_trace(
        graph,
        3,
        fixed_point.deletion_rounds,
        fixed_point.trace_sha256,
    ):
        raise EvaluationAuditError(
            f"row {row.index} one-guard fixed point is not certified empty"
        )
    record.update(
        {
            "deletion_rounds": serialize_deletion_rounds(
                fixed_point.deletion_rounds
            ),
            "deletion_trace_sha256": fixed_point.trace_sha256,
            "independent_mask": mask_of(independent_three),
            "initial_dominating_configurations": fixed_point.initial_count,
            "private_obstruction_present": computed_private is not None,
            "size4_edge_count": len(size_four_failures),
            "size4_edge_sha256": witness_digest(size_four_failures),
        }
    )
    return record


def _expect_record_base(row: UniqueRow, record: Mapping[str, object]) -> None:
    for key, expected in _base_record(row).items():
        if record.get(key) != expected:
            raise EvaluationAuditError(
                f"certificate row {row.index} has false {key}"
            )


def _record_int(
    record: Mapping[str, object], key: str, row: UniqueRow, *, minimum: int = 0
) -> int:
    return _require_exact_int(
        record.get(key), f"certificate row {row.index} {key}", minimum=minimum
    )


def _record_sha(
    record: Mapping[str, object], key: str, row: UniqueRow
) -> str:
    return _require_sha256(
        record.get(key), f"certificate row {row.index} {key}"
    )


def _verify_record(row: UniqueRow, value: object) -> None:
    record = _require_mapping(value, f"certificate row {row.index}")
    _expect_record_base(row, record)
    graph = row.graph
    gamma_keys = {
        "category",
        "dominating_mask",
        "graph6",
        "recorded_gamma",
        "row",
        "type",
    }
    common_three_keys = {
        "category",
        "dominating_mask",
        "graph6",
        "pair_failure_count",
        "pair_failure_sha256",
        "row",
        "type",
    }
    if row.category == CATEGORY_GAMMA:
        if set(record) != gamma_keys or record.get("recorded_gamma") != row.gamma:
            raise EvaluationAuditError(
                f"certificate row {row.index} gamma record schema differs"
            )
        state = configuration_from_mask(
            graph, _record_int(record, "dominating_mask", row)
        )
        if len(state) != row.gamma or not is_dominating(graph, state):
            raise EvaluationAuditError(
                f"certificate row {row.index} has false domination witness"
            )
        if row.gamma == 2 and first_dominating_set(graph, 1, 1) is not None:
            raise EvaluationAuditError(
                f"certificate row {row.index} overlooks a dominating singleton"
            )
        return

    pair_failures = failed_dominating_pair_witnesses(graph)
    if pair_failures is None:
        raise EvaluationAuditError(
            f"certificate row {row.index} overlooks a dominating pair"
        )
    if (
        record.get("pair_failure_count") != len(pair_failures)
        or record.get("pair_failure_sha256") != witness_digest(pair_failures)
    ):
        raise EvaluationAuditError(
            f"certificate row {row.index} pair-exhaustion digest is false"
        )
    dominating = configuration_from_mask(
        graph, _record_int(record, "dominating_mask", row)
    )
    if len(dominating) != 3 or not is_dominating(graph, dominating):
        raise EvaluationAuditError(
            f"certificate row {row.index} has false dominating triple"
        )

    if row.category == CATEGORY_ALPHA:
        expected_keys = common_three_keys | {
            "independent_mask",
            "size5_edge_count",
            "size5_edge_sha256",
        }
        if set(record) != expected_keys:
            raise EvaluationAuditError(
                f"certificate row {row.index} alpha record schema differs"
            )
        independent = configuration_from_mask(
            graph, _record_int(record, "independent_mask", row)
        )
        size_five_failures = nonindependent_subset_witnesses(graph, 5)
        if (
            len(independent) != 4
            or not is_independent(graph, independent)
            or size_five_failures is None
            or record.get("size5_edge_count") != len(size_five_failures)
            or record.get("size5_edge_sha256")
            != witness_digest(size_five_failures)
        ):
            raise EvaluationAuditError(
                f"certificate row {row.index} alpha=4 proof is false"
            )
        return

    expected_keys = common_three_keys | {
        "deletion_rounds",
        "deletion_trace_sha256",
        "independent_mask",
        "initial_dominating_configurations",
        "private_obstruction_present",
        "size4_edge_count",
        "size4_edge_sha256",
    }
    if set(record) != expected_keys:
        raise EvaluationAuditError(
            f"certificate row {row.index} eternal record schema differs"
        )
    independent = configuration_from_mask(
        graph, _record_int(record, "independent_mask", row)
    )
    size_four_failures = nonindependent_subset_witnesses(graph, 4)
    if (
        len(independent) != 3
        or not is_independent(graph, independent)
        or size_four_failures is None
        or record.get("size4_edge_count") != len(size_four_failures)
        or record.get("size4_edge_sha256")
        != witness_digest(size_four_failures)
    ):
        raise EvaluationAuditError(
            f"certificate row {row.index} alpha=3 proof is false"
        )
    computed_private = find_private_obstruction(graph, 3)
    expected_private = row.category == CATEGORY_PRIVATE
    if (
        (computed_private is not None) != expected_private
        or record.get("private_obstruction_present") is not expected_private
    ):
        raise EvaluationAuditError(
            f"certificate row {row.index} private classification is false"
        )
    if expected_private and (
        row.stored_private_obstruction is None
        or not verify_private_obstruction(
            graph, 3, row.stored_private_obstruction
        )
    ):
        raise EvaluationAuditError(
            f"certificate row {row.index} stored private witness is false"
        )
    initial_count = len(dominating_configurations(graph, 3))
    if record.get("initial_dominating_configurations") != initial_count:
        raise EvaluationAuditError(
            f"certificate row {row.index} initial family size is false"
        )
    try:
        rounds = deserialize_deletion_rounds(
            graph, record.get("deletion_rounds")
        )
    except ValueError as error:
        raise EvaluationAuditError(
            f"certificate row {row.index} has malformed deletion trace"
        ) from error
    trace_sha256 = _record_sha(record, "deletion_trace_sha256", row)
    if (
        sum(len(round_) for round_ in rounds) != initial_count
        or not verify_empty_fixed_point_trace(
            graph, 3, rounds, trace_sha256
        )
    ):
        raise EvaluationAuditError(
            f"certificate row {row.index} fixed-point trace is false"
        )


def _header(
    binding: Mapping[str, object],
    source_manifest: Sequence[tuple[str, str]],
    policy: EvaluationPolicy,
) -> dict[str, object]:
    return {
        "binding": dict(binding),
        "checker_source_manifest": [list(record) for record in source_manifest],
        "checker_source_set_sha256": _manifest_sha256(source_manifest),
        "expected_category_counts": dict(policy.expected_category_counts),
        "expected_rows": policy.expected_rows,
        "format": CERTIFICATE_FORMAT,
        "type": "header",
    }


def _write_line(handle: object, value: object) -> bytes:
    payload = _canonical_json(value) + b"\n"
    handle.write(payload)  # type: ignore[attr-defined]
    return payload


def write_certificate(
    unique_csv: Path,
    certificate: Path,
    *,
    binding: Mapping[str, object],
    source_manifest: Sequence[tuple[str, str]],
    policy: EvaluationPolicy,
) -> EvaluationSummary:
    """Generate, replay-check, and atomically install a certificate stream."""

    expected_counts = policy.category_counts()
    certificate.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_text = tempfile.mkstemp(
        prefix=certificate.name + ".",
        suffix=".partial",
        dir=certificate.parent,
    )
    temporary = Path(temporary_text)
    row_digest = sha256()
    counts = {category: 0 for category in expected_counts}
    row_count = 0
    try:
        with os.fdopen(descriptor, "wb") as handle:
            _write_line(handle, _header(binding, source_manifest, policy))
            for row in _iter_unique_rows(unique_csv, policy):
                if row.category not in counts:
                    raise EvaluationAuditError(
                        f"row {row.index} category is outside policy"
                    )
                record_payload = _write_line(handle, _generate_record(row))
                row_digest.update(record_payload)
                counts[row.category] += 1
                row_count += 1
            if counts != expected_counts:
                raise EvaluationAuditError(
                    f"category counts differ: {counts!r} != {expected_counts!r}"
                )
            footer = {
                "category_counts": counts,
                "record_lines_sha256": row_digest.hexdigest(),
                "row_count": row_count,
                "type": "footer",
            }
            _write_line(handle, footer)
            handle.flush()
            os.fsync(handle.fileno())
        verify_certificate(
            unique_csv,
            temporary,
            binding=binding,
            source_manifest=source_manifest,
            policy=policy,
        )
        os.replace(temporary, certificate)
        verified = verify_certificate(
            unique_csv,
            certificate,
            binding=binding,
            source_manifest=source_manifest,
            policy=policy,
        )
        return verified
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def _read_json_line(handle: object, label: str) -> tuple[object, bytes]:
    try:
        payload = handle.readline()  # type: ignore[attr-defined]
    except OSError as error:
        raise EvaluationAuditError(f"cannot read {label}: {error}") from error
    if not payload:
        raise EvaluationAuditError(f"unexpected end of {label}")
    if not payload.endswith(b"\n"):
        raise EvaluationAuditError(f"{label} has a truncated final line")
    try:
        text = payload[:-1].decode("ascii")
    except UnicodeError as error:
        raise EvaluationAuditError(f"{label} is not ASCII JSON") from error
    return strict_json_loads(text, label), payload


def verify_certificate(
    unique_csv: Path,
    certificate: Path,
    *,
    binding: Mapping[str, object] | None = None,
    source_manifest: Sequence[tuple[str, str]] | None = None,
    policy: EvaluationPolicy = PRODUCTION_POLICY,
) -> EvaluationSummary:
    """Replay every compact row certificate against the graph definition."""

    expected_counts = policy.category_counts()
    counts = {category: 0 for category in expected_counts}
    row_digest = sha256()
    row_count = 0
    try:
        with certificate.open("rb") as handle:
            raw_header, _payload = _read_json_line(handle, "certificate header")
            header = _require_mapping(raw_header, "certificate header")
            expected_header_keys = {
                "binding",
                "checker_source_manifest",
                "checker_source_set_sha256",
                "expected_category_counts",
                "expected_rows",
                "format",
                "type",
            }
            if (
                set(header) != expected_header_keys
                or header["type"] != "header"
                or header["format"] != CERTIFICATE_FORMAT
                or header["expected_rows"] != policy.expected_rows
                or header["expected_category_counts"] != expected_counts
            ):
                raise EvaluationAuditError("certificate header differs")
            if binding is not None and header["binding"] != dict(binding):
                raise EvaluationAuditError("certificate binding differs")
            if source_manifest is not None:
                expected_manifest = [list(record) for record in source_manifest]
                if (
                    header["checker_source_manifest"] != expected_manifest
                    or header["checker_source_set_sha256"]
                    != _manifest_sha256(source_manifest)
                ):
                    raise EvaluationAuditError(
                        "certificate checker-source binding differs"
                    )
            header_binding = _require_mapping(
                header["binding"], "certificate binding"
            )
            unique_hash = _require_sha256(
                header_binding.get("unique_csv_sha256"),
                "certificate unique CSV hash",
            )
            if sha256_file(unique_csv) != unique_hash:
                raise EvaluationAuditError(
                    "certificate does not bind supplied unique CSV"
                )

            for row in _iter_unique_rows(unique_csv, policy):
                raw_record, payload = _read_json_line(
                    handle, f"certificate row {row.index}"
                )
                _verify_record(row, raw_record)
                row_digest.update(payload)
                counts[row.category] += 1
                row_count += 1

            raw_footer, _payload = _read_json_line(handle, "certificate footer")
            footer = _require_mapping(raw_footer, "certificate footer")
            if set(footer) != {
                "category_counts",
                "record_lines_sha256",
                "row_count",
                "type",
            }:
                raise EvaluationAuditError("certificate footer schema differs")
            if (
                footer["type"] != "footer"
                or footer["row_count"] != row_count
                or footer["category_counts"] != counts
                or footer["record_lines_sha256"] != row_digest.hexdigest()
                or counts != expected_counts
            ):
                raise EvaluationAuditError("certificate footer is false")
            if handle.read(1):
                raise EvaluationAuditError(
                    "certificate contains data after its footer"
                )
    except OSError as error:
        raise EvaluationAuditError(
            f"cannot read certificate {certificate}: {error}"
        ) from error
    return EvaluationSummary(
        row_count=row_count,
        category_counts=tuple((key, counts[key]) for key in expected_counts),
        record_lines_sha256=row_digest.hexdigest(),
        certificate_sha256=sha256_file(certificate),
    )


def _hash_bound_path(
    mapping: Mapping[str, object], path: Path, label: str
) -> str:
    matches = [
        value
        for raw_path, value in mapping.items()
        if isinstance(raw_path, str) and _resolve(Path(raw_path)) == path
    ]
    if len(matches) != 1:
        raise EvaluationAuditError(f"{label} path is not uniquely bound")
    return _require_sha256(matches[0], f"{label} SHA-256")


def _verify_relative_manifest(
    campaign_root: Path, raw_manifest: object, label: str
) -> tuple[tuple[str, str], ...]:
    if not isinstance(raw_manifest, list):
        raise EvaluationAuditError(f"{label} is not an array")
    parsed: list[tuple[str, str]] = []
    for index, item in enumerate(raw_manifest):
        if (
            not isinstance(item, list)
            or len(item) != 2
            or not isinstance(item[0], str)
        ):
            raise EvaluationAuditError(f"{label}[{index}] is malformed")
        parsed.append(
            (item[0], _require_sha256(item[1], f"{label}[{index}] hash"))
        )
    actual = _manifest(campaign_root, tuple(path for path, _hash in parsed))
    if tuple(parsed) != actual:
        raise EvaluationAuditError(f"{label} does not match current bytes")
    return tuple(parsed)


def collect_binding(
    paths: EvaluationPaths,
    policy: EvaluationPolicy = PRODUCTION_POLICY,
) -> tuple[dict[str, object], tuple[tuple[str, str], ...]]:
    """Validate and bind the completed search and coverage artifacts."""

    root = _resolve(paths.campaign_root)
    read_paths = {
        "unique_csv": _require_file(paths.unique_csv, "unique CSV"),
        "provenance_csv": _require_file(
            paths.provenance_csv, "provenance CSV"
        ),
        "database": _require_file(paths.database, "search database"),
        "checkpoint": _require_file(paths.checkpoint, "search checkpoint"),
        "coverage_report": _require_file(
            paths.coverage_report, "coverage report"
        ),
        "coverage_state_database": _require_file(
            paths.coverage_state_database, "coverage state database"
        ),
    }
    write_paths = {
        "certificate": _resolve(paths.certificate),
        "report": _resolve(paths.report),
    }
    roles: dict[Path, list[str]] = {}
    for role, path in {**read_paths, **write_paths}.items():
        roles.setdefault(path, []).append(role)
    collisions = {path: names for path, names in roles.items() if len(names) > 1}
    if collisions:
        raise EvaluationAuditError(f"evaluation path roles alias: {collisions!r}")
    for database in (
        read_paths["database"],
        read_paths["coverage_state_database"],
    ):
        for suffix in ("-wal", "-shm", "-journal"):
            if Path(str(database) + suffix).exists():
                raise EvaluationAuditError(
                    f"live SQLite companion prevents stable binding: "
                    f"{database}{suffix}"
                )

    hashes = {
        f"{name}_sha256": sha256_file(path)
        for name, path in read_paths.items()
    }
    checkpoint = _require_mapping(
        strict_json_file(read_paths["checkpoint"]), "search checkpoint"
    )
    expected_categories = policy.category_counts()
    if (
        checkpoint.get("status") != "complete"
        or checkpoint.get("unique_canonical_graphs") != policy.expected_rows
        or checkpoint.get("unique_category_counts") != expected_categories
        or checkpoint.get("candidate_path") is not None
    ):
        raise EvaluationAuditError(
            "search checkpoint is not the expected completed negative run"
        )
    if policy.expected_origins is not None and (
        checkpoint.get("raw_expected") != policy.expected_origins
        or checkpoint.get("raw_processed") != policy.expected_origins
    ):
        raise EvaluationAuditError("search checkpoint origin counts differ")
    if (
        not isinstance(checkpoint.get("database"), str)
        or _resolve(Path(checkpoint["database"])) != read_paths["database"]
        or checkpoint.get("database_sha256") != hashes["database_sha256"]
    ):
        raise EvaluationAuditError("search checkpoint database binding differs")
    output_hashes = _require_mapping(
        checkpoint.get("output_sha256"), "checkpoint output_sha256"
    )
    if (
        _hash_bound_path(
            output_hashes, read_paths["unique_csv"], "checkpoint unique CSV"
        )
        != hashes["unique_csv_sha256"]
        or _hash_bound_path(
            output_hashes,
            read_paths["provenance_csv"],
            "checkpoint provenance CSV",
        )
        != hashes["provenance_csv_sha256"]
    ):
        raise EvaluationAuditError("checkpoint output hashes differ")
    coverage_inside = _require_mapping(
        checkpoint.get("coverage_audit"), "checkpoint coverage_audit"
    )
    if coverage_inside.get("passed") is not True:
        raise EvaluationAuditError("search checkpoint internal audit did not pass")
    candidate_state = _require_mapping(
        checkpoint.get("candidate_state"), "checkpoint candidate_state"
    )
    if (
        candidate_state.get("pending") is not False
        or candidate_state.get("candidate_row_count") != 0
        or candidate_state.get("candidate_origin_row_count") != 0
    ):
        raise EvaluationAuditError("search checkpoint has a candidate")

    configuration = _require_mapping(
        checkpoint.get("configuration"), "checkpoint configuration"
    )
    configuration_sha = _require_sha256(
        checkpoint.get("configuration_sha256"),
        "checkpoint configuration SHA-256",
    )
    if _json_sha256(configuration) != configuration_sha:
        raise EvaluationAuditError("checkpoint configuration digest is false")
    if configuration.get("target_guard_count") != 3:
        raise EvaluationAuditError("search target guard count is not 3")
    search_manifest = _verify_relative_manifest(
        root,
        configuration.get("runtime_source_manifest"),
        "search runtime source manifest",
    )
    if configuration.get("runtime_source_set_sha256") != _manifest_sha256(
        search_manifest
    ):
        raise EvaluationAuditError("search runtime source-set digest is false")

    coverage = _require_mapping(
        strict_json_file(read_paths["coverage_report"]), "coverage report"
    )
    if (
        coverage.get("format") != "gamma-theta-extension-postrun-audit-v1"
        or coverage.get("status") != "complete"
        or coverage.get("passed") is not True
        or coverage.get("unique_canonical_graphs") != policy.expected_rows
        or coverage.get("database_sha256") != hashes["database_sha256"]
    ):
        raise EvaluationAuditError("coverage report is not the expected pass")
    if policy.expected_origins is not None and (
        coverage.get("expected_origins") != policy.expected_origins
        or coverage.get("verified_origins") != policy.expected_origins
    ):
        raise EvaluationAuditError("coverage report origin counts differ")
    if (
        not isinstance(coverage.get("state_database"), str)
        or _resolve(Path(coverage["state_database"]))
        != read_paths["coverage_state_database"]
        or coverage.get("state_database_sha256")
        != hashes["coverage_state_database_sha256"]
    ):
        raise EvaluationAuditError("coverage state database binding differs")
    coverage_binding = _require_mapping(
        coverage.get("audit_binding"), "coverage audit_binding"
    )
    if coverage.get("audit_binding_sha256") != _json_sha256(coverage_binding):
        raise EvaluationAuditError("coverage audit binding digest is false")
    expected_coverage_hashes = {
        "unique_sha256": hashes["unique_csv_sha256"],
        "provenance_sha256": hashes["provenance_csv_sha256"],
        "database_sha256": hashes["database_sha256"],
        "checkpoint_sha256": hashes["checkpoint_sha256"],
    }
    if any(
        coverage_binding.get(key) != expected
        for key, expected in expected_coverage_hashes.items()
    ):
        raise EvaluationAuditError("coverage report artifact hashes differ")
    coverage_manifest = _verify_relative_manifest(
        root,
        coverage_binding.get("checker_source_manifest"),
        "coverage checker source manifest",
    )
    if coverage_binding.get(
        "checker_source_set_sha256"
    ) != _manifest_sha256(coverage_manifest):
        raise EvaluationAuditError("coverage checker source-set digest is false")

    checker_manifest = _manifest(root, CHECKER_SOURCE_PATHS)
    binding: dict[str, object] = {
        **hashes,
        "configuration_sha256": configuration_sha,
        "coverage_audit_binding_sha256": coverage["audit_binding_sha256"],
        "coverage_origin_chain_sha256": _require_sha256(
            coverage.get("origin_chain_sha256"),
            "coverage origin-chain SHA-256",
        ),
        "coverage_checker_source_manifest": [
            list(record) for record in coverage_manifest
        ],
        "coverage_checker_source_set_sha256": _manifest_sha256(
            coverage_manifest
        ),
        "paths": {
            name: str(path)
            for name, path in {**read_paths, **write_paths}.items()
        },
        "search_runtime_source_manifest": [
            list(record) for record in search_manifest
        ],
        "search_runtime_source_set_sha256": _manifest_sha256(search_manifest),
    }
    return binding, checker_manifest


def run_evaluation_audit(
    paths: EvaluationPaths,
    policy: EvaluationPolicy = PRODUCTION_POLICY,
) -> EvaluationSummary:
    """Bind inputs, evaluate all rows, replay the certificate, write report."""

    started = time.time()
    binding, checker_manifest = collect_binding(paths, policy)
    immutable_before = {
        key: value
        for key, value in binding.items()
        if key.endswith("_sha256") and key not in {
            "configuration_sha256",
            "coverage_audit_binding_sha256",
            "coverage_origin_chain_sha256",
            "coverage_checker_source_set_sha256",
            "search_runtime_source_set_sha256",
        }
    }
    summary = write_certificate(
        _resolve(paths.unique_csv),
        _resolve(paths.certificate),
        binding=binding,
        source_manifest=checker_manifest,
        policy=policy,
    )
    binding_after, manifest_after = collect_binding(paths, policy)
    if binding_after != binding or manifest_after != checker_manifest:
        raise EvaluationAuditError(
            "input or checker bytes changed during mathematical audit"
        )
    for key, value in immutable_before.items():
        if binding_after.get(key) != value:
            raise EvaluationAuditError(f"bound input changed during audit: {key}")
    final_replay = verify_certificate(
        _resolve(paths.unique_csv),
        _resolve(paths.certificate),
        binding=binding,
        source_manifest=checker_manifest,
        policy=policy,
    )
    if final_replay != summary:
        raise EvaluationAuditError("post-install certificate replay differs")
    finished = time.time()
    category_counts = dict(summary.category_counts)
    eternal_false_count = (
        category_counts.get(CATEGORY_ETERNAL, 0)
        + category_counts.get(CATEGORY_PRIVATE, 0)
    )
    report = {
        "binding": binding,
        "certificate": str(_resolve(paths.certificate)),
        "certificate_sha256": summary.certificate_sha256,
        "checker_source_manifest": [
            list(record) for record in checker_manifest
        ],
        "checker_source_set_sha256": _manifest_sha256(checker_manifest),
        "finished_unix": finished,
        "format": REPORT_FORMAT,
        "mathematical_discharge": {
            "alpha_above_3_rows_gamma_3_alpha_4": category_counts.get(
                CATEGORY_ALPHA, 0
            ),
            "eternal_false_rows_gamma_alpha_3_empty_one_guard_gfp": (
                eternal_false_count
            ),
            "gamma_below_3_rows": category_counts.get(CATEGORY_GAMMA, 0),
            "surviving_counterexample_candidates": 0,
        },
        "maximum_resident_set_size_mib": _rss_mib(),
        "passed": True,
        "record_lines_sha256": summary.record_lines_sha256,
        "replay_passed": True,
        "row_count": summary.row_count,
        "category_counts": category_counts,
        "started_unix": started,
        "status": "complete",
        "wall_seconds": finished - started,
        "warning": (
            "This is a certificate-backed finite result for the delimited "
            "one-vertex-extension artifact, not a resolution of the universal "
            "gamma-theta conjecture."
        ),
        "checker_limitations": [
            (
                "Coverage of the 110,537 labeled origins and their reduction "
                "to 54,216 canonical rows is inherited only through the bound, "
                "independently passed coverage-audit artifact."
            ),
            (
                "The mathematical checker proves the category predicates "
                "requested here; it does not independently recompute clique "
                "cover numbers because every extension retains its published "
                "host as an induced subgraph."
            ),
        ],
    }
    _atomic_json(_resolve(paths.report), report)
    return summary

