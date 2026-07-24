#!/usr/bin/env python3
"""Independent coverage and structural-obstruction audit for E=2 replacement."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from core_completion_catalog_batch import atomic_json  # noqa: E402
from core_completion_k2 import build_k2_completion_instance  # noqa: E402
from e2_triple_replacement_compact import (  # noqa: E402
    HEADER_BYTES,
    RECORD_BYTES,
    STATUS_LIMIT,
    STATUS_OBSERVED_UNSAT,
    STATUS_STRUCTURAL,
    TRIPLES,
    TRIPLES_PER_INPUT,
    iter_records,
    sha256_file,
    validate_file,
)
from graph_io import read_graph, validate_simple  # noqa: E402


CHECKER_ID = "ramsey55_e2_triple_replacement_coverage_checker_v1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def forbidden_five_sets(
    adjacency: list[int],
) -> tuple[tuple[str, tuple[int, ...]], ...]:
    validate_simple(adjacency)
    conflicts: list[tuple[str, tuple[int, ...]]] = []
    for vertices in itertools.combinations(range(len(adjacency)), 5):
        edges = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        if edges == 10:
            conflicts.append(("clique", vertices))
        elif edges == 0:
            conflicts.append(("independent", vertices))
    return tuple(conflicts)


def retained_count(
    conflicts: tuple[tuple[str, tuple[int, ...]], ...],
    deleted: tuple[int, int, int],
) -> int:
    removed = set(deleted)
    return sum(not removed.intersection(vertices) for _, vertices in conflicts)


def induced_core_three(
    adjacency: list[int], deleted: tuple[int, int, int]
) -> list[int]:
    retained = [v for v in range(len(adjacency)) if v not in deleted]
    if len(adjacency) != 43 or len(retained) != 40:
        raise ValueError("expected a delete-three core of order 40")
    core = [0] * 40
    for new_left, old_left in enumerate(retained):
        for new_right in range(new_left + 1, 40):
            old_right = retained[new_right]
            if (adjacency[old_left] >> old_right) & 1:
                core[new_left] |= 1 << new_right
                core[new_right] |= 1 << new_left
    validate_simple(core)
    return core


def check_formula_statistics(
    adjacency: list[int], deleted: tuple[int, int, int], record: object
) -> dict[str, int | list[int]]:
    core = induced_core_three(adjacency, deleted)
    instance = build_k2_completion_instance(core)
    clique = instance.clique_counts_by_new_count
    independent = instance.independent_counts_by_new_count
    expected = {
        "clauses": len(instance.clauses),
        "core_k4": clique[0] // 3,
        "core_i4": independent[0] // 3,
        "core_k3": clique[1] // 3,
        "core_i3": independent[1] // 3,
        "core_edges": clique[2],
        "core_nonedges": independent[2],
    }
    actual = {key: int(getattr(record, key)) for key in expected}
    if expected != actual:
        raise ValueError(
            f"independent formula statistics mismatch for {deleted}: "
            f"{actual} != {expected}"
        )
    return {
        "deleted_vertices": list(deleted),
        **expected,
    }


def expected_shards(plan: dict[str, object]) -> list[dict[str, object]]:
    raw = plan.get("shards")
    if not isinstance(raw, list) or not raw:
        raise ValueError("plan has no shards")
    shards: list[dict[str, object]] = []
    cursors = {1: 0, 2: 0}
    for expected_id, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError("non-object shard")
        shard = dict(item)
        if int(shard.get("shard", -1)) != expected_id:
            raise ValueError("shard IDs are not sequential")
        input_index = int(shard.get("input_index", 0))
        start = int(shard.get("triple_start", -1))
        end = int(shard.get("triple_end", -1))
        if input_index not in (1, 2) or start != cursors[input_index]:
            raise ValueError("shard ranges are not contiguous")
        if not start < end <= TRIPLES_PER_INPUT:
            raise ValueError("invalid planned shard range")
        if int(shard.get("record_count", -1)) != end - start:
            raise ValueError("planned shard record count mismatch")
        if int(shard.get("record_bytes", -1)) != (
            HEADER_BYTES + (end - start) * RECORD_BYTES
        ):
            raise ValueError("planned shard byte count mismatch")
        cursors[input_index] = end
        shards.append(shard)
    if cursors != {1: TRIPLES_PER_INPUT, 2: TRIPLES_PER_INPUT}:
        raise ValueError("plan does not exactly cover both triple spaces")
    return shards


def run_check(
    plan_path: Path,
    corpus_path: Path,
    shard_dir: Path,
) -> dict[str, object]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan_sha256 = sha256_file(plan_path)
    corpus_sha256 = sha256_file(corpus_path)
    if plan.get("schema") != "ramsey55.e2_triple_replacement_plan.v1":
        raise ValueError("unexpected plan schema")
    if plan.get("corpus_sha256") != corpus_sha256:
        raise ValueError("plan/corpus SHA-256 mismatch")
    shards = expected_shards(plan)

    inputs: dict[int, list[int]] = {
        index: read_graph(corpus_path, index) for index in (1, 2)
    }
    conflicts = {
        index: forbidden_five_sets(adjacency)
        for index, adjacency in inputs.items()
    }
    expected_conflicts = {
        1: (
            ("clique", (10, 11, 13, 28, 42)),
            ("clique", (11, 13, 18, 28, 42)),
        ),
        2: (
            ("independent", (10, 12, 26, 34, 42)),
            ("independent", (10, 23, 26, 34, 42)),
        ),
    }
    if conflicts != expected_conflicts:
        raise ValueError(f"frozen source conflict mismatch: {conflicts!r}")

    sample_ordinals = {
        int(index): {int(value) for value in values}
        for index, values in dict(
            plan.get("formula_reconstruction_ordinals", {})
        ).items()
    }
    reconstructed: list[dict[str, object]] = []
    totals = {
        "record_count": 0,
        "structural_obstruction_count": 0,
        "observed_unsat_count": 0,
        "limit_count": 0,
        "total_nodes": 0,
    }
    per_input = {
        1: {key: 0 for key in totals},
        2: {key: 0 for key in totals},
    }
    shard_records: list[dict[str, object]] = []
    for shard in shards:
        input_index = int(shard["input_index"])
        start = int(shard["triple_start"])
        end = int(shard["triple_end"])
        path = shard_dir / str(shard["filename"])
        audit = validate_file(
            path,
            expected_input_index=input_index,
            expected_range=(start, end),
            expected_corpus_sha256=corpus_sha256,
            node_limit=int(plan["node_limit_per_instance"]),
        )
        shard_records.append(
            {
                "shard": int(shard["shard"]),
                "path": str(path.resolve().relative_to(ROOT)),
                **audit,
            }
        )
        for record in iter_records(
            path,
            expected_input_index=input_index,
            expected_range=(start, end),
            expected_corpus_sha256=corpus_sha256,
        ):
            independently_retained = retained_count(
                conflicts[input_index], record.deleted_vertices
            )
            if independently_retained:
                if (
                    record.status != STATUS_STRUCTURAL
                    or record.retained_conflicts != independently_retained
                ):
                    raise ValueError(
                        "structural-obstruction classification mismatch at "
                        f"input {input_index}, triple "
                        f"{record.triple_ordinal}"
                    )
            elif record.status == STATUS_STRUCTURAL:
                raise ValueError(
                    "eligible core incorrectly marked structural at input "
                    f"{input_index}, triple {record.triple_ordinal}"
                )
            if (
                independently_retained == 0
                and record.triple_ordinal
                in sample_ordinals.get(input_index, set())
            ):
                reconstructed.append(
                    {
                        "input_index": input_index,
                        "triple_ordinal": record.triple_ordinal,
                        **check_formula_statistics(
                            inputs[input_index],
                            record.deleted_vertices,
                            record,
                        ),
                    }
                )
            key = (
                "structural_obstruction_count"
                if record.status == STATUS_STRUCTURAL
                else (
                    "observed_unsat_count"
                    if record.status == STATUS_OBSERVED_UNSAT
                    else "limit_count"
                )
            )
            totals["record_count"] += 1
            totals[key] += 1
            totals["total_nodes"] += record.nodes
            per_input[input_index]["record_count"] += 1
            per_input[input_index][key] += 1
            per_input[input_index]["total_nodes"] += record.nodes

    expected_samples = sum(len(values) for values in sample_ordinals.values())
    if len(reconstructed) != expected_samples:
        raise ValueError("not every formula reconstruction sample was checked")
    expected_total = 2 * TRIPLES_PER_INPUT
    if totals["record_count"] != expected_total:
        raise ValueError("coverage record count is incomplete")
    if totals["structural_obstruction_count"] != 18_204:
        raise ValueError("unexpected exact structural-obstruction count")
    if sum(
        totals[key]
        for key in (
            "structural_obstruction_count",
            "observed_unsat_count",
            "limit_count",
        )
    ) != expected_total:
        raise ValueError("terminal status partition is not exact")
    return {
        "schema": "ramsey55.e2_triple_replacement_coverage.v1",
        "checker": CHECKER_ID,
        "checked_utc": utc_now(),
        "valid": True,
        "plan": str(plan_path.resolve().relative_to(ROOT)),
        "plan_sha256": plan_sha256,
        "corpus": str(corpus_path.resolve().relative_to(ROOT)),
        "corpus_sha256": corpus_sha256,
        "shard_directory": str(shard_dir.resolve().relative_to(ROOT)),
        "shard_count": len(shards),
        "exact_labeled_triple_coverage": True,
        "triple_count_per_input": TRIPLES_PER_INPUT,
        "input_count": 2,
        "totals": totals,
        "per_input": [
            {"input_index": index, **per_input[index]}
            for index in (1, 2)
        ],
        "source_conflicts": [
            {
                "input_index": index,
                "conflicts": [
                    {"colour": colour, "vertices": list(vertices)}
                    for colour, vertices in conflicts[index]
                ],
            }
            for index in (1, 2)
        ],
        "formula_reconstruction_samples": reconstructed,
        "shards": shard_records,
        "negative_certified_count": totals[
            "structural_obstruction_count"
        ],
        "solver_negative_proof_checked_count": 0,
        "construction_found": False,
        "claim_boundary": (
            "The structural-obstruction records are exact fixed-core "
            "nonextension results. DPLL UNSAT records are reproducible "
            "proof-free observations. The screen covers only delete-three/"
            "add-three replacements of the two frozen E=2 representatives "
            "and is not a global order-43 nonexistence result."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--shard-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = run_check(args.plan, args.corpus, args.shard_dir)
    except Exception as error:
        failure = {
            "schema": "ramsey55.e2_triple_replacement_coverage.v1",
            "checker": CHECKER_ID,
            "checked_utc": utc_now(),
            "valid": False,
            "error": str(error),
        }
        if args.output:
            atomic_json(args.output, failure)
        print(json.dumps(failure, sort_keys=True))
        return 1
    if args.output:
        atomic_json(args.output, result)
        result["output_sha256"] = sha256_file(args.output)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
