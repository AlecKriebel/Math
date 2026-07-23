#!/usr/bin/env python3
"""Strict, standard-library audit of the 48 x 8 common-type CP corpus.

This verifier checks the integrity and internal consistency of the recorded
CP-SAT shard results.  It deliberately does not import OR-Tools or claim to
re-prove an ``INFEASIBLE`` result from a solver certificate: CP-SAT did not
emit such certificates.  Instead it attests that the corpus has exactly one
terminal record for every advertised shard, that every record and its solver
transcript agree, that no candidate or nonterminal status was recorded, and
that the stored byte hashes match a deterministic manifest.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any, Iterable


BASE = Path(__file__).resolve().parent
DEFAULT_CORPUS = BASE / "output" / "five_comb_common_type_cp"
DEFAULT_MANIFEST = BASE / "FIVE_COMB_COMMON_TYPE_CORPUS_MANIFEST.json"

QUARTET_COUNT = 48
PROJECTIVE_COUNT = 8
SHARD_COUNT = QUARTET_COUNT * PROJECTIVE_COUNT
CORPUS_FORMAT = "h668-five-comb-common-type-shard-v1"
MANIFEST_FORMAT = "h668-five-comb-common-type-corpus-manifest-v1"
SOLVER_SCRIPT = "search_five_comb_common_type_cp_sat.py"

RECORD_KEYS = {
    "booleans",
    "branches",
    "command",
    "conflicts",
    "finished_at",
    "format",
    "projective",
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
    "projective",
    "quartet",
    "status",
    "wall_time",
}
COMMAND_FLAGS = {
    "--max-memory-mb",
    "--projective",
    "--quartet",
    "--time-limit",
    "--workers",
}


class AuditError(ValueError):
    """Raised when a corpus or manifest invariant fails."""


def expected_names() -> tuple[str, ...]:
    return tuple(
        f"q{quartet:02d}_p{projective}.json"
        for quartet in range(QUARTET_COUNT)
        for projective in range(PROJECTIVE_COUNT)
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
        text = raw.decode("utf-8")
        value = json.loads(
            text,
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
    command: list[str], quartet: int, projective: int, label: str
) -> str:
    if len(command) < 2 or Path(command[1]).name != SOLVER_SCRIPT:
        raise AuditError(f"{label} does not invoke {SOLVER_SCRIPT}")
    tail = command[2:]
    if len(tail) % 2:
        raise AuditError(f"{label} has an unpaired option")
    options: dict[str, str] = {}
    for flag, value in zip(tail[::2], tail[1::2]):
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
        command_projective = int(options["--projective"])
        time_limit = float(options["--time-limit"])
        workers = int(options["--workers"])
        memory = int(options["--max-memory-mb"])
    except ValueError as error:
        raise AuditError(f"{label} has nonnumeric solver options") from error
    if command_quartet != quartet or command_projective != projective:
        raise AuditError(f"{label} shard identity disagrees with its record")
    if not math.isfinite(time_limit) or time_limit <= 0:
        raise AuditError(f"{label} has an invalid time limit")
    if workers <= 0 or memory <= 0:
        raise AuditError(f"{label} has invalid worker or memory metadata")
    return "subprocess"


def validate_command(
    value: Any, quartet: int, projective: int, label: str
) -> str:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(item, str) for item in value)
    ):
        raise AuditError(f"{label} must be a nonempty string list")
    if value[0] == "in-process":
        expected = ["in-process", f"q={quartet}", f"p={projective}"]
        if value != expected:
            raise AuditError(f"{label} in-process shard identity is malformed")
        return "in-process"
    return parse_subprocess_command(value, quartet, projective, label)


def validate_record(
    path: Path, quartet: int, projective: int
) -> tuple[dict[str, Any], bytes]:
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
        require_exact_int(payload["projective"], f"{label}.projective")
        != projective
    ):
        raise AuditError(f"{label} has the wrong projective identity")
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

    mode = validate_command(
        payload["command"], quartet, projective, f"{label}.command"
    )
    transcript = parse_transcript(payload["stdout"], f"{label}.stdout")
    if transcript["status"] != payload["status"]:
        raise AuditError(f"{label} transcript status disagrees")
    transcript_integers = {
        "quartet": quartet,
        "projective": projective,
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
            "projective": projective,
            "quartet": quartet,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "size_bytes": len(raw),
            "started_at": payload["started_at"],
            "status": payload["status"],
            "wall_time_seconds": wall_time,
        },
        raw,
    )


def _framed_corpus_hash(records: list[tuple[str, bytes]]) -> str:
    digest = hashlib.sha256()
    for name, raw in records:
        encoded_name = name.encode("utf-8")
        digest.update(len(encoded_name).to_bytes(4, "big"))
        digest.update(encoded_name)
        digest.update(len(raw).to_bytes(8, "big"))
        digest.update(raw)
    return digest.hexdigest()


def audit_corpus(corpus: Path) -> dict[str, Any]:
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
    for quartet in range(QUARTET_COUNT):
        for projective in range(PROJECTIVE_COUNT):
            name = f"q{quartet:02d}_p{projective}.json"
            record, raw = validate_record(corpus / name, quartet, projective)
            files.append(record)
            framed_records.append((name, raw))

    candidate_files = sorted(
        path.name
        for path in corpus.parent.glob("five_comb_common_q*_p*.json")
        if path.is_file()
    )
    if candidate_files:
        raise AuditError(f"candidate files are present: {candidate_files}")

    status_counts = Counter(record["status"] for record in files)
    command_modes = Counter(record["command_mode"] for record in files)
    if status_counts != Counter({"INFEASIBLE": SHARD_COUNT}):
        raise AuditError(f"unexpected terminal status counts: {status_counts}")
    booleans = [record["booleans"] for record in files]
    return {
        "candidate_file_count": 0,
        "command_mode_counts": dict(sorted(command_modes.items())),
        "corpus_directory": "output/five_comb_common_type_cp",
        "corpus_format": CORPUS_FORMAT,
        "corpus_sha256": _framed_corpus_hash(framed_records),
        "files": files,
        "format": MANIFEST_FORMAT,
        "grid": {
            "projectives": PROJECTIVE_COUNT,
            "quartets": QUARTET_COUNT,
        },
        "hash_scheme": (
            "sha256 over sorted records framed as "
            "uint32be(name_bytes)||name_bytes||uint64be(content_bytes)||content_bytes"
        ),
        "solver_totals": {
            "booleans_max": max(booleans),
            "booleans_min": min(booleans),
            "branches": sum(record["branches"] for record in files),
            "conflicts": sum(record["conflicts"] for record in files),
            "wall_time_seconds": round(
                math.fsum(record["wall_time_seconds"] for record in files), 6
            ),
        },
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
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--write-manifest",
        action="store_true",
        help="atomically replace the manifest with the current audited corpus",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        generated = audit_corpus(args.corpus)
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
    print(f"wall_time_seconds={totals['wall_time_seconds']:.6f}")
    print(f"conflicts={totals['conflicts']}")
    print(f"branches={totals['branches']}")
    print(
        f"booleans_range={totals['booleans_min']}..{totals['booleans_max']}"
    )
    print(f"corpus_sha256={generated['corpus_sha256']}")
    print(f"manifest_sha256={hashlib.sha256(manifest_bytes).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
