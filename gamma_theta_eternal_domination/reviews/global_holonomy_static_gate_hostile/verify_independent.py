#!/usr/bin/env python3
"""Clean-room audit of the global-holonomy static-gate control.

This program uses only the Python standard library.  It does not import the
candidate verifier, either campaign eternal-domination evaluator, or the
candidate SAT generator.  The only external programs are pinned nauty
``labelg`` and ``geng`` binaries, used respectively for the advertised
canonical labels and an independent unlabeled cross-check.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
from collections import Counter, deque
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge_tuple(raw: object, order: int) -> tuple[tuple[int, int], ...]:
    if not isinstance(raw, list):
        raise AssertionError("edge collection is not a list")
    answer: set[tuple[int, int]] = set()
    for item in raw:
        if (
            not isinstance(item, list)
            or len(item) != 2
            or any(type(vertex) is not int for vertex in item)
        ):
            raise AssertionError("malformed edge")
        u, v = item
        if not 0 <= u < order or not 0 <= v < order or u == v:
            raise AssertionError("invalid endpoint")
        answer.add((u, v) if u < v else (v, u))
    if len(answer) != len(raw):
        raise AssertionError("duplicate edge")
    return tuple(sorted(answer))


def adjacency(order: int, edges: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    rows = [0] * order
    for u, v in edges:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return tuple(rows)


def graph6_encode(order: int, edges: tuple[tuple[int, int], ...]) -> str:
    if not 0 <= order <= 62:
        raise AssertionError("only short graph6 records are supported")
    chosen = set(edges)
    bits = [
        int((u, v) in chosen)
        for v in range(1, order)
        for u in range(v)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = 2 * value + bit
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


def graph6_decode(record: str) -> tuple[int, tuple[tuple[int, int], ...]]:
    if not record or ord(record[0]) not in range(63, 126):
        raise AssertionError("not a short graph6 record")
    order = ord(record[0]) - 63
    bit_count = order * (order - 1) // 2
    expected_payload = (bit_count + 5) // 6
    if len(record) != expected_payload + 1:
        raise AssertionError("wrong graph6 length")
    bits: list[int] = []
    for character in record[1:]:
        value = ord(character) - 63
        if not 0 <= value <= 63:
            raise AssertionError("bad graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if any(bits[bit_count:]):
        raise AssertionError("nonzero graph6 padding")
    edges = []
    cursor = 0
    for v in range(1, order):
        for u in range(v):
            if bits[cursor]:
                edges.append((u, v))
            cursor += 1
    return order, tuple(sorted(edges))


def canonical_label(labelg: Path, record: str) -> str:
    process = subprocess.run(
        [str(labelg.resolve()), "-q"],
        input=record + "\n",
        text=True,
        capture_output=True,
        check=True,
    )
    lines = process.stdout.splitlines()
    if len(lines) != 1:
        raise AssertionError("labelg returned an unexpected number of records")
    return lines[0]


def isomorphic(
    left: tuple[int, ...], right: tuple[int, ...]
) -> tuple[int, ...] | None:
    if len(left) != len(right):
        return None
    order = len(left)
    if sorted(row.bit_count() for row in left) != sorted(
        row.bit_count() for row in right
    ):
        return None
    for permutation in itertools.permutations(range(order)):
        if any(
            bool(left[u] >> v & 1)
            != bool(right[permutation[u]] >> permutation[v] & 1)
            for u, v in itertools.combinations(range(order), 2)
        ):
            continue
        return permutation
    return None


def masks(order: int, size: int):
    for chosen in itertools.combinations(range(order), size):
        mask = 0
        for vertex in chosen:
            mask |= 1 << vertex
        yield mask


def independent(rows: tuple[int, ...], chosen: int) -> bool:
    residual = chosen
    while residual:
        bit = residual & -residual
        vertex = bit.bit_length() - 1
        residual ^= bit
        if rows[vertex] & residual:
            return False
    return True


def dominating(rows: tuple[int, ...], chosen: int) -> bool:
    covered = chosen
    residual = chosen
    while residual:
        bit = residual & -residual
        residual ^= bit
        covered |= rows[bit.bit_length() - 1]
    return covered == (1 << len(rows)) - 1


def minimum_size(rows: tuple[int, ...], predicate) -> int:
    for size in range(len(rows) + 1):
        if any(predicate(rows, chosen) for chosen in masks(len(rows), size)):
            return size
    raise AssertionError("no feasible subset")


def maximum_independent(rows: tuple[int, ...]) -> int:
    for size in range(len(rows), -1, -1):
        if any(independent(rows, chosen) for chosen in masks(len(rows), size)):
            return size
    raise AssertionError("no independent set")


def colorable(rows: tuple[int, ...], limit: int) -> bool:
    order = len(rows)
    colors = [-1] * order

    def extend(colored: int) -> bool:
        if colored == order:
            return True
        uncolored = [vertex for vertex in range(order) if colors[vertex] < 0]
        vertex = max(
            uncolored,
            key=lambda item: (
                len(
                    {
                        colors[neighbor]
                        for neighbor in range(order)
                        if rows[item] >> neighbor & 1 and colors[neighbor] >= 0
                    }
                ),
                rows[item].bit_count(),
                -item,
            ),
        )
        forbidden = {
            colors[neighbor]
            for neighbor in range(order)
            if rows[vertex] >> neighbor & 1 and colors[neighbor] >= 0
        }
        for color in range(limit):
            if color in forbidden:
                continue
            colors[vertex] = color
            if extend(colored + 1):
                return True
            colors[vertex] = -1
        return False

    return extend(0)


def chromatic(rows: tuple[int, ...]) -> int:
    for limit in range(1, len(rows) + 1):
        if colorable(rows, limit):
            return limit
    raise AssertionError("no coloring")


def greatest_kernel(
    rows: tuple[int, ...], guard_count: int
) -> tuple[set[int], Counter[int]]:
    """One-guard, one-edge, unoccupied-attack greatest fixed point."""

    order = len(rows)
    universe = {
        chosen
        for chosen in masks(order, guard_count)
        if dominating(rows, chosen)
    }
    active = set(universe)
    ranks: Counter[int] = Counter()
    round_number = 1
    while active:
        doomed: set[int] = set()
        for source in active:
            for attack in range(order):
                attack_bit = 1 << attack
                if source & attack_bit:
                    continue
                legal = False
                guards = source
                while guards:
                    guard_bit = guards & -guards
                    guards ^= guard_bit
                    guard = guard_bit.bit_length() - 1
                    if not rows[guard] & attack_bit:
                        continue
                    target = (source ^ guard_bit) | attack_bit
                    if target in active:
                        legal = True
                        break
                if not legal:
                    doomed.add(source)
                    break
        if not doomed:
            break
        ranks[round_number] = len(doomed)
        active.difference_update(doomed)
        round_number += 1
    return active, ranks


def clique_strategy() -> set[int]:
    answer = set()
    for first in (0, 1):
        for second in (2, 3):
            for third in (4, 5):
                answer.add(
                    (1 << first) | (1 << second) | (1 << third) | (1 << 6)
                )
    return answer


def family_is_eternal(rows: tuple[int, ...], family: set[int]) -> bool:
    if not family:
        return False
    order = len(rows)
    for source in family:
        if source.bit_count() != 4 or not dominating(rows, source):
            return False
        for attack in range(order):
            attack_bit = 1 << attack
            if source & attack_bit:
                continue
            if not any(
                rows[guard] & attack_bit
                and ((source ^ (1 << guard)) | attack_bit) in family
                for guard in range(order)
                if source >> guard & 1
            ):
                return False
    return True


def link_data(rows: tuple[int, ...], root: int) -> tuple[bool, bool, bool, list[int]]:
    vertices_mask = rows[root]
    vertices = [
        vertex for vertex in range(len(rows)) if vertices_mask >> vertex & 1
    ]
    isolate_free = all(rows[vertex] & vertices_mask for vertex in vertices)
    colors: dict[int, int] = {}
    components = 0
    bipartite = True
    for start in vertices:
        if start in colors:
            continue
        components += 1
        colors[start] = 0
        queue = [start]
        while queue:
            vertex = queue.pop()
            neighbors = rows[vertex] & vertices_mask
            while neighbors:
                bit = neighbors & -neighbors
                neighbors ^= bit
                neighbor = bit.bit_length() - 1
                if neighbor not in colors:
                    colors[neighbor] = 1 - colors[vertex]
                    queue.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    bipartite = False
    degrees = sorted((rows[vertex] & vertices_mask).bit_count() for vertex in vertices)
    return bipartite, isolate_free, components == 1, degrees


def has_k4(rows: tuple[int, ...]) -> bool:
    return any(
        all(rows[u] >> v & 1 for u, v in itertools.combinations(four, 2))
        for four in itertools.combinations(range(len(rows)), 4)
    )


def has_triangle(rows: tuple[int, ...]) -> bool:
    return any(
        all(rows[u] >> v & 1 for u, v in itertools.combinations(triple, 2))
        for triple in itertools.combinations(range(len(rows)), 3)
    )


def static_base(rows: tuple[int, ...]) -> bool:
    if has_k4(rows):
        return False
    if any(
        rows[u] & rows[v] == 0
        for u, v in itertools.combinations(range(len(rows)), 2)
    ):
        return False
    return all(
        (lambda data: data[0] and data[1])(link_data(rows, root))
        for root in range(len(rows))
    )


def link_is_cycle(rows: tuple[int, ...], root: int) -> bool:
    bipartite, _, connected, degrees = link_data(rows, root)
    return bipartite and connected and bool(degrees) and set(degrees) == {2}


def enumerate_labeled_to_six() -> tuple[dict[str, object], int]:
    expected_normalized = [0, 0, 1, 6, 100, 2055]
    direct_counts: list[int] = []
    normalized_counts: list[int] = []
    countermodel_counts: list[int] = []
    graph_counts: list[int] = []
    checked = 0
    for order in range(1, 7):
        pairs = tuple(itertools.combinations(range(order), 2))
        direct = normalized = countermodels = 0
        for graph_mask in range(1 << len(pairs)):
            edges = tuple(
                pair
                for position, pair in enumerate(pairs)
                if graph_mask >> position & 1
            )
            rows = adjacency(order, edges)
            if static_base(rows):
                direct += 1
                if has_triangle(rows):
                    normalized += 1
                if not colorable(rows, 3):
                    countermodels += 1
        total = 1 << len(pairs)
        checked += total
        graph_counts.append(total)
        direct_counts.append(direct)
        normalized_counts.append(normalized)
        countermodel_counts.append(countermodels)
    if checked != 33867:
        raise AssertionError("wrong labeled coverage total")
    if normalized_counts != expected_normalized:
        raise AssertionError("candidate triangle-normalized counts do not reproduce")
    if direct_counts != [1, 0, 1, 6, 100, 2055]:
        raise AssertionError("unexpected direct static-base counts")
    if any(countermodel_counts):
        raise AssertionError("a static countermodel exists below order seven")
    return (
        {
            "orders": list(range(1, 7)),
            "labeled_graphs": graph_counts,
            "direct_static_base_counts": direct_counts,
            "triangle_normalized_static_base_counts": normalized_counts,
            "non_three_colorable_counts": countermodel_counts,
        },
        checked,
    )


def geng_records(geng: Path, order: int) -> list[str]:
    process = subprocess.run(
        [str(geng.resolve()), "-q", str(order)],
        text=True,
        capture_output=True,
        check=True,
    )
    return process.stdout.splitlines()


def enumerate_unlabeled(geng: Path) -> dict[str, object]:
    expected_totals = [1, 2, 4, 11, 34, 156, 1044, 12346, 274668]
    totals = []
    static_countermodels: dict[str, int] = {}
    closed_link_countermodels: dict[str, int] = {}
    order_seven_records: list[str] = []
    order_seven_sizes: list[int] = []
    for order in range(1, 10):
        records = geng_records(geng, order)
        totals.append(len(records))
        if len(records) != expected_totals[order - 1]:
            raise AssertionError("unexpected geng coverage count")
        static_count = 0
        closed_count = 0
        for record in records:
            decoded_order, edges = graph6_decode(record)
            if decoded_order != order:
                raise AssertionError("geng order mismatch")
            rows = adjacency(order, edges)
            if not static_base(rows) or colorable(rows, 3):
                continue
            static_count += 1
            if order == 7:
                order_seven_records.append(record)
                order_seven_sizes.append(len(edges))
            if all(link_is_cycle(rows, root) for root in range(order)):
                closed_count += 1
        static_countermodels[str(order)] = static_count
        closed_link_countermodels[str(order)] = closed_count
    if order_seven_sizes != [12, 13, 14]:
        raise AssertionError("order-seven type/size census mismatch")
    if any(closed_link_countermodels.values()):
        raise AssertionError("closed-link countermodel found through order nine")
    return {
        "geng_unlabeled_totals": totals,
        "static_countermodels": static_countermodels,
        "closed_link_countermodels": closed_link_countermodels,
        "order_seven_records": order_seven_records,
        "order_seven_edge_counts": order_seven_sizes,
    }


def surface_audit(rows: tuple[int, ...]) -> dict[str, object]:
    order = len(rows)
    clique_masks = [
        chosen
        for chosen in range(1, 1 << order)
        if independent(
            tuple(
                ((1 << order) - 1) ^ rows[vertex] ^ (1 << vertex)
                for vertex in range(order)
            ),
            chosen,
        )
    ]
    # The expression above recognizes H-cliques as independent sets in
    # complement(H); independently also check all pair incidences directly.
    direct_cliques = [
        chosen
        for chosen in range(1, 1 << order)
        if all(
            rows[u] >> v & 1
            for u, v in itertools.combinations(
                [x for x in range(order) if chosen >> x & 1], 2
            )
        )
    ]
    if clique_masks != direct_cliques:
        raise AssertionError("two clique enumerations disagree")
    facets = [
        chosen
        for chosen in direct_cliques
        if not any(
            chosen != other and chosen & other == chosen
            for other in direct_cliques
        )
    ]
    if {chosen.bit_count() for chosen in facets} != {3} or len(facets) != 7:
        raise AssertionError("clique complex is not pure with seven triangles")
    expected = {
        sum(1 << vertex for vertex in {i, (i + 2) % 7, (i + 4) % 7})
        for i in range(7)
    }
    if set(facets) != expected:
        raise AssertionError("facet formula mismatch")
    edge_incidence: Counter[tuple[int, int]] = Counter()
    facet_vertices = []
    for facet in facets:
        vertices = tuple(vertex for vertex in range(order) if facet >> vertex & 1)
        facet_vertices.append(vertices)
        edge_incidence.update(itertools.combinations(vertices, 2))
    if sorted(edge_incidence.values()) != [1] * 7 + [2] * 7:
        raise AssertionError("bad surface edge incidence")
    boundary = sorted(edge for edge, count in edge_incidence.items() if count == 1)
    boundary_rows = adjacency(order, tuple(boundary))
    if any(row.bit_count() != 2 for row in boundary_rows):
        raise AssertionError("boundary is not 2-regular")
    reached = 1
    frontier = 1
    while frontier:
        bit = frontier & -frontier
        frontier ^= bit
        vertex = bit.bit_length() - 1
        fresh = boundary_rows[vertex] & ~reached
        reached |= fresh
        frontier |= fresh
    if reached != (1 << order) - 1:
        raise AssertionError("boundary is not connected")

    # Orientability constraints on the seven triangles.  Base-orient each
    # sorted triangle cyclically.  Across an interior edge, induced
    # directions must be opposite after optional facet flips.
    interior = [edge for edge, count in edge_incidence.items() if count == 2]

    def edge_sign(facet: tuple[int, int, int], edge: tuple[int, int]) -> int:
        a, b, c = facet
        directed = {(a, b), (b, c), (c, a)}
        return 1 if edge in directed else -1

    constraints: dict[int, list[tuple[int, int]]] = {
        index: [] for index in range(len(facet_vertices))
    }
    for edge in interior:
        incident = [
            index
            for index, facet in enumerate(facet_vertices)
            if set(edge).issubset(facet)
        ]
        if len(incident) != 2:
            raise AssertionError("interior edge does not have two facets")
        first, second = incident
        same_direction = (
            edge_sign(facet_vertices[first], edge)
            == edge_sign(facet_vertices[second], edge)
        )
        required_xor = int(same_direction)
        constraints[first].append((second, required_xor))
        constraints[second].append((first, required_xor))
    flips: dict[int, int] = {}
    orientable = True
    for seed in constraints:
        if seed in flips:
            continue
        flips[seed] = 0
        queue = deque([seed])
        while queue:
            current = queue.popleft()
            for neighbor, parity in constraints[current]:
                wanted = flips[current] ^ parity
                if neighbor not in flips:
                    flips[neighbor] = wanted
                    queue.append(neighbor)
                elif flips[neighbor] != wanted:
                    orientable = False
    if orientable:
        raise AssertionError("the surface should be nonorientable")
    return {
        "flag": True,
        "pure_dimension": 2,
        "f_vector": [
            order,
            sum(1 for chosen in direct_cliques if chosen.bit_count() == 2),
            len(facets),
        ],
        "euler_characteristic": order - len(edge_incidence) + len(facets),
        "facets": [list(vertices) for vertices in sorted(facet_vertices)],
        "boundary_edges": [list(edge) for edge in boundary],
        "boundary_components": 1,
        "orientable": orientable,
        "classification": "Moebius band",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--labelg", type=Path, required=True)
    parser.add_argument("--geng", type=Path, required=True)
    arguments = parser.parse_args()

    candidate = arguments.candidate.resolve()
    witness_path = candidate / "WITNESS.json"
    witness = json.loads(witness_path.read_text(encoding="utf-8"))
    if witness["schema"] != "gamma-theta-global-holonomy-static-control-v1":
        raise AssertionError("wrong candidate witness schema")

    expected_g_edges = tuple(
        sorted(
            {
                (min(vertex, (vertex + 1) % 7), max(vertex, (vertex + 1) % 7))
                for vertex in range(7)
            }
        )
    )
    all_pairs = set(itertools.combinations(range(7), 2))
    expected_h_edges = tuple(sorted(all_pairs - set(expected_g_edges)))
    g_edges = edge_tuple(witness["G"]["edges"], 7)
    h_edges = edge_tuple(witness["H"]["edges"], 7)
    if g_edges != expected_g_edges or h_edges != expected_h_edges:
        raise AssertionError("witness is not the declared labeled C7/complement pair")
    if set(g_edges).intersection(h_edges) or set(g_edges).union(h_edges) != all_pairs:
        raise AssertionError("witness graphs are not complements")

    encoding_report = {}
    for name, edges in (("G", g_edges), ("H", h_edges)):
        labeled = witness[name]["labeled_graph6"]
        canonical = witness[name]["canonical_graph6"]
        if graph6_encode(7, edges) != labeled:
            raise AssertionError(f"{name} labeled graph6 mismatch")
        if graph6_decode(labeled) != (7, edges):
            raise AssertionError(f"{name} labeled graph6 decode mismatch")
        if canonical_label(arguments.labelg, labeled) != canonical:
            raise AssertionError(f"{name} canonical labelg mismatch")
        canonical_order, canonical_edges = graph6_decode(canonical)
        if canonical_order != 7:
            raise AssertionError("canonical record has wrong order")
        witness_rows = adjacency(7, edges)
        canonical_rows = adjacency(7, canonical_edges)
        permutation = isomorphic(witness_rows, canonical_rows)
        if permutation is None:
            raise AssertionError("canonical record is not isomorphic to witness")
        encoding_report[name] = {
            "labeled_graph6": labeled,
            "canonical_graph6": canonical,
            "bruteforce_isomorphism": list(permutation),
        }

    g_rows = adjacency(7, g_edges)
    h_rows = adjacency(7, h_edges)
    if not static_base(h_rows) or colorable(h_rows, 3):
        raise AssertionError("H does not refute the proposed static implication")
    common_neighbors = {
        f"{u},{v}": [
            vertex
            for vertex in range(7)
            if h_rows[u] >> vertex & 1 and h_rows[v] >> vertex & 1
        ]
        for u, v in itertools.combinations(range(7), 2)
    }
    link_reports = {}
    for root in range(7):
        bipartite, isolate_free, connected, degrees = link_data(h_rows, root)
        if (bipartite, isolate_free, connected, degrees) != (
            True,
            True,
            True,
            [1, 1, 2, 2],
        ):
            raise AssertionError("a link is not a connected P4")
        link_reports[str(root)] = {
            "vertices": [
                vertex for vertex in range(7) if h_rows[root] >> vertex & 1
            ],
            "degrees": degrees,
        }

    gamma = minimum_size(g_rows, dominating)
    alpha = maximum_independent(g_rows)
    independent_domination = minimum_size(
        g_rows,
        lambda rows, chosen: independent(rows, chosen) and dominating(rows, chosen),
    )
    theta = chromatic(h_rows)
    kernels = {}
    eternal = None
    for guards in range(1, 8):
        surviving, rank_counts = greatest_kernel(g_rows, guards)
        kernels[str(guards)] = {
            "surviving": len(surviving),
            "deletion_round_counts": {
                str(round_number): count
                for round_number, count in sorted(rank_counts.items())
            },
        }
        if surviving and eternal is None:
            eternal = guards
    parameters = {
        "gamma": gamma,
        "independent_domination": independent_domination,
        "alpha": alpha,
        "eternal_domination": eternal,
        "theta": theta,
    }
    if parameters != {
        "gamma": 3,
        "independent_domination": 3,
        "alpha": 3,
        "eternal_domination": 4,
        "theta": 4,
    }:
        raise AssertionError("wrong exact parameter tuple")
    if kernels["3"] != {
        "surviving": 0,
        "deletion_round_counts": {"1": 7, "2": 7},
    }:
        raise AssertionError("wrong three-guard rank census")
    explicit_family = clique_strategy()
    if len(explicit_family) != 8 or not family_is_eternal(g_rows, explicit_family):
        raise AssertionError("four-guard clique family is not eternal")

    # Independently replay the accepted C-020 tree, including completeness of
    # every response branch and domination of the unique intermediate state.
    root = (1 << 0) | (1 << 2) | (1 << 4)
    if not independent(g_rows, root) or not dominating(g_rows, root):
        raise AssertionError("C-020 root is not an independent dominating triple")
    first_attack = 1
    eligible_first = {
        guard
        for guard in range(7)
        if root >> guard & 1 and g_rows[guard] >> first_attack & 1
    }
    if eligible_first != {0, 2}:
        raise AssertionError("first attack branch set is incomplete")
    first_targets = {
        guard: (root ^ (1 << guard)) | (1 << first_attack)
        for guard in eligible_first
    }
    if dominating(g_rows, first_targets[0]):
        raise AssertionError("0-to-1 branch should fail domination")
    intermediate = first_targets[2]
    if not dominating(g_rows, intermediate):
        raise AssertionError("2-to-1 branch should dominate")
    second_attack = 3
    eligible_second = {
        guard
        for guard in range(7)
        if intermediate >> guard & 1 and g_rows[guard] >> second_attack & 1
    }
    if eligible_second != {4}:
        raise AssertionError("second attack branch set is incomplete")
    terminal = (intermediate ^ (1 << 4)) | (1 << second_attack)
    if dominating(g_rows, terminal):
        raise AssertionError("terminal branch should fail domination")

    topology = surface_audit(h_rows)
    if topology["f_vector"] != [7, 14, 7] or topology["euler_characteristic"] != 0:
        raise AssertionError("wrong clique-complex invariants")

    labeled_report, labeled_total = enumerate_labeled_to_six()
    unlabeled_report = enumerate_unlabeled(arguments.geng)

    # Seven of the fourteen H-edge deletions (precisely its boundary edges)
    # remain static countermodels, all in the unique 13-edge type.
    deletion_survivors = []
    deletion_labels = []
    boundary_edges = {tuple(edge) for edge in topology["boundary_edges"]}
    for deleted in h_edges:
        reduced_edges = tuple(edge for edge in h_edges if edge != deleted)
        reduced_rows = adjacency(7, reduced_edges)
        if static_base(reduced_rows) and not colorable(reduced_rows, 3):
            deletion_survivors.append(deleted)
            deletion_labels.append(
                canonical_label(arguments.labelg, graph6_encode(7, reduced_edges))
            )
    if set(deletion_survivors) != boundary_edges or len(set(deletion_labels)) != 1:
        raise AssertionError("boundary-edge deletion classification mismatch")

    manifest_path = candidate / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["scope"]["campaign_conjecture_resolved"] is not False:
        raise AssertionError("candidate inflates campaign scope")
    artifact_hashes = {}
    for relative, expected_hash in manifest["artifacts"].items():
        actual_hash = sha256(candidate / relative)
        if actual_hash != expected_hash:
            raise AssertionError(f"candidate artifact hash mismatch: {relative}")
        artifact_hashes[relative] = actual_hash

    discovery_report = {}
    for order in range(6, 11):
        data = json.loads(
            (candidate / f"discovery_n{order}.json").read_text(encoding="utf-8")
        )
        if data["order"] != order:
            raise AssertionError("discovery order mismatch")
        final = data["final"]
        if order == 6:
            if final != {"status": "UNSAT"}:
                raise AssertionError("unexpected order-six discovery status")
        else:
            if final["status"] != "WITNESS":
                raise AssertionError("missing discovery witness")
            discovery_edges = edge_tuple(final["edges"], order)
            discovery_rows = adjacency(order, discovery_edges)
            if not static_base(discovery_rows) or colorable(discovery_rows, 3):
                raise AssertionError("invalid discovery witness")
            if graph6_encode(order, discovery_edges) != final["graph6"]:
                raise AssertionError("discovery graph6 mismatch")
        discovery_report[str(order)] = {
            "status": final["status"],
            "cut_count": data["cut_count"],
        }

    output = {
        "schema": "gamma-theta-global-holonomy-static-gate-hostile-v1",
        "verdict": "UNCONDITIONAL_PASS",
        "candidate_commits": ["1b6353a0", "6e3f9436"],
        "candidate_manifest_sha256": sha256(manifest_path),
        "candidate_artifact_hashes_verified": len(artifact_hashes),
        "graph_encoding": encoding_report,
        "static_H": {
            "K4_free": not has_k4(h_rows),
            "chromatic_number": chromatic(h_rows),
            "every_pair_common_neighbor": all(common_neighbors.values()),
            "all_links_connected_P4": True,
            "link_reports": link_reports,
        },
        "parameters_G": parameters,
        "one_guard_game": {
            "attacks_only_unoccupied": True,
            "exactly_one_guard_moves_along_one_edge": True,
            "kernels": kernels,
            "explicit_four_family_size": len(explicit_family),
            "C020_attack_tree": {
                "root": [0, 2, 4],
                "attack_1": 1,
                "first_guards": sorted(eligible_first),
                "only_dominating_first_guard": 2,
                "attack_2": 3,
                "second_guards": sorted(eligible_second),
                "terminal_missed_vertex": 5,
            },
        },
        "clique_complex": topology,
        "minimality": {
            "labeled_graphs_checked": labeled_total,
            "labeled_through_order_six": labeled_report,
            "order_seven_is_minimal_for_exact_static_implication": True,
            "unlabeled_cross_check": unlabeled_report,
            "boundary_edge_deletion_survivors": [
                list(edge) for edge in deletion_survivors
            ],
            "boundary_deletions_share_one_13_edge_type": deletion_labels[0],
        },
        "discovery_scope": {
            "runs": discovery_report,
            "large_order_UNSAT_proof_claimed": False,
            "used_for_theorem_or_minimality": False,
            "CEGAR_status": "exploratory encoding manually audited; candidate n=4 truth table replayed separately",
        },
        "scope": {
            "new_counterexample_to_gamma_theta": False,
            "universal_conjecture_resolved": False,
            "C7_tuple_or_two_attack_tree_claimed_novel": False,
            "static_strengthening_refuted": True,
            "hereditary_forbidden_subcomplex_inference": False,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
