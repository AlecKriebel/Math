#!/usr/bin/env python3
"""Normalize, align, and deterministically pair the 22 E=2 elite graphs."""

from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_io import complement, encode_graph6, read_graph  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def graph_sha256(adjacency: list[int]) -> str:
    return hashlib.sha256((encode_graph6(adjacency) + "\n").encode("ascii")).hexdigest()


def edge_hamming(
    left: list[int], right: list[int], mapping: list[int] | None = None
) -> int:
    if len(left) != len(right):
        raise ValueError("graphs have different orders")
    if mapping is None:
        mapping = list(range(len(left)))
    return sum(
        ((left[a] >> b) & 1)
        != ((right[mapping[a]] >> mapping[b]) & 1)
        for a in range(len(left))
        for b in range(a + 1, len(left))
    )


def vertex_signature(adjacency: list[int], vertex: int) -> tuple[object, ...]:
    neighbors = [
        other
        for other in range(len(adjacency))
        if (adjacency[vertex] >> other) & 1
    ]
    neighbor_degrees = sorted(adjacency[other].bit_count() for other in neighbors)
    triangles = sum(
        (adjacency[left] >> right) & 1
        for offset, left in enumerate(neighbors)
        for right in neighbors[offset + 1 :]
    )
    return (
        len(neighbors),
        triangles,
        tuple(neighbor_degrees),
        vertex,
    )


def swap_delta(
    left: list[int],
    right: list[int],
    mapping: list[int],
    first: int,
    second: int,
) -> int:
    old = 0
    new = 0
    mapped_first = mapping[first]
    mapped_second = mapping[second]
    for other in range(len(left)):
        if other in (first, second):
            continue
        mapped_other = mapping[other]
        left_first = (left[first] >> other) & 1
        left_second = (left[second] >> other) & 1
        old += left_first != ((right[mapped_first] >> mapped_other) & 1)
        old += left_second != ((right[mapped_second] >> mapped_other) & 1)
        new += left_first != ((right[mapped_second] >> mapped_other) & 1)
        new += left_second != ((right[mapped_first] >> mapped_other) & 1)
    return new - old


def locally_align(
    left: list[int], right: list[int], initial: list[int]
) -> tuple[int, list[int], int]:
    mapping = initial.copy()
    distance = edge_hamming(left, right, mapping)
    iterations = 0
    while True:
        best_delta = 0
        best_pair: tuple[int, int] | None = None
        for first in range(len(left)):
            for second in range(first + 1, len(left)):
                delta = swap_delta(left, right, mapping, first, second)
                if delta < best_delta:
                    best_delta = delta
                    best_pair = (first, second)
        if best_pair is None:
            break
        first, second = best_pair
        mapping[first], mapping[second] = mapping[second], mapping[first]
        distance += best_delta
        iterations += 1
    if distance != edge_hamming(left, right, mapping):
        raise RuntimeError("incremental alignment distance is inconsistent")
    return distance, mapping, iterations


def align(left: list[int], right: list[int]) -> tuple[int, list[int], str, int]:
    identity = list(range(len(left)))
    left_order = sorted(
        range(len(left)), key=lambda vertex: vertex_signature(left, vertex)
    )
    right_order = sorted(
        range(len(right)), key=lambda vertex: vertex_signature(right, vertex)
    )
    signature_mapping = [0] * len(left)
    for left_vertex, right_vertex in zip(left_order, right_order):
        signature_mapping[left_vertex] = right_vertex
    candidates = [
        (*locally_align(left, right, identity), "identity"),
        (*locally_align(left, right, signature_mapping), "signature"),
    ]
    distance, mapping, iterations, origin = min(
        candidates,
        key=lambda item: (item[0], item[1], item[3]),
    )
    return distance, mapping, origin, iterations


def distribution(values: list[int]) -> dict[str, float | int]:
    return {
        "minimum": min(values),
        "maximum": max(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--summary",
        type=Path,
        default=ROOT
        / "results/verification/conflict_block_catalog22_followup_summary.json",
    )
    parser.add_argument(
        "--member-source",
        choices=("start", "final"),
        default="start",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    if (
        summary.get("completed_run_count") != 22
        or summary.get("best_objective") != 2
        or summary.get("valid_candidate_found") is not False
    ):
        raise SystemExit("elite summary is not the completed 22-graph E=2 pool")

    elites: list[dict[str, object]] = []
    oriented: list[list[int]] = []
    for run in summary["runs"]:
        if args.member_source == "start":
            member_path = run["start"]
            member_sha256 = run["start_sha256"]
            member_cliques = run["initial_C5"]
            member_independent = run["initial_I5"]
        else:
            member_path = run["final_candidate"]
            member_sha256 = run["final_candidate_sha256"]
            member_cliques = run["C5"]
            member_independent = run["I5"]
        path = ROOT / member_path
        if sha256(path) != member_sha256:
            raise SystemExit(f"elite hash mismatch: {path}")
        graph = read_graph(path)
        use_complement = member_cliques == 0 and member_independent == 2
        if not use_complement and not (
            member_cliques == 2 and member_independent == 0
        ):
            raise SystemExit("elite is not one-sided E=2")
        normalized = complement(graph) if use_complement else graph
        oriented.append(normalized)
        elites.append(
            {
                "catalog_line": run["catalog_line"],
                "path": member_path,
                "sha256": member_sha256,
                "input_C5": member_cliques,
                "input_I5": member_independent,
                "complemented_to_C5_only": use_complement,
                "oriented_graph6_sha256": graph_sha256(normalized),
                "oriented_edge_count": sum(
                    neighbors.bit_count() for neighbors in normalized
                )
                // 2,
            }
        )

    raw_distances: list[int] = []
    oriented_distances: list[int] = []
    aligned_distances: list[int] = []
    pair_records: list[dict[str, object]] = []
    for left in range(len(elites)):
        raw_left = read_graph(ROOT / str(elites[left]["path"]))
        for right in range(left + 1, len(elites)):
            raw_right = read_graph(ROOT / str(elites[right]["path"]))
            raw_distance = edge_hamming(raw_left, raw_right)
            oriented_distance = edge_hamming(oriented[left], oriented[right])
            distance, mapping, origin, iterations = align(
                oriented[left], oriented[right]
            )
            raw_distances.append(raw_distance)
            oriented_distances.append(oriented_distance)
            aligned_distances.append(distance)
            pair_records.append(
                {
                    "left_index": left,
                    "right_index": right,
                    "left_catalog_line": elites[left]["catalog_line"],
                    "right_catalog_line": elites[right]["catalog_line"],
                    "raw_labeled_hamming": raw_distance,
                    "oriented_labeled_hamming": oriented_distance,
                    "aligned_hamming": distance,
                    "alignment_origin": origin,
                    "alignment_swap_iterations": iterations,
                    "right_vertex_for_left_label": mapping,
                }
            )

    unused = set(range(len(elites)))
    selected: list[dict[str, object]] = []
    require_opposite_input_sides = args.member_source == "start"
    for record in sorted(
        pair_records,
        key=lambda item: (
            -int(item["aligned_hamming"]),
            int(item["left_catalog_line"]),
            int(item["right_catalog_line"]),
        ),
    ):
        left = int(record["left_index"])
        right = int(record["right_index"])
        if require_opposite_input_sides and (
            bool(elites[left]["complemented_to_C5_only"])
            == bool(elites[right]["complemented_to_C5_only"])
        ):
            continue
        if left in unused and right in unused:
            selected.append(record)
            unused.remove(left)
            unused.remove(right)
    if unused or len(selected) != 11:
        raise RuntimeError("greedy alignment pairing did not cover the pool")

    pair_lookup = {
        (int(item["left_index"]), int(item["right_index"])): item
        for item in pair_records
    }

    def pair_record(first: int, second: int) -> dict[str, object]:
        return pair_lookup[(min(first, second), max(first, second))]

    two_opt_updates = 0
    while True:
        best: tuple[
            tuple[int, int, int],
            tuple[int, int, int, int],
            int,
            int,
            dict[str, object],
            dict[str, object],
        ] | None = None
        for first_index in range(len(selected)):
            for second_index in range(first_index + 1, len(selected)):
                old_first = selected[first_index]
                old_second = selected[second_index]
                a = int(old_first["left_index"])
                b = int(old_first["right_index"])
                c = int(old_second["left_index"])
                d = int(old_second["right_index"])
                old_distances = sorted(
                    [
                        int(old_first["aligned_hamming"]),
                        int(old_second["aligned_hamming"]),
                    ]
                )
                old_score = (
                    sum(old_distances),
                    old_distances[0],
                    old_distances[1],
                )
                endpoint_options = [((a, c), (b, d)), ((a, d), (b, c))]
                if require_opposite_input_sides:
                    complemented = [
                        vertex
                        for vertex in (a, b, c, d)
                        if bool(
                            elites[vertex]["complemented_to_C5_only"]
                        )
                    ]
                    retained = [
                        vertex
                        for vertex in (a, b, c, d)
                        if not bool(
                            elites[vertex]["complemented_to_C5_only"]
                        )
                    ]
                    endpoint_options = [
                        (
                            (complemented[0], retained[1]),
                            (complemented[1], retained[0]),
                        )
                    ]
                for endpoints in endpoint_options:
                    new_first = pair_record(*endpoints[0])
                    new_second = pair_record(*endpoints[1])
                    new_distances = sorted(
                        [
                            int(new_first["aligned_hamming"]),
                            int(new_second["aligned_hamming"]),
                        ]
                    )
                    new_score = (
                        sum(new_distances),
                        new_distances[0],
                        new_distances[1],
                    )
                    if new_score <= old_score:
                        continue
                    lines = tuple(
                        sorted(
                            (
                                int(new_first["left_catalog_line"]),
                                int(new_first["right_catalog_line"]),
                                int(new_second["left_catalog_line"]),
                                int(new_second["right_catalog_line"]),
                            )
                        )
                    )
                    candidate = (
                        new_score,
                        lines,
                        first_index,
                        second_index,
                        new_first,
                        new_second,
                    )
                    if best is None or candidate[:2] > best[:2]:
                        best = candidate
        if best is None:
            break
        _, _, first_index, second_index, new_first, new_second = best
        selected[first_index] = new_first
        selected[second_index] = new_second
        two_opt_updates += 1
    selected.sort(
        key=lambda item: (
            -int(item["aligned_hamming"]),
            int(item["left_catalog_line"]),
            int(item["right_catalog_line"]),
        )
    )

    result = {
        "schema": "ramsey55.path_relink_elite_pool_audit.v1",
        "algorithm": "complement_normalized_two_start_swap_alignment_v1",
        "member_source": args.member_source,
        "pair_selection": (
            "Sort all pairs by decreasing aligned Hamming distance, then "
            "catalog line numbers. For the start pool, require one original "
            "I5-only graph and one original C5-only graph in every pair; "
            "greedily take a pair iff both endpoints are unused. Then apply "
            "deterministic improving two-pair rewirings, prioritizing total "
            "aligned distance and then the smaller affected distance."
        ),
        "required_opposite_input_color_sides": require_opposite_input_sides,
        "pair_selection_two_opt_updates": two_opt_updates,
        "summary": str(args.summary.relative_to(ROOT)),
        "summary_sha256": sha256(args.summary),
        "elite_count": len(elites),
        "all_raw_graphs_unique": len(
            {str(item["sha256"]) for item in elites}
        )
        == len(elites),
        "complemented_count": sum(
            bool(item["complemented_to_C5_only"]) for item in elites
        ),
        "orientation_policy": (
            "Complement precisely I5-only E=2 graphs; retain C5-only E=2 "
            "graphs, so every oriented elite is C5-only."
        ),
        "elites": elites,
        "all_pair_count": len(pair_records),
        "raw_labeled_hamming": distribution(raw_distances),
        "oriented_labeled_hamming": distribution(oriented_distances),
        "locally_aligned_hamming": distribution(aligned_distances),
        "selected_pair_count": len(selected),
        "selected_pairs": selected,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
