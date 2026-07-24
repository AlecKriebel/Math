#!/usr/bin/env python3
"""Certify a tiny pair sample and project order-7 proof-bundle storage."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

import pysat
from pysat.solvers import Glucose3


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "verify"
if str(VERIFY) not in sys.path:
    sys.path.insert(0, str(VERIFY))

import automorphism7_side_orbit_cover as one_side  # noqa: E402
import automorphism7_side_pair_orbit_sweep as sweep  # noqa: E402
from residual_completion import checker_says_verified  # noqa: E402
from residual_completion_glucose import write_proof_atomic  # noqa: E402


PIPELINE = "ramsey55_automorphism7_pair_proof_size_sample_v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def write_dimacs(
    path: Path,
    variable_count: int,
    clauses: tuple[tuple[int, ...], ...],
) -> None:
    with path.open("w", encoding="ascii") as stream:
        stream.write(f"p cnf {variable_count} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")
        stream.flush()
        os.fsync(stream.fileno())


def zstd_payload(path: Path, executable: Path, level: int) -> bytes:
    completed = subprocess.run(
        [str(executable), f"-{level}", "-q", "-c", str(path)],
        capture_output=True,
        check=False,
        timeout=180,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"zstd failed for {path}: {completed.stderr.decode(errors='replace')}"
        )
    return completed.stdout


def parse_plan(path: Path) -> dict[str, Any]:
    plan = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(plan, dict):
        raise ValueError("plan is not an object")
    return plan


def validate_pin(record: object, path: Path, label: str) -> None:
    if (
        not isinstance(record, dict)
        or Path(record.get("path", "")).resolve() != path.resolve()
        or record.get("sha256") != sha256_file(path)
    ):
        raise ValueError(f"pin mismatch for {label}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing to overwrite output")
    plan = parse_plan(args.plan)
    if (
        plan.get("schema")
        != "ramsey55.automorphism7_pair_proof_size_sample_plan.v1"
        or plan.get("status") != "PREREGISTERED"
    ):
        raise SystemExit("invalid plan schema/status")

    paths = {
        "cnf": ROOT / str(plan["cnf"]["path"]),
        "metadata": ROOT / str(plan["metadata"]["path"]),
        "runner": ROOT / str(plan["runner"]["path"]),
        "pair_audit": ROOT / str(plan["pair_audit"]["path"]),
        "drat_trim": Path(str(plan["drat_trim"]["path"])),
        "lrat_check": Path(str(plan["lrat_check"]["path"])),
        "zstd": Path(str(plan["zstd"]["path"])),
    }
    for label, path in paths.items():
        validate_pin(plan[label], path, label)
    validate_pin(plan["sample_runner"], Path(__file__).resolve(), "sample_runner")
    if Path(plan.get("output", "")).resolve() != args.output.resolve():
        raise SystemExit("plan output mismatch")
    if plan.get("pysat_version") != pysat.__version__:
        raise SystemExit("PySAT version mismatch")

    storage = plan.get("storage_gate")
    if not isinstance(storage, dict):
        raise SystemExit("storage gate missing")
    maximum_transient = storage.get("maximum_transient_bytes")
    reserve = storage.get("minimum_free_bytes")
    required = storage.get("required_prelaunch_free_bytes")
    if (
        any(type(value) is not int or value < 1 for value in (
            maximum_transient,
            reserve,
            required,
        ))
        or required != maximum_transient + reserve
    ):
        raise SystemExit("invalid storage gate")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    available = shutil.disk_usage(args.output.parent).free
    if available < required:
        raise SystemExit(
            f"storage gate failed: free {available} < required {required}"
        )

    setup_started = time.monotonic()
    edge_orbits, class_representatives, pair_schedule = (
        sweep.build_pair_schedule()
    )
    if (
        len(pair_schedule) != plan["pair_schedule_count"]
        or plan["pair_schedule_sha256"]
        != sweep.EXPECTED_PAIR_SCHEDULE_SHA256
    ):
        raise AssertionError("pair schedule mismatch")
    samples = plan.get("samples")
    if not isinstance(samples, list) or len(samples) < 1:
        raise ValueError("empty sample")
    selected: list[tuple[int, tuple[int, int]]] = []
    for sample in samples:
        if not isinstance(sample, dict) or type(sample.get("pair_index")) is not int:
            raise ValueError("malformed sample")
        pair_index = sample["pair_index"]
        pair = pair_schedule[pair_index]
        if list(pair) != sample.get("pair"):
            raise AssertionError("sample pair mismatch")
        left_model = format(class_representatives[pair[0]], "030b")
        right_model = format(class_representatives[pair[1]], "030b")
        if [left_model, right_model] != sample.get("models"):
            raise AssertionError("sample model mismatch")
        selected.append((pair_index, pair))

    variable_count, base_clauses = one_side.parse_dimacs(paths["cnf"])
    metadata = json.loads(paths["metadata"].read_text(encoding="utf-8"))
    if variable_count != 129 or not isinstance(metadata, dict):
        raise ValueError("unexpected formula")
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

    records: list[dict[str, Any]] = []
    setup_seconds = time.monotonic() - setup_started
    run_started = time.monotonic()
    with tempfile.TemporaryDirectory(
        prefix="automorphism7-pair-proof-sample-",
        dir=args.output.parent,
    ) as temporary_directory:
        temporary_root = Path(temporary_directory)
        for sample_position, (pair_index, pair) in enumerate(selected):
            left_class, right_class = pair
            left_model = class_representatives[left_class]
            right_model = class_representatives[right_class]
            units = list(fixed_units)
            units.extend(
                variable if left_model >> index & 1 else -variable
                for index, variable in enumerate(map_a)
            )
            units.extend(
                -variable if right_model >> index & 1 else variable
                for index, variable in enumerate(map_b)
            )
            if len(units) != 66 or len({abs(unit) for unit in units}) != 66:
                raise AssertionError("sample does not fix 66 variables")
            clauses = tuple(base_clauses) + tuple((unit,) for unit in units)
            stem = f"sample_{sample_position:02d}_pair_{pair_index}"
            formula_path = temporary_root / f"{stem}.cnf"
            proof_path = temporary_root / f"{stem}.drat"
            lrat_path = temporary_root / f"{stem}.lrat"
            write_dimacs(formula_path, variable_count, clauses)
            formula_sha256 = sha256_file(formula_path)

            solve_started = time.monotonic()
            with Glucose3(
                bootstrap_with=clauses, with_proof=True, use_timer=True
            ) as solver:
                outcome = solver.solve()
                solver_cpu_seconds = solver.time_accum()
                stats = solver.accum_stats()
                proof = solver.get_proof() if outcome is False else None
            solve_seconds = time.monotonic() - solve_started
            if outcome is not False or proof is None:
                raise AssertionError(
                    f"sample {pair_index} did not solve UNSAT"
                )
            proof_sha256, proof_bytes = write_proof_atomic(proof_path, proof)

            drat_started = time.monotonic()
            drat = subprocess.run(
                [
                    str(paths["drat_trim"]),
                    str(formula_path),
                    str(proof_path),
                    "-I",
                    "-L",
                    str(lrat_path),
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=180,
            )
            drat_seconds = time.monotonic() - drat_started
            if (
                drat.returncode != 0
                or not checker_says_verified(drat.stdout + drat.stderr)
                or not lrat_path.is_file()
            ):
                raise AssertionError(f"DRAT check failed for sample {pair_index}")

            lrat_started = time.monotonic()
            lrat = subprocess.run(
                [
                    str(paths["lrat_check"]),
                    str(formula_path),
                    str(lrat_path),
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=180,
            )
            lrat_seconds = time.monotonic() - lrat_started
            if (
                lrat.returncode != 0
                or not checker_says_verified(lrat.stdout + lrat.stderr)
            ):
                raise AssertionError(f"LRAT check failed for sample {pair_index}")

            lrat_bytes = lrat_path.stat().st_size
            lrat_sha256 = sha256_file(lrat_path)
            proof_zstd = zstd_payload(
                proof_path, paths["zstd"], int(plan["zstd_level"])
            )
            lrat_zstd = zstd_payload(
                lrat_path, paths["zstd"], int(plan["zstd_level"])
            )
            records.append(
                {
                    "sample_position": sample_position,
                    "pair_index": pair_index,
                    "pair": list(pair),
                    "models": [
                        format(left_model, "030b"),
                        format(right_model, "030b"),
                    ],
                    "formula_sha256": formula_sha256,
                    "formula_bytes": formula_path.stat().st_size,
                    "formula_clause_count": len(clauses),
                    "unit_count": len(units),
                    "solver": "Glucose3",
                    "solver_status": "UNSAT",
                    "solver_cpu_seconds": solver_cpu_seconds,
                    "solver_wall_seconds": solve_seconds,
                    "solver_stats": stats,
                    "drat_record_count": len(proof),
                    "drat_sha256": proof_sha256,
                    "drat_bytes": proof_bytes,
                    "drat_zstd_bytes": len(proof_zstd),
                    "drat_zstd_sha256": sha256_bytes(proof_zstd),
                    "drat_trim_valid": True,
                    "drat_trim_seconds": drat_seconds,
                    "lrat_sha256": lrat_sha256,
                    "lrat_bytes": lrat_bytes,
                    "lrat_zstd_bytes": len(lrat_zstd),
                    "lrat_zstd_sha256": sha256_bytes(lrat_zstd),
                    "lrat_check_valid": True,
                    "lrat_check_seconds": lrat_seconds,
                }
            )
            formula_path.unlink()
            proof_path.unlink()
            lrat_path.unlink()
            if shutil.disk_usage(args.output.parent).free < reserve:
                raise RuntimeError("storage reserve breached during sample")
            print(
                json.dumps(
                    {
                        "event": "sample_complete",
                        "sample_position": sample_position,
                        "pair_index": pair_index,
                        "drat_zstd_bytes": len(proof_zstd),
                        "lrat_zstd_bytes": len(lrat_zstd),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

    def measurement(field: str) -> dict[str, float | int]:
        values = [int(record[field]) for record in records]
        return {
            "minimum": min(values),
            "median": statistics.median(values),
            "maximum": max(values),
            "mean": statistics.mean(values),
        }

    target_count = len(pair_schedule)
    combined_zstd = [
        int(record["drat_zstd_bytes"]) + int(record["lrat_zstd_bytes"])
        for record in records
    ]
    projection = {
        "target_pair_count": target_count,
        "drat_zstd_median_projection_bytes": int(
            statistics.median(
                int(record["drat_zstd_bytes"]) for record in records
            )
            * target_count
        ),
        "drat_zstd_max_projection_bytes": (
            max(int(record["drat_zstd_bytes"]) for record in records)
            * target_count
        ),
        "lrat_zstd_median_projection_bytes": int(
            statistics.median(
                int(record["lrat_zstd_bytes"]) for record in records
            )
            * target_count
        ),
        "lrat_zstd_max_projection_bytes": (
            max(int(record["lrat_zstd_bytes"]) for record in records)
            * target_count
        ),
        "combined_zstd_median_projection_bytes": int(
            statistics.median(combined_zstd) * target_count
        ),
        "combined_zstd_max_projection_bytes": max(combined_zstd)
        * target_count,
    }
    result = {
        "pipeline": PIPELINE,
        "evidence_label": "CERTIFIED STRATIFIED PROOF-SIZE SAMPLE",
        "claim_boundary": (
            "Every sampled pair is DRAT- and LRAT-certified UNSAT. The sample "
            "does not certify unsampled pairs; storage projections are "
            "engineering estimates, not proof artifacts."
        ),
        "plan_path": str(args.plan.resolve()),
        "plan_sha256": sha256_file(args.plan),
        "cnf_sha256": sha256_file(paths["cnf"]),
        "metadata_sha256": sha256_file(paths["metadata"]),
        "pysat_version": pysat.__version__,
        "storage_preflight_free_bytes": available,
        "storage_gate": storage,
        "setup_seconds": setup_seconds,
        "sample_count": len(records),
        "all_drat_valid": all(record["drat_trim_valid"] for record in records),
        "all_lrat_valid": all(record["lrat_check_valid"] for record in records),
        "records": records,
        "measurements": {
            "drat_bytes": measurement("drat_bytes"),
            "drat_zstd_bytes": measurement("drat_zstd_bytes"),
            "lrat_bytes": measurement("lrat_bytes"),
            "lrat_zstd_bytes": measurement("lrat_zstd_bytes"),
        },
        "projection": projection,
        "retained_proof_artifact_count": 0,
        "runtime_seconds": time.monotonic() - run_started,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    print(
        json.dumps(
            {key: value for key, value in result.items() if key != "records"},
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
