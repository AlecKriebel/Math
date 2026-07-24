#!/usr/bin/env python3
"""Freeze and execute the resume-safe two-representative triple screen."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import shutil
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
    parse_last_json,
    sha256_file,
)
from core_completion_k2 import completed_adjacency_k2  # noqa: E402
from e2_triple_replacement_compact import (  # noqa: E402
    HEADER_BYTES,
    RECORD_BYTES,
    TRIPLES,
    TRIPLES_PER_INPUT,
    validate_file,
)
from graph_io import (  # noqa: E402
    encode_graph6,
    read_graph,
    validate_simple,
    write_canonical_artifact,
)


RUN_ID = "ramsey55_e2_triple_replacement_screen_v1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def json_records(text: str) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            records.append(value)
    return records


def forbidden_sets(adjacency: list[int]) -> list[dict[str, object]]:
    import itertools

    result: list[dict[str, object]] = []
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        if edge_count in (0, 10):
            result.append(
                {
                    "colour": "clique" if edge_count == 10 else "independent",
                    "vertices": list(vertices),
                }
            )
    return result


def source_specs() -> list[dict[str, object]]:
    return [
        {
            "input_index": 1,
            "source_catalog_line": 42,
            "source_metadata": (
                "certificates/"
                "catalog42_line042_exact_e2_extensions.metadata.json"
            ),
            "source_model_index": 0,
            "representative": "clique-conflict complement class",
        },
        {
            "input_index": 2,
            "source_catalog_line": 256,
            "source_metadata": (
                "certificates/"
                "catalog42_line256_exact_e2_extensions.metadata.json"
            ),
            "source_model_index": 1,
            "representative": "independent-conflict complement class",
        },
    ]


def validate_sources(corpus: Path) -> list[dict[str, object]]:
    lines = [
        line.strip()
        for line in corpus.read_text(encoding="ascii").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if len(lines) != 2:
        raise ValueError("representative corpus must have two data lines")
    validated: list[dict[str, object]] = []
    for spec in source_specs():
        input_index = int(spec["input_index"])
        metadata_path = ROOT / str(spec["source_metadata"])
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        model_index = int(spec["source_model_index"])
        model = metadata["models"][model_index]
        if metadata.get("catalog_line") != spec["source_catalog_line"]:
            raise ValueError("source catalog line mismatch")
        if model.get("extension_cost") != 2:
            raise ValueError("selected source model is not E=2")
        if model.get("extended_graph6") != lines[input_index - 1]:
            raise ValueError("corpus line does not match certified metadata")
        adjacency = read_graph(corpus, input_index)
        conflicts = forbidden_sets(adjacency)
        if len(conflicts) != 2:
            raise ValueError("selected representative is not exact E=2")
        left = set(conflicts[0]["vertices"])
        right = set(conflicts[1]["vertices"])
        if len(left & right) != 4:
            raise ValueError("source conflicts do not overlap in four")
        validated.append(
            {
                **spec,
                "source_metadata_sha256": sha256_file(metadata_path),
                "graph6_sha256": __import__("hashlib")
                .sha256((lines[input_index - 1] + "\n").encode("ascii"))
                .hexdigest(),
                "graph6": lines[input_index - 1],
                "conflicts": conflicts,
            }
        )
    return validated


def immutable_files(
    *,
    solver: Path,
    corpus: Path,
    runner: Path,
    checker: Path,
    parser_source: Path,
    tests: Path,
    exhaustive: Path,
    bitset: Path,
) -> list[dict[str, str]]:
    paths = [
        corpus,
        solver,
        runner,
        checker,
        parser_source,
        ROOT / "src" / "e2_triple_replacement_solver.cpp",
        ROOT / "src" / "core_completion_k2_persistent_solver.cpp",
        ROOT / "src" / "core_completion_k2.py",
        ROOT / "src" / "graph_io.py",
        tests,
        exhaustive,
        bitset,
        ROOT
        / "certificates"
        / "catalog42_line042_exact_e2_extensions.metadata.json",
        ROOT
        / "certificates"
        / "catalog42_line256_exact_e2_extensions.metadata.json",
        ROOT
        / "certificates"
        / "catalog42_lines42_256_exact_e2_extensions.report.md",
        ROOT
        / "certificates"
        / "e2_near_miss_isomorphism_collapse_v1.report.md",
    ]
    return [
        {"path": relative(path), "sha256": sha256_file(path)}
        for path in paths
    ]


def make_plan(
    *,
    plan_path: Path,
    solver: Path,
    corpus: Path,
    output_dir: Path,
    checker: Path,
    parser_source: Path,
    tests: Path,
    exhaustive: Path,
    bitset: Path,
    shard_size: int,
    node_limit: int,
    seconds_limit: float,
    shard_timeout: float,
    output_byte_cap: int,
    reserve_bytes: int,
) -> dict[str, object]:
    if plan_path.exists():
        raise FileExistsError(f"refusing to overwrite frozen plan {plan_path}")
    if not 1 <= shard_size <= TRIPLES_PER_INPUT:
        raise ValueError("invalid shard size")
    sources = validate_sources(corpus)
    shards: list[dict[str, object]] = []
    shard_id = 0
    for input_index in (1, 2):
        for start in range(0, TRIPLES_PER_INPUT, shard_size):
            end = min(start + shard_size, TRIPLES_PER_INPUT)
            filename = (
                f"input_{input_index}_triples_{start:05d}_{end:05d}"
                ".e2t3rp"
            )
            shards.append(
                {
                    "shard": shard_id,
                    "input_index": input_index,
                    "triple_start": start,
                    "triple_end": end,
                    "record_count": end - start,
                    "record_bytes": (
                        HEADER_BYTES + (end - start) * RECORD_BYTES
                    ),
                    "filename": filename,
                }
            )
            shard_id += 1
    formula_samples: dict[str, list[int]] = {}
    for source in sources:
        input_index = int(source["input_index"])
        conflict_sets = [
            set(conflict["vertices"])
            for conflict in source["conflicts"]
        ]
        eligible = [
            ordinal
            for ordinal, triple in enumerate(TRIPLES)
            if all(set(triple) & conflict for conflict in conflict_sets)
        ]
        if len(eligible) != 3_239:
            raise ValueError("unexpected eligible triple count")
        formula_samples[str(input_index)] = [
            eligible[0],
            eligible[len(eligible) // 3],
            eligible[2 * len(eligible) // 3],
            eligible[-1],
        ]
    runner = Path(__file__).resolve()
    plan = {
        "schema": "ramsey55.e2_triple_replacement_plan.v1",
        "experiment": RUN_ID,
        "frozen_utc": utc_now(),
        "question": (
            "Does any graph obtained by deleting three vertices from either "
            "frozen E=2 complement-class representative and adding three "
            "unconstrained vertices give a (5,5;43)-graph?"
        ),
        "corpus": relative(corpus),
        "corpus_sha256": sha256_file(corpus),
        "inputs": sources,
        "input_count": 2,
        "triples_per_input": TRIPLES_PER_INPUT,
        "total_labeled_triples": 2 * TRIPLES_PER_INPUT,
        "expected_structural_obstructions": 18_204,
        "expected_solver_eligible": 6_478,
        "deduplication": False,
        "deduplication_policy": (
            "No isomorphism or automorphism deduplication is used; every "
            "labeled deletion triple is recorded."
        ),
        "formula": (
            "The exact 40-core/add-three homogeneous-five-set CNF from "
            "core_completion_k2_persistent_solver.cpp."
        ),
        "variables_per_solver_instance": 123,
        "node_limit_per_instance": node_limit,
        "seconds_limit_per_instance": seconds_limit,
        "shard_timeout_seconds": shard_timeout,
        "shard_size": shard_size,
        "shards": shards,
        "shard_count": len(shards),
        "expected_record_bytes": sum(
            int(shard["record_bytes"]) for shard in shards
        ),
        "output_directory": relative(output_dir),
        "output_byte_cap": output_byte_cap,
        "free_disk_reserve_bytes": reserve_bytes,
        "formula_reconstruction_ordinals": formula_samples,
        "solver": relative(solver),
        "runner": relative(runner),
        "coverage_checker": relative(checker),
        "compact_parser": relative(parser_source),
        "tests": relative(tests),
        "exhaustive_sat_verifier": relative(exhaustive),
        "bitset_sat_verifier": relative(bitset),
        "immutable_files": immutable_files(
            solver=solver,
            corpus=corpus,
            runner=runner,
            checker=checker,
            parser_source=parser_source,
            tests=tests,
            exhaustive=exhaustive,
            bitset=bitset,
        ),
        "sat_policy": (
            "Stop immediately, preserve model/graph6/canonical adjacency and "
            "edge artifact, and require both independent graph verifiers."
        ),
        "negative_policy": (
            "A retained fixed homogeneous five-set is an exact obstruction. "
            "DPLL UNSAT is retained only as an unchecked observation; no "
            "negative proof artifacts are generated."
        ),
        "claim_boundary": (
            "This is a finite two-input replacement screen, not a global "
            "order-43 nonexistence theorem and not a Ramsey-bound change."
        ),
    }
    atomic_json(plan_path, plan)
    return plan


def validate_plan(plan_path: Path) -> dict[str, object]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("schema") != "ramsey55.e2_triple_replacement_plan.v1":
        raise ValueError("unexpected plan schema")
    for record in plan.get("immutable_files", []):
        path = ROOT / str(record["path"])
        actual = sha256_file(path)
        if actual != record.get("sha256"):
            raise ValueError(
                f"immutable file changed: {record['path']} "
                f"{actual} != {record.get('sha256')}"
            )
    corpus = ROOT / str(plan["corpus"])
    if sha256_file(corpus) != plan.get("corpus_sha256"):
        raise ValueError("corpus changed after plan freeze")
    if len(plan.get("shards", [])) != plan.get("shard_count"):
        raise ValueError("shard count mismatch")
    cursors = {1: 0, 2: 0}
    for expected_id, shard in enumerate(plan["shards"]):
        if int(shard["shard"]) != expected_id:
            raise ValueError("nonsequential shard ID")
        input_index = int(shard["input_index"])
        start = int(shard["triple_start"])
        end = int(shard["triple_end"])
        if start != cursors[input_index] or not start < end:
            raise ValueError("noncontiguous shard range")
        if int(shard["record_count"]) != end - start:
            raise ValueError("shard record-count mismatch")
        if int(shard["record_bytes"]) != (
            HEADER_BYTES + (end - start) * RECORD_BYTES
        ):
            raise ValueError("shard byte-count mismatch")
        cursors[input_index] = end
    if cursors != {1: TRIPLES_PER_INPUT, 2: TRIPLES_PER_INPUT}:
        raise ValueError("plan does not cover both exact triple spaces")
    return plan


def induced_core_three(
    adjacency: list[int], deleted: tuple[int, int, int]
) -> tuple[list[int], tuple[int, ...]]:
    retained = tuple(v for v in range(43) if v not in deleted)
    core = [0] * 40
    for new_left, old_left in enumerate(retained):
        for new_right in range(new_left + 1, 40):
            old_right = retained[new_right]
            if (adjacency[old_left] >> old_right) & 1:
                core[new_left] |= 1 << new_right
                core[new_right] |= 1 << new_left
    validate_simple(core)
    return core, retained


def preserve_sat(
    *,
    solver_record: dict[str, object],
    plan_path: Path,
    plan_sha256: str,
    corpus: Path,
    output_dir: Path,
    exhaustive: Path,
    bitset: Path,
) -> dict[str, object]:
    input_index = int(solver_record["input_index"])
    ordinal = int(solver_record["triple_ordinal"])
    deleted_raw = solver_record.get("deleted_vertices")
    true_raw = solver_record.get("true_variables")
    if not isinstance(deleted_raw, list) or len(deleted_raw) != 3:
        raise ValueError("SAT record has no deletion triple")
    if not isinstance(true_raw, list):
        raise ValueError("SAT record has no true-variable list")
    deleted = tuple(int(value) for value in deleted_raw)
    if deleted != TRIPLES[ordinal]:
        raise ValueError("SAT deletion labels do not match ordinal")
    true_variables = sorted(int(value) for value in true_raw)
    if (
        len(true_variables) != len(set(true_variables))
        or any(not 0 <= value < 123 for value in true_variables)
    ):
        raise ValueError("SAT model contains invalid variables")
    source = read_graph(corpus, input_index)
    core, retained = induced_core_three(source, deleted)
    true_set = set(true_variables)
    completed = completed_adjacency_k2(
        core, [index in true_set for index in range(123)]
    )
    stem = (
        f"input_{input_index}_triple_{ordinal:05d}_delete_"
        f"{deleted[0]:02d}_{deleted[1]:02d}_{deleted[2]:02d}"
    )
    candidate_dir = output_dir / "sat_candidate" / stem
    model_path = candidate_dir / f"{stem}.model.json"
    graph6_path = candidate_dir / f"{stem}.g6"
    canonical_path = candidate_dir / f"{stem}.canonical.json"
    atomic_json(
        model_path,
        {
            "schema": "ramsey55.e2_triple_replacement_sat_model.v1",
            "run": RUN_ID,
            "preserved_utc": utc_now(),
            "plan": relative(plan_path),
            "plan_sha256": plan_sha256,
            "corpus": relative(corpus),
            "corpus_sha256": sha256_file(corpus),
            "input_index": input_index,
            "triple_ordinal": ordinal,
            "deleted_original_vertices": list(deleted),
            "retained_original_vertices": list(retained),
            "true_variables_zero_based": true_variables,
            "raw_solver_record": solver_record,
        },
    )
    atomic_write(
        graph6_path, (encode_graph6(completed) + "\n").encode("ascii")
    )
    canonical_sha256 = write_canonical_artifact(
        completed,
        canonical_path,
        provenance={
            "source": RUN_ID,
            "plan_sha256": plan_sha256,
            "corpus_sha256": sha256_file(corpus),
            "input_index": input_index,
            "triple_ordinal": ordinal,
            "deleted_original_vertices": list(deleted),
            "retained_original_vertices": list(retained),
            "model_sha256": sha256_file(model_path),
        },
    )
    exhaustive_run = subprocess.run(
        (sys.executable, str(exhaustive), str(graph6_path)),
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    bitset_run = subprocess.run(
        (str(bitset), str(graph6_path)),
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    exhaustive_result = parse_last_json(
        exhaustive_run.stdout, "exhaustive verifier"
    )
    bitset_result = parse_last_json(bitset_run.stdout, "bitset verifier")
    verified = (
        exhaustive_run.returncode == 0
        and exhaustive_result.get("valid") is True
        and bitset_run.returncode == 0
        and bitset_result.get("valid") is True
    )
    verification_path = candidate_dir / f"{stem}.verification.json"
    verification = {
        "schema": "ramsey55.e2_triple_replacement_sat_verification.v1",
        "verified": verified,
        "exhaustive_returncode": exhaustive_run.returncode,
        "exhaustive_stderr": exhaustive_run.stderr,
        "exhaustive_result": exhaustive_result,
        "bitset_returncode": bitset_run.returncode,
        "bitset_stderr": bitset_run.stderr,
        "bitset_result": bitset_result,
    }
    atomic_json(verification_path, verification)
    return {
        "classification": (
            "DUAL_VERIFIED_R55_43_CONSTRUCTION"
            if verified
            else "SAT_MODEL_VERIFICATION_FAILED"
        ),
        "verified": verified,
        "model": relative(model_path),
        "model_sha256": sha256_file(model_path),
        "graph6": relative(graph6_path),
        "graph6_sha256": sha256_file(graph6_path),
        "canonical_artifact": relative(canonical_path),
        "canonical_artifact_sha256": canonical_sha256,
        "verification": relative(verification_path),
        "verification_sha256": sha256_file(verification_path),
    }


def archive_partial(partial: Path, output_dir: Path) -> Path:
    diagnostics = output_dir / "diagnostics"
    diagnostics.mkdir(parents=True, exist_ok=True)
    destination = diagnostics / (
        f"{partial.name}.{time.time_ns()}.preserved"
    )
    os.replace(partial, destination)
    return destination


def run_screen(plan_path: Path) -> int:
    plan = validate_plan(plan_path)
    plan_sha256 = sha256_file(plan_path)
    corpus = ROOT / str(plan["corpus"])
    solver = ROOT / str(plan["solver"])
    checker = ROOT / str(plan["coverage_checker"])
    exhaustive = ROOT / str(plan["exhaustive_sat_verifier"])
    bitset = ROOT / str(plan["bitset_sat_verifier"])
    output_dir = ROOT / str(plan["output_directory"])
    shard_dir = output_dir / "shards"
    result_dir = output_dir / "shard_results"
    shard_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)
    lock_path = output_dir / ".run.lock"
    started = time.monotonic()
    reused_count = executed_count = 0
    with lock_path.open("a+b") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError("another replacement-screen run holds lock") from error
        for shard in plan["shards"]:
            shard_id = int(shard["shard"])
            input_index = int(shard["input_index"])
            start = int(shard["triple_start"])
            end = int(shard["triple_end"])
            records = shard_dir / str(shard["filename"])
            result_path = result_dir / (
                f"shard_{shard_id:03d}.json"
            )
            if records.exists():
                audit = validate_file(
                    records,
                    expected_input_index=input_index,
                    expected_range=(start, end),
                    expected_corpus_sha256=str(plan["corpus_sha256"]),
                    node_limit=int(plan["node_limit_per_instance"]),
                )
                atomic_json(
                    result_path,
                    {
                        "schema": "ramsey55.e2_triple_replacement_shard.v1",
                        "status": "COMPLETE",
                        "reused": True,
                        "plan_sha256": plan_sha256,
                        "shard": shard_id,
                        **audit,
                    },
                )
                reused_count += 1
                continue
            partial = Path(str(records) + ".partial")
            if partial.exists():
                archive_partial(partial, output_dir)
            if (
                sum(
                    item.stat().st_size
                    for item in output_dir.rglob("*")
                    if item.is_file()
                )
                > int(plan["output_byte_cap"])
            ):
                raise RuntimeError("output byte cap exceeded")
            if shutil.disk_usage(output_dir).free < int(
                plan["free_disk_reserve_bytes"]
            ):
                raise RuntimeError("free-disk reserve breached")
            command = (
                str(solver),
                "--graph",
                str(corpus),
                "--records",
                str(records),
                "--input-index",
                str(input_index),
                "--triple-start",
                str(start),
                "--triple-end",
                str(end),
                "--corpus-sha256",
                str(plan["corpus_sha256"]),
                "--node-limit",
                str(plan["node_limit_per_instance"]),
                "--seconds-limit",
                str(plan["seconds_limit_per_instance"]),
                "--record-byte-cap",
                str(shard["record_bytes"]),
            )
            shard_started = time.monotonic()
            process = subprocess.run(
                command,
                text=True,
                capture_output=True,
                check=False,
                timeout=float(plan["shard_timeout_seconds"]),
            )
            runtime = time.monotonic() - shard_started
            parsed = json_records(process.stdout)
            sat_records = [
                record
                for record in parsed
                if record.get("record_type") == "SAT"
                and record.get("status") == "SAT"
            ]
            if sat_records:
                if len(sat_records) != 1 or process.returncode != 10:
                    raise RuntimeError("malformed SAT-stop result")
                preserved = preserve_sat(
                    solver_record=sat_records[0],
                    plan_path=plan_path,
                    plan_sha256=plan_sha256,
                    corpus=corpus,
                    output_dir=output_dir,
                    exhaustive=exhaustive,
                    bitset=bitset,
                )
                found = {
                    "schema": "ramsey55.e2_triple_replacement_found.v1",
                    "created_utc": utc_now(),
                    "plan": relative(plan_path),
                    "plan_sha256": plan_sha256,
                    "shard": shard_id,
                    "solver_returncode": process.returncode,
                    "solver_stdout": process.stdout,
                    "solver_stderr": process.stderr,
                    **preserved,
                }
                atomic_json(output_dir / "FOUND.json", found)
                print(json.dumps(found, sort_keys=True))
                return 0 if preserved["verified"] else 1
            if process.returncode not in (0, 2):
                raise RuntimeError(
                    f"shard {shard_id} failed rc={process.returncode}: "
                    f"{process.stderr}"
                )
            if not records.exists():
                raise RuntimeError("producer did not promote complete shard")
            audit = validate_file(
                records,
                expected_input_index=input_index,
                expected_range=(start, end),
                expected_corpus_sha256=str(plan["corpus_sha256"]),
                node_limit=int(plan["node_limit_per_instance"]),
            )
            atomic_json(
                result_path,
                {
                    "schema": "ramsey55.e2_triple_replacement_shard.v1",
                    "status": "COMPLETE",
                    "reused": False,
                    "completed_utc": utc_now(),
                    "runtime_seconds": runtime,
                    "plan_sha256": plan_sha256,
                    "shard": shard_id,
                    "producer_returncode": process.returncode,
                    "producer_stdout": process.stdout,
                    "producer_stderr": process.stderr,
                    **audit,
                },
            )
            executed_count += 1

        coverage_path = output_dir / "coverage.json"
        checker_run = subprocess.run(
            (
                sys.executable,
                str(checker),
                "--plan",
                str(plan_path),
                "--corpus",
                str(corpus),
                "--shard-dir",
                str(shard_dir),
                "--output",
                str(coverage_path),
            ),
            text=True,
            capture_output=True,
            check=False,
            timeout=600,
        )
        if checker_run.returncode != 0:
            raise RuntimeError(
                "independent coverage checker failed: "
                f"{checker_run.stdout}\n{checker_run.stderr}"
            )
        coverage = parse_last_json(
            checker_run.stdout, "coverage checker"
        )
        if coverage.get("valid") is not True:
            raise RuntimeError("coverage checker did not return valid")
        totals = coverage["totals"]
        result = {
            "schema": "ramsey55.e2_triple_replacement_result.v1",
            "completed_utc": utc_now(),
            "status": (
                "COMPLETE_OBSERVATIONAL_NEGATIVE"
                if int(totals["limit_count"]) == 0
                else "COMPLETE_WITH_LIMITS_NO_CONCLUSION"
            ),
            "plan": relative(plan_path),
            "plan_sha256": plan_sha256,
            "runtime_seconds_this_invocation": time.monotonic() - started,
            "executed_shard_count": executed_count,
            "reused_shard_count": reused_count,
            "coverage": relative(coverage_path),
            "coverage_sha256": sha256_file(coverage_path),
            "exact_labeled_triple_coverage": True,
            "totals": totals,
            "construction_found": False,
            "negative_certified_count": int(
                totals["structural_obstruction_count"]
            ),
            "solver_negative_proof_checked_count": 0,
            "proof_generation": False,
            "claim_boundary": plan["claim_boundary"],
        }
        result_path = output_dir / "result.json"
        atomic_json(result_path, result)
        result["result_sha256"] = sha256_file(result_path)
        print(json.dumps(result, sort_keys=True))
        return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--make-plan", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument(
        "--plan",
        type=Path,
        default=(
            ROOT
            / "results"
            / "benchmark_plans"
            / "e2_triple_replacement_screen_v1.json"
        ),
    )
    parser.add_argument(
        "--solver",
        type=Path,
        default=ROOT / "build" / "e2_triple_replacement_solver",
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        default=ROOT / "data" / "e2_complement_class_representatives.g6",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=(
            ROOT
            / "results"
            / "constructive"
            / "e2_triple_replacement_screen_v1"
        ),
    )
    parser.add_argument(
        "--checker",
        type=Path,
        default=ROOT / "verify" / "e2_triple_replacement_coverage.py",
    )
    parser.add_argument(
        "--parser-source",
        type=Path,
        default=ROOT / "src" / "e2_triple_replacement_compact.py",
    )
    parser.add_argument(
        "--tests",
        type=Path,
        default=ROOT / "tests" / "e2_triple_replacement_tests.py",
    )
    parser.add_argument(
        "--exhaustive",
        type=Path,
        default=ROOT / "verify" / "exhaustive_verify.py",
    )
    parser.add_argument(
        "--bitset",
        type=Path,
        default=ROOT / "build" / "bitset_verify",
    )
    parser.add_argument("--shard-size", type=int, default=256)
    parser.add_argument("--node-limit", type=int, default=100_000)
    parser.add_argument("--seconds-limit", type=float, default=0.5)
    parser.add_argument("--shard-timeout", type=float, default=300.0)
    parser.add_argument("--output-byte-cap", type=int, default=50_000_000)
    parser.add_argument(
        "--free-disk-reserve-bytes", type=int, default=4_000_000_000
    )
    args = parser.parse_args()
    if args.make_plan == args.run:
        parser.error("select exactly one of --make-plan and --run")
    if args.make_plan:
        plan = make_plan(
            plan_path=args.plan,
            solver=args.solver,
            corpus=args.corpus,
            output_dir=args.output_dir,
            checker=args.checker,
            parser_source=args.parser_source,
            tests=args.tests,
            exhaustive=args.exhaustive,
            bitset=args.bitset,
            shard_size=args.shard_size,
            node_limit=args.node_limit,
            seconds_limit=args.seconds_limit,
            shard_timeout=args.shard_timeout,
            output_byte_cap=args.output_byte_cap,
            reserve_bytes=args.free_disk_reserve_bytes,
        )
        print(
            json.dumps(
                {
                    "status": "PLAN_FROZEN",
                    "plan": relative(args.plan),
                    "plan_sha256": sha256_file(args.plan),
                    "shard_count": plan["shard_count"],
                },
                sort_keys=True,
            )
        )
        return 0
    return run_screen(args.plan)


if __name__ == "__main__":
    raise SystemExit(main())
