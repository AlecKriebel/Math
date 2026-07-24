#!/usr/bin/env python3
"""Fail-closed checker for the frozen double-forced E=2 search artifacts.

The checker is intentionally specific to the one production run frozen in
``e2_low_closure_double_forced_v1.json``.  In addition to binding the search
and audit artifacts by SHA-256, it independently decodes and recounts every
retained endpoint.  It does not replay the heuristic trajectories and makes
no global Ramsey claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parents[1]
ORDER = 43
EDGE_COUNT = ORDER * (ORDER - 1) // 2
FULL_MASK = (1 << ORDER) - 1
SCHEMA = "ramsey55.e2_double_forced_result_check.v1"

SEARCH_PLAN_PATH = Path(
    "results/benchmark_plans/e2_low_closure_double_forced_v1.json"
)
SEARCH_RESULT_PATH = Path(
    "results/constructive/e2_low_closure_v2/double_forced.result.json"
)
BINARY_PATH = Path("build/search43_e2_barrier_escape")
AUDIT_PLAN_PATH = Path(
    "results/benchmark_plans/e2_double_forced_discovery_audit_v2.json"
)
AUDIT_RESULT_PATH = Path(
    "results/verification/e2_double_forced_discovery_audit_v2.json"
)

EXPECTED_HASHES = {
    "search_plan": (
        "07a8f8a238775bbe70621c221446e250ba4852973f167d0313990b8784dbbb54"
    ),
    "search_result": (
        "68a95613c09406cea836523f43ee39aa3345edf1023b883e20016b259e160071"
    ),
    "search_source": (
        "18079f5b3f1a0018cd0d47ac7965091401aa9a9a9c59dcd492c26ec4d327dcca"
    ),
    "search_binary": (
        "578fd32bc5312b844e411789660e64eca05ea207cd2df8a1698bf2cfaa0d2214"
    ),
    "quotient_audit": (
        "cd1f8a9e56e76b0c94df1c5705ca7090588e2eb12a2bd0009f3e53e115f47725"
    ),
    "e3_representatives": (
        "0f9485a82ecb6dba9b19ea0759ba37ef7c9bc64d481cf8fd7a248480b348471d"
    ),
    "e4_representatives": (
        "2ea9964afed1205884e971fb50fce77d783925804ae9d1064460e7b89190bca4"
    ),
    "known_e2_corpus": (
        "172fd8dca7e2a465bb483148036c7dd7a549796b191078742b80ef7df0ff34f0"
    ),
    "e2_output": (
        "ad48e7eb76403abc050bd6200003720ff781840116c6c6651414cbc27b90b646"
    ),
    "audit_plan": (
        "a9948365b9938ce36ec40d8b168bc8fc2f53e05d26b6d5140964b8939fd6a348"
    ),
    "audit_result": (
        "6b853b060f8a8b603af62bc86036475258cd448b183e57e39bcfda37cbe8e9f7"
    ),
    "audit_source": (
        "60cd9fbb6224ccda33504cd9010dacf61567a99b2f580bf8286f1563c020f87c"
    ),
    "audit_tests": (
        "38ea83d15a97bf80bdc7f94fb52c228339bef33b9471d346be907309506b89dc"
    ),
    "audit_representatives": (
        "94c052a7a5bcabcd7df9fa9c1246a2344846d4875ecb4fe0294651388513a205"
    ),
    "audit_novel_representatives": (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    ),
}

EXPECTED_SEARCH_SCALARS = {
    "seed": 20261322,
    "low_seed_file_count": 2,
    "low_seed_count": 53,
    "known_E2_state_count": 1892,
    "first_barrier_count": 47675,
    "first_barrier_exact_replays": 47675,
    "first_nonconflict_barrier_count": 46225,
    "first_high_conflict_barrier_count": 1450,
    "second_candidate_count": 39511631,
    "second_barrier_count": 47675,
    "second_barrier_exact_replays": 47675,
    "first_without_second_candidate_count": 0,
    "low_barriers_per_seed": 0,
    "low_second_barriers_per_first": 1,
    "rollouts_per_barrier": 1,
    "rollouts": 47675,
    "steps": 2720135,
    "steps_per_rollout": 256,
    "tabu_tenure": 11,
    "noise_per_million": 90000,
    "objective_ceiling": 80,
    "best_E": 2,
    "maximum_E": 80,
    "E1_visits": 0,
    "absorbed_known_cycle": 0,
    "known_cycle_visits": 0,
    "repeated_barrier_crossings": 0,
    "exhausted": 14296,
    "new_E2_unique_count": 1878,
    "exact_objective_checks": 2767810,
    "ceiling_rejections": 6390028,
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level JSON value is not an object")
    return value


def decode_graph6(text: str) -> tuple[int, ...]:
    """Independently decode one canonical short graph6 order-43 record."""

    if not text or text != text.strip():
        raise ValueError("graph6 record has surrounding whitespace")
    values = [ord(character) - 63 for character in text]
    if any(value < 0 or value >= 64 for value in values):
        raise ValueError("graph6 record contains an invalid byte")
    if values[0] != ORDER:
        raise ValueError("graph6 record is not an order-43 graph")
    payload = values[1:]
    if len(payload) != (EDGE_COUNT + 5) // 6:
        raise ValueError("graph6 payload length is not canonical")
    bits = [
        (value >> shift) & 1
        for value in payload
        for shift in range(5, -1, -1)
    ]
    if any(bits[EDGE_COUNT:]):
        raise ValueError("graph6 record has nonzero padding bits")
    adjacency = [0] * ORDER
    cursor = 0
    for right in range(1, ORDER):
        for left in range(right):
            if bits[cursor]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            cursor += 1
    return tuple(adjacency)


def encode_graph6(adjacency: Sequence[int]) -> str:
    """Independently encode one simple order-43 graph."""

    if len(adjacency) != ORDER:
        raise ValueError("adjacency has the wrong order")
    for vertex, row in enumerate(adjacency):
        if row & ~FULL_MASK or row & (1 << vertex):
            raise ValueError("adjacency is not a simple order-43 graph")
        for other in range(ORDER):
            if ((row >> other) & 1) != (
                (adjacency[other] >> vertex) & 1
            ):
                raise ValueError("adjacency is asymmetric")
    bits = [
        (adjacency[left] >> right) & 1
        for right in range(1, ORDER)
        for left in range(right)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload: list[str] = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(ORDER + 63) + "".join(payload)


def graph_complement(adjacency: Sequence[int]) -> tuple[int, ...]:
    if len(adjacency) != ORDER:
        raise ValueError("adjacency has the wrong order")
    return tuple(
        FULL_MASK & ~(row | (1 << vertex))
        for vertex, row in enumerate(adjacency)
    )


def count_five_cliques(
    adjacency: Sequence[int], stop_after: int | None = None
) -> int:
    """Count five-cliques, optionally stopping once a rejection is certain."""

    count = 0

    def recurse(candidates: int, depth: int) -> None:
        nonlocal count
        if stop_after is not None and count >= stop_after:
            return
        needed = 5 - depth
        if candidates.bit_count() < needed:
            return
        if needed == 0:
            count += 1
            return
        while candidates:
            if candidates.bit_count() < needed:
                return
            low = candidates & -candidates
            vertex = low.bit_length() - 1
            candidates ^= low
            recurse(candidates & adjacency[vertex], depth + 1)
            if stop_after is not None and count >= stop_after:
                return

    recurse(FULL_MASK, 0)
    return count


def exact_objective(adjacency: Sequence[int], reject_above: int | None = None) -> int:
    clique_count = count_five_cliques(adjacency, reject_above)
    if reject_above is not None and clique_count >= reject_above:
        return clique_count
    remaining = (
        None if reject_above is None else reject_above - clique_count
    )
    return clique_count + count_five_cliques(
        graph_complement(adjacency), remaining
    )


def read_graph6_stream(path: Path) -> list[str]:
    raw = path.read_bytes()
    if not raw.endswith(b"\n"):
        raise ValueError(f"{path}: stream lacks a final newline")
    if b"\r" in raw:
        raise ValueError(f"{path}: stream contains carriage returns")
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise ValueError(f"{path}: stream is not ASCII") from error
    if not lines or any(not line or line.startswith("#") for line in lines):
        raise ValueError(f"{path}: stream has blank/comment records")
    for index, line in enumerate(lines):
        adjacency = decode_graph6(line)
        if encode_graph6(adjacency) != line:
            raise ValueError(
                f"{path}: graph6 round trip failed at record {index}"
            )
    return lines


def recorded_path_matches(
    observed: object,
    planned: str,
    artifact: Path,
    project_root: Path,
) -> bool:
    if not isinstance(observed, str):
        return False
    accepted = {
        planned,
        f"{project_root.name}/{planned}",
        str(artifact.resolve()),
    }
    return observed in accepted


def validate_search_counters(
    result: dict[str, object], plan: dict[str, object]
) -> dict[str, bool]:
    checks: dict[str, bool] = {
        "search_mode": result.get("mode")
        == "low_seed_double_forced_search",
        "search_algorithm": result.get("algorithm")
        == "e2_low_closure_double_forced_v1",
        "search_evidence_label": result.get("evidence_label")
        == "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
    }
    for name, expected in EXPECTED_SEARCH_SCALARS.items():
        checks[f"counter_{name}"] = result.get(name) == expected

    first_by_source = result.get("first_by_source_objective")
    first_by_height = result.get("first_by_height")
    second_by_height = result.get("second_by_height")
    second_delta = result.get("second_delta_distribution")
    terminal_best = result.get("terminal_best_distribution")
    if not all(
        isinstance(item, dict)
        for item in (
            first_by_source,
            first_by_height,
            second_by_height,
            second_delta,
            terminal_best,
        )
    ):
        checks["counter_histograms_are_objects"] = False
        return checks

    assert isinstance(first_by_source, dict)
    assert isinstance(first_by_height, dict)
    assert isinstance(second_by_height, dict)
    assert isinstance(second_delta, dict)
    assert isinstance(terminal_best, dict)
    checks.update(
        {
            "counter_histograms_are_objects": True,
            "first_source_distribution": first_by_source
            == {"3": 8100, "4": 39575},
            "first_height_sum": sum(first_by_height.values()) == 47675,
            "first_height_maximum": max(map(int, first_by_height)) == 47,
            "first_kind_identity": (
                result.get("first_nonconflict_barrier_count", -1)
                + result.get("first_high_conflict_barrier_count", -1)
                == result.get("first_barrier_count")
            ),
            "first_replay_identity": result.get(
                "first_barrier_exact_replays"
            )
            == result.get("first_barrier_count"),
            "second_height_sum": sum(second_by_height.values()) == 47675,
            "second_delta_distribution": second_delta
            == {"0": 15615, "1": 32060},
            "second_delta_sum": sum(second_delta.values()) == 47675,
            "second_replay_identity": result.get(
                "second_barrier_exact_replays"
            )
            == result.get("second_barrier_count"),
            "rollout_schedule_identity": result.get("rollouts")
            == result.get("second_barrier_count")
            * result.get("rollouts_per_barrier"),
            "terminal_best_sum": sum(terminal_best.values()) == 47675,
            "terminal_E2_and_exhausted_identity": terminal_best.get("2")
            + result.get("exhausted")
            == result.get("rollouts"),
            "exact_check_identity": result.get("exact_objective_checks")
            == result.get("steps") + result.get("rollouts"),
        }
    )

    first_plan = plan.get("first_barrier_schedule")
    second_plan = plan.get("second_barrier_schedule")
    repair_plan = plan.get("repair")
    if not all(
        isinstance(item, dict)
        for item in (first_plan, second_plan, repair_plan)
    ):
        checks["plan_schedule_objects"] = False
        return checks
    assert isinstance(first_plan, dict)
    assert isinstance(second_plan, dict)
    assert isinstance(repair_plan, dict)
    checks.update(
        {
            "plan_schedule_objects": True,
            "first_schedule_matches_plan": (
                result.get("first_barrier_count")
                == first_plan.get("expected_first_barrier_count")
                and result.get("first_nonconflict_barrier_count")
                == first_plan.get("expected_nonconflict_count")
                and result.get("first_high_conflict_barrier_count")
                == first_plan.get("expected_high_conflict_count")
                and max(map(int, first_by_height))
                == first_plan.get("expected_maximum_height")
            ),
            "second_schedule_matches_plan": (
                result.get("low_second_barriers_per_first")
                == second_plan.get("barriers_per_first")
                and result.get("first_without_second_candidate_count") == 0
            ),
            "repair_parameters_match_plan": (
                result.get("seed") == repair_plan.get("seed")
                and result.get("rollouts_per_barrier")
                == repair_plan.get("rollouts_per_second_barrier")
                and result.get("steps_per_rollout")
                == repair_plan.get("steps_per_rollout")
                and result.get("tabu_tenure")
                == repair_plan.get("tabu_tenure")
                and result.get("noise_per_million")
                == repair_plan.get("noise_per_million")
                and result.get("objective_ceiling")
                == repair_plan.get("objective_ceiling")
            ),
        }
    )
    return checks


def _check(project_root: Path) -> dict[str, object]:
    checks: dict[str, bool] = {}
    project_root = project_root.resolve()

    search_plan_path = project_root / SEARCH_PLAN_PATH
    search_result_path = project_root / SEARCH_RESULT_PATH
    audit_plan_path = project_root / AUDIT_PLAN_PATH
    audit_result_path = project_root / AUDIT_RESULT_PATH
    binary_path = project_root / BINARY_PATH
    search_plan = read_json(search_plan_path)
    search_result = read_json(search_result_path)
    audit_plan = read_json(audit_plan_path)
    audit_result = read_json(audit_result_path)

    checks.update(
        {
            "search_plan_hash": sha256_file(search_plan_path)
            == EXPECTED_HASHES["search_plan"],
            "search_result_hash": sha256_file(search_result_path)
            == EXPECTED_HASHES["search_result"],
            "audit_plan_hash": sha256_file(audit_plan_path)
            == EXPECTED_HASHES["audit_plan"],
            "audit_result_hash": sha256_file(audit_result_path)
            == EXPECTED_HASHES["audit_result"],
            "search_plan_schema": search_plan.get("schema")
            == "ramsey55.e2_low_closure_double_forced_plan.v1",
            "search_plan_frozen": search_plan.get("status")
            == "FROZEN_BEFORE_PRODUCTION",
            "audit_plan_schema": audit_plan.get("schema")
            == "ramsey55.e2_double_forced_discovery_audit_plan.v2",
            "audit_plan_frozen": audit_plan.get("status")
            == "FROZEN_BEFORE_AUDIT",
        }
    )

    implementation = search_plan["implementation"]
    if not isinstance(implementation, dict):
        raise ValueError("search-plan implementation is not an object")
    source_path = project_root / str(implementation["source"])
    binding = search_result["binding"]
    if not isinstance(binding, dict):
        raise ValueError("search-result binding is not an object")
    checks.update(
        {
            "source_hash_expected": sha256_file(source_path)
            == EXPECTED_HASHES["search_source"],
            "source_hash_matches_plan": sha256_file(source_path)
            == implementation.get("source_sha256"),
            "source_hash_matches_result": sha256_file(source_path)
            == binding.get("source_sha256"),
            "binary_exists": binary_path.is_file(),
            "binary_is_executable": os.access(binary_path, os.X_OK),
            "binary_hash_expected": sha256_file(binary_path)
            == EXPECTED_HASHES["search_binary"],
            "binary_hash_matches_plan": sha256_file(binary_path)
            == implementation.get("binary_sha256"),
            "binary_hash_matches_result": sha256_file(binary_path)
            == binding.get("binary_sha256"),
            "result_exit_code": binding.get("exit_code") == 0,
            "result_plan_path": binding.get("plan")
            == SEARCH_PLAN_PATH.as_posix(),
            "result_plan_hash": binding.get("plan_sha256")
            == EXPECTED_HASHES["search_plan"],
        }
    )
    checks.update(validate_search_counters(search_result, search_plan))

    input_plan = search_plan["input"]
    if not isinstance(input_plan, dict):
        raise ValueError("search-plan input is not an object")
    quotient_path = project_root / str(input_plan["quotient_audit"])
    quotient = read_json(quotient_path)
    checks.update(
        {
            "quotient_audit_hash_expected": sha256_file(quotient_path)
            == EXPECTED_HASHES["quotient_audit"],
            "quotient_audit_hash_matches_plan": sha256_file(quotient_path)
            == input_plan.get("quotient_audit_sha256"),
            "quotient_audit_valid": quotient.get("valid") is True,
            "quotient_audit_has_53_classes": quotient.get(
                "total_complement_isomorphism_class_count"
            )
            == 53,
        }
    )

    representative_graphs: list[str] = []
    representative_distribution: Counter[int] = Counter()
    for objective, prefix in ((3, "E3"), (4, "E4")):
        path = project_root / str(input_plan[f"{prefix}_representatives"])
        lines = read_graph6_stream(path)
        expected_count = 9 if objective == 3 else 44
        expected_hash = EXPECTED_HASHES[
            "e3_representatives" if objective == 3
            else "e4_representatives"
        ]
        checks[f"{prefix}_representative_hash_expected"] = (
            sha256_file(path) == expected_hash
        )
        checks[f"{prefix}_representative_hash_matches_plan"] = (
            sha256_file(path)
            == input_plan.get(f"{prefix}_representatives_sha256")
        )
        checks[f"{prefix}_representative_count"] = (
            len(lines)
            == input_plan.get(f"{prefix}_representative_count")
            == expected_count
        )
        for line in lines:
            value = exact_objective(decode_graph6(line))
            representative_distribution[value] += 1
        representative_graphs.extend(lines)
    checks.update(
        {
            "all_53_representatives_unique": len(representative_graphs)
            == len(set(representative_graphs))
            == 53,
            "all_53_representatives_independently_recounted": dict(
                sorted(representative_distribution.items())
            )
            == {3: 9, 4: 44},
            "search_seed_distribution_matches_recount": search_result.get(
                "low_seed_objective_distribution"
            )
            == {
                str(key): value
                for key, value in sorted(
                    representative_distribution.items()
                )
            },
        }
    )

    known_directory = project_root / str(
        input_plan["known_E2_seed_directory"]
    )
    known_paths = sorted(known_directory.glob("line_*.g6"))
    known_graphs: list[str] = []
    for path in known_paths:
        lines = read_graph6_stream(path)
        if len(lines) != 1:
            raise ValueError(f"{path}: known seed file is not a singleton")
        known_graphs.extend(lines)
    known_corpus_hash = hashlib.sha256(
        b"".join(path.read_bytes() for path in known_paths)
    ).hexdigest()
    known_objectives = Counter(
        exact_objective(decode_graph6(line)) for line in known_graphs
    )
    checks.update(
        {
            "known_seed_file_count": len(known_paths)
            == input_plan.get("known_E2_seed_count")
            == 22,
            "known_seed_graphs_unique": len(known_graphs)
            == len(set(known_graphs))
            == 22,
            "known_seed_corpus_hash_expected": known_corpus_hash
            == EXPECTED_HASHES["known_e2_corpus"],
            "known_seed_corpus_hash_matches_plan": known_corpus_hash
            == input_plan.get(
                "known_E2_seed_corpus_concatenated_sha256"
            ),
            "known_seed_graphs_independently_recounted": dict(
                known_objectives
            )
            == {2: 22},
            "known_labeled_cycle_count_binding": (
                input_plan.get("expected_known_E2_labeled_state_count")
                == search_result.get("known_E2_state_count")
                == 1892
            ),
        }
    )

    repair_plan = search_plan["repair"]
    if not isinstance(repair_plan, dict):
        raise ValueError("search-plan repair is not an object")
    endpoint_path = project_root / str(repair_plan["E2_discovery_output"])
    endpoint_lines = read_graph6_stream(endpoint_path)
    endpoint_hash = sha256_file(endpoint_path)
    endpoint_objectives = Counter()
    for line in endpoint_lines:
        endpoint_objectives[
            exact_objective(decode_graph6(line), reject_above=3)
        ] += 1
    checks.update(
        {
            "E2_output_path": recorded_path_matches(
                search_result.get("discovery_output"),
                str(repair_plan["E2_discovery_output"]),
                endpoint_path,
                project_root,
            ),
            "E2_output_count": len(endpoint_lines) == 1878,
            "E2_output_unique": len(endpoint_lines)
            == len(set(endpoint_lines))
            == 1878,
            "E2_output_sorted": endpoint_lines == sorted(endpoint_lines),
            "E2_output_hash_expected": endpoint_hash
            == EXPECTED_HASHES["e2_output"],
            "E2_output_count_matches_result": binding.get(
                "E2_output_line_count"
            )
            == search_result.get("new_E2_unique_count")
            == len(endpoint_lines),
            "E2_output_hash_matches_result": binding.get(
                "E2_output_sha256"
            )
            == endpoint_hash,
            "all_1878_outputs_independently_recounted_to_E2": dict(
                endpoint_objectives
            )
            == {2: 1878},
        }
    )

    near_path = project_root / str(repair_plan["E1_output"])
    checks.update(
        {
            "E1_output_path": recorded_path_matches(
                search_result.get("near_output"),
                str(repair_plan["E1_output"]),
                near_path,
                project_root,
            ),
            "E1_output_absent": not near_path.exists(),
            "E1_binding_absent": binding.get("E1_output_exists") is False,
            "E1_counter_zero": search_result.get("E1_visits") == 0,
            "E0_not_found": search_result.get("E0_found") is False,
        }
    )

    audit_input = audit_plan["input"]
    audit_implementation = audit_plan["implementation"]
    audit_output = audit_plan["output"]
    if not all(
        isinstance(item, dict)
        for item in (audit_input, audit_implementation, audit_output)
    ):
        raise ValueError("audit plan has a malformed object")
    assert isinstance(audit_input, dict)
    assert isinstance(audit_implementation, dict)
    assert isinstance(audit_output, dict)
    audit_source_path = project_root / str(audit_implementation["source"])
    audit_tests_path = project_root / str(audit_implementation["tests"])
    audit_representatives_path = project_root / str(
        audit_output["representatives"]
    )
    audit_novel_path = project_root / str(
        audit_output["novel_representatives"]
    )
    checks.update(
        {
            "audit_binds_search_plan_path": audit_input.get("search_plan")
            == SEARCH_PLAN_PATH.as_posix(),
            "audit_binds_search_plan_hash": audit_input.get(
                "search_plan_sha256"
            )
            == EXPECTED_HASHES["search_plan"],
            "audit_binds_search_result_path": audit_input.get(
                "search_result"
            )
            == SEARCH_RESULT_PATH.as_posix(),
            "audit_binds_search_result_hash": audit_input.get(
                "search_result_sha256"
            )
            == EXPECTED_HASHES["search_result"],
            "audit_binds_endpoint_path": audit_input.get("endpoint_stream")
            == str(repair_plan["E2_discovery_output"]),
            "audit_binds_endpoint_count": audit_input.get("endpoint_count")
            == len(endpoint_lines)
            == 1878,
            "audit_binds_endpoint_hash": audit_input.get(
                "endpoint_stream_sha256"
            )
            == endpoint_hash,
            "audit_binds_known_seed_count": audit_input.get(
                "known_seed_count"
            )
            == len(known_paths)
            == 22,
            "audit_binds_known_seed_hash": audit_input.get(
                "known_seed_corpus_sha256"
            )
            == known_corpus_hash,
            "audit_source_hash_expected": sha256_file(audit_source_path)
            == EXPECTED_HASHES["audit_source"],
            "audit_source_hash_matches_plan": sha256_file(
                audit_source_path
            )
            == audit_implementation.get("source_sha256"),
            "audit_source_hash_matches_result": sha256_file(
                audit_source_path
            )
            == audit_result.get("source_sha256"),
            "audit_tests_hash_expected": sha256_file(audit_tests_path)
            == EXPECTED_HASHES["audit_tests"],
            "audit_tests_hash_matches_plan": sha256_file(audit_tests_path)
            == audit_implementation.get("tests_sha256"),
            "audit_result_valid": audit_result.get("valid") is True,
            "audit_recount_fact": audit_result.get(
                "all_endpoints_independently_recounted_to_E2"
            )
            is True,
            "audit_dense_sparse_ordinary_match": audit_result.get(
                "dense_sparse_ordinary_partition_match"
            )
            is True,
            "audit_dense_sparse_complement_match": audit_result.get(
                "dense_sparse_complement_partition_match"
            )
            is True,
            "audit_dense_sparse_novelty_match": audit_result.get(
                "dense_sparse_novelty_decisions_match"
            )
            is True,
            "audit_discovery_count": audit_result.get("discovery_count")
            == len(endpoint_lines)
            == 1878,
            "audit_discovery_hash": audit_result.get("discovery_sha256")
            == endpoint_hash,
            "audit_known_seed_count": audit_result.get("known_seed_count")
            == 22,
            "audit_known_seed_hash": audit_result.get(
                "known_seed_corpus_sha256"
            )
            == known_corpus_hash,
            "audit_two_known_classes": audit_result.get(
                "known_complement_isomorphism_class_count"
            )
            == 2,
            "audit_two_discovery_classes": audit_result.get(
                "discovery_complement_isomorphism_class_count"
            )
            == 2,
            "audit_no_novel_labeled_endpoints": audit_result.get(
                "novel_labeled_endpoint_count"
            )
            == 0,
            "audit_no_novel_classes": audit_result.get(
                "novel_complement_isomorphism_class_count"
            )
            == 0,
            "audit_representative_hash_expected": sha256_file(
                audit_representatives_path
            )
            == EXPECTED_HASHES["audit_representatives"],
            "audit_representative_hash_matches_result": sha256_file(
                audit_representatives_path
            )
            == audit_result.get("representative_sha256"),
            "audit_novel_file_empty": audit_novel_path.read_bytes() == b"",
            "audit_novel_hash_expected": sha256_file(audit_novel_path)
            == EXPECTED_HASHES["audit_novel_representatives"],
            "audit_novel_hash_matches_result": sha256_file(
                audit_novel_path
            )
            == audit_result.get("novel_representative_sha256"),
        }
    )

    return {
        "schema": SCHEMA,
        "status": (
            "VALID_FROZEN_DOUBLE_FORCED_ARTIFACT_BINDING"
            if all(checks.values())
            else "INVALID"
        ),
        "valid": all(checks.values()),
        "checks": dict(sorted(checks.items())),
        "metrics": {
            "input_representative_count": len(representative_graphs),
            "input_representative_objective_distribution": {
                str(key): value
                for key, value in sorted(
                    representative_distribution.items()
                )
            },
            "known_seed_count": len(known_graphs),
            "known_seed_objective_distribution": {
                str(key): value
                for key, value in sorted(known_objectives.items())
            },
            "output_count": len(endpoint_lines),
            "output_objective_distribution": {
                str(key): value
                for key, value in sorted(endpoint_objectives.items())
            },
            "search_rollouts": search_result["rollouts"],
            "search_steps": search_result["steps"],
            "search_best_E": search_result["best_E"],
            "search_E1_visits": search_result["E1_visits"],
            "audit_novel_complement_isomorphism_class_count": (
                audit_result["novel_complement_isomorphism_class_count"]
            ),
        },
        "hashes": {
            "checker_source": sha256_file(Path(__file__)),
            "search_plan": sha256_file(search_plan_path),
            "search_result": sha256_file(search_result_path),
            "search_source": sha256_file(source_path),
            "search_binary": sha256_file(binary_path),
            "E2_output": endpoint_hash,
            "audit_plan": sha256_file(audit_plan_path),
            "audit_result": sha256_file(audit_result_path),
            "audit_source": sha256_file(audit_source_path),
        },
        "claim_boundary": (
            "This fail-closed checker binds one frozen heuristic search and "
            "its finite endpoint audit. It independently recounts the 1,878 "
            "retained endpoints to E=2, but it does not replay the stochastic "
            "repair trajectories, classify all E=2 graphs, or prove a global "
            "Ramsey existence or nonexistence statement."
        ),
    }


def check(project_root: Path = ROOT) -> dict[str, object]:
    """Run the checker, converting every missing/malformed input to failure."""

    try:
        return _check(project_root)
    except Exception as error:  # Deliberately fail closed at the outer edge.
        return {
            "schema": SCHEMA,
            "status": "INVALID",
            "valid": False,
            "checks": {"fatal_error_absent": False},
            "fatal_error": f"{type(error).__name__}: {error}",
            "claim_boundary": (
                "An input was missing or malformed. No artifact claim is "
                "accepted."
            ),
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root",
        type=Path,
        default=ROOT,
        help="ramsey55 project root (default: inferred from this script)",
    )
    args = parser.parse_args()
    result = check(args.project_root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
