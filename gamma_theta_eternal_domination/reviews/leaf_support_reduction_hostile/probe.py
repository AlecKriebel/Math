#!/usr/bin/env python3
"""Clean-room small-graph probe for the leaf--support reduction.

Nauty's ``geng`` supplies only the unlabeled graph6 instances.  Graph6 parsing,
all graph parameters, and the one-guard eternal fixed point are computed below
from integer adjacency masks.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
import subprocess


def popcount(mask: int) -> int:
    return mask.bit_count()


def parse_graph6(encoded: str) -> tuple[int, ...]:
    data = encoded.encode("ascii")
    assert data and data[0] != ord("~"), "probe only handles graph6 order <= 62"
    n = data[0] - 63
    bits: list[int] = []
    for byte in data[1:]:
        value = byte - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    assert len(bits) >= needed
    adjacency = [0] * n
    cursor = 0
    for right in range(1, n):
        for left in range(right):
            if bits[cursor]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            cursor += 1
    return tuple(adjacency)


def generate_unlabeled_graphs(maximum_order: int) -> list[tuple[str, tuple[int, ...]]]:
    repository = Path(__file__).resolve().parents[2]
    geng = repository / "tools" / "nauty2_9_3" / "geng"
    assert geng.is_file()
    instances: list[tuple[str, tuple[int, ...]]] = []
    for order in range(1, maximum_order + 1):
        completed = subprocess.run(
            [str(geng), "-q", str(order)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for line in completed.stdout.splitlines():
            encoded = line.strip()
            if encoded:
                adjacency = parse_graph6(encoded)
                assert len(adjacency) == order
                instances.append((encoded, adjacency))
    return instances


def is_connected(adjacency: tuple[int, ...]) -> bool:
    if not adjacency:
        return False
    reached = 1
    frontier = 1
    while frontier:
        next_frontier = 0
        cursor = frontier
        while cursor:
            vertex_bit = cursor & -cursor
            vertex = vertex_bit.bit_length() - 1
            next_frontier |= adjacency[vertex]
            cursor ^= vertex_bit
        next_frontier &= ~reached
        reached |= next_frontier
        frontier = next_frontier
    return reached == (1 << len(adjacency)) - 1


def induced_adjacency(
    adjacency: tuple[int, ...], kept_vertices: tuple[int, ...]
) -> tuple[int, ...]:
    old_to_new = {old: new for new, old in enumerate(kept_vertices)}
    return tuple(
        sum(
            1 << old_to_new[old_neighbor]
            for old_neighbor in kept_vertices
            if adjacency[old_vertex] & (1 << old_neighbor)
        )
        for old_vertex in kept_vertices
    )


def is_dominating(adjacency: tuple[int, ...], state: int) -> bool:
    dominated = state
    cursor = state
    while cursor:
        guard_bit = cursor & -cursor
        guard = guard_bit.bit_length() - 1
        dominated |= adjacency[guard]
        cursor ^= guard_bit
    return dominated == (1 << len(adjacency)) - 1


def is_independent(adjacency: tuple[int, ...], state: int) -> bool:
    cursor = state
    while cursor:
        vertex_bit = cursor & -cursor
        vertex = vertex_bit.bit_length() - 1
        if adjacency[vertex] & (state ^ vertex_bit):
            return False
        cursor ^= vertex_bit
    return True


def is_clique(adjacency: tuple[int, ...], state: int) -> bool:
    cursor = state
    while cursor:
        vertex_bit = cursor & -cursor
        vertex = vertex_bit.bit_length() - 1
        if (state ^ vertex_bit) & ~adjacency[vertex]:
            return False
        cursor ^= vertex_bit
    return True


def domination_number(adjacency: tuple[int, ...]) -> int:
    n = len(adjacency)
    for size in range(n + 1):
        for vertices in combinations(range(n), size):
            state = sum(1 << vertex for vertex in vertices)
            if is_dominating(adjacency, state):
                return size
    raise AssertionError("the full vertex set must dominate")


def independence_number(adjacency: tuple[int, ...]) -> int:
    return max(
        popcount(state)
        for state in range(1 << len(adjacency))
        if is_independent(adjacency, state)
    )


def maximal_independent_sizes(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    full = (1 << len(adjacency)) - 1
    sizes: list[int] = []
    for state in range(1 << len(adjacency)):
        if not is_independent(adjacency, state):
            continue
        outside = full ^ state
        if all(
            not is_independent(adjacency, state | (1 << vertex))
            for vertex in range(len(adjacency))
            if outside & (1 << vertex)
        ):
            sizes.append(popcount(state))
    return tuple(sorted(sizes))


def clique_partition_number(adjacency: tuple[int, ...]) -> int:
    n = len(adjacency)
    full = (1 << n) - 1
    clique = tuple(is_clique(adjacency, state) for state in range(1 << n))
    best = [n + 1] * (1 << n)
    best[0] = 0
    for covered in range(1 << n):
        if best[covered] > n:
            continue
        remaining = full ^ covered
        if not remaining:
            continue
        anchor = remaining & -remaining
        submask = remaining
        while submask:
            if submask & anchor and clique[submask]:
                new_covered = covered | submask
                best[new_covered] = min(best[new_covered], best[covered] + 1)
            submask = (submask - 1) & remaining
    return best[full]


def eternal_kernel(adjacency: tuple[int, ...], guard_count: int) -> frozenset[int]:
    n = len(adjacency)
    full = (1 << n) - 1
    alive = {
        state
        for state in range(1 << n)
        if popcount(state) == guard_count and is_dominating(adjacency, state)
    }
    while True:
        retained: set[int] = set()
        for state in alive:
            valid = True
            unoccupied = full ^ state
            for attacked in range(n):
                attacked_bit = 1 << attacked
                if not unoccupied & attacked_bit:
                    continue
                responders = adjacency[attacked] & state
                has_response = False
                while responders:
                    guard_bit = responders & -responders
                    successor = (state ^ guard_bit) | attacked_bit
                    if successor in alive:
                        has_response = True
                        break
                    responders ^= guard_bit
                if not has_response:
                    valid = False
                    break
            if valid:
                retained.add(state)
        if retained == alive:
            return frozenset(alive)
        alive = retained


def eternal_domination_number(adjacency: tuple[int, ...]) -> int:
    for guard_count in range(len(adjacency) + 1):
        if eternal_kernel(adjacency, guard_count):
            return guard_count
    raise AssertionError("the full occupied state is eternally closed")


def verify_leaf_slice(
    adjacency: tuple[int, ...],
    leaf: int,
    support: int,
    guard_count: int,
    family: frozenset[int],
) -> None:
    n = len(adjacency)
    kept = tuple(vertex for vertex in range(n) if vertex not in (leaf, support))
    q_adjacency = induced_adjacency(adjacency, kept)
    old_to_new = {old: new for new, old in enumerate(kept)}

    projected: set[int] = set()
    for state in family:
        if not state & (1 << leaf):
            continue
        assert not state & (1 << support)
        q_state = sum(
            1 << old_to_new[old]
            for old in kept
            if state & (1 << old)
        )
        assert popcount(q_state) == guard_count - 1
        assert is_dominating(q_adjacency, q_state)
        projected.add(q_state)

    assert projected
    full_q = (1 << len(q_adjacency)) - 1
    for q_state in projected:
        unoccupied = full_q ^ q_state
        for attacked in range(len(q_adjacency)):
            attacked_bit = 1 << attacked
            if not unoccupied & attacked_bit:
                continue
            responders = q_adjacency[attacked] & q_state
            assert any(
                ((q_state ^ (1 << guard)) | attacked_bit) in projected
                for guard in range(len(q_adjacency))
                if responders & (1 << guard)
            )


def main() -> None:
    instances = generate_unlabeled_graphs(maximum_order=8)

    checked_graphs = 0
    equality_graphs = 0
    leaf_instances = 0
    exception_graphs: list[dict[str, object]] = []

    for encoded, adjacency in instances:
        n = len(adjacency)
        edge_count = sum(popcount(neighborhood) for neighborhood in adjacency) // 2
        gamma = domination_number(adjacency)
        gamma_eternal = eternal_domination_number(adjacency)

        if is_connected(adjacency) and min(map(popcount, adjacency)) >= 2:
            if 5 * gamma > 2 * n:
                alpha_exception = independence_number(adjacency)
                theta_exception = clique_partition_number(adjacency)
                exception_graphs.append(
                    {
                        "order": n,
                        "size": edge_count,
                        "gamma": gamma,
                        "alpha": alpha_exception,
                        "gamma_eternal": gamma_eternal,
                        "theta": theta_exception,
                        "graph6": encoded,
                    }
                )

        checked_graphs += 1
        if gamma != gamma_eternal:
            continue
        equality_graphs += 1
        alpha = independence_number(adjacency)
        theta = clique_partition_number(adjacency)
        family = eternal_kernel(adjacency, gamma)
        assert family

        for leaf in range(n):
            if popcount(adjacency[leaf]) != 1:
                continue
            support = (adjacency[leaf] & -adjacency[leaf]).bit_length() - 1
            kept = tuple(vertex for vertex in range(n) if vertex not in (leaf, support))
            if not kept:
                continue
            leaf_instances += 1
            q_adjacency = induced_adjacency(adjacency, kept)
            q_gamma = domination_number(q_adjacency)
            q_alpha = independence_number(q_adjacency)
            q_gamma_eternal = eternal_domination_number(q_adjacency)
            q_theta = clique_partition_number(q_adjacency)
            q_maximal_sizes = maximal_independent_sizes(q_adjacency)

            assert alpha == gamma
            assert q_gamma == gamma - 1
            assert q_alpha == gamma - 1
            assert q_gamma_eternal == gamma - 1
            assert q_maximal_sizes
            assert set(q_maximal_sizes) == {gamma - 1}
            assert theta == q_theta + 1
            verify_leaf_slice(adjacency, leaf, support, gamma, family)

    assert len(exception_graphs) == 7
    assert [item["order"] for item in exception_graphs] == [4] + [7] * 6

    result = {
        "schema": "leaf-support-hostile-probe-v1",
        "instance_source": "nauty 2.9.3 geng (unlabeled graph6 instances only)",
        "graph6_and_parameter_implementation": "clean-room integer bitmasks",
        "maximum_order": 8,
        "nonempty_unlabeled_graphs_checked": checked_graphs,
        "gamma_equals_gamma_eternal_graphs": equality_graphs,
        "eligible_leaf_instances_checked": leaf_instances,
        "mcuaig_shepherd_small_exception_census": exception_graphs,
        "verdict": "PASS",
    }
    output = Path(__file__).with_name("probe_result.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
