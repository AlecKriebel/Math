#!/usr/bin/env python3
"""Strict standard-library audit of the full unrestricted-projective corpus.

The corpus contains one CP-SAT result for every pair of 48 complementary
length-five quartets and 32 projective parameter cores.  This verifier checks
coverage, byte integrity, record and transcript consistency, source hashes,
candidate absence, and the exact structured-family scope.

It deliberately does not import OR-Tools and does not re-prove any recorded
``INFEASIBLE`` status.  CP-SAT emitted no independently checkable UNSAT proof
certificates.  The shard JSON also does not embed a source hash or the parent
scheduler's limits, so source attribution and invocation settings cannot be
recovered from a record alone; those limitations are explicit in the
generated manifest.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import sys
from typing import Any, Iterable, Sequence


BASE = Path(__file__).resolve().parent
DEFAULT_CORPUS = (
    BASE / "output" / "five_comb_unrestricted_core_cp_v2"
)
DEFAULT_CANDIDATE_DIRECTORIES = (
    BASE / "output" / "five_comb_unrestricted_core_candidates_v2",
    BASE / "output" / "five_comb_unrestricted_core_candidates",
)
DEFAULT_MANIFEST = (
    BASE / "FIVE_COMB_UNRESTRICTED_FULL_CORPUS_MANIFEST.json"
)

QUARTET_COUNT = 48
CORE_COUNT = 32
SHARD_COUNT = QUARTET_COUNT * CORE_COUNT
CORPUS_FORMAT = "h668-five-comb-unrestricted-core-shard-v1"
MANIFEST_FORMAT = "h668-five-comb-unrestricted-full-corpus-manifest-v1"
SOLVER_SCRIPT = "search_five_comb_unrestricted_projective_cp_sat.py"

SOURCE_EXPECTATIONS = {
    "check_five_comb_mub_reductions.py": (
        19_482,
        "56bea0e45f06bfc7918318b670e43463b0991b219015b44b73f826ada7e183df",
        "complementary quartets, projective vectors, and modulo-four constants",
    ),
    "run_five_comb_unrestricted_core_shards.py": (
        9_383,
        "cb054c5bf1ee7c09982c5f5ae10c50a67399f06f52897e0ae565a3a1678551ba",
        "resume-safe scheduler and shard-record writer",
    ),
    "search_five_comb_common_type_cp_sat.py": (
        16_839,
        "d50214cff57710687b5ca8152adfe0457b5616665393fd9d5f270b2c9c7036c2",
        "shared contribution tables and row-sum profiles",
    ),
    SOLVER_SCRIPT: (
        31_254,
        "76dc604f0bb61ebeb5a9892f9d63c7b193fbee68beb47b2abc6e04aa575ff06b",
        "exact unrestricted-projective common-type CP-SAT model executed",
    ),
    "verify_five_comb_high_lag_boundary.py": (
        26_989,
        "9c71073ca53e5e4783cbd912f1196feb17c8eb3e148e29ae8d9d379f4976f127",
        "exact physical E2 boundary-table derivation used by the solver",
    ),
}

E2_FULL_ROW_COUNT = 10_934
E2_PARAMETER_ROW_COUNT = 2_434
E2_FULL_SHA256 = (
    "441c25786c4a0bc56f9e86c84bf9c8c8252595a9f75298aad960c31320aeb6b4"
)
E2_PARAMETER_SHA256 = (
    "85972db2c71b3e1415705017b0f3f1e57aab3f7cba880104c8f60d83c687d2c0"
)
CANONICAL_E2_BY_CORE = (
    8, 16, 30, 28, 10, 16, 30, 16,
    12, 32, 15, 31, 16, 16, 32, 16,
    23, 30, 29, 12, 16, 28, 28, 16,
    26, 30, 29, 16, 27, 30, 32, 22,
)

RECORD_KEYS = {
    "booleans",
    "branches",
    "command",
    "conflicts",
    "finished_at",
    "format",
    "projective_core",
    "quartet",
    "returncode",
    "started_at",
    "status",
    "stdout",
    "wall_time_seconds",
}
TRANSCRIPT_KEYS = {
    "booleans",
    "branches",
    "conflicts",
    "projective_core",
    "quartet",
    "status",
    "wall_time",
}


class AuditError(ValueError):
    """Raised when a corpus, source, or manifest invariant fails."""


def expected_names() -> tuple[str, ...]:
    return tuple(
        f"q{quartet:02d}_core{core:02d}.json"
        for quartet in range(QUARTET_COUNT)
        for core in range(CORE_COUNT)
    )


def _reject_json_constant(token: str) -> None:
    raise AuditError(f"non-finite JSON number {token!r}")


def _unique_object(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AuditError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> tuple[Any, bytes]:
    try:
        raw = path.read_bytes()
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_json_constant,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditError(f"{path}: invalid JSON: {error}") from error
    return value, raw


def require_exact_int(
    value: Any,
    label: str,
    minimum: int | None = None,
) -> int:
    if type(value) is not int:
        raise AuditError(f"{label} must be an integer")
    if minimum is not None and value < minimum:
        raise AuditError(f"{label} must be at least {minimum}")
    return value


def require_finite_number(
    value: Any,
    label: str,
    *,
    positive: bool = False,
) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise AuditError(f"{label} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        raise AuditError(f"{label} must be finite")
    if positive and result <= 0:
        raise AuditError(f"{label} must be positive")
    return result


def parse_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str):
        raise AuditError(f"{label} must be an ISO-8601 string")
    try:
        result = datetime.fromisoformat(value)
    except ValueError as error:
        raise AuditError(f"{label} is not a valid ISO-8601 timestamp") from error
    if result.tzinfo is None or result.utcoffset() != timezone.utc.utcoffset(result):
        raise AuditError(f"{label} must carry an explicit UTC offset")
    return result


def parse_transcript(text: Any, label: str) -> dict[str, str]:
    if not isinstance(text, str) or not text.endswith("\n"):
        raise AuditError(f"{label} must be a newline-terminated string")
    result: dict[str, str] = {}
    for line in text.splitlines():
        if "=" not in line:
            raise AuditError(f"{label} contains a non key-value line")
        key, value = line.split("=", 1)
        if not key or key in result:
            raise AuditError(f"{label} contains an empty or duplicate key")
        result[key] = value
    if set(result) != TRANSCRIPT_KEYS:
        raise AuditError(
            f"{label} keys differ: missing={sorted(TRANSCRIPT_KEYS - set(result))}, "
            f"extra={sorted(set(result) - TRANSCRIPT_KEYS)}"
        )
    if "candidate=" in text or "verified_hadamard_order=" in text:
        raise AuditError(f"{label} records a candidate")
    return result


def validate_command(
    value: Any,
    quartet: int,
    core: int,
    label: str,
) -> str:
    if (
        not isinstance(value, list)
        or any(not isinstance(item, str) for item in value)
    ):
        raise AuditError(f"{label} must be a string list")
    expected = ["in-process", f"q={quartet}", f"core={core}"]
    if value != expected:
        raise AuditError(
            f"{label} must be the exact abbreviated in-process command {expected}"
        )
    return "in-process"


def validate_record(
    path: Path,
    quartet: int,
    core: int,
) -> tuple[dict[str, Any], bytes, datetime, datetime]:
    payload, raw = load_json(path)
    label = path.name
    if not isinstance(payload, dict):
        raise AuditError(f"{label} must contain a JSON object")
    keys = set(payload)
    if keys != RECORD_KEYS:
        raise AuditError(
            f"{label} keys differ: missing={sorted(RECORD_KEYS - keys)}, "
            f"extra={sorted(keys - RECORD_KEYS)}"
        )
    if payload["format"] != CORPUS_FORMAT:
        raise AuditError(f"{label} has an unsupported format")
    if require_exact_int(payload["quartet"], f"{label}.quartet") != quartet:
        raise AuditError(f"{label} has the wrong quartet identity")
    if (
        require_exact_int(
            payload["projective_core"],
            f"{label}.projective_core",
        )
        != core
    ):
        raise AuditError(f"{label} has the wrong projective-core identity")
    if payload["status"] != "INFEASIBLE":
        raise AuditError(
            f"{label} is not terminal-infeasible: status={payload['status']!r}"
        )
    if require_exact_int(payload["returncode"], f"{label}.returncode") != 1:
        raise AuditError(f"{label} has the wrong INFEASIBLE return code")

    wall_time = require_finite_number(
        payload["wall_time_seconds"],
        f"{label}.wall_time_seconds",
        positive=True,
    )
    conflicts = require_exact_int(
        payload["conflicts"],
        f"{label}.conflicts",
        minimum=0,
    )
    branches = require_exact_int(
        payload["branches"],
        f"{label}.branches",
        minimum=0,
    )
    booleans = require_exact_int(
        payload["booleans"],
        f"{label}.booleans",
        minimum=0,
    )
    started = parse_timestamp(payload["started_at"], f"{label}.started_at")
    finished = parse_timestamp(payload["finished_at"], f"{label}.finished_at")
    if finished < started:
        raise AuditError(f"{label} finishes before it starts")
    if (finished - started).total_seconds() + 0.05 < wall_time:
        raise AuditError(f"{label} solver wall time exceeds its recorded interval")

    mode = validate_command(
        payload["command"],
        quartet,
        core,
        f"{label}.command",
    )
    transcript = parse_transcript(payload["stdout"], f"{label}.stdout")
    if transcript["status"] != payload["status"]:
        raise AuditError(f"{label} transcript status disagrees")
    transcript_integers = {
        "quartet": quartet,
        "projective_core": core,
        "conflicts": conflicts,
        "branches": branches,
        "booleans": booleans,
    }
    for key, expected in transcript_integers.items():
        try:
            actual = int(transcript[key])
        except ValueError as error:
            raise AuditError(f"{label} transcript {key} is not an integer") from error
        if actual != expected:
            raise AuditError(f"{label} transcript {key} disagrees")
    try:
        transcript_wall_time = float(transcript["wall_time"])
    except ValueError as error:
        raise AuditError(f"{label} transcript wall_time is invalid") from error
    if not math.isfinite(transcript_wall_time) or not math.isclose(
        transcript_wall_time,
        wall_time,
        rel_tol=0.0,
        abs_tol=0.5e-6,
    ):
        raise AuditError(f"{label} transcript wall_time disagrees")

    return (
        {
            "booleans": booleans,
            "branches": branches,
            "command_mode": mode,
            "conflicts": conflicts,
            "finished_at": payload["finished_at"],
            "path": label,
            "projective_core": core,
            "quartet": quartet,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "size_bytes": len(raw),
            "started_at": payload["started_at"],
            "status": payload["status"],
            "wall_time_seconds": wall_time,
        },
        raw,
        started,
        finished,
    )


def normalized_projective_labels(
    parameters: Sequence[int],
) -> tuple[int, ...]:
    """Independent replay of the normalized twelve-bit parametrization."""

    if len(parameters) != 12 or any(bit not in (0, 1) for bit in parameters):
        raise AuditError("the projective parametrization needs twelve bits")
    alpha, beta, u5, u6, u7, *middle_tail = parameters
    low = (0, 0, beta, alpha, 0, 0, alpha, beta)
    middle = (0, *middle_tail)
    high = (
        0,
        beta ^ u7,
        alpha ^ beta ^ u6,
        alpha ^ u5,
        0,
        u5,
        u6,
        u7,
    )
    return tuple(
        low[slot] + 2 * middle[slot] + 4 * high[slot]
        for slot in range(8)
    )


def row_orbit_is_canonical(labels: Sequence[int]) -> bool:
    """Replay the long-row/short-row swap lex leader."""

    values = tuple(labels)
    if len(values) != 8 or values[0] != 0:
        raise AuditError("expected eight normalized projective labels")
    middle = tuple((label >> 1) & 1 for label in values[1:])
    low = tuple(label & 1 for label in values[1:])
    high = tuple((label >> 2) & 1 for label in values[1:])
    masks = (
        low,
        high,
        tuple(a ^ b for a, b in zip(low, high, strict=True)),
    )
    return all(
        middle
        <= tuple(
            value ^ mask_bit
            for value, mask_bit in zip(middle, mask, strict=True)
        )
        for mask in masks
    )


def audit_projective_scope() -> dict[str, Any]:
    """Check the 32-core partition and the exact E2 necessary-condition table."""

    all_parameters = tuple(product((0, 1), repeat=12))
    labelings = {
        normalized_projective_labels(parameters)
        for parameters in all_parameters
    }
    raw_by_core = [0] * CORE_COUNT
    canonical_by_core = [0] * CORE_COUNT
    for parameters in all_parameters:
        core = sum(parameters[bit] << bit for bit in range(5))
        raw_by_core[core] += 1
        if row_orbit_is_canonical(normalized_projective_labels(parameters)):
            canonical_by_core[core] += 1
    if len(labelings) != 4096 or raw_by_core != [128] * CORE_COUNT:
        raise AuditError("the 32 cores no longer partition 4,096 labelings")
    if sum(canonical_by_core) != 1440:
        raise AuditError("the row-pair symmetry no longer has 1,440 leaders")

    try:
        from verify_five_comb_high_lag_boundary import (
            canonical_rows_sha256,
            e2_boundary_rows,
            e2_parameter_rows,
        )
    except ImportError as error:
        raise AuditError(f"cannot import the standard-library E2 verifier: {error}")

    e2_full = e2_boundary_rows()
    e2_parameters = e2_parameter_rows()
    if len(e2_full) != E2_FULL_ROW_COUNT:
        raise AuditError("the physical E2 full-table row count changed")
    if len(e2_parameters) != E2_PARAMETER_ROW_COUNT:
        raise AuditError("the physical E2 parameter-table row count changed")
    if canonical_rows_sha256(e2_full, 19) != E2_FULL_SHA256:
        raise AuditError("the physical E2 full-table hash changed")
    if canonical_rows_sha256(e2_parameters, 12) != E2_PARAMETER_SHA256:
        raise AuditError("the physical E2 parameter-table hash changed")

    e2_canonical_by_core = [0] * CORE_COUNT
    for parameters in e2_parameters:
        if not (
            parameters[1]
            or parameters[4]
            or parameters[5]
            or parameters[11]
        ):
            raise AuditError("an E2 row violates the exact lag-81 Boolean cut")
        if row_orbit_is_canonical(normalized_projective_labels(parameters)):
            core = sum(parameters[bit] << bit for bit in range(5))
            e2_canonical_by_core[core] += 1
    if tuple(e2_canonical_by_core) != CANONICAL_E2_BY_CORE:
        raise AuditError("the canonical physical-E2 core distribution changed")

    return {
        "canonical_labelings_after_physical_e2_table": sum(
            e2_canonical_by_core
        ),
        "canonical_labelings_by_core_after_physical_e2_table": (
            e2_canonical_by_core
        ),
        "canonical_labelings_by_core_before_high_lag_cuts": canonical_by_core,
        "canonical_labelings_before_high_lag_cuts": sum(canonical_by_core),
        "core_bit_order_little_endian": [
            "alpha",
            "beta",
            "u5",
            "u6",
            "u7",
        ],
        "normalized_projective_labelings": len(labelings),
        "physical_e2_full_rows": len(e2_full),
        "physical_e2_full_rows_sha256": E2_FULL_SHA256,
        "physical_e2_parameter_rows": len(e2_parameters),
        "physical_e2_parameter_rows_sha256": E2_PARAMETER_SHA256,
        "raw_labelings_per_core": 128,
    }


def _framed_hash(records: Iterable[tuple[str, bytes]]) -> str:
    digest = hashlib.sha256()
    for name, raw in records:
        encoded_name = name.encode("utf-8")
        digest.update(len(encoded_name).to_bytes(4, "big"))
        digest.update(encoded_name)
        digest.update(len(raw).to_bytes(8, "big"))
        digest.update(raw)
    return digest.hexdigest()


def audit_sources() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    framed: list[tuple[str, bytes]] = []
    for relative, (size, expected_hash, role) in sorted(
        SOURCE_EXPECTATIONS.items()
    ):
        path = BASE / relative
        try:
            raw = path.read_bytes()
        except OSError as error:
            raise AuditError(f"cannot read source file {relative}: {error}") from error
        actual_hash = hashlib.sha256(raw).hexdigest()
        if len(raw) != size or actual_hash != expected_hash:
            raise AuditError(f"source hash or size changed: {relative}")
        records.append(
            {
                "path": relative,
                "role": role,
                "sha256": actual_hash,
                "size_bytes": len(raw),
            }
        )
        framed.append((relative, raw))
    return {
        "attribution": (
            "generation-session provenance states that every shard was run "
            "after the physical E2 table was integrated and that the exact "
            "solver bytes pinned here remained unchanged throughout"
        ),
        "attribution_limit": (
            "shard JSON does not embed a source hash, so the record bytes "
            "alone cannot independently bind an individual CP-SAT result "
            "to these source bytes"
        ),
        "hash_scheme": (
            "sha256 over sorted source records framed as "
            "uint32be(name_bytes)||name_bytes||uint64be(content_bytes)||content_bytes"
        ),
        "record_embedded_source_hash": False,
        "source_bundle_sha256": _framed_hash(framed),
        "source_files": records,
    }


def _has_overlapping_intervals(
    intervals: Iterable[tuple[datetime, datetime]],
) -> bool:
    ordered = sorted(intervals)
    if not ordered:
        return False
    latest_finish = ordered[0][1]
    for started, finished in ordered[1:]:
        if started < latest_finish:
            return True
        latest_finish = max(latest_finish, finished)
    return False


def _display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(BASE.resolve()))
    except ValueError:
        return str(path.resolve())


def audit_corpus(
    corpus: Path,
    candidate_directories: Sequence[Path],
) -> dict[str, Any]:
    if not corpus.is_dir():
        raise AuditError(f"corpus directory does not exist: {corpus}")
    expected = expected_names()
    expected_set = set(expected)
    entries = {path.name for path in corpus.iterdir()}
    if entries != expected_set:
        raise AuditError(
            f"corpus entries differ: missing={sorted(expected_set - entries)}, "
            f"extra={sorted(entries - expected_set)}"
        )

    files: list[dict[str, Any]] = []
    framed_records: list[tuple[str, bytes]] = []
    intervals: list[tuple[datetime, datetime]] = []
    q00_intervals: list[tuple[datetime, datetime]] = []
    later_intervals: list[tuple[datetime, datetime]] = []
    index = 0
    for quartet in range(QUARTET_COUNT):
        for core in range(CORE_COUNT):
            name = expected[index]
            index += 1
            record, raw, started, finished = validate_record(
                corpus / name,
                quartet,
                core,
            )
            files.append(record)
            framed_records.append((name, raw))
            intervals.append((started, finished))
            if quartet == 0:
                q00_intervals.append((started, finished))
            else:
                later_intervals.append((started, finished))

    candidate_files: list[Path] = []
    for directory in candidate_directories:
        if directory.exists():
            if not directory.is_dir():
                raise AuditError(
                    f"candidate path is not a directory: {directory}"
                )
            candidate_files.extend(
                path.resolve()
                for path in directory.rglob("*")
                if path.is_file()
            )
    if candidate_files:
        raise AuditError(
            f"candidate files are present: {sorted(candidate_files)}"
        )

    status_counts = Counter(record["status"] for record in files)
    command_modes = Counter(record["command_mode"] for record in files)
    if status_counts != Counter({"INFEASIBLE": SHARD_COUNT}):
        raise AuditError(f"unexpected terminal status counts: {status_counts}")
    if command_modes != Counter({"in-process": SHARD_COUNT}):
        raise AuditError(f"unexpected command-mode counts: {command_modes}")

    q00_finished = max(finished for _, finished in q00_intervals)
    later_started = min(started for started, _ in later_intervals)
    if not q00_finished < later_started:
        raise AuditError("q00 is not temporally separate from q01 through q47")
    if not _has_overlapping_intervals(later_intervals):
        raise AuditError("q01 through q47 no longer show mixed-run overlap")

    booleans = [record["booleans"] for record in files]
    totals = {
        "booleans": sum(booleans),
        "booleans_max": max(booleans),
        "booleans_min": min(booleans),
        "booleans_zero_shards": sum(value == 0 for value in booleans),
        "branches": sum(record["branches"] for record in files),
        "conflicts": sum(record["conflicts"] for record in files),
        "wall_time_seconds": round(
            math.fsum(record["wall_time_seconds"] for record in files),
            6,
        ),
    }
    return {
        "candidate_directories_checked": [
            _display_path(path) for path in candidate_directories
        ],
        "candidate_file_count": 0,
        "command_mode_counts": dict(sorted(command_modes.items())),
        "corpus_directory": _display_path(corpus),
        "corpus_format": CORPUS_FORMAT,
        "corpus_sha256": _framed_hash(framed_records),
        "files": files,
        "format": MANIFEST_FORMAT,
        "grid": {
            "projective_cores": CORE_COUNT,
            "quartets": QUARTET_COUNT,
            "shards": SHARD_COUNT,
        },
        "hash_scheme": (
            "sha256 over sorted records framed as "
            "uint32be(name_bytes)||name_bytes||uint64be(content_bytes)||content_bytes"
        ),
        "model_scope": {
            **audit_projective_scope(),
            "carrier_family": (
                "all 48 normalized complementary length-five quartets in "
                "the repository's common-type five-comb packing, with an "
                "arbitrary permutation of eight polarized types, carrier "
                "orientations, physical hole signs, and unrestricted "
                "normalized projective slot labels"
            ),
            "exact_constraints": (
                "all 83 aperiodic correlation equations and the row-square "
                "identity, with exact modulo-four hole fiber, physical E2 "
                "lags-78-through-81 table, direct high-lag channel, and "
                "verified construction symmetries"
            ),
            "scope_limit": (
                "this excludes only the unrestricted-projective common-type "
                "five-comb packing across its 48 quartet representatives; "
                "it does not exclude arbitrary five-comb packings, arbitrary "
                "BS(84,83), or a Hadamard matrix of order 668"
            ),
        },
        "proof_status": {
            "independent_unsat_certificates": 0,
            "meaning": (
                "INFEASIBLE is CP-SAT's recorded terminal status; this "
                "standard-library audit verifies the records, coverage, "
                "transcripts, hashes, and scope but does not re-prove UNSAT"
            ),
        },
        "run_metadata": {
            "all_shard_commands_are_abbreviated_in_process": True,
            "earliest_started_at": min(
                record["started_at"] for record in files
            ),
            "latest_finished_at": max(
                record["finished_at"] for record in files
            ),
            "q00_finished_at": max(
                record["finished_at"]
                for record in files
                if record["quartet"] == 0
            ),
            "q00_is_temporally_separate": True,
            "q01_to_q47_first_started_at": min(
                record["started_at"]
                for record in files
                if record["quartet"] != 0
            ),
            "q01_to_q47_have_overlapping_intervals": True,
            "record_limitations": (
                "the shard format stores no parent invocation ID, batch ID, "
                "candidate directory, Python/OR-Tools version, source hash, "
                "time limit, worker count, or memory limit; timestamps are "
                "consistent with a separate q00 pilot followed by mixed "
                "q01-through-q47 execution, but cannot certify the exact "
                "scheduler command lines or batch partition"
            ),
        },
        "solver_totals": totals,
        "source_scope": audit_sources(),
        "status_counts": dict(sorted(status_counts.items())),
        "terminal_shards": len(files),
    }


def canonical_bytes(manifest: dict[str, Any]) -> bytes:
    return (
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    ).encode("utf-8")


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(content)
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument(
        "--candidate-directory",
        action="append",
        type=Path,
        dest="candidate_directories",
        help=(
            "candidate directory to require empty; repeatable (defaults to "
            "both the v2 and legacy scheduler locations)"
        ),
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--write-manifest",
        action="store_true",
        help="atomically write the canonical manifest for the audited corpus",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    candidate_directories = tuple(
        args.candidate_directories or DEFAULT_CANDIDATE_DIRECTORIES
    )
    try:
        generated = audit_corpus(args.corpus, candidate_directories)
        generated_bytes = canonical_bytes(generated)
        if args.write_manifest:
            atomic_write(args.manifest, generated_bytes)
        else:
            stored, stored_bytes = load_json(args.manifest)
            if stored != generated:
                raise AuditError("stored manifest content does not match the corpus")
            if stored_bytes != generated_bytes:
                raise AuditError("stored manifest is not in canonical encoding")
        manifest_bytes = args.manifest.read_bytes()
    except (AuditError, OSError) as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 1

    totals = generated["solver_totals"]
    scope = generated["model_scope"]
    print(f"PASS terminal_shards={generated['terminal_shards']}")
    print(
        "status_counts="
        + json.dumps(
            generated["status_counts"],
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    print(f"candidate_file_count={generated['candidate_file_count']}")
    print(
        "projective_labelings="
        f"{scope['normalized_projective_labelings']} normalized, "
        f"{scope['canonical_labelings_before_high_lag_cuts']} row-orbit, "
        f"{scope['canonical_labelings_after_physical_e2_table']} physical-E2"
    )
    print(f"wall_time_seconds={totals['wall_time_seconds']:.6f}")
    print(f"conflicts={totals['conflicts']}")
    print(f"branches={totals['branches']}")
    print(f"booleans={totals['booleans']}")
    print(
        "booleans_range="
        f"{totals['booleans_min']}..{totals['booleans_max']} "
        f"(zero_shards={totals['booleans_zero_shards']})"
    )
    print(f"corpus_sha256={generated['corpus_sha256']}")
    print(
        "source_bundle_sha256="
        f"{generated['source_scope']['source_bundle_sha256']}"
    )
    print(f"manifest_sha256={hashlib.sha256(manifest_bytes).hexdigest()}")
    print("unsat_proof_certificates=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
