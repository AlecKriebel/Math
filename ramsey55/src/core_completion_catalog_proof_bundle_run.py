#!/usr/bin/env python3
"""Generate and independently replay one fixed-core proof bundle."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_catalog_batch import (  # noqa: E402
    atomic_json,
    atomic_write,
    sha256_file,
)
from core_completion_catalog_screen import (  # noqa: E402
    VERIFIED_SAT,
    preserve_and_verify_sat,
)


RUNNER_ID = "ramsey55_core_completion_catalog_proof_bundle_run_v1"


def parse_pairs(path: Path) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for physical_line, raw in enumerate(
        path.read_text(encoding="ascii").splitlines(), start=1
    ):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        fields = stripped.split()
        if len(fields) != 2:
            raise ValueError(
                f"invalid pair record at physical line {physical_line}"
            )
        pair = int(fields[0]), int(fields[1])
        if pair[0] < 1 or not 0 <= pair[1] < 42:
            raise ValueError(f"pair outside allowed range: {pair}")
        pairs.append(pair)
    if not pairs or len(pairs) != len(set(pairs)):
        raise ValueError("pair list is empty or contains duplicates")
    return pairs


def parse_json_lines(raw: str, label: str) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for line_number, line in enumerate(raw.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"{label} line {line_number} is invalid JSON"
            ) from error
        if not isinstance(record, dict):
            raise ValueError(f"{label} line {line_number} is not an object")
        records.append(record)
    if not records:
        raise ValueError(f"{label} is empty")
    return records


def validate_plan(
    plan_path: Path,
    *,
    catalog_sha256: str,
    pairs_sha256: str,
    producer_sha256: str,
    checker_sha256: str,
    seconds_limit: float,
    node_limit: int,
    bundle_byte_limit: int,
    max_wall_seconds: float,
) -> dict[str, object]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    planned_pairs_hashes = {
        value
        for value in (
            plan.get("sample_pairs_sha256"),
            plan.get("pairs_sha256"),
        )
        if isinstance(value, str)
    }
    for shard in plan.get("shards", []):
        if isinstance(shard, dict) and isinstance(
            shard.get("pairs_sha256"), str
        ):
            planned_pairs_hashes.add(shard["pairs_sha256"])
    required = {
        "catalog_sha256": catalog_sha256,
        "producer_binary_sha256": producer_sha256,
        "checker_binary_sha256": checker_sha256,
        "seconds_limit_per_instance": seconds_limit,
        "node_limit_per_instance": node_limit,
        "bundle_byte_limit_per_shard": bundle_byte_limit,
        "max_wall_seconds": max_wall_seconds,
    }
    observed = {
        "catalog_sha256": plan.get("catalog_sha256"),
        "producer_binary_sha256": plan.get("producer_binary_sha256"),
        "checker_binary_sha256": plan.get("checker_binary_sha256"),
        "seconds_limit_per_instance": plan.get(
            "seconds_limit_per_instance"
        ),
        "node_limit_per_instance": plan.get("node_limit_per_instance"),
        "bundle_byte_limit_per_shard": plan.get(
            "bundle_byte_limit_per_shard"
        ),
        "max_wall_seconds": plan.get("max_wall_seconds"),
    }
    mismatches = {
        key: {"plan": observed[key], "command": value}
        for key, value in required.items()
        if observed[key] != value
    }
    if pairs_sha256 not in planned_pairs_hashes:
        mismatches["pairs_sha256"] = {
            "plan": sorted(planned_pairs_hashes),
            "command": pairs_sha256,
        }
    if mismatches:
        raise ValueError(f"proof-bundle plan mismatch: {mismatches}")
    return plan


def run_bundle(
    *,
    catalog: Path,
    pairs_path: Path,
    producer: Path,
    checker: Path,
    plan: Path,
    output_dir: Path,
    seconds_limit: float,
    node_limit: int,
    bundle_byte_limit: int,
    max_wall_seconds: float,
    python: Path,
    exhaustive_verifier: Path,
    bitset_verifier: Path,
) -> tuple[dict[str, object], int]:
    started = time.monotonic()
    for required in (
        catalog,
        pairs_path,
        producer,
        checker,
        plan,
        python,
        exhaustive_verifier,
        bitset_verifier,
    ):
        if not required.is_file():
            raise ValueError(f"required file is absent: {required}")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("output directory must be absent or empty")
    output_dir.mkdir(parents=True, exist_ok=True)

    pairs = parse_pairs(pairs_path)
    catalog_sha256 = sha256_file(catalog)
    pairs_sha256 = sha256_file(pairs_path)
    producer_sha256 = sha256_file(producer)
    checker_sha256 = sha256_file(checker)
    validate_plan(
        plan,
        catalog_sha256=catalog_sha256,
        pairs_sha256=pairs_sha256,
        producer_sha256=producer_sha256,
        checker_sha256=checker_sha256,
        seconds_limit=seconds_limit,
        node_limit=node_limit,
        bundle_byte_limit=bundle_byte_limit,
        max_wall_seconds=max_wall_seconds,
    )

    bundle = output_dir / "proofs.c2dpb"
    producer_transcript = output_dir / "producer.jsonl"
    checker_transcript = output_dir / "checker.jsonl"
    producer_started = time.monotonic()
    produced = subprocess.run(
        (
            str(producer),
            "--graph",
            str(catalog),
            "--pairs",
            str(pairs_path),
            "--bundle",
            str(bundle),
            "--catalog-sha256",
            catalog_sha256,
            "--pairs-sha256",
            pairs_sha256,
            "--node-limit",
            str(node_limit),
            "--seconds-limit",
            str(seconds_limit),
            "--bundle-byte-limit",
            str(bundle_byte_limit),
        ),
        text=True,
        capture_output=True,
        check=False,
        timeout=max_wall_seconds,
    )
    producer_wall_seconds = time.monotonic() - producer_started
    atomic_write(
        producer_transcript,
        produced.stdout.encode("utf-8"),
    )
    producer_records = parse_json_lines(
        produced.stdout, "producer transcript"
    )
    pair_records = [
        record
        for record in producer_records
        if record.get("record_type") == "PAIR"
    ]
    selected_pairs = [
        (int(record["catalog_line"]), int(record["deleted_vertex"]))
        for record in pair_records
    ]
    expected_prefix = pairs[: len(selected_pairs)]
    if selected_pairs != expected_prefix:
        raise ValueError("producer transcript pair order is invalid")

    sat_records = [
        record for record in pair_records if record.get("status") == "SAT"
    ]
    sat_verifications: list[dict[str, object]] = []
    for solver_result in sat_records:
        verified = preserve_and_verify_sat(
            catalog=catalog,
            catalog_sha256=catalog_sha256,
            line=int(solver_result["catalog_line"]),
            deleted=int(solver_result["deleted_vertex"]),
            solver_result=solver_result,
            output_dir=output_dir,
            python=python,
            exhaustive_verifier=exhaustive_verifier,
            bitset_verifier=bitset_verifier,
        )
        sat_verifications.append(verified)

    final_producer = producer_records[-1]
    checker_result: dict[str, object] | None = None
    checker_wall_seconds = 0.0
    checker_stdout = ""
    checker_stderr = ""
    if produced.returncode == 0:
        if (
            final_producer.get("record_type") != "BUNDLE"
            or final_producer.get("status") != "UNSAT_BUNDLE_COMPLETE"
            or len(pair_records) != len(pairs)
            or any(record.get("status") != "UNSAT" for record in pair_records)
            or not bundle.is_file()
        ):
            raise ValueError("producer completion record is inconsistent")
        checker_started = time.monotonic()
        remaining_wall = max_wall_seconds - (
            time.monotonic() - started
        )
        if remaining_wall <= 0:
            raise TimeoutError("bundle run reached its global wall stop")
        checked = subprocess.run(
            (
                str(checker),
                "--graph",
                str(catalog),
                "--pairs",
                str(pairs_path),
                "--bundle",
                str(bundle),
                "--transcript",
                str(checker_transcript),
                "--catalog-sha256",
                catalog_sha256,
                "--pairs-sha256",
                pairs_sha256,
            ),
            text=True,
            capture_output=True,
            check=False,
            timeout=remaining_wall,
        )
        checker_wall_seconds = time.monotonic() - checker_started
        checker_stdout = checked.stdout
        checker_stderr = checked.stderr
        checker_records = parse_json_lines(checked.stdout, "checker stdout")
        if len(checker_records) != 1:
            raise ValueError("checker did not emit one summary object")
        checker_result = checker_records[0]
        if (
            checked.returncode != 0
            or checker_result.get("status")
            != "VERIFIED_UNSAT_FIXED_CORE_BUNDLE"
            or checker_result.get("pair_count") != len(pairs)
            or not checker_transcript.is_file()
        ):
            raise ValueError(
                "independent checker rejected or returned inconsistent data: "
                f"returncode={checked.returncode} stderr={checked.stderr!r}"
            )
        replay_records = parse_json_lines(
            checker_transcript.read_text(encoding="utf-8"),
            "checker transcript",
        )
        replay_pairs = [
            (int(record["catalog_line"]), int(record["deleted_vertex"]))
            for record in replay_records
        ]
        if (
            replay_pairs != pairs
            or any(
                record.get("status")
                != "VERIFIED_UNSAT_FIXED_41_CORE_TWO_VERTEX_COMPLETION"
                for record in replay_records
            )
        ):
            raise ValueError("checker transcript does not certify exact pairs")

    if produced.returncode == 0 and checker_result is not None:
        status = "CERTIFIED_UNSAT_FIXED_CORE_BUNDLE"
        exit_code = 0
    elif produced.returncode == 10 and sat_verifications:
        status = (
            "DUAL_VERIFIED_SAT_CONSTRUCTION"
            if all(
                result.get("classification") == VERIFIED_SAT
                for result in sat_verifications
            )
            else "SAT_MODEL_VERIFICATION_FAILED"
        )
        exit_code = (
            10
            if status == "DUAL_VERIFIED_SAT_CONSTRUCTION"
            else 1
        )
    elif produced.returncode == 2:
        status = "LIMIT_NO_CONCLUSION"
        exit_code = 2
    else:
        status = "BUNDLE_RUN_ERROR"
        exit_code = 1

    artifacts: dict[str, object] = {
        "producer_transcript": str(producer_transcript.resolve()),
        "producer_transcript_sha256": sha256_file(producer_transcript),
        "producer_transcript_bytes": producer_transcript.stat().st_size,
    }
    for label, path in (
        ("bundle", bundle),
        ("partial_bundle", Path(str(bundle) + ".partial")),
        ("checker_transcript", checker_transcript),
    ):
        if path.is_file():
            artifacts[label] = str(path.resolve())
            artifacts[f"{label}_sha256"] = sha256_file(path)
            artifacts[f"{label}_bytes"] = path.stat().st_size

    result = {
        "runner": RUNNER_ID,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "scope": (
            "only the explicitly listed fixed induced 41-vertex cores; "
            "never global order-43 nonexistence"
        ),
        "catalog": str(catalog.resolve()),
        "catalog_sha256": catalog_sha256,
        "pairs": str(pairs_path.resolve()),
        "pairs_sha256": pairs_sha256,
        "expected_pair_count": len(pairs),
        "producer_pair_count": len(pair_records),
        "producer_returncode": produced.returncode,
        "producer_stderr": produced.stderr,
        "producer_wall_seconds": producer_wall_seconds,
        "producer_records": pair_records,
        "checker_result": checker_result,
        "checker_stdout": checker_stdout,
        "checker_stderr": checker_stderr,
        "checker_wall_seconds": checker_wall_seconds,
        "sat_verifications": sat_verifications,
        "seconds_limit_per_instance": seconds_limit,
        "node_limit_per_instance": node_limit,
        "bundle_byte_limit": bundle_byte_limit,
        "max_wall_seconds": max_wall_seconds,
        "producer": str(producer.resolve()),
        "producer_sha256": producer_sha256,
        "checker": str(checker.resolve()),
        "checker_sha256": checker_sha256,
        "plan": str(plan.resolve()),
        "plan_sha256": sha256_file(plan),
        "runner_source_sha256": sha256_file(Path(__file__)),
        "artifacts": artifacts,
        "runtime_seconds": time.monotonic() - started,
    }
    result_path = output_dir / "result.json"
    atomic_json(result_path, result)
    return result, exit_code


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--pairs", required=True, type=Path)
    parser.add_argument("--producer", required=True, type=Path)
    parser.add_argument("--checker", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--seconds-limit-per-instance", required=True, type=float)
    parser.add_argument("--node-limit-per-instance", required=True, type=int)
    parser.add_argument("--bundle-byte-limit", required=True, type=int)
    parser.add_argument("--max-wall-seconds", required=True, type=float)
    parser.add_argument("--python", type=Path, default=Path(sys.executable))
    parser.add_argument(
        "--exhaustive-verifier",
        type=Path,
        default=ROOT / "verify" / "exhaustive_verify.py",
    )
    parser.add_argument(
        "--bitset-verifier",
        type=Path,
        default=ROOT / "build" / "bitset_verify",
    )
    args = parser.parse_args()
    result, exit_code = run_bundle(
        catalog=args.catalog.resolve(),
        pairs_path=args.pairs.resolve(),
        producer=args.producer.resolve(),
        checker=args.checker.resolve(),
        plan=args.plan.resolve(),
        output_dir=args.output_dir.resolve(),
        seconds_limit=args.seconds_limit_per_instance,
        node_limit=args.node_limit_per_instance,
        bundle_byte_limit=args.bundle_byte_limit,
        max_wall_seconds=args.max_wall_seconds,
        python=args.python.resolve(),
        exhaustive_verifier=args.exhaustive_verifier.resolve(),
        bitset_verifier=args.bitset_verifier.resolve(),
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "expected_pair_count": result["expected_pair_count"],
                "producer_pair_count": result["producer_pair_count"],
                "producer_wall_seconds": result["producer_wall_seconds"],
                "checker_wall_seconds": result["checker_wall_seconds"],
                "runtime_seconds": result["runtime_seconds"],
                "result": str(
                    (args.output_dir / "result.json").resolve()
                ),
            },
            sort_keys=True,
        )
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
