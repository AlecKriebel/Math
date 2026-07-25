#!/usr/bin/env python3
"""Detached replay of the long-block triage and its bounded certificates."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import subprocess
import tempfile
import time

import benchmark_exact_crt_sat as sat_benchmark
import run_mod4_walsh_census as walsh_runner
import verify_long_block_exact_triage as triage


HERE = Path(__file__).resolve().parent


def without_timing(payload: dict[str, object]) -> dict[str, object]:
    result = json.loads(json.dumps(payload))
    result.pop("verification_seconds", None)
    return result


def verify_triage() -> dict[str, object]:
    expected = json.loads(triage.CERTIFICATE.read_text())
    actual = triage.derive(run_pilots=True)
    if without_timing(actual) != without_timing(expected):
        raise AssertionError("the exact triage certificate changed")
    return {
        "semantic_sha256": actual["semantic_sha256"],
        "cases": len(actual["cases"]),
    }


def normalized_walsh(payload: dict[str, object]) -> dict[str, object]:
    result = json.loads(json.dumps(payload))
    result.pop("seconds", None)
    result.pop("combinations_per_second", None)
    return result


def verify_walsh() -> dict[str, object]:
    expected = json.loads(walsh_runner.CERTIFICATE.read_text())
    semantic = json.loads(json.dumps(expected))
    claimed_hash = semantic.pop("semantic_sha256")
    for result in semantic["results"]:
        result["walsh"].pop("seconds", None)
        result["walsh"].pop("combinations_per_second", None)
    if triage.compact_hash(semantic) != claimed_hash:
        raise AssertionError("the Walsh semantic hash failed")
    if not expected["complete_pencil"] or expected["cases"] != list(
        triage.CASES
    ):
        raise AssertionError("the Walsh certificate is not all-open-case")

    with tempfile.TemporaryDirectory(
        prefix="h668_mod4_walsh_verify_"
    ) as temporary:
        temporary_path = Path(temporary)
        engine = temporary_path / "mod4_walsh"
        walsh_runner.compile_engine(engine)
        for expected_case in expected["results"]:
            case_number = int(expected_case["case"])
            model = temporary_path / f"case_{case_number}.bin"
            metadata = walsh_runner.write_model(model, case_number)
            if (
                metadata["anf_sha256"] != expected_case["anf_sha256"]
                or metadata["binary_model_sha256"]
                != expected_case["binary_model_sha256"]
                or metadata["binary_model_bytes"]
                != expected_case["binary_model_bytes"]
            ):
                raise AssertionError("a Walsh model payload changed")
            completed = subprocess.run(
                [
                    str(engine),
                    str(model),
                    "0",
                    str(1 << 20),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            actual = json.loads(completed.stdout)
            common_zeros = int(actual["common_zeros"])
            actual["effective_bits_removed"] = (
                57 - math.log2(common_zeros)
            )
            if normalized_walsh(actual) != normalized_walsh(
                expected_case["walsh"]
            ):
                raise AssertionError(
                    f"case {case_number} Walsh census changed"
                )
    return {
        "semantic_sha256": claimed_hash,
        "cases": len(expected["results"]),
        "complete_combinations_per_case": 1 << 20,
    }


def normalized_sat_record(
    payload: dict[str, object],
) -> dict[str, object]:
    result = json.loads(json.dumps(payload))
    result.pop("build_seconds", None)
    result.pop("solve_seconds", None)
    return result


def verify_sat(rerun_solver: bool) -> dict[str, object]:
    expected = json.loads(sat_benchmark.CERTIFICATE.read_text())
    semantic = json.loads(json.dumps(expected))
    claimed_hash = semantic.pop("semantic_sha256")
    for result in semantic["results"]:
        result.pop("build_seconds", None)
        result.pop("solve_seconds", None)
    calculated_hash = sat_benchmark.hashlib.sha256(
        json.dumps(
            semantic, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()
    if calculated_hash != claimed_hash:
        raise AssertionError("the SAT benchmark semantic hash failed")

    by_encoding = dict(sat_benchmark.ENCODINGS)
    for record in expected["results"]:
        case_number = int(record["case"])
        encoding = str(record["encoding"])
        moduli = by_encoding[encoding]
        case = sat_benchmark.char3.canonical_cases()[case_number]
        if moduli is None:
            cnf, _, _ = sat_benchmark.exact.build(
                case, None, modulus=42, add_mod4=False
            )
        else:
            cnf, _, _, _ = sat_benchmark.char3.build(case, moduli)
        if (
            cnf.nv != record["variables"]
            or len(cnf.clauses) != record["clauses"]
            or sat_benchmark.cnf_hash(cnf.clauses)
            != record["cnf_sha256"]
        ):
            raise AssertionError("a SAT benchmark CNF changed")
        stats = record["solver_stats"]
        if (
            record["status"] != "UNKNOWN"
            or not (
                record["conflict_budget"]
                <= stats["conflicts"]
                <= record["conflict_budget"] + 2
            )
        ):
            raise AssertionError("the bounded SAT status is malformed")
        if rerun_solver:
            actual = sat_benchmark.benchmark(
                case_number,
                encoding,
                moduli,
                int(record["conflict_budget"]),
            )
            if normalized_sat_record(actual) != normalized_sat_record(
                record
            ):
                raise AssertionError(
                    f"case {case_number} {encoding} benchmark changed"
                )
    return {
        "semantic_sha256": claimed_hash,
        "records": len(expected["results"]),
        "solver_rerun": rerun_solver,
        "cnfs_rebuilt": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rerun-sat",
        action="store_true",
        help="also repeat all sixteen 10,000-conflict solver controls",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    started = time.monotonic()
    result = {
        "status": "PASS",
        "triage": verify_triage(),
        "walsh": verify_walsh(),
        "sat_benchmark": verify_sat(args.rerun_sat),
        "production_search_run": False,
    }
    result["seconds"] = time.monotonic() - started
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
