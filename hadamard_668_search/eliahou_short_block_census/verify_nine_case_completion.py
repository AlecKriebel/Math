#!/usr/bin/env python3
"""Strictly verify the complete nine-case short-block Eliahou census.

The default verification is independent of the ignored production output.
It validates the tracked certificate, both pinned base certificates, all
tracked source hashes, exact search-space arithmetic, regenerated models,
and independent NumPy/physical replays of every case's global best witness
and the two exceptional fallback-gauge quotients.

``--live`` additionally validates the exact config, aggregate, model,
binary, and range-manifest sets in all nine ignored production directories.
It hashes every normalized semantic field of every range (not merely the
survivor streams), recomputes all totals and retained witnesses, and reruns
the exceptional quotients in both gauged and ungauged C++ modes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import subprocess
import sys
from typing import Any, Iterable


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
CASE26_DIR = SEARCH / "eliahou_global_quotient_plan"
CERTIFICATE_PATH = HERE / "NINE_CASE_COMPLETION_CERTIFICATE.json"
ALGEBRA_CERTIFICATE_PATH = HERE / "SHORT_BLOCK_CERTIFICATE.json"
CASE26_CERTIFICATE_PATH = CASE26_DIR / "COMPLETION_CERTIFICATE.json"
INVENTORY_PATH = HERE / "ARTIFACT_SHA256.txt"
DEFAULT_SHORT_OUTPUT = HERE / "output"
DEFAULT_CASE26_OUTPUT = CASE26_DIR / "output" / "production"

CERTIFICATE_SCHEMA = "h668-eliahou-short-block-nine-case-completion-v1"
SHORT_CONFIG_SCHEMA = "h668-eliahou-short-block-production-v1"
SHORT_AGGREGATE_SCHEMA = "h668-eliahou-short-block-aggregate-v1"
SHORT_RANGE_SCHEMA = "h668-eliahou-short-block-range-v1"
CASE26_CONFIG_SCHEMA = "h668-case26-global-quotient-production-v1"
CASE26_AGGREGATE_SCHEMA = "h668-case26-global-quotient-aggregate-v1"
CASE26_RANGE_SCHEMA = "h668-case26-global-quotient-range-v1"
CASE26_CERTIFICATE_SCHEMA = (
    "h668-case26-global-quotient-completion-certificate-v1"
)

CASES = tuple(range(21, 30))
Q_INDICES = tuple(range(2, 20, 2))
CASE_TO_Q = dict(zip(CASES, Q_INDICES))
EXCEPTIONAL_QUOTIENTS = {24: 156_922, 27: 6_143}
QUOTIENT_DIMENSION = 18
QUOTIENT_STATES = 1 << QUOTIENT_DIMENSION
CHUNK_SIZE = 1 << 10
RANGE_COUNT = QUOTIENT_STATES // CHUNK_SIZE
L_GAUGE_ROWS_PER_STATE = 2 * ((1 << 19) + (1 << 18))
S_GAUGE_ROWS_PER_STATE = 2 * ((1 << 20) + (1 << 17))
NORMAL_CASE_ROWS = QUOTIENT_STATES * L_GAUGE_ROWS_PER_STATE
EXCEPTIONAL_SURCHARGE = S_GAUGE_ROWS_PER_STATE - L_GAUGE_ROWS_PER_STATE
TOTAL_JOIN_ROWS = 3_710_853_316_608
HEX64 = re.compile(r"^[0-9a-f]{64}$")

PERFORMANCE_RANGE_KEYS = frozenset(
    {"kernel_seconds", "join_rows_per_second"}
)
COMMON_RANGE_KEYS = frozenset(
    {
        "best_witness",
        "bitpacked_physical_replays",
        "block",
        "case",
        "central_values_per_state",
        "exact_candidates",
        "exact_integer_supports",
        "integer_polynomial_checks",
        "join_rows",
        "join_rows_per_second",
        "joined_representatives",
        "joint_mod6_supports",
        "kernel_seconds",
        "model_sha256",
        "producer_sources_sha256",
        "q_index",
        "reconstructed_reflection_mates",
        "reflection_gauge",
        "reflection_gauge_rule",
        "schema",
        "start",
        "states",
        "status",
        "stop",
        "survivor_stream_sha256",
    }
)
SHORT_RANGE_KEYS = COMMON_RANGE_KEYS | frozenset(
    {"L_gauge_states", "S_fallback_gauge_states"}
)
CASE26_RANGE_KEYS = COMMON_RANGE_KEYS

EXPECTED_INVENTORY_PATHS = {
    ".gitignore",
    "BOUNDED_BENCHMARK.json",
    "NINE_CASE_COMPLETION_CERTIFICATE.json",
    "README.md",
    "RESEARCH_LOG.md",
    "SHORT_BLOCK_CERTIFICATE.json",
    "aggregate_short_block_census.py",
    "replay_short_block_range.py",
    "run_short_block_census.py",
    "short_block_census.cpp",
    "verify_nine_case_completion.py",
    "verify_short_block_census.py",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("ascii")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise AssertionError(
            f"{label} changed: {actual!r} != {expected!r}"
        )


def require_int(value: Any, label: str, minimum: int | None = None) -> int:
    require(
        isinstance(value, int) and not isinstance(value, bool),
        f"{label} is not an integer",
    )
    if minimum is not None:
        require(value >= minimum, f"{label} is below {minimum}")
    return value


def require_hash(value: Any, label: str) -> str:
    require(
        isinstance(value, str) and HEX64.fullmatch(value) is not None,
        f"{label} is not a lowercase SHA-256",
    )
    return value


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"required JSON artifact is absent: {path}")
    payload = json.loads(path.read_text())
    require(isinstance(payload, dict), f"{path} is not a JSON object")
    return payload


def witness_score(record: dict[str, Any]) -> tuple[int, ...]:
    return (
        int(record["nonzero_lags"]),
        int(record["l1"]),
        int(record["linf"]),
        int(record["quotient_index"]),
        int(record["central_value"]),
        int(record["pair_state"]),
    )


def verify_witness(
    witness: Any,
    start: int,
    stop: int,
    label: str,
    *,
    exact: bool = False,
) -> dict[str, Any]:
    require(isinstance(witness, dict), f"{label} is not an object")
    require_equal(
        set(witness),
        {
            "quotient_index",
            "central_value",
            "pair_state",
            "normalized_residuals",
            "nonzero_lags",
            "l1",
            "linf",
        },
        f"{label} field set",
    )
    quotient = require_int(witness["quotient_index"], f"{label} quotient")
    central = require_int(witness["central_value"], f"{label} central value")
    pair_state = require_int(
        witness["pair_state"], f"{label} pair state", minimum=0
    )
    require(start <= quotient < stop, f"{label} quotient is out of range")
    require(central in (0, 1), f"{label} central value is not binary")
    require(pair_state < 1 << 39, f"{label} pair state exceeds 39 bits")

    residuals = witness["normalized_residuals"]
    require(
        isinstance(residuals, list) and len(residuals) == 20,
        f"{label} residual vector does not have length 20",
    )
    require(
        all(isinstance(value, int) and not isinstance(value, bool)
            for value in residuals),
        f"{label} residual vector is not integral",
    )
    require(
        all(value % 6 == 0 for value in residuals),
        f"{label} contains a residual not divisible by six",
    )
    nonzero = sum(value != 0 for value in residuals)
    l1 = sum(abs(value) for value in residuals)
    linf = max(map(abs, residuals))
    require_equal(
        require_int(witness["nonzero_lags"], f"{label} nonzero count", 0),
        nonzero,
        f"{label} nonzero count",
    )
    require_equal(
        require_int(witness["l1"], f"{label} L1", 0),
        l1,
        f"{label} L1",
    )
    require_equal(
        require_int(witness["linf"], f"{label} Linf", 0),
        linf,
        f"{label} Linf",
    )
    if exact:
        require_equal(nonzero, 0, f"{label} exact residual count")
    return witness


def verify_exact_candidates(
    candidates: Any, expected_count: Any, start: int, stop: int, label: str
) -> list[dict[str, Any]]:
    count = require_int(expected_count, f"{label} count", minimum=0)
    require(isinstance(candidates, list), f"{label} list is invalid")
    require_equal(len(candidates), count, f"{label} list length")
    checked = [
        verify_witness(
            candidate,
            start,
            stop,
            f"{label}[{index}]",
            exact=True,
        )
        for index, candidate in enumerate(candidates)
    ]
    require_equal(
        checked,
        sorted(
            checked,
            key=lambda record: (
                record["quotient_index"],
                record["central_value"],
                record["pair_state"],
            ),
        ),
        f"{label} ordering",
    )
    return checked


def survivor_stream_sha256(records: Iterable[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for record in records:
        digest.update(
            struct.pack(
                "<IBQ20h",
                int(record["quotient_index"]),
                int(record["central_value"]),
                int(record["pair_state"]),
                *map(int, record["normalized_residuals"]),
            )
        )
    return digest.hexdigest()


def combined_sources_sha256(paths: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.name.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def short_producer_sources_sha256() -> str:
    return combined_sources_sha256(
        (
            HERE / "short_block_census.cpp",
            CASE26_DIR / "benchmark_global_quotient.cpp",
            CASE26_DIR / "global_quotient_census.cpp",
        )
    )


def case26_producer_sources_sha256() -> str:
    return combined_sources_sha256(
        (
            CASE26_DIR / "benchmark_global_quotient.cpp",
            CASE26_DIR / "global_quotient_census.cpp",
        )
    )


def verify_inventory() -> int:
    require(
        INVENTORY_PATH.is_file(),
        "tracked artifact inventory is absent",
    )
    seen: set[str] = set()
    checked = 0
    for line_number, raw_line in enumerate(
        INVENTORY_PATH.read_text().splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        pieces = line.split(maxsplit=1)
        require(len(pieces) == 2, f"invalid inventory line {line_number}")
        expected, relative = pieces
        require_hash(expected, f"inventory line {line_number}")
        require(relative not in seen, f"duplicate inventory path {relative}")
        path = HERE / relative
        require(path.is_file(), f"inventory artifact is missing: {relative}")
        require_equal(
            sha256_file(path), expected, f"inventory hash {relative}"
        )
        seen.add(relative)
        checked += 1
    require_equal(
        seen,
        EXPECTED_INVENTORY_PATHS,
        "artifact inventory path set",
    )
    return checked


def expected_case_rows(case: int) -> int:
    return NORMAL_CASE_ROWS + (
        EXCEPTIONAL_SURCHARGE if case in EXCEPTIONAL_QUOTIENTS else 0
    )


def verify_case_certificate(
    record: Any, expected_case: int
) -> dict[str, Any]:
    require(isinstance(record, dict), f"case {expected_case} is not an object")
    require_equal(record["case"], expected_case, f"case {expected_case} id")
    require_equal(record["block"], "S", f"case {expected_case} block")
    require_equal(
        record["q_index"],
        CASE_TO_Q[expected_case],
        f"case {expected_case} q-index",
    )
    search = record["search_space"]
    result = record["result"]
    provenance = record["provenance"]
    replay = record["independent_best_quotient_replay"]

    require_equal(
        search["quotient_dimension"],
        QUOTIENT_DIMENSION,
        f"case {expected_case} quotient dimension",
    )
    require_equal(search["start"], 0, f"case {expected_case} start")
    require_equal(
        search["stop"], QUOTIENT_STATES, f"case {expected_case} stop"
    )
    require_equal(
        search["quotient_states"],
        QUOTIENT_STATES,
        f"case {expected_case} quotient states",
    )
    require_equal(
        search["chunk_size"], CHUNK_SIZE, f"case {expected_case} chunk size"
    )
    require_equal(
        search["range_count"], RANGE_COUNT, f"case {expected_case} ranges"
    )
    require_equal(
        search["central_values_per_state"],
        2,
        f"case {expected_case} central values",
    )
    require_equal(
        search["reflection_gauge"],
        True,
        f"case {expected_case} reflection gauge",
    )
    exceptions = (
        [EXCEPTIONAL_QUOTIENTS[expected_case]]
        if expected_case in EXCEPTIONAL_QUOTIENTS
        else []
    )
    require_equal(
        search["S_fallback_quotient_indices"],
        exceptions,
        f"case {expected_case} fallback quotients",
    )
    require_equal(
        search["L_gauge_states"],
        QUOTIENT_STATES - len(exceptions),
        f"case {expected_case} L-gauge states",
    )
    require_equal(
        search["S_fallback_gauge_states"],
        len(exceptions),
        f"case {expected_case} S-gauge states",
    )
    require_equal(
        search["join_rows"],
        expected_case_rows(expected_case),
        f"case {expected_case} join rows",
    )

    survivors = require_int(
        result["joint_mod6_supports"],
        f"case {expected_case} survivors",
        minimum=0,
    )
    require_equal(
        result["integer_polynomial_checks"],
        survivors,
        f"case {expected_case} integer checks",
    )
    require_equal(
        result["bitpacked_physical_replays"],
        survivors,
        f"case {expected_case} physical replays",
    )
    candidates = verify_exact_candidates(
        result["exact_candidates"],
        result["exact_integer_supports"],
        0,
        QUOTIENT_STATES,
        f"case {expected_case} exact candidates",
    )
    require_equal(candidates, [], f"case {expected_case} exact candidates")
    best = verify_witness(
        result["best_witness"],
        0,
        QUOTIENT_STATES,
        f"case {expected_case} best witness",
    )
    for key in (
        "range_stream_digest_sha256",
        "range_semantic_digest_sha256",
        "range_manifest_digest_sha256",
    ):
        require_hash(result[key], f"case {expected_case} {key}")

    require_equal(
        replay["quotient_index"],
        best["quotient_index"],
        f"case {expected_case} replay quotient",
    )
    require_equal(
        replay["states"], 1, f"case {expected_case} replay state count"
    )
    replay_survivors = require_int(
        replay["joint_mod6_supports"],
        f"case {expected_case} replay survivors",
        minimum=0,
    )
    require_equal(
        replay["integer_polynomial_checks"],
        replay_survivors,
        f"case {expected_case} replay integer checks",
    )
    require_equal(
        replay["bitpacked_physical_replays"],
        replay_survivors,
        f"case {expected_case} replay physical checks",
    )
    require_equal(
        replay["exact_integer_supports"],
        0,
        f"case {expected_case} replay exact count",
    )
    require_equal(
        replay["best_witness_match"],
        "exact",
        f"case {expected_case} replay best match",
    )
    require_hash(
        replay["survivor_stream_sha256"],
        f"case {expected_case} replay stream",
    )

    for key in (
        "run_config_sha256",
        "aggregate_sha256",
        "model_sha256",
        "binary_sha256",
        "producer_sources_sha256",
    ):
        require_hash(provenance[key], f"case {expected_case} {key}")
    require_equal(
        provenance["model_bytes"],
        247_808,
        f"case {expected_case} model size",
    )
    performance = record["performance"]
    require_int(
        performance["wall_seconds"],
        f"case {expected_case} wall seconds",
        minimum=1,
    )
    kernel_seconds = performance["sum_kernel_seconds"]
    require(
        isinstance(kernel_seconds, (int, float))
        and not isinstance(kernel_seconds, bool)
        and math.isfinite(float(kernel_seconds))
        and float(kernel_seconds) > 0,
        f"case {expected_case} kernel time is invalid",
    )
    return record


def verify_case26_base(
    certificate: dict[str, Any],
    case26_record: dict[str, Any],
) -> dict[str, Any]:
    provenance = certificate["provenance"]
    expected_hash = require_hash(
        provenance["case26_completion_certificate_sha256"],
        "case-26 completion-certificate pin",
    )
    require(
        CASE26_CERTIFICATE_PATH.is_file(),
        "pinned case-26 completion certificate is absent",
    )
    require_equal(
        sha256_file(CASE26_CERTIFICATE_PATH),
        expected_hash,
        "case-26 completion-certificate hash",
    )
    base = load_json(CASE26_CERTIFICATE_PATH)
    require_equal(
        base["schema"],
        CASE26_CERTIFICATE_SCHEMA,
        "case-26 completion-certificate schema",
    )
    require_equal(base["status"], "complete", "case-26 base status")
    search = case26_record["search_space"]
    result = case26_record["result"]
    base_search = base["search_space"]
    base_result = base["result"]
    for key in (
        "case",
        "block",
        "q_index",
        "quotient_dimension",
        "start",
        "stop",
        "quotient_states",
        "chunk_size",
        "range_count",
        "central_values_per_state",
        "reflection_gauge",
        "join_rows",
    ):
        expected = (
            case26_record[key]
            if key in ("case", "block", "q_index")
            else search[key]
        )
        require_equal(base_search[key], expected, f"case-26 base {key}")
    mapping = {
        "range_digest_sha256": "range_stream_digest_sha256",
        "joint_mod6_supports": "joint_mod6_supports",
        "integer_polynomial_checks": "integer_polynomial_checks",
        "bitpacked_physical_replays": "bitpacked_physical_replays",
        "exact_integer_supports": "exact_integer_supports",
        "exact_candidates": "exact_candidates",
        "best_witness": "best_witness",
    }
    for base_key, combined_key in mapping.items():
        require_equal(
            base_result[base_key],
            result[combined_key],
            f"case-26 base result {base_key}",
        )
    base_provenance = base["provenance"]
    for base_key, combined_key in (
        ("run_config_sha256", "run_config_sha256"),
        ("aggregate_sha256", "aggregate_sha256"),
        ("model_sha256", "model_sha256"),
        ("binary_sha256", "binary_sha256"),
        ("producer_sources_sha256", "producer_sources_sha256"),
        ("model_bytes", "model_bytes"),
    ):
        require_equal(
            base_provenance[base_key],
            case26_record["provenance"][combined_key],
            f"case-26 base provenance {base_key}",
        )
    return base


def verify_models_and_sources(
    certificate: dict[str, Any],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    provenance = certificate["provenance"]
    algebra_hash = require_hash(
        provenance["short_block_algebra_certificate_sha256"],
        "short-block algebra-certificate pin",
    )
    require(
        ALGEBRA_CERTIFICATE_PATH.is_file(),
        "pinned short-block algebra certificate is absent",
    )
    require_equal(
        sha256_file(ALGEBRA_CERTIFICATE_PATH),
        algebra_hash,
        "short-block algebra-certificate hash",
    )
    require_equal(
        sha256_file(Path(__file__).resolve()),
        provenance["completion_verifier_sha256"],
        "completion-verifier self hash",
    )
    tracked = provenance["tracked_inputs_sha256"]
    require(isinstance(tracked, dict), "tracked input pins are not a map")
    for relative, expected in tracked.items():
        require_hash(expected, f"tracked input {relative}")
        path = HERE / relative
        require(path.is_file(), f"tracked input is absent: {relative}")
        require_equal(
            sha256_file(path), expected, f"tracked input {relative}"
        )

    short_source_hash = short_producer_sources_sha256()
    case26_source_hash = case26_producer_sources_sha256()
    for record in records:
        expected = (
            case26_source_hash if record["case"] == 26 else short_source_hash
        )
        require_equal(
            record["provenance"]["producer_sources_sha256"],
            expected,
            f"case {record['case']} producer-source hash",
        )

    sys.path.insert(0, str(HERE))
    import verify_short_block_census as short_plan

    algebra = short_plan.derive_all()
    short_plan.verify_certificate(algebra)
    require_equal(
        algebra["total_join_rows"],
        TOTAL_JOIN_ROWS,
        "regenerated all-nine row total",
    )
    model_hashes: dict[int, str] = {}
    short_case26_bytes: bytes | None = None
    for record in records:
        case = int(record["case"])
        derived = short_plan.derive_case(case)
        encoded = short_plan.model_bytes(derived)
        model_hash = hashlib.sha256(encoded).hexdigest()
        require_equal(
            model_hash,
            record["provenance"]["model_sha256"],
            f"case {case} regenerated model hash",
        )
        require_equal(
            len(encoded),
            record["provenance"]["model_bytes"],
            f"case {case} regenerated model size",
        )
        model_hashes[case] = model_hash
        if case == 26:
            short_case26_bytes = encoded

    sys.path.insert(0, str(CASE26_DIR))
    import verify_global_quotient_plan as case26_plan

    base_derived = case26_plan.derive()
    base_bytes = case26_plan.model_bytes(base_derived)
    require(short_case26_bytes is not None, "short case-26 model is absent")
    require_equal(
        short_case26_bytes,
        base_bytes,
        "short/base case-26 model byte equivalence",
    )
    return {
        "short_producer_sources_sha256": short_source_hash,
        "case26_producer_sources_sha256": case26_source_hash,
        "model_sha256_by_case": model_hashes,
        "case26_models_byte_identical": True,
    }


def verify_independent_replays(
    certificate: dict[str, Any],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    sys.path.insert(0, str(HERE))
    from replay_short_block_range import reference_records, score

    best_reports: list[dict[str, Any]] = []
    for record in records:
        case = int(record["case"])
        expected = record["independent_best_quotient_replay"]
        quotient = int(expected["quotient_index"])
        replayed = reference_records(case, quotient)
        exact = [
            candidate
            for candidate in replayed
            if int(candidate["nonzero_lags"]) == 0
        ]
        best = min(replayed, key=score) if replayed else None
        require_equal(
            len(replayed),
            expected["joint_mod6_supports"],
            f"case {case} independent replay survivors",
        )
        require_equal(
            len(exact),
            expected["exact_integer_supports"],
            f"case {case} independent replay exact count",
        )
        require_equal(
            best,
            record["result"]["best_witness"],
            f"case {case} independent replay best witness",
        )
        stream_hash = survivor_stream_sha256(replayed)
        require_equal(
            stream_hash,
            expected["survivor_stream_sha256"],
            f"case {case} independent replay stream",
        )
        best_reports.append(
            {
                "case": case,
                "quotient_index": quotient,
                "survivors": len(replayed),
                "exact_integer_supports": len(exact),
                "survivor_stream_sha256": stream_hash,
                "best_witness_match": "exact",
            }
        )

    exceptional_reports: list[dict[str, Any]] = []
    exceptional = certificate["exceptional_gauge_replays"]
    require_equal(
        [entry["case"] for entry in exceptional],
        sorted(EXCEPTIONAL_QUOTIENTS),
        "exceptional replay case list",
    )
    for entry in exceptional:
        case = int(entry["case"])
        quotient = int(entry["quotient_index"])
        require_equal(
            quotient,
            EXCEPTIONAL_QUOTIENTS[case],
            f"case {case} exceptional quotient",
        )
        require_equal(
            entry["fallback_gauge"],
            "lowest odd noncentral S pair has y=0",
            f"case {case} fallback-gauge rule",
        )
        replayed = reference_records(case, quotient)
        exact = [
            candidate
            for candidate in replayed
            if int(candidate["nonzero_lags"]) == 0
        ]
        best = min(replayed, key=score) if replayed else None
        require_equal(
            len(replayed),
            entry["joint_mod6_supports"],
            f"case {case} exceptional replay survivors",
        )
        require_equal(
            len(exact),
            entry["exact_integer_supports"],
            f"case {case} exceptional replay exact count",
        )
        require_equal(
            best,
            entry["best_witness"],
            f"case {case} exceptional replay best",
        )
        stream_hash = survivor_stream_sha256(replayed)
        require_equal(
            stream_hash,
            entry["survivor_stream_sha256"],
            f"case {case} exceptional replay stream",
        )
        require_equal(
            entry["gauged_vs_ungauged_production_match"],
            True,
            f"case {case} exceptional production comparison",
        )
        exceptional_reports.append(
            {
                "case": case,
                "quotient_index": quotient,
                "survivors": len(replayed),
                "exact_integer_supports": len(exact),
                "survivor_stream_sha256": stream_hash,
            }
        )
    return {
        "global_best_quotients": best_reports,
        "exceptional_fallback_quotients": exceptional_reports,
    }


def verify_default(certificate: dict[str, Any]) -> dict[str, Any]:
    require_equal(certificate["schema"], CERTIFICATE_SCHEMA, "schema")
    require_equal(certificate["status"], "complete", "status")
    require_equal(certificate["completed_date"], "2026-07-25", "date")
    case_payloads = certificate["cases"]
    require(
        isinstance(case_payloads, list),
        "certificate cases are not a list",
    )
    require_equal(len(case_payloads), 9, "certificate case count")
    records = [
        verify_case_certificate(record, case)
        for record, case in zip(case_payloads, CASES)
    ]

    summary = certificate["summary"]
    require_equal(summary["case_numbers"], list(CASES), "summary cases")
    require_equal(summary["q_indices"], list(Q_INDICES), "summary q-indices")
    require_equal(summary["case_count"], 9, "summary case count")
    require_equal(
        summary["total_quotient_states"],
        9 * QUOTIENT_STATES,
        "summary quotient states",
    )
    require_equal(
        summary["total_range_count"],
        9 * RANGE_COUNT,
        "summary range count",
    )
    require_equal(
        summary["total_join_rows"],
        sum(record["search_space"]["join_rows"] for record in records),
        "summary join rows from cases",
    )
    require_equal(
        summary["total_join_rows"],
        TOTAL_JOIN_ROWS,
        "summary exact all-nine row total",
    )
    survivor_total = sum(
        record["result"]["joint_mod6_supports"] for record in records
    )
    require_equal(
        summary["total_joint_mod6_supports"],
        survivor_total,
        "summary survivor total",
    )
    require_equal(
        summary["total_integer_polynomial_checks"],
        survivor_total,
        "summary integer-check total",
    )
    require_equal(
        summary["total_bitpacked_physical_replays"],
        survivor_total,
        "summary physical-replay total",
    )
    require_equal(
        summary["total_exact_integer_supports"],
        0,
        "summary exact count",
    )
    require_equal(
        summary["total_exact_candidates"],
        [],
        "summary exact candidates",
    )

    case26_record = records[26 - CASES[0]]
    verify_case26_base(certificate, case26_record)
    model_report = verify_models_and_sources(certificate, records)
    replay_report = verify_independent_replays(certificate, records)
    inventory_count = verify_inventory()
    return {
        "certificate": str(CERTIFICATE_PATH),
        "inventory_artifacts_checked": inventory_count,
        "case_numbers": list(CASES),
        "q_indices": list(Q_INDICES),
        "quotient_states": summary["total_quotient_states"],
        "ranges": summary["total_range_count"],
        "join_rows": summary["total_join_rows"],
        "joint_mod6_supports": survivor_total,
        "exact_integer_supports": 0,
        "models_and_sources": model_report,
        "independent_replays": replay_report,
    }


def gauge_counts(
    case: int, start: int, states: int
) -> tuple[int, int, int]:
    exceptional = EXCEPTIONAL_QUOTIENTS.get(case)
    s_count = int(
        exceptional is not None and start <= exceptional < start + states
    )
    l_count = states - s_count
    return (
        l_count,
        s_count,
        l_count * L_GAUGE_ROWS_PER_STATE
        + s_count * S_GAUGE_ROWS_PER_STATE,
    )


def validate_live_range(
    payload: dict[str, Any],
    record: dict[str, Any],
    expected_start: int,
    expected_states: int,
) -> None:
    case = int(record["case"])
    expected_keys = CASE26_RANGE_KEYS if case == 26 else SHORT_RANGE_KEYS
    require_equal(
        set(payload),
        expected_keys,
        f"case {case} range {expected_start} field set",
    )
    provenance = record["provenance"]
    l_count, s_count, rows = gauge_counts(
        case, expected_start, expected_states
    )
    expected = {
        "schema": CASE26_RANGE_SCHEMA if case == 26 else SHORT_RANGE_SCHEMA,
        "status": "complete",
        "case": case,
        "block": "S",
        "q_index": record["q_index"],
        "start": expected_start,
        "states": expected_states,
        "stop": expected_start + expected_states,
        "central_values_per_state": 2,
        "reflection_gauge": True,
        "join_rows": rows,
        "producer_sources_sha256": provenance["producer_sources_sha256"],
        "model_sha256": provenance["model_sha256"],
    }
    if case != 26:
        expected.update(
            {
                "L_gauge_states": l_count,
                "S_fallback_gauge_states": s_count,
                "reflection_gauge_rule":
                    "lowest odd noncentral L pair, else S pair, has y=0",
            }
        )
    else:
        expected["reflection_gauge_rule"] = (
            "lowest-index odd noncentral L pair has y=0"
        )
    for key, value in expected.items():
        require_equal(
            payload[key],
            value,
            f"case {case} range {expected_start} field {key}",
        )
    survivors = require_int(
        payload["joint_mod6_supports"],
        f"case {case} range {expected_start} survivors",
        minimum=0,
    )
    for key in ("integer_polynomial_checks", "bitpacked_physical_replays"):
        require_equal(
            payload[key],
            survivors,
            f"case {case} range {expected_start} {key}",
        )
    representatives = require_int(
        payload["joined_representatives"],
        f"case {case} range {expected_start} representatives",
        minimum=0,
    )
    require_equal(
        2 * representatives,
        survivors,
        f"case {case} range {expected_start} reconstructed count",
    )
    require_equal(
        payload["reconstructed_reflection_mates"],
        representatives,
        f"case {case} range {expected_start} reflected mates",
    )
    require_hash(
        payload["survivor_stream_sha256"],
        f"case {case} range {expected_start} survivor stream",
    )
    candidates = verify_exact_candidates(
        payload["exact_candidates"],
        payload["exact_integer_supports"],
        expected_start,
        expected_start + expected_states,
        f"case {case} range {expected_start} exact candidates",
    )
    best = payload["best_witness"]
    if survivors:
        verify_witness(
            best,
            expected_start,
            expected_start + expected_states,
            f"case {case} range {expected_start} best witness",
        )
        if candidates:
            require_equal(
                witness_score(best),
                min(map(witness_score, candidates)),
                f"case {case} range {expected_start} exact best score",
            )
    else:
        require_equal(
            best,
            None,
            f"case {case} range {expected_start} empty best witness",
        )
    for key in PERFORMANCE_RANGE_KEYS:
        value = payload[key]
        require(
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(float(value))
            and float(value) > 0,
            f"case {case} range {expected_start} invalid {key}",
        )


def update_named_payload_digest(
    digest: Any, name: str, content: bytes
) -> None:
    encoded_name = name.encode("ascii")
    digest.update(len(encoded_name).to_bytes(2, "little"))
    digest.update(encoded_name)
    digest.update(len(content).to_bytes(8, "little"))
    digest.update(content)


def live_paths(
    case: int, short_output: Path, case26_output: Path
) -> tuple[Path, Path, Path]:
    if case == 26:
        root = case26_output
        return (
            root,
            root / "case26-model.bin",
            root / "global_quotient_census",
        )
    root = short_output / f"production-case{case}"
    return (
        root,
        root / f"case{case}-model.bin",
        root / "short_block_census",
    )


def verify_live_case(
    record: dict[str, Any], short_output: Path, case26_output: Path
) -> dict[str, Any]:
    case = int(record["case"])
    root, model_path, binary_path = live_paths(
        case, short_output, case26_output
    )
    config_path = root / "RUN_CONFIG.json"
    aggregate_path = root / "AGGREGATE.json"
    for path in (
        config_path,
        aggregate_path,
        model_path,
        binary_path,
        root / "ranges",
    ):
        require(path.exists(), f"case {case} live artifact is absent: {path}")
    provenance = record["provenance"]
    for path, key, label in (
        (config_path, "run_config_sha256", "run config"),
        (aggregate_path, "aggregate_sha256", "aggregate"),
        (model_path, "model_sha256", "model"),
        (binary_path, "binary_sha256", "binary"),
    ):
        require_equal(
            sha256_file(path),
            provenance[key],
            f"case {case} live {label} hash",
        )
    require_equal(
        model_path.stat().st_size,
        provenance["model_bytes"],
        f"case {case} live model size",
    )

    search = record["search_space"]
    config = load_json(config_path)
    config_expected = {
        "schema": (
            CASE26_CONFIG_SCHEMA if case == 26 else SHORT_CONFIG_SCHEMA
        ),
        "case": case,
        "block": "S",
        "q_index": record["q_index"],
        "quotient_dimension": QUOTIENT_DIMENSION,
        "start": 0,
        "stop": QUOTIENT_STATES,
        "chunk_size": CHUNK_SIZE,
        "range_count": RANGE_COUNT,
        "reflection_gauge": True,
        "producer_sources_sha256": provenance["producer_sources_sha256"],
        "model_sha256": provenance["model_sha256"],
        "model_bytes": provenance["model_bytes"],
        "binary_sha256": provenance["binary_sha256"],
    }
    if case != 26:
        config_expected.update(
            {
                "S_fallback_quotient_indices":
                    search["S_fallback_quotient_indices"],
                "expected_full_join_rows": search["join_rows"],
                "gauge_policy":
                    "lowest odd noncentral L pair, else S pair",
            }
        )
    for key, value in config_expected.items():
        require_equal(
            config.get(key), value, f"case {case} config field {key}"
        )

    range_root = root / "ranges"
    expected_ranges = [
        (
            start,
            range_root
            / f"range_{start:06d}_{start + CHUNK_SIZE:06d}.json",
        )
        for start in range(0, QUOTIENT_STATES, CHUNK_SIZE)
    ]
    expected_paths = {path for _start, path in expected_ranges}
    actual_paths = set(range_root.glob("range_*.json"))
    require_equal(
        actual_paths, expected_paths, f"case {case} exact live range path set"
    )

    stream_digest = hashlib.sha256()
    semantic_digest = hashlib.sha256()
    manifest_digest = hashlib.sha256()
    totals = {
        "L_gauge_states": 0,
        "S_fallback_gauge_states": 0,
        "join_rows": 0,
        "joint_mod6_supports": 0,
        "integer_polynomial_checks": 0,
        "bitpacked_physical_replays": 0,
        "exact_integer_supports": 0,
        "joined_representatives": 0,
    }
    exact_candidates: list[dict[str, Any]] = []
    best: dict[str, Any] | None = None
    for expected_start, path in expected_ranges:
        raw = path.read_bytes()
        payload = json.loads(raw)
        require(
            isinstance(payload, dict),
            f"case {case} range {expected_start} is not an object",
        )
        validate_live_range(payload, record, expected_start, CHUNK_SIZE)
        l_count, s_count, _rows = gauge_counts(
            case, expected_start, CHUNK_SIZE
        )
        totals["L_gauge_states"] += l_count
        totals["S_fallback_gauge_states"] += s_count
        for key in (
            "join_rows",
            "joint_mod6_supports",
            "integer_polynomial_checks",
            "bitpacked_physical_replays",
            "exact_integer_supports",
            "joined_representatives",
        ):
            totals[key] += int(payload[key])
        exact_candidates.extend(payload["exact_candidates"])
        candidate = payload["best_witness"]
        if candidate is not None and (
            best is None or witness_score(candidate) < witness_score(best)
        ):
            best = candidate

        stream_digest.update(expected_start.to_bytes(4, "little"))
        stream_digest.update(CHUNK_SIZE.to_bytes(4, "little"))
        stream_digest.update(
            bytes.fromhex(payload["survivor_stream_sha256"])
        )
        semantic = {
            key: value
            for key, value in payload.items()
            if key not in PERFORMANCE_RANGE_KEYS
        }
        update_named_payload_digest(
            semantic_digest, path.name, canonical_bytes(semantic)
        )
        update_named_payload_digest(manifest_digest, path.name, raw)

    result = record["result"]
    require_equal(
        totals["L_gauge_states"],
        search["L_gauge_states"],
        f"case {case} live L-gauge total",
    )
    require_equal(
        totals["S_fallback_gauge_states"],
        search["S_fallback_gauge_states"],
        f"case {case} live S-gauge total",
    )
    require_equal(
        totals["join_rows"],
        search["join_rows"],
        f"case {case} live row total",
    )
    for key in (
        "joint_mod6_supports",
        "integer_polynomial_checks",
        "bitpacked_physical_replays",
        "exact_integer_supports",
    ):
        require_equal(
            totals[key], result[key], f"case {case} live {key}"
        )
    require_equal(
        exact_candidates,
        result["exact_candidates"],
        f"case {case} live retained exact candidates",
    )
    require_equal(
        best,
        result["best_witness"],
        f"case {case} live retained best witness",
    )
    require_equal(
        2 * totals["joined_representatives"],
        totals["joint_mod6_supports"],
        f"case {case} live gauge-orbit reconstruction",
    )
    require_equal(
        stream_digest.hexdigest(),
        result["range_stream_digest_sha256"],
        f"case {case} live stream range digest",
    )
    require_equal(
        semantic_digest.hexdigest(),
        result["range_semantic_digest_sha256"],
        f"case {case} live semantic range digest",
    )
    require_equal(
        manifest_digest.hexdigest(),
        result["range_manifest_digest_sha256"],
        f"case {case} live full-manifest range digest",
    )

    aggregate = load_json(aggregate_path)
    aggregate_expected = {
        "schema": (
            CASE26_AGGREGATE_SCHEMA
            if case == 26
            else SHORT_AGGREGATE_SCHEMA
        ),
        "status": "complete",
        "case": case,
        "block": "S",
        "q_index": record["q_index"],
        "start": 0,
        "stop": QUOTIENT_STATES,
        "quotient_states": QUOTIENT_STATES,
        "range_count": RANGE_COUNT,
        "central_values_per_state": 2,
        "reflection_gauge": True,
        "join_rows": search["join_rows"],
        "joint_mod6_supports": result["joint_mod6_supports"],
        "integer_polynomial_checks": result["integer_polynomial_checks"],
        "bitpacked_physical_replays": result[
            "bitpacked_physical_replays"
        ],
        "exact_integer_supports": result["exact_integer_supports"],
        "exact_candidates": result["exact_candidates"],
        "best_witness": result["best_witness"],
        "range_digest_sha256": result["range_stream_digest_sha256"],
        "producer_sources_sha256": provenance["producer_sources_sha256"],
        "model_sha256": provenance["model_sha256"],
        "binary_sha256": provenance["binary_sha256"],
    }
    if case != 26:
        aggregate_expected.update(
            {
                "L_gauge_states": search["L_gauge_states"],
                "S_fallback_gauge_states":
                    search["S_fallback_gauge_states"],
            }
        )
    for key, value in aggregate_expected.items():
        require_equal(
            aggregate.get(key),
            value,
            f"case {case} aggregate field {key}",
        )
    return {
        "case": case,
        "live_root": str(root),
        "ranges_checked": RANGE_COUNT,
        "join_rows": totals["join_rows"],
        "joint_mod6_supports": totals["joint_mod6_supports"],
        "exact_integer_supports": totals["exact_integer_supports"],
        "range_semantic_digest_sha256": semantic_digest.hexdigest(),
        "range_manifest_digest_sha256": manifest_digest.hexdigest(),
    }


def run_exceptional_modes(
    certificate: dict[str, Any],
    records: list[dict[str, Any]],
    short_output: Path,
    case26_output: Path,
) -> list[dict[str, Any]]:
    by_case = {int(record["case"]): record for record in records}
    reports: list[dict[str, Any]] = []
    compare_keys = (
        "joint_mod6_supports",
        "integer_polynomial_checks",
        "bitpacked_physical_replays",
        "exact_integer_supports",
        "exact_candidates",
        "best_witness",
        "survivor_stream_sha256",
    )
    entries = {
        int(entry["case"]): entry
        for entry in certificate["exceptional_gauge_replays"]
    }
    for case, quotient in EXCEPTIONAL_QUOTIENTS.items():
        record = by_case[case]
        expected = entries[case]
        root, model_path, binary_path = live_paths(
            case, short_output, case26_output
        )
        config = load_json(root / "RUN_CONFIG.json")
        outputs: dict[str, dict[str, Any]] = {}
        for mode in ("gauged", "ungauged"):
            command = [
                str(binary_path),
                str(model_path),
                "--case",
                str(case),
                "--q-index",
                str(record["q_index"]),
                "--start",
                str(quotient),
                "--states",
                "1",
                "--source-sha",
                str(config["producer_sources_sha256"]),
                "--model-sha",
                str(config["model_sha256"]),
                "--mode",
                mode,
            ]
            completed = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(completed.stdout)
            require(
                isinstance(payload, dict),
                f"case {case} {mode} exceptional replay is invalid",
            )
            outputs[mode] = {
                key: payload[key] for key in compare_keys
            }
        require_equal(
            outputs["gauged"],
            outputs["ungauged"],
            f"case {case} gauged/ungauged exceptional replay",
        )
        expected_payload = {
            "joint_mod6_supports": expected["joint_mod6_supports"],
            "integer_polynomial_checks": expected[
                "joint_mod6_supports"
            ],
            "bitpacked_physical_replays": expected[
                "joint_mod6_supports"
            ],
            "exact_integer_supports": expected[
                "exact_integer_supports"
            ],
            "exact_candidates": [],
            "best_witness": expected["best_witness"],
            "survivor_stream_sha256": expected[
                "survivor_stream_sha256"
            ],
        }
        require_equal(
            outputs["gauged"],
            expected_payload,
            f"case {case} exceptional production/reference replay",
        )
        reports.append(
            {
                "case": case,
                "quotient_index": quotient,
                "gauged_vs_ungauged": "exact match",
                "reference_replay": "exact match",
                "survivor_stream_sha256":
                    expected["survivor_stream_sha256"],
            }
        )
    return reports


def verify_live(
    certificate: dict[str, Any],
    short_output: Path,
    case26_output: Path,
) -> dict[str, Any]:
    records = certificate["cases"]
    case_reports = [
        verify_live_case(record, short_output, case26_output)
        for record in records
    ]
    require_equal(
        sum(report["join_rows"] for report in case_reports),
        TOTAL_JOIN_ROWS,
        "live all-nine row total",
    )
    require_equal(
        sum(report["joint_mod6_supports"] for report in case_reports),
        certificate["summary"]["total_joint_mod6_supports"],
        "live all-nine survivor total",
    )
    require_equal(
        sum(report["exact_integer_supports"] for report in case_reports),
        0,
        "live all-nine exact count",
    )
    exceptional_reports = run_exceptional_modes(
        certificate, records, short_output, case26_output
    )
    return {
        "cases": case_reports,
        "case_count": len(case_reports),
        "ranges_checked": 9 * RANGE_COUNT,
        "join_rows": TOTAL_JOIN_ROWS,
        "joint_mod6_supports":
            certificate["summary"]["total_joint_mod6_supports"],
        "exact_integer_supports": 0,
        "exceptional_gauge_replays": exceptional_reports,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live",
        action="store_true",
        help=(
            "strictly validate all ignored production outputs and rerun "
            "both exceptional quotients in gauged and ungauged modes"
        ),
    )
    parser.add_argument(
        "--short-output",
        type=Path,
        default=DEFAULT_SHORT_OUTPUT,
        help="parent of production-case21, ..., production-case29",
    )
    parser.add_argument(
        "--case26-output",
        type=Path,
        default=DEFAULT_CASE26_OUTPUT,
        help="case-26 production output directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    certificate = load_json(CERTIFICATE_PATH)
    report = {
        "schema": "h668-eliahou-short-block-nine-case-verification-v1",
        "status": "PASS",
        "default": verify_default(certificate),
        "live": (
            verify_live(
                certificate,
                args.short_output.resolve(),
                args.case26_output.resolve(),
            )
            if args.live
            else None
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
