#!/usr/bin/env python3
"""Proof-producing all-catalog screen for one-vertex extensions with E <= 2."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import itertools
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from residual_completion import (  # noqa: E402
    DEFAULT_DRAT_TRIM,
    DEFAULT_LRAT_CHECK,
    DEFAULT_PYSAT_PATH,
    DEFAULT_PYTHON,
    PINNED_HASHES,
    Toolchain,
    verify_toolchain,
)


BATCH_ID = "ramsey55_catalog42_e2_extension_proof_batch_v1"
WORKER_ID = "ramsey55_pysat_glucose3_proof_worker_v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def parse_one_json(text: str, label: str) -> dict[str, Any]:
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) != 1:
        raise RuntimeError(f"{label} did not emit exactly one JSON line")
    result = json.loads(lines[0])
    if not isinstance(result, dict):
        raise RuntimeError(f"{label} JSON is not an object")
    return result


def run(
    command: list[str],
    *,
    timeout: float,
    environment: dict[str, str] | None = None,
    allowed: set[int] = {0},
) -> subprocess.CompletedProcess[str]:
    try:
        completed = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
            env=environment,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f"command timed out: {command[0]}") from error
    if completed.returncode not in allowed:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"{completed.stderr}"
        )
    return completed


def decode_graph6(text: str) -> list[int]:
    order = ord(text[0]) - 63
    if order != 42:
        raise ValueError("expected short graph6 of order 42")
    adjacency = [0] * order
    bit = 0
    for right in range(1, order):
        for left in range(right):
            value = ord(text[1 + bit // 6]) - 63
            if not 0 <= value < 64:
                raise ValueError("invalid graph6 byte")
            if (value >> (5 - bit % 6)) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            bit += 1
    return adjacency


def check_primary_model(core_graph6: str, bits: str) -> dict[str, Any]:
    if len(bits) != 42 or set(bits) - {"0", "1"}:
        raise ValueError("primary model is not a 42-bit string")
    adjacency = decode_graph6(core_graph6) + [0]
    for vertex, bit in enumerate(bits):
        if bit == "1":
            adjacency[vertex] |= 1 << 42
            adjacency[42] |= 1 << vertex
    conflicts: list[dict[str, Any]] = []
    for vertices in itertools.combinations(range(43), 5):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        if edge_count == 10:
            conflicts.append({"colour": "clique", "vertices": list(vertices)})
        elif edge_count == 0:
            conflicts.append(
                {"colour": "independent", "vertices": list(vertices)}
            )
    return {
        "checker": "batch_independent_all_five_subset_model_check_v1",
        "valid": len(conflicts) <= 2,
        "bits": bits,
        "conflict_count": len(conflicts),
        "conflicts": conflicts,
        "edge_count": sum(row.bit_count() for row in adjacency) // 2,
        "degree_sequence": sorted(row.bit_count() for row in adjacency),
    }


def proof_verified(output: str) -> bool:
    return any(line.strip() == "s VERIFIED" for line in output.splitlines())


def solve_line(
    line_number: int,
    core_graph6: str,
    *,
    catalog: Path,
    proof_dir: Path,
    orchestrator_python: Path,
    generator: Path,
    checker: Path,
    worker: Path,
    toolchain: Toolchain,
    generate_timeout: float,
    solve_timeout: float,
    proof_timeout: float,
) -> dict[str, Any]:
    proof = proof_dir / f"line_{line_number:03d}.drat"
    if proof.exists():
        raise RuntimeError(f"proof path already exists: {proof}")
    with tempfile.TemporaryDirectory(
        prefix=f"ramsey55-catalog-e2-{line_number:03d}."
    ) as directory:
        temporary = Path(directory)
        cnf = temporary / "formula.cnf"
        metadata = temporary / "metadata.json"
        check_output = temporary / "check.json"
        generated = run(
            [
                str(orchestrator_python),
                str(generator),
                "--catalog",
                str(catalog),
                "--line",
                str(line_number),
                "--output",
                str(cnf),
                "--metadata",
                str(metadata),
            ],
            timeout=generate_timeout,
        )
        generator_result = parse_one_json(
            generated.stdout, f"generator line {line_number}"
        )
        checked = run(
            [
                str(orchestrator_python),
                str(checker),
                "--catalog",
                str(catalog),
                "--line",
                str(line_number),
                "--cnf",
                str(cnf),
                "--metadata",
                str(metadata),
                "--output",
                str(check_output),
            ],
            timeout=generate_timeout,
        )
        checker_result = parse_one_json(
            checked.stdout, f"checker line {line_number}"
        )
        cnf_sha256 = sha256_file(cnf)
        if (
            checker_result.get("valid") is not True
            or checker_result.get("catalog_line") != line_number
            or checker_result.get("cnf_sha256") != cnf_sha256
            or generator_result.get("cnf_sha256") != cnf_sha256
            or generator_result.get("core_graph6") != core_graph6
        ):
            raise RuntimeError(f"formula reconstruction failed on line {line_number}")

        environment = os.environ.copy()
        environment.update(
            {
                "PYTHONPATH": str(toolchain.pysat_path),
                "PYTHONHASHSEED": "0",
                "LC_ALL": "C",
            }
        )
        solved = run(
            [
                str(toolchain.python),
                str(worker),
                str(cnf),
                "--proof",
                str(proof),
            ],
            timeout=solve_timeout,
            environment=environment,
            allowed={10, 20},
        )
        solver_result = parse_one_json(
            solved.stdout, f"solver line {line_number}"
        )
        if (
            solver_result.get("worker") != WORKER_ID
            or solver_result.get("solver") != "Glucose3"
            or solver_result.get("cnf_sha256") != cnf_sha256
            or solver_result.get("variable_count")
            != checker_result.get("variable_count")
            or solver_result.get("clause_count")
            != checker_result.get("clause_count")
        ):
            raise RuntimeError(f"solver/formula mismatch on line {line_number}")

        common = {
            "catalog_line": line_number,
            "core_graph6": core_graph6,
            "cnf_sha256": cnf_sha256,
            "cnf_bytes": cnf.stat().st_size,
            "metadata_sha256": sha256_file(metadata),
            "structural_check_sha256": sha256_file(check_output),
            "structural_check_valid": True,
            "variable_count": checker_result["variable_count"],
            "clause_count": checker_result["clause_count"],
            "constraint_count": checker_result["constraint_count"],
            "clique_constraint_count": checker_result[
                "clique_constraint_count"
            ],
            "independent_constraint_count": checker_result[
                "independent_constraint_count"
            ],
            "solver_stats": {
                key: solver_result.get(key)
                for key in (
                    "runtime_seconds",
                    "solver_cpu_seconds",
                    "conflicts",
                    "decisions",
                    "propagations",
                    "restarts",
                )
            },
        }
        if solved.returncode == 10:
            if (
                solver_result.get("status") != "SAT"
                or solver_result.get("proof_written") is not False
                or proof.exists()
            ):
                raise RuntimeError(f"malformed SAT result on line {line_number}")
            true_variables = solver_result.get("true_variables")
            if not isinstance(true_variables, list):
                raise RuntimeError(f"SAT model missing on line {line_number}")
            true_set = set(int(value) for value in true_variables)
            bits = "".join(
                "1" if variable in true_set else "0"
                for variable in range(1, 43)
            )
            model_check = check_primary_model(core_graph6, bits)
            if model_check["valid"] is not True:
                raise RuntimeError(f"SAT graph check failed on line {line_number}")
            return {
                **common,
                "status": "SAT_MODEL_VERIFIED",
                "model": model_check,
                "proof": None,
            }

        if (
            solver_result.get("status") != "UNSAT"
            or solver_result.get("proof_written") is not True
            or not proof.is_file()
        ):
            raise RuntimeError(f"malformed UNSAT result on line {line_number}")
        proof_sha256 = sha256_file(proof)
        if (
            solver_result.get("proof_sha256") != proof_sha256
            or solver_result.get("proof_bytes") != proof.stat().st_size
        ):
            raise RuntimeError(f"proof fingerprint mismatch on line {line_number}")
        verified = run(
            [str(toolchain.drat_trim), str(cnf), str(proof)],
            timeout=proof_timeout,
        )
        transcript = verified.stdout + verified.stderr
        if not proof_verified(transcript):
            raise RuntimeError(f"DRAT verification failed on line {line_number}")
        if sha256_file(cnf) != cnf_sha256 or sha256_file(proof) != proof_sha256:
            raise RuntimeError(f"post-check hash changed on line {line_number}")
        return {
            **common,
            "status": "CERTIFIED_UNSAT",
            "model": None,
            "proof": {
                "path": str(proof),
                "bytes": proof.stat().st_size,
                "sha256": proof_sha256,
                "drat_trim_valid": True,
                "drat_trim_verified_line": "s VERIFIED",
            },
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--proof-dir", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--expected-count", type=int, default=328)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--generate-timeout", type=float, default=60)
    parser.add_argument("--solve-timeout", type=float, default=60)
    parser.add_argument("--proof-timeout", type=float, default=120)
    parser.add_argument("--python", type=Path, default=DEFAULT_PYTHON)
    parser.add_argument("--pysat-path", type=Path, default=DEFAULT_PYSAT_PATH)
    parser.add_argument("--drat-trim", type=Path, default=DEFAULT_DRAT_TRIM)
    parser.add_argument("--lrat-check", type=Path, default=DEFAULT_LRAT_CHECK)
    parser.add_argument(
        "--orchestrator-python", type=Path, default=Path(sys.executable)
    )
    parser.add_argument(
        "--generator",
        type=Path,
        default=ROOT / "src" / "catalog42_e2_extension_cnf.py",
    )
    parser.add_argument(
        "--checker",
        type=Path,
        default=ROOT / "verify" / "catalog42_e2_extension_cnf_check.py",
    )
    args = parser.parse_args()
    if (
        args.jobs < 1
        or args.generate_timeout <= 0
        or args.solve_timeout <= 0
        or args.proof_timeout <= 0
    ):
        parser.error("jobs and timeouts must be positive")
    if args.proof_dir.exists() and any(args.proof_dir.iterdir()):
        raise SystemExit("proof directory exists and is not empty")

    catalog_bytes = args.catalog.read_bytes()
    catalog_sha256 = hashlib.sha256(catalog_bytes).hexdigest()
    lines = [
        line.strip()
        for line in catalog_bytes.decode("ascii").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if (
        catalog_sha256 != args.expected_sha256
        or len(lines) != args.expected_count
        or len(set(lines)) != len(lines)
    ):
        raise SystemExit("catalog hash, count, or uniqueness check failed")
    args.proof_dir.mkdir(parents=True, exist_ok=True)

    toolchain = Toolchain(
        args.python,
        args.pysat_path,
        args.drat_trim,
        args.lrat_check,
        PINNED_HASHES,
    )
    tool_metadata = verify_toolchain(toolchain)
    worker = ROOT / "src" / "residual_completion_glucose.py"
    source_paths = {
        "batch": Path(__file__),
        "generator": args.generator,
        "generator_shared_definition": (
            ROOT / "src" / "catalog42_optimal_extension_certificate.py"
        ),
        "counter": ROOT / "src" / "direct_ramsey_cnf.py",
        "graph_io": ROOT / "src" / "graph_io.py",
        "checker": args.checker,
        "checker_helpers": (
            ROOT / "verify" / "catalog42_optimal_extension_check.py"
        ),
        "worker": worker,
        "orchestrator_python": args.orchestrator_python,
    }
    source_hashes = {
        key: sha256_file(path) for key, path in source_paths.items()
    }

    started = time.monotonic()
    records: list[dict[str, Any] | None] = [None] * len(lines)
    completed_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {
            executor.submit(
                solve_line,
                line_number,
                lines[line_number - 1],
                catalog=args.catalog,
                proof_dir=args.proof_dir,
                orchestrator_python=args.orchestrator_python,
                generator=args.generator,
                checker=args.checker,
                worker=worker,
                toolchain=toolchain,
                generate_timeout=args.generate_timeout,
                solve_timeout=args.solve_timeout,
                proof_timeout=args.proof_timeout,
            ): line_number
            for line_number in range(1, len(lines) + 1)
        }
        for future in concurrent.futures.as_completed(futures):
            line_number = futures[future]
            records[line_number - 1] = future.result()
            completed_count += 1
            if completed_count % 25 == 0 or completed_count == len(lines):
                sat_so_far = sum(
                    record is not None
                    and record["status"] == "SAT_MODEL_VERIFIED"
                    for record in records
                )
                print(
                    json.dumps(
                        {
                            "progress": completed_count,
                            "total": len(lines),
                            "sat_so_far": sat_so_far,
                            "wall_seconds": time.monotonic() - started,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )

    complete = [record for record in records if record is not None]
    if len(complete) != len(lines):
        raise RuntimeError("batch coverage is incomplete")
    sat_records = [
        record for record in complete if record["status"] == "SAT_MODEL_VERIFIED"
    ]
    unsat_records = [
        record for record in complete if record["status"] == "CERTIFIED_UNSAT"
    ]
    coverage = [record["catalog_line"] for record in complete]
    proof_stream = "".join(
        f"{record['catalog_line']} {record['cnf_sha256']} "
        f"{record['proof']['sha256']}\n"
        for record in unsat_records
    ).encode("ascii")
    result = {
        "batch": BATCH_ID,
        "status": "CERTIFIED_COMPLETE_CATALOG_E2_SCREEN",
        "claim_boundary": (
            "This classifies E<=2 one-vertex extensions only for the supplied "
            "328 labeled order-42 cores and, by complement symmetry, their "
            "328 complements. It is not a complete catalog of all order-42 "
            "Ramsey graphs or a global order-43 result."
        ),
        "catalog_path": str(args.catalog),
        "catalog_sha256": catalog_sha256,
        "catalog_graph_count": len(lines),
        "coverage_lines": coverage,
        "coverage_exact": coverage == list(range(1, len(lines) + 1)),
        "sat_count": len(sat_records),
        "certified_unsat_count": len(unsat_records),
        "sat_lines": [record["catalog_line"] for record in sat_records],
        "certified_unsat_lines": [
            record["catalog_line"] for record in unsat_records
        ],
        "proof_count": len(unsat_records),
        "proof_bytes_total": sum(
            record["proof"]["bytes"] for record in unsat_records
        ),
        "proof_bundle_sha256": hashlib.sha256(proof_stream).hexdigest(),
        "jobs": args.jobs,
        "timeouts_seconds": {
            "generate_and_check": args.generate_timeout,
            "solve": args.solve_timeout,
            "drat_check": args.proof_timeout,
        },
        "wall_seconds": time.monotonic() - started,
        "toolchain": tool_metadata,
        "source_paths": {key: str(path) for key, path in source_paths.items()},
        "source_sha256": source_hashes,
        "records": complete,
    }
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "batch": BATCH_ID,
                "status": result["status"],
                "sat_lines": result["sat_lines"],
                "certified_unsat_count": result["certified_unsat_count"],
                "proof_bytes_total": result["proof_bytes_total"],
                "wall_seconds": result["wall_seconds"],
                "result": str(args.result),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
