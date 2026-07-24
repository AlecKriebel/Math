#!/usr/bin/env python3
"""Benchmark indexed cross-proof compression on the certified C7 sample."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from pysat.solvers import Glucose3


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "verify"
for directory in (ROOT / "src", VERIFY):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import automorphism7_pair_proof_size_sample as sample  # noqa: E402
import automorphism7_side_orbit_cover as one_side  # noqa: E402
import automorphism7_side_pair_orbit_sweep as sweep  # noqa: E402
from residual_completion import checker_says_verified  # noqa: E402
from residual_completion_glucose import write_proof_atomic  # noqa: E402


PIPELINE = "ramsey55_automorphism7_pair_concat_proof_sample_v1"
MAGIC = b"R55AUT7INDEXED1\n"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def append_file(destination: Path, source: Path) -> tuple[int, int]:
    offset = destination.stat().st_size if destination.exists() else 0
    with destination.open("ab") as output, source.open("rb") as input_stream:
        shutil.copyfileobj(input_stream, output, 1 << 20)
        output.flush()
        os.fsync(output.fileno())
    return offset, source.stat().st_size


def build_indexed_archive(
    artifact: str,
    payload_path: Path,
    records: list[dict[str, Any]],
    archive_path: Path,
) -> dict[str, int | str]:
    index = {
        "schema": "ramsey55.indexed_proof_concatenation.v1",
        "artifact": artifact,
        "payload_bytes": payload_path.stat().st_size,
        "records": records,
    }
    index_payload = (
        json.dumps(index, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    with archive_path.open("wb") as output, payload_path.open("rb") as payload:
        output.write(MAGIC)
        output.write(struct.pack(">Q", len(index_payload)))
        output.write(index_payload)
        shutil.copyfileobj(payload, output, 1 << 20)
        output.flush()
        os.fsync(output.fileno())
    return {
        "index_bytes": len(index_payload),
        "payload_bytes": payload_path.stat().st_size,
        "archive_bytes": archive_path.stat().st_size,
        "archive_sha256": sha256_file(archive_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing to overwrite output")
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if (
        not isinstance(plan, dict)
        or plan.get("schema")
        != "ramsey55.automorphism7_pair_concat_proof_sample_plan.v1"
        or plan.get("status") != "PREREGISTERED"
    ):
        raise SystemExit("invalid plan")

    pins = {
        "source_sample_plan": ROOT / plan["source_sample_plan"]["path"],
        "source_sample_result": ROOT / plan["source_sample_result"]["path"],
        "cnf": ROOT / plan["cnf"]["path"],
        "metadata": ROOT / plan["metadata"]["path"],
        "sweep_runner": ROOT / plan["sweep_runner"]["path"],
        "runner": Path(__file__).resolve(),
        "drat_trim": Path(plan["drat_trim"]["path"]),
        "lrat_check": Path(plan["lrat_check"]["path"]),
        "zstd": Path(plan["zstd"]["path"]),
    }
    for label, path in pins.items():
        record = plan["runner" if label == "runner" else label]
        if (
            Path(record["path"]).resolve()
            != (path if path.is_absolute() else ROOT / path).resolve()
            or record["sha256"] != sha256_file(path)
        ):
            raise SystemExit(f"pin mismatch: {label}")
    if Path(plan["output"]).resolve() != args.output.resolve():
        raise SystemExit("output mismatch")

    source_plan = json.loads(
        pins["source_sample_plan"].read_text(encoding="utf-8")
    )
    source_result = json.loads(
        pins["source_sample_result"].read_text(encoding="utf-8")
    )
    if (
        source_result.get("sample_count") != 12
        or source_result.get("all_drat_valid") is not True
        or source_result.get("all_lrat_valid") is not True
    ):
        raise SystemExit("source sample is not fully certified")

    gate = plan["storage_gate"]
    if (
        gate["required_prelaunch_free_bytes"]
        != gate["maximum_transient_bytes"] + gate["minimum_free_bytes"]
    ):
        raise SystemExit("invalid storage gate")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    available = shutil.disk_usage(args.output.parent).free
    if available < gate["required_prelaunch_free_bytes"]:
        raise SystemExit("storage gate failed")

    setup_started = time.monotonic()
    edge_orbits, class_representatives, pair_schedule = (
        sweep.build_pair_schedule()
    )
    variable_count, base_clauses = one_side.parse_dimacs(pins["cnf"])
    metadata = json.loads(pins["metadata"].read_text(encoding="utf-8"))
    edge_table = one_side.global_edge_table(metadata)
    map_a = [edge_table[orbit[0]] for orbit in edge_orbits]
    map_b = [
        edge_table[(orbit[0][0] + 21, orbit[0][1] + 21)]
        for orbit in edge_orbits
    ]
    fixed_orbits = sorted(
        {
            variable
            for (left, right), variable in edge_table.items()
            if right == 42
        },
        key=lambda variable: min(
            left
            for (left, right), observed in edge_table.items()
            if right == 42 and observed == variable
        ),
    )
    fixed_units = fixed_orbits[:3] + [
        -variable for variable in fixed_orbits[3:]
    ]
    selected = source_plan["samples"]
    setup_seconds = time.monotonic() - setup_started

    drat_index: list[dict[str, Any]] = []
    lrat_index: list[dict[str, Any]] = []
    run_started = time.monotonic()
    with tempfile.TemporaryDirectory(
        prefix="automorphism7-concat-proof-sample-",
        dir=args.output.parent,
    ) as temporary_directory:
        temporary_root = Path(temporary_directory)
        drat_payload = temporary_root / "drat.payload"
        lrat_payload = temporary_root / "lrat.payload"
        for sample_position, selected_record in enumerate(selected):
            pair_index = int(selected_record["pair_index"])
            pair = pair_schedule[pair_index]
            if list(pair) != selected_record["pair"]:
                raise AssertionError("sample pair mismatch")
            left_model = class_representatives[pair[0]]
            right_model = class_representatives[pair[1]]
            units = list(fixed_units)
            units.extend(
                variable if left_model >> index & 1 else -variable
                for index, variable in enumerate(map_a)
            )
            units.extend(
                -variable if right_model >> index & 1 else variable
                for index, variable in enumerate(map_b)
            )
            clauses = tuple(base_clauses) + tuple((unit,) for unit in units)
            formula_path = temporary_root / "formula.cnf"
            proof_path = temporary_root / "proof.drat"
            lrat_path = temporary_root / "proof.lrat"
            sample.write_dimacs(formula_path, variable_count, clauses)
            with Glucose3(
                bootstrap_with=clauses, with_proof=True, use_timer=True
            ) as solver:
                outcome = solver.solve()
                proof = solver.get_proof() if outcome is False else None
            if outcome is not False or proof is None:
                raise AssertionError("sample did not solve UNSAT")
            proof_sha256, _ = write_proof_atomic(proof_path, proof)
            drat = subprocess.run(
                [
                    str(pins["drat_trim"]),
                    str(formula_path),
                    str(proof_path),
                    "-I",
                    "-L",
                    str(lrat_path),
                ],
                capture_output=True,
                text=True,
                timeout=180,
                check=False,
            )
            lrat = subprocess.run(
                [
                    str(pins["lrat_check"]),
                    str(formula_path),
                    str(lrat_path),
                ],
                capture_output=True,
                text=True,
                timeout=180,
                check=False,
            )
            if (
                drat.returncode != 0
                or lrat.returncode != 0
                or not checker_says_verified(drat.stdout + drat.stderr)
                or not checker_says_verified(lrat.stdout + lrat.stderr)
            ):
                raise AssertionError("proof verification failed")
            drat_offset, drat_bytes = append_file(drat_payload, proof_path)
            lrat_offset, lrat_bytes = append_file(lrat_payload, lrat_path)
            drat_index.append(
                {
                    "sample_position": sample_position,
                    "pair_index": pair_index,
                    "offset": drat_offset,
                    "bytes": drat_bytes,
                    "sha256": proof_sha256,
                }
            )
            lrat_index.append(
                {
                    "sample_position": sample_position,
                    "pair_index": pair_index,
                    "offset": lrat_offset,
                    "bytes": lrat_bytes,
                    "sha256": sha256_file(lrat_path),
                }
            )
            formula_path.unlink()
            proof_path.unlink()
            lrat_path.unlink()
            print(
                json.dumps(
                    {
                        "event": "sample_complete",
                        "sample_position": sample_position,
                        "pair_index": pair_index,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

        drat_archive = temporary_root / "drat.indexed"
        lrat_archive = temporary_root / "lrat.indexed"
        drat_measure = build_indexed_archive(
            "DRAT", drat_payload, drat_index, drat_archive
        )
        lrat_measure = build_indexed_archive(
            "LRAT", lrat_payload, lrat_index, lrat_archive
        )
        compression_started = time.monotonic()
        drat_zstd = sample.zstd_payload(
            drat_archive, pins["zstd"], int(plan["zstd_level"])
        )
        drat_compression_seconds = time.monotonic() - compression_started
        compression_started = time.monotonic()
        lrat_zstd = sample.zstd_payload(
            lrat_archive, pins["zstd"], int(plan["zstd_level"])
        )
        lrat_compression_seconds = time.monotonic() - compression_started

    target_count = len(pair_schedule)
    concat_lrat_projection = (
        len(lrat_zstd) * target_count + len(selected) - 1
    ) // len(selected)
    conservative_lrat_projection = int(
        source_result["projection"]["lrat_zstd_max_projection_bytes"]
    )
    full_gate = {
        "projection_basis": (
            "maximum per-file zstd-19 LRAT size in the certified sample"
        ),
        "projected_lrat_bytes": conservative_lrat_projection,
        "additional_working_reserve_bytes": int(
            plan["full_bundle_working_reserve_bytes"]
        ),
        "required_prelaunch_free_bytes": conservative_lrat_projection
        + int(plan["full_bundle_working_reserve_bytes"]),
        "available_at_sample_launch_bytes": available,
        "passes_at_sample_launch": available
        >= conservative_lrat_projection
        + int(plan["full_bundle_working_reserve_bytes"]),
    }
    result = {
        "pipeline": PIPELINE,
        "evidence_label": "CERTIFIED CONCATENATED PROOF-SIZE SAMPLE",
        "claim_boundary": (
            "All 12 proofs were regenerated and checked. Compression "
            "projections are engineering estimates; no unsampled pair is "
            "certified and the full bundle remains unlaunched."
        ),
        "plan_path": str(args.plan.resolve()),
        "plan_sha256": sha256_file(args.plan),
        "source_sample_result_sha256": sha256_file(
            pins["source_sample_result"]
        ),
        "sample_count": len(selected),
        "setup_seconds": setup_seconds,
        "drat": {
            **drat_measure,
            "zstd_level": int(plan["zstd_level"]),
            "zstd_bytes": len(drat_zstd),
            "zstd_sha256": hashlib.sha256(drat_zstd).hexdigest(),
            "compression_seconds": drat_compression_seconds,
            "sum_individual_zstd_bytes": sum(
                int(record["drat_zstd_bytes"])
                for record in source_result["records"]
            ),
        },
        "lrat": {
            **lrat_measure,
            "zstd_level": int(plan["zstd_level"]),
            "zstd_bytes": len(lrat_zstd),
            "zstd_sha256": hashlib.sha256(lrat_zstd).hexdigest(),
            "compression_seconds": lrat_compression_seconds,
            "sum_individual_zstd_bytes": sum(
                int(record["lrat_zstd_bytes"])
                for record in source_result["records"]
            ),
            "concat_average_projection_bytes": concat_lrat_projection,
            "conservative_per_file_max_projection_bytes": (
                conservative_lrat_projection
            ),
        },
        "retention_policy": (
            "LRAT-only after each DRAT has been converted and both DRAT and "
            "LRAT checks pass; formulas and DRAT files are transient."
        ),
        "full_lrat_only_storage_gate": full_gate,
        "storage_gate": gate,
        "runtime_seconds": time.monotonic() - run_started,
    }
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
