#!/usr/bin/env python3
"""Checkpointed MapleChrono certificates for 40 orientation-selector pairs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
BASE_CNF = ROOT / "certificates" / "order43_automorphism5_eight_cycles.cnf"
SELECTOR_GENERATOR = ROOT / "src" / "automorphism5_selector_cover_cnf.py"
WORKER = ROOT / "src" / "global_proof_worker.py"
CHECKER = ROOT / "verify" / "automorphism5_orientation_pair_bundle_check.py"
STRUCTURAL_CHECKER = ROOT / "verify" / "automorphism5_selector_cover_check.py"
TESTS = ROOT / "tests" / "automorphism5_orientation_pair_bundle_tests.py"
PLAN = (
    ROOT
    / "results"
    / "benchmark_plans"
    / "automorphism5_orientation_pair40_v1.json"
)
OUTPUT = (
    ROOT
    / "certificates"
    / "order43_automorphism5_orientation_pairs40"
)
SUMMARY = (
    ROOT
    / "results"
    / "global_exact"
    / "automorphism5_orientation_pair40_v1.json"
)

PYTHON = Path("/opt/homebrew/opt/python@3.11/bin/python3.11")
PYSAT_PATH = Path("/tmp/ramsey55-pysat.4YSXId")
DRAT_TRIM = Path("/tmp/ramsey55-drat-trim.x3nb3p/src/drat-trim")
LRAT_CHECK = Path("/tmp/ramsey55-drat-trim.x3nb3p/src/lrat-check")
ZSTD = Path("/opt/homebrew/bin/zstd")

PINNED_HASHES = {
    "python": "831365631dac62f232a720858703d0b2ddca5eed33e0a51986cf06aac9d38bc0",
    "pysat_solvers_py": "253654d8efabae650a0d136ad2f2e6d30b57206b1fb70846c714197468a28f7e",
    "pysolvers_extension": "e9828032a114da49429305e5afcf58db259034687a9c098c996da65e5e099ded",
    "drat_trim": "f58f63b0f76945d4c4c9ff6e87afaf870f579e67c0f7cca589492df8fc7ebd47",
    "lrat_check": "bd7eb8052623525814a0a37502b47f05375d9d9dfaf96ddc2fcd858958517cea",
    "zstd": "aff8169fb421bb925fb16c44a7e0143fa2c7a941dc45cce76b15062a2ce54917",
}

PLAN_ID = "ramsey55_order5_orientation_pair40_plan_v1"
RESULT_ID = "ramsey55_order5_orientation_pair_result_v1"
WORKFLOW_ID = "ramsey55_order5_orientation_pair40_bundle_v1"
BASE_SHA256 = "8abb891e769995940c06f403bb261b8d4e4c7c5d03749b7a13ca445182c4b7c6"
CONFLICT_BUDGET = 5_000_000
SOLVER_TIMEOUT_SECONDS = 420
CHECK_TIMEOUT_SECONDS = 600
MAX_ARTIFACT_BYTES = 2_000_000_000
MAX_TRANSIENT_BYTES = 1_000_000_000
RESERVE_BYTES = 4_294_967_296


class BundleError(RuntimeError):
    """A frozen workflow invariant failed."""


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def atomic_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=path.name + ".",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary = stream.name
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


def tool_paths() -> dict[str, Path]:
    extensions = sorted(PYSAT_PATH.glob("pysolvers*.so"))
    if len(extensions) != 1:
        raise BundleError("pinned PySAT extension is unavailable")
    return {
        "python": PYTHON,
        "pysat_solvers_py": PYSAT_PATH / "pysat" / "solvers.py",
        "pysolvers_extension": extensions[0],
        "drat_trim": DRAT_TRIM,
        "lrat_check": LRAT_CHECK,
        "zstd": ZSTD,
    }


def pinned_files(paths: Mapping[str, Path]) -> dict[str, object]:
    result: dict[str, object] = {}
    for name, expected in PINNED_HASHES.items():
        path = paths[name]
        if not path.is_file() or sha256_file(path) != expected:
            raise BundleError(f"pinned tool changed: {name}")
        result[name] = {
            "path": str(path.resolve()),
            "sha256": expected,
            "bytes": path.stat().st_size,
        }
    return result


def source_files() -> dict[str, Path]:
    return {
        "bundle": Path(__file__).resolve(),
        "selector_generator": SELECTOR_GENERATOR,
        "solver_worker": WORKER,
        "bundle_checker": CHECKER,
        "structural_checker": STRUCTURAL_CHECKER,
        "tests": TESTS,
    }


def run(
    command: Sequence[str],
    *,
    environment: Mapping[str, str] | None = None,
    timeout: int | None = None,
    accepted: set[int] = {0},
) -> tuple[subprocess.CompletedProcess[str], float]:
    started = time.monotonic()
    completed = subprocess.run(
        list(command),
        text=True,
        capture_output=True,
        check=False,
        env=dict(environment) if environment is not None else None,
        timeout=timeout,
    )
    elapsed = time.monotonic() - started
    if completed.returncode not in accepted:
        raise BundleError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"{completed.stdout[-3000:]}\n{completed.stderr[-3000:]}"
        )
    return completed, elapsed


def batch_id(start: int, count: int = 2) -> str:
    return f"pair_{start:03d}_{start + count - 1:03d}"


def generate_formula(
    directory: Path, start: int, count: int = 2
) -> tuple[Path, Path, dict[str, object]]:
    directory.mkdir(parents=True, exist_ok=True)
    cnf = directory / "formula.cnf"
    metadata_path = directory / "formula.metadata.json"
    run(
        (
            str(sys.executable),
            str(SELECTOR_GENERATOR),
            "--base-cnf",
            str(BASE_CNF),
            "--portion",
            "orientations",
            "--batch-start",
            str(start),
            "--batch-count",
            str(count),
            "--selectors-first",
            "--cnf",
            str(cnf),
            "--metadata",
            str(metadata_path),
        )
    )
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    return cnf, metadata_path, metadata


def prepare_plan() -> dict[str, object]:
    if sha256_file(BASE_CNF) != BASE_SHA256:
        raise BundleError("order-5 base CNF changed")
    sources = {}
    for name, path in source_files().items():
        if not path.is_file():
            raise BundleError(f"missing source: {path}")
        sources[name] = {
            "path": str(path.resolve()),
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }
    batches = []
    with tempfile.TemporaryDirectory(prefix="r55-aut5-pair-plan-") as raw:
        temporary = Path(raw)
        for start in range(0, 80, 2):
            cnf, _, metadata = generate_formula(
                temporary / batch_id(start), start
            )
            batches.append(
                {
                    "id": batch_id(start),
                    "start": start,
                    "count": 2,
                    "orientation_indices": [start, start + 1],
                    "orientations": [
                        leaf["internal_orientation"]
                        for leaf in metadata["leaves"]
                    ],
                    "formula_variable_count": metadata["variable_count"],
                    "formula_clause_count": metadata["clause_count"],
                    "formula_sha256": sha256_file(cnf),
                    "formula_bytes": cnf.stat().st_size,
                    "appended_clause_stream_sha256": metadata[
                        "appended_clause_stream_sha256"
                    ],
                }
            )
    required = MAX_ARTIFACT_BYTES + MAX_TRANSIENT_BYTES + RESERVE_BYTES
    return {
        "plan": PLAN_ID,
        "claim_scope": (
            "Exact pairwise selector cover of all 80 internal-orientation "
            "representatives for the one-edge all-ones normalized 5^8 1^3 "
            "type."
        ),
        "base_cnf": {
            "path": str(BASE_CNF.resolve()),
            "sha256": BASE_SHA256,
            "bytes": BASE_CNF.stat().st_size,
        },
        "batch_count": len(batches),
        "orientation_representative_count": 80,
        "batch_size": 2,
        "batches": batches,
        "solver": {
            "name": "MapleChrono",
            "conflict_budget_per_batch": CONFLICT_BUDGET,
            "wall_clock_timeout_seconds": SOLVER_TIMEOUT_SECONDS,
            "pysat_version": "1.9.dev7",
        },
        "proof_checks": {
            "timeout_seconds": CHECK_TIMEOUT_SECONDS,
            "drat_trim_to_core_and_lrat": True,
            "core_drat_rechecked": True,
            "lrat_rechecked": True,
        },
        "compression": {
            "program": "zstd",
            "level": 9,
            "threads": 1,
            "archives_tested_and_stream_hash_replayed": True,
        },
        "storage_gate": {
            "maximum_artifact_bytes": MAX_ARTIFACT_BYTES,
            "maximum_transient_bytes": MAX_TRANSIENT_BYTES,
            "minimum_free_reserve_bytes": RESERVE_BYTES,
            "required_prelaunch_free_bytes": required,
        },
        "tools": pinned_files(tool_paths()),
        "pysat_path": str(PYSAT_PATH.resolve()),
        "sources": sources,
        "output_directory": str(OUTPUT.resolve()),
    }


def validate_plan(plan: Mapping[str, object]) -> None:
    if plan.get("plan") != PLAN_ID:
        raise BundleError("unexpected plan identifier")
    if sha256_file(BASE_CNF) != BASE_SHA256:
        raise BundleError("base CNF changed")
    sources = plan.get("sources")
    if not isinstance(sources, dict):
        raise BundleError("plan source pins are missing")
    for name, path in source_files().items():
        record = sources.get(name)
        if (
            not isinstance(record, dict)
            or record.get("sha256") != sha256_file(path)
            or record.get("bytes") != path.stat().st_size
        ):
            raise BundleError(f"source changed after plan: {name}")
    pinned_files(tool_paths())
    batches = plan.get("batches")
    if not isinstance(batches, list) or len(batches) != 40:
        raise BundleError("plan does not contain 40 pairs")
    indices = [
        int(index)
        for batch in batches
        for index in batch["orientation_indices"]
    ]
    if indices != list(range(80)):
        raise BundleError("pair schedule is not an exact ordered cover")


def artifact_bytes() -> int:
    if not OUTPUT.exists():
        return 0
    return sum(
        path.stat().st_size
        for path in OUTPUT.iterdir()
        if path.is_file()
    )


def storage_check(plan: Mapping[str, object], prelaunch: bool) -> dict[str, int]:
    gate = plan["storage_gate"]
    assert isinstance(gate, dict)
    used = artifact_bytes()
    maximum = int(gate["maximum_artifact_bytes"])
    transient = int(gate["maximum_transient_bytes"])
    reserve = int(gate["minimum_free_reserve_bytes"])
    available = shutil.disk_usage(ROOT).free
    required = (
        int(gate["required_prelaunch_free_bytes"])
        if prelaunch
        else maximum - used + transient + reserve
    )
    if used > maximum or available < required:
        raise BundleError(
            f"storage gate failed: used={used}, free={available}, "
            f"required={required}"
        )
    return {
        "stored_artifact_bytes": used,
        "available_bytes": available,
        "required_bytes": required,
    }


def says_verified(output: str) -> bool:
    return any(
        "VERIFIED" in line and "NOT VERIFIED" not in line
        for line in output.splitlines()
    )


def compress(source: Path, target: Path) -> None:
    temporary = target.with_name(target.name + ".tmp")
    temporary.unlink(missing_ok=True)
    try:
        run(
            (
                str(ZSTD),
                "-9",
                "-T1",
                "-q",
                "-f",
                str(source),
                "-o",
                str(temporary),
            ),
            timeout=CHECK_TIMEOUT_SECONDS,
        )
        run((str(ZSTD), "-t", "-q", str(temporary)))
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def decompressed_digest(path: Path) -> tuple[str, int]:
    process = subprocess.Popen(
        (str(ZSTD), "-d", "-c", "-q", str(path)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdout is not None
    state = hashlib.sha256()
    byte_count = 0
    for block in iter(lambda: process.stdout.read(1 << 20), b""):
        state.update(block)
        byte_count += len(block)
    stderr = process.stderr.read() if process.stderr is not None else b""
    returncode = process.wait()
    if returncode != 0:
        raise BundleError(stderr.decode(errors="replace"))
    return state.hexdigest(), byte_count


def paths(identifier: str) -> dict[str, Path]:
    return {
        "metadata": OUTPUT / f"{identifier}.metadata.json",
        "result": OUTPUT / f"{identifier}.result.json",
        "drat": OUTPUT / f"{identifier}.drat.zst",
        "lrat": OUTPUT / f"{identifier}.lrat.zst",
    }


def completed_valid(
    expected: Mapping[str, object],
) -> dict[str, object] | None:
    artifact = paths(str(expected["id"]))
    if not all(path.is_file() for path in artifact.values()):
        return None
    try:
        result = json.loads(artifact["result"].read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    if (
        result.get("result") != RESULT_ID
        or result.get("status") != "CERTIFIED_UNSAT"
        or result.get("formula_sha256") != expected["formula_sha256"]
        or result.get("orientation_indices") != expected["orientation_indices"]
    ):
        return None
    for kind in ("drat", "lrat"):
        record = result.get(f"{kind}_zstd")
        if (
            not isinstance(record, dict)
            or record.get("sha256") != sha256_file(artifact[kind])
            or record.get("bytes") != artifact[kind].stat().st_size
        ):
            return None
    return result


def summary_payload(
    plan: Mapping[str, object],
    records: Sequence[Mapping[str, object]],
    started: float,
    preflight: Mapping[str, int],
) -> dict[str, object]:
    counts = Counter(str(record.get("status")) for record in records)
    covered = sorted(
        int(index)
        for record in records
        if record.get("status") == "CERTIFIED_UNSAT"
        for index in record["orientation_indices"]
    )
    return {
        "workflow": WORKFLOW_ID,
        "status": (
            "CERTIFIED_UNSAT"
            if covered == list(range(80))
            else "IN_PROGRESS"
        ),
        "claim_scope": (
            "The exact 80-representative internal-orientation cover of the "
            "one-edge all-ones normalized order-5 type only."
        ),
        "plan_path": str(PLAN.resolve()),
        "plan_sha256": sha256_file(PLAN),
        "scheduled_batch_count": 40,
        "completed_record_count": len(records),
        "status_counts": dict(sorted(counts.items())),
        "certified_orientation_indices": covered,
        "all_orientations_certified_unsat": covered == list(range(80)),
        "storage_preflight": dict(preflight),
        "stored_artifact_bytes": artifact_bytes(),
        "records": list(records),
        "runtime_seconds": time.monotonic() - started,
    }


def run_bundle(plan: Mapping[str, object]) -> int:
    validate_plan(plan)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    work_root = OUTPUT / ".work"
    work_root.mkdir(exist_ok=True)
    preflight = storage_check(plan, prelaunch=True)
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONPATH": str(PYSAT_PATH),
            "PYTHONHASHSEED": "0",
            "LC_ALL": "C",
        }
    )
    records: list[dict[str, object]] = []
    started = time.monotonic()
    batches = plan["batches"]
    assert isinstance(batches, list)
    for expected in batches:
        assert isinstance(expected, dict)
        resumed = completed_valid(expected)
        if resumed is not None:
            records.append(resumed)
            print(
                json.dumps(
                    {
                        "event": "batch_resumed",
                        "id": expected["id"],
                        "completed": len(records),
                        "scheduled": 40,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            continue
        storage_check(plan, prelaunch=False)
        identifier = str(expected["id"])
        work = work_root / identifier
        if work.exists():
            shutil.rmtree(work)
        work.mkdir()
        cnf, metadata_path, metadata = generate_formula(
            work, int(expected["start"]), int(expected["count"])
        )
        if (
            sha256_file(cnf) != expected["formula_sha256"]
            or cnf.stat().st_size != expected["formula_bytes"]
            or metadata.get("leaves") is None
            or [
                leaf["internal_orientation"] for leaf in metadata["leaves"]
            ]
            != expected["orientations"]
        ):
            raise BundleError(f"formula changed for {identifier}")
        shutil.copyfile(metadata_path, paths(identifier)["metadata"])
        raw_drat = work / "raw.drat"
        core_drat = work / "core.drat"
        lrat = work / "proof.lrat"
        worker_result_path = work / "worker.json"
        print(
            json.dumps(
                {
                    "event": "batch_started",
                    "id": identifier,
                    "completed": len(records),
                    "scheduled": 40,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        try:
            worker_process, solver_wall = run(
                (
                    str(PYTHON),
                    str(WORKER),
                    str(cnf),
                    "--solver",
                    "MapleChrono",
                    "--proof",
                    str(raw_drat),
                    "--conflict-budget",
                    str(CONFLICT_BUDGET),
                    "--output",
                    str(worker_result_path),
                ),
                environment=environment,
                timeout=SOLVER_TIMEOUT_SECONDS,
                accepted={2, 10, 20},
            )
        except subprocess.TimeoutExpired:
            result = {
                "result": RESULT_ID,
                "status": "TIMEOUT",
                "id": identifier,
                "orientation_indices": expected["orientation_indices"],
                "formula_sha256": expected["formula_sha256"],
                "wall_clock_timeout_seconds": SOLVER_TIMEOUT_SECONDS,
                "negative_certified": False,
            }
            atomic_json(paths(identifier)["result"], result)
            records.append(result)
            atomic_json(
                SUMMARY,
                summary_payload(plan, records, started, preflight),
            )
            shutil.rmtree(work)
            return 2
        worker = json.loads(worker_result_path.read_text(encoding="utf-8"))
        if worker_process.returncode != 20:
            result = {
                "result": RESULT_ID,
                "status": worker.get("status", "ERROR"),
                "id": identifier,
                "orientation_indices": expected["orientation_indices"],
                "formula_sha256": expected["formula_sha256"],
                "negative_certified": False,
                "solver_wall_seconds": solver_wall,
                "solver_result": worker,
            }
            atomic_json(paths(identifier)["result"], result)
            records.append(result)
            atomic_json(
                SUMMARY,
                summary_payload(plan, records, started, preflight),
            )
            shutil.rmtree(work)
            return worker_process.returncode
        if (
            worker.get("status") != "UNSAT"
            or worker.get("cnf_sha256") != expected["formula_sha256"]
            or worker.get("proof_sha256") != sha256_file(raw_drat)
        ):
            raise BundleError("worker result is not bound to formula/proof")

        converted, convert_wall = run(
            (
                str(DRAT_TRIM),
                str(cnf),
                str(raw_drat),
                "-I",
                "-l",
                str(core_drat),
                "-L",
                str(lrat),
            ),
            timeout=CHECK_TIMEOUT_SECONDS,
        )
        if not says_verified(converted.stdout + converted.stderr):
            raise BundleError("drat-trim rejected raw proof")
        core_checked, core_wall = run(
            (str(DRAT_TRIM), str(cnf), str(core_drat), "-I"),
            timeout=CHECK_TIMEOUT_SECONDS,
        )
        lrat_checked, lrat_wall = run(
            (str(LRAT_CHECK), str(cnf), str(lrat)),
            timeout=CHECK_TIMEOUT_SECONDS,
        )
        if not says_verified(core_checked.stdout + core_checked.stderr):
            raise BundleError("trimmed DRAT core failed recheck")
        if not says_verified(lrat_checked.stdout + lrat_checked.stderr):
            raise BundleError("LRAT failed recheck")

        raw_hash = sha256_file(raw_drat)
        core_hash, core_bytes = sha256_file(core_drat), core_drat.stat().st_size
        lrat_hash, lrat_bytes = sha256_file(lrat), lrat.stat().st_size
        artifact = paths(identifier)
        compress(core_drat, artifact["drat"])
        compress(lrat, artifact["lrat"])
        if decompressed_digest(artifact["drat"]) != (core_hash, core_bytes):
            raise BundleError("DRAT archive decompression mismatch")
        if decompressed_digest(artifact["lrat"]) != (lrat_hash, lrat_bytes):
            raise BundleError("LRAT archive decompression mismatch")
        result = {
            "result": RESULT_ID,
            "status": "CERTIFIED_UNSAT",
            "id": identifier,
            "orientation_indices": expected["orientation_indices"],
            "orientations": expected["orientations"],
            "formula_sha256": expected["formula_sha256"],
            "formula_bytes": expected["formula_bytes"],
            "formula_variable_count": expected["formula_variable_count"],
            "formula_clause_count": expected["formula_clause_count"],
            "solver": {
                "name": "MapleChrono",
                "conflict_budget": CONFLICT_BUDGET,
                "wall_clock_timeout_seconds": SOLVER_TIMEOUT_SECONDS,
            },
            "solver_wall_seconds": solver_wall,
            "solver_result": worker,
            "raw_drat": {
                "sha256": raw_hash,
                "bytes": raw_drat.stat().st_size,
            },
            "drat_trim_conversion_valid": True,
            "drat_trim_conversion_wall_seconds": convert_wall,
            "drat_core_check_valid": True,
            "drat_core_check_wall_seconds": core_wall,
            "lrat_check_valid": True,
            "lrat_check_wall_seconds": lrat_wall,
            "drat_uncompressed": {
                "sha256": core_hash,
                "bytes": core_bytes,
            },
            "drat_zstd": {
                "path": str(artifact["drat"].resolve()),
                "sha256": sha256_file(artifact["drat"]),
                "bytes": artifact["drat"].stat().st_size,
            },
            "lrat_uncompressed": {
                "sha256": lrat_hash,
                "bytes": lrat_bytes,
            },
            "lrat_zstd": {
                "path": str(artifact["lrat"].resolve()),
                "sha256": sha256_file(artifact["lrat"]),
                "bytes": artifact["lrat"].stat().st_size,
            },
        }
        atomic_json(artifact["result"], result)
        records.append(result)
        atomic_json(
            SUMMARY,
            summary_payload(plan, records, started, preflight),
        )
        shutil.rmtree(work)
        print(
            json.dumps(
                {
                    "event": "batch_certified",
                    "id": identifier,
                    "completed": len(records),
                    "scheduled": 40,
                    "conflicts": worker.get("conflicts"),
                },
                sort_keys=True,
            ),
            flush=True,
        )
    final = summary_payload(plan, records, started, preflight)
    atomic_json(SUMMARY, final)
    return 20 if final["all_orientations_certified_unsat"] else 3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if args.prepare == args.run:
        parser.error("choose exactly one of --prepare or --run")
    if args.prepare:
        plan = prepare_plan()
        atomic_json(PLAN, plan)
        print(json.dumps(plan, sort_keys=True))
        return 0
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    return run_bundle(plan)


if __name__ == "__main__":
    raise SystemExit(main())
