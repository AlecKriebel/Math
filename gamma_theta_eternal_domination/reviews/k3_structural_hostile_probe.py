#!/usr/bin/env python3
"""Independent definition-level probes for the day-one k=3 restrictions.

This review program deliberately imports neither campaign verifier, wheel
recognizer, nor graph class.  It parses small graph6 records into Boolean
matrices and implements domination, independence, clique partitioning, the
one-guard fixed point, and induced-wheel recognition directly.
"""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
GENG = ROOT / "tools" / "nauty2_9_3" / "geng"
Matrix = tuple[tuple[bool, ...], ...]


def decode_small_graph6(record: str) -> Matrix:
    """Decode canonical one-byte-order graph6 syntax (orders at most 62)."""

    record = record.strip()
    values = [ord(character) - 63 for character in record]
    if not values or not 0 <= values[0] <= 62:
        raise ValueError("unsupported graph6 header")
    order = values[0]
    bit_count = order * (order - 1) // 2
    expected_payload = (bit_count + 5) // 6
    if len(values) != expected_payload + 1:
        raise ValueError("wrong graph6 payload length")
    if any(not 0 <= value <= 63 for value in values[1:]):
        raise ValueError("invalid graph6 character")
    bits = tuple(
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    )
    if any(bits[bit_count:]):
        raise ValueError("nonzero graph6 padding")
    rows = [[False] * order for _ in range(order)]
    position = 0
    for higher in range(1, order):
        for lower in range(higher):
            rows[lower][higher] = rows[higher][lower] = bool(bits[position])
            position += 1
    return tuple(tuple(row) for row in rows)


def complement(matrix: Matrix) -> Matrix:
    order = len(matrix)
    return tuple(
        tuple(first != second and not matrix[first][second] for second in range(order))
        for first in range(order)
    )


def is_independent(matrix: Matrix, vertices: frozenset[int]) -> bool:
    return all(
        not matrix[first][second]
        for first, second in combinations(sorted(vertices), 2)
    )


def is_dominating(matrix: Matrix, vertices: frozenset[int]) -> bool:
    return all(
        vertex in vertices
        or any(matrix[vertex][guard] for guard in vertices)
        for vertex in range(len(matrix))
    )


def alpha(matrix: Matrix) -> int:
    vertices = range(len(matrix))
    return max(
        size
        for size in range(len(matrix) + 1)
        if any(
            is_independent(matrix, frozenset(subset))
            for subset in combinations(vertices, size)
        )
    )


def gamma(matrix: Matrix) -> int:
    vertices = range(len(matrix))
    return next(
        size
        for size in range(1, len(matrix) + 1)
        if any(
            is_dominating(matrix, frozenset(subset))
            for subset in combinations(vertices, size)
        )
    )


def theta(matrix: Matrix) -> int:
    """Minimum clique partition, assigned directly in the original graph."""

    order = len(matrix)
    assignment = [-1] * order

    def can_partition(color_count: int, vertex: int) -> bool:
        if vertex == order:
            return True
        for color in range(color_count):
            if all(
                assignment[earlier] != color or matrix[earlier][vertex]
                for earlier in range(vertex)
            ):
                assignment[vertex] = color
                if can_partition(color_count, vertex + 1):
                    return True
        assignment[vertex] = -1
        return False

    return next(
        color_count
        for color_count in range(1, order + 1)
        if can_partition(color_count, 0)
    )


def eternal_at_most(matrix: Matrix, guard_count: int) -> bool:
    """Literal greatest closed family over dominating configurations."""

    vertices = frozenset(range(len(matrix)))
    active = {
        frozenset(configuration)
        for configuration in combinations(vertices, guard_count)
        if is_dominating(matrix, frozenset(configuration))
    }
    changed = True
    while changed:
        changed = False
        doomed: set[frozenset[int]] = set()
        for state in active:
            for attack in vertices - state:
                if not any(
                    matrix[guard][attack]
                    and (state - {guard}) | {attack} in active
                    for guard in state
                ):
                    doomed.add(state)
                    break
        if doomed:
            active.difference_update(doomed)
            changed = True
    return bool(active)


def is_cycle_on(matrix: Matrix, rim: frozenset[int]) -> bool:
    if any(sum(matrix[v][w] for w in rim) != 2 for v in rim):
        return False
    reached = {next(iter(rim))}
    frontier = list(reached)
    while frontier:
        vertex = frontier.pop()
        for neighbor in rim - reached:
            if matrix[vertex][neighbor]:
                reached.add(neighbor)
                frontier.append(neighbor)
    return reached == set(rim)


def odd_wheel_lengths(matrix: Matrix) -> frozenset[int]:
    """Find induced K1 join odd cycles by subset definition."""

    vertices = frozenset(range(len(matrix)))
    found: set[int] = set()
    for length in range(5, len(matrix), 2):
        for rim_tuple in combinations(vertices, length):
            rim = frozenset(rim_tuple)
            if not is_cycle_on(matrix, rim):
                continue
            if any(
                all(matrix[hub][vertex] for vertex in rim)
                for hub in vertices - rim
            ):
                found.add(length)
    return frozenset(found)


def maximum_clique_size(matrix: Matrix) -> int:
    return alpha(complement(matrix))


def every_pair_has_common_neighbor(matrix: Matrix) -> bool:
    return all(
        any(matrix[first][w] and matrix[second][w] for w in range(len(matrix)))
        for first, second in combinations(range(len(matrix)), 2)
    )


def every_maximal_clique_is_triangle(matrix: Matrix) -> bool:
    vertices = frozenset(range(len(matrix)))
    for size in range(1, len(matrix) + 1):
        for subset_tuple in combinations(vertices, size):
            subset = frozenset(subset_tuple)
            if not is_independent(complement(matrix), subset):
                continue
            if not any(
                all(matrix[outside][inside] for inside in subset)
                for outside in vertices - subset
            ) and size != 3:
                return False
    return True


def minimum_degree(matrix: Matrix) -> int:
    return min(sum(row) for row in matrix)


def diameter_at_most_two(matrix: Matrix) -> bool:
    return all(
        matrix[first][second]
        or any(matrix[first][w] and matrix[second][w] for w in range(len(matrix)))
        for first, second in combinations(range(len(matrix)), 2)
    )


def geng_records(order: int, *, connected: bool) -> tuple[str, ...]:
    option = "-qc" if connected else "-q"
    result = subprocess.run(
        (str(GENG), option, str(order)),
        check=True,
        capture_output=True,
        text=True,
    )
    return tuple(line for line in result.stdout.splitlines() if line)


def wheel_graph(rim_length: int) -> Matrix:
    order = rim_length + 1
    hub = rim_length
    rows = [[False] * order for _ in range(order)]
    for vertex in range(rim_length):
        successor = (vertex + 1) % rim_length
        rows[vertex][successor] = rows[successor][vertex] = True
        rows[hub][vertex] = rows[vertex][hub] = True
    return tuple(tuple(row) for row in rows)


def base_wheel_checks() -> list[dict[str, int]]:
    results: list[dict[str, int]] = []
    for rim_length in (5, 7, 9, 11):
        graph = complement(wheel_graph(rim_length))
        assert gamma(graph) == 3
        assert not eternal_at_most(graph, 3)
        assert eternal_at_most(graph, 4)
        results.append(
            {
                "rim_length": rim_length,
                "order": rim_length + 1,
                "gamma": 3,
                "gamma_infinity": 4,
            }
        )
    return results


def local_w5_check() -> None:
    graph = complement(wheel_graph(5))
    center = 5
    state = frozenset((center, 0, 1))
    attack = 3
    assert is_independent(graph, state)
    assert attack not in state
    successors = []
    for guard in state:
        if graph[guard][attack]:
            successor = (state - {guard}) | {attack}
            successors.append((guard, successor, is_dominating(graph, successor)))
    assert successors == [
        (0, frozenset((center, 1, 3)), False),
        (1, frozenset((center, 0, 3)), False),
    ]


def small_order_counts() -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for order in (6, 7, 8):
        static_count = 0
        wheel_count = 0
        eternal_three = 0
        wheel_lengths: dict[int, int] = {}
        theorem_two_hosts = 0
        for record in geng_records(order, connected=True):
            graph = decode_small_graph6(record)
            host_lengths = odd_wheel_lengths(complement(graph))
            if host_lengths:
                theorem_two_hosts += 1
                assert not eternal_at_most(graph, 3)
            if gamma(graph) != 3 or alpha(graph) != 3 or theta(graph) <= 3:
                continue
            static_count += 1
            if eternal_at_most(graph, 3):
                eternal_three += 1
                assert not host_lengths
            if host_lengths:
                wheel_count += 1
                for length in host_lengths:
                    wheel_lengths[length] = wheel_lengths.get(length, 0) + 1
        output.append(
            {
                "order": order,
                "connected_unlabeled_graphs": len(
                    geng_records(order, connected=True)
                ),
                "static_prefilter": static_count,
                "odd_wheel_rejections": wheel_count,
                "eternal_three": eternal_three,
                "wheel_lengths": wheel_lengths,
                "all_odd_wheel_hosts_checked": theorem_two_hosts,
            }
        )
    return output


def redundancy_checks() -> list[dict[str, int]]:
    output: list[dict[str, int]] = []
    for order in range(3, 9):
        premise_count = 0
        for record in geng_records(order, connected=False):
            graph = decode_small_graph6(record)
            if maximum_clique_size(graph) != 3:
                continue
            if not every_pair_has_common_neighbor(graph):
                continue
            premise_count += 1
            assert every_maximal_clique_is_triangle(graph)
            assert minimum_degree(graph) >= 2
            assert diameter_at_most_two(graph)
        output.append({"order": order, "premise_graphs": premise_count})
    return output


def main() -> None:
    if not GENG.is_file():
        raise SystemExit(f"geng not found: {GENG}")
    local_w5_check()
    result = {
        "base_wheels": base_wheel_checks(),
        "small_order_counts": small_order_counts(),
        "static_redundancy": redundancy_checks(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
