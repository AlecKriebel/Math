#!/usr/bin/env python3
"""Fail-closed audit of the frozen two-forced-edge constructive search.

This checker does four independent things:

1. verifies all frozen hashes, parameters, aggregate identities, and output
   paths;
2. compiles and runs ``e2_double_forced_schedule_exact.cpp``, which
   reconstructs all 47,675 first barriers and all 39,511,631 eligible second
   candidates without importing production search code;
3. independently recounts all 1,878 retained E=2 endpoints and reconstructs
   their ordinary/complement-isomorphism quotient with Traces ``shortg -t``;
4. reruns the hash-bound production binary in a temporary directory and
   requires byte-identical E=2 output and no E=1 output.

The checked experiment remains heuristic after its two exact forced moves.
Nothing here is a Ramsey nonexistence proof.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Iterable, Sequence


ORDER = 43
EDGE_COUNT = ORDER * (ORDER - 1) // 2
FULL_MASK = (1 << ORDER) - 1
SCHEMA = "ramsey55.e2_double_forced_search_independent_check.v1"

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
    "e3_representatives": (
        "0f9485a82ecb6dba9b19ea0759ba37ef7c9bc64d481cf8fd7a248480b348471d"
    ),
    "e4_representatives": (
        "2ea9964afed1205884e971fb50fce77d783925804ae9d1064460e7b89190bca4"
    ),
    "quotient_audit": (
        "cd1f8a9e56e76b0c94df1c5705ca7090588e2eb12a2bd0009f3e53e115f47725"
    ),
    "known_e2_corpus": (
        "172fd8dca7e2a465bb483148036c7dd7a549796b191078742b80ef7df0ff34f0"
    ),
    "endpoint_stream": (
        "ad48e7eb76403abc050bd6200003720ff781840116c6c6651414cbc27b90b646"
    ),
    "endpoint_audit_source": (
        "60cd9fbb6224ccda33504cd9010dacf61567a99b2f580bf8286f1563c020f87c"
    ),
    "endpoint_audit_tests": (
        "38ea83d15a97bf80bdc7f94fb52c228339bef33b9471d346be907309506b89dc"
    ),
    "endpoint_audit_v1_plan": (
        "b67f43f1800aa4fdc19f1897dea13be8dd43fa51e0e1903e52af7df9546d2ae4"
    ),
    "endpoint_audit_v1_result": (
        "51e96399543b837115b0111e86dcd1e3a5c7d3d2b4dc0a6326dd7ebef280bdf4"
    ),
    "endpoint_audit_v2_plan": (
        "a9948365b9938ce36ec40d8b168bc8fc2f53e05d26b6d5140964b8939fd6a348"
    ),
    "endpoint_audit_v2_result": (
        "6b853b060f8a8b603af62bc86036475258cd448b183e57e39bcfda37cbe8e9f7"
    ),
    "endpoint_representatives": (
        "94c052a7a5bcabcd7df9fa9c1246a2344846d4875ecb4fe0294651388513a205"
    ),
    "empty_stream": (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    ),
    "shortg_traces": (
        "d31954e657d682802ea4d1f881cad175066b3a8ed624e91e4bfa9b8eb94d39d8"
    ),
}

EXPECTED_SEARCH_FIELDS = {
    "mode": "low_seed_double_forced_search",
    "algorithm": "e2_low_closure_double_forced_v1",
    "seed": 20261322,
    "low_seed_file_count": 2,
    "low_seed_count": 53,
    "low_seed_objective_distribution": {"3": 9, "4": 44},
    "known_E2_state_count": 1892,
    "first_barrier_count": 47_675,
    "first_barrier_exact_replays": 47_675,
    "first_nonconflict_barrier_count": 46_225,
    "first_high_conflict_barrier_count": 1_450,
    "first_by_source_objective": {"3": 8_100, "4": 39_575},
    "second_candidate_count": 39_511_631,
    "second_barrier_count": 47_675,
    "second_barrier_exact_replays": 47_675,
    "first_without_second_candidate_count": 0,
    "second_delta_distribution": {"0": 15_615, "1": 32_060},
    "low_barriers_per_seed": 0,
    "low_second_barriers_per_first": 1,
    "rollouts_per_barrier": 1,
    "rollouts": 47_675,
    "steps": 2_720_135,
    "steps_per_rollout": 256,
    "tabu_tenure": 11,
    "noise_per_million": 90_000,
    "objective_ceiling": 80,
    "best_E": 2,
    "maximum_E": 80,
    "E1_visits": 0,
    "absorbed_known_cycle": 0,
    "known_cycle_visits": 0,
    "repeated_barrier_crossings": 0,
    "exhausted": 14_296,
    "new_E2_unique_count": 1_878,
    "exact_objective_checks": 2_767_810,
    "ceiling_rejections": 6_390_028,
    "E0_found": False,
}


class AuditFailure(RuntimeError):
    """Raised for a fail-closed audit mismatch."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def strict_json_load(path: Path) -> dict[str, object]:
    def no_duplicates(
        pairs: list[tuple[str, object]],
    ) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise AuditFailure(f"{path}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=no_duplicates,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise AuditFailure(f"{path}: cannot parse strict JSON") from error
    if not isinstance(value, dict):
        raise AuditFailure(f"{path}: top-level JSON is not an object")
    return value


def demand_equal(label: str, observed: object, expected: object) -> None:
    if observed != expected:
        raise AuditFailure(
            f"{label}: observed {observed!r}, expected {expected!r}"
        )


def demand_hash(label: str, path: Path, expected: str) -> str:
    if not path.is_file():
        raise AuditFailure(f"{label}: missing file {path}")
    observed = sha256_file(path)
    demand_equal(f"{label} SHA-256", observed, expected)
    return observed


def ordered_corpus_hash(paths: Sequence[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.read_bytes())
    return digest.hexdigest()


def decode_graph6(text: str) -> tuple[int, ...]:
    if not text or text != text.strip():
        raise AuditFailure("graph6 record has whitespace or is empty")
    values = [ord(character) - 63 for character in text]
    if any(value < 0 or value >= 64 for value in values):
        raise AuditFailure("graph6 record has an invalid byte")
    if values[0] != ORDER:
        raise AuditFailure("graph6 record is not order 43")
    payload = values[1:]
    if len(payload) != (EDGE_COUNT + 5) // 6:
        raise AuditFailure("graph6 record length is noncanonical")
    bits = [
        (value >> shift) & 1
        for value in payload
        for shift in range(5, -1, -1)
    ]
    if any(bits[EDGE_COUNT:]):
        raise AuditFailure("graph6 record has nonzero padding")
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
    if len(adjacency) != ORDER:
        raise AuditFailure("adjacency has wrong order")
    for vertex, row in enumerate(adjacency):
        if row & ~FULL_MASK or row & (1 << vertex):
            raise AuditFailure("adjacency is not a simple graph")
        for other in range(ORDER):
            if ((row >> other) & 1) != (
                (adjacency[other] >> vertex) & 1
            ):
                raise AuditFailure("adjacency is asymmetric")
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


def complement(adjacency: Sequence[int]) -> tuple[int, ...]:
    return tuple(
        FULL_MASK & ~(row | (1 << vertex))
        for vertex, row in enumerate(adjacency)
    )


def graph6_stream(path: Path, *, allow_empty: bool = False) -> list[str]:
    raw = path.read_bytes()
    if raw and not raw.endswith(b"\n"):
        raise AuditFailure(f"{path}: graph6 stream lacks a final newline")
    if b"\r" in raw:
        raise AuditFailure(f"{path}: graph6 stream has carriage returns")
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise AuditFailure(f"{path}: graph6 stream is not ASCII") from error
    if not lines:
        if allow_empty:
            return []
        raise AuditFailure(f"{path}: graph6 stream is empty")
    if any(not line or line.startswith("#") for line in lines):
        raise AuditFailure(f"{path}: graph6 stream has blank/comment lines")
    for line in lines:
        adjacency = decode_graph6(line)
        demand_equal("graph6 round trip", encode_graph6(adjacency), line)
    return lines


def five_cliques(adjacency: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    selected: list[int] = []
    result: list[tuple[int, ...]] = []

    def recurse(candidates: int) -> None:
        needed = 5 - len(selected)
        if candidates.bit_count() < needed:
            return
        if needed == 0:
            result.append(tuple(selected))
            return
        while candidates:
            if candidates.bit_count() < needed:
                return
            low = candidates & -candidates
            vertex = low.bit_length() - 1
            candidates ^= low
            selected.append(vertex)
            recurse(candidates & adjacency[vertex])
            selected.pop()

    recurse(FULL_MASK)
    return tuple(result)


def recount_e2_stream(lines: Sequence[str]) -> dict[str, object]:
    splits: collections.Counter[str] = collections.Counter()
    geometries: collections.Counter[str] = collections.Counter()
    digest = hashlib.sha256()
    for index, line in enumerate(lines):
        adjacency = decode_graph6(line)
        cliques = five_cliques(adjacency)
        independent = five_cliques(complement(adjacency))
        if len(cliques) + len(independent) != 2:
            raise AuditFailure(
                f"endpoint {index} recounts to "
                f"{len(cliques) + len(independent)}, not E=2"
            )
        split = f"{len(cliques)},{len(independent)}"
        splits[split] += 1
        selected = cliques if cliques else independent
        if len(selected) != 2:
            raise AuditFailure(f"endpoint {index} has mixed-colour conflicts")
        overlap = len(set(selected[0]) & set(selected[1]))
        geometry = f"same_colour_pair;overlap={overlap}"
        if overlap != 4:
            raise AuditFailure(
                f"endpoint {index} conflict overlap is {overlap}, not four"
            )
        geometries[geometry] += 1
        digest.update(f"{line} {split} {geometry}\n".encode("ascii"))
    return {
        "record_count": len(lines),
        "unique_record_count": len(set(lines)),
        "all_recount_to_E2": True,
        "conflict_split_counts": dict(sorted(splits.items())),
        "geometry_counts": dict(sorted(geometries.items())),
        "ordered_recount_sha256": digest.hexdigest(),
    }


VERBOSE_GROUP = re.compile(r"^\s*(\d+)\s*:\s*(.*)$")


def parse_shortg_verbose(text: str) -> tuple[tuple[int, ...], ...]:
    groups: list[list[int]] = []
    current: list[int] | None = None
    for raw_line in text.splitlines():
        match = VERBOSE_GROUP.match(raw_line)
        if match:
            current = [int(token) for token in match.group(2).split()]
            groups.append(current)
            continue
        stripped = raw_line.strip()
        if current is not None and stripped:
            tokens = stripped.split()
            if all(token.isdigit() for token in tokens):
                current.extend(int(token) for token in tokens)
                continue
        current = None
    return tuple(tuple(group) for group in groups)


def quotient_with_traces(
    *,
    shortg: Path,
    endpoints: Sequence[str],
    known: Sequence[str],
    representatives: Sequence[str],
    directory: Path,
) -> dict[str, object]:
    originals = [*endpoints, *known, *representatives]
    duals = [
        encode_graph6(complement(decode_graph6(line)))
        for line in originals
    ]
    combined = [*originals, *duals]
    input_path = directory / "traces_quotient.input.g6"
    output_path = directory / "traces_quotient.output.g6"
    input_path.write_text(
        "".join(line + "\n" for line in combined), encoding="ascii"
    )
    completed = subprocess.run(
        [
            str(shortg),
            "-t",
            "-v",
            "-g",
            str(input_path),
            str(output_path),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise AuditFailure(
            "shortg -t quotient failed:\n"
            + completed.stdout
            + "\n"
            + completed.stderr
        )
    groups = parse_shortg_verbose(
        completed.stdout + "\n" + completed.stderr
    )
    canonical_lines = output_path.read_text(encoding="ascii").splitlines()
    if len(groups) != len(canonical_lines):
        raise AuditFailure("shortg group/output class counts disagree")
    members = sorted(member for group in groups for member in group)
    if members != list(range(1, len(combined) + 1)):
        raise AuditFailure("shortg groups are not an exact input partition")
    for line in canonical_lines:
        demand_equal(
            "shortg canonical graph6 round trip",
            encode_graph6(decode_graph6(line)),
            line,
        )

    group_of = {
        member: group_index
        for group_index, group in enumerate(groups)
        for member in group
    }
    parent = list(range(len(groups)))

    def find(value: int) -> int:
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def union(left: int, right: int) -> None:
        left = find(left)
        right = find(right)
        if left != right:
            parent[right] = left

    count = len(originals)
    for index in range(count):
        union(group_of[1 + index], group_of[1 + count + index])

    endpoint_count = len(endpoints)
    known_start = endpoint_count
    representative_start = endpoint_count + len(known)
    endpoint_ordinary = {
        group_of[1 + index] for index in range(endpoint_count)
    }
    endpoint_roots = [
        find(group_of[1 + index]) for index in range(endpoint_count)
    ]
    known_roots = {
        find(group_of[1 + known_start + index])
        for index in range(len(known))
    }
    representative_roots = {
        find(group_of[1 + representative_start + index])
        for index in range(len(representatives))
    }
    endpoint_root_set = set(endpoint_roots)
    novel_flags = [root not in known_roots for root in endpoint_roots]
    class_sizes = collections.Counter(endpoint_roots)
    class_size_histogram = collections.Counter(class_sizes.values())
    partition_digest = hashlib.sha256()
    normalized_groups: dict[int, list[int]] = {}
    for index, root in enumerate(endpoint_roots):
        normalized_groups.setdefault(root, []).append(index)
    for group in sorted(tuple(values) for values in normalized_groups.values()):
        partition_digest.update(
            (",".join(map(str, group)) + "\n").encode("ascii")
        )
    if representative_roots != endpoint_root_set:
        raise AuditFailure(
            "published v2 representatives do not bind one-for-one to "
            "endpoint complement classes"
        )
    return {
        "method": "nauty Traces via shortg -t",
        "input_record_count_with_complements": len(combined),
        "augmented_ordinary_class_count": len(groups),
        "endpoint_ordinary_isomorphism_class_count": len(
            endpoint_ordinary
        ),
        "endpoint_complement_isomorphism_class_count": len(
            endpoint_root_set
        ),
        "known_complement_isomorphism_class_count": len(known_roots),
        "endpoint_complement_class_size_histogram": {
            str(key): value
            for key, value in sorted(class_size_histogram.items())
        },
        "novel_labeled_endpoint_count": sum(novel_flags),
        "novel_complement_isomorphism_class_count": len(
            {root for root, novel in zip(endpoint_roots, novel_flags) if novel}
        ),
        "representative_class_coverage_exact": True,
        "endpoint_complement_partition_sha256": (
            partition_digest.hexdigest()
        ),
        "shortg_stdout_sha256": hashlib.sha256(
            completed.stdout.encode("utf-8")
        ).hexdigest(),
        "shortg_stderr_sha256": hashlib.sha256(
            completed.stderr.encode("utf-8")
        ).hexdigest(),
        "shortg_canonical_output_sha256": sha256_file(output_path),
    }


def inspect_e1_semantics(source: str) -> dict[str, object]:
    normalized = re.sub(r"\s+", " ", source)
    checks = {
        "near_kind_declared": "kNearConstruction" in source,
        "near_output_option_parsed": (
            'option == "--near-output"' in source
            and "options.near_output = value();" in source
        ),
        "in_loop_E1_stop": bool(
            re.search(
                r"if \(objective == 1\) \{ "
                r"\+\+counters\.e1_visits; "
                r"return \{RolloutResult::kNearConstruction, graph, 1, step\}; "
                r"\}",
                normalized,
            )
        ),
        "terminal_E1_stop": bool(
            re.search(
                r"if \(objective == 1\) \{ "
                r"\+\+counters\.e1_visits; "
                r"return \{RolloutResult::kNearConstruction, graph, 1, "
                r"options\.steps_per_rollout\}; \}",
                normalized,
            )
        ),
        "double_mode_E1_exact_recount": (
            "low-double E=1 near-construction replay failed" in source
            and "all_conflicts(result.graph).size() != 1" in source
        ),
        "double_mode_E1_write": (
            "write_single_graph( options.near_output, code, "
            '"near-construction");' in normalized
        ),
        "double_mode_E1_exit_11": bool(
            re.search(
                r"if \(result\.kind == RolloutResult::kNearConstruction\) "
                r"\{.*?return 11; \}",
                normalized,
            )
        ),
        "both_forced_edges_initially_tabu": (
            "Edge additional_forced = {-1, -1}" in source
            and "tabu[edge_index[additional_forced.left]"
            "[additional_forced.right]] = options.tabu_tenure + 1;"
            in normalized
            and "counters, first.edge" in source
        ),
        "terminal_state_recount_present": (
            "const std::vector<Conflict> terminal_conflicts = "
            "all_conflicts(graph);" in normalized
        ),
    }
    if not all(checks.values()):
        failed = [key for key, value in checks.items() if not value]
        raise AuditFailure(
            "hash-bound E=1/source semantic inspection failed: "
            + ", ".join(failed)
        )
    return {
        **checks,
        "near_return_site_count": source.count(
            "RolloutResult::kNearConstruction, graph, 1"
        ),
        "E1_counter_increment_site_count": source.count(
            "++counters.e1_visits;"
        ),
    }


def compile_and_run_schedule_checker(
    *,
    source: Path,
    compiler: Path,
    e3: Path,
    e4: Path,
    known_directory: Path,
    directory: Path,
) -> tuple[dict[str, object], dict[str, object]]:
    binary = directory / "e2_double_forced_schedule_exact"
    compile_command = [
        str(compiler),
        "-std=c++20",
        "-O3",
        "-DNDEBUG",
        "-Wall",
        "-Wextra",
        "-pedantic",
        str(source),
        "-o",
        str(binary),
    ]
    compiled = subprocess.run(
        compile_command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if compiled.returncode != 0:
        raise AuditFailure(
            "independent schedule checker compilation failed:\n"
            + compiled.stdout
            + "\n"
            + compiled.stderr
        )
    if compiled.stdout or compiled.stderr:
        raise AuditFailure(
            "independent schedule checker compilation emitted diagnostics"
        )
    started = time.monotonic()
    completed = subprocess.run(
        [
            str(binary),
            "--e3",
            str(e3),
            "--e4",
            str(e4),
            "--known-directory",
            str(known_directory),
            "--ceiling",
            "80",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=300,
    )
    elapsed = time.monotonic() - started
    if completed.returncode != 0 or completed.stderr:
        raise AuditFailure(
            "independent exact schedule checker failed:\n"
            + completed.stdout
            + "\n"
            + completed.stderr
        )
    lines = completed.stdout.splitlines()
    if len(lines) != 1:
        raise AuditFailure("schedule checker did not emit exactly one record")
    try:
        result = json.loads(lines[0])
    except json.JSONDecodeError as error:
        raise AuditFailure("schedule checker emitted malformed JSON") from error
    if not isinstance(result, dict) or result.get("valid") is not True:
        raise AuditFailure("schedule checker did not report valid=true")
    compiler_version = subprocess.run(
        [str(compiler), "--version"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    ).stdout.splitlines()[0]
    return result, {
        "source_sha256": sha256_file(source),
        "binary_sha256": sha256_file(binary),
        "compiler": str(compiler.resolve()),
        "compiler_version_first_line": compiler_version,
        "compile_flags": compile_command[1:-2],
        "compile_diagnostics_empty": True,
        "runtime_seconds": elapsed,
        "exit_code": completed.returncode,
    }


def compare_schedule(
    schedule: dict[str, object], production: dict[str, object]
) -> None:
    pairs = {
        "low_seed_count": "low_seed_count",
        "low_seed_objective_distribution": (
            "low_seed_objective_distribution"
        ),
        "known_E2_state_count": "known_E2_state_count",
        "first_barrier_count": "first_barrier_count",
        "first_barrier_exact_replays": "first_barrier_exact_replays",
        "first_nonconflict_barrier_count": (
            "first_nonconflict_barrier_count"
        ),
        "first_high_conflict_barrier_count": (
            "first_high_conflict_barrier_count"
        ),
        "first_by_source_objective": "first_by_source_objective",
        "first_by_height": "first_by_height",
        "second_candidate_count": "second_candidate_count",
        "second_barrier_count": "second_barrier_count",
        "second_barrier_exact_replays": "second_barrier_exact_replays",
        "first_without_second_candidate_count": (
            "first_without_second_candidate_count"
        ),
        "second_by_height": "second_by_height",
        "second_delta_distribution": "second_delta_distribution",
        "objective_ceiling": "objective_ceiling",
    }
    for schedule_key, production_key in pairs.items():
        demand_equal(
            f"independent schedule {schedule_key}",
            schedule.get(schedule_key),
            production.get(production_key),
        )
    demand_equal(
        "independent neutral-cycle histogram",
        schedule.get("neutral_cycle_length_histogram"),
        {"86": 22},
    )


def run_frozen_search_replay(
    *,
    binary: Path,
    plan: dict[str, object],
    production: dict[str, object],
    known_paths: Sequence[Path],
    e3: Path,
    e4: Path,
    frozen_endpoints: Path,
    project_root: Path,
    directory: Path,
) -> dict[str, object]:
    repair = plan["repair"]
    first = plan["first_barrier_schedule"]
    second = plan["second_barrier_schedule"]
    if not isinstance(repair, dict) or not isinstance(first, dict) or not isinstance(
        second, dict
    ):
        raise AuditFailure("search plan schedule/repair sections are malformed")
    replay_e2 = directory / "replay_E2.g6"
    replay_e1 = directory / "replay_E1.g6"
    command = [str(binary)]
    for path in known_paths:
        command.extend(["--seed-graph", str(path)])
    command.extend(
        [
            "--low-seed-file",
            str(e3),
            "--low-seed-file",
            str(e4),
            "--low-double-barrier",
            "--seed",
            str(repair["seed"]),
            "--rollouts-per-barrier",
            str(repair["rollouts_per_second_barrier"]),
            "--steps",
            str(repair["steps_per_rollout"]),
            "--tabu",
            str(repair["tabu_tenure"]),
            "--noise-per-million",
            str(repair["noise_per_million"]),
            "--objective-ceiling",
            str(repair["objective_ceiling"]),
            "--low-barriers-per-seed",
            str(first["per_seed_limit"]),
            "--low-second-barriers-per-first",
            str(second["barriers_per_first"]),
            "--progress-interval",
            str(repair["progress_interval"]),
            "--discovery-output",
            str(replay_e2),
            "--near-output",
            str(replay_e1),
        ]
    )
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=project_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=600,
    )
    elapsed = time.monotonic() - started
    if completed.returncode != 0:
        raise AuditFailure(
            "frozen search replay returned nonzero:\n"
            + completed.stdout
            + "\n"
            + completed.stderr
        )
    stdout_lines = completed.stdout.splitlines()
    if len(stdout_lines) != 1:
        raise AuditFailure("frozen search replay emitted != 1 stdout record")
    try:
        replay = json.loads(stdout_lines[0])
    except json.JSONDecodeError as error:
        raise AuditFailure("frozen search replay emitted malformed JSON") from error
    if not isinstance(replay, dict):
        raise AuditFailure("frozen search replay JSON is not an object")
    excluded = {
        "binding",
        "runtime_seconds",
        "discovery_output",
        "near_output",
    }
    production_keys = set(production) - excluded
    replay_keys = set(replay) - excluded
    demand_equal("search replay key set", replay_keys, production_keys)
    for key in sorted(production_keys):
        demand_equal(
            f"search replay field {key}",
            replay.get(key),
            production.get(key),
        )
    if replay_e1.exists():
        raise AuditFailure("frozen replay unexpectedly created an E=1 output")
    demand_hash(
        "frozen replay E=2 stream",
        replay_e2,
        EXPECTED_HASHES["endpoint_stream"],
    )
    if replay_e2.read_bytes() != frozen_endpoints.read_bytes():
        raise AuditFailure("replay E=2 bytes differ despite hash check")
    progress_lines = [
        line
        for line in completed.stderr.splitlines()
        if line.startswith("low_double_progress ")
    ]
    unexpected_stderr = [
        line
        for line in completed.stderr.splitlines()
        if line and not line.startswith("low_double_progress ")
    ]
    if unexpected_stderr:
        raise AuditFailure(
            "search replay emitted unexpected diagnostics: "
            + repr(unexpected_stderr)
        )
    return {
        "performed": True,
        "exit_code": completed.returncode,
        "runtime_seconds": elapsed,
        "stdout_record_count": len(stdout_lines),
        "progress_record_count": len(progress_lines),
        "all_nonruntime_result_fields_match": True,
        "E1_visits": replay.get("E1_visits"),
        "E1_output_exists": False,
        "E0_found": replay.get("E0_found"),
        "E2_output_line_count": len(graph6_stream(replay_e2)),
        "E2_output_sha256": sha256_file(replay_e2),
        "E2_output_byte_identical": True,
    }


def validate_search_aggregates(
    *,
    plan: dict[str, object],
    result: dict[str, object],
    endpoint_count: int,
    near_path: Path,
) -> dict[str, object]:
    for key, expected in EXPECTED_SEARCH_FIELDS.items():
        demand_equal(f"search result {key}", result.get(key), expected)
    for histogram_key, total_key in (
        ("first_by_height", "first_barrier_count"),
        ("second_by_height", "second_barrier_count"),
        ("second_delta_distribution", "second_barrier_count"),
        ("first_by_source_objective", "first_barrier_count"),
        ("terminal_best_distribution", "rollouts"),
    ):
        histogram = result.get(histogram_key)
        if not isinstance(histogram, dict):
            raise AuditFailure(f"{histogram_key} is not an object")
        demand_equal(
            f"sum({histogram_key})",
            sum(histogram.values()),
            result.get(total_key),
        )
    demand_equal(
        "first schedule category sum",
        result["first_nonconflict_barrier_count"]
        + result["first_high_conflict_barrier_count"],
        result["first_barrier_count"],
    )
    demand_equal(
        "rollout count from selected barriers",
        result["second_barrier_count"] * result["rollouts_per_barrier"],
        result["rollouts"],
    )
    demand_equal(
        "exact objective checks identity",
        result["steps"] + result["rollouts"],
        result["exact_objective_checks"],
    )
    demand_equal(
        "terminal outcome count",
        result["exhausted"]
        + result["terminal_best_distribution"]["2"],
        result["rollouts"],
    )
    demand_equal(
        "endpoint line count/result unique count",
        endpoint_count,
        result["new_E2_unique_count"],
    )
    if near_path.exists():
        raise AuditFailure("frozen E=1 output path exists despite E1_visits=0")
    binding = result.get("binding")
    if not isinstance(binding, dict):
        raise AuditFailure("search result binding is missing")
    demand_equal("binding exit code", binding.get("exit_code"), 0)
    demand_equal(
        "binding plan hash",
        binding.get("plan_sha256"),
        EXPECTED_HASHES["search_plan"],
    )
    demand_equal(
        "binding source hash",
        binding.get("source_sha256"),
        EXPECTED_HASHES["search_source"],
    )
    demand_equal(
        "binding binary hash",
        binding.get("binary_sha256"),
        EXPECTED_HASHES["search_binary"],
    )
    demand_equal(
        "binding endpoint count",
        binding.get("E2_output_line_count"),
        endpoint_count,
    )
    demand_equal(
        "binding endpoint hash",
        binding.get("E2_output_sha256"),
        EXPECTED_HASHES["endpoint_stream"],
    )
    demand_equal(
        "binding E1 absence", binding.get("E1_output_exists"), False
    )
    demand_equal("plan status", plan.get("status"), "FROZEN_BEFORE_PRODUCTION")
    return {
        "all_hard_coded_fields_match": True,
        "histogram_sums_match": True,
        "first_category_partition_matches": True,
        "rollout_count_identity_matches": True,
        "exact_objective_check_identity_matches": True,
        "terminal_outcome_identity_matches": True,
        "result_binding_matches": True,
        "frozen_E1_output_absent": True,
    }


def resolve_from_project(project_root: Path, value: object) -> Path:
    if not isinstance(value, str):
        raise AuditFailure("planned artifact path is not a string")
    path = Path(value)
    return path if path.is_absolute() else project_root / path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--shortg", type=Path, required=True)
    parser.add_argument(
        "--compiler",
        type=Path,
        default=Path(shutil.which("clang++") or "clang++"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project_root = args.project_root.resolve()

    paths = {
        "search_plan": (
            project_root
            / "results/benchmark_plans/e2_low_closure_double_forced_v1.json"
        ),
        "search_result": (
            project_root
            / "results/constructive/e2_low_closure_v2/"
            "double_forced.result.json"
        ),
        "search_source": (
            project_root / "src/search43_e2_barrier_escape.cpp"
        ),
        "search_binary": (
            project_root / "build/search43_e2_barrier_escape"
        ),
        "e3_representatives": (
            project_root
            / "results/constructive/e2_low_closure_v2/"
            "representatives.e3.g6"
        ),
        "e4_representatives": (
            project_root
            / "results/constructive/e2_low_closure_v2/"
            "representatives.e4.g6"
        ),
        "quotient_audit": (
            project_root
            / "results/verification/e2_low_closure_isomorphism_audit_v1.json"
        ),
        "endpoint_stream": (
            project_root
            / "results/constructive/e2_low_closure_v2/"
            "double_forced_new_E2.g6"
        ),
        "endpoint_audit_source": (
            project_root / "src/e2_second_barrier_discovery_audit.py"
        ),
        "endpoint_audit_tests": (
            project_root
            / "tests/e2_second_barrier_discovery_audit_tests.py"
        ),
        "endpoint_audit_v1_plan": (
            project_root
            / "results/benchmark_plans/"
            "e2_double_forced_discovery_audit_v1.json"
        ),
        "endpoint_audit_v1_result": (
            project_root
            / "results/verification/"
            "e2_double_forced_discovery_audit_v1.json"
        ),
        "endpoint_audit_v2_plan": (
            project_root
            / "results/benchmark_plans/"
            "e2_double_forced_discovery_audit_v2.json"
        ),
        "endpoint_audit_v2_result": (
            project_root
            / "results/verification/"
            "e2_double_forced_discovery_audit_v2.json"
        ),
        "endpoint_representatives_v1": (
            project_root
            / "results/constructive/e2_low_closure_v2/"
            "double_forced_E2_representatives.g6"
        ),
        "endpoint_representatives_v2": (
            project_root
            / "results/constructive/e2_low_closure_v2/"
            "double_forced_E2_representatives_v2.g6"
        ),
        "novel_representatives_v1": (
            project_root
            / "results/constructive/e2_low_closure_v2/"
            "double_forced_E2_novel_representatives.g6"
        ),
        "novel_representatives_v2": (
            project_root
            / "results/constructive/e2_low_closure_v2/"
            "double_forced_E2_novel_representatives_v2.g6"
        ),
        "schedule_checker_source": (
            project_root / "verify/e2_double_forced_schedule_exact.cpp"
        ),
    }

    recorded_hashes: dict[str, str] = {}
    for label in (
        "search_plan",
        "search_result",
        "search_source",
        "search_binary",
        "e3_representatives",
        "e4_representatives",
        "quotient_audit",
        "endpoint_stream",
        "endpoint_audit_source",
        "endpoint_audit_tests",
        "endpoint_audit_v1_plan",
        "endpoint_audit_v1_result",
        "endpoint_audit_v2_plan",
        "endpoint_audit_v2_result",
    ):
        recorded_hashes[label] = demand_hash(
            label, paths[label], EXPECTED_HASHES[label]
        )
    for label in ("endpoint_representatives_v1", "endpoint_representatives_v2"):
        recorded_hashes[label] = demand_hash(
            label,
            paths[label],
            EXPECTED_HASHES["endpoint_representatives"],
        )
    for label in ("novel_representatives_v1", "novel_representatives_v2"):
        recorded_hashes[label] = demand_hash(
            label, paths[label], EXPECTED_HASHES["empty_stream"]
        )
    recorded_hashes["shortg_traces"] = demand_hash(
        "shortg Traces", args.shortg, EXPECTED_HASHES["shortg_traces"]
    )

    known_directory = (
        project_root
        / "results/constructive/catalog_seed_search_stratified_v1"
    )
    known_paths = sorted(known_directory.glob("line_*.g6"))
    demand_equal("known E=2 seed file count", len(known_paths), 22)
    known_corpus_hash = ordered_corpus_hash(known_paths)
    demand_equal(
        "ordered known E=2 corpus SHA-256",
        known_corpus_hash,
        EXPECTED_HASHES["known_e2_corpus"],
    )
    known_lines: list[str] = []
    for path in known_paths:
        lines = graph6_stream(path)
        demand_equal(f"{path} graph count", len(lines), 1)
        known_lines.extend(lines)

    search_plan = strict_json_load(paths["search_plan"])
    search_result = strict_json_load(paths["search_result"])
    v1_plan = strict_json_load(paths["endpoint_audit_v1_plan"])
    v1_result = strict_json_load(paths["endpoint_audit_v1_result"])
    v2_plan = strict_json_load(paths["endpoint_audit_v2_plan"])
    v2_result = strict_json_load(paths["endpoint_audit_v2_result"])

    plan_input = search_plan.get("input")
    plan_implementation = search_plan.get("implementation")
    plan_repair = search_plan.get("repair")
    if not all(
        isinstance(value, dict)
        for value in (plan_input, plan_implementation, plan_repair)
    ):
        raise AuditFailure("search plan has malformed binding sections")
    assert isinstance(plan_input, dict)
    assert isinstance(plan_implementation, dict)
    assert isinstance(plan_repair, dict)
    demand_equal(
        "plan quotient audit hash",
        plan_input.get("quotient_audit_sha256"),
        EXPECTED_HASHES["quotient_audit"],
    )
    demand_equal(
        "plan E3 hash",
        plan_input.get("E3_representatives_sha256"),
        EXPECTED_HASHES["e3_representatives"],
    )
    demand_equal(
        "plan E4 hash",
        plan_input.get("E4_representatives_sha256"),
        EXPECTED_HASHES["e4_representatives"],
    )
    demand_equal(
        "plan known corpus hash",
        plan_input.get("known_E2_seed_corpus_concatenated_sha256"),
        EXPECTED_HASHES["known_e2_corpus"],
    )
    demand_equal(
        "plan source hash",
        plan_implementation.get("source_sha256"),
        EXPECTED_HASHES["search_source"],
    )
    demand_equal(
        "plan binary hash",
        plan_implementation.get("binary_sha256"),
        EXPECTED_HASHES["search_binary"],
    )
    source_semantics = inspect_e1_semantics(
        paths["search_source"].read_text(encoding="utf-8")
    )

    endpoints = graph6_stream(paths["endpoint_stream"])
    demand_equal("endpoint record count", len(endpoints), 1_878)
    demand_equal("endpoint uniqueness", len(set(endpoints)), len(endpoints))
    endpoint_recount = recount_e2_stream(endpoints)
    representatives_v1 = graph6_stream(paths["endpoint_representatives_v1"])
    representatives_v2 = graph6_stream(paths["endpoint_representatives_v2"])
    demand_equal(
        "v1/v2 representative bytes",
        paths["endpoint_representatives_v1"].read_bytes(),
        paths["endpoint_representatives_v2"].read_bytes(),
    )
    demand_equal("v2 representative count", len(representatives_v2), 2)
    representative_recount = recount_e2_stream(representatives_v2)
    demand_equal(
        "v1 novel representative stream",
        graph6_stream(paths["novel_representatives_v1"], allow_empty=True),
        [],
    )
    demand_equal(
        "v2 novel representative stream",
        graph6_stream(paths["novel_representatives_v2"], allow_empty=True),
        [],
    )

    # Preserve and bind both audit generations.  V1's amendment records the
    # stale inherited prose; V2 is a new corrected artifact and supersedes it
    # without overwriting either V1 file.
    if not isinstance(v1_plan.get("amendment"), dict):
        raise AuditFailure("v1 endpoint plan lacks its stale-prose amendment")
    supersedes = v2_plan.get("supersedes")
    if not isinstance(supersedes, dict):
        raise AuditFailure("v2 endpoint plan lacks supersession metadata")
    demand_equal(
        "v2 superseded plan",
        supersedes.get("plan"),
        "results/benchmark_plans/e2_double_forced_discovery_audit_v1.json",
    )
    for audit_result, label in ((v1_result, "v1"), (v2_result, "v2")):
        demand_equal(f"{label} endpoint audit valid", audit_result.get("valid"), True)
        demand_equal(
            f"{label} discovery count",
            audit_result.get("discovery_count"),
            1_878,
        )
        demand_equal(
            f"{label} discovery hash",
            audit_result.get("discovery_sha256"),
            EXPECTED_HASHES["endpoint_stream"],
        )
        demand_equal(
            f"{label} ordinary class count",
            audit_result.get("discovery_ordinary_isomorphism_class_count"),
            4,
        )
        demand_equal(
            f"{label} complement class count",
            audit_result.get("discovery_complement_isomorphism_class_count"),
            2,
        )
        demand_equal(
            f"{label} complement class histogram",
            audit_result.get("discovery_complement_class_size_histogram"),
            {"930": 1, "948": 1},
        )
        demand_equal(
            f"{label} novel complement class count",
            audit_result.get("novel_complement_isomorphism_class_count"),
            0,
        )
        boundary = audit_result.get("claim_boundary")
        if not isinstance(boundary, str) or "1,878 retained" not in boundary:
            raise AuditFailure(f"{label} claim boundary is not corrected")

    aggregate_checks = validate_search_aggregates(
        plan=search_plan,
        result=search_result,
        endpoint_count=len(endpoints),
        near_path=resolve_from_project(
            project_root, plan_repair.get("E1_output")
        ),
    )

    with tempfile.TemporaryDirectory(
        prefix="ramsey55-double-forced-independent."
    ) as temporary_name:
        temporary = Path(temporary_name)
        schedule, schedule_tool = compile_and_run_schedule_checker(
            source=paths["schedule_checker_source"],
            compiler=args.compiler,
            e3=paths["e3_representatives"],
            e4=paths["e4_representatives"],
            known_directory=known_directory,
            directory=temporary,
        )
        compare_schedule(schedule, search_result)
        quotient = quotient_with_traces(
            shortg=args.shortg,
            endpoints=endpoints,
            known=known_lines,
            representatives=representatives_v2,
            directory=temporary,
        )
        demand_equal(
            "independent endpoint ordinary class count",
            quotient["endpoint_ordinary_isomorphism_class_count"],
            4,
        )
        demand_equal(
            "independent endpoint complement class count",
            quotient["endpoint_complement_isomorphism_class_count"],
            2,
        )
        demand_equal(
            "independent endpoint class-size histogram",
            quotient["endpoint_complement_class_size_histogram"],
            {"930": 1, "948": 1},
        )
        demand_equal(
            "independent novel labeled endpoint count",
            quotient["novel_labeled_endpoint_count"],
            0,
        )
        demand_equal(
            "independent novel complement class count",
            quotient["novel_complement_isomorphism_class_count"],
            0,
        )
        replay = run_frozen_search_replay(
            binary=paths["search_binary"],
            plan=search_plan,
            production=search_result,
            known_paths=known_paths,
            e3=paths["e3_representatives"],
            e4=paths["e4_representatives"],
            frozen_endpoints=paths["endpoint_stream"],
            project_root=project_root,
            directory=temporary,
        )

    result = {
        "schema": SCHEMA,
        "status": (
            "VALID_EXACT_FORCED_SCHEDULE_AND_REPRODUCIBLE_HEURISTIC_OUTCOME"
        ),
        "evidence_label": "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
        "valid": True,
        "checker_source_sha256": sha256_file(Path(__file__)),
        "schedule_checker_source_sha256": sha256_file(
            paths["schedule_checker_source"]
        ),
        "artifact_hashes": recorded_hashes,
        "known_E2_corpus": {
            "seed_file_count": len(known_paths),
            "ordered_concatenated_sha256": known_corpus_hash,
        },
        "plan_and_result_aggregate_checks": aggregate_checks,
        "source_semantics": source_semantics,
        "exact_schedule_reconstruction": schedule,
        "exact_schedule_tool": schedule_tool,
        "endpoint_recount": endpoint_recount,
        "representative_recount": representative_recount,
        "independent_traces_quotient": quotient,
        "endpoint_audit_generation_binding": {
            "v1_plan_preserved": True,
            "v1_result_preserved": True,
            "v1_amendment_records_stale_inherited_prose": True,
            "v2_plan_preserved": True,
            "v2_result_preserved": True,
            "v2_claim_boundary_uses_actual_counts": True,
            "v1_v2_representative_streams_byte_identical": True,
        },
        "frozen_binary_replay": replay,
        "conclusions": {
            "all_47675_first_barriers_reconstructed": True,
            "all_39511631_second_candidates_reconstructed": True,
            "all_selected_first_and_second_graphs_exactly_recounted": True,
            "all_1878_E2_endpoints_exactly_recounted": True,
            "endpoint_quotient_is_four_ordinary_two_complement_classes": True,
            "zero_novel_classes_relative_to_supplied_22_seed_corpus": True,
            "deterministic_replay_E2_stream_byte_identical": True,
            "deterministic_replay_observed_no_E1_or_E0": True,
        },
        "claim_boundary": (
            "The two forced schedules are exact finite enumerations relative "
            "to the 53 supplied low-frontier representatives and their "
            "stated edge rules. The subsequent 256-step tabu repairs are "
            "heuristic. This audit reproduces their recorded negative search "
            "outcome but proves no global nonexistence statement and does "
            "not change 43 <= R(5,5) <= 46."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AuditFailure as error:
        print(f"FAIL-CLOSED: {error}", file=os.sys.stderr)
        raise SystemExit(2)
