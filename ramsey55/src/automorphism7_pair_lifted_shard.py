#!/usr/bin/env python3
"""Fail-closed selector-lifted proof runner for one C7 pair shard."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pysat
from pysat.solvers import Glucose3


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "verify"
for directory in (ROOT / "src", VERIFY):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import automorphism7_pair_lifted_blocker_sample as lifting  # noqa: E402
import automorphism7_side_orbit_cover as one_side  # noqa: E402
import automorphism7_side_pair_orbit_sweep as sweep  # noqa: E402
from residual_completion import checker_says_verified  # noqa: E402
from residual_completion_glucose import model_satisfies  # noqa: E402


PIPELINE = "ramsey55_automorphism7_pair_lifted_shard_v1"
BASE_VARIABLE_COUNT = 129


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_pin(record: object, path: Path, label: str) -> None:
    if (
        not isinstance(record, dict)
        or Path(str(record.get("path", ""))).resolve() != path.resolve()
        or record.get("sha256") != sha256_file(path)
    ):
        raise ValueError(f"pin mismatch: {label}")


def run_file_gated(
    gate_script: Path,
    filesystem: Path,
    minimum_free_bytes: int,
    maximum_file_bytes: int,
    command: list[str],
    timeout: int,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(gate_script),
            "--filesystem",
            str(filesystem),
            "--minimum-free-bytes",
            str(minimum_free_bytes),
            "--maximum-file-bytes",
            str(maximum_file_bytes),
            "--",
            *command,
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if (
        plan.get("schema")
        != "ramsey55.automorphism7_pair_lifted_shard_pilot_plan.v1"
        or plan.get("status") != "PREREGISTERED"
    ):
        raise SystemExit("wrong plan")
    if Path(plan["outputs"]["result"]).resolve() != args.result.resolve():
        raise SystemExit("result path mismatch")

    paths = {
        label: (
            Path(record["path"])
            if Path(record["path"]).is_absolute()
            else ROOT / record["path"]
        )
        for label, record in plan["pins"].items()
    }
    paths["runner"] = Path(__file__).resolve()
    for label, path in paths.items():
        record = plan["runner"] if label == "runner" else plan["pins"][label]
        validate_pin(record, path, label)
    if pysat.__version__ != plan["pysat_version"]:
        raise SystemExit("PySAT version mismatch")

    outputs = {
        name: ROOT / relative for name, relative in plan["outputs"].items()
    }
    if any(path.exists() for path in outputs.values()):
        raise SystemExit("refusing to overwrite output")
    outputs["wrapper_cnf"].parent.mkdir(parents=True, exist_ok=True)
    args.result.parent.mkdir(parents=True, exist_ok=True)

    caps = plan["hard_caps"]
    required = sum(
        int(caps[key])
        for key in (
            "raw_drat_bytes",
            "raw_lrat_bytes",
            "wrapper_bytes",
            "compressed_drat_bytes",
            "compressed_lrat_bytes",
            "minimum_free_bytes_after_completion",
        )
    )
    if required != int(caps["required_prelaunch_free_bytes"]):
        raise SystemExit("storage gate arithmetic mismatch")
    prelaunch_free = shutil.disk_usage(args.result.parent).free
    if prelaunch_free < required:
        raise SystemExit(f"storage gate failed: {prelaunch_free} < {required}")

    side_bundle = json.loads(
        paths["side_exhaustion_bundle"].read_text(encoding="utf-8")
    )
    if (
        side_bundle.get("valid") is not True
        or side_bundle.get("model_count") != 191394
    ):
        raise SystemExit("side-model exhaustion certificate missing")

    setup_started = time.monotonic()
    edge_orbits, representatives, pair_schedule = sweep.build_pair_schedule()
    shard_index = int(plan["shard"]["index"])
    shard_count = int(plan["shard"]["count"])
    pair_indices = [
        pair_index
        for pair_index in range(len(pair_schedule))
        if pair_index % shard_count == shard_index
    ]
    if (
        len(pair_schedule) != 37194
        or len(pair_indices) != int(plan["shard"]["expected_pair_count"])
        or pair_indices[0] != int(plan["shard"]["first_pair_index"])
        or pair_indices[-1] != int(plan["shard"]["last_pair_index"])
    ):
        raise AssertionError("shard schedule mismatch")

    variable_count, base_clauses = one_side.parse_dimacs(paths["cnf"])
    metadata = json.loads(paths["metadata"].read_text(encoding="utf-8"))
    fixed_units, map_a, map_b = lifting.fixed_and_side_maps(
        metadata, edge_orbits
    )
    if variable_count != BASE_VARIABLE_COUNT:
        raise AssertionError("bad base variable count")

    cubes: list[dict[str, Any]] = []
    for pair_index in pair_indices:
        left_class, right_class = pair_schedule[pair_index]
        cube = lifting.side_units(
            representatives[left_class],
            representatives[right_class],
            map_a,
            map_b,
        )
        cubes.append(
            {
                "pair_index": pair_index,
                "pair": [left_class, right_class],
                "selector": BASE_VARIABLE_COUNT + pair_index + 1,
                "side_units": list(cube),
                "blocker": [-literal for literal in cube],
            }
        )
    wrapper = lifting.wrapper_clauses(base_clauses, fixed_units, cubes)
    wrapper_payload = lifting.dimacs_bytes(
        BASE_VARIABLE_COUNT + len(pair_schedule), wrapper
    )
    if len(wrapper_payload) > int(caps["wrapper_bytes"]):
        raise RuntimeError("wrapper cap exceeded")
    lifting.write_bytes(outputs["wrapper_cnf"], wrapper_payload)

    records: list[dict[str, Any]] = []
    conflict_budget = int(plan["conflict_budget_per_pair"])
    run_started = time.monotonic()
    with outputs["lifted_drat"].open("wb") as stream:
        for shard_position, cube_record in enumerate(cubes):
            cube = tuple(int(literal) for literal in cube_record["side_units"])
            formula = tuple(base_clauses) + tuple(
                (unit,) for unit in (*fixed_units, *cube)
            )
            solve_started = time.monotonic()
            with Glucose3(
                bootstrap_with=formula, with_proof=True, use_timer=True
            ) as solver:
                solver.conf_budget(conflict_budget)
                outcome = solver.solve_limited()
                stats = solver.accum_stats()
                cpu_seconds = solver.time_accum()
                raw_proof = solver.get_proof() if outcome is False else None
                raw_model = solver.get_model() if outcome is True else None
            wall_seconds = time.monotonic() - solve_started
            if outcome is True:
                if raw_model is None or not model_satisfies(raw_model, formula):
                    raise AssertionError("SAT result failed direct replay")
                result = {
                    "pipeline": PIPELINE,
                    "status": "SAT",
                    "claim_boundary": "A SAT result stops the negative pipeline.",
                    "shard_index": shard_index,
                    "pair_index": cube_record["pair_index"],
                    "pair": cube_record["pair"],
                    "model": raw_model,
                    "cnf_replay": True,
                }
                lifting.write_bytes(
                    outputs["result"],
                    (json.dumps(result, indent=2, sort_keys=True) + "\n").encode(),
                )
                return 10
            if outcome is None or raw_proof is None:
                raise RuntimeError(
                    f"pair {cube_record['pair_index']} exhausted "
                    f"{conflict_budget} conflicts"
                )
            raw_payload = lifting.proof_payload(raw_proof)
            if len(raw_payload) > int(caps["per_cube_raw_proof_bytes"]):
                raise RuntimeError("per-cube raw proof cap exceeded")
            segment, measurements = lifting.lift_proof_segment(
                raw_proof,
                int(cube_record["selector"]),
                tuple(int(literal) for literal in cube_record["blocker"]),
            )
            projected = stream.tell() + len(segment) + 2
            if projected > int(caps["raw_drat_bytes"]):
                raise RuntimeError("raw lifted DRAT cap exceeded")
            offset = stream.tell()
            stream.write(segment)
            if shard_position % 16 == 15:
                stream.flush()
                os.fsync(stream.fileno())
            record = {
                **cube_record,
                **measurements,
                "shard_position": shard_position,
                "segment_offset": offset,
                "raw_proof_bytes": len(raw_payload),
                "raw_proof_sha256": hashlib.sha256(raw_payload).hexdigest(),
                "solver": "Glucose3",
                "solver_status": "UNSAT",
                "solver_cpu_seconds": cpu_seconds,
                "solver_wall_seconds": wall_seconds,
                "solver_stats": stats,
            }
            records.append(record)
            free = shutil.disk_usage(args.result.parent).free
            if free < (
                int(caps["minimum_free_bytes_after_completion"])
                + int(caps["raw_lrat_bytes"])
            ):
                raise RuntimeError("reserve for LRAT conversion breached")
            if (
                (shard_position + 1) % 16 == 0
                or shard_position + 1 == len(cubes)
            ):
                print(
                    json.dumps(
                        {
                            "event": "progress",
                            "shard_index": shard_index,
                            "completed": shard_position + 1,
                            "total": len(cubes),
                            "last_pair_index": cube_record["pair_index"],
                            "drat_bytes": projected - 2,
                            "elapsed_seconds": time.monotonic() - run_started,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
        stream.write(b"0\n")
        stream.flush()
        os.fsync(stream.fileno())

    gate_script = paths["file_gate"]
    minimum_before_lrat = (
        int(caps["minimum_free_bytes_after_completion"])
        + int(caps["raw_lrat_bytes"])
    )
    drat_started = time.monotonic()
    drat = run_file_gated(
        gate_script,
        args.result.parent,
        minimum_before_lrat,
        int(caps["raw_lrat_bytes"]),
        [
            str(paths["drat_trim"]),
            str(outputs["wrapper_cnf"]),
            str(outputs["lifted_drat"]),
            "-I",
            "-L",
            str(outputs["lifted_lrat"]),
        ],
        int(plan["proof_check_timeout_seconds"]),
    )
    drat_seconds = time.monotonic() - drat_started
    drat_valid = (
        drat.returncode == 0
        and checker_says_verified(drat.stdout + drat.stderr)
        and outputs["lifted_lrat"].is_file()
        and outputs["lifted_lrat"].stat().st_size <= int(caps["raw_lrat_bytes"])
    )
    if not drat_valid:
        raise RuntimeError("DRAT verification/conversion failed")

    lrat_started = time.monotonic()
    lrat = subprocess.run(
        [
            str(paths["lrat_check"]),
            str(outputs["wrapper_cnf"]),
            str(outputs["lifted_lrat"]),
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=int(plan["proof_check_timeout_seconds"]),
    )
    lrat_seconds = time.monotonic() - lrat_started
    lrat_valid = (
        lrat.returncode == 0 and checker_says_verified(lrat.stdout + lrat.stderr)
    )
    if not lrat_valid:
        raise RuntimeError("LRAT verification failed")

    for raw_name, compressed_name, cap_name in (
        ("lifted_drat", "lifted_drat_zstd", "compressed_drat_bytes"),
        ("lifted_lrat", "lifted_lrat_zstd", "compressed_lrat_bytes"),
    ):
        compressed = run_file_gated(
            gate_script,
            args.result.parent,
            int(caps["minimum_free_bytes_after_completion"]),
            int(caps[cap_name]),
            [
                str(paths["zstd"]),
                f"-{int(plan['zstd_level'])}",
                "-q",
                "-f",
                str(outputs[raw_name]),
                "-o",
                str(outputs[compressed_name]),
            ],
            600,
        )
        if (
            compressed.returncode != 0
            or not outputs[compressed_name].is_file()
            or outputs[compressed_name].stat().st_size > int(caps[cap_name])
        ):
            raise RuntimeError(f"{compressed_name} compression/cap failed")

    result = {
        "pipeline": PIPELINE,
        "status": "CERTIFIED_UNSAT_SHARD",
        "evidence_label": "FAIL-CLOSED SELECTOR-LIFTED SHARD CERTIFICATE",
        "claim_boundary": (
            "This certifies only the listed pair-index shard. The global "
            "order-7 conclusion requires all 128 shards and the exact "
            "side/pair cover."
        ),
        "shard_index": shard_index,
        "shard_count": shard_count,
        "pair_count": len(pair_indices),
        "first_pair_index": pair_indices[0],
        "last_pair_index": pair_indices[-1],
        "pair_schedule_sha256": sweep.EXPECTED_PAIR_SCHEDULE_SHA256,
        "conflict_budget_per_pair": conflict_budget,
        "wrapper": {
            "path": str(outputs["wrapper_cnf"].resolve()),
            "sha256": sha256_file(outputs["wrapper_cnf"]),
            "bytes": outputs["wrapper_cnf"].stat().st_size,
            "variable_count": BASE_VARIABLE_COUNT + len(pair_schedule),
            "clause_count": len(wrapper),
        },
        "lifted_drat": {
            "path": str(outputs["lifted_drat"].resolve()),
            "sha256": sha256_file(outputs["lifted_drat"]),
            "bytes": outputs["lifted_drat"].stat().st_size,
            "zstd_path": str(outputs["lifted_drat_zstd"].resolve()),
            "zstd_sha256": sha256_file(outputs["lifted_drat_zstd"]),
            "zstd_bytes": outputs["lifted_drat_zstd"].stat().st_size,
            "drat_trim_valid": drat_valid,
            "drat_trim_seconds": drat_seconds,
        },
        "lifted_lrat": {
            "path": str(outputs["lifted_lrat"].resolve()),
            "sha256": sha256_file(outputs["lifted_lrat"]),
            "bytes": outputs["lifted_lrat"].stat().st_size,
            "zstd_path": str(outputs["lifted_lrat_zstd"].resolve()),
            "zstd_sha256": sha256_file(outputs["lifted_lrat_zstd"]),
            "zstd_bytes": outputs["lifted_lrat_zstd"].stat().st_size,
            "lrat_check_valid": lrat_valid,
            "lrat_check_seconds": lrat_seconds,
        },
        "records": records,
        "measurements": {
            "total_conflicts": sum(
                int(record["solver_stats"]["conflicts"]) for record in records
            ),
            "maximum_conflicts": max(
                int(record["solver_stats"]["conflicts"]) for record in records
            ),
            "solver_wall_seconds_sum": sum(
                float(record["solver_wall_seconds"]) for record in records
            ),
            "segment_bytes_sum": sum(
                int(record["segment_bytes"]) for record in records
            ),
            "segment_bytes_maximum": max(
                int(record["segment_bytes"]) for record in records
            ),
            "raw_deletion_records_removed": sum(
                int(record["raw_deletion_record_count"]) for record in records
            ),
            "raw_addition_records_lifted": sum(
                int(record["raw_addition_record_count"]) for record in records
            ),
        },
        "hard_caps": caps,
        "prelaunch_free_bytes": prelaunch_free,
        "setup_seconds": run_started - setup_started,
        "run_seconds": time.monotonic() - run_started,
        "side_exhaustion_bundle_sha256": sha256_file(
            paths["side_exhaustion_bundle"]
        ),
        "plan_sha256": sha256_file(args.plan),
        "all_pairs_unsat_within_budget": True,
        "all_blockers_derived": True,
        "drat_trim_valid": drat_valid,
        "lrat_check_valid": lrat_valid,
    }
    payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
    lifting.write_bytes(outputs["result"], payload)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
