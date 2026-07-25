#!/usr/bin/env python3
"""Measure the k=3 induced-odd-wheel filter on small unlabeled graphs.

This is an observational probe, not a coverage certificate.  It deliberately
cross-checks the bitset evaluator and the set/frozenset evaluator, including
two separately written induced-wheel recognizers.
"""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT))

from src.verifier_a.core import (  # noqa: E402
    BitGraph,
    alpha as alpha_a,
    clique_cover as clique_cover_a,
    domination_number as domination_number_a,
    eternal_domination_number as eternal_domination_number_a,
)
from src.verifier_b.eternal import eternal_domination_number as eternal_b  # noqa: E402
from src.verifier_b.graph import Graph  # noqa: E402
from src.verifier_b.invariants import (  # noqa: E402
    clique_cover_number as clique_cover_b,
    domination_number as domination_number_b,
    independence_number as alpha_b,
)


def is_connected_a(graph: BitGraph) -> bool:
    """Test connectivity with packed neighborhoods."""

    if graph.n == 0:
        return False
    seen = 1
    frontier = 1
    while frontier:
        vertex_bit = frontier & -frontier
        frontier ^= vertex_bit
        vertex = vertex_bit.bit_length() - 1
        new = graph.adj[vertex] & ~seen
        seen |= new
        frontier |= new
    return seen == graph.full


def _is_one_cycle_a(graph: BitGraph, rim: tuple[int, ...]) -> bool:
    rim_mask = sum(1 << vertex for vertex in rim)
    if any((graph.adj[vertex] & rim_mask).bit_count() != 2 for vertex in rim):
        return False
    seen = 1 << rim[0]
    frontier = seen
    while frontier:
        vertex_bit = frontier & -frontier
        frontier ^= vertex_bit
        vertex = vertex_bit.bit_length() - 1
        new = graph.adj[vertex] & rim_mask & ~seen
        seen |= new
        frontier |= new
    return seen == rim_mask


def odd_wheel_lengths_a(graph: BitGraph) -> frozenset[int]:
    """Recognize induced odd wheels using the bitset representation."""

    lengths: set[int] = set()
    for length in range(5, graph.n, 2):
        for rim in combinations(range(graph.n), length):
            if not _is_one_cycle_a(graph, rim):
                continue
            rim_mask = sum(1 << vertex for vertex in rim)
            for hub in range(graph.n):
                if rim_mask & (1 << hub):
                    continue
                if graph.adj[hub] & rim_mask == rim_mask:
                    lengths.add(length)
                    break
    return frozenset(lengths)


def _is_one_cycle_b(graph: Graph, rim: frozenset[int]) -> bool:
    if any(len(graph.adjacency[vertex] & rim) != 2 for vertex in rim):
        return False
    seen = {next(iter(rim))}
    frontier = set(seen)
    while frontier:
        vertex = frontier.pop()
        new = set(graph.adjacency[vertex] & rim) - seen
        seen.update(new)
        frontier.update(new)
    return seen == set(rim)


def odd_wheel_lengths_b(graph: Graph) -> frozenset[int]:
    """Recognize induced odd wheels using ordinary Python sets."""

    lengths: set[int] = set()
    all_vertices = frozenset(graph.vertices)
    for length in range(5, graph.order, 2):
        for rim_tuple in combinations(graph.vertices, length):
            rim = frozenset(rim_tuple)
            if not _is_one_cycle_b(graph, rim):
                continue
            if any(
                rim <= graph.adjacency[hub]
                for hub in all_vertices - rim
            ):
                lengths.add(length)
    return frozenset(lengths)


def audit_order(geng: Path, order: int) -> dict[str, object]:
    """Stream one order, cross-checking every graph that passes the prefilter."""

    process = subprocess.Popen(
        (str(geng), "-qc", str(order)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if process.stdout is None or process.stderr is None:
        raise RuntimeError("failed to capture geng output")

    connected_count = 0
    static_count = 0
    eternal_three_count = 0
    wheel_count = 0
    wheel_lengths: Counter[int] = Counter()

    for record in process.stdout:
        graph_a = BitGraph.from_graph6(record)
        if not is_connected_a(graph_a):
            raise AssertionError("geng -c emitted a disconnected graph")
        connected_count += 1

        gamma_a = domination_number_a(graph_a)
        independence_a = alpha_a(graph_a)
        theta_a = clique_cover_a(graph_a).value
        if not (gamma_a == independence_a == 3 and theta_a > 3):
            continue
        static_count += 1

        graph_b = Graph.from_graph6(record)
        static_b = (
            domination_number_b(graph_b),
            alpha_b(graph_b),
            clique_cover_b(graph_b),
        )
        if static_b != (gamma_a, independence_a, theta_a):
            raise AssertionError(
                f"static evaluator disagreement on {record.strip()}: "
                f"A={(gamma_a, independence_a, theta_a)}, B={static_b}"
            )

        eternal_value_a = eternal_domination_number_a(graph_a)
        eternal_value_b = eternal_b(graph_b)
        if eternal_value_a != eternal_value_b:
            raise AssertionError(
                f"eternal evaluator disagreement on {record.strip()}: "
                f"A={eternal_value_a}, B={eternal_value_b}"
            )
        if eternal_value_a == 3:
            eternal_three_count += 1

        lengths_a = odd_wheel_lengths_a(graph_a.complement())
        lengths_b = odd_wheel_lengths_b(graph_b.complement())
        if lengths_a != lengths_b:
            raise AssertionError(
                f"wheel recognizer disagreement on {record.strip()}: "
                f"A={sorted(lengths_a)}, B={sorted(lengths_b)}"
            )
        if lengths_a:
            wheel_count += 1
            for length in lengths_a:
                wheel_lengths[length] += 1
            if eternal_value_a == 3:
                raise AssertionError(
                    "empirical violation of the odd-wheel obstruction on "
                    f"{record.strip()}"
                )

    stderr = process.stderr.read()
    return_code = process.wait()
    if return_code:
        raise RuntimeError(
            f"geng failed for order {order} with status {return_code}: {stderr}"
        )

    return {
        "order": order,
        "connected_unlabeled_graphs": connected_count,
        "static_gamma_alpha_3_theta_gt_3": static_count,
        "eternal_three": eternal_three_count,
        "odd_wheel_rejections": wheel_count,
        "wheel_lengths": {
            str(length): wheel_lengths[length]
            for length in sorted(wheel_lengths)
        },
        "implementations": ["verifier_a", "verifier_b"],
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--geng",
        type=Path,
        default=REPOSITORY_ROOT / "tools" / "nauty2_9_3" / "geng",
    )
    parser.add_argument(
        "orders",
        type=int,
        nargs="*",
        default=(6, 7, 8),
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    if not arguments.geng.is_file():
        raise SystemExit(f"geng not found: {arguments.geng}")
    results = [
        audit_order(arguments.geng.resolve(), order)
        for order in arguments.orders
    ]
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
