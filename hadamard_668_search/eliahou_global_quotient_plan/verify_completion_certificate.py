#!/usr/bin/env python3
"""Verify the tracked case-26 completion certificate.

The default path is independent of ignored production output.  It checks the
certificate arithmetic, hashes the pinned tracked sources, and regenerates
the compact binary model from the mathematical derivation.  ``--live`` adds a
strict audit of RUN_CONFIG.json, AGGREGATE.json, all 256 range manifests, the
binary, and the binary model in an ignored production directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
CERTIFICATE_PATH = HERE / "COMPLETION_CERTIFICATE.json"
INVENTORY_PATH = HERE / "ARTIFACT_SHA256.txt"
DEFAULT_LIVE_ROOT = HERE / "output" / "production"
CERTIFICATE_SCHEMA = "h668-case26-global-quotient-completion-certificate-v1"
CONFIG_SCHEMA = "h668-case26-global-quotient-production-v1"
AGGREGATE_SCHEMA = "h668-case26-global-quotient-aggregate-v1"
RANGE_SCHEMA = "h668-case26-global-quotient-range-v1"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise AssertionError(
            f"{label} changed: {actual!r} != {expected!r}"
        )


def require_hash(value: Any, label: str) -> str:
    require(
        isinstance(value, str) and HEX64.fullmatch(value) is not None,
        f"{label} is not a lowercase SHA-256",
    )
    return value


def load_json(path: Path) -> dict[str, Any]:
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
    witness: dict[str, Any], start: int, stop: int
) -> None:
    residuals = witness.get("normalized_residuals")
    require(
        isinstance(residuals, list)
        and len(residuals) == 20
        and all(isinstance(value, int) for value in residuals),
        "best witness residual vector changed",
    )
    require_equal(
        sum(value != 0 for value in residuals),
        witness.get("nonzero_lags"),
        "best witness nonzero-lag count",
    )
    require_equal(
        sum(abs(value) for value in residuals),
        witness.get("l1"),
        "best witness L1 norm",
    )
    require_equal(
        max(map(abs, residuals)),
        witness.get("linf"),
        "best witness Linf norm",
    )
    require(
        start <= int(witness["quotient_index"]) < stop,
        "best witness quotient lies outside the census",
    )
    require(
        int(witness["central_value"]) in (0, 1),
        "best witness central value is not binary",
    )
    require(int(witness["pair_state"]) >= 0, "negative pair state")


def producer_sources_sha256() -> str:
    digest = hashlib.sha256()
    for path in (
        HERE / "benchmark_global_quotient.cpp",
        HERE / "global_quotient_census.cpp",
    ):
        digest.update(path.name.encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def verify_inventory(required_paths: set[str]) -> int:
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
        require_equal(sha256_file(path), expected, f"inventory hash {relative}")
        seen.add(relative)
        checked += 1
    missing = required_paths - seen
    require(not missing, f"inventory omits required artifacts: {sorted(missing)}")
    return checked


def verify_default(certificate: dict[str, Any]) -> dict[str, Any]:
    require_equal(certificate.get("schema"), CERTIFICATE_SCHEMA, "schema")
    require_equal(certificate.get("status"), "complete", "status")
    search = certificate["search_space"]
    result = certificate["result"]
    replay = certificate["independent_best_quotient_replay"]
    provenance = certificate["provenance"]

    require_equal(search["case"], 26, "case")
    require_equal(search["block"], "S", "block")
    require_equal(search["q_index"], 12, "q-index")
    dimension = int(search["quotient_dimension"])
    start = int(search["start"])
    stop = int(search["stop"])
    states = stop - start
    require_equal(dimension, 18, "quotient dimension")
    require_equal(start, 0, "census start")
    require_equal(stop, 1 << dimension, "census stop")
    require_equal(search["quotient_states"], states, "quotient-state count")
    chunk_size = int(search["chunk_size"])
    require_equal(states % chunk_size, 0, "range divisibility")
    require_equal(
        search["range_count"], states // chunk_size, "range count"
    )
    require_equal(
        search["central_values_per_state"], 2, "central-value count"
    )
    require_equal(search["reflection_gauge"], True, "reflection gauge")
    right_rows = 1 << 18
    left_rows = 1 << 19
    require_equal(
        search["right_rows_per_state_and_central"],
        right_rows,
        "right rows",
    )
    require_equal(
        search["left_rows_per_state_and_central"],
        left_rows,
        "left rows",
    )
    join_rows = states * (right_rows + left_rows) * 2
    require_equal(search["join_rows"], join_rows, "join-row count")

    survivors = int(result["joint_mod6_supports"])
    require(survivors >= 0, "negative survivor count")
    require_equal(
        result["integer_polynomial_checks"],
        survivors,
        "integer replay count",
    )
    require_equal(
        result["bitpacked_physical_replays"],
        survivors,
        "physical replay count",
    )
    require_equal(result["exact_integer_supports"], 0, "exact count")
    require_equal(result["exact_candidates"], [], "exact candidates")
    require_hash(result["range_digest_sha256"], "range digest")
    best = result["best_witness"]
    verify_witness(best, start, stop)

    require_equal(
        replay["quotient_index"],
        best["quotient_index"],
        "independent replay quotient",
    )
    require_equal(replay["states"], 1, "independent replay state count")
    replay_survivors = int(replay["joint_mod6_supports"])
    require_equal(replay_survivors, 46, "independent replay survivors")
    require_equal(
        replay["integer_polynomial_checks"],
        replay_survivors,
        "independent integer replay count",
    )
    require_equal(
        replay["bitpacked_physical_replays"],
        replay_survivors,
        "independent physical replay count",
    )
    require_equal(
        replay["exact_integer_supports"], 0, "independent exact count"
    )
    require_equal(
        replay["best_witness_match"], "exact", "independent best match"
    )

    for key in (
        "run_config_sha256",
        "aggregate_sha256",
        "producer_sources_sha256",
        "model_sha256",
        "binary_sha256",
        "completion_verifier_sha256",
    ):
        require_hash(provenance[key], key)
    require_equal(
        sha256_file(Path(__file__).resolve()),
        provenance["completion_verifier_sha256"],
        "completion verifier hash",
    )
    pinned_inputs = provenance["tracked_inputs_sha256"]
    require(isinstance(pinned_inputs, dict), "tracked input pins are not a map")
    for relative, expected in pinned_inputs.items():
        require_hash(expected, f"tracked input {relative}")
        require_equal(
            sha256_file(HERE / relative),
            expected,
            f"tracked input hash {relative}",
        )
    require_equal(
        producer_sources_sha256(),
        provenance["producer_sources_sha256"],
        "combined producer-source hash",
    )

    # Regenerate the binary model from the mathematical source tree.  This
    # repeats the 2^18-state quotient arithmetic but performs no search.
    sys.path.insert(0, str(HERE))
    import verify_global_quotient_plan as plan

    derived = plan.derive()
    model = plan.model_bytes(derived)
    require_equal(derived["case"], 26, "derived case")
    require_equal(derived["block"], "S", "derived block")
    require_equal(derived["q_index"], 12, "derived q-index")
    require_equal(
        derived["quotient_dimension"], dimension, "derived quotient dimension"
    )
    require_equal(
        derived["quotient_states"], states, "derived quotient-state count"
    )
    require_equal(len(model), provenance["model_bytes"], "derived model size")
    require_equal(
        hashlib.sha256(model).hexdigest(),
        provenance["model_sha256"],
        "derived model hash",
    )

    required_inventory_paths = set(pinned_inputs) | {
        "COMPLETION_CERTIFICATE.json",
        "verify_completion_certificate.py",
        "README.md",
        "RESEARCH_LOG.md",
    }
    inventory_count = verify_inventory(required_inventory_paths)
    return {
        "certificate": str(CERTIFICATE_PATH),
        "inventory_artifacts_checked": inventory_count,
        "derived_model_sha256": provenance["model_sha256"],
        "quotient_states": states,
        "join_rows": join_rows,
        "certified_survivors": survivors,
        "exact_integer_supports": 0,
    }


def validate_live_range(
    payload: dict[str, Any],
    start: int,
    states: int,
    certificate: dict[str, Any],
) -> None:
    search = certificate["search_space"]
    provenance = certificate["provenance"]
    expected = {
        "schema": RANGE_SCHEMA,
        "status": "complete",
        "case": 26,
        "block": "S",
        "q_index": 12,
        "start": start,
        "states": states,
        "stop": start + states,
        "central_values_per_state": 2,
        "reflection_gauge": True,
        "join_rows": states
        * (
            int(search["right_rows_per_state_and_central"])
            + int(search["left_rows_per_state_and_central"])
        )
        * 2,
        "producer_sources_sha256": provenance["producer_sources_sha256"],
        "model_sha256": provenance["model_sha256"],
    }
    for key, value in expected.items():
        require_equal(payload.get(key), value, f"range {start} field {key}")
    survivors = payload.get("joint_mod6_supports")
    require(
        isinstance(survivors, int) and survivors >= 0,
        f"range {start} survivor count is invalid",
    )
    for key in ("integer_polynomial_checks", "bitpacked_physical_replays"):
        require_equal(
            payload.get(key), survivors, f"range {start} field {key}"
        )
    representatives = payload.get("joined_representatives")
    require(
        isinstance(representatives, int) and representatives >= 0,
        f"range {start} representative count is invalid",
    )
    require_equal(
        representatives * 2,
        survivors,
        f"range {start} reconstructed survivor count",
    )
    require_equal(
        payload.get("reconstructed_reflection_mates"),
        representatives,
        f"range {start} reflection mates",
    )
    exact = payload.get("exact_integer_supports")
    candidates = payload.get("exact_candidates")
    require(
        isinstance(exact, int)
        and exact >= 0
        and isinstance(candidates, list)
        and len(candidates) == exact,
        f"range {start} exact-candidate list is invalid",
    )
    require_hash(
        payload.get("survivor_stream_sha256"),
        f"range {start} survivor-stream hash",
    )
    witness = payload.get("best_witness")
    if witness is not None:
        require(
            isinstance(witness, dict), f"range {start} best witness is invalid"
        )
        verify_witness(witness, start, start + states)


def verify_live(
    certificate: dict[str, Any], root: Path
) -> dict[str, Any]:
    root = root.resolve()
    config_path = root / "RUN_CONFIG.json"
    aggregate_path = root / "AGGREGATE.json"
    model_path = root / "case26-model.bin"
    binary_path = root / "global_quotient_census"
    for path in (config_path, aggregate_path, model_path, binary_path):
        require(path.is_file(), f"live artifact is missing: {path}")

    search = certificate["search_space"]
    result = certificate["result"]
    provenance = certificate["provenance"]
    require_equal(
        sha256_file(config_path),
        provenance["run_config_sha256"],
        "live run-config hash",
    )
    require_equal(
        sha256_file(aggregate_path),
        provenance["aggregate_sha256"],
        "live aggregate hash",
    )
    require_equal(
        sha256_file(model_path),
        provenance["model_sha256"],
        "live binary-model hash",
    )
    require_equal(
        model_path.stat().st_size,
        provenance["model_bytes"],
        "live binary-model size",
    )
    require_equal(
        sha256_file(binary_path),
        provenance["binary_sha256"],
        "live executable hash",
    )

    config = load_json(config_path)
    expected_config = {
        "schema": CONFIG_SCHEMA,
        "case": 26,
        "block": "S",
        "q_index": 12,
        "quotient_dimension": 18,
        "start": search["start"],
        "stop": search["stop"],
        "chunk_size": search["chunk_size"],
        "range_count": search["range_count"],
        "reflection_gauge": True,
        "producer_sources_sha256": provenance["producer_sources_sha256"],
        "model_sha256": provenance["model_sha256"],
        "model_bytes": provenance["model_bytes"],
        "binary_sha256": provenance["binary_sha256"],
        "core_source_sha256": provenance["tracked_inputs_sha256"][
            "benchmark_global_quotient.cpp"
        ],
        "production_source_sha256": provenance["tracked_inputs_sha256"][
            "global_quotient_census.cpp"
        ],
        "model_generator_sha256": provenance["tracked_inputs_sha256"][
            "verify_global_quotient_plan.py"
        ],
        "runner_sha256": provenance["tracked_inputs_sha256"][
            "run_global_quotient_census.py"
        ],
    }
    for key, value in expected_config.items():
        require_equal(config.get(key), value, f"run-config field {key}")

    range_root = root / "ranges"
    starts = range(
        int(search["start"]),
        int(search["stop"]),
        int(search["chunk_size"]),
    )
    expected_ranges = [
        (
            start,
            range_root
            / f"range_{start:06d}_{start + int(search['chunk_size']):06d}.json",
        )
        for start in starts
    ]
    expected_paths = {path for _start, path in expected_ranges}
    actual_paths = set(range_root.glob("range_*.json"))
    require_equal(actual_paths, expected_paths, "live range-manifest set")

    digest = hashlib.sha256()
    total_join_rows = 0
    total_survivors = 0
    total_integer_checks = 0
    total_physical_replays = 0
    total_exact = 0
    total_representatives = 0
    exact_candidates: list[dict[str, Any]] = []
    best: dict[str, Any] | None = None
    chunk_size = int(search["chunk_size"])
    for expected_start, path in expected_ranges:
        payload = load_json(path)
        validate_live_range(
            payload, expected_start, chunk_size, certificate
        )
        total_join_rows += int(payload["join_rows"])
        total_survivors += int(payload["joint_mod6_supports"])
        total_integer_checks += int(payload["integer_polynomial_checks"])
        total_physical_replays += int(payload["bitpacked_physical_replays"])
        total_exact += int(payload["exact_integer_supports"])
        total_representatives += int(payload["joined_representatives"])
        exact_candidates.extend(payload["exact_candidates"])
        candidate = payload.get("best_witness")
        if candidate is not None and (
            best is None or witness_score(candidate) < witness_score(best)
        ):
            best = candidate
        digest.update(expected_start.to_bytes(4, "little"))
        digest.update(chunk_size.to_bytes(4, "little"))
        digest.update(bytes.fromhex(payload["survivor_stream_sha256"]))

    require_equal(total_join_rows, search["join_rows"], "live join-row total")
    require_equal(
        total_survivors,
        result["joint_mod6_supports"],
        "live survivor total",
    )
    require_equal(
        total_integer_checks,
        result["integer_polynomial_checks"],
        "live integer-check total",
    )
    require_equal(
        total_physical_replays,
        result["bitpacked_physical_replays"],
        "live physical-replay total",
    )
    require_equal(total_exact, result["exact_integer_supports"], "live exact total")
    require_equal(exact_candidates, result["exact_candidates"], "live candidates")
    require_equal(best, result["best_witness"], "live best witness")
    require_equal(
        digest.hexdigest(),
        result["range_digest_sha256"],
        "live range digest",
    )
    require_equal(
        total_representatives * 2,
        total_survivors,
        "live gauge-orbit reconstruction",
    )

    aggregate = load_json(aggregate_path)
    expected_aggregate = {
        "schema": AGGREGATE_SCHEMA,
        "status": "complete",
        "case": 26,
        "block": "S",
        "q_index": 12,
        "start": search["start"],
        "stop": search["stop"],
        "quotient_states": search["quotient_states"],
        "range_count": search["range_count"],
        "central_values_per_state": 2,
        "reflection_gauge": True,
        "join_rows": result.get("join_rows", search["join_rows"]),
        "joint_mod6_supports": result["joint_mod6_supports"],
        "integer_polynomial_checks": result["integer_polynomial_checks"],
        "bitpacked_physical_replays": result["bitpacked_physical_replays"],
        "exact_integer_supports": result["exact_integer_supports"],
        "exact_candidates": result["exact_candidates"],
        "best_witness": result["best_witness"],
        "range_digest_sha256": result["range_digest_sha256"],
        "producer_sources_sha256": provenance["producer_sources_sha256"],
        "model_sha256": provenance["model_sha256"],
        "binary_sha256": provenance["binary_sha256"],
    }
    for key, value in expected_aggregate.items():
        require_equal(aggregate.get(key), value, f"aggregate field {key}")

    return {
        "live_root": str(root),
        "run_config_sha256": provenance["run_config_sha256"],
        "aggregate_sha256": provenance["aggregate_sha256"],
        "ranges_checked": len(expected_paths),
        "range_digest_sha256": digest.hexdigest(),
        "manifest_survivors": total_survivors,
        "exact_integer_supports": total_exact,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live",
        action="store_true",
        help="strictly validate the ignored production config, aggregate, and ranges",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_LIVE_ROOT,
        help="production output root used with --live",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    certificate = load_json(CERTIFICATE_PATH)
    report = {
        "schema": "h668-case26-global-quotient-completion-verification-v1",
        "status": "PASS",
        "default": verify_default(certificate),
        "live": verify_live(certificate, args.output) if args.live else None,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
