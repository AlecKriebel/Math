#!/usr/bin/env python3
"""Strict standard-library audit of the q39 unrestricted-core CP corpus.

The audit checks byte integrity, shard coverage, mixed subprocess/in-process
metadata, solver-transcript consistency, source hashes, and the exact
projective-core scope.  It deliberately does not import OR-Tools and does not
re-prove a solver ``INFEASIBLE`` result: these runs contain no independently
checkable UNSAT proof certificates.

The executed solver source is recoverable exactly from the current source.
After the corpus finished, a universal lag-81 cut and an exact high-lag
boundary table were inserted.  Removing those pinned additions reproduces
the 27,414-byte source whose retained CPython-3.12 code object was checked
byte-for-byte during this audit.  Thus the recorded runs used a weaker model
than the current source; an ``INFEASIBLE`` result for the executed model also
covers both later strengthenings.
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
from typing import Any, Iterable


BASE = Path(__file__).resolve().parent
DEFAULT_CORPUS = BASE / "output" / "five_comb_unrestricted_core_cp"
DEFAULT_CANDIDATES = (
    BASE / "output" / "five_comb_unrestricted_core_candidates"
)
DEFAULT_MANIFEST = BASE / "FIVE_COMB_UNRESTRICTED_CORE_CORPUS_MANIFEST.json"

QUARTET = 39
CORE_COUNT = 32
SHARD_COUNT = CORE_COUNT
CORPUS_FORMAT = "h668-five-comb-unrestricted-core-shard-v1"
MANIFEST_FORMAT = "h668-five-comb-unrestricted-core-corpus-manifest-v1"
SOLVER_SCRIPT = "search_five_comb_unrestricted_projective_cp_sat.py"
SCHEDULER_SCRIPT = "run_five_comb_unrestricted_core_shards.py"

EXECUTED_SOLVER_SHA256 = (
    "f6781fd615ff9e189e5ea37cd4af5b3791d4bc7bac10bca726cb7310b7d2194f"
)
EXECUTED_SOLVER_SIZE = 27_414
EXECUTED_CODE_OBJECT_SHA256 = (
    "b8f503b4025fd04eb4a0bb951a4a0ceb58a6b4ca7b4dee048fcc504755eff49d"
)
SOURCE_EXPECTATIONS = {
    "check_five_comb_mub_reductions.py": (
        19_482,
        "56bea0e45f06bfc7918318b670e43463b0991b219015b44b73f826ada7e183df",
        "finite quartet, projective-vector, and modulo-four constants",
    ),
    "run_five_comb_unrestricted_core_shards.py": (
        9_383,
        "cb054c5bf1ee7c09982c5f5ae10c50a67399f06f52897e0ae565a3a1678551ba",
        "current resume-safe scheduler and record writer",
    ),
    "search_five_comb_common_type_cp_sat.py": (
        16_839,
        "d50214cff57710687b5ca8152adfe0457b5616665393fd9d5f270b2c9c7036c2",
        "shared contribution tables and row-sum profiles",
    ),
    SOLVER_SCRIPT: (
        31_254,
        "76dc604f0bb61ebeb5a9892f9d63c7b193fbee68beb47b2abc6e04aa575ff06b",
        "current exact model, including both post-corpus strengthenings",
    ),
    "verify_five_comb_high_lag_boundary.py": (
        26_989,
        "9c71073ca53e5e4783cbd912f1196feb17c8eb3e148e29ae8d9d379f4976f127",
        "post-corpus exact lags-78-through-81 boundary-table derivation",
    ),
}

POST_CORPUS_STRENGTHENING = b"""\
    # Lag 81 alone excludes the all-zero corner of these four parameters.
    model.add_bool_or(
        (
            label_bits[2][0],  # beta
            label_bits[7][2],  # u7
            label_bits[1][1],  # y1
            label_bits[7][1],  # y7
        )
    )
"""
POST_CORPUS_STRENGTHENING_SHA256 = (
    "9469172dce397409d2a81cbba4f2bb19bd74e76becec6aac8d4efb4a2465b01c"
)
POST_CORPUS_BOUNDARY_IMPORT = (
    b"from verify_five_comb_high_lag_boundary import e2_boundary_rows\n"
)
POST_CORPUS_BOUNDARY_BLOCKS = {
    "import": (
        64,
        "d8913dc1512ccf7134a216a19530f6556875436caffab45c4e931d1fa9ef6849",
    ),
    "helpers": (
        3_355,
        "1eff21cf9e85bc0c200935a0cd24690e4677a2dad0e3bea28289834043102948",
    ),
    "model_call": (
        153,
        "5944d5e74426b3bb7afae1b581d61739561c504f7963b4b0fa5c39cda5a5d98d",
    ),
}

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
COMMAND_FLAGS = {
    "--max-memory-mb",
    "--output",
    "--projective-core",
    "--quartet",
    "--time-limit",
    "--workers",
}


class AuditError(ValueError):
    """Raised when a corpus, source, or manifest invariant fails."""


def expected_names() -> tuple[str, ...]:
    return tuple(f"q{QUARTET:02d}_core{core:02d}.json" for core in range(32))


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


def require_exact_int(value: Any, label: str, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise AuditError(f"{label} must be an integer")
    if minimum is not None and value < minimum:
        raise AuditError(f"{label} must be at least {minimum}")
    return value


def require_finite_number(
    value: Any, label: str, *, positive: bool = False
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


def parse_subprocess_command(
    command: list[str], core: int, label: str
) -> tuple[str, Path]:
    if len(command) < 2 or Path(command[1]).name != SOLVER_SCRIPT:
        raise AuditError(f"{label} does not invoke {SOLVER_SCRIPT}")
    tail = command[2:]
    if len(tail) % 2:
        raise AuditError(f"{label} has an unpaired option")
    options: dict[str, str] = {}
    for flag, value in zip(tail[::2], tail[1::2], strict=True):
        if flag in options:
            raise AuditError(f"{label} repeats {flag}")
        options[flag] = value
    if set(options) != COMMAND_FLAGS:
        raise AuditError(
            f"{label} flags differ: missing={sorted(COMMAND_FLAGS - set(options))}, "
            f"extra={sorted(set(options) - COMMAND_FLAGS)}"
        )
    try:
        command_quartet = int(options["--quartet"])
        command_core = int(options["--projective-core"])
        time_limit = float(options["--time-limit"])
        workers = int(options["--workers"])
        memory = int(options["--max-memory-mb"])
    except ValueError as error:
        raise AuditError(f"{label} has nonnumeric solver options") from error
    if command_quartet != QUARTET or command_core != core:
        raise AuditError(f"{label} shard identity disagrees with its record")
    if time_limit != 90.0 or workers != 2 or memory != 3072:
        raise AuditError(f"{label} solver limits differ from the recorded run")
    output = Path(options["--output"])
    if output.name != f"q{QUARTET:02d}_core{core:02d}_candidate.json":
        raise AuditError(f"{label} has the wrong candidate output name")
    if output.parent.name != DEFAULT_CANDIDATES.name:
        raise AuditError(f"{label} has the wrong candidate output directory")
    return "subprocess", output


def validate_command(value: Any, core: int, label: str) -> tuple[str, Path]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) for item in value)
    ):
        raise AuditError(f"{label} must be a nonempty string list")
    if value[0] == "in-process":
        expected = ["in-process", f"q={QUARTET}", f"core={core}"]
        if value != expected:
            raise AuditError(f"{label} in-process shard identity is malformed")
        output = (
            DEFAULT_CANDIDATES
            / f"q{QUARTET:02d}_core{core:02d}_candidate.json"
        )
        return "in-process", output
    return parse_subprocess_command(value, core, label)


def validate_record(path: Path, core: int) -> tuple[dict[str, Any], bytes, Path]:
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
    if require_exact_int(payload["quartet"], f"{label}.quartet") != QUARTET:
        raise AuditError(f"{label} has the wrong quartet identity")
    if (
        require_exact_int(payload["projective_core"], f"{label}.projective_core")
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
        payload["wall_time_seconds"], f"{label}.wall_time_seconds", positive=True
    )
    conflicts = require_exact_int(
        payload["conflicts"], f"{label}.conflicts", minimum=0
    )
    branches = require_exact_int(
        payload["branches"], f"{label}.branches", minimum=0
    )
    booleans = require_exact_int(
        payload["booleans"], f"{label}.booleans", minimum=1
    )
    started = parse_timestamp(payload["started_at"], f"{label}.started_at")
    finished = parse_timestamp(payload["finished_at"], f"{label}.finished_at")
    if finished < started:
        raise AuditError(f"{label} finishes before it starts")
    if (finished - started).total_seconds() + 0.05 < wall_time:
        raise AuditError(f"{label} solver wall time exceeds its recorded interval")

    mode, candidate = validate_command(payload["command"], core, f"{label}.command")
    expected_mode = "subprocess" if core <= 8 else "in-process"
    if mode != expected_mode:
        raise AuditError(
            f"{label} command mode is {mode}, expected {expected_mode}"
        )
    if candidate.exists():
        raise AuditError(f"{label} has a surviving candidate file: {candidate}")

    transcript = parse_transcript(payload["stdout"], f"{label}.stdout")
    if transcript["status"] != payload["status"]:
        raise AuditError(f"{label} transcript status disagrees")
    transcript_integers = {
        "quartet": QUARTET,
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
    if not math.isclose(
        transcript_wall_time, wall_time, rel_tol=0.0, abs_tol=0.5e-6
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
            "quartet": QUARTET,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "size_bytes": len(raw),
            "started_at": payload["started_at"],
            "status": payload["status"],
            "wall_time_seconds": wall_time,
        },
        raw,
        candidate,
    )


def normalized_projective_labels(parameters: tuple[int, ...]) -> tuple[int, ...]:
    """Independent standard-library replay of the twelve-bit parametrization."""

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


def row_orbit_is_canonical(labels: tuple[int, ...]) -> bool:
    middle = tuple((label >> 1) & 1 for label in labels[1:])
    low = tuple(label & 1 for label in labels[1:])
    high = tuple((label >> 2) & 1 for label in labels[1:])
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
    labelings: set[tuple[int, ...]] = set()
    raw_by_core = [0] * CORE_COUNT
    executed_by_core = [0] * CORE_COUNT
    current_by_core = [0] * CORE_COUNT
    for parameters in product((0, 1), repeat=12):
        labels = normalized_projective_labels(parameters)
        labelings.add(labels)
        core = sum(parameters[bit] << bit for bit in range(5))
        raw_by_core[core] += 1
        if not row_orbit_is_canonical(labels):
            continue
        executed_by_core[core] += 1
        # Current-only strengthening: beta OR u7 OR y1 OR y7.
        if parameters[1] or parameters[4] or parameters[5] or parameters[11]:
            current_by_core[core] += 1

    expected_executed = [
        128, 32, 32, 32, 64, 32, 32, 32,
        64, 64, 32, 32, 64, 32, 32, 32,
        64, 32, 64, 32, 64, 32, 32, 32,
        64, 32, 32, 64, 64, 32, 32, 32,
    ]
    expected_current = [
        96, 24, 32, 32, 48, 24, 32, 32,
        48, 48, 32, 32, 48, 24, 32, 32,
        64, 32, 64, 32, 64, 32, 32, 32,
        64, 32, 32, 64, 64, 32, 32, 32,
    ]
    if len(labelings) != 4096 or raw_by_core != [128] * CORE_COUNT:
        raise AuditError("the 32 projective cores do not partition 4,096 maps")
    if executed_by_core != expected_executed or sum(executed_by_core) != 1440:
        raise AuditError("the executed row-pair orbit scope changed")
    if current_by_core != expected_current or sum(current_by_core) != 1320:
        raise AuditError("the current lag-81-strengthened scope changed")
    return {
        "canonical_labelings_by_core_after_lag81_cut": current_by_core,
        "canonical_labelings_by_core_executed": executed_by_core,
        "canonical_labelings_after_lag81_cut": sum(current_by_core),
        "canonical_labelings_executed": sum(executed_by_core),
        "core_bit_order_little_endian": ["alpha", "beta", "u5", "u6", "u7"],
        "normalized_projective_labelings": len(labelings),
        "raw_labelings_per_core": 128,
    }


def audit_sources() -> dict[str, Any]:
    records = []
    source_bytes: dict[str, bytes] = {}
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
        source_bytes[relative] = raw
        records.append(
            {
                "path": relative,
                "role": role,
                "sha256": actual_hash,
                "size_bytes": len(raw),
            }
        )

    solver = source_bytes[SOLVER_SCRIPT]
    if solver.count(POST_CORPUS_STRENGTHENING) != 1:
        raise AuditError("the post-corpus strengthening block is not unique")
    if hashlib.sha256(POST_CORPUS_STRENGTHENING).hexdigest() != (
        POST_CORPUS_STRENGTHENING_SHA256
    ):
        raise AuditError("the embedded strengthening block hash changed")

    if solver.count(POST_CORPUS_BOUNDARY_IMPORT) != 1:
        raise AuditError("the post-corpus boundary import is not unique")
    helper_start = b"def projective_parameter_variables("
    helper_end = b"def projective_row_orbit_is_canonical("
    if solver.count(helper_start) != 1 or solver.count(helper_end) != 1:
        raise AuditError("the post-corpus boundary helper markers changed")
    helper_left = solver.index(helper_start)
    helper_right = solver.index(helper_end)
    boundary_helpers = solver[helper_left:helper_right]

    call_start = b"    add_physical_high_lag_boundary_table(\n"
    call_end = b"    # Channel only the boundary coefficients"
    if solver.count(call_start) != 1 or solver.count(call_end) != 1:
        raise AuditError("the post-corpus boundary-call markers changed")
    call_left = solver.index(call_start)
    call_right = solver.index(call_end, call_left)
    boundary_call = solver[call_left:call_right]
    boundary_blocks = {
        "helpers": boundary_helpers,
        "import": POST_CORPUS_BOUNDARY_IMPORT,
        "model_call": boundary_call,
    }
    for name, block in boundary_blocks.items():
        expected_size, expected_hash = POST_CORPUS_BOUNDARY_BLOCKS[name]
        if (
            len(block) != expected_size
            or hashlib.sha256(block).hexdigest() != expected_hash
        ):
            raise AuditError(f"the post-corpus {name} block changed")

    executed = solver.replace(POST_CORPUS_BOUNDARY_IMPORT, b"", 1)
    executed = executed.replace(boundary_helpers, b"", 1)
    executed = executed.replace(POST_CORPUS_STRENGTHENING, b"", 1)
    # The inserted call occupied a pre-existing blank separator line.
    executed = executed.replace(boundary_call, b"\n", 1)
    if len(executed) != EXECUTED_SOLVER_SIZE:
        raise AuditError("the reconstructed executed solver has the wrong size")
    if hashlib.sha256(executed).hexdigest() != EXECUTED_SOLVER_SHA256:
        raise AuditError("the reconstructed executed solver hash changed")

    return {
        "executed_solver_source": {
            "historical_cpython": "3.12.13",
            "marshaled_code_object_sha256": EXECUTED_CODE_OBJECT_SHA256,
            "path": SOLVER_SCRIPT,
            "reconstruction": (
                "current source minus the exact post-corpus lag-81 cut and "
                "E2 high-lag boundary-table additions"
            ),
            "sha256": EXECUTED_SOLVER_SHA256,
            "size_bytes": EXECUTED_SOLVER_SIZE,
        },
        "post_corpus_strengthenings": [
            {
                "effect": (
                    "removes 120 of 1,440 canonical projective labelings"
                ),
                "name": "lag-81 projective BoolOr",
                "sha256": POST_CORPUS_STRENGTHENING_SHA256,
                "size_bytes": len(POST_CORPUS_STRENGTHENING),
            },
            {
                "effect": (
                    "channels the exact physical-hole equations at lags "
                    "78 through 81; the corpus already excluded the weaker "
                    "model without this table"
                ),
                "name": "E2 high-lag boundary table",
                "source_blocks": [
                    {
                        "name": name,
                        "sha256": digest,
                        "size_bytes": size,
                    }
                    for name, (size, digest) in sorted(
                        POST_CORPUS_BOUNDARY_BLOCKS.items()
                    )
                ],
            },
        ],
        "source_files": records,
    }


def _framed_corpus_hash(records: list[tuple[str, bytes]]) -> str:
    digest = hashlib.sha256()
    for name, raw in records:
        encoded_name = name.encode("utf-8")
        digest.update(len(encoded_name).to_bytes(4, "big"))
        digest.update(encoded_name)
        digest.update(len(raw).to_bytes(8, "big"))
        digest.update(raw)
    return digest.hexdigest()


def audit_corpus(corpus: Path, candidates: Path) -> dict[str, Any]:
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
    expected_candidate_paths: set[Path] = set()
    for core, name in enumerate(expected):
        record, raw, candidate = validate_record(corpus / name, core)
        files.append(record)
        framed_records.append((name, raw))
        expected_candidate_paths.add(candidate.resolve())

    candidate_files = (
        sorted(path.resolve() for path in candidates.rglob("*") if path.is_file())
        if candidates.exists()
        else []
    )
    if candidate_files:
        raise AuditError(f"candidate files are present: {candidate_files}")
    if any(path.exists() for path in expected_candidate_paths):
        raise AuditError("an expected shard candidate file is present")

    status_counts = Counter(record["status"] for record in files)
    command_modes = Counter(record["command_mode"] for record in files)
    if status_counts != Counter({"INFEASIBLE": SHARD_COUNT}):
        raise AuditError(f"unexpected terminal status counts: {status_counts}")
    if command_modes != Counter({"in-process": 23, "subprocess": 9}):
        raise AuditError(f"unexpected command-mode counts: {command_modes}")

    booleans = [record["booleans"] for record in files]
    source_scope = audit_sources()
    projective_scope = audit_projective_scope()
    return {
        "candidate_file_count": 0,
        "command_mode_counts": dict(sorted(command_modes.items())),
        "corpus_directory": "output/five_comb_unrestricted_core_cp",
        "corpus_format": CORPUS_FORMAT,
        "corpus_sha256": _framed_corpus_hash(framed_records),
        "files": files,
        "format": MANIFEST_FORMAT,
        "grid": {
            "projective_cores": CORE_COUNT,
            "quartet": QUARTET,
        },
        "hash_scheme": (
            "sha256 over sorted records framed as "
            "uint32be(name_bytes)||name_bytes||uint64be(content_bytes)||content_bytes"
        ),
        "model_scope": {
            **projective_scope,
            "carrier_family": (
                "quartet 39 common-type five-comb packing with an arbitrary "
                "permutation of eight polarized types, carrier orientations, "
                "and physical hole signs"
            ),
            "exact_constraints": (
                "all 83 aperiodic correlation equations plus the row-square "
                "identity, modulo-four fiber, high-lag Boolean channeling, "
                "and verified construction symmetries"
            ),
            "scope_limit": (
                "this is one unrestricted-projective common-type quartet "
                "family, not all five-comb packings and not all BS(84,83)"
            ),
        },
        "proof_status": {
            "independent_unsat_certificates": 0,
            "meaning": (
                "INFEASIBLE is CP-SAT's recorded terminal status; this corpus "
                "audit checks records and integrity but does not re-prove UNSAT"
            ),
        },
        "solver_totals": {
            "booleans_max": max(booleans),
            "booleans_min": min(booleans),
            "branches": sum(record["branches"] for record in files),
            "conflicts": sum(record["conflicts"] for record in files),
            "wall_time_seconds": round(
                math.fsum(record["wall_time_seconds"] for record in files), 6
            ),
        },
        "source_scope": source_scope,
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
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--write-manifest",
        action="store_true",
        help="atomically write the canonical manifest for the audited corpus",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        generated = audit_corpus(args.corpus, args.candidates)
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
        + json.dumps(generated["status_counts"], sort_keys=True, separators=(",", ":"))
    )
    print(
        "command_mode_counts="
        + json.dumps(
            generated["command_mode_counts"], sort_keys=True, separators=(",", ":")
        )
    )
    print(f"candidate_file_count={generated['candidate_file_count']}")
    print(
        "canonical_labelings="
        f"{scope['canonical_labelings_executed']} executed, "
        f"{scope['canonical_labelings_after_lag81_cut']} after-lag81"
    )
    print(f"wall_time_seconds={totals['wall_time_seconds']:.6f}")
    print(f"conflicts={totals['conflicts']}")
    print(f"branches={totals['branches']}")
    print(f"booleans_range={totals['booleans_min']}..{totals['booleans_max']}")
    print(f"corpus_sha256={generated['corpus_sha256']}")
    print(f"manifest_sha256={hashlib.sha256(manifest_bytes).hexdigest()}")
    print("unsat_proof_certificates=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
