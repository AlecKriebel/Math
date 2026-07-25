#!/usr/bin/env python3
"""Strict completeness audit and detached witness replay for production."""

from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any

from production_common import (
    ADDITIVE_COUNTER_KEYS,
    AGGREGATE_SCHEMA,
    BURNSIDE,
    DIAGNOSTIC_COUNTER_KEYS,
    EXACT_ORBIT_POLICY,
    MANIFEST_SCHEMA,
    PREFIX_COUNT,
    PRODUCTION_SCHEMA,
    RESULT_SCHEMA,
    RUNNER_VERSION,
    SHELLS,
    WITNESS_NAMES,
    parse_key_value_output,
    partition_audit,
    prefix_cells,
    require_nonnegative_integer,
    shard_id,
    workload_audit,
)
from production_orbits import ExactOrbit, validate_exact_orbit_output
from verify_dense_shell_classifier_pilot import replay_witness


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "output" / "production"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def selected_shells(value: str) -> tuple[str, ...]:
    return SHELLS if value == "both" else (value,)


def validate_manifest(
    output: Path, requested: tuple[str, ...]
) -> dict[str, object]:
    manifest_path = output / "manifest.json"
    manifest = read_json(manifest_path)
    if not isinstance(manifest, dict):
        raise ValueError("manifest is not an object")
    required = {
        "schema": MANIFEST_SCHEMA,
        "runner_version": RUNNER_VERSION,
        "partition_audit": partition_audit(),
        "workload_audit": workload_audit(),
        "exact_orbit_policy": EXACT_ORBIT_POLICY,
    }
    for key, expected in required.items():
        if manifest.get(key) != expected:
            raise ValueError(f"manifest {key} mismatch")
    source = Path(str(manifest.get("source_path", "")))
    binary = Path(str(manifest.get("binary_path", "")))
    if not source.is_file() or sha256(source) != manifest.get(
        "source_sha256"
    ):
        raise ValueError("manifest source path/hash mismatch")
    if not binary.is_file() or sha256(binary) != manifest.get(
        "binary_sha256"
    ):
        raise ValueError("manifest binary path/hash mismatch")
    expected_shards = manifest.get("expected_shards")
    if not isinstance(expected_shards, dict):
        raise ValueError("manifest expected_shards is malformed")
    for shell in requested:
        expected = [cell.identifier for cell in prefix_cells(shell)]
        if expected_shards.get(shell) != expected:
            raise ValueError(
                f"manifest {shell} expected-shard order mismatch"
            )
    return manifest


def validate_candidate_records(
    output: Path, manifest: dict[str, object]
) -> bool:
    del manifest
    paths = sorted((output / "candidates").glob("*.json"))
    if not paths:
        return False
    raise ValueError(
        "stop-on-first candidate records are incompatible with the "
        "v2 exhaustive-orbit production manifest; use a fresh output "
        f"directory (found {paths[0]})"
    )


def validate_result_record(
    record: object,
    *,
    path: Path,
    shell: str,
    first: int,
    second: int,
    manifest: dict[str, object],
) -> tuple[dict[str, str], tuple[ExactOrbit, ...]]:
    if not isinstance(record, dict):
        raise ValueError(f"{path}: result is not an object")
    identifier = shard_id(shell, first, second)
    binary = str(manifest["binary_path"])
    command = [
        binary,
        "--shell",
        shell,
        "--complete-shard",
        "--enumerate-exact-orbits",
        "--prefix",
        str(first),
        str(second),
    ]
    required = {
        "schema": RESULT_SCHEMA,
        "runner_version": RUNNER_VERSION,
        "shard_id": identifier,
        "shell": shell,
        "prefix_first": first,
        "prefix_second": second,
        "source_sha256": manifest["source_sha256"],
        "binary_sha256": manifest["binary_sha256"],
        "command": command,
        "returncode": 0,
        "complete": True,
        "candidate": False,
    }
    for key, expected in required.items():
        if record.get(key) != expected:
            raise ValueError(
                f"{path}: {key} mismatch "
                f"({record.get(key)!r} != {expected!r})"
            )
    parsed = record.get("parsed")
    transcript = record.get("transcript")
    if (
        not isinstance(parsed, dict)
        or not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in parsed.items()
        )
        or not isinstance(transcript, str)
        or parse_key_value_output(transcript) != parsed
    ):
        raise ValueError(f"{path}: transcript/parse mismatch")
    required_output = {
        "schema": PRODUCTION_SCHEMA,
        "mode": "complete_shard",
        "shell": shell,
        "shard_id": identifier,
        "prefix_first": str(first),
        "prefix_second": str(second),
        "upper_exact_scope": "char2_mod9_intersection",
        "shard_complete": "1",
        "exact_orbit_mode": "enumerate",
        "exact_orbit_collection": "complete_shard",
    }
    for key, expected in required_output.items():
        if parsed.get(key) != expected:
            raise ValueError(
                f"{path}: output {key} mismatch "
                f"({parsed.get(key)!r} != {expected!r})"
            )
    for key in (*ADDITIVE_COUNTER_KEYS, *DIAGNOSTIC_COUNTER_KEYS):
        require_nonnegative_integer(parsed, key)
    exact_orbits = validate_exact_orbit_output(
        parsed, shell, expected_collection="complete_shard"
    )
    for witness in WITNESS_NAMES[:-1]:
        replay_witness(parsed, witness, shell)
    return parsed, exact_orbits


def aggregate_shell(
    output: Path,
    shell: str,
    manifest: dict[str, object],
) -> dict[str, object]:
    cells = prefix_cells(shell)
    expected_names = {
        f"{cell.identifier}.json" for cell in cells
    }
    result_directory = output / "results"
    actual_names = {
        path.name
        for path in result_directory.glob(f"{shell}-*.json")
    }
    missing = sorted(expected_names - actual_names)
    extras = sorted(actual_names - expected_names)
    if missing or extras:
        raise ValueError(
            f"{shell}: result set mismatch: "
            f"{len(missing)} missing, {len(extras)} extras"
        )

    sums: dict[str, int] = defaultdict(int)
    diagnostics: dict[str, int] = defaultdict(int)
    identities: set[str] = set()
    retained_witnesses = 0
    retained_exact_orbits = 0
    exact_orbits: dict[
        tuple[tuple[int, ...], int],
        tuple[ExactOrbit, list[str]],
    ] = {}
    for cell in cells:
        path = result_directory / f"{cell.identifier}.json"
        record = read_json(path)
        parsed, shard_orbits = validate_result_record(
            record,
            path=path,
            shell=shell,
            first=cell.first,
            second=cell.second,
            manifest=manifest,
        )
        if parsed["shard_id"] in identities:
            raise ValueError(
                f"{shell}: duplicate shard identity "
                f"{parsed['shard_id']}"
            )
        identities.add(parsed["shard_id"])
        if (
            require_nonnegative_integer(
                parsed, "raw_skeletons_seen"
            )
            != cell.raw_skeletons
            or require_nonnegative_integer(
                parsed, "raw_decorations_seen"
            )
            != cell.raw_decorations
        ):
            raise ValueError(
                f"{cell.identifier}: prefix census mismatch"
            )
        if require_nonnegative_integer(
            parsed, "canonical_decorations_seen"
        ) != require_nonnegative_integer(
            parsed, "canonical_decorations_processed"
        ):
            raise ValueError(
                f"{cell.identifier}: complete shard skipped a canonical "
                "decoration"
            )
        for key in ADDITIVE_COUNTER_KEYS:
            sums[key] += require_nonnegative_integer(parsed, key)
        for key in DIAGNOSTIC_COUNTER_KEYS:
            diagnostics[key] += require_nonnegative_integer(parsed, key)
        retained_witnesses += sum(
            require_nonnegative_integer(parsed, f"{name}_present")
            for name in WITNESS_NAMES
        )
        retained_exact_orbits += len(shard_orbits)
        for orbit in shard_orbits:
            existing = exact_orbits.get(orbit.key)
            if existing is None:
                exact_orbits[orbit.key] = (
                    orbit,
                    [cell.identifier],
                )
            else:
                retained, sources = existing
                if retained != orbit:
                    raise ValueError(
                        f"{cell.identifier}: canonical exact-orbit "
                        "record disagrees across shards"
                    )
                sources.append(cell.identifier)

    expected = BURNSIDE[shell]
    exact_checks = {
        "raw_skeletons_seen": expected["raw_skeletons"],
        "raw_decorations_seen": expected["raw_decorations"],
        "canonical_decorations_seen":
            expected["canonical_decorations"],
        "canonical_decorations_processed":
            expected["canonical_decorations"],
        "weighted_decorations_processed":
            expected["raw_decorations"],
    }
    for key, wanted in exact_checks.items():
        if sums[key] != wanted:
            raise ValueError(
                f"{shell}: aggregate {key} mismatch "
                f"({sums[key]} != {wanted})"
            )
    if (
        sums["weighted_exact_zero_hits"] < sums["exact_zero_hits"]
        or sums["mod27_hits"] < sums["exact_zero_hits"]
        or sums["post_mod9_lambda_hits"] < sums["exact_zero_hits"]
        or sums["char2_mod9_hits"] < sums["exact_zero_hits"]
    ):
        raise ValueError(f"{shell}: aggregate exact-hit accounting failed")
    orbit_rows = []
    for key in sorted(exact_orbits):
        orbit, sources = exact_orbits[key]
        row = orbit.as_dict()
        row["source_shards"] = sorted(sources)
        orbit_rows.append(row)
    return {
        "prefix_shards": len(identities),
        "complete": len(identities) == PREFIX_COUNT,
        "upper_exact_scope": "char2_mod9_intersection",
        "counters": dict(sums),
        "diagnostic_idlex_coincidence_counters": dict(diagnostics),
        "retained_witnesses_independently_replayed": retained_witnesses,
        "retained_exact_orbits_across_shards": retained_exact_orbits,
        "distinct_canonical_exact_profile_orbits":
            len(exact_orbits),
        "exact_profile_orbits": orbit_rows,
        "burnside_weighted_partition_check": "PASS",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT
    )
    parser.add_argument(
        "--shell", choices=("both", *SHELLS), default="both"
    )
    parser.add_argument(
        "--aggregate-output",
        type=Path,
        help="default: OUTPUT/aggregate-{shell}.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    requested = selected_shells(args.shell)
    manifest = validate_manifest(output, requested)
    if validate_candidate_records(output, manifest):
        return 2
    known_result_names = {
        f"{cell.identifier}.json"
        for shell in SHELLS
        for cell in prefix_cells(shell)
    }
    unknown_results = sorted(
        path.name
        for path in (output / "results").glob("*.json")
        if path.name not in known_result_names
    )
    if unknown_results:
        raise ValueError(
            "unknown result files: " + ", ".join(unknown_results)
        )
    summaries = {
        shell: aggregate_shell(output, shell, manifest)
        for shell in requested
    }
    aggregate = {
        "schema": AGGREGATE_SCHEMA,
        "source_sha256": manifest["source_sha256"],
        "binary_sha256": manifest["binary_sha256"],
        "shells": summaries,
        "status": "PASS: every required prefix shard is complete",
    }
    destination = (
        args.aggregate_output.resolve()
        if args.aggregate_output
        else output
        / (
            "aggregate-both.json"
            if len(requested) == 2
            else f"aggregate-{requested[0]}.json"
        )
    )
    atomic_json(destination, aggregate)
    print(
        f"PASS: strict complete-shell aggregate written to {destination}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
