#!/usr/bin/env python3
"""Test selector-guarded cube-proof lifting on the twelve C7 samples.

For a side cube C and a fresh selector s, the wrapper formula contains

    s -> C,    C -> s.

Every addition D in a DRUP proof of B /\ C is replaced by D \/ -s.  The
terminal empty clause therefore becomes -s.  From -s and C -> s we derive
the ordinary blocking clause -C.  After deleting the temporary guarded
derivation, -s is rederived from -C and s -> C.  A selector cover clause then
closes a single streamed proof for the union of all sampled cubes.
"""

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

import automorphism7_side_orbit_cover as one_side  # noqa: E402
import automorphism7_side_pair_orbit_sweep as sweep  # noqa: E402
from residual_completion import checker_says_verified  # noqa: E402


PIPELINE = "ramsey55_automorphism7_pair_lifted_blocker_sample_v1"
BASE_VARIABLE_COUNT = 129
FIXED_UNIT_COUNT = 6
SIDE_UNIT_COUNT = 60


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def dimacs_bytes(
    variable_count: int, clauses: tuple[tuple[int, ...], ...]
) -> bytes:
    lines = [f"p cnf {variable_count} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode("ascii")


def write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


def proof_payload(records: list[str]) -> bytes:
    return "".join(record + "\n" for record in records).encode("ascii")


def parse_proof_record(record: str) -> tuple[bool, tuple[int, ...]]:
    fields = record.split()
    deletion = bool(fields and fields[0] == "d")
    if deletion:
        fields = fields[1:]
    if not fields or fields[-1] != "0":
        raise ValueError(f"malformed proof record: {record!r}")
    literals = tuple(map(int, fields[:-1]))
    if 0 in literals:
        raise ValueError("zero inside proof clause")
    return deletion, literals


def clause_record(clause: tuple[int, ...], deletion: bool = False) -> str:
    prefix = "d " if deletion else ""
    body = " ".join(map(str, clause))
    return f"{prefix}{body} 0" if body else f"{prefix}0"


def lift_proof_segment(
    proof: list[str],
    selector: int,
    blocker: tuple[int, ...],
) -> tuple[bytes, dict[str, object]]:
    """Return one self-cleaning lifted DRAT segment and its measurements."""

    original_additions: list[str] = []
    guarded: list[tuple[int, ...]] = []
    deletion_count = 0
    for record in proof:
        deletion, clause = parse_proof_record(record)
        if deletion:
            deletion_count += 1
            continue
        if any(abs(literal) == selector for literal in clause):
            raise ValueError("selector collision")
        original_additions.append(record)
        guarded.append(clause + (-selector,) if clause else (-selector,))
    if not guarded or guarded[-1] != (-selector,):
        raise ValueError("proof does not end in an empty-clause addition")

    records: list[str] = []
    records.extend(clause_record(clause) for clause in guarded)

    # The temporary -s and the reverse definition (s \/ -C) make -C RUP.
    records.append(clause_record(blocker))

    # Remove the temporary guarded derivation, including its first copy of
    # -s.  This prevents the final cover proof from bypassing the blocker.
    records.extend(clause_record(clause, deletion=True) for clause in guarded)

    # With blocker -C retained, assuming s propagates every literal of C and
    # falsifies -C, so -s is now RUP for a second, blocker-dependent reason.
    records.append(clause_record((-selector,)))
    payload = proof_payload(records)
    additions_payload = proof_payload(original_additions)
    return payload, {
        "raw_proof_record_count": len(proof),
        "raw_deletion_record_count": deletion_count,
        "raw_addition_record_count": len(original_additions),
        "original_additions_bytes": len(additions_payload),
        "original_additions_sha256": sha256_bytes(additions_payload),
        "guarded_addition_count": len(guarded),
        "segment_record_count": len(records),
        "segment_bytes": len(payload),
        "segment_sha256": sha256_bytes(payload),
        "temporary_guarded_clauses_deleted": len(guarded),
        "blocker_derived": True,
        "selector_rederived_from_blocker": True,
    }


def validate_pin(record: object, path: Path, label: str) -> None:
    if (
        not isinstance(record, dict)
        or Path(str(record.get("path", ""))).resolve() != path.resolve()
        or record.get("sha256") != sha256_file(path)
    ):
        raise ValueError(f"pin mismatch: {label}")


def fixed_and_side_maps(
    metadata: dict[str, object],
    edge_orbits: tuple[tuple[tuple[int, int], ...], ...],
) -> tuple[list[int], list[int], list[int]]:
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
    if (
        len(fixed_units) != FIXED_UNIT_COUNT
        or len(map_a) != 30
        or len(map_b) != 30
        or len(set(map(abs, fixed_units + map_a + map_b))) != 66
    ):
        raise AssertionError("unexpected fixed/side variable partition")
    return fixed_units, map_a, map_b


def side_units(
    left_model: int,
    right_model: int,
    map_a: list[int],
    map_b: list[int],
) -> tuple[int, ...]:
    units = [
        variable if left_model >> index & 1 else -variable
        for index, variable in enumerate(map_a)
    ]
    units.extend(
        -variable if right_model >> index & 1 else variable
        for index, variable in enumerate(map_b)
    )
    if len(units) != SIDE_UNIT_COUNT or len(set(map(abs, units))) != 60:
        raise AssertionError("malformed side cube")
    return tuple(units)


def wrapper_clauses(
    base_clauses: tuple[tuple[int, ...], ...],
    fixed_units: list[int],
    samples: list[dict[str, Any]],
) -> tuple[tuple[int, ...], ...]:
    clauses = list(base_clauses)
    clauses.extend((unit,) for unit in fixed_units)
    selectors: list[int] = []
    for sample in samples:
        selector = int(sample["selector"])
        cube = tuple(int(literal) for literal in sample["side_units"])
        blocker = tuple(-literal for literal in cube)
        selectors.append(selector)
        clauses.extend((-selector, literal) for literal in cube)
        clauses.append((selector, *blocker))
    clauses.append(tuple(selectors))
    return tuple(clauses)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if (
        not isinstance(plan, dict)
        or plan.get("schema")
        != "ramsey55.automorphism7_pair_lifted_blocker_sample_plan.v1"
        or plan.get("status") != "PREREGISTERED"
    ):
        raise SystemExit("invalid plan")
    if Path(str(plan.get("result", ""))).resolve() != args.result.resolve():
        raise SystemExit("result path mismatch")

    paths = {
        "cnf": ROOT / str(plan["cnf"]["path"]),
        "metadata": ROOT / str(plan["metadata"]["path"]),
        "source_sample_plan": ROOT / str(plan["source_sample_plan"]["path"]),
        "source_sample_result": ROOT / str(plan["source_sample_result"]["path"]),
        "pair_audit": ROOT / str(plan["pair_audit"]["path"]),
        "runner": Path(__file__).resolve(),
        "checker": ROOT / str(plan["checker"]["path"]),
        "tests": ROOT / str(plan["tests"]["path"]),
        "drat_trim": Path(str(plan["drat_trim"]["path"])),
        "lrat_check": Path(str(plan["lrat_check"]["path"])),
        "zstd": Path(str(plan["zstd"]["path"])),
        "pysat": Path(str(plan["pysat"]["path"])),
    }
    for label, path in paths.items():
        validate_pin(plan[label], path, label)
    if plan.get("pysat_version") != pysat.__version__:
        raise SystemExit("PySAT version mismatch")

    outputs = {
        name: ROOT / str(relative)
        for name, relative in plan["outputs"].items()
    }
    if outputs["result"].resolve() != args.result.resolve():
        raise SystemExit("output result mismatch")
    if any(path.exists() for path in outputs.values()):
        raise SystemExit("refusing to overwrite an output")

    gate = plan["storage_gate"]
    required = (
        int(gate["maximum_transient_bytes"])
        + int(gate["maximum_retained_bytes"])
        + int(gate["minimum_free_bytes_after_completion"])
    )
    if required != int(gate["required_prelaunch_free_bytes"]):
        raise SystemExit("invalid storage gate")
    args.result.parent.mkdir(parents=True, exist_ok=True)
    available = shutil.disk_usage(args.result.parent).free
    if available < required:
        raise SystemExit(f"storage gate failed: {available} < {required}")

    source_plan = json.loads(
        paths["source_sample_plan"].read_text(encoding="utf-8")
    )
    source_result = json.loads(
        paths["source_sample_result"].read_text(encoding="utf-8")
    )
    source_records = {
        int(record["pair_index"]): record for record in source_result["records"]
    }
    selected = source_plan["samples"]
    if len(selected) != 12 or len(source_records) != 12:
        raise SystemExit("expected the existing twelve-sample set")

    setup_started = time.monotonic()
    edge_orbits, class_representatives, pair_schedule = (
        sweep.build_pair_schedule()
    )
    variable_count, base_clauses = one_side.parse_dimacs(paths["cnf"])
    metadata = json.loads(paths["metadata"].read_text(encoding="utf-8"))
    if variable_count != BASE_VARIABLE_COUNT or not isinstance(metadata, dict):
        raise ValueError("unexpected base formula")
    fixed_units, map_a, map_b = fixed_and_side_maps(metadata, edge_orbits)

    sample_data: list[dict[str, Any]] = []
    for position, sample in enumerate(selected):
        pair_index = int(sample["pair_index"])
        pair = pair_schedule[pair_index]
        if list(pair) != sample["pair"]:
            raise AssertionError("pair schedule mismatch")
        left_model = class_representatives[pair[0]]
        right_model = class_representatives[pair[1]]
        if [
            format(left_model, "030b"),
            format(right_model, "030b"),
        ] != sample["models"]:
            raise AssertionError("sample model mismatch")
        cube = side_units(left_model, right_model, map_a, map_b)
        sample_data.append(
            {
                "sample_position": position,
                "pair_index": pair_index,
                "pair": list(pair),
                "models": list(sample["models"]),
                "selector": BASE_VARIABLE_COUNT + position + 1,
                "side_units": list(cube),
                "blocker": [-literal for literal in cube],
            }
        )

    wrapper = wrapper_clauses(base_clauses, fixed_units, sample_data)
    wrapper_variable_count = BASE_VARIABLE_COUNT + len(sample_data)
    wrapper_payload = dimacs_bytes(wrapper_variable_count, wrapper)
    write_bytes(outputs["wrapper_cnf"], wrapper_payload)

    outputs["lifted_drat"].parent.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    run_started = time.monotonic()
    with outputs["lifted_drat"].open("wb") as proof_stream:
        for sample in sample_data:
            pair_index = int(sample["pair_index"])
            side_cube = tuple(int(literal) for literal in sample["side_units"])
            cube_units = tuple(fixed_units) + side_cube
            cube_formula = tuple(base_clauses) + tuple(
                (unit,) for unit in cube_units
            )
            formula_payload = dimacs_bytes(variable_count, cube_formula)
            source_record = source_records[pair_index]
            if (
                sha256_bytes(formula_payload) != source_record["formula_sha256"]
                or len(formula_payload) != source_record["formula_bytes"]
            ):
                raise AssertionError("cube formula differs from source sample")

            solve_started = time.monotonic()
            with Glucose3(
                bootstrap_with=cube_formula, with_proof=True, use_timer=True
            ) as solver:
                outcome = solver.solve()
                solver_cpu_seconds = solver.time_accum()
                solver_stats = solver.accum_stats()
                raw_proof = solver.get_proof() if outcome is False else None
            solver_wall_seconds = time.monotonic() - solve_started
            if outcome is not False or raw_proof is None:
                raise AssertionError(f"sample {pair_index} was not UNSAT")
            raw_payload = proof_payload(raw_proof)
            if (
                sha256_bytes(raw_payload) != source_record["drat_sha256"]
                or len(raw_payload) != source_record["drat_bytes"]
                or len(raw_proof) != source_record["drat_record_count"]
            ):
                raise AssertionError("raw proof differs from source sample")

            segment, measurements = lift_proof_segment(
                raw_proof,
                int(sample["selector"]),
                tuple(int(literal) for literal in sample["blocker"]),
            )
            offset = proof_stream.tell()
            proof_stream.write(segment)
            proof_stream.flush()
            os.fsync(proof_stream.fileno())
            record = dict(sample)
            record.update(measurements)
            record.update(
                {
                    "segment_offset": offset,
                    "raw_proof_bytes": len(raw_payload),
                    "raw_proof_sha256": sha256_bytes(raw_payload),
                    "solver": "Glucose3",
                    "solver_status": "UNSAT",
                    "solver_cpu_seconds": solver_cpu_seconds,
                    "solver_wall_seconds": solver_wall_seconds,
                    "solver_stats": solver_stats,
                }
            )
            records.append(record)
            if shutil.disk_usage(args.result.parent).free < int(
                gate["minimum_free_bytes_after_completion"]
            ):
                raise RuntimeError("storage reserve breached")
            print(
                json.dumps(
                    {
                        "event": "sample_lifted",
                        "pair_index": pair_index,
                        "selector": sample["selector"],
                        "segment_bytes": len(segment),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
        proof_stream.write(b"0\n")
        proof_stream.flush()
        os.fsync(proof_stream.fileno())

    drat_started = time.monotonic()
    drat = subprocess.run(
        [
            str(paths["drat_trim"]),
            str(outputs["wrapper_cnf"]),
            str(outputs["lifted_drat"]),
            "-I",
            "-L",
            str(outputs["lifted_lrat"]),
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=int(plan["proof_check_timeout_seconds"]),
    )
    drat_seconds = time.monotonic() - drat_started
    drat_valid = (
        drat.returncode == 0
        and checker_says_verified(drat.stdout + drat.stderr)
        and outputs["lifted_lrat"].is_file()
    )
    if not drat_valid:
        raise AssertionError("lifted DRAT verification failed")

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
        lrat.returncode == 0
        and checker_says_verified(lrat.stdout + lrat.stderr)
    )
    if not lrat_valid:
        raise AssertionError("lifted LRAT verification failed")

    for artifact, output_name in (
        ("lifted_drat", "lifted_drat_zstd"),
        ("lifted_lrat", "lifted_lrat_zstd"),
    ):
        compressed = subprocess.run(
            [
                str(paths["zstd"]),
                f"-{int(plan['zstd_level'])}",
                "-q",
                "-f",
                str(outputs[artifact]),
                "-o",
                str(outputs[output_name]),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=300,
        )
        if compressed.returncode != 0:
            raise RuntimeError(f"zstd failed: {compressed.stderr}")

    segment_sizes = [int(record["segment_bytes"]) for record in records]
    result: dict[str, Any] = {
        "pipeline": PIPELINE,
        "status": "CERTIFIED_UNSAT_SAMPLE_UNION",
        "evidence_label": "SELECTOR-GUARDED DRUP LIFTING, DRAT AND LRAT CHECKED",
        "claim_boundary": (
            "The wrapper asserts that at least one of the twelve sampled "
            "side-pair cubes holds.  Its UNSAT certificate validates the "
            "lifting transformation on those cubes only; it is not a proof "
            "for the other 37,182 representatives or for the global C7 "
            "branch."
        ),
        "sample_count": len(records),
        "target_pair_count": len(pair_schedule),
        "pair_schedule_sha256": sweep.EXPECTED_PAIR_SCHEDULE_SHA256,
        "base_formula": {
            "path": str(paths["cnf"].resolve()),
            "sha256": sha256_file(paths["cnf"]),
            "variable_count": variable_count,
            "clause_count": len(base_clauses),
        },
        "wrapper": {
            "path": str(outputs["wrapper_cnf"].resolve()),
            "sha256": sha256_file(outputs["wrapper_cnf"]),
            "bytes": outputs["wrapper_cnf"].stat().st_size,
            "variable_count": wrapper_variable_count,
            "clause_count": len(wrapper),
            "base_clause_count": len(base_clauses),
            "fixed_unit_count": len(fixed_units),
            "selector_definition_clause_count": 61 * len(records),
            "selector_cover_clause_count": 1,
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
            "drat_trim_stdout_sha256": sha256_bytes(
                drat.stdout.encode("utf-8")
            ),
            "drat_trim_stderr_sha256": sha256_bytes(
                drat.stderr.encode("utf-8")
            ),
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
            "lrat_check_stdout_sha256": sha256_bytes(
                lrat.stdout.encode("utf-8")
            ),
            "lrat_check_stderr_sha256": sha256_bytes(
                lrat.stderr.encode("utf-8")
            ),
        },
        "records": records,
        "measurements": {
            "segment_bytes_sum": sum(segment_sizes),
            "segment_bytes_minimum": min(segment_sizes),
            "segment_bytes_maximum": max(segment_sizes),
            "segment_bytes_mean": sum(segment_sizes) / len(segment_sizes),
            "raw_drat_bytes_sum": sum(
                int(record["raw_proof_bytes"]) for record in records
            ),
            "raw_deletion_records_removed": sum(
                int(record["raw_deletion_record_count"]) for record in records
            ),
            "raw_addition_records_lifted": sum(
                int(record["raw_addition_record_count"]) for record in records
            ),
        },
        "setup_seconds": run_started - setup_started,
        "run_seconds": time.monotonic() - run_started,
        "plan": {
            "path": str(args.plan.resolve()),
            "sha256": sha256_file(args.plan),
        },
        "source_sample_result": {
            "path": str(paths["source_sample_result"].resolve()),
            "sha256": sha256_file(paths["source_sample_result"]),
        },
        "all_source_proof_hashes_matched": True,
        "all_blockers_derived": True,
        "all_selectors_rederived_from_blockers": True,
        "drat_trim_valid": drat_valid,
        "lrat_check_valid": lrat_valid,
    }
    retained_before_result = sum(
        path.stat().st_size
        for name, path in outputs.items()
        if name != "result"
    )
    result["storage"] = {
        "prelaunch_free_bytes": available,
        "retained_bytes_before_result": retained_before_result,
        "maximum_retained_bytes": int(gate["maximum_retained_bytes"]),
        "minimum_free_bytes_after_completion": int(
            gate["minimum_free_bytes_after_completion"]
        ),
    }
    result_payload = (
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    if (
        retained_before_result + len(result_payload)
        > int(gate["maximum_retained_bytes"])
    ):
        raise RuntimeError("outputs breach retained-artifact gate")
    write_bytes(outputs["result"], result_payload)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
