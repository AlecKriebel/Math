#!/usr/bin/env python3
"""Independent hostile replay for the repair-square holonomy candidate.

This file deliberately shares no import or transition routine with the
candidate.  Graph states are integer bitmasks, the eternal kernel is rebuilt
from the one-guard definition, and the abstract repair audit explicitly tests
shortest-path descent, non-simple synchronized walks, and parity padding.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter, deque
from functools import lru_cache


CONTROL_G6 = "NslalntvXzn^{~n||^w"
U, X, P, Q, R, B, A, W, Z = 0, 1, 2, 3, 4, 5, 6, 10, 13


def graph6_to_masks(text: str) -> tuple[int, ...]:
    """Decode the short graph6 form directly into open-neighborhood masks."""
    encoded = [ord(character) - 63 for character in text]
    if not encoded or not 0 <= encoded[0] <= 62:
        raise AssertionError("clean-room decoder accepts only short graph6")
    order = encoded[0]
    stream = "".join(f"{value:06b}" for value in encoded[1:])
    needed = order * (order - 1) // 2
    if len(stream) < needed or "1" in stream[needed:]:
        raise AssertionError("bad graph6 length or padding")
    adjacency = [0] * order
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if stream[cursor] == "1":
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return tuple(adjacency)


def masks_of_weight(order: int, weight: int):
    for vertices in itertools.combinations(range(order), weight):
        state = 0
        for vertex in vertices:
            state |= 1 << vertex
        yield state


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    remaining = state
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        remaining ^= bit
        if adjacency[vertex] & remaining:
            return False
    return True


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in vertices(state):
        covered |= adjacency[vertex]
    return covered == (1 << len(adjacency)) - 1


def greatest_kernel(adjacency: tuple[int, ...], guard_count: int):
    """Literal synchronous greatest-fixed-point deletion from the definition."""
    order = len(adjacency)
    live = {
        state
        for state in masks_of_weight(order, guard_count)
        if dominates(adjacency, state)
    }
    rank: dict[int, int] = {}
    wave_sizes: list[int] = []
    round_number = 0
    all_vertices = (1 << order) - 1
    while True:
        doomed = set()
        for state in live:
            unattacked = all_vertices ^ state
            for target in vertices(unattacked):
                target_bit = 1 << target
                legal = False
                for guard in vertices(state & adjacency[target]):
                    successor = (state ^ (1 << guard)) | target_bit
                    if successor in live:
                        legal = True
                        break
                if not legal:
                    doomed.add(state)
                    break
        if not doomed:
            return live, rank, wave_sizes
        round_number += 1
        for state in doomed:
            rank[state] = round_number
        live -= doomed
        wave_sizes.append(len(doomed))


def parameter_tuple(adjacency: tuple[int, ...]):
    order = len(adjacency)
    all_masks = range(1, 1 << order)
    gamma = min(mask.bit_count() for mask in all_masks if dominates(adjacency, mask))
    alpha = max(mask.bit_count() for mask in all_masks if independent(adjacency, mask))
    independent_domination = min(
        mask.bit_count()
        for mask in all_masks
        if independent(adjacency, mask) and dominates(adjacency, mask)
    )

    complement = tuple(
        ((1 << order) - 1) ^ (1 << vertex) ^ adjacency[vertex]
        for vertex in range(order)
    )

    def colorable(color_count: int):
        colors = [-1] * order

        def search(colored: int):
            if colored == order:
                return tuple(colors)
            candidates = [vertex for vertex in range(order) if colors[vertex] < 0]
            vertex = max(
                candidates,
                key=lambda item: (
                    len(
                        {
                            colors[neighbor]
                            for neighbor in vertices(complement[item])
                            if colors[neighbor] >= 0
                        }
                    ),
                    (complement[item] & sum(1 << c for c in candidates)).bit_count(),
                    item,
                ),
            )
            forbidden = {
                colors[neighbor]
                for neighbor in vertices(complement[vertex])
                if colors[neighbor] >= 0
            }
            for color in range(color_count):
                if color in forbidden:
                    continue
                colors[vertex] = color
                answer = search(colored + 1)
                if answer is not None:
                    return answer
                colors[vertex] = -1
            return None

        return search(0)

    theta = next(count for count in range(1, order + 1) if colorable(count))
    coloring = colorable(theta)
    kernels = {}
    gamma_infinity = None
    for size in range(1, alpha + 1):
        kernels[size] = greatest_kernel(adjacency, size)
        if kernels[size][0] and gamma_infinity is None:
            gamma_infinity = size
    if gamma_infinity is None:
        for size in range(alpha + 1, order + 1):
            kernels[size] = greatest_kernel(adjacency, size)
            if kernels[size][0]:
                gamma_infinity = size
                break
    assert gamma_infinity is not None
    return {
        "gamma": gamma,
        "i": independent_domination,
        "alpha": alpha,
        "gamma_infinity": gamma_infinity,
        "theta": theta,
    }, coloring, kernels


def mask(items) -> int:
    result = 0
    for item in items:
        result |= 1 << item
    return result


def active_rows(
    adjacency: tuple[int, ...],
    family: set[int],
    source: int,
    target: int,
):
    rows = []
    for state in masks_of_weight(len(adjacency), 3):
        if not independent(adjacency, state):
            continue
        if not state & (1 << source) or state & (1 << target):
            continue
        successor = (state ^ (1 << source)) | (1 << target)
        rows.append(
            {
                "state": sorted(vertices(state)),
                "successor_retained": successor in family,
            }
        )
    if not rows:
        raise AssertionError("activity relation has no independent source state")
    return rows


def complement_link(adjacency: tuple[int, ...], pivot: int):
    order = len(adjacency)
    link_vertices = [
        vertex
        for vertex in range(order)
        if vertex != pivot and not adjacency[pivot] & (1 << vertex)
    ]
    link_set = set(link_vertices)
    link = {
        vertex: {
            other
            for other in link_set - {vertex}
            if not adjacency[vertex] & (1 << other)
        }
        for vertex in link_vertices
    }
    components = []
    unseen = set(link_vertices)
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        queue = deque([root])
        component = []
        while queue:
            vertex = queue.popleft()
            component.append(vertex)
            for other in sorted(link[vertex] & unseen):
                unseen.remove(other)
                queue.append(other)
        components.append(sorted(component))
    return link, sorted(components)


def audit_control():
    adjacency = graph6_to_masks(CONTROL_G6)
    parameters, coloring, kernels = parameter_tuple(adjacency)
    expected = {
        "gamma": 2,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    if parameters != expected:
        raise AssertionError(("control parameter mismatch", parameters))
    family, rank, waves = kernels[3]
    if len(family) != 285 or waves != [2, 8, 10, 24, 26, 5]:
        raise AssertionError("control greatest-family mismatch")

    named_orientations = {
        "u_to_x": active_rows(adjacency, family, U, X),
        "x_to_u": active_rows(adjacency, family, X, U),
        "z_to_a": active_rows(adjacency, family, Z, A),
        "a_to_z": active_rows(adjacency, family, A, Z),
    }
    truth = {
        name: {row["successor_retained"] for row in rows}
        for name, rows in named_orientations.items()
    }
    if truth != {
        "u_to_x": {True},
        "x_to_u": {False},
        "z_to_a": {True},
        "a_to_z": {False},
    }:
        raise AssertionError(("C-108 uniform activity mismatch", truth))

    common = [
        vertex
        for vertex in range(len(adjacency))
        if vertex not in (U, X)
        and not adjacency[U] & (1 << vertex)
        and not adjacency[X] & (1 << vertex)
    ]
    if common != [W]:
        raise AssertionError("selected pair does not have the named unique witness")
    link, components = complement_link(adjacency, W)
    if components != [[U, A], [X, Z]]:
        raise AssertionError(("wrong physical link components", components))
    if {vertex: sorted(neighbors) for vertex, neighbors in link.items()} != {
        U: [A],
        X: [Z],
        A: [U],
        Z: [X],
    }:
        raise AssertionError("link is not the claimed 2K2")

    S = mask([U, W, A])
    T = mask([X, W, Z])
    D = mask([X, W, A])
    R_state = mask([U, X, W])
    P_state = mask([A, Z, W])
    O = mask([U, W, Z])
    if not all(state in family for state in (S, T, D, R_state, P_state)):
        raise AssertionError("one of the five repair states is not retained")
    if O in family or rank.get(O) != 3:
        raise AssertionError("repair omitted corner does not have rank three")
    if O != (T ^ (1 << X)) | (1 << U):
        raise AssertionError("first literal corner identity fails")
    if O != (S ^ (1 << A)) | (1 << Z):
        raise AssertionError("second literal corner identity fails")

    endpoint = mask([X, P, Q])
    reverse = mask([U, P, Q])
    if not independent(adjacency, endpoint) or endpoint not in family:
        raise AssertionError("rank-one endpoint is not a retained independent triple")
    if rank.get(reverse) != 1 or not dominates(adjacency, reverse):
        raise AssertionError("canonical reverse is not dominating rank one")
    if (endpoint & ~T).bit_count() != 2 or abs(rank[reverse] - rank[O]) != 2:
        raise AssertionError("C-146 bound is not attained sharply")

    dominating_pairs = [
        sorted(vertices(state))
        for state in masks_of_weight(len(adjacency), 2)
        if dominates(adjacency, state)
    ]
    if len(dominating_pairs) != 23 or [U, X] in dominating_pairs:
        raise AssertionError("global gamma-two boundary mismatch")

    obligations = 0
    response_histogram = Counter()
    all_vertices = (1 << len(adjacency)) - 1
    for state in family:
        for target in vertices(all_vertices ^ state):
            movers = []
            for guard in vertices(state & adjacency[target]):
                successor = (state ^ (1 << guard)) | (1 << target)
                if successor in family:
                    movers.append(guard)
            if not movers:
                raise AssertionError("literal one-guard closure failure")
            obligations += 1
            response_histogram[len(movers)] += 1

    return {
        "graph6": CONTROL_G6,
        "order": len(adjacency),
        "size": sum(row.bit_count() for row in adjacency) // 2,
        "parameters": parameters,
        "theta_coloring": list(coloring),
        "kernel_sizes_1_2_3": [len(kernels[size][0]) for size in (1, 2, 3)],
        "triple_family_size": len(family),
        "triple_wave_sizes": waves,
        "triple_rank_histogram": dict(sorted(Counter(rank.values()).items())),
        "activity_row_counts": {
            name: len(rows) for name, rows in named_orientations.items()
        },
        "link_components": components,
        "five_repair_states_retained": True,
        "shared_corner": sorted(vertices(O)),
        "shared_corner_rank": rank[O],
        "canonical_reverse_rank": rank[reverse],
        "rank_difference": abs(rank[reverse] - rank[O]),
        "dominating_pair_count": len(dominating_pairs),
        "dominating_pairs_sha256": hashlib.sha256(
            json.dumps(dominating_pairs, separators=(",", ":")).encode()
        ).hexdigest(),
        "one_guard_obligations": obligations,
        "retained_mover_count_histogram": dict(sorted(response_histogram.items())),
    }


def line_graph_k33_complement():
    """Construct G = complement of the line graph of K_3,3."""
    edges = [(left, right) for left in range(3) for right in range(3)]
    order = len(edges)
    line = [0] * order
    for first, edge_one in enumerate(edges):
        for second, edge_two in enumerate(edges):
            if first != second and (
                edge_one[0] == edge_two[0] or edge_one[1] == edge_two[1]
            ):
                line[first] |= 1 << second
    complete_without_self = [(1 << order) - 1 ^ (1 << vertex) for vertex in range(order)]
    graph = tuple(complete_without_self[v] ^ line[v] for v in range(order))
    return graph


def audit_equality_warning():
    graph = line_graph_k33_complement()
    parameters, _, _ = parameter_tuple(graph)
    expected = {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    if parameters != expected:
        raise AssertionError(("line-graph-complement parameter mismatch", parameters))
    component_shapes = []
    for pivot in range(len(graph)):
        link, components = complement_link(graph, pivot)
        degrees = sorted(len(neighbors) for neighbors in link.values())
        if sorted(map(len, components)) != [2, 2] or degrees != [1, 1, 1, 1]:
            raise AssertionError("warning graph has a link other than 2K2")
        component_shapes.append([len(component) for component in components])
    return {
        "parameters": parameters,
        "order": len(graph),
        "size": sum(row.bit_count() for row in graph) // 2,
        "all_nine_link_component_sizes": component_shapes,
    }


def bipartition(adjacency: tuple[frozenset[int], ...]):
    color: dict[int, int] = {}
    component: dict[int, int] = {}
    component_number = 0
    for root in range(len(adjacency)):
        if root in color:
            continue
        color[root] = 0
        component[root] = component_number
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for other in adjacency[vertex]:
                if other not in color:
                    color[other] = 1 - color[vertex]
                    component[other] = component_number
                    queue.append(other)
                elif color[other] == color[vertex]:
                    return None
        component_number += 1
    return color, component


def repair_saturation(adjacency, source: int, target: int):
    """Saturate (s,t) -> (neighbor(t),neighbor(s)); flag exact conflicts."""
    forced = {(source, target)}
    frontier = deque([(source, target)])
    while frontier:
        left, right = frontier.popleft()
        for left_step in adjacency[left]:
            for right_step in adjacency[right]:
                successor = (right_step, left_step)
                if (
                    successor[0] == successor[1]
                    or successor[1] in adjacency[successor[0]]
                    or (successor[1], successor[0]) in forced
                ):
                    return forced, True
                if successor not in forced:
                    forced.add(successor)
                    frontier.append(successor)
    return forced, False


def shortest_path(adjacency, source, target):
    parent = {source: None}
    queue = deque([source])
    while queue:
        vertex = queue.popleft()
        if vertex == target:
            break
        for other in adjacency[vertex]:
            if other not in parent:
                parent[other] = vertex
                queue.append(other)
    if target not in parent:
        return None
    result = []
    vertex = target
    while vertex is not None:
        result.append(vertex)
        vertex = parent[vertex]
    return list(reversed(result))


def exact_walk_endpoints(adjacency, root, length):
    reached = {root}
    for _ in range(length):
        reached = {
            neighbor
            for vertex in reached
            for neighbor in adjacency[vertex]
        }
    return reached


def audit_abstract():
    totals = Counter()
    distance_histogram = Counter()
    for order in range(2, 7):
        possible_edges = list(itertools.combinations(range(order), 2))
        for edge_mask in range(1 << len(possible_edges)):
            rows = [set() for _ in range(order)]
            for offset, (left, right) in enumerate(possible_edges):
                if edge_mask & (1 << offset):
                    rows[left].add(right)
                    rows[right].add(left)
            adjacency = tuple(frozenset(row) for row in rows)
            if any(not row for row in adjacency):
                continue
            partition = bipartition(adjacency)
            if partition is None:
                continue
            color, component = partition
            totals["isolate_free_bipartite_graphs"] += 1
            for source in range(order):
                for target in range(order):
                    if source == target or target in adjacency[source]:
                        continue
                    totals["oriented_link_nonedges"] += 1
                    forced, conflict = repair_saturation(adjacency, source, target)
                    if component[source] == component[target]:
                        totals["same_component_roots"] += 1
                        path = shortest_path(adjacency, source, target)
                        assert path is not None
                        distance = len(path) - 1
                        distance_histogram[distance] += 1
                        if distance < 2 or not conflict:
                            raise AssertionError("same-component shortest path did not close")
                    else:
                        totals["separated_roots"] += 1
                        if conflict:
                            raise AssertionError("separated root developed a false conflict")
                        source_component = [
                            vertex
                            for vertex in range(order)
                            if component[vertex] == component[source]
                        ]
                        target_component = [
                            vertex
                            for vertex in range(order)
                            if component[vertex] == component[target]
                        ]
                        for left in source_component:
                            for right in target_component:
                                if color[left] == color[source] and color[right] == color[target]:
                                    expected = (left, right)
                                elif color[left] != color[source] and color[right] != color[target]:
                                    expected = (right, left)
                                else:
                                    continue
                                totals["checkerboard_pairs"] += 1
                                if expected not in forced:
                                    raise AssertionError("checkerboard saturation missing a pair")

                        # Explicitly exercise non-simple walks through length six.
                        for length in range(7):
                            left_ends = exact_walk_endpoints(adjacency, source, length)
                            right_ends = exact_walk_endpoints(adjacency, target, length)
                            for left in left_ends:
                                for right in right_ends:
                                    expected = (left, right) if length % 2 == 0 else (right, left)
                                    totals["synchronized_walk_endpoint_pairs"] += 1
                                    if expected not in forced:
                                        raise AssertionError("non-simple synchronized walk law failed")

                        # Check the exact parity-padding step for every same-side pair.
                        for left in source_component:
                            for right in target_component:
                                if color[left] != color[source] or color[right] != color[target]:
                                    continue
                                left_distance = len(shortest_path(adjacency, source, left)) - 1
                                right_distance = len(shortest_path(adjacency, target, right)) - 1
                                common_length = max(left_distance, right_distance)
                                if (
                                    left not in exact_walk_endpoints(adjacency, source, common_length)
                                    or right not in exact_walk_endpoints(adjacency, target, common_length)
                                ):
                                    raise AssertionError("two-step parity padding failed")
                                totals["parity_padding_pairs"] += 1
    return {
        "totals": dict(sorted(totals.items())),
        "same_component_shortest_distance_histogram": dict(
            sorted(distance_histogram.items())
        ),
        "walk_lengths_checked": list(range(7)),
    }


def evaluate():
    return {
        "schema": "repair-square-holonomy-hostile-cleanroom-v1",
        "status": "PASS",
        "control": audit_control(),
        "equality_disconnected_link_warning": audit_equality_warning(),
        "abstract": audit_abstract(),
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2, sort_keys=True))
