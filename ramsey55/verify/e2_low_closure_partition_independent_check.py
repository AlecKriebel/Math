#!/usr/bin/env python3
"""Independent audit of the exported E=3/E=4 low-conflict closure.

This checker intentionally imports none of the production graph, search, or
quotient modules.  It:

* decodes and re-encodes every graph6 record independently;
* reconstructs file hashes, record counts, uniqueness, and complementation;
* uses ``shortg -t`` (the Traces engine) rather than the published audit's
  dense/sparse ``labelg`` route;
* feeds each raw stream, its complement, and the published representatives
  through one augmented Traces partition, binding every representative to
  exactly one complement-isomorphism class;
* independently enumerates every K5 and I5 in all 53 representatives; and
* independently reconstructs the frozen all-53 first-barrier schedule.

The finite-corpus classification is exact relative to the supplied streams.
Neither it nor the later heuristic repair search is a Ramsey nonexistence
proof.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence


ORDER = 43
EDGE_COUNT = ORDER * (ORDER - 1) // 2
FULL_MASK = (1 << ORDER) - 1
SCHEMA = "ramsey55.e2_low_closure_partition_independent_check.v2"

EXPECTED_HASHES = {
    "e3_stream": (
        "e592a201aa862c62ed98fdb7a3442665fe625f44da8b4586f6fd759580426c58"
    ),
    "e4_stream": (
        "62baebe26a52f34b677ef6f6b1b07a21bc1e19a44a8f20ff9939d82c751a9f04"
    ),
    "e3_representatives": (
        "0f9485a82ecb6dba9b19ea0759ba37ef7c9bc64d481cf8fd7a248480b348471d"
    ),
    "e4_representatives": (
        "2ea9964afed1205884e971fb50fce77d783925804ae9d1064460e7b89190bca4"
    ),
    "published_audit": (
        "cd1f8a9e56e76b0c94df1c5705ca7090588e2eb12a2bd0009f3e53e115f47725"
    ),
    "quotient_plan": (
        "aa57d82dd10b297c33ad92a66f9f16fb1a5b34404302f43e1fe714602befa654"
    ),
    "export_result": (
        "1315e444b3edf91e763b3739b96431c1305331d8c7746495ef339c0844d75864"
    ),
    "second_barrier_plan": (
        "edb75ba318df551b370112867443a1502438eaba4bda9971caf079b3f8bc42c3"
    ),
    "prior_second_barrier_plan": (
        "ebbe4ce7d5a6b9027651fe0e1d2ca70b729eda5545b6f84a44e3c5291ec8cac7"
    ),
    "initial_invalid_audit": (
        "0a83743f5c04011efefa6f201c3c87332805d4ffa0216826de9901455f27aed8"
    ),
    "known_e2_seed_audit": (
        "07969bcbbfb62fcd1e40ef3d2fb718816b1f5630c71db67c9e9a53322ed2be7b"
    ),
    "search_source": (
        "cdddaef4c35dfb9ccdbcc7478029c15eb909247714ffc2bef9e8fa636fb0099c"
    ),
    "search_binary": (
        "4597c7fb130edbf75c9a192a2042f44acda0a897193fcef22af98b56165b0a34"
    ),
    "shortg_traces": (
        "d31954e657d682802ea4d1f881cad175066b3a8ed624e91e4bfa9b8eb94d39d8"
    ),
    "production_result": (
        "4969871cccbd0e07edf169fd468aafa2a3584f176ba858d706d104fc77d60da4"
    ),
    "discovery_stream": (
        "ba35df48ba6577605135fda1c893283b76420724bd9ff70b4c0641427ec96e97"
    ),
    "discovery_audit": (
        "fae8b82dd05df36cfc353848fb0c1ebd3f049c8975b3e02bf237d2a0ea06f2b1"
    ),
    "discovery_representatives": (
        "94c052a7a5bcabcd7df9fa9c1246a2344846d4875ecb4fe0294651388513a205"
    ),
    "known_e2_class_representatives": (
        "376fce9067c2d50da09c6eaa5df40b03ce96768bcdc4273fffef93eefc1eea48"
    ),
}

EXPECTED = {
    3: {
        "stream_count": 16_082,
        "representative_count": 9,
        "ordinary_count": 18,
        "ordinary_histogram": {"43": 1, "86": 8, "903": 1, "1806": 8},
        "complement_histogram": {"946": 1, "1892": 8},
        "split_counts": {"1,2": 4, "2,1": 1, "3,0": 4},
    },
    4: {
        "stream_count": 73_788,
        "representative_count": 44,
        "ordinary_count": 88,
        "ordinary_histogram": {"43": 10, "86": 34, "903": 10, "1806": 34},
        "complement_histogram": {"946": 10, "1892": 34},
        "split_counts": {"0,4": 2, "2,2": 23, "4,0": 19},
    },
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def decode_graph6(text: str) -> tuple[int, ...]:
    """Independently decode canonical short graph6 for one order-43 graph."""

    if not text or text != text.strip():
        raise ValueError("graph6 record has surrounding whitespace")
    values = [ord(character) - 63 for character in text]
    if any(value < 0 or value >= 64 for value in values):
        raise ValueError("graph6 record contains an invalid byte")
    if values[0] != ORDER:
        raise ValueError("graph6 record does not have order 43")
    needed = EDGE_COUNT
    payload = values[1:]
    if len(payload) != (needed + 5) // 6:
        raise ValueError("graph6 payload length is not canonical")
    bits = [
        (value >> shift) & 1
        for value in payload
        for shift in range(5, -1, -1)
    ]
    if any(bits[needed:]):
        raise ValueError("graph6 record has nonzero padding")
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
    payload = []
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


def read_graph6_stream(path: Path) -> tuple[list[str], dict[str, object]]:
    raw = path.read_bytes()
    if not raw.endswith(b"\n"):
        raise ValueError(f"{path}: stream has no final newline")
    if b"\r" in raw:
        raise ValueError(f"{path}: stream contains carriage returns")
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as error:
        raise ValueError(f"{path}: stream is not ASCII") from error
    if not lines or any(not line or line.startswith("#") for line in lines):
        raise ValueError(f"{path}: stream has blank/comment records")
    if len(set(lines)) != len(lines):
        raise ValueError(f"{path}: stream repeats a labeled graph")
    edge_histogram: Counter[int] = Counter()
    degree_sequence_digest = hashlib.sha256()
    complement_digest = hashlib.sha256()
    for index, line in enumerate(lines):
        adjacency = decode_graph6(line)
        if encode_graph6(adjacency) != line:
            raise ValueError(f"{path}: graph6 round trip failed at {index}")
        edge_count = sum(row.bit_count() for row in adjacency) // 2
        edge_histogram[edge_count] += 1
        degrees = sorted(row.bit_count() for row in adjacency)
        degree_sequence_digest.update(
            (",".join(map(str, degrees)) + "\n").encode("ascii")
        )
        dual = graph_complement(adjacency)
        if graph_complement(dual) != adjacency:
            raise AssertionError("complement is not an involution")
        complement_digest.update((encode_graph6(dual) + "\n").encode("ascii"))
    return lines, {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "record_count": len(lines),
        "unique": True,
        "graph6_round_trip_all": True,
        "complement_involution_all": True,
        "edge_count_histogram": {
            str(key): value for key, value in sorted(edge_histogram.items())
        },
        "ordered_degree_sequences_sha256": degree_sequence_digest.hexdigest(),
        "ordered_complements_sha256": complement_digest.hexdigest(),
    }


def iter_k_cliques(
    adjacency: Sequence[int], size: int
) -> Iterable[tuple[int, ...]]:
    selected: list[int] = []

    def recurse(candidates: int) -> Iterable[tuple[int, ...]]:
        needed = size - len(selected)
        if candidates.bit_count() < needed:
            return
        if needed == 0:
            yield tuple(selected)
            return
        while candidates:
            if candidates.bit_count() < needed:
                return
            low = candidates & -candidates
            vertex = low.bit_length() - 1
            candidates ^= low
            selected.append(vertex)
            yield from recurse(candidates & adjacency[vertex])
            selected.pop()

    yield from recurse(FULL_MASK)


def conflicts(
    adjacency: Sequence[int],
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    clique = tuple(iter_k_cliques(adjacency, 5))
    independent = tuple(iter_k_cliques(graph_complement(adjacency), 5))
    return clique, independent


def triangle_count(adjacency: Sequence[int], vertices: int) -> int:
    total = 0
    remaining_left = vertices
    while remaining_left:
        left_bit = remaining_left & -remaining_left
        left = left_bit.bit_length() - 1
        remaining_left ^= left_bit
        neighbors_left = remaining_left & adjacency[left]
        remaining_right = neighbors_left
        while remaining_right:
            right_bit = remaining_right & -remaining_right
            right = right_bit.bit_length() - 1
            remaining_right ^= right_bit
            total += (
                neighbors_left
                & adjacency[right]
                & ~((1 << (right + 1)) - 1)
            ).bit_count()
    return total


def exact_post_flip_height(
    adjacency: Sequence[int],
    clique_conflicts: Sequence[Sequence[int]],
    independent_conflicts: Sequence[Sequence[int]],
    left: int,
    right: int,
) -> int:
    """Compute the exact post-toggle conflict count from first principles."""

    if not 0 <= left < right < ORDER:
        raise ValueError("edge endpoints are invalid")
    present = bool(adjacency[left] & (1 << right))
    selected_conflicts = clique_conflicts if present else independent_conflicts
    destroyed = sum(
        left in conflict and right in conflict
        for conflict in selected_conflicts
    )
    excluded = FULL_MASK & ~((1 << left) | (1 << right))
    if present:
        dual = graph_complement(adjacency)
        common = dual[left] & dual[right] & excluded
        created = triangle_count(dual, common)
    else:
        common = adjacency[left] & adjacency[right] & excluded
        created = triangle_count(adjacency, common)
    return (
        len(clique_conflicts)
        + len(independent_conflicts)
        - destroyed
        + created
    )


def toggled(adjacency: Sequence[int], left: int, right: int) -> tuple[int, ...]:
    result = list(adjacency)
    result[left] ^= 1 << right
    result[right] ^= 1 << left
    return tuple(result)


VERBOSE_CLASS = re.compile(r"^\s*(\d+)\s*:\s*(.*)$")


def parse_shortg_verbose(text: str) -> tuple[tuple[int, ...], ...]:
    groups: list[list[int]] = []
    current: list[int] | None = None
    for raw_line in text.splitlines():
        match = VERBOSE_CLASS.match(raw_line)
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


def partition_sha256(groups: Sequence[Sequence[int]]) -> str:
    normalized = sorted(tuple(sorted(group)) for group in groups)
    payload = "".join(
        ",".join(map(str, group)) + "\n" for group in normalized
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def histogram(values: Iterable[int]) -> dict[str, int]:
    counts = Counter(values)
    return {str(key): counts[key] for key in sorted(counts)}


def run_traces_partition(
    shortg: Path,
    lines: Sequence[str],
    directory: Path,
    tag: str,
) -> dict[str, object]:
    input_path = directory / f"{tag}.input.g6"
    output_path = directory / f"{tag}.output.g6"
    input_path.write_text(
        "".join(line + "\n" for line in lines), encoding="ascii"
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
        raise RuntimeError(
            f"shortg -t failed for {tag}: "
            f"{completed.stdout}\n{completed.stderr}"
        )
    groups = parse_shortg_verbose(
        completed.stdout + "\n" + completed.stderr
    )
    output_lines = output_path.read_text(encoding="ascii").splitlines()
    if len(groups) != len(output_lines):
        raise RuntimeError(
            f"shortg verbose/output class count differs for {tag}"
        )
    members = sorted(member for group in groups for member in group)
    if members != list(range(1, len(lines) + 1)):
        raise RuntimeError(f"shortg membership is not a partition for {tag}")
    for line in output_lines:
        adjacency = decode_graph6(line)
        if encode_graph6(adjacency) != line:
            raise RuntimeError(f"shortg emitted malformed graph6 for {tag}")
    return {
        "groups": groups,
        "class_count": len(groups),
        "class_size_histogram": histogram(len(group) for group in groups),
        "partition_sha256": partition_sha256(groups),
        "canonical_output_sha256": hashlib.sha256(
            "".join(line + "\n" for line in output_lines).encode("ascii")
        ).hexdigest(),
    }


def analyze_augmented_partition(
    groups: Sequence[Sequence[int]],
    raw_count: int,
    representative_count: int,
) -> dict[str, object]:
    offsets = {
        "raw": (1, raw_count),
        "raw_complements": (raw_count + 1, 2 * raw_count),
        "representatives": (
            2 * raw_count + 1,
            2 * raw_count + representative_count,
        ),
        "representative_complements": (
            2 * raw_count + representative_count + 1,
            2 * raw_count + 2 * representative_count,
        ),
    }

    def in_range(member: int, label: str) -> bool:
        low, high = offsets[label]
        return low <= member <= high

    group_of: dict[int, int] = {}
    for group_index, group in enumerate(groups):
        for member in group:
            if member in group_of:
                raise ValueError("augmented ordinary groups overlap")
            group_of[member] = group_index
    expected_members = 2 * raw_count + 2 * representative_count
    if sorted(group_of) != list(range(1, expected_members + 1)):
        raise ValueError("augmented ordinary groups omit an input record")

    # Traces computes ordinary isomorphism.  Complement-isomorphism is the
    # quotient obtained by joining the ordinary class of each graph to the
    # ordinary class of its explicitly supplied complement.
    parent = list(range(len(groups)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    for raw_index in range(raw_count):
        union(
            group_of[1 + raw_index],
            group_of[1 + raw_count + raw_index],
        )
    for representative_index in range(representative_count):
        union(
            group_of[1 + 2 * raw_count + representative_index],
            group_of[
                1
                + 2 * raw_count
                + representative_count
                + representative_index
            ],
        )
    component_groups: dict[int, list[int]] = {}
    for group_index in range(len(groups)):
        component_groups.setdefault(find(group_index), []).append(group_index)

    raw_groups: list[tuple[int, ...]] = []
    representative_indices: list[int] = []
    binding_rows: list[dict[str, int]] = []
    valid = len(component_groups) == representative_count
    for ordinary_group_indices in component_groups.values():
        component_members = [
            member
            for group_index in ordinary_group_indices
            for member in groups[group_index]
        ]
        raw = tuple(
            sorted(
                member
                for member in component_members
                if in_range(member, "raw")
            )
        )
        dual_count = sum(
            in_range(member, "raw_complements")
            for member in component_members
        )
        representatives = [
            member - offsets["representatives"][0]
            for member in component_members
            if in_range(member, "representatives")
        ]
        representative_duals = [
            member - offsets["representative_complements"][0]
            for member in component_members
            if in_range(member, "representative_complements")
        ]
        valid = valid and (
            bool(raw)
            and len(raw) == dual_count
            and len(ordinary_group_indices) == 2
            and len(representatives) == 1
            and len(representative_duals) == 1
            and representatives == representative_duals
        )
        if representatives:
            representative_indices.extend(representatives)
        raw_groups.append(raw)
        binding_rows.append(
            {
                "raw_record_count": len(raw),
                "raw_complement_record_count": dual_count,
                "ordinary_class_count": len(ordinary_group_indices),
                "representative_index": (
                    representatives[0] if len(representatives) == 1 else -1
                ),
            }
        )
    valid = valid and sorted(representative_indices) == list(
        range(representative_count)
    )
    return {
        "valid": valid,
        "augmented_ordinary_class_count": len(groups),
        "raw_complement_class_count": len(component_groups),
        "raw_complement_class_size_histogram": histogram(
            len(group) for group in raw_groups
        ),
        "raw_complement_partition_sha256": partition_sha256(raw_groups),
        "each_class_has_one_published_representative_and_its_complement": valid,
        "representative_index_coverage_exact": (
            sorted(representative_indices)
            == list(range(representative_count))
        ),
        "binding_rows": sorted(
            binding_rows, key=lambda row: row["representative_index"]
        ),
    }


def representative_and_schedule_audit(
    objective: int, representatives: Sequence[str]
) -> dict[str, object]:
    split_counts: Counter[str] = Counter()
    conflict_union_histogram: Counter[int] = Counter()
    forced_height_histogram: Counter[int] = Counter()
    direct_recount_checks = 0
    nonconflict_barriers = 0
    high_conflict_barriers = 0
    retained_closure_edges = 0
    ceiling_exclusions = 0
    per_seed_schedule: list[dict[str, object]] = []
    all_heights: list[int] = []
    representative_objective_digest = hashlib.sha256()
    for representative_index, line in enumerate(representatives):
        adjacency = decode_graph6(line)
        clique_conflicts, independent_conflicts = conflicts(adjacency)
        observed_objective = len(clique_conflicts) + len(independent_conflicts)
        if observed_objective != objective:
            raise AssertionError(
                f"E={objective} representative {representative_index} "
                f"recounts to {observed_objective}"
            )
        split_counts[
            f"{len(clique_conflicts)},{len(independent_conflicts)}"
        ] += 1
        representative_objective_digest.update(
            (
                f"{line} {len(clique_conflicts)} "
                f"{len(independent_conflicts)}\n"
            ).encode("ascii")
        )
        conflict_union = {
            pair
            for conflict in (*clique_conflicts, *independent_conflicts)
            for pair in itertools.combinations(conflict, 2)
        }
        conflict_union_histogram[len(conflict_union)] += 1
        local_heights: list[tuple[int, int, int, bool]] = []
        local_nonconflict = 0
        local_high_conflict = 0
        local_retained = 0
        local_ceiling = 0
        for left in range(ORDER):
            for right in range(left + 1, ORDER):
                height = exact_post_flip_height(
                    adjacency,
                    clique_conflicts,
                    independent_conflicts,
                    left,
                    right,
                )
                nonconflict = (left, right) not in conflict_union
                if nonconflict and height < objective:
                    raise AssertionError(
                        "non-conflict edge unexpectedly destroys a conflict"
                    )
                outside = nonconflict or height > 4
                if not outside:
                    local_retained += 1
                    continue
                if height > 80:
                    local_ceiling += 1
                    continue
                local_heights.append((height, left, right, nonconflict))
                forced_height_histogram[height] += 1
                all_heights.append(height)
                if nonconflict:
                    local_nonconflict += 1
                else:
                    local_high_conflict += 1
        if (
            len(local_heights)
            + local_retained
            + local_ceiling
            != EDGE_COUNT
        ):
            raise AssertionError("first-edge schedule does not partition 903 edges")

        # Directly re-enumerate selected extrema, independently checking the
        # local post-toggle height formula on every representative.
        local_heights.sort()
        audit_edges = {
            (0, 1),
            (ORDER - 2, ORDER - 1),
        }
        if local_heights:
            audit_edges.add((local_heights[0][1], local_heights[0][2]))
            audit_edges.add((local_heights[-1][1], local_heights[-1][2]))
        for left, right in sorted(audit_edges):
            predicted = exact_post_flip_height(
                adjacency,
                clique_conflicts,
                independent_conflicts,
                left,
                right,
            )
            changed = toggled(adjacency, left, right)
            after_clique, after_independent = conflicts(changed)
            if predicted != len(after_clique) + len(after_independent):
                raise AssertionError("post-toggle height recount mismatch")
            direct_recount_checks += 1

        nonconflict_barriers += local_nonconflict
        high_conflict_barriers += local_high_conflict
        retained_closure_edges += local_retained
        ceiling_exclusions += local_ceiling
        per_seed_schedule.append(
            {
                "representative_index": representative_index,
                "objective": objective,
                "conflict_union_edge_count": len(conflict_union),
                "scheduled_barrier_count": len(local_heights),
                "nonconflict_barrier_count": local_nonconflict,
                "high_conflict_barrier_count": local_high_conflict,
                "within_closure_edge_count": local_retained,
                "ceiling_excluded_edge_count": local_ceiling,
                "minimum_scheduled_height": (
                    local_heights[0][0] if local_heights else None
                ),
                "maximum_scheduled_height": (
                    local_heights[-1][0] if local_heights else None
                ),
            }
        )

    return {
        "objective": objective,
        "representative_count": len(representatives),
        "representative_conflict_split_counts": dict(sorted(split_counts.items())),
        "representative_objective_recount_sha256": (
            representative_objective_digest.hexdigest()
        ),
        "all_representatives_recounted": True,
        "conflict_union_edge_count_histogram": {
            str(key): value
            for key, value in sorted(conflict_union_histogram.items())
        },
        "scheduled_barrier_count": nonconflict_barriers
        + high_conflict_barriers,
        "nonconflict_barrier_count": nonconflict_barriers,
        "high_conflict_barrier_count": high_conflict_barriers,
        "within_closure_edge_count": retained_closure_edges,
        "ceiling_excluded_edge_count": ceiling_exclusions,
        "forced_barrier_height_histogram": {
            str(key): value
            for key, value in sorted(forced_height_histogram.items())
        },
        "minimum_scheduled_height": min(all_heights),
        "maximum_scheduled_height": max(all_heights),
        "direct_post_toggle_recount_check_count": direct_recount_checks,
        "per_seed_schedule": per_seed_schedule,
    }


def independent_discovery_recount(lines: Sequence[str]) -> dict[str, object]:
    splits: Counter[str] = Counter()
    geometry: Counter[str] = Counter()
    recount_digest = hashlib.sha256()
    for index, line in enumerate(lines):
        adjacency = decode_graph6(line)
        clique_conflicts, independent_conflicts = conflicts(adjacency)
        if len(clique_conflicts) + len(independent_conflicts) != 2:
            raise AssertionError(
                f"discovery {index} does not independently recount to E=2"
            )
        split = f"{len(clique_conflicts)},{len(independent_conflicts)}"
        splits[split] += 1
        selected = (
            clique_conflicts
            if clique_conflicts
            else independent_conflicts
        )
        same_colour = len(selected) == 2
        overlap = (
            len(set(selected[0]) & set(selected[1]))
            if same_colour
            else -1
        )
        label = (
            f"{'same_colour_pair' if same_colour else 'mixed_colour_pair'};"
            f"overlap={overlap}"
        )
        geometry[label] += 1
        recount_digest.update(
            f"{line} {split} {label}\n".encode("ascii")
        )
    return {
        "record_count": len(lines),
        "all_endpoints_independently_recounted_to_E2": True,
        "conflict_split_counts": dict(sorted(splits.items())),
        "geometry_counts": dict(sorted(geometry.items())),
        "ordered_recount_sha256": recount_digest.hexdigest(),
    }


def compare_complement_representative_sets(
    *,
    shortg: Path,
    left: Sequence[str],
    right: Sequence[str],
    directory: Path,
    tag: str,
) -> dict[str, object]:
    if len(left) != len(right) or not left:
        raise ValueError("representative sets must have one common size")
    count = len(left)
    left_duals = [
        encode_graph6(graph_complement(decode_graph6(line))) for line in left
    ]
    right_duals = [
        encode_graph6(graph_complement(decode_graph6(line))) for line in right
    ]
    partition_record = run_traces_partition(
        shortg,
        [*left, *left_duals, *right, *right_duals],
        directory,
        tag,
    )
    groups = partition_record["groups"]
    group_of = {
        member: group_index
        for group_index, group in enumerate(groups)
        for member in group
    }
    parent = list(range(len(groups)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left_index: int, right_index: int) -> None:
        left_root = find(left_index)
        right_root = find(right_index)
        if left_root != right_root:
            parent[right_root] = left_root

    for index in range(count):
        union(group_of[1 + index], group_of[1 + count + index])
        union(
            group_of[1 + 2 * count + index],
            group_of[1 + 3 * count + index],
        )
    components: dict[int, list[int]] = {}
    for group_index in range(len(groups)):
        components.setdefault(find(group_index), []).append(group_index)
    mappings: list[dict[str, int]] = []
    valid = len(groups) == 2 * count and len(components) == count
    for ordinary_groups in components.values():
        members = [
            member
            for group_index in ordinary_groups
            for member in groups[group_index]
        ]
        left_indices = [
            member - 1 for member in members if 1 <= member <= count
        ]
        left_dual_indices = [
            member - (1 + count)
            for member in members
            if count + 1 <= member <= 2 * count
        ]
        right_indices = [
            member - (1 + 2 * count)
            for member in members
            if 2 * count + 1 <= member <= 3 * count
        ]
        right_dual_indices = [
            member - (1 + 3 * count)
            for member in members
            if 3 * count + 1 <= member <= 4 * count
        ]
        row_valid = (
            len(ordinary_groups) == 2
            and len(left_indices) == 1
            and left_indices == left_dual_indices
            and len(right_indices) == 1
            and right_indices == right_dual_indices
        )
        valid = valid and row_valid
        mappings.append(
            {
                "left_index": left_indices[0] if len(left_indices) == 1 else -1,
                "right_index": (
                    right_indices[0] if len(right_indices) == 1 else -1
                ),
            }
        )
    valid = valid and sorted(row["left_index"] for row in mappings) == list(
        range(count)
    )
    valid = valid and sorted(row["right_index"] for row in mappings) == list(
        range(count)
    )
    return {
        "valid": valid,
        "ordinary_class_count": len(groups),
        "complement_class_count": len(components),
        "class_mapping": sorted(mappings, key=lambda row: row["left_index"]),
        "traces_partition_sha256": partition_record["partition_sha256"],
        "traces_canonical_output_sha256": partition_record[
            "canonical_output_sha256"
        ],
    }


def compare_field(
    errors: list[str],
    label: str,
    observed: object,
    expected: object,
) -> None:
    if observed != expected:
        errors.append(f"{label}: observed {observed!r}, expected {expected!r}")


def recorded_output_matches_artifact(
    *,
    observed: object,
    planned: object,
    artifact: Path,
    project_root: Path,
) -> bool:
    """Match a recorded output path under the two documented run roots.

    The frozen plan records paths relative to the project root.  The completed
    run was launched either there or from its parent, so its JSON may include
    the project-directory prefix.  Resolve both spellings to the independently
    supplied artifact instead of comparing their text.
    """

    if not isinstance(observed, str) or not isinstance(planned, str):
        return False
    planned_path = Path(planned)
    if planned_path.is_absolute():
        planned_artifact = planned_path.resolve()
    else:
        planned_artifact = (project_root / planned_path).resolve()
    artifact = artifact.resolve()
    if planned_artifact != artifact:
        return False
    observed_path = Path(observed)
    if observed_path.is_absolute():
        observed_candidates = {observed_path.resolve()}
    else:
        observed_candidates = {
            (project_root / observed_path).resolve(),
            (project_root.parent / observed_path).resolve(),
        }
    return artifact in observed_candidates


def frozen_git_blob(
    repository_root: Path,
    revision: str,
    repository_relative_path: Path,
) -> tuple[str, bytes]:
    """Resolve a revision and return the exact named Git blob."""

    commit = subprocess.run(
        ["git", "rev-parse", f"{revision}^{{commit}}"],
        cwd=repository_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout.strip()
    blob = subprocess.run(
        [
            "git",
            "show",
            f"{commit}:{repository_relative_path.as_posix()}",
        ],
        cwd=repository_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout
    return commit, blob


def ordered_seed_corpus_sha256(paths: Sequence[Path]) -> str:
    """Hash graph6 seed records in command-line order."""

    digest = hashlib.sha256()
    for path in paths:
        raw = path.read_bytes()
        if not raw.endswith(b"\n") or raw.count(b"\n") != 1:
            raise ValueError(f"{path}: expected one newline-terminated seed")
        digest.update(raw)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--e3", type=Path, required=True)
    parser.add_argument("--e4", type=Path, required=True)
    parser.add_argument("--representatives-e3", type=Path, required=True)
    parser.add_argument("--representatives-e4", type=Path, required=True)
    parser.add_argument("--published-audit", type=Path, required=True)
    parser.add_argument("--quotient-plan", type=Path, required=True)
    parser.add_argument("--export-result", type=Path, required=True)
    parser.add_argument("--second-barrier-plan", type=Path, required=True)
    parser.add_argument("--initial-invalid-audit", type=Path, required=True)
    parser.add_argument("--known-e2-seed-audit", type=Path, required=True)
    parser.add_argument("--search-source", type=Path, required=True)
    parser.add_argument("--frozen-source-commit", default="HEAD")
    parser.add_argument("--search-binary", type=Path, required=True)
    parser.add_argument("--cxx", default="c++")
    parser.add_argument("--shortg", type=Path, required=True)
    parser.add_argument("--production-result", type=Path, required=True)
    parser.add_argument("--discovery-stream", type=Path, required=True)
    parser.add_argument("--discovery-audit", type=Path, required=True)
    parser.add_argument(
        "--discovery-representatives", type=Path, required=True
    )
    parser.add_argument(
        "--known-e2-class-representatives", type=Path, required=True
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    named_paths = {
        "e3_stream": args.e3,
        "e4_stream": args.e4,
        "e3_representatives": args.representatives_e3,
        "e4_representatives": args.representatives_e4,
        "published_audit": args.published_audit,
        "quotient_plan": args.quotient_plan,
        "export_result": args.export_result,
        "second_barrier_plan": args.second_barrier_plan,
        "initial_invalid_audit": args.initial_invalid_audit,
        "known_e2_seed_audit": args.known_e2_seed_audit,
        "shortg_traces": args.shortg,
        "production_result": args.production_result,
        "discovery_stream": args.discovery_stream,
        "discovery_audit": args.discovery_audit,
        "discovery_representatives": args.discovery_representatives,
        "known_e2_class_representatives": (
            args.known_e2_class_representatives
        ),
    }
    file_hashes = {
        name: sha256_file(path) for name, path in named_paths.items()
    }
    repository_root = Path(
        subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=args.search_source.parent,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout.strip()
    )
    relative_search_source = args.search_source.resolve().relative_to(
        repository_root.resolve()
    )
    frozen_commit, frozen_source_bytes = frozen_git_blob(
        repository_root,
        args.frozen_source_commit,
        relative_search_source,
    )
    file_hashes["search_source"] = hashlib.sha256(
        frozen_source_bytes
    ).hexdigest()
    file_hashes["search_source_worktree"] = sha256_file(args.search_source)
    file_hashes["search_binary_worktree"] = sha256_file(args.search_binary)
    frozen_compile_flags = [
        "-std=c++20",
        "-O3",
        "-DNDEBUG",
        "-Wall",
        "-Wextra",
        "-pedantic",
    ]
    with tempfile.TemporaryDirectory(
        prefix="ramsey55-e2-frozen-binary-rebuild."
    ) as rebuild_directory_name:
        rebuild_directory = Path(rebuild_directory_name)
        rebuild_source = rebuild_directory / args.search_source.name
        rebuild_binary = rebuild_directory / args.search_binary.name
        rebuild_source.write_bytes(frozen_source_bytes)
        rebuilt = subprocess.run(
            [
                args.cxx,
                *frozen_compile_flags,
                str(rebuild_source),
                "-o",
                str(rebuild_binary),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if rebuilt.returncode != 0:
            raise RuntimeError(
                "frozen search binary rebuild failed: "
                f"{rebuilt.stdout}\n{rebuilt.stderr}"
            )
        file_hashes["search_binary"] = sha256_file(rebuild_binary)
    errors: list[str] = []
    for name, expected_hash in EXPECTED_HASHES.items():
        if name == "prior_second_barrier_plan":
            continue
        compare_field(errors, f"{name} SHA-256", file_hashes[name], expected_hash)
    compare_field(
        errors,
        "preserved production binary SHA-256",
        file_hashes["search_binary_worktree"],
        EXPECTED_HASHES["search_binary"],
    )

    published = json.loads(args.published_audit.read_text(encoding="utf-8"))
    quotient_plan = json.loads(args.quotient_plan.read_text(encoding="utf-8"))
    export_result = json.loads(args.export_result.read_text(encoding="utf-8"))
    second_plan = json.loads(
        args.second_barrier_plan.read_text(encoding="utf-8")
    )
    project_root = args.second_barrier_plan.resolve().parents[2]
    prior_plan_path = (
        project_root / second_plan.get("prior_run", {}).get("plan", "")
    )
    file_hashes["prior_second_barrier_plan"] = sha256_file(prior_plan_path)
    compare_field(
        errors,
        "prior_second_barrier_plan SHA-256",
        file_hashes["prior_second_barrier_plan"],
        EXPECTED_HASHES["prior_second_barrier_plan"],
    )
    prior_second_plan = json.loads(
        prior_plan_path.read_text(encoding="utf-8")
    )
    initial_invalid = json.loads(
        args.initial_invalid_audit.read_text(encoding="utf-8")
    )
    known_e2_seed_audit = json.loads(
        args.known_e2_seed_audit.read_text(encoding="utf-8")
    )
    production_result = json.loads(
        args.production_result.read_text(encoding="utf-8")
    )
    discovery_audit = json.loads(
        args.discovery_audit.read_text(encoding="utf-8")
    )

    compare_field(errors, "published valid", published.get("valid"), True)
    compare_field(
        errors,
        "published total labeled count",
        published.get("total_labeled_graph_count"),
        89_870,
    )
    compare_field(
        errors,
        "published total complement classes",
        published.get("total_complement_isomorphism_class_count"),
        53,
    )
    compare_field(
        errors,
        "export closure complete",
        export_result.get("closure_complete"),
        True,
    )
    compare_field(errors, "export E0", export_result.get("E0_found"), False)
    compare_field(
        errors,
        "export closure distribution",
        export_result.get("closure_state_distribution"),
        {"3": 16_082, "4": 73_788},
    )
    compare_field(
        errors,
        "export output counts",
        export_result.get("closure_output_counts"),
        {"3": 16_082, "4": 73_788},
    )
    compare_field(
        errors,
        "export off-cycle E2 count",
        export_result.get("offcycle_E2_count"),
        0,
    )
    compare_field(
        errors,
        "second-plan quotient audit hash",
        prior_second_plan.get("input", {}).get("quotient_audit_sha256"),
        EXPECTED_HASHES["published_audit"],
    )
    compare_field(
        errors,
        "recovery-plan schema",
        second_plan.get("schema"),
        "ramsey55.e2_low_closure_second_barrier_recovery_plan.v2",
    )
    compare_field(
        errors,
        "recovery-plan frozen status",
        second_plan.get("status"),
        "FROZEN_BEFORE_PRODUCTION",
    )
    compare_field(
        errors,
        "recovery-plan initial audit hash",
        second_plan.get("recovery_reason", {}).get("initial_audit_sha256"),
        EXPECTED_HASHES["initial_invalid_audit"],
    )
    compare_field(
        errors,
        "initial audit status",
        initial_invalid.get("status"),
        "INVALID",
    )
    compare_field(errors, "initial audit valid", initial_invalid.get("valid"), False)
    compare_field(
        errors,
        "initial audit sole error",
        initial_invalid.get("errors"),
        [
            "production result discovery_output: observed "
            "'ramsey55/results/constructive/e2_low_closure_v2/"
            "second_barrier_new_E2.g6', expected "
            "'results/constructive/e2_low_closure_v2/"
            "second_barrier_new_E2.g6'"
        ],
    )
    compare_field(
        errors,
        "recovery-plan frozen commit",
        second_plan.get("implementation", {}).get("source_git_commit"),
        frozen_commit,
    )
    compare_field(
        errors,
        "recovery-plan repository source path",
        second_plan.get("implementation", {}).get("source_repository_path"),
        relative_search_source.as_posix(),
    )
    compare_field(
        errors,
        "second-plan source hash",
        second_plan.get("implementation", {}).get("source_sha256"),
        EXPECTED_HASHES["search_source"],
    )
    compare_field(
        errors,
        "second-plan binary hash",
        second_plan.get("implementation", {}).get("binary_sha256"),
        EXPECTED_HASHES["search_binary"],
    )
    compare_field(
        errors,
        "second-plan binary bytes",
        second_plan.get("implementation", {}).get("binary_bytes"),
        args.search_binary.stat().st_size,
    )
    if not recorded_output_matches_artifact(
        observed=second_plan.get("implementation", {}).get("binary"),
        planned=second_plan.get("implementation", {}).get("binary"),
        artifact=args.search_binary,
        project_root=project_root,
    ):
        errors.append(
            "recovery-plan binary path does not resolve to the preserved binary"
        )
    compare_field(
        errors,
        "recovery-plan compiler hash",
        second_plan.get("implementation", {}).get("compiler_sha256"),
        sha256_file(Path(args.cxx)),
    )
    compare_field(
        errors,
        "recovery-plan known-E2 audit hash",
        second_plan.get("inputs", {}).get("known_e2_seed_audit_sha256"),
        EXPECTED_HASHES["known_e2_seed_audit"],
    )
    planned_seed_strings = second_plan.get("inputs", {}).get(
        "known_e2_seed_paths", []
    )
    audited_seed_strings = [
        record.get("path") for record in known_e2_seed_audit.get("records", [])
    ]
    compare_field(
        errors,
        "recovery-plan ordered known-E2 seed paths",
        planned_seed_strings,
        audited_seed_strings,
    )
    compare_field(
        errors,
        "recovery-plan ordered seed-path hash",
        second_plan.get("inputs", {}).get(
            "known_e2_seed_argument_order_sha256"
        ),
        hashlib.sha256(
            "".join(f"{path}\n" for path in audited_seed_strings).encode(
                "utf-8"
            )
        ).hexdigest(),
    )
    audited_seed_paths = [project_root / path for path in audited_seed_strings]
    compare_field(
        errors,
        "recovery-plan ordered seed-corpus hash",
        second_plan.get("inputs", {}).get("known_e2_seed_corpus_sha256"),
        ordered_seed_corpus_sha256(audited_seed_paths),
    )
    compare_field(
        errors,
        "known-E2 audit corpus hash",
        known_e2_seed_audit.get("candidate_corpus_sha256"),
        ordered_seed_corpus_sha256(audited_seed_paths),
    )
    planned_low_seeds = second_plan.get("inputs", {}).get(
        "low_seed_files", []
    )
    compare_field(errors, "recovery-plan low-seed count", len(planned_low_seeds), 2)
    for index, (planned_record, path, expected_hash) in enumerate(
        zip(
            planned_low_seeds,
            (args.representatives_e3, args.representatives_e4),
            (
                EXPECTED_HASHES["e3_representatives"],
                EXPECTED_HASHES["e4_representatives"],
            ),
            strict=True,
        )
    ):
        if not recorded_output_matches_artifact(
            observed=planned_record.get("path"),
            planned=planned_record.get("path"),
            artifact=path,
            project_root=project_root,
        ):
            errors.append(
                f"recovery-plan low-seed path {index} does not resolve"
            )
        compare_field(
            errors,
            f"recovery-plan low-seed hash {index}",
            planned_record.get("sha256"),
            expected_hash,
        )
    compare_field(
        errors,
        "second-plan per-seed limit",
        second_plan.get("first_barrier_schedule", {}).get("per_seed_limit"),
        0,
    )
    compare_field(
        errors,
        "second-plan ceiling",
        second_plan.get("first_barrier_schedule", {}).get("objective_ceiling"),
        80,
    )
    compare_field(
        errors,
        "second-plan repair ceiling",
        second_plan.get("repair", {}).get("objective_ceiling"),
        80,
    )

    stream_paths = {3: args.e3, 4: args.e4}
    representative_paths = {
        3: args.representatives_e3,
        4: args.representatives_e4,
    }
    raw_lines: dict[int, list[str]] = {}
    representative_lines: dict[int, list[str]] = {}
    stream_records: dict[int, dict[str, object]] = {}
    for objective in (3, 4):
        raw_lines[objective], stream_record = read_graph6_stream(
            stream_paths[objective]
        )
        representative_lines[objective], representative_record = (
            read_graph6_stream(representative_paths[objective])
        )
        expected = EXPECTED[objective]
        compare_field(
            errors,
            f"E={objective} raw count",
            len(raw_lines[objective]),
            expected["stream_count"],
        )
        compare_field(
            errors,
            f"E={objective} representative count",
            len(representative_lines[objective]),
            expected["representative_count"],
        )
        stream_records[objective] = {
            "raw_stream": stream_record,
            "representative_stream": representative_record,
        }

    discovery_lines, discovery_stream_record = read_graph6_stream(
        args.discovery_stream
    )
    discovery_representatives, discovery_representative_record = (
        read_graph6_stream(args.discovery_representatives)
    )
    known_e2_representatives, known_e2_representative_record = (
        read_graph6_stream(args.known_e2_class_representatives)
    )
    compare_field(
        errors, "discovery stream count", len(discovery_lines), 1_670
    )
    compare_field(
        errors,
        "discovery representative count",
        len(discovery_representatives),
        2,
    )
    compare_field(
        errors,
        "known E2 representative count",
        len(known_e2_representatives),
        2,
    )
    discovery_recount = independent_discovery_recount(discovery_lines)
    compare_field(
        errors,
        "published discovery audit valid",
        discovery_audit.get("valid"),
        True,
    )
    compare_field(
        errors,
        "published discovery hash",
        discovery_audit.get("discovery_sha256"),
        file_hashes["discovery_stream"],
    )
    compare_field(
        errors,
        "published discovery count",
        discovery_audit.get("discovery_count"),
        len(discovery_lines),
    )
    compare_field(
        errors,
        "published independent E2 recount claim",
        discovery_audit.get("all_endpoints_independently_recounted_to_E2"),
        True,
    )
    compare_field(
        errors,
        "published discovery complement class count",
        discovery_audit.get("discovery_complement_isomorphism_class_count"),
        2,
    )
    compare_field(
        errors,
        "published discovery novelty count",
        discovery_audit.get("novel_complement_isomorphism_class_count"),
        0,
    )
    compare_field(
        errors,
        "published discovery geometry",
        discovery_audit.get("labeled_geometry_counts"),
        discovery_recount["geometry_counts"],
    )

    published_records = {
        int(record["objective"]): record for record in published["records"]
    }
    traces_records: dict[int, dict[str, object]] = {}
    schedule_records: dict[int, dict[str, object]] = {}
    discovery_partition: dict[str, object]
    with tempfile.TemporaryDirectory(
        prefix="ramsey55-e2-closure-independent."
    ) as directory_name:
        directory = Path(directory_name)
        for objective in (3, 4):
            raw = raw_lines[objective]
            representatives = representative_lines[objective]
            ordinary = run_traces_partition(
                args.shortg, raw, directory, f"e{objective}.ordinary"
            )
            duals = [
                encode_graph6(graph_complement(decode_graph6(line)))
                for line in raw
            ]
            representative_duals = [
                encode_graph6(graph_complement(decode_graph6(line)))
                for line in representatives
            ]
            augmented_lines = [
                *raw,
                *duals,
                *representatives,
                *representative_duals,
            ]
            augmented = run_traces_partition(
                args.shortg,
                augmented_lines,
                directory,
                f"e{objective}.augmented",
            )
            complement_analysis = analyze_augmented_partition(
                augmented["groups"],
                len(raw),
                len(representatives),
            )
            expected = EXPECTED[objective]
            compare_field(
                errors,
                f"E={objective} Traces ordinary class count",
                ordinary["class_count"],
                expected["ordinary_count"],
            )
            compare_field(
                errors,
                f"E={objective} Traces ordinary histogram",
                ordinary["class_size_histogram"],
                expected["ordinary_histogram"],
            )
            compare_field(
                errors,
                f"E={objective} augmented ordinary class count",
                augmented["class_count"],
                expected["ordinary_count"],
            )
            compare_field(
                errors,
                f"E={objective} complement class count",
                complement_analysis["raw_complement_class_count"],
                expected["representative_count"],
            )
            compare_field(
                errors,
                f"E={objective} complement histogram",
                complement_analysis["raw_complement_class_size_histogram"],
                expected["complement_histogram"],
            )
            compare_field(
                errors,
                f"E={objective} representative binding",
                complement_analysis["valid"],
                True,
            )
            published_record = published_records[objective]
            compare_field(
                errors,
                f"E={objective} published input hash",
                published_record.get("input_sha256"),
                stream_records[objective]["raw_stream"]["sha256"],
            )
            compare_field(
                errors,
                f"E={objective} published representative hash",
                published_record.get("representative_sha256"),
                stream_records[objective]["representative_stream"]["sha256"],
            )
            compare_field(
                errors,
                f"E={objective} published ordinary count",
                published_record.get("ordinary_isomorphism_class_count"),
                ordinary["class_count"],
            )
            compare_field(
                errors,
                f"E={objective} published complement count",
                published_record.get("complement_isomorphism_class_count"),
                complement_analysis["raw_complement_class_count"],
            )
            compare_field(
                errors,
                f"E={objective} published ordinary histogram",
                published_record.get("ordinary_class_size_histogram"),
                ordinary["class_size_histogram"],
            )
            compare_field(
                errors,
                f"E={objective} published complement histogram",
                published_record.get("complement_class_size_histogram"),
                complement_analysis["raw_complement_class_size_histogram"],
            )
            traces_records[objective] = {
                "ordinary": {
                    key: value
                    for key, value in ordinary.items()
                    if key != "groups"
                },
                "augmented_graph_complement": {
                    key: value
                    for key, value in augmented.items()
                    if key != "groups"
                },
                "published_representative_binding": complement_analysis,
            }
            schedule = representative_and_schedule_audit(
                objective, representatives
            )
            compare_field(
                errors,
                f"E={objective} representative split counts",
                schedule["representative_conflict_split_counts"],
                expected["split_counts"],
            )
            compare_field(
                errors,
                f"E={objective} published split counts",
                published_record.get("representative_conflict_split_counts"),
                schedule["representative_conflict_split_counts"],
            )
            schedule_records[objective] = schedule

        discovery_ordinary = run_traces_partition(
            args.shortg,
            discovery_lines,
            directory,
            "discovery.ordinary",
        )
        discovery_duals = [
            encode_graph6(graph_complement(decode_graph6(line)))
            for line in discovery_lines
        ]
        discovery_augmented = run_traces_partition(
            args.shortg,
            [
                *discovery_lines,
                *discovery_duals,
                *discovery_representatives,
                *[
                    encode_graph6(graph_complement(decode_graph6(line)))
                    for line in discovery_representatives
                ],
            ],
            directory,
            "discovery.augmented",
        )
        discovery_binding = analyze_augmented_partition(
            discovery_augmented["groups"],
            len(discovery_lines),
            len(discovery_representatives),
        )
        known_class_match = compare_complement_representative_sets(
            shortg=args.shortg,
            left=discovery_representatives,
            right=known_e2_representatives,
            directory=directory,
            tag="discovery.known-class-match",
        )
        compare_field(
            errors,
            "discovery Traces ordinary class count",
            discovery_ordinary["class_count"],
            4,
        )
        compare_field(
            errors,
            "discovery Traces complement class count",
            discovery_binding["raw_complement_class_count"],
            2,
        )
        compare_field(
            errors,
            "discovery published representative binding",
            discovery_binding["valid"],
            True,
        )
        compare_field(
            errors,
            "discovery known-class match",
            known_class_match["valid"],
            True,
        )
        compare_field(
            errors,
            "published discovery ordinary count",
            discovery_audit.get("discovery_ordinary_isomorphism_class_count"),
            discovery_ordinary["class_count"],
        )
        compare_field(
            errors,
            "published discovery complement histogram",
            discovery_audit.get("discovery_complement_class_size_histogram"),
            discovery_binding["raw_complement_class_size_histogram"],
        )
        discovery_partition = {
            "ordinary": {
                key: value
                for key, value in discovery_ordinary.items()
                if key != "groups"
            },
            "augmented": {
                key: value
                for key, value in discovery_augmented.items()
                if key != "groups"
            },
            "representative_binding": discovery_binding,
            "known_class_match": known_class_match,
        }

    combined_height_histogram: Counter[int] = Counter()
    for record in schedule_records.values():
        combined_height_histogram.update(
            {
                int(height): count
                for height, count in record[
                    "forced_barrier_height_histogram"
                ].items()
            }
        )
    total_schedule = {
        "seed_count": sum(
            record["representative_count"]
            for record in schedule_records.values()
        ),
        "forced_barrier_count": sum(
            record["scheduled_barrier_count"]
            for record in schedule_records.values()
        ),
        "nonconflict_barrier_count": sum(
            record["nonconflict_barrier_count"]
            for record in schedule_records.values()
        ),
        "high_conflict_barrier_count": sum(
            record["high_conflict_barrier_count"]
            for record in schedule_records.values()
        ),
        "within_closure_edge_count": sum(
            record["within_closure_edge_count"]
            for record in schedule_records.values()
        ),
        "ceiling_excluded_edge_count": sum(
            record["ceiling_excluded_edge_count"]
            for record in schedule_records.values()
        ),
        "minimum_scheduled_height": min(
            record["minimum_scheduled_height"]
            for record in schedule_records.values()
        ),
        "maximum_scheduled_height": max(
            record["maximum_scheduled_height"]
            for record in schedule_records.values()
        ),
        "direct_post_toggle_recount_check_count": sum(
            record["direct_post_toggle_recount_check_count"]
            for record in schedule_records.values()
        ),
        "barriers_by_source_objective": {
            str(objective): schedule_records[objective][
                "scheduled_barrier_count"
            ]
            for objective in (3, 4)
        },
        "forced_barriers_by_height": {
            str(height): count
            for height, count in sorted(combined_height_histogram.items())
        },
    }
    compare_field(errors, "total seed count", total_schedule["seed_count"], 53)
    if total_schedule["ceiling_excluded_edge_count"] != 0:
        errors.append(
            "objective ceiling 80 excludes at least one otherwise eligible "
            "first edge"
        )
    compare_field(
        errors,
        "all first edges accounted",
        (
            total_schedule["forced_barrier_count"]
            + total_schedule["within_closure_edge_count"]
            + total_schedule["ceiling_excluded_edge_count"]
        ),
        53 * EDGE_COUNT,
    )

    production_expectations = {
        "mode": "low_seed_second_barrier_search",
        "algorithm": "e2_low_closure_second_barrier_v1",
        "seed": second_plan.get("repair", {}).get("seed"),
        "low_seed_file_count": 2,
        "low_seed_count": total_schedule["seed_count"],
        "low_seed_objective_distribution": {"3": 9, "4": 44},
        "known_E2_state_count": 1_892,
        "forced_barrier_count": total_schedule["forced_barrier_count"],
        "forced_barrier_exact_replays": total_schedule[
            "forced_barrier_count"
        ],
        "nonconflict_barrier_count": total_schedule[
            "nonconflict_barrier_count"
        ],
        "high_conflict_barrier_count": total_schedule[
            "high_conflict_barrier_count"
        ],
        "barriers_by_source_objective": total_schedule[
            "barriers_by_source_objective"
        ],
        "forced_barriers_by_height": total_schedule[
            "forced_barriers_by_height"
        ],
        "low_barriers_per_seed": 0,
        "rollouts_per_barrier": second_plan.get("repair", {}).get(
            "rollouts_per_barrier"
        ),
        "rollouts": total_schedule["forced_barrier_count"],
        "steps_per_rollout": second_plan.get("repair", {}).get(
            "steps_per_rollout"
        ),
        "tabu_tenure": second_plan.get("repair", {}).get("tabu_tenure"),
        "noise_per_million": second_plan.get("repair", {}).get(
            "noise_per_million"
        ),
        "objective_ceiling": second_plan.get("repair", {}).get(
            "objective_ceiling"
        ),
        "E1_visits": 0,
        "new_E2_unique_count": len(discovery_lines),
        "E0_found": False,
    }
    for field, expected_value in production_expectations.items():
        compare_field(
            errors,
            f"production result {field}",
            production_result.get(field),
            expected_value,
        )
    planned_discovery_output = second_plan.get("outputs", {}).get(
        "discovery_output"
    )
    observed_discovery_output = production_result.get("discovery_output")
    if not recorded_output_matches_artifact(
        observed=observed_discovery_output,
        planned=planned_discovery_output,
        artifact=args.discovery_stream,
        project_root=project_root,
    ):
        errors.append(
            "production result discovery_output does not resolve to the "
            "frozen discovery artifact"
        )
    if not recorded_output_matches_artifact(
        observed=second_plan.get("outputs", {}).get("result"),
        planned=second_plan.get("outputs", {}).get("result"),
        artifact=args.production_result,
        project_root=project_root,
    ):
        errors.append(
            "recovery-plan result path does not resolve to the production result"
        )
    compare_field(
        errors,
        "production ceiling covers all eligible first edges",
        total_schedule["ceiling_excluded_edge_count"],
        0,
    )

    design_findings = [
        {
            "severity": "important_follow_up",
            "finding": (
                "E=1 states are counted but neither returned nor written to "
                "the discovery stream. Preserve and independently replay "
                "them; they are stronger near-constructions than E=2."
            ),
            "invalidates_observational_run": False,
        },
        {
            "severity": "required_post_run_binding",
            "finding": (
                "The search JSON does not itself carry source, binary, "
                "input-stream, or discovery-output hashes. A fail-closed "
                "post-run manifest/checker must bind those hashes and the "
                "exact schedule counts before retaining the result. This "
                "independent check supplies that binding for the frozen run."
            ),
            "resolved_by_this_checker": not errors,
            "invalidates_observational_run": False,
        },
        {
            "severity": "heuristic_scope",
            "finding": (
                "One representative per complement-isomorphism class is "
                "exact for the first-edge structural schedule, but one "
                "randomized repair trajectory is not isomorphism- or "
                "complement-exhaustive. In particular conflict enumeration "
                "order changes under complementation. This is acceptable "
                "only with the plan's explicit heuristic claim boundary."
            ),
            "invalidates_observational_run": False,
        },
    ]
    result = {
        "schema": SCHEMA,
        "status": (
            "VALID_FINITE_CORPUS_PARTITION_AND_SCHEDULE_AUDIT"
            if not errors
            else "INVALID"
        ),
        "valid": not errors,
        "errors": errors,
        "claim_boundary": (
            "This independently classifies only the supplied finite "
            "E=3/E=4 streams and audits the configured first-edge schedule. "
            "The subsequent repair is heuristic; no nonexistence conclusion "
            "follows from a negative search."
        ),
        "checker_source_sha256": sha256_file(Path(__file__)),
        "file_hashes": file_hashes,
        "frozen_source_binding": {
            "git_commit": frozen_commit,
            "repository_relative_path": relative_search_source.as_posix(),
            "frozen_source_sha256": file_hashes["search_source"],
            "current_worktree_source_sha256": file_hashes[
                "search_source_worktree"
            ],
            "compile_command": [args.cxx, *frozen_compile_flags],
            "rebuilt_frozen_binary_sha256": file_hashes["search_binary"],
            "current_worktree_binary_sha256": file_hashes[
                "search_binary_worktree"
            ],
            "worktree_has_advanced_after_frozen_run": (
                file_hashes["search_source_worktree"]
                != file_hashes["search_source"]
            ),
            "worktree_binary_has_advanced_after_frozen_run": (
                file_hashes["search_binary_worktree"]
                != file_hashes["search_binary"]
            ),
        },
        "recovery_binding": {
            "recovery_plan_sha256": file_hashes["second_barrier_plan"],
            "prior_plan_sha256": file_hashes[
                "prior_second_barrier_plan"
            ],
            "initial_invalid_audit_sha256": file_hashes[
                "initial_invalid_audit"
            ],
            "known_e2_seed_audit_sha256": file_hashes[
                "known_e2_seed_audit"
            ],
            "preserved_binary_sha256": file_hashes[
                "search_binary_worktree"
            ],
            "independently_rebuilt_binary_sha256": file_hashes[
                "search_binary"
            ],
            "preserved_and_rebuilt_binary_identical": (
                file_hashes["search_binary_worktree"]
                == file_hashes["search_binary"]
            ),
            "rerun_matches_prior_discovery_byte_for_byte": (
                file_hashes["discovery_stream"]
                == EXPECTED_HASHES["discovery_stream"]
            ),
        },
        "stream_records": {
            str(key): value for key, value in stream_records.items()
        },
        "traces_method": {
            "executable": str(args.shortg.resolve()),
            "executable_sha256": file_hashes["shortg_traces"],
            "mode": "shortg -t (Traces), distinct from published dense/sparse labelg",
            "augmented_input_order": (
                "raw graphs, raw complements, published representatives, "
                "published representative complements"
            ),
        },
        "traces_records": {
            str(key): value for key, value in traces_records.items()
        },
        "schedule_records": {
            str(key): value for key, value in schedule_records.items()
        },
        "total_schedule": total_schedule,
        "production_result_binding": {
            "valid": not errors,
            "result_sha256": file_hashes["production_result"],
            "source_sha256": file_hashes["search_source"],
            "binary_sha256": file_hashes["search_binary_worktree"],
            "recovery_plan_sha256": file_hashes[
                "second_barrier_plan"
            ],
            "prior_second_barrier_plan_sha256": file_hashes[
                "prior_second_barrier_plan"
            ],
            "input_stream_sha256": {
                "E3": file_hashes["e3_representatives"],
                "E4": file_hashes["e4_representatives"],
            },
            "independent_forced_barrier_count": total_schedule[
                "forced_barrier_count"
            ],
            "independent_ceiling_exclusion_count": total_schedule[
                "ceiling_excluded_edge_count"
            ],
            "discovery_stream_sha256": file_hashes["discovery_stream"],
            "discovery_record_count": len(discovery_lines),
            "E1_visits": production_result.get("E1_visits"),
            "E0_found": production_result.get("E0_found"),
        },
        "discovery_recount": discovery_recount,
        "discovery_stream_record": discovery_stream_record,
        "discovery_representative_stream_record": (
            discovery_representative_record
        ),
        "known_E2_representative_stream_record": (
            known_e2_representative_record
        ),
        "discovery_traces_partition": discovery_partition,
        "design_findings": design_findings,
        "quotient_reconstruction": {
            "total_labeled_graph_count": sum(
                len(raw_lines[objective]) for objective in (3, 4)
            ),
            "total_complement_isomorphism_class_count": sum(
                traces_records[objective][
                    "published_representative_binding"
                ]["raw_complement_class_count"]
                for objective in (3, 4)
            ),
            "E3_classes": traces_records[3][
                "published_representative_binding"
            ]["raw_complement_class_count"],
            "E4_classes": traces_records[4][
                "published_representative_binding"
            ]["raw_complement_class_count"],
        },
    }
    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite {args.output}")
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
